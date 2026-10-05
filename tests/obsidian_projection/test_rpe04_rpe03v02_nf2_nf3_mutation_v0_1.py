from __future__ import annotations

import pathlib
import shutil
import types
import unittest
from unittest import mock

from tests.obsidian_projection.test_rpe04_real_remote_observation_adapter_v0_1 import (
    CONTROL,
    LOCAL_REF,
    MODULE,
    OBSERVER,
    PRODUCER,
    git,
    init_fixture,
)


def load_mutant(name: str, replacements):
    source = MODULE.read_text(encoding="utf-8")
    for old, new in replacements:
        if source.count(old) != 1:
            raise AssertionError(f"mutation anchor count != 1: {old!r}")
        source = source.replace(old, new, 1)
    module = types.ModuleType(name)
    module.__file__ = str(MODULE)
    exec(compile(source, str(MODULE), "exec"), module.__dict__)
    return module


class TestRPE04RPE03V02NF2NF3Mutation(unittest.TestCase):
    def setUp(self):
        self.a = init_fixture()

    def tearDown(self):
        shutil.rmtree(CONTROL, ignore_errors=True)

    def test_nf2_peeling_mutant_is_discriminated(self):
        base = load_mutant("rpe04_nf2_base", ())
        mutant = load_mutant(
            "rpe04_nf2_peeling_mutant",
            ((
'''def _extract_observed_sha() -> str | None:
    try:
        cp = _run_local_git(
            "for-each-ref",
            "--format=%(refname) %(objectname)",
            _LOCAL_REF,
        )
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    lines = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        return None
    parts = lines[0].split()
    if len(parts) != 2 or parts[0] != _LOCAL_REF:
        return None
    return parts[1]
''',
'''def _extract_observed_sha() -> str | None:
    try:
        cp = _run_local_git("rev-parse", "--verify", f"{_LOCAL_REF}^{{commit}}")
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    if cp.returncode != 0:
        return None
    return cp.stdout.strip()
'''
            ),),
        )
        git("tag", "-a", "mutation-tag", "-m", "mutation", self.a, cwd=PRODUCER)
        tag_oid = git("rev-parse", "refs/tags/mutation-tag", cwd=PRODUCER).stdout.strip()
        peeled = git("rev-parse", "refs/tags/mutation-tag^{commit}", cwd=PRODUCER).stdout.strip()
        git("fetch", str(PRODUCER / ".git"), f"refs/tags/mutation-tag:{LOCAL_REF}", cwd=OBSERVER)
        self.assertEqual(base._extract_observed_sha(), tag_oid)
        self.assertEqual(mutant._extract_observed_sha(), peeled)
        self.assertNotEqual(tag_oid, peeled)

    def test_nf3_alternates_guard_mutant_is_discriminated(self):
        base = load_mutant("rpe04_nf3_alt_base", ())
        mutant = load_mutant(
            "rpe04_nf3_alt_mutant",
            ((
'''    alternates = repo_path / "objects" / "info" / "alternates"
    if _lexists(alternates):
        return False, "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN"
''',
'''    alternates = repo_path / "objects" / "info" / "alternates"
    if False:
        return False, "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN"
'''
            ),),
        )
        alt = OBSERVER / "objects" / "info" / "alternates"
        alt.write_text(r"C:\outside-object-store" + "\n", encoding="ascii")
        self.assertEqual(
            base._verify_physical_object_domain(OBSERVER),
            (False, "PHYSICAL_GIT_DOMAIN_ALTERNATES_FORBIDDEN"),
        )
        self.assertEqual(mutant._verify_physical_object_domain(OBSERVER), (True, None))

    def test_nf3_recursive_indirection_guard_mutant_is_discriminated(self):
        base = load_mutant("rpe04_nf3_walk_base", ())
        mutant = load_mutant(
            "rpe04_nf3_walk_mutant",
            ((
'''                if _is_indirection(child):
                    return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
''',
'''                if False:
                    return False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"
'''
            ),),
        )
        pack = OBSERVER / "objects" / "pack" / "pack-mutant.pack"
        pack.write_bytes(b"fixture")
        original_base = base._is_indirection
        original_mutant = mutant._is_indirection

        def base_indirection(path):
            if pathlib.Path(path) == pack:
                return True
            return original_base(path)

        def mutant_indirection(path):
            if pathlib.Path(path) == pack:
                return True
            return original_mutant(path)

        with mock.patch.object(base, "_is_indirection", side_effect=base_indirection):
            self.assertEqual(
                base._verify_physical_object_domain(OBSERVER),
                (False, "PHYSICAL_GIT_DOMAIN_INDIRECTION"),
            )
        with mock.patch.object(mutant, "_is_indirection", side_effect=mutant_indirection):
            self.assertEqual(mutant._verify_physical_object_domain(OBSERVER), (True, None))


if __name__ == "__main__":
    unittest.main()
