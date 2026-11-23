# Coding Agents Collaboration · Anatomy of a public handoff

[Batcave PR #10](https://github.com/batman-begun/batcave-agent-skills/pull/10) shipped the registry landing page and FFmpeg showcase. It provides a public example of the artifacts the two skills use to exchange work.

| Handoff step | What to leave for the next person | Where PR #10 shows it |
| --- | --- | --- |
| Scope | Goal, expected output and boundaries | The PR summary lists the README, the reproducible demo and the social card. |
| Contributor delivery | Diff and checks tied to the changes | The PR records rendered candidates, decode and format checks, sampled FX and local registry tests. |
| Review | A shared result tied to the PR head | [GitHub Actions run](https://github.com/batman-begun/batcave-agent-skills/actions/runs/45164664730) records the registry check. |
| Integration | Merged commit and published output | [Merge commit](https://github.com/batman-begun/batcave-agent-skills/commit/6fb35bf9b6070893635d91ecc8aa44519fb540bc) ties the diff to `main`. |

The PR history establishes the artifacts and merge. Individual agent assignments and an independent review are unverified in this example.

Try the same pattern by giving a contributor a bounded task and explicit verification criteria. Have the contributor attach the results to a PR, then have the designated leader review the diff and evidence before taking the authorized merge action.

[Leader skill](../../../skills/coding-agents-collab-leader/SKILL.md) · [Contributor skill](../../../skills/coding-agents-collab-contributor/SKILL.md)
