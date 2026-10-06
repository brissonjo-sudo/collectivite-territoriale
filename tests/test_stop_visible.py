"""Régressions du premier texte visible, sans confondre mise en forme et préambule."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_coactivation_v2 import observable_checks


class PremierTexteVisible(unittest.TestCase):
    """Exerce la décision déterministe sur des événements de réponse ordonnés."""

    def examiner(self, texts: list[str]) -> bool:
        """Construit une trace minimale avec un garde-fou exigé."""
        events = [{"type": "assistant_text", "text": text, "event_id": f"e{index}"}
                  for index, text in enumerate(texts)]
        case = {"invariant_objects": [{"deterministic_check": "stop_first"}]}
        return observable_checks(events, case)["stop_first"]

    def test_garde_fou_visible_sans_pretexte(self) -> None:
        for text in ("STOP — Incident", "**STOP** — Incident", "## STOP — Incident",
                     "```\nSTOP — Incident\n```", "```text\nSTOP APJA\n```"):
            with self.subTest(text=text):
                self.assertTrue(self.examiner([text]))

    def test_annonce_titre_et_separateur_restent_refuses(self) -> None:
        for text in ("Je charge les rôles.\nSTOP", "## Analyse\nSTOP",
                     "---\nSTOP", "```\nJe recherche.\nSTOP\n```"):
            with self.subTest(text=text):
                self.assertFalse(self.examiner([text]))
        self.assertFalse(self.examiner(["Je charge les rôles.", "STOP"]))
