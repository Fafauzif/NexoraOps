# Nexora logistics analysis package

Read the findings and master context pack first. No national rollout clears the strict central annual-profit-growth gate. Detailed street GIS acquisition is partial; regional layers are a labelled corridor fallback.

## Reproduce

Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8. No package installation was required.

```bash
python code/model.py
python code/geography.py
python code/prepare_deliverables.py
python code/verify_workbook.py
```

Run the workbook builder between preparation and verification. It requires the Codex bundled `@oai/artifact-tool`. Use a private OS temporary directory with a `node_modules` symlink to `CODEX_PRIMARY_RUNTIME_NODE_MODULES`, copy `code/build_workbook.mjs` there, and run it with `CODEX_PRIMARY_RUNTIME_NODE` and `NEXORA_ROOT` set to this package directory. See the builder header and dependency record. A standard Python environment with NumPy/SciPy/Matplotlib can rerun the analysis without workbook authoring.

`python code/retrieve_roads.py` prints the optional buffered request plan. Add `--download` only when Overpass access is available. No successful detailed extract is claimed here. Conditional access and turn restrictions still require additional work afterward.

Simulation tables are imported workbook snapshots. Finance inputs recalculate deterministic cash flows; operating changes require scripts and workbook refresh. Currency is IDR. National financial tables use Rp trillion, regional tables IDR/day and incident tables IDR/four-hour window.
