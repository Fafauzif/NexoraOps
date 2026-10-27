# NexoraOps

NexoraOps is an interactive logistics decision platform for the IBSC 2026 Nexora case. It connects Greater Jakarta operations, allocation choices, service resilience, and investment outcomes in a shared scenario. The interface is in Bahasa Indonesia.

The package includes the runnable website, production build, complete analytical package, supplied visual references, source material, model tests, and the updated master context pack.

## Run locally

Requires Node.js 20 or later. There are no npm dependencies and no installation step.

```sh
npm run dev
```

Open `http://localhost:5173`. A local HTTP server is necessary because the app loads JSON and starts a module worker. Opening `index.html` as a local file will not load the application.

```sh
npm test
npm run build
```

The static production site is written to `dist/`. An alternative is to serve `dist/` with any ordinary static HTTP server. For example, `python3 -m http.server 8080 --directory dist` runs a static server when Python is installed.

## Deploy to Vercel

Set the project root to this folder, build command to `npm run build`, and output directory to `dist`. The included `vercel.json` supplies these settings. No environment variables, server functions, databases, API keys, or external CDNs are required. See [deployment instructions](docs/DEPLOYMENT.md) for the exact workflow and preflight checks.

## Explore the product

1. Start in **Digital twin**. Select a hub and enter **Fasilitas** to inspect the procedural cutaway. Switch to Indonesia for representative market summaries, or choose 2D for a simpler network view.
2. Open **Atur skenario**. Choose a policy, demand level, capacity condition, or disruption. Apply it to carry the same state through the analytical screens.
3. Open **Policy Lab**. Select a matrix cell, then run 200, 1,000, or 10,000 matched worlds. The calculation runs locally in a background worker.
4. Compare the three incident responses. Apply a response and return to the twin to inspect the consistent regional allocation and effective capacity.
5. Open **Dampak**. Read both the project return and the group operating-profit test. Adjust discount, cost inflation, or the separate non-logistics contribution assumption.
6. Use **Simpan** for device storage, **Ekspor JSON** for a portable scenario, **Ekspor CSV** for annual results, and **Impor skenario** under **Bukti & asumsi** to restore one.

The optional **Jelajah demo** at the top right provides a short walkthrough. It never blocks normal navigation.

## Package contents

| Folder or file | Contents |
| --- | --- |
| `website/` | Editable application source, procedural renderer, worker and numerical engine |
| `dist/` | Ready-to-host static build |
| `analysis/` | Original workbook, Python model, findings, evidence, simulation draws, data exports and workbook previews |
| `references/images/` | Supplied visual references with meaningful filenames |
| `references/stitch/` | Supplied Stitch HTML, screenshots and design guidance |
| `references/` | Original casebook, recovered discussion, and historical context pack |
| `docs/` | Product brief, architecture, simulation specification, reference guide, deployment and verified behavior |
| `resources/` | Requested design-resource registry, project adaptations and optional acquisition script |
| `tests/` | Executable numerical regression tests and Python regional parity fixture generator |
| `Nexora_Master_Context_Pack.md` | Authoritative current context followed by preserved historical context |

## Analytical interpretation

The default conditional software candidate has a five-year central project NPV of Rp572.99 billion. Across the 10,000 held-out worlds, its mean NPV is Rp509.02 billion, p10 is Rp−160.51 billion, and 80.49% of worlds have positive NPV. The central annual group operating-profit-growth condition fails. The product exposes this distinction directly.

The national annual model and the regional daily transport model have different scopes. Regional volume is a 20% national-share planning assumption. The geographic scene uses coarse corridor weights, hypothetical facility profiles, and procedural buildings. Intraday and weekly profiles are team planning assumptions. These are documented in the evidence view and [model specification](docs/MODEL_AND_SIMULATION.md).

## Technical notes

The 3D engine uses native WebGL2 instancing, with a Canvas 2D projection fallback when WebGL is unavailable. Both use the same 3D geometry and camera controls. The user relaxed the original stack constraint; Three.js and Vite are not dependencies. No runtime assets are downloaded from third-party hosts.

The full upstream design repositories could not be downloaded in this environment. Their exact links and clearly identified project adaptations are included under `resources/`; the package does not misrepresent these as complete upstream checkouts.
