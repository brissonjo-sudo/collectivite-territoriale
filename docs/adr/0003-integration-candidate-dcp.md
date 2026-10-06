# ADR 0003 — Intégration candidate de la commande publique

- Date : 2026-10-06
- Statut : accepté pour préparer le candidat ; qualification non acquise
- Autorisation : l'utilisateur demande de poursuivre l'intégration et diffère
  la relecture praticien à après cette intégration.

## Décision

Ajouter `dcp-fpt` 0.1.0 comme sixième skill du plugin, cinquième expertise
métier. Figer le commit amont de fusion de la PR #4
`eeb1cb14a3ad94d78631661dce5ae11f1e071308` dans `upstream.json` et utiliser
le synchroniseur existant. La version du plugin devient le candidat 1.2.0.

Copier le point d'entrée, `agents/openai.yaml`, les références et objets du
paquet amont, avec la licence. Exclure le cache de valeurs, les scripts,
tests, documents de conception et notes de maintenance. Aucun contenu DCP
n'est modifié localement ; les cinq bases existantes et leurs trois
surcharges restent figées. Le MCP `droit-francais` reste unique et inchangé.

## Frontières et accès aux sources

DCP conduit le volet achat, les autres skills conservent leur périmètre.
Les blocs BASCULE et STOP restent ceux de l'amont. Une compétence déléguée
ne poursuit que si elle est effectivement chargée. `dsi-fpt` n'est pas
embarqué : son absence ne permet ni une fausse activation ni une réponse
technique produite par DCP.

Le registre DCP est daté ; sa copie ne constitue aucune nouvelle lecture
officielle ni attestation de vigueur. Le plugin dispose du MCP juridique,
dont l'accès doit être qualifié avant campagne. Le lanceur autonome DCP
sans MCP représente un profil distinct et ne qualifie pas implicitement
ce plugin.

## Ordre et conséquences

Préparer l'intégration candidate, effectuer les mesures et essais du runtime
intégré, puis obtenir la relecture praticien avant qualification et
publication. DCP conserve la mention « non mesuré, non relu par un praticien »
tant que les deux étapes ne sont pas acquises.

Ajouter cinq scénarios DCP au contrat du plugin, sans les exécuter dans ce
lot. Ils complètent les essais de coactivation ; ils ne remplacent pas la
suite métier amont. Une preuve dédiée 1.2.0 conserve `release_ready=false`
et les prérequis ouverts. Les anciennes traces restent historiques.

La CI distingue intégration technique et qualification de publication dans
deux jobs. Le test de publication reste identique, dans `ReleaseGateTests`,
et reste inclus dans la découverte complète. Le job candidat sélectionne
les trois classes de contrôles techniques ; toute nouvelle classe technique
devra être ajoutée à cette sélection. Aucun passage au vert n'est attribué
à la publication avant mesure, smoke et relecture.

L'intégration candidate sur une branche ne met pas à jour les installations.
La marketplace suivant `main`, une fusion distribuerait le candidat : cette
fusion et la publication restent des décisions distinctes, sans automatisme.

## Sort du candidat 1.1.1

Décision du propriétaire du 2026-10-06 : le candidat 1.1.1 est **abandonné**
et ne sera jamais publié. Il n'avait pas été qualifié. Ses changements
(`drh-fpt` 0.6.0) sont repris tels quels dans le candidat 1.2.0, dont la
qualification couvre donc deux évolutions : DCP et l'alignement DRH. La
campagne 1.2.0 porte sur les neuf scénarios, y compris ceux qui mobilisent
`drh-fpt`. `tests/evidence/release-1.1.1.json` est conservé comme trace
historique et marqué supplanté par 1.2.0.
