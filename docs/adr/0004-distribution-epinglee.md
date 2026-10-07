# ADR 0004 — Distribution épinglée sur une étiquette publiée

- Date : 2026-10-06
- Précision du 2026-10-07 : exception pour l'étiquette légère historique et
  séparation explicite des jobs d'intégration et de publication.
- Statut : accepté par le propriétaire ; effectif dès la création de
  l'étiquette `v1.1.1` et la fusion de la PR qui épingle les marketplaces.

## Contexte

Les deux marketplaces suivaient `main` : la marketplace Claude Code par une
source relative (`./`), la marketplace Codex par `ref: main`. Toute fusion
distribuait donc immédiatement son contenu. `main` ne pouvait pas accueillir
un candidat non qualifié, comme l'intégration de `dcp-fpt` (PR #9), sans le
publier. Aucune version n'a encore été qualifiée par la barrière de
publication : le candidat 1.1.1 (`cad8bbd`) est pourtant celui que reçoivent
les utilisateurs aujourd'hui.

## Décision

1. Distribuer une **étiquette** `v<version>`, jamais le runtime courant de `main`.
   Les nouvelles publications utilisent une étiquette annotée. Le gel
   historique `v1.1.1` conserve son étiquette légère existante, sans déplacement
   ni recréation ; son commit est vérifié comme celui d'une étiquette annotée.
   - Claude Code : source `github` sur ce même dépôt, avec `ref` (étiquette)
     et `sha` (commit complet), conformément à la référence des marketplaces
     de Claude Code.
   - Codex : source `url` avec `ref` sur la même étiquette.
2. **Geler l'existant** : étiquette `v1.1.1` sur `cad8bbd`. Les utilisateurs
   reçoivent exactement le contenu qu'ils recevaient. Elle est consignée comme
   **non qualifiée, distribuée par défaut** jusqu'à la qualification de 1.2.0.
3. `main` devient la branche d'intégration : un candidat peut y être fusionné
   avec sa barrière de publication rouge, sans être distribué.
4. Toute nouvelle publication suit `docs/publication.md` : qualification,
   étiquette sur le commit qualifié, puis PR de distribution.

## Contrôles

- `test_distribution_epinglee_sur_etiquette` : source épinglée, `ref` égale à
  `v<version>`, `sha` complet, version distribuée inférieure ou égale à celle
  de `main`, ligne présente dans le registre de `docs/publication.md`.
- `test_marketplace_distribue_la_racine_sans_copie` : Codex suit la même
  étiquette que Claude Code.
- `test_etiquette_designe_le_commit_epingle` : l'étiquette existe et désigne
  le commit épinglé. Obligatoire en CI (`CT_EXIGER_ETIQUETTE=1`, historique
  complet) : un épinglage vers une étiquette inexistante ne peut pas passer.

## Conséquences

- Le champ `version` de la marketplace Claude Code n'égale plus forcément
  celui des manifestes de `main` : il désigne la version distribuée.
- La création d'une étiquette est un acte de publication, distinct de la
  fusion. Elle se fait sur GitHub ou en ligne de commande par le propriétaire.
- Le catalogue reste lu sur `main` ; la source du plugin est épinglée à
  l'étiquette. Le gel 1.1.1 préserve une distribution existante non qualifiée,
  sans transformer la barrière rouge en validation de publication.
- Retour arrière : repointer vers l'étiquette précédente du registre.
- La CI découvre tous les tests avec `CT_SAUTER_BARRIERE=1` pour
  l'intégration ; seul `ReleaseGateTests` y est sauté. Le job de publication
  force `CT_SAUTER_BARRIERE=0` ; la découverte complète sans variable conserve
  aussi cette barrière. Aucun résultat d'intégration ne qualifie la publication.
