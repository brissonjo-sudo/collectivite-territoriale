"""Contrôle les frontières du remplacement de section, sans oracle métier."""
from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from instruction_overlays import apply_overlays, validate_overlays


class ReplaceBlockTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'overlays').mkdir()
        self.anchor = b'### Old\nold instruction\n\n'
        self.content = b'### Old\nnew instruction\n\n'
        self.base = b'---\nname: test\n---\n# Entry\n' + self.anchor + b'### Next\nuntouched\n'
        (self.root / 'overlays/block.md').write_bytes(self.content)
        self.spec = {'target':'SKILL.md','source':'overlays/block.md','operation':'replace-block',
                     'anchor':self.anchor.decode(),'base_sha256':self.sha(self.base),
                     'source_sha256':self.sha(self.content)}

    @staticmethod
    def sha(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def test_section_remplacee_et_tous_les_autres_octets_preserves(self) -> None:
        original = {'SKILL.md':self.base, 'references/test.md':b'reference', 'LICENSE':b'license'}
        result = apply_overlays(self.root, original, [self.spec])
        self.assertEqual(result['SKILL.md'], self.base.replace(self.anchor, self.content, 1))
        self.assertEqual(original['SKILL.md'], self.base)
        self.assertEqual(result['references/test.md'], b'reference')
        self.assertEqual(result['LICENSE'], b'license')

    def test_refuse_ancre_absente_et_dupliquee(self) -> None:
        for base in [self.base.replace(self.anchor,b''), self.base + self.anchor]:
            spec = {**self.spec,'base_sha256':self.sha(base)}
            with self.subTest(base=base), self.assertRaisesRegex(ValueError,'ancre'):
                apply_overlays(self.root, {'SKILL.md':base}, [spec])

    def test_refuse_empreintes_base_source_et_operation_dupliquee(self) -> None:
        with self.assertRaisesRegex(ValueError,'amont divergente'):
            apply_overlays(self.root, {'SKILL.md':self.base+b'drift'}, [self.spec])
        (self.root/'overlays/block.md').write_bytes(self.content+b'drift')
        with self.assertRaisesRegex(ValueError,'locale divergente'):
            apply_overlays(self.root, {'SKILL.md':self.base}, [self.spec])
        with self.assertRaisesRegex(ValueError,'dupliquée'):
            validate_overlays([self.spec,self.spec])

    def test_refuse_reference_et_source_non_markdown(self) -> None:
        for mutation in [{'target':'references/test.md'}, {'source':'overlays/block.yaml'}]:
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate_overlays([{**self.spec,**mutation}])

    def test_refuse_ancre_partielle_et_deux_sections(self) -> None:
        for anchor in [b'### Old\n', self.anchor+b'### Next\nuntouched\n']:
            spec = {**self.spec,'anchor':anchor.decode()}
            with self.subTest(anchor=anchor), self.assertRaisesRegex(ValueError,'section'):
                apply_overlays(self.root, {'SKILL.md':self.base}, [spec])

    def test_refuse_modification_du_frontmatter(self) -> None:
        base = b'---\nname: test\n' + self.anchor + b'---\n# Entry\n'
        spec = {**self.spec,'base_sha256':self.sha(base)}
        with self.assertRaisesRegex(ValueError,'frontmatter'):
            apply_overlays(self.root, {'SKILL.md':base}, [spec])

    def test_refuse_changement_titre_et_extension_sur_autre_section(self) -> None:
        for content in [self.content.replace(b'### Old',b'### New'),self.content+b'### Extra\nextra\n']:
            (self.root/'overlays/block.md').write_bytes(content)
            spec = {**self.spec,'source_sha256':self.sha(content)}
            with self.subTest(content=content), self.assertRaisesRegex(ValueError,'section'):
                apply_overlays(self.root, {'SKILL.md':self.base}, [spec])

    def test_reconstruction_ordonnee_exige_empreinte_intermediaire(self) -> None:
        insertion_content=b'## Priority\ncontract\n'
        (self.root/'overlays/priority.md').write_bytes(insertion_content)
        insertion={'target':'SKILL.md','source':'overlays/priority.md','anchor':'# Entry',
                   'base_sha256':self.sha(self.base),'source_sha256':self.sha(insertion_content)}
        intermediate=apply_overlays(self.root, {'SKILL.md':self.base}, [insertion])['SKILL.md']
        replacement={**self.spec,'base_sha256':self.sha(intermediate)}
        result=apply_overlays(self.root, {'SKILL.md':self.base}, [insertion,replacement])
        self.assertEqual(result['SKILL.md'],intermediate.replace(self.anchor,self.content,1))
        with self.assertRaisesRegex(ValueError,'amont divergente'):
            apply_overlays(self.root, {'SKILL.md':self.base}, [insertion,self.spec])


if __name__=='__main__':
    unittest.main()
