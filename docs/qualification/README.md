# Qualification de la coactivation au 7 octobre 2026

La campagne native Codex R2 est achevée : seize réponses et seize juges frais,
soit 32 rôles distincts ; 4 réussites, 6 échecs et 6 cas bloqués. Les 124 exigences atomiques
donnent 107 vraies, 6 fausses et 11 indéterminées.
Onze cas imposent les rôles et cinq permettent leur sélection spontanée.

Cette mesure porte exclusivement sur dev.5 au commit candidat
`3f0d34bd068e3427edc9335a4f1415aaf1c7c98d`, runtime `ebeee944e878b11177d5ccb85d9043c4c97260a9`. L'audit indépendant rejoue les appels
natifs, les lectures par fragments, les réponses et les jugements ; il contrôle
les 211 fichiers gelés, dont 166 fichiers de runtime. Les messages initiaux
opaques et l'isolation complète du système partagé ne sont pas vérifiés.
Les séquences imposées et le rappel initial de STOP ne démontrent pas,
à eux seuls, un déclenchement autonome par le plugin.

Les agents ont chargé les fichiers candidats. L'activation réelle du plugin
n'est pas démontrée ; une exigence littérale « via Skill » ne peut donc pas
être validée par cette seule lecture. Les sources retrouvées, leur pertinence
pour chaque affirmation et leur vigueur sont des contrôles distincts.
Certains retours de sources sont tronqués ; leur transport réel est conservé,
sans prétendre que leur contenu complet a été disponible au répondant.
La tentative d'écriture hors périmètre du cas spontané RSSI/RH a été refusée
par Windows, conservée et classée comme échec technique. Aucune réponse
n'a été réécrite ni relancée pour améliorer le score.

Le candidat courant `1.2.0-dev.6` est distinct et **non mesuré**. La campagne dev.5 reste historique et aucun de ses scores ne lui est transféré. Un nouveau gel, une mesure propre à ses octets et son smoke Codex restent nécessaires.

Cette campagne a été exécutée ici avec les sous-agents natifs Codex, sans
lancer Claude Code ni exiger son authentification. Les avis humains DSI/RSSI
et juridiques, le smoke du candidat et la qualification de release restent
ouverts ; `release_ready=false`. Ni fusion, ni publication n'est autorisée
par la mesure ou par une CI seule.

Voir le [rapport R2](../../tests/evidence/coactivation-codex-dev5-r2/rapport.md),
la [synthèse](../../tests/evidence/coactivation-codex-dev5-r2/synthese.json) et
l'[audit natif complet](../../tests/evidence/coactivation-codex-dev5-r2/audit-natif-final.json).
L'outillage et l'inventaire des octets sont archivés avec les preuves R2.

La portée R1 exploratoire, les premières lectures tronquées et les tentatives
rejetées sont conservées. Elles ne contribuent pas aux résultats R2.
R7 dev.4 reste une mesure partielle : six réponses et six juges frais,
une réussite et cinq échecs ; trois nominaux `needs-auth`, un cas interrompu
sans réponse et neuf cas non exécutés. Voir le
[rapport r7](../../tests/evidence/coactivation-corrigee/rapport-partiel-corrections-r7.md).
R4, R5 et R6, leurs synthèses et leurs traces restent dans
`tests/evidence/coactivation-corrigee`. Leurs scores ne sont pas transférés.

Le script historique `Reprendre-coactivation-corrigee.ps1` et son outillage
restent conservés pour reproductibilité de l'ancienne voie d'exécution.
Ils ne sont pas un préalable à la campagne native Codex exécutée ici.
Une future mesure devra utiliser le candidat courant figé, des rôles frais
et une nouvelle portée de preuve ; aucun dossier achevé ne doit être complété
après changement de candidat ou d'authentification.

La [PR DSI #5](https://github.com/brissonjo-sudo/DSI-fpt/pull/5) porte le bilan
et la présentation. La
[PR plugin #11](https://github.com/brissonjo-sudo/collectivite-territoriale/pull/11)
reste brouillon. Le contrôle local, la CI, la mesure, les avis humains, le smoke
et la publication sont rapportés séparément.
