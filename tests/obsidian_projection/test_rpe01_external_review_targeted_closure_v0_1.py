import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"


def load_guard():
    spec = importlib.util.spec_from_file_location("rpe01_guard_targeted_closure", GUARD_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load RPE-01 guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def schema_raw() -> str:
    return json.dumps(
        {
            "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
            "artifact_role": "RPE01_TARGETED_CLOSURE_SYNTHETIC",
            "root": {
                "kind": "object",
                "fields": {
                    "a": {"kind": "integer"},
                },
            },
        },
        separators=(",", ":"),
    )


class NB1RawSchemaOnlyPublicApiTests(unittest.TestCase):
    def test_validate_governed_json_accepts_legitimate_raw_schema(self):
        g = load_guard()
        result = g.validate_governed_json('{"a":1}', schema_raw())
        self.assertEqual(result, {"a": 1})

    def test_validate_governed_json_rejects_preparsed_schema_object(self):
        g = load_guard()
        parsed_schema = json.loads(schema_raw())
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json('{"a":1}', parsed_schema)

    def test_public_validation_rejects_duplicate_schema_member_before_widening(self):
        g = load_guard()
        widened_duplicate_schema = (
            '{"schema":"ATDS_GOVERNED_JSON_SCHEMA_V0_1",'
            '"artifact_role":"RPE01_TARGETED_CLOSURE_SYNTHETIC",'
            '"root":{"kind":"object",'
            '"fields":{"a":{"kind":"integer"}},'
            '"fields":{"a":{"kind":"integer"},'
            '"evaluation_override":{"kind":"boolean"}}}}'
        )
        with self.assertRaises(g.GovernedSchemaError):
            g.validate_governed_json(
                '{"a":1,"evaluation_override":true}',
                widened_duplicate_schema,
            )

    def test_parsed_document_schema_validator_is_not_public(self):
        g = load_guard()
        self.assertFalse(
            hasattr(g, "validate_document"),
            "parsed-document/schema public bypass must not remain exposed",
        )


class NB2NormalizedExceptionTests(unittest.TestCase):
    def test_pathological_integer_conversion_is_normalized(self):
        g = load_guard()
        pathological = '{"a":' + ("9" * 5000) + "}"
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_json_strict(pathological)

    def test_pathological_nesting_is_normalized(self):
        g = load_guard()
        depth = 5000
        pathological = ("[" * depth) + "0" + ("]" * depth)
        with self.assertRaises(g.GovernedSchemaError):
            g.parse_json_strict(pathological)


if __name__ == "__main__":
    unittest.main()
