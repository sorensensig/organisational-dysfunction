# The external verdict

*Dysfunction #30 in Trond Hjorteland's ["Organisational Dysfunction of the Day"](https://www.linkedin.com/posts/trondhjort_opensystemstheory-sociotechnical-orgdesign-activity-7462389110390034433-buX5) series — synthesised through open sociotechnical systems theory; paraphrased, not quoted.*

## How it shows up

- A consultancy is hired to review the codebase / architecture / ways of working and hand back a verdict.
- The report lands, and the team's first reaction is defensive: "they didn't understand our context."
- Findings are dismissed as naïve or out of date; the few that are accepted are the ones the team already knew.
- The document goes into a folder and changes almost nothing.
- Reviewers gathered their evidence in one-to-one interviews, which the team experienced as being assessed individually rather than as a group.

## The sociotechnical diagnosis

The move itself is DP1: judgement and control are placed *outside* the group doing the work. An external party is appointed to decide whether the work is good. That structural choice is what produces the defensiveness, not thin skin — when someone else owns the verdict, the only rational stance is to defend your patch against it.

It also fails on its own terms. The knowledge that explains *why* the system looks the way it does — the constraints, the trade-offs, the decisions taken under pressure — is distributed across the people who built it. A reviewer parachuting in for two weeks of interviews can't reach it, so the report is accurate about surface and wrong about cause. And running the review through individual interviews quietly reinforces individualisation: it treats quality as the sum of what each person knows, rather than something the group holds together.

In DP2 the group owns the quality of its own work. That ownership cannot be subcontracted. The instant you hire someone to be the judge, you've told the team that quality is not theirs — which is precisely the belief that lets quality rot.

## What to do

**The real fix is structural — the team must own the verdict; outside eyes are a mirror, never a judge.**
- Run the review as a collective sense-making session: the team leads, names the problems it already knows, and walks the external input through its own context.
- Treat the consultant's findings as *one perspective* to react to, not *the* judgement to comply with.
- Keep ownership of quality inside the group — commission help to see better, not to be graded.

**If you can't change the structure yet:**
- Get the report read together as a team, out loud, rather than absorbed privately and defended in silos.
- Translate every finding into "is this true *for us*, and what would we do about it?" — convert verdict into hypothesis.
- Reframe defensiveness for what it is: a sane response to externalised judgement, not the team being closed-minded.

## Related

- [[dora-the-wrong-way-round]] — outside metrics used to grade teams rather than help them see.
- [[fixing-people]] — locating the fault in individuals instead of the design.
- [[the-powerless-retrospective]] — the group reflects but doesn't own the levers to act.
- [[individualism]] — quality treated as a sum of individuals, not a group property.
- [[the-error-factory]] — judgement-from-above producing defensiveness instead of learning.
