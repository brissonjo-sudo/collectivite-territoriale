# ADR 0041 — Nouveau H1 de la 1.5.3 : cycle groupé, même contrat v4

Date : 26 novembre 2026. Décisions de Jo : « Groupée » (dcp-fpt, drh-fpt 0.8.0 et
recherche-juridique 3.7.0 dans un même candidat), puis, pour la préparation du plugin,
« 1.5.3, nouveau H1 (Recommandé) » et « Reporter (Recommandé) » pour le 19e cas.
Préparation H1 ; aucun modèle, aucune campagne, aucun smoke ni aucune preuve dans ce
lot.

Cette décision complète l'[ADR 0039](0039-mesure-1-5-3-contrat-v4.md) sans la réécrire :
le mécanisme de mesure de la 1.5.3 est inchangé ; seul le commit candidat change.

## Contexte

Trois tentatives de campagne ont été consommées sur le H1 `c1659bf` (a, b, c), sans
mesure liée : `MEASUREMENT_153_V4` est resté `None` et la transition 0039 n'a jamais été
fermée. La tentative c a échoué sur le type de STOP du cas `plugin-dcp-acte-irreversible`,
corrigé en amont par DCP-fpt 0.2.1 puis 0.2.2 (ADR 0040). Le runtime du candidat change :
`c1659bf` ne le représente plus.

## Décision

1. **Version et branche.** Le candidat reste la 1.5.3, sur `prep/1-5-3` (PR 45). La 1.5.3
   n'a jamais été publiée et `c1659bf` n'est lié à aucune mesure. Le nouveau H1 est le
   commit de tête de `prep/1-5-3` qui contient ce lot ; il est relevé par le harnais au
   réarmement, comme pour les cycles précédents.
2. **Runtime du candidat**, par rapport à `c1659bf` :

| Skill | Avant | Après | Pin |
|---|---|---|---|
| dcp-fpt | 0.2.0 | 0.2.2 | `86d9896` (ADR 0040) |
| drh-fpt | 0.7.0 | 0.8.0 | `1880d02` (Drh-fpt#28) |
| recherche-juridique | 3.6.0 | 3.7.0 | `ce675c6` (étiquette `skill-v3.7.0`) |

   Pour drh-fpt, l'inventaire fermé de `overlays/drh-fpt.md` reçoit
   `references/carriere-paie/mobilite.md` et `references/references-verifiees.md`, et
   l'ancre devient `# Skill : drh-fpt (v0.8.0)`. Les autres surcharges ne changent pas ;
   leurs empreintes sont rechaînées par `rehash_overlays`.
3. **Contrat v4 à l'identique** : mêmes 18 cas, mêmes invariants, même empreinte
   `be70f64b…`. Le 19e cas `drh-detachement-pm-equivalence` est reporté : il exige un
   nouveau contrat de cycle et sa propre ADR. Ce contrat ne s'appellera pas « v5 », nom
   déjà porté par le profil `codex-copies-natives-mcp-v5` et par les preuves
   `2026-10-07-codex-natif-v5` de la 1.3.0.
4. **Même CLI, même mécanisme.** `CAMPAIGN_150_CLI`, `MEASUREMENT_153_V4`,
   `TRANSITION_153_V4`, `MIGRATION_153_V4`, `prepared_cycles["1.5.3-v4"]` et la
   transition 0039 sont repris tels quels. H2 et H3 suivent l'ADR 0039, sur le seul
   nouveau H1 mesuré.
5. **Aucun assouplissement.** Les entrées, preuves et transitions antérieures ne changent
   pas. `c1659bf` ne peut pas servir de H1 après ce lot : son runtime diffère du candidat.

## Points ouverts pour Jo

- **Budget** : campagne 18 cas (36 sessions) et smoke (2 sessions), à autoriser après
  pré-vol.
- **Serveur MCP** : relever le commit déployé de `droit-francais-skill` (au moins
  `ce675c6`) dans l'autorisation, et geler les fusions pendant la mesure.
- **Couverture** : les cas du plugin touchant DCP, la mobilité DRH et `search_texts` ne
  sont compatibles avec ce runtime que par lecture ; seule la campagne le confirmera.
- **Poussée, fusion et publication** restent des décisions de Jo.
