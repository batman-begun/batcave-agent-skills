import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from registry_core import RegistryError, build

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'skills').mkdir()

    def create_skill(self, slug='sample-skill', name='sample-skill', description='Helps with one task.'):
        directory = self.root / 'skills' / slug
        directory.mkdir()
        (directory / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: {description}\n---\n# Skill\n', encoding='utf-8')
        return directory

    def test_empty_registry(self):
        self.assertEqual(build(self.root)['skills'], [])

    def test_valid_skill(self):
        self.create_skill()
        entry = build(self.root)['skills'][0]
        self.assertEqual(entry['entrypoint'], 'skills/sample-skill/SKILL.md')

    def test_wrong_name_rejected(self):
        self.create_skill(name='another-name')
        with self.assertRaisesRegex(RegistryError, 'mismatch'):
            build(self.root)

    def test_missing_skill_md_rejected(self):
        (self.root / 'skills' / 'broken').mkdir()
        with self.assertRaisesRegex(RegistryError, 'missing regular SKILL.md'):
            build(self.root)

    def test_metadata_accepted(self):
        d = self.create_skill()
        (d / 'skill.meta.json').write_text(json.dumps({'category':'education','tags':['language']}))
        self.assertEqual(build(self.root)['skills'][0]['category'], 'education')

    def test_invalid_metadata_rejected(self):
        d = self.create_skill()
        (d / 'skill.meta.json').write_text(json.dumps({'evil-field':'x'}))
        with self.assertRaisesRegex(RegistryError, 'invalid metadata keys'):
            build(self.root)

    def test_multiline_desc_rejected(self):
        self.create_skill(description='>')
        with self.assertRaisesRegex(RegistryError, 'multiline'):
            build(self.root)

if __name__ == '__main__':
    unittest.main()
