# Gabarit interactif — Cahier des charges technique (v0.2.0)

> **Usage** : formaliser le besoin technique, les engagements et les preuves de réception.
> **Périmètre** : spécifications et exécution ; passation des marchés hors périmètre.

## Préalables impératifs

Lire `../analyse-situation.md` avant toute question technique. Afficher
intégralement le garde-fou incident du SKILL §5.2 en premier si incident en
cours ou récent. Afficher le garde-fou surveillance §5.3 avant tout contenu
technique s'il est déclenché. Effectuer les `BASCULE dpo-ct`, `drh-fpt`,
`dpm-fpt`, `dirfi-fpt` pertinentes, puis arrêter leur volet de fond.
Une frontière ne s'illustre pas.

Lire `../ecrits-numerique.md` et les branches du besoin. Poser les questions
**une par une**, attendre la réponse ; ne pas redemander ce qui est connu.
Ne demander aucune donnée nominative, aucun secret ou détail d'architecture
exploitable. Décrire les dépendances par catégories et les responsables par rôle.

## Questions à poser dans l'ordre

1. Quel service ou résultat technique doit être fourni, et à qui ce brouillon est-il destiné ?
2. Quel est le mode d'exercice et quels rôles valident les exigences et la réception ?
3. Quels périmètre et exclusions sont confirmés ?
4. Quels usages, fonctions et interfaces sont attendus ?
5. Quels besoins d'hébergement et de sécurité ont été instruits ?
6. Quels besoins d'accessibilité s'appliquent au service ?
7. Quelles exigences d'exploitation, support et continuité sont réellement attendues ?
8. Quelles preuves permettront de constater la réalisation de chaque exigence ?
9. Quels éléments sont attendus pour la documentation, le transfert de compétence et la réversibilité ?
10. Quels niveaux de service, jalons et documents contractuels sont déjà confirmés ?
11. Quelles hypothèses ou décisions restent à instruire ?

Ne pas transformer un souhait en engagement acquis. Ne pas inventer un niveau
de service, une architecture, une référence contractuelle ou un calendrier.
Une exigence juridique est vérifiée avant d'être introduite comme obligation.

## Trame d'assemblage

```text
[INCOMPLET] Cahier des charges technique — [intitulé anonymisé]
Besoin et résultat attendu : [à renseigner]
Mode d'exercice / rôles de validation : [à renseigner]
Périmètre / exclusions : [à renseigner]
Usages et fonctions : [à renseigner]
Interfaces et dépendances par catégories : [à renseigner]
Hébergement et sécurité : [exigences instruites / réserves]
Accessibilité : [exigences instruites / preuves attendues]
Exploitation, support et continuité : [à renseigner]
Table des exigences : [identifiant interne / exigence / origine / preuve / rôle validateur]
Réception : [conditions établies / preuves / gestion des réserves]
Documentation et transfert de compétence : [à renseigner]
Réversibilité et restitution : [périmètre / preuve / responsabilités]
Niveaux de service et jalons : [confirmés, ou à définir]
Documents contractuels effectivement applicables : [confirmés, ou à vérifier]
Sources mobilisées et dates de consultation : [à renseigner]
Hypothèses, décisions en attente et champs manquants : [liste explicite]
```

## Vérification avant livraison

Conserver `[INCOMPLET]` jusqu'à renseignement des éléments nécessaires. Chaque
exigence possède une origine et une preuve ; aucun critère de sélection ou
choix de procédure de marché n'est produit. Vérifier applicabilité et valeurs
selon `../socle-sources-verification.md` et `../references-verifiees.md`.

Fond métier selon le besoin : `../applications-interoperabilite.md`,
`../infrastructures-reseaux.md`, `../cloud-hebergement.md`,
`../securite-si.md`, `../accessibilite-numerique.md`,
`../contrats-prestataires.md`, `../crise-cyber-continuite.md`.
Lire chaque branche mobilisée et citer son chemin au point d'usage.
