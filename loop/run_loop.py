#!/usr/bin/env python3
"""
run_loop.py — the autoresearch-style improvement loop for the org-dysfunction skill.

Modelled on Karpathy's autoresearch shape: a fixed evaluation (the "metric"), an agent
that proposes a change, keep-if-better / revert-if-worse, logged each iteration.

Two modes:

  --mode quant   Optimise TRIGGERING + ROUTING. Each iteration, an agent ("the researcher")
                 reads the failing scenarios and proposes a new description and/or router
                 index tweaks. We re-score; keep the change only if the composite metric
                 improves, otherwise revert. The mutation surface is deliberately limited to
                 the description and the router (SKILL.md) — the levers the metric measures —
                 so the loop is safe to run unattended. Best version wins.

  --mode qual    Run the LLM-judge over the actual answers, then synthesise concrete
                 improvement suggestions for the lowest-scoring references. Does NOT auto-edit
                 reference prose — advice quality needs a human in the loop — it produces a
                 review file for you to act on.

Usage:
  python3 run_loop.py --mode quant --iterations 5 [--model claude-opus-4-8]
  python3 run_loop.py --mode qual  [--limit 8]

Requires the local `claude` CLI (see harness.py). Note: this calls `claude -p` many times
and consumes tokens/billing — start with a small --iterations / --limit.
"""

import json
import sys
import time
from pathlib import Path

import harness as H

HISTORY_DIR = H.HARNESS_DIR / "history"
RESEARCH_MD = H.HARNESS_DIR / "research.md"


def _arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def _log_history(record: dict):
    HISTORY_DIR.mkdir(exist_ok=True)
    with open(HISTORY_DIR / "history.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


def _save_report(name: str, report: dict):
    HISTORY_DIR.mkdir(exist_ok=True)
    (HISTORY_DIR / name).write_text(json.dumps(report, indent=2), encoding="utf-8")


# --- quant loop --------------------------------------------------------------


def propose_change(report: dict, model: str) -> dict:
    """Ask the researcher agent for a new description + router replacements to fix failures."""
    fails = [r for r in report["rows"] if not (r["trigger_ok"] and r["routing_ok"])]
    fail_lines = []
    for r in fails:
        fail_lines.append(
            f"- [{r['id']}] positive={r['positive']} | triggered={r['triggered']} "
            f"(want {r['positive']}) | predicted_refs={r['predicted_refs']} "
            f"| expected_refs={r['expected_refs']}"
        )
    research = RESEARCH_MD.read_text(encoding="utf-8") if RESEARCH_MD.exists() else ""
    prompt = f"""{research}

## Current scores
trigger_accuracy={report['trigger_accuracy']}  routing_accuracy={report['routing_accuracy']}  composite={report['composite']}

## Failing scenarios (these are what to fix)
{chr(10).join(fail_lines) if fail_lines else "(none — propose a small robustness improvement)"}

## Current description
{H.get_description()}

## Current SKILL.md (router)
{H.read_skill_md()}

## Your task
Propose ONE focused improvement. You may rewrite the `description` and/or make a few exact-string
replacements inside SKILL.md's index to fix the routing failures above (e.g. sharpen a recognition
cue so the right reference is chosen, or disambiguate two entries the model is confusing). Do NOT
rewrite reference files. Keep the description tight (2 sentences, umbrella terms + the "structure
not people" discriminating hook). Every `find` string must appear VERBATIM in the current SKILL.md.

Reply with ONLY this JSON:
{{
  "description": "<new full description, or the current one unchanged>",
  "router_replacements": [{{"find": "<exact substring in SKILL.md>", "replace": "<new text>"}}],
  "rationale": "<one sentence>"
}}"""
    reply = H.call_claude(prompt, model=model, timeout=240)
    data = H._extract_json(reply)
    return data if isinstance(data, dict) else None


def apply_change(change: dict) -> bool:
    """Apply description + router replacements to SKILL.md. Returns False if any find is missing."""
    text = H.read_skill_md()
    new_desc = change.get("description", "").strip()
    if new_desc:
        text = H.re.sub(r"^description:.*$", f"description: {new_desc}", text, count=1, flags=H.re.MULTILINE)
    for rep in change.get("router_replacements", []) or []:
        find, replace = rep.get("find", ""), rep.get("replace", "")
        if find and find in text:
            text = text.replace(find, replace, 1)
        elif find:
            return False  # stale find — reject whole change to stay safe
    H.SKILL_MD.write_text(text, encoding="utf-8")
    return True


def quant_loop(model: str, iterations: int):
    original = H.read_skill_md()
    print(f"\n=== Baseline eval (model={model}) ===")
    best = H.run_quant(model)
    _save_report("iteration-0.json", best)
    _log_history({"iter": 0, "composite": best["composite"],
                  "trigger": best["trigger_accuracy"], "routing": best["routing_accuracy"],
                  "kept": True, "note": "baseline"})
    print(f"baseline composite={best['composite']} (trigger={best['trigger_accuracy']} routing={best['routing_accuracy']})")
    best_text = original

    for i in range(1, iterations + 1):
        print(f"\n=== Iteration {i}/{iterations} ===")
        change = propose_change(best, model)
        if not change:
            print("  researcher returned no parseable change; stopping.")
            break
        print(f"  proposal: {change.get('rationale','(no rationale)')}")
        if not apply_change(change):
            print("  proposal had a stale find-string; skipping (reverting).")
            H.SKILL_MD.write_text(best_text, encoding="utf-8")
            _log_history({"iter": i, "kept": False, "note": "stale-find rejected"})
            continue
        trial = H.run_quant(model)
        improved = trial["composite"] > best["composite"]
        print(f"  trial composite={trial['composite']} vs best={best['composite']} -> {'KEEP' if improved else 'REVERT'}")
        if improved:
            best, best_text = trial, H.read_skill_md()
            _save_report(f"iteration-{i}.json", trial)
        else:
            H.SKILL_MD.write_text(best_text, encoding="utf-8")  # revert
        _log_history({"iter": i, "composite": trial["composite"],
                      "trigger": trial["trigger_accuracy"], "routing": trial["routing_accuracy"],
                      "kept": improved, "rationale": change.get("rationale", "")})

    H.SKILL_MD.write_text(best_text, encoding="utf-8")  # ensure best is on disk
    print(f"\n=== Done. Best composite={best['composite']}. SKILL.md left at best version. ===")
    print(f"History: {HISTORY_DIR/'history.jsonl'}")


# --- qual report -------------------------------------------------------------


def qual_report(model: str, limit):
    print(f"\n=== Qualitative judge pass (model={model}) ===")
    report = H.run_qual(model, limit=int(limit) if limit else None)
    _save_report("qual-report.json", report)
    weak = sorted(report["rows"], key=lambda r: r["avg"])[:5]
    weak_block = "\n\n".join(
        f"### {r['id']} (avg {r['avg']}) refs={r['refs_used']}\nScores: {r['scores']}\nAnswer:\n{r['answer'][:1500]}"
        for r in weak
    )
    prompt = f"""You are improving an org-design skill's reference files. Below are its weakest-scoring
answers from a rubric judge (structural diagnosis, OST fidelity, altitude-awareness, actionability,
rings-true). For EACH, name the reference file(s) likely responsible and give 1-3 concrete edits that
would raise the score — sharper symptoms, a crisper DP1/DP2 diagnosis, more honest local moves, etc.
Be specific and brief.

{weak_block}

Reply as markdown with one section per scenario."""
    suggestions = H.call_claude(prompt, model=model, timeout=240)
    out = HISTORY_DIR / "qual-suggestions.md"
    HISTORY_DIR.mkdir(exist_ok=True)
    out.write_text(f"# Qual improvement suggestions\n\nOverall rubric score: {report['overall']}\n\n{suggestions}\n", encoding="utf-8")
    print(f"overall rubric score = {report['overall']}")
    print(f"Suggestions written to {out} (review and apply by hand).")


if __name__ == "__main__":
    mode = _arg("--mode", "quant")
    model = _arg("--model", H.DEFAULT_MODEL)
    if mode == "quant":
        quant_loop(model, int(_arg("--iterations", "5")))
    else:
        qual_report(model, _arg("--limit"))
