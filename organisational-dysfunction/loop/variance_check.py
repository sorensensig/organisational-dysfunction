#!/usr/bin/env python3
"""Run the quant eval N times to measure score stability (LLM nondeterminism)."""
import json
import statistics
import sys
from collections import Counter

import harness as H

N = int(sys.argv[sys.argv.index("--runs") + 1]) if "--runs" in sys.argv else 3
model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else H.DEFAULT_MODEL

runs = []
for i in range(N):
    print(f"\n--- run {i + 1}/{N} ---", flush=True)
    r = H.run_quant(model, verbose=False)
    runs.append(r)
    print(f"run {i + 1}: composite={r['composite']} trigger={r['trigger_accuracy']} routing={r['routing_accuracy']}", flush=True)

print("\n=== aggregate over", N, "runs ===")
for key in ["composite", "trigger_accuracy", "routing_accuracy"]:
    vals = [r[key] for r in runs]
    stdev = statistics.pstdev(vals) if len(vals) > 1 else 0.0
    print(f"{key:18} mean={statistics.mean(vals):.4f}  stdev={stdev:.4f}  min={min(vals):.4f}  max={max(vals):.4f}")

# which scenarios ever failed, and how often
fails = Counter()
for r in runs:
    for row in r["rows"]:
        if not (row["trigger_ok"] and row["routing_ok"]):
            fails[row["id"]] += 1
print("\nflaky/failed scenarios (id: times-failed of", N, "):", dict(fails) or "none — perfect every run")

(H.HARNESS_DIR / "history").mkdir(exist_ok=True)
out = H.HARNESS_DIR / "history" / "variance.json"
out.write_text(json.dumps({
    "runs": N, "model": model,
    "per_run": [{k: r[k] for k in ("composite", "trigger_accuracy", "routing_accuracy")} for r in runs],
    "flaky": dict(fails),
}, indent=2), encoding="utf-8")
print(f"\nsaved {out}")
