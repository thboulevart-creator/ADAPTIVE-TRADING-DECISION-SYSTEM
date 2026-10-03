import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"
SCHEMA_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_governed_schema_v0_1.json"
CONTRACT_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"


def load_guard():
    spec = importlib.util.spec_from_file_location("rpe01_guard_sweep", GUARD_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load RPE-01 guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_nodes(value, path=()):
    yield path, value
    if type(value) is dict:
        for key, child in value.items():
            yield from iter_nodes(child, path + (key,))
    elif type(value) is list:
        for index, child in enumerate(value):
            yield from iter_nodes(child, path + (index,))


def get_node(root, path):
    node = root
    for part in path:
        node = node[part]
    return node


def set_node(root, path, value):
    if not path:
        raise AssertionError("root replacement not used by this sweep")
    parent = get_node(root, path[:-1])
    parent[path[-1]] = value


def wrong_type(value):
    if type(value) is bool:
        return 0
    if type(value) is int:
        return float(value)
    if type(value) is str:
        return False
    if value is None:
        return "NOT_NULL"
    raise AssertionError(f"unsupported leaf type: {type(value).__name__}")


def run_sweep():
    guard = load_guard()
    schema_raw = SCHEMA_PATH.read_text(encoding="utf-8")
    baseline = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    raw_baseline = CONTRACT_PATH.read_text(encoding="utf-8")
    guard.validate_governed_json(raw_baseline, schema_raw)

    parsed_object_attempted = 0
    raw_json_attempted = 0
    survivors = []

    def expect_reject(label, mutated):
        nonlocal parsed_object_attempted
        parsed_object_attempted += 1
        try:
            guard.validate_governed_json(
                json.dumps(mutated, ensure_ascii=False),
                schema_raw,
            )
        except guard.GovernedSchemaError:
            return
        survivors.append(label)

    def expect_raw_reject(label, raw_document, expected_reason, raw_schema=None):
        nonlocal raw_json_attempted
        raw_json_attempted += 1
        try:
            guard.validate_governed_json(
                raw_document,
                schema_raw if raw_schema is None else raw_schema,
            )
        except guard.GovernedSchemaError as exc:
            if expected_reason in str(exc):
                return
            survivors.append(f"{label}:WRONG_REASON:{exc}")
            return
        survivors.append(label)

    nodes = list(iter_nodes(baseline))

    # Unknown key at every object node.
    for path, value in nodes:
        if type(value) is not dict:
            continue
        mutated = copy.deepcopy(baseline)
        target = get_node(mutated, path)
        probe = "__rpe01_unknown_key__"
        if probe in target:
            raise AssertionError("unexpected probe collision")
        target[probe] = True
        expect_reject(f"ADD_UNKNOWN:{path}", mutated)

    # Remove every required key from every object node.
    for path, value in nodes:
        if type(value) is not dict:
            continue
        for key in value:
            mutated = copy.deepcopy(baseline)
            target = get_node(mutated, path)
            del target[key]
            expect_reject(f"REMOVE_REQUIRED:{path + (key,)}", mutated)

    # Change every scalar leaf to a different JSON type.
    for path, value in nodes:
        if type(value) in (dict, list):
            continue
        mutated = copy.deepcopy(baseline)
        set_node(mutated, path, wrong_type(value))
        expect_reject(f"WRONG_TYPE:{path}", mutated)

    # Every concrete contract list is preregistered as unique and closed vocabulary.
    for path, value in nodes:
        if type(value) is not list or not value:
            continue

        if len(value) >= 2:
            mutated = copy.deepcopy(baseline)
            target = get_node(mutated, path)
            target[1] = target[0]
            expect_reject(f"DUPLICATE_LIST_MEMBER:{path}", mutated)

        mutated = copy.deepcopy(baseline)
        target = get_node(mutated, path)
        target[0] = "__RPE01_UNKNOWN_LIST_MEMBER__"
        expect_reject(f"UNKNOWN_LIST_MEMBER:{path}", mutated)

    # Exact order is normative for the real end-to-end stage pipeline.
    path = ("end_to_end_definition", "real_end_to_end_stages")
    mutated = copy.deepcopy(baseline)
    target = get_node(mutated, path)
    target[0], target[1] = target[1], target[0]
    expect_reject("ORDER_CHANGE:real_end_to_end_stages", mutated)

    # Raw JSON breaker families constructed from otherwise-valid governed artifacts.
    def replace_once(raw, old, replacement):
        if raw.count(old) != 1:
            raise AssertionError(f"expected one raw anchor: {old!r}")
        return raw.replace(old, replacement, 1)

    authority_anchor = '    "evaluation_authorized": false,'
    duplicate_authority = replace_once(
        raw_baseline,
        authority_anchor,
        authority_anchor + '\n    "evaluation_authorized": true,',
    )
    expect_raw_reject(
        "RAW_REAL_AUTHORITY_DUPLICATE",
        duplicate_authority,
        "duplicate JSON member: evaluation_authorized",
    )

    escaped_duplicate_authority = replace_once(
        raw_baseline,
        authority_anchor,
        authority_anchor + '\n    "\\u0065valuation_authorized": true,',
    )
    expect_raw_reject(
        "RAW_REAL_AUTHORITY_ESCAPED_DUPLICATE",
        escaped_duplicate_authority,
        "duplicate JSON member: evaluation_authorized",
    )

    poll_anchor = '    "poll_interval_seconds": 30,'
    duplicate_poll = replace_once(
        raw_baseline,
        poll_anchor,
        poll_anchor + '\n    "poll_interval_seconds": 31,',
    )
    expect_raw_reject(
        "RAW_REAL_NUMERIC_DUPLICATE",
        duplicate_poll,
        "duplicate JSON member: poll_interval_seconds",
    )

    expect_raw_reject(
        "RAW_REAL_NAN",
        replace_once(
            raw_baseline,
            poll_anchor,
            '    "poll_interval_seconds": NaN,',
        ),
        "non-standard JSON numeric constant forbidden: NaN",
    )

    latency_anchor = '    "detection_latency_seconds_max": 60,'
    expect_raw_reject(
        "RAW_REAL_POSITIVE_INFINITY",
        replace_once(
            raw_baseline,
            latency_anchor,
            '    "detection_latency_seconds_max": Infinity,',
        ),
        "non-standard JSON numeric constant forbidden: Infinity",
    )
    expect_raw_reject(
        "RAW_REAL_NEGATIVE_INFINITY",
        replace_once(
            raw_baseline,
            latency_anchor,
            '    "detection_latency_seconds_max": -Infinity,',
        ),
        "non-standard JSON numeric constant forbidden: -Infinity",
    )

    schema_role_anchor = (
        '  "artifact_role": "P5E_V0_1_ADOPTED_CONTRACT_CLOSED_SCHEMA",'
    )
    duplicate_schema = replace_once(
        schema_raw,
        schema_role_anchor,
        schema_role_anchor + "\n" + schema_role_anchor,
    )
    expect_raw_reject(
        "RAW_VALID_SCHEMA_DUPLICATE_MEMBER",
        raw_baseline,
        "duplicate JSON member: artifact_role",
        duplicate_schema,
    )

    mutation_checks = 0
    mutation_kills = 0
    mutation_survivors = []

    # Mutant 1: remove duplicate-member protection. The real authority duplicate
    # becomes structurally valid because N4 intentionally does not freeze its bool value.
    mutation_checks += 1
    original_strict_object = guard._strict_object
    guard._strict_object = dict
    try:
        try:
            guard.validate_governed_json(duplicate_authority, schema_raw)
        except guard.GovernedSchemaError as exc:
            mutation_survivors.append(
                f"DUPLICATE_DETECTION_MUTANT_SURVIVED:{exc}"
            )
        else:
            mutation_kills += 1
    finally:
        guard._strict_object = original_strict_object

    # Mutant 2: remove non-standard constant parser rejection. The document
    # remains fail-closed later on type, but the parser-specific breaker is killed.
    mutation_checks += 1
    original_reject_constant = guard._reject_constant
    guard._reject_constant = lambda value: float(value)
    try:
        try:
            guard.validate_governed_json(
                replace_once(
                    raw_baseline,
                    poll_anchor,
                    '    "poll_interval_seconds": NaN,',
                ),
                schema_raw,
            )
        except guard.GovernedSchemaError as exc:
            if "non-standard JSON numeric constant forbidden: NaN" not in str(exc):
                mutation_kills += 1
            else:
                mutation_survivors.append(
                    "NONSTANDARD_CONSTANT_MUTANT_SURVIVED"
                )
        else:
            mutation_kills += 1
    finally:
        guard._reject_constant = original_reject_constant

    # Mutant 3: remove deterministic depth protection. Depth 65 must then parse.
    mutation_checks += 1
    original_depth_guard = guard._enforce_max_json_depth
    guard._enforce_max_json_depth = lambda text: None
    try:
        depth_65 = ("[" * 65) + "0" + ("]" * 65)
        try:
            guard.parse_json_strict(depth_65)
        except guard.GovernedSchemaError as exc:
            mutation_survivors.append(
                f"DEPTH_GUARD_MUTANT_SURVIVED:{exc}"
            )
        else:
            mutation_kills += 1
    finally:
        guard._enforce_max_json_depth = original_depth_guard

    return {
        "parsed_object_attempted": parsed_object_attempted,
        "raw_json_attempted": raw_json_attempted,
        "mutation_kill_checks": mutation_checks,
        "mutation_kills": mutation_kills,
        "mutation_survivors": mutation_survivors,
        "attempted": parsed_object_attempted + raw_json_attempted,
        "survivors": survivors,
        "survivor_count": len(survivors),
    }


class RPE01MutationSweepTests(unittest.TestCase):
    def test_all_preregistered_contract_schema_mutations_are_rejected(self):
        result = run_sweep()
        self.assertEqual(result["parsed_object_attempted"], 433)
        self.assertEqual(result["raw_json_attempted"], 7)
        self.assertEqual(result["attempted"], 440)
        self.assertEqual(result["survivors"], [])
        self.assertEqual(result["mutation_kill_checks"], 3)
        self.assertEqual(result["mutation_kills"], 3)
        self.assertEqual(result["mutation_survivors"], [])


if __name__ == "__main__":
    result = run_sweep()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["survivor_count"] == 0 else 1)
