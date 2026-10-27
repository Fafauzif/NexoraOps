# Nexora Methodology and Findings

Version 1.0.0 · October 27, 2026 · Nominal IDR unless stated

## Recommendation and binding conditions

No national rollout clears all requirements in the central model. All **133 evaluated policies fail positive annual group operating-profit growth** in at least one year under flat commercial demand and monetisation, 2.5% nominal logistics cost inflation, and zero other net operating-profit change. Positive incremental project value does not override this constraint.

The best evaluated investment candidate under the stated service and downside preference is **P_SOFTWARE_70_88**. It uses software-led allocation with an 88% capacity buffer setting and a 70% maximum internal-share ceiling. Its realised internal share is only **53.7%** in held-out worlds. The ceiling is not a forecast of 70% insourcing.

Central initial spending is Rp180 billion of software/integration capex, Rp1.8 billion of working capital, and Rp60 billion of Year 1 transition expense. The five-year central NPV is **Rp0.573 trillion** at 14%, project IRR **92.6%**, payback **1.40 years**, and discounted payback **1.57 years**. The asymmetric overrun distribution raises expected initial capex to Rp204.4 billion.

Across 10,000 held-out worlds, mean NPV is **Rp0.509 trillion**, p10 NPV **Rp-0.161 trillion**, and **80.5%** of worlds have positive NPV. These describe the authored distributions, not empirical confidence about Nexora.

The existing-TMS rules package is a close challenger. The software candidate exceeds `P_RULES_70_88` by only Rp40.5 billion mean NPV and wins 52.4% of matched worlds. The paired p10 difference is Rp-253.7 billion. Urban-heavy weights favour rules, while regional-heavy weights make both lose. This supports validating the rules/configuration alternative before committing to software. No pilot has occurred.

The maximum expected-return alternative is `P_SOFTWARE_75_100`, with mean NPV Rp1.016 trillion. It has planning-service violations in 27.9% of worlds and fails the selected service safeguard. Large physical expansion loses value in the central model. Targeted capacity can become preferable under a higher fixed-cost decomposition or a flatter marginal route-mix gradient.

| Policy | Mean NPV, Rp tn | p10, Rp tn | Service-violation worlds | Year 1 incremental EBIT, Rp tn |
|---|---:|---:|---:|---:|
| P_CURRENT | 0.000 | 0.000 | 6.9% | 0.000 |
| P_RULES_70_88 | 0.469 | -0.218 | 2.1% | 0.142 |
| P_SOFTWARE_70_88 | 0.509 | -0.161 | 1.8% | 0.062 |
| P_SOFTWARE_75_100 | 1.016 | 0.258 | 27.9% | 0.208 |
| P_TARGETED_75_100 | 0.359 | -0.348 | 6.1% | -0.030 |
| P_LARGE_85_100 | -3.220 | -4.119 | 0.6% | -0.620 |

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
- Fresh shortlist: 14 candidates × 10,000 held-out worlds.
- Heatmap: 66 cells × 1,000 held-out worlds per cell.
- Structural sensitivity: eight variants × 14 candidates × 2,000 worlds.
- Regional switching: 200 worlds; regional LP/proxy comparisons and the incident executed separately.

Screen seed is 20261027; holdout seed 20261101; regional seed 73027. Sampling uses NumPy PCG64. Final national analysis runtime was 15.36 seconds, excluding document/workbook generation and subsequent QA. Earlier provisional runs are superseded by the final exported run.

Persistent parameter uncertainty includes triangular productivity (0, 0.03, 0.07), adoption (0.5, 0.9, 1.05), overrun (0.9, 1, 1.5), inflation (0, 0.025, 0.06), and common demand/cost factors. Annual operating variation includes lognormal demand/travel/input/carrier factors, capacity noise and a separate daily surge. Demand and travel share a normal factor; input and carrier price share a cost factor. Exact coefficients, truncation and array identities are in `model.py` and the assumption register. Central planned execution is not the mean of asymmetric draws.

Policy loops do not consume random numbers. Each receives matched named draws. The package exports 200 JSON reference worlds plus all 10,000 compressed held-out worlds. Frontend parity can use those draws without implementing PCG64. Recommended mean-NPV Monte Carlo standard error is Rp5.78 billion. Percentiles quantify the chosen distribution, not empirical uncertainty about a causal Nexora effect.

Adaptive allocation treats rates, traffic and capacity as if observable for planning. A fixed-priority structural variant tests this optimistic information assumption. Risk score is `E[NPV] - 0.5*(E[NPV]-p10)`, also tested at weights 0, 0.25 and 1. A current-policy or smaller-investment alternative can win.

## Service safeguards

The model requires at least 99.5% of annual parcels served and 95% planning feasibility. A sampled world violates if any model year breaches either. The candidate must have no more than 10% violating worlds and must not worsen matched current-policy mean planning feasibility or world-violation frequency. These thresholds are authored safeguards, not supplied case SLAs or calibrated delivery probabilities.

The selected candidate has violations in 1.79% of worlds, versus 6.86% for current policy. Expected explicitly deferred quantity is about 42,166 parcels/year; it is not hidden by a high percentage served. Peak-day feasibility uses a separate daily disturbance from the annual demand axis. No modelled service improvement is converted into buyer/seller retention revenue.

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

| Model year | Current-policy group OP, Rp tn | Candidate group OP, Rp tn | Candidate YoY growth |
|---|---:|---:|---:|
| 2026 | 4.500 | 4.576 | -8.5% |
| 2027 | 3.988 | 4.255 | -7.0% |
| 2028 | 3.462 | 3.780 | -11.2% |
| 2029 | 2.924 | 3.251 | -14.0% |
| 2030 | 2.372 | 2.720 | -16.3% |

Central Year 1 group OP is Rp4.576 trillion versus Rp5 trillion in 2025, despite positive incremental logistics EBIT. A constant annual increase in other net operating contribution of just over **Rp531.4 billion/year** is needed to make every central annual change strictly positive. This is a break-even condition, not an assumed or validated commercial benefit.

The candidate’s central break-even initial capex is about Rp592.8 billion with the stated linked transition, refresh and tax treatment. It is not an approved budget. Delivery cost stays around Rp9,800/parcel in 2025-price terms; the model does not support Rp5,000–6,000 blended costs.

## Stress, reversals and incident

Nine stress definitions were executed: campaign surge, 30% capacity loss, 60% travel disruption, weak productivity, 60% implementation overrun, carrier price +20%, carrier price −20%, combined downside, and upside execution. Neutral and losing results remain in the exported tables. High fixed-cost and flat route-mix structures can favour targeted expansion. Regional-heavy weights can favour current policy over software/rules. The calibration does not uniquely identify the cost curve.

The incident is 50% loss of Cawang-cluster capacity for a four-hour window in a 12-hour planning day. That is a 16.67% daily-capacity reduction, not a 50% whole-day loss. Actions freeze the original assignment and defer displaced parcels, reallocate through remaining hubs/reserved carriers, or add up to 40,000 emergency 3PL parcels at Rp14,000. The four-hour and daily totals reconcile, and backlog is explicit. Assessment is scripted demo logic; no AI API calls occurred.

## Validation and remaining limitations

Baseline identities, alternative-weight recalibration, parcel conservation, capacity constraints, seeded reproducibility and re-execution of 10,000 recommended-candidate NPVs pass. All 133 central annual-growth failures are detected. JSON exports reject NaN/Infinity. Workbook deterministic financial formulas are editable; imported simulation tables require script refresh. Workbook formula/cache/input-change/render checks are recorded separately.

Remaining dependencies are detailed GIS, actual network ownership/capacity, lane-level avoidable cost, external contracts, implementation quotes, empirical service observations, survey/interview results and a supported consolidated group-profit forecast. No causal retention effect or demand elasticity has been measured. The package provides conditional opportunity analysis and prototype inputs, not an empirically validated digital twin.

## References and actual access

**CASE** — International Business Solution Competition. (2026). *Casebook preliminary IBSC 2026* [Case extract transcribed in the supplied handoff]. Full supplied extract preserved in the master pack. Retrieved October 27, 2026. Access: Incoming Markdown read completely. Original PDF NOT supplied/inspected.

**SRC_GEOAI** — Opengeos. (n.d.). *geoai-skills* [Computer software]. GitHub. https://github.com/opengeos/geoai-skills. Retrieved October 27, 2026. Access: README and overture-data instructions inspected through research service; raw endpoint403; plugin NOT executed.

**SRC_OVERTURE** — Overture Maps Foundation. (2026). *Transportation guide* [Release 2026-10-21.0 documented]. https://docs.overturemaps.org/guides/transportation/. Retrieved October 27, 2026. Access: Documentation inspected; NO Overture dataset downloaded.

**SRC_BPJT** — Badan Pengatur Jalan Tol. (2023, June 22). *Dirgahayu Kota Jakarta ke-496, ini dia beragam jalan tol yang ada di Jakarta*. https://bpjt.pu.go.id/dirgahayu-kota-jakarta-ke-496-ini-dia-beragam-jalan-tol-yang-ada-di-jakarta/. Retrieved October 27, 2026. Access: Page text inspected through research service.

**SRC_KEPPRES** — Republic of Indonesia. (1981). *Keputusan Presiden Republik Indonesia Nomor 38 Tahun 1981 tentang penetapan jalan bebas hambatan dan jembatan menjadi jalan tol dan jembatan tol*. https://bphn.go.id/data/documents/81kp038.pdf. Retrieved October 27, 2026. Access: Research service PDF text inspected, Appendix p.3; no local PDF acquired.

**SRC_BPS_DKI** — Badan Pusat Statistik Provinsi DKI Jakarta. (2025). *Population, population growth rate, percentage distribution, population density, and population sex ratio by regency/municipality* [Statistical table]. https://jakarta.bps.go.id/en/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMyMzMTAw/jumlah-penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-kabupaten-kota-di-provinsi-dki-jakarta.html?year=2025. Retrieved October 27, 2026. Access: Search-index table observations only; direct page403.

**SRC_BPS_JABAR** — Badan Pusat Statistik Provinsi Jawa Barat. (2025). *Proyeksi penduduk di Provinsi Jawa Barat menurut jenis kelamin dan kabupaten/kota* [Statistical table]. https://jabar.bps.go.id/id/statistics-table/2/OTY3IzI%3D/proyeksi-penduduk-di-provinsi-jawa-barat-menurut-jenis-kelamin-dan-kabupaten-kota.html. Retrieved October 27, 2026. Access: Search-index observations only; direct page403.

**SRC_DJP** — Direktorat Jenderal Pajak. (n.d.). *Income tax calculation mechanism entity*. https://www.pajak.go.id/id/node/80250. Retrieved October 27, 2026. Access: Official page inspected.

**SRC_BI** — Bank Indonesia. (2026, October 21). *BI-Rate tetap 5,75%: Memperkuat stabilitas, mendorong pertumbuhan ekonomi* [Press release]. https://www.bi.go.id/id/publikasi/ruang-media/news-release/Pages/sp_2823326.aspx. Retrieved October 27, 2026. Access: Official current release verified through both research engines.

**SRC_ADB** — Asian Development Bank. (n.d.). *AsianBondsOnline: Indonesia market watch* [Market data, October 23, 2026 snapshot]. https://asianbondsonline.adb.org/indonesia/. Retrieved October 27, 2026. Access: Primary market-data portal verified through both research engines.

**SRC_JT** — J&T Express. (2026, April 1). *J&T Express reports 18.5% YoY revenue growth for FY2025* [Press release]. https://www.jtexpress.sg/insights/press-jt-express-reports-18.5-yoy-growth?hs_amp=true. Retrieved October 27, 2026. Access: Operator page inspected.

**SRC_ARCGIS** — DKI Jakarta. (n.d.). *Peta Jalan DKI* [Feature service metadata]. https://gis-dpmptsp.jakarta.go.id/arcgis/rest/services/Hosted/Peta_Jalan_DKI/FeatureServer/1. Retrieved October 27, 2026. Access: Metadata found in search; feature query inaccessible; cloud browser environment denied URL. NO features downloaded.

**SRC_OSM** — OpenStreetMap contributors. (n.d.). *OpenStreetMap and Overpass API* [Data service]. https://overpass-api.de/api/interpreter. Retrieved October 27, 2026. Access: Direct API403; research-service API queries inaccessible. NO road extract acquired.
