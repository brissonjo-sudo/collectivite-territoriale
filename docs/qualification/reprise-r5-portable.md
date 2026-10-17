# Outillage R5 récupérable — contrôles locaux sans inférence

Le [manifeste](../../scripts/r5-dependencies.json) fixe les modules publics au
commit #16 `b02dd247e328b4401cd82826a276d8fa1b31f1bb`. Aucun protocole ni état
R4/R5 n'est une dépendance à récupérer. Les copies de source sont des archives
de code public ; leur disponibilité ne qualifie ni leur exécution sur 1.3.0
ni le candidat. Voir l'[ADR 0011](../adr/0011-reprise-r5-portable.md).

## Récupérer seulement les sources

Depuis la racine du dépôt, choisir un dépôt local contenant le commit public
(un clone Git en lecture suffit), puis une destination extérieure à ce dépôt
et encore absente, dont le parent existe :

```text
python -B scripts/reprise_dev7.py recover --repository <depot-public-local> --folder <destination-neuve>
```

Ou fournir un bundle vérifié et son empreinte issue d'un manifeste de confiance :

```text
python -B scripts/reprise_dev7.py recover --bundle <bundle-public> --bundle-sha256 <sha256-manifeste> --folder <destination-neuve>
```

Les sept fichiers Python sont contrôlés avant écriture exclusive ; aucun fichier
d'état, profil, OAuth, gel, cache ou protocole n'est sélectionné. Le mode bundle
emploie un dépôt bare temporaire sans checkout. Aucune requête réseau ni import
du harnais n'est effectué par ces commandes.

## Contrôler un contrat nouveau

`check` exige `--contract`, son `--contract-sha256`, `--source-root`, le
`--candidate-commit` complet correspondant à HEAD propre, `--state-root`,
`--installed-path`, `--cli`, `--cli-sha256` et `--cli-version`. Aucun défaut
historique n'est proposé. Les deux chemins d'état désignent un état futur
encore absent ; cette vérification ne lit ni ne prépare un profil.
Le libellé de version CLI est déclaratif : les octets sont contrôlés, sans
exécuter le binaire. Une incohérence fait échouer le contrôle.

Le document JSON `r5-portable-contract-v1`, fourni explicitement et sans être
copié par le lanceur, porte :

- `identity` : `source_git_root`, `candidate_commit`, `candidate_tree`,
  `state_root`, `installed_path`, `cli`, `cli_sha256`, `cli_version` ;
- `public_tools_sha256` : chaque nom de module `.py` et son SHA-256 du manifeste ;
- `launcher_sha256` : empreinte du lanceur exécuté ;
- `permissions` : exactement `sandbox=read-only` et `approval_policy=never` ;
- `attempts_per_case=1`, `timeout_seconds_per_case=240`, `max_seconds=5700` ;
- `status=non_mesure`, `historical_scores_reused=false`, et les `cases` nouveaux.

Le contrat lie les paramètres et les outils ; `check` ne juge pas les cas et
ne les envoie nulle part. Aucun contrat réel n'est créé en L5 : seuls les tests
en construisent des exemples synthétiques temporaires. La planification pure
`r5_portable.plan` vérifie les mêmes propriétés sans écrire de destination.

## Limite de récupération native

Les sources historiques restent récupérables avec leurs validateurs stricts,
qui sont liés à dev.7/R3/R4. Ils ne sont pas importés pour `check` et ne sont
pas déclarés compatibles avec 1.3.0. `init`, `preflight`, `prepare`, `run-all`
et `export` sont refusés explicitement dans cette version du lanceur. Leur
portage est la question de cadre de l'ADR 0011 ; aucun ancien contrôle n'est
assoupli pour permettre ce lancement. Aucun ancien gel ou score n'est repris.
