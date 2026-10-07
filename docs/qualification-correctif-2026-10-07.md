# Qualification du candidat avec DCP 0.1.1 — 2026-10-07

Correctif DCP épinglé au commit amont `caef7fd9e680dc28056998532d24befa0e8680ec`.
Seul `skills/dcp-fpt/SKILL.md` change dans les copies métier ; aucun changement
des cinq autres bases, surcharges, MCP ou catalogues. Distribution v1.1.1.

Les 28 cas autonomes sont mesurés dans un nouveau kit côté DCP. Les deux
réserves cas-01 et cas-16 sont jugées RÉUSSITE dans ce kit ; cela ne constitue
pas encore un score global. Les neuf cas plugin doivent aussi être rejoués
sur ces nouveaux octets, sans réécriture des réponses historiques.

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

## Profil de coactivation v2

Les cas et invariants restent inchangés. Le lanceur refuse de compter comme
lecture une commande mixte, un chemin extérieur ou un extrait demandé par
Tail/TotalCount. Il confronte le contenu complet de chaque point d'entrée à
la sortie de lecture avant de valider sa preuve, sans conserver ce contenu
dans la trace publique. Les réponses et appels MCP sont filtrés en mémoire.

La preuve initiale de publication est copiée byte pour byte dans
`tests/evidence/2026-10-07-candidat/release-initial-0.1.0.json`. Les tests
historiques comparent leurs empreintes au commit initial et non au nouveau
runtime. La preuve courante reste non qualifiée pendant la nouvelle mesure.
Avis praticien non renseigné, barrière de publication toujours active.
