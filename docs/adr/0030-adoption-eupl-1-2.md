# ADR 0030 : adoption de l'EUPL 1.2

Date : 2026-11-01. Décision de Jo (Jonathan BRISSON, @brissonjo-sudo), auteur
du plugin et de ses sept dépôts amont.

## Contexte

Le plugin et ses skills étaient diffusés sous CC-BY-SA-4.0. Creative Commons
déconseille ses licences pour le logiciel et les admet pour sa documentation
(FAQ officielle, question « Can I apply a Creative Commons license to
software? », https://creativecommons.org/faq/, consultée le 2026-11-01).

L'article D323-2-1 du code des relations entre le public et l'administration
(version en vigueur depuis le 4 décembre 2021, Légifrance, consulté le
2026-11-01) liste, en son II, les licences qu'une administration peut retenir
pour la réutilisation à titre gratuit d'un logiciel. La « European Union
Public License » y figure parmi les licences avec obligation de réciprocité ;
les licences Creative Commons n'y figurent pas.

## Décision

1. Code, skills, scripts, tests et manifestes : **EUPL-1.2**, à compter de la
   version 1.5.0 du plugin et des commits de licence des sept dépôts amont
   (Dpm-fpt, Drh-fpt, DPO-CT, DirFi-fpt, DCP-fpt, DSI-fpt,
   droit-francais-skill).
2. Documentation de `docs/` : reste sous **CC-BY-SA-4.0**.
3. Ponytail (`.agents/skills/ponytail/`) : garde sa licence **MIT** d'origine.
4. Les versions 1.4.0 et antérieures restent sous CC-BY-SA-4.0 : cette
   licence est irrévocable pour les copies déjà diffusées. Aucune réécriture
   de l'historique Git.
5. Textes officiels de la Commission européenne, jamais réécrits : anglais
   dans `LICENSE` et `LICENSES/EUPL-1.2.txt`, français dans `LICENCE.fr.txt`
   et `skills/*/LICENCE.fr.txt`. Toutes les versions
   linguistiques approuvées par la Commission ont la même valeur (article 13
   de la licence). Le texte français est conservé octet pour octet
   (`.gitattributes` : `-text -whitespace` sur ce seul fichier, décision de Jo
   du 2026-11-01).
6. Répartition déclarée dans `REUSE.toml`.

## Motifs

- Licence conçue pour le logiciel, ce que CC-BY-SA n'est pas.
- Licence listée par l'article D323-2-1 : une collectivité qui adapte le
  plugin peut rediffuser sa version sous une licence admise pour les
  administrations.
- Réciprocité maintenue, comme l'ancienne clause « partage dans les mêmes
  conditions » ; licence conçue pour le secteur public et disponible en
  version française officielle.

## Titularité des droits

Jo est l'unique contributeur des huit dépôts. Le plugin a été créé sur son
temps personnel, avec son matériel personnel et son compte GitHub personnel,
sans instruction de son employeur. Selon la déclaration de l'auteur, les
conditions de l'article L113-9 du code de la propriété intellectuelle
(dévolution à l'employeur des droits patrimoniaux sur les logiciels et leur
documentation créés par un employé dans l'exercice de ses fonctions ou
d'après les instructions de son employeur, applicable aussi aux agents des
collectivités publiques) ne sont donc pas réunies.

L'historique Git (annexe) montre plusieurs noms d'auteur. Jo a confirmé le
2026-11-01 que « Murukan » (même adresse brisson.jo@gmail.com) est l'une de ses
identités Git, et que Claude, Codex, Vibe Nuage Agent, github-actions et
dependabot sont des outils qu'il opère, sans droits de tiers.

## Épingles et comportement

Aucun comportement ne change : seuls les fichiers de licence diffèrent.

- Dpm, Drh, DPO, DirFi et DSI sont réépinglés sur le commit de licence
  fusionné dans leur `main` ; sur les chemins synchronisés, seuls `LICENSE`
  et `LICENCE.fr.txt` diffèrent des anciennes épingles.
- recherche-juridique (3.6.0) et dcp-fpt (0.1.4) : leur `main` contient des
  changements de comportement postérieurs aux épingles. Ils sont donc
  épinglés sur des commits dédiés, branches permanentes
  `licence/rj-3.6.0-eupl` (30c9c90, parent f3ddffb) et
  `licence/dcp-0.1.4-eupl` (7874c62, parent 414cd4e), qui n'ajoutent que les
  textes de licence.
- `upstream.json` copie `LICENSE` et `LICENCE.fr.txt` pour les sept skills.

## Qualification

La preuve 1.4.0 reste liée à ses épingles et n'est pas transférée. Le
manifeste passe en **candidat 1.5.0 non mesuré, non qualifié** ; les deux
catalogues restent sur 1.4.0. La licence EUPL n'atteint donc les utilisateurs
de la marketplace qu'après mesure et publication de la 1.5.0.

Ajustements faits pour le candidat, sans tolérance générale :

- référence DCP-014 (`scripts/dcp-protocol.json`, `scripts/dcp_reference.py`,
  `scripts/qualify_distribution.py`) : la preuve reste exigée au pin mesuré
  414cd4e ; seul le pin distribué 7874c62 est admis en plus, et
  `LICENCE.fr.txt` rejoint `LICENSE` hors mesure. La vérification octet par
  octet des 30 fichiers mesurés est inchangée ;
- tests : épingles DSI et DCP attendues, licence attendue des manifestes, copie
  historique DCP sans le texte français, deux tests du lanceur 1.4.0 fixés
  explicitement sur cette version.

Reste à trancher avant la mesure 1.5.0 : le contrat de cycle de cette version.
Sans contrat lié, le lanceur retombe aujourd'hui sur le cycle v2 de 1.3.0 ;
ce repli, antérieur au présent ADR, ne doit pas servir de mesure 1.5.0.

## Annexe : `git shortlog -sne --all`
### collectivite-territoriale (relevé du 2026-11-01)

```text
   124	Jo <brisson.jo@gmail.com>
    24	Murukan <brisson.jo@gmail.com>
     5	Claude <noreply@anthropic.com>
     3	Codex <codex@local.invalid>
     3	Jonathan Brisson <brisson.jo@gmail.com>
```

### Dpm-fpt (relevé du 2026-11-01)

```text
    82	Claude <noreply@anthropic.com>
    14	Murukan <brisson.jo@gmail.com>
    11	Jo <brisson.jo@gmail.com>
     1	Codex <codex@local.invalid>
```

### Drh-fpt (relevé du 2026-11-01)

```text
    29	Jonathan Brisson <brisson.jo@gmail.com>
    28	Jo <brisson.jo@gmail.com>
    25	Murukan <brisson.jo@gmail.com>
    16	brissonjo-sudo <brisson.jo@gmail.com>
     4	Claude <noreply@anthropic.com>
```

### DPO-CT (relevé du 2026-11-01)

```text
     5	Claude <noreply@anthropic.com>
     4	Murukan <brisson.jo@gmail.com>
     2	Jo <brisson.jo@gmail.com>
```

### DirFi-fpt (relevé du 2026-11-01)

```text
    25	Claude <noreply@anthropic.com>
     9	Murukan <brisson.jo@gmail.com>
     3	Jo <brisson.jo@gmail.com>
     2	Jonathan Brisson <brisson.jo@gmail.com>
```

### DCP-fpt (relevé du 2026-11-01)

```text
    26	Jo <brisson.jo@gmail.com>
    13	Claude <noreply@anthropic.com>
    12	Murukan <brisson.jo@gmail.com>
```

### DSI-fpt (relevé du 2026-11-01)

```text
    24	Jo <brisson.jo@gmail.com>
    13	Claude <noreply@anthropic.com>
    10	Murukan <brisson.jo@gmail.com>
     1	Codex <codex@local.invalid>
```

### droit-francais-skill (relevé du 2026-11-01)

```text
   306	github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
   135	Murukan <brisson.jo@gmail.com>
   134	Jo <brisson.jo@gmail.com>
    18	Jonathan Brisson <brisson.jo@gmail.com>
    12	dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
     8	Claude <noreply@anthropic.com>
     3	brissonjo-sudo <2.81237092e+08+brissonjo-sudo@users.noreply.github.com>
     2	Murukan <Murukan@users.noreply.github.com>
     1	Vibe Nuage Agent <vibe@mistral.ai>
     1	brissonjo-sudo <brisson.jo@users.noreply.github.com>
     1	brissonjo-sudo <brissonjo-sudo@users.noreply.github.com>
```
