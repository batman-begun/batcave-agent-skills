# EXPAND protocol — escape the original framing

## Objective

Create a *search space*, not a polished answer too early. Treat user examples as seeds, never as a closed list. When the goal is blurry, Klein must generate the framing it needs, then seek external signals capable of changing that framing.

## Procedure

1. **Separate** objective, explicit hard constraints, supplied examples, hidden assumptions, and unknowns. Draft at least two *competing interpretations* of the opportunity/problem; avoid turning either into fact.
2. **Build orthogonal lanes.** Choose lanes because they differ in causal lens or source population, not simply keyword spelling. Candidate lenses: unmet demand, waste/inefficiency, workaround behaviors, regulatory shifts, geography, supply-chain changes, technology inflections, failures, emerging subcultures, analogs in distant industries, upstream/downstream stakeholders, nonconsumption, contrarian explanations. Expand or discard these depending on the domain.
3. **Top-down pass:** search from candidate domain taxonomies toward subcategories. **Bottom-up pass:** sample field signals first (complaints, developer issues, public datasets, niche communities, job listings, policy texts, failures) and *induce* new categories without forcing them into the top-down taxonomy. **Cross-domain pass:** search distant analogs and test transferability, not just similarity.
4. **De-anchor:** reserve meaningful exploration effort for at least one path that would be invisible if all user seed examples were removed. Ask: What would a skilled outsider with no conversation context search for? Start it from a different source class or independent problem framing.
5. **Discovery node** (when useful): `id`, `origin` (user seed / source-led / cross-domain / contradiction), `observation-or-hypothesis`, `source pointer`, `why this matters`, `new questions`, `next lanes`, `status`.
6. **Recursive expansion:** For each surprising verified finding, ask which adjacent assumptions, related actors, prerequisites, substitutes, or failure causes it exposes. Open a new lane only if it could alter recommendation, coverage, or uncertainty; otherwise park it.

## Guardrails

- Do not confuse *novelty* with *market opportunity*, *association* with *causation*, or *absence of hits* with *absence of a company or solution*.
- Look for disconfirming or boring explanations before promoting an exciting narrative.
- Don't claim a numerical percentage of all options discovered. A saturation signal only indicates diminishing novelty within searched lenses.
- If searches are mostly duplicates, change source population, causal lens, region, language, or unit of analysis—not only terms.

## Lane selection examples

- **API hunt:** model-first, provider-first, aggregator-first, community-hosted, geographic/language variation, pricing mechanisms, documented endpoints, alternative architectures.
- **Unknown startup domain:** operational waste, recurring pain, regulation, labor/workarounds, imported models, technical discontinuity, nonconsumption, failures, underserved actors.
- **Scientific discovery:** alternative theories, contradictory experiments, nearby disciplines, measurement methods, publication bias, untested boundary conditions.
