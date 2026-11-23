# Domain profiles (additive to universal core)

Select profiles based on actual work, not project title. Mixed projects use scoped role maps and union of obligations. Every profile must define what counts as acceptance, evidence, failure and revision. A verified claim never exceeds its evidence. No automated check is required where not meaningful; state a manual protocol and its limits. Software profile is mandatory for shipped/operated executable software; load software-floor.md separately.

| Profile | Canonical knowledge / artifacts | Verification obligations |
|---|---|---|
| Novel | premise, POV, character bible, world rules, timeline, locked canon, chapter versions, draft/accepted manuscript, outline, style guide | continuity and chronology, character motivation, POV/voice, factual research where applicable, contradictions and owner acceptance; editorial judgment not objective truth |
| Comic | story and world canon, character/asset IDs, scripts, panel/arc manifest, visual refs, lettering specs, approved vs draft versions, publishing order | panel sequence, continuity, character likeness against authorized references, typography, asset completeness, rights, version/publishing alignment; visual owner UAT |
| Science | problem, definitions/assumptions, claim/hypothesis register, methods, data and provenance, protocols, equations, analysis notebooks, citations, negative findings | reproducibility, assumptions, controls, uncertainty, counterexamples, peer critique, independent data/measurement when possible; distinguish proof, empirical evidence and plausibility |
| Philosophy | definitions, propositions, premises, argument/dependency graph, schools/sources, objections, alternatives, unresolved questions | logical consistency, validity vs soundness, hidden assumptions, steelman alternative views, counterexamples; distinguish descriptive, normative and metaphysical claims |
| Contemplation | private dated observations, questions, practices chosen by owner, evolving interpretations, distinctions between experience and explanation | reflective review, alternative explanations, uncertainty, corroboration if appropriate; no claim of enlightenment certification, diagnosis, or universal truth from subjective experience; avoid invasive tracking or unsafe practices |
| Business | vision, stakeholders, strategy, requirements, SOPs, risk/decision registers, operational metrics, finance assumptions, deliverables | measurable acceptance, evidence of process execution, stakeholder review, data quality, risk and privacy compliance; projections marked as such |
| Knowledge | taxonomy, glossary, source register, claim records, relationships, open questions, current syntheses | provenance, citation quality, contradiction/deduplication checks, freshness and scope; don't collapse conflicting evidence into false consensus |
| Custom | document domain-specific roles, semantics, units, deliverables, privacy, authority and gates | explicit fit criteria, failure modes, counterexamples, acceptance and review method; cannot waive software floor |

## Operating specifics
Creative: retain divergent ideas as proposals or branches without polluting canon. Canon changes call out affected scenes/panels, propagate through indexes, retain superseded references. Approval of a panel or manuscript version is not blanket approval of downstream publisher artifacts. Asset manifest uses IDs, version, checksum if available, dimensions, rights, storage pointer, dependency and acceptance state. Never invent biometric or character reference access.

Research: retain negative outcomes and alternative hypotheses; link exact dataset/code/instrument versions, source date and retrieval date if material. Do not silently alter raw data. Record corrections as new derived datasets. Cite sources near claims. When computation supports a research result, preserve runnable environment and analysis provenance; if software is distributed or operated, apply software floor to it. For sensitive datasets keep raw inputs out of Git and link access-controlled manifests. An independent reviewer may reproduce calculations against a fixed input or challenge assumptions separately.

Philosophy/contemplation: separate raw observation, interpretation, hypothesis, adopted working view and claim of external fact. Owner approval establishes a current personal view, not scientific validity. Preserve uncertainty and alternative explanations, avoid treating subjective phenomena as evidence of external supernatural cause without independent support. Do not force private journals into repositories; optional local encrypted store and redacted index. Allow owner to restrict retention or delete sensitive entries; privacy overrides history preservation. Do not treat distress as a research task when safety support is needed.

Business/knowledge: designate source of truth for changing data; Git records assumptions and observed snapshots, not automatically the operational database. Timestamp metrics; no credentials or customer records by default. Record decisions with tradeoffs, owners and review trigger. Keep raw transcripts optional and authorization-scoped.

## Choose an example for the intended reader

| Domain | Representative example | Evidence to link |
|---|---|---|
| Software or media tools | A real render, a working interaction, or a short before/after | Versioned input, the command or steps, the run record, and what the checks covered |
| Science or philosophy | A small worked example, derivation, argument map, or counterexample | Definitions, assumptions, each material inference, scope, unresolved objections, and how to reproduce or challenge it |
| Novel or comic | An approved excerpt, scene or sequence | Version and publishing scope, with canon pointers where the audience may view them |
| Business or knowledge | A worked process, a decision, or a reproducible synthesis | Approved inputs, provenance, evidence and limits on generalization |
| Contemplation or other private work | A concise internal starting point | Owner-authorized pointers; use public examples only with separate permission |

A technical derivation or well-sourced text walkthrough can be the complete showcase. Add diagrams or media when they help readers inspect the result.

## Examples (not actual project state)
- GiftU-like product: software profile; native source paths + architecture, intent/story and real CI/test gates; approved interaction contract links to UAT.
- COMIC002-like series: comic + science-fiction knowledge; draft panel image lives in object storage, versioned manifest tracks approved panel and publishing order; optional publishing app has separate software obligations.
- Batcave Agent Skills: software and knowledge. The [public README](https://github.com/batman-begun/batcave-agent-skills/blob/479c9a84be23b26376037e1a21012ab1a00e1bcc/README.md) leads from the FFmpeg render to inputs and replay steps. HanYu and Hallmark link to actual renderer or browser checks. Workflow skills link to a relevant text case.
- A theoretical world model: science and philosophy. Introduce the question and link to the approved map of entries. Walk through one small instance from scoped premises to one consequence, then show an objection, counterexample or open boundary. Distinguish a derivation within the model from independent support in the world.
- A private journal: contemplation, micro, local. Current reflections distinct from raw observations; no remote by default.
