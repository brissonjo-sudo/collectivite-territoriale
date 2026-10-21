# ADR 0024 — Lier la distribution à l'outillage et aux CLI du smoke

Date : 2026-10-21. Statut : retenu pour le candidat 1.4.0, lot B1.

## Contexte et autorisation

Le brief B1 et le plan de phase B 1.4.0 autorisent le renforcement local du
qualificateur, sans action externe et sans assouplissement. L'assembleur
comparait déjà l'identité complète du candidat au smoke ; le qualificateur
de distribution contrôlait runtime, configuration et lanceur de campagne,
mais pas tout l'inventaire ni les reçus CLI du smoke.

Sources techniques consultées : `scripts/assemble_release_evidence.py`
(`assemble`), `scripts/measurement_common.py` (`snapshot`),
`scripts/cli_toolchains.py` (`prove_toolchains`, `compatibility_files`),
`scripts/human_resolution.py` (`compatible`), `scripts/public_projection.py`
(`ProjectionView`, `verify_ci`) et `.github/workflows/ci.yml`.

## Décision

Le qualificateur utilise `snapshot()` pour recalculer `case_file_sha256`,
`upstream_sha256` et l'inventaire `toolchain_sha256`. Il compare l'union des
chemins mesurés et courants afin de refuser aussi un ajout ou une omission.
Le jeu `permitted` reprend exactement celui de `compatible()` : assembleur,
résolution humaine, puis seuls fichiers autorisés par `compatibility_files()`.
Aucune nouvelle transition ni exception générale de version n'est introduite.
Un changement ultérieur du qualificateur ne peut donc pas réutiliser un ancien
smoke sans une transition fermée déjà applicable.

Les CLI déclarées par la release doivent correspondre aux verrous, et la
déclaration `smoke_cli` du smoke doit être identique. Le commit de mesure est
lu dans l'index humain lié, comme pour la sélection du contrat de cas.
`prove_toolchains()` revérifie tous les reçus de campagne, de relecture et les
deux reçus de smoke ; les liens de ces derniers sont contrôlés avant lecture.
Dans la vue CI, `ProjectionView.bound()` conserve le sens des empreintes
sources. Les scripts restent des fichiers publics ordinaires accessibles
depuis la racine de la projection ; aucune pièce privée n'est nécessaire.

Le staging de l'assembleur copie tous les chemins de l'inventaire calculé,
afin que son propre passage dans le qualificateur voie les mêmes scripts.

## Tests et conséquences

Les contre-épreuves B1 couvrent chaque nouveau champ divergent ou manquant,
les inventaires ajoutés/incomplets, les reçus altérés ou d'une autre phase,
un contrat conforme, la vue CI et une transition fermée existante, avec refus
d'une dérive supplémentaire. Les tests de transition utilisent les blobs Git
de la tête réellement mesurée par la preuve 1.3.0 : les empreintes approuvées
ne suivent jamais les modifications de développement.

Les anciennes contre-épreuves gardent leurs assertions. Leurs copies
temporaires sont enrichies de champs et reçus explicitement synthétiques
(`test_only_synthetic_fixture`, `release_evidence: false`), sans modifier les
preuves historiques versionnées ni présenter ces fixtures comme des mesures.
Les suites sont exécutées en cp1252 puis UTF-8 avec `CT_SAUTER_BARRIERE=1` ;
la barrière est exécutée séparément avec `CT_SAUTER_BARRIERE=0`, comme en CI.

La preuve 1.3.0 présente sur la base `11ecfcf` est acceptée avant B1. Avec le
qualificateur renforcé et l'outillage B1, elle est refusée. Elle n'est ni
réécrite ni exemptée : la barrière de release de la branche reste rouge
jusqu'à l'assemblage 1.4.0. La nouvelle règle n'entrera sur `main` qu'avec la
release 1.4.0, sur décision de Jo. Les tests locaux ne valent ni CI distante,
ni campagne, smoke réel, relecture humaine ou qualification juridique.
