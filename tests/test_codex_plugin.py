"""Contrat de la distribution Codex, sans modifier les skills amont."""

from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class CodexPluginTests(unittest.TestCase):
    def test_les_quatre_skills_amont_sont_exposes(self) -> None:
        manifest = load_json(".codex-plugin/plugin.json")
        pinned = load_json("upstream.json")["skills"]
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(
            {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()},
            set(pinned),
        )
        for name in pinned:
            with self.subTest(skill=name):
                self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file())

    def test_mcp_juridique_est_declare(self) -> None:
        manifest = load_json(".codex-plugin/plugin.json")
        self.assertEqual(manifest["mcpServers"], "./.mcp.json")
        server = load_json(".mcp.json")["mcpServers"]["droit-francais"]
        self.assertEqual(server["type"], "http")
        self.assertTrue(server["url"].startswith("https://"))

    def test_identite_du_plugin_coherente(self) -> None:
        codex = load_json(".codex-plugin/plugin.json")
        claude = load_json(".claude-plugin/plugin.json")
        self.assertEqual(codex["name"], claude["name"])
        self.assertEqual(codex["version"], claude["version"])
        self.assertEqual(codex["repository"], claude["repository"])
        self.assertEqual(codex["homepage"], claude["homepage"])

    def test_cas_prime_depart_couvre_les_trois_capacites(self) -> None:
        cases = load_json("tests/cas-plugin.json")
        self.assertEqual(len(cases), 1)
        case = cases[0]
        self.assertEqual(case["skills"], ["dirfi-fpt", "drh-fpt"])
        self.assertEqual(case["mcp"], "droit-francais")
        self.assertGreaterEqual(len(case["invariants"]), 6)
        dirfi = (ROOT / "skills/dirfi-fpt/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Co-activation dans un plugin agrégateur", dirfi)
        self.assertIn("gratification libre ou", dirfi)
        self.assertIn("ad personam", dirfi)

    def test_marketplace_distribue_la_racine_sans_copie(self) -> None:
        marketplace = load_json(".agents/plugins/marketplace.json")
        plugin = load_json(".codex-plugin/plugin.json")
        self.assertEqual(marketplace["name"], plugin["name"])
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], plugin["name"])
        self.assertEqual(
            entry["source"],
            {"source": "url", "url": plugin["repository"] + ".git", "ref": "main"},
        )
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(entry["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(entry["category"], plugin["interface"]["category"])


if __name__ == "__main__":
    unittest.main()
