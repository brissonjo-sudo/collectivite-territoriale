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
   avec `distribution.scope: open_source` et `distribution.ready: true`,
   et CI entièrement verte, barrière technique de distribution comprise.
   Depuis le 2026-10-08, la relecture praticien est différée jusqu'au déploiement
   opérationnel dans une structure tierce : [ADR 0007](adr/0007-distribution-open-source-et-deploiement.md).
   `deployment.ready` et le champ historique `release_ready` restent faux
   tant que cette qualification métier n'est pas réalisée.
2. **Après accord de l'auteur, créer l'étiquette annotée** `v<version>` sur le
   commit qualifié présent dans `main`. `plugin_commit` désigne la baseline
   mesurée : le commit publié peut ajouter les preuves et la documentation,
   à condition que les fichiers de skills et la configuration installée aient
   les mêmes empreintes. Le commit publié est consigné dans le registre et
   `source.sha`. Depuis GitHub : *Releases → Draft
   a new release → Choose a tag → v<version> → Target : le commit qualifié*.
   En ligne de commande :

   ```text
   git tag -a v<version> <commit> -m "Publication <version>"
   git push origin v<version>
   ```

3. **Ouvrir une PR de distribution** qui modifie uniquement :
   - `.claude-plugin/marketplace.json` : `version`, `source.ref`
     (`v<version>`), `source.sha` (commit complet) et description du contenu ;
   - `.agents/plugins/marketplace.json` : `source.ref` (`v<version>`) ;
   - ce registre (nouvelle ligne).
4. **Fusionner** une fois la CI verte : l'étape « Vérifier l'étiquette
   distribuée » échoue tant que l'étiquette n'existe pas ou ne désigne pas
   le commit épinglé.

Le statut du registre distingue « distribution open source qualifiée
techniquement » et « déploiement tiers non qualifié ». Le contrôle
`python scripts/qualify_distribution.py` vérifie les empreintes des preuves,
la couverture des scénarios, le runtime et la configuration installée.
Une revue différée ne permet pas d'ignorer un échec technique ou un runtime
modifié. Les preuves historiques gardent leurs statuts d'origine.

La [note praticien conservée](deploiement-collectivite.md) doit être reprise
avant le déploiement dans une collectivité ou une structure tierce.

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
