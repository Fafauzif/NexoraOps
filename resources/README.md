# Requested design and browser resources

The following four upstream resources were specifically requested in the recovered discussion. Public repository or skill pages were inspected on 27 October 2026. Direct Git, npm and raw-file downloads were restricted in the build environment. This folder therefore contains exact source locations, project-authored adaptations, and an acquisition script. It is not a complete vendor snapshot and does not claim an upstream commit lock.

| Resource | Exact source | Included treatment |
| --- | --- | --- |
| Taste skill | https://github.com/Leonxlnx/taste-skill | Resource record and project visual-review adaptation |
| Vercel Web Design Guidelines | https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines | Resource record and project accessibility/interaction checklist |
| Awesome DESIGN.md | https://github.com/voltagent/awesome-design-md | Resource record and NexoraOps-specific `DESIGN.md` |
| Playwright CLI | https://github.com/microsoft/playwright-cli | Resource record and browser smoke-test protocol |

Taste's inspected skill path is `skills/taste-skill/SKILL.md`. The Vercel skill path is `skills/web-design-guidelines/SKILL.md`; it points reviewers to the current Web Interface Guidelines source. Playwright CLI's inspected skill is `skills/playwright-cli/SKILL.md`. Awesome DESIGN.md is a design-document collection rather than a single executable skill.

The runtime has no dependency on these resources. Their procedures are adapted in [project review guidance](PROJECT_REVIEW_GUIDANCE.md), with user instructions taking precedence. Upstream licensing and revision identifiers must be checked in the actual acquired checkout before redistributing copied source. The acquisition script retains each repository's own license files; it does not execute installed software.
