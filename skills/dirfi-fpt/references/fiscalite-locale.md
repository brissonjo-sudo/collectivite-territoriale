# Branche — Fiscalité locale (v1.0.0)

> Structure conforme à `_gabarit-branche.md`. Aucun taux, aucun seuil, aucun
> coefficient de revalorisation et aucun numéro d'article n'est cité de
> mémoire : seules les **règles**, les **méthodes** et la consigne de
> vérifier la version en vigueur figurent ci-dessous.

## 1. Périmètre / Exclusions

- **Périmètre** : panorama des impositions directes locales perçues par le
  bloc communal et les autres strates — taxe foncière sur les propriétés
  bâties (TFPB), taxe foncière sur les propriétés non bâties (TFPNB),
  cotisation foncière des entreprises (CFE), impositions forfaitaires sur les
  entreprises de réseaux (IFER), taxe d'habitation sur les résidences
  secondaires (THRS), taxe d'enlèvement des ordures ménagères (TEOM), taxe de
  séjour, taxe locale sur la publicité extérieure (TLPE) ; compétence et
  calendrier de vote des taux et des tarifs ; règles de lien entre les taux ;
  bases d'imposition, revalorisation forfaitaire, rôles ; abattements et
  exonérations ; états fiscaux notifiés ; commission communale des impôts
  directs (CCID) ; reversements et attribution de compensation en
  intercommunalité ; contentieux fiscal et dégrèvements.
- **Exclusions** : les **dotations de l'État et la péréquation** →
  `dotations-perequation.md` ; la **tarification des services publics** (non
  fiscale, redevance pour service rendu) → `execution-recette.md` ;
  l'**émission et le recouvrement des titres** → `execution-recette.md`.

---

## 2. Questions couvertes

- Quelle imposition s'applique à tel bien, tel local ou telle activité, et
  qui la perçoit (commune, EPCI, autre strate) ?
- Qui vote le taux ou le tarif, sur quel support, et à quelle date limite ?
- Comment la base d'imposition est-elle établie, revalorisée, corrigée par
  rôle supplémentaire ?
- Quelles exonérations sont mobilisables, sur délibération ou de droit, et
  sont-elles compensées par l'État ?
- Comment lire et exploiter l'état fiscal notifié à la collectivité pour
  construire le budget ?
- Quel est le rôle de la commission communale des impôts directs ?
- Comment se calcule et se révise l'attribution de compensation entre un
  EPCI et ses communes membres ?
- Comment traiter une réclamation contentieuse ou un dégrèvement, et quel en
  est l'effet budgétaire ?

---

## 3. Arbre de traitement

`qualifier l'imposition concernée (§5.1) → identifier la strate bénéficiaire
(bloc communal / EPCI / autre) → objet de la question : taux, tarif, base,
exonération ou contentieux → autorité compétente (assemblée délibérante /
exécutif / DDFIP-service des impôts) → règle de lien ou plafond applicable
(§5.3) → déclencheur de vérification (§7) → écrit ou livrable (§10)`

Toujours commencer par distinguer une **imposition** (base légale fiscale,
vote de taux) d'une **redevance** ou d'un **tarif de service public** (base
contractuelle ou réglementaire non fiscale) : la confusion est fréquente pour
les déchets (TEOM/REOM) et pour l'eau ou l'assainissement.

---

## 4. Variables à lever

- **Strate de collectivité** : commune, EPCI à fiscalité propre, département,
  région (compétence fiscale résiduelle sur les impositions directes
  locales).
- **Régime fiscal de l'EPCI** : fiscalité professionnelle unique (FPU) ou
  fiscalité additionnelle — conditionne l'existence même d'une attribution de
  compensation et la répartition de la CFE.
- **Compétence exercée ou transférée** : gestion des déchets (TEOM/REOM),
  compétence tourisme (taxe de séjour) — la taxe suit la compétence.
- **Exercice et année de référence des bases** : la base d'une année
  d'imposition se réfère à une situation constatée à une date antérieure ; ne
  jamais raisonner sur l'exercice courant sans vérifier l'année de référence.
- **Délibération antérieure** encore en vigueur, à renouveler, ou tombée en
  désuétude (durée de validité propre à chaque exonération ou tarif).
- **Existence d'un pacte financier et fiscal** ou d'une commission locale
  d'évaluation des charges transférées (CLECT) conditionnant l'attribution de
  compensation.
- **Nature du redevable** : personne physique, entreprise, propriétaire ou
  occupant — certaines impositions distinguent strictement les deux.

---

## 5. Règles métier

### 5.1 Panorama des impositions directes locales

| Imposition | Nature de l'assiette | Redevable type | Bénéficiaire type |
|---|---|---|---|
| TFPB | Valeur locative cadastrale des propriétés bâties | Propriétaire | Bloc communal (et autres strates selon réforme) |
| TFPNB | Valeur locative cadastrale des propriétés non bâties | Propriétaire | Bloc communal |
| CFE | Valeur locative des biens professionnels | Entreprise, professionnel | EPCI (FPU) ou commune (fiscalité additionnelle) |
| IFER | Valeur forfaitaire selon la nature de l'installation | Exploitant d'un réseau ou d'une installation visée | Bloc communal, département, région selon la composante |
| THRS | Valeur locative du local affecté à la résidence secondaire | Occupant (propriétaire ou locataire) | Bloc communal |
| TEOM | Valeur locative des propriétés bâties, assise comme la TFPB | Propriétaire (répercutée sur l'occupant selon le cas) | Commune ou EPCI compétent en gestion des déchets |
| Taxe de séjour | Fréquentation touristique (par nuitée ou au réel/forfait) | Touriste, collectée par l'hébergeur | Commune ou EPCI compétent tourisme |
| TLPE | Surface des supports publicitaires | Exploitant du support | Commune ou EPCI |

Ce tableau qualifie la **nature** de chaque imposition ; **aucun taux, aucun
tarif et aucun montant** ne s'en déduisent sans vérification (§9).

### 5.2 Compétence et calendrier de vote des taux et des tarifs

- **Autorité compétente** : l'**assemblée délibérante** vote chaque année les
  taux des impositions directes locales et les tarifs des taxes propres
  (TEOM, taxe de séjour, TLPE), par délibération distincte du budget.
- **Date limite de vote** : fixée chaque année par le calendrier budgétaire
  et fiscal — **à vérifier avant toute annonce de délai**, y compris pour un
  exercice déjà traité l'année précédente.
- **Articulation avec le budget** : les taux sont en principe arrêtés avant
  ou concomitamment au vote du budget primitif, pour permettre l'inscription
  du produit attendu ; un vote tardif ou une absence de délibération entraîne
  la reconduction des taux de l'exercice antérieur selon la règle applicable
  — **à vérifier**.
- **Tarifs propres** (TEOM, taxe de séjour, TLPE) : compétence de la même
  assemblée, mais texte de référence et calendrier propres à chacun ; ne pas
  présumer un calendrier unique pour toutes les impositions.

### 5.3 Règles de lien entre les taux

- **Principe du lien** : la variation du taux de la cotisation foncière des
  entreprises est encadrée par référence à la variation du ou des taux des
  impositions ménages (méthode de plafonnement de la hausse relative), afin
  d'éviter un report de la pression fiscale sur les seules entreprises.
- **Assouplissement possible** : ce lien peut être assoupli par délibération
  spécifique de l'assemblée délibérante, dans des conditions et limites
  fixées par le texte — **méthode à vérifier**, jamais de coefficient chiffré
  de mémoire.
- **Vigilance** : toute simulation de hausse ciblée d'un taux professionnel
  doit tester la règle de lien avant d'être présentée comme réalisable.

### 5.4 Bases d'imposition, revalorisation, rôles

- **Valeur locative cadastrale** : socle de la plupart des impositions
  directes locales (TFPB, TFPNB, CFE, THRS) ; méthode d'évaluation propre à
  chaque nature de local, distincte pour les locaux professionnels et les
  locaux d'habitation.
- **Revalorisation forfaitaire annuelle** : les valeurs locatives sont
  revalorisées chaque année par un coefficient national ; **ce coefficient
  est une valeur volatile** — jamais citée de mémoire, jamais sans date
  d'effet (§5.4 point 2 du `SKILL.md`).
- **Rôle général** : émission annuelle de l'imposition sur la base arrêtée
  pour l'exercice.
- **Rôle supplémentaire** : rectification d'une erreur, omission ou
  changement constaté après l'émission du rôle général ; effet sur
  l'exercice de rattachement de la recette à vérifier avec `execution-recette.md`.

### 5.5 Abattements et exonérations

- **Distinction structurante** :
  - **facultatives sur délibération** — nécessitent un acte de l'assemblée
    délibérante, produisent effet pour une durée et une portée définies par
    la délibération, révisables ou reconductibles selon le texte ;
  - **de droit** — s'appliquent sans délibération, dès lors que les
    conditions légales sont réunies.
- **Compensées ou non par l'État** : une exonération peut donner lieu à une
  compensation budgétaire (à distinguer d'une recette fiscale réelle) ou
  rester à la charge nette de la collectivité. Vérifier systématiquement ce
  régime avant toute simulation d'impact budgétaire — variable d'ajustement
  possible (voir `dotations-perequation.md` §5.8).
- **Portée temporelle** : une exonération facultative a une durée
  d'application et des règles de renouvellement propres ; ne jamais présumer
  sa reconduction tacite sans vérifier le texte support.

### 5.6 États fiscaux notifiés à la collectivité

- **Contenu** : bases prévisionnelles par imposition, taux appliqués
  l'exercice précédent, simulation de produit à taux constant, éléments
  nécessaires à l'inscription budgétaire de la recette fiscale.
- **Exploitation** : comparer les bases notifiées à celles de l'exercice
  précédent, identifier les écarts significatifs (nouvelle construction,
  fermeture d'activité, rôle supplémentaire), croiser avec la décision de
  vote de taux avant inscription au budget.
- **Vigilance** : la dénomination exacte et le support de cet état (papier
  ou dématérialisé) évoluent ; vérifier le canal de notification en vigueur
  auprès du service compétent (DDFIP) avant toute procédure.

### 5.7 Commission communale des impôts directs (CCID)

- **Rôle** : instance consultative associée à la détermination des valeurs
  locatives des locaux, notamment pour les mises à jour et les
  classifications.
- **Composition** : commissaires désignés selon une procédure propre,
  distincte de la composition de l'assemblée délibérante — **à vérifier**
  avant toute description précise.
- **Portée** : avis consultatif ; ne se substitue pas à la compétence
  fiscale de l'assemblée délibérante sur le vote des taux.

### 5.8 Reversements et attribution de compensation en intercommunalité

- **Attribution de compensation (AC)** : mécanisme de neutralité budgétaire
  lors du passage à la fiscalité professionnelle unique ou d'un transfert de
  compétence, destiné à corriger les effets du transfert de la fiscalité
  professionnelle entre l'EPCI et ses communes membres.
- **Rôle de la CLECT** : la commission locale d'évaluation des charges
  transférées évalue le coût net des charges transférées, sur la base
  duquel l'AC est déterminée ou révisée.
- **Révision** : l'AC peut être révisée par délibérations concordantes de
  l'EPCI et des communes concernées, dans les conditions fixées par le
  texte — **à vérifier**, notamment la majorité requise.
- **Distinction avec la dotation de solidarité communautaire** : l'AC
  neutralise un transfert de charges ; la dotation de solidarité
  communautaire est un choix de péréquation interne à l'intercommunalité
  (voir `dotations-perequation.md`) — ne pas confondre les deux mécanismes.

### 5.9 Contentieux fiscal et dégrèvements

- **Réclamation du contribuable** : portée devant l'administration fiscale
  (DDFIP), non devant la collectivité, qui n'est pas décisionnaire du
  dégrèvement.
- **Dégrèvement** : décidé par l'État ; peut être total ou partiel, avec un
  effet variable sur la recette communale selon que le dégrèvement est pris
  en charge par l'État ou vient en déduction du produit perçu par la
  collectivité — **à vérifier au cas par cas**.
- **Rôle de l'ordonnateur** : suivre l'impact budgétaire des dégrèvements
  notifiés, ne pas se substituer à l'administration fiscale sur le fond du
  contentieux, orienter le contribuable vers la voie de réclamation fiscale
  compétente.

---

## 6. Calculs et procédures

- **Formule générale du produit attendu** : `produit = base nette × taux`,
  imposition par imposition. Poser la méthode, jamais le résultat sur une
  base ou un taux non vérifiés à la source.
- **Procédure annuelle de vote des taux** :
  1. réception de l'état fiscal notifié (§5.6) ;
  2. simulation du produit à taux constant et à taux modifié ;
  3. test de la règle de lien (§5.3) si une variation différenciée est
     envisagée ;
  4. délibération de l'assemblée dans le délai applicable (à vérifier) ;
  5. transmission de la délibération au contrôle de légalité et au service
     des impôts.
- **Procédure de délibération d'exonération facultative** : détermination de
  la portée (quelle imposition, quels biens ou quels redevables), de la
  durée d'application, délibération avant l'échéance fixée par le texte pour
  produire effet sur l'exercice suivant, transmission.
- **Procédure de calcul de l'attribution de compensation** : rapport de la
  CLECT évaluant les charges transférées, délibérations concordantes de
  l'EPCI et des communes, notification du montant, révision selon la
  procédure applicable.
- **Signaler comme données manquantes** : le montant exact des bases, le
  taux voté l'exercice précédent, la date limite de vote de l'exercice en
  cours, la portée exacte d'une exonération déjà votée — ne jamais les
  déduire par défaut.

---

## 7. Déclencheurs de vérification

Appliquer le socle-sources (`SKILL.md` §5.4, matrice §2.2) avant de conclure
dès que :
- un **taux, un tarif, un coefficient de revalorisation ou un montant** doit
  être cité ;
- une **date limite de vote** ou un **délai de délibération** est en jeu ;
- une **condition d'éligibilité à une exonération** doit être qualifiée ;
- la **compétence** (assemblée / exécutif / DDFIP) est incertaine sur un
  point précis ;
- un **contentieux fiscal** ou une **jurisprudence** (CE, CRC) est invoqué ;
- une **réforme récente** (loi de finances de l'année) touche l'une de ces
  impositions.

---

## 8. Pièges & confusions fréquentes

1. Confondre **exonération facultative** (sur délibération, portée choisie)
   et **exonération de droit** (automatique) — impact différent sur la
   compensation budgétaire.
2. Voter le taux **après le délai limite** sans vérifier l'effet exact
   (reconduction des taux antérieurs ou autre règle).
3. Modifier un taux professionnel sans tester la **règle de lien** (§5.3).
4. Confondre la **TEOM** (imposition, assise comme la TFPB) et la **REOM**
   (redevance pour service rendu, non fiscale) → la REOM relève de
   `execution-recette.md`, pas de cette branche.
5. Confondre l'**attribution de compensation** (neutralité budgétaire d'un
   transfert) et la **dotation de solidarité communautaire** (choix de
   péréquation) — voir `dotations-perequation.md`.
6. Traiter un **dégrèvement** comme une décision de la collectivité, alors
   qu'il relève de l'administration fiscale.
7. Présenter un **rôle supplémentaire** comme relevant du même exercice de
   rattachement que le rôle général sans vérifier la règle applicable.
8. Citer un **taux, un tarif ou un montant de mémoire**, y compris pour un
   exercice déjà traité l'an dernier.

---

## 9. Données / valeurs à vérifier

- **Code général des impôts (CGI)** — fondement de l'assiette, des taux
  plafonds, des exonérations et du régime de chaque imposition directe
  locale (« à confirmer en version consolidée » ; aucun article cité de
  mémoire dans cette branche).
- **Code général des collectivités territoriales (CGCT)** — compétence de
  l'assemblée délibérante en matière fiscale (« à confirmer en version
  consolidée »).
- **Taux plafonds et règle de lien entre les taux** — valeurs volatiles,
  jamais citées sans vérification et sans date d'effet.
- **Coefficient annuel de revalorisation forfaitaire des valeurs locatives**
  — valeur volatile, propre à chaque exercice.
- **Tarifs de la taxe de séjour, de la TLPE et de la TEOM** — valeurs
  votées localement, à vérifier délibération par délibération.
- **Date limite annuelle de vote des taux et des tarifs** — fixée chaque
  année, à revérifier systématiquement.
- **Seuils et conditions d'éligibilité aux exonérations facultatives et de
  droit** — à vérifier avant toute délibération ou toute simulation.
- **Modalités précises de composition et de désignation de la CCID** — à
  vérifier avant toute description opérationnelle.
- **Règles de majorité pour la révision de l'attribution de compensation**
  — à vérifier avant toute procédure.
- **Jurisprudence relative à la requalification d'une AC ou à un
  contentieux fiscal** — relève de `recherche-juridique` en cas de doute.

---

## 10. Écrits & livrables

1. **Délibération fiscale** (vote des taux, institution ou modification d'un
   tarif, exonération facultative) — utiliser le gabarit de
   `templates/deliberation-budgetaire.md` en l'adaptant à l'objet fiscal ;
   vérifier la compétence, les mentions obligatoires et la transmission au
   contrôle de légalité (`controle-budgetaire.md`).
2. **Note d'impact financier** (simulation d'une variation de taux, effet
   d'une exonération nouvelle, révision d'une attribution de compensation)
   → `templates/note-impact-financier.md`.
3. **Fiche de procédure financière** (exploitation de l'état fiscal notifié,
   contrôle des rôles supplémentaires) → `templates/fiche-procedure-financiere.md`.
4. **Réponse à réclamation ou signalement de contentieux fiscal** : aucun
   générateur dédié dans le socle actuel — signaler l'absence de gabarit et
   construire la réponse au cas par cas, en orientant le contribuable vers
   la voie de réclamation fiscale compétente.

---

## 11. Double échelle [risque / confiance]

| Sous-domaine | Risque | Confiance |
|---|---|---|
| Vote annuel des taux dans le délai | Élevé (nullité ou reconduction en cas d'erreur) | Stable dans son principe, délai à vérifier chaque exercice |
| Règle de lien entre les taux | Moyen à élevé | Stable dans son principe, modalités d'assouplissement à vérifier |
| Exonération facultative | Moyen | À vérifier (portée et durée par délibération) |
| Exonération de droit et compensation | Moyen à élevé | À vérifier (régime de compensation évolutif) |
| Attribution de compensation et CLECT | Élevé | Stable dans son principe, règles de révision à vérifier |
| Contentieux fiscal et dégrèvement | Moyen | Stable dans son principe (hors compétence de la collectivité) |
| Exploitation de l'état fiscal notifié | Faible à moyen | Stable |

---

## 12. Checklist de branche

1. Imposition exactement qualifiée et distinguée d'une redevance non fiscale
   (§3, §8 piège 4) ?
2. Strate bénéficiaire et autorité compétente identifiées sans confusion ?
3. Règle de lien testée avant toute simulation de variation différenciée de
   taux (§5.3) ?
4. Exonération qualifiée comme facultative ou de droit, régime de
   compensation précisé ou signalé à vérifier (§5.5) ?
5. Aucun taux, tarif, coefficient ou montant énoncé sans vérification ou
   sans réserve explicite (§9) ?
6. Attribution de compensation distinguée de la dotation de solidarité
   communautaire, renvoi fait à `dotations-perequation.md` si pertinent ?
7. Dégrèvement traité comme relevant de l'administration fiscale, pas de la
   collectivité ?
8. Écrit demandé produit via le gabarit approprié, ou absence de gabarit
   signalée explicitement (§10) ?
9. Délai de vote et calendrier fiscal signalés comme « à vérifier », jamais
   donnés de mémoire ?
