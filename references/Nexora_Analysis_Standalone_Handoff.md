# Nexora logistics analysis and prototype data handoff

## 1. Instruction to the receiving assistant

You are the analytical workstream for an Indonesian e-commerce business competition project. **Carry out the research, calculations, geospatial preparation, policy evaluation, Monte Carlo analysis, and financial modelling described below. Deliver the actual files, including a complete master context pack.** Do not stop at a proposed methodology or a list of things the user should calculate.

This document is self-contained. Do not assume access to previous chats, their files, connected accounts, or the original PDF. Verified relevant casebook figures and constraints are transcribed below. If the original PDF is separately attached, it takes precedence over any transcription error. Otherwise use this extract and accurately describe your source access; do not claim you personally inspected the PDF.

The user has authorised you to independently research and select remaining technical and financial assumptions. Do not ask the user to invent costs, discount rates, elasticities, capacities, or forecast inputs. Make educated, documented assumptions and test consequential alternatives. Ask only if a material dependency cannot reasonably be resolved. Use available spreadsheet and geospatial skills and tools according to their instructions.

**This chat does the analysis. A different chat will build the prototype from your outputs. Do not build or deploy the website.**

## 2. Project and strategic context

Nexora is fictional. Indonesia is the case market. NexExpress is its internal logistics arm, operating alongside third-party logistics providers, called 3PLs. All monetary case figures are Indonesian rupiah (IDR/Rp).

Official case question:

> How can Nexora achieve sustainable profitable growth while strengthening its competitive position and mitigating seller and buyer attrition in Indonesia's increasingly competitive e-commerce market?

The wider team has three working goals: grow transaction value, monetise sustainably, and deliver efficiently and reliably. This workstream concerns the third goal and its financial consequences. Buyer surveys have been distributed, and seller interviews are being prepared. No survey results, completed interview findings, or validated demand elasticities are supplied here. Print-on-demand is a separate growth hypothesis; do not incorporate its revenue or demand into this logistics model.

The operational hypothesis is that better allocation between NexExpress and 3PLs, more effective use of existing capacity, and selective investments can improve consolidated economics without sacrificing service. The answer is not assumed to be more insourcing everywhere. A current-policy or smaller-investment alternative is allowed to win.

The competition prototype will demonstrate a delivery operations control room, a policy heatmap, and incident-response decisions. It will contain actual browser-side numerical calculations and potentially thousands of Monte Carlo runs, using case anchors, external evidence, and explicit hypothetical operating assumptions. It is not a live company digital twin.

The user wants an optimistic but rational opportunity assessment. Interpret optimism as pursuing plausible improvements and staged investment in favourable locations, not forcing favourable assumptions or a positive result. Present a central case, a justified upside, and meaningful downside cases.

## 3. Confirmed user decisions

These choices are settled. Do not ask them again.

1. **Investment life:** choose the evaluation horizon from the proposed assets' and systems' economic lives. Explain the choice and test alternative horizons. Do not keep extending the horizon until IRR passes.
2. **Objective:** prioritise consolidated group operating-profit improvement, with investment economics and service safeguards also reported. Use NPV to assess value across mutually exclusive investment alternatives; do not rank different-sized projects solely by IRR.
3. **Budget:** no approved investment ceiling or required payback period exists. Evaluate a range of investment packages and show efficient trade-offs and break-even spending. Do not invent an approved budget.
4. **Operating scope:** compare both software-led coordination/allocation and more capital-intensive physical expansion. Include software-only, targeted shifts/vehicles/upgrades, and larger physical investment alternatives where supportable.
5. **Profit constraint:** the recommended rollout must preserve positive annual consolidated group operating-profit growth from Year 1. This is stricter than merely remaining profitable. Test it explicitly; do not disguise a failure.
6. **Commercial scope:** isolate logistics economics first. Hold underlying transaction demand and monetisation constant between each policy and its matching counterfactual. Additional demand, fee relief, retention gains, and shipping subsidies belong in separate optional extensions, not the core benefit calculation.
7. **Geography:** use a national financial perspective through transparent representative delivery-market types, plus a more detailed real-geography-grounded Greater Jakarta model for the prototype.
8. **Risk preference:** favour strong expected performance with tolerable downside; also display the maximum-expected-return alternative and explain the trade-off.
9. **Assumptions:** independently research and choose all other technical and financial assumptions, with provenance and sensitivity testing.
10. **Prototype AI:** no live Jev integration is required. A later prototype may use rule-based or scripted incident assessment labelled as a demo. Do not make AI API calls a dependency of this analysis.

## 4. Authoritative casebook extract

Source: *Casebook Preliminary IBSC 2026*, International Business Solution Competition 2026. The originating chat inspected the supplied 18-page PDF and verified the constraint page visually. Page numbers below are PDF page numbers and match printed numbering on the cited pages.

### Operational matrix — page 7

| KPI | 2024 | 2025 |
|---|---:|---:|
| GMV | Rp560 trillion | Rp600 trillion |
| Platform revenue | Rp45 trillion | Rp60 trillion |
| Reported take rate | 8% | 10% |
| Marketing expense | Rp28 trillion | Rp24 trillion |
| Average delivery cost per parcel | Rp12,000 | Rp10,000 |
| Operating profit or loss | −Rp3 trillion | +Rp5 trillion |
| Annual small-seller churn | 7% | 12% |

Take rate is revenue divided by GMV. The exact implied 2024 ratio is 45/560, approximately 8.0357%; the exhibit reports a rounded 8%.

### Additional operating data — page 10

| Measure | Value |
|---|---:|
| Annual parcels delivered in 2025 | 2 billion |
| NexExpress share of parcels in 2025 | 50% |
| Average cost per NexExpress parcel | Rp8,000 |
| Average cost per third-party courier parcel | Rp12,000 |
| Small sellers active at beginning of 2025 | 1.2 million |
| Repeat-buyer rate, 2024 to 2025 | 62% → 57% |

No order count, active-buyer count, route-level costs, network map, internal capacity, 2024 parcel volume, delivery failure rates, or definitions of the churn/repeat cohorts are supplied.

### Seller segments — page 10

| Segment | 2025 GMV, Rp trillion | 2025 platform revenue, Rp trillion | Annual churn |
|---|---:|---:|---:|
| Small sellers / MSMEs | 200 | 20 | 12% |
| Mid-size sellers | 220 | 22 | 5% |
| Other Segments | 180 | 18 | 2% |

Retain the label Other Segments. The case does not define it as large sellers or brands. Equal implied segment revenue/GMV ratios do not establish equal commission schedules or contribution margins.

### Competitors — page 8

| Indicator | Nexora | Scrolla | Avori | Borong.id |
|---|---:|---:|---:|---:|
| 2025 GMV, Rp trillion | 600 | 330 | 180 | 90 |
| Reported GMV growth | 7% | 32% | 3% | 6% |
| Reported take rate | 10% | 6% | 8% | 7% |
| General free shipping | No, targeted incentives only | Yes | Limited | Yes, with minimum spend |
| Delivery cost per parcel, Rp | 10,000 | 12,500 | 11,000 | 11,500 |

Competitor profitability, service levels, and subsidy funding are not supplied. Do not infer them from these figures.

### Market — page 9

| Measure | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| Market growth | 9% | 14% | 11% |
| Nexora GMV value share | 50% | 48% | 46% |
| Scrolla share | 14% | 21% | 25% |
| Avori share | 20% | 15% | 14% |
| Borong.id share | 8% | 7% | 7% |
| Other players | 8% | 9% | 8% |

Displayed values are rounded and do not fully reconcile when reverse-engineered. Preserve reported values rather than silently changing them.

### Background and management positions — pages 4–6

Nexora gradually raised commissions, reduced broad promotions, and increased internal delivery. Commission schedules vary approximately 8%–20%+ by category, plus service fees; these are not the same as the blended revenue/GMV take rate. Logistics contributes to revenue as well as cost, but recognition and internal-transfer details are absent.

Management emphasises growing profit, cheaper current internal delivery, seller variety, and data/automation at scale. The logistics director's view that internal delivery is cheaper does not establish that the next parcel on every remaining lane is cheaper internally.

### Mandatory constraints — pages 11–12

- Profit growth must remain positive and sustainable.
- Digital technology and innovation must form the core driver.
- Additional assumptions must be realistic, explicit, and consistent with case facts.
- External references are permitted.
- Evaluate financial impact and operational feasibility with credible evidence and rigorous reasoning.

The user's Year-1 annual profit-growth interpretation is specified in Section 3. A positive project NPV does not override a failure of this separate constraint.

### Competition context — pages 14–15

The preliminary executive summary is limited to three pages excluding cover, references, and appendix; references use APA style. Deadline stated in the supplied casebook: 1 November 2026 at 23:59 GMT+7. Rubric: problem analysis 20%, strategic solution 30%, impact/feasibility 30%, data/evidence 15%, essay structure 5%. Your current deliverables are analytical files, not that submission. Provide a few concise exhibits and defensible conclusions that can later support it.

## 5. Accounting and interpretation boundaries

Use these checks before designing the model:

- Current blend: 0.5 × Rp8,000 + 0.5 × Rp12,000 = Rp10,000 per parcel.
- Assuming aligned cost and volume scopes, implied delivery spending is 2bn × Rp10,000 = Rp20tn, comprising Rp8tn internal and Rp12tn external. This is derived, not an audited logistics P&L.
- Rp600tn / 2bn = Rp300,000 **GMV per parcel**, not proven average order value.
- Rp60tn / 2bn = Rp30,000 platform revenue per parcel on an aggregate basis; not marginal contribution per new parcel.
- Rp60tn − Rp24tn marketing − Rp5tn operating profit = Rp31tn other operating costs including logistics.
- Subtracting the derived Rp20tn delivery cost leaves Rp11tn as a conditional residual. It is not verified fixed overhead, technology expense, or a directly observed cost bucket. Do not confidently forecast it as wholly fixed.
- For unchanged volume and constant unit costs, shifting 10 percentage points internally mechanically saves Rp0.8tn annually. This is a reference calculation, not a forecast after capacity investment or changed route mix.
- Every Rp1,000 per parcel at two billion parcels equals Rp2tn annually. Use this as a unit sanity check.
- Current average cost is not marginal cost. The current internal network may already serve easier or denser lanes.
- Nexora–NexExpress internal transfers do not create consolidated profit. Do not invent new external revenue from transfer pricing.
- Include technology and expansion costs once, and distinguish capital expenditure from depreciation and recurring expense.
- Do not double-count failed-delivery expense already included in a cost estimate.
- A seller departure is not proportional GMV loss. A five-percentage-point repeat-buyer change is not automatically parcel growth or churn.
- Buyer retention, seller retention, and parcel growth can refer to the same underlying transactions; do not add them as independent benefits.
- Lower logistics cost alone does not prove improved buyer/seller retention. Report those as strategic hypotheses unless supported by additional evidence.

A prior informal proposal targeted 65–85% internal delivery and Rp5,000–6,000 blended costs. **These are not approved constraints or validated targets.** Do not centre the analysis on achieving them. At 80% internal share and Rp12,000 external cost, a Rp6,000 blend requires Rp4,500 internal cost; a Rp5,000 blend requires Rp3,250. Let the model establish what is plausible.

## 6. Research and evidence protocol

For each input distinguish:

1. CASE FACT — from the extract, with page.
2. DERIVED — arithmetic from case or external observations, with formula.
3. EXTERNAL OBSERVATION — primary-source benchmark with geography, date, unit, scope, and URL.
4. ASSUMPTION — an authored input or distribution, with reasoning and alternatives.

Prefer original datasets, official statistics, operator disclosures, official tariffs, primary research, and tool documentation. Check source applicability rather than collecting large volumes of citations. A public courier tariff is not internal marginal cost. A foreign efficiency estimate is not a Nexora saving coefficient.

For important assumptions record low/central/high or distribution parameters, correlation logic, impact sensitivity, and confidence in provenance. Distinguish parameter uncertainty from random operating variability. Do not claim that Monte Carlo confidence under assumed distributions is empirical confidence about Nexora.

Record retrieval dates, dataset versions, licenses/attribution, failures, and data-quality limitations. Do not use unrelated or poorly matched data simply to increase the number of sources. Do not silently replace inaccessible data with invented observations.

## 7. Geography workstream

### Required investigation

Inspect and selectively use https://github.com/opengeos/geoai-skills for actual geographic grounding. It is a Claude Code plugin built on the GeoAI Python library, not guaranteed to be a drop-in plugin in your environment. Inspect current instructions and dependencies before use. If its launcher is unavailable, use compatible underlying Python/library or direct-data workflows, recording the route actually used. Do not claim the plugin executed if you merely followed its methods.

Relevant repository capabilities identified during planning include geographic inspection, Overture data extraction, raster processing, STAC imagery search, and imagery-based object detection. Overture workflows can retrieve buildings, places, transportation segments, and connectors. Primary transportation reference: https://docs.overturemaps.org/guides/transportation/ . Verify current coverage and schemas yourself.

Use existing mapped features first. Do not make satellite object detection mandatory when roads/buildings are already available. Some imagery workflows are US-specific, so check Indonesian coverage before choosing one. Additional sources such as OpenStreetMap, Indonesian official statistics, or gridded population products may be used where relevant and accessible; investigate rather than assume availability or completeness.

### Geographic analysis tasks

- Select and document a bounded Greater Jakarta study area: Jakarta, Bogor, Depok, Tangerang, Bekasi as appropriate to available data and feasible scope.
- Retrieve real geographic features and inspect coordinate systems, geometries, completeness, dates, and attributes.
- Construct a connected road-network representation with an appropriate buffer beyond the study boundary. Handle direction/access restrictions where available, disconnected components, and unreachable destinations explicitly.
- Use network travel distances for hub-to-zone accessibility. Label travel times as estimates unless sourced from actual measured times. Speed limits are not observed speeds; congestion needs separate assumptions or evidence.
- Select a manageable zoning resolution based on the analysis. Compare at least one alternative zoning or demand-distribution assumption to avoid false precision.
- Create transparent synthetic parcel-demand allocations using suitable settlement/population/building/activity proxies. These are not measured Nexora order locations. Normalise the chosen regional volume explicitly and vary proxy weights.
- Place **hypothetical** existing and candidate facilities at plausible accessible locations. Actual warehouse geometry does not establish NexExpress ownership or spare capacity.
- Calculate catchments, hub-to-zone distance/time matrices, service feasibility, and spatial cost drivers.
- Export an actual geographic decision layer: preferred delivery mode under each selected policy, marginal cost advantage, capacity pressure, and uncertainty/switching where supportable.

Use suitable geospatial tools as needed; you need not use deep learning to justify the work. Avoid arbitrary straight lines across barriers in the analytical routing network. Simplified lines may be used for visual overview only if the underlying distances are network-derived and the distinction is clear.

### National versus regional treatment

The case's two billion parcels are national annual volume. The Greater Jakarta volume is an assumption requiring a documented allocation method; do not treat all national parcels as local or reuse an arbitrary demonstration volume as observed data.

Use representative national delivery-market types with explicit weights and assumptions, such as dense urban, suburban/periurban, lower-density regional, and difficult/inter-island service where relevant. Weights must reconcile with national volume and baseline allocation/cost anchors. Test alternative weights. Do not multiply one Jakarta cost saving uniformly across the entire country. Label extrapolated results as modelled national scenarios.

## 8. Required analysis 1 — Baseline economics

Reconcile the baseline case, cost scopes, units, national annual and regional daily scales. Build a matching counterfactual for each forecast period. Keep demand and monetisation identical between policy and counterfactual in the core analysis; shared background inflation or exogenous changes may be modelled symmetrically and disclosed.

Use an incremental bridge from reported group operating profit where the case lacks a reliable full cost breakdown. Do not manufacture a fully identified historical P&L.

Baseline calibration should reproduce the 50% internal share and aggregate Rp8,000/Rp12,000 costs. A single calibration match does not identify fixed/variable splits or unique cost curves. Document alternative plausible decompositions and test their consequences.

Output baseline ledger, provenance, formulas, residual treatment, and assumptions.

## 9. Required analysis 2 — Marginal cost and capacity

Construct an explicit, operationally interpretable cost function:

- Existing committed capacity and utilisation.
- Avoidable/incremental labour, distance, vehicle time, fuel, handling, dispatch, and redelivery costs.
- Cost spreading as utilisation increases, where justified.
- Overtime, queues, missed cut-offs, and overflow near capacity.
- Discrete added shifts, vehicles, sorting upgrades, facilities, or collection points where applicable.
- Implementation delays, ramp-up, spare capacity, replacement expenditure, and stranded costs.
- External carrier tariffs, capacity, service availability, and possible repricing/contract effects.

Identify where the next increment of internal allocation is attractive relative to the actual alternative. Ensure spillovers between zones and shared hub capacity are respected; individually cheap zones may not all be simultaneously feasible.

Deliver marginal and average cost curves, capacity thresholds, expansion steps, and a geographic map of cost advantage. Do not hard-code a U-shaped curve or an interior optimum just to make 100% internal look bad. Any internal share can win if supported by the defined conditions.

## 10. Required analysis 3 — Policy and investment comparison

Distinguish decision variables from uncertain world conditions.

Decisions may include lane/zone allocation, overflow rules, dispatch/consolidation, added shifts, vehicles, hub upgrades, and phased investment. Uncertainties may include demand, travel time, cost inflation, productivity, failures, and implementation outcomes.

At minimum compare:

- Current 50/50 aggregate allocation, respecting its assumed geography.
- Simple feasible allocation/overflow rules.
- Software-led coordination/allocation with existing assets.
- Targeted capacity upgrades.
- More capital-intensive expansion.
- A capacity-aware recommended policy and a highest-expected-return alternative if different.

Evaluate no-investment alternatives fairly, including their costs and limitations. Do not award an intervention savings for capabilities implicitly assumed absent without explanation.

A grid or other transparent search is acceptable. Use a suitable solver if warranted. Report the best **evaluated** feasible policy unless global optimality is established. Target internal share and feasible realised internal share are different fields; unused capacity, unserved demand, and outsourced overflow must be visible.

Create:

1. A numeric heatmap with internal-share policies versus demand conditions, with expected incremental contribution and infeasible cells.
2. A companion geographic allocation/cost-advantage layer.
3. A policy comparison table including service and investment.

For each heatmap point compare against the counterfactual under the same demand level. Define the demand axis separately from stochastic demand variation around that level. Do not subtract a fixed 2025 profit from every higher-demand scenario and call all volume benefit policy benefit.

## 11. Required analysis 4 — Monte Carlo, stress, and sensitivity

Actually execute the numerical analysis, with recorded seeds, code, run counts, and runtime. Use seeded stochastic sampling so results are reproducible and policies encounter matched operating worlds. Preserve independent random-variable identities where possible when policy structures differ.

Start with a pilot performance/convergence check. A suggested plan is approximately 100 policy candidates × 1,000 sampled worlds for screening, then approximately 10,000 fresh worlds for shortlisted policies. Adjust to computational feasibility and convergence; these are planning sizes, not achieved results or mandatory wasteful counts. Do not claim a completed 10,000-run surface if only finalists received that many runs.

Document distributions, plausible correlations, constraints, and truncation. Include structural sensitivity to cost-curve forms, geographic allocation, demand proxies, and national weights, not just random noise around one preferred model.

Report expected/median outcomes, downside percentiles, share of runs improving over baseline, service violations, investment exposure, and policy-ranking stability. If you use a risk penalty or service threshold, specify and justify it and test alternatives. A 10th percentile outcome is not a 90% confidence interval for a real-world causal effect.

Stress at least: campaign surge, reduced hub capacity, corridor/travel-time disruption, weak productivity improvement, higher implementation costs, and external-carrier repricing. Include cases where the intervention is neutral or loses. Evaluate shortlisted policies on fresh draws rather than reporting only selection-sample winners.

Provide a sensitivity/tornado exhibit and break-even thresholds: which assumptions would reverse the recommendation, or cause it to miss profit/service requirements?

## 12. Required analysis 5 — Financial and service impact

### Profit and cash flow

Build a transparent consolidated operating-profit bridge and separate incremental investment cash-flow model. Account for technology implementation, recurring software/cloud/AI costs where relevant, integration, training, labour changes, transition costs, depreciation, maintenance, replacement, working capital, and taxes using researched or disclosed assumptions.

Use unlevered incremental project cash flows as the default; do not invent financing arrangements or present project IRR as equity IRR. Match nominal/real and currency treatment between cash flows and discount rates. Research a defensible nominal IDR discount-rate range; do not label an assumed hurdle rate as Nexora's observed WACC.

Choose the horizon from economic lives and rollout timing. Avoid a perpetuity terminal value in the main case. Use supported residual/salvage values, replacement, and decommissioning where relevant; expose any terminal-value dependence separately.

Calculate NPV, project IRR/XIRR as appropriate, payback, discounted payback, peak funding need, and break-even investment. For no-investment policies, IRR may be undefined; report N/A rather than fabricate it. If cash-flow sign changes produce multiple or unreliable IRRs, emphasise NPV and explain the issue. Do not silently turn operating profit into cash flow.

The user's desired hurdle is **IRR above the chosen discount rate**, with positive NPV over a justified horizon. This is an evaluation criterion, not permission to manufacture success. If it cannot be met, report that and investigate a smaller or differently phased policy within plausible assumptions.

### Annual growth constraint

Starting from reported 2025 group operating profit of Rp5tn, report annual group operating profit, year-on-year growth, the corresponding counterfactual, and incremental policy impact. Explicitly test positive annual profit growth from Year 1 and through the modelled horizon. Merely being above Rp5tn every year is insufficient if a later year declines.

Do not force the counterfactual or savings trajectory to make this pass. If no supported policy satisfies the user's constraint and investment criteria, state so and show the binding conditions and nearest feasible alternatives.

### Service safeguards

Define a manageable set of modelled measures: on-time performance or service feasibility, overflow/unserved parcels, backlog, and capacity utilisation. Justify thresholds, and distinguish daily planning feasibility from an empirically calibrated delivery probability. Cheap but infeasible policies must not win.

Do not claim a modelled service improvement has demonstrated a buyer-repeat or seller-retention effect. A concise strategic interpretation is welcome, but leave unmeasured benefits unquantified.

### Optional extensions

Only after completing core logistics analysis, optionally show separately budgeted subsidy reinvestment or commercial growth scenarios. Require incremental contribution to cover incentives, additional fulfilment, and related costs. No survey-derived elasticity is available in this brief. Keep these extensions out of headline core savings.

## 13. Prototype handoff requirements

The other chat will likely use React, TypeScript, Vite, Three.js, ECharts, Zustand, and browser Web Workers. Data and calculation semantics matter more than framework-specific code.

Three target screens:

1. Network Control Room: regional twin, facilities, routes, allocation, utilisation, costs, selected scenario, and controls.
2. Policy Lab: numeric Monte Carlo heatmap, policy comparison, downside distribution, assumptions, and apply-policy action.
3. Incident Response: capacity/corridor disruption, structured demo assessment, feasible action comparison, and before/after consequences.

The twin replays one selected world; the heatmap summarises multiple worlds. All displays must consume a consistent selected scenario. No live Jev, real company telemetry, or production authentication is required.

Provide:

- Stable zone, hub, lane, policy, scenario, and intervention IDs.
- Versioned JSON schema/data dictionary, units, time bases, and financial scope.
- Clear separation of case constants, researched inputs, assumptions, decisions, draws, and results.
- Slider ranges and defaults justified by analysis; do not assume a previous UI fixture is a factual constraint.
- Formulas/pseudocode sufficient to reimplement the numerical engine in TypeScript.
- Seed/random-generation specification if cross-language replication is expected. Otherwise export sampled worlds so both implementations can use identical inputs.
- Small reference test fixtures with expected outputs and tolerances to verify workbook/Python/frontend parity.
- Numeric heatmap cells and feasibility reasons, not only chart images.
- Geographic layers and network-derived route geometry or clearly labelled visual simplifications.
- One worked incident, such as hub capacity loss, with feasible alternatives and reconciled cost/volume effects. Keep dispatch-window and daily totals distinct.
- Provenance and simulated-status labels that can be surfaced in an assumptions drawer.

Do not place heavy raw geospatial datasets inside browser JSON. Supply simplified display layers and compact analytical matrices, retaining full-resolution source layers separately. Keep displayed precision appropriate to source uncertainty.

## 14. Required deliverables

Deliver actual files with usable links. Suggested package:

### A. `Nexora_Logistics_Analysis.xlsx`

A well-formatted workbook containing at least:

- Read Me and model scope.
- Case facts and baseline reconciliation.
- Source and assumption register.
- Geography/zone summaries and national weighting.
- Marginal cost and capacity functions.
- Investment alternatives and rollout.
- Policy comparison and numeric heatmap.
- Monte Carlo summary, recorded samples/draw references, and sensitivity.
- Operating-profit bridge and incremental project cash flows.
- NPV/IRR/payback and service safeguards.
- Executive findings and validation checks.

Use editable formulas for deterministic financial and operating calculations where practical. Label externally computed simulation results as imported results. Include formula caches or recalculated values so the workbook opens with meaningful numbers. Do not require macros. Changing a financial assumption should update linked formulas; changing a simulation parameter may require rerunning the supplied script, and the workbook must say so. Do not imply imported Monte Carlo tables automatically recalculate in Excel.

### B. Prototype-ready data

Prefer separate compact JSON/GeoJSON files for assumptions/configuration, policies, heatmap, selected outcomes, incidents, facilities/zones/routes, and reference test fixtures. A combined file is acceptable if well structured. Include valid JSON values, explicit null handling, and stable units; no NaN/Infinity.

### C. Geospatial evidence

GeoPackage or equivalent analytical layers; source/data dictionary and attribution. Preserve necessary source references and reproducible retrieval/preparation scripts. Package feasible scoped inputs, not an indiscriminate country-scale download. State any redistribution restrictions.

### D. Reproducible code

Python scripts/notebooks or another suitable executable workflow for data preparation, cost calculations, policy search, Monte Carlo, exports, and QA. Include dependency versions, exact commands, seeds, and fallback routes. Do not leave the core findings dependent on inaccessible chat-only calculations.

### E. `Nexora_Methodology_and_Findings.md`

Explain data access, geography, accounting, assumptions, policy search, uncertainty, validation, findings, limitations, and recommended rollout. Include APA-style external references with URLs and dates. State what was actually executed versus only proposed.

### F. `Nexora_Prototype_Handoff.md`

Document the result schema, calculation rules, state transitions, illustrative/demo boundaries, reference fixtures, and the few analytical conclusions the UI should communicate. A ZIP containing deliverables and a concise manifest is useful in addition to the main XLSX link.

### G. `Nexora_Master_Context_Pack.md`

This is a mandatory additional deliverable. The user explicitly wants to preserve the new chat's important context so another assistant can continue without the conversation history. It is a continuity record, not just an executive summary.

**Create it early and update it at major milestones**, after substantive decisions, after corrections or changes in scope, and before context compaction when feasible. Produce a final version after all outputs and validation results are known. Do not rely on remembering the whole session at the end. Maintain this file through the available persistent artifact/file workflow; keep reproducible working checkpoints where appropriate.

The final pack must contain:

1. **Read first and current state:** purpose, latest status, completed work, outstanding work, and a navigation guide. Distinguish verified execution, assumptions, proposed future work, and failed or blocked work.
2. **Original incoming context:** preserve this entire handoff document in a clearly delimited appendix, unchanged, including the confirmed user choices and case extract. A reference to a file that may not be available in a later chat is not sufficient. Avoid recursive copies of earlier pack versions; keep the initial brief once and a versioned change log.
3. **User steering and scope changes:** important subsequent user instructions, preferences, constraints, and authorisations, with exact wording where needed for meaning. Clearly identify changes that supersede the incoming brief.
4. **Decision register:** stable IDs, what was chosen, rationale, alternatives considered, reasons for rejecting or deferring them, evidence relied on, and whether the user approved the decision or the analyst chose it under delegated authority.
5. **Assumption register:** final values, ranges/distributions, units, provenance category, reasoning, correlations, revisions, sensitivity, and remaining uncertainty. Include evaluation life, discount rate, financial treatment, economic/physical life distinctions, geographic weights, demand proxies, costs, capacity, and service thresholds.
6. **Source and geography record:** exact source URLs, retrieval dates, dataset/repository versions or commit IDs where available, geographic scope, coordinate systems, coverage gaps, licenses, and actual access routes. Do not describe a catalogued dataset as downloaded or inspected unless it was.
7. **Model specification:** accounting boundaries, counterfactuals, equations, cost-curve forms, allocation rules, investments, rollout, demand normalisation, national extrapolation, cash-flow construction, risk objectives, and constraints. Preserve consequential implementation details needed to reproduce the results.
8. **Executed analysis record:** actual candidate counts, sampled-world counts, seeds, held-out evaluation design, distribution parameters, scenario definitions, software/dependency versions, runtime where measured, validation results, and outputs. Distinguish plans from achieved work.
9. **Findings and interpretation:** the recommended policy, alternatives, financial and service effects, break-even points, downside cases, structural sensitivities, and boundaries of what the evidence supports. Preserve failed or unfavourable results relevant to the recommendation.
10. **Corrections and abandoned approaches:** what was wrong or changed, why, and which former figures or conclusions must no longer be used. Label historical entries as superseded rather than leaving contradictory figures unresolved.
11. **Output manifest:** exact final filenames, available artifact IDs/links, schema versions, paths, checksums where practical, and what each file contains. Include the workbook, spatial outputs, JSON, code, findings, and prototype handoff. Do not invent identifiers or depend on temporary execution paths as the only locator.
12. **Prototype continuation:** which outputs drive each of the three screens, shared state and units, reference fixtures, simulated versus observed fields, known performance limitations, and remaining UI decisions.
13. **Open issues and next actions:** unresolved analytical questions, dependencies, limits, and a copy-ready continuation prompt for the prototype-building chat. The next assistant should not need to ask the user to repeat settled decisions.

Use a concise current-state section plus detailed appendices. The pack must be self-contained for understanding the work, while clearly identifying companion data/code files required to rerun it; it need not duplicate every raw geospatial feature or Monte Carlo draw. Do not replace specifics with statements such as “see earlier conversation.” Preserve analytical reasoning and decision rationale, not private hidden reasoning. Do not include credentials or unnecessary personal data.

If the session must end before all work is complete, deliver an updated partial pack with exact completed and pending status. At final completion, reconcile the pack against the actual delivered files and results. Provide the master pack as its own downloadable MD file in addition to any ZIP.

## 15. Validation and completion gates

Complete relevant checks before delivery:

- Baseline identities and national-volume weights reconcile.
- Allocations conserve parcels: demand equals internal + external + explicitly unserved/deferred quantities for the defined window. Backlog carries over if modelled.
- Hub/vehicle/shift capacity and service constraints are respected or violations reported.
- Distance units, coordinate systems, daily/annual scaling, and monetary magnitudes are correct.
- Unreachable road-network locations are not treated as zero distance.
- Fixed costs, expansion spending, depreciation, technology fees, subsidies, and internal transfers are not double-counted.
- No savings are credited for unchanged capabilities in the counterfactual.
- Cash-flow/NPV/IRR calculations reconcile; Excel beginning-period cash flows are handled correctly.
- Year-on-year group profit growth and project investment criteria are separately checked.
- Seeded results reproduce, comparisons use matched worlds, and finalist results use fresh draws.
- The recommended policy is not an accidental winner from one assumed geographic distribution, cost-curve form, or expansion threshold.
- JSON/GeoJSON is valid; IDs and units match tables and workbook; reference fixtures agree across outputs.
- Workbook formulas do not contain errors or broken external links, and charts/labels are readable.

Use a concise execution plan initially, then proceed autonomously through analysis and delivery. Keep the user updated at meaningful milestones. Finish with the actual recommendation, key conditions, principal risks, executed run counts, and file links, including the separate final master context pack. If a tool or source is blocked, use a materially suitable documented fallback where possible and report the precise remaining limitation. Do not fabricate acquisition, runs, validation, or results.
