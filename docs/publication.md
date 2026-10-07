# Publication et distribution du plugin

> Les marketplaces Claude Code (`.claude-plugin/marketplace.json`) et Codex
> (`.agents/plugins/marketplace.json`) distribuent une **étiquette publiée**,
> jamais l'état courant de `main`. `main` peut donc accueillir un candidat
> non qualifié sans le distribuer. Décision : `docs/adr/0004-distribution-epinglee.md`.

## Registre des étiquettes distribuées

| Étiquette | Commit | Date | Statut | Motif |
|---|---|---|---|---|
| `v1.1.1` | `cad8bbdbc1db2163c758fb46ef3e745a18c9c957` | 2026-10-06 | **non qualifiée**, distribuée par défaut | Gel de ce que la marketplace distribuait en suivant `main`, en attendant la qualification de 1.2.0 |

Ajouter une ligne par étiquette distribuée ; ne jamais réécrire une ligne.
Le test `test_distribution_epinglee_sur_etiquette` exige que l'étiquette et
le commit épinglés figurent dans ce tableau.

Le gel historique `v1.1.1` utilise une étiquette légère déjà existante,
vérifiée sur le commit du tableau. C'est une exception à la procédure des
nouvelles publications ci-dessous, qui exige une étiquette annotée. Cette
étiquette historique ne doit être ni déplacée ni recréée ; son existence
ne qualifie pas le contenu distribué.

## Publier une nouvelle version

1. **Qualifier le candidat sur `main`** : `tests/evidence/release-<version>.json`
   avec `release_ready: true` (campagne, relecture juridique, smoke Codex),
   et CI entièrement verte, barrière de publication comprise.
2. **Créer l'étiquette annotée** `v<version>` sur le commit qualifié, celui qui
   figure dans `plugin_commit` de la preuve. Depuis GitHub : *Releases → Draft
   a new release → Choose a tag → v<version> → Target : le commit qualifié*.
   En ligne de commande :

   ```text
   git tag -a v<version> <commit> -m "Publication <version>"
   git push origin v<version>
   ```

3. **Ouvrir une PR de distribution** qui modifie uniquement :
   - `.claude-plugin/marketplace.json` : `version`, `source.ref`
     (`v<version>`) et `source.sha` (commit complet) ;
   - `.agents/plugins/marketplace.json` : `source.ref` (`v<version>`) ;
   - ce registre (nouvelle ligne).
4. **Fusionner** une fois la CI verte : l'étape « Vérifier l'étiquette
   distribuée » échoue tant que l'étiquette n'existe pas ou ne désigne pas
   le commit épinglé.

## Effet pour les utilisateurs

- Claude Code : `/plugin marketplace update collectivite-territoriale`
  puis `/plugin update collectivite-territoriale@collectivite-territoriale`.
  La version du cache est celle du champ `version` : tant qu'elle ne change
  pas, aucune mise à jour n'est appliquée.
- Codex : `codex plugin marketplace upgrade collectivite-territoriale`. Le
  catalogue est lu sur `main` ; le plugin est récupéré à l'étiquette.

## Revenir en arrière

Repointer les deux marketplaces vers l'étiquette précédente du registre, par
une PR de distribution. Ne jamais déplacer ni supprimer une étiquette publiée.
