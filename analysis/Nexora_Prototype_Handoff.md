# Nexora Prototype Handoff

Schema version 1.0.0 · October 27, 2026

## Read first

Build the three screens in the next chat. No website was built or deployed here. Read the master pack, findings, `data/config.json` and reference fixtures first. Treat all operating allocations, capacities and demand locations as modelled. The original casebook PDF was not inspected.

No national rollout clears all requirements in the central model. All **133 evaluated policies fail positive annual group operating-profit growth** in at least one year under flat commercial demand and monetisation, 2.5% nominal logistics cost inflation, and zero other net operating-profit change. Positive incremental project value does not override this constraint.

The best evaluated investment candidate under the stated service and downside preference is **P_SOFTWARE_70_88**. It uses software-led allocation with an 88% capacity buffer setting and a 70% maximum internal-share ceiling. Its realised internal share is only **53.7%** in held-out worlds. The ceiling is not a forecast of 70% insourcing.

Central initial spending is Rp180 billion of software/integration capex, Rp1.8 billion of working capital, and Rp60 billion of Year 1 transition expense. The five-year central NPV is **Rp0.573 trillion** at 14%, project IRR **92.6%**, payback **1.40 years**, and discounted payback **1.57 years**. The asymmetric overrun distribution raises expected initial capex to Rp204.4 billion.

Across 10,000 held-out worlds, mean NPV is **Rp0.509 trillion**, p10 NPV **Rp-0.161 trillion**, and **80.5%** of worlds have positive NPV. These describe the authored distributions, not empirical confidence about Nexora.

The existing-TMS rules package is a close challenger. The software candidate exceeds `P_RULES_70_88` by only Rp40.5 billion mean NPV and wins 52.4% of matched worlds. The paired p10 difference is Rp-253.7 billion. Urban-heavy weights favour rules, while regional-heavy weights make both lose. This supports validating the rules/configuration alternative before committing to software. No pilot has occurred.

The maximum expected-return alternative is `P_SOFTWARE_75_100`, with mean NPV Rp1.016 trillion. It has planning-service violations in 27.9% of worlds and fails the selected service safeguard. Large physical expansion loses value in the central model. Targeted capacity can become preferable under a higher fixed-cost decomposition or a flatter marginal route-mix gradient.

## Screen inputs

| Screen | Main payloads | Scope |
|---|---|---|
| Network Control Room | regional_outcomes, facilities, decision_zones, routes, selected_outcomes | Separate regional daily and national annual views |
| Policy Lab | policies, heatmap, cost_curves, worlds_reference | Distribution summaries versus one selected world |
| Incident Response | incidents, shared scenario state | Four-hour dispatch window plus unchanged eight-hour component |

`data/policies.json` contains 133 screened policies and 14 fresh finalists. `recommended_candidate` is conditional; `recommendation_eligible_full_rollout` is false. `selected_outcomes.json` is one deterministic central world per finalist, not the Monte Carlo mean. `heatmap.json` has 66 numeric cells, realised shares and feasibility reasons. The requested share is a ceiling. False feasibility can mean the requested share was not attained; show the actual fallback result explicitly.

`geo/*.geojson` contains nine analytical square catchments, four hypothetical clusters and schematic corridor lines. `routes.json` has 36 coarse Dijkstra lane estimates. Local-access distance is null. Do not label these as acquired street geometry, official boundaries or measured travel times. `regional_outcomes.json` is a separate regional transport LP; never multiply its saving across the country.

## Shared state and identifiers

Use one state object with `policyId`, `scenarioId`, `worldId`, `demandAxis`, `financeControls`, `activeIncidentActionId`, `scope` (national/regional) and `engineVersion`. Each change produces one result consumed by all three screens. The twin replays one world; the heatmap aggregates worlds. Keep central, mean and percentile labels distinct.

Stable IDs are `P_*` policy, `S_*` scenario, `Z_00`–`Z_08` zone, `H_*` facility, `L_*` lane, `C_00`–`C_16` corridor, `A_*` action, `W_*` sampled world and `F_*` fixture. Unknown/unreachable/unsupported values are null, never zero. Each JSON payload carries schema version 1.0.0; GeoJSON properties carry status labels.

| Scope | Volume | Cost |
|---|---|---|
| National operating model | Billion parcels/year | Rp trillion/year; IDR/parcel inputs |
| National finance | Annual time-zero/end-year cash flows | Nominal Rp trillion |
| Regional planning | Parcels/day | IDR/day |
| Incident | Parcels/four-hour window | IDR/four-hour window |

Sanity check: two billion parcels × Rp1,000 = Rp2 trillion. Do not confuse GMV/parcel with order value or marginal revenue. Every demand-axis point uses a matching counterfactual.

## Numerical port

Port `code/model.py` before adding assumptions. Use float64 and stable descending sort over 96 tranches; ties retain type/tranche order. There are 24 tranches/type. Positive-saving parcels are accepted up to the share ceiling, then rollout/adoption is applied. `demand = internal + external + deferred`; capacity overflow must remain visible. Current geography is fixed except forced overflow.

Use exported draws rather than recreating PCG64 in TypeScript. `worlds_reference.json` has 200 worlds. `results/worlds_holdout_10000.npz` contains all 10,000 with named arrays, and `finalist_npvs.npz` contains matched outcomes. A conversion step can create a compact browser binary. Each policy receives identical draw identities; do not reseed per policy.

```text
cost = fixed + v*q/1000
       + k*max(q-.85K,0)^2/(.30K)/1000
       + b*max(q-q0,0)^2/(2*max(D-q0,epsilon))/1000
       + external_price*external_q/1000
```

Calibration removes baseline overtime from the variable intercept. Software affects only 65% of variable cost. Package recurring/fixed cost, rollout, transition, depreciation and replacement follow Python. No internal transfers, subsidies or retention benefits are added. Finance uses incremental EBITDA less tax/capex/replacement/working-capital changes plus salvage. Group OP uses the incremental bridge in the findings. Check each annual change from the Rp5 trillion 2025 anchor separately from NPV/IRR.

The regional solver is a shared-capacity transport LP, not a vehicle-routing problem. Replay its exported results or use a deterministic LP solver. A heuristic needs its own label and checks. Distances are graph attributes containing assumptions; display chords are not analytic routes. Actual road/ramp/turn/local-access verification is still required.

## Controls

Analysed share ceilings: 45–95% in 5-point steps. Demand axis: 80–140% of the two-billion workload; random variation is separate. Buffers: 88%, 94%, 100%. Default conditional candidate: `P_SOFTWARE_70_88`. Financial defaults: five years, 14% nominal IDR discount, 22% tax, 2.5% logistics inflation, zero other net OP increase. Three-/seven-year and 11–18% discount sensitivities are included. Regional volume fraction is assumed at 20%, with a 12–25% control range requiring LP refresh.

Imported heatmaps do not update from arbitrary slider movement. Recompute in a Web Worker or snap to an analysed cell and label it. Do not offer 80% insourcing or Rp5,000 costs as established targets.

## Incident calculation

`S_HUB_CAW_4H_LOSS` reduces one cluster by 50% for four hours of a 12-hour day. Choose one action and calculate daily variable cost as unchanged eight-hour cost plus the selected four-hour action. Add committed daily cost once. Internal/external/emergency/deferred quantities must reconcile. Deferred four-hour volume is backlog; no automatic same-day clearance is assumed. Scripted assessment must say demo. No live Jev, authentication, telemetry or AI API dependency exists.

Loading this incident sets shared `policyId` to its exported `base_policy_id` (`P_RULES_70_88`), `worldId` to `central`, and scope to `regional`. Do not leave the other screens showing a software world while applying a rules-based incident. Regional `capacity_daily_planning` includes the policy buffer/ceiling; `physical_hub_utilisation` and `unused_capacity_daily` refer to available physical capacity. Keep these definitions distinct.

## Parity and continuation

Verify `F_BASE_2025`, `F_CENTRAL_RECOMMENDED` and `F_INCIDENT` before UI polish. Tolerances: money 1e-8 Rp tn, ratios 1e-8, national volume 1e-9 billion, regional money Rp1. LP assignment ties may differ while objective/conservation/capacity match. Test those first.

Remaining UI decisions are renderer, charts, worker batch size and draw subset. No frontend exists yet, so TypeScript parity has not been tested. Preserve the failed annual-profit gate and partial detailed-GIS status prominently. No external deployment was requested.
