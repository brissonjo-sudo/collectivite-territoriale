# Branche — Nomenclature & comptabilité M57 (v0.1.0)

> Structure conforme à `_gabarit-branche.md`. Aucun numéro d'article, aucun
> numéro de compte détaillé, aucun seuil ni durée d'amortissement n'est cité
> de mémoire : seules les **règles**, les **méthodes** et la consigne de
> vérifier l'instruction en vigueur figurent ici. Les références
> structurelles stables (nom de l'instruction, du plan de comptes) sont
> citées avec la réserve « à confirmer en version consolidée ».

## 1. Périmètre / Exclusions

- **Périmètre** : l'**architecture de la nomenclature M57** — référentiel
  budgétaire et comptable de droit commun des collectivités —, ses
  déclinaisons (développée, abrégée, simplifiée), le plan de comptes et ses
  classes, la fongibilité des crédits, les amortissements, les provisions et
  dépréciations, le rattachement des charges et produits à l'exercice, les
  restes à réaliser, les immobilisations et l'inventaire, la distinction
  opérations d'ordre / opérations réelles, l'articulation budgets annexes /
  TVA, l'état de l'actif et le compte financier unique (CFU) sous son angle
  **comptable**.
- **Exclusions** : la **mécanique du vote** et le **calendrier** du cycle
  budgétaire (DOB, BP, DM, CA/CFU sous son angle procédural) →
  `budget-cycle.md` ; le **circuit d'exécution** de la dépense (engagement,
  liquidation, mandatement) et de la recette (titre, recouvrement) →
  `execution-depense.md` et `execution-recette.md`.

---

## 2. Questions couvertes

- Qu'est-ce que la M57, et en quoi diffère-t-elle des nomenclatures
  antérieures (M14, M52, M71, M4) qu'elle a vocation à remplacer ?
- Quelle différence entre M57 développée, abrégée et simplifiée, et laquelle
  s'applique à cette collectivité ?
- Comment est organisé le plan de comptes, et à quoi correspondent les
  grandes classes de comptes ?
- Qu'est-ce que la fongibilité des crédits en M57, et comment s'articule-t-elle
  avec le niveau de vote choisi ?
- Quels biens doivent être amortis, qui fixe la durée d'amortissement, et
  comment sortir un bien de l'inventaire ?
- Dans quels cas une provision est-elle obligatoire, et comment distinguer
  provision et dépréciation ?
- Qu'est-ce que le rattachement des charges et produits à l'exercice, et en
  quoi diffère-t-il de la journée complémentaire ?
- Que sont les restes à réaliser, et comment les identifier en dépenses et en
  recettes ?
- Qu'est-ce qu'une opération d'ordre, par opposition à une opération réelle ?
- Comment un budget annexe s'articule-t-il avec l'assujettissement à la TVA ?
- Qu'est-ce que l'état de l'actif, et quel est son lien avec l'inventaire
  physique et le compte financier unique ?

---

## 3. Arbre de traitement

`qualifier l'opération comptable en cause (amortissement / provision /
rattachement / RAR / opération d'ordre / immobilisation) → identifier le
régime M57 applicable à la collectivité (développée / abrégée / simplifiée) →
situer l'opération dans le plan de comptes (classe, éventuellement compte) →
tester si l'opération est une obligation ou une faculté → vérifier l'exercice
de rattachement → vérifier la cohérence avec l'état de l'actif / l'inventaire
→ déclencheurs de vérification (§7) → signaler tout risque d'irrégularité
comptable ou d'incidence sur le compte financier unique → orienter vers
l'écrit (§10)`.

Ne jamais qualifier une écriture sans avoir d'abord identifié si elle relève
d'une opération **réelle** (flux de trésorerie) ou d'une opération **d'ordre**
(écriture sans flux) : la confusion des deux fausse tout raisonnement
d'équilibre.

---

## 4. Variables à lever

- **Régime M57 applicable** : développée, abrégée ou simplifiée — conditionne
  le niveau de détail du plan de comptes et certaines obligations annexes
  (états, présentation croisée). À vérifier, jamais présumé par défaut.
- **Nature du bien ou de la charge en cause** : immobilisation corporelle,
  incorporelle, financière ; charge à rattacher ; produit à rattacher.
- **Caractère obligatoire ou facultatif** de l'amortissement ou de la
  provision selon la nature du bien, la strate de la collectivité et la
  section budgétaire concernée.
- **Existence d'un ou plusieurs budgets annexes** et leur régime de TVA
  (assujetti, non assujetti, secteurs distincts).
- **Stade d'entrée dans le régime cible du compte financier unique (CFU)**,
  distinct du régime transitoire (compte administratif + compte de gestion) —
  conditionne la présentation de certains états (état de l'actif notamment).
- **Exercice de rattachement en cause** : l'opération se rapporte-t-elle à
  l'exercice clos, à l'exercice en cours, ou est-elle éligible à la journée
  complémentaire (→ `budget-cycle.md` §5.10, ne pas confondre) ?
- **Existence de restes à réaliser** identifiés à la clôture, en dépenses
  comme en recettes, pouvant affecter l'équilibre du budget suivant.

---

## 5. Règles métier

### 5.1 Architecture générale de la M57

- La M57 est le **référentiel budgétaire et comptable de droit commun** des
  collectivités territoriales et de leurs établissements publics, destiné à
  se substituer progressivement aux nomenclatures sectorielles antérieures
  (communale, départementale, régionale) — nom exact de l'instruction et
  texte fondateur : référence structurelle stable, **à confirmer en version
  consolidée**.
- Elle repose sur les **mêmes principes budgétaires** que les nomenclatures
  antérieures (annualité, unité, universalité, spécialité, équilibre réel,
  sincérité — détaillés en `budget-cycle.md` §5.8), et introduit des
  instruments renforcés : fongibilité étendue des crédits, AP/CP et AE/CP
  généralisées, compte financier unique.
- Elle s'organise, comme les nomenclatures antérieures, en un **plan de
  comptes** structuré par **classes**, décliné en une présentation budgétaire
  par **nature** et, le cas échéant, par **fonction** (→ `budget-cycle.md`
  §5.9 pour le vote).

### 5.2 M57 développée, abrégée, simplifiée

- **M57 développée** : niveau de détail le plus complet, applicable de plein
  droit ou sur option selon la strate — critère exact à vérifier.
- **M57 abrégée** : niveau intermédiaire, allégeant certaines obligations
  (état de la dette détaillé, annexes) sans changer les principes.
- **M57 simplifiée** : niveau le plus allégé, réservé aux collectivités dont
  la taille ou les enjeux financiers ne justifient pas un détail complet —
  critères d'éligibilité à vérifier avant toute affirmation.
- **Ce que le choix du régime ne change pas** : les principes budgétaires, la
  distinction opérations réelles/d'ordre, l'existence même des obligations
  d'amortissement et de provision (§5.5-5.6) — il module seulement le
  **niveau de détail** et certaines obligations documentaires.

### 5.3 Plan de comptes et classes de comptes

- Le plan de comptes M57 s'organise en **classes**, dont la portée générale
  peut être rappelée sans détail chiffré : comptes de bilan (immobilisations,
  stocks, tiers, financiers) et comptes de gestion (charges, produits). Le
  détail exact des classes et sous-comptes est une donnée de nomenclature
  technique : **à vérifier dans l'instruction en vigueur**, jamais reconstitué
  de mémoire pour une imputation précise.
- **Méthode d'imputation** : qualifier d'abord la **nature économique** de
  l'opération (immobilisation, charge, produit, opération financière), puis
  rechercher la classe et le compte correspondants dans l'instruction à jour
  — ne jamais imputer par analogie avec une autre nomenclature (M14 notamment)
  sans vérifier la table de correspondance officielle.
- Une erreur d'imputation n'est pas qu'une question de forme : elle peut
  fausser la lecture de l'équilibre par section et la sincérité du CFU.

### 5.4 Fongibilité des crédits

- La M57 renforce la **fongibilité** des crédits par rapport aux
  nomenclatures antérieures, en particulier lorsque le vote est organisé par
  **chapitre** : les crédits d'un même chapitre peuvent financer plusieurs
  articles sans virement formalisé, sous réserve des chapitres à régime
  spécifique (personnel, dépenses imprévues — → `budget-cycle.md` §5.5 et
  §5.9 pour l'articulation avec le niveau de vote).
- La fongibilité ne dispense **jamais** du respect de la spécialité : un
  crédit ouvert pour un objet déterminé ne finance que cet objet, même à
  l'intérieur d'un chapitre fongible.

### 5.5 Amortissements

- **Biens amortissables** : immobilisations dont la valeur se déprécie de
  manière certaine et irréversible avec le temps, l'usage ou l'obsolescence.
  L'obligation d'amortir varie selon la **nature du bien** et la **section**
  concernée (certaines catégories de biens, ou certaines strates pour la
  section de fonctionnement, connaissent des régimes différenciés — à
  vérifier avant de conclure à une obligation générale).
- **Durée d'amortissement** : fixée par **l'assemblée délibérante**, par
  catégorie de biens, dans le respect de bornes éventuellement fixées par le
  CGCT ou l'instruction — durées et bornes **à vérifier**, jamais chiffrées de
  mémoire. Une durée fixée doit être **appliquée de façon constante** d'un
  exercice à l'autre, sauf délibération motivée de changement.
- **Méthode** : identifier le bien → vérifier son caractère amortissable → vérifier l'existence d'une délibération fixant sa durée de catégorie → à défaut, alerter sur la lacune avant de proposer un taux ou une durée.
- **Sortie de l'inventaire** : un bien cédé, détruit ou réformé doit être
  sorti de façon **concordante** de l'inventaire et de l'état de l'actif, avec
  traitement de la valeur nette comptable résiduelle par une opération
  d'ordre appropriée (§5.9).

### 5.6 Provisions et dépréciations

- **Provision** : constatation comptable d'un **risque ou d'une charge**
  probable, non certaine dans son montant ou son échéance (contentieux,
  garantie donnée, risque financier identifié).
- **Dépréciation** : constatation d'une **perte de valeur** d'un actif
  (créance douteuse, immobilisation financière) sans disparition du bien
  lui-même.
- **Cas de provision obligatoire** (liste de principe, conditions exactes à
  vérifier avant toute affirmation) : contentieux dans lequel la collectivité
  est partie défenderesse dès lors qu'un risque est identifié ; créances dont
  le recouvrement est compromis ; garantie d'emprunt accordée à un tiers
  présentant un risque avéré ; ouverture d'une procédure collective
  concernant un débiteur ou un organisme garanti. **Ne jamais présumer
  l'absence d'obligation** sans avoir testé chacun de ces cas.
- **Méthode** : identifier le risque ou la perte de valeur → qualifier son caractère probable et évaluable → vérifier s'il entre dans un cas de provision obligatoire → à défaut, apprécier l'opportunité d'une provision facultative → documenter le calcul et la délibération le cas échéant.
- L'absence de provision dans un cas obligatoire est un **signal du
  garde-fou budgétaire** (`SKILL.md` §5.3) : le signaler avant toute
  recommandation d'exécution du budget en l'état.

### 5.7 Rattachement des charges et produits à l'exercice

- **Principe** : les charges et produits sont rattachés à l'exercice au titre
  duquel ils ont été **juridiquement engagés ou constatés** (service fait pour
  la dépense, droit constaté pour la recette), **indépendamment de la date de
  paiement ou d'encaissement**. C'est une application du principe de
  sincérité et d'indépendance des exercices.
- **Méthode** : identifier la date du fait générateur (service fait,
  livraison, prestation exécutée) → si elle se situe sur l'exercice clos mais
  que le mandatement ou le titre intervient après la clôture → rattacher par
  une écriture de rattachement, dans les conditions et limites fixées par
  l'instruction (à vérifier, notamment le seuil de matérialité éventuel).
- **À ne pas confondre avec la journée complémentaire** (`budget-cycle.md`
  §5.10) : le rattachement est une **règle d'imputation comptable** fondée sur
  le fait générateur ; la journée complémentaire est une **fenêtre
  calendaire** pendant laquelle certaines opérations peuvent encore être
  passées sur l'exercice clos. Les deux mécanismes se combinent mais ne se
  substituent pas l'un à l'autre.

### 5.8 Restes à réaliser (RAR)

- **Définition** : en section d'investissement principalement, les **RAR en
  dépenses** correspondent aux dépenses engagées mais non mandatées à la
  clôture ; les **RAR en recettes** correspondent aux recettes certaines dans
  leur principe mais non encore titrées ou encaissées à la clôture.
- **Effet** : les RAR sont repris au budget de l'exercice suivant (budget
  supplémentaire ou décision modificative) et **entrent dans le calcul du
  besoin de financement** de la section d'investissement pour l'affectation
  du résultat (→ `budget-cycle.md` §5.7).
- **Méthode d'identification** : pour chaque dépense engagée mais non
  mandatée à la clôture, vérifier l'existence d'un engagement juridique
  valide ; pour chaque recette attendue, vérifier qu'elle est **certaine dans
  son principe** (convention signée, décision notifiée), pas seulement
  probable. Une **sous-évaluation ou omission** fausse l'affectation du
  résultat et peut caractériser une insincérité budgétaire.

### 5.9 Immobilisations, inventaire et opérations d'ordre / réelles

- **Immobilisations** : biens destinés à servir de façon durable à l'activité
  de la collectivité, suivis à la fois par l'**ordonnateur** (inventaire
  physique et comptable) et par le **comptable public** (état de l'actif). La
  **concordance** entre inventaire et état de l'actif est une obligation
  permanente, pas seulement un exercice de clôture (§5.10).
- **Opération réelle** : donne lieu à un **flux financier effectif** (encaisse
  ou décaisse des fonds, ou modifie une créance/dette envers un tiers réel).
- **Opération d'ordre** : écriture comptable **sans flux de trésorerie**,
  destinée à retracer un mouvement patrimonial ou budgétaire interne
  (amortissement, sortie d'inventaire, intégration de travaux en régie,
  certaines opérations entre sections). On distingue les opérations d'ordre
  **budgétaires** (mouvementent les deux sections) et **semi-budgétaires**
  (mouvementent une seule section, l'autre écriture étant purement
  comptable) — la qualification exacte d'une opération donnée est une donnée
  technique à vérifier dans l'instruction, jamais présumée.
- **Méthode** : une opération qui ne modifie ni la trésorerie ni une
  créance/dette envers un tiers externe est, par construction, une opération
  d'ordre, dont la **contrepartie** est fixée par l'instruction — ne jamais
  l'inventer par analogie.

### 5.10 État de l'actif et compte financier unique

- **État de l'actif** : document tenu par le comptable public, recensant les
  immobilisations de la collectivité valorisées à leur coût comptable, et
  devant être **concordant** avec l'inventaire physique et comptable tenu par
  l'ordonnateur.
- Une **divergence** entre inventaire et état de l'actif doit être
  **régularisée avant la clôture de l'exercice**, jamais laissée en l'état
  d'un exercice sur l'autre : elle fausse à la fois le calcul des
  amortissements et la fiabilité du bilan.
- **Compte financier unique (CFU)** : sous son angle comptable, il intègre et
  rend cohérents la balance générale, le bilan, le compte de résultat et
  l'état de l'actif, établis conjointement par l'ordonnateur et le comptable —
  volet **procédural** du vote du CFU renvoyé à `budget-cycle.md` §5.6, ne pas
  le dupliquer ici.

### 5.11 Budgets annexes et assujettissement à la TVA

- Un budget annexe retraçant une activité de nature **industrielle et
  commerciale** est, selon les cas, **assujetti à la TVA** — la qualification
  exacte (assujettissement de plein droit, option, exonération) dépend de la
  nature de l'activité et d'un texte fiscal à vérifier au cas par cas, sans
  jamais présumer un régime par analogie avec un autre budget annexe.
- L'assujettissement à la TVA a des conséquences comptables directes :
  comptabilisation hors taxes des opérations concernées, suivi de la TVA
  collectée et déductible, articulation avec le mécanisme du FCTVA pour la
  part **non assujettie** — l'éligibilité au FCTVA d'une dépense donnée est
  une donnée à vérifier, jamais déduite par défaut de la nature du budget
  annexe.
- Le régime budgétaire et le cycle propre de chaque budget annexe relèvent de
  `budget-cycle.md` §5.11, ne pas le dupliquer ici.

---

## 6. Calculs et procédures

### 6.1 Méthode générale d'imputation

Qualifier la nature économique de l'opération (immobilisation, charge,
produit, opération financière, opération d'ordre) → identifier le régime M57
applicable (développée/abrégée/simplifiée) → rechercher la classe et le
compte dans l'instruction à jour, sans reconstitution de mémoire → vérifier la
cohérence avec une éventuelle opération miroir (opération d'ordre à double
écriture) → documenter la pièce justificative correspondante (→
`execution-depense.md` / `execution-recette.md`).

### 6.2 Méthode de calcul d'un amortissement

Poser la **formule**, jamais un résultat chiffré présumé : dotation annuelle =
fonction de la **base amortissable** (valeur d'acquisition, éventuellement
diminuée de la valeur résiduelle) et de la **durée fixée par l'assemblée**
pour la catégorie de bien concernée, selon le mode retenu (linéaire en
principe). Toute application chiffrée suppose de disposer de la
**délibération fixant la durée** : à défaut, ne pas inventer une durée usuelle
et demander la donnée manquante.

### 6.3 Méthode de constitution d'une provision

Identifier le fait générateur du risque ou de la perte de valeur → apprécier
son **caractère probable** (par opposition à une simple éventualité) → évaluer
le montant sur la meilleure estimation disponible, documentée → vérifier si le
cas entre dans une hypothèse de provision **obligatoire** (§5.6) → délibérer
si nécessaire → suivre la provision jusqu'à sa reprise (risque réalisé,
disparu, ou réévalué).

### 6.4 Méthode de traitement d'un rattachement ou d'un reste à réaliser

Identifier la date du fait générateur → la situer par rapport à la date de
clôture → si antérieure à la clôture et non mandatée/titrée : rattachement
(charges/produits, §5.7) ou reste à réaliser (engagements d'investissement,
§5.8) selon la nature de l'opération → documenter dans l'état correspondant,
annexé au compte financier unique.

---

## 7. Déclencheurs de vérification

Appliquer le socle-sources (`SKILL.md` §5.4, matrice §2.2) avant de conclure
dès que la question porte sur :

- le **régime M57** exact applicable à la collectivité (développée, abrégée,
  simplifiée) et ses conséquences documentaires ;
- une **durée d'amortissement** ou une **catégorie de biens amortissables**
  non couverte par une délibération déjà vérifiée ;
- le **caractère obligatoire** d'une provision dans un cas non manifestement
  couvert par la liste de principe (§5.6) ;
- un **numéro de compte ou de classe** précis nécessaire à une imputation
  réelle ;
- le **régime de TVA** ou d'éligibilité au FCTVA d'un budget annexe ou d'une
  opération donnée ;
- l'articulation exacte entre **régime transitoire** et **compte financier
  unique cible** pour la collectivité concernée ;
- toute **réforme récente** de l'instruction M57 ou du plan de comptes.

---

## 8. Pièges & confusions fréquentes

1. Confondre **provision** (risque ou charge probable) et **dépréciation**
   (perte de valeur d'un actif) : régimes et objets distincts.
2. Confondre **rattachement des charges et produits** et **journée
   complémentaire** : le premier est une règle d'imputation, la seconde une
   fenêtre calendaire (§5.7).
3. Imputer par **analogie** avec une nomenclature antérieure (M14 notamment)
   sans vérifier la table de correspondance officielle vers la M57.
4. Présumer une **durée d'amortissement usuelle** sans vérifier la
   délibération de l'assemblée qui la fixe pour la catégorie de bien
   concernée.
5. Oublier un **cas de provision obligatoire** (contentieux, créance
   compromise, garantie d'emprunt à risque) faute de test systématique.
6. Sous-évaluer ou omettre des **restes à réaliser**, faussant le calcul du
   besoin de financement et l'affectation du résultat.
7. Confondre **opération réelle** et **opération d'ordre** : seule la première
   comporte un flux de trésorerie effectif.
8. Laisser subsister une **divergence entre inventaire et état de l'actif**
   d'un exercice sur l'autre au lieu de la régulariser avant clôture.
9. Présumer un **régime de TVA** pour un budget annexe par analogie avec un
   autre, sans vérification propre à l'activité concernée.
10. Citer un **numéro de compte ou de classe** de mémoire dans un acte ou une
    pièce, au lieu de vérifier l'instruction en vigueur.

---

## 9. Données / valeurs à vérifier

| Donnée | Statut |
|---|---|
| Nom et texte fondateur exact de l'instruction M57 | Référence structurelle stable — **à confirmer en version consolidée** |
| Critères d'application de la M57 développée / abrégée / simplifiée selon la strate | **À vérifier** |
| Liste et numéros exacts des classes et comptes du plan de comptes M57 | **À vérifier** — jamais reconstitués de mémoire pour une imputation réelle |
| Liste exacte des biens amortissables et des exceptions par strate/section | **À vérifier** |
| Durées d'amortissement par catégorie de biens | **À vérifier** — fixées par délibération locale, dans des bornes éventuelles du texte |
| Liste exhaustive et conditions précises des cas de provision obligatoire | **À vérifier** |
| Seuil de matérialité éventuel pour le rattachement des charges et produits | **À vérifier** |
| Régime précis de TVA et d'éligibilité au FCTVA d'une activité de budget annexe | **À vérifier**, propre à chaque activité |
| Nomenclature de qualification opération d'ordre budgétaire / semi-budgétaire pour une écriture donnée | **À vérifier** dans l'instruction en vigueur |
| Date d'entrée effective de la collectivité dans le régime cible du CFU | **À vérifier**, propre à chaque collectivité |

---

## 10. Écrits & livrables

| Écrit | Élément obligatoire | Générateur |
|---|---|---|
| Délibération fixant les durées d'amortissement par catégorie de biens | Catégories couvertes, durées, date d'effet, constance dans le temps | `references/templates/deliberation-budgetaire.md` |
| Délibération constituant une provision | Fait générateur, montant documenté, caractère obligatoire ou facultatif | `references/templates/deliberation-budgetaire.md` |
| État des restes à réaliser | Liste par opération, dépense ou recette, montant engagé/attendu | Annexe au compte financier unique, sans gabarit dédié à ce stade |
| Note d'impact financier sur un choix de nomenclature ou de durée | Hypothèses annoncées, données manquantes signalées | `references/templates/note-impact-financier.md` |

Toute écriture affectant l'équilibre du budget (provision obligatoire non
constituée, RAR omis) doit être signalée avant la production d'un acte
budgétaire → `budget-cycle.md` et, en cas d'irrégularité,
`controle-budgetaire.md`.

---

## 11. Double échelle [risque / confiance]

| Sous-domaine | Risque | Confiance |
|---|---|---|
| Choix du régime M57 (développée/abrégée/simplifiée) | Moyen | À vérifier |
| Imputation sur un compte précis | Moyen à élevé | À vérifier systématiquement |
| Durée d'amortissement d'une catégorie de biens | Moyen | Stable dans la méthode, durée à vérifier |
| Caractère obligatoire d'une provision | Élevé | À vérifier au cas par cas |
| Rattachement des charges et produits | Moyen à élevé | Stable dans le principe, seuil à vérifier |
| Restes à réaliser et effet sur l'affectation du résultat | Élevé | Stable dans la méthode |
| Qualification opération d'ordre / opération réelle | Moyen | Stable dans le principe |
| Régime de TVA d'un budget annexe | Élevé | À vérifier |
| Concordance inventaire / état de l'actif | Élevé | Stable dans le principe |

---

## 12. Checklist de branche

1. **Régime M57** applicable identifié et non présumé par défaut ?
2. **Nature économique** de l'opération qualifiée avant toute recherche
   d'imputation ?
3. **Opération réelle / opération d'ordre** correctement distinguée ?
4. Si amortissement : **délibération fixant la durée** vérifiée, pas de durée
   usuelle inventée ?
5. Si provision : **cas d'obligation** testé systématiquement (§5.6), et
   garde-fou budgétaire déclenché si absence dans un cas obligatoire ?
6. **Rattachement** distingué de la **journée complémentaire** ?
7. **Restes à réaliser** recensés et leur effet sur l'affectation du résultat
   signalé (→ `budget-cycle.md`) ?
8. **Concordance inventaire / état de l'actif** vérifiée si des
   immobilisations sont en cause ?
9. Si budget annexe : **régime de TVA** traité comme donnée à vérifier, non
   présumé ?
10. Aucun **numéro de compte, durée ou seuil** cité de mémoire, tous marqués
    « à vérifier » ou « à confirmer en version consolidée » ?
11. Couple **[risque / confiance]** (§11) indiqué quand utile à la décision ?
12. **Écrit** demandé effectivement produit (délibération, état annexe, note
    d'impact) ?
