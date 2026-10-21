# ADR 0026 — Transition fermée de liaison 1.4.0

Date : 2026-10-21. Décision de Jo, lot B5 : ajouter avant le gel la branche
fermée nécessaire au refus R2 du pré-vol B4. Les transitions historiques et
leurs manifestes restent inchangés. Aucun modèle ni aucune poussée dans B5.

## Séquence et fermeture

H1 est la tête propre de la campagne, runtime et contrat v3 définitifs.
Le lanceur externe préparé épingle v3 et la CLI 0.163.0-alpha.10.2 avec ses
trois compagnons, avant tout modèle. Il ne dépend pas d'une liaison à son
propre SHA dans le dépôt. Après la campagne, H2 ne fait que lier le H1 mesuré.
Le smoke futur porte H2 ; H3 ne contient que la projection publique de release.

Le fichier `scripts/toolchain-transition-0026.json` est préparé non fermé :
`measurement_commit` et les quatre empreintes source/cible restent `null`.
`MEASUREMENT_140` et la liaison dans `measurement-cli.json` restent également
`None` / `null`. Aucune mesure 1.4.0 n'est recevable dans cet état. Un champ
de preuve, une version ou HEAD ne sélectionne jamais une nouvelle mesure.

La branche est sélectionnée uniquement par l'égalité du commit source lié
avec le seul `MEASUREMENT_140` explicitement inscrit en H2. Son manifeste doit
être fermé sur ce SHA complet, l'ADR 0026, le contrat v3 et l'identité CLI exacte
déjà fixés en B5. Les compagnons ne peuvent être omis ni remplacés.

Le périmètre autorisé est exactement :

- `scripts/cli_toolchains.py` ;
- `scripts/measurement-cli.json` ;
- `scripts/toolchain-transition-0026.json`.

Aucun changement de CHANGELOG n'est nécessaire en H2 : la documentation est
préparée avant H1. Les inventaires source/cible du manifeste contiennent les
deux premiers chemins seulement. Le manifeste n'inscrit pas son propre hash,
qui est contrôlé par le snapshot cible ; son état non fermé de H1 est relu
dans l'objet Git H1 et comparé au snapshot source.

Les empreintes des deux autres sources sont également recalculées depuis
les objets Git du H1 explicitement autorisé, puis comparées au snapshot et au
manifeste. Les cibles sont comparées au snapshot et aux octets du checkout.
Tout fichier d'outillage supplémentaire est refusé, y compris les exceptions
générales d'assemblage. Quand le SHA cible est présent, tout autre fichier
du diff Git H1→cible est refusé. L'ascendance reste vérifiée par le lecteur humain.
Les fichiers v2 et v3 doivent garder leurs empreintes exactes en H1 et en H2.

La fermeture limite aussi le contenu des deux fichiers modifiés : le lecteur
doit rester identique à H1 sauf l'affectation littérale de `MEASUREMENT_140` ;
le verrou doit rester identique comme objet JSON sauf l'entrée de mesure H1
et la liaison du cycle préparé. Même des empreintes cibles recalculées ne
permettent donc pas de modifier un validateur ou un pin historique en H2.

## Procédure exacte du lot H2 — après la campagne

1. Lire le SHA complet H1 de la campagne effectivement exécutée, vérifier sa
   tête propre et ses pièces liées. Ne pas inventer une identité provisoire.
2. Dans `scripts/cli_toolchains.py`, remplacer uniquement la ligne
   `MEASUREMENT_140: str | None = None` par
   `MEASUREMENT_140: str | None = '<SHA H1 complet>'`, avec ces quotes simples.
   Conserver tous les autres octets du fichier H1, en UTF-8/LF.
3. Dans `scripts/measurement-cli.json`, modifier seulement
   `prepared_cycles["1.4.0"].measurement_commit` vers H1 et ajouter
   `campaign_measurements[H1]` avec les deux clés exactes :
   `case_contract_sha256` =
   `deb0d39efc93a24b16444922dbafddbb6570801a67e21ca23d612343ba471e89`
   et `campaign_cli` = l'objet complet `CAMPAIGN_140_CLI` de B5, également
   présent dans le manifeste préparé. Ne toucher ni au pin historique
   `codex`, ni aux mesures historiques, ni aux autres données JSON.
4. Fermer `scripts/toolchain-transition-0026.json` : écrire H1 dans
   `measurement_commit`, les SHA-256 des objets Git
   `H1:scripts/cli_toolchains.py` et `H1:scripts/measurement-cli.json` dans
   `source_files_sha256`, puis les SHA-256 des fichiers modifiés en étapes
   2 et 3 dans `target_files_sha256`. Conserver ADR, v3 et CLI/compagnons
   exactement comme dans le manifeste non fermé de H1. Aucune autre clé.
5. Contrôler les trois chemins du diff, `git diff --check`, les contre-épreuves
   et les suites cp1252 puis UTF-8 hors barrière. Commit local H2 des seuls
   trois fichiers. Vérifier le manifeste fermé contre H1 et H2 propres.
   Régénérer les empreintes du lanceur de smoke pour H2 et refaire son dry-run.

Rien d'autre ne change dans ce lot H2 : ni tests, ni seuils, ni skills, ni cas,
ni assembleur, ni avis humains, ni CHANGELOG. Tout défaut supplémentaire
renvoie au pré-vol et à une décision distincte. Le smoke, les authentifications,
la campagne, la publication et les poussées exigent toujours leurs accords.

## Contre-épreuves

Les fixtures portent explicitement `release_evidence: false` et créent leurs
propres commits Git locaux. Le cas conforme vérifie aussi le lecteur humain.
Les refus couvrent le manifeste non fermé, un chemin supplémentaire, les SHA
source/cible ou H1 divergents, v2/v3 altérés, une CLI ou un compagnon divergent,
un lecteur modifié au-delà du SHA et un pin historique changé malgré des
empreintes recalculées. Les suites historiques restent exécutées sans changement.

Le pré-vol B4 est rejoué sur la nouvelle tête dans une copie distincte, avec
les mêmes écarts non probants de campagne d/smoke f, invariant et anciennes
lectures/activations. Le manifeste n'est fermé que dans cette copie, sur son
SHA H1 de diagnostic. Aucun résultat 1.4.0 réel n'est fabriqué dans le candidat.
