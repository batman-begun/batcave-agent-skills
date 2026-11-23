#!/usr/bin/env python3
"""UPR/1 offline scaffolder and structural lint (v1.2.0). No network, Git, or overwriting."""
import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath

SKILL_VERSION = '1.2.0'
ROLES = ('intent', 'context', 'knowledge', 'constraints', 'state', 'artifacts', 'verification', 'evolution')
PROFILES = {'software', 'novel', 'comic', 'science', 'philosophy', 'contemplation', 'business', 'knowledge', 'custom'}
TIERS = ('lite', 'micro', 'standard', 'extended')
LIFECYCLES = {'proposed', 'active', 'paused', 'archived', 'completed'}
VISIBILITIES = {'local', 'private', 'internal', 'public'}
MANIFESTS = ('PROJECT.json', 'PROJECT.yaml')  # both hold JSON-compatible YAML; exactly one may exist
SLUG = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
MARK = 'UPR-TODO'

PROMPTS = dict(
    intent='Owner, purpose, goals, non-goals, approved acceptance IDs',
    context='Raw story, origins, relevant context; distinguish authority',
    knowledge='Current canon/specs/claims, source references and status',
    constraints='Binding invariants, exclusions, safety and privacy',
    state='Actual baseline, completed/planned work, blockers and next action',
    artifacts='Native working paths, versioned output or external asset manifest',
    verification='Criteria, executed checks, evidence and limitations',
    evolution='Decision IDs, rationale, approval and supersession')
CONTROLS = ('Intent and contract', 'Architecture and trust boundaries', 'Reproducible build', 'Source hygiene',
            'Change control', 'Tests and regression', 'Security and dependencies', 'Deployment, recovery and monitoring')
GATES = ('Intent/design', 'Build', 'Behavior', 'Risk/review', 'Delivery')


def safe_path(root, value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('expected relative POSIX path')
    p = PurePosixPath(value)
    if p.is_absolute() or str(p) != value or any(x in ('..', '.') for x in p.parts) or value == '.':
        raise ValueError('unsafe or noncanonical relative path')
    candidate = root
    for part in p.parts:
        candidate = candidate / part
        if candidate.is_symlink():
            raise ValueError('symlink not allowed in mapped paths')
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError('path escapes project')
    return candidate


def role_map(tier):
    if tier == 'lite':
        return {r: 'STATE.md' for r in ROLES}
    if tier == 'micro':
        m = {r: 'RECORD.md' for r in ROLES}
        m['artifacts'] = 'ARTIFACTS.md'
        return m
    return dict(zip(ROLES, ('intent/INTENT.md', 'intent/CONTEXT.md', 'knowledge/INDEX.md', 'knowledge/CONSTRAINTS.md',
                            'state/STATUS.md', 'workspace/INDEX.md', 'verification/INDEX.md', 'history/DECISIONS.md')))


def build(project_id, title, profiles, tier, manifest_name='PROJECT.json'):
    if not SLUG.fullmatch(project_id) or not title.strip() or any(c in title for c in '\r\n'):
        raise ValueError('invalid project id or title')
    if not profiles or len(set(profiles)) != len(profiles) or set(profiles) - PROFILES or tier not in TIERS:
        raise ValueError('invalid profiles or tier')
    if manifest_name not in MANIFESTS:
        raise ValueError('invalid manifest name')
    software = 'software' in profiles
    roles = role_map(tier)
    manifest = dict(schema='upr/1', project_id=project_id, title=title, profiles=profiles, tier=tier,
                    lifecycle='proposed', visibility='local', skill_version=SKILL_VERSION, roles=roles)
    files = {}
    if tier == 'lite':
        files['STATE.md'] = f'# {title} — project record\n\n'
    for role, path in roles.items():
        files[path] = files.get(path, '') + f'## {role.upper()}\n\n{MARK}: {PROMPTS[role]}. No approval or evidence recorded yet.\n\n'
    controls = '\n'.join(f'- {MARK}: {x}; owner, actual method, enforcement, evidence, gap.' for x in CONTROLS) + '\n'
    gates = '\n'.join(f'- {MARK}: G{i} {x}; exact command/protocol, target, result, evidence, limitation.' for i, x in enumerate(GATES)) + '\n'
    if software and tier == 'lite':
        manifest['software'] = {'controls': 'STATE.md', 'verification': 'STATE.md'}
        files['STATE.md'] += '## SOFTWARE CONTROLS — NOT CONFIGURED\n\n' + controls + '\n## SOFTWARE VERIFICATION — NOT RUN\n\n' + gates
    elif software:
        manifest['software'] = {'controls': 'harness/CONTROLS.md', 'verification': 'verification/SOFTWARE.md'}
        files['harness/CONTROLS.md'] = '# Software controls — NOT CONFIGURED\n\n' + controls
        files['verification/SOFTWARE.md'] = '# Software verification — NOT RUN\n\n' + gates
    if tier == 'extended':
        files['RISK-REGISTER.md'] = f'# Risk register\n\n{MARK}: risk, owner, mitigation, residual risk, decision.\n'
        files['COMPONENTS.md'] = f'# Component index\n\n{MARK}: scope, profile, role map, dependencies, authority.\n'
    files['README.md'] = (f'# {title}\n\n{MARK}: describe the purpose, current stage and first thing a reader should read or try. See {manifest_name} for the role map'
                          + ('; AGENTS.md for navigation' if tier != 'lite' else '; STATE.md for the project record')
                          + '. Scaffold only; no publication or readiness implied.\n')
    if tier != 'lite':
        files['AGENTS.md'] = ('# Agent navigation\n\nRead ' + manifest_name + ' and mapped state, intent and constraints first; load only relevant knowledge and artifacts. '
                              'Raw discussion is nonbinding. Stop affected irreversible work on authority conflicts. Preserve native layouts and user changes. '
                              'Capture actual evidence and update state at meaningful checkpoints. Do not publish secrets or private material.\n\n'
                              + ('Software floor applies. See the software controls and verification records named in the manifest. '
                                 'Never claim a configured gate is enforced or passed without evidence.\n\n' if software else '')
                              + f'{MARK}: add project-specific governing references, real verification commands and profile obligations.\n')
    files[manifest_name] = json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
    return files


def check(root, strict=False):
    """Structural lint. strict=True turns scaffold placeholders and empty role files into errors."""
    errors, warnings = [], []
    root = Path(root)

    def soft(msg):
        (errors if strict else warnings).append(msg)

    lite_sections = {}

    def mapped(label, value, allow_dir=False, section=None):
        try:
            p = safe_path(root, value)
            if not (p.is_file() or (allow_dir and p.is_dir())):
                errors.append(f'{label}: missing file/path {value}')
                return None
            if strict and section and p.is_file():
                lite_sections.setdefault(p, set()).add(section)
            if p.is_file():
                try:
                    txt = p.read_text(encoding='utf-8')
                    if not txt.strip():
                        soft(f'{label}: empty {value}')
                    if MARK in txt:
                        soft(f'{label}: scaffold placeholders remain in {value}')
                except (OSError, UnicodeError):
                    soft(f'{label}: not readable UTF-8 text: {value}')
            return p
        except (ValueError, OSError) as e:
            errors.append(f'{label}: {e}')
            return None

    present = [n for n in MANIFESTS if (root / n).exists() or (root / n).is_symlink()]
    if len(present) != 1:
        errors.append('manifest: expected exactly one of PROJECT.json / PROJECT.yaml, found ' + (', '.join(present) or 'none'))
        mapped('README.md', 'README.md')
        return errors, warnings
    mpath = mapped('manifest', present[0])
    if mpath is None:
        return errors, warnings
    try:
        m = json.loads(mpath.read_text(encoding='utf-8'))
        if not isinstance(m, dict):
            raise ValueError('manifest must be object')
    except (ValueError, OSError, UnicodeError) as e:
        return errors + [f'manifest: invalid JSON-compatible YAML: {e}'], warnings
    mapped('README.md', 'README.md')
    if m.get('tier') != 'lite':
        mapped('AGENTS.md', 'AGENTS.md')
    if m.get('schema') != 'upr/1':
        errors.append('unsupported schema')
    pid, title = m.get('project_id'), m.get('title')
    if not isinstance(pid, str) or not SLUG.fullmatch(pid):
        errors.append('invalid project_id')
    if not isinstance(title, str) or not title.strip():
        errors.append('invalid title')
    profiles = m.get('profiles')
    if not isinstance(profiles, list) or not profiles or not all(isinstance(x, str) for x in profiles) \
            or len(set(profiles)) != len(profiles) or set(profiles) - PROFILES:
        errors.append('invalid profiles')
        profiles = []
    for key, allowed in (('tier', set(TIERS)), ('lifecycle', LIFECYCLES), ('visibility', VISIBILITIES)):
        if not isinstance(m.get(key), str) or m[key] not in allowed:
            errors.append(f'invalid {key}')
    roles = m.get('roles')
    if not isinstance(roles, dict):
        errors.append('roles must be object')
        roles = {}
    lite = m.get('tier') == 'lite'
    seen = {}
    for role in ROLES:
        p = mapped(f'role {role}', roles.get(role), allow_dir=not lite, section=role.upper() if lite else None)
        if p is not None:
            seen.setdefault(str(p), []).append(role)
    if m.get('tier') in ('standard', 'extended') and any(len(v) > 1 for v in seen.values()):
        warnings.append('Several roles share one file in a standard/extended project; keep sections labeled or split them.')
    if 'software' in profiles:
        s = m.get('software')
        if not isinstance(s, dict):
            errors.append('software floor references missing')
            s = {}
        for key in ('controls', 'verification'):
            mapped(f'software {key}', s.get(key), section=f'SOFTWARE {key.upper()}' if lite else None)
        warnings.append('Software floor requires substantive review and actual gates; this lint does not verify them.')
    for path, required in lite_sections.items():
        try:
            lines = path.read_text(encoding='utf-8').splitlines()
        except (UnicodeError, OSError):
            continue  # Reported by mapped().
        populated = set()
        heading = None
        for line in lines:
            if re.match(r'^#{1,6}\s', line):
                match = re.fullmatch(r'##\s+(.+?)(?:\s+[—–-]\s+.+)?\s*', line)
                heading = match[1].upper() if match else None
            elif heading in required and line.strip():
                populated.add(heading)
        for section in sorted(required - populated):
            errors.append(f'{path.relative_to(root)}: missing or empty section {section}')
    if m.get('tier') == 'extended':
        warnings.append('Review component mapping and risk register separately.')
    return list(dict.fromkeys(errors)), list(dict.fromkeys(warnings))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='action', required=True)
    i = sub.add_parser('init', help='dry-run scaffold by default; --apply writes into an absent/empty directory')
    i.add_argument('target', type=Path)
    i.add_argument('--id', required=True)
    i.add_argument('--title', required=True)
    i.add_argument('--profiles', required=True)
    i.add_argument('--tier', choices=TIERS, default='lite')
    i.add_argument('--yaml', action='store_true', help='write PROJECT.yaml (JSON-compatible) instead of PROJECT.json')
    i.add_argument('--apply', action='store_true')
    c = sub.add_parser('check', help='structure-only lint; --strict fails while placeholders remain')
    c.add_argument('target', type=Path)
    c.add_argument('--strict', action='store_true')
    a = p.parse_args(argv)
    if a.action == 'check':
        errors, warnings = check(a.target, strict=a.strict)
        status = 'FAIL' if errors else 'STRUCTURE_OK_WITH_WARNINGS' if warnings else 'STRUCTURE_OK'
        print(json.dumps({'scope': 'structure-only', 'strict': a.strict, 'errors': errors, 'warnings': warnings, 'status': status},
                         ensure_ascii=False, indent=2))
        return 1 if errors else 0
    try:
        files = build(a.id, a.title, [x.strip() for x in a.profiles.split(',')], a.tier,
                      'PROJECT.yaml' if a.yaml else 'PROJECT.json')
        root = a.target
        if root.is_symlink() or (root.exists() and (not root.is_dir() or any(root.iterdir()))):
            raise ValueError('init requires absent or empty directory; audit existing repo instead')
        for name in files:  # validate every path before writing anything
            safe_path(root, name)
        print(json.dumps({'mode': 'apply' if a.apply else 'dry-run', 'target': str(root), 'files': sorted(files),
                          'readiness': 'SCAFFOLDED_ONLY'}, indent=2))
        if a.apply:
            root.mkdir(parents=True, exist_ok=True)
            for name, content in files.items():
                path = safe_path(root, name)
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('x', encoding='utf-8') as f:
                    f.write(content)
        return 0
    except (ValueError, OSError) as e:
        print(f'ERROR: {e}; if applying, inspect any partially created files before retry', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
