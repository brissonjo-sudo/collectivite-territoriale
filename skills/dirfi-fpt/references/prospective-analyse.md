# Branche — Prospective & analyse financière (v1.0.0)

> Structure conforme à `_gabarit-branche.md`. Les ratios sont donnés en
> **formule** (numérateur / dénominateur), jamais avec un seuil d'alerte
> chiffré : le seuil est toujours à vérifier à la source.

## 1. Périmètre / Exclusions

**Périmètre** : lecture de la **chaîne de l'épargne** (épargne de gestion,
brute, nette) ; **capacité de désendettement** ; ratios de structure
(**taux d'épargne brute**, **effort d'équipement**, **taux de rigidité des
charges structurelles**, **coefficient de mobilisation du potentiel
fiscal**) ; ratios obligatoires annexés au budget ; **fonds de roulement**,
**besoin en fonds de roulement**, **trésorerie nette** ; construction d'une
**prospective pluriannuelle** et d'une **programmation pluriannuelle des
investissements (PPI)** ; **analyse rétrospective** ; sources de données de
comparaison ; pilotage de la **masse salariale sous l'angle budgétaire**.

**Exclusions** :
- La **gestion de la dette elle-même** (compétence, produits, couverture,
  ligne de trésorerie, garanties) → `references/dette-tresorerie.md`. Cette
  branche lit et projette l'endettement, elle ne le gère pas.
- Les **règles statutaires et indemnitaires** des agents (carrière, régime
  indemnitaire, GVT au sens du droit individuel) → **`drh-fpt`**. Cette
  branche ne traite la masse salariale que comme une **masse budgétaire**
  (cadrage, enveloppe, glissement global), jamais comme un droit individuel.
- L'**imputation comptable** des opérations entrant dans le calcul des
  ratios → `references/nomenclature-m57.md`.

---

## 2. Questions couvertes

- Comment se lit la chaîne de l'épargne, et que signale une dégradation de
  l'épargne nette ?
- Comment calculer la capacité de désendettement, et quelles sont ses
  limites méthodologiques ?
- Comment interpréter le taux d'épargne brute, l'effort d'équipement, le
  taux de rigidité des charges structurelles, le coefficient de
  mobilisation du potentiel fiscal ?
- Quels ratios sont obligatoirement annexés au budget ?
- Comment calculer le fonds de roulement, le besoin en fonds de roulement
  et la trésorerie nette, et que signale chacun ?
- Comment construire une prospective financière pluriannuelle fiable, avec
  quelles hypothèses et quelle sensibilité ?
- Comment articuler une PPI avec les autorisations de programme / crédits
  de paiement (AP/CP) et un plan de financement ?
- Comment mener une analyse rétrospective robuste, avec quels retraitements
  et quelle comparaison à la strate ?
- Où trouver des données de comparaison fiables, et quelles en sont les
  limites ?
- Comment cadrer la masse salariale d'un point de vue budgétaire sans
  empiéter sur le champ RH ?

---

## 3. Arbre de traitement

`question → variables à lever (§4) → décision → vérification (§7) →
écrit/livrable (§10)`

Avant tout calcul ou toute lecture de ratio, lever : l'**exercice ou la
série d'exercices** concernés, le **périmètre** budgétaire retenu (budget
principal seul, ou consolidé avec les budgets annexes), et l'**origine des
données** (comptes de gestion réalisés, budget primitif, projection). Sans
ces trois éléments, marquer l'analyse `[INCOMPLET]` et les demander
explicitement plutôt que de supposer un périmètre par défaut.

---

## 4. Variables à lever

- **Exercice(s) analysé(s)** : un seul exercice (photographie) ou une série
  (rétrospective, §5.7) — la méthode et la lecture diffèrent.
- **Périmètre budgétaire** : budget principal seul, ou consolidation avec
  budgets annexes et satellites significatifs.
- **Origine des données** : compte de gestion / compte financier unique
  (réalisé), budget primitif (prévisionnel), ou projection (hypothèses de
  travail) — ne jamais mélanger sans le signaler.
- **Régime comptable** (M57 de droit commun ou abrégé, selon la strate) :
  conditionne certains agrégats et leur comparabilité — à vérifier.
- **Horizon de la prospective demandée** : nombre d'exercices, et
  articulation ou non avec un mandat ou une PPI déjà engagée.
- **Hypothèses macro-budgétaires disponibles** : évolution attendue des
  bases fiscales, des dotations, de l'inflation appliquée aux charges — à
  demander explicitement, jamais supposées par défaut sans le signaler.
- **Existence d'une PPI ou d'AP/CP déjà votées** dont la prospective doit
  tenir compte.
- **Source de comparaison souhaitée** (données nationales de la strate,
  observatoire local, réseau de pairs) et son degré d'actualité.

---

## 5. Règles métier

### 5.1 La chaîne de l'épargne

- **Épargne de gestion** : différence entre les recettes réelles de
  fonctionnement et les dépenses réelles de fonctionnement **hors intérêts
  de la dette**. Elle mesure la capacité de gestion courante, indépendamment
  du poids de la dette.
- **Épargne brute** (ou autofinancement brut) : épargne de gestion **moins
  les intérêts de la dette**. Elle mesure ce qui reste du fonctionnement
  pour couvrir le remboursement du capital de la dette et contribuer au
  financement de l'investissement.
- **Épargne nette** : épargne brute **moins le remboursement en capital de
  la dette** de l'exercice. Elle mesure la capacité résiduelle
  d'autofinancement des investissements une fois la dette servie.
- **Lecture** : une épargne de gestion stable mais une épargne brute qui se
  dégrade signale un poids croissant de la charge d'intérêts. Une épargne
  brute stable mais une épargne nette qui se dégrade signale un poids
  croissant du remboursement en capital, donc de l'encours de dette.
  L'épargne nette négative signale une incapacité à autofinancer
  l'investissement sans recette exceptionnelle ou nouvel emprunt — point de
  vigilance à signaler explicitement, sans en tirer seul une conclusion de
  déséquilibre budgétaire (renvoi `references/controle-budgetaire.md`
  uniquement si un déséquilibre réel de la section est établi).

### 5.2 Capacité de désendettement

- **Formule** : `encours de dette au 31 décembre / épargne brute de
  l'exercice`. Le résultat s'exprime en nombre d'années : le nombre
  d'exercices qu'il faudrait, en théorie, pour rembourser l'intégralité de
  l'encours si toute l'épargne brute y était consacrée.
- **Seuils d'alerte** : des repères existent et sont utilisés dans le débat
  public et par certains textes ou pratiques de contrôle. **Ne jamais les
  citer de mémoire** : vérifier la valeur en vigueur et sa source exacte
  avant toute conclusion présentée comme engageante.
- **Limites de l'indicateur** :
  - il suppose une épargne brute **stable dans le temps**, hypothèse
    rarement vérifiée ;
  - il ne dit rien du **profil d'amortissement** de la dette (un encours
    concentré sur des échéances proches pèse différemment d'un encours
    lissé) ;
  - il est sensible à un **effet de ciseau ponctuel** (recette
    exceptionnelle ou dépense exceptionnelle sur l'exercice de calcul), qui
    peut fausser la lecture d'une seule année ;
  - il ignore la **qualité** de la dette (taux, structure au sens de la
    charte Gissler, renvoi `references/dette-tresorerie.md`) ;
  - il doit se lire en **tendance sur plusieurs exercices**, pas sur une
    seule année isolée.

### 5.3 Ratios de structure

- **Taux d'épargne brute** : `épargne brute / recettes réelles de
  fonctionnement`. Mesure la part des recettes de fonctionnement
  transformée en capacité d'autofinancement.
- **Effort d'équipement** : `dépenses d'équipement de l'exercice / recettes
  réelles de fonctionnement` (ou parfois rapporté à la population, selon la
  convention retenue — préciser laquelle avant toute comparaison). Mesure
  l'intensité de l'investissement rapportée à la richesse de fonctionnement.
- **Taux de rigidité des charges structurelles** : `(charges de personnel +
  charges financières + contingents et participations obligatoires) /
  recettes réelles de fonctionnement`. Mesure la part des charges peu ou
  pas pilotables à court terme dans le total des recettes de
  fonctionnement — un taux élevé signale une marge de manœuvre budgétaire
  réduite.
- **Coefficient de mobilisation du potentiel fiscal** : `produit fiscal
  effectivement perçu sur les impositions concernées / potentiel fiscal de
  la collectivité`. Mesure le degré d'utilisation, par la collectivité, de
  sa capacité fiscale théorique par rapport à la référence retenue pour ce
  potentiel.
- **Aucun de ces ratios ne se lit isolément** : toujours les croiser avec la
  chaîne de l'épargne (§5.1) et la tendance pluriannuelle (§5.5), jamais sur
  un seul exercice.

### 5.4 Ratios obligatoires annexés au budget, fonds de roulement, BFR, trésorerie nette

- Un jeu de **ratios obligatoires** doit figurer en annexe du budget primitif
  et du compte administratif ou du compte financier unique, dont la liste
  exacte et la présentation relèvent d'un texte à vérifier (CGCT, dispositions
  relatives aux documents budgétaires — à confirmer en version consolidée).
  Ne jamais présenter une liste de ces ratios comme exhaustive sans l'avoir
  vérifiée.
- **Fonds de roulement (FR)** : ressources stables (financements permanents)
  moins emplois stables (immobilisations nettes). Mesure la marge de
  sécurité structurelle de la collectivité.
- **Besoin en fonds de roulement (BFR)** : décalage entre les besoins de
  financement du cycle d'exploitation courant (créances, stocks le cas
  échéant) et les ressources courantes correspondantes (dettes
  fournisseurs et assimilées). Pour une collectivité, il reflète
  essentiellement les décalages entre émission des titres/mandats et leur
  recouvrement/paiement effectif.
- **Trésorerie nette (TN)** : `TN = FR − BFR`. Une trésorerie nette
  durablement négative, alors que le fonds de roulement paraît suffisant,
  signale un BFR anormalement élevé (délais de recouvrement dégradés, par
  exemple) à investiguer, plutôt qu'un problème de fonds de roulement.
- Ne jamais confondre la **trésorerie nette** ainsi calculée avec le solde
  du compte au comptable public à un instant donné : le second est un
  solde de caisse, la première un agrégat de gestion sur la durée.

### 5.5 Construction d'une prospective pluriannuelle

**Méthode**, dans l'ordre :
1. **Scénario tendanciel** : projeter chaque grande masse (recettes
   fiscales, dotations, charges de personnel, charges à caractère général,
   charges financières, investissement récurrent) sur la base des
   **tendances observées** en rétrospective (§5.7), sans rupture supposée.
2. **Hypothèses explicites et documentées** : chaque hypothèse retenue
   (évolution des bases fiscales, des dotations, de l'inflation appliquée
   aux charges, glissement de la masse salariale) doit être **écrite, datée
   et justifiée**, jamais implicite — une hypothèse non documentée invalide
   la lecture qui en découle.
3. **Sensibilité** : faire varier une à une les hypothèses les plus
   incertaines (taux d'un futur emprunt, dynamique des bases fiscales,
   évolution d'une dotation) pour identifier ce qui pèse le plus sur la
   trajectoire d'épargne et d'endettement.
4. **Scénario de rupture** : construire un scénario alternatif intégrant un
   choc identifié (réforme fiscale ou de dotations, charge nouvelle,
   investissement majeur) pour mesurer l'écart au tendanciel et la marge de
   manœuvre résiduelle.
- Jamais de **donnée manquante comblée par supposition silencieuse** :
  demander la donnée, ou signaler explicitement l'hypothèse retenue.
- Croiser systématiquement la trajectoire projetée d'épargne nette (§5.1)
  et de capacité de désendettement (§5.2) avec la dette existante
  (`references/dette-tresorerie.md`).

### 5.6 Programmation pluriannuelle des investissements (PPI)

- **Méthode** : recenser les projets par échéance envisagée, les classer
  par degré d'engagement (déjà engagé, décidé non engagé, à l'étude), puis
  les confronter à la capacité de financement dégagée par la prospective
  (§5.5) — recettes propres, subventions attendues, épargne nette
  disponible, recours à l'emprunt.
- **Articulation AP/CP** : une PPI validée politiquement se traduit, pour
  les opérations significatives, en **autorisations de programme et
  crédits de paiement**, ouverts et révisés par l'assemblée délibérante
  (renvoi `references/budget-cycle.md` pour le formalisme, non dupliqué
  ici).
- **Plan de financement** : distinguer les recettes mobilisables par
  nature (subventions à confirmer, FCTVA à échéance à vérifier, emprunt,
  autofinancement) et confronter le total au besoin, en signalant tout
  écart non couvert plutôt que de le combler par une hypothèse d'emprunt
  non assumée comme telle.
- Une PPI dont le financement suppose une épargne supérieure à celle
  réellement projetée (§5.5) est un signal à faire remonter avant
  présentation à l'assemblée.

### 5.7 Analyse rétrospective

- Porte sur une **série d'exercices clos** (nombre à adapter au besoin,
  généralement plusieurs années), jamais sur un seul exercice présenté
  comme représentatif d'une tendance.
- **Retraitements nécessaires** avant comparaison inter-exercices :
  neutraliser les éléments exceptionnels ou non récurrents (cession
  exceptionnelle, recette ou dépense non reconductible, changement de
  périmètre par intégration ou sortie d'un budget annexe), signaler tout
  changement de nomenclature ou de règle comptable affectant la
  comparabilité d'une année sur l'autre.
- **Comparaison à la strate** : rapprocher les ratios de la collectivité de
  ceux d'un groupe de comparaison pertinent (collectivités de même
  catégorie et de taille comparable), en vérifiant à chaque fois la
  définition exacte retenue par la source de comparaison pour chaque
  agrégat (§5.8) — deux sources peuvent définir un même ratio différemment.
- Une rétrospective sert de **fondement** au scénario tendanciel de la
  prospective (§5.5) : sans rétrospective retraitée et fiable, aucune
  prospective ne peut être présentée comme robuste.

### 5.8 Sources de données de comparaison et leurs limites

- Les données de comparaison à la strate proviennent de bases publiques
  (données financières et fiscales des collectivités) ou d'observatoires
  spécialisés. Ne jamais citer un chiffre de comparaison sans en vérifier
  la source, la date d'actualisation et le périmètre exact retenu.
- **Limites systématiques** : hétérogénéité des périmètres (budget
  principal seul ou consolidé selon les collectivités comparées), décalage
  temporel entre l'exercice de la collectivité analysée et celui de la
  base de comparaison, définitions parfois différentes d'un même ratio
  selon la source.
- Présenter toute comparaison à la strate avec sa **réserve méthodologique**
  explicite plutôt que comme un constat brut.

### 5.9 Pilotage de la masse salariale — angle budgétaire uniquement

- Cette branche traite la masse salariale (chapitre budgétaire dédié)
  strictement comme une **masse à cadrer** : enveloppe globale, évolution
  prévisionnelle, poids dans les charges de fonctionnement (renvoi §5.3,
  taux de rigidité), articulation avec la prospective (§5.5).
- **Glissement vieillesse-technicité (GVT)** et **effet de noria** peuvent
  être **nommés** comme composantes de l'évolution de la masse salariale
  d'un exercice à l'autre (progression liée à l'ancienneté et aux
  avancements pour le GVT, effet de l'écart de rémunération entre agents
  partants et agents recrutés pour la noria), à des fins de **cadrage
  budgétaire global** uniquement.
- **Renvoi obligatoire à `drh-fpt`** dès que la question porte sur : le
  calcul individuel d'un droit statutaire, une mesure de régime
  indemnitaire, une ligne directrice de gestion, ou tout paramètre
  RH nécessitant une compétence statutaire pour être chiffré précisément.
  Appliquer alors le **bloc BASCULE** du `SKILL.md` §5.5 avant tout contenu
  statutaire, y compris si la question n'était, au départ, qu'une question
  de cadrage budgétaire glissant vers le détail individuel.
- **Ce qui reste permis** après la bascule : citer l'enveloppe globale
  votée, son évolution en euros ou en pourcentage d'un exercice à l'autre,
  son poids dans les charges de fonctionnement, et le calendrier
  budgétaire d'inscription. **Ce qui est interdit** : tout montant de
  régime indemnitaire, tout plafond par groupe de fonctions, toute
  condition individuelle d'attribution.

---

## 6. Calculs et procédures

1. **Chaîne de l'épargne** — poser les trois formules du §5.1 dans l'ordre
   (gestion → brute → nette), jamais isolément.
2. **Capacité de désendettement** — `encours au 31/12 / épargne brute` ;
   lire en tendance sur plusieurs exercices, jamais sur une seule année, et
   ne jamais énoncer le seuil d'alerte sans l'avoir vérifié.
3. **Ratios de structure** — poser chaque formule du §5.3 avec son
   numérateur et son dénominateur exacts ; préciser la convention retenue
   quand plusieurs existent (ex. effort d'équipement rapporté aux recettes
   ou à la population).
4. **FR / BFR / TN** — poser `TN = FR − BFR` et interpréter un écart avant
   toute conclusion sur la trésorerie disponible.
5. **Prospective pluriannuelle** — dérouler les quatre étapes du §5.5 dans
   l'ordre ; ne jamais sauter l'étape de sensibilité ni celle du scénario
   de rupture pour une prospective présentée comme robuste.
6. **PPI et plan de financement** — confronter le besoin de financement
   recensé aux ressources mobilisables par nature (§5.6), signaler tout
   écart non couvert.
7. **Rétrospective** — appliquer les retraitements de neutralisation avant
   toute comparaison inter-exercices ou inter-collectivités (§5.7).

---

## 7. Déclencheurs de vérification

Appliquer le socle-sources (matrice §2.2 du `SKILL.md`) dès que :
- un **seuil d'alerte chiffré** de capacité de désendettement ou de tout
  autre ratio est sur le point d'être énoncé ;
- la **liste exacte des ratios obligatoires** annexés au budget est
  invoquée comme exhaustive ;
- une **source de comparaison à la strate** est citée pour fonder une
  conclusion présentée comme engageante ;
- un **chiffre de dotation, de base fiscale ou de charge future** est
  intégré à une hypothèse de prospective sans être explicitement marqué
  comme hypothèse ;
- la question glisse du **cadrage budgétaire de la masse salariale** vers
  un **droit individuel ou un régime indemnitaire** (bascule `drh-fpt`
  obligatoire, `SKILL.md` §5.5).

---

## 8. Pièges & confusions fréquentes

1. Lire la **capacité de désendettement** sur un seul exercice, sans
   tendance ni retraitement des éléments exceptionnels.
2. Confondre **épargne de gestion**, **épargne brute** et **épargne
   nette** : chacune répond à une question différente (§5.1).
3. Présenter une **liste de ratios obligatoires** comme exhaustive sans
   l'avoir vérifiée à la source.
4. Bâtir une **prospective** sur des hypothèses implicites, non écrites ni
   datées, ou sans étape de sensibilité ni scénario de rupture.
5. Construire une **PPI** dont le plan de financement suppose une épargne
   nette supérieure à celle réellement projetée.
6. Comparer des ratios à la strate sans vérifier que la **définition** du
   ratio et le **périmètre** budgétaire sont identiques d'une source à
   l'autre.
7. Confondre **trésorerie nette** de gestion (FR − BFR) et **solde de
   caisse** instantané au comptable public.
8. Traiter la **masse salariale** comme un sujet purement RH dans cette
   branche, ou au contraire chiffrer un droit individuel ici plutôt que de
   basculer vers `drh-fpt`.
9. Confondre le **coefficient de mobilisation du potentiel fiscal** avec un
   simple taux de pression fiscale nominal.

---

## 9. Données / valeurs à vérifier

- **Jamais de mémoire** : tout seuil d'alerte de capacité de
  désendettement, la liste exacte des ratios obligatoires annexés au
  budget et leur présentation réglementaire, tout taux d'évolution
  utilisé en hypothèse de prospective (bases fiscales, dotations,
  inflation), toute donnée issue d'une base de comparaison à la strate
  (valeur et date d'actualisation).
- **Références structurelles stables, citables avec la réserve « à
  confirmer en version consolidée »** : le **CGCT**, pour les dispositions
  relatives aux documents et annexes budgétaires ; l'**instruction
  budgétaire et comptable M57**, pour l'architecture des agrégats
  comptables utilisés dans les calculs.
- **Aucun numéro d'article ni identifiant Légifrance
  (LEGIARTI/JORFTEXT/NOR)** n'est cité de mémoire dans cette branche : à
  défaut de vérification dans la session, s'en tenir au nom du texte et à
  la réserve.
- Toute donnée de masse salariale au-delà du cadrage global (GVT nommé,
  effet de noria nommé) relève de `drh-fpt` pour son détail — ne pas la
  vérifier ici, basculer.

---

## 10. Écrits & livrables

| Écrit | Nature | Compétence | Générateur / renvoi |
|---|---|---|---|
| Rapport d'orientation budgétaire (volet prospectif et pluriannuel) | Écrit de pilotage, support d'un débat obligatoire selon la strate | Exécutif présente, assemblée délibère du débat | `references/templates/rapport-orientation-budgetaire.md` |
| Note d'impact financier sur un scénario prospectif ou une PPI | Écrit de pilotage | DirFi | `references/templates/note-impact-financier.md` |
| Note de cadrage budgétaire (dont enveloppe globale de masse salariale) | Écrit de pilotage | DirFi | `references/templates/note-impact-financier.md` ou fiche interne, selon le destinataire |
| Fiche de procédure interne (méthode de construction de la prospective, du plan de financement PPI) | Écrit de procédure | DirFi | `references/templates/fiche-procedure-financiere.md` |
| Annexe de ratios obligatoires au budget | Annexe obligatoire | Services financiers | Formalisme renvoyé à `references/ecrits-financiers.md` ; contenu chiffré vérifié avant publication |

**Logique interactive** : toute production d'un rapport d'orientation
budgétaire ou d'une note de cadrage suit la règle `SKILL.md` §6 — poser les
questions une à une (exercice, périmètre, hypothèses, horizon), ne jamais
halluciner une donnée manquante, marquer `[INCOMPLET]` sinon.

---

## 11. Double échelle [risque / confiance]

| Sous-domaine | Risque | Confiance | Repère |
|---|---|---|---|
| Formules de la chaîne de l'épargne et des ratios de structure | Faible | Stable | Réponse directe, formule rappelée |
| Seuils d'alerte de capacité de désendettement | Élevé | À vérifier systématiquement | Jamais de seuil chiffré sans vérification |
| Liste des ratios obligatoires annexés au budget | Élevé | À vérifier | Citation obligatoire avant de la présenter comme complète |
| Hypothèses de prospective pluriannuelle | Moyen à élevé selon l'horizon | À vérifier, à documenter explicitement | Sensibilité et scénario de rupture obligatoires |
| Comparaison à la strate | Moyen | À vérifier (source, périmètre, définition) | Réserve méthodologique systématique |
| Masse salariale — cadrage budgétaire | Moyen | Stable sur l'enveloppe globale | Bascule `drh-fpt` obligatoire au-delà du cadrage |

---

## 12. Checklist de branche

1. **Exercice(s), périmètre et origine des données** levés avant tout
   calcul ou toute lecture de ratio ?
2. **Chaîne de l'épargne** posée dans l'ordre (gestion → brute → nette),
   jamais un seul niveau isolé présenté comme suffisant ?
3. **Capacité de désendettement** lue en tendance, jamais sur un seul
   exercice, et son seuil d'alerte marqué à vérifier plutôt qu'énoncé ?
4. Chaque **ratio de structure** posé avec sa formule exacte
   (numérateur / dénominateur), sans seuil chiffré non vérifié ?
5. **FR / BFR / TN** correctement distingués d'un solde de caisse
   instantané ?
6. **Prospective pluriannuelle** : les quatre étapes (tendanciel,
   hypothèses documentées, sensibilité, rupture) toutes présentes ?
7. **PPI** : plan de financement confronté à la capacité réellement
   projetée, pas à une capacité supposée ?
8. **Rétrospective** : retraitements de neutralisation appliqués avant
   toute comparaison inter-exercices ou à la strate ?
9. **Comparaison à la strate** assortie de sa réserve méthodologique
   (source, périmètre, définition) ?
10. **Masse salariale** : cadrage budgétaire seul traité ici ; dès qu'un
    droit individuel ou un régime indemnitaire apparaît, **bloc BASCULE**
    `drh-fpt` émis avant tout contenu statutaire, et `drh-fpt` nommé
    explicitement (`SKILL.md` §5.5) ?
11. Toute référence citée porte-t-elle sa provenance ou la réserve « à
    confirmer en version consolidée » (§9) ?
12. Couple **[risque / confiance]** (§11) indiqué quand utile à la
    décision ?
