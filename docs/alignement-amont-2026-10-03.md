# Alignement des runtimes amont — 2026-10-03

Le candidat 1.1.1 corrige le retard DRH constaté dans la distribution 1.1.0.
Les dépôts GitHub ont été consultés le 3 octobre 2026. La copie installée de
la 1.1.0 correspondait à `main` du plugin (`9a86298`), sans différence de
contenu ; les différences de fins de ligne Windows étaient sans effet.

| Skill | Base 1.1.0 | Base 1.1.1 | Commit retenu depuis `main` |
|---|---|---|---|
| dpm-fpt | 1.0.5 | 1.0.5 | `1668c89798f1f50a829c0b94d3cf6bf33a3640fb` |
| drh-fpt | 0.5.1 | 0.6.0 | `f81c9b955f7ebb47df7e93bdc41ac743d85a2973` |
| dpo-ct | 0.2.1 | 0.2.1 | `f3406f412368199a33f47e7861eb450eab2b2cdb` |
| dirfi-fpt | 1.0.4 | 1.0.4 | `d970fe530d3f50f6b4c330e3cfb85db35b7126ab` |
| recherche-juridique | 3.5.0 | 3.5.0 | `e437d10a2d4bbf66ba7a9c1e9fb49e773166054e` |

DRH comporte dix fichiers d'exécution modifiés et un nouveau fichier,
`references/contrat-execution.md`. Les changements de commits DPO et DirFi
depuis leurs bases figées ne modifient aucun fichier sélectionné pour le
runtime : leurs bases restent donc inchangées. Les trois surcharges DPM,
DPO et recherche juridique restent déclarées et contrôlées par empreintes.

## Référence DPM

Le dépôt DPM a pour branche par défaut `claude/prompt-execution-planning-wzrg8w`
au commit `bcd488b`, dont le skill est en 1.0.3. La branche `main` est au
commit `1668c897`, avec le skill en 1.0.5 ; c'est la référence du plugin.
Le checkout local DPM contient du travail en cours sur la première branche.

Une mise en cohérence du paramètre GitHub vers `main` est à proposer au
propriétaire. Elle ne nécessite ni fusion ni réécriture des autres branches.
Le checkout local DPM et son travail en cours ne sont pas modifiés par le
candidat du plugin.

## Qualification

La synchronisation contrôlée aux blobs Git couvre les cinq skills et
136 fichiers. Les traces 1.1.0 sont conservées comme historique. Le statut
`tests/evidence/release-1.1.1.json` décrit un nouveau candidat non qualifié :
aucune campagne, validation humaine ou authentification actuelle ne lui
est attribuée par réemploi des anciennes preuves.

La publication reste bloquée. La fusion d'un changement, son installation,
les contrôles statiques et les essais comportementaux sont des étapes
distinctes.

## Contrôles locaux du candidat

- `scripts/check_sync.py` avec clonages temporaires des cinq dépôts GitHub :
  cinq skills conformes aux commits figés et aux surcharges déclarées.
- Tests unitaires : 28 réussites sur 29 ; seul
  `test_barriere_de_release_comportementale` échoue pour maintenir la
  publication bloquée jusqu'aux validations encore dues.
- Validateur Claude : marketplace et manifeste du plugin validés séparément.
- Contrôle de diff : aucune erreur d'espacement ; aucun pointeur Markdown
  vers un dépôt voisin dans les runtimes et aucun secret repéré par le
  contrôle ciblé des nouveaux contenus.
- Aucun résultat de CI GitHub ni essai comportemental du candidat 1.1.1
  n'est attribué à ces vérifications locales.
