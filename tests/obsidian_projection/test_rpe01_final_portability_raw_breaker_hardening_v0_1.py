import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"
CONTRACT_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
SCHEMA_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_governed_schema_v0_1.json"


def load_guard():
    spec = importlib.util.spec_from_file_location("rpe01_guard_final_hardening", GUARD_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load RPE-01 guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract_raw():
    return CONTRACT_PATH.read_text(encoding="utf-8")


def schema_raw():
    return SCHEMA_PATH.read_text(encoding="utf-8")


def replace_once(raw: str, old: str, new: str) -> str:
    if raw.count(old) != 1:
        raise AssertionError(f"expected exactly one raw anchor: {old!r}")
    return raw.replace(old, new, 1)


def duplicate_real_authority_raw(*, escaped: bool = False) -> str:
    raw = contract_raw()
    anchor = '    "evaluation_authorized": false,'
    if escaped:
        duplicate = '    "\\u0065valuation_authorized": true,'
    else:
        duplicate = '    "evaluation_authorized": true,'
    return replace_once(raw, anchor, anchor + "\n" + duplicate)


def nonstandard_numeric_real_contract(token: str, field: str, original: int) -> str:
    raw = contract_raw()
    anchor = f'    "{field}": {original},'
    replacement = f'    "{field}": {token},'
    return replace_once(raw, anchor, replacement)


def duplicate_valid_schema_member_raw() -> str:
    raw = schema_raw()
    anchor = '  "artifact_role": "P5E_V0_1_ADOPTED_CONTRACT_CLOSED_SCHEMA",'
    return replace_once(raw, anchor, anchor + "\n" + anchor)


def nested_array_raw(depth: int) -> str:
    return ("[" * depth) + "0" + ("]" * depth)


def nested_array_schema_raw(array_levels: int) -> str:
    node = {"kind": "null"}
    for _ in range(array_levels):
        node = {"kind": "array", "items": node}
    return json.dumps(
        {
            "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
            "artifact_role": "RPE01_DEPTH_BOUNDARY",
            "root": node,
        },
        separators=(",", ":"),
    )


def syntactic_container_depth(raw: str) -> int:
    depth = 0
    maximum = 0
    in_string = False
    escaped = False
    for char in raw:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            maximum = max(maximum, depth)
        elif char in "]}":
            depth -= 1
    if depth != 0:
        raise AssertionError("test fixture is not container-balanced")
    return maximum


def rejection_message(guard, raw_document: str, raw_schema: str | None = None):
    try:
        if raw_schema is None:
            guard.parse_json_strict(raw_document)
        else:
            guard.validate_governed_json(raw_document, raw_schema)
    except guard.GovernedSchemaError as exc:
        return str(exc)
    return None


class NBA_DeterministicDepthTests(unittest.TestCase):
    def test_preregistered_depth_constant_exists_and_is_exact(self):
        g = load_guard()
        self.assertEqual(g.MAX_GOVERNED_JSON_DEPTH, 64)

    def test_document_depth_64_allowed_and_65_rejected_by_depth_guard(self):
        g = load_guard()
        at_limit = nested_array_raw(64)
        above_limit = nested_array_raw(65)
        self.assertEqual(syntactic_container_depth(at_limit), 64)
        self.assertEqual(syntactic_container_depth(above_limit), 65)
        g.parse_json_strict(at_limit)
        with self.assertRaisesRegex(
            g.GovernedSchemaError,
            "maximum governed JSON depth",
        ):
            g.parse_json_strict(above_limit)

    def test_schema_depth_64_allowed_and_65_rejected_by_depth_guard(self):
        g = load_guard()
        at_limit = nested_array_schema_raw(62)
        above_limit = nested_array_schema_raw(63)
        self.assertEqual(syntactic_container_depth(at_limit), 64)
        self.assertEqual(syntactic_container_depth(above_limit), 65)
        g.parse_schema_json_strict(at_limit)
        with self.assertRaisesRegex(
            g.GovernedSchemaError,
            "maximum governed JSON depth",
        ):
            g.parse_schema_json_strict(above_limit)

    def test_validate_schema_definition_normalizes_residual_recursion(self):
        g = load_guard()
        schema = {
            "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
            "artifact_role": "RPE01_FORCED_RECURSION",
            "root": {"kind": "null"},
        }
        original = g._validate_schema_node

        def forced(*args, **kwargs):
            raise RecursionError("forced schema recursion")

        g._validate_schema_node = forced
        try:
            with self.assertRaises(g.GovernedSchemaError):
                g.validate_schema_definition(schema)
        finally:
            g._validate_schema_node = original

    def test_public_document_validation_normalizes_residual_recursion(self):
        g = load_guard()
        raw_schema = json.dumps(
            {
                "schema": "ATDS_GOVERNED_JSON_SCHEMA_V0_1",
                "artifact_role": "RPE01_FORCED_RECURSION",
                "root": {"kind": "null"},
            },
            separators=(",", ":"),
        )
        original = g._validate_document_node

        def forced(*args, **kwargs):
            raise RecursionError("forced document recursion")

        g._validate_document_node = forced
        try:
            with self.assertRaises(g.GovernedSchemaError):
                g.validate_governed_json("null", raw_schema)
        finally:
            g._validate_document_node = original


class NBB_DiscriminatingRawBreakerTests(unittest.TestCase):
    def assert_parser_reason(self, raw_document, expected, raw_schema=None):
        g = load_guard()
        message = rejection_message(
            g,
            raw_document,
            schema_raw() if raw_schema is None else raw_schema,
        )
        self.assertIsNotNone(message)
        self.assertIn(expected, message)

    def test_real_authority_duplicate_is_rejected_for_duplicate_reason(self):
        self.assert_parser_reason(
            duplicate_real_authority_raw(),
            "duplicate JSON member: evaluation_authorized",
        )

    def test_real_authority_escaped_duplicate_is_rejected_for_duplicate_reason(self):
        self.assert_parser_reason(
            duplicate_real_authority_raw(escaped=True),
            "duplicate JSON member: evaluation_authorized",
        )

    def test_real_numeric_nan_is_rejected_by_nonstandard_constant_rule(self):
        self.assert_parser_reason(
            nonstandard_numeric_real_contract(
                "NaN",
                "poll_interval_seconds",
                30,
            ),
            "non-standard JSON numeric constant forbidden: NaN",
        )

    def test_real_numeric_positive_infinity_is_rejected_by_constant_rule(self):
        self.assert_parser_reason(
            nonstandard_numeric_real_contract(
                "Infinity",
                "detection_latency_seconds_max",
                60,
            ),
            "non-standard JSON numeric constant forbidden: Infinity",
        )

    def test_real_numeric_negative_infinity_is_rejected_by_constant_rule(self):
        self.assert_parser_reason(
            nonstandard_numeric_real_contract(
                "-Infinity",
                "detection_latency_seconds_max",
                60,
            ),
            "non-standard JSON numeric constant forbidden: -Infinity",
        )

    def test_otherwise_valid_raw_schema_duplicate_is_rejected_for_duplicate_reason(self):
        self.assert_parser_reason(
            contract_raw(),
            "duplicate JSON member: artifact_role",
            duplicate_valid_schema_member_raw(),
        )


class TargetedMutationKillTests(unittest.TestCase):
    def test_duplicate_member_breaker_kills_duplicate_detection_mutant(self):
        g = load_guard()
        raw = duplicate_real_authority_raw()
        baseline = rejection_message(g, raw, schema_raw())
        self.assertIn("duplicate JSON member: evaluation_authorized", baseline)

        original = g._strict_object
        g._strict_object = dict
        try:
            mutant_message = rejection_message(g, raw, schema_raw())
        finally:
            g._strict_object = original

        self.assertIsNone(
            mutant_message,
            "without duplicate detection this structural breaker must survive",
        )

    def test_constant_breaker_kills_parse_constant_mutant(self):
        g = load_guard()
        raw = nonstandard_numeric_real_contract(
            "NaN",
            "poll_interval_seconds",
            30,
        )
        expected = "non-standard JSON numeric constant forbidden: NaN"
        baseline = rejection_message(g, raw, schema_raw())
        self.assertIn(expected, baseline)

        original = g._reject_constant
        g._reject_constant = lambda value: float(value)
        try:
            mutant_message = rejection_message(g, raw, schema_raw())
        finally:
            g._reject_constant = original

        self.assertIsNotNone(mutant_message)
        self.assertNotIn(
            expected,
            mutant_message,
            "removing parse_constant protection must kill the parser-specific breaker",
        )

    def test_depth_65_breaker_kills_depth_guard_mutant(self):
        g = load_guard()
        raw = nested_array_raw(65)
        baseline = rejection_message(g, raw)
        self.assertIn("maximum governed JSON depth", baseline)

        original = g._enforce_max_json_depth
        g._enforce_max_json_depth = lambda text: None
        try:
            mutant_message = rejection_message(g, raw)
        finally:
            g._enforce_max_json_depth = original

        self.assertIsNone(
            mutant_message,
            "without the deterministic depth guard depth 65 must survive parsing",
        )


if __name__ == "__main__":
    unittest.main()
