"""Issue #21 : ressources de skill refusées sur tout hôte, sans réseau."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from skill_citation import forbidden_skill_path
import campaign_contract as contract
import run_codex_campaign as campaign


class SkillCitationURLTests(unittest.TestCase):
    def test_contre_exemple_github_et_integration_campagne(self) -> None:
        text = '[skill](https://github.com/brissonjo-sudo/collectivite-territoriale/blob/main/skills/dsi-fpt/SKILL.md)'
        self.assertTrue(forbidden_skill_path(text))
        case = next(c for c in contract.load_cycle_cases(ROOT, 'scripts/cas-plugin-cycle-v4.json')
                    if c['id'] == 'l8-dsi-technique-spontanee')
        errors = campaign.failures([{'type': 'reply', 'text': text}, {'type': 'turn_completed'}], case, 0)
        self.assertIn('skill_path_in_response', errors)

    def test_variantes_url_refusees(self) -> None:
        urls = [
            'https://raw.githubusercontent.com/brissonjo-sudo/collectivite-territoriale/main/skills/dsi-fpt/SKILL.md',
            'https://example.org/skills/dsi-fpt/%53%4b%49%4c%4c%2emd',
            'https://example.org/skills%2Fdsi-fpt%2FSKILL.md',
            'https://example.org/references/x.md',
            'https://example.org/%72eferences%2Fx.md',
            'https://example.org/objets/x.md',
            'https://example.org/objets/x.json',
            'https://example.org/.agents/skills/dsi-fpt/guide.txt',
            'https://example.org/%2eagents%2Fskills%2Fdsi-fpt%2Fguide.txt',
            'HTTP://EXAMPLE.ORG/REFERENCES/X.MD',
            'https://example.org/SKILL.md?raw=1#section',
            # Un hôte officiel ne donne pas d'exemption à une cible interdite.
            'https://www.senat.fr/skills/dsi-fpt/SKILL.md',
        ]
        for url in urls:
            for text in (url, '<' + url + '>', '[skill](' + url + ')', '[skill](<' + url + '>)'):
                with self.subTest(text=text):
                    self.assertTrue(forbidden_skill_path(text))

    def test_sources_officielles_mesurees_restent_permises(self) -> None:
        # URL exactes de campagne-l140-d, sans assertion sur leur contenu juridique.
        # Les trois premières apparaissent dans les réponses ; EUR-Lex dans la
        # trace web de plugin-violation-donnees, pas dans sa réponse finale.
        urls = [
            'https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044424763',
            'https://www.senat.fr/questions/base/2024/qSEQ241001222.html',
            'https://www.cnil.fr/fr/violations-de-donnees-personnelles-les-regles-suivre',
            'https://eur-lex.europa.eu/eli/reg/2016/679/oj/fra',
        ]
        for url in urls:
            for text in (url, '<' + url + '>', '[source](' + url + ')'):
                with self.subTest(text=text):
                    self.assertFalse(forbidden_skill_path(text))

    def test_citation_nom_section_et_liens_sans_ressource(self) -> None:
        for text in ('dsi-fpt, section Sécurité', 'SKILL.md, section Déclenchement',
                     '[documentation](https://example.org/documentation.html)'):
            with self.subTest(text=text):
                self.assertFalse(forbidden_skill_path(text))

    def test_chemins_locaux_restent_refuses(self) -> None:
        for text in ('[skill](dsi-fpt/SKILL.md)', '[ref](references/x.md)',
                     '[objet](objets/x.md)', '.agents/skills/dsi-fpt/guide.txt',
                     '[skill](file:///skills/dsi-fpt/SKILL.md)'):
            with self.subTest(text=text):
                self.assertTrue(forbidden_skill_path(text))
