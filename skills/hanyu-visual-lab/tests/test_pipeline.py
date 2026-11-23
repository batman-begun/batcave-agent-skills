from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

SPEC=importlib.util.spec_from_file_location('hanyu_render',Path(__file__).resolve().parents[1]/'scripts'/'render.py')
r=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r)
ROOT=Path(__file__).resolve().parents[1]

class PipelineTests(unittest.TestCase):
    def test_import_three_columns(self):
        rows=r.load_table(ROOT/'examples'/'short-table.tsv')
        self.assertEqual(len(rows),4)
        self.assertEqual(rows[0]['hanzi'],'听音乐')
        self.assertEqual(rows[1]['pinyin'],'chàng yì shǒu gē')
    def test_validate_example(self):
        d=r.dict_from_json(ROOT/'examples'/'home-leisure.json')
        errors,warnings=r.validate(d)
        self.assertEqual(errors,[])
        self.assertEqual(len(r.item_index(d)),20)
    def test_duplicate_id_rejected(self):
        d=r.dict_from_json(ROOT/'examples'/'home-leisure.json')
        d['sections'][1]['items'][0]['id']='01'
        self.assertIn('Duplicate item ids',r.validate(d)[0])
    def test_reject_more_than_twenty(self):
        d=r.dict_from_json(ROOT/'examples'/'home-leisure.json')
        item=dict(d['sections'][0]['items'][0]);item['id']='21'
        d['sections'][0]['items'].append(item)
        self.assertTrue(any('More than 20' in x for x in r.validate(d)[0]))
    def test_script_does_not_synthesize_data(self):
        d=r.dict_from_json(ROOT/'examples'/'home-leisure.json')
        markup=r.make_html(d,ROOT)
        self.assertEqual(markup.count('data-entry='),20)
        self.assertIn('tīng yīnyuè',markup)
        self.assertIn('rất đáng yêu',markup)

if __name__=='__main__':unittest.main()
