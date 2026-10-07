# Gabarit décisionnel des branches

> Méta-document (instructions de conception, pas de contenu métier). Toute
> branche de `references/` suit **exactement** cette structure, dans cet ordre.
> Objectif : une écriture interprétable par le modèle, orientée **décision**
> plutôt que description.

## Structure imposée d'une branche

1. **Périmètre / Exclusions** — bloc d'ouverture **obligatoire** : ce que
   couvre la branche (deux phrases) et, en regard, ce qu'elle **exclut** avec
   le renvoi explicite vers la branche ou le skill compétent (évite tout
   chevauchement). Reprend la ligne du tableau §4 du `SKILL.md`.
2. **Questions couvertes** — les familles de questions typiques (liste courte).
3. **Arbre de traitement** — le réflexe de raisonnement :
   `question → variables à lever → décision → vérification → livrable`.
4. **Variables à lever** — paramètres (régime applicable, responsable de
   traitement, catégories de données, échelle, personnes vulnérables...) et
   données manquantes propres à la branche, à clarifier avant de trancher.
5. **Règles métier** — le fond, par sous-domaine. Distinguer toujours :
   régime RGPD / régime Police-Justice, responsable de traitement /
   sous-traitant, obligation / bonne pratique, avis DPO / décision du
   responsable de traitement.
6. **Procédures et délais** (si la branche en comporte) — étapes, acteurs,
   échéances, points de contrôle. Annoncer les hypothèses ; demander les
   données manquantes ; signaler les délais à vérifier.
7. **Déclencheurs de vérification** — les points qui imposent le socle-sources
   (matrice §2.2 du `SKILL.md`).
8. **Pièges & confusions fréquentes** — erreurs typiques à bloquer (notamment
   les confusions de régime, de base légale et de responsabilité).
9. **Données / références à vérifier** — articles, référentiels, listes et
   valeurs à ne jamais citer de mémoire (réserve « à confirmer en version
   consolidée » ; pour la doctrine CNIL/CEPD, dater la version).
10. **Livrables** — classés par nature + éléments obligatoires (pointeur vers
    le générateur `assets/` concerné).
11. **Double échelle [risque / confiance]** — repères par sous-domaine
    (cf. `SKILL.md` §5.1).
12. **Checklist de branche** — contrôles spécifiques avant sortie, dont les
    garde-fous §5.2 si la branche peut les déclencher.

## Règles d'écriture

- Impératif, phrases courtes, une idée par point.
- Aucune **valeur datée** ni numéro d'article cité **de mémoire** : seulement
  les **règles** et la consigne de vérifier la source en vigueur. Les
  références structurelles stables (RGPD, loi 78-17, codes) sont citées avec
  le rappel « à confirmer en version consolidée ».
- **Pas de duplication** : renvoyer aux autres branches et aux générateurs
  par pointeur, ne pas recopier leur contenu. La jurisprudence de fond relève
  de `recherche-juridique`.
- Pas d'instruction de méta-conception dans le corps métier : elle reste ici.
