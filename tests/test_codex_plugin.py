"""Contrat de la distribution Codex, sans modifier les skills amont."""

from __future__ import annotations

import hashlib
import json
import os
import struct
import subprocess
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_plugin_campaign import build_command, build_prompt, technical_failures, sanitize  # noqa: E402


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class CodexPluginTests(unittest.TestCase):
    def test_les_cinq_skills_amont_sont_exposes(self) -> None:
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

    def test_recherche_juridique_est_autonome_et_sans_secret(self) -> None:
        skill = ROOT / "skills/recherche-juridique"
        entrypoint = (skill / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("version: 3.5.0", entrypoint)
        self.assertTrue((skill / "references/format-citation.md").is_file())
        self.assertTrue((skill / "profils/collectivites.md").is_file())
        self.assertTrue((skill / "scripts/legifrance.py").is_file())
        self.assertTrue((skill / "LICENSE").is_file())
        self.assertFalse((skill / "skill").exists())
        self.assertFalse((skill / "skills").exists())
        forbidden = [
            path.relative_to(skill).as_posix()
            for path in skill.rglob("*")
            if path.is_file()
            and (path.name == ".env" or path.suffix == ".pyc" or "__pycache__" in path.parts)
        ]
        self.assertEqual(forbidden, [])

    def test_mcp_juridique_est_declare(self) -> None:
        manifest = load_json(".codex-plugin/plugin.json")
        self.assertEqual(manifest["mcpServers"], "./.mcp.json")
        server = load_json(".mcp.json")["mcpServers"]["droit-francais"]
        self.assertEqual(len(load_json(".mcp.json")["mcpServers"]), 1)
        self.assertEqual(server["type"], "http")
        self.assertTrue(server["url"].startswith("https://"))
        self.assertEqual(
            server["oauth"],
            {
                "clientId": "tpc_gCoyj4qPSuyrg1ZZWDyp4D",
                "callbackPort": 44956,
            },
        )
        self.assertNotIn("clientSecret", server["oauth"])

    def test_identite_du_plugin_coherente(self) -> None:
        codex = load_json(".codex-plugin/plugin.json")
        claude = load_json(".claude-plugin/plugin.json")
        self.assertEqual(codex["name"], claude["name"])
        self.assertEqual(codex["version"], claude["version"])
        self.assertEqual(codex["repository"], claude["repository"])
        self.assertEqual(codex["homepage"], claude["homepage"])
        self.assertEqual(codex["license"], "CC-BY-SA-4.0")
        self.assertEqual(claude["license"], "CC-BY-SA-4.0")
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn(
            "Creative Commons Attribution-ShareAlike 4.0 International",
            license_text,
        )

    def test_distribution_epinglee_sur_etiquette(self) -> None:
        """La marketplace distribue une étiquette publiée, pas l'état de main."""
        manifest = load_json(".codex-plugin/plugin.json")
        entry = load_json(".claude-plugin/marketplace.json")["plugins"][0]
        published = entry["version"]
        source = entry["source"]
        self.assertEqual(source["source"], "github")
        self.assertEqual("https://github.com/" + source["repo"], manifest["repository"])
        self.assertEqual(source["ref"], f"v{published}")
        self.assertRegex(source["sha"], r"^[0-9a-f]{40}$")
        # main peut porter un candidat plus récent que la version distribuée,
        # jamais une version plus ancienne.
        self.assertLessEqual(
            tuple(int(part) for part in published.split(".")),
            tuple(int(part) for part in manifest["version"].split(".")),
        )
        registre = (ROOT / "docs/publication.md").read_text(encoding="utf-8")
        self.assertIn(f"| `{source['ref']}` | `{source['sha']}` |", registre)

    def test_etiquette_designe_le_commit_epingle(self) -> None:
        """L'étiquette distribuée existe et désigne le commit épinglé.

        Hors CI, l'absence de l'étiquette locale saute le test ; en CI
        (CT_EXIGER_ETIQUETTE=1, historique complet), elle le fait échouer, ce
        qui empêche de fusionner un épinglage vers une étiquette inexistante.
        """
        source = load_json(".claude-plugin/marketplace.json")["plugins"][0]["source"]
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "--quiet", f"refs/tags/{source['ref']}^{{commit}}"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            message = f"Étiquette {source['ref']} absente : la créer sur {source['sha']} avant fusion"
            if os.environ.get("CT_EXIGER_ETIQUETTE") == "1":
                self.fail(message)
            self.skipTest(message)
        self.assertEqual(result.stdout.strip(), source["sha"])

    def test_metadonnees_publiques_et_iconographie(self) -> None:
        manifest = load_json(".codex-plugin/plugin.json")
        interface = manifest["interface"]
        self.assertEqual(interface["composerIcon"], "./assets/icon.png")
        self.assertEqual(interface["logo"], "./assets/icon.png")
        self.assertEqual(
            interface["privacyPolicyURL"],
            "https://github.com/brissonjo-sudo/collectivite-territoriale/"
            "blob/main/PRIVACY.md",
        )

        icon = ROOT / "assets/icon.png"
        data = icon.read_bytes()
        self.assertLessEqual(len(data), 5 * 1024 * 1024)
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(data[12:16], b"IHDR")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual(width, height)
        self.assertGreaterEqual(width, 48)
        self.assertLessEqual(width, 4096)
        self.assertEqual(
            hashlib.sha256(data).hexdigest().upper(),
            "10ACA45CB876735F06E10B352B9A2BA004B5DEAE462E08D8DFBA092044AAEE1F",
        )

        privacy = (ROOT / "PRIVACY.md").read_text(encoding="utf-8")
        for heading in (
            "## Données traitées",
            "## Finalités",
            "## Destinataires et prestataires",
            "## Conservation",
            "## Choix et droits des utilisateurs",
            "## Sécurité et mises à jour",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, privacy)
        self.assertIn("droit-francais-skill", privacy)

    def test_cas_plugin_couvrent_les_coactivations_juridiques(self) -> None:
        cases = load_json("tests/cas-plugin.json")
        self.assertEqual(len(cases), 4)
        by_id = {case["id"]: case for case in cases}
        self.assertEqual(
            by_id["plugin-prime-depart-retraite"]["skills"],
            ["dirfi-fpt", "drh-fpt", "recherche-juridique"],
        )
        self.assertEqual(
            by_id["plugin-garde-fou-apja"]["skills"],
            ["dpm-fpt", "recherche-juridique"],
        )
        self.assertEqual(
            by_id["plugin-violation-donnees"]["skills"],
            ["dpo-ct", "recherche-juridique"],
        )
        self.assertEqual(
            by_id["plugin-mcp-indisponible"]["skills"],
            ["recherche-juridique"],
        )
        for case in cases[:3]:
            self.assertEqual(case["mcp"], "droit-francais")
            self.assertEqual(case["mcp_mode"], "required")
            self.assertEqual(case["activation_sequence"], case["skills"])
            self.assertGreaterEqual(case["max_budget_usd"], 1.0)
            self.assertGreaterEqual(len(case["invariants"]), 4)
        self.assertEqual(by_id["plugin-violation-donnees"]["web_mode"], "official_source")
        self.assertEqual(
            by_id["plugin-violation-donnees"]["official_source_hosts"],
            ["eur-lex.europa.eu", "www.cnil.fr"],
        )
        degraded = by_id["plugin-mcp-indisponible"]
        self.assertIsNone(degraded["mcp"])
        self.assertEqual(degraded["mcp_mode"], "disabled")
        self.assertEqual(degraded["activation_sequence"], degraded["skills"])
        self.assertGreaterEqual(degraded["max_budget_usd"], 0.5)
        self.assertEqual(degraded["web_mode"], "disabled")
        self.assertGreaterEqual(len(degraded["invariants"]), 4)
        dirfi = (ROOT / "skills/dirfi-fpt/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Co-activation dans un plugin agrégateur", dirfi)
        self.assertIn("gratification libre ou", dirfi)
        self.assertIn("ad personam", dirfi)

    def test_harnais_impose_isolation_et_activation_qualifiee(self) -> None:
        cases = load_json("tests/cas-plugin.json")
        prime = next(case for case in cases if case["id"] == "plugin-prime-depart-retraite")
        command = build_command(prime, "claude")
        prompt = build_prompt(prime)
        self.assertIn("--strict-mcp-config", command)
        self.assertIn("--restricted", command)
        self.assertIn("--tools", command)
        self.assertIn("--no-session-persistence", command)
        self.assertIn("--permission-prompts", command)
        self.assertIn("collectivite-territoriale:dirfi-fpt", prompt)
        self.assertIn("collectivite-territoriale:drh-fpt", prompt)
        self.assertIn("collectivite-territoriale:recherche-juridique", prompt)

        dpo = next(case for case in cases if case["id"] == "plugin-violation-donnees")
        dpo_command = build_command(dpo, "claude")
        self.assertEqual(dpo_command[dpo_command.index("--tools") + 1], "Skill,Read,WebFetch")
        degraded = next(case for case in cases if case["id"] == "plugin-mcp-indisponible")
        degraded_command = build_command(degraded, "claude")
        self.assertEqual(degraded_command[degraded_command.index("--tools") + 1], "Skill,Read")
        self.assertIn("Read(./skills/**)", command[command.index("--allowedTools") + 1])

    def test_lecture_des_references_bornee_et_assainie(self) -> None:
        case = load_json("tests/cas-plugin.json")[0]
        calls = [
            {"type": "tool_use", "name": "Read", "id": "read1",
             "input": {"file_path": str(ROOT / "skills/recherche-juridique/references/modules.md")}},
            {"type": "tool_use", "name": "Read", "id": "read2",
             "input": {"file_path": str(ROOT / ".env")}},
        ]
        clean = sanitize([{"message": {"content": calls}},
                          {"message": {"content": [{"type": "tool_result", "tool_use_id": "read1", "content": "NOT_TO_RETAIN"}]}}], case)
        self.assertEqual(clean[0]["type"], "plugin_file_read")
        self.assertTrue(clean[0]["succeeded"])
        self.assertEqual(clean[0]["path"], "recherche-juridique/references/modules.md")
        self.assertEqual(clean[1]["type"], "unexpected_tool_call")
        self.assertNotIn("NOT_TO_RETAIN", json.dumps(clean))

    def test_mcp_desactive_refuse_meme_un_appel_en_echec(self) -> None:
        case = load_json("tests/cas-plugin.json")[-1]
        self.assertIn("plugin_mcp_call_unexpected", technical_failures([
            {"type": "plugin_mcp_call", "succeeded": False}
        ], case))

    def test_harnais_refuse_skill_autonome_et_mcp_etranger(self) -> None:
        case = next(
            case
            for case in load_json("tests/cas-plugin.json")
            if case["id"] == "plugin-garde-fou-apja"
        )
        clean = [
            {
                "type": "init",
                "standalone_recherche_juridique_loaded": True,
            },
            {
                "type": "skill_activation",
                "skill": "collectivite-territoriale:dpm-fpt",
            },
            {
                "type": "skill_activation",
                "skill": "collectivite-territoriale:recherche-juridique",
            },
            {"type": "foreign_mcp_call", "tool": "mcp__claude_ai_Droit_Francais__search"},
            {"type": "unexpected_tool_call", "tool": "WebFetch"},
            {"type": "result", "is_error": False},
        ]
        failures = technical_failures(clean, case)
        self.assertIn("standalone_recherche_juridique_loaded", failures)
        self.assertIn("foreign_mcp_call", failures)
        self.assertIn("unexpected_tool_call", failures)
        self.assertIn("plugin_mcp_call_missing", failures)

    def test_preuve_comportementale_respecte_le_contrat(self) -> None:
        evidence = load_json("tests/evidence/2026-09-20-validation-locale.json")
        cases = {case["id"]: case for case in load_json("tests/cas-plugin.json")}
        self.assertEqual(evidence["plugin_version"], "1.1.0")
        self.assertRegex(evidence["plugin_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(
            set(evidence["available_skills"]),
            set(load_json("upstream.json")["skills"]),
        )
        runs = {run["case_id"]: run for run in evidence["runs"]}
        self.assertEqual(set(runs), set(cases))
        for case_id, run in runs.items():
            with self.subTest(case=case_id):
                self.assertIn(run["status"], {"passed", "failed", "blocked"})
                self.assertTrue((ROOT / run["evidence_path"]).is_file())
                self.assertIsInstance(run["activated_skills"], list)
                self.assertIsInstance(run["mcp_tools"], list)
                self.assertIsInstance(run["invariants"], dict)
                if run["status"] == "passed":
                    self.assertTrue(
                        set(cases[case_id]["skills"]).issubset(
                            run["activated_skills"]
                        )
                    )
                    self.assertTrue(all(run["invariants"].values()))
                    if cases[case_id]["mcp_mode"] == "required":
                        self.assertTrue(
                            any(
                                tool.startswith("mcp__droit-francais__")
                                for tool in run["mcp_tools"]
                            )
                        )
                    else:
                        self.assertEqual(run["mcp_status"], "disabled")
                        self.assertEqual(run["mcp_tools"], [])
        self.assertEqual(
            evidence["release_ready"],
            all(run["status"] == "passed" for run in runs.values())
            and evidence.get("review", {}).get("human_legal_validation") is True
            and evidence.get("codex_smoke", {}).get("status") == "passed"
            and evidence.get("codex_smoke", {}).get("plugin_commit") == evidence["plugin_commit"],
        )

    def test_preuve_courante_correspond_au_runtime(self) -> None:
        manifest = load_json(".codex-plugin/plugin.json")
        evidence = load_json(f"tests/evidence/release-{manifest['version']}.json")
        self.assertEqual(evidence["plugin_version"], manifest["version"])
        self.assertEqual(
            evidence["upstream_commits"],
            {name: spec["commit"] for name, spec in load_json("upstream.json")["skills"].items()},
        )
        cases = {case["id"]: case for case in load_json("tests/cas-plugin.json")}
        runs = {run["case_id"]: run for run in evidence["runs"]}
        self.assertEqual(len(runs), len(evidence["runs"]))
        qualified_runs = set(runs) == set(cases) and all(
            run["status"] == "passed"
            and run.get("plugin_commit") == evidence["plugin_commit"]
            and set(cases[case_id]["skills"]).issubset(run["activated_skills"])
            and bool(run["invariants"])
            and all(run["invariants"].values())
            and (ROOT / run["evidence_path"]).is_file()
            and (
                any(tool.startswith("mcp__droit-francais__") for tool in run["mcp_tools"])
                if cases[case_id]["mcp_mode"] == "required"
                else run["mcp_status"] == "disabled" and not run["mcp_tools"]
            )
            for case_id, run in runs.items()
        )
        qualified_commit = (
            isinstance(evidence["plugin_commit"], str)
            and len(evidence["plugin_commit"]) == 40
            and all(char in "0123456789abcdef" for char in evidence["plugin_commit"])
        )
        self.assertEqual(
            evidence["release_ready"],
            qualified_runs and qualified_commit
            and evidence["review"]["human_legal_validation"] is True
            and evidence["codex_smoke"]["status"] == "passed"
            and evidence["codex_smoke"]["plugin_commit"] == evidence["plugin_commit"],
        )

    def test_marketplace_distribue_la_racine_sans_copie(self) -> None:
        marketplace = load_json(".agents/plugins/marketplace.json")
        plugin = load_json(".codex-plugin/plugin.json")
        published = load_json(".claude-plugin/marketplace.json")["plugins"][0]["version"]
        self.assertEqual(marketplace["name"], plugin["name"])
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], plugin["name"])
        # Codex suit la même étiquette publiée que Claude, jamais main.
        self.assertEqual(
            entry["source"],
            {"source": "url", "url": plugin["repository"] + ".git", "ref": f"v{published}"},
        )
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(entry["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(entry["category"], plugin["interface"]["category"])


@unittest.skipIf(
    os.environ.get("CT_SAUTER_BARRIERE") == "1",
    "Barrière de publication contrôlée par le job « Qualification de publication »",
)
class ReleaseGateTests(unittest.TestCase):
    """Verrou de publication distinct des contrôles d'intégration candidate.

    Le job « Intégration candidate » lance toute la découverte avec
    CT_SAUTER_BARRIERE=1 : toute nouvelle classe de tests y est donc exécutée
    sans liste à tenir à jour. Seule cette classe y est sautée.
    """

    def test_barriere_de_release_comportementale(self) -> None:
        manifest = load_json(".codex-plugin/plugin.json")
        evidence = load_json(f"tests/evidence/release-{manifest['version']}.json")
        self.assertTrue(
            evidence["release_ready"],
            "Release bloquée : " + " | ".join(evidence["release_blockers"]),
        )


if __name__ == "__main__":
    unittest.main()
