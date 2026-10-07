# Qualification du candidat avec DCP 0.1.1 — 2026-10-07

Correctif DCP épinglé au commit amont `caef7fd9e680dc28056998532d24befa0e8680ec`.
Seul `skills/dcp-fpt/SKILL.md` change dans les copies métier ; aucun changement
des cinq autres bases, surcharges, MCP ou catalogues. Distribution v1.1.1.

Les 28 cas autonomes sont achevés : 27 RÉUSSITE, une DEMI-RÉUSSITE (cas-24),
zéro ÉCHEC. Le seuil automatique est atteint ; cas-01 et cas-16 réussis.
Sept critiques réussis et un demi-réussi. Vingt alertes de citations dans
huit cas restent à relire. Les neuf cas plugin sont rejoués séparément sur
ces nouveaux octets, sans réécriture des réponses historiques.

## Contrôle d'installation réel

Marketplace locale `qualification-locale`, source locale du candidat,
`CODEX_HOME` dédié, sans compte ni copie de secrets. Les commandes
marketplace add, plugin add et plugin list réussissent. Le serveur Codex
est initialisé et `skills/list` découvre les six noms qualifiés avec leur
pluginId et leurs chemins sous le cache de cette installation. Les 167
fichiers de skills sont identiques au candidat. Aucune copie native n'est
ajoutée au workspace pour ce contrôle.

Preuve assainie : `tests/evidence/2026-10-07-correctif/installation-codex.json`.
Ce smoke prouve l'installation locale et la découverte par le gestionnaire
de plugins. Il ne teste ni l'installation Git depuis le catalogue distribué,
ni la réponse d'un modèle ou l'appel MCP depuis ce plugin installé sans compte.
Le moteur signale un skill global invalide, non chargé ; les skills système
restent visibles malgré le CODEX_HOME distinct.

## Essai de coactivation v2 et profil corrigé v3

L'essai v2 est arrêté après deux cas complets : la sortie brute contenait
le point d'entrée juridique complet, mais le modèle déclarait une restitution
tronquée. Les deux preuves restent intactes dans leur dossier d'essai ; leur
statut technique ne prouve pas la visibilité intégrale du texte au modèle.
Voir la [politique de troncature Codex](https://github.com/openai/codex/blob/main/codex-rs/core/src/tools/context.rs).

Le profil v3 restitue chaque point d'entrée par plages contiguës de lignes,
au plus 6000 octets chacune, dans des appels séparés. Le lanceur compare les
plages ordonnées à la partition attendue, refuse trous et doublons, et
confronte chaque contenu retourné au segment source. Seul le pipeline de
lecture strictement généré est accepté ; les expressions libres et chemins
extérieurs sont refusés. Les traces ne conservent que chemins, plages,
empreintes et résultats de contrôle. Cela contrôle la restitution native,
sans attester l'attention du modèle ou le déclenchement implicite du skill.
Les cas et invariants métier restent inchangés.

La preuve initiale de publication est copiée byte pour byte dans
`tests/evidence/2026-10-07-candidat/release-initial-0.1.0.json`. Les tests
historiques comparent leurs empreintes au commit initial et non au nouveau
runtime. La preuve courante reste non qualifiée pendant la nouvelle mesure.
Avis praticien non renseigné, barrière de publication toujours active.
