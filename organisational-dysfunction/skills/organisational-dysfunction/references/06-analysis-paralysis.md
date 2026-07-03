# Analysis paralysis

*Dysfunction `#6` in Trond Hjorteland's ["Organisational Dysfunction of the Day"](https://www.linkedin.com/posts/trondhjort_opensystemstheory-sociotechnical-orgdesign-share-7447929340174077952-OK7t) series — synthesised through open sociotechnical systems theory; paraphrased, not quoted.*

## How it shows up

- A team rewriting a legacy system gets stuck mapping every existing behaviour before it dares ship anything.
- The goal quietly becomes "function parity" — reproduce the old thing exactly — rather than deliver value.
- People go hunting for the original developers and chase down who in the business actually owns each rule.
- Months pass with diligent analysis and no release; the work is technically underway but produces nothing.
- Every attempt to cut scope stalls on "but we can't drop that — someone, somewhere, might depend on it."

## The sociotechnical diagnosis

The instinct is to read this as a discipline problem — the team is over-thinking, being too cautious. But agile is more or less purpose-built for exactly this kind of uncertainty: start small, release, learn. So if a team *can't* work that way, the question is what's stopping it. Hjorteland's answer is ownership.

This team controls only the technical layer. It does not own the product end to end, nor the relationship with the users, nor the authority to decide what the rewrite actually needs to do. Those sit with external parties. A self-managing DP2 team can take full responsibility for delivery because it owns the whole problem — goals, trade-offs, and users included. Strip the ownership down to "just build it like the old one" and the team has no basis on which to say *this matters, that doesn't*. With no authority to make those calls, exhaustive parity analysis becomes the only safe move: reproduce everything, because you're not allowed to decide what's unnecessary.

So the paralysis is structural. It's the rational output of a team given technical responsibility without the product authority that would let it scope, prioritise, and release.

## What to do

**The real fix is structural — give the team end-to-end ownership of the whole product, not just its plumbing.**
- Put goals, users, and trade-off authority with the team building it, so it can decide what parity is actually worth reproducing.
- Make it a genuine self-managing product team (DP2): responsible *and* accountable for outcomes, not just for code.
- Collapse the distance to real users so the team can validate by releasing, instead of by interrogating the old system.

**If you can't change the structure yet:**
- Replace "function parity" with a thin, real slice of value and ship it; let actual usage, not archaeology, reveal what matters.
- Force the prioritisation question to a named owner: "we'll drop X unless someone tells us it's needed" surfaces the truth far faster than mapping every path.
- Reframe with the team: the stalling isn't timidity, it's the only safe behaviour given how little they're allowed to decide. The cure is authority, not willpower.

## Related

- [[passing-the-buck]] — both stem from teams holding responsibility without matching authority.
- [[the-product-owner-trap]] — ownership that's nominal rather than real produces this scoping paralysis.
- [[fear-of-making-decisions]] — without authority to decide, "analyse more" is the safe default.
- [[the-customer-we-never-met]] — distance from real users forces guesswork to stand in for feedback.
- [[built-for-yesterday]] — chasing exact parity rebuilds the past instead of the needed future.
