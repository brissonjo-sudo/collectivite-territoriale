# ADR 0034 : mesure 1.5.1 sous contrat v4, même CLI que la 1.5.0

Date : 2026-11-08. Décisions de Jo : « 1.5.1 complète (Recommandé) », puis
« Go » pour l'étape 4 (préparation du cycle). Préparation H1 ; aucun modèle,
aucune campagne, aucun smoke ni aucune preuve dans ce lot.

## Contexte

La 1.5.1 est un candidat de patch : épingles de veille du 2026-11-03 (dpm-fpt,
dirfi-fpt, dpo-ct, dsi-fpt) et dcp-fpt 0.1.7 sur la référence DCP-017
([ADR 0033](0033-dcp-017-reference-autonome.md)). Aucun contrat de cycle n'était
lié à la 1.5.1 : le pré-vol à blanc (`run_codex_campaign.py --cycle-v4
--dry-run`) et le pin smoke de la version courante échouaient (« Contrat de
cycle v4 absent ou divergent »), la mesure 1.5.0 ne couvrant pas ce runtime.

## Décision

1. La 1.5.1 est mesurée avec le **contrat de cycle v4 à l'identique** :
   `scripts/cas-plugin-cycle-v4.json`, empreinte
   `be70f64b4650a72c15a33e477c81f84c61c602ceb22ad23cc1783c3412888f24`, mêmes
   18 cas, mêmes invariants. Ce fichier ne change pas.
2. **Même CLI que la 1.5.0** pour la campagne et le smoke : `CAMPAIGN_150_CLI`
   (`codex-cli 0.164.0-alpha.11.1`, copie figée du harnais). Entre les deux
   mesures, seul le runtime du candidat change.
3. Le mécanisme de l'[ADR 0031](0031-mesure-1-5-0-contrat-v4.md) est réutilisé
   tel quel ; seule une entrée de version est ajoutée :

| Version | Commit lié | Transition | CLI |
|---|---|---|---|
| 1.5.1 | `MEASUREMENT_151_V4` (`None` en H1) | `toolchain-transition-0034.json` | `CAMPAIGN_150_CLI` |

   - `scripts/cli_toolchains.py` : constantes `MEASUREMENT_151_V4`,
     `TRANSITION_151_V4`, `MIGRATION_151_V4`, `ADR_151_V4`, entrée `1.5.1` de
     `v4_measurements()` ; la 1.5.1 rejoint `SMOKE_FOLLOWS_MEASUREMENT`.
   - `scripts/measurement-cli.json` : `prepared_cycles["1.5.1-v4"]`, non lié.
   - `scripts/toolchain-transition-0034.json` : préparé non fermé.
4. Aucun assouplissement. Les entrées, preuves et transitions 1.3.0, 1.4.0 et
   1.5.0 ne changent pas. Le commit mesuré de la 1.5.0 est refusé comme H1 de la
   1.5.1, comme tout commit déjà lié à une autre mesure.

## H2 et H3

H2 (après la campagne, sur le seul H1 mesuré) ne modifie que les trois fichiers
de `MIGRATION_151_V4`, selon la règle de l'ADR 0031 : l'affectation
`MEASUREMENT_151_V4: str | None = None` reçoit le SHA H1 complet ;
`prepared_cycles["1.5.1-v4"].measurement_commit` et
`campaign_measurements[H1]` (CLI `CAMPAIGN_150_CLI`, empreinte v4) sont
renseignés ; la transition 0034 est fermée. H3 ne contient que la projection
publique de `tests/evidence/release-1.5.1.json` et ses pièces ; elle remplace
`tests/evidence/mesure-courante`. La preuve 1.5.0 reste vérifiable au commit de
sa publication.

## Tests

`tests/test_transition_151_v4.py` calque la contre-épreuve 1.5.0 et ajoute le
refus du commit mesuré de la 1.5.0 comme H1. Les tests de pin smoke
(`tests/test_cli_toolchains.py`) simulent la liaison de la version courante du
plugin, lue dans son manifeste comme le fait `phase_pin`.

## Points ouverts pour Jo

- **Budget** : campagne 18 cas (36 sessions) et smoke (2 sessions), à autoriser
  après pré-vol.
- **Poussée, fusion et publication** restent des décisions de Jo.
