# DORA, the wrong way round

*Dysfunction `#24` in Trond Hjorteland's ["Organisational Dysfunction of the Day"](https://www.linkedin.com/posts/trondhjort_opensystemstheory-sociotechnical-orgdesign-activity-7459489978226651136-JqmL) series — synthesised through open sociotechnical systems theory; paraphrased, not quoted.*

## How it shows up

- DORA metrics (deployment frequency, lead time, change-fail rate, time-to-restore) are treated as **targets**: teams build dashboards, set quarterly goals, and run initiatives to move the numbers.
- Gains appear, then mysteriously reverse. Leadership responds by demanding more discipline, better tooling, or more training.
- Cargo-culting sets in — the rituals of high performers are copied without the conditions that made them high performers.

## The sociotechnical diagnosis

This confuses **measurement with causation**. DORA metrics were built as *research instruments* — downstream **signals** of healthy software delivery, not the **drivers** of it. Turning a signal into a target triggers Goodhart's Law: "the moment a measure becomes a target, it stops being a good measure."

The actual driver is structural. The numbers are good when teams are genuinely **self-managing (DP2)**: they own the whole product, can make decisions without escalation, and have tight feedback loops. Remove those conditions — keep a DP1 structure with handoffs, approvals, and fragmented ownership — and the metrics regress no matter how many dashboards you build. Chasing the numbers in a DP1 org optimises the appearance of the signal, not the system that produces it.

## What to do

**The real fix: build the conditions, not the numbers.**
- Stop targeting the metrics. Instead create the structural conditions that produce them: self-managing teams owning a whole product, deciding without escalation, with short feedback loops to real users.
- Use DORA as a *thermometer* — a way to notice whether the system is healthy — not a *thermostat* you crank. When the conditions are right, the same numbers emerge naturally as side effects of work done well; you don't have to chase them.
- When a number is bad, ask "what in our structure is producing this?" rather than "how do we hit the target?" The metric points at the system; fix the system.

**If you can't change the structure yet:**
- At minimum, stop tying DORA numbers to targets, reviews, or team comparisons — that actively makes them lie.
- Frame the metrics internally as learning signals the team interprets, not goals imposed on it.

## Related

- [[okrs-imposed-from-above]] — the same signal-as-target confusion, applied to goals.
- [[local-optimisations]] — improving a local number while the whole degrades.
- [[the-error-factory]] — measuring and punishing the symptom instead of fixing conditions.
- [[the-performance-review]] — individual measurement layered onto collective work.
