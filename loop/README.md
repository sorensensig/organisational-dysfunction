# The loop harness

An autoresearch-style evaluation + improvement loop for the `organisational-dysfunction` skill,
inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch): a fixed metric, an
agent that proposes a change, keep-if-better / revert-if-worse, logged each iteration.

It is **dependency-free** (Python 3 stdlib only) and drives the local `claude` CLI.

## Files

| file | role |
|---|---|
| `../evals/scenarios.json` | the scenario set — positives (with the reference they *should* route to) and near-miss negatives |
| `harness.py` | evaluation core: routing / triggering probes + the LLM-judge rubric |
| `run_loop.py` | the keep-best loop (quant) and the judge+suggestions report (qual) |
| `research.md` | the optimiser's brief — what to change, what not to, how to read failures |
| `history/` | per-iteration reports + `history.jsonl` (created on first run) |

## The two metrics

- **Triggering** — should the skill fire? Positives yes; near-misses that merely share vocabulary
  ("reword these OKRs", "summarise my performance review PDF", "optimise these slow queries") no.
- **Routing** — when it fires, does the router lead to the right reference file?

`composite = 0.5·triggering + 0.5·routing`.

## Running it

> Each run calls `claude -p` many times and consumes tokens/billing. Start small.

```bash
cd loop

# One-off score, no changes:
python3 harness.py eval --mode quant

# Quant keep-best loop (auto-tunes description + router; reverts regressions):
python3 run_loop.py --mode quant --iterations 5

# Qualitative judge pass over the actual answers -> writes history/qual-suggestions.md for you:
python3 run_loop.py --mode qual --limit 8

# Pin a model (defaults to claude-opus-4-8):
python3 run_loop.py --mode quant --iterations 5 --model claude-opus-4-8
```

## Modes, and why they differ

- **quant** auto-applies changes, but only to the **description** and the **router index** — the
  levers the metric actually measures — so it is safe to leave running. It never touches reference
  prose. Best version is left on disk; every iteration is logged.
- **qual** runs the rubric judge (structural diagnosis, OST fidelity, altitude-awareness,
  actionability, rings-true) on the real answers, finds the weakest references, and writes concrete
  improvement suggestions to `history/qual-suggestions.md`. It deliberately does **not** rewrite
  advice automatically — that stays a human decision.

## Extending the scenario set

Add entries to `evals/scenarios.json`. For a positive, set `should_trigger: true` and list every
acceptable reference slug (filename without `.md`) in `expected_refs`. For a near-miss, set
`should_trigger: false` and `expected_refs: []`. The most valuable additions are tricky negatives
and scenarios that currently route to the wrong place.
