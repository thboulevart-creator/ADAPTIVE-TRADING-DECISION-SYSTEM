from pathlib import Path


PATH = Path("tests/test_trading_breaks_recovery_batch02.py")


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    old = "assert len(queue) == 61"
    new = "assert len(queue) == 57"
    if new in text:
        print("Batch 02 regression already aligned to post-Batch03 unresolved count.")
        return 0
    if text.count(old) != 1:
        raise RuntimeError("BATCH02_QUEUE_COUNT_ASSERTION_NOT_UNIQUE")
    PATH.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("Updated Batch 02 historical regression to current post-Batch03 queue count: 57.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
