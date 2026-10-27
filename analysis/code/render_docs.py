"""Readable report and continuity exports; no chat history required."""
from pathlib import Path
import json,platform
import numpy as np
import scipy,matplotlib
from model import ROOT,write_json

def read(name):return json.loads((ROOT/name).read_text())

def render(a,p,checks,sources,assumptions):
 r=a['recommended'];m=a['maxreturn'];out=read('data/selected_outcomes.json')['outcomes'];o=out[r['policy_id']];f=o['financial']
 npvs=np.load(ROOT/'results/finalist_npvs.npz');paired=npvs[r['policy_id']]-npvs['P_RULES_70_88']
 facts=f"""No national rollout clears all requirements in the central model. All **133 evaluated policies fail positive annual group operating-profit growth** in at least one year under flat commercial demand and monetisation, 2.5% nominal logistics cost inflation, and zero other net operating-profit change. Positive incremental project value does not override this constraint.

The best evaluated investment candidate under the stated service and downside preference is **{r['policy_id']}**. It uses software-led allocation with an 88% capacity buffer setting and a 70% maximum internal-share ceiling. Its realised internal share is only **{r['realised_internal_share']:.1%}** in held-out worlds. The ceiling is not a forecast of 70% insourcing.

Central initial spending is Rp180 billion of software/integration capex, Rp1.8 billion of working capital, and Rp60 billion of Year 1 transition expense. The five-year central NPV is **Rp{f['npv']:.3f} trillion** at 14%, project IRR **{o['irr']:.1%}**, payback **{o['payback']:.2f} years**, and discounted payback **{o['discounted_payback']:.2f} years**. The asymmetric overrun distribution raises expected initial capex to Rp{r['initial_capex_tn']*1000:.1f} billion.

Across 10,000 held-out worlds, mean NPV is **Rp{r['expected_npv_tn']:.3f} trillion**, p10 NPV **Rp{r['p10_npv_tn']:.3f} trillion**, and **{r['prob_positive_npv']:.1%}** of worlds have positive NPV. These describe the authored distributions, not empirical confidence about Nexora.

The existing-TMS rules package is a close challenger. The software candidate exceeds `P_RULES_70_88` by only Rp{paired.mean()*1000:.1f} billion mean NPV and wins {np.mean(paired>0):.1%} of matched worlds. The paired p10 difference is Rp{np.percentile(paired,10)*1000:.1f} billion. Urban-heavy weights favour rules, while regional-heavy weights make both lose. This supports validating the rules/configuration alternative before committing to software. No pilot has occurred.

The maximum expected-return alternative is `{m['policy_id']}`, with mean NPV Rp{m['expected_npv_tn']:.3f} trillion. It has planning-service violations in {m['service_violation_world_fraction']:.1%} of worlds and fails the selected service safeguard. Large physical expansion loses value in the central model. Targeted capacity can become preferable under a higher fixed-cost decomposition or a flatter marginal route-mix gradient.
"""
 ids=['P_CURRENT','P_RULES_70_88',r['policy_id'],m['policy_id'],'P_TARGETED_75_100','P_LARGE_85_100']
 table='| Policy | Mean NPV, Rp tn | p10, Rp tn | Service-violation worlds | Year 1 incremental EBIT, Rp tn |\n|---|---:|---:|---:|---:|\n'
 for id in ids:
  s=next(x for x in p['finalists'] if x['policy_id']==id)
  table+=f"| {id} | {s['expected_npv_tn']:.3f} | {s['p10_npv_tn']:.3f} | {s['service_violation_world_fraction']:.1%} | {s['expected_y1_ebit_tn']:.3f} |\n"
 growth='| Model year | Current-policy group OP, Rp tn | Candidate group OP, Rp tn | Candidate YoY growth |\n|---|---:|---:|---:|\n'
 for i,(cv,pv,chg) in enumerate(zip(f['cfprofit'],f['profit'],f['growth_amount'])):
  growth+=f"| {2026+i} | {cv:.3f} | {pv:.3f} | {chg/(5 if i==0 else f['profit'][i-1]):.1%} |\n"
 apa={
 'CASE':'International Business Solution Competition. (2026). *Casebook preliminary IBSC 2026* [Case extract transcribed in the supplied handoff].',
 'SRC_GEOAI':'Opengeos. (n.d.). *geoai-skills* [Computer software]. GitHub.',
 'SRC_OVERTURE':'Overture Maps Foundation. (2026). *Transportation guide* [Release 2026-10-21.0 documented].',
 'SRC_BPJT':'Badan Pengatur Jalan Tol. (2023, June 22). *Dirgahayu Kota Jakarta ke-496, ini dia beragam jalan tol yang ada di Jakarta*.',
 'SRC_KEPPRES':'Republic of Indonesia. (1981). *Keputusan Presiden Republik Indonesia Nomor 38 Tahun 1981 tentang penetapan jalan bebas hambatan dan jembatan menjadi jalan tol dan jembatan tol*.',
 'SRC_BPS_DKI':'Badan Pusat Statistik Provinsi DKI Jakarta. (2025). *Population, population growth rate, percentage distribution, population density, and population sex ratio by regency/municipality* [Statistical table].',
 'SRC_BPS_JABAR':'Badan Pusat Statistik Provinsi Jawa Barat. (2025). *Proyeksi penduduk di Provinsi Jawa Barat menurut jenis kelamin dan kabupaten/kota* [Statistical table].',
 'SRC_DJP':'Direktorat Jenderal Pajak. (n.d.). *Income tax calculation mechanism entity*.',
 'SRC_BI':'Bank Indonesia. (2026, October 21). *BI-Rate tetap 5,75%: Memperkuat stabilitas, mendorong pertumbuhan ekonomi* [Press release].',
 'SRC_ADB':'Asian Development Bank. (n.d.). *AsianBondsOnline: Indonesia market watch* [Market data, October 23, 2026 snapshot].',
 'SRC_JT':'J&T Express. (2026, April 1). *J&T Express reports 18.5% YoY revenue growth for FY2025* [Press release].',
 'SRC_ARCGIS':'DKI Jakarta. (n.d.). *Peta Jalan DKI* [Feature service metadata].',
 'SRC_OSM':'OpenStreetMap contributors. (n.d.). *OpenStreetMap and Overpass API* [Data service].'}
 references='\n\n'.join(f"**{s['id']}** — {apa[s['id']]} {s['url'] or 'Full supplied extract preserved in the master pack'}. Retrieved October 27, 2026. Access: {s['access']}" for s in sources)
 method=f"""# Nexora Methodology and Findings

Version 1.0.0 · October 27, 2026 · Nominal IDR unless stated

## Recommendation and binding conditions

{facts}
{table}
Do not approve a national rollout from this package alone. Obtain actual lane/hub costs and capacity, verify carrier reservations, validate the group-profit bridge, and compare a bounded existing-TMS configuration against incremental software. These are proposed next steps, not executed interventions.

## Historical baseline and accounting

The original casebook PDF was not supplied to this chat. Historical facts use the self-contained Markdown handoff, preserved unchanged in the master context pack. No personal inspection of the original PDF is claimed.

The baseline blend is `50% × 8,000 + 50% × 12,000 = Rp10,000/parcel`. With two billion annual parcels, this implies Rp20 trillion delivery spending: Rp8 trillion internal and Rp12 trillion external, conditional on matching scopes. GMV per parcel is Rp300,000 and aggregate platform revenue per parcel Rp30,000. Neither is a proven average order value or marginal contribution. Revenue minus marketing and operating profit gives Rp31 trillion of other costs, including logistics. Subtracting the derived Rp20 trillion leaves a conditional Rp11 trillion residual; it is not identified fixed overhead.

The model therefore uses an incremental bridge from reported 2025 operating profit of Rp5 trillion. Commercial demand and monetisation match between a policy and its counterfactual. Parcel-workload variations receive no invented incremental GMV or margin. Counterfactual cost uses the same demand, traffic, inflation and capacity world. Other net operating-profit change is a separate explicit assumption, centrally zero. This does not classify the Rp11 trillion residual as wholly fixed.

There are no retention, subsidy, print-on-demand or fee-relief benefits in core savings. Internal Nexora–NexExpress transfers create no consolidated revenue. Failure costs, maintenance, capex, depreciation, transition and recurring technology costs are each included once.

## National capacity and marginal costs

Four authored market types have parcel weights 35% dense urban, 30% suburban, 25% regional and 10% difficult. Historical internal shares are 80%, 60%, 16% and 0%, giving 50% nationally. Type internal averages are Rp7,000, Rp8,500, Rp12,750 and Rp18,000. External prices are Rp10,000, Rp11,000, Rp12,000 and Rp14,600. Weighted historical internal/external costs reproduce Rp8,000/Rp12,000. The unused difficult-market internal cost is not identified by that calibration.

Assumed annual internal capacity is 0.64/0.43/0.13/0.02 billion parcels. It represents the minimum of sortation, linehaul and courier ceilings. Reference linehaul/courier ceilings are 1.05/1.10 times the sorter limit; the upgrade assumes all three expand. The workbook includes fleet/labour equivalents, not an observed fleet inventory. Spare capacity is a consequential unverified assumption.

For each type, with volumes in billion parcels and costs in Rp trillion:

```text
cost = F + v*q/1000 + overtime + route_mix + external_price*external_q/1000
overtime = k/2 * max(q - 0.85K, 0)^2 / (0.15K) / 1000
route_mix = b/2 * max(q - q0, 0)^2 / max(D - q0, epsilon) / 1000
```

Committed fixed cost is initially 25% of historical internal cost. The variable intercept removes historical overtime before calibration. Fixed costs stay committed when parcels are moved elsewhere. Structural alternatives use 10% and 40% fixed shares. Marginal route-mix gradients are Rp3,500/6,000/10,000/14,000; zero and 1.8-times gradients are also tested. Average costs are outputs of these components; no U-shaped curve or interior optimum is imposed.

The allocator divides each type’s feasible capacity into 24 tranches, ranks 96 midpoint marginal savings against external delivery, fills positive-saving tranches up to the chosen maximum internal share, and applies rollout/adoption. Shared capacity is respected at the national type-pool level; the regional model uses actual shared hub constraints within its hypothetical facility structure. A share ceiling may not be reached because of capacity or economics. Several 75–95% ceilings produce identical outcomes. This is a transparent approximate search, not proof of a global optimum.

Current policy already has normal routing and a TMS. Rules receive allocation improvements and pay configuration/oversight/training costs, but no software productivity or capacity gain. Software centrally improves only 65% of variable cost by 3%, with 2% capacity release at that productivity. Physical expansion pays committed costs even if its capacity is unused. Finite external capacity can cause explicit deferred parcels, charged an authored escalation/recovery cost without inventing lost GMV.

## Investment alternatives and rollout

Software capex is Rp180 billion: Rp120 billion development and Rp60 billion capitalisable integration. Annual recurring opex is Rp45 billion and Year 1 transition Rp60 billion. Rules have no capitalised investment, Rp8 billion annual oversight/configuration opex and Rp15 billion Year 1 transition. These are analyst estimates, not quotes.

Targeted physical investment is Rp850 billion plus the software package, adding 190 million annual parcels of capacity. Large physical investment is Rp3.6 trillion plus software, adding 600 million. Physical costs are split 30% vehicles/linehaul equipment, 40% sortation and 30% leasehold upgrades. Additional fixed cash costs are Rp150/Rp550 billion annually, ramped with deployment. Physical maintenance is 3% of physical capex and already included in recurring operating cost.

Rules ramp 85%/100%; software 55%/90%/100%; targeted 35%/80%/100%; large 15%/60%/90%/100%. Adoption uncertainty modifies these. Upfront investment is paid at time zero; phased deployment and partial first-year depreciation are explicit. Existing committed network costs do not disappear.

## Geographic access and the delivered fallback

The `opengeos/geoai-skills` README and Overture skill instructions were inspected. It is a Claude Code plugin using `geoai-py`. That launcher and GeoAI/GeoPandas were unavailable. No plugin execution is claimed. Overture’s documented 2026-10-21.0 transportation schema was inspected, including segments/connectors and access/direction concepts; no Overture dataset was downloaded. The repository commit could not be pinned because the commit endpoint was inaccessible.

Direct raw GitHub and Overpass requests returned 403. API queries through the research service were inaccessible, and the cloud browser’s ArcGIS request was denied by the environment. BPS population values were primary-source search-index observations; direct BPS pages returned 403. These failures are recorded precisely. No roads, buildings, settlement raster or full-resolution administrative boundaries were downloaded.

The delivered fallback contains 16 approximate named corridor nodes, 17 undirected corridors (34 directed arcs), nine analytical catchments, four hypothetical facility clusters and 36 hub-zone matrix entries. Selected markets lie within approximately 106.50–107.05°E and 6.09–6.65°S, covering Jakarta and Bogor/Depok/Tangerang/Bekasi corridors. This is not the complete administrative union or the requested detailed buffered street extract.

BPJT textual concession lengths are preserved with attribution. Subsection and local-access lengths are separately marked as assumptions. The historical 16 km Cawang–Tomang alignment is not a verified current measurement. Coordinates and square polygons are authored display anchors, not official boundaries. Endpoint lines are schematic and never used as chord routing distances.

Dijkstra actually runs on the coarse corridor graph’s length attributes. These are network-derived corridor estimates containing assumptions, not measured or OSM shortest street paths. Two-way van/truck access is assumed; toll-road motorcycle access is excluded. Ramp, turn, freight and local-access restrictions remain unverified. The coarse graph is connected with no unreachable delivered pairs. Local-access distance remains null. The supplied optional street script requests a buffered OSM extract, retains shared-node topology and direction/access tags, avoids joining grade-separated crossings, and leaves unreachable routes null. It has not completed a download here.

Regional volume is explicitly assumed at 20% of national volume: 400 million parcels/year, approximately 1.096 million/day over 365 days. Nine broad catchment weights blend 80% population proxies with 20% authored activity scores. They are not Nexora orders or measured merchant locations. Population-only, activity-only, uniform, and an 18-child-zone representation were executed. The regional transport LP respects shared facility and carrier capacities and estimated 120-minute one-way corridor feasibility. It is not a last-mile vehicle-routing solution. Regional results do not get multiplied across the national two billion parcels.

Detailed street/building acquisition, coverage, buffered topology, actual access restrictions and last-mile routing remain **PARTIAL**. The fallback supports prototype scenario design, not real dispatch certification.

## Executed simulation and uncertainty

- Pilot: 250, 500 and 1,000 worlds for convergence/performance comparison.
- Screening: 133 policies × 1,000 matched worlds.
- Fresh shortlist: {a['finalists']} candidates × 10,000 held-out worlds.
- Heatmap: 66 cells × 1,000 held-out worlds per cell.
- Structural sensitivity: eight variants × {a['finalists']} candidates × 2,000 worlds.
- Regional switching: 200 worlds; regional LP/proxy comparisons and the incident executed separately.

Screen seed is 20261027; holdout seed 20261101; regional seed 73027. Sampling uses NumPy PCG64. Final national analysis runtime was {a['runtime_seconds']:.2f} seconds, excluding document/workbook generation and subsequent QA. Earlier provisional runs are superseded by the final exported run.

Persistent parameter uncertainty includes triangular productivity (0, 0.03, 0.07), adoption (0.5, 0.9, 1.05), overrun (0.9, 1, 1.5), inflation (0, 0.025, 0.06), and common demand/cost factors. Annual operating variation includes lognormal demand/travel/input/carrier factors, capacity noise and a separate daily surge. Demand and travel share a normal factor; input and carrier price share a cost factor. Exact coefficients, truncation and array identities are in `model.py` and the assumption register. Central planned execution is not the mean of asymmetric draws.

Policy loops do not consume random numbers. Each receives matched named draws. The package exports 200 JSON reference worlds plus all 10,000 compressed held-out worlds. Frontend parity can use those draws without implementing PCG64. Recommended mean-NPV Monte Carlo standard error is Rp{r['npv_mcse']*1000:.2f} billion. Percentiles quantify the chosen distribution, not empirical uncertainty about a causal Nexora effect.

Adaptive allocation treats rates, traffic and capacity as if observable for planning. A fixed-priority structural variant tests this optimistic information assumption. Risk score is `E[NPV] - 0.5*(E[NPV]-p10)`, also tested at weights 0, 0.25 and 1. A current-policy or smaller-investment alternative can win.

## Service safeguards

The model requires at least 99.5% of annual parcels served and 95% planning feasibility. A sampled world violates if any model year breaches either. The candidate must have no more than 10% violating worlds and must not worsen matched current-policy mean planning feasibility or world-violation frequency. These thresholds are authored safeguards, not supplied case SLAs or calibrated delivery probabilities.

The selected candidate has violations in {r['service_violation_world_fraction']:.2%} of worlds, versus 6.86% for current policy. Expected explicitly deferred quantity is about {r['mean_unserved_parcels_annual']:,.0f} parcels/year; it is not hidden by a high percentage served. Peak-day feasibility uses a separate daily disturbance from the annual demand axis. No modelled service improvement is converted into buyer/seller retention revenue.

## Cash flow, horizon and annual profit growth

The main five-year horizon covers the software/vehicle cycle, with three- and seven-year alternatives. Economic lives are four years for software, five for vehicles, eight for sortation and ten for leasehold improvements. Half-year first/last depreciation is an accounting convention. Software refresh is 50% of initial software cost in Year 5; vehicle replacement occurs in Year 6 for the seven-year case. No perpetuity terminal value is used. Physical salvage is 35% of remaining physical book value; software salvage is zero. Working capital is 1% of software plus 2% of physical capex, released at the selected horizon.

Unlevered nominal IDR cash flows use a 14% authored discount rate, tested at 11–18%. ADB’s 5-year sovereign yield of 7.245% and 10-year 7.446%, together with BI’s 5.75% policy rate, provide context. The project risk premium is authored; this is not observed Nexora WACC. General corporate tax of 22% is sourced to DJP. Listed-company relief is unverified, and negative incremental EBIT receives no immediate tax credit.

```text
incremental benefit = matching current cost - policy operating cost
EBITDA = benefit - transition expense
EBIT = EBITDA - depreciation
tax = max(EBIT, 0) * tax_rate
FCF = EBITDA - tax - capex - replacement - working_capital_change + salvage
group OP = 5 - (matching current logistics cost - 20)
           + elapsed_year * other_net_OP_increase + incremental EBIT
```

Upfront cash flow is time zero, outside the period-one range in Excel NPV. IRR is project IRR, not equity IRR. No financing is invented. Current/rules have no initial capital outlay and their IRR is N/A. Payback and funding are separately reported.

{growth}
Central Year 1 group OP is Rp{f['profit'][0]:.3f} trillion versus Rp5 trillion in 2025, despite positive incremental logistics EBIT. A constant annual increase in other net operating contribution of just over **Rp{a['minimum_annual_nonlogistics_ebit_increase_tn']*1000:.1f} billion/year** is needed to make every central annual change strictly positive. This is a break-even condition, not an assumed or validated commercial benefit.

The candidate’s central break-even initial capex is about Rp{a['break_even_initial_capex_tn']*1000:.1f} billion with the stated linked transition, refresh and tax treatment. It is not an approved budget. Delivery cost stays around Rp9,800/parcel in 2025-price terms; the model does not support Rp5,000–6,000 blended costs.

## Stress, reversals and incident

Nine stress definitions were executed: campaign surge, 30% capacity loss, 60% travel disruption, weak productivity, 60% implementation overrun, carrier price +20%, carrier price −20%, combined downside, and upside execution. Neutral and losing results remain in the exported tables. High fixed-cost and flat route-mix structures can favour targeted expansion. Regional-heavy weights can favour current policy over software/rules. The calibration does not uniquely identify the cost curve.

The incident is 50% loss of Cawang-cluster capacity for a four-hour window in a 12-hour planning day. That is a 16.67% daily-capacity reduction, not a 50% whole-day loss. Actions freeze the original assignment and defer displaced parcels, reallocate through remaining hubs/reserved carriers, or add up to 40,000 emergency 3PL parcels at Rp14,000. The four-hour and daily totals reconcile, and backlog is explicit. Assessment is scripted demo logic; no AI API calls occurred.

## Validation and remaining limitations

Baseline identities, alternative-weight recalibration, parcel conservation, capacity constraints, seeded reproducibility and re-execution of 10,000 recommended-candidate NPVs pass. All 133 central annual-growth failures are detected. JSON exports reject NaN/Infinity. Workbook deterministic financial formulas are editable; imported simulation tables require script refresh. Workbook formula/cache/input-change/render checks are recorded separately.

Remaining dependencies are detailed GIS, actual network ownership/capacity, lane-level avoidable cost, external contracts, implementation quotes, empirical service observations, survey/interview results and a supported consolidated group-profit forecast. No causal retention effect or demand elasticity has been measured. The package provides conditional opportunity analysis and prototype inputs, not an empirically validated digital twin.

## References and actual access

{references}
"""
 (ROOT/'Nexora_Methodology_and_Findings.md').write_text(method)
 handoff=f"""# Nexora Prototype Handoff

Schema version 1.0.0 · October 27, 2026

## Read first

Build the three screens in the next chat. No website was built or deployed here. Read the master pack, findings, `data/config.json` and reference fixtures first. Treat all operating allocations, capacities and demand locations as modelled. The original casebook PDF was not inspected.

{facts}
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

Analysed share ceilings: 45–95% in 5-point steps. Demand axis: 80–140% of the two-billion workload; random variation is separate. Buffers: 88%, 94%, 100%. Default conditional candidate: `{r['policy_id']}`. Financial defaults: five years, 14% nominal IDR discount, 22% tax, 2.5% logistics inflation, zero other net OP increase. Three-/seven-year and 11–18% discount sensitivities are included. Regional volume fraction is assumed at 20%, with a 12–25% control range requiring LP refresh.

Imported heatmaps do not update from arbitrary slider movement. Recompute in a Web Worker or snap to an analysed cell and label it. Do not offer 80% insourcing or Rp5,000 costs as established targets.

## Incident calculation

`S_HUB_CAW_4H_LOSS` reduces one cluster by 50% for four hours of a 12-hour day. Choose one action and calculate daily variable cost as unchanged eight-hour cost plus the selected four-hour action. Add committed daily cost once. Internal/external/emergency/deferred quantities must reconcile. Deferred four-hour volume is backlog; no automatic same-day clearance is assumed. Scripted assessment must say demo. No live Jev, authentication, telemetry or AI API dependency exists.

Loading this incident sets shared `policyId` to its exported `base_policy_id` (`P_RULES_70_88`), `worldId` to `central`, and scope to `regional`. Do not leave the other screens showing a software world while applying a rules-based incident. Regional `capacity_daily_planning` includes the policy buffer/ceiling; `physical_hub_utilisation` and `unused_capacity_daily` refer to available physical capacity. Keep these definitions distinct.

## Parity and continuation

Verify `F_BASE_2025`, `F_CENTRAL_RECOMMENDED` and `F_INCIDENT` before UI polish. Tolerances: money 1e-8 Rp tn, ratios 1e-8, national volume 1e-9 billion, regional money Rp1. LP assignment ties may differ while objective/conservation/capacity match. Test those first.

Remaining UI decisions are renderer, charts, worker batch size and draw subset. No frontend exists yet, so TypeScript parity has not been tested. Preserve the failed annual-profit gate and partial detailed-GIS status prominently. No external deployment was requested.
"""
 (ROOT/'Nexora_Prototype_Handoff.md').write_text(handoff)
 source_record='# Source and Acquisition Record\n\nRetrieved October 27, 2026.\n\n'+ '\n\n'.join(f"## {s['id']}\n\n{s['title']}\n\n- URL: {s['url'] or 'Incoming handoff'}\n- Access: {s['access']}\n- Scope: {s['scope']}\n- Observation: {s['observation']}\n- License: {s['license']}" for s in sources)
 (ROOT/'evidence/Source_and_Acquisition_Record.md').write_text(source_record)
 write_json('data/sources.json',dict(schema_version='1.0.0',sources=sources))
 write_json('data/assumptions.json',dict(schema_version='1.0.0',assumptions=assumptions))
 decisions=[
 ('D001','Preserve settled choices and analysis-only scope','User-authorised incoming brief. No website, deployment or communications.'),
 ('D002','Use an incremental group-profit bridge','The case residual does not identify a full historical P&L. Zero other net contribution is disclosed, not a fixed-overhead fact.'),
 ('D003','Evaluate five years, test three/seven','Software/vehicle commercial cycle; refresh, replacement and conservative residuals are explicit.'),
 ('D004','Use 14% nominal IDR discount, test 11–18%','Authored premium above sourced sovereign benchmarks. Not observed Nexora WACC.'),
 ('D005','Separate national types from regional LP','Do not multiply a Jakarta saving uniformly across national parcels.'),
 ('D006','Use a labelled corridor fallback','Acquisition restricted. Full street/building validation remains PARTIAL; no invented observed features.'),
 ('D007','Retain an existing-TMS rules challenger','Current operations already have routine technology. Software receives only incremental productivity and capacity benefits.'),
 ('D008','Identify a conditional software candidate','Risk score plus no worse matched service. This is not rollout approval.'),
 ('D009','Reject unconditional national rollout','Zero of 133 central policies pass every annual profit-growth test.'),
 ('D010','Export named draws for frontend parity','Do not rely on cross-language PCG64 implementations. Keep float64 and stable tranche ties.')]
 decision_text='\n\n'.join(f"**{id}: {choice}.** {why} {'User-authorised.' if id=='D001' else 'Analyst chosen under delegated authority.'}" for id,choice,why in decisions)
 assumption_text='\n\n'.join(f"**{x['id']} — {x['name']}**\n\nValue: `{json.dumps(x['value'])}` {x['unit']}. Low/high: `{json.dumps(x['low'])}` / `{json.dumps(x['high'])}`. Category: {x['category']}. {x['reason']} Correlation: {x['correlation']}. Confidence: {x['confidence']}. Source: {x['source'] or 'Analyst-authored'}. Refresh: {x['refresh']}" for x in assumptions)
 source_brief='\n\n'.join(f"**{s['id']}** — {s['url'] or 'Supplied handoff'}. Version/date: {s['date']}. Scope: {s['scope']}. Actual access: {s['access']} License: {s['license']}" for s in sources)
 incoming=(ROOT/'evidence/Incoming_Handoff.md').read_text()
 pack=f"""# Nexora Master Context Pack

Version 1.0.0 · October 27, 2026

## Read first and current state

National analysis, financial modelling, policy search, simulation, stress, structural sensitivity, prototype data, workbook and reports are complete within documented access limits. **Detailed street/building geospatial acquisition remains PARTIAL.** The regional package is a labelled corridor fallback. No website was built or deployed.

No evaluated national rollout satisfies the strict central annual group-profit-growth gate. Do not describe positive project NPV as investment approval. Read `Nexora_Methodology_and_Findings.md`, then `Nexora_Prototype_Handoff.md`, `data/config.json` and `data/reference_fixtures.json`. The ZIP contains all companion data, code, draws and evidence. The original incoming brief is preserved unchanged once at the end of this pack.

## User steering and scope

The exact instruction was: **“Run this. Good luck”**. No subsequent user steering changed the brief. The user delegated remaining researched assumptions, not deployment or external communications. All confirmed choices in the original brief remain binding. No survey findings or completed interviews were supplied. Print-on-demand, retention, fee relief, subsidies and new commercial demand remain outside core benefits.

## Completed and outstanding

Completed: baseline reconciliation; primary-source research and access attempts; 133-policy screening; 14 fresh finalists; 66 numeric heatmap cells; nine stresses; eight structural variants; three-/five-/seven-year finance; regional nine-/18-zone/proxy LP comparisons; 200 switching worlds; a four-hour incident; JSON/GeoJSON, fixtures, code and workbook exports; analytical and workbook QA.

Outstanding: actual buffered street/building/settlement data, detailed access/turn restrictions, real lane/hub/fleet costs and capacities, implementation quotes, carrier reservations, empirical service calibration, survey/retention effects, supported group-profit forecasts, prototype implementation and TypeScript parity. Pilots and rollout stages are proposals, not completed actions.

## Decision register

{decision_text}

## Findings and investment interpretation

{facts}
{table}
Central annual candidate group OP: `{f['profit']}` Rp tn. Matching current-policy group OP: `{f['cfprofit']}`. Cash flows: `{f['flows']}` Rp tn, including time zero. Central project NPV: `{f['npv']:.12f}` Rp tn; IRR `{o['irr']:.12f}`; payback `{o['payback']:.9f}` years; discounted payback `{o['discounted_payback']:.9f}`; peak funding `{o['peak_funding_tn']:.9f}` Rp tn.

Annual-growth passes: **0/133**. Required constant annual increase in other net operating contribution: more than `{a['minimum_annual_nonlogistics_ebit_increase_tn']:.9f}` Rp tn/year. This is a break-even requirement, not a supported benefit. Central break-even initial capex: `{a['break_even_initial_capex_tn']:.9f}` Rp tn under linked transition/refresh/tax treatment. No approved budget exists.

The model does not support Rp5,000–6,000 blended delivery costs. A regional-heavy national mix reverses software/rules value, while high committed fixed costs or a flat marginal route-mix gradient can favour targeted expansion. Preserve these unfavourable findings when continuing.

## Model specification

National units are billion parcels/year, IDR/parcel and Rp trillion. Four market weights are 35/30/25/10%; historical internal shares 80/60/16/0%. Weighted costs reproduce 50% internal share and Rp8,000/Rp12,000. Capacity is 0.64/0.43/0.13/0.02 billion, interpreted as the minimum of sorter, linehaul and courier ceilings. Upgrades must expand all three.

For each type, q0 = two billion × weight × historical share. Fixed cost is 25% of historical internal spending. The variable intercept equals average cost × (1 − fixed share), less historical overtime per parcel. Overtime and route-mix equations are in the findings and `model.py`. Allocation uses 24 tranches/type, 96 stable-ranked midpoint savings, positive avoidable savings only, a share ceiling, then adoption/ramp. Carrier capacity and explicit deferred handling are finite. Fixed costs remain committed.

Rules receive allocation benefits only. Software affects 65% of variable cost, with a central 3% component improvement and 2% capacity release. Physical capex and fixed/maintenance costs remain even if capacity is unused. No internal-transfer, subsidy or retention revenue is credited. Matching worlds keep demand and commercial economics identical between policy/counterfactual.

Group OP = 5 − (matched current logistics cost − 20) + elapsed year × other net OP increase + incremental policy EBIT. The default other-net term is zero; the residual is not assumed wholly fixed overhead. Demand-axis workload is distinct from random variation around each axis point.

Finance is nominal IDR, unlevered, annual time zero/end-year cash flow. Main horizon five years, alternatives three/seven. Discount 14% (11–18% tested); general CIT 22%; no immediate incremental loss credit. Lives: software four, vehicles five, sortation eight, leasehold ten. Half-year first/last depreciation; 50% software refresh in Year 5; vehicle replacement in Year 6 for longer evaluation. Working capital 1% software plus 2% physical, released at the horizon. Software salvage zero; physical salvage 35% of remaining physical book value. No perpetuity value or invented financing.

## Executed analysis record

Final national runtime: `{a['runtime_seconds']:.3f}` seconds, excluding export and later QA. Pilot sizes: 250/500/1,000. Screening: 133 × 1,000 policy-worlds. Fresh shortlist: 14 × 10,000. Heatmap: 66 × 1,000. Structural sensitivity: eight × 14 × 2,000. Regional switching: 200. Nine central stress definitions are in `results/analysis.json`.

Seeds: 20261027 screening, 20261101 holdout, 73027 regional. NumPy PCG64; Python {platform.python_version()}, NumPy {np.__version__}, SciPy {scipy.__version__}, Matplotlib {matplotlib.__version__}. Full held-out named arrays and policy NPVs are compressed NPZ; 200 reference worlds are JSON. Draws are created outside policy loops. Recommended-candidate NPVs were independently re-executed across all 10,000 worlds and matched saved outcomes.

Persistent parameter uncertainty includes productivity, adoption, overrun, inflation and shared demand/cost factors. Annual operating noise includes travel, demand, input/carrier price, capacity and a separate daily surge. Exact distributions, coefficients, truncation and correlations are in `model.py` and the assumption register below. Demand/travel share a factor; input/carrier prices share another. Adaptive allocation assumes rates/traffic/capacity observable for planning; fixed-priority structural sensitivity was executed. Percentiles are not empirical causal confidence intervals.

The risk score is E[NPV] − 0.5 × (E[NPV] − p10), with 0/0.25/1 alternatives. Service thresholds are 99.5% served, 95% planning feasibility, at most 10% worlds with any annual violation, and no worsening of matched current mean feasibility or world-violation frequency. Annual profit growth remains a separate gate.

## Source, geography and access record

{source_brief}

All retrieval dates are October 27, 2026. `evidence/Source_and_Acquisition_Record.md` and `data/sources.json` preserve exact URLs, scope, status and attribution. No GeoAI plugin, Overture extract, OSM street extract, object detection or GeoPandas execution occurred. The repository main commit was not retrievable; do not invent a commit. Overture 2026-10-21.0 was a documented release, not downloaded data.

The executed regional route uses official textual corridor descriptions/lengths plus authored subdivisions and display coordinates. There are 16 nodes, 17 corridors/34 directed arcs, nine square catchments, four hypothetical facility clusters and 36 lanes. CRS is OGC:CRS84 (longitude, latitude). Corridor endpoint lines are schematic; their geometric chord lengths are never the analytical distance. Dijkstra operates on stored attributes. Ramp/turn/freight/local-access restrictions are unresolved. All delivered coarse pairs are connected; unsupported local-access distances are null. The detailed buffered retrieval script is a future fallback, not successful acquisition.

Regional volume is 400 million/year on 365 days, an assumed 20% national allocation. Population/activity weights are 80/20; activity is authored. Population-only, activity-only, uniform and 18-child-zone comparisons were executed. Regional daily costs and national annual calibrated costs are separate. Do not extrapolate one Jakarta saving uniformly.

## Assumption register

{assumption_text}

## Corrections and superseded approaches

1. The initial shortlist retained only expected-NPV winners. It missed lower-buffer rules/software candidates. The final shortlist adds service/risk candidates by family and contains 14. Any provisional targeted-investment recommendation is superseded.
2. An intermediate absolute 10% service limit allowed `P_SOFTWARE_60_94` despite worse mean service than current. Final eligibility also checks no worsening of matched current mean feasibility and world-violation frequency. `P_SOFTWARE_70_88` is the final conditional investment candidate.
3. Alternative national weights initially would have changed historical anchors. Final `market_inputs` recalibrates type shares and costs at each weight set. Independent QA verifies Rp20 trillion spending and 50% internal share.
4. Detailed road acquisition failed. Never relabel the fallback as an OSM street network, the square zones as official boundaries, or authored travel times as measured.
5. Several high share ceilings have identical realised allocations. They do not imply 75–95% realised internal delivery.
6. Software economic life is four years, while the evaluation horizon is five. Three/seven-year alternatives include refresh/replacement; the horizon was not extended until IRR passed.

## Validation and manifest

Analytical validation results:

{json.dumps(checks,indent=2)}

Workbook formula, cache, input-change, native-table and visual checks are recorded in `results/workbook_validation.json`. Final filenames, roles, sizes and SHA-256 hashes are in `MANIFEST.json`. Companion data/code are in the complete ZIP. The separate persisted master pack replaces the early checkpoint at `libfile_528fff67c6108191833dbc3d4c8746d3`. Artifact receipts and final workbook verification are appended after final saving; no credentials or signed transfer URLs are retained.

## Prototype continuation

Network Control Room consumes regional outcomes, zones, facilities, lanes and a selected central/sample world. Policy Lab consumes policies, numeric heatmap, curves and draws. Incident Response consumes reconciled actions. Share one policy/scenario/world/scope state. Clearly label national annual, regional daily and incident four-hour units, central replay versus distribution summaries, synthetic demand and schematic geometry.

Use the three reference fixtures before UI polish. Tolerances: money 1e-8 Rp trillion, ratios 1e-8, national volume 1e-9 billion, regional money Rp1. No live Jev, AI API, telemetry or authentication is required. Frontend parity is pending because no frontend was built. Detailed GIS and empirical operations remain open dependencies.

## Copy-ready continuation prompt

Read `Nexora_Master_Context_Pack.md`, `Nexora_Methodology_and_Findings.md` and `Nexora_Prototype_Handoff.md`, then inspect the ZIP manifest and reference fixtures. Build the three prototype screens using the exported data and port or replay the engine with one consistent selected scenario/world. Do not reopen settled user choices, claim real telemetry or detailed street acquisition, or hide the failed annual profit-growth gate. Preserve conditional investment status and the costed rules challenger. Verify numerical fixtures before UI polish. Keep national/regional/window units explicit and label synthetic demand and schematic corridors. No external deployment is authorised by this handoff.

## Change log

- Version 0.1: early context checkpoint created and persisted before modelling, with the entire incoming brief.
- Version 1.0.0: final national/corridor analysis, 14 finalists, failed annual-growth gate, documented acquisition limits, exports and validation. Final workbook/save receipts are appended without duplicating the original brief.

## Original incoming context — unchanged

<!-- BEGIN ORIGINAL HANDOFF -->
{incoming}
<!-- END ORIGINAL HANDOFF -->
"""
 (ROOT/'Nexora_Master_Context_Pack.md').write_text(pack)
 (ROOT/'README.md').write_text(f"""# Nexora logistics analysis package

Read the findings and master context pack first. No national rollout clears the strict central annual-profit-growth gate. Detailed street GIS acquisition is partial; regional layers are a labelled corridor fallback.

## Reproduce

Python {platform.python_version()}, NumPy {np.__version__}, SciPy {scipy.__version__}, Matplotlib {matplotlib.__version__}. No package installation was required.

```bash
python code/model.py
python code/geography.py
python code/prepare_deliverables.py
python code/verify_workbook.py
```

Run the workbook builder between preparation and verification. It requires the Codex bundled `@oai/artifact-tool`. Use a private OS temporary directory with a `node_modules` symlink to `CODEX_PRIMARY_RUNTIME_NODE_MODULES`, copy `code/build_workbook.mjs` there, and run it with `CODEX_PRIMARY_RUNTIME_NODE` and `NEXORA_ROOT` set to this package directory. See the builder header and dependency record. A standard Python environment with NumPy/SciPy/Matplotlib can rerun the analysis without workbook authoring.

`python code/retrieve_roads.py` prints the optional buffered request plan. Add `--download` only when Overpass access is available. No successful detailed extract is claimed here. Conditional access and turn restrictions still require additional work afterward.

Simulation tables are imported workbook snapshots. Finance inputs recalculate deterministic cash flows; operating changes require scripts and workbook refresh. Currency is IDR. National financial tables use Rp trillion, regional tables IDR/day and incident tables IDR/four-hour window.
""")
 # Actual per-payload schemas, not a permissive metadata-only placeholder.
 schema={
  '$schema':'https://json-schema.org/draft/2020-12/schema','title':'Nexora payload envelope','type':'object','required':['schema_version'],'properties':{'schema_version':{'const':'1.0.0'}},
  '$defs':{
   'policy':{'type':'object','required':['policy_id','package','target','buffer','expected_npv_tn','realised_internal_share'],'properties':{'policy_id':{'type':'string','pattern':'^P_'},'package':{'enum':['current','rules','software','targeted','large']},'target':{'type':'number','minimum':0,'maximum':1},'buffer':{'type':'number','minimum':0,'maximum':1},'expected_npv_tn':{'type':'number'},'realised_internal_share':{'type':'number','minimum':0,'maximum':1}}},
   'heatmap_cell':{'type':'object','required':['cell_id','target_share','demand_axis','expected_y5_ebit_tn','realised_internal_share','feasible','reasons'],'properties':{'cell_id':{'type':'string'},'target_share':{'type':'number'},'demand_axis':{'type':'number'},'expected_y5_ebit_tn':{'type':'number'},'realised_internal_share':{'type':'number'},'feasible':{'type':'boolean'},'reasons':{'type':'array','items':{'type':'string'}}}},
   'lane':{'type':'object','required':['lane_id','hub_id','zone_id','corridor_network_km','reachable','distance_status'],'properties':{'lane_id':{'type':'string'},'hub_id':{'type':'string'},'zone_id':{'type':'string'},'corridor_network_km':{'type':['number','null'],'minimum':0},'reachable':{'type':'boolean'},'distance_status':{'type':'string'},'local_access_distance_km':{'type':['number','null']}}}},
  'x-units':{'national_volume':'billion_parcels_per_year','national_money':'IDR_trillion','regional_volume':'parcels_per_day','regional_money':'IDR_per_day','incident_volume':'parcels_per_four_hour_window','incident_money':'IDR_per_four_hour_window','coordinates':'longitude_latitude_degrees'},
  'x-null-semantics':'unknown, unreachable or unsupported; never coerce to zero'}
 write_json('data/schema.json',schema)
