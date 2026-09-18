# Branche — Exécution de la dépense (v0.1.0)

> Structure conforme à `_gabarit-branche.md`. Aucun numéro d'article, aucun
> délai chiffré (délai global de paiement, taux d'intérêts moratoires), aucun
> seuil ni montant n'est cité de mémoire : seules les **règles**, les
> **méthodes** et la consigne de vérifier la version en vigueur figurent ici.

## 1. Périmètre / Exclusions

- **Périmètre** : le **circuit d'exécution de la dépense** une fois les
  crédits ouverts — les trois temps de l'ordonnateur (engagement,
  liquidation, mandatement) et le paiement par le comptable, le service fait,
  les pièces justificatives, le délai global de paiement et les intérêts
  moratoires, la dématérialisation, les dépenses avant le vote du budget, les
  dépenses obligatoires, les avances et acomptes, les régies d'avances, les
  dépenses imprévues et le contrôle allégé en partenariat.
- **Exclusions** : le **volet financier des marchés publics** (révision de
  prix, retenue de garantie, pénalités) → `commande-publique-financiere.md` ;
  l'**organisation du contrôle interne** (cartographie des risques, plan de
  contrôle) → `controle-interne-financier.md` ; l'**ouverture des crédits**
  et le calendrier budgétaire → `budget-cycle.md` ; les **règles
  d'imputation** → `nomenclature-m57.md`.

---

## 2. Questions couvertes

- Quels sont les trois temps de l'exécution de la dépense côté ordonnateur, et
  qu'ajoute le comptable ?
- Qu'est-ce que le service fait, et comment le certifier ?
- Quelles pièces justificatives exiger pour tel type de dépense, et que
  risque un mandat qui en est dépourvu ?
- Le comptable peut-il rejeter un mandat, pour quels motifs, et que peut faire
  l'ordonnateur face à un rejet ?
- Qu'est-ce que le délai global de paiement, et que déclenchent des intérêts
  moratoires ?
- Quelles obligations de dématérialisation pèsent sur l'ordonnateur et le
  comptable (flux, signature) ?
- Peut-on payer une dépense avant le vote du budget primitif, et à quelles
  conditions ?
- Qu'est-ce qu'une dépense obligatoire, et que se passe-t-il si elle n'est pas
  couverte par des crédits ?
- Comment fonctionnent les avances, les acomptes et les régies d'avances ?
- À quoi sert le chapitre des dépenses imprévues, et quelle est sa limite ?
- Qu'est-ce que le contrôle allégé en partenariat entre ordonnateur et
  comptable ?

---

## 3. Arbre de traitement

`identifier le stade de la dépense (engagement / liquidation / mandatement /
paiement) → vérifier l'existence et le montant du crédit disponible → vérifier
le service fait et sa certification → identifier les pièces justificatives
requises pour ce type de dépense → contrôler la cohérence des pièces avec
l'engagement → tester un motif de rejet éventuel côté comptable → si rejet,
qualifier réquisition possible ou non (§5.3) → vérifier le respect du délai
global de paiement → détecter un maniement de fonds hors circuit (garde-fou
§5.2 SKILL) → orienter vers l'écrit/le contrôle interne (§10)`.

Ne jamais recommander un mandatement sans avoir vérifié, dans cet ordre, le
crédit disponible, le service fait et les pièces justificatives : l'ordre
inverse expose à un rejet du comptable évitable.

---

## 4. Variables à lever

- **Stade de l'exercice** : avant ou après le vote du budget primitif —
  conditionne le régime applicable (§5.6).
- **Nature de la dépense** : fonctionnement ou investissement, obligatoire ou
  non, régie ou marché, avance ou acompte — chaque nature a ses pièces
  justificatives propres.
- **Niveau de crédit disponible** sur le chapitre/article concerné au moment
  de l'engagement (→ `budget-cycle.md` §5.5 et §5.9 pour la fongibilité).
- **Régime de dématérialisation** effectivement en place (PES V2, Chorus Pro,
  signature électronique) — à vérifier, ne pas présumer un niveau
  d'équipement.
- **Existence d'une convention de contrôle allégé en partenariat** avec le
  comptable, et son périmètre exact (catégories de dépenses concernées, seuils
  d'échantillonnage).
- **Existence d'une régie d'avances** habilitée à porter la dépense, par
  opposition à un circuit de mandatement classique.
- **Qualité du bénéficiaire** (tiers, agent, régisseur) — conditionne
  certaines pièces justificatives et le canal de paiement.

---

## 5. Règles métier

### 5.1 Les trois temps de l'ordonnateur et le paiement du comptable

- **Engagement** : acte par lequel la collectivité crée ou constate une
  **obligation** de laquelle résultera une charge. Distinguer l'**engagement
  juridique** (l'acte qui crée l'obligation vis-à-vis du tiers — bon de
  commande, marché, décision d'attribution) de l'**engagement comptable**
  (réservation du crédit correspondant) : les deux doivent être **concordants**
  et **antérieurs** à l'exécution de la prestation.
- **Liquidation** : vérification de la **réalité de la dette** et arrêt du
  **montant exact** à payer, sur la base du service fait constaté (§5.2).
  Aucune liquidation n'est régulière sans un service fait établi.
- **Mandatement** : acte par lequel l'ordonnateur **donne l'ordre** au
  comptable de payer la dette liquidée. Le mandat est accompagné des pièces
  justificatives requises (§5.3).
- **Paiement** : dernier temps, réalisé par le **comptable public** après ses
  propres contrôles (§5.3) — c'est le seul temps qui relève du comptable, non
  de l'ordonnateur : cette séparation est le cœur de la posture
  ordonnateur/comptable (`SKILL.md`, bloc Objet, et §5.2).
- **Faculté / obligation** : les trois temps de l'ordonnateur sont un
  **enchaînement obligatoire**, non substituable : on ne mandate pas sans
  liquidation préalable, on ne liquide pas sans engagement préalable
  régulier.

### 5.2 Service fait et sa certification

- **Service fait** : constat que la prestation, la fourniture ou les travaux
  ont été **effectivement exécutés**, conformément à l'engagement, avant tout
  paiement (sous réserve des exceptions limitées — avances, acomptes, §5.8).
- **Certification** : acte formel par lequel une personne habilitée par
  l'ordonnateur atteste la réalité du service fait — habilitation à documenter
  explicitement (délégation de signature ou de fonction), jamais présumée du
  seul fait de la position hiérarchique de l'agent.
- Un mandatement sans certification régulière du service fait expose à un
  **rejet du comptable** (§5.3) et, en cas de paiement indu, à un risque de
  gestion de fait ou de mise en jeu de la responsabilité de l'ordonnateur —
  signaler ce risque avant toute recommandation de régularisation a
  posteriori.

### 5.3 Pièces justificatives, contrôle du comptable, rejet, réquisition

- **Nomenclature réglementaire** des pièces justificatives : un texte fixe,
  par catégorie de dépense, la liste des pièces à produire à l'appui du
  mandat — nomenclature technique et évolutive, **à vérifier** avant toute
  affirmation sur une catégorie précise, jamais reconstituée de mémoire.
- **Contrôle du comptable** : porte notamment sur la qualité de l'ordonnateur
  ou de son délégataire, la disponibilité des crédits, l'exacte imputation, la
  validité de la créance (pièces justificatives produites, calculs de
  liquidation), et l'application des règles de prescription. Ce contrôle est
  un contrôle de **régularité formelle et de cohérence des pièces**, non un
  contrôle d'opportunité de la dépense.
- **Rejet** : si le contrôle révèle une irrégularité, le comptable **suspend
  le paiement** et notifie à l'ordonnateur les motifs du rejet, pièce par
  pièce. Un rejet n'est jamais discrétionnaire : il doit être motivé sur un
  cas prévu par les textes régissant les contrôles du comptable — motifs
  précis à vérifier au cas par cas.
- **Réquisition de l'ordonnateur** : faculté pour l'ordonnateur d'exiger, par
  écrit et sous sa responsabilité, que le comptable procède néanmoins au
  paiement. **Limites strictes** : la réquisition ne peut porter sur certains
  motifs de rejet limitativement énumérés par le texte applicable (absence de
  crédits disponibles, notamment, en fait toujours exclue de la réquisition)
  — liste exacte des cas où le comptable **doit refuser d'obtempérer** même
  requis, **à vérifier avant toute réquisition envisagée**. La réquisition
  transfère la responsabilité de la dépense à l'ordonnateur, elle ne
  régularise pas le fond de l'irrégularité.

### 5.4 Délai global de paiement et intérêts moratoires

- **Délai global de paiement** : durée maximale, courant de la réception de la
  demande de paiement (ou du service fait si postérieur) jusqu'au paiement
  effectif, se répartissant entre le **délai de l'ordonnateur** (jusqu'au
  mandatement) et le **délai du comptable** (jusqu'au paiement) — durée exacte
  et répartition **à vérifier**, jamais chiffrées de mémoire.
- **Intérêts moratoires** : dus de plein droit au créancier en cas de
  dépassement du délai global de paiement, sans mise en demeure préalable
  nécessaire ; taux et modalités de calcul **à vérifier**, valeur volatile par
  nature (régime des intérêts légaux).
- **Suspension du délai** : certains événements suspendent le décompte du
  délai (demande de pièces complémentaires régulière, litige sur le service
  fait) — conditions exactes à vérifier avant d'opposer une suspension à un
  fournisseur.
- Un dépassement systématique du délai global de paiement est un **signal de
  contrôle interne** à faire remonter, indépendamment du traitement du cas
  d'espèce (→ `controle-interne-financier.md`).

### 5.5 Dématérialisation

- **PES V2** : protocole d'échange dématérialisé entre l'ordonnateur et le
  comptable pour la transmission des flux comptables et des pièces
  justificatives — généralisation et modalités exactes à vérifier selon la
  catégorie de collectivité.
- **Chorus Pro** : portail de facturation électronique par lequel les
  fournisseurs déposent leurs factures destinées aux personnes publiques —
  obligation de réception par ce canal à vérifier selon le type de créancier
  et le seuil éventuellement applicable.
- **Signature électronique** : les actes et pièces dématérialisés doivent
  porter une signature dont le niveau de fiabilité (simple, avancée,
  qualifiée) est fixé par un texte propre à la nature de l'acte — niveau exact
  à vérifier, ne jamais présumer qu'une simple image de signature suffit.
- La dématérialisation ne change **aucune règle de fond** du circuit de la
  dépense (engagement, liquidation, mandatement, contrôle du comptable) : elle
  n'en modifie que le support et la traçabilité.

### 5.6 Dépenses avant le vote du budget

- **Avant le vote du budget primitif** (début d'exercice, ou année de
  renouvellement de l'assemblée), l'exécutif peut engager, liquider et
  mandater certaines dépenses de fonctionnement dans la limite des crédits
  ouverts l'exercice précédent (hors crédits afférents au remboursement de la
  dette), et certaines dépenses d'investissement dans une limite fixée en
  proportion des crédits ouverts au budget précédent — proportion et
  modalités **à vérifier**, jamais chiffrées de mémoire.
- Cette faculté suppose, pour l'investissement, une **autorisation expresse**
  de l'assemblée délibérante (délibération distincte) précisant le montant et
  l'affectation des crédits — vérifier l'existence de cette délibération avant
  toute exécution en investissement sur ce régime.
- Ce régime dérogatoire prend fin au vote du budget primitif ; les dépenses
  engagées à ce titre s'imputent ensuite sur les crédits du budget voté.

### 5.7 Dépenses obligatoires

- Une **dépense obligatoire** est une dépense que la collectivité est tenue
  d'inscrire et d'exécuter en vertu d'un texte ou d'une décision de justice
  devenue définitive (remboursement de la dette, dépenses de personnel
  statutaires, exécution d'une décision juridictionnelle, notamment) — liste
  précise et régime à vérifier, non limitée aux exemples cités.
- L'**absence d'inscription** d'une dépense obligatoire au budget, ou son
  inscription pour un montant manifestement insuffisant, est un signe du
  **garde-fou budgétaire** (`SKILL.md` §5.3) : procédure spécifique
  d'inscription d'office par le représentant de l'État, sur saisine de la
  chambre régionale des comptes — détail et déclenchement → renvoyer à
  `controle-budgetaire.md`, ne pas le traiter ici.

### 5.8 Avances et acomptes

- **Avance** : paiement effectué **avant tout commencement d'exécution** de la
  prestation, par dérogation au principe du service fait — encadrée par des
  conditions et des plafonds propres à la nature de la dépense (marché
  public notamment, → `commande-publique-financiere.md` pour le volet
  marché) — conditions générales à vérifier avant toute recommandation.
- **Acompte** : paiement correspondant à un service **partiellement fait**,
  proportionné à l'exécution réellement constatée à la date du paiement.
- Toute avance ou acompte doit être **régularisé** lors du paiement final, par
  déduction du montant déjà versé — l'absence de suivi de cette déduction
  expose à un double paiement.

### 5.9 Régies d'avances

- Une **régie d'avances** permet à un agent habilité (le régisseur) de payer
  directement certaines dépenses de faible montant ou nécessitant une
  rapidité d'exécution incompatible avec le circuit normal de mandatement,
  pour le compte de l'ordonnateur, sous le contrôle du comptable.
- Institution, nomination du régisseur, cautionnement et contrôles :
  mécanique **partagée** avec la régie de recettes → `objets/regie.md`
  (pointer, ne pas dupliquer ici le détail opérationnel).
- Une régie d'avances est la **seule voie régulière** pour qu'un agent autre
  que le comptable manie des fonds publics en paiement : toute pratique
  équivalente hors régie régulièrement instituée déclenche le garde-fou
  ordonnateur/comptable (`SKILL.md` §5.2).

### 5.10 Dépenses imprévues

- Le **chapitre des dépenses imprévues**, lorsqu'il est ouvert au budget,
  permet de financer des dépenses **imprévisibles au moment du vote**, dans
  une limite fixée par le CGCT — limite et conditions de virement vers un
  chapitre ordinaire à vérifier, jamais chiffrées de mémoire (→
  `budget-cycle.md` §5.5).
- Le virement d'un crédit de ce chapitre vers un chapitre de dépense
  effective doit être **documenté et notifié** dans les conditions fixées par
  le texte applicable — ne jamais l'utiliser pour couvrir une dépense
  prévisible non budgétée par ailleurs.

### 5.11 Contrôle allégé en partenariat

- Dispositif conventionnel entre l'ordonnateur et le comptable, organisant un
  **contrôle par échantillonnage** de certaines catégories de dépenses
  jugées à faible risque, en contrepartie d'un **renforcement du contrôle
  interne** de l'ordonnateur sur ces mêmes catégories.
- Ne dispense **jamais** du respect des règles de fond (service fait, pièces
  justificatives, disponibilité des crédits) : il modifie l'**intensité du
  contrôle a priori** du comptable, pas les obligations de l'ordonnateur.
- Le périmètre exact (catégories de dépenses, taux d'échantillonnage) est
  fixé par la convention propre à chaque collectivité — à vérifier, jamais
  présumé identique d'une collectivité à l'autre. Organisation générale du
  contrôle interne → `controle-interne-financier.md`, ne pas la dupliquer
  ici.

---

## 6. Calculs et procédures

### 6.1 Séquence normale d'une dépense

Engagement juridique et comptable (crédit réservé) → exécution de la
prestation → constat et certification du service fait → liquidation (montant
exact arrêté) → mandatement (pièces justificatives jointes) → transmission au
comptable → contrôle du comptable → paiement, ou rejet motivé (§5.3).

### 6.2 Méthode de calcul du délai global de paiement

Poser la **méthode**, sans chiffrer : point de départ (réception de la
demande de paiement ou service fait si postérieur) → décompte des journées
courant jusqu'au paiement effectif → déduction des périodes de suspension
régulières → répartition entre part ordonnateur et part comptable → comparaison
à la durée maximale applicable (**à vérifier**) → si dépassement, calcul des
intérêts moratoires selon le taux en vigueur (**à vérifier**, valeur
volatile).

### 6.3 Méthode de traitement d'un rejet du comptable

Lire le motif exact notifié → vérifier s'il porte sur une pièce manquante ou
incohérente (régularisable) ou sur une irrégularité de fond (crédit
insuffisant, créance non fondée) → si régularisable, compléter et
retransmettre → si l'ordonnateur estime le rejet infondé, évaluer la
réquisition (§5.3) en vérifiant d'abord qu'elle n'est pas exclue pour ce motif
précis → documenter la décision et ses motifs.

---

## 7. Déclencheurs de vérification

Appliquer le socle-sources (`SKILL.md` §5.4, matrice §2.2) avant de conclure
dès que la question porte sur :

- la **liste des pièces justificatives** exigibles pour une catégorie de
  dépense précise ;
- les **motifs de rejet** exacts du comptable et les cas **exclus de la
  réquisition** ;
- la **durée du délai global de paiement**, sa répartition, et le **taux des
  intérêts moratoires** ;
- les **limites chiffrées** applicables aux dépenses avant le vote du budget,
  aux avances, ou au chapitre des dépenses imprévues ;
- la **qualification d'une dépense obligatoire** dans un cas litigieux ;
- l'**obligation de dématérialisation** (Chorus Pro, PES V2, niveau de
  signature) applicable à une catégorie de créancier ou d'acte ;
- le **périmètre exact** d'une convention de contrôle allégé en partenariat.

---

## 8. Pièges & confusions fréquentes

1. Mandater sans **service fait certifié**, en anticipant une exécution
   encore en cours, hors les cas d'avance ou d'acompte régulièrement prévus.
2. Confondre **engagement juridique** et **engagement comptable** : les deux
   sont distincts et doivent être concordants.
3. Croire la **réquisition** toujours possible : certains motifs de rejet
   l'excluent par principe (notamment l'absence de crédits disponibles).
4. Présenter la réquisition comme **régularisant le fond** de l'irrégularité :
   elle ne fait que transférer la responsabilité à l'ordonnateur.
5. Oublier de **déduire une avance ou un acompte** déjà versé lors du paiement
   final, au risque d'un double paiement.
6. Utiliser le **chapitre des dépenses imprévues** pour une dépense
   prévisible non budgétée par ailleurs.
7. Considérer le **contrôle allégé en partenariat** comme une dispense des
   règles de fond, alors qu'il ne modifie que l'intensité du contrôle a
   priori.
8. Laisser un agent hors régie régulièrement instituée **manier des fonds**
   en paiement : bascule immédiate vers le garde-fou ordonnateur/comptable
   (`SKILL.md` §5.2).
9. Ignorer un **dépassement récurrent** du délai global de paiement au lieu
   de le signaler comme point de contrôle interne.
10. Citer un **délai, un taux ou un plafond** de mémoire au lieu de le
    marquer « à vérifier ».

---

## 9. Données / valeurs à vérifier

| Donnée | Statut |
|---|---|
| Durée du délai global de paiement et sa répartition ordonnateur/comptable | **À vérifier** |
| Taux des intérêts moratoires applicables | **À vérifier** — valeur volatile |
| Nomenclature réglementaire exacte des pièces justificatives par catégorie de dépense | **À vérifier** |
| Liste exacte des motifs de rejet et des cas exclus de la réquisition | **À vérifier** |
| Limite proportionnelle des dépenses d'investissement engageables avant le vote du budget | **À vérifier** |
| Plafond du chapitre des dépenses imprévues | **À vérifier** |
| Conditions et plafonds des avances par nature de dépense | **À vérifier** |
| Obligation exacte de facturation par Chorus Pro selon le créancier | **À vérifier** |
| Niveau de signature électronique exigé selon la nature de l'acte | **À vérifier** |
| Périmètre de la convention de contrôle allégé en partenariat de la collectivité | **À vérifier**, propre à chaque collectivité |

---

## 10. Écrits & livrables

| Écrit | Élément obligatoire | Générateur |
|---|---|---|
| Mandat de paiement | Pièces justificatives complètes, service fait certifié, imputation vérifiée | Circuit métier / logiciel financier, hors gabarit `templates/` |
| Décision de réquisition du comptable | Motifs, engagement de responsabilité de l'ordonnateur, vérification préalable de non-exclusion | `references/templates/fiche-procedure-financiere.md` |
| Note d'impact financier sur un régime dérogatoire (avant vote du budget, avance) | Hypothèses annoncées, données manquantes signalées | `references/templates/note-impact-financier.md` |
| Fiche de procédure — circuit de la dépense, contrôle allégé en partenariat | Étapes, acteurs, points de contrôle | `references/templates/fiche-procedure-financiere.md` |

---

## 11. Double échelle [risque / confiance]

| Sous-domaine | Risque | Confiance |
|---|---|---|
| Enchaînement engagement/liquidation/mandatement | Moyen | Stable dans la méthode |
| Certification du service fait | Élevé | Stable dans le principe, habilitation à vérifier |
| Pièces justificatives exigibles | Moyen à élevé | À vérifier par catégorie |
| Motif de rejet et champ de la réquisition | Élevé | À vérifier avant toute réquisition |
| Délai global de paiement et intérêts moratoires | Élevé | À vérifier, valeur volatile |
| Dépenses avant le vote du budget | Élevé | Stable dans le principe, limite à vérifier |
| Dépenses obligatoires non couvertes | Critique | Stable dans le principe — bascule garde-fou budgétaire |
| Avances, acomptes | Moyen | Stable dans la méthode |
| Régie d'avances hors cadre régulier | Critique | Bascule garde-fou ordonnateur/comptable |
| Contrôle allégé en partenariat | Moyen | À vérifier selon la convention locale |

---

## 12. Checklist de branche

1. **Garde-fou ordonnateur/comptable (`SKILL.md` §5.2)** testé : un agent
   manie-t-il des fonds hors régie régulièrement instituée ? Si oui, STOP
   affiché avant tout contenu métier.
2. **Garde-fou budgétaire (`SKILL.md` §5.3)** testé : une dépense obligatoire
   est-elle non couverte par des crédits suffisants ?
3. **Trois temps de l'ordonnateur** respectés dans l'ordre, avant tout
   mandatement recommandé ?
4. **Service fait** certifié par une personne habilitée avant liquidation ?
5. **Pièces justificatives** de la catégorie de dépense vérifiées, non
   présumées ?
6. Si rejet en cause : **motif exact** identifié et **champ de la
   réquisition** vérifié avant toute recommandation de réquisition ?
7. **Délai global de paiement** traité comme donnée à vérifier, jamais
   chiffré de mémoire ?
8. Si dépense avant le vote du budget : **autorisation expresse** de
   l'assemblée vérifiée pour l'investissement ?
9. Si avance ou acompte : **déduction lors du paiement final** rappelée ?
10. Renvoi fait vers `objets/regie.md` pour le détail opérationnel d'une régie
    d'avances, sans duplication ?
11. Couple **[risque / confiance]** (§11) indiqué quand utile à la décision ?
12. **Écrit** demandé effectivement produit ?
