# Data Product Operator

The shared language for teams that own data products: the people who decide, build, and check whether a data product changed the outcome it was built for.

## Products

**Data asset**:
Data with a named owner and documentation. It has value on its own only when a data product uses it.
_Avoid_: Data product (for an asset with no consumer or purpose), dataset-as-product

**Data product**:
A data asset with a named consumer, a quality promise, and a reason to exist: the decision it improves. It is judged by the revenue, cost, or risk outcome it changes.
_Avoid_: Dashboard, report, "the data"

**Delivery surface**:
The way a consumer reaches a data product: a dashboard, API, app, or analytics agent. A delivery surface is never the product by itself.
_Avoid_: Data product (for a dashboard or agent), front end

**Analytics agent**:
A delivery surface that answers questions in natural language over one or more data products.
_Avoid_: AI analyst, data product (for the agent itself)

## Layers

A data product has one frame and four layers: data assets, semantics, context, and the delivery surface. Design from the decision down, build from the data up, and ship the surface last. Governance and evals run across all four layers.

**Decision frame**:
The consumer, the decision they make, the outcome it changes, and the quality promise. It is not a layer of data; it is what turns a data asset into a data product.
_Avoid_: Context (for the decision itself), requirements (when no decision is named)

**Semantics**:
One written, approved definition for each metric and field: its grain, filters, time window, and calculation. A semantic layer or curated views hold it. A change needs an approver, because every surface on top changes with it.
_Avoid_: Metrics layer (when it holds more than metrics), business logic (when it is not written down)

**Context**:
What a newcomer or an agent needs to read the numbers right: synonyms, caveats, conventions, sample questions, and the reason behind a rule. It sits above semantics, changes weekly, and is fed by failed questions. Team Loop's `context/` folder is wider: it holds a product's decision frame and working notes.
_Avoid_: Context (for the decision frame), prompt (when it is a maintained asset)

## People

**Data product operator**:
The person who owns a data product and makes its decisions with the team, whatever their job title.
_Avoid_: Data product manager (as a required title), data owner

**Data product team**:
The people who build and run a data product with its operator: data engineers, data scientists, analysts, and anyone else whose handoff the product depends on.
_Avoid_: Data team (when it means a service desk), squad

**Consumer**:
The named person or team whose decision a data product improves.
_Avoid_: User (when unnamed), stakeholder, customer

## Loops

**Team loop**:
The daily and weekly cycle where a data product team builds, ships, reads the evidence, and records decisions.
_Avoid_: DPM OS, sprint (when it means the whole cycle)

**Strategy review**:
The quarterly loop where the operator reads the decision log and asks whether the strategy still holds: what paid off, which consumers were lost, and what to stop.
_Avoid_: QBR, planning (when nothing in the log is read)
