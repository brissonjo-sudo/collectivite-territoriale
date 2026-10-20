# Gabarit décisionnel des branches

> Méta-document (instructions de conception, pas de contenu métier). Toute
> branche de `references/` suit **exactement** cette structure, dans cet ordre.
> Objectif : une écriture interprétable par le modèle, orientée **décision**
> plutôt que description.

## Structure imposée d'une branche

1. **Périmètre / Exclusions** — bloc d'ouverture **obligatoire** : ce que
   couvre la branche (deux phrases) et ce qu'elle **exclut**, avec le renvoi
   explicite vers la branche ou le skill compétent. Reprend la fiche de cadrage
   de la branche (`docs/cadrage.md` §6).
2. **Questions couvertes** — familles de questions typiques (liste courte).
3. **Arbre de traitement** —
   `question → variables à lever → décision → vérification → écrit/livrable`.
4. **Variables à lever** — mode d'exercice (internalisé, mutualisé,
   externalisé) ; catégorie et taille de la collectivité quand un texte en
   dépend ; nature et sensibilité des données ; criticité du service ;
   prestataire et contrat en place ; date de référence.
5. **Règles métier** — le fond, par sous-domaine. Distinguer toujours :
   **obligation** (texte qui vise la collectivité) / **bonne pratique**
   (doctrine) ; **collectivité** / **État** ; **décision** (exécutif,
   assemblée) / **exécution technique** (DSI) / **exigence** (DPO).
6. **Procédures** (si la branche en comporte) — étapes, acteurs, points de
   contrôle. Annoncer les hypothèses ; demander les données manquantes ;
   signaler les délais à vérifier.
7. **Déclencheurs de vérification** — les points qui imposent le
   socle-sources et le test d'applicabilité (matrice `SKILL.md` §2.2).
8. **Pièges et confusions fréquentes** — erreurs typiques à bloquer, dont les
   confusions État / collectivité, obligation / doctrine, et tout ce qui
   approche les garde-fous.
9. **Données et valeurs à vérifier** — textes, seuils, délais, dates
   d'application et versions de référentiels à ne **jamais** citer de mémoire.
   Les nommer **sans** les valeurs ; renvoyer à `references-verifiees.md`.
10. **Écrits et livrables** — nature, éléments obligatoires, pointeur vers le
    gabarit de `references/templates/`.
11. **Double échelle [risque / confiance]** — repères par sous-domaine
    (`SKILL.md` §5.1).
12. **Checklist de branche** — contrôles avant sortie, dont les garde-fous
    (§5.2 incident, §5.3 surveillance) si la branche peut les déclencher, et
    les frontières concernées.

## Règles d'écriture

- Impératif, phrases courtes, une idée par point.
- **Aucun identifiant officiel** (Légifrance, CELEX) : ils ne figurent que
  dans `references-verifiees.md`. Citer les textes par leur objet, avec la
  réserve « à confirmer en version consolidée ».
- **Aucune valeur** (montant, seuil, délai, date d'application, numéro de
  version de référentiel) : seulement la règle et l'endroit où vérifier.
- **Applicabilité explicite** : toute obligation énoncée dit pourquoi elle
  vise la collectivité, ou signale qu'elle ne la vise pas.
- **Pas de duplication** : renvoyer aux autres branches, objets et skills par
  leur chemin ou leur nom.
- **Aucun mode opératoire offensif**, aucun secret, aucun détail
  d'architecture exploitable.
- Pas d'instruction de méta-conception dans le corps métier : elle reste ici.
