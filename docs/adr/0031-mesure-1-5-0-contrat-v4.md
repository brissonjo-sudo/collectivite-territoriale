# ADR 0031 : mesure 1.5.0 sous contrat v4 et nouveau pin de CLI

Date : 2026-11-01. Décision de Jo, préparation H1 de la mesure 1.5.0. Aucun
modèle, aucune poussée, aucune fusion ni aucune preuve dans ce lot.

## Contexte

La 1.5.0 (ADR 0030) est un candidat non mesuré. Trois constats ont été faits
en lecture seule avant ce lot.

1. **Repli v2.** Aucun contrat de cycle n'était lié à la version 1.5.0. Un
   lancement sans commit lié passait `require_cycle_version`, qui ne gardait
   que 1.4.0, puis chargeait le contrat v2 (`CYCLE_CASES_FILE`) : une mesure
   1.5.0 aurait pu être lue sous le contrat de la 1.3.0.
2. **v4 réservé à la 1.4.0.** Le contrat v4 (ADR 0028) était refusé pour toute
   autre version (« Contrat de cycle v4 réservé à la mesure 1.4.0 »), et la
   liaison `MEASUREMENT_140_V4` ne connaissait qu'un seul commit.
3. **Binaire 0.163 disparu.** La CLI `codex-cli 0.163.0-alpha.10.2` épinglée
   pour la 1.4.0 n'existe plus sur le poste de mesure.

## Décision de Jo du 2026-11-01

1. La 1.5.0 est mesurée avec le **contrat de cycle v4 à l'identique** :
   `scripts/cas-plugin-cycle-v4.json`, empreinte
   `be70f64b4650a72c15a33e477c81f84c61c602ceb22ad23cc1783c3412888f24`, mêmes
   18 cas, mêmes invariants, `V4_PATH_CASES` et consignes web. Ce fichier ne
   change pas.
2. **Nouveau pin de CLI** pour la campagne et pour le smoke de la 1.5.0,
   `CAMPAIGN_150_CLI`, copie figée du harnais :
   - `codex.exe` : `codex-cli 0.164.0-alpha.11.1`,
     `1103e9e09c71fa2cd0afd6d8f3b9a2d63174fe8efd7cb5bd09f1cb14ef58a098` ;
   - `codex-code-mode-host.exe` :
     `2727abaa2b30eb4afbe64b1da51a26cb594dd18dda82c6292b5373b15a758257` ;
   - `codex-command-runner.exe` :
     `598fbfbad52ccd717b60aa94185541ccecf27e849349026f93884e9519f7ac61` ;
   - `codex-windows-sandbox-setup.exe` :
     `5765c3951b2c247611dec18176660bd3d2e81f20baba61096b454888ee821b2c`.
3. **Comparabilité.** Par rapport à la 1.4.0, seul le moteur change (CLI
   0.163 vers 0.164) en plus du runtime du candidat. La comparaison entre les
   deux mesures est limitée d'autant : un écart de résultat ne se rapporte pas
   à la seule différence de runtime.
4. Aucun assouplissement : aucune assertion retirée, aucun seuil baissé, aucun
   test historique affaibli. `CAMPAIGN_140_CLI`, les preuves, constantes et tests
   1.3.0 et 1.4.0 gardent leur comportement.

## Liaison version, commit et mesure v4

`scripts/cli_toolchains.py` porte désormais, pour chaque version v4, le
quintuplet (commit lié, manifeste de transition, ADR, périmètre de migration,
CLI), lu à l'appel par `v4_measurements()` :

| Version | Commit lié | Transition | CLI |
|---|---|---|---|
| 1.4.0 | `MEASUREMENT_140_V4` (`acfa12e`) | `toolchain-transition-0028.json` | `CAMPAIGN_140_CLI` |
| 1.5.0 | `MEASUREMENT_150_V4` (`None` en H1) | `toolchain-transition-0031.json` | `CAMPAIGN_150_CLI` |

- `measurement_contract` retrouve la version dont le commit lié égale le commit
  demandé, vérifie `prepared_cycles[version-v4]` et exige que l'entrée
  `campaign_measurements[commit]` soit exactement la CLI de cette version et
  l'empreinte v4. Deux versions liées au même commit sont refusées.
- `require_cycle_version(contract, version, commit)` n'accepte v4 que si la
  version figure dans `v4_measurements()` et si le commit égale le commit lié de
  cette version (« Contrat de cycle v4 réservé aux mesures liées 1.4.0 et 1.5.0 »).
  Tous les appelants passent le commit : `campaign_contract.py`,
  `qualify_distribution.py`, `assemble_release_evidence.py`, `human_resolution.py`.
- `prepared_cycle_v4(root, version)` lit `prepared_cycles[version + '-v4']`.
- Le smoke d'une mesure 1.5.0 liée est épinglé sur `CAMPAIGN_150_CLI`
  (`toolchains` et `phase_pin`) ; celui de la 1.4.0 reste `scripts/smoke-cli.json`.
- La transition H1 vers H2 est paramétrée par version
  (`transition_v4_files(root, measured, target, version)`). L'enveloppe
  `transition_140_v4_files` est conservée. Les commits déjà liés à une autre
  mesure (`MEASUREMENT_D`, `MEASUREMENT_140`, l'autre SHA v4) ne peuvent pas
  servir de H1.

## Fermeture du repli

`UNBOUND_HISTORICAL_VERSIONS = {1.1.0, 1.1.1, 1.2.0, 1.3.0}` est la liste
fermée des mesures sans contrat lié qui gardent leur lecture v1 (règle de
l'ADR 0025). Toute autre version sans commit lié à un contrat est refusée
(« Mesure <version> sans commit lié à un contrat de cycle »). Le message
historique de la 1.4.0 (« sans commit lié au contrat de cycle v3 ») est conservé.

Le qualificateur exige la projection publique pour toute version hors
`{1.1.0, 1.1.1, 1.2.0}` : 1.3.0 et 1.4.0 gardent leur condition historique,
toute version plus récente l'exige sans condition. Une 1.5.0 ou suivante ne
passe donc jamais sans projection.

## Préparation H1, puis H2 et H3

En H1, `MEASUREMENT_150_V4` vaut `None`, `prepared_cycles["1.5.0-v4"].measurement_commit`
vaut `null`, aucune entrée `campaign_measurements` n'existe pour la 1.5.0 et
`scripts/toolchain-transition-0031.json` est préparé non fermé. Aucune mesure
1.5.0 n'est recevable dans cet état.

H2 (après la campagne et le smoke, sur le seul H1 effectivement mesuré) ne
modifie que trois fichiers sous `scripts/` :

1. Dans `scripts/cli_toolchains.py`, remplacer uniquement la ligne
   `MEASUREMENT_150_V4: str | None = None` par
   `MEASUREMENT_150_V4: str | None = '<SHA H1 complet>'` (guillemets simples,
   UTF-8, LF). Tous les autres octets du fichier H1 sont conservés.
2. Dans `scripts/measurement-cli.json`, modifier seulement
   `prepared_cycles["1.5.0-v4"].measurement_commit` vers H1 et ajouter
   `campaign_measurements[H1]` avec `case_contract_sha256` = l'empreinte v4 et
   `campaign_cli` = l'objet complet `CAMPAIGN_150_CLI`. Ni `codex`, ni l'entrée
   `1.4.0-v4`, ni les mesures existantes ne changent.
3. Fermer `scripts/toolchain-transition-0031.json` : H1 dans `measurement_commit`,
   les SHA-256 des objets Git `H1:scripts/cli_toolchains.py` et
   `H1:scripts/measurement-cli.json` dans `source_files_sha256`, les SHA-256 des
   fichiers modifiés aux étapes 1 et 2 dans `target_files_sha256`.

Les trois contrats v2, v3 et v4 sont vérifiés depuis Git H1, le snapshot et le
checkout H2. Tout fichier supplémentaire, tout changement du lecteur autre que
l'affectation, tout changement du verrou autre que la liaison est refusé même
avec des empreintes recalculées.

H3 ne contient que la projection publique de la release `tests/evidence/release-1.5.0.json`
et ses pièces.

## Lanceurs

Le lanceur du dépôt (`run_codex_campaign.py --cycle-v4 --dry-run`) ne sert qu'au
pré-vol à blanc : il n'écrit rien et ne lance aucun processus. La mesure réelle
est faite par un harnais externe, comme pour la 1.4.0, avec la CLI figée
`harnais-mesure-150\cli\codex-cli-0.164.0-alpha.11.1\`. Le lanceur
`run_codex_smoke.py` et `measurement_common.py` ne sont pas modifiés.

## Ce qui ne change pas

`scripts/cas-plugin-cycle-v4.json` et son empreinte, v2 et v3, les cas, les seuils,
les transitions 0013, 0017, 0026 et 0028, `run_codex_campaign.py`,
`run_codex_smoke.py`, `measurement_common.py`, `public_projection.py`, les pins
`codex` et `smoke_cli`, et toutes les preuves de `tests/evidence/**`.

## Contre-épreuves

`tests/test_transition_150_v4.py` calque la transition 1.4.0 (fixture H1 non
probante) et ajoute : H1 égal au commit lié de la 1.4.0 refusé, modification de
l'entrée `1.4.0-v4` ou de `campaign_measurements[acfa12e]` refusée même avec
empreinte recalculée, modification de la ligne `MEASUREMENT_140_V4` refusée,
CLI d'une autre version refusée.
`tests/test_qualification_cycle_v4_150.py` couvre le cas positif 1.5.0 et les
refus : 1.5.0 avec le commit de la 1.4.0, 1.4.0 avec le commit de la 1.5.0,
commit inconnu, absence de projection, 1.6.0 non liée, repli sans v4 en
préparation, entrée `1.5.0-v4` altérée, CLI 0.163 présentée pour la 1.5.0.
Un test de cohérence du dépôt réel reste valable en H1, H2 et H3 sans jamais
affirmer que `MEASUREMENT_150_V4` vaut `None`.

## Points ouverts pour Jo

- **Budget** de la campagne et du smoke 1.5.0 (18 cas, 36 sessions en high).
- **Poussées** : ce lot est commité localement, non poussé ; la poussée et la
  fusion restent des décisions de Jo.
- **Publication** : catalogues et étiquette restent sur 1.4.0 jusqu'à la
  procédure de `docs/publication.md`.
- **H3 écrase `mesure-courante`** : la projection de la 1.5.0 remplace le
  dossier `tests/evidence/mesure-courante`. La preuve 1.4.0 reste vérifiable au
  commit `f2382f3` (et non plus sur la tête, dont l'outillage a changé).
- **Pin de smoke hors contexte de mesure** : `verify_package` (donc
  `run_codex_smoke.py`) et la branche smoke de `measurement_common.checked`
  résolvent encore le pin de smoke sans commit de mesure, donc sur
  `scripts/smoke-cli.json` (0.163). Le smoke réel de la 1.5.0 passe par le
  harnais externe ; l'assemblage de ses pièces en H3 demandera une décision
  distincte (changement minimal de `measurement_common.py` ou du lanceur). Le
  refus actuel est le comportement strict, jamais un assouplissement.
