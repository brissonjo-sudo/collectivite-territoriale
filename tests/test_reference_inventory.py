"""Inventaires documentaires : aucun contrôle comportemental ni résultat de campagne."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import reference_inventory as inventory


class ReferenceInventoryTests(unittest.TestCase):
    def test_generation_exacte_pour_les_sept_arborescences(self) -> None:
        for directory in (ROOT / 'skills').iterdir():
            with self.subTest(skill=directory.name):
                expected = inventory.reference_paths(ROOT, directory.name)
                self.assertEqual(inventory.listed(inventory.render(ROOT, directory.name)), expected)
                self.assertEqual(len(expected), len(set(expected)))
                self.assertTrue(all((directory / p).is_file() for p in expected))

    def test_six_inventaires_installes_DCP_bloque_par_contrat_DCP0(self) -> None:
        # Le septième inventaire est proposé hors candidat : aucune exception DCP-0 ajoutée.
        names = {p.name for p in (ROOT / 'skills').iterdir()} - {'dcp-fpt'}
        self.assertEqual(len(names), 6)
        for name in names:
            with self.subTest(skill=name):
                text = (ROOT / 'skills' / name / 'SKILL.md').read_text(encoding='utf-8')
                self.assertEqual(inventory.listed(text), inventory.reference_paths(ROOT, name))

    def test_formes_documentaires_dans_le_contrat_commun_juridique(self) -> None:
        text = (ROOT / 'skills/recherche-juridique/SKILL.md').read_text(encoding='utf-8')
        for fragment in ('Select-Object -First N', '-Skip M -First N', 'jamais par `-Skip` seul',
                         'jamais par une autre commande'):
            self.assertIn(fragment, text)

    def test_inventaire_manquant_ou_duplique_refuse(self) -> None:
        for text in ('absent', inventory.BEGIN + inventory.END + inventory.BEGIN):
            with self.subTest(text=text), self.assertRaises(ValueError):
                inventory.listed(text)


if __name__ == '__main__':
    unittest.main()
