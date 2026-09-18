# Générateur interactif — Rapport d'orientation budgétaire (v1.0.0)

> Couche 4 (`references/templates/`), piloté par `references/ecrits-financiers.md`
> et par `SKILL.md` §6. Mécanique de dialogue alignée sur les générateurs du
> skill frère `Dpm-fpt` (questions posées **une à une**, aucune donnée
> inventée, règle `[INCOMPLET]` stricte, checklist finale). Le contenu
> métier est propre aux finances locales.
>
> **Nature de l'écrit** : le rapport d'orientation budgétaire (ROB) est un
> document **préalable** au débat d'orientation budgétaire (DOB). Il n'est
> **pas lui-même une décision** : il n'a pas à être voté au fond, mais sa
> **présentation** est une formalité substantielle du cycle budgétaire dont
> l'omission fragilise le budget primitif voté ensuite. Branches de
> rattachement : `../budget-cycle.md` (fond du DOB/ROB), `../prospective-analyse.md`
> (contenu prospectif et ratios), `../dette-tresorerie.md` (volet dette).
>
> **Ce fichier ne tranche jamais seul** si l'obligation de ROB s'applique à
> la collectivité concernée, ni le contenu minimal exigé selon sa strate :
> ce point est une variable à lever en premier (§1 étape 2).

---

## 0. Quand utiliser ce générateur

Le ROB sert à **informer** l'assemblée avant le débat d'orientation
budgétaire : contexte financier, grandes orientations, structure de la
dette, perspectives pluriannuelles. Il précède le vote du budget primitif.

**Avant d'ouvrir ce générateur**, vérifier que l'écrit demandé est bien un
ROB et non un autre document :

1. **S'agit-il de décider un dispositif budgétaire précis (vote de crédits,
   affectation, garantie) ?** Oui → `deliberation-budgetaire.md`, pas ce
   générateur — le ROB n'a pas de dispositif décisionnel chiffré au sens
   d'un vote de crédits.
2. **S'agit-il de chiffrer l'impact d'un projet précis pour une décision
   ponctuelle ?** Oui → `note-impact-financier.md`, pas ce générateur — le
   ROB porte sur l'ensemble de la politique budgétaire de l'exercice, pas sur
   un projet isolé.
3. **La question porte-t-elle sur le contenu individuel du régime
   indemnitaire ou sur une mesure statutaire précise ?** Oui → n'aborder ici
   que l'**enveloppe** ; émettre le bloc **BASCULE `drh-fpt`** (§5, `SKILL.md`
   §5.5) dès que la discussion dépasse l'enveloppe.

Si aucun de ces cas ne redirige ailleurs : le **ROB** est le bon écrit.
Poursuivre au §1.

---

## 1. Séquence interactive obligatoire

**Principe directeur** (`SKILL.md` §6) : questions posées **une à une**,
jamais en bloc. Confirmer chaque réponse avant de passer au champ suivant.
Ne jamais pré-remplir un champ non fourni : appliquer la règle `[INCOMPLET]`
(§4).

### Étape 1 — Exercice concerné
- Q1 : « Pour quel exercice budgétaire ce rapport est-il préparé ? »
- Pourquoi : toute donnée macroéconomique, tout taux ou seuil cité doit être
  rattaché à une date de référence précise (`SKILL.md` §5.4 point 3) — un ROB
  ne se rédige jamais « pour l'exercice courant » par défaut.

### Étape 2 — Strate de la collectivité et obligation de ROB
- Q2 : « Quelle est la catégorie et la taille de la collectivité (commune,
  EPCI, département, région — et, si pertinent, la population ou le seuil
  d'effectifs) ? »
- Pourquoi : **l'obligation de tenir un DOB avec rapport, et le contenu
  minimal exigé, varient selon la strate** — ce point n'est **jamais**
  présumé. Si la strate ou le seuil applicable ne sont pas connus avec
  certitude, marquer `[INCOMPLET — préciser : strate exacte / seuil
  applicable — à vérifier avant de fixer le contenu minimal du rapport]` et
  renvoyer à vérification avant de fixer la structure définitive du document.

### Étape 3 — Contexte macroéconomique et loi de finances
- Q3 : « Quels éléments de contexte macroéconomique et de loi de finances de
  l'année souhaitez-vous faire figurer (évolutions de la fiscalité locale,
  des dotations, des concours de l'État) ? »
- Pourquoi : ces éléments sont des valeurs volatiles (`SKILL.md` §5.4
  point 2) — jamais citées de mémoire, toujours datées. Renvoi
  `../dotations-perequation.md` et `../fiscalite-locale.md` pour le fond.

### Étape 4 — Rétrospective
- Q4 : « Sur quelle période souhaitez-vous présenter la rétrospective
  (évolution des principaux agrégats : recettes, dépenses, épargne,
  encours de dette) ? Disposez-vous déjà de ces séries chiffrées ? »
- Pourquoi : la rétrospective éclaire la prospective ; renvoi
  `../prospective-analyse.md` §5.7 pour la méthode. Si les séries ne sont pas
  fournies, ne jamais les reconstituer : marquer `[INCOMPLET — préciser :
  séries rétrospectives]`.

### Étape 5 — Prospective de fonctionnement et d'investissement
- Q5 : « Quelles sont les grandes orientations envisagées en fonctionnement
  (évolution des charges, des recettes) et en investissement (projets
  structurants, montant global envisagé) pour les exercices à venir ? »
- Pourquoi : distinction stricte des deux sections, conforme aux principes
  budgétaires (renvoi `../budget-cycle.md`). Aucun montant prospectif n'est
  avancé sans être qualifié de projection, jamais présenté comme acquis.

### Étape 6 — Structure et gestion de la dette
- Q6 : « Quel est l'état de l'encours de dette (montant global, structure par
  type de taux, profil d'extinction) et la stratégie de gestion envisagée
  pour l'exercice ? »
- Pourquoi : le ROB comporte en principe une présentation de la structure de
  la dette — renvoi `../dette-tresorerie.md` pour le fond et les ratios
  associés.

### Étape 7 — Engagements pluriannuels
- Q7 : « Existe-t-il des autorisations de programme/crédits de paiement
  (AP/CP) ou des engagements pluriannuels (marchés, conventions de
  subvention pluriannuelles) à mentionner ? »
- Pourquoi : ces engagements conditionnent la marge de manœuvre des
  exercices suivants — renvoi `../budget-cycle.md` §5.9 bis.

### Étape 8 — Ressources humaines, sous l'angle de l'enveloppe uniquement
- Q8 : « Quelle est l'évolution envisagée de l'enveloppe globale de la masse
  salariale (chapitre 012) pour l'exercice à venir, en montant global ou en
  taux d'évolution ? »
- Pourquoi : `SKILL.md` §5.5 — `dirfi-fpt` reste compétent tant que la
  discussion porte sur l'**enveloppe, le coût et l'imputation**. Dès que la
  réponse approche le **droit individuel** d'un agent ou le **régime
  indemnitaire** (taux, plafond par groupe de fonctions, condition
  d'attribution), **interrompre** cette rubrique et émettre le bloc
  **BASCULE** avant de poursuivre :

```
BASCULE drh-fpt — Cette demande porte sur le droit statutaire ou indemnitaire
des agents. Je ne la traite pas ici, y compris si drh-fpt est mobilisable dans
cette session.
À reprendre côté drh-fpt : [objet précis].
```

- Ce qui reste permis après la bascule : nommer l'étape sans la dérouler,
  chiffrer l'impact budgétaire global, signaler un enjeu de calendrier
  (`SKILL.md` §5.5).

### Étape 9 — Programmation des investissements
- Q9 : « Une programmation pluriannuelle des investissements (PPI) existe-t-
  elle ou est-elle à construire ? Quels sont les projets et montants
  envisagés, même provisoires ? »
- Pourquoi : renvoi `../prospective-analyse.md` §5.6. Toute valeur provisoire
  doit être présentée comme telle, jamais comme un montant arrêté.

### Étape 10 — Transmission et publicité
- Q10 : « Ce rapport sera-t-il mis à disposition du public (site internet ou
  autre support), et selon quelles modalités et quel délai ? »
- Pourquoi : la publicité du ROB est une formalité propre à vérifier selon
  la strate (étape 2) — ne jamais présumer son absence ou sa dispense.

**À l'issue de l'étape 10** : si toutes les réponses nécessaires ont été
recueillies, passer à l'assemblage (§2). Sinon, appliquer la règle
`[INCOMPLET]` (§4).

---

## 2. Gabarit d'assemblage

> Champs à compléter entre `[ ]`. Aucune collectivité, aucun nom de personne
> ou d'organisme réel ne figure dans ce canevas.

```
[COLLECTIVITÉ — en-tête]

RAPPORT D'ORIENTATION BUDGÉTAIRE
Exercice [année — étape 1]

Présenté en vue du débat d'orientation budgétaire du [date de séance].

Strate et régime applicable : [catégorie de collectivité, seuil ou
population — étape 2 ; obligation de ROB et contenu minimal — [INCOMPLET —
préciser : à vérifier] si non confirmés].

I. CONTEXTE MACROÉCONOMIQUE ET FINANCIER
[Éléments de loi de finances et de contexte macroéconomique de l'exercice —
étape 3, chacun daté ; renvoi ../fiscalite-locale.md, ../dotations-perequation.md]

II. RÉTROSPECTIVE
[Évolution des principaux agrégats sur la période retenue — étape 4 ;
renvoi ../prospective-analyse.md §5.7. Si des séries manquent :
[INCOMPLET — préciser : séries rétrospectives].]

III. ORIENTATIONS DE FONCTIONNEMENT
[Grandes orientations en fonctionnement — étape 5, section fonctionnement
uniquement]

IV. ORIENTATIONS D'INVESTISSEMENT
[Grandes orientations en investissement, projets structurants — étape 5,
section investissement uniquement]

V. STRUCTURE ET GESTION DE LA DETTE
[Encours, structure par type de taux, profil d'extinction, stratégie
envisagée — étape 6 ; renvoi ../dette-tresorerie.md]

VI. ENGAGEMENTS PLURIANNUELS
[AP/CP en cours, conventions pluriannuelles — étape 7 ; renvoi
../budget-cycle.md §5.9 bis]

VII. RESSOURCES HUMAINES — ENVELOPPE GLOBALE
[Évolution de l'enveloppe de masse salariale (chapitre 012) — étape 8,
montant global ou taux uniquement. Si un point statutaire ou indemnitaire a
été soulevé pendant l'entretien, le bloc BASCULE figure ci-dessus, avant
cette section, et aucun contenu statutaire individuel n'apparaît ici.]

VIII. PROGRAMMATION DES INVESTISSEMENTS (PPI)
[Programmation pluriannuelle, projets et montants — étape 9, toute valeur
provisoire signalée comme telle ; renvoi ../prospective-analyse.md §5.6]

IX. TRANSMISSION ET PUBLICITÉ
[Modalités de mise à disposition du public — étape 10, ou [INCOMPLET] si non
précisées]

Fait à [lieu], le [date].
[Signature de l'autorité exécutive ou du directeur des finances]
```

---

## 3. Mentions obligatoires et contrôles de cohérence

- [ ] Exercice budgétaire concerné identifié sans ambiguïté (étape 1).
- [ ] Strate de la collectivité qualifiée, obligation de ROB et contenu
  minimal vérifiés ou explicitement `[INCOMPLET]` (étape 2).
- [ ] Toute donnée macroéconomique ou de loi de finances datée (étape 3).
- [ ] Section fonctionnement et section investissement distinguées, jamais
  fusionnées (étape 5).
- [ ] Structure de la dette présentée avec renvoi `../dette-tresorerie.md`
  (étape 6).
- [ ] Aucun contenu statutaire individuel ou indemnitaire dans la section
  RH — uniquement l'enveloppe (étape 8) ; bloc BASCULE émis si un tel
  contenu a été approché pendant l'entretien.
- [ ] Toute valeur prospective ou de PPI présentée explicitement comme une
  projection, jamais comme un montant arrêté (étape 5, étape 9).
- [ ] Modalités de transmission et de publicité renseignées ou marquées
  `[INCOMPLET]` (étape 10).
- [ ] Cohérence entre les montants de la rétrospective, de la prospective et
  de la PPI signalée si un écart apparaît entre sections.

---

## 4. Règle `[INCOMPLET]` — application stricte

**Interdiction absolue d'halluciner une donnée manquante** : série
rétrospective, montant prospectif, taux macroéconomique, obligation de ROB
selon la strate, modalité de publicité.

1. Produire le brouillon avec les champs disponibles ; une section
   incomplète ne bloque pas la rédaction des autres.
2. Marquer chaque champ manquant `[INCOMPLET — préciser : <nom du champ>]`.
3. En fin de document, si au moins un champ est marqué `[INCOMPLET]`,
   ajouter :

```
---
## CHAMPS MANQUANTS — RAPPORT NON FINALISABLE EN L'ÉTAT

Les informations suivantes sont requises avant présentation au débat
d'orientation budgétaire :
- [champ manquant 1 — étape correspondante]
- [champ manquant 2 — étape correspondante]
- [...]

Ce rapport ne doit être ni présenté en séance, ni mis à disposition du
public, tant que ces champs ne sont pas renseignés — sous réserve de la
vérification de l'obligation exacte applicable à la strate (étape 2).
```

4. **Demander explicitement** ces données à l'utilisateur, en reprenant la
   formulation de la question d'étape correspondante (§1).
5. Ne jamais marquer le document comme « prêt à présenter » tant qu'une
   mention `[INCOMPLET]` subsiste, en particulier sur la strate et
   l'obligation de ROB (étape 2), qui conditionne le contenu minimal exigé.

---

## 5. Frontière RH — rappel opérationnel

Le ROB aborde nécessairement la masse salariale : c'est un point de
vigilance permanent, pas une exception.

- **Reste ici** : montant ou taux d'évolution de l'enveloppe globale,
  impact budgétaire d'une mesure collective déjà décidée ailleurs, calendrier
  d'une négociation en cours (sans en détailler le contenu).
- **Bascule vers `drh-fpt`** : tout plafond par groupe de fonctions, tout
  taux individuel de RIFSEEP/IFSE, toute condition d'attribution, toute
  référence à une instance de dialogue social (CST, F3SCT) ou à une
  procédure statutaire.
- **Format imposé** dès qu'un déclencheur apparaît : le bloc BASCULE
  (§1 étape 8) est émis **avant** tout contenu statutaire, jamais en note de
  bas de page après coup.

---

## 6. Double échelle [risque / confiance]

| Point | Risque | Confiance |
|---|---|---|
| Obligation de ROB et contenu minimal selon la strate | Élevé | À vérifier systématiquement (étape 2) |
| Données macroéconomiques et de loi de finances | Moyen à élevé | Jamais de mémoire, toujours datées |
| Rétrospective / prospective | Moyen | Distinguer valeur constatée et projection |
| Structure de la dette | Élevé | Renvoi `../dette-tresorerie.md` |
| Enveloppe RH (masse salariale) | Moyen | Bascule `drh-fpt` dès le droit individuel |
| Programmation des investissements (PPI) | Moyen | Toute valeur provisoire signalée comme telle |
| Publicité et transmission | Moyen | À vérifier selon la strate |

---

## 7. Checklist avant remise

1. Toutes les étapes du §1 parcourues une à une, avec confirmation à chaque
   étape.
2. Strate de la collectivité et obligation de ROB vérifiées avant de figer
   le contenu minimal du rapport (étape 2) — jamais présumées.
3. Sections fonctionnement et investissement distinguées à chaque rubrique
   concernée (étape 5).
4. Aucune donnée macroéconomique, aucun taux, aucun seuil cité sans date
   d'effet (étape 3, §5.4 `SKILL.md`).
5. Section RH limitée à l'enveloppe ; bloc BASCULE émis avant tout contenu
   statutaire ou indemnitaire approché pendant l'entretien (étape 8, §5).
6. Toute valeur prospective ou de PPI présentée comme projection, jamais
   comme montant acquis (étape 5, étape 9).
7. Aucune donnée manquante comblée par supposition — règle `[INCOMPLET]`
   (§4) appliquée et champs listés explicitement si nécessaire.
8. Modalités de transmission et de publicité renseignées ou marquées à
   vérifier (étape 10).
9. Aucune donnée nominative, aucun nom d'organisme ou de collectivité réel
   dans le document produit.
10. Mention finale claire : rapport **prêt à présenter** ou marqué
    **`[INCOMPLET]`** avec demande explicite des champs manquants — jamais
    d'état intermédiaire ambigu.
