# Verified behavior

Verification date: 27 October 2026.

## Automated numerical checks

`npm test` executes two suites. The national-model suite passes 4,063 checks: 2025 cost/share calibration, five-year central recommended policy costs and shares, group profit, cash flows, NPV, IRR, strict growth result, full 10,000-world held-out distribution, parcel conservation, capacity limits, a transport-solver example and incident parcel conservation.

The actual worker module is exercised with exported worlds. Its weak-productivity Monte Carlo result matches a direct engine calculation. Its 66-cell campaign heatmap applies the demand uplift correctly and matches a direct calculation at the 70%/100% cell. Progress reaches completion. No independent random-number generator is substituted.

The full 10,000-world software 70/88 calculation returns mean NPV `0.5090185115539968` Rp tn, p10 `-0.1605076098587722`, positive-NPV fraction `0.8049`, and service-violation-world fraction `0.0179`. These reproduce archived analysis outputs within the documented tolerances.

Independent source checks additionally reproduced mean NPV, p10 and service-violation fractions for current, software, targeted capacity and large expansion using all 10,000 worlds. Syntax checks pass for application, engine, renderer and worker modules.

## Browser checks

All nine navigation screens loaded and displayed their expected headings. The regional scene and facility cutaway were visually inspected. Camera-related controls, facility selection and the route-cost layer were present. The route dialog showed nine corridor distances, travel times and calculated variable costs for the selected hub.

The browser's actual module worker completed 10,000 worlds in approximately 1.59 seconds in the observed run and displayed the expected Rp509.0bn mean, Rp−160.5bn p10, 80.5% positive fraction and 1.8% rounded service-violation fraction. This single run is not a general device-performance guarantee.

Applying the reallocation response updated Cawang's effective daily capacity to 200,000, internal volume to 176,000 and utilization to 88%. Regional daily totals remained scoped separately from annual finance.

JSON and CSV downloads were captured through the browser and parsed. The JSON central NPV matched the fixture. The CSV had one header row and five correctly scoped annual result rows. Example exports are included under `tests/fixtures/`.

A 390px-wide iframe created an actual narrow CSS viewport for inspection. The phone layout used a navigation drawer, two-column metrics, stacked panels and a default 2D network view. This was a browser viewport check, not a physical phone test.

## Workbook preservation

Nine frozen-pane definitions were removed to match the explicit user instruction. Artifact Tool imported, unfroze and recalculated the workbook. Only the requested view changes were transferred into the final workbook package so its native data tables and cached values were retained. A package comparison confirms every changed worksheet differs only in view metadata; all cells, formulas, cached results, styles, tables and other ZIP members remain unchanged. No frozen panes remain. The supplied builder also uses unfrozen sheets.

Existing analytical workbook checks and rendered sheet previews are retained. Desktop Excel was not executed for this website handoff.

## Scope of remaining verification

This browser did not support WebGL2. The Canvas projection fallback was inspected; the hardware WebGL path needs a compatible deployment browser for direct rendering verification. No frame-rate claim is made for untested hardware. Local save/import, full keyboard coverage and print pagination were reviewed in source but were not exhaustively browser tested.

Detailed street/building GIS remains unavailable; the scene uses the documented corridor fallback and procedural buildings. Intraday/weekly profiles are normalized planning assumptions. Full upstream repository snapshots could not be downloaded; exact links, project guidance and an acquisition script are supplied. No external deployment or live operational integration was performed.
