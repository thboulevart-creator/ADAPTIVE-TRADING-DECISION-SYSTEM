import ast
import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"
P5E_SCHEMA_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_governed_schema_v0_1.json"
P5E_CONTRACT_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
P5E_ADV_PATH = ROOT / "tests" / "obsidian_projection" / "test_p5e_end_to_end_near_real_time_adversarial_v0_1.py"


def load_module(path: Path, name: str):
    if not path.exists():
        raise AssertionError(f"required implementation missing: {path}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_guard():
    return load_module(GUARD_PATH, "rpe01_guard_under_test")


def load_schema():
    if not P5E_SCHEMA_PATH.exists():
        raise AssertionError(f"required governed schema missing: {P5E_SCHEMA_PATH}")
    return json.loads(P5E_SCHEMA_PATH.read_text(encoding="utf-8"))


def current_contract_raw() -> str:
    return P5E_CONTRACT_PATH.read_text(encoding="utf-8")


def synthetic_schema():
    return {
        "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
        "artifact_role": "RPE01_SYNTHETIC_ADJACENT_CONFIG",
        "root": {
            "kind": "object",
            "fields": {
                "interval_ns": {
                    "kind": "integer",
                    "minimum": 1,
                    "maximum": 60_000_000_000,
                },
                "enabled": {"kind": "boolean", "const": False},
                "mode": {
                    "kind": "string",
                    "enum": ["FIXED_RATE", "DISABLED"],
                },
                "stages": {
                    "kind": "array",
                    "items": {"kind": "string"},
                    "min_items": 2,
                    "max_items": 2,
                    "unique": True,
                    "ordered_const": ["OBSERVE", "STOP"],
                },
            },
        },
    }


class ExistingGapEvidenceTests(unittest.TestCase):
    def test_existing_p5e_invariants_do_not_close_unknown_keys(self):
        adv = load_module(P5E_ADV_PATH, "rpe01_gap_adv")
        contract = json.loads(current_contract_raw())
        mutated = copy.deepcopy(contract)
        mutated["authority_boundary"]["rpe01_probe_unknown_authority"] = True
        # This PASS demonstrates the pre-RPE01 structural gap.
        adv.assert_contract_invariants(mutated)


class StrictRawJsonTests(unittest.TestCase):
    def test_duplicate_authority_member_is_rejected_before_dict_construction(self):
        g = load_guard()
        raw = '{"evaluation_authorized":true,"evaluation_authorized":false}'
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_json_strict(raw)

    def test_duplicate_nested_member_is_rejected(self):
        g = load_guard()
        raw = '{"outer":{"x":1,"x":2}}'
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_json_strict(raw)

    def test_nan_and_infinities_are_rejected(self):
        g = load_guard()
        for raw in ('{"x":NaN}', '{"x":Infinity}', '{"x":-Infinity}'):
            with self.subTest(raw=raw):
                with self.assertRaises(g.GovernedSchemaError):
                    g.parse_json_strict(raw)


class SchemaDefinitionTests(unittest.TestCase):
    def test_schema_definition_rejects_unknown_schema_language_key(self):
        g = load_guard()
        schema = synthetic_schema()
        schema["root"]["surprise"] = True
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_schema_definition(schema)

    def test_schema_definition_rejects_wrong_constraint_type(self):
        g = load_guard()
        schema = synthetic_schema()
        schema["root"]["fields"]["interval_ns"]["minimum"] = "1"
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_schema_definition(schema)

    def test_schema_definition_rejects_unsupported_kind(self):
        g = load_guard()
        schema = synthetic_schema()
        schema["root"]["fields"]["interval_ns"]["kind"] = "number"
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_schema_definition(schema)


class StrictTypeAndListTests(unittest.TestCase):
    def assert_rejected(self, document):
        g = load_guard()
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(document), synthetic_schema())

    def test_float_and_scientific_float_where_integer_required_are_rejected(self):
        self.assert_rejected({"interval_ns": 30.0, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})
        g = load_guard()
        raw = '{"interval_ns":1e2,"enabled":false,"mode":"FIXED_RATE","stages":["OBSERVE","STOP"]}'
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(raw, synthetic_schema())

    def test_boolean_where_integer_required_is_rejected(self):
        self.assert_rejected({"interval_ns": True, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})

    def test_integer_where_boolean_required_is_rejected(self):
        self.assert_rejected({"interval_ns": 30, "enabled": 0, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]})

    def test_unknown_enum_is_rejected(self):
        self.assert_rejected({"interval_ns": 30, "enabled": False, "mode": "COALESCE", "stages": ["OBSERVE", "STOP"]})

    def test_duplicate_list_member_is_rejected(self):
        self.assert_rejected({"interval_ns": 30, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "OBSERVE"]})

    def test_normative_order_change_is_rejected(self):
        self.assert_rejected({"interval_ns": 30, "enabled": False, "mode": "FIXED_RATE", "stages": ["STOP", "OBSERVE"]})

    def test_unknown_adjacent_config_authority_keys_are_rejected(self):
        base = {"interval_ns": 30, "enabled": False, "mode": "FIXED_RATE", "stages": ["OBSERVE", "STOP"]}
        for key in ("evaluation_authorized", "environment_override", "cli_override"):
            with self.subTest(key=key):
                mutated = dict(base)
                mutated[key] = True
                self.assert_rejected(mutated)


class P5EConcreteSchemaTests(unittest.TestCase):
    def test_adopted_contract_is_accepted_without_byte_mutation(self):
        g = load_guard()
        schema = load_schema()
        doc = g.validate_governed_json(current_contract_raw(), schema)
        self.assertEqual(doc["schema"], "ATDS_OBSIDIAN_P5E_END_TO_END_NEAR_REAL_TIME_CONTRACT_V0_1")

    def test_unknown_keys_at_representative_depths_are_rejected(self):
        g = load_guard()
        schema = load_schema()
        contract = json.loads(current_contract_raw())
        paths = [
            (),
            ("authority_boundary",),
            ("near_real_time_timing",),
            ("queue_and_supersession",),
            ("external_review_targeted_closure", "findings"),
        ]
        for path in paths:
            with self.subTest(path=path):
                mutated = copy.deepcopy(contract)
                node = mutated
                for key in path:
                    node = node[key]
                node["rpe01_unknown_key"] = True
                with self.assertRaises(g.GovernedSchemaError):
                    g.validate_governed_json(json.dumps(mutated), schema)

    def test_missing_required_key_is_rejected(self):
        g = load_guard()
        schema = load_schema()
        contract = json.loads(current_contract_raw())
        del contract["authority_boundary"]["evaluation_authorized"]
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(contract), schema)

    def test_normative_list_duplicate_unknown_and_order_change_are_rejected(self):
        g = load_guard()
        schema = load_schema()
        contract = json.loads(current_contract_raw())

        duplicate = copy.deepcopy(contract)
        duplicate["claim_boundary"]["forbidden_current_claims"][1] = duplicate["claim_boundary"]["forbidden_current_claims"][0]
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(duplicate), schema)

        unknown = copy.deepcopy(contract)
        unknown["required_synthetic_cases"][0] = "RPE01_UNKNOWN_CASE"
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(unknown), schema)

        reordered = copy.deepcopy(contract)
        stages = reordered["end_to_end_definition"]["real_end_to_end_stages"]
        stages[0], stages[1] = stages[1], stages[0]
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(json.dumps(reordered), schema)


class GuardPurityTests(unittest.TestCase):
    def test_guard_source_has_no_implicit_authority_channels(self):
        if not GUARD_PATH.exists():
            self.fail(f"required implementation missing: {GUARD_PATH}")
        source = GUARD_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)
        forbidden_import_roots = {
            "argparse", "os", "socket", "subprocess", "sys", "urllib",
            "requests", "httpx",
        }
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(imported.isdisjoint(forbidden_import_roots), imported & forbidden_import_roots)
        for forbidden_text in ("os.environ", "sys.argv", "input(", "open(", ".read_text(", ".read_bytes("):
            self.assertNotIn(forbidden_text, source)


if __name__ == "__main__":
    unittest.main()
