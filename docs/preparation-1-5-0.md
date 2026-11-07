# Collectivité 1.5.0 : candidat non mesuré, non qualifié

État au **7 novembre 2026**. La 1.5.0 porte le passage à la licence
EUPL 1.2 ([ADR 0030](adr/0030-adoption-eupl-1-2.md)). La version publiée et
les deux catalogues restent sur **1.4.0** jusqu'à la
[procédure prévue](publication.md).

## Nouveau candidat du 7 novembre 2026

Après l'audit du candidat 87b6dac, sur lequel aucune campagne n'a réussi, le
candidat change ([ADR 0032](adr/0032-relecture-attestee-et-statuts-definis.md)) :

- quatrième correction de comportement : dsi-fpt sans contradiction amont
  (motif d'abstention, citation sans chemin) ; trois règles des tentatives e,
  g et h portées dans dpm-fpt, drh-fpt, dirfi-fpt, dpo-ct et
  recherche-juridique ; dcp-fpt inchangé (référence DCP-014) ;
- relecture du harnais à statuts définis et invariants mécaniques non
  abaissables (`mechanical_attestations`), harnais versionné ; le contrat de
  cycle v4 et ses 18 cas ne changent pas ;
- outillage : rechaînage des surcouches, projection publique étendue, timeout
  tolérant une dernière ligne coupée.

Nouvelle série de tentatives sur ce candidat ; la comparaison avec les
tentatives a à i est perdue.

## Épingles et licence (ADR 0030)

- Les sept épingles de `upstream.json` n'ajoutent que les textes de licence ;
  `python scripts/check_sync.py` le contrôle fichier par fichier.
- Les fichiers synchronisés qui changent sont uniquement `skills/*/LICENSE` et
  `skills/*/LICENCE.fr.txt`. Aucun `SKILL.md`, fichier de référence, objet ou
  script de skill ne change.
- La référence DCP-014 reste vérifiée octet par octet sur ses 30 fichiers
  mesurés (`python scripts/check_dcp_protocol.py`).

## Ce qui reste avant publication

1. Contrat de cycle de la 1.5.0 : **tranché**. Contrat v4 à l'identique
   (`scripts/cas-plugin-cycle-v4.json`, mêmes 18 cas) et nouveau pin de CLI
   `codex-cli 0.164.0-alpha.11.1` pour la campagne et le smoke
   ([ADR 0031](adr/0031-mesure-1-5-0-contrat-v4.md)). Le repli v2 est fermé.
2. Mesure complète sur le nouveau runtime (campagne, avis de Jo, smoke réel) :
   la preuve 1.4.0 n'est pas transférée. Pré-vol à blanc, sans processus ni
   écriture, à rejouer sur la tête propre du candidat (dossier hors dépôt, inexistant) :
   `python -B scripts/run_codex_campaign.py --cycle-v4 --plugin-commit <commit> --output-dir <dossier> --dry-run`
   doit afficher `case_contract` v4, l'empreinte `be70f64b...12888f24` et 18 sessions ;
   la même commande sans `--cycle-v4` doit être refusée (« sans commit lié »).
   La mesure réelle passe par le harnais externe et la CLI figée ; H2 lie ensuite
   le seul H1 mesuré (procédure de l'ADR 0031). Le smoke demande la connexion
   Codex et l'OAuth du MCP par Jo :
   `python scripts/run_codex_smoke.py --plugin-commit <commit> --output-dir <dossier> --phase install`
   puis `--phase run`.
3. Assemblage de `tests/evidence/release-1.5.0.json`, puis publication.
