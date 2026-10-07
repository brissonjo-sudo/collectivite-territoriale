# Historique des versions

## 1.2.0-dev.5 — 2026-10-07 — Correctif après mesure partielle r7

- STOP conservatoire sans annonce préalable et décision explicite entre preuve
  primaire reçue et voie sans source, limitée aux faits, inconnues et questions.
- Transfert RH persistant dans toutes les rubriques et dans la conclusion.
- Activation DSI demandée dès la description, même pour un cadrage technique
  générique ; questions distinctes sur les collectivités et l'État, sans droit
  confirmé de mémoire.
- Six pins et onze opérations de surcharge inchangés. Aucun scénario, oracle,
  barème ou harnais de mesure modifié.
- R7 dev.4 conservée : six réponses et six juges, une réussite et cinq échecs.
  Un cas interrompu sans réponse et neuf non exécutés. Dev.5 n'en reçoit aucun
  score et reste entièrement non mesuré ; OAuth juridique à renouveler.
- Lanceur arrêté dès qu'un cas nominal constate un MCP non connecté.

## 1.2.0-dev.4 — 2026-10-06 — Correctif méthodologique non mesuré

- Confrontation mot à mot des catégories, qualités, interlocuteurs et conditions
  du primaire à chaque phrase finale ; retrait des équivalences ambiguës.
- Bascule explicite vers DRH avant le fond RH, même après un chargement imposé
  des skills ; cadrage DSI avec inventaire, exploitation, continuité,
  responsabilités, preuves, recette et questions manquantes.
- Six bases amont inchangées ; seuls les contrats locaux déclarés évoluent.
- Conservation de la tentative dev.3 r6 : une réponse APJA complète en échec,
  quinze interruptions de quota. Dev.4 n'a aucune mesure ni score transféré.
- Nouveau gel et seize nouvelles conversations requis ; revues humaines et
  smoke Codex ouverts ; `release_ready=false`.

## 1.2.0-dev.3 — 2026-10-06 — Renforcement de la coactivation, publication bloquée

- Conservation de la campagne dev.2 : 16 cas exécutés, dont trois échecs
  techniques de sélection spontanée. Ses résultats restent attachés à ses
  octets ; aucun jugement ni score n'est transféré vers ce candidat.
- Contrat prioritaire en tête des six skills : STOP avant toute annonce,
  chargement réel de la recherche juridique, texte primaire pertinent pour
  chaque affirmation et abstention intégrale si la récupération est insuffisante.
- Descriptions des cinq métiers resserrées ; variantes locales DSI et DirFi
  déclarées et contrôlées depuis les mêmes commits amont.
- Nouveau gel et nouvelle campagne requis. Relectures DSI/RSSI et juridique
  humaines et smoke Codex non acquis ; `release_ready=false`.

## 1.2.0-dev.2 — 2026-10-06 — Candidat correctif, publication bloquée

- Intégration de DSI 0.2.1 depuis le commit source
  `704e5dd6a3d15994ed431b23585aabd72086ca75`, sans modification locale de ses
  trente fichiers runtime. Les cinq autres bases amont restent figées.
- STOP initial visible, mobilisation effective de la recherche juridique,
  abstention complète sans source primaire et traitement du statut RH inconnu.
  Les surcharges restent déclarées, bornées et contrôlées par empreinte.
- Correction des descriptions DPM/DPO dès la découverte du skill, avec une
  opération de remplacement limitée à ce seul champ de métadonnées.
- Suite de coactivation à seize cas et 124 exigences atomiques, dont cinq
  sélections spontanées. Nouvelle qualification sur le runtime corrigé,
  sans transfert des scores des campagnes antérieures.
- Gel fondé sur les blobs Git bruts, contrôlé avant et après chaque cas,
  et jugement lié à l'exécution native d'un sous-agent frais.
- Collecte des textes primaires assainis et correction de l'assainissement
  qui masquait à tort un titre contenant « signature » sans valeur secrète.
- Retrait des renvois DSI d'exécution vers le cache de maintenance qui n'est
  pas distribué dans le paquet runtime.
- Revue DSI/RSSI, revue juridique humaine et smoke du candidat dans Codex
  restent des barrières distinctes : `release_ready=false`.

## 1.1.1 — 2026-10-03 — Candidat d'alignement DRH

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
