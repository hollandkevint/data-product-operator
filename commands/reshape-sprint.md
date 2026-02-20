---
description: Convert sprint artifacts into a shaped pitch with problem, appetite, solution, rabbit holes, and no-gos
argument-hint: <sprint backlog, user stories, or project description>
allowed-tools: Read, Write, AskUserQuestion
---

# Reshape a Sprint into a Shaped Pitch

Convert sprint-style artifacts (backlog items, user stories, story points, sprint plans) into a Shape Up pitch. Shape Up works better for data product teams because data work has inherent uncertainty that fixed-scope sprints can't accommodate.

The output is a shaped pitch that your team can evaluate at a betting table.

## Gather Context

If `$ARGUMENTS` provides a file path or description, use it. Otherwise, ask:

**Question 1:** Share your sprint artifacts. Options: paste backlog items, provide a file/doc, or describe what the sprint is supposed to accomplish.

**Question 2:** How long is the current sprint? (1 week, 2 weeks, other)

**Question 3:** What's the actual problem this sprint is trying to solve? (not the list of stories, but the customer or business problem underneath them)

**Question 4:** What is this work worth to the business? How much time should you budget for a solution? (This becomes the appetite.)

## Transformation Process

### Step 1: Find the Problem

Sprint backlogs list solutions (stories, tasks). Strip those away and find the underlying problem.

Look for:
- The user story at the top of the backlog (that's closest to the problem)
- Acceptance criteria that describe outcomes (not implementation steps)
- Any "why" documented in epic descriptions or comments

Rewrite as a problem statement: "[Who] needs to [do what] because [why], but currently [obstacle]."

### Step 2: Set the Appetite

Convert the sprint estimate into an appetite:

- Sprint velocity / story points are estimates of effort. Appetite is a budget of time.
- Ask: "If we could only spend [X weeks] on this, what's the smallest version that delivers value?"
- Standard appetites: 1 week (small batch) or 6 weeks (big batch)
- If the sprint is 2 weeks of work, that's a small batch (1 week appetite with buffer)
- If the sprint is 4-8 weeks of work, that's a big batch (6 week appetite)

### Step 3: Sketch the Solution

Convert user stories into a solution sketch:
- Not wireframes or specifications
- A rough description of the approach at the right level of abstraction
- Focus on the flow, not the details
- Include enough for a senior engineer to understand the approach and fill in the blanks

### Step 4: Identify Rabbit Holes

Look through the sprint backlog for:
- Stories marked as "spike" or "research" (uncertainty that could blow up the timeline)
- Dependencies on other teams or systems
- Technical unknowns flagged in comments
- Edge cases listed in acceptance criteria that might be more complex than they appear

Name each rabbit hole explicitly: "If the claims data API doesn't support real-time queries, this approach won't work. Verify API capabilities before committing."

### Step 5: Define No-Gos

Look for scope that was discussed but deprioritized, or that should be explicitly excluded:
- "Nice to have" items in the backlog
- Features that were in the original scope but cut
- Integrations or polish that can wait for a future cycle

State each no-go clearly: "We will NOT build the export-to-PDF feature in this cycle. Manual screenshots are acceptable for now."

## Write the Pitch

Write to `shaped-pitch-<name>.md` where `<name>` is a kebab-case summary of the problem.

### Output Structure

```markdown
# Shaped Pitch: [Problem Title]

**Appetite:** [1 week / 6 weeks]
**Author:** [team or person]
**Date:** [today]

## Problem

[2-3 paragraphs describing the problem from the user's perspective. Include evidence: customer quotes, support tickets, usage data, workaround descriptions.]

## Appetite

[Why this time budget is appropriate. What we're NOT willing to spend more time on.]

## Solution

[Solution sketch at the right level of abstraction. Describe the approach, not the implementation. Include rough flow: user does X -> system does Y -> result is Z.]

## Rabbit Holes

- [Risk 1]: [What could go wrong and how to check before committing]
- [Risk 2]: [What could go wrong and how to check before committing]

## No-Gos

- [Explicitly excluded scope 1]
- [Explicitly excluded scope 2]
```

### Key Principles

ALWAYS frame the pitch around the problem, not the solution backlog. The sprint had 15 stories. The pitch should describe 1 problem worth solving.

ALWAYS set an appetite, not an estimate. "This is worth 6 weeks of our time" is different from "this will take 6 weeks." The first is a business decision. The second is a guess.

NEVER carry over story points or velocity. Those are sprint artifacts. The pitch should stand on its own without sprint context.

When in doubt, make the appetite smaller and the no-gos list longer. It's better to ship a smaller version that works than to run out of time on a bigger version.
