"""Deterministic, network-free v0 public skill registry helper.

Deliberately restricted frontmatter reader: single-line name and description only.
For arbitrary YAML frontmatter, use a YAML parser with a tested migration.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_META = {"version", "category", "tags", "runtime_requirements", "compatibility", "license"}

class RegistryError(ValueError):
    pass

def _unquote(value: str) -> str:
    value = value.strip()
    if not value:
        raise RegistryError("empty frontmatter value")
    if value[0] in {"'", '"'}:
        if value[-1] != value[0] or len(value) < 2:
            raise RegistryError("unclosed quoted scalar")
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError as exc:
                raise RegistryError(f"invalid quoted scalar: {exc}") from exc
        return value[1:-1].replace("''", "'")
    if value in {'|', '>', '|-', '>-'}:
        raise RegistryError("multiline metadata not supported by this portable v0 parser")
    return value

def read_skill_metadata(path: Path) -> dict:
    contents = path.read_text(encoding="utf-8-sig")
    lines = contents.splitlines()
    if not lines or lines[0].strip() != '---':
        raise RegistryError(f"{path}: missing YAML frontmatter start")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == '---')
    except StopIteration as exc:
        raise RegistryError(f"{path}: missing YAML frontmatter end") from exc
    result = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith('#') or line.startswith(' '):
            continue
        m = re.fullmatch(r"([a-z][a-z0-9_-]*):\s*(.*?)\s*", line)
        if m and m.group(1) in {'name', 'description'}:
            key = m.group(1)
            if key in result:
                raise RegistryError(f"{path}: repeated {key}")
            result[key] = _unquote(m.group(2))
    for required in ('name', 'description'):
        if not result.get(required):
            raise RegistryError(f"{path}: missing {required}")
    return result

def build(root: Path) -> dict:
    skills_root = root / 'skills'
    output = []
    for directory in sorted(skills_root.iterdir()):
        if not directory.is_dir() or directory.name.startswith('.'):
            continue
        if directory.is_symlink():
            raise RegistryError(f"refusing symlinked skill folder: {directory}")
        if not SLUG.fullmatch(directory.name):
            raise RegistryError(f"invalid skill folder: {directory.name}")
        doc = directory / 'SKILL.md'
        if not doc.exists() or doc.is_symlink():
            raise RegistryError(f"{directory.name}: missing regular SKILL.md")
        fm = read_skill_metadata(doc)
        if fm['name'] != directory.name:
            raise RegistryError(f"{directory.name}: name mismatch: {fm['name']}")
        entry = {'id': directory.name, 'name': fm['name'], 'description': fm['description'], 'entrypoint': f'skills/{directory.name}/SKILL.md'}
        metadata_file = directory / 'skill.meta.json'
        if metadata_file.exists():
            if metadata_file.is_symlink():
                raise RegistryError(f"{directory.name}: symlink metadata prohibited")
            metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
            if not isinstance(metadata, dict) or set(metadata) - ALLOWED_META:
                raise RegistryError(f"{directory.name}: invalid metadata keys")
            for key, value in metadata.items():
                if key in {'tags', 'runtime_requirements', 'compatibility'}:
                    if not isinstance(value, list) or not all(isinstance(x, str) and x for x in value):
                        raise RegistryError(f"{directory.name}: {key} must be list[str]")
                elif not isinstance(value, str) or not value:
                    raise RegistryError(f"{directory.name}: {key} must be nonempty string")
            entry.update(metadata)
        output.append(entry)
    return {'schema': 'batcave-skills/catalog/v1', 'skills': output}
