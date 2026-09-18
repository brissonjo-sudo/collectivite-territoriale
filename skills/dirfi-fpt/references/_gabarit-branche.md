# Gabarit décisionnel des branches

> Méta-document (instructions de conception, pas de contenu métier). Toute
> branche de `references/` suit **exactement** cette structure, dans cet ordre.
> Objectif : une écriture interprétable par le modèle, orientée **décision**
> plutôt que description.

## Structure imposée d'une branche

1. **Périmètre / Exclusions** — bloc d'ouverture **obligatoire** : ce que couvre
   la branche (deux phrases) et, en regard, ce qu'elle **exclut** avec le renvoi
   explicite vers la branche compétente (évite tout chevauchement). Reprend la
   ligne du tableau §4 du `SKILL.md`.
2. **Questions couvertes** — les familles de questions typiques (liste courte).
3. **Arbre de traitement** — le réflexe de raisonnement :
   `question → variables à lever → décision → vérification → écrit/livrable`.
4. **Variables à lever** — paramètres (strate de collectivité, régime M57 de
   droit commun ou abrégé, existence d'un budget annexe, délégation consentie à
   l'exécutif, date d'effet) et données manquantes propres à la branche, à
   clarifier avant de trancher.
5. **Règles métier** — le fond, par sous-domaine. Distinguer toujours :
   **section** de fonctionnement / d'investissement ; **autorité compétente**
   (assemblée délibérante / exécutif par délégation / comptable public) ;
   **obligation / faculté** ; **crédit ouvert / crédit consommé** ; **acte
   budgétaire / acte d'exécution**.
6. **Calculs et procédures** (si la branche en comporte) — étapes, acteurs,
   échéances, points de contrôle. Poser la **formule** et la **méthode**, jamais
   un résultat reposant sur une valeur non vérifiée. Annoncer les hypothèses ;
   demander les données manquantes ; signaler les délais à vérifier.
7. **Déclencheurs de vérification** — les points qui imposent le socle-sources
   (matrice §2.2 du `SKILL.md`).
8. **Pièges & confusions fréquentes** — erreurs typiques à bloquer (notamment
   les confusions de compétence, les confusions de section, et tout ce qui
   approche la gestion de fait).
9. **Données / valeurs à vérifier** — articles, décrets, taux, seuils, plafonds
   et montants à ne **jamais** citer de mémoire. Appliquer le régime à deux
   vitesses du `SKILL.md` §5.4 point 2 : valeur volatile = jamais de mémoire et
   jamais sans date d'effet ; référence structurelle stable = citable avec la
   réserve « à confirmer en version consolidée ».
10. **Écrits & livrables** — classés par nature (délibération / acte d'exécution
    / note / rapport / convention) + éléments obligatoires (compétence,
    imputation, mentions obligatoires, transmission au contrôle de légalité) +
    pointeur vers le générateur `references/templates/`.
11. **Double échelle [risque / confiance]** — repères par sous-domaine
    (cf. `SKILL.md` §5.1).
12. **Checklist de branche** — contrôles spécifiques avant sortie, dont les deux
    garde-fous (§5.2 ordonnateur/comptable, §5.3 budgétaire) si la branche peut
    les déclencher, et la frontière RH (§5.5) le cas échéant.

## Règles d'écriture

- Impératif, phrases courtes, une idée par point.
- Aucune **valeur datée** ni numéro d'article cité **de mémoire** : seulement
  les **règles**, les **formules** et la consigne de vérifier la source en
  vigueur. Les références structurelles stables (codes, décrets fondateurs) sont
  citées avec le rappel « à confirmer en version consolidée ».
- **Pas de duplication** : renvoyer aux autres branches et aux objets par
  pointeur, ne pas recopier leur contenu. La jurisprudence de fond relève de
  `recherche-juridique`.
- Pas d'instruction de méta-conception dans le corps métier : elle reste ici.
