"""Alignement des règles communes des surcouches (audit du 07/11/2026)."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMON = ("dpm-fpt", "drh-fpt", "dirfi-fpt")
FIVE = COMMON + ("dpo-ct", "recherche-juridique")
RULES = (
    # Campagne e : volet attribué dans un commentaire de progression avant la BASCULE.
    "Cette règle vaut aussi pour les commentaires de progression visibles avant ou entre "
    "les outils : y nommer seulement les rôles chargés, sans leur répartir de volet, "
    "ou y émettre déjà la BASCULE.",
    # Campagne g : volet d'un autre rôle traité dans le STOP.
    "Le STOP se limite à l’alerte et aux mesures conservatoires : il ne traite aucun "
    "volet confié à un autre rôle ; ce volet n’apparaît qu’après sa BASCULE.",
    # Campagne h : indisponibilité des sources non annoncée.
    "Sources désactivées, inaccessibles ou outil indisponible : l’annoncer explicitement "
    "avant l’abstention, par exemple « sources officielles indisponibles dans cette "
    "session » ; « aucun texte récupéré » ne suffit pas.",
)


def overlay(name: str) -> str:
    return (ROOT / "overlays" / f"{name}.md").read_text(encoding="utf-8")


def between(text: str, start: str, end: str) -> str:
    begin = text.index(start)
    return text[begin:text.index(end, begin)]


class OverlayAlignmentTests(unittest.TestCase):
    def test_contrat_prioritaire_identique_entre_metiers(self) -> None:
        blocks = {name: between(overlay(name), "## Contrat prioritaire", "\n## Contrat commun")
                  for name in COMMON}
        self.assertEqual(len(set(blocks.values())), 1, sorted(blocks))
        # recherche-juridique garde son item 1 propre ; les items 2 à 6 sont communs.
        start = "2. **Coactivation réelle.**"
        juridique = between(overlay("recherche-juridique"), "## Contrat prioritaire",
                            "\n## Contrat commun")
        self.assertEqual(juridique[juridique.index(start):],
                         blocks["drh-fpt"][blocks["drh-fpt"].index(start):])

    def test_routage_identique_entre_metiers(self) -> None:
        sections = {name: between(overlay(name), "## Routage explicite",
                                  "compétence sur tous les volets.")
                    for name in COMMON + ("recherche-juridique",)}
        self.assertEqual(len(set(sections.values())), 1, sorted(sections))

    def test_trois_regles_presentes_une_fois_partout(self) -> None:
        for name in FIVE:
            for relative in (f"overlays/{name}.md", f"skills/{name}/SKILL.md"):
                text = " ".join((ROOT / relative).read_text(encoding="utf-8").split())
                for rule in RULES:
                    with self.subTest(fichier=relative, regle=rule[:40]):
                        self.assertEqual(text.count(rule), 1)

    def test_aucune_mention_propre_a_la_dsi(self) -> None:
        for name in FIVE:
            with self.subTest(surcouche=name):
                self.assertNotIn("alerte cyber et aux mesures techniques", overlay(name))


if __name__ == "__main__":
    unittest.main()
