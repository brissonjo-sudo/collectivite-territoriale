# Gabarit des objets métier

> Méta-document (instructions de conception, pas de contenu métier). Toute
> fiche de `objets/` suit **exactement** cette structure. Principe directeur :
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

1. **Acteurs et autorités compétentes** — tableau : qui **décide**
   (exécutif, assemblée), qui **exécute** (DSI, service mutualisé,
   prestataire), qui **exige et contrôle** (DPO, RSSI), qui **paie**
   (`dirfi-fpt`). Faire apparaître le mode d'exercice.
2. **Textes applicables** — **pointeurs** vers les branches de `references/`,
   pas de recopie. Nommer le texte structurant sans en citer les valeurs, et
   dire s'il vise la collectivité.
3. **Procédures** — étapes numérotées, points de contrôle. Signaler les délais
   à vérifier plutôt que de les énoncer de mémoire.
4. **Écrits associés** — pointeur vers `references/templates/` et mentions
   propres à l'objet.
5. **Jurisprudence clé** — pointeur vers `recherche-juridique`. Ne jamais citer
   une décision par son seul nom d'usage ou son millésime.
6. **Check-list opérationnelle** — cases `- [ ]`, incluant les garde-fous
   (`SKILL.md` §5.2, §5.3) dès que l'objet peut les déclencher, et les bascules
   de frontière.

## Section finale

**Références et remontées** — branches et skills de frontière mobilisés, et
point de mise à jour requis (texte en attente, calendrier échelonné, nouvelle
version de référentiel).

## Règles d'écriture

- Impératif, phrases courtes.
- Aucune valeur de mémoire, aucun identifiant officiel.
- Aucune donnée nominative, aucun secret, aucun détail d'architecture
  exploitable.
- Tout renvoi se fait en chemin relatif depuis `objets/` (ex.
  `../references/securite-si.md`).
