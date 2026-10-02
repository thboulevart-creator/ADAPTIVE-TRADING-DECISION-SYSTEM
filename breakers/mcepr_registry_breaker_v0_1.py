from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import importlib
import json
import re
import subprocess
from pathlib import Path

import pytest


CONTRACT_BLOB = "55957058f610cca9de2e20b52d2ad1335f194d16"
CONTRACT_PATH = Path("GOVERNANCE/MINIMAL-CROSS-EXPERIMENT-PROVENANCE-REGISTRY-IMPLEMENTATION-CONTRACT-V0.1.json")
CANDIDATE_MODULE = "src.mcepr_registry"

EVENT_CONTRACT = "ATDS_MCEPR_EVENT_V0_1"
RELATION_CONTRACT = "ATDS_MCEPR_RELATION_V0_1"
SEGMENT_CONTRACT = "ATDS_MCEPR_REGISTRY_SEGMENT_V0_1"
SEGMENT_SCHEMA = "ATDS_MCEPR_REGISTRY_SEGMENT_V0_1"

GIT_A = "git_blob:" + "a" * 40
GIT_B = "git_blob:" + "b" * 40
GIT_C = "git_commit:" + "c" * 40
ALLOWED_GIT = {GIT_A, GIT_B, GIT_C}

CASES = (
    ("MCEPR-IC-01", "canonical hash is invariant to input object key insertion order"),
    ("MCEPR-IC-02", "canonical JSON uses UTF-8 sort_keys separators comma/colon ensure_ascii false with no BOM"),
    ("MCEPR-IC-03", "duplicate JSON object key is rejected"),
    ("MCEPR-IC-04", "unknown structural field is rejected"),
    ("MCEPR-IC-05", "JSON number inside an identity-bearing payload is rejected"),
    ("MCEPR-IC-06", "identical event core produces identical full-length EVENT_ID"),
    ("MCEPR-IC-07", "material event-core mutation changes EVENT_ID"),
    ("MCEPR-IC-08", "EVENT_ID/content mismatch fails"),
    ("MCEPR-IC-09", "invalid occurred_at_utc fails"),
    ("MCEPR-IC-10", "partial period boundary fails"),
    ("MCEPR-IC-11", "reversed event period fails"),
    ("MCEPR-IC-12", "source_refs and evidence_refs must be lexicographically sorted and duplicate-free"),
    ("MCEPR-IC-13", "consultation_intensity outside null/I1/I2/I3 fails"),
    ("MCEPR-IC-14", "non-null consultation_intensity without evidence_refs fails"),
    ("MCEPR-IC-15", "I1 without information_accessed fails"),
    ("MCEPR-IC-16", "identical relation core produces identical full-length RELATION_ID"),
    ("MCEPR-IC-17", "material relation-core mutation changes RELATION_ID"),
    ("MCEPR-IC-18", "RELATION_ID/content mismatch fails"),
    ("MCEPR-IC-19", "relation type outside INFORMED_BY/PREREGISTERED_BY/RESERVED_FOR/CLASSIFIED_BY fails"),
    ("MCEPR-IC-20", "relation status outside DECLARED/ADJUDICATED/DISPUTED/UNKNOWN fails"),
    ("MCEPR-IC-21", "missing or syntactically invalid BASIS_REF fails"),
    ("MCEPR-IC-22", "ADJUDICATED without separately human-authorized basis is BLOCKED"),
    ("MCEPR-IC-23", "supersedes ref must resolve to an ancestor relation"),
    ("MCEPR-IC-24", "supersession must preserve source_ref relation_type and target_ref"),
    ("MCEPR-IC-25", "superseding a non-active relation fails"),
    ("MCEPR-IC-26", "same prior relation cannot have two active direct successors"),
    ("MCEPR-IC-27", "invalid typed-reference syntax fails"),
    ("MCEPR-IC-28", "unresolvable git blob or commit reference is BLOCKED"),
    ("MCEPR-IC-29", "unresolvable event/relation/registry reference is BLOCKED"),
    ("MCEPR-IC-30", "valid genesis has null parent and becomes sole initial head"),
    ("MCEPR-IC-31", "multiple genesis segments are BLOCKED"),
    ("MCEPR-IC-32", "missing parent registry segment is BLOCKED"),
    ("MCEPR-IC-33", "REGISTRY_ID/content mismatch fails"),
    ("MCEPR-IC-34", "segment filename must exactly match REGISTRY_ID"),
    ("MCEPR-IC-35", "empty segment fails"),
    ("MCEPR-IC-36", "events array must be strictly sorted by event_id and duplicate-free"),
    ("MCEPR-IC-37", "relations array must be strictly sorted by relation_id and duplicate-free"),
    ("MCEPR-IC-38", "event id already present in ancestor chain fails even if byte-equivalent"),
    ("MCEPR-IC-39", "relation id already present in ancestor chain fails even if byte-equivalent"),
    ("MCEPR-IC-40", "two children of one parent produce REGISTRY_FORK and BLOCKED"),
    ("MCEPR-IC-41", "one fully resolvable linear chain has one derived head and may PASS technical validation"),
    ("MCEPR-IC-42", "omission of an ancestor event from a child segment does not delete the ancestor event"),
    ("MCEPR-IC-43", "tampering with a persisted segment changes its content-bound registry identity and fails"),
    ("MCEPR-IC-44", "event references inside the same segment may resolve after event-id validation"),
    ("MCEPR-IC-45", "relation refs to relations created in the same segment are forbidden"),
    ("MCEPR-IC-46", "validator output cannot claim registry completeness pristine status scientific support or independence"),
    ("MCEPR-IC-47", "validator output cannot compute or assert N_budget or N_famille"),
    ("MCEPR-IC-48", "retrospective occurred_at does not imply earlier durable knowledge; chain/Git ancestry governs persistence order"),
    ("MCEPR-IC-49", "RESERVED_FOR and CLASSIFIED_BY can use a non-event SOURCE_REF such as immutable git_blob"),
    ("MCEPR-IC-50", "all four adopted relation types are representable without adding a fifth relation type"),
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _head_blob(path: Path) -> tuple[str, bytes]:
    root = _repo_root()
    rel = path.as_posix()
    sha = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", f"HEAD:{rel}"],
        text=True,
    ).strip()
    raw = subprocess.check_output(
        ["git", "-C", str(root), "show", f"HEAD:{rel}"],
    )
    return sha, raw


def _reference_canonical(value: object) -> bytes:
    def reject_numbers(v: object) -> None:
        if isinstance(v, bool) or v is None or isinstance(v, str):
            return
        if isinstance(v, (int, float)):
            raise ValueError("JSON number forbidden in identity payload")
        if isinstance(v, list):
            for item in v:
                reject_numbers(item)
            return
        if isinstance(v, dict):
            for key, item in v.items():
                if not isinstance(key, str):
                    raise ValueError("non-string JSON object key")
                reject_numbers(item)
            return
        raise ValueError(f"unsupported identity value: {type(v)!r}")

    reject_numbers(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256_hex(value: object) -> str:
    return hashlib.sha256(_reference_canonical(value)).hexdigest()


def _event_core(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "occurred_at_utc": "2026-10-02T12:00:00Z",
        "operator": "synthetic-breaker",
        "nature": "synthetic observation",
        "declared_purpose": "breaker fixture",
        "source_refs": [GIT_A],
        "asset": "SYNTHETIC",
        "period_start_utc": "2026-01-01T00:00:00Z",
        "period_end_utc": "2026-01-02T00:00:00Z",
        "consultation_intensity": None,
        "information_accessed": None,
        "evidence_refs": [],
    }
    value.update(overrides)
    return value


def _ref_event(core: dict[str, object] | None = None) -> dict[str, object]:
    core = copy.deepcopy(core if core is not None else _event_core())
    payload = {"contract": EVENT_CONTRACT, "event_core": core}
    return {"event_id": "EVT-" + _sha256_hex(payload), "event_core": core}


def _relation_core(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "source_ref": GIT_A,
        "relation_type": "INFORMED_BY",
        "target_ref": GIT_B,
        "relation_status": "DECLARED",
        "basis_ref": GIT_A,
        "supersedes_relation_ref": None,
    }
    value.update(overrides)
    return value


def _ref_relation(core: dict[str, object] | None = None) -> dict[str, object]:
    core = copy.deepcopy(core if core is not None else _relation_core())
    payload = {"contract": RELATION_CONTRACT, "relation_core": core}
    return {"relation_id": "REL-" + _sha256_hex(payload), "relation_core": core}


def _ref_segment(parent_registry_ref: str | None, events: list[dict[str, object]], relations: list[dict[str, object]]) -> dict[str, object]:
    events = sorted(copy.deepcopy(events), key=lambda item: str(item["event_id"]))
    relations = sorted(copy.deepcopy(relations), key=lambda item: str(item["relation_id"]))
    core = {"schema": SEGMENT_SCHEMA, "parent_registry_ref": parent_registry_ref, "events": events, "relations": relations}
    payload = {"contract": SEGMENT_CONTRACT, "segment_core": core}
    return {
        "schema": SEGMENT_SCHEMA,
        "registry_id": "RGS-" + _sha256_hex(payload),
        "parent_registry_ref": parent_registry_ref,
        "events": events,
        "relations": relations,
    }


def _segment_file(segment: dict[str, object]) -> tuple[str, bytes]:
    name = str(segment["registry_id"]) + ".json"
    raw = json.dumps(segment, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return name, raw


def _files(*segments: dict[str, object]) -> dict[str, bytes]:
    return dict(_segment_file(segment) for segment in segments)


def _resolver(ref: str) -> bool:
    return ref in ALLOWED_GIT


def _candidate():
    try:
        module = importlib.import_module(CANDIDATE_MODULE)
    except ModuleNotFoundError as exc:
        if exc.name == CANDIDATE_MODULE:
            pytest.fail(
                "MCEPR candidate absent — expected pre-implementation RED: src.mcepr_registry does not exist",
                pytrace=False,
            )
        raise
    required = (
        "MCEPRFail",
        "MCEPRBlocked",
        "parse_json_strict",
        "canonical_bytes",
        "make_event",
        "make_relation",
        "make_segment",
        "validate_registry_files",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        pytest.fail(f"MCEPR candidate surface incomplete: {missing}", pytrace=False)
    return module


def _expect_fail(mod, fn) -> None:
    with pytest.raises(mod.MCEPRFail):
        fn()


def _expect_blocked(mod, fn) -> None:
    with pytest.raises(mod.MCEPRBlocked):
        fn()


def _validate(mod, segments: dict[str, bytes], *, allowlist: set[str] | None = None):
    return mod.validate_registry_files(
        segments,
        git_resolver=_resolver,
        adjudication_basis_allowlist=set() if allowlist is None else allowlist,
    )


def _case_01(mod) -> None:
    assert mod.canonical_bytes({"z": "last", "a": "first"}) == mod.canonical_bytes({"a": "first", "z": "last"})


def _case_02(mod) -> None:
    value = {"é": "✓", "a": "b"}
    expected = '{"a":"b","é":"✓"}'.encode("utf-8")
    assert mod.canonical_bytes(value) == expected
    assert not mod.canonical_bytes(value).startswith(b"\xef\xbb\xbf")


def _case_03(mod) -> None:
    _expect_fail(mod, lambda: mod.parse_json_strict(b'{"a":"x","a":"y"}'))


def _case_04(mod) -> None:
    core = _event_core()
    core["unexpected"] = "x"
    _expect_fail(mod, lambda: mod.make_event(core))


def _case_05(mod) -> None:
    _expect_fail(mod, lambda: mod.canonical_bytes({"number": 1}))


def _case_06(mod) -> None:
    a = mod.make_event(_event_core())
    b = mod.make_event(_event_core())
    assert a == b
    assert re.fullmatch(r"EVT-[0-9a-f]{64}", a["event_id"])


def _case_07(mod) -> None:
    assert mod.make_event(_event_core())["event_id"] != mod.make_event(_event_core(declared_purpose="different"))["event_id"]


def _case_08(mod) -> None:
    event = _ref_event()
    event["event_core"]["declared_purpose"] = "tampered"
    seg = _ref_segment(None, [event], [])
    _expect_fail(mod, lambda: _validate(mod, _files(seg)))


def _case_09(mod) -> None:
    _expect_fail(mod, lambda: mod.make_event(_event_core(occurred_at_utc="2026-10-02 12:00:00")))


def _case_10(mod) -> None:
    _expect_fail(mod, lambda: mod.make_event(_event_core(period_end_utc=None)))


def _case_11(mod) -> None:
    _expect_fail(mod, lambda: mod.make_event(_event_core(period_start_utc="2026-01-03T00:00:00Z", period_end_utc="2026-01-02T00:00:00Z")))


def _case_12(mod) -> None:
    _expect_fail(mod, lambda: mod.make_event(_event_core(source_refs=[GIT_B, GIT_A])))
    _expect_fail(mod, lambda: mod.make_event(_event_core(source_refs=[GIT_A, GIT_A])))
    _expect_fail(mod, lambda: mod.make_event(_event_core(evidence_refs=[GIT_B, GIT_A])))


def _case_13(mod) -> None:
    _expect_fail(mod, lambda: mod.make_event(_event_core(consultation_intensity="I4", evidence_refs=[GIT_A])))


def _case_14(mod) -> None:
    _expect_fail(mod, lambda: mod.make_event(_event_core(consultation_intensity="I2", evidence_refs=[])))


def _case_15(mod) -> None:
    _expect_fail(mod, lambda: mod.make_event(_event_core(consultation_intensity="I1", information_accessed=None, evidence_refs=[GIT_A])))


def _case_16(mod) -> None:
    a = mod.make_relation(_relation_core())
    b = mod.make_relation(_relation_core())
    assert a == b
    assert re.fullmatch(r"REL-[0-9a-f]{64}", a["relation_id"])


def _case_17(mod) -> None:
    assert mod.make_relation(_relation_core())["relation_id"] != mod.make_relation(_relation_core(relation_status="DISPUTED"))["relation_id"]


def _case_18(mod) -> None:
    relation = _ref_relation()
    relation["relation_core"]["relation_status"] = "DISPUTED"
    seg = _ref_segment(None, [], [relation])
    _expect_fail(mod, lambda: _validate(mod, _files(seg)))


def _case_19(mod) -> None:
    _expect_fail(mod, lambda: mod.make_relation(_relation_core(relation_type="CAUSES")))


def _case_20(mod) -> None:
    _expect_fail(mod, lambda: mod.make_relation(_relation_core(relation_status="TRUE")))


def _case_21(mod) -> None:
    _expect_fail(mod, lambda: mod.make_relation(_relation_core(basis_ref=None)))
    _expect_fail(mod, lambda: mod.make_relation(_relation_core(basis_ref="some/file.md")))


def _case_22(mod) -> None:
    rel = _ref_relation(_relation_core(relation_status="ADJUDICATED", basis_ref=GIT_A))
    seg = _ref_segment(None, [], [rel])
    _expect_blocked(mod, lambda: _validate(mod, _files(seg), allowlist=set()))


def _case_23(mod) -> None:
    missing = "relation:REL-" + "9" * 64
    successor = _ref_relation(_relation_core(relation_status="DISPUTED", supersedes_relation_ref=missing))
    seg = _ref_segment(None, [], [successor])
    _expect_fail(mod, lambda: _validate(mod, _files(seg)))


def _case_24(mod) -> None:
    original = _ref_relation()
    genesis = _ref_segment(None, [], [original])
    successor = _ref_relation(_relation_core(source_ref=GIT_B, relation_status="DISPUTED", supersedes_relation_ref="relation:" + str(original["relation_id"])))
    child = _ref_segment("registry:" + str(genesis["registry_id"]), [], [successor])
    _expect_fail(mod, lambda: _validate(mod, _files(genesis, child)))


def _case_25(mod) -> None:
    r1 = _ref_relation()
    genesis = _ref_segment(None, [], [r1])
    r2 = _ref_relation(_relation_core(relation_status="DISPUTED", supersedes_relation_ref="relation:" + str(r1["relation_id"])))
    s2 = _ref_segment("registry:" + str(genesis["registry_id"]), [], [r2])
    r3 = _ref_relation(_relation_core(relation_status="UNKNOWN", supersedes_relation_ref="relation:" + str(r1["relation_id"])))
    s3 = _ref_segment("registry:" + str(s2["registry_id"]), [], [r3])
    _expect_fail(mod, lambda: _validate(mod, _files(genesis, s2, s3)))


def _case_26(mod) -> None:
    r1 = _ref_relation()
    genesis = _ref_segment(None, [], [r1])
    r2 = _ref_relation(_relation_core(relation_status="DISPUTED", supersedes_relation_ref="relation:" + str(r1["relation_id"])))
    r3 = _ref_relation(_relation_core(relation_status="UNKNOWN", supersedes_relation_ref="relation:" + str(r1["relation_id"])))
    child = _ref_segment("registry:" + str(genesis["registry_id"]), [], [r2, r3])
    _expect_fail(mod, lambda: _validate(mod, _files(genesis, child)))


def _case_27(mod) -> None:
    _expect_fail(mod, lambda: mod.make_relation(_relation_core(target_ref="git_blob:XYZ")))
    _expect_fail(mod, lambda: mod.make_relation(_relation_core(target_ref="latest")))


def _case_28(mod) -> None:
    unknown = "git_blob:" + "d" * 40
    rel = _ref_relation(_relation_core(target_ref=unknown))
    seg = _ref_segment(None, [], [rel])
    _expect_blocked(mod, lambda: _validate(mod, _files(seg)))


def _case_29(mod) -> None:
    unknown = "event:EVT-" + "e" * 64
    rel = _ref_relation(_relation_core(target_ref=unknown))
    seg = _ref_segment(None, [], [rel])
    _expect_blocked(mod, lambda: _validate(mod, _files(seg)))


def _case_30(mod) -> None:
    genesis = _ref_segment(None, [_ref_event()], [])
    result = _validate(mod, _files(genesis))
    assert result["status"] == "PASS"
    assert result["head_ref"] == "registry:" + str(genesis["registry_id"])


def _case_31(mod) -> None:
    a = _ref_segment(None, [_ref_event(_event_core(declared_purpose="a"))], [])
    b = _ref_segment(None, [_ref_event(_event_core(declared_purpose="b"))], [])
    _expect_blocked(mod, lambda: _validate(mod, _files(a, b)))


def _case_32(mod) -> None:
    child = _ref_segment("registry:RGS-" + "1" * 64, [_ref_event()], [])
    _expect_blocked(mod, lambda: _validate(mod, _files(child)))


def _case_33(mod) -> None:
    seg = _ref_segment(None, [_ref_event()], [])
    seg["registry_id"] = "RGS-" + "2" * 64
    filename = str(seg["registry_id"]) + ".json"
    raw = json.dumps(seg, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    _expect_fail(mod, lambda: _validate(mod, {filename: raw}))


def _case_34(mod) -> None:
    seg = _ref_segment(None, [_ref_event()], [])
    _, raw = _segment_file(seg)
    _expect_fail(mod, lambda: _validate(mod, {"wrong-name.json": raw}))


def _case_35(mod) -> None:
    _expect_fail(mod, lambda: mod.make_segment(None, [], []))


def _case_36(mod) -> None:
    a = _ref_event(_event_core(declared_purpose="a"))
    b = _ref_event(_event_core(declared_purpose="b"))
    events = sorted([a, b], key=lambda item: str(item["event_id"]), reverse=True)
    core = {"schema": SEGMENT_SCHEMA, "parent_registry_ref": None, "events": events, "relations": []}
    seg = {"schema": SEGMENT_SCHEMA, "registry_id": "RGS-" + _sha256_hex({"contract": SEGMENT_CONTRACT, "segment_core": core}), "parent_registry_ref": None, "events": events, "relations": []}
    _expect_fail(mod, lambda: _validate(mod, _files(seg)))


def _case_37(mod) -> None:
    a = _ref_relation(_relation_core(relation_status="DECLARED"))
    b = _ref_relation(_relation_core(relation_status="UNKNOWN"))
    relations = sorted([a, b], key=lambda item: str(item["relation_id"]), reverse=True)
    core = {"schema": SEGMENT_SCHEMA, "parent_registry_ref": None, "events": [], "relations": relations}
    seg = {"schema": SEGMENT_SCHEMA, "registry_id": "RGS-" + _sha256_hex({"contract": SEGMENT_CONTRACT, "segment_core": core}), "parent_registry_ref": None, "events": [], "relations": relations}
    _expect_fail(mod, lambda: _validate(mod, _files(seg)))


def _case_38(mod) -> None:
    event = _ref_event()
    genesis = _ref_segment(None, [event], [])
    child = _ref_segment("registry:" + str(genesis["registry_id"]), [event], [])
    _expect_fail(mod, lambda: _validate(mod, _files(genesis, child)))


def _case_39(mod) -> None:
    rel = _ref_relation()
    genesis = _ref_segment(None, [], [rel])
    child = _ref_segment("registry:" + str(genesis["registry_id"]), [], [rel])
    _expect_fail(mod, lambda: _validate(mod, _files(genesis, child)))


def _case_40(mod) -> None:
    genesis = _ref_segment(None, [_ref_event()], [])
    parent = "registry:" + str(genesis["registry_id"])
    a = _ref_segment(parent, [_ref_event(_event_core(declared_purpose="a"))], [])
    b = _ref_segment(parent, [_ref_event(_event_core(declared_purpose="b"))], [])
    _expect_blocked(mod, lambda: _validate(mod, _files(genesis, a, b)))


def _case_41(mod) -> None:
    genesis = _ref_segment(None, [_ref_event(_event_core(declared_purpose="g"))], [])
    child = _ref_segment("registry:" + str(genesis["registry_id"]), [_ref_event(_event_core(declared_purpose="c"))], [])
    result = _validate(mod, _files(genesis, child))
    assert result["status"] == "PASS"
    assert result["head_ref"] == "registry:" + str(child["registry_id"])


def _case_42(mod) -> None:
    event = _ref_event()
    genesis = _ref_segment(None, [event], [])
    child = _ref_segment("registry:" + str(genesis["registry_id"]), [_ref_event(_event_core(declared_purpose="new"))], [])
    result = _validate(mod, _files(genesis, child))
    assert str(event["event_id"]) in set(result.get("event_ids", ()))


def _case_43(mod) -> None:
    event = _ref_event()
    seg = _ref_segment(None, [event], [])
    seg["events"][0]["event_core"]["nature"] = "tampered"
    _, raw = _segment_file(seg)
    _expect_fail(mod, lambda: _validate(mod, {str(seg["registry_id"]) + ".json": raw}))


def _case_44(mod) -> None:
    event = _ref_event()
    rel = _ref_relation(_relation_core(source_ref="event:" + str(event["event_id"]), target_ref=GIT_B, basis_ref=GIT_A))
    seg = _ref_segment(None, [event], [rel])
    assert _validate(mod, _files(seg))["status"] == "PASS"


def _case_45(mod) -> None:
    first = _ref_relation()
    second = _ref_relation(_relation_core(source_ref="relation:" + str(first["relation_id"]), relation_type="CLASSIFIED_BY"))
    seg = _ref_segment(None, [], [first, second])
    _expect_fail(mod, lambda: _validate(mod, _files(seg)))


def _case_46(mod) -> None:
    result = _validate(mod, _files(_ref_segment(None, [_ref_event()], [])))
    text = json.dumps(result, sort_keys=True).upper()
    assert all(token not in text for token in ("REGISTRY_COMPLETE", "PRISTINE", "SCIENTIFIC_SUPPORT", "SCIENTIFIC_INDEPENDENCE"))


def _case_47(mod) -> None:
    result = _validate(mod, _files(_ref_segment(None, [_ref_event()], [])))
    text = json.dumps(result, sort_keys=True).lower()
    assert "n_budget" not in text
    assert "n_famille" not in text


def _case_48(mod) -> None:
    old = _ref_event(_event_core(occurred_at_utc="2020-01-01T00:00:00Z"))
    result = _validate(mod, _files(_ref_segment(None, [old], [])))
    assert result["status"] == "PASS"
    assert result.get("persisted_at_utc") != "2020-01-01T00:00:00Z"


def _case_49(mod) -> None:
    reserved = _ref_relation(_relation_core(source_ref=GIT_A, relation_type="RESERVED_FOR", target_ref=GIT_B))
    classified = _ref_relation(_relation_core(source_ref=GIT_B, relation_type="CLASSIFIED_BY", target_ref=GIT_A))
    assert _validate(mod, _files(_ref_segment(None, [], [reserved, classified])))["status"] == "PASS"


def _case_50(mod) -> None:
    event = _ref_event()
    event_ref = "event:" + str(event["event_id"])
    relations = [
        _ref_relation(_relation_core(source_ref=event_ref, relation_type="INFORMED_BY", target_ref=GIT_B)),
        _ref_relation(_relation_core(source_ref=event_ref, relation_type="PREREGISTERED_BY", target_ref=GIT_C)),
        _ref_relation(_relation_core(source_ref=GIT_A, relation_type="RESERVED_FOR", target_ref=GIT_B)),
        _ref_relation(_relation_core(source_ref=event_ref, relation_type="CLASSIFIED_BY", target_ref=GIT_A)),
    ]
    assert _validate(mod, _files(_ref_segment(None, [event], relations)))["status"] == "PASS"


CASE_HANDLERS = {f"MCEPR-IC-{index:02d}": globals()[f"_case_{index:02d}"] for index in range(1, 51)}


@pytest.mark.parametrize(("case_id", "description"), CASES, ids=[item[0] for item in CASES])
def test_preregistered_case(case_id: str, description: str) -> None:
    del description
    mod = _candidate()
    CASE_HANDLERS[case_id](mod)


def _self_check(expect_absent: bool) -> dict[str, object]:
    root = _repo_root()
    observed_blob, raw = _head_blob(CONTRACT_PATH)
    if observed_blob != CONTRACT_BLOB:
        raise SystemExit(f"contract blob mismatch: {observed_blob} != {CONTRACT_BLOB}")
    contract = json.loads(raw.decode("utf-8"))
    contract_cases = tuple(tuple(item) for item in contract["future_breaker_specification"]["test_cases"])
    if contract_cases != CASES:
        raise SystemExit("embedded breaker cases differ from frozen implementation contract")
    if set(CASE_HANDLERS) != {item[0] for item in CASES}:
        raise SystemExit("breaker handler set does not exactly match 50 preregistered IDs")
    if len(CASES) != 50:
        raise SystemExit(f"unexpected test count: {len(CASES)}")
    if contract["future_breaker_specification"]["breaker_candidate_path"] != "breakers/mcepr_registry_breaker_v0_1.py":
        raise SystemExit("breaker path mismatch")
    if contract["future_breaker_specification"]["breaker_implementation_status"] != "NOT_AUTHORIZED":
        raise SystemExit("frozen contract authority mismatch")
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(Path(__file__)))
    forbidden_prefixes = ("src.decision", "src.memory", "src.research", "tools.sfe")
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imported_modules.append(node.module)
    if any(module.startswith(forbidden_prefixes) for module in imported_modules):
        raise SystemExit("breaker imports a forbidden existing runtime surface")
    candidate_path = root / "src" / "mcepr_registry.py"
    absent = not candidate_path.exists()
    if expect_absent and not absent:
        raise SystemExit("expected absent candidate implementation, but src/mcepr_registry.py exists")
    return {
        "status": "PASS",
        "contract_blob": observed_blob,
        "test_case_count": len(CASES),
        "handler_count": len(CASE_HANDLERS),
        "candidate_module": CANDIDATE_MODULE,
        "candidate_file_absent": absent,
        "existing_runtime_surface_imports": "NONE",
        "fixtures": "INLINE_SYNTHETIC_ONLY",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--expect-absent", action="store_true")
    args = parser.parse_args()
    if not args.self_check:
        parser.error("only --self-check is supported outside pytest")
    print(json.dumps(_self_check(args.expect_absent), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
