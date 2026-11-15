"""Contrat de la distribution Antigravity (ADR 0037), sans toucher aux skills."""

from __future__ import annotations

import unittest

from test_codex_plugin import ROOT, load_json

# Champs de premier niveau lus par Antigravity ; les autres sont ignorés en silence.
CHAMPS_ADMIS = {"name", "description", "logo", "suggestedPrompts", "displayName",
                "version", "author", "homepage", "repository", "disabled"}


class AntigravityPluginTests(unittest.TestCase):
    def test_identite_alignee_sur_les_autres_manifestes(self) -> None:
        antigravity = load_json("plugin.json")
        for relative in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
            other = load_json(relative)
            for key in ("name", "version", "repository", "homepage"):
                with self.subTest(manifeste=relative, champ=key):
                    self.assertEqual(antigravity[key], other[key])

    def test_champs_admis_et_logo_present(self) -> None:
        manifest = load_json("plugin.json")
        self.assertLessEqual(set(manifest), CHAMPS_ADMIS)
        self.assertTrue((ROOT / manifest["logo"]).is_file())
        self.assertLessEqual(len(manifest["suggestedPrompts"]), 3)

    def test_mcp_juridique_sans_pont_ni_secret(self) -> None:
        servers = load_json("mcp_config.json")["mcpServers"]
        self.assertEqual(set(servers), {"droit-francais"})
        server = servers["droit-francais"]
        reference = load_json(".mcp.json")["mcpServers"]["droit-francais"]
        self.assertEqual(set(server), {"serverUrl", "oauth"})
        self.assertEqual(server["serverUrl"], reference["url"])
        self.assertEqual(server["oauth"], {"clientId": reference["oauth"]["clientId"]})


if __name__ == "__main__":
    unittest.main()
