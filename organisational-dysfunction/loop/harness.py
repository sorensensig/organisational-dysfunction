#!/usr/bin/env python3
"""
harness.py — evaluation core for the organisational-dysfunction skill loop.

Dependency-free (stdlib only). Drives the local `claude` CLI to measure how well
the skill performs, on two axes:

  ROUTING   — given the router (SKILL.md) and a user scenario, does the model open
              the right reference file(s)?
  TRIGGERING — given only the skill's description and a user scenario, would the
              skill fire at all? (positives should fire, near-miss negatives should not)

And, for qualitative mode, an LLM-judge that scores the actual answer the skill
would produce against a rubric (faithful to OST, structural diagnosis, altitude-aware,
actionable).

This file is a library; run it via run_eval.py / run_loop.py, or directly:
    python3 harness.py eval --mode quant
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

# --- paths -------------------------------------------------------------------

HARNESS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = HARNESS_DIR.parent
SKILL_DIR = PLUGIN_ROOT / "skills" / "organisational-dysfunction"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFS_DIR = SKILL_DIR / "references"
SCENARIOS = PLUGIN_ROOT / "evals" / "scenarios.json"

DEFAULT_MODEL = "claude-opus-4-8"

# --- claude CLI --------------------------------------------------------------


def call_claude(prompt: str, model: str = DEFAULT_MODEL, timeout: int = 180) -> str:
    """Run `claude -p` headlessly, prompt on stdin, return stdout text.

    CLAUDECODE is stripped from the child env so this works when invoked from inside
    another Claude Code session (the nested-session guard otherwise refuses to launch).
    """
    child_env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        proc = subprocess.run(
            ["claude", "-p", "--model", model],
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout,
            env=child_env,
        )
    except FileNotFoundError:
        sys.exit("ERROR: `claude` CLI not found on PATH. Install it or adjust call_claude().")
    except subprocess.TimeoutExpired:
        return ""
    if proc.returncode != 0:
        sys.stderr.write(f"[claude error] {proc.stderr[:400]}\n")
    return proc.stdout.strip()


def _extract_json(text: str):
    """Pull the first JSON value (array or object) out of a noisy model reply."""
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


# --- skill introspection -----------------------------------------------------


def read_skill_md() -> str:
    return SKILL_MD.read_text(encoding="utf-8")


def get_description(skill_md: str = None) -> str:
    skill_md = skill_md or read_skill_md()
    m = re.search(r"^description:\s*(.+?)\s*$", skill_md, re.MULTILINE)
    return m.group(1) if m else ""


def valid_slugs() -> set:
    return {p.stem for p in REFS_DIR.glob("*.md")}


def load_scenarios() -> list:
    return json.loads(SCENARIOS.read_text(encoding="utf-8"))["scenarios"]


# --- the three probes --------------------------------------------------------


def probe_routing(scenario: dict, model: str) -> list:
    """Return the list of reference slugs the model would open for this scenario."""
    prompt = f"""You are deciding which reference file(s) of a skill to open.

Below is the skill's router file (SKILL.md). A user has said:

\"\"\"{scenario['prompt']}\"\"\"

Based ONLY on the router's index, which reference file(s) would you open to answer
well? Reply with a JSON array of the file identifiers (the `NN-slug` part, WITHOUT
the .md extension). If none of the dysfunctions genuinely fit, reply with [].
Reply with ONLY the JSON array, nothing else.

--- SKILL.md ---
{read_skill_md()}
"""
    reply = call_claude(prompt, model=model)
    data = _extract_json(reply)
    if not isinstance(data, list):
        return []
    return [str(x).replace(".md", "").strip() for x in data]


def probe_trigger(scenario: dict, model: str) -> bool:
    """Return whether the model thinks the skill should fire, from the description alone."""
    desc = get_description()
    prompt = f"""A Claude assistant has access to a skill with this description:

\"\"\"{desc}\"\"\"

The user says:

\"\"\"{scenario['prompt']}\"\"\"

Should Claude consult this skill to answer? Consider that skills should fire when they
genuinely add value and NOT for adjacent requests that merely share vocabulary.
Reply with ONLY one word: YES or NO."""
    reply = call_claude(prompt, model=model).upper()
    return reply.startswith("Y") or "YES" in reply[:10]


JUDGE_RUBRIC = [
    ("structural_diagnosis", "Diagnoses the problem as structural (DP1/DP2, system design) rather than blaming individuals, mindset, or 'communication'."),
    ("faithful_to_ost", "Uses the open sociotechnical systems lens accurately and specifically, not generic management advice."),
    ("altitude_aware", "Distinguishes the real structural fix from realistic local moves the person can make from where they sit."),
    ("actionable", "Gives concrete, usable next steps rather than vague platitudes."),
    ("rings_true", "Names the dysfunction in a way that would feel recognisable to someone living it."),
]


def probe_answer(scenario: dict, model: str, refs: list) -> str:
    """Produce the answer the skill would give: router + the routed reference files + the prompt."""
    ref_texts = []
    for slug in refs:
        f = REFS_DIR / f"{slug}.md"
        if f.exists():
            ref_texts.append(f.read_text(encoding="utf-8"))
    bundle = "\n\n---\n\n".join(ref_texts) if ref_texts else "(no specific reference matched; reason from the core lens)"
    prompt = f"""You are answering a user using the 'organisational-dysfunction' skill.
Use the router guidance and the reference material below. Be sharp and concrete.

User:
\"\"\"{scenario['prompt']}\"\"\"

--- SKILL.md (router + lens) ---
{read_skill_md()}

--- Routed reference material ---
{bundle}
"""
    return call_claude(prompt, model=model)


def probe_judge(scenario: dict, answer: str, model: str) -> dict:
    rubric_lines = "\n".join(f"- {k}: {desc}" for k, desc in JUDGE_RUBRIC)
    prompt = f"""Score an answer that an org-design assistant gave to a user.

User asked:
\"\"\"{scenario['prompt']}\"\"\"

Answer to score:
\"\"\"{answer}\"\"\"

Score each criterion from 0.0 to 1.0:
{rubric_lines}

Reply with ONLY a JSON object: {{"<criterion>": <score>, ...}} using the exact keys above."""
    reply = call_claude(prompt, model=model)
    data = _extract_json(reply)
    keys = [k for k, _ in JUDGE_RUBRIC]
    if not isinstance(data, dict):
        return {k: 0.0 for k in keys}
    return {k: float(data.get(k, 0.0)) for k in keys}


# --- scoring -----------------------------------------------------------------


def run_quant(model: str, verbose: bool = True) -> dict:
    """Routing + triggering accuracy across the scenario set."""
    scenarios = load_scenarios()
    rows = []
    for s in scenarios:
        positive = s["should_trigger"]
        triggered = probe_trigger(s, model)
        trigger_ok = (triggered == positive)

        routing_ok = None
        predicted = []
        if positive:
            predicted = probe_routing(s, model)
            expected = set(s["expected_refs"])
            routing_ok = bool(expected & set(predicted))  # lenient: any acceptable ref hit
        else:
            # negatives: routing should be empty / not over-eager
            predicted = probe_routing(s, model)
            routing_ok = (len(predicted) == 0)

        row = {
            "id": s["id"], "positive": positive,
            "triggered": triggered, "trigger_ok": trigger_ok,
            "expected_refs": s.get("expected_refs", []),
            "predicted_refs": predicted, "routing_ok": routing_ok,
        }
        rows.append(row)
        if verbose:
            mark = "✓" if (trigger_ok and routing_ok) else "✗"
            print(f"  {mark} {s['id']:<32} trig={'Y' if triggered else 'N'}({'ok' if trigger_ok else 'X'}) route={predicted or '[]'}")

    n = len(rows)
    trig_acc = sum(r["trigger_ok"] for r in rows) / n
    route_acc = sum(r["routing_ok"] for r in rows) / n
    composite = 0.5 * trig_acc + 0.5 * route_acc
    return {
        "mode": "quant", "model": model, "n": n,
        "trigger_accuracy": round(trig_acc, 4),
        "routing_accuracy": round(route_acc, 4),
        "composite": round(composite, 4),
        "rows": rows,
    }


def run_qual(model: str, verbose: bool = True, limit: int = None) -> dict:
    """LLM-judge rubric scores on the actual answers for positive scenarios."""
    scenarios = [s for s in load_scenarios() if s["should_trigger"]]
    if limit:
        scenarios = scenarios[:limit]
    rows = []
    for s in scenarios:
        refs = s["expected_refs"] or probe_routing(s, model)
        answer = probe_answer(s, model, refs)
        scores = probe_judge(s, answer, model)
        avg = sum(scores.values()) / len(scores) if scores else 0.0
        rows.append({"id": s["id"], "refs_used": refs, "scores": scores,
                     "avg": round(avg, 3), "answer": answer})
        if verbose:
            print(f"  {s['id']:<32} avg={avg:.2f}  " +
                  " ".join(f"{k[:6]}={v:.1f}" for k, v in scores.items()))
    overall = sum(r["avg"] for r in rows) / len(rows) if rows else 0.0
    return {"mode": "qual", "model": model, "n": len(rows),
            "overall": round(overall, 4), "rows": rows}


if __name__ == "__main__":
    mode = sys.argv[sys.argv.index("--mode") + 1] if "--mode" in sys.argv else "quant"
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else DEFAULT_MODEL
    result = run_quant(model) if mode == "quant" else run_qual(model)
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}, indent=2))
