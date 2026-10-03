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

    def expect_raw_reject(label, raw_document, raw_schema=None):
        nonlocal raw_json_attempted
        raw_json_attempted += 1
        try:
            guard.validate_governed_json(
                raw_document,
                schema_raw if raw_schema is None else raw_schema,
            )
        except guard.GovernedSchemaError:
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

    # Raw JSON breaker families preregistered separately from parsed-object mutations.
    expect_raw_reject("RAW_DUPLICATE_TOP_LEVEL", '{"x":1,"x":2}')
    expect_raw_reject("RAW_DUPLICATE_NESTED", '{"outer":{"x":1,"x":2}}')
    expect_raw_reject(
        "RAW_ESCAPED_DUPLICATE",
        '{"evaluation_authorized":true,"\u0065valuation_authorized":false}',
    )
    expect_raw_reject("RAW_NAN", '{"x":NaN}')
    expect_raw_reject("RAW_POSITIVE_INFINITY", '{"x":Infinity}')
    expect_raw_reject("RAW_NEGATIVE_INFINITY", '{"x":-Infinity}')
    duplicate_schema = (
        '{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1",'
        '"artifact_role":"A","artifact_role":"B",'
        '"root":{"kind":"null"}}'
    )
    expect_raw_reject("RAW_SCHEMA_DUPLICATE_MEMBER", 'null', duplicate_schema)

    return {
        "parsed_object_attempted": parsed_object_attempted,
        "raw_json_attempted": raw_json_attempted,
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


if __name__ == "__main__":
    result = run_sweep()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["survivor_count"] == 0 else 1)
