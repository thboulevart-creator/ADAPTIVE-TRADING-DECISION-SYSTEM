from __future__ import annotations

try:
    import tools.probe_dukascopy_trading_breaks_official_page as base
except ModuleNotFoundError:  # Direct execution: python tools/<script>.py
    import probe_dukascopy_trading_breaks_official_page as base


CDP_ORIGIN = "http://localhost"
SCHEMA = "DUKASCOPY_TRADING_BREAKS_OFFICIAL_PAGE_CDP_V2"


def browser_command(browser: str, profile, port: int) -> list[str]:
    command = list(base.browser_command(browser, profile, port))
    allow_arg = f"--remote-allow-origins={CDP_ORIGIN}"
    if allow_arg not in command:
        command.insert(-1, allow_arg)
    return command


# Keep the WebSocket Origin and Chrome's allowed origin deliberately identical.
_original_connect = base.WebSocketClient.connect


@classmethod
def _connect(cls, url: str, timeout: float = 10.0):
    # base.WebSocketClient.connect already sends Origin: http://localhost.
    # This wrapper exists so V2's launch contract is explicit and testable.
    return _original_connect.__func__(cls, url, timeout)


base.SCHEMA = SCHEMA
base.browser_command = browser_command
base.WebSocketClient.connect = _connect


if __name__ == "__main__":
    raise SystemExit(base.main())
