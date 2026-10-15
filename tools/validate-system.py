#!/usr/bin/env python3
"""Validate the canonical trading-system document set before handoff."""
from pathlib import Path
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REQUIRED = [
    "00-MASTER-EXECUTION-CHECKLIST.md",
    "01-SYSTEM-VISION.md",
    "02-ASSET-PROFILE-DATABASE.md",
    "03-REGIME-EXPERT-RESEARCH-FOUNDATION.md",
    "04-VALIDATION-CRITERIA.md",
    "05-DATA-CONTRACT.md",
]
MIN_BYTES = {
    "00-MASTER-EXECUTION-CHECKLIST.md": 5000,
    "01-SYSTEM-VISION.md": 5000,
    "02-ASSET-PROFILE-DATABASE.md": 5000,
    "03-REGIME-EXPERT-RESEARCH-FOUNDATION.md": 5000,
    "04-VALIDATION-CRITERIA.md": 10000,
    "05-DATA-CONTRACT.md": 5000,
}

errors = []
print("ADAPTIVE TRADING DECISION SYSTEM — INTEGRITY GATE")
print("Canonical source: docs/00 → docs/05")

for name in REQUIRED:
    path = DOCS / name
    if not path.exists():
        errors.append(f"MISSING: {path}")
        continue
    size = path.stat().st_size
    if size < MIN_BYTES[name]:
        errors.append(f"SUSPICIOUSLY SMALL: {path} ({size} bytes; minimum {MIN_BYTES[name]})")
        continue
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        errors.append(f"EMPTY: {path}")
        continue
    if "TODO" in text or "PLACEHOLDER" in text:
        errors.append(f"PLACEHOLDER MARKER FOUND: {path}")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    print(f"OK  {name:55} {size:7} bytes  sha256:{digest}")

# Detect accidental split/duplicate numbered documents outside docs/.
for p in ROOT.glob("0[0-9]-*.md"):
    errors.append(f"NUMBERED DOC OUTSIDE docs/: {p.relative_to(ROOT)}")

if errors:
    print("\nINTEGRITY GATE: FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("\nINTEGRITY GATE: PASSED")
print("The canonical document set is complete, non-empty, and structurally located in docs/.")
