# {{PROJECT_NAME}} · Agent collaboration

## Start here

GitHub is the shared project thread. A teammate should be able to continue from this repo alone.

| What to find | Where to look |
| --- | --- |
| Goal, users, scope | [README](README.md) and [product spec](docs/PRODUCT.md) |
| Current progress, blockers, next task | [Handoff](docs/HANDOFF.md) |
| Verify shipped behavior | {{LIVE_PRODUCT_URL_OR_UNPUBLISHED_STATUS}} |
| How to run, test, and release | [README](README.md) and [release instructions](docs/RELEASE.md) |

Before editing, read these sources and any applicable nested instructions. Check your branch, HEAD, and worktree. Preserve existing work. Record product decisions and their rationale in the repo, with private data and secrets kept outside Git.

## Branches and review

Agents with repo access can commit and push to working branches and open PRs. The project owner designates the leader ({{PROJECT_LEADER}}). Only that leader performs final review, merge, and authorized releases on the owner’s behalf. Contributors use working branches. Access is enforced by repository permissions and rulesets where configured. Use the project's established deployment process. Keep PRs ready for leader review and include the handoff context in the final merge or squash commit.

## Every commit hands work forward

Update the handoff in the same commit. Record the current state, exact next actionable task, and any blockers. Update the product spec or decision record when requirements or behavior change. Use a descriptive subject and these fields in the commit body or in a clearly referenced handoff section included in the commit.

- **Why** — Product goal or requirement served.
- **Changes** — What changed and its current status.
- **Verification** — Commands or user flows actually checked, results, and gaps. Include the live URL and build when relevant. Mark local or PR checks and pending deployment explicitly.
- **Open / Next** — First task to resume, its starting point, and blockers.

If interrupted, push an authorized checkpoint to your working branch. Include the branch or commit, what is unfinished, and how to reproduce the current state. After a release, record the live URL, deployed build, source revision, and smoke-test result.
