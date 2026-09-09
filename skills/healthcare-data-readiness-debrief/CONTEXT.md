# Start here

Healthcare Data Readiness Debrief helps you turn one project's data-preparation problems into a short brief: What happened, what evidence is missing, who can check it and what the result would change.

Use it for an active project or a retrospective. It does not inspect your data or approve a launch. “Readiness” names the decision you are investigating, not a certification the skill provides.

## Use the package

Keep this folder together. Give `SKILL.md` and the relevant reference files to an AI assistant approved by your organization, or read the instructions as a guided worksheet. Native installation depends on the assistant; this package does not install or configure anything automatically. If the assistant cannot read a linked file, supply that file before expecting domain-specific guidance. No separate Matt Pocock or Compound plugin is needed.

Describe one project in your own words. You can include the intended use, what you expected, what surprised the team and what remains uncertain. You do not need to fill out every field before starting.

Choose either a one-question-at-a-time interview or ask for a brief from the summary you supplied. Say “brief now” whenever you want to stop the interview. For completed work, ask for a retrospective lesson rather than a new action list.

Use synthetic examples, schema descriptions or approved aggregate summaries. Do not upload patient records, credentials, confidential contracts, restricted study materials or proprietary measure manuals. The responsible team should perform record-level checks inside its approved environment.

## What's included

| File | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Interview and brief instructions |
| [Quality and trials](references/quality-and-trials.md) | Separate HEDIS/eCQM routes, trial purpose, derivations and blinding |
| [Records and mapping](references/records-and-mapping.md) | Retrieval coverage, identity, access and HL7/FHIR meaning |
| [Claims and operations](references/claims-and-operations.md) | Claim/payment stages, scheduling state and support behavior |
| [Original example](example.md) | One complete fictional debrief |
| [Twelve worked scenarios](examples/scenarios.md) | Additional synthetic cases across the domains above |

The domain notes contain dated public-source links. They provide investigation prompts, not executable reporting logic, payer rules or clinical trial criteria. The applicable owner must confirm project-specific rules and versions. A cited release is not automatically the release your project uses.

## What has been tested

On September 8, 2026, three research reviewers and a fourth fresh-context tester contributed to 25 simulated conversations: Nine baseline cases, nine revised replays, three added revised cases and four fresh-context cases. The review found no endorsement of the unsafe action tested in those conversations.

These were same-model conversational exercises with an AI reviewer. Most testers retained prior context; one grilling demonstration was explicitly guided. Four cases used a fresh context. The work did not include independent healthcare-professional review, live data tests, clinical validation or a field pilot. The original skill also handled the baseline cases well, so the results do not establish a measured improvement from revision.

This packaging follow-up clarified single-question interviewing, shorter briefs and completed-retrospective handling. Those edits received structural and editorial checks; the 25 conversations predate them and were not rerun. Their results should not be presented as a fresh benchmark of this exact package.

Review the brief before using it. Check whether it preserves your account, identifies a consequential uncertainty and proposes a check your team can perform. Correct mistaken interpretations. An unresolved answer is useful when the brief identifies who can resolve it.

## Design context

The instructions adapt Matt Pocock's dependency-by-dependency grilling, Compound Engineering's outcome-focused planning and Compound Writing's separation of a person's account from interpretation. These are design influences, not endorsements. Historical questions stay neutral; recommendations concern the next decision or check.

Kevin Holland prepared this as a standalone resource for healthcare data professionals. Using it does not require booking a conversation, sending the brief to Kevin or sharing project data. The package contains no connectors, telemetry code or lead form. Your chosen assistant's own data handling still applies.
