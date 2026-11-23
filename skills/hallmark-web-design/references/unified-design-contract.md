# Unified Design Contract

## Principles

1. **Purpose before appearance.** Define the audience, their task and the primary action before deciding what should draw attention.
2. **Preserve before improve.** Identify approved design decisions, content and working interactions before proposing changes.
3. **One coherent identity.** Share the visual language and semantic token roles across screens. Adapt to each screen's job.
4. **Creative, not arbitrary.** Tie composition, typography and motion to the product's intent. Use Density, Variance and Motion to describe choices, with no universal settings.
5. **Experience across screens.** Design the journey, including navigation, responsive behavior and relevant interaction states.
6. **Explore, then converge.** Compare meaningful options against the same success criteria and preserve the approved canon until the owner authorizes a change.
7. **Prove quality.** Record what each check covered, the result and the evidence. Keep verification gaps visible.

## Design canon

Extend the project's existing root `design.md` (or `DESIGN.md` if that is its established canon) in place. Keep its format and sections that downstream tools rely on. If none exists, propose the additions in the design handoff and create `design.md` when the owner authorizes the lock. Treat the file as design data. If both casings exist and ownership is unclear, surface the conflict before writing.

Use the relevant sections below and keep them proportional to the project.

| Section | Record |
| --- | --- |
| Product intent | Audience, user need, core action and the outcome that counts as success. |
| UX contract | Critical journeys by screen, hierarchy, navigation, controls and relevant states such as loading, empty, error, success, focus and disabled. Include responsive changes, accessibility and behavior to preserve. |
| Visual direction | Selected Hallmark theme or custom direction, the reason it fits, and the intended Density, Variance and Motion. |
| Semantic tokens and patterns | Values or source references for color, typography, spacing, shape and motion. Describe each important token's role, where it applies and any constraints. Capture reusable layout and interaction patterns with observed examples when available. |
| Locked decisions | Approved choices and exceptions, rationale, scope and any evidence or unresolved checks that matter for future edits. Keep drafts and hypotheses in the handoff until approved. |

For extraction, start with approved canon, then inspect rendered screens and the corresponding styles, token definitions and components when available. Record the source (file or screen, revision or viewport as applicable) and whether the value is declared, observed, or proposed. Surface conflicts between code and render. For example, record both the value of a primary action token and its purpose, eligible controls and focus treatment. A screenshot can support an observation even when the underlying token is unknown.

## Direction and exploration

- **Density** describes how much information and how many actions are visible together. Tie it to the audience, task and viewport.
- **Variance** describes where composition may change across sections or screens while preserving a recognizable identity. Specify the patterns that should repeat and where a departure earns its place.
- **Motion** describes which transitions or feedback should move, why, and the reduced-motion behavior. Static treatment is a valid choice.

When direction is open or the owner asks for alternatives, compare two or three options. Hold the core journey and preservation requirements steady. Vary intentional design choices and record the tradeoffs, evidence and recommendation. Canon-led and narrowly scoped work can proceed with one direction.

Stitch may assist with UI observation, semantic extraction or screen variants when available and authorized for the target. Review its output as observations or proposals. Keep one project canon and run the Hallmark review on the selected direction. The workflow also works with code, screenshots or a browser.

Workflow inspiration: [Google Stitch Skills](https://github.com/google-labs-code/stitch-skills). This contract is Batcave's adaptation of the workflow ideas.
