from __future__ import annotations

import unittest
from pathlib import Path

from tools.obsidian_projection.inventory import load_inventory


class PilotInventoryTests(unittest.TestCase):
    def test_frozen_pilot_inventory_shape(self) -> None:
        root = Path(__file__).resolve().parents[2]
        inventory_path = (
            root
            / "tools"
            / "obsidian_projection"
            / "pilot_inventory_v0_1.json"
        )
        inventory = load_inventory(inventory_path)

        self.assertEqual(
            inventory.source_repository,
            "thboulevart-creator/ADAPTIVE-TRADING-DECISION-SYSTEM",
        )
        self.assertEqual(
            inventory.source_branch,
            "integration/system-v1",
        )
        self.assertEqual(
            inventory.source_commit,
            "7bd8c1312430dfc3def5523eb65397a5d6a5ae05",
        )
        self.assertEqual(
            inventory.source_tree,
            "66eeb08a338732d4cf7f5b7f4f5e5fd9fbb4d54b",
        )
        self.assertEqual(inventory.source_artifact_count, 74)
        self.assertEqual(len(inventory.entries), 74)
        self.assertEqual(len(inventory.digest_sha256), 64)

        paths = [entry.source_path for entry in inventory.entries]
        self.assertEqual(len(paths), len(set(paths)))


if __name__ == "__main__":
    unittest.main()
