"""Fail-closed synthetic MT5 observation validator. No imports/connectors to MT5."""
from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any

from .provenance import canonical_bytes, provenance_check, source_index, time_utc
from .schema import (ATTR, MONEY_FIELDS, OBS_CLASSES, TIME_PRECISION, TIMEZONE_STATUS,
                     exact_decimal, is_sha256, validate_shape)


def _time(row: dict, errors: list[str]) -> None:
    raw = row.get("timestamp_raw")
    utc = row.get("timestamp_utc")
    tz = row.get("timezone_status")
    if row.get("time_precision") not in TIME_PRECISION:
        errors.append("INVALID_TIME_PRECISION")
    if tz not in TIMEZONE_STATUS or not isinstance(raw, str) or not raw:
        errors.append("INVALID_RAW_TIME")
        return
    if tz == "UNKNOWN":
        if utc is not None:
            errors.append("FABRICATED_UTC_FROM_UNKNOWN_TIMEZONE")
        return
    try:
        raw_dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        errors.append("INVALID_RAW_TIME")
        return
    utc_dt = time_utc(utc)
    if raw_dt.tzinfo is None or utc_dt is None or raw_dt != utc_dt:
        errors.append("TEMPORAL_IDENTITY_MISMATCH")


def _money(obj: Any, errors: list[str]) -> None:
    if isinstance(obj, float):
        errors.append("BINARY_FLOAT_FORBIDDEN")
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if key in MONEY_FIELDS and value is not None and not exact_decimal(value):
                if isinstance(value, float):
                    errors.append("BINARY_FLOAT_FORBIDDEN")
                errors.append("INVALID_DECIMAL:" + key)
            else:
                _money(value, errors)
    elif isinstance(obj, list):
        for value in obj:
            _money(value, errors)


def _attribution(row: dict, run: dict, sources: dict, errors: list[str],
                 warnings: list[str]) -> bool:
    attr = row.get("ea_attribution", row.get("attribution"))
    if not isinstance(attr, dict) or attr.get("status") not in ATTR:
        errors.append("INVALID_ATTRIBUTION")
        return False
    if attr["status"] != "EXACT":
        warnings.append("EA_ATTRIBUTION_NOT_EXACT")
        return False
    src = sources.get(row.get("source_id"), {})
    attested_ref = attr.get("binding_evidence_ref")
    if (not run or run.get("ea_isolated") is not True or
            run.get("attested_binding") is not True
            or attr.get("ea_id") != run.get("ea_id")
            or not isinstance(attested_ref, str)
            or attested_ref not in src.get("raw_refs", set())
            or src.get("raw_map", {}).get(attested_ref, {}).get("tag") != "EA_BINDING"):
        errors.append("UNPROVEN_EXACT_ATTRIBUTION")
        return False
    return True


def _ids(items: list[dict], key: str, errors: list[str], label: str) -> dict:
    out = {}
    for row in items:
        if not isinstance(row, dict):
            continue
        identifier = row.get(key)
        if not isinstance(identifier, str) or not identifier or identifier in out:
            errors.append("DUPLICATE_OR_INVALID_" + label + "_ID")
        else:
            out[identifier] = row
    return out


def validate_batch(batch: object) -> dict[str, Any]:
    """Every malformed input must yield a controlled FAIL, never an exception."""
    try:
        return _validate_batch_core(batch)
    except (TypeError, ValueError, KeyError, OverflowError, ArithmeticError,
            RecursionError) as exc:
        return {
            "overall_status": "FAIL", "structural_status": "FAIL",
            "attribution_status": "NOT_ASSESSED", "economic_status": "NOT_ASSESSED",
            "scientific_status": "NOT_ASSESSED", "trading_authority": False,
            "capital_authority": False, "real_observation_authority": False,
            "errors": ["INVALID_INPUT"], "warnings": [],
            "effective_event_count": 0,
            "trading_realized_gross_synthetic": None,
            "configuration_count": 0,
        }


def _validate_batch_core(batch: object) -> dict[str, Any]:
    """Validate only synthetic structure and admissibility; never certifies a strategy."""
    errors = validate_shape(batch)
    result: dict[str, Any] = {
        "overall_status": "FAIL",
        "structural_status": "FAIL",
        "attribution_status": "NOT_ASSESSED",
        "economic_status": "NOT_ASSESSED",
        "scientific_status": "NOT_ASSESSED",
        "trading_authority": False,
        "capital_authority": False,
        "real_observation_authority": False,
        "errors": errors,
        "warnings": [],
        "effective_event_count": 0,
        "trading_realized_gross_synthetic": None,
        "configuration_count": 0,
    }
    if errors or not isinstance(batch, dict):
        return result
    warnings: list[str] = result["warnings"]
    sources, src_errors = source_index(batch)
    errors.extend(src_errors)
    eas = _ids(batch["ea_registry"], "ea_id", errors, "EA")
    runs = _ids(batch["run_manifest"], "run_id", errors, "RUN")
    for ea in eas.values():
        if not is_sha256(ea.get("binary_sha256")):
            errors.append("INVALID_EA_BINARY_SHA256")
        config = ea.get("config_sha256")
        if config is not None and not is_sha256(config):
            errors.append("INVALID_EA_CONFIG_SHA256")
        if ea.get("ownership") not in {"THIRD_PARTY_PRIVATE", "INDEPENDENT", "SYNTHETIC"}:
            errors.append("INVALID_EA_OWNERSHIP")
    configs = set()
    for run in runs.values():
        if run.get("ea_id") not in eas or run.get("source_id") not in sources:
            errors.append("UNBOUND_RUN")
        if run.get("mode") != "SYNTHETIC":
            errors.append("REAL_RUN_FORBIDDEN")
        if run.get("position_mode") not in {"NETTING", "HEDGING", "EXCHANGE", "UNKNOWN"}:
            errors.append("INVALID_POSITION_MODE")
        if not isinstance(run.get("account_scope"), str) or not run["account_scope"]:
            errors.append("INVALID_ACCOUNT_SCOPE")
        if not isinstance(run.get("market_symbol"), str) or not run["market_symbol"]:
            errors.append("INVALID_SYMBOL")
        if not isinstance(run.get("account_currency"), str) or not run["account_currency"]:
            errors.append("INVALID_CURRENCY")
        cfg = run.get("config_sha256")
        if cfg is not None and not is_sha256(cfg):
            errors.append("INVALID_RUN_CONFIG_SHA256")
        configs.add((run.get("ea_id"), cfg))
        if run.get("equity_coverage") not in {"COMPLETE_MARKED_PATH", "FINAL_ONLY", "PARTIAL", "UNKNOWN"}:
            errors.append("INVALID_EQUITY_COVERAGE")
    result["configuration_count"] = len(configs)
    _money(batch, errors)
    _check_source_cardinality(batch, errors)
    event_ids: dict[str, bytes] = {}
    native_deals: dict[tuple, bytes] = {}
    deal_rows: list[dict] = []
    sequenced: list[int] = []
    timestamps = set()
    all_exact = True
    for row in batch["trade_events"]:
        if not isinstance(row, dict):
            continue
        run = runs.get(row.get("run_id"))
        if run is None or row.get("source_id") != run.get("source_id"):
            errors.append("EVENT_RUN_SOURCE_MISMATCH")
        errors.extend(provenance_check(row, sources))
        _time(row, errors)
        if row.get("observation_class") not in OBS_CLASSES:
            errors.append("INVALID_OBSERVATION_CLASS")
        event_id = row.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            errors.append("INVALID_EVENT_ID")
            continue
        record_bytes = canonical_bytes(row)
        previous = event_ids.get(event_id)
        if previous is not None:
            if previous != record_bytes:
                errors.append("CONFLICTING_EVENT_ID")
            continue  # identical replay, original raw list untouched
        event_ids[event_id] = record_bytes
        seq = row.get("source_seq")
        if type(seq) is not int or seq < 0:
            errors.append("INVALID_SOURCE_SEQUENCE")
        else:
            sequenced.append(seq)
        tkey = (row.get("run_id"), row.get("timestamp_raw"))
        if tkey in timestamps:
            warnings.append("SIMULTANEOUS_EVENTS_CAUSAL_ORDER_UNKNOWN")
        timestamps.add(tkey)
        if row.get("event_type") not in {"ORDER", "DEAL", "CASH_FLOW"}:
            errors.append("UNKNOWN_EVENT_TYPE")
        if row.get("event_type") == "ORDER" and (not row.get("native_order_id")
                                                or not row.get("order_state")):
            errors.append("INVALID_ORDER_EVENT")
        if row.get("event_type") == "DEAL":
            needed = ("native_deal_id", "native_order_id", "native_position_id",
                      "symbol", "side", "entry_type", "volume", "price")
            if any(row.get(k) is None for k in needed):
                errors.append("INVALID_DEAL_EVENT")
            if row.get("entry_type") not in {"IN", "OUT", "INOUT", "OUT_BY"}:
                errors.append("INVALID_DEAL_ENTRY_TYPE")
            if row.get("side") not in {"BUY", "SELL"}:
                errors.append("INVALID_DEAL_SIDE")
            if not exact_decimal(row.get("volume")) or Decimal(row["volume"]) <= 0:
                errors.append("INVALID_DEAL_VOLUME")
            if not exact_decimal(row.get("price")):
                errors.append("INVALID_DEAL_PRICE")
            elif run:
                _price_semantics(row, run, sources, errors, warnings)
            if row.get("entry_type") == "INOUT" and run and run.get("position_mode") == "HEDGING":
                errors.append("NETTING_REVERSAL_IN_HEDGING")
            native_key = (row.get("run_id"), row.get("native_deal_id"))
            if native_key in native_deals and native_deals[native_key] != record_bytes:
                errors.append("CONFLICTING_NATIVE_DEAL")
            native_deals[native_key] = record_bytes
            deal_rows.append(row)
        if row.get("event_type") == "CASH_FLOW":
            if (row.get("cash_flow_kind") not in {"DEPOSIT", "WITHDRAWAL", "ADJUSTMENT"}
                    or not exact_decimal(row.get("amount"))):
                errors.append("INVALID_NON_TRADING_CASH_FLOW")
        if not _attribution(row, run or {}, sources, errors, warnings):
            all_exact = False
    result["effective_event_count"] = len(event_ids)
    if sequenced != sorted(sequenced):
        warnings.append("EVENT_ARRIVAL_NOT_CAUSAL")
    # Deal-related PnL intentionally excludes cash-flow operations.
    fully_observed = all(row.get("observation_class") == "OBSERVED_DIRECT"
                         for row in deal_rows)
    realized = [Decimal(row["profit"]) for row in deal_rows
                if row.get("observation_class") == "OBSERVED_DIRECT"
                and exact_decimal(row.get("profit"))]
    result["trading_realized_gross_synthetic"] = (
        str(sum(realized, Decimal("0")))
        if fully_observed and len(realized) == len(deal_rows) else None
    )
    for name in ("position_snapshots", "account_snapshots"):
        _ids(batch[name], "snapshot_id", errors, name.upper())
        for row in batch[name]:
            if not isinstance(row, dict):
                continue
            run = runs.get(row.get("run_id"))
            if run is None or row.get("source_id") != run.get("source_id"):
                errors.append("SNAPSHOT_RUN_SOURCE_MISMATCH")
            errors.extend(provenance_check(row, sources))
            _time(row, errors)
            if name == "position_snapshots":
                if row.get("side") not in {"BUY", "SELL"}:
                    errors.append("INVALID_POSITION_SIDE")
                if not exact_decimal(row.get("volume")) or Decimal(row["volume"]) <= 0:
                    errors.append("INVALID_POSITION_VOLUME")
                if not _attribution(row, run or {}, sources, errors, warnings):
                    all_exact = False
    # A NETTING symbol can have one aggregate position per account at a given snapshot time.
    netting_keys: dict[tuple, str] = {}
    for row in batch["position_snapshots"]:
        run = runs.get(row.get("run_id"))
        if run and run.get("position_mode") == "NETTING":
            k = (run.get("account_scope"), row.get("timestamp_utc"), row.get("symbol"))
            other = netting_keys.setdefault(k, row.get("native_position_id"))
            if other != row.get("native_position_id"):
                errors.append("MULTIPLE_NETTING_POSITIONS_SAME_SYMBOL")
    _reconcile_bounded_deals(batch, runs, sources, deal_rows, errors)
    for row in batch["market_context_refs"]:
        run = runs.get(row.get("run_id"))
        if run is None or row.get("source_id") != run.get("source_id"):
            errors.append("CONTEXT_RUN_SOURCE_MISMATCH")
        errors.extend(provenance_check(row, sources))
        if time_utc(row.get("available_at_utc")) is None or time_utc(row.get("decision_at_utc")) is None:
            errors.append("INVALID_CONTEXT_TIME")
        elif (row.get("use_for_decision") is True and
              time_utc(row["available_at_utc"]) > time_utc(row["decision_at_utc"])):
            errors.append("LOOKAHEAD_CONTEXT_FORBIDDEN")
        if (row.get("use_for_decision") is True and run and
                row.get("market_symbol", run.get("market_symbol")) != run.get("market_symbol")):
            errors.append("UNATTESTED_SYMBOL_EQUIVALENCE")
    # A cost/FX/coverage condition is a claim-scope check, not proof of profitability.
    cost_complete = all(
        row.get("observation_class") == "OBSERVED_DIRECT" and
        all(exact_decimal(row.get(field)) for field in ("profit", "commission", "swap", "fee"))
        for row in deal_rows
    ) and all(
        sources.get(run.get("source_id"), {}).get("row", {}).get("completeness", {}).get("deals") == "COMPLETE"
        for run in runs.values()
    )
    money_scope = all(run.get("cost_conversion_status") == "COMPLETE"
                      and is_sha256(run.get("config_sha256")) for run in runs.values())
    attribution_ok = all_exact and bool(batch["trade_events"])
    economic_ready = cost_complete and money_scope and attribution_ok and bool(deal_rows)
    result["attribution_status"] = "EXACT_SYNTHETIC_ONLY" if attribution_ok else "AMBIGUOUS_OR_UNASSIGNED"
    result["economic_status"] = ("STRUCTURALLY_ELIGIBLE_SYNTHETIC_ONLY" if economic_ready
                                 else "INSUFFICIENT_FOR_ECONOMIC_CLAIM")
    if errors:
        result["overall_status"] = "FAIL"
        result["trading_realized_gross_synthetic"] = None
        result["errors"] = sorted(set(errors))
        return result
    result["structural_status"] = "STRUCTURALLY_VALID"
    claim = batch.get("requested_claim", "DESCRIPTIVE")
    if claim == "TRADING_AUTHORIZATION":
        result["overall_status"] = "BLOCKED"
        warnings.append("TRADING_AUTHORITY_NEVER_GRANTED")
    elif claim in {"EA_NET_PNL", "PORTFOLIO_NET_PNL"}:
        result["overall_status"] = "BLOCKED"
        warnings.append("ECONOMIC_CLAIM_OUTSIDE_D1" if economic_ready
                        else "UNQUALIFIED_NET_ECONOMIC_CLAIM")
    elif claim == "EXACT_DRAWDOWN":
        # A snapshot's "complete" label cannot prove a tick-complete path by itself.
        result["overall_status"] = "BLOCKED"
        warnings.append("EXACT_DRAWDOWN_NOT_OBSERVABLE")
    elif claim == "EXACT_EA_RISK":
        # Attribution and path risk require a separate qualified portfolio engine.
        result["overall_status"] = "BLOCKED"
        warnings.append("EXACT_EA_RISK_UNPROVEN")
    elif warnings or not economic_ready:
        result["overall_status"] = "PARTIAL_DESCRIPTIVE_ONLY"
    else:
        result["overall_status"] = "STRUCTURALLY_VALID"
    result["warnings"] = sorted(set(warnings))
    result["errors"] = sorted(set(errors))
    return result


def _reconcile_bounded_deals(batch: dict, runs: dict, sources: dict,
                             deal_rows: list[dict], errors: list[str]) -> None:
    """Only replay fully scoped synthetic deal history with attested initial flat state.

    No inference for real histories, incomplete streams, tied clocks or untrusted sequence.
    """
    for run_id, run in runs.items():
        if not run.get("deal_replay_qualified"):
            continue
        src = sources.get(run.get("source_id"), {}).get("row", {})
        if (run.get("opening_state") != "FLAT" or
                src.get("completeness", {}).get("deals") != "COMPLETE"):
            errors.append("REPLAY_WITHOUT_COMPLETE_INITIAL_STATE")
            continue
        deals = [row for row in deal_rows if row.get("run_id") == run_id]
        times = [time_utc(row.get("timestamp_utc")) for row in deals]
        seqs = [row.get("source_seq") for row in deals]
        if (not all(times) or len(set(times)) != len(times)
                or any(type(seq) is not int for seq in seqs) or len(set(seqs)) != len(seqs)):
            errors.append("REPLAY_CAUSAL_ORDER_UNPROVEN")
            continue
        ordered = sorted(deals, key=lambda row: row["source_seq"])
        if [time_utc(row["timestamp_utc"]) for row in ordered] != sorted(times):
            errors.append("REPLAY_TEMPORAL_ORDER_MISMATCH")
            continue
        ledger: dict[str, tuple[str, Decimal]] = {}
        for row in ordered:
            pos_id = str(row.get("native_position_id"))
            qty = Decimal(row["volume"]) if exact_decimal(row.get("volume")) else Decimal("-1")
            if qty <= 0:
                errors.append("REPLAY_INVALID_VOLUME")
                break
            side = row.get("side")
            if side not in {"BUY", "SELL"}:
                errors.append("REPLAY_INVALID_SIDE")
                break
            old_side, old_qty = ledger.get(pos_id, (side, Decimal("0")))
            entry = row.get("entry_type")
            if entry == "IN":
                if old_qty > 0 and side != old_side:
                    errors.append("REPLAY_OPPOSITE_IN_WITHOUT_REVERSAL")
                    break
                ledger[pos_id] = (side, old_qty + qty)
            elif entry in {"OUT", "OUT_BY"}:
                if old_qty < qty or side == old_side:
                    errors.append("REPLAY_OVER_CLOSE_OR_INVALID_SIDE")
                    break
                ledger[pos_id] = (old_side, old_qty - qty)
            elif entry == "INOUT" and run.get("position_mode") == "NETTING":
                if old_qty <= 0 or qty <= old_qty or side == old_side:
                    errors.append("REPLAY_INVALID_REVERSAL")
                    break
                ledger[pos_id] = (side, qty - old_qty)
            else:
                errors.append("REPLAY_UNSUPPORTED_ENTRY")
                break
        # Compare only the last snapshot of the exact position after last known deal.
        if not deals or any(issue.startswith("REPLAY_") for issue in errors):
            continue
        final_time = max(times)
        for snapshot in batch["position_snapshots"]:
            if snapshot.get("run_id") != run_id:
                continue
            snap_time = time_utc(snapshot.get("timestamp_utc"))
            if snap_time is None or snap_time < final_time:
                continue
            pos_id = str(snapshot.get("native_position_id"))
            if pos_id not in ledger:
                errors.append("SNAPSHOT_POSITION_ABSENT_FROM_REPLAY")
                continue
            side, qty = ledger[pos_id]
            if (not exact_decimal(snapshot.get("volume"))
                    or qty != Decimal(snapshot["volume"]) or side != snapshot.get("side")):
                errors.append("REPLAY_SNAPSHOT_MISMATCH")


def _check_source_cardinality(batch: dict, errors: list[str]) -> None:
    """One raw record may mint only one distinct observation. Exact reimport is safe."""
    seen: dict[tuple[str, str], tuple[str, str, bytes]] = {}
    identifiers = {
        "trade_events": "event_id",
        "position_snapshots": "snapshot_id",
        "account_snapshots": "snapshot_id",
        "market_context_refs": "context_id",
    }
    for collection, id_field in identifiers.items():
        for row in batch[collection]:
            sid, ref = row.get("source_id"), row.get("source_record_ref")
            if not isinstance(sid, str) or not isinstance(ref, str):
                errors.append("INVALID_INPUT")
                continue
            signature = (collection, str(row.get(id_field)), canonical_bytes(row))
            key = (sid, ref)
            previous = seen.setdefault(key, signature)
            if previous != signature:
                errors.append("SOURCE_RECORD_CARDINALITY_VIOLATION")


def _price_semantics(row: dict, run: dict, sources: dict,
                     errors: list[str], warnings: list[str]) -> None:
    """No global positive-price rule. Instrument bounds require a bound source."""
    amount = Decimal(row["price"])
    spec = run.get("instrument_price_spec")
    if spec is None:
        if amount < 0:
            warnings.append("PRICE_SEMANTICS_UNATTESTED")
        return
    if not isinstance(spec, dict):
        errors.append("INSTRUMENT_PRICE_SPEC_UNATTESTED")
        return
    sid, ref = spec.get("source_id"), spec.get("source_record_ref")
    source = sources.get(sid) if isinstance(sid, str) else None
    raw = source.get("raw_map", {}).get(ref) if source and isinstance(ref, str) else None
    fields = {"symbol": spec.get("symbol"), "minimum_price": spec.get("minimum_price")}
    if (sid != run.get("source_id") or not raw
            or raw.get("tag") != "INSTRUMENT_SPEC"
            or raw.get("values") != fields
            or fields["symbol"] != run.get("market_symbol")
            or not exact_decimal(fields["minimum_price"])):
        errors.append("INSTRUMENT_PRICE_SPEC_UNATTESTED")
        return
    if amount < Decimal(fields["minimum_price"]):
        errors.append("PRICE_BELOW_ATTESTED_MINIMUM")
