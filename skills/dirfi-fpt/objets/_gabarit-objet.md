# Gabarit des objets métier

> Méta-document (instructions de conception, pas de contenu métier). Toute fiche
> de `objets/` suit **exactement** cette structure. Principe directeur :
> **l'objet agrège et pointe, il ne duplique pas**. Le fond reste dans les
> branches de `references/` ; l'objet rassemble ce qui concerne une **situation
> type récurrente** et donne le chemin.

## En-tête obligatoire

```
# Objet métier — [nom] (vX.Y.Z)

> **Situation type** : [une phrase décrivant la situation concrète]
> **[Risque / Confiance]** : [niveau / niveau]
```

## Structure imposée (6 sections)

1. **Acteurs et autorités compétentes** — tableau : qui décide, qui exécute, qui
   contrôle, qui paie. Faire apparaître l'assemblée délibérante, l'exécutif,
   l'ordonnateur, le comptable public assignataire et, le cas échéant, le
   représentant de l'État.
2. **Textes applicables** — **pointeurs** vers les branches de `references/`,
   pas de recopie. Nommer le texte structurant sans en citer les valeurs.
3. **Procédures** — étapes numérotées, délais, points de contrôle. Signaler les
   délais à vérifier plutôt que de les énoncer de mémoire.
4. **Écrits associés** — pointeur vers `references/templates/` et mentions
   obligatoires propres à l'objet.
5. **Jurisprudence clé** — pointeur vers `recherche-juridique`. Ne jamais citer
   une décision par son seul nom d'usage ou son millésime.
6. **Check-list opérationnelle** — cases `- [ ]`, incluant le garde-fou
   ordonnateur/comptable (`SKILL.md` §5.2) dès que l'objet peut le déclencher, et
   le garde-fou budgétaire (§5.3) le cas échéant.

## Section finale

**Références et remontées** — branches de frontière mobilisées, et point de mise
à jour requis (valeur volatile, réforme attendue).

## Règles d'écriture

- Impératif, phrases courtes.
- Aucune valeur chiffrée de mémoire.
- Aucune donnée nominative.
- Tout renvoi se fait en chemin relatif depuis `objets/` (ex.
  `../references/execution-recette.md`).
