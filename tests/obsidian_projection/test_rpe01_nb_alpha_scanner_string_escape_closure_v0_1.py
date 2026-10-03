import importlib.util
import json
import types
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = ROOT / "tools" / "obsidian_projection" / "rpe01_governed_closed_schema.py"
CONTRACT_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_end_to_end_near_real_time_contract_v0_1.json"
SCHEMA_PATH = ROOT / "tools" / "obsidian_projection" / "p5e_v0_1_governed_schema_v0_1.json"


def load_guard():
    spec = importlib.util.spec_from_file_location("rpe01_guard_nb_alpha", GUARD_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load RPE-01 guard")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_mutant_guard(*, neutralize_in_string=False, neutralize_escaped=False):
    source = GUARD_PATH.read_text(encoding="utf-8")

    if neutralize_in_string:
        old = """        if char == '"':
            in_string = True
            continue
"""
        new = """        if False:
            in_string = True
            continue
"""
        if source.count(old) != 1:
            raise AssertionError("in_string mutation anchor must occur exactly once")
        source = source.replace(old, new, 1)

    if neutralize_escaped:
        old = """            elif char == "\\\\":
                escaped = True
"""
        new = """            elif False:
                escaped = True
"""
        if source.count(old) != 1:
            raise AssertionError("escaped mutation anchor must occur exactly once")
        source = source.replace(old, new, 1)

    module = types.ModuleType("rpe01_guard_nb_alpha_mutant")
    module.__file__ = str(GUARD_PATH)
    exec(compile(source, str(GUARD_PATH), "exec"), module.__dict__)
    return module


def real_contract_with_bracket_heavy_string() -> str:
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    contract["objective"]["purpose"] = "[" * 100
    return json.dumps(contract, ensure_ascii=False, separators=(",", ":"))


def escaped_quote_followed_by_real_depth_over_limit() -> str:
    nested = 0
    # Root array depth 1 + 66 nested arrays = real JSON container depth 67.
    for _ in range(66):
        nested = [nested]
    # The first string contains an escaped quote followed by close-bracket characters.
    # A scanner that ignores escape state can incorrectly leave the string and
    # under-count the real nested arrays that follow.
    return json.dumps(
        ['"]]]]]]]]', nested],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def string_brackets_do_not_consume_depth(guard) -> bool:
    try:
        guard.validate_governed_json(
            real_contract_with_bracket_heavy_string(),
            SCHEMA_PATH.read_text(encoding="utf-8"),
        )
    except guard.GovernedSchemaError:
        return False
    return True


def escaped_string_cannot_hide_real_depth(guard) -> bool:
    raw = escaped_quote_followed_by_real_depth_over_limit()
    try:
        guard.parse_json_strict(raw)
    except guard.GovernedSchemaError as exc:
        return "maximum governed JSON depth" in str(exc)
    return False


class NBAlphaScannerStringEscapeTests(unittest.TestCase):
    def test_real_contract_string_brackets_do_not_consume_depth_budget(self):
        guard = load_guard()
        self.assertEqual(guard.MAX_GOVERNED_JSON_DEPTH, 64)
        self.assertGreater(
            len(json.loads(real_contract_with_bracket_heavy_string())["objective"]["purpose"]),
            guard.MAX_GOVERNED_JSON_DEPTH,
        )
        self.assertTrue(string_brackets_do_not_consume_depth(guard))

    def test_escaped_quote_cannot_hide_real_depth_over_limit(self):
        guard = load_guard()
        self.assertTrue(escaped_string_cannot_hide_real_depth(guard))

    def test_neutralizing_in_string_logic_is_killed(self):
        guard = load_guard()
        mutant = load_mutant_guard(neutralize_in_string=True)
        self.assertTrue(string_brackets_do_not_consume_depth(guard))
        self.assertFalse(
            string_brackets_do_not_consume_depth(mutant),
            "in_string-neutralized mutant must be killed by the real-contract string test",
        )

    def test_neutralizing_escape_logic_is_killed(self):
        guard = load_guard()
        mutant = load_mutant_guard(neutralize_escaped=True)
        self.assertTrue(escaped_string_cannot_hide_real_depth(guard))
        self.assertFalse(
            escaped_string_cannot_hide_real_depth(mutant),
            "escaped-state-neutralized mutant must be killed by the adversarial depth test",
        )


if __name__ == "__main__":
    unittest.main()
