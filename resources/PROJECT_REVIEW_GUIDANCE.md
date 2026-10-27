# NexoraOps review guidance

This is project-authored guidance, not a verbatim copy of any upstream skill.

## Visual review

Compare the actual rendered website with the supplied Lintara, JakCool and warehouse references. Judge the dominance of the scene or chart, the readability of the main metric, the spacing between decisions, the restraint of color, and the scale of moving objects. A screen should have one clear main job. Remove miniature panels that repeat detail available elsewhere.

Use the project's white and burnt-orange system rather than borrowing another brand. Ensure tables align numerical units consistently and inactive states remain distinct from zero operating activity. Inspect the page at ordinary browser zoom, without shrinking the whole interface to hide overflow.

## Interaction review

Check navigation, selection, focused dialogs, keyboard use, pause/replay, camera controls, imports, downloads and worker cancellation. A control must either change the intended state or state its explicit scope. Preserve context when moving between pages. Verify that stale simulation results are not attached to a changed scenario.

## Numerical review

Use reference fixtures and matched worlds. Reconcile daily regional parcels across internal, external, emergency and deferred volumes. Keep physical capacity separate from planning limits and incident-effective capacity. Preserve the 50% per-zone baseline when a custom current-policy scenario is evaluated. Reconcile intraday integration to daily demand.

## Review-and-revision loop

Define the requirements, finish a complete attempt, inspect actual outputs, obtain an independent review when available, and rank defects by impact. Correct broken behavior and numerical errors before layout polish. Recheck affected behavior after each correction. Limit the loop to four substantive rounds. Do not invent passing scores or claim checks that were not performed.

Review ratings and critique exchanges belong outside audience-facing deliverables. Verification documentation records concrete tests and material gaps, not self-congratulation.

## Browser smoke protocol

Open the local website through the preview server. Inspect the network scene, facility cutaway and all nine screens. Run the full 10,000-world worker and confirm its visible result. Change a matrix cell and a finance assumption, verify the change, and restore central settings. Apply an incident, inspect regional capacity, undo it, and check the baseline again. Test JSON and CSV exports, a valid import and one rejected invalid import. Inspect a narrow viewport and check that navigation and tables remain usable.

The attached automated Node test covers deterministic numerical behavior. It does not replace visual inspection or claim a complete browser automation suite.
