# ADR 0036 : mesure 1.5.2 sous contrat v4, même CLI que la 1.5.0

Date : 2026-11-11. Décisions de Jo : « Cycle 1.5.2 », puis « DCP + drh +
recherche-juridique (Recommandé) » pour le périmètre, puis « H1 1.5.2 ».
Préparation H1 ; aucun modèle, aucune campagne, aucun smoke ni aucune preuve
dans ce lot.

## Contexte

La 1.5.2 est un candidat de patch : dcp-fpt 0.1.9 sur la référence DCP-019
([ADR 0035](0035-dcp-019-reference-autonome.md)), drh-fpt 0.7.0 au `6f5e906`
(décret n° 2026-705, veille du 2026-11-03) et recherche-juridique 3.6.0 au
`d8d49bd` (entrée amont « Non publié »). Aucun contrat de cycle n'était lié à
la 1.5.2 : le pin smoke de la version courante échouait (« Contrat de cycle v4
absent ou divergent »), la mesure 1.5.1 ne couvrant pas ce runtime.

## Décision

1. La 1.5.2 est mesurée avec le **contrat de cycle v4 à l'identique** :
   `scripts/cas-plugin-cycle-v4.json`, empreinte
   `be70f64b4650a72c15a33e477c81f84c61c602ceb22ad23cc1783c3412888f24`, mêmes
   18 cas, mêmes invariants. Ce fichier ne change pas.
2. **Même CLI que la 1.5.0 et la 1.5.1** pour la campagne et le smoke :
   `CAMPAIGN_150_CLI` (`codex-cli 0.164.0-alpha.11.1`, copie figée du harnais).
   Entre les mesures, seul le runtime du candidat change.
3. Le mécanisme des [ADR 0031](0031-mesure-1-5-0-contrat-v4.md) et
   [0034](0034-mesure-1-5-1-contrat-v4.md) est réutilisé tel quel ; seule une
   entrée de version est ajoutée :

| Version | Commit lié | Transition | CLI |
|---|---|---|---|
| 1.5.2 | `MEASUREMENT_152_V4` (`None` en H1) | `toolchain-transition-0036.json` | `CAMPAIGN_150_CLI` |

   - `scripts/cli_toolchains.py` : constantes `MEASUREMENT_152_V4`,
     `TRANSITION_152_V4`, `MIGRATION_152_V4`, `ADR_152_V4`, entrée `1.5.2` de
     `v4_measurements()` ; la 1.5.2 rejoint `SMOKE_FOLLOWS_MEASUREMENT`.
   - `scripts/measurement-cli.json` : `prepared_cycles["1.5.2-v4"]`, non lié.
   - `scripts/toolchain-transition-0036.json` : préparé non fermé.
4. Les manifestes `.claude-plugin/plugin.json` et `.codex-plugin/plugin.json`
   passent en 1.5.2 ; les catalogues restent sur 1.5.1.
5. Aucun assouplissement. Les entrées, preuves et transitions 1.3.0, 1.4.0,
   1.5.0 et 1.5.1 ne changent pas. Le commit mesuré de la 1.5.1 est refusé comme
   H1 de la 1.5.2, comme tout commit déjà lié à une autre mesure.

## H2 et H3

H2 (après la campagne, sur le seul H1 mesuré) ne modifie que les trois fichiers
de `MIGRATION_152_V4`, selon la règle de l'ADR 0031 : l'affectation
`MEASUREMENT_152_V4: str | None = None` reçoit le SHA H1 complet ;
`prepared_cycles["1.5.2-v4"].measurement_commit` et
`campaign_measurements[H1]` (CLI `CAMPAIGN_150_CLI`, empreinte v4) sont
renseignés ; la transition 0036 est fermée. H3 ne contient que la projection
publique de `tests/evidence/release-1.5.2.json` et ses pièces ; elle remplace
`tests/evidence/mesure-courante`. La preuve 1.5.1 reste vérifiable au commit de
sa publication (`793bd79`).

## Tests

`tests/test_transition_152_v4.py` calque la contre-épreuve 1.5.1 et ajoute le
refus du commit mesuré de la 1.5.1 comme H1. Les tests de pin smoke
(`tests/test_cli_toolchains.py`) simulent la liaison de la version courante du
plugin, lue dans son manifeste comme le fait `phase_pin`.

## Points ouverts pour Jo

- **Budget** : campagne 18 cas (36 sessions) et smoke (2 sessions), à autoriser
  après pré-vol.
- **Serveur MCP** : il se redéploie à chaque fusion sur `droit-francais-skill`.
  Le commit déployé doit figurer dans la provenance de la campagne, et les
  fusions sont gelées pendant la mesure.
- **Poussée, fusion et publication** restent des décisions de Jo.
