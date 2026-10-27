# Model and simulation specification

## Scope and accounting

Case anchors: 2 billion annual parcels, 50% internal delivery, Rp8,000 average internal cost, Rp12,000 external cost, and Rp5 trillion 2025 group operating profit. The implied delivery spend is Rp20 trillion. The full group P&L is not identified by these facts. The default other net operating contribution change is zero; it is a planning assumption.

The four national market types are dense urban, suburban, regional, and difficult/inter-island. Their planning weights are 35%, 30%, 25%, and 10%. These weights do not claim observed Nexora demand shares. Annual commercial demand and monetization remain flat in the central finance case. Changing parcel workload changes logistics workload for both policy and counterfactual; it does not automatically create revenue or customer retention benefits.

## National allocation

For every world and year, the engine computes demand, cost inflation, traffic-sensitive variable cost, available internal capacity and external capacity. Non-current policies rank 24 marginal tranches in each of four types, creating 96 stable-ranked opportunities. It accepts economically beneficial tranches up to the selected ceiling, then applies the package ramp and adoption level. The ceiling can remain inactive when additional insourcing has no economic value.

The model retains committed fixed costs. Internal overtime and route-mix costs rise nonlinearly. External reservations are finite. Unserved demand is retained and charged emergency/deferred handling; it does not disappear from parcel conservation.

Planning service is a modeled feasibility measure using annual shortfall, daily surge overload and high-utilization lateness. A world violates the service condition if any year has more than 0.5% annual unserved demand or less than 95% planning service. This is not an observed on-time-delivery rate.

## Investment finance

Cash flow includes initial capex, working capital, transition expense, recurring software and maintenance costs, tax on positive EBIT, depreciation, software refresh in year 5, vehicle replacement in year 6 where relevant, working-capital release and conservative physical salvage.

The default horizon is five years; archived analysis also tests three and seven. The nominal IDR discount rate is 14%, with 11–18% sensitivity. The website calculates NPV, IRR, simple and discounted payback, peak funding and the group operating-profit bridge.

A positive NPV is incremental project value against the same-world counterfactual. It does not imply that total group profit rises in every year. Under the central flat-commercial, 2.5% logistics-inflation, zero-other-contribution assumptions, 0 of the 133 evaluated policies pass the strict annual group-profit-growth condition.

## Reproducible simulation

The archived study screens 133 policies on 1,000 worlds, then evaluates 14 finalists on 10,000 fresh worlds. It includes 66 heatmap cells, stress tests, structural alternatives, matched policy comparisons and a regional incident. Screening seed: 20261027. Holdout seed: 20261101.

The website stores the 10,000 held-out named worlds as JSON. A 200- or 1,000-world browser run uses the first corresponding subset; a 10,000-world run reproduces the full holdout. Each policy receives the same named worlds, avoiding noisy comparisons between unrelated draws.

The archived heatmap uses 1,000 worlds per cell for software at 88% utilization. Browser recalculation uses 100 worlds per cell to keep all 66 cells interactive. The active label distinguishes the reference matrix from the browser result. A cell with an internal ceiling above the economic realization is marked as an inactive ceiling, rather than a hard constraint failure. Service-risk flags remain separate in the interpretation.

Curated stresses include campaign workload, capacity loss, slower travel, weak software productivity/adoption, and implementation overrun. The browser worker applies the same stress transformations as the central view. Custom sliders remain within bounded ranges.

## Regional allocation and geography

The selected Greater Jakarta market assumes 400 million annual parcels, divided by 365 to give approximately 1.096 million parcels/day. Nine zone weights combine 80% population proxy and 20% authored activity. This allocation is not measured parcel demand.

The corridor model contains 16 nodes, 17 corridors, 34 directed arcs, four hypothetical facility profiles and 36 candidate lanes. Distances use a weighted shortest-path corridor graph. Straight drawn lines and square zones are schematic; they are not street routes or cadastral catchments.

The regional continuous transport solver minimizes internal route cost, external carrier cost, emergency capacity and deferred handling. Hub capacities are shared across zones. The current policy holds 50% internal allocation per zone when capacity permits. Targeted packages raise existing capacity by 18%; large expansion activates the Bekasi candidate and multiplies physical capacity by 1.35. Package cost modifiers, handling rates, local productivity and SLA travel limits are team assumptions.

No detailed OSM, Overture, building or settlement extract is included as downloaded measured data. The procedural scene illustrates the operational concept. Regional savings are not multiplied uniformly across Indonesia.

## Incident

Cawang loses 50% of its capacity for four hours of a twelve-hour operating day. This is a 16.67% effective daily loss at that hub: 240,000 becomes 200,000 daily available capacity. The defined incident uses the rules 70/88 policy. The app compares fixed-route deferral, reallocation within existing hubs and reservations, and emergency 3PL capacity.

The four-hour response is combined with the unchanged other eight hours. Daily committed cost is counted once. Deferred volume remains visible. Applying an incident response affects regional operations, while annual project cash flows remain on their explicitly chosen annual scenario.

## Time profiles

Intraday rates use an authored seven-point shape normalized so trapezoidal integration across 07:00–19:00 equals daily regional demand. Weekly multipliers are normalized to an average of one, so a seven-day view sums to seven daily equivalents. The displayed band is a scenario variation around this profile. It is not a trained forecast confidence interval or a measured forecast accuracy claim.

## Reference outcome

For software 70/88: central NPV Rp0.572988151470 trillion; IRR 92.5543%; payback 1.39555 years. Holdout mean NPV Rp0.509018511554 trillion, p10 Rp−0.160507609859 trillion, positive fraction 80.49%, service-violation world fraction 1.79%. Realized internal share differs between the central case (54.7162% in year 5) and the held-out average (53.6786%).

Central annual group profit is approximately Rp4.576T, Rp4.255T, Rp3.780T, Rp3.251T and Rp2.720T. A separate constant annual increase in other net operating contribution must exceed approximately Rp0.531354T/year to close every annual-growth gap. This is a threshold requirement, not a credited benefit.
