# E1-TD-03C-JF02-D3-F1 — CONNECTION-FAILURE READ-ONLY FORENSIC V0.1

## Verdict

`CONNECTION_FAILURE_ROOT_CAUSE = SUPPORTED_BUT_NOT_PROVEN`

The strongest supported explanation is not an explicit credential rejection. The D3 collector called `client.connect(...)`, that call returned without propagating a documented authentication/version exception, and the collector then spent its fixed 30-second window polling `client.isConnected()`.

Static inspection of JForex 3.6.51 / API 2.13.99 shows that `isConnected()` requires both the transport to be online and the internal session to be fully initialized. The internal `initialized` flag is set only after account/session initialization, followed by `ISystemListener.onConnect()`.

Therefore the direct observation is:

```
CLIENT_FULLY_READY_WITHIN_30_SECONDS = FALSE
```

not:

```
PROVIDER_EXPLICITLY_REJECTED_CONNECTION = TRUE
```

## Most supported candidates

- `F1-C05 JFOREX_SDK_BOOTSTRAP_OR_SESSION_INITIALIZATION_FAILURE = SUPPORTED`
- `F1-C11 COLLECTOR_IMPLEMENTATION_DEFECT_IN_CONNECTION_PHASE = SUPPORTED`
- `F1-C09 COLLECTOR_30_SECOND_CONNECTION_DEADLINE_TOO_SHORT = PLAUSIBLE`

The collector's diagnostic design is materially insufficient for this failure mode: its `ISystemListener` callbacks are empty, it records no transport-vs-initialization state, and it collapses all non-readiness at 30 seconds into `JF02_CONNECT_FAILED`.

## Rejected / weakened explanations

Explicit credential/authentication rejection is rejected for this attempt because the SDK documents `JFAuthenticationException` and static bytecode performs authentication before the later transport/session path; D3 reached the post-connect polling loop.

Permanent SDK/JNLP version incompatibility is rejected: no `JFVersionException` was propagated, and the same SDK 3.6.51 / API 2.13.99 stack previously achieved authentication and subscription in READ_A.

Local proxy/firewall interference is weakly supported only: no user proxy, proxy environment variables, or Java/JForex app-specific firewall rule was observed.

## What remains unresolved

D3-F1 cannot distinguish between:
- transport not reaching online state;
- session/account initialization not completing;
- a transient provider/service issue;
- a later DNS/TCP/TLS transport problem;
- the 30-second deadline expiring before eventual readiness.

No raw provider diagnostic survived D3, so none of these may be promoted to PROVEN.

## Scientific necessity

A further real experiment is necessary only if the JForex path is to be recovered. It should not yet request market history.

Recommended next candidate:

`E1-TD-03C-JF02-D3-F2 — CONNECTION-ONLY STATE-OBSERVABILITY CONTROL V0.1`

One login, one connect, no reconnect, no strategy, no `getTicks`, no market data. Record exact connect exception class, connect duration, `onConnect/onDisconnect`, and `isConnected` over a preregistered longer window (recommended 120 seconds).

D3-F2 is not authorized by D3-F1.
