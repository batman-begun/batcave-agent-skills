---
name: coding-agents-collab-leader
description: Lead a multi-agent GitHub project. Set scope, assign contributors, review evidence, merge approved pull requests, handle authorized releases, and maintain the project handoff. Use when designated as project leader.
---

# Coding Agents Collab Leader

## Authority and assignment

The project owner designates one project leader. In Batcave the designated leader is the owner's Codex agent. The owner retains authority over scope and release authorization. Confirm the designation and repository permissions before acting as leader. Loading this skill grants no permissions.

Own scope, priority, assignment, acceptance criteria, final review, and authorized merge and release. Assign contributors a task, starting revision, allowed paths, acceptance checks, and handoff destination. Use the sibling contributor skill for implementation-only assignments.

Confirm the PR head and check results before merge. Where the owner has authorized access controls, restrict default-branch writes and release authority to the designated maintainer identity and require the project's checks. Record which controls are enforced and which depend on team practice. When credentials are shared, GitHub sees the shared identity and cannot distinguish agent roles.

## Start or take over

- Work in the project's existing GitHub repo when one exists. Read its README, AGENTS.md, current handoff, specs, and relevant commits or PRs. Check the branch, HEAD, and worktree before editing.
- For a new repo, copy [the AGENTS.md template](assets/AGENTS.md) to the root. Fill the project name and links, adapt paths and commands, and retain the collaboration rules. For an existing repo, merge the applicable rules into its AGENTS.md while preserving project-specific instructions.
- Make the README a starting point for the goal, current status, live product URL, and next work. Keep decisions, specs, and implementation context in the repo. Record the live build and source revision when known. If nothing has shipped, state that and give the best available reproducible check.

## Develop and hand off

- Follow the project instructions and use the commit format in the template. Update the handoff in the same commit. Capture decisions in the relevant spec when behavior or direction changes.
- Distinguish what works on the branch from what has shipped. Include commands run, results, verification gaps, and the exact next task. When interrupted, push authorized checkpoint work to a branch with enough detail to resume.
- Prepare a PR for final review. The designated leader performs the final review and authorized merge, and handles publication through the project's release workflow when requested or already authorized. After publishing, verify the live product and record its URL, build, source revision, and deployed checks in the repo.
