# Collectivité 1.5.0 : candidat non mesuré, non qualifié

État au **1er novembre 2026**. La 1.5.0 porte le passage à la licence
EUPL 1.2 ([ADR 0030](adr/0030-adoption-eupl-1-2.md)). La version publiée et
les deux catalogues restent sur **1.4.0** jusqu'à la
[procédure prévue](publication.md).

## Aucun comportement modifié

- Les sept épingles de `upstream.json` n'ajoutent que les textes de licence ;
  `python scripts/check_sync.py` le contrôle fichier par fichier.
- Les fichiers synchronisés qui changent sont uniquement `skills/*/LICENSE` et
  `skills/*/LICENCE.fr.txt`. Aucun `SKILL.md`, fichier de référence, objet ou
  script de skill ne change.
- La référence DCP-014 reste vérifiée octet par octet sur ses 30 fichiers
  mesurés (`python scripts/check_dcp_protocol.py`).

## Ce qui reste avant publication

1. Décider le contrat de cycle de la 1.5.0 (aucun n'est lié à cette version).
2. Mesure complète sur le nouveau runtime (campagne, avis de Jo, smoke réel) :
   la preuve 1.4.0 n'est pas transférée. Le smoke demande la connexion Codex
   et l'OAuth du MCP par Jo :
   `python scripts/run_codex_smoke.py --plugin-commit <commit> --output-dir <dossier> --phase install`
   puis `--phase run`.
3. Assemblage de `tests/evidence/release-1.5.0.json`, puis publication.
