# Historique des versions

## Qualification candidate — 2026-10-07

- Mesure autonome DCP complète : 26 réussites, une demi-réussite, un échec
  selon le juge ; huit cas critiques réussis. Relecture et sources réservées.
- Précontrôle MCP Codex réussi avec connexion existante. Nouveau lanceur
  séquentiel pour les neuf cas, copies natives et preuves d'outils filtrées.
- Profil Codex distinct de l'activation Skill de Claude et de l'installation
  marketplace ; ADR 0005. Timeout, mode dégradé explicite, preuves sans
  écrasement ni raisonnement. Barrière de publication inchangée.

## Distribution — 2026-10-06 — Marketplaces épinglées (sans changement de version)

- Les marketplaces Claude Code et Codex distribuent l'étiquette `v1.1.1`
  (`cad8bbd`), et non plus `main` : une fusion ne publie plus rien.
- `v1.1.1` est consignée comme non qualifiée, distribuée par défaut jusqu'à
  la qualification de la version suivante.
- Procédure de publication et registre des étiquettes : `docs/publication.md` ;
  décision : `docs/adr/0004-distribution-epinglee.md`.
- CI : vérification obligatoire que l'étiquette distribuée existe et désigne
  le commit épinglé.

## 1.2.0 — 2026-10-06 — Candidat d'intégration DCP

- Ajout de `dcp-fpt` 0.1.0 au commit de fusion amont
  `eeb1cb14a3ad94d78631661dce5ae11f1e071308`, sans surcharge locale.
- Copie des 30 fichiers runtime et de la licence ; cache de valeurs,
  conception, outillage et preuves amont exclus.
- Conservation des cinq autres bases, des trois surcharges et du MCP unique.
- Manifestes Claude/Codex et présentation adaptés aux six skills.
- Cinq scénarios DCP ajoutés au contrat de campagne : égalité, acte
  irréversible, frontières financières/données, DSI externe et mode dégradé.
- Nouvelle preuve de candidat avec `release_ready=false`. Mesure, smoke et
  relecture praticien restent à faire après l'intégration candidate.
- Les preuves historiques conservent leur inventaire d'origine ; elles
  n'attestent aucune activation DCP.
- Reprise du candidat 1.1.1 abandonné (`drh-fpt` 0.6.0) : la qualification
  1.2.0 couvre aussi cet alignement.

## 1.1.1 — 2026-10-03 — Candidat d'alignement DRH (cible de qualification abandonnée, distribution gelée)

- **Abandonné comme cible de qualification le 2026-10-06** par décision du propriétaire ;
  ses changements restent à qualifier dans 1.2.0. L'étiquette `v1.1.1`
  demeure distribuée par défaut, non qualifiée, jusqu'à une nouvelle distribution.

- Mise à jour de `drh-fpt` vers 0.6.0 depuis `main`, au commit
  `f81c9b955f7ebb47df7e93bdc41ac743d85a2973` : dix fichiers modifiés et
  ajout de `references/contrat-execution.md`.
- Conservation des quatre autres bases et des trois surcharges déclarées.
- Clarification de la référence DPM : `main` en 1.0.5, distinct de la branche
  par défaut et du checkout local en 1.0.3 au jour du contrôle.
- Nouvelle barrière de release liée à la 1.1.1 ; les preuves historiques de
  la 1.1.0 ne valent pas qualification de cette mise à jour.

## 1.1.0 — 2026-09-20

- Corrections locales traçables des instructions DPM, DPO et recherche
  juridique : provenance de session, abstention, absence de pouvoir d'attente
  et calcul des délais uniquement à partir de faits connus. Les bases amont
  restent figées ; surcharges contrôlées par SHA-256 et ancre unique.

- Ajout de `recherche-juridique` v3.5.0 comme cinquième skill, figé sur le
  commit amont `e437d10a2d4bbf66ba7a9c1e9fb49e773166054e`.
- Conservation d'un unique serveur MCP `droit-francais` : le skill apporte la
  méthode de vérification, le serveur apporte l'accès aux sources.
- Extension du synchroniseur pour les racines amont, les noms de dépôts locaux
  distincts et les fichiers additionnels attribués.
- Ajout de cas de co-activation DPM/juridique et DPO/juridique, et renforcement
  du cas DirFi/DRH/juridique.
- Ajout de la licence CC-BY-SA-4.0 au runtime juridique embarqué.
- Adoption de CC-BY-SA-4.0 comme licence globale du plugin et de ses cinq
  contenus embarqués.
- Ajout de l'identité visuelle du plugin pour les surfaces Codex et ChatGPT.
- Publication d'une politique de confidentialité propre au plugin, avec renvoi
  vers la politique détaillée du serveur MCP `droit-francais`.
- Déclaration du client OAuth public Claude Code et de son callback local fixe,
  sans secret distribué dans le plugin.
- Ajout d'un lanceur de campagne isolé qui exige les coactivations qualifiées,
  exclut les connecteurs juridiques globaux et assainit les traces avant revue.

## 1.0.1 — 2026-09-19

- Mise à jour de `dirfi-fpt` vers la v1.0.4, figée sur le commit amont
  `d970fe530d3f50f6b4c330e3cfb85db35b7126ab`.
- Clarification de la co-activation DirFi/DRH dans le plugin agrégateur.
- Ajout d'un cas de non-régression ChatGPT/Codex sur une gratification de
  départ à la retraite sans base juridique préalable.

## Distribution Codex — 2026-09-19

- Ajout du manifeste Codex, sans modification des quatre skills ni du serveur MCP partagé.
- Ajout de contrôles automatiques pour les skills exposés, le serveur juridique et l'identité du plugin.
- Ajout d'une marketplace Codex pointant vers la racine Git du dépôt, sans duplication des skills.

## 1.0.0 — 2026-09-18

- Première distribution des quatre skills `dpm-fpt`, `drh-fpt`, `dpo-ct` et `dirfi-fpt` depuis des commits amont figés.
- Déclaration du serveur MCP juridique Légifrance/Judilibre.
- Ajout de `upstream.json`, des scripts de synchronisation et du contrôle CI des copies.
- Le contenu métier des skills reste identique aux dépôts amont.
