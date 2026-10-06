"""Contrats de campagne v2 : mutations synthétiques, sans SDK ni réseau."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import coactivation_assessment as assessment
import run_coactivation_v2 as campaign


STAMP = "2026-10-06T14:00:00Z"
TRACE_SHA = "a" * 64
TOOL = "mcp__droit-francais__get_article"
ARTICLE_ID = "LEGIART000000000001"
ARTICLE_URL = f"https://www.legifrance.gouv.fr/codes/article_lc/{ARTICLE_ID}"
ALL_SKILLS = (
    "dirfi-fpt", "drh-fpt", "dpm-fpt", "dpo-ct", "recherche-juridique", "dsi-fpt",
)
CASES = json.loads((ROOT / "tests/cas-coactivation-v2.json").read_text(encoding="utf-8"))
BY_ID = {case["id"]: case for case in CASES}


def fictitious_article() -> dict[str, Any]:
    """Aucune disposition réelle : le contenu sert uniquement de pièce de test."""
    return {
        "id": ARTICLE_ID,
        "url": ARTICLE_URL,
        "title": "Article synthétique de test",
        "text": "Disposition fictive destinée au contrôle documentaire du harnais.",
        "metadata": {"applicable_at_as_of_date": True, "as_of_date": "2026-10-06"},
    }


def message(*blocks: dict[str, Any], kind: str = "assistant") -> dict[str, Any]:
    """Construit un message avec un ordre de blocs observable."""
    return {"type": kind, "message": {"content": list(blocks)}}


def call(name: str, identifier: str, **inputs: Any) -> dict[str, Any]:
    """Construit un appel réel dans le flux synthétique."""
    return {"type": "tool_use", "name": name, "id": identifier, "input": inputs}


def result(identifier: str, content: Any = "Effectué", **fields: Any) -> dict[str, Any]:
    """Construit un résultat lié explicitement à son appel."""
    return {"type": "tool_result", "tool_use_id": identifier, "content": content, **fields}


def raw_trace(
    case: dict[str, Any], *, order: list[str] | None = None,
    source: str = "primary", text: str = "Réponse synthétique réservant les décisions métier.",
) -> list[dict[str, Any]]:
    """Session complète : six skills, activations/lectures acquittées, résultat final."""
    events = [{
        "type": "system", "subtype": "init", "model": "claude-sonnet-4-6",
        "skills": [f"collectivite-territoriale:{name}" for name in ALL_SKILLS],
        "mcp_servers": ([{"name": "droit-francais", "status": "connected"}]
                        if case["mcp_mode"] == "required" else []),
    }]
    for index, name in enumerate(order or case["activation_sequence"]):
        skill_id, read_id = f"toolu_skill_{index}", f"toolu_read_{index}"
        events.extend([
            message(call("Skill", skill_id, skill=f"collectivite-territoriale:{name}")),
            message(result(skill_id), kind="user"),
            message(call("Read", read_id, file_path=str(ROOT / "skills" / name / "SKILL.md"))),
            message(result(read_id, "Instructions synthétiques lues."), kind="user"),
        ])
    if case["mcp_mode"] == "required":
        article = fictitious_article()
        content: Any = json.dumps(article, ensure_ascii=False)
        flags: dict[str, Any] = {}
        name = TOOL
        if source == "empty":
            content = ""
        elif source == "failed":
            flags["is_error"] = True
        elif source == "search":
            name = "mcp__droit-francais__search_articles"
            content = json.dumps({"results": [article]}, ensure_ascii=False)
        elif source == "truncated":
            article["text"] = "Disposition synthétique. " * 1000
            content = json.dumps(article, ensure_ascii=False)
        events.extend([
            message(call(name, "toolu_source_1", id=ARTICLE_ID)),
            message(result("toolu_source_1", content, **flags), kind="user"),
        ])
    if case["web_mode"] == "official_source":
        events.extend([
            message(call("WebFetch", "toolu_web_1", url=ARTICLE_URL, prompt="Lire la source")),
            message(result("toolu_web_1", "Résumé synthétique fourni par WebFetch."), kind="user"),
        ])
    events.extend([
        message({"type": "text", "text": text}),
        {"type": "result", "subtype": "success", "is_error": False, "result": text},
    ])
    return events


def trace(case: dict[str, Any], **fields: Any) -> list[dict[str, Any]]:
    """Assainit une session synthétique et ajoute le bilan du processus."""
    events = campaign.sanitize(raw_trace(case, **fields), case, captured_at=STAMP)
    refresh_assessment(case, events)
    return events


def refresh_assessment(case: dict[str, Any], events: list[dict[str, Any]]) -> None:
    """Recalcule un bilan après mutation pour distinguer fraude et échec explicite."""
    events[:] = [event for event in events if event["type"] != "technical_assessment"]
    failures = campaign.technical_failures(events, case)
    events.append({
        "type": "technical_assessment", "case_id": case["id"], "process_exit": 0,
        "status": "failed" if failures else "passed", "failures": failures,
        "observables": campaign.observable_checks(events, case),
        "requires_independent_judgment": True,
    })


def judgment(case: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    """Avis fictif du juge : son fond métier n'est pas inféré par les tests."""
    text_ref = next(event["event_id"] for event in events if event["type"] == "assistant_text")
    primary_ref = next((event["event_id"] for event in events
                        if event["type"] == "source_evidence"), text_ref)
    return {
        "case_id": case["id"], "trace_sha256": TRACE_SHA, "verdict": "reussite",
        "invariants": {
            item["id"]: {
                "status": True,
                "basis": "retrieval" if item["category"] == "preuve_source" else "observation",
                "evidence_refs": [primary_ref if item["category"] == "preuve_source" else text_ref],
                "rationale": "Appréciation synthétique du juge indépendant pour ce contrat.",
            } for item in case["invariant_objects"]
        },
    }


class SuiteContractTests(unittest.TestCase):
    def test_gel_r3_sans_mesure_v2_refuse_meme_si_ses_empreintes_sont_valides(self) -> None:
        frozen = json.loads((ROOT / "tests/evidence/qualification-dsi/gel-r3.json").read_text(encoding="utf-8"))
        self.assertNotIn("tests/cas-coactivation-v2.json", frozen["files"])
        self.assertNotIn("scripts/run_coactivation_v2.py", frozen["files"])
        # L'oracle r3 est accepté ici : le rejet doit porter sur la couverture
        # de mesure v2, indépendamment de la dérive du candidat historique.
        with patch.object(campaign.legacy, "frozen_failures", return_value=[]):
            failures = campaign.frozen_failures_v2(frozen)
        self.assertTrue(failures, "Un gel r3 ne fige ni suite, ni harnais, ni juge v2.")
        # Changer seulement l'étiquette de schéma d'un gel r3 ne doit pas
        # permettre de masquer l'absence des empreintes de la mesure v2.
        frozen["schema_version"] = 2
        with patch.object(campaign.legacy, "frozen_failures", return_value=[]):
            failures = campaign.frozen_failures_v2(frozen)
        self.assertTrue(any("cas-coactivation-v2.json" in failure
                            or "run_coactivation_v2.py" in failure for failure in failures))

    def test_douze_questions_historiques_exactes_et_seize_cas(self) -> None:
        historical = json.loads((ROOT / "tests/cas-plugin.json").read_text(encoding="utf-8"))
        cases = campaign.load_cases()
        self.assertEqual(len(historical), 12)
        self.assertEqual(len(cases), 16)
        preserved = {case["id"]: case for case in cases if case["historical"]}
        self.assertEqual(set(preserved), {case["id"] for case in historical})
        for old in historical:
            with self.subTest(case=old["id"]):
                self.assertEqual(preserved[old["id"]]["prompt"], old["prompt"])
                self.assertEqual(preserved[old["id"]]["invariants"], old["invariants"])

    def test_identites_uniques_et_couverture_atomique_des_attentes_historiques(self) -> None:
        identifiers = [case["id"] for case in CASES]
        self.assertEqual(len(set(identifiers)), 16)
        atoms = [item["id"] for case in CASES for item in case["invariant_objects"]]
        self.assertEqual(len(set(atoms)), len(atoms))
        for case in CASES:
            with self.subTest(case=case["id"]):
                self.assertEqual({item["legacy_label"] for item in case["invariant_objects"]},
                                 set(case["invariants"]))
                self.assertTrue(all(item["id"].startswith(case["id"] + ".")
                                    and item["status"] is None and item["critical"] is True
                                    and item["expectation"] and item["observable"]
                                    for item in case["invariant_objects"]))
        retirement = BY_ID["plugin-prime-depart-retraite"]
        split = [item for item in retirement["invariant_objects"]
                 if item["legacy_label"] == "aucun CIA, RIFSEEP ou ISFE présumé avant qualification de l'agent"]
        self.assertEqual(len(split), 3, "Les trois régimes doivent recevoir chacun un jugement.")

    def test_chargeur_refuse_identites_et_modes_ambigus(self) -> None:
        mutations = []
        duplicate = copy.deepcopy(CASES)
        duplicate[-1]["id"] = duplicate[0]["id"]
        mutations.append(duplicate)
        for key, value in (("schema_version", 1), ("activation_mode", "aléatoire"),
                           ("mcp_mode", "auto"), ("source_evidence_policy", "supposée")):
            changed = copy.deepcopy(CASES)
            changed[0][key] = value
            mutations.append(changed)
        duplicate_atom = copy.deepcopy(CASES)
        duplicate_atom[0]["invariant_objects"].append(duplicate_atom[0]["invariant_objects"][0])
        mutations.append(duplicate_atom)
        with tempfile.TemporaryDirectory() as directory:
            suite = Path(directory) / "suite.json"
            for changed in mutations:
                with self.subTest(mutation=changed[0]["id"]):
                    suite.write_text(json.dumps(changed, ensure_ascii=False), encoding="utf-8")
                    with patch.object(campaign, "SUITE", suite), self.assertRaises(ValueError):
                        campaign.load_cases()

    def test_selection_spontanee_ne_revele_pas_oracle_au_repondant(self) -> None:
        for case in CASES:
            if case["activation_mode"] != "spontaneous":
                continue
            with self.subTest(case=case["id"]):
                prompt = campaign.build_prompt(case)
                self.assertTrue(prompt.endswith(case["prompt"]))
                self.assertEqual(campaign.build_command(case, "claude-synthetique")[-1], prompt)
                for name in ALL_SKILLS:
                    self.assertNotIn(name, prompt)
                self.assertNotIn("activation_sequence", prompt)
                self.assertNotIn(" puis ", prompt.partition(case["prompt"])[0])

    def test_deux_ordres_spontanes_valides_mais_controle_force_reste_ordonne(self) -> None:
        case = BY_ID["plugin-spontane-budget"]
        for order in (case["activation_sequence"], list(reversed(case["activation_sequence"]))):
            with self.subTest(order=order):
                events = trace(case, order=order)
                self.assertEqual(campaign.technical_failures(events, case), [])
        forced = BY_ID[case["paired_case_id"]]
        self.assertIn("activation_sequence_mismatch", campaign.technical_failures(
            trace(forced, order=list(reversed(forced["activation_sequence"]))), forced))

    def test_ensemble_spontane_strict_et_activations_reellement_reussies(self) -> None:
        case = BY_ID["plugin-spontane-budget"]
        for order in (case["skills"][:-1], case["skills"] + ["dpm-fpt"],
                      case["skills"] + [case["skills"][0]]):
            with self.subTest(order=order):
                self.assertIn("activation_set_mismatch", campaign.technical_failures(trace(case, order=order), case))
        events = trace(case)
        next(event for event in events if event["type"] == "skill_activation")["succeeded"] = False
        self.assertIn("skill_activation_not_successful", campaign.technical_failures(events, case))


class TraceContractTests(unittest.TestCase):
    def test_secrets_textes_visibles_et_resultats_absents_de_la_trace_persistable(self) -> None:
        case = BY_ID["plugin-garde-fou-apja"]
        text = (
            "STOP — opération réservée.\n"
            "Authorization: Bearer synthetic-private-harness001\n"
            "Contact : personne@example.test\n"
            "Texte public après masquage."
        )
        raw = raw_trace(case, text=text)
        raw[-1]["result"] = "token=synthetic-private-harness002\nRésultat public."
        events = campaign.sanitize(raw, case, captured_at=STAMP)
        persisted = "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events)
        self.assertNotIn("synthetic-private-harness", persisted)
        self.assertNotIn("personne@example.test", persisted)
        visible = next(event for event in events if event["type"] == "assistant_text")
        final = next(event for event in events if event["type"] == "result")
        self.assertTrue(visible["text"].startswith("STOP"))
        self.assertIn("Texte public après masquage.", visible["text"])
        self.assertIn("Résultat public.", final["result"])
        self.assertTrue(campaign.observable_checks(events, case)["stop_first"])
        self.assertIn("visible_text_redacted", campaign.technical_failures(events, case))

    def test_chemin_url_sensible_ne_fuit_pas_via_official_source_call(self) -> None:
        case = copy.deepcopy(BY_ID["plugin-dsi-budget"])
        case.update(web_mode="official_source", official_source_hosts=["www.cnil.fr"])
        sensitive_url = "https://www.cnil.fr/fr/token=synthetic-private-path"
        raw = raw_trace(case)
        raw.insert(-2, message(call("WebFetch", "toolu_sensitive_path", url=sensitive_url, prompt="Lire")))
        raw.insert(-2, message(result("toolu_sensitive_path", "Résumé public."), kind="user"))
        events = campaign.sanitize(raw, case, captured_at=STAMP)
        self.assertNotIn("synthetic-private-path", json.dumps(events, ensure_ascii=False))
        web_call = next(event for event in events if event.get("call_id") == "toolu_sensitive_path"
                        and event["type"] == "official_source_call")
        self.assertNotIn("source_path", web_call)
        evidence = next(event for event in events if event.get("call_id") == "toolu_sensitive_path"
                        and event["type"] == "source_evidence")
        self.assertEqual(evidence["status"], "missing")
        self.assertEqual(evidence["documents"], [])

    def test_erreurs_brutes_non_persistees_mais_compteur_diagnostic_preserve(self) -> None:
        case = BY_ID["plugin-dsi-budget"]
        raw = raw_trace(case)
        raw[-1].update(
            subtype="error_during_execution", is_error=True,
            errors=["Authorization: Bearer synthetic-private-error001",
                    {"debug": "token=synthetic-private-error002"}],
        )
        events = campaign.sanitize(raw, case, captured_at=STAMP)
        final = next(event for event in events if event["type"] == "result")
        self.assertNotIn("errors", final)
        self.assertEqual(final["errors_count"], 2)
        self.assertNotIn("synthetic-private-error", json.dumps(events))
        self.assertIn("result_error_or_absent", campaign.technical_failures(events, case))

    def test_assainissement_preserve_stop_textes_ordinaires_et_ordre_visible(self) -> None:
        case = BY_ID["plugin-garde-fou-apja"]
        ordinary = "**STOP APJA** — opération réservée.\nLa signature du maire demeure requise."
        continuation = f"Lire [source synthétique]({ARTICLE_URL}) avant toute conclusion."
        raw = raw_trace(case, text=continuation)
        raw.insert(1, message(
            {"type": "text", "text": ordinary},
            call("Read", "toolu_scrub_order", file_path=str(ROOT / "skills/dpm-fpt/SKILL.md")),
            {"type": "text", "text": "Texte public après appel."},
        ))
        raw.insert(2, message(result("toolu_scrub_order"), kind="user"))
        events = campaign.sanitize(raw, case, captured_at=STAMP)
        self.assertEqual([event["type"] for event in events[1:4]],
                         ["assistant_text", "plugin_file_read", "assistant_text"])
        self.assertEqual([event["text"] for event in events if event["type"] == "assistant_text"],
                         [ordinary, "Texte public après appel.", continuation])
        self.assertEqual(next(event for event in events if event["type"] == "result")["result"], continuation)
        self.assertTrue(campaign.observable_checks(events, case)["stop_first"])

    def test_fixture_transport_complet_et_disponibilite_sans_validite_juridique(self) -> None:
        case = BY_ID["plugin-dsi-budget"]
        events = trace(case)
        self.assertEqual(campaign.technical_failures(events, case), [])
        observable = campaign.observable_checks(events, case)
        self.assertTrue(observable["primary_content_available"])
        self.assertIsNone(observable["legal_validity"])
        source = next(event for event in events if event["type"] == "source_evidence")
        self.assertEqual(source["call_id"], "toolu_source_1")
        self.assertEqual(source["documents"][0]["excerpt"], fictitious_article()["text"])
        self.assertEqual(source["content_trust"], "untrusted_source_data")

    def test_init_model_mcp_et_lectures_conformes_sont_requis(self) -> None:
        case = BY_ID["plugin-dsi-budget"]
        for target, field, value, expected in (
            ("init", "model", "autre-modele", "model_mismatch"),
            ("init", "available_skills", [], "available_skills_mismatch"),
            ("init", "mcp_servers", [], "mcp_not_connected"),
            ("plugin_file_read", "succeeded", False, "plugin_read_not_successful"),
        ):
            with self.subTest(expected=expected):
                events = trace(case)
                next(event for event in events if event["type"] == target)[field] = value
                self.assertIn(expected, campaign.technical_failures(events, case))

    def test_ordre_blocs_textes_outils_et_stop_premier_texte_visible(self) -> None:
        case = BY_ID["plugin-garde-fou-apja"]
        for before, expected in (("STOP — opération réservée.", True),
                                 ("Je consulte d'abord le cadre.", False)):
            with self.subTest(before=before):
                raw = raw_trace(case, text="STOP — ne pas poursuivre.")
                raw.insert(1, message(
                    {"type": "text", "text": before},
                    call("Read", "toolu_visible_read", file_path=str(ROOT / "skills/dpm-fpt/SKILL.md")),
                    {"type": "text", "text": "Texte après appel."},
                ))
                raw.insert(2, message(result("toolu_visible_read"), kind="user"))
                events = campaign.sanitize(raw, case, captured_at=STAMP)
                self.assertEqual([event["type"] for event in events[1:4]],
                                 ["assistant_text", "plugin_file_read", "assistant_text"])
                self.assertEqual(campaign.observable_checks(events, case)["stop_first"], expected)

    def test_resultats_inconnus_et_dupliques_ne_deviennent_pas_preuves(self) -> None:
        case = BY_ID["plugin-dsi-budget"]
        for identifier in ("toolu_inconnu", "toolu_source_1"):
            with self.subTest(identifier=identifier):
                raw = raw_trace(case)
                raw.insert(-2, message(result(identifier, json.dumps(fictitious_article())), kind="user"))
                events = campaign.sanitize(raw, case, captured_at=STAMP)
                self.assertIn("unexpected_tool_call", campaign.technical_failures(events, case))
                self.assertEqual(sum(event["type"] == "source_evidence" for event in events), 1)

    def test_callid_duplique_et_activation_sans_resultat_refuses(self) -> None:
        case = BY_ID["plugin-dsi-budget"]
        raw = raw_trace(case)
        raw.insert(-2, message(call(TOOL, "toolu_source_1", id=ARTICLE_ID)))
        events = campaign.sanitize(raw, case, captured_at=STAMP)
        self.assertIn("unexpected_tool_call", campaign.technical_failures(events, case))
        raw = raw_trace(case)
        raw.pop(2)
        events = campaign.sanitize(raw, case, captured_at=STAMP)
        self.assertIn("skill_activation_not_successful", campaign.technical_failures(events, case))

    def test_transport_reussi_empty_search_ne_prouvent_pas_texte_primaire(self) -> None:
        case = BY_ID["plugin-dsi-budget"]
        for source in ("empty", "search", "truncated"):
            with self.subTest(source=source):
                events = trace(case, source=source)
                self.assertEqual(campaign.technical_failures(events, case), [])
                self.assertFalse(campaign.observable_checks(events, case)["primary_content_available"])
        self.assertIn("plugin_mcp_call_missing", campaign.technical_failures(trace(case, source="failed"), case))

    def test_webfetch_resume_reste_resume(self) -> None:
        case = copy.deepcopy(BY_ID["plugin-dsi-budget"])
        case.update(web_mode="official_source", official_source_hosts=["www.legifrance.gouv.fr"])
        events = trace(case, source="empty")
        self.assertEqual(campaign.technical_failures(events, case), [])
        web_source = next(event for event in events if event["type"] == "source_evidence" and event["tool"] == "WebFetch")
        self.assertEqual(web_source["documents"][0]["nature"], "tool_summary")
        self.assertFalse(campaign.observable_checks(events, case)["primary_content_available"])


class JudgeContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.case = BY_ID["plugin-dsi-budget"]
        self.events = trace(self.case)
        self.judge = judgment(self.case, self.events)

    def validate(self, judge: dict[str, Any] | None = None) -> dict[str, Any]:
        """Valide le contrat sans exécuter de juge externe."""
        return assessment.validate_judgment(self.case, self.events, judge or self.judge, TRACE_SHA)

    def test_schema_atomique_et_succes_ne_qualifie_pas_release(self) -> None:
        for value in self.judge["invariants"].values():
            self.assertEqual(set(value), {"status", "basis", "evidence_refs", "rationale"})
        accepted = self.validate()
        self.assertEqual(accepted["verdict"], "reussite")
        self.assertEqual(accepted["behavior_status"], "passed")
        self.assertEqual(accepted["documentary_status"], "passed")
        self.assertFalse(accepted["release_ready"])

    def test_texte_visible_tronque_interdit_reussite_meme_si_fin_contradictoire_masquee(self) -> None:
        for target in ("assistant_text", "result"):
            with self.subTest(target=target):
                raw = raw_trace(self.case)
                long_text = ("Analyse synthétique réservant la décision métier.\n" * 2000
                             + "Conclusion contradictoire : engager sans aucune vérification.")
                if target == "assistant_text":
                    raw[-2]["message"]["content"][0]["text"] = long_text
                else:
                    raw[-1]["result"] = long_text
                events = campaign.sanitize(raw, self.case, captured_at=STAMP)
                visible = next(event for event in events if event["type"] == target)
                self.assertTrue(visible["text_truncated"])
                self.assertNotIn("Conclusion contradictoire", visible.get("text", visible.get("result", "")))
                self.assertIn("visible_text_truncated", campaign.technical_failures(events, self.case))
                refresh_assessment(self.case, events)
                judge = judgment(self.case, events)
                with self.assertRaises(ValueError):
                    assessment.validate_judgment(self.case, events, judge, TRACE_SHA)
                # Une retouche du bilan local ne peut faire disparaître le
                # signal de troncature que le juge recalcule depuis les pièces.
                events[-1].update(status="passed", failures=[])
                with self.assertRaises(ValueError):
                    assessment.validate_judgment(self.case, events, judge, TRACE_SHA)

    def test_oracle_transmis_au_juge_et_hash_des_octets_de_la_trace(self) -> None:
        case = BY_ID["plugin-spontane-budget"]
        events = trace(case)
        with tempfile.TemporaryDirectory() as directory:
            trace_file, protocol = Path(directory) / "trace.jsonl", Path(directory) / "protocole.md"
            trace_file.write_text("".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events), encoding="utf-8", newline="\n")
            protocol.write_text("Rubrique synthétique du juge indépendant.", encoding="utf-8")
            packet = assessment.build_judge_packet(case, trace_file, protocol)
            self.assertEqual(packet["trace_sha256"], hashlib.sha256(trace_file.read_bytes()).hexdigest())
            self.assertEqual(packet["question"], case["prompt"])
            self.assertEqual(packet["invariant_objects"], case["invariant_objects"])
            self.assertEqual(packet.get("skills"), case["skills"], "Le juge doit connaître l'ensemble attendu que le répondant ignore.")
            self.assertEqual(packet.get("activation_sequence"), case["activation_sequence"])

    def test_statut_un_chaine_et_objet_ne_sont_pas_booleens(self) -> None:
        key = next(iter(self.judge["invariants"]))
        for value in (1, 0, "true", [], {}):
            with self.subTest(value=value):
                judge = copy.deepcopy(self.judge)
                judge["invariants"][key]["status"] = value
                with self.assertRaises(ValueError):
                    self.validate(judge)

    def test_quatre_champs_exacts_cles_invariants_et_references_reelles(self) -> None:
        key = next(iter(self.judge["invariants"]))
        for mutation in ("extra_field", "missing_field", "missing_atom", "foreign_atom", "foreign_ref", "no_refs", "empty_reason", "false_basis"):
            with self.subTest(mutation=mutation):
                judge = copy.deepcopy(self.judge)
                atom = judge["invariants"][key]
                if mutation == "extra_field":
                    atom["score"] = 1
                elif mutation == "missing_field":
                    del atom["basis"]
                elif mutation == "missing_atom":
                    del judge["invariants"][key]
                elif mutation == "foreign_atom":
                    judge["invariants"]["autre.invariant"] = atom
                elif mutation == "foreign_ref":
                    atom["evidence_refs"] = ["e-invente"]
                elif mutation == "no_refs":
                    atom["evidence_refs"] = []
                elif mutation == "empty_reason":
                    atom["rationale"] = "  "
                else:
                    atom["basis"] = "affirmation"
                with self.assertRaises(ValueError):
                    self.validate(judge)

    def test_autre_case_ou_sha_ne_peuvent_heriter_du_succes(self) -> None:
        for key, value in (("case_id", "plugin-dsi-rssi-rh"), ("trace_sha256", "b" * 64)):
            with self.subTest(key=key):
                judge = copy.deepcopy(self.judge)
                judge[key] = value
                with self.assertRaises(ValueError):
                    self.validate(judge)

    def test_commentaire_avant_stop_interdit_succes_malgre_juge(self) -> None:
        case = BY_ID["plugin-garde-fou-apja"]
        raw = raw_trace(case, text="STOP — opération réservée.")
        raw.insert(1, message({"type": "text", "text": "Je vérifie d'abord le dossier."}))
        events = campaign.sanitize(raw, case, captured_at=STAMP)
        refresh_assessment(case, events)
        self.assertEqual(campaign.technical_failures(events, case), [])
        with self.assertRaisesRegex(ValueError, "STOP"):
            assessment.validate_judgment(case, events, judgment(case, events), TRACE_SHA)

    def test_resume_search_empty_tronque_ne_peuvent_valoir_primaire(self) -> None:
        for source in ("empty", "search", "truncated"):
            with self.subTest(source=source):
                events = trace(self.case, source=source)
                with self.assertRaises(ValueError):
                    assessment.validate_judgment(self.case, events, judgment(self.case, events), TRACE_SHA)
        events = copy.deepcopy(self.events)
        next(event for event in events if event["type"] == "source_evidence")["documents"][0]["nature"] = "tool_summary"
        refresh_assessment(self.case, events)
        with self.assertRaises(ValueError):
            assessment.validate_judgment(self.case, events, self.judge, TRACE_SHA)

    def test_preuve_sans_callid_anterieur_ou_appel_echoue_refusee(self) -> None:
        for mutation in ("unknown", "before_call", "failed"):
            with self.subTest(mutation=mutation):
                events = copy.deepcopy(self.events)
                source = next(event for event in events if event["type"] == "source_evidence")
                source_call = next(event for event in events if event["type"] == "plugin_mcp_call")
                if mutation == "unknown":
                    source["call_id"] = "toolu_invente"
                elif mutation == "before_call":
                    events.remove(source)
                    events.insert(0, source)
                else:
                    source_call["succeeded"] = False
                refresh_assessment(self.case, events)
                judge = copy.deepcopy(self.judge)
                if mutation == "failed":
                    judge["verdict"] = "echec"
                with self.assertRaises(ValueError):
                    assessment.validate_judgment(self.case, events, judge, TRACE_SHA)

    def test_cache_observable_forge_et_passed_sans_init_refuses(self) -> None:
        for mutation in ("primary", "stop", "init", "process"):
            with self.subTest(mutation=mutation):
                self.events = trace(self.case)
                control = self.events[-1]
                if mutation == "primary":
                    control["observables"]["primary_content_available"] = False
                elif mutation == "stop":
                    control["observables"]["stop_first"] = True
                elif mutation == "init":
                    self.events[:] = [event for event in self.events if event["type"] != "init"]
                else:
                    control["process_exit"] = 1
                with self.assertRaises(ValueError):
                    self.validate()

    def test_assessment_absent_duplique_et_eventid_ambigu_refuses(self) -> None:
        original = copy.deepcopy(self.events)
        for mutation in ("absent", "duplicate", "event_id"):
            with self.subTest(mutation=mutation):
                self.events = copy.deepcopy(original)
                if mutation == "absent":
                    self.events.pop()
                elif mutation == "duplicate":
                    self.events.append(copy.deepcopy(self.events[-1]))
                else:
                    self.events[1]["event_id"] = self.events[0]["event_id"]
                with self.assertRaises(ValueError):
                    self.validate()

    def test_source_inapplicable_ne_peut_etre_validee(self) -> None:
        source = next(event for event in self.events if event["type"] == "source_evidence")
        source["documents"][0]["metadata"]["applicable_at_as_of_date"] = False
        refresh_assessment(self.case, self.events)
        with self.assertRaisesRegex(ValueError, "non applicable"):
            self.validate()

    def test_verdict_agrege_separe_echec_metier_incomplet_et_transport(self) -> None:
        behavior = next(item["id"] for item in self.case["invariant_objects"] if item["category"] == "comportement")
        source = next(item["id"] for item in self.case["invariant_objects"] if item["category"] == "preuve_source")
        for key, status, verdict, category, category_status in (
            (behavior, False, "echec", "behavior_status", "failed"),
            (source, False, "echec", "documentary_status", "failed"),
            (behavior, None, "bloque", "behavior_status", "incomplete"),
            (source, None, "bloque", "documentary_status", "incomplete"),
        ):
            with self.subTest(key=key, status=status):
                judge = copy.deepcopy(self.judge)
                judge["invariants"][key]["status"] = status
                with self.assertRaises(ValueError):
                    self.validate(judge)
                judge["verdict"] = verdict
                accepted = self.validate(judge)
                self.assertEqual(accepted["verdict"], verdict)
                self.assertEqual(accepted[category], category_status)
                self.assertEqual(accepted["technical_status"], "passed")
        self.events[-1].update(status="failed", process_exit=1, failures=["process_exit_nonzero"])
        self.judge["verdict"] = "echec"
        accepted = self.validate()
        self.assertEqual(accepted["behavior_status"], "passed")
        self.assertEqual(accepted["technical_status"], "failed")

    def test_abstention_admise_ne_masque_pas_primaire_absent_en_nominal(self) -> None:
        self.events = trace(self.case, source="empty")
        judge = judgment(self.case, self.events)
        text_ref = next(event["event_id"] for event in self.events if event["type"] == "assistant_text")
        for item in self.case["invariant_objects"]:
            if item["category"] == "preuve_source":
                judge["invariants"][item["id"]].update(basis="abstention", evidence_refs=[text_ref])
        with self.assertRaises(ValueError):
            self.validate(judge)
        judge["verdict"] = "bloque"
        accepted = self.validate(judge)
        self.assertEqual(accepted["documentary_status"], "passed")
        self.assertFalse(accepted["primary_content_available"])
        self.assertEqual(accepted["verdict"], "bloque")

    def test_cas_purement_technique_ne_demande_pas_de_preuve_juridique(self) -> None:
        case = BY_ID["plugin-dsi-technique"]
        events = trace(case)
        self.assertEqual(campaign.technical_failures(events, case), [])
        accepted = assessment.validate_judgment(case, events, judgment(case, events), TRACE_SHA)
        self.assertEqual(accepted["verdict"], "reussite")
        self.assertEqual(accepted["documentary_status"], "not_required")
        self.assertFalse(accepted["primary_content_available"])
        self.assertFalse(accepted["release_ready"])


if __name__ == "__main__":
    unittest.main()
