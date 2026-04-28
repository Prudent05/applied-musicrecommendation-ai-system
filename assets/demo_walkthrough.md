# Demo Walkthrough (No Loom)

This project includes a text walkthrough alternative with reproducible commands and captured outputs.

## 1. End-to-end system run

Command:

```bash
python -m src.main
```

Observed sample outputs (top results per profile):

- High-Energy Pop
  - 1. Sunrise City by Neon Echo | score=6.49
  - 2. Gym Hero by Max Pulse | score=5.27
  - 3. Rooftop Lights by Indigo Parade | score=4.38
- Chill Lofi
  - 1. Library Rain by Paper Lanterns | score=6.58
  - 2. Midnight Coding by LoRoom | score=6.42
  - 3. Focus Flow by LoRoom | score=5.29
- Deep Intense Rock
  - 1. Storm Runner by Voltline | score=6.58
  - 2. Gym Hero by Max Pulse | score=4.30
  - 3. Iron Pulse by Granite Sky | score=3.22

## 2. Reliability and guardrail behavior

Command:

```bash
python -m src.evaluate
```

Observed output:

```text
=== Reliability Harness ===
1. [PASS] High-Energy Pop | expected: Top-1 genre should be pop | top=Sunrise City (pop) score=6.491 conf=0.969
2. [PASS] Chill Lofi | expected: Top-1 genre should be lofi | top=Library Rain (lofi) score=6.584 conf=0.983
3. [PASS] Deep Intense Rock | expected: Top-1 genre should be rock | top=Storm Runner (rock) score=6.580 conf=0.982
4. [PASS] Guardrail Out-of-Range Input | expected: System should return valid scores after clamping | top=Sunrise City (pop) score=5.344 conf=0.798

=== Summary ===
Passed 4/4 checks
Average confidence: 0.933
```

## 3. Automated tests

Command:

```bash
python -m pytest -q
```

Observed output:

```text
..
2 passed
```

## 4. One-command run (presentation mode)

Command:

```bash
python scripts/run_all.py
```

This runs demo output, unit tests, and reliability checks in one sequence.
