# SOURCE ROUTING — tool selection for heterogeneous evidence

**Routing intent:** different retrieval mechanisms expose different *parts of reality*. Do not optimize raw tool count. Only use tools present, authorized, and relevant in this chat; Klein adds no MCP server of its own. If user forbids external access, honor it and mark all external claims accordingly.

## Discovery / retrieval ladder

| Signal wanted | Preferred tool when available | Why / caution |
|---|---|---|
| Broad facts, recent news, keyword precision | Native web search | Search internationally and across languages where justified; validate dated claims. |
| Semantic leads outside familiar names | Exa `web_search_exa` | Describe *the page/source sought*, not just keywords. Semantic similarity is not evidence. |
| Read promising pages | Exa `web_fetch_exa`, native fetch, Firecrawl `firecrawl_scrape` | Check actual paragraphs rather than relying solely on snippets. |
| Structure/technical docs/site-wide missing pages | Firecrawl `firecrawl_map` / `firecrawl_crawl` / `firecrawl_scrape` | Scope limits, cost and freshness. Use a bounded crawl. |
| Multi-site structured entity dataset | Firecrawl provider discovery / structured extraction; verified public APIs | Check permissions, cost and record provenance; avoid fake precision. |
| Dynamic interactive site | TinyFish or available browser tools | Only when necessary; read-only by default. Do not bypass access controls or approve financial actions. |
| Open-source grassroots problems | GitHub issues, repos, release notes; Firecrawl developer search | Bugs and workarounds can reveal needs; not representative sample. |
| AI model/dataset frontier | Hugging Face models, datasets, Spaces; papers | Distinguish demo/model availability from reliable production API. |
| Scholarship | Original journal/paper, Firecrawl research papers, academic index | Distinguish abstract from full-text findings and preprints from reviewed work. |
| Industry economics and policy | Official statistics, regulators, annual reports, filings, credible primary data | Verify jurisdiction, time window, coverage and comparability. |
| Community pain or product adoption | Reviews, independent forums, Reddit, niche communities | Detect selection and moderation bias; treat as hypothesis leads. |

## Practical sequence (adapt, don't ritualize)

1. For open-ended research, use at least **two genuinely different search framings** and preferably two mechanisms/source populations if available. One should not depend on user seed names.
2. Compare overlap and **novel qualified finds**, not simply the number of hits. Exa and Firecrawl might index identical materials; same source across providers is not independent corroboration.
3. Retrieve high-value original pages before making consequential claims. If extraction fails, switch to another reader and disclose gaps instead of hallucinating contents.
4. If discovery stalls, switch language, geography, stakeholder, underlying economic mechanism, or evidence type. Avoid synonym-only query loops.
5. On sensitive or expensive tools (Firecrawl agent jobs, bulk crawl, rate-limited APIs), bound breadth and cost. Never promise quotas without checking.
6. If a specialized connector is unavailable, use accessible authoritative sources, name the missing perspective, and proceed proportionately. Don't request API keys or new infrastructure by default.

## Connector caveat

Exa and Firecrawl are separate user-connected plugins. Their presence in a different conversation does not prove availability in the current task. A skills-only plugin cannot force another tool to be installed, connected, or invoked. Route by **capability**, not hard-coded dependency, and never claim a tool was called if it was not.
