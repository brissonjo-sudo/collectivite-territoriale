# ADR 0009 — Reprise sélective DSI depuis main

Date : 13 octobre 2026. Statut : voie retenue par Jo, préparation locale uniquement.

## Décision

Partir de main 051e13c6. Conserver DCP et la distribution actuelle, éviter de reprendre les 2 498 fichiers de preuves dans le nouveau diff. Les preuves et commits historiques restent récupérables par bundles, aucune suppression ni fermeture.

Reprendre le contenu R5 de #16 comme base d’outillage : trois fichiers source/documentation copiés sans modification, quatrième fichier de tests conservé dans archive et historique, sans ajout ni exécution de tests. Ne pas utiliser les anciens gels pour un nouveau runtime. Le lanceur exige encore les dépendances historiques et un CLI choisi : aucun répondant, juge ou préflight lancé ici.

Retenir DPO 0.2.2 (58ea45c4) pour la prochaine intégration : reprendre les sources figées, recalculer les empreintes et ancres des surcharges, préserver le contrôle humain et les frontières. La copie runtime n’est pas encore effectuée dans ce commit préparatoire.

Conserver DCP 0.1.3 (129f374e) déjà distribuée. Main amont porte encore 0.1.0 ; #6 est brouillon. Ne pas rétrograder ni promouvoir le candidat de #6 sans sa qualification et une validation distincte. Les autres bases restent figées.

## Conséquences

Le successeur est traçable localement par branche, commit et bundle. Il prépare la reprise de #11 et #16 ; il ne contient pas encore l’union runtime DCP/DSI ni la mise à jour DPO. Ces intégrations exigent un nouveau candidat, des manifestes et gels cohérents, de nouvelles preuves et des avis humains. Aucun ancien résultat ne qualifie ces changements.

La fermeture de #11 et #16, la création d’une nouvelle PR, toute poussée et toute campagne restent des validations séparées. Ne proposer la fermeture qu’après un successeur fonctionnel traçable et des liens de remplacement. T44 est reportée.

## Dette hors chantier

DSI-fpt : absence de CI technique sur main et sur la tête actualisée de #1. La revue automatique ignorée sur un brouillon ne la remplace pas. Les jobs des branches de construction ne couvrent pas main. Dette à traiter dans un chantier séparé, sans ajout de workflow ici.
