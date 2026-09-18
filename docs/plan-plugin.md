> **Origine** : copie versionnée du fichier de plan de la session Claude Code
> (`/root/.claude/plans/planifie-l-audit-du-skill-swirling-alpaca.md`, non
> versionné par nature — stockage de session, perdu si le conteneur est
> recyclé). Committé ici tel quel le 2026-09-18 pour ne pas perdre la
> trace du plan qui gouverne la construction de ce plugin. Contient, dans
> l'ordre inverse : le plan du plugin `collectivite-territoriale` (Phases
> 0 à 4) suivi, pour mémoire, du plan clos de l'audit `dpm-fpt` (v1.0.3 →
> v1.0.5) qui l'a précédé et l'a rendu possible.

---

# Plan — Plugin `collectivite-territoriale`

## Étape déjà faite (pour mémoire)

**Phase 2 (`DPO-CT`) close** : créé par l'utilisateur, versé (commit
`f3406f4`), poussé sur `main`, état local propre.

## Étape immédiate (ce tour)

L'utilisateur a **déjà créé** `brissonjo-sudo/collectivite-territoriale`
sur GitHub (même contournement que pour `DPO-CT`, anticipé cette fois).
**`add_repo` déjà fait** (5 dépôts dans la session). Reste à cloner
(`git clone --depth 1 … /home/user/collectivite-territoriale`, un seul
appel inline, pas de sous-agent) puis `register_repo_root`.

**Ce que ça change** : plus besoin de `mcp__github__create_repository`
(qui échouerait de toute façon) pour ce dépôt. Ce que ça ne change pas :
les préalables de contenu. Le dépôt existe, mais son remplissage (Phase 3 :
`skills/`, `.mcp.json`, `upstream.json`, scripts de synchronisation) reste
subordonné à des travaux non faits :

| Préalable | État |
|---|---|
| Phase 0 — inventaire `DirFi-fpt` | non fait (dépôt pas encore attaché à la session) |
| Phase 1 — `dpm-fpt` v1.0.5 (pointeurs inter-dépôts + fond réservé) | non fait |
| Phase 2 — dépôt `DPO-CT` | ✅ fait |

**Action de ce tour** : attacher et cloner `collectivite-territoriale` dès
maintenant (coût nul, évite un aller-retour), sans y verser de contenu de
skill tant que les phases 0 et 1 ne sont pas closes — verser maintenant
obligerait à recopier `dpm-fpt` une seconde fois après son correctif v1.0.5.

1. `add_repo(owner="brissonjo-sudo", repo="collectivite-territoriale", access="push")`.
2. Cloner dans `/home/user/collectivite-territoriale`, `register_repo_root`.
3. Vérifier l'état (`git log`, `git status`) — probablement vide ou avec un
   README initial, comme pour `DPO-CT`.
4. **Ne rien y écrire d'autre ce tour.** Poser au dépôt, en tête de son
   propre `README.md` s'il est vide, une seule ligne de statut : « Dépôt créé,
   en attente des phases 0 et 1 avant remplissage (voir le plan d'audit
   `Dpm-fpt`) » — pour qu'un lecteur du dépôt ne le croie pas abandonné.
5. Enchaîner directement sur la **Phase 0** (`DirFi-fpt`), qui était la
   suite logique du plan avant cette interruption : `add_repo`, clone,
   inventaire en lecture seule (version, frontmatter, architecture, poids,
   CI, pointeurs inter-dépôts).

**Arrêt** : après l'inventaire de `DirFi-fpt` (Phase 0), pas d'enchaînement
automatique sur la Phase 1 (correctifs `dpm-fpt`) ni la Phase 3 (remplissage
du plugin) — ce sont des modifications de fond qui méritent un point d'étape.

---

## Phase 1 — État et suite (1a-1c faits et poussés, reste 1d)

**Fait, poussé sur `claude/audit-skill-dpm-x387zc`** (3 commits, `validate_repo.py`
vert à chaque étape) :

- `de11db5` — 15 pointeurs inter-dépôts neutralisés, `validate_repo.py`
  détecte désormais cette classe de défaut (testé positif/négatif).
- `3b87d77` — trois points de fond vérifiés à la source le 2026-09-17 et
  corrigés (C. route L. 413-1, CSI R. 511-1/CP R. 633-6, CGCT L. 5211-9-2
  I.A/I.B) ; §9 ajoutée à `references-verifiees.md`.
- `7c941b4` — version 1.0.4 → 1.0.5 dans `SKILL.md`, `README.md`,
  `vault/index-dpm-fpt.md`, les trois scripts ; `CHANGELOG.md` et
  `JOURNAL.md` à jour ; score marqué « en attente d'exécution ».

**Décision (2026-09-17)** : mesurer par un **partiel ciblé de 8 cas**, pas
une campagne complète — recommandé et retenu.

### 1d — Partiel clos (2026-09-18) — PHASE 1 TERMINÉE

**8/8 cas jugés** : 6 RÉUSSITE (12, 13, 14, 16, 27, 28), 1 DEMI-RÉUSSITE
(18), 1 ÉCHEC (20, non critique). **Zéro échec sur les six cas critiques —
seuil de release atteint.**

Reprise post-rate-limit (2026-09-18) en séquentiel strict (pas de nouvelle
confirmation de parallélisme demandée) : cas 20 (réponse + jugement ÉCHEC),
27 (réponse + jugement — voir incident méthodologique ci-dessous), 28
(réponse + jugement RÉUSSITE).

**Incident méthodologique détecté et corrigé en cours de mesure** : le
premier prompt du juge du cas 27 référençait explicitement le précédent de
sourcing du cas 20 (« sois particulièrement attentif... précédent : cas
20 »), ce qui a orienté ce juge vers un test de sourcing plus strict que le
texte du barème et produit un ÉCHEC à tort. Ce jugement a été détecté comme
contaminé, **écarté avant toute consignation**, et rejugé avec un prompt
neutre — RÉUSSITE confirmé. Le juge du cas 28 a ensuite reçu un rappel
explicite du test littéral du barème, sans référence à un cas antérieur.

**Documentation mise à jour et poussée** (commit `3dc8a71`) : `SKILL.md`,
`README.md`, `CHANGELOG.md`, `JOURNAL.md`, `tests/bareme-cas-de-test.md`,
`tests/runs/claude-v1.0.5-partiel/summary.json` (nouveau). Deux constats
non éliminatoires réservés à la v1.0.6 (hiérarchie des gabarits d'écrit au
cas 18 ; uniformisation de la discipline de citation au cas 20), non
appliqués à chaud.

**PR #9 fusionnée** (2026-09-18, commit de merge `1668c89`) dans `main`.
`main` porte désormais la v1.0.5. Désabonnement effectué, check-in
programmé annulé. `validate_repo.py` : 1032 contrôles OK.

**Phase 1 est close, y compris sa fusion dans `main`.** Prochaine étape du
plan global : **Phase 3** (remplissage du dépôt `collectivite-territoriale` :
`skills/`, `.mcp.json`, `upstream.json`, scripts de synchronisation, CI) —
plus aucun préalable ne la bloque côté `dpm-fpt`. Reste, avant de recopier
`DirFi-fpt` dans `upstream.json`, à corriger sa propre dérive `plugin.json`
1.0.0 vs `SKILL.md` 1.0.3 (constat de la Phase 0, non traité).

### 1d — Partiel ciblé : 8 cas (rappel du protocole)

| Cas | Rôle dans le partiel |
|---|---|
| 12, 13, 14, 18, 27, 28 | Les six cas critiques — non-régression obligatoire |
| 16-salubrite-rsd-brulage-depots | Teste directement le correctif CSI R. 511-1 / CP R. 633-6 |
| 20-transfert-epci-police-dechets | Teste directement le correctif CGCT L. 5211-9-2 (I.A/I.B) |

**Réserve assumée** : aucun cas de la suite ne porte sur le grand excès de
vitesse (L. 413-1) — lacune de couverture déjà connue de l'audit (« élargir
la suite avant `r5` »). Le partiel ne peut donc pas mesurer ce correctif ;
il reste vérifié à la source mais non éprouvé par un cas.

**Protocole** (allégé du protocole `r3`/`r4`, même discipline) :

1. `tests/runs/claude-v1.0.5-partiel/` — répertoire créé à la main (pas
   `eval_suite.py prepare`, qui prépare les 28 cas et dont `summarize`
   exige les 28 réponses/jugements — inadapté à un sous-ensemble). Contient
   un `prompt.md` par cas retenu (copié depuis `tests/cas-de-test.json`),
   un `manifest.json` (sha256 de `SKILL.md` à `HEAD`, liste des 8 cas,
   justification du choix), un `controle-protocole.md`.
2. **8 répondants** Claude Opus 5, contexte frais et isolé, `prompt.md`
   seul, skill lu depuis le dépôt à `HEAD` (commit `7c941b4`) ; sha256 de
   `SKILL.md` contrôlé dans chaque réponse.
3. **8 juges** Claude Opus 5, contexte isolé, `response.md` + `attendus[]`
   du cas + `tests/bareme-normatif.md` (ou son équivalent figé) →
   `judgment.json` `{verdict, notes}`.
4. Exécution **strictement séquentielle** (un agent, on attend son retour,
   on committe, on lance le suivant) — règle du 2026-09-17, jamais de
   lancement groupé.
5. Synthèse écrite à la main dans `tests/runs/claude-v1.0.5-partiel/summary.json`
   (même format que `summary.json` des campagnes complètes, `case_count: 8`)
   — pas via `eval_suite.py summarize`, indisponible pour un sous-ensemble.

**Seuil** : 0 échec sur les 8 cas, en particulier sur les 6 cas critiques
(aucune régression). Une demi-réussite ou un échec sur 16/20 rouvre le
correctif concerné, ne bloque pas nécessairement la version si le garde-fou
tient.

### Après le partiel

1. `tests/bareme-cas-de-test.md` — nouvelle ligne pour le partiel v1.0.5
   (préciser explicitement « partiel 8/28, non comparable à r1-r4 »).
2. `CHANGELOG.md`, `README.md`, `SKILL.md` — remplacer « en attente
   d'exécution » par le résultat.
3. `JOURNAL.md` — compléter l'entrée du 2026-09-17 avec le résultat.
4. `validate_repo.py` vert, commit, push sur la branche existante.
5. Ouvrir une PR `claude/audit-skill-dpm-x387zc` → `main` (la précédente,
   #8, est fusionnée) une fois le partiel consigné — pas avant, pour ne pas
   ouvrir une PR avec un score « en attente ».

---

## Phase 0 — Résultat de l'inventaire `DirFi-fpt` (fait)

**`DirFi-fpt` est le skill le plus mûr des quatre.** Il a déjà son propre
scaffolding de plugin (`.claude-plugin/plugin.json` + `marketplace.json` +
`skills/dirfi-fpt/SKILL.md` — adaptateur, même patron que `droit-francais`),
une CI qui tourne sur push/PR, et une campagne `r3` complète.

| Critère | État |
|---|---|
| Version `SKILL.md` | **1.0.3** |
| Version `plugin.json` / `marketplace.json` | **1.0.0** — **même dérive** que `droit-francais` (constat 2 du plan) |
| Frontmatter | `name` + `description` seuls, ~1150 caractères — compatible plugin et upload claude.ai |
| Taille runtime | `SKILL.md` 574 lignes (> 500, seul des 4 skills à dépasser le seuil recommandé) ; `references/` 524 Ko ; `objets/` 112 Ko |
| CI | `.github/workflows/validate.yml`, tourne `validate_repo.py` sur push/PR — la seule CI réelle des 4 skills |
| `validate_repo.py` | 1245 contrôles, **vert** ; ne vérifie **pas** les pointeurs inter-dépôts (même angle mort que `dpm-fpt`) |
| Pointeurs inter-dépôts (`Dpm-fpt/…`, `Drh-fpt/…`, etc.) | **aucun** — `grep` négatif |
| Cas de test | 28 cas, 3 campagnes (`r1` 1.0.0, `r2` 1.0.1, `r3` 1.0.3) |
| Score `r3` (mesure la v1.0.3) | **27 RÉUSSITE / 1 DEMI / 0 ÉCHEC**, achevée 2026-09-16 |
| Frontière déclarée | exclut `drh-fpt` (RH statutaire) et la commande publique ; garde-fous propres : gestion de fait, contrôle budgétaire |

**Décision (sortie de phase 0) : `DirFi-fpt` entre dans la v1 du plugin.**
Aucune réserve de maturité — au contraire, sa CI et son scaffolding de
plugin existant sont un modèle à suivre pour `dpm-fpt` et `dpo-ct`, pas une
raison d'attendre.

**Conséquence pour la Phase 3** : `DirFi-fpt` a déjà un plugin autonome
publiable. Le plugin `collectivite-territoriale` n'a donc pas besoin de
réinventer sa structure — il peut recopier le patron `skills/<nom>/SKILL.md`
(adaptateur) déjà validé par `DirFi-fpt` et `droit-francais`, plutôt que
d'en inventer une troisième variante.

**Nouveau point pour la Phase 3** : corriger aussi la dérive `plugin.json`
1.0.0 vs `SKILL.md` 1.0.3 de `DirFi-fpt` **avant** de le recopier dans
`upstream.json` — sans quoi le plugin `collectivite-territoriale` fige une
version fausse dès sa première mesure.

---

## Plan complet (pour mémoire, exécution différée)

### Contexte

**Objectif** : distribuer la famille de skills métier de la fonction publique
territoriale comme **un plugin Claude Code unique**, incluant `DirFi-fpt`.

Ce qui motive le plugin : un plugin peut embarquer un **`.mcp.json`**, pas un
skill. Aujourd'hui `dpm-fpt` exige de « vérifier toute règle de droit sur une
source officielle » et le serveur MCP Légifrance/Judilibre existe déjà
(`droit-francais-skill.onrender.com/mcp`) — mais les deux ne sont reliés que
par une phrase en prose (`SKILL.md` ligne 39, « dépendances recommandées »).
Le plugin transforme cette convention en câblage. C'est la **seule** chose
qu'un plugin fait et qu'un skill ne peut pas faire.

### Constats établis ce tour (lecture seule, première main)

**1. Aucun plugin n'est actif sur le compte.**
`/root/.claude/plugins/synced/<id>/` est **vide** ;
`/root/.claude/skills/synced/<id>/` contient **24 skills**. Le plugin
`droit-francais`, construit le 1ᵉʳ septembre et couvert par
`tests/check_plugin.py` en CI, **n'est pas installé**. Tout ce qui sert
aujourd'hui passe par la synchronisation de skills.

**2. La dérive de version est générale, pas limitée à `dpm-fpt`.**

| Skill | Synchronisé | Dépôt | Écart |
|---|---|---|---|
| `dpm-fpt` | 1.0.1 | 1.0.4 | **3 versions** |
| `recherche-juridique` | 3.3.0 | 3.5.0 | **2 versions** |
| `drh-fpt` | 0.5.1 | 0.5.1 | aligné |
| `dpo-ct` | 0.2.1 | *aucun dépôt* | — |
| `droit-francais` `plugin.json` | — | 0.8.3 | **numérotation tierce** |

Le `plugin.json` de `droit-francais` suit la version du serveur MCP, pas celle
du skill (3.5.0). Le piège que `check_plugin.py` documente est donc **déjà
réalisé** dans le seul plugin existant.

**3. `dpo-ct` est orphelin.** 236 Ko, `SKILL.md` + `references/` + `assets/`,
aucune mention de dépôt GitHub, absent des 26 dépôts du compte. La copie
synchronisée est sa **seule source**.

**4. `DirFi-fpt` n'est pas rattaché à la session.** Le dépôt existe
(public, `can_push`, dernier push 2026-09-16) mais l'accès GitHub le refuse :
le périmètre reste `droit-francais-skill`, `Dpm-fpt`, `Drh-fpt`. **Son contenu
est inconnu** — le plan ne peut pas le dimensionner avant la phase 0.

**5. Il n'existe aucun appel programmatique d'un skill vers un autre**
(documentation Claude Code). Grouper les skills garantit leur
**co-installation**, jamais leur co-activation : le routage reste porté par
les `description`. Corollaire : les 14 pointeurs `Drh-fpt/…` de `dpm-fpt` ne
seront pas « réparés » par le plugin — ils sont faux dans tous les modes.

**6. Les skills de plugin sont préfixés** (`collectivite-territoriale:dpm-fpt`)
et **coexistent** avec les skills synchronisés sans les écraser. Installer le
plugin *en plus* des skills synchronisés double le coût de contexte.

### Décisions prises avec l'utilisateur

1. **`dpo-ct`** : créer son dépôt **avant** de l'intégrer.
2. **Architecture** : un dépôt plugin qui **versionne des copies** des skills,
   avec un **contrôle CI** qui échoue si une copie diverge de son amont.

---

## Phase 0 — Débloquer et inventorier `DirFi-fpt`

Préalable à tout dimensionnement.

1. `add_repo(owner="brissonjo-sudo", repo="DirFi-fpt", access="push")`.
2. Cloner dans `/home/user/DirFi-fpt`, puis `register_repo_root`.
3. **Inventaire** : version, frontmatter (`name`/`description` seuls ?
   longueur), architecture en couches, poids runtime, CI, scripts de
   validation, suite de test, et **pointeurs inter-dépôts** (`Dpm-fpt/…`,
   `Drh-fpt/…`) — le défaut mesuré dans `dpm-fpt`.

**Sortie** : un tableau de maturité comparant les 4 skills, qui décide si
`DirFi-fpt` entre dans la v1 du plugin ou attend.

---

## Phase 1 — `dpm-fpt` v1.0.5 : pointeurs inter-dépôts et fond réservé

`main` porte la v1.0.4 depuis la fusion de la PR #8. La branche désignée
`claude/audit-skill-dpm-x387zc` est fusionnée : **la redémarrer depuis `main`**
(`git fetch origin main && git checkout -B claude/audit-skill-dpm-x387zc origin/main`).

### 1a. Neutraliser les 14 pointeurs

**Règle** : nommer le skill, jamais le fichier d'un autre dépôt.

| Cible actuelle | Occurrences | Fichiers |
|---|---|---|
| `Drh-fpt/references/carriere-paie.md` | 8 | `rh-specificites-pm.md`, `controle-legalite.md` |
| `Drh-fpt/assets/decision-modele.md` | 6 | 4 gabarits de `templates/`, `arrete-modele.md` ×3 |
| `droit-francais-skill/skill/references/format-citation.md` | 1 | `socle-sources-verification.md:231` |

Remplacement type : `Drh-fpt/references/carriere-paie.md`, §5.7 →
**« le skill `drh-fpt` (volet carrière et paie, ISFE) »**. La référence garde
son sens pour le modèle et cesse de désigner un chemin qui n'existe pas hors
environnement multi-dépôts.

### 1b. Rendre le défaut impossible à réintroduire

Étendre `scripts/validate_repo.py` : échec sur tout chemin de la forme
`<Dépôt>/…\.md` dans `SKILL.md`, `references/`, `objets/`. Le validateur ne
contrôle aujourd'hui que les liens **internes** — c'est pourquoi 14 pointeurs
morts ont traversé un audit complet.

### 1c. Traiter le fond déjà réservé

Le `CHANGELOG` réserve trois points à la v1.0.5 : C. route **L. 413-1** (grand
excès de vitesse constitutif d'un délit), articulation **CSI R. 511-1 / CP
R. 610-5 / CP R. 633-6**, distinctions de **transfert EPCI**. Vérification au
socle (identifiant + date) avant rédaction.

### 1d. Mesurer

Ces fichiers sont dans le runtime → le protocole impose une mesure. **Partiel
ciblé**, pas une campagne complète (`r4` a coûté ≈ 5,4 M tokens) : les cas qui
touchent la frontière RH, les gabarits et la vitesse. Seuil : aucun échec, et
aucune régression sur les six cas critiques.

---

## Phase 2 — Créer le dépôt `Dpo-ct`

Un skill RGPD sans source versionnée est un risque en soi : ni historique, ni
réversibilité, ni audit possible.

- **Source** : `/root/.claude/skills/synced/<id>/dpo-ct/` (seule source
  existante). Versement à l'identique, **sans retouche de fond**, en v0.2.1.
- **Gouvernance reprise de `Dpm-fpt`** : `README.md`, `CHANGELOG.md`
  (entrée initiale « versement de la copie déployée, contenu inchangé »),
  `JOURNAL.md`, `AGENTS.md`.
- **`scripts/validate_repo.py`** adapté : comptages, pointeurs internes, et
  d'emblée le contrôle de la phase 1b.
- **CI** minimale sur le modèle de `Drh-fpt/.github/workflows/`.
- **Hors périmètre** : aucun audit de fond de `dpo-ct` ici. Le dépôt rend le
  skill auditable ; l'audit est un chantier distinct.

---

## Phase 3 — Le dépôt plugin `collectivite-territoriale`

Nouveau dépôt public `brissonjo-sudo/collectivite-territoriale`.

```
collectivite-territoriale/
├── .claude-plugin/
│   ├── plugin.json          # name, version, description, license, repository
│   └── marketplace.json     # catalogue : 1 plugin, source "./"
├── skills/
│   ├── dpm-fpt/             # runtime recopié depuis Dpm-fpt
│   ├── drh-fpt/
│   ├── dpo-ct/
│   └── dirfi-fpt/           # sous réserve de la phase 0
├── .mcp.json                # serveur Légifrance/Judilibre
├── scripts/
│   ├── sync_skills.py       # recopie le runtime depuis chaque amont, à un ref figé
│   └── check_sync.py        # CI : échoue si une copie diverge de son ref
├── upstream.json            # dépôt + commit figé + version, par skill
├── .github/workflows/ci.yml
├── CHANGELOG.md
└── README.md
```

### Points de construction

- **`upstream.json` est la source de vérité des versions.** Chaque skill garde
  sa version dans son propre `SKILL.md` ; le plugin n'en fait pas de copie
  manuelle. C'est ce qui évite de reproduire l'écart `plugin.json` 0.8.3 vs
  skill 3.5.0 constaté sur `droit-francais`.
- **`check_sync.py` en CI** : compare chaque `skills/<nom>/` au commit figé de
  son amont et échoue à la moindre divergence. La duplication est assumée,
  mais vérifiée par machine — jamais par relecture.
- **Version du plugin** : `plugin.json` porte un `version` explicite. La doc
  est nette — l'auto-update est **désactivée par défaut** pour les marketplaces
  tierces, et un `version` figé n'est repris qu'après incrément. Le `README`
  doit donc documenter `/plugin update` ; sans quoi on réinstalle exactement
  la dérive constatée au constat 2.
- **Ne pas embarquer `recherche-juridique`** : il a son propre dépôt, son
  propre plugin et sa propre cadence (3.5.0). Le `.mcp.json` suffit à câbler
  l'outil ; dupliquer le skill créerait un cinquième front de dérive.
- **Frontmatter** : `dpm-fpt` n'a que `name` + `description` (993 caractères),
  donc compatible à la fois plugin et upload claude.ai — **aucun fork de
  `SKILL.md` n'est nécessaire**. À vérifier sur les trois autres en phase 0/2.

### Avertissement à porter dans le `README`

Le plugin est destiné à la **distribution vers d'autres collectivités**.
L'auteur, qui a déjà ces skills synchronisés sur son compte, ne doit **pas**
installer le plugin en plus : les deux jeux coexistent sous des préfixes
distincts et doublent le coût de contexte sans arbitrage.

---

## Phase 4 — Vérification de bout en bout

- `claude plugin validate ./ --strict` → aucune erreur, aucun avertissement.
- `claude --plugin-dir ./` en session jetable : les 4 skills apparaissent sous
  `collectivite-territoriale:<nom>`, le serveur MCP est déclaré.
- `python3 scripts/check_sync.py` → vert ; puis, après modification volontaire
  d'une copie, **rouge** (le contrôle prouve qu'il détecte).
- `grep -rE '\b(Dpm-fpt|Drh-fpt|Dpo-ct|DirFi-fpt|droit-francais-skill)/' skills/`
  → **aucun résultat** (aucun pointeur inter-dépôts n'a survécu au versement).
- Côté `Dpm-fpt` : `validate_repo.py` vert, partiel de la phase 1d sans échec.
- Une PR par dépôt touché, aucune fusion sans revue.

---

## Ce que ce plan ne fait pas

- **Aucun audit de fond** de `dpo-ct` ni de `DirFi-fpt`.
- **Aucune campagne complète** de type `r4`. Seul un partiel ciblé en phase 1d.
- **Aucune modification de `droit-francais-skill`**. Son plugin inutilisé et sa
  dérive 3.3.0 / 3.5.0 sont constatés, pas traités ici.
- **Aucune resynchronisation** des skills déployés : c'est une action côté
  compte claude.ai, hors d'atteinte depuis cette session.

## Risques assumés

| Risque | Traitement |
|---|---|
| `DirFi-fpt` trop immature pour la v1 | La phase 0 tranche ; le plugin sort à 3 skills si besoin |
| Duplication des runtimes dans le plugin | `check_sync.py` en CI, `upstream.json` figé |
| L'utilisateur n'installe jamais ce plugin, comme le précédent | Constat 1 posé d'emblée ; la question de l'usage réel prime sur la construction |
| Coût de la phase 1d | Partiel ciblé, jamais une campagne complète |

---

# Plan précédent (clos) — Audit du skill `dpm-fpt` (v1.0.3)

## Contexte

Le skill `dpm-fpt` (Directeur de Police Municipale) est en **v1.0.3** dans le dépôt, mais :

- `origin/main` est resté à **v1.0.0** (PR #7). Les 7 commits v1.0.1 → v1.0.3 vivent sur `claude/prompt-execution-planning-wzrg8w`, sans PR ouverte.
- Le skill Claude **déployé** (synced) est en **v1.0.1** : deux versions de retard sur le dépôt, dont le durcissement de la frontière RH (v1.0.2) et la jurisprudence au socle (v1.0.3).
- La v1.0.3 **n'a jamais été mesurée** : le CHANGELOG exige une campagne `r4`. Le score 26/28 porte sur la v1.0.2.
- Dernier audit complet : v0.8.3 (2026-07-01, 4 dimensions orchestrées). La « revue de rentrée » du 1er septembre prévue par `SKILL.md` §9 n'a pas d'entrée dédiée dans `JOURNAL.md`.
- `validate_repo.py` passe (641 contrôles OK) mais `package_skill.py` est resté en `VERSION="1.0.2"`.

**Objectif de l'audit** : produire un rapport d'audit daté et traçable, corriger ce qui est mécanique et ce qui manque au socle (→ v1.0.4), mesurer cette version par une campagne complète `r4`, et laisser le dépôt dans un état publiable (PR vers `main`). La resynchronisation du skill Claude déployé (v1.0.1) se fait côté utilisateur après fusion ; le plan la signale, il ne peut pas l'exécuter.

**Ordre d'exécution** : B et C en parallèle → E.1–E.3 (correctifs, v1.0.4) → D (`r4`) → E.4–E.7 (rapport, journal, PR).

**Ce que l'audit ne fait pas** : réécrire le fond métier, changer l'architecture 4 couches, modifier `tests/cas-de-test.json` (empreinte de suite figée, sinon `r4` ne se compare plus à `r3`).

---

## Rituel de parallélisation / modèle / isolation

Aucun « rituel » formalisé n'existe dans les 3 dépôts ni dans `/root/.claude` (le `AGENTS.md` du projet renvoie vers `C:\Users\Krn\Documents\ClaudeMemory\`, inaccessible ici). Je l'applique donc explicitement, phase par phase :

| Phase | Parallélisable ? | Modèle | Isolation |
|---|---|---|---|
| A. Contrôles mécaniques | oui (3 lots) | **Haiku** (grep/compte/diff) | lecture seule, contexte frais |
| B. Vérification de vigueur du socle | oui (1 agent par code : CGCT, CSI, CPP, route, CP, jurisprudence) | **Sonnet** + WebFetch Légifrance | lecture seule, pas de `tests/` en contexte |
| C. Audit méthodologique (4 dimensions, comme v0.8.3) | oui (4 agents) | **Sonnet** (sourcing, gabarits) / **Opus** (garde-fou APJA, frontière RH) | lecture seule, chacun ne voit que son périmètre |
| D. Campagne `r4` | oui (28 répondants puis 28 juges) | **Opus** répondant et juge (protocole `r3` reconduit) | **stricte** : répondant sans `tests/`, `JOURNAL`, `CHANGELOG`, `README`, `docs/` ; juge sans réponse des autres cas ni historique |
| E. Correctifs + rapport | non (séquentiel, moi) | Fable | branche `claude/audit-skill-dpm-x387zc` |

Règle de coût : un agent Haiku/Sonnet ne reçoit que les fichiers de son lot, jamais le dépôt entier. Les juges `r4` reçoivent `bareme-normatif.md` (figé, sans historique), pas `bareme-cas-de-test.md`.

---

## Livrables

1. `docs/audit/2026-09-audit-v1.0.3.md` — rapport d'audit (constats, verdicts ✅/🟡/❌ sur le modèle `Drh-fpt/SYNTHESE-CRITIQUES-v0.2.0.md`, plan P1/P2/P3).
2. `tests/runs/claude-v1.0.4-r4/` — campagne complète (prompt/response/judgment × 28, `manifest.json`, `suite.json`, `summary.json`, `controle-protocole.md`, `bareme-normatif.md`).
3. Correctifs mécaniques commités séparément (voir phase E).
4. Entrées `JOURNAL.md` (revue de rentrée + audit) et `CHANGELOG.md` (**v1.0.4** : correctifs de socle et de docs, puis section « Validé » avec le score `r4`).
5. `vault/index-dpm-fpt.md` mis à jour (nouveaux fichiers d'audit indexés). Graphify : introuvable dans l'environnement ; je le signale sans le mettre en place (voir « Questions ouvertes »).
6. PR `claude/audit-skill-dpm-x387zc` → `main` (fait passer `main` de v1.0.0 à v1.0.3+audit).

---

## Phases

### Phase A — Contrôles mécaniques (**déjà faits pendant la planification**)

Pointeurs, comptages, versions/dates, réserves résiduelles, gabarits, portabilité : tout est relevé dans « Constats préliminaires » ci-dessous. Il ne reste qu'à reporter ces constats dans le rapport et à les corriger en phase E. Un seul contrôle à rejouer en fin d'audit : `validate_repo.py` + `diff -rq --strip-trailing-cr` package vs dépôt.

### Phase B — Vérification de vigueur du socle (Sonnet ×6, parallèle, ~30 min)

Source : `references/references-verifiees.md` (§1–§7). Méthode : WebFetch `https://www.legifrance.gouv.fr/codes/article_lc/<LEGIARTI>` (accès confirmé en session), un agent par code. Pour chaque identifiant : état (en vigueur / modifié / abrogé), date de version, concordance avec la date consignée. Sortie : tableau par agent, consolidé dans le rapport. Tout écart → correctif dans le socle + branches concernées (phase E), avec nouvelle date de vérification `2026-09-XX`.

Contrainte : aucun identifiant n'est reconstitué de mémoire ; un identifiant non atteignable est marqué « non recontrôlé », pas « vérifié ».

Hors périmètre de cette phase : `liste-RSD.md` (96 URL préfectorales/ARS) — recontrôle par échantillon de 10, le reste signalé comme non recontrôlé.

### Phase C — Audit méthodologique 4 dimensions (parallèle, ~40 min)

Même découpage qu'en v0.8.3, pour comparabilité :

- C1. **Discipline de sourcing** (Sonnet) : articles cités avec numéro précis dans branches/objets/templates mais absents du socle ; cohérence des identifiants entre socle et branches (précédent : art. 537 CPP contradictoire en v0.8.3).
- C2. **Garde-fou APJA et frontières** (Opus) : le STOP, le routeur 53/73 → 78-6 → aucun fondement, le bloc BASCULE, sont-ils encodés sans contradiction dans les 4 couches (SKILL §5.2/§5.4, `analyse-situation.md`, `penal-procedure.md`, `rapport-mise-a-disposition.md`, `objets/agent.md`) ?
- C3. **Gabarits et duplication** (Sonnet) : contenu dupliqué entre branches et objets (principe « agréger et pointer ») ; sections hors gabarit.
- C4. **Tests et DoD** (Sonnet) : couverture des 28 cas vs branches et objets ; cas critiques ; `cas-co-activation.md` (5 cas jamais rejoués depuis v0.8.6 ?) ; cohérence `bareme-cas-de-test.md` ↔ `validate_repo.py`.

Complément propre à Claude : C5. **Déclenchement** — la `description` du frontmatter est-elle discriminante vis-à-vis de `drh-fpt` et `dpo-ct` ? Test léger avec 10 prompts (5 dans le périmètre, 5 limites) via le `skill-creator` synced (`run_eval.py`) si `claude -p` est disponible ; sinon revue manuelle et consignée comme non testée.

### Phase D — Campagne `r4` (mesure de la v1.0.4 = v1.0.3 + correctifs de socle de l'audit)

Protocole `r3` reconduit à l'identique (`tests/runs/claude-v1.0.2-r3/controle-protocole.md`), avec :

1. `python3 scripts/eval_suite.py prepare --run-dir tests/runs/claude-v1.0.4-r4 --responder "Claude Opus 5" --judge "Claude Opus 5"` (fige `suite.json`, empreinte attendue `8dbcf5e1…`).
2. Copier `bareme-normatif.md` et rédiger `controle-protocole.md` (skill lu depuis le dépôt à HEAD **après** les commits 1 à 3 de la phase E, sha256 de `SKILL.md` consigné).
3. 28 répondants Opus, contexte frais, `prompt.md` seul + skills `recherche-juridique` / `drh-fpt` invocables ; sha256 de `SKILL.md` contrôlé dans chaque réponse.
4. 28 juges Opus, contexte isolé, `response.md` + `attendus[]` + `bareme-normatif.md` → `judgment.json` `{verdict, notes}`.
5. `python3 scripts/eval_suite.py summarize --run-dir tests/runs/claude-v1.0.4-r4`.

Ordre : cas **15 et 21 d'abord** (cible du correctif v1.0.3), puis les 26 autres. Seuil : ≥ 25/28 RÉUSSITE et 0 ÉCHEC sur 12/13/14/18/27/28. Nouveauté : consigner tokens/durée par cas dans `manifest.json` (jamais fait, demandé par le protocole).

### Phase E — Correctifs et clôture (séquentiel)

Commits séparés, dans l'ordre :

1. `fix(build)`: `package_skill.py` VERSION → 1.0.3 ; `agents/openai.yaml` : ajouter un champ version (si le schéma Codex l'admet, sinon commentaire).
2. `fix(docs)`: `AGENTS.md` (chemins relatifs + note de portabilité) ; `JOURNAL.md` : clôturer les 2 entrées « à traiter » (2026-08-03, 2026-08-08) en « intégré (v1.0.2) » ; `objets/occupation-domaine-public.md` : fondre la 7e section numérotée dans les 6 du gabarit ; libellé `recherche-juridique` dans `socle-sources-verification.md:230`.
3. `fix(socle)`: porter au socle L. 2131-4 et L. 2212-3 CGCT, L. 512-2 CSI (après vérification WebFetch en phase B) ; lever les réserves périmées sur L. 130-4 code de la route et L. 3332-15 CSP ; écarts de vigueur (phase B) et références hors socle (C1). Ces fichiers sont dans le runtime → **v1.0.4**. Ordre imposé : ces correctifs sont commités **avant** `eval_suite.py prepare`, pour que `r4` mesure la v1.0.4 (sha256 de `SKILL.md` consigné). Un correctif runtime découvert **pendant** `r4` n'est pas appliqué à chaud : il va dans le rapport et dans une v1.0.5 mesurée par un partiel ultérieur.
4. `test`: versement de `tests/runs/claude-v1.0.3-r4/`.
5. `docs`: rapport d'audit, `JOURNAL.md` (2 entrées), `CHANGELOG.md`, `vault/index`, `README.md` (score).
6. `python3 scripts/validate_repo.py` vert avant chaque push ; `package_skill.py` lancé une fois pour vérifier l'archive (non versionnée, `dist/` ignoré).
7. Push `-u origin claude/audit-skill-dpm-x387zc`, PR vers `main`, abonnement PR.

---

## Constats préliminaires (déjà établis, à reporter dans le rapport)

- ❌ `package_skill.py` VERSION 1.0.2 vs dépôt 1.0.3.
- ❌ Skill synced v1.0.1 : 12 fichiers runtime diffèrent du dépôt hors fins de ligne (`SKILL.md`, `objets/commerce.md`, `manifestation.md`, `references/analyse-situation.md`, `armement-equipements.md`, `conformite-deontologie-donnees.md`, `controle-legalite.md`, `pouvoirs-police.md`, `references-verifiees.md`, `rh-specificites-pm.md`, `socle-sources-verification.md`, `templates/arrete-modele.md`).
- ❌ `main` à v1.0.0, 7 commits non fusionnés, aucune PR ouverte.
- 🟡 `AGENTS.md` : chemins absolus Windows non portables.
- 🟡 Aucun coût (tokens/durée) consigné dans les campagnes précédentes.
- 🟡 Légifrance direct en `curl` → 403 ; WebFetch fonctionne (vérifié sur `LEGIARTI000006417218`). Le serveur MCP `droit-francais-skill.onrender.com` répond mais exige un jeton OAuth absent de l'environnement.
- ✅ `validate_repo.py` : 641 contrôles OK.
- ✅ Protocole d'évaluation reproductible (`eval_suite.py prepare/summarize`), empreinte de suite stable depuis `r2`.

Cohérence interne (exploration exhaustive, faits vérifiés) :

- ✅ Versions et dates alignées à 1.0.3 / 2026-09-06 sur SKILL, README, CHANGELOG, vault, JOURNAL. Comptages exacts (14 fichiers de branches/postures, 8 objets, 5 générateurs, 28 cas). Aucun pointeur interne cassé.
- ❌ **3 articles cités avec numéro précis mais absents du socle** : CGCT L. 2131-4 (`controle-legalite.md:283,292`, `arrete-modele.md:420`), CGCT L. 2212-3 (`pouvoirs-police.md:159`, `objets/manifestation.md:107,200`), CSI L. 512-2 et s. (`rh-specificites-pm.md:186`). → phase B les vérifie, phase E les porte au socle.
- ❌ **2 réserves « à confirmer » périmées** : L. 130-4 code de la route (`ecrits-professionnels.md:356`) et CSP L. 3332-15 (`reglementation-appliquee.md:169`) sont déjà au socle. → lever la réserve avec la provenance.
- ✅ Pointeurs externes vérifiés : `Drh-fpt/assets/decision-modele.md` et `droit-francais-skill/skill/references/format-citation.md` existent tous deux dans les dépôts clonés. Seule remarque : le second est nommé par son dépôt, pas par le nom de skill `recherche-juridique` (harmonisation de libellé, P3).
- 🟡 **2 entrées JOURNAL « à traiter »** (2026-08-03 et 2026-08-08, campagne r2) jamais clôturées alors que la v1.0.2 les a traitées. → passer en « intégré (v1.0.2) ».
- 🟡 Écarts de gabarit : sections additives hors gabarit dans 2 branches et 5 objets ; `occupation-domaine-public.md` numérote une 7e section (gabarit : « exactement 6 »). Précédent v0.8.3 : écarts additifs acceptés ; seule la 7e section numérotée est à réaligner.
- 🟡 `agents/openai.yaml` ne porte ni version ni date (pas de contradiction, rupture de parallélisme).
- 🟡 Réserves résiduelles : 29 fichiers avec « à confirmer », 13 avec `[INCOMPLET]` (ce dernier est attendu : marqueur de brouillon des générateurs). Fichiers les plus chargés : `objets/police-chiens.md` (35), `conformite-deontologie-donnees.md` (32).
- ℹ️ Taille du runtime : ≈ 9 300 lignes / 76 000 mots (SKILL.md 434 lignes, sous la limite de 500 des Agent Skills). Fichiers les plus lourds : `police-chiens.md` (550 l.), `conformite-deontologie-donnees.md` (516 l.), `reglementation-appliquee.md` (495 l.). Pas d'action dans cet audit ; consigné pour une optimisation ultérieure.

---

## Vérification de bout en bout

- `python3 scripts/validate_repo.py` → `[OK]`, code 0.
- `python3 scripts/eval_suite.py summarize --run-dir tests/runs/claude-v1.0.4-r4` → `summary.json` avec 28 cas, empreinte `8dbcf5e1…`, verdicts valides.
- `python3 scripts/package_skill.py` → `dist/dpm-fpt-1.0.4.zip` contenant uniquement `SKILL.md`, `agents/openai.yaml`, `references/`, `objets/`.
- `diff -rq --strip-trailing-cr` entre le dépôt et le package extrait : aucun fichier runtime manquant.
- Le rapport d'audit cite, pour chaque constat, le fichier et la ligne ; chaque référence recontrôlée porte sa date.

---

## État au 2026-09-16 — campagne r4 à mi-parcours, bloquée par la limite de session

**14 cas sur 28 sont mesurés, tous en RÉUSSITE (14/14).**

| Cas | Réponse | Jugement |
|---|---|---|
| 01, 02, 03, 04, 05, 06, 12, 13, 14, 15, 18, 21, 27, 28 | ✅ | ✅ RÉUSSITE |
| 07, 08, 09, 10, 11, 16, 17, 19, 20, 22, 23, 24, 25, 26 | — | — |

Ce que ce demi-parcours établit déjà :

- **Les six cas critiques (12, 13, 14, 18, 27, 28) sont tous en RÉUSSITE** — la condition
  la plus dure du seuil de release est remplie.
- **Le cas 21 passe**, alors qu'il franchissait la frontière RH en `r2` et échouait au
  sourcing en `r3`. **Le cas 15 passe** aussi, alors qu'il échouait en `r3` sur la
  jurisprudence *Benjamin* hors socle : les deux échecs de `r3` sont corrigés.
- Le contrôle de version est conforme sur les 14 réponses (v1.0.4, sha256 `8a461746…`).
- Aucun jugement ne relève de référence citée de mémoire.

**Blocage** : la limite de session du compte est atteinte (réinitialisation annoncée à
20 h 30 UTC). Deux vagues d'agents ont échoué en `rate_limit` (HTTP 429). Aucun agent
Opus ne peut repartir avant la réinitialisation ; le protocole `r3` impose Opus pour les
répondants comme pour les juges.

**Décision (2026-09-16)** : attendre la réinitialisation et **terminer les 28 cas**, pour
un score de suite comparable à `r3`. Pas de bascule sur Sonnet, pas de clôture partielle.

## Régime d'exécution imposé (2026-09-17) — un seul sous-agent à la fois

Le forfait ne supporte pas le parallélisme : trois vagues successives (12, 12 puis 10
agents) ont chacune épuisé la limite avant d'aboutir. **Nouvelle règle : un agent, on
attend son retour, on commite, on lance le suivant.** Aucun lancement groupé.

**Avancement au 2026-09-17** : 17 réponses et 15 jugements sur 28. Tous les verdicts
rendus sont des RÉUSSITE (15/15), dont les six cas critiques.

Reste **24 exécutions séquentielles** :

| Lot | Cas |
|---|---|
| 11 réponses manquantes | 07, 11, 16, 17, 19, 20, 22, 23, 24, 25, 26 |
| 13 jugements manquants | 09, 10, puis les 11 ci-dessus |

Ordre : pour chaque cas sans réponse, lancer le répondant, committer, lancer son juge,
committer. Les jugements en retard (09, 10) passent en premier, ils sont moins coûteux.

**Puis, la campagne close** :

1. `python3 scripts/eval_suite.py summarize --run-dir tests/runs/claude-v1.0.4-r4`.
2. Consigner le coût dans `manifest.json` (champ `cost`), compléter `controle-protocole.md`
   (résultat du contrôle de version : 28/28 attendu).
3. Section §6 du rapport d'audit, entrée « Validé » du CHANGELOG, ligne du barème
   (`tests/bareme-cas-de-test.md`), score dans `README.md` et `SKILL.md`.
4. `validate_repo.py` vert, push, mise à jour de la description de la PR #8.

**Réserve honnête** : 24 exécutions séquentielles représentent plusieurs heures et
plusieurs fenêtres de forfait. La campagne avancera par paliers, en committant à chaque
étape pour qu'aucune interruption ne fasse perdre de travail.

## État au 2026-09-15 (reprise après limite de session)

Phases A, B, C et E.1–E.3 **terminées** : 5 commits poussés, PR #8 ouverte vers `main`
(mergeable, aucun CI configuré sur le dépôt, aucun commentaire), rapport d'audit versé,
v1.0.4 publiée sur la branche.

Phase D (campagne `r4`) **en cours**, interrompue par la limite de session Opus :

| État | Cas |
|---|---|
| Réponse + jugement RÉUSSITE | 02, 12, 13, 14, 18, 21, 27, 28 (8) |
| Réponse écrite, jugement à faire | 01, 03, 04, 05, 06, 15 (6) |
| Ni réponse ni jugement | 07, 08, 09, 10, 11, 16, 17, 19, 20, 22, 23, 24, 25, 26 (14) |

Les 14 réponses écrites portent toutes la ligne de contrôle attendue
(v1.0.4, sha256 `8a461746…`). Les 8 cas jugés incluent **les six cas critiques**
(12, 13, 14, 18, 27, 28) : tous en RÉUSSITE, et le cas 21, qui échouait en `r3`,
passe également.

**Reprise** : 6 juges (cas déjà répondus), puis 14 répondants et 14 juges, par
vagues de 6 à 8 agents pour rester sous la limite. Puis `summarize`, versement,
section §6 du rapport, CHANGELOG, JOURNAL, barème, push.

## Décisions prises avec l'utilisateur (2026-09-14)

1. **Campagne `r4` complète** : 28 cas, 28 répondants + 28 juges Opus, contextes isolés. Seule voie comparable à `r3`.
2. **Une PR unique** `claude/audit-skill-dpm-x387zc` → `main`, qui embarque v1.0.1 → v1.0.3 et l'audit.
3. **Graphify ignoré** pour cet audit ; le vault Obsidian est mis à jour. À traiter dans une session dédiée.
