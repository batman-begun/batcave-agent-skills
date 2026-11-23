# Batcave Agent Skills

Reusable skills for AI agents that design interfaces, turn images into motion, explore research questions, or keep projects moving across sessions and contributors.

[![Registry validation](https://github.com/batman-begun/batcave-agent-skills/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/batman-begun/batcave-agent-skills/actions/workflows/validate.yml) [Registry license](LICENSE) · [Skill catalog](catalog.json)

## See it in action

[![A sunset landscape refracts through moving prism panes, rendered with FFmpeg Motion Director](docs/showcase/ffmpeg-motion-director/prism-glass.gif)](docs/showcase/ffmpeg-motion-director/README.md)

**FFmpeg Motion Director** turns still images into clips with 15 procedural motion effects. This six-second preview uses the bundled renderer on original demo artwork. [See all 15 effects and reproduce the demo](docs/showcase/ffmpeg-motion-director/README.md).

## Find a skill

| Skill | Use it to |
| --- | --- |
| [FFmpeg Motion Director](skills/ffmpeg-motion-director/SKILL.md) | Turn a set of still images into 30-second clips and batched ZIPs with motion plans and render reports. |
| [Hallmark Web Design](skills/hallmark-web-design/SKILL.md) | Design or audit an interface and preserve working user journeys during a redesign. |
| [HanYu Visual Lab](skills/hanyu-visual-lab/SKILL.md) | Turn Chinese, Pinyin and Vietnamese lesson data into an infographic with real typeset text. |
| [WonderAnime](skills/wonderanime-gouache-grungecel-image/SKILL.md) | Develop prompts and guide reference edits in a gouache and grungecel house style. |
| [Klein Explorer](skills/klein-explorer/SKILL.md) | Investigate open-ended questions, trace evidence and look for counterexamples. |
| [Coding Agents Collaboration · Leader](skills/coding-agents-collab-leader/SKILL.md) | Coordinate agent contributors, review their evidence and manage GitHub handoffs. |
| [Coding Agents Collaboration · Contributor](skills/coding-agents-collab-contributor/SKILL.md) | Pick up a scoped task, work on a branch and deliver a verified pull request. |
| [Universal Project Repository](skills/universal-project-repository/SKILL.md) | Give a project a durable record of intent, decisions, current state and verification. This registry uses the approach. |

## Use a skill

Pick a skill above and ask your agent to read its `SKILL.md` and linked requirements before starting. For example, “Use FFmpeg Motion Director to inspect these images, assign motion effects, and render the first batch.”

**Hermes users** can register this repository as a skill source.

```bash
hermes skills tap add batman-begun/batcave-agent-skills
```

Check the selected skill's runtime requirements and your agent's access to its tools. Source registration and skill execution are separate steps.

For programmatic discovery, use the [JSON catalog](catalog.json) or [fetch it as raw JSON](https://raw.githubusercontent.com/batman-begun/batcave-agent-skills/main/catalog.json). Its entries link to [Agent Skills](https://agentskills.io/specification) entrypoints.

## Maintain the registry

This repository uses UPR/1 Standard Tier. See [project intent](intent/INTENT.md), [current status](state/STATUS.md), [agent instructions](AGENTS.md), [publication rules](knowledge/CONSTRAINTS.md) and [verification](verification/SOFTWARE.md).

Update `SKILL.md` and its optional `skill.meta.json`, then regenerate and verify the catalog.

```bash
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
python3 -m unittest discover -s tests -v
```

## Licensing

Registry code and documentation are covered by [MIT](LICENSE). Check the license for each skill and any separately documented media. Hallmark retains its [upstream MIT notice](skills/hallmark-web-design/LICENSE.upstream). WonderAnime's MIT grant covers its written material. Its private visual references have no public license grant.
