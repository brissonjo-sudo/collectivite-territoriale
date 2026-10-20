# Gabarit interactif — Fiche projet SI (v0.2.0)

> **Usage** : préparer un arbitrage ou le pilotage d'un projet SI.
> **Statut du produit** : brouillon d'aide à la décision ; aucune décision réputée prise.

## Préalables impératifs

Lire `../analyse-situation.md` avant toute question de rédaction. Si incident
en cours ou récent, afficher intégralement le garde-fou du SKILL §5.2 comme
premier livrable. Si accès aux contenus ou traces d'une personne, ou surveillance,
afficher intégralement le garde-fou §5.3 avant tout contenu technique.
Effectuer les blocs `BASCULE` puis arrêter le volet concerné : `dpo-ct`,
`drh-fpt`, `dpm-fpt`, `dirfi-fpt`. Passation hors périmètre.

Lire `../ecrits-numerique.md`, puis les branches ci-dessous. Poser les
questions **une par une**, attendre la réponse, réutiliser les informations
déjà fournies. Ne demander que des rôles et catégories anonymisés. Aucune
donnée nominative, aucun secret, aucune architecture réelle exploitable.

## Questions à poser dans l'ordre

1. Quelle décision concrète attendez-vous, et à quel rôle la fiche est-elle destinée ?
2. Quel besoin de service public motive le projet et quel résultat est attendu ?
3. La fonction SI est-elle internalisée, mutualisée ou externalisée ?
4. Quel est le périmètre du projet et quelles sont ses exclusions ?
5. Quels rôles portent le besoin, pilotent et valident la réception ?
6. Quelles dépendances et interfaces faut-il décrire par catégories ?
7. Quelles options sont réellement envisagées et quels faits permettent de les comparer ?
8. Quels risques et points à vérifier ont déjà été identifiés ?
9. Quels jalons et moyens ont été confirmés, et lesquels restent des hypothèses ?
10. Quels critères de réception, d'exploitation et de sortie sont attendus ?
11. Quels éléments techniques de coût complet sont disponibles pour le volet financier compétent ?
12. Quelle option proposez-vous à l'arbitrage, avec quelles réserves ?

Ne pas inventer une option, un coût, un prestataire, une date ou un niveau de
service. Une recommandation de la DSI reste distincte de la décision.

## Trame d'assemblage

```text
[INCOMPLET] Fiche projet SI — [intitulé anonymisé]
Destinataire : [rôle]
Décision attendue : [à renseigner]
Besoin et résultat attendu : [à renseigner]
Périmètre / exclusions : [à renseigner]
Mode d'exercice et responsabilités : [à renseigner]
Dépendances et interfaces, par catégories : [à renseigner]
Options et éléments de comparaison : [à renseigner]
Risques / confiance / vérifications requises : [à renseigner]
Jalons et moyens confirmés / hypothèses : [à renseigner]
Réception, exploitation et sortie : [à renseigner]
Éléments techniques de coût complet : [à renseigner ou BASCULE dirfi-fpt]
Proposition soumise à arbitrage et réserves : [à renseigner]
Décision effectivement prise : [non renseignée tant que non communiquée]
Sources mobilisées et dates de consultation : [à renseigner]
Champs manquants : [liste explicite]
```

## Vérification avant livraison

Conserver `[INCOMPLET]` et la liste des champs manquants tant qu'une donnée
nécessaire manque. Vérifier les obligations, compétences, versions et valeurs
selon `../socle-sources-verification.md` et `../references-verifiees.md`.
Citer chaque chemin de branche à l'endroit où son contenu est utilisé.

Fond métier : `../gouvernance-strategie.md`,
`../applications-interoperabilite.md`, `../securite-si.md`,
`../contrats-prestataires.md`. Aucun fond budgétaire, RH ou RGPD dans la fiche.
