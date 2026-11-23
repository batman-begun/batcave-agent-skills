# {{PROJECT_NAME}} · Agent collaboration

> Template for the repo root `AGENTS.md`. Use it only when the team lead asks for a
> repo to be prepared for collaboration — it is scaffolding, not part of your own task.
> Replace every `{{...}}` placeholder and delete rows that do not apply.

## Start here

GitHub is the shared project thread. A teammate should be able to continue from this repo alone.

| What to find | Where to look |
| --- | --- |
| Goal, users, scope | [README](README.md) and [product spec](docs/PRODUCT.md) |
| Current progress, blockers, next task | [Handoff](docs/HANDOFF.md) |
| Verify shipped behavior | {{LIVE_PRODUCT_URL_OR_UNPUBLISHED_STATUS}} |
| How to run, test, and release | [README](README.md) and [release instructions](docs/RELEASE.md) |

Before editing, read these sources and any applicable nested instructions. Check your
branch, HEAD, and worktree. Preserve existing work — including uncommitted changes
another agent left in the tree. Record product decisions and their rationale in the
repo, with private data and secrets kept outside Git.

## Roles

The team lead owns scope and task assignment. The designated leader owns final review, merge into
the default branch, release tagging, deployment, and publishing. Contributors own
implementation, verification, and handoff. Route merge and release requests to the designated leader.

Follow the current explicit assignment within approved scope. Use the handoff
Next entry when asked to resume from it. Flag conflicts and proceed on the parts
that are clear. If the current worktree contains someone else's changes, use a
separate Git worktree from the appropriate verified base commit.

## Branches and review

Agents with repo access commit and push to working branches and open PRs. Keep PRs
review-ready: the handoff context travels in the PR body or the final squash commit.
The designated leader performs final review and merge and handles releases through the project's
existing deployment process.

## Every commit hands work forward

Update the handoff in the same commit. Record the current state, the exact next
actionable task, and any blockers. Update the product spec or decision record when
requirements or behavior change. Use a descriptive subject and these fields in the
commit body, or in a clearly referenced handoff section included in the commit.

- **Why** — product goal or requirement served.
- **Changes** — what changed and its current status.
- **Verification** — commands or user flows actually checked, results, and gaps.
  Include the live URL and build when relevant. Mark local, PR, and pending-deployment
  checks explicitly.
- **Open / Next** — first task to resume, its starting point, and blockers.

If interrupted, push an authorized checkpoint to your working branch. Include the
branch or commit, what is unfinished, and how to reproduce the current state. After a
release, record the live URL, deployed build, source revision, and smoke-test result.
