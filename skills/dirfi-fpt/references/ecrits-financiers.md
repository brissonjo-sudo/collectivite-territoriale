# Branche — Écrits financiers (v1.0.0)

> Structure conforme à `_gabarit-branche.md`. Branche pilote de la couche 4.
> Aucune valeur datée ni numéro d'article cité de mémoire : seules les
> **règles** figurent, avec consigne de vérifier la version en vigueur à la
> date de l'acte.

## 1. Périmètre / Exclusions

**Périmètre** : cette branche **pilote les cinq générateurs interactifs**
de `references/templates/` : typologie des écrits d'une direction des
finances classés par nature, compétence et mentions obligatoires pour
chacun, transmission au contrôle de légalité et délais, motivation et
voies de recours des actes faisant grief, logique interactive obligatoire
et règles de rédaction communes à tous ces écrits.

**Exclusions** : le **contenu métier** de chaque domaine (fond du calcul
d'un ratio, régime d'une compétence, procédure d'un contrôle) reste dans la
branche correspondante — `references/budget-cycle.md`,
`references/dette-tresorerie.md`, `references/subventions.md`,
`references/controle-interne-financier.md`, etc. Cette branche **assemble
et met en forme**, elle ne tranche pas le fond ; toute question de fond
posée pendant l'assemblage d'un écrit se renvoie à la branche compétente
plutôt que d'être improvisée ici.

---

## 2. Questions couvertes

- Quel écrit produire pour telle décision ou telle situation financière ?
- Qui est compétent pour signer ou adopter cet écrit ?
- Quelles mentions sont obligatoires pour être régulier ?
- Cet écrit doit-il être transmis au contrôle de légalité, et dans quel
  délai ?
- Cet écrit fait-il grief ? Si oui, comment le motiver et quelles voies de
  recours indiquer ?
- Comment piloter le générateur interactif correspondant : quelles
  questions poser, dans quel ordre, comment traiter une donnée manquante ?
- Comment garantir la cohérence des montants entre le corps de l'écrit et
  ses annexes ?

---

## 3. Arbre de traitement

`identifier la nature de la décision ou de l'opération financière →
qualifier la nature de l'écrit (§4) → vérifier la compétence et les
mentions obligatoires (§5) → ouvrir le générateur references/templates/
correspondant → poser les questions une à une (objet, exercice, montant,
imputation, section, autorité compétente, calendrier) → si donnée
manquante : marquer [INCOMPLET] et la demander explicitement (jamais
halluciner) → assembler le document → vérifier la transmission requise
(§5, §6) → produire le livrable`.

Avant toute production, tester si l'écrit s'inscrit dans un **garde-fou**
du `SKILL.md` : un projet de délibération ou de convention qui ferait
manier des fonds hors circuit du comptable (§5.2 SKILL) ou qui exécuterait
un acte budgétaire irrégulier (§5.3 SKILL) impose le STOP ou l'ALERTE
correspondante **avant** toute mise en forme.

---

## 4. Variables à lever

- **Nature de la décision ou de l'opération** à l'origine de l'écrit
  (budgétaire, fiscale, garantie, subvention, procédure interne...).
- **Autorité compétente pressentie** : assemblée délibérante, exécutif,
  DirFi, service — à confirmer selon la branche de fond concernée avant de
  la présenter comme acquise.
- **Exercice budgétaire** concerné et date des faits.
- **Montant(s) en jeu** et **imputation** (section, chapitre, article
  selon la nomenclature applicable — renvoi `references/nomenclature-m57.md`
  pour le détail).
- **Destinataire(s) et transmission** requise (contrôle de légalité,
  organisme tiers, assemblée).
- **Caractère faisant grief ou non** de l'acte, conditionnant la
  motivation et les voies de recours.
- **Données manquantes** bloquant l'assemblage → règle `[INCOMPLET]`
  (§5.6).

---

## 5. Règles métier

### 5.1 Typologie des écrits d'une direction des finances

| Catégorie | Écrits type | Nature |
|---|---|---|
| **Acte décisionnel** | Délibération budgétaire, délibération fiscale, délibération de garantie d'emprunt | Acte de l'assemblée délibérante, exécutoire après transmission et publicité |
| **Acte d'exécution** | Certificat administratif, état de mandatement | Acte de l'ordonnateur, dans le cadre de crédits déjà ouverts |
| **Écrit de pilotage** | Note d'impact financier, note de cadrage budgétaire, rapport d'orientation budgétaire | Aide à la décision, non un acte au sens juridique strict |
| **Écrit conventionnel** | Convention de subvention, convention financière | Engagement contractuel entre la collectivité et un tiers |
| **Écrit de procédure** | Fiche de procédure interne | Document d'organisation interne, opposable en contrôle interne |

Un même dossier peut cumuler plusieurs de ces écrits : une opération de
garantie d'emprunt combine typiquement une délibération (acte décisionnel),
une convention avec le bénéficiaire (écrit conventionnel) et une note
d'impact financier préalable (écrit de pilotage). Ne jamais réduire une
opération complexe à un seul écrit sans avoir vérifié les autres nécessaires.

### 5.2 Acte décisionnel — compétence, mentions, transmission

- **Délibération budgétaire** (budget primitif, décision modificative,
  budget supplémentaire) : compétence de l'**assemblée délibérante**.
  Mentions obligatoires minimales : identification de l'exercice, respect
  du cadre et de la présentation budgétaire applicables, vote par section
  et, selon le régime en vigueur, par chapitre ou par article — vérifier
  le niveau de vote exact avant toute affirmation. **Transmission** au
  représentant de l'État au titre du contrôle de légalité, dans un délai à
  vérifier ; l'acte n'est exécutoire qu'après transmission et publicité.
- **Délibération fiscale** (vote des taux, institution d'une exonération
  facultative) : compétence de l'assemblée délibérante. Mentions
  obligatoires : identification précise de l'imposition concernée, taux ou
  dispositif voté, exercice d'application. **Délai de vote et de
  transmission aux services fiscaux** à vérifier systématiquement : un
  retard peut priver la mesure d'effet pour l'exercice visé.
- **Délibération de garantie d'emprunt** (renvoi
  `references/dette-tresorerie.md` §5.9 pour le fond) : compétence de
  l'assemblée délibérante, non délégable dans les mêmes conditions qu'une
  opération de dette propre. Mentions obligatoires : identité du
  bénéficiaire, caractéristiques du prêt garanti, quotité de garantie,
  ratios prudentiels vérifiés. **Acte faisant grief potentiel** : passage
  obligatoire par `references/controle-budgetaire.md` avant production,
  motivation en fait et en droit, transmission au contrôle de légalité.

### 5.3 Acte d'exécution — compétence, mentions, transmission

- **Certificat administratif** : établi par l'**ordonnateur** ou son
  délégataire, pour attester un fait ou une situation nécessaire à
  l'exécution d'une dépense ou d'une recette (absence de pièce type,
  justification d'une créance). Mentions obligatoires : objet précis,
  base de l'attestation, référence à l'engagement ou au dossier concerné,
  signature de l'autorité compétente. Pas de transmission au contrôle de
  légalité en tant que tel : pièce interne à la chaîne comptable, remise
  au comptable à l'appui du mandat ou du titre.
- **État de mandatement** : document récapitulatif établi par les services
  de l'ordonnateur pour transmettre au comptable un ensemble de mandats.
  Mentions obligatoires : identification de l'exercice, du chapitre et de
  l'imputation, cohérence entre le total de l'état et la somme des mandats
  qui le composent (règle de cohérence, §5.7). Pas d'acte faisant grief :
  document d'exécution, pas de voies de recours à prévoir.

### 5.4 Écrit de pilotage — compétence, mentions, transmission

- **Note d'impact financier** : rédigée par le **DirFi** ou ses services,
  destinée à éclairer une décision (de l'exécutif ou de l'assemblée) sur
  le coût, l'imputation et le calendrier budgétaire d'un projet. Pas d'acte
  au sens juridique : pas de transmission obligatoire, mais rigueur exigée
  sur les montants et l'imputation car elle **fonde** souvent une
  délibération ultérieure. Générateur : `references/templates/note-impact-financier.md`.
- **Note de cadrage budgétaire** : rédigée par le DirFi pour fixer les
  hypothèses et les enveloppes d'un exercice ou d'une prospective (renvoi
  `references/prospective-analyse.md`). Même nature qu'une note d'impact :
  outil de pilotage, pas un acte.
- **Rapport d'orientation budgétaire (ROB)** : rédigé sous l'autorité de
  l'**exécutif**, présenté à l'assemblée en vue du **débat d'orientation
  budgétaire** lorsque ce débat est obligatoire selon la strate de la
  collectivité (seuil à vérifier). Mentions attendues : orientations
  budgétaires, engagements pluriannuels envisagés, structure et gestion de
  la dette (renvoi `references/dette-tresorerie.md`), et, selon le seuil de
  population applicable, présentation de la structure des effectifs et de
  l'évolution des dépenses de personnel — **jonction obligatoire avec
  `drh-fpt`** pour le chiffrage RH détaillé (§5.8). Le rapport donne lieu à
  un **débat**, dont **acte est pris par une délibération spécifique** :
  ne pas confondre la présentation du rapport et la délibération actant le
  débat, deux formalités distinctes. Générateur :
  `references/templates/rapport-orientation-budgetaire.md`.

### 5.5 Écrit conventionnel et écrit de procédure

- **Convention de subvention** : engagement contractuel entre la
  collectivité (exécutif, sur habilitation de la délibération d'attribution)
  et le bénéficiaire. Mentions obligatoires : objet précis de la
  subvention, montant, modalités de versement, obligations du bénéficiaire
  (compte rendu financier, contrôle sur place le cas échéant), durée.
  Renvoi `references/subventions.md` pour le fond du régime applicable.
  Générateur : `references/templates/convention-subvention.md`.
- **Convention financière** (partenariat DGFiP, convention avec un
  satellite) : mentions obligatoires variables selon l'objet, toujours
  vérifiées dans la branche de fond concernée
  (`references/controle-interne-financier.md` pour une convention DGFiP).
  Pas de générateur dédié parmi les cinq : construire à partir de la
  logique interactive commune (§5.6) en s'appuyant sur la branche de fond.
- **Fiche de procédure financière** (interne) : document d'organisation
  décrivant un processus (plan de trésorerie, cartographie des risques,
  circuit de validation) pour la traçabilité et le contrôle interne
  (renvoi `references/controle-interne-financier.md`). Pas d'acte
  externe : validation interne (DirFi, ordonnateur selon le processus).
  Générateur : `references/templates/fiche-procedure-financiere.md`.

### 5.6 Logique interactive obligatoire

- **Détecter le type d'écrit** attendu à partir de la décision ou de
  l'opération décrite (§5.1), avant toute question de détail.
- **Poser les questions une à une** : objet, exercice, montant, imputation,
  section, autorité compétente, calendrier — un champ à la fois,
  confirmation avant de passer au suivant (`SKILL.md` §6).
- **Interdiction absolue d'halluciner une donnée manquante** — ni un
  montant, ni une imputation, ni une date de délibération, ni un nom
  d'autorité compétente.
- **Cas incomplet** : produire le brouillon avec les champs disponibles,
  marquer explicitement chaque champ manquant par `[INCOMPLET — préciser :
  <nom du champ>]`, lister ces champs en fin de document, et les demander
  explicitement avant de considérer l'écrit comme finalisé.
- Ne jamais transmettre, viser, ni présenter comme définitif un document
  portant une mention `[INCOMPLET]` non résolue.

### 5.7 Règles de rédaction communes

- **Précision de l'imputation** : toute mention d'imputation budgétaire
  (section, chapitre, article) doit être cohérente avec la nomenclature
  applicable à la collectivité — renvoi `references/nomenclature-m57.md`
  pour le détail, jamais improvisée ici.
- **Cohérence des montants entre le corps et les annexes** : un montant
  cité dans le corps d'un écrit doit être **strictement identique** à celui
  figurant dans toute annexe ou tableau récapitulatif joint. Un écart,
  même minime, doit être corrigé avant transmission, jamais laissé en
  l'état avec une réserve.
- **Anonymisation** : aucun écrit produit par cette branche n'expose de
  donnée nominative inutile (agent, administré, bénéficiaire personne
  physique identifié) au-delà de ce qui est strictement requis par la
  nature de l'acte (par exemple, une convention de subvention à une
  personne physique peut légitimement la nommer ; un tableau
  d'illustration de méthode ne le doit jamais).

### 5.8 Motivation et voies de recours des actes faisant grief

- Un acte financier **fait grief** lorsqu'il modifie directement la
  situation juridique d'un tiers ou crée une obligation à sa charge
  (délibération de garantie d'emprunt affectant un tiers, délibération
  fiscale créant une imposition, décision de rejet d'une demande de
  subvention motivée).
- Un tel acte doit être **motivé en fait et en droit** : exposer les
  circonstances qui le justifient et la base précise sur laquelle il
  s'appuie (renvoi à la branche de fond pour la base exacte, jamais
  inventée ici).
- Il doit indiquer les **voies et délais de recours** applicables
  (recours administratif préalable le cas échéant, recours contentieux),
  dont le contenu exact est à vérifier avant toute mention chiffrée de
  délai.
- Passage **obligatoire** par `references/controle-budgetaire.md` avant
  toute production d'un acte soumis au contrôle de légalité, pour vérifier
  la compétence de l'organe, la présence des mentions obligatoires et les
  délais de transmission applicables (`SKILL.md` §6).

### 5.9 Jonction obligatoire avec `drh-fpt`

Dès qu'un écrit financier (typiquement le rapport d'orientation budgétaire,
§5.4) doit intégrer un volet relatif aux effectifs, à la structure des
emplois ou à l'évolution détaillée des dépenses de personnel au-delà du
simple montant global, appliquer le **bloc BASCULE** du `SKILL.md` §5.5
avant tout contenu statutaire : cette branche assemble l'écrit et y
intègre l'enveloppe globale chiffrée, mais ne rédige jamais elle-même le
détail des effectifs, des grades ou du régime indemnitaire.

---

## 6. Calculs et procédures

1. **Identification du type d'écrit** (§5.1) — première étape, avant toute
   collecte de donnée.
2. **Vérification préalable des garde-fous** (`SKILL.md` §5.2, §5.3) —
   toute opération sous-jacente à l'écrit est testée avant assemblage.
3. **Recueil interactif** (§5.6) — un champ à la fois, jamais en bloc.
4. **Vérification de la compétence et des mentions obligatoires** (§5.2 à
   §5.5) avant assemblage final.
5. **Vérification de la cohérence des montants** entre corps et annexes
   (§5.7) avant toute transmission.
6. **Transmission** — selon le type d'écrit : contrôle de légalité pour un
   acte décisionnel soumis à cette obligation, comptable pour un acte
   d'exécution, bénéficiaire pour un écrit conventionnel, archivage interne
   pour une fiche de procédure.
7. **Archivage et traçabilité** — conserver la version transmise et, pour
   un acte faisant grief, la preuve de la notification des voies de
   recours.

---

## 7. Déclencheurs de vérification

Appliquer le socle-sources (matrice §2.2 du `SKILL.md`) dès que :
- la **compétence exacte** pour adopter ou signer l'écrit est en cause ;
- une **mention obligatoire** ou un **délai de transmission** au contrôle
  de légalité conditionne la régularité de l'acte ;
- un **seuil démographique** conditionne l'obligation d'un rapport
  d'orientation budgétaire ou son contenu détaillé ;
- l'écrit produit **fait grief** et nécessite une motivation ou des voies
  de recours précises ;
- un **identifiant Légifrance (LEGIARTI/JORFTEXT/NOR)** doit figurer dans
  l'écrit produit (règle de provenance, `SKILL.md` §5.4).

---

## 8. Pièges & confusions fréquentes

1. Produire une **délibération** sans vérifier que l'organe compétent est
   bien l'assemblée et non l'exécutif (ou l'inverse en cas de délégation).
2. Confondre la **présentation du rapport d'orientation budgétaire** et la
   **délibération actant le débat** : deux formalités distinctes,
   toutes deux nécessaires.
3. Halluciner un **montant ou une imputation manquante** plutôt que de
   marquer `[INCOMPLET]` et de la demander.
4. Laisser un **écart de montant** entre le corps d'un écrit et son
   annexe sans le corriger avant transmission.
5. Omettre la **motivation en fait et en droit** ou les **voies de
   recours** d'un acte faisant grief.
6. Rédiger le détail des **effectifs ou du régime indemnitaire** dans un
   rapport d'orientation budgétaire au lieu de basculer vers `drh-fpt`.
7. Exposer une **donnée nominative** non nécessaire à la nature de l'acte.
8. Traiter une **note d'impact financier** comme un acte juridique
   engageant, alors qu'elle n'est qu'un écrit de pilotage.
9. Oublier le passage par `references/controle-budgetaire.md` avant de
   produire un acte soumis au contrôle de légalité.

---

## 9. Données / valeurs à vérifier

- **Jamais de mémoire** : délai de transmission au contrôle de légalité
  d'une délibération budgétaire, fiscale ou de garantie ; seuil
  démographique déclenchant le rapport d'orientation budgétaire et son
  contenu renforcé (effectifs) ; délais et voies de recours exacts d'un
  acte faisant grief ; niveau de vote budgétaire exact (chapitre ou
  article) selon le régime applicable.
- **Références structurelles stables, citables avec la réserve « à
  confirmer en version consolidée »** : le **CGCT**, pour les dispositions
  relatives aux délibérations budgétaires et fiscales, au débat
  d'orientation budgétaire et au contrôle de légalité ; l'**instruction
  budgétaire et comptable M57**, pour la présentation formelle des actes
  budgétaires.
- **Aucun numéro d'article ni identifiant Légifrance
  (LEGIARTI/JORFTEXT/NOR)** n'est cité de mémoire dans cette branche : à
  défaut de vérification dans la session, s'en tenir au nom du texte et à
  la réserve.

---

## 10. Écrits & livrables — routage vers les générateurs

| Écrit | Catégorie | Générateur |
|---|---|---|
| Délibération budgétaire, fiscale ou de garantie d'emprunt | Acte décisionnel | `references/templates/deliberation-budgetaire.md` |
| Rapport d'orientation budgétaire | Écrit de pilotage | `references/templates/rapport-orientation-budgetaire.md` |
| Note d'impact financier / note de cadrage budgétaire | Écrit de pilotage | `references/templates/note-impact-financier.md` |
| Convention de subvention | Écrit conventionnel | `references/templates/convention-subvention.md` |
| Fiche de procédure financière | Écrit de procédure | `references/templates/fiche-procedure-financiere.md` |

**Écrits sans générateur dédié** (certificat administratif, état de
mandatement, convention financière hors subvention) : appliquer la même
logique interactive (§5.6) et les mêmes règles de rédaction (§5.7), en
s'appuyant sur la branche de fond concernée pour les mentions obligatoires
exactes.

**Rappel** (`SKILL.md` §6) : détecter le type d'écrit → poser les
questions une à une → assembler le document ; ne jamais halluciner une
donnée manquante, brouillon `[INCOMPLET]` sinon.

---

## 11. Double échelle [risque / confiance]

| Sous-domaine | Risque | Confiance | Repère |
|---|---|---|---|
| Choix du bon type d'écrit | Moyen | Stable | Vérification ponctuelle si situation mixte |
| Compétence de l'autorité signataire ou délibérante | Élevé | À vérifier systématiquement | Citation obligatoire avant production |
| Mentions obligatoires d'un acte décisionnel | Élevé | À vérifier selon le type d'acte | Citation + vérification avant transmission |
| Délai de transmission au contrôle de légalité | Élevé | À vérifier | Abstention si délai non confirmé |
| Acte faisant grief (motivation, voies de recours) | Critique | À vérifier systématiquement | Citation + motivation + voies de recours obligatoires |
| Donnée manquante dans un écrit | Élevé | N/A | `[INCOMPLET]` obligatoire, jamais d'hallucination |
| Volet effectifs d'un rapport d'orientation budgétaire | Élevé | Bascule `drh-fpt` obligatoire au-delà du montant global | Bloc BASCULE avant tout contenu statutaire |

---

## 12. Checklist de branche

1. **Garde-fous testés** (`SKILL.md` §5.2, §5.3) : l'opération sous-jacente
   à l'écrit fait-elle manier des fonds hors circuit du comptable, ou
   exécute-t-elle un acte irrégulier ? Si oui, STOP ou ALERTE affiché
   avant toute production.
2. **Type d'écrit correctement identifié** selon la typologie (§5.1),
   cumul d'écrits signalé si l'opération est complexe.
3. **Compétence** de l'autorité (assemblée / exécutif / DirFi / service)
   vérifiée et non supposée.
4. **Mentions obligatoires** toutes présentes pour le type d'écrit
   concerné (§5.2 à §5.5).
5. **Aucune donnée manquante comblée par supposition** : règle
   `[INCOMPLET]` appliquée et champs listés explicitement (§5.6).
6. **Cohérence des montants** entre le corps et les annexes vérifiée
   avant transmission (§5.7).
7. **Acte faisant grief** : motivation en fait et en droit, voies et
   délais de recours présents, passage par
   `references/controle-budgetaire.md` effectué.
8. **Aucune donnée nominative** exposée au-delà de ce que la nature de
   l'acte impose.
9. **Volet effectifs ou régime indemnitaire** : bloc BASCULE `drh-fpt` émis
   avant tout contenu statutaire, `drh-fpt` nommé explicitement, si le
   seuil de bascule est atteint.
10. **Fond métier** de chaque domaine renvoyé à la branche compétente, non
    improvisé dans cette branche.
11. Toute référence citée porte-t-elle sa provenance ou la réserve « à
    confirmer en version consolidée » (§9) ?
12. Couple **[risque / confiance]** (§11) indiqué quand utile à la
    décision ?
