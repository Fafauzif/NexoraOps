# Architecture

## Runtime

The application is a static ES-module website. It uses browser APIs, authored SVG charts, native HTML controls, local storage, a module worker and a procedural 3D renderer. No build-time or runtime package installation is required.

| Module | Responsibility |
| --- | --- |
| `app.js` | Shared state, nine views, controls, regional allocation, import/export and replay |
| `engine.js` | Float64 national operating model, investment finance, statistics and transport solver |
| `worker.js` | Asynchronous matched-world simulation and heatmap recalculation |
| `scene.js` | Procedural geometry, orthographic camera, picking labels, aggregate animation, WebGL2 and Canvas fallback |
| `styles.css` | Layout, tokens, responsive behavior, print and reduced-motion styling |
| `data/` | Model configuration, named worlds, reference outcomes, regional fixtures and evidence |

## Calculation pipeline

A policy sets an internal-share ceiling and utilization limit. The engine evaluates the chosen operating conditions and a current-policy counterfactual using the same demand, traffic and cost conditions. Incremental project cash flows are then calculated. A separate group-profit bridge evaluates each annual growth step.

The regional solver uses nine demand zones, shared hub capacities and finite carrier reservation capacity. It solves a continuous transport allocation, not a vehicle-routing problem. Precomputed default regional fixtures preserve the original Python results. Custom settings trigger a browser solve. Current-policy custom scenarios preserve the baseline 50% internal allocation per zone when capacity permits; displaced internal volume becomes deferred demand.

The website fetches compact reference JSON on startup. The 10,000 named-world file is fetched only when a worker calculation begins. Simulation progress is posted in batches. Parameter signatures prevent a completed old result from appearing as the result for newly selected controls.

## Data contracts

Volumes in the national engine are billions of parcels per year. Money is Rp trillions. Regional volumes are individual parcels per day or per four-hour window; regional money is IDR. Conversion to display format happens at the view boundary.

Scenario JSON uses `schema_version: 1.0.0`. Import limits file size to 1MB, accepts known policy IDs, allowlists enum controls and bounds numeric controls. An export includes the state, active policy, annual and regional-daily results, scope and matching Monte Carlo summary if available. CSV uses a single header row and consistent annual-national units.

## Persistence

Device storage holds one active scenario. It does not upload data. JSON provides portable restoration. Results are reproducible because the exported worlds retain their sampled values and identity; the browser does not attempt to reproduce NumPy PCG64 with a different random-number generator.

## Renderer

WebGL2 uses instanced cube geometry and a faceted tree mesh with a simple lighting shader. The fallback projects the same 3D boxes through the camera matrix and paints visible faces to Canvas 2D. Decorative quality is reduced for the fallback. No downloaded models or textures are required.

Selection is exposed through DOM buttons, so a hub can be chosen without pixel-perfect canvas picking. National cities and 2D hubs support keyboard activation. The parameter drawer and guided tour keep keyboard focus inside their active dialog.

## Hosting

`npm run build` copies the website into `dist/`. This is a static build; no server rendering or edge runtime is used. Vercel can serve all assets directly. Worker and JSON paths remain same-origin. A static host must serve JavaScript with a JavaScript content type.
