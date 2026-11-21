# First principles of a good data product team

Nine principles explain why this repo works the way it does. Each one is credited to named authors with links. Where the authors disagree, the page says so, in [Where the sources disagree](#where-the-sources-disagree).

How to read it. The principles are Kevin Holland's synthesis of the public sources linked under each one. No source states all nine. A principle is listed only if at least one author says it in their own terms. Quotes are short and copied from the linked page. Read the original before you rely on a detail.

Terms follow the [glossary](../GLOSSARY.md).

## What a data product is

Sources use "data product" for three different things. The glossary keeps them apart as three layers. Each layer takes the strongest point from one school of thought.

- **Data asset (the packaging school).** Gartner, McKinsey, Databricks, Snowflake and AWS describe a curated, documented, governed bundle with an owner. That is the strongest point of this school, and it is a data asset in the glossary. It is necessary, but a well-governed table with no user is still only an asset. ([Gartner](https://www.gartner.com/en/documents/5456063), [McKinsey](https://www.mckinsey.com/capabilities/quantumblack/our-insights/how-to-unlock-the-full-value-of-data-manage-it-like-a-product), [Databricks](https://www.databricks.com/blog/building-high-quality-and-trusted-data-products-databricks))
- **Data product, part one: a named consumer (the consumer school).** Brian T. O'Neill, Nick Zervoudis and Thoughtworks say a data product is built for someone, not just stored. The glossary requires a named consumer. ([O'Neill](https://designingforanalytics.com/resources/the-definition-of-data-product/), [Zervoudis](https://designingforanalytics.com/resources/episodes/130-nick-zervoudis-on-data-product-management-ux-design-training-and-overcoming-imposter-syndrome), [Thoughtworks](https://www.thoughtworks.com/en-us/radar/techniques/data-product-thinking))
- **Data product, part two: a decision (the outcome school).** DJ Patil, and Emilie Schario with Taylor Murphy, say the point is an end goal or a decision. The glossary asks for the decision the product improves, and judges the product by the outcome it changes. ([Patil, as quoted by Databricks](https://www.databricks.com/blog/building-high-quality-and-trusted-data-products-databricks), [Schario and Murphy](https://locallyoptimistic.com/post/run-your-data-team-like-a-product-team))
- **Delivery surface.** A dashboard, API, app or agent is how a consumer reaches the product. Most 2025 and 2026 writing treats an agent as a consumer of data products, not as a product ([Google Cloud](https://cloud.google.com/transform/from-asset-to-action-how-data-products-have-become-the-foundation-for-ai-agents), [Fowler](https://martinfowler.com/articles/making-data-ready-for-agentic-ai.html)). The glossary follows that reading. An analytics agent is a delivery surface.

Why three layers and not one definition. Asset alone passes a governed table nobody asked for. Consumer alone has no check on quality. Decision alone is so wide that a bank statement qualifies. Together they exclude all three failures. If you also want a machine-readable description, the [Open Data Product Standard](https://bitol-io.github.io/open-data-product-standard/latest/) and the [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) from Bitol are the nearest fit. Two unrelated standards share the name ODPS, so name the one you mean.

## The nine principles

### P1. Start from the decision, not the artifact

Name the decision, who owns it, and what changes if the answer changes. Dashboards, pipelines and agents come after.

- Ben Rogojan asks first: "What question or decision is this data supposed to support?" ([Six questions before a data project](https://seattledataguy.substack.com/p/are-data-teams-solving-the-right))
- Nick Valiotti: "a modern stack without defined KPIs is just a prettier spreadsheet." ([Stop overbuilding your data stack](https://nickvaliotti.substack.com/p/stop-overbuilding-your-data-stack))
- Vin Vashishta works from the opportunity to the workflow to the technology ([metric vs outcome](https://vinvashishta.substack.com/p/the-metric-isnt-the-outcome-how-to)).
- Peter Everill: a data team helps the business decide where to focus ([The purpose of a data team](https://petereverill.substack.com/p/the-purpose-of-a-data-team)).
- Emilie Schario's jobs-to-be-done method turns requests into the job behind them ([JTBD for data teams](https://locallyoptimistic.com/?p=671)).

### P2. Own an outcome, not a queue

A support function that takes tickets becomes a bottleneck. A product team owns a consumer's problem or metric from end to end.

- Xavier Gumara Rigol says a data asset works as a product when it has named consumers, clear ownership and someone accountable for its life cycle ([The two pillars of data-driven product organizations](https://moderndata101.substack.com/p/pillars-of-data-driven-product))
- Nick Zervoudis: the team should ask whether it works on the right problem, not take orders ([interview](https://designingforanalytics.com/resources/episodes/130-nick-zervoudis-on-data-product-management-ux-design-training-and-overcoming-imposter-syndrome)).
- Zhamak Dehghani names the central platform backlog as the bottleneck ([From monolith to mesh](https://martinfowler.com/articles/data-monolith-to-mesh.html)).
- Eric Weber argues a data team can no longer attribute its value to throughput. ([Stop counting dashboards](https://ericdataproduct.substack.com/p/stop-counting-dashboards-data-team))

### P3. One written definition and one named owner for each decision metric, before any tool or AI

- Nick Valiotti: "If 'no one' owns data, then 'everyone' ignores it." ([10 data strategy mistakes](https://nickvaliotti.substack.com/p/10-mistakes-i-see-in-every-startups))
- Tristan Handy, quoting Ian Macomber, says consensus is the scarce resource ([The analyst's new competitive advantage](https://open.substack.com/pub/dataanalysis/p/the-analysts-new-competitive-advantage)).
- Ben Rogojan asks where the real source of truth lives ([Six questions](https://seattledataguy.substack.com/p/are-data-teams-solving-the-right)).
- Zhamak Dehghani puts quality accountability at the source ([Data mesh principles](https://martinfowler.com/articles/data-mesh-principles.html)).
- Modern Data 101 puts semantics inside the product contract ([Data products: the essential context](https://moderndata101.substack.com/p/data-products-the-essential-context)).

### P4. Treat a data asset as a product: a named consumer, a contract, a life cycle that includes retirement

- Zhamak Dehghani: domain data must be treated as a product, with an owner who knows its users ([Data mesh principles](https://martinfowler.com/articles/data-mesh-principles.html)).
- Modern Data 101: "It has a named consumer in mind." ([Essential context](https://moderndata101.substack.com/p/data-products-the-essential-context))
- Brian T. O'Neill: owner and contract are not enough. The product must also work as a decision solution for a person ([definition](https://designingforanalytics.com/resources/the-definition-of-data-product/)).
- Benn Stancil: production is a state you declare and then support. Mark the assets that are in production ([What is production?](https://benn.substack.com/p/what-is-production)).

### P5. Show the cost of yes

Challenge a request, then compare use cases as investments.

- Nick Zervoudis, in a guest post for Dylan Anderson's newsletter: "A good use case is not necessarily a good investment." ([Value-driven prioritisation](https://thedataecosystem.substack.com/p/issue-66-value-driven-prioritisation))
- Ben Rogojan lists the cost of not doing the work as one of his six questions ([Six questions](https://seattledataguy.substack.com/p/are-data-teams-solving-the-right)).
- Eric Weber tracks how many experiments pay off ([Stop counting dashboards](https://ericdataproduct.substack.com/p/stop-counting-dashboards-data-team)).

### P6. Measure value at the decision or workflow, not at the activity

Dashboards built and queries answered are activity. Decision speed, outcome lift and countermetrics are value.

- Vin Vashishta: "Any metric that is disconnected from an outcome can be gamed, and that’s what happened in most businesses." ([Why are businesses so good at lying](https://vinvashishta.substack.com/p/why-are-businesses-so-good-at-lying))
- Vashishta also describes four linked levels: adoption, model performance, workflow outcome, business outcome ([metric vs outcome](https://vinvashishta.substack.com/p/the-metric-isnt-the-outcome-how-to)).
- Eric Weber proposes decision velocity, experiment yield and revenue affected ([Stop counting dashboards](https://ericdataproduct.substack.com/p/stop-counting-dashboards-data-team)).
- Brian T. O'Neill: judge the product by the outcome in the user's own workflow ([Surgery or healing?](https://designingforanalytics.com/resources/does-your-data-product-enable-surgery-or-healing/)).
- Dylan Anderson's critic, Benny Benford: "More complex analytics ≠ more value." ([LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7134843183393300480))

### P7. Match stage and stack to today's decisions

Buy a tool when a KPI and a decision need it, not before.

- Nick Valiotti ties data function problems to company stage, not to tools ([stages post](https://www.linkedin.com/posts/valiotti_most-founders-build-their-data-function-one-share-7506244865148690434--ZVY/)).
- Ben Rogojan argues a pipeline needs a clear purpose beyond moving data from A to B ([Why data pipelines exist](https://seattledataguy.substack.com/p/why-data-pipelines-exist))
- Dylan Anderson: ask how mature you need to be for what is expected today ([Data and AI maturity](https://thedataecosystem.substack.com/p/issue-61-data-and-ai-maturity)).

### P8. Adoption is an incentive and structure problem

Map incentives before you design the product.

- Anna Bergevin: "The Incentive Map is the invisible layer that powers organizational behavior." ([The incentive map](https://dataprodmgmt.substack.com/p/the-incentive-map-every-data-platform))
- Vin Vashishta says data teams support the business but own nothing outside the data team, so incentives must cross teams ([cross-functional organizations](https://vinvashishta.substack.com/p/building-cross-functional-data-organizations)).
- Eric Weber says the technical and operating halves multiply ([Data infra PM](https://ericdataproduct.substack.com/p/data-infra-pm-the-most-important)).
- Benn Stancil's test is pull: the work should be bought, not sold ([Data teams and product-market fit](https://benn.substack.com/p/data-teams-product-market-fit)).

### P9. Trust is the scarce good as production gets cheap

Govern use, evaluate outputs, and give agents context.

- Olga Berezovsky, in her interview with Tristan Handy: the bottleneck shifts from producing analytics to making sense of them. AI lowers the cost of producing analytics, not the cost of trusting it ([interview](https://open.substack.com/pub/dataanalysis/p/the-analysts-new-competitive-advantage)).
- Nick Valiotti separates a running query from a trusted answer ([The job was never the code](https://nickvaliotti.substack.com/p/the-job-was-never-the-code)).
- Eric Weber: "Humans are remarkably good at putting up with a mess (while also complaining about it)." Agents are not. ([Data infra PM](https://ericdataproduct.substack.com/p/data-infra-pm-the-most-important))
- Modern Data 101 treats context as a first-class asset ([Essential context](https://moderndata101.substack.com/p/data-products-the-essential-context)).
- Peter Everill: the team also manages the machine, meaning explainability, inputs and ethics ([The purpose of a data team](https://petereverill.substack.com/p/the-purpose-of-a-data-team)).

## Where the sources disagree

- **Accountability for the result (P2).** Peter Everill says the data team guides the evidence and the operating team decides the action. Eric Weber says take a causal position and claim the revenue. Vin Vashishta says data teams own nothing outside the data team and must lead without authority. This repo treats it as a design choice for each team.
- **Tone when you challenge a request (P1, P5).** Nick Zervoudis says build trust slowly and stay curious. Ben Rogojan says engineering should push back. The goal is the same. The method differs.
- **Causal claims about value (P6).** Eric Weber wants a revenue ledger. The Vashishta position is that business-outcome claims are confounded and workflow outcomes are the least you should claim. Weber's 70 percent experiment-yield line has no stated basis.
- **Size of the stack (P7).** Valiotti and Rogojan lean small. Weber and Modern Data 101 say agents need heavy context infrastructure. The stage test resolves it: a small stack for early decisions, a context layer once agents act on the data.
- **Where the filter sits (P1, P9).** Vashishta says the filter was always the quality of the opportunity, and agents removed the productivity limit. The Berezovsky interview with Handy says trust and interpretation are now the limit. Both hold: P1 picks the problem, P9 keeps the answer safe.
- **Is an owned asset already a product? (P4).** Xavier Gumara Rigol says yes, an owned asset is a product. Brian T. O'Neill says no, "data as a product" is only a refined asset, and a data product is a human-in-the-loop decision solution.
- **Does the product model fit every company? (P2, P4).** Benn Stancil questions the "everything is a product" frame in [The problem was the product](https://benn.substack.com/p/the-problem-was-the-product) and asks whether a data team has product-market fit at all. Schario and Murphy and the mesh authors assume it does.
- **Who is the customer? (P2).** Schario and Murphy treat colleagues as customers. Later commentary says the company is the customer. This repo does not settle it. Use the glossary word consumer.
- **What counts as a data product.** The packaging school asks what the thing is. Zervoudis says it should be defined by how you make it. Dehghani limits the term to analytical data on a mesh, while Patil includes end-user applications.
- **Product or service.** Databricks now argues "Stop building data products. Start building data services," because one product per use case breaks when agents are the consumer ([Databricks](https://www.databricks.com/blog/stop-building-data-products-start-building-data-services)). This repo keeps the product frame and treats an agent as a delivery surface.
- **Are agents products or consumers?** Most 2025 and 2026 writing says consumers. Some vendor pages list agents as products. The glossary picks consumer-side: an analytics agent is a delivery surface.
- **Maturity ladders.** Dylan Anderson and Benny Benford argue against one ladder for a whole company. This page keeps the stages and scores them per use case, which is the fix Anderson proposes.

## Maturity model, scored per use case

This model is Kevin Holland's synthesis. It combines stage signals from Gumara Rigol's three phases and Valiotti's stages, and it keeps the critique above. It has not been tested against real teams.

Score each use case on its own. One team can sit at stage 3 for one workflow and stage 1 for another. The stages are not a strict order. The lowest dimension is the limit.

| Stage | What the team does | Signs you are here | Next gap |
|---|---|---|---|
| 0. Intuition | One person answers questions by hand | Spreadsheets, conflicting numbers, no owner | One written metric definition and one owner |
| 1. Foundations | Builds a warehouse, pipelines and reports that describe what happened | Reports exist, definitions live in people's heads, reconciliation is monthly | Definitions and owners for each decision metric |
| 2. Support function | Takes tickets and requests | The queue grows, nobody pushes back, output is counted in dashboards shipped | Challenge requests, show the cost of yes, name the decision |
| 3. Product driver | Owns outcomes. Each asset has an owner, a consumer, a contract and a life cycle | Owners sit outside the data team, a retire rule exists, a decision metric is reviewed on a schedule | Link engineering work to measured business value |
| 4. Decision system | Measures value at the workflow. Agents run under evals and shared context | Decision speed is tracked, holdouts exist, evals run after launch, people manage agents | Keep the loop alive as models and data change |

Sources behind the stages: Gumara Rigol for stages 1 to 3, Valiotti for stages 0 and 3, Zervoudis for stage 2, Weber, Handy and Modern Data 101 for stage 4. Anderson and Benford shape how to use the table.

Gaps. The sources say little about how a team moves from stage 2 to stage 3 beyond Gumara Rigol's advice to start with one team and one problem. Healthcare adds clinical, privacy and validation steps that none of these authors cover.

## Credits

This page summarizes and links to the work below. Nothing here replaces the originals.

- Nick Valiotti, [The Datapreneur](https://nickvaliotti.substack.com)
- Vin Vashishta, [High ROI AI](https://vinvashishta.substack.com)
- Ben Rogojan, [Seattle Data Guy](https://seattledataguy.substack.com)
- Peter Everill, [newsletter](https://petereverill.substack.com)
- Nick Zervoudis, with Dylan Anderson, [The Data Ecosystem](https://thedataecosystem.substack.com)
- Eric Weber, [Data as a Product](https://ericdataproduct.substack.com)
- Tristan Handy, interviewed by Olga Berezovsky ([article](https://open.substack.com/pub/dataanalysis/p/the-analysts-new-competitive-advantage))
- Xavier Gumara Rigol and the [Modern Data 101](https://moderndata101.substack.com) authors
- Anna Bergevin, [When Data Met Product](https://dataprodmgmt.substack.com)
- Zhamak Dehghani, [Data mesh principles](https://martinfowler.com/articles/data-mesh-principles.html) and [From monolith to mesh](https://martinfowler.com/articles/data-monolith-to-mesh.html)
- Brian T. O'Neill, [Designing for Analytics](https://designingforanalytics.com)
- Emilie Schario and Taylor Murphy, [Locally Optimistic](https://locallyoptimistic.com/post/run-your-data-team-like-a-product-team)
- Benn Stancil, [benn.substack.com](https://benn.substack.com)
- Benny Benford, [LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7134843183393300480)
- DJ Patil, [Data Jujitsu](https://www.oreilly.com/library/view/data-jujitsu-the/9781449342692/index.html)
- Bitol, [Open Data Product Standard](https://bitol-io.github.io/open-data-product-standard/latest/) and [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/)
