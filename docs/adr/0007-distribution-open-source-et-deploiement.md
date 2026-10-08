# ADR 0007 — Distribution open source et déploiement opérationnel

Date : 2026-10-08. Statut : accepté, instruction explicite de l'auteur.

## Décision

La relecture praticien devient une condition du déploiement dans une
collectivité ou une structure tierce. Elle ne bloque plus l'intégration ni
la distribution du plugin open source. Cette décision supersède uniquement
cette condition de publication des ADR 0003 à 0006 et des rapports antérieurs.

La distribution conserve un contrôle technique : runtime identique aux preuves,
neuf cas plugin réussis techniquement, absence de violation textuelle constatée
par la relecture automatisée, seuil autonome DCP atteint et smoke installé
réussi. Les sources non vérifiables, la demi-réussite et les limites de contexte
restent publiées. Les STOP, BASCULE et validations humaines des actes métier
restent dans les skills.

## Deux états

`distribution.ready` qualifie ces conditions techniques pour la distribution
open source. `deployment.ready` qualifie l'usage opérationnel dans une structure.
Le champ historique `release_ready` garde son sens de qualification métier
complète et reste faux sans les avis requis : il n'est plus le verrou de
distribution. Les statuts historiques, invariants non attestés et preuves
originales ne sont pas promus ni réécrits.

La note praticien est conservée dans `docs/deploiement-collectivite.md` et
les grilles existantes restent vierges. Avant un déploiement tiers, les avis
doivent porter sur la version effectivement déployée et les circonstances
locales ; la qualification technique ne les remplace pas.

## Publication

Le job de distribution vérifie les preuves, leurs empreintes, les 167 fichiers
de skills et la configuration installée. Le catalogue reste épinglé sur une
étiquette. Fusion, création de l'étiquette annotée et bascule des catalogues
restent des actions distinctes, suivant `docs/publication.md` et l'accord
de l'auteur. Cette décision ne réalise aucune de ces actions.
