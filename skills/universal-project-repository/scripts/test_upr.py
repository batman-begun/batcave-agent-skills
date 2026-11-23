import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from upr import main, check


class Tests(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.addCleanup(self.d.cleanup)
        self.root = Path(self.d.name) / 'project'

    def run_main(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return main(list(args))

    def init(self, profiles='software', tier='standard', apply=True, *extra):
        return self.run_main('init', str(self.root), '--id', 'sample', '--title', 'Sample', '--profiles', profiles,
                             '--tier', tier, *(['--apply'] if apply else []), *extra)

    def manifest_path(self):
        return self.root / ('PROJECT.json' if (self.root / 'PROJECT.json').exists() else 'PROJECT.yaml')

    def edit(self, fn):
        p = self.manifest_path()
        m = json.loads(p.read_text())
        fn(m)
        p.write_text(json.dumps(m))

    def fill(self):
        for f in self.root.rglob('*.md'):
            f.write_text(f.read_text().replace('UPR-TODO', 'FILLED'))

    # --- v1.0.0 behaviours (kept) ---
    def test_dry_run(self):
        self.assertEqual(self.init(apply=False), 0)
        self.assertFalse(self.root.exists())

    def test_software(self):
        self.assertEqual(self.init(), 0)
        e, w = check(self.root)
        self.assertFalse(e)
        self.assertTrue(w)
        self.assertTrue((self.root / 'harness/CONTROLS.md').exists())

    def test_micro_software(self):
        self.assertEqual(self.init(tier='micro'), 0)
        self.assertFalse(check(self.root)[0])
        self.assertTrue((self.root / 'verification/SOFTWARE.md').exists())

    def test_mixed(self):
        self.assertEqual(self.init('comic,software', 'extended'), 0)
        self.assertFalse(check(self.root)[0])
        self.assertTrue((self.root / 'harness/CONTROLS.md').exists())

    def test_private_journal(self):
        self.assertEqual(self.init('contemplation', 'micro'), 0)
        self.assertFalse(check(self.root)[0])
        self.assertFalse((self.root / 'harness').exists())
        self.assertEqual(json.loads(self.manifest_path().read_text())['visibility'], 'local')

    def test_no_overwrite(self):
        self.root.mkdir()
        (self.root / 'keep').write_text('original')
        self.assertEqual(self.init(), 2)
        self.assertEqual((self.root / 'keep').read_text(), 'original')
        self.assertFalse((self.root / 'PROJECT.json').exists())

    def test_missing_role(self):
        self.init()
        (self.root / 'state/STATUS.md').unlink()
        self.assertTrue(check(self.root)[0])

    def test_path_escape(self):
        self.init()
        self.edit(lambda m: m['roles'].update(state='../outside'))
        self.assertTrue(check(self.root)[0])

    def test_missing_software(self):
        self.init()
        self.edit(lambda m: m.pop('software'))
        self.assertTrue(check(self.root)[0])

    def test_malformed_manifest(self):
        self.init()
        self.edit(lambda m: m.update(profiles=[{}], tier=[]))
        self.assertTrue(check(self.root)[0])

    def test_symlink_role(self):
        self.init()
        (self.root / 'state/STATUS.md').unlink()
        (self.root / 'state/STATUS.md').symlink_to(self.root / 'README.md')
        self.assertTrue(check(self.root)[0])

    def test_unknown_profile(self):
        self.assertEqual(self.init('alien'), 2)
        self.assertFalse(self.root.exists())

    # --- v1.1.0 additions ---
    def test_lite_is_default_and_has_three_files(self):
        self.assertEqual(self.run_main('init', str(self.root), '--id', 'sample', '--title', 'Sample',
                                       '--profiles', 'knowledge', '--apply'), 0)
        names = sorted(p.name for p in self.root.rglob('*') if p.is_file())
        self.assertEqual(names, ['PROJECT.json', 'README.md', 'STATE.md'])
        self.assertFalse(check(self.root)[0])

    def test_lite_keeps_software_floor(self):
        self.assertEqual(self.init('software', 'lite'), 0)
        m = json.loads((self.root / 'PROJECT.json').read_text())
        self.assertEqual(m['software'], {'controls': 'STATE.md', 'verification': 'STATE.md'})
        txt = (self.root / 'STATE.md').read_text()
        self.assertIn('SOFTWARE CONTROLS — NOT CONFIGURED', txt)
        self.assertIn('SOFTWARE VERIFICATION — NOT RUN', txt)
        self.assertFalse(check(self.root)[0])
        self.edit(lambda m: m.pop('software'))
        self.assertTrue(check(self.root)[0])

    def test_lite_does_not_create_directories(self):
        self.init('software', 'lite')
        self.assertEqual([p for p in self.root.iterdir() if p.is_dir()], [])

    def test_agents_required_above_lite(self):
        self.init('knowledge', 'standard')
        (self.root / 'AGENTS.md').unlink()
        self.assertTrue(check(self.root)[0])

    def test_strict_fails_on_placeholders_but_lenient_passes(self):
        self.init('software', 'lite')
        self.assertEqual(self.run_main('check', str(self.root)), 0)
        self.assertEqual(self.run_main('check', str(self.root), '--strict'), 1)
        e, _ = check(self.root, strict=True)
        self.assertTrue(any('placeholders' in x for x in e))

    def test_strict_passes_when_filled(self):
        self.init('software', 'lite')
        self.fill()
        self.assertEqual(self.run_main('check', str(self.root), '--strict'), 0)

    def test_strict_fails_on_empty_role_file(self):
        self.init('knowledge', 'standard')
        self.fill()
        (self.root / 'state/STATUS.md').write_text('')
        self.assertEqual(self.run_main('check', str(self.root), '--strict'), 1)

    def test_strict_rejects_missing_and_empty_lite_sections(self):
        self.init('software', 'lite')
        self.fill()
        (self.root / 'STATE.md').write_text('# Sample\n\n## INTENT\n', encoding='utf-8')
        errors, _ = check(self.root, strict=True)
        self.assertEqual(sum('missing or empty section' in error for error in errors), 10)

    def test_strict_rejects_unreadable_lite_record(self):
        self.init('software', 'lite')
        self.fill()
        (self.root / 'STATE.md').write_bytes(b'\xff')
        errors, _ = check(self.root, strict=True)
        self.assertTrue(any('not readable UTF-8' in error for error in errors))

    def test_malformed_control_reference_returns_lint_error(self):
        self.init('software', 'lite')
        self.fill()
        self.edit(lambda manifest: manifest['software'].update(controls=[]))
        errors, _ = check(self.root, strict=True)
        self.assertIn('software controls: expected relative POSIX path', errors)

    def test_yaml_manifest_still_supported(self):
        self.assertEqual(self.init('knowledge', 'lite', True, '--yaml'), 0)
        self.assertTrue((self.root / 'PROJECT.yaml').exists())
        self.assertFalse((self.root / 'PROJECT.json').exists())
        self.assertFalse(check(self.root)[0])

    def test_two_manifests_is_an_error(self):
        self.init('knowledge', 'lite')
        (self.root / 'PROJECT.yaml').write_text((self.root / 'PROJECT.json').read_text())
        e, _ = check(self.root)
        self.assertTrue(any('exactly one' in x for x in e))

    def test_no_manifest_is_an_error(self):
        self.root.mkdir()
        (self.root / 'README.md').write_text('hi')
        self.assertEqual(self.run_main('check', str(self.root)), 1)

    def test_check_never_writes(self):
        self.init('software', 'standard')
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        check(self.root)
        check(self.root, strict=True)
        after = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_invalid_id_writes_nothing(self):
        # an invalid project id must be rejected before anything is written
        self.assertEqual(self.run_main('init', str(self.root), '--id', 'Bad_ID', '--title', 'x', '--profiles', 'software', '--apply'), 2)
        self.assertFalse(self.root.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
