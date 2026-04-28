"""Run demo, tests, and reliability checks in one command."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_step(label: str, command: list[str]) -> int:
    print(f"\n=== {label} ===")
    print("$", " ".join(command))
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        print(f"\nStep failed: {label} (exit code {completed.returncode})")
        return completed.returncode
    print(f"Step passed: {label}")
    return 0


def main() -> int:
    root = Path(__file__).resolve().parents[1]

    steps = [
        ("Demo Run", [sys.executable, "-m", "src.main"]),
        ("Unit Tests", [sys.executable, "-m", "pytest", "-q"]),
        ("Reliability Harness", [sys.executable, "-m", "src.evaluate"]),
    ]

    for label, command in steps:
        code = run_step(label, command)
        if code != 0:
            return code

    print("\nAll checks passed. Project is presentation-ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
