# Research brief: improving the organisational-dysfunction skill

You are an optimisation agent improving a Claude *skill* — a router (`SKILL.md`) plus 59 reference
files — that diagnoses organisational dysfunctions through open sociotechnical systems theory.

This is the `program.md`-equivalent of an autoresearch loop: each iteration you propose ONE focused
change, it is scored against a fixed scenario set, and it is kept only if the metric improves.

## The metric you are optimising (quant mode)

A composite of two measured quantities over `evals/scenarios.json`:

- **Triggering accuracy** — positive scenarios should fire the skill; near-miss negatives (which
  share vocabulary like "OKR", "performance review", "forming-storming" but need something else)
  should NOT. This is driven almost entirely by the `description`.
- **Routing accuracy** — for a positive scenario, the router's index should lead the model to open
  the correct reference file(s). This is driven by the index entries' recognition cues.

composite = 0.5 × triggering + 0.5 × routing.

## What you may change

- **The `description`.** Keep it ~2 sentences. It must carry both *what the skill does* and *when to
  reach for it*, and its discriminating signal is the idea of **structure rather than people** —
  "symptoms blamed on individuals, mindset, or communication". Do not bloat it back into a long
  enumeration of every ritual; umbrella terms (org design, team autonomy, ways of working, incentives,
  leadership, transformation) plus that hook are what make it both trigger and not over-trigger.
- **The router index entries** in `SKILL.md` — the one-line recognition cue and grouping. If two
  dysfunctions are being confused, sharpen the cue that distinguishes them. If a positive scenario
  routes nowhere, the cue probably doesn't surface the words people actually use.

## What you must NOT change

- The reference files' content. Advice quality is judged separately (qual mode) with a human in the
  loop — never silently rewrite someone's diagnosis to chase a number.
- The DP1/DP2 core-lens section. It is the spine; leave it intact unless a failure clearly traces to it.

## How to think about failures

- **Negative scenario triggered (false positive):** the description is too broad or keyword-greedy.
  Tighten the "when to reach for it" so adjacent tasks (copy-editing OKRs, summarising a review doc,
  tuning DB performance) fall outside it — usually by leaning harder on the "diagnose a structural
  dysfunction" framing rather than the noun.
- **Positive scenario didn't trigger (false negative):** the description doesn't connect the user's
  lived phrasing to the skill. Add the missing bridge in umbrella terms, not a new keyword dump.
- **Wrong reference chosen:** the two entries' cues overlap. Make each cue name the distinctive
  symptom, not the shared theme.

Avoid overfitting to single scenarios. A change that fixes one case but reads as a hack (stuffing a
scenario's exact words into the index) will tend to break others and is the wrong kind of fix —
prefer changes that generalise.
