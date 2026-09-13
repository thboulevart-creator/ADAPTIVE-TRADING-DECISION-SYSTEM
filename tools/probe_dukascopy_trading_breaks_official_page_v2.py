from __future__ import annotations

try:
    import tools.probe_dukascopy_trading_breaks_official_page as base
except ModuleNotFoundError:  # Direct execution: python tools/<script>.py
    import probe_dukascopy_trading_breaks_official_page as base


CDP_ORIGIN = "http://localhost"
SCHEMA = "DUKASCOPY_TRADING_BREAKS_OFFICIAL_PAGE_CDP_V2"

# Capture the V1 callables before applying any V2 monkey-patch. Without this,
# browser_command() would call base.browser_command after that name had already
# been rebound to browser_command(), causing infinite recursion.
_original_browser_command = base.browser_command
_original_connect = base.WebSocketClient.connect


def browser_command(browser: str, profile, port: int) -> list[str]:
    command = list(_original_browser_command(browser, profile, port))
    allow_arg = f"--remote-allow-origins={CDP_ORIGIN}"
    if allow_arg not in command:
        command.insert(-1, allow_arg)
    return command


# Keep the WebSocket Origin and Chrome's allowed origin deliberately identical.
@classmethod
def _connect(cls, url: str, timeout: float = 10.0):
    # V1 WebSocketClient.connect already sends Origin: http://localhost.
    # Call the captured original descriptor so V2 cannot recurse through the
    # monkey-patched class attribute.
    return _original_connect.__func__(cls, url, timeout)


base.SCHEMA = SCHEMA
base.browser_command = browser_command
base.WebSocketClient.connect = _connect


if __name__ == "__main__":
    raise SystemExit(base.main())
