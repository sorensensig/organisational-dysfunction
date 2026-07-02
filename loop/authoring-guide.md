# Authoring guide: writing a dysfunction reference

How to write one `references/NN-slug.md` file for the `organisational-dysfunction` skill. This is the durable, versioned version of the guide used to author the original set — follow it so new entries match the existing voice and structure. Synthesise and paraphrase from the source post; never copy verbatim.

## Inputs you need per entry

- **number** (`N`) and **exact title** (from the canonical full-list article)
- **slug** — lowercase; drop apostrophes/punctuation; spaces and en/em dashes → single hyphens (e.g. "DORA, the wrong way round" → `dora-the-wrong-way-round`, "It's just a job" → `its-just-a-job`)
- **post URL** — the LinkedIn post the article links for that item
- **content** — fetch the post URL and extract: (1) the symptom, (2) the sociotechnical / Open Systems Theory diagnosis (note DP1/DP2 and any specific construct he uses), (3) the suggested remedy. If the fetch fails or is thin, **stop and skip this entry** — do not fabricate.

## The shared lens (already in SKILL.md — apply it, don't re-explain it)

- **DP1 (redundancy of parts):** coordination/control sits one level *above* the work — hierarchy, individuals doing fragments integrated by a manager.
- **DP2 (redundancy of functions):** coordination/control sits *with* the people doing the work — multi-skilled self-managing teams owning a whole task.
- **Recurring diagnosis:** most dysfunctions = a DP2 idea run on a DP1 structure (or a DP1 fix applied to a DP1 problem); the symptom is the friction, and the real fix is structural — not a better ritual, more motivation, or "fixing the people". Lean on the named OST constructs where they fit (variance control at the point of work, Emery/Trist's six psychological job requirements, suboptimisation of the whole, Search Conference / butcher's paper, the Norwegian Industrial Democracy Programme, etc.).

## Exact template

```markdown
# <Title>

*Dysfunction #<N> in Trond Hjorteland's ["Organisational Dysfunction of the Day"](<POST_URL>) series — synthesised through open sociotechnical systems theory; paraphrased, not quoted.*

## How it shows up

- 3–5 concrete, recognisable symptom bullets that ring true to someone living it.

## The sociotechnical diagnosis

2–3 short paragraphs explaining WHY the structure produces this, via the DP1/DP2 lens and the specific OST construct the post uses. Be insightful and specific, not generic. Don't restate the full DP1/DP2 definitions — apply them.

## What to do

**The real fix is structural — <one-line framing>.**
- 2–4 bullets on the structural remedy (move authority/coordination to where the work happens, etc.).

**If you can't change the structure yet:**
- 2–3 bullets on realistic local moves the reader can make from where they sit, plus reframing that defuses misdirected blame.

## Related

- [[slug-1]] — half-sentence on the connection.
- [[slug-2]] — ...
- [[slug-3]] — ... (3–5 links; use ONLY slugs that exist in references/ — check with `ls references`)
```

## Quality bar

- Lean & sharp: ~¾ to 1 page. No filler, no throat-clearing.
- Imperative, confident voice — an experienced org designer, not a textbook.
- Name the specific OST construct the post relies on (this is the dimension most likely to be thin — don't skip it).
- Be honest about altitude in "If you can't change the structure yet".
- `[[links]]` use bare slugs (no number) and must resolve to a real `references/<NN>-<slug>.md` file.
