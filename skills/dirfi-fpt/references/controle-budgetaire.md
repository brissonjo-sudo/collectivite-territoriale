# Brique posture — Contrôle budgétaire (v0.1.0)

> Brique transverse, pas une branche métier. Structure adaptée du gabarit
> `_gabarit-branche.md` : on conserve les 12 sections, dans l'ordre, en les
> pliant à une **procédure** plutôt qu'à un sous-domaine de gestion courante.
> C'est le fichier que le **garde-fou budgétaire** (`SKILL.md` §5.3) appelle
> dès qu'un acte budgétaire paraît irrégulier. Aucun numéro d'article, aucun
> délai en jours et aucun seuil chiffré n'est énoncé ici de mémoire : chacun
> est **nommé** puis marqué **« à vérifier »**, conformément à la matrice
> §2.2 du `SKILL.md` (toute case de cette procédure y relève d'une ligne
> « Oui »).

## 1. Périmètre / Exclusions

- **Périmètre** : la procédure de **contrôle budgétaire**, exercée par le
  représentant de l'État avec le concours de la **chambre régionale des
  comptes (CRC)**, dans les quatre cas de saisine limitativement prévus —
  budget non voté, budget en déséquilibre réel, compte administratif en
  déficit excessif, dépense obligatoire non ou insuffisamment inscrite — ainsi
  que son articulation avec le contrôle de légalité de droit commun appliqué
  aux actes budgétaires.
- **Exclusions** : la **responsabilité personnelle** d'un gestionnaire ou d'un
  comptable, la **gestion de fait** et les **contrôles non juridictionnels**
  (examen de la gestion) → `contentieux-financier.md`. Le **fond** de chaque
  procédure budgétaire courante (élaboration, vote, DM, compte administratif)
  → `references/budget-cycle.md`. Le **maniement irrégulier de deniers
  publics** hors circuit du comptable → garde-fou `SKILL.md` §5.2 (brique
  distincte : ce fichier traite l'**irrégularité de l'acte budgétaire**, pas
  l'irrégularité du **circuit d'encaissement/paiement**). La **recherche de
  jurisprudence** financière → `recherche-juridique`. Le **retour
  d'expérience** après un cas traité → `retex.md`.

---

## 2. Questions couvertes

- « Le budget n'a pas été voté à la date limite : que se passe-t-il ? »
- « Notre budget est-il en déséquilibre réel ? Qui le constate, et avec
  quelles conséquences ? »
- « Le compte administratif ressort en déficit : sommes-nous au-dessus du
  seuil qui déclenche la procédure ? »
- « Une dépense obligatoire n'a pas été inscrite (ou pas assez) : quelle est
  la procédure, et jusqu'où va-t-elle ? »
- « La chambre régionale des comptes est saisie : que peut encore faire
  l'assemblée délibérante ? »
- « Quelle différence entre cette procédure et le contrôle de légalité
  classique sur le même acte ? »
- « Nous avons détecté le problème en interne avant toute saisine : que
  faire, dans quel ordre, avec qui ? »

---

## 3. Arbre de traitement

`acte ou situation budgétaire signalé → qualifier lequel des quatre cas de
saisine est concerné (§5.1) → identifier l'autorité de saisine et le fait
générateur (§5.1) → vérifier si le délai de régularisation court encore
(§6.3) → engager la régularisation volontaire si elle est encore possible
(§6.3) → si la saisine est déjà intervenue, situer l'étape de la procédure
(§6.1) et les pouvoirs encore ouverts à l'assemblée (§6.2) → vérifier les
valeurs et délais mobilisés (§9) → écrit adapté (§10)`

**Réflexe impératif** : ne jamais répondre « rien à faire, le préfet
tranchera » — la marge de régularisation (§6.3) existe à presque tous les
stades tant que le préfet n'a pas rendu son acte de règlement. La qualifier
et la chiffrer en calendrier est le premier apport utile d'une direction des
finances.

---

## 4. Variables à lever

- **Strate et catégorie de la collectivité** (commune, EPCI, département,
  région) — conditionne l'autorité de saisine exacte, certains seuils et,
  parfois, la chambre territorialement compétente.
- **Nature du budget concerné** : budget principal ou budget annexe — un
  déséquilibre ou un déficit peut être propre à un budget annexe sans affecter
  le budget principal, et inversement une consolidation peut être exigée
  selon le cas.
- **Section en cause** : fonctionnement, investissement, ou les deux — la
  qualification du déséquilibre en dépend directement (§5.2).
- **Stade de la procédure** : simple détection interne, saisine déjà
  intervenue, avis de la CRC déjà rendu, ou règlement d'office déjà notifié —
  chaque stade ferme des options et en ouvre d'autres.
- **Existence d'un plan de redressement antérieur** ou d'une DM corrective
  déjà votée sur le même exercice.
- **Origine du blocage** pour un budget non voté : absence de majorité,
  absence de rapport d'orientation budgétaire préalable, délai matériel non
  tenu — la cause éclaire la voie de régularisation la plus rapide.
- **Nature exacte de la dépense contestée comme obligatoire** : certaines
  dépenses sont obligatoires par détermination de la loi, d'autres résultent
  d'une décision de justice ou d'un engagement contractuel — la qualification
  n'est jamais automatique (§5.4).

---

## 5. Règles métier

### 5.1 Les quatre cas de saisine

| Cas | Qualification | Autorité de saisine | Effet sur l'exécution | Voie de régularisation |
|---|---|---|---|---|
| **Budget non voté** dans les délais | Carence de l'assemblée délibérante à adopter le budget primitif avant la date limite | Représentant de l'État saisit la CRC | Exécution provisoire limitée dans l'attente (mécanisme de continuité, à vérifier dans `budget-cycle.md`) ; **l'assemblée est dessaisie dès la saisine** et jusqu'au règlement préfectoral (L. 1612-2 al. 2) | Vote du budget par l'assemblée **avant la saisine** uniquement ; après la saisine, la régularisation passe par le règlement préfectoral, sur la base des propositions de la CRC |
| Budget voté **en déséquilibre réel** | Non-respect de l'équilibre réel au sens de la notion définie en §5.2 | Représentant de l'État saisit la CRC dans un délai suivant la transmission du budget | Le budget reste en principe applicable jusqu'au règlement, sous réserve des effets propres à chaque étape (à vérifier) | Nouvelle délibération de l'assemblée reprenant les mesures de redressement proposées par la CRC, dans le délai imparti |
| **Compte administratif** en déficit au-delà du seuil légal | Le déficit constaté au compte administratif dépasse un seuil, exprimé en proportion des recettes de fonctionnement et variable selon la strate | Représentant de l'État saisit la CRC | Le budget primitif suivant doit intégrer les mesures de redressement ; jusque-là le déficit reste supporté par le budget en cours | Mesures de redressement inscrites au budget primitif de l'exercice suivant, sur proposition de la CRC |
| **Dépense obligatoire** non ou insuffisamment inscrite | Une dépense répondant à la notion de dépense obligatoire (§5.4) est absente du budget ou sous-dotée | Saisine ouverte à un cercle de personnes intéressées (créancier, préfet, comptable public, autres — à vérifier), qui saisissent la CRC | La dépense reste due indépendamment de son inscription ; le créancier n'est pas privé de sa créance | Mise en demeure d'inscrire les crédits ; à défaut, inscription d'office par le préfet ; à défaut d'exécution, mandatement d'office |

**Lecture transversale** : dans les trois premiers cas, la CRC **formule des
propositions ou un avis** que l'assemblée est invitée à suivre avant toute
substitution du préfet. Dans le quatrième cas, la logique est différente :
il ne s'agit pas d'un déséquilibre global mais d'une créance identifiée, et
la procédure va, en cas d'inertie persistante, jusqu'au **mandatement
d'office** — c'est-à-dire que le préfet peut se substituer non seulement à
l'assemblée (inscription) mais aussi à l'**ordonnateur** (mandatement).

### 5.2 La notion d'équilibre réel

L'équilibre réel ne se réduit pas à un solde global nul. Il suppose la
réunion de plusieurs conditions cumulatives :

- **Équilibre de chaque section** : la section de fonctionnement est
  équilibrée par ses seules recettes et dépenses de fonctionnement, la
  section d'investissement par ses seules recettes et dépenses
  d'investissement — un excédent de fonctionnement ne « compense » un
  déficit d'investissement qu'à travers les mouvements d'ordre prévus à cet
  effet (virement, affectation du résultat), pas par un simple rapprochement
  global des deux sections.
- **Évaluation sincère** des recettes et des dépenses : une recette
  surestimée ou une dépense sous-évaluée de façon manifeste rompt l'équilibre
  réel même si le document présente formellement un solde à zéro. La
  sincérité budgétaire porte sur le **réalisme** des prévisions, pas
  seulement sur leur présentation formelle.
- **Couverture du remboursement en capital de la dette par des ressources
  propres** : l'annuité en capital des emprunts (hors intérêts, qui relèvent
  du fonctionnement) doit être couverte par des ressources définitives de la
  section d'investissement — l'emprunt ne peut financer le remboursement d'un
  autre emprunt de manière déguisée.

**Conséquence pratique pour une direction des finances** : le contrôle de
l'équilibre réel est un contrôle de **fond**, pas seulement de présentation
comptable. Une maquette budgétaire qui « boucle » à zéro sur le total général
peut néanmoins être en déséquilibre réel si l'une de ces trois conditions
n'est pas remplie.

### 5.3 Le compte administratif en déficit

Le seuil au-delà duquel un déficit du compte administratif déclenche la
procédure est **variable selon la strate et la catégorie de la collectivité**
et s'exprime en proportion des recettes de fonctionnement. Ce taux ne se cite
**jamais** de mémoire (§9). Le déficit s'apprécie sur le compte administratif
(ou le compte financier unique selon le régime applicable), pas sur une
simple prévision d'exécution en cours d'exercice.

### 5.4 La notion de dépense obligatoire

Une dépense obligatoire est une dépense que la collectivité est **tenue
d'inscrire et d'exécuter**, indépendamment de sa volonté budgétaire :
dépenses résultant de l'exécution d'une décision de justice devenue
définitive, remboursement de la dette, cotisations et contributions
obligatoires, dépenses résultant d'une obligation légale ou réglementaire
précise, entretien de certains biens dont la loi impose la charge à la
collectivité. La liste exacte et ses contours (notamment pour les dépenses
d'origine contractuelle ou jurisprudentielle) **se vérifient**, cas par cas,
avant toute qualification ferme — une dépense « souhaitable » ou même
« engagée de fait » n'est pas nécessairement une dépense obligatoire au sens
de cette procédure.

---

## 6. Calculs et procédures

### 6.1 Déroulé procédural type

| Étape | Acteur | Contenu |
|---|---|---|
| 1. Fait générateur | Assemblée délibérante / ordonnateur | Non-vote, déséquilibre, déficit ou dépense non inscrite constaté |
| 2. Saisine | Représentant de l'État (ou, pour la dépense obligatoire, une personne intéressée) | Saisine formelle de la CRC, dans un délai à vérifier selon le cas |
| 3. Instruction | CRC | Instruction contradictoire ; échange avec l'ordonnateur ; délai d'instruction à vérifier |
| 4. Avis ou propositions | CRC | Propositions de redressement (cas 1 à 3) ou constat de dépense obligatoire et proposition d'inscription (cas 4) ; transmis à la collectivité et au représentant de l'État |
| 5. Délai de réponse de l'assemblée | Assemblée délibérante | Nouvelle délibération reprenant tout ou partie des propositions, dans un délai à vérifier |
| 6. Appréciation | CRC | Avis sur le caractère suffisant des mesures adoptées, le cas échéant |
| 7. Règlement par le préfet | Représentant de l'État | À défaut de délibération suffisante dans le délai, le préfet règle le budget (ou inscrit d'office la dépense, ou mandate d'office) et le rend exécutoire |

**Point de méthode** : chaque délai de cette chaîne (saisine, instruction,
réponse de l'assemblée) est **spécifique à la procédure de contrôle
budgétaire** et **distinct** des délais de droit commun du contrôle de
légalité (§6.4). Ne jamais transposer un délai de l'un à l'autre sans
vérification.

### 6.2 Effets de la saisine sur les pouvoirs budgétaires de l'assemblée

> **L'effet de la saisine n'est pas le même selon son fondement.** C'est le
> point le plus contre-intuitif de cette brique, et une règle unique énoncée
> pour « toute saisine de la CRC » est fausse dans un sens ou dans l'autre.

**Budget non voté dans les délais — l'assemblée est DESSAISIE.** À compter de
la saisine de la chambre régionale des comptes et jusqu'au règlement du budget
par le représentant de l'État, l'organe délibérant **ne peut adopter aucune
délibération sur le budget de l'exercice en cours** (CGCT, art. L. 1612-2,
al. 2 — référence et identifiant au registre `references-verifiees.md` §2,
vérifiés le 2026-09-15).

Conséquences opérationnelles, à opposer fermement :

- **Convoquer l'assemblée pour « voter le budget en urgence » après la saisine
  est une fausse solution** : la délibération serait prise par une autorité
  dessaisie, donc irrégulière. La fenêtre pour voter se referme à la saisine,
  pas au règlement préfectoral.
- Le dessaisissement porte sur le **budget de l'exercice en cours**. Il cesse
  au règlement du budget par le préfet.
- **Exception légale** : le mécanisme ne s'applique pas lorsque le défaut
  d'adoption résulte de l'absence de communication, avant une date limite, des
  informations indispensables à l'établissement du budget ; l'assemblée dispose
  alors d'un délai propre pour arrêter le budget (al. 3 du même article — délai
  à vérifier à la date d'usage).

**Budget voté en déséquilibre réel — l'assemblée reste COMPÉTENTE.** La
procédure repose au contraire sur elle : la chambre **demande une nouvelle
délibération**, que l'assemblée doit prendre dans le délai imparti. Le règlement
préfectoral n'intervient qu'à titre **subsidiaire**, si l'assemblée ne délibère
pas ou délibère insuffisamment (CGCT, art. L. 1612-5 — registre
`references-verifiees.md` §2, vérifié le 2026-09-15). Aucune clause de
dessaisissement n'y figure.

- Pendant l'instruction, l'exécution du budget en cours **se poursuit**
  selon les règles de continuité applicables (mécanisme de reconduction ou
  de crédits provisoires selon le cas — à vérifier dans `budget-cycle.md`),
  sauf disposition contraire propre au cas traité.
- Une fois le **règlement d'office** intervenu, l'assemblée est dessaisie
  **sur les seuls points réglés** par l'acte du préfet ; elle recouvre sa
  compétence pleine et entière pour toute décision modificative ultérieure
  qui respecte l'équilibre ainsi fixé.
- Pour la dépense obligatoire, le **mandatement d'office** dessaisit,
  ponctuellement et pour cette seule dépense, l'**ordonnateur** lui-même —
  cas le plus intrusif des quatre, car il touche à l'exécution, pas
  seulement à l'acte budgétaire.

### 6.3 Marge de régularisation

- La marge la plus large existe **avant toute saisine** : une direction des
  finances qui détecte l'un des quatre cas en interne peut proposer une
  décision modificative corrective, un plan de redressement volontaire ou
  l'inscription spontanée de la dépense manquante, sans attendre l'ouverture
  formelle de la procédure.
- Après saisine, la marge se **rétrécit à chaque étape** (§6.1) mais ne
  disparaît qu'au moment où le préfet rend son acte de règlement, d'inscription
  d'office ou de mandatement d'office exécutoire.
- Une régularisation **partielle** peut ne pas suffire : la CRC apprécie si
  les mesures adoptées répondent effectivement au manquement constaté (retour
  à l'équilibre réel effectif, résorption du déficit dans les proportions
  attendues, inscription intégrale de la dépense).

### 6.4 Articulation avec le contrôle de légalité de droit commun

- Les actes budgétaires (délibération de budget primitif, décision
  modificative, délibération arrêtant le compte administratif) figurent
  parmi les actes **transmissibles** au représentant de l'État et deviennent
  **exécutoires** après publicité et transmission, selon le régime de droit
  commun applicable aux actes des collectivités (`references/budget-cycle.md`
  pour le détail par type d'acte).
- Le **contrôle de légalité de droit commun** porte sur la **légalité** de
  l'acte (compétence, procédure, base légale, contenu) et s'exerce par la
  voie du **déféré préfectoral** au tribunal administratif, dans un délai de
  droit commun distinct de ceux de la présente procédure.
- Le **contrôle budgétaire** porte sur des motifs **limitativement
  énumérés** (les quatre cas de §5.1) et ne passe **pas**, à ce stade, par le
  juge administratif : il passe par la CRC puis, le cas échéant, par le
  pouvoir de substitution du préfet. Seul l'**acte final de règlement** du
  préfet est, lui, susceptible d'un recours contentieux devant le juge
  administratif.
- **Les deux contrôles peuvent se cumuler** sur un même acte : un budget
  peut être à la fois déféré pour un vice de forme et, indépendamment, saisi
  au titre du déséquilibre réel. Traiter les deux volets **séparément**, sans
  supposer que l'un couvre l'autre.

---

## 7. Déclencheurs de vérification

Appliquer systématiquement le socle-sources (`SKILL.md` §5.4,
`references/socle-sources-verification.md`) dès que la réponse porte sur :

- la **date limite** de vote du budget primitif ;
- le **délai** de saisine de la CRC par le préfet, quel que soit le cas ;
- le **délai d'instruction** de la CRC et le **délai de réponse** laissé à
  l'assemblée ;
- le **seuil** de déficit du compte administratif déclenchant la procédure,
  et sa variation selon la strate ;
- la **liste exacte** des dépenses obligatoires et la qualification d'une
  dépense précise comme telle ;
- le **délai** ouvert à l'assemblée pour régulariser après mise en demeure ;
- toute **jurisprudence** relative à la qualification de l'une des quatre
  situations → `recherche-juridique` ;
- toute **réforme récente** du cadre budgétaire et comptable des
  collectivités (M57, décret GBCP, loi de finances de l'année).

---

## 8. Pièges & confusions fréquentes

1. Confondre le **contrôle budgétaire** (quatre cas limitatifs, CRC puis
   préfet) et le **contrôle de légalité de droit commun** (tout motif de
   légalité, déféré direct au TA) — deux procédures cumulables, jamais
   substituables l'une à l'autre (§6.4).
2. Énoncer une règle **unique** sur l'effet de la saisine — faux dans un sens
   ou dans l'autre selon le cas. **Budget non voté** : l'assemblée est
   **dessaisie dès la saisine** et jusqu'au règlement préfectoral ; proposer de
   la convoquer pour voter en urgence est une fausse solution, la délibération
   serait irrégulière. **Budget en déséquilibre réel** : l'assemblée reste au
   contraire **pleinement compétente**, la chambre lui demandant une nouvelle
   délibération (§6.2).
3. Affirmer qu'un budget qui « boucle à zéro » est nécessairement en
   équilibre réel — faux si l'une des trois conditions cumulatives de §5.2
   n'est pas remplie (sincérité, équilibre par section, couverture du capital
   de la dette).
4. Confondre le **déficit du compte administratif** (constaté a posteriori
   sur l'exécution) et le **déséquilibre du budget primitif** (constaté a
   priori sur la prévision) — deux cas distincts, deux temporalités
   distinctes, deux seuils/critères distincts.
5. Considérer qu'une dépense « importante » ou « urgente » est
   automatiquement une **dépense obligatoire** au sens de cette procédure —
   la qualification est stricte et se vérifie (§5.4).
6. Oublier que le **mandatement d'office** (cas de la dépense obligatoire)
   touche l'ordonnateur, alors que le **règlement d'office du budget** (les
   trois autres cas) touche l'assemblée — deux niveaux de substitution
   différents.
7. Traiter la détection interne d'un déséquilibre comme une fatalité —
   omettre de proposer la régularisation volontaire, qui reste la voie la
   plus rapide et la moins risquée pour la collectivité.
8. Citer un délai ou un seuil de mémoire « parce que c'est classique » — toute
   valeur de cette procédure est une ligne « Oui » de la matrice §2.2 :
   aucune exception de notoriété.

---

## 9. Données / valeurs à vérifier

Aucune des valeurs suivantes n'est chiffrée dans ce document. Toutes sont à
confirmer sur source officielle avant tout usage en acte, avec leur date de
référence :

- **Date limite** de vote du budget primitif (et régime particulier l'année
  d'un renouvellement de l'assemblée).
- **Délai de saisine** de la CRC par le représentant de l'État, pour chacun
  des quatre cas.
- **Délai d'instruction** de la CRC et **délai de réponse** laissé à
  l'assemblée délibérante après transmission des propositions ou de l'avis.
- **Seuil de déficit** du compte administratif déclenchant la procédure,
  exprimé en proportion des recettes de fonctionnement, et sa **variation
  selon la strate** de collectivité.
- **Liste exacte des dépenses obligatoires** et ses évolutions.
- **Délai** ouvert après mise en demeure avant inscription d'office, et
  délai avant mandatement d'office.
- **Références structurelles stables**, citables uniquement avec la réserve
  « à confirmer en version consolidée » : le **code général des collectivités
  territoriales (CGCT)**, dont les dispositions relatives au contrôle
  budgétaire ; le **code des juridictions financières (CJF)**, pour
  l'organisation de la CRC ; le **décret relatif à la gestion budgétaire et
  comptable publique (GBCP)** — aucun de ces textes n'est cité ici avec un
  numéro d'article précis, faute de vérification dans la présente session.

---

## 10. Écrits & livrables

- **Note d'alerte interne** (DirFi → DGS → exécutif), dès la détection d'un
  des quatre cas, datée et tracée : constat, chiffrage, options de
  régularisation, calendrier. Format libre, à documenter dans le dossier de
  suivi budgétaire.
- **Décision modificative corrective** — voir `references/budget-cycle.md`
  et, pour la production de l'acte, `references/templates/deliberation-budgetaire.md`
  : vérifier la compétence de l'assemblée, les mentions obligatoires et la
  cohérence avec les mesures attendues par la CRC si la saisine est déjà
  intervenue.
- **Réponse aux propositions de la CRC** — dossier de délibération
  reprenant ou motivant l'écart aux mesures proposées ; joindre les pièces
  justificatives de sincérité (hypothèses de recettes, plan de trésorerie).
- **Note d'impact financier** d'un plan de redressement —
  `references/templates/note-impact-financier.md`.
- **Acte soumis au contrôle de légalité** : toute délibération produite dans
  ce cadre reste soumise, en parallèle, aux règles de transmission et de
  caractère exécutoire de droit commun (§6.4) — ne pas les négliger au motif
  que la procédure budgétaire est déjà engagée.

---

## 11. Double échelle [risque / confiance]

| Sous-cas | Risque | Confiance |
|---|---|---|
| Budget non voté à la date limite | Élevé | Stable sur le principe, à vérifier sur les dates |
| Déséquilibre réel (constat) | Élevé | Stable sur la notion (§5.2), à vérifier sur les délais |
| Déficit du compte administratif | Élevé à critique selon l'ampleur | Stable sur le principe, à vérifier sur le seuil exact |
| Dépense obligatoire non inscrite | Élevé à critique (le créancier reste titulaire de sa créance) | À vérifier sur la qualification et sur les délais de chaque étape |
| Articulation contrôle budgétaire / contrôle de légalité | Moyen | Stable sur la distinction de principe (§6.4) |
| Détection interne avant saisine, régularisation volontaire engagée | Moyen (décroît si la régularisation est rapide) | Stable sur la méthode, à vérifier sur les délais restants |

---

## 12. Checklist de branche

1. Le cas de saisine a-t-il été **qualifié précisément** parmi les quatre
   (§5.1), sans les mélanger ?
2. L'**autorité de saisine** et l'étape exacte de la procédure (§6.1)
   ont-elles été identifiées ?
3. La **marge de régularisation** encore ouverte (§6.3) a-t-elle été
   chiffrée en calendrier, pas seulement mentionnée dans l'absolu ?
4. Pour un déséquilibre, les **trois conditions de l'équilibre réel** (§5.2)
   ont-elles été testées une à une, pas seulement le solde global ?
5. Pour une dépense obligatoire, la **qualification** a-t-elle été vérifiée
   avant d'affirmer le caractère obligatoire (§5.4) ?
6. L'**articulation avec le contrôle de légalité de droit commun** (§6.4) a-t-elle
   été signalée si l'acte est aussi transmissible à ce titre ?
7. Aucun **délai ni seuil** de cette procédure n'a-t-il été énoncé sans la
   mention « à vérifier » (§9) ?
8. La **conduite interne** (note d'alerte, régularisation volontaire,
   traçabilité) a-t-elle été proposée avant toute résignation à la
   procédure contrainte ?
9. Le **garde-fou budgétaire** (`SKILL.md` §5.3) a-t-il précédé tout contenu
   métier si le déclencheur était déjà avéré au moment de la question ?
10. Un éventuel **maniement de fonds hors circuit du comptable** envisagé
    pour « reboucler » artificiellement le budget a-t-il été écarté et, le
    cas échéant, le garde-fou `SKILL.md` §5.2 opposé ?
11. Couple **[risque / confiance]** (§11) restitué pour le sous-cas traité ?
12. Cas journalisable (nouveau motif de déséquilibre, écrit récurrent,
    lacune de méthode) proposé pour `JOURNAL.md` (`SKILL.md` §9) ?

[risque / confiance] : risque élevé à critique par construction — cette
brique est appelée par un garde-fou (`SKILL.md` §5.3) — confiance stable sur
les notions et la mécanique procédurale, systématiquement à vérifier sur
tout délai, seuil et référence d'article avant citation ou usage en acte.
