from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import secrets
import socket
import struct
import subprocess
import tempfile
import time
import urllib.request
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

try:
    from tools.probe_dukascopy_trading_breaks_widget import (
        detect_browser,
        epoch_ms_for_day,
        matching_rows,
        parse_rows,
        text_contexts,
    )
except ModuleNotFoundError:  # Direct execution: python tools/<script>.py
    from probe_dukascopy_trading_breaks_widget import (
        detect_browser,
        epoch_ms_for_day,
        matching_rows,
        parse_rows,
        text_contexts,
    )


SCHEMA = "DUKASCOPY_TRADING_BREAKS_OFFICIAL_PAGE_CDP_V1"
OFFICIAL_PAGE_URL = "https://www.dukascopy.com/trading-tools/widgets/calendars/trading_breaks"
WIDGET_PATH_TOKEN = "trading_breaks/index"


@dataclass
class WebSocketClient:
    sock: socket.socket
    next_id: int = 1

    @classmethod
    def connect(cls, url: str, timeout: float = 10.0) -> "WebSocketClient":
        parsed = urlparse(url)
        if parsed.scheme != "ws":
            raise RuntimeError(f"unsupported websocket scheme: {parsed.scheme}")
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 80
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query

        sock = socket.create_connection((host, port), timeout=timeout)
        key = base64.b64encode(secrets.token_bytes(16)).decode("ascii")
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}:{port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "Origin: http://localhost\r\n"
            "\r\n"
        )
        sock.sendall(request.encode("ascii"))
        response = b""
        while b"\r\n\r\n" not in response:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk
        status_line = response.split(b"\r\n", 1)[0]
        if b" 101 " not in status_line:
            sock.close()
            raise RuntimeError(
                f"websocket handshake failed: {status_line.decode('latin1', errors='replace')}"
            )
        return cls(sock=sock)

    def close(self) -> None:
        try:
            self._send_frame(b"", opcode=8)
        except Exception:
            pass
        self.sock.close()

    def _read_exact(self, size: int) -> bytes:
        data = b""
        while len(data) < size:
            chunk = self.sock.recv(size - len(data))
            if not chunk:
                raise RuntimeError("websocket closed unexpectedly")
            data += chunk
        return data

    def _send_frame(self, payload: bytes, opcode: int = 1) -> None:
        first = 0x80 | opcode
        length = len(payload)
        mask_key = secrets.token_bytes(4)
        if length < 126:
            header = bytes([first, 0x80 | length])
        elif length <= 0xFFFF:
            header = bytes([first, 0x80 | 126]) + struct.pack("!H", length)
        else:
            header = bytes([first, 0x80 | 127]) + struct.pack("!Q", length)
        masked = bytes(value ^ mask_key[index % 4] for index, value in enumerate(payload))
        self.sock.sendall(header + mask_key + masked)

    def _recv_message(self) -> str:
        fragments: list[bytes] = []
        message_opcode: int | None = None
        while True:
            first, second = self._read_exact(2)
            fin = bool(first & 0x80)
            opcode = first & 0x0F
            masked = bool(second & 0x80)
            length = second & 0x7F
            if length == 126:
                length = struct.unpack("!H", self._read_exact(2))[0]
            elif length == 127:
                length = struct.unpack("!Q", self._read_exact(8))[0]
            mask_key = self._read_exact(4) if masked else b""
            payload = self._read_exact(length) if length else b""
            if masked:
                payload = bytes(
                    value ^ mask_key[index % 4] for index, value in enumerate(payload)
                )

            if opcode == 8:
                raise RuntimeError("websocket peer closed connection")
            if opcode == 9:
                self._send_frame(payload, opcode=10)
                continue
            if opcode == 10:
                continue
            if opcode in (1, 2):
                message_opcode = opcode
                fragments = [payload]
            elif opcode == 0:
                fragments.append(payload)
            else:
                continue

            if fin and message_opcode is not None:
                data = b"".join(fragments)
                if message_opcode != 1:
                    raise RuntimeError("unexpected binary websocket message")
                return data.decode("utf-8", errors="replace")

    def command(self, method: str, params: dict | None = None, timeout: float = 20.0) -> dict:
        message_id = self.next_id
        self.next_id += 1
        payload = {"id": message_id, "method": method}
        if params is not None:
            payload["params"] = params
        self._send_frame(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
        previous_timeout = self.sock.gettimeout()
        self.sock.settimeout(timeout)
        try:
            while True:
                message = json.loads(self._recv_message())
                if message.get("id") == message_id:
                    if "error" in message:
                        raise RuntimeError(f"CDP {method} error: {message['error']}")
                    return message.get("result", {})
        finally:
            self.sock.settimeout(previous_timeout)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def choose_debug_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def browser_command(browser: str, profile: Path, port: int) -> list[str]:
    return [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--no-default-browser-check",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile}",
        OFFICIAL_PAGE_URL,
    ]


def fetch_json(url: str, timeout: float = 5.0):
    with urllib.request.urlopen(url, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_page_target(port: int, timeout: float) -> dict:
    deadline = time.monotonic() + timeout
    last_error: str | None = None
    while time.monotonic() < deadline:
        try:
            targets = fetch_json(f"http://127.0.0.1:{port}/json")
            pages = [item for item in targets if item.get("type") == "page"]
            preferred = [
                item
                for item in pages
                if "dukascopy.com" in str(item.get("url", ""))
                and item.get("webSocketDebuggerUrl")
            ]
            if preferred:
                return preferred[0]
            if pages and pages[0].get("webSocketDebuggerUrl"):
                return pages[0]
        except Exception as exc:
            last_error = f"{type(exc).__name__}:{exc}"
        time.sleep(0.25)
    raise RuntimeError(f"CDP page target unavailable: {last_error}")


def cdp_value(result: dict):
    remote = result.get("result", {})
    if "value" in remote:
        return remote["value"]
    if remote.get("type") == "undefined":
        return None
    return remote.get("description")


def eval_js(cdp: WebSocketClient, expression: str, context_id: int | None = None):
    params = {
        "expression": expression,
        "returnByValue": True,
        "awaitPromise": True,
    }
    if context_id is not None:
        params["contextId"] = context_id
    result = cdp.command("Runtime.evaluate", params)
    if result.get("exceptionDetails"):
        raise RuntimeError(f"Runtime.evaluate exception: {result['exceptionDetails']}")
    return cdp_value(result)


def widget_iframe_expression() -> str:
    return """
(() => Array.from(document.querySelectorAll('iframe'))
  .map(frame => frame.src || '')
  .find(src => src.includes('trading_breaks/index')) || null)()
""".strip()


def rewrite_widget_expression(epoch_ms: int) -> str:
    return f"""
(() => {{
  const frame = Array.from(document.querySelectorAll('iframe'))
    .find(item => (item.src || '').includes('trading_breaks/index'));
  if (!frame) return null;
  const url = new URL(frame.src);
  url.searchParams.set('currentDate', 'false');
  url.searchParams.set('date', '{epoch_ms}');
  frame.src = url.toString();
  return frame.src;
}})()
""".strip()


def walk_frames(node: dict):
    yield node.get("frame", {})
    for child in node.get("childFrames", []) or []:
        yield from walk_frames(child)


def find_widget_frame(frame_tree: dict, epoch_ms: int) -> dict | None:
    desired = f"date={epoch_ms}"
    frames = list(walk_frames(frame_tree))
    exact = [
        frame
        for frame in frames
        if WIDGET_PATH_TOKEN in str(frame.get("url", ""))
        and desired in str(frame.get("url", ""))
    ]
    if exact:
        return exact[0]
    fallback = [
        frame for frame in frames if WIDGET_PATH_TOKEN in str(frame.get("url", ""))
    ]
    return fallback[0] if fallback else None


def wait_for_widget_iframe(cdp: WebSocketClient, timeout: float) -> str:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = eval_js(cdp, widget_iframe_expression())
        if isinstance(value, str) and value:
            return value
        time.sleep(0.5)
    raise RuntimeError("official page did not expose a trading_breaks iframe")


def wait_for_frame(cdp: WebSocketClient, epoch_ms: int, timeout: float) -> dict:
    deadline = time.monotonic() + timeout
    last_frame: dict | None = None
    while time.monotonic() < deadline:
        tree = cdp.command("Page.getFrameTree").get("frameTree", {})
        frame = find_widget_frame(tree, epoch_ms)
        if frame:
            last_frame = frame
            url = str(frame.get("url", ""))
            if f"date={epoch_ms}" in url:
                return frame
        time.sleep(0.5)
    if last_frame:
        return last_frame
    raise RuntimeError("widget frame not present in CDP frame tree")


def frame_context(cdp: WebSocketClient, frame_id: str) -> int:
    result = cdp.command(
        "Page.createIsolatedWorld",
        {"frameId": frame_id, "worldName": "dukascopy-calendar-probe"},
    )
    return int(result["executionContextId"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Load Dukascopy's official Trading Breaks page in Chrome/Edge, rewrite "
            "its embedded widget to one historical date, then inspect the child "
            "frame via Chrome DevTools Protocol without navigating to freeserv directly."
        )
    )
    parser.add_argument("--date", required=True, help="Historical UTC date YYYY-MM-DD")
    parser.add_argument("--browser", default=None)
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        day = date.fromisoformat(args.date)
    except ValueError:
        print(json.dumps({"schema": SCHEMA, "verdict": "FAIL", "reason": "INVALID_DATE"}, indent=2))
        return 1
    if args.timeout_seconds <= 0:
        print(json.dumps({"schema": SCHEMA, "verdict": "FAIL", "reason": "INVALID_TIMEOUT"}, indent=2))
        return 1

    browser = detect_browser(args.browser)
    if browser is None:
        print(json.dumps({
            "schema": SCHEMA,
            "date": day.isoformat(),
            "verdict": "BLOCKED",
            "reason": "EDGE_OR_CHROME_NOT_FOUND",
        }, indent=2))
        return 2

    epoch_ms = epoch_ms_for_day(day)
    with tempfile.TemporaryDirectory(prefix="dukascopy-official-page-cdp-") as temp_name:
        temp = Path(temp_name)
        port = choose_debug_port()
        process = subprocess.Popen(
            browser_command(browser, temp / "profile", port),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        cdp: WebSocketClient | None = None
        try:
            target = wait_for_page_target(port, args.timeout_seconds)
            cdp = WebSocketClient.connect(target["webSocketDebuggerUrl"])
            cdp.command("Page.enable")
            cdp.command("Runtime.enable")

            initial_widget_url = wait_for_widget_iframe(cdp, args.timeout_seconds)
            rewritten_widget_url = eval_js(cdp, rewrite_widget_expression(epoch_ms))
            if not rewritten_widget_url:
                raise RuntimeError("unable to rewrite official widget iframe date")

            frame = wait_for_frame(cdp, epoch_ms, args.timeout_seconds)
            context_id = frame_context(cdp, str(frame["id"]))

            # Give the widget a short render window after frame navigation.
            deadline = time.monotonic() + args.timeout_seconds
            body_text = ""
            dom = ""
            while time.monotonic() < deadline:
                body_text = str(
                    eval_js(
                        cdp,
                        "document.body ? document.body.innerText : ''",
                        context_id,
                    )
                    or ""
                )
                dom = str(
                    eval_js(
                        cdp,
                        "document.documentElement ? document.documentElement.outerHTML : ''",
                        context_id,
                    )
                    or ""
                )
                if body_text.strip() or dom.strip():
                    break
                time.sleep(0.5)

            rows = parse_rows(dom)
            matches = matching_rows(rows)
            contexts = text_contexts(body_text)
            lower_text = body_text.lower()
            access_denied = (
                "http error 403" in lower_text
                or "access to" in lower_text and "denied" in lower_text
                or "accès" in lower_text and "refus" in lower_text
            )
            evidence_found = bool(matches or contexts)

            output_dir = Path(args.output_dir) if args.output_dir else None
            if output_dir:
                output_dir.mkdir(parents=True, exist_ok=True)
                (output_dir / "widget_frame_dom.html").write_text(dom, encoding="utf-8")
                (output_dir / "widget_frame_text.txt").write_text(body_text, encoding="utf-8")

            if evidence_found:
                verdict = "PASS"
                reason = "USATECH_EVIDENCE_RENDERED_INSIDE_OFFICIAL_DUKASCOPY_PAGE"
            elif access_denied:
                verdict = "BLOCKED"
                reason = "OFFICIAL_PAGE_EMBEDDED_WIDGET_RETURNED_403"
            else:
                verdict = "BLOCKED"
                reason = "OFFICIAL_PAGE_WIDGET_RENDERED_WITHOUT_USATECH_EVIDENCE"

            report = {
                "schema": SCHEMA,
                "date": day.isoformat(),
                "browser": browser,
                "official_page_url": OFFICIAL_PAGE_URL,
                "initial_widget_url": initial_widget_url,
                "rewritten_widget_url": rewritten_widget_url,
                "frame_url": frame.get("url"),
                "frame_security_origin": frame.get("securityOrigin"),
                "dom_sha256": sha256_text(dom),
                "dom_length": len(dom),
                "visible_text_length": len(body_text),
                "visible_text_sample": body_text[:1000],
                "table_row_count": len(rows),
                "matching_rows": matches,
                "text_contexts": contexts,
                "artifact_output_dir": args.output_dir,
                "verdict": verdict,
                "reason": reason,
            }
            print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
            return 0 if verdict == "PASS" else 2
        except Exception as exc:
            report = {
                "schema": SCHEMA,
                "date": day.isoformat(),
                "browser": browser,
                "official_page_url": OFFICIAL_PAGE_URL,
                "verdict": "BLOCKED",
                "reason": "CDP_OFFICIAL_PAGE_PROBE_FAILED",
                "error": f"{type(exc).__name__}:{exc}",
            }
            print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
            return 2
        finally:
            if cdp is not None:
                cdp.close()
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
