# Qualification du candidat avec DCP 0.1.1 — 2026-10-07

Correctif DCP épinglé au commit amont `caef7fd9e680dc28056998532d24befa0e8680ec`.
Seul `skills/dcp-fpt/SKILL.md` change dans les copies métier ; aucun changement
des cinq autres bases, surcharges, MCP ou catalogues. Distribution v1.1.1.

Les 28 cas autonomes sont achevés : 27 RÉUSSITE, une DEMI-RÉUSSITE (cas-24),
zéro ÉCHEC. Le seuil automatique est atteint ; cas-01 et cas-16 réussis.
Sept critiques réussis et un demi-réussi. Vingt alertes de citations dans
huit cas restent à relire. Les neuf cas plugin sont exécutés séparément sur
ces nouveaux octets. Baseline d'exécution : `4dfec61aa81b54b21b347b2ebe077bdc54fc8940`.
Vérificateur corrigé : `bf2e695fa752edf3ffd3c2f0d4d8c74d4a282698`.

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

## Résultats et audit des lectures

Les neuf contrôles techniques passent après audit. Les rapports d'exécution
initiaux comptent **cinq réussites et quatre faux positifs** : APJA, égalité,
acte irréversible et frontière DSI. Le lanceur rejetait sept sélections de
références réalisées avec Get-Content / Select-Object, alors que les références
peuvent être consultées par passages. Le contrôle intégral des points
d'entrée reste obligatoire et inchangé.

Les commandes ont été extraites des seuls journaux locaux correspondant
aux neuf sessions, puis chaque sortie a été confrontée byte pour byte au
segment attendu du runtime figé. Aucun raisonnement n'est exporté. Un hash
de chaque journal source rattache cette extraction ; ces journaux restent
privés. Le correctif n'admet ni commande mixte ni chemin extérieur. Les
contre-épreuves refusent une sortie différente ou une commande augmentée.

Les réponses, statuts et empreintes d'exécution initiaux sont conservés.
L'audit supplémentaire et le statut vérifié figurent séparément dans
`audit-lectures.json` et `summary.json`. La reprise APJA, réalisée avant le
diagnostic, reste supplémentaire et ne remplace pas la réponse initiale.
Aucun nouveau contexte modèle ni attendu métier pour cette reclassification.

Deuxième contrôle : BASCULE dirfi-fpt et dpo-ct avant leurs intertitres,
STOP en première ligne des trois cas concernés, aucun identifiant cité
sans récupération correspondante dans les métadonnées MCP. Ces constats
mécaniques de l'assistant ne vérifient pas le texte, la vigueur ou la portée.
**Réserve DPO :** la décision est attribuée au responsable de traitement,
sans revue humaine explicitement demandée avant chaque notification externe.
Voir `relecture-assistant.json` et la grille praticien.

Certaines références complémentaires sont restituées avec troncature,
signalée dans les réponses. Le contrôle intégral couvre les points d'entrée,
pas toutes les références possibles. Un lien contenant le chemin personnel
d'un dossier temporaire a été converti en chemin runtime relatif dans la
preuve publique ; l'original filtré est conservé hors dépôt et les deux
réponses sont empreintées dans le champ `redaction`.

Preuves : `tests/evidence/2026-10-07-codex-natif-v3/`, reprise séparée,
`tests/evidence/2026-10-07-correctif/dcp-autonome.json` et installation locale.
Grille concrète : `docs/relecture-correctif-codex-2026-10-07.md`.
**56 tests logiciels découverts : 55 réussis, seule barrière de publication
sautée dans l'intégration.** Les six copies restent conformes à upstream.json.
La barrière exécutée séparément reste en échec, `release_ready=false`.
La CI du nouveau commit final reste à observer.

La preuve initiale de publication est copiée byte pour byte dans
`tests/evidence/2026-10-07-candidat/release-initial-0.1.0.json`. Les tests
historiques comparent leurs empreintes au commit initial et non au nouveau
runtime. La preuve courante reste non qualifiée pendant la nouvelle mesure.
Avis praticien non renseigné, barrière de publication toujours active.
