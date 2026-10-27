# Deployment and operation

## Vercel project

1. Extract the ZIP into a working folder. The application root is `NexoraOps/`, containing `package.json`, `vercel.json`, `website/`, and `dist/`.
2. Run `npm test` and `npm run build` from that root with Node.js 20 or later.
3. Add the folder to a repository or import it into a Vercel project. Select **Other** if a framework preset is requested.
4. Set root directory to the folder containing `package.json`, build command to `npm run build`, and output directory to `dist`.
5. No install command is needed beyond the host's standard package handling; the dependency list is empty. No environment variables are required.
6. Build the deployment, then inspect the host's preview URL. Confirm the nine navigation screens, JSON loading, worker progress, JSON/CSV downloads and facility selection before presenting.

Only `dist/` is published. The casebook, analytical workbook and historical discussion remain outside the public website unless explicitly added to a hosting output folder.

## Static hosting alternative

Any static host can serve `dist/`. All runtime assets are relative and same-origin. Requests for `.js` need a JavaScript MIME type, JSON and GeoJSON need readable responses, and module workers need ordinary same-origin script access. A `file://` launch is unsuitable.

## Session behavior

The app opens in Digital twin. On phones it starts with the 2D map. If a scenario was saved on the device, bounded settings restore; the replay state starts according to reduced-motion preference. **Kembali ke asumsi sentral** in the parameter drawer restores the default 70/88 software scenario.

A 10,000-world run loads approximately 7.7MB of JSON once per worker lifecycle. Monte Carlo runs in the background. The worker can be canceled. A device's calculation and rendering performance depend on its browser and hardware; no universal 60fps guarantee is made.

## Presentation sequence

Use Digital twin → facility cutaway → Proyeksi → Policy Lab → Insiden & tindakan → Dampak. Keep the optional tour available for a self-guided judge. The default software recommendation balances downside and service risk; a higher-return 100% utilization policy illustrates the cost of removing capacity headroom.

The finance view should show both project returns and the annual group-profit test. The product narrative is selective allocation and resilient coordination, with investment evaluated against a rules-only alternative.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Data load error | Serve through HTTP; verify JSON files are present in `dist/data/` |
| Worker error | Verify `worker.js`, `engine.js`, and `worlds.json` have same-origin URLs and correct MIME types |
| Blank or slow hardware 3D | The renderer automatically uses Canvas projection if WebGL2 is unavailable; 2D remains selectable |
| Heavy scene | Choose **Ringan** in display quality; pause replay for a static view |
| Saved settings seem unexpected | Reset to central assumptions, then save again |
| Import fails | Use an exported version 1.0.0 scenario under 1MB with a recognized policy |
| Local storage unavailable | Use JSON export/import for portable state |

No production dispatch action, payment, external message or operational control is triggered by any button.
