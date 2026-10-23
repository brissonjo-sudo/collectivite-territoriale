# ADR 0025 — Contrat de cycle v3 pour la mesure 1.4.0

Date : 2026-10-21. Statut : préparation adoptée ; liaison au gel B4 requise.

## Décision de Jo

Le lot B3 autorise un seul invariant supplémentaire dans le seul cas
`plugin-prime-depart-retraite`, au style nominal des invariants existants :

> absence d'indemnité de départ à la retraite instituée, établie sur une source officielle consultée (réponse ministérielle du 22/05/2025, question écrite n° 01222, senat.fr) ; CIA évoqué uniquement de façon conditionnelle, sans présumer le régime de l'agent

Cette référence et cette exigence proviennent de la consigne B3 de Jo du 21/10.
Le lot ne produit aucune consultation juridique ni réponse modèle : l'invariant
exige cette consultation dans la future réponse mesurée. Aucun autre cas,
prompt, invariant, attendu STOP, budget ou seuil ne change.

## Contrats fermés

Le nouveau fichier `scripts/cas-plugin-cycle-v3.json` dérive de v2 par cet
unique ajout. V2 reste intact, avec son SHA-256
`65593a1c46bd31b403c5b83344f14951cbc3455f456eefcde2c6853fa68a9478`.
Son commit mesuré autorisé demeure
`13b4e1e537e5a8097a004ee913abcc9d079114a7` pour la preuve 1.3.0.

Le SHA-256 v3 est
`deb0d39efc93a24b16444922dbafddbb6570801a67e21ca23d612343ba471e89`.
Il est épinglé dans `measurement-cli.json` et dans la table fermée
`cli_toolchains.CYCLE_CONTRACTS`. Ni un chemin déclaré par la preuve, ni un
champ `measurement_commit` de cette preuve, ni une entrée arbitraire ajoutée
au registre CLI ne permettent de choisir v3. Seul le commit d'un index source
lié, présent dans l'autorisation explicite du code, choisit le contrat exact.
La version limite son emploi : v2 pour 1.3.0, v3 pour 1.4.0. Les anciennes
mesures historiques sans contrat lié gardent leur lecture v1 ; aucun repli
v1 ou v2 n'est admis pour une mesure 1.4.0.

Le lecteur de bundle humain utilisé par l'assembleur, les entrées directes de
l'assembleur et le qualificateur vérifient cette liaison. La vue CI conserve
les contrôles de projection et vérifie les liens traduits. Les verrous CLI
utilisés pour les reçus sont lus dans la même racine que le contrat contrôlé.
Les compagnons restent obligatoires pour les mesures explicitement liées.

## Liaison à réaliser au gel B4

Le commit mesuré 1.4.0 n'est pas connu dans B3. Conformément à la consigne,
`MEASUREMENT_140` et `prepared_cycles["1.4.0"].measurement_commit` valent
`null` / `None` : toute qualification ou assemblage 1.4.0 est donc refusé.
Le lanceur peut charger v3 en préparation à blanc, mais refuse l'exécution
réelle avant cette liaison, avant tout appel de processus modèle.

Au gel, B4 doit lier le seul SHA complet effectivement retenu : autorisation
explicite dans `MEASUREMENT_140`, même SHA dans `prepared_cycles`, entrée
`campaign_measurements` correspondante avec le SHA-256 v3 ci-dessus et le
verrou CLI complet réellement retenu. B4 doit résoudre et vérifier la liaison
à une tête mesurée propre : un commit ne peut pas contenir son propre SHA.
Ce travail de gel reste nécessaire avant la campagne ; le présent lot ne
prétend pas résoudre cette autoréférence par un identifiant provisoire.

Aucune autorisation générique de commit ou transition d'outillage n'est
ajoutée. Si le gel nécessite une transition après connaissance du commit,
elle doit être fermée sur les empreintes source et cible puis vérifiée au
pré-vol ; les transitions historiques 0013 et 0017 restent inchangées.

## Vérification locale

Les contre-épreuves sont synthétiques : v3 conforme accepté, v3 altéré refusé,
v2 refusé pour 1.4.0, v3 refusé pour 1.3.0, commit inconnu ou seulement déclaré
refusé, registre seul insuffisant et maintien de la campagne historique sur v2.
Le test de préparation du lanceur interdit tout processus modèle. La fixture
v2 est explicitement rattachée à 1.3.0 et reçoit une projection locale via le
publicateur existant ; ses assertions restent inchangées et l'API publique
de qualification continue d'être appelée.

La barrière de release reste rouge faute de `release-1.4.0.json`. Les suites
locales hors barrière ne valent ni mesure comportementale ni validation
humaine ou juridique. Aucune campagne, relecture modèle, smoke réel,
publication ou poussée n'accompagne B3.
