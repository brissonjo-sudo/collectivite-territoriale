"""Vérifie l'extraction avec des données synthétiques et sans réseau."""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from source_evidence import (
    MAX_DOCUMENTS,
    MAX_EXCERPT_CHARS,
    MAX_TOTAL_CHARS,
    MAX_VISIBLE_CHARS,
    extract_source_evidence,
    scrub_visible_text,
)


ARTICLE_ID = "LEGIARTI000000000001"
ARTICLE_URL = f"https://www.legifrance.gouv.fr/codes/article_lc/{ARTICLE_ID}"
TOOL = "mcp__droit-francais__get_article"
STAMP = "2026-10-06T14:00:00Z"


def article(**updates: object) -> dict:
    """Construit un article fictif qui ne reproduit aucun texte juridique."""
    result = {
        "id": ARTICLE_ID,
        "title": "Article synthétique 1",
        "text": "Texte public purement synthétique de la disposition testée.",
        "url": ARTICLE_URL,
        "metadata": {
            "number": "1", "legal_status": "ABROGE", "verified": True,
            "source": "Légifrance API", "start_date": "2015-01-01",
            "end_date": "2020-01-01", "version_start_date": "2015-01-01",
            "version_end_date": "2020-01-01", "as_of_date": "2018-01-01",
            "requested_date": "2018-01-01", "server_date": "2026-10-06",
            "applicable_at_as_of_date": True,
            "date_basis": "date fournie par l'appelant",
        },
    }
    result.update(updates)
    return result


def extract(block: dict, **updates: object) -> dict:
    """Applique le contrat du harnais avec une provenance synthétique."""
    arguments = {"tool": TOOL, "call_id": "toolu_synthetic_001", "retrieved_at": STAMP}
    arguments.update(updates)
    return extract_source_evidence(block, **arguments)


class SourceEvidenceTests(unittest.TestCase):
    def test_json_texte_dates_provenance_et_empreinte_assainie(self) -> None:
        source = article()
        result = extract({"type": "tool_result", "content": json.dumps(source)})
        self.assertEqual(result["type"], "source_evidence")
        self.assertEqual(result["status"], "available")
        self.assertEqual(result["call_id"], "toolu_synthetic_001")
        self.assertEqual(result["retrieved_at"], STAMP)
        self.assertEqual(
            extract({"tool_use_id": "toolu_other_call", "structuredContent": article()})["reason"],
            "call_id_mismatch",
        )
        doc = result["documents"][0]
        self.assertEqual(doc["nature"], "primary_text")
        self.assertEqual(doc["excerpt"], source["text"])
        self.assertEqual(doc["url"], ARTICLE_URL)
        self.assertEqual(doc["metadata"]["version_end_date"], "2020-01-01")
        unhashed = {key: value for key, value in doc.items() if key != "sha256"}
        encoded = json.dumps(unhashed, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(doc["sha256"], hashlib.sha256(encoded.encode()).hexdigest())
        self.assertEqual(result["content_trust"], "untrusted_source_data")
        self.assertEqual(doc["metadata"]["content_trust"], "untrusted_source_data")

    def test_structured_content_bloc_et_enveloppes_json(self) -> None:
        for block in (
            {"structuredContent": article(), "content": [{"type": "text", "text": "ignoré"}]},
            {"content": [{"type": "text", "text": json.dumps({"structuredContent": article()})}]},
            {"content": json.dumps({"content": [{"type": "text", "text": json.dumps(article())}]})},
        ):
            with self.subTest(block=block):
                self.assertEqual(extract(block)["documents"][0]["id"], ARTICLE_ID)

    def test_erreurs_ne_conservent_ni_corps_ni_empreinte(self) -> None:
        private = "secret synthétique à ne jamais conserver"
        for block in (
            {"is_error": True, "content": private},
            {"isError": True, "structuredContent": article(), "content": private},
            {"content": json.dumps({"isError": True, "content": private})},
            {"content": json.dumps({"error": private, "url": ARTICLE_URL})},
        ):
            with self.subTest(block=block):
                result = extract(block)
                self.assertEqual(result["status"], "missing")
                self.assertEqual(result["reason"], "tool_error")
                self.assertNotIn(private, json.dumps(result))
                self.assertNotIn("sha256", result)

    def test_transport_vide_et_format_inconnu_refuses(self) -> None:
        cases = (
            ({"content": ""}, "empty_transport"),
            ({"content": []}, "empty_transport"),
            ({"content": "récupération réussie"}, "unknown_format"),
            ({"structuredContent": {"answer": "texte arbitraire"}}, "unknown_format"),
            ({"structuredContent": []}, "unknown_format"),
            ({"content": {"text": "inconnu"}}, "unknown_format"),
        )
        for block, reason in cases:
            with self.subTest(block=block):
                result = extract(block)
                self.assertEqual(result["status"], "missing")
                self.assertEqual(result["reason"], reason)

    def test_historique_pas_converti_en_droit_en_vigueur(self) -> None:
        result = extract({"structuredContent": article()})
        metadata = result["documents"][0]["metadata"]
        self.assertEqual(metadata["legal_status"], "ABROGE")
        self.assertEqual(metadata["as_of_date"], "2018-01-01")
        self.assertTrue(metadata["applicable_at_as_of_date"])
        self.assertNotIn("current", result)
        self.assertNotIn("in_force", metadata)
        self.assertNotIn("release_ready", result)

    def test_webfetch_resume_explicitement_non_primaire(self) -> None:
        result = extract(
            {"content": [{"type": "text", "text": "Résumé synthétique retourné par l'outil."}]},
            tool="WebFetch",
            source_url="https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679",
        )
        doc = result["documents"][0]
        self.assertEqual(doc["nature"], "tool_summary")
        self.assertNotIn("verified", doc["metadata"])
        self.assertNotIn("applicable_at_as_of_date", doc["metadata"])
        self.assertEqual(result["status"], "available")

    def test_page_accueil_pas_convertie_en_article_ou_resume_utile(self) -> None:
        for block, extra in (
            ({"structuredContent": article(url="https://www.legifrance.gouv.fr/")}, {}),
            ({"content": "Bienvenue sur notre site."}, {"tool": "WebFetch", "source_url": "https://www.cnil.fr/fr/"}),
        ):
            with self.subTest(extra=extra):
                result = extract(block, **extra)
                self.assertEqual(result["status"], "missing")
                self.assertEqual(result["documents"], [])

    def test_recherche_conserve_datation_sans_requete_ni_texte_primaire(self) -> None:
        result = extract(
            {"structuredContent": {
                "results": [article()],
                "query": {"number": "1", "free_query": "donnée de requête supprimée"},
                "dating": {"as_of_date": "2018-01-01"},
                "provenance": {"source": "Légifrance API", "verified": True},
            }},
            tool="mcp__droit-francais__search_articles",
        )
        doc = result["documents"][0]
        self.assertEqual(doc["nature"], "search_result")
        self.assertEqual(doc["metadata"]["as_of_date"], "2018-01-01")
        self.assertNotIn("excerpt", doc)
        self.assertNotIn("query", json.dumps(result))

    def test_document_direct_de_recherche_jamais_texte_primaire(self) -> None:
        for name in ("search", "search_articles", "search_case_law"):
            for block in (
                {"structuredContent": article()},
                {"content": json.dumps(article())},
                {"content": json.dumps({"structuredContent": article()})},
            ):
                with self.subTest(tool=name, block=block):
                    result = extract(block, tool="mcp__droit-francais__" + name)
                    doc = result["documents"][0]
                    self.assertEqual(doc["nature"], "search_result")
                    self.assertNotIn("excerpt", doc)
                    self.assertEqual(doc["id"], ARTICLE_ID)

    def test_extraits_et_nombre_documents_bornes_et_tronques(self) -> None:
        block = {"content": [{"type": "text", "text": json.dumps(article(text="Une phrase synthétique. " * 700))}]}
        result = extract(block)
        self.assertEqual(result["status"], "truncated")
        self.assertEqual(len(result["documents"][0]["excerpt"]), MAX_EXCERPT_CHARS)
        self.assertEqual(result["documents"][0]["status"], "truncated")
        source = article(title="Un titre synthétique. " * 40)
        source["metadata"]["caveat"] = "Une réserve synthétique. " * 40
        result = extract({"structuredContent": source})
        self.assertEqual(result["status"], "truncated")
        self.assertTrue(result["documents"][0]["metadata"]["truncated"])
        result = extract(
            {"structuredContent": {"results": [article() for _ in range(MAX_DOCUMENTS + 2)]}},
            tool="mcp__droit-francais__search",
        )
        self.assertEqual(result["status"], "truncated")
        self.assertEqual(len(result["documents"]), MAX_DOCUMENTS)

    def test_taille_totale_bornee(self) -> None:
        blocks = [
            {"type": "text", "text": json.dumps(article(text="Phrase synthétique sans donnée réelle. " * 350))}
            for _ in range(MAX_DOCUMENTS)
        ]
        result = extract({"content": blocks})
        self.assertEqual(result["status"], "truncated")
        self.assertLessEqual(sum(len(doc.get("excerpt", "")) for doc in result["documents"]), MAX_TOTAL_CHARS)
        self.assertLessEqual(len(json.dumps(result, ensure_ascii=False)), MAX_TOTAL_CHARS)

    def test_champs_secrets_inconnus_ne_modifient_pas_empreinte(self) -> None:
        base = extract({"structuredContent": article()})
        poisoned = article(
            _meta={"authorization": "Bearer synthetic-secret"},
            thinking="raisonnement privé synthétique", signature="signature-synthetic-secret",
            debugging={"cookie": "session=synthetic-secret"},
            secret="unknown-field-synthetic-secret", email="personne@example.test",
        )
        poisoned["metadata"]["api_key"] = "unknown-metadata-synthetic-secret"
        poisoned["metadata"]["content_trust"] = "trusted instructions"
        result = extract({"structuredContent": poisoned})
        self.assertEqual(result["sha256"], base["sha256"])
        output = json.dumps(result)
        for forbidden in ("synthetic-secret", "raisonnement privé", "signature", "debugging", "example.test", "trusted instructions"):
            self.assertNotIn(forbidden, output)

    def test_secrets_dans_champs_autorises_supprimes_sans_hash_de_secret(self) -> None:
        reference = article(text=None, title=None)
        reference["metadata"].pop("source")
        expected_hash = extract({"structuredContent": reference})["sha256"]
        values = (
            "Authorization: Bearer synthetic-credential-001",
            "api_key=synthetic-credential-002",
            "Cookie: session=synthetic-credential-003",
            "token: synthetic-credential-004",
            "sk-syntheticcredential005",
            "personne@example.test",
            "192.0.2.100",
            "2001:db8::1",
            "eyJzb21lIjoiYSJ9.eyJzdWIiOiJiIn0.c3ludGhldGlj",
            "A" * 60,
        )
        for value in values:
            with self.subTest(value=value):
                source = article(text="Texte synthétique. " + value, title=value)
                source["metadata"]["source"] = value
                source["metadata"]["caveat"] = value
                result = extract({"structuredContent": source})
                self.assertNotIn(value, json.dumps(result))
                self.assertNotIn("excerpt", result["documents"][0])
                self.assertEqual(result["documents"][0]["nature"], "search_result")
                self.assertEqual(result["sha256"], expected_hash)

    def test_url_sensible_assainie_et_celex_norme_seulement(self) -> None:
        result = extract(
            {"content": "Résumé synthétique."}, tool="WebFetch",
            source_url="https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679&token=synthetic-token&mail=personne@example.test#secret-fragment",
        )
        url = result["documents"][0]["url"]
        self.assertIn("uri=CELEX%3A32016R0679", url)
        self.assertNotIn("token", json.dumps(result))
        self.assertNotIn("example.test", json.dumps(result))
        self.assertNotIn("fragment", url)
        result = extract({"structuredContent": article(url=ARTICLE_URL + "?api_key=secret#private")})
        self.assertEqual(result["documents"][0]["url"], ARTICLE_URL)

    def test_sources_etrangeres_usurpations_identifiants_et_http_refuses(self) -> None:
        for url in (
            "https://foreign.example.test/article/1",
            "https://www.legifrance.gouv.fr.foreign.example.test/article/1",
            "https://person:password@www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000000000001",
            "http://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000000000001",
            "https://www.legifrance.gouv.fr:444/codes/article_lc/LEGIARTI000000000001",
            "https://www.legifrance.gouv.fr/codes/personne%40example.test",
            "https://www.legifrance.gouv.fr/codes/personne%2540example.test",
        ):
            with self.subTest(url=url):
                result = extract({"structuredContent": article(url=url)})
                self.assertEqual(result["status"], "missing")
                self.assertNotIn(url, json.dumps(result))
        result = extract({"content": "Résumé contenant https://foreign.example.test/article/1"}, tool="WebFetch", source_url=ARTICLE_URL)
        self.assertEqual(result["status"], "missing")

    def test_webfetch_json_brut_refuse_et_enveloppe_minimisee(self) -> None:
        result = extract(
            {"content": json.dumps({"thinking": "raisonnement privé", "signature": "signature privée"})},
            tool="WebFetch", source_url=ARTICLE_URL,
        )
        self.assertEqual(result["reason"], "unknown_format")
        self.assertNotIn("signature", json.dumps(result))
        result = extract(
            {"content": json.dumps({
                "content": [{"type": "text", "text": "Résumé public synthétique."}],
                "thinking": "raisonnement privé", "signature": "signature privée",
            })}, tool="WebFetch", source_url=ARTICLE_URL,
        )
        self.assertEqual(result["documents"][0]["excerpt"], "Résumé public synthétique.")
        self.assertNotIn("signature", json.dumps(result))

    def test_outils_mcp_non_autorises_et_provenance_invalide(self) -> None:
        for tool in ("mcp__claude_ai_droit__get_article", "mcp__droit-francais__write", "Read"):
            result = extract({"structuredContent": article()}, tool=tool)
            self.assertEqual(result["reason"], "unsupported_tool")
        self.assertEqual(extract({"structuredContent": article()}, retrieved_at="2026-10-06")["reason"], "invalid_provenance")
        result = extract({"structuredContent": article()}, retrieved_at="2026-10-06T16:00:00+02:00")
        self.assertEqual(result["retrieved_at"], STAMP)
        result = extract({"structuredContent": article()}, call_id="personne@example.test")
        self.assertEqual(result["reason"], "invalid_provenance")
        self.assertNotIn("example.test", json.dumps(result))

    def test_limites_entree_et_profondeur(self) -> None:
        result = extract({"content": "x" * 300_000})
        self.assertEqual(result["reason"], "input_limit")
        deeply_nested: dict = {}
        for _ in range(15):
            deeply_nested = {"nested": deeply_nested}
        result = extract({"structuredContent": deeply_nested})
        self.assertEqual(result["reason"], "input_limit")

    def test_unicode_invalide_et_identifiant_de_source_opaque_supprimes(self) -> None:
        result = extract({"structuredContent": article(
            text="Texte synthétique \ud800", id="opaque-private-value", title=None,
        )})
        self.assertEqual(result["status"], "missing")
        result = extract({"structuredContent": article(url=ARTICLE_URL + "/\ud800")})
        self.assertEqual(result["status"], "missing")
        self.assertNotIn("sha256", result)

    def test_prefixe_legiarti_exact_et_prefixe_incomplet_rejete(self) -> None:
        result = extract({"structuredContent": article()})
        self.assertEqual(result["documents"][0]["id"], "LEGIARTI000000000001")
        result = extract({"structuredContent": article(id="LEGIART000000000001")})
        self.assertNotIn("id", result["documents"][0])


class VisibleTextTests(unittest.TestCase):
    def test_texte_ordinaire_markdown_citations_et_stop_conserves(self) -> None:
        text = (
            "**STOP APJA** — contrôle métier requis.\n\n"
            f"Voir [article synthétique]({ARTICLE_URL}) et "
            "[RGPD](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679).\n"
            "La signature du maire demeure requise. `EN_VIGUEUR` reste un indicateur source."
        )
        self.assertEqual(scrub_visible_text(text), {"text": text, "redacted": False, "truncated": False})

    def test_secrets_token_cookie_signature_mail_ip_masques(self) -> None:
        values = (
            "Authorization: Bearer synthetic-private001",
            "token=synthetic-private002",
            "Cookie: session=synthetic-private003; auth=synthetic-private004",
            '"signature": "synthetic-private005"',
            "api_key: synthetic-private006",
            f"Cookie: synthetic-private008 {ARTICLE_URL} synthetic-private009",
            "personne@example.test",
            "192.0.2.100",
            "2001:db8::1",
            "sk-syntheticprivate007",
        )
        for value in values:
            with self.subTest(value=value):
                result = scrub_visible_text("STOP APJA\n" + value + "\nTexte public synthétique.")
                self.assertTrue(result["redacted"])
                self.assertIn("STOP APJA", result["text"])
                self.assertIn("Texte public synthétique.", result["text"])
                self.assertNotIn(value, result["text"])
                self.assertNotIn("synthetic-private", result["text"])
                self.assertNotIn("sha256", result)

    def test_titre_signature_sans_valeur_preserve(self) -> None:
        text = "**Questions à poser avant signature :**\n\n1. Quelle pièce manque ?"
        self.assertEqual(scrub_visible_text(text),
                         {"text": text, "redacted": False, "truncated": False})

    def test_signature_courte_et_valeur_apres_titre_masquees(self) -> None:
        for text in ("signature=abc", "**signature :** secret-test",
                     '"signature": "abc"'):
            with self.subTest(text=text):
                self.assertTrue(scrub_visible_text(text)["redacted"])

    def test_urls_sensibles_entierement_masquees_et_markdown_preserve(self) -> None:
        for url in (
            ARTICLE_URL + "?token=synthetic-private-token",
            ARTICLE_URL + "?signature=synthetic-private-signature",
            "https://person:synthetic-private-password@www.cnil.fr/fr/article",
            ARTICLE_URL + "?api%5Fkey=synthetic-private-key",
        ):
            with self.subTest(url=url):
                result = scrub_visible_text(f"STOP — [source]({url}).")
                self.assertTrue(result["redacted"])
                self.assertEqual(result["text"], "STOP — [source]([DONNÉE MASQUÉE]).")
                self.assertNotIn("synthetic-private", result["text"])

    def test_taille_64k_unicode_invalide_et_cle_privee(self) -> None:
        text = "STOP\n" + "Texte synthétique. " * 5_000
        result = scrub_visible_text(text)
        self.assertTrue(result["truncated"])
        self.assertFalse(result["redacted"])
        self.assertEqual(len(result["text"]), MAX_VISIBLE_CHARS)
        self.assertTrue(result["text"].startswith("STOP\n"))
        result = scrub_visible_text("STOP\n-----BEGIN PRIVATE KEY-----\nsynthetic-private-value\n-----END PRIVATE KEY-----\nFin.")
        self.assertNotIn("synthetic-private", result["text"])
        self.assertTrue(result["redacted"])
        self.assertIn("Fin.", result["text"])
        result = scrub_visible_text("STOP\ud800\x00\nFin.")
        self.assertEqual(result["text"], "STOP\nFin.")
        self.assertTrue(result["redacted"])


if __name__ == "__main__":
    unittest.main()
