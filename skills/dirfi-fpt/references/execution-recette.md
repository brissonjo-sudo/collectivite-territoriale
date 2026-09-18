# Branche — Exécution de la recette (v0.1.0)

> Structure conforme à `_gabarit-branche.md`. Aucun numéro d'article, aucun
> délai de prescription chiffré, aucun seuil, taux ou montant n'est cité de
> mémoire : seules les **règles**, les **méthodes** et la consigne de
> vérifier la version en vigueur figurent ici.

## 1. Périmètre / Exclusions

- **Périmètre** : le **circuit d'exécution de la recette** — constatation des
  droits, liquidation, émission du titre, prise en charge et recouvrement par
  le comptable, mentions obligatoires et voies de recours, recouvrement
  amiable puis contentieux, admissions en non-valeur et créances éteintes,
  prescription de l'action en recouvrement, régies de recettes (principe),
  tarification des services publics locaux, produits des services, du
  domaine, redevances d'occupation, annulation et réduction de titre.
- **Exclusions** : la **fiscalité locale** et les **dotations** →
  `fiscalite-locale.md` et `dotations-perequation.md` ; le **détail
  opérationnel de la régie** (acte constitutif, nomination, cautionnement,
  contrôles) → `objets/regie.md` (pointer, ne pas dupliquer) ; l'**ouverture
  budgétaire** des recettes et le calendrier → `budget-cycle.md` ; les
  **règles d'imputation** → `nomenclature-m57.md`.

---

## 2. Questions couvertes

- Quelles sont les étapes de l'exécution d'une recette, de la constatation du
  droit au recouvrement ?
- Que doit obligatoirement mentionner un titre de recettes, et quelles voies
  de recours ouvre-t-il ?
- Comment s'enchaînent recouvrement amiable et recouvrement contentieux, et
  quels actes de poursuite le comptable peut-il engager ?
- Quelle différence entre admission en non-valeur et créance éteinte, et qui
  décide de laquelle ?
- Dans quel délai l'action en recouvrement d'une créance se prescrit-elle ?
- Comment instituer et faire fonctionner une régie de recettes, à un niveau de
  principe ?
- Comment fixer le tarif d'un service public local, dans le respect du
  principe d'égalité, et peut-on le moduler ?
- Que recouvrent les produits des services, du domaine, et les redevances
  d'occupation ?
- Comment annuler ou réduire un titre déjà émis, et quels en sont les effets ?

---

## 3. Arbre de traitement

`identifier la nature de la recette (fiscale exclue, produit de service,
redevance, produit domanial, subvention reçue) → vérifier la constatation du
droit → liquider le montant exact → émettre le titre avec ses mentions
obligatoires → transmettre au comptable pour prise en charge → suivre le
recouvrement (amiable puis contentieux si nécessaire) → détecter un
encaissement hors circuit du comptable (garde-fou §5.2 SKILL) → en cas
d'échec du recouvrement, qualifier admission en non-valeur ou créance éteinte
→ vérifier la prescription applicable → orienter vers l'écrit (§10)`.

Ne jamais recommander l'abandon d'une créance (non-valeur, extinction, remise
gracieuse) sans avoir d'abord vérifié que les actes de poursuite utiles ont
été engagés et que la prescription n'a pas été négligée par carence.

---

## 4. Variables à lever

- **Nature de la recette** : produit d'un service public (redevance pour
  service rendu), produit domanial, subvention ou participation reçue,
  produit financier — chaque nature obéit à des règles de fixation et de
  recouvrement distinctes.
- **Qualité du débiteur** : usager, tiers de droit privé, autre personne
  publique — conditionne les actes de poursuite mobilisables.
- **Stade du recouvrement** atteint : amiable, contentieux engagé, poursuites
  déjà tentées et infructueuses.
- **Motif de non-recouvrement invoqué** : insolvabilité du débiteur
  (non-valeur), disparition juridique de la dette (extinction), négligence de
  poursuite (à ne jamais couvrir par une non-valeur de confort).
- **Existence d'une régie de recettes** habilitée à encaisser directement,
  par opposition à un circuit de titre classique.
- **Mode de tarification retenu** pour un service public local (tarif unique,
  modulé selon critères objectifs, gratuité) et son fondement.
- **Existence d'une convention ou d'un titre d'occupation** du domaine public
  fondant une redevance.

---

## 5. Règles métier

### 5.1 Constatation des droits, liquidation, émission, prise en charge

- **Constatation des droits** : identification du fait générateur de la
  créance (prestation rendue, occupation autorisée, participation due) et de
  son fondement juridique (texte, délibération, convention, décision
  individuelle).
- **Liquidation** : détermination du **montant exact** dû, sur la base du
  tarif ou de la formule applicable — jamais un montant estimé sans base
  documentée.
- **Émission du titre de recettes** : acte par lequel l'ordonnateur **rend
  exécutoire** la créance et ordonne au comptable de la recouvrer. Le titre
  peut être individuel ou collectif (rôle).
- **Prise en charge par le comptable** : le comptable contrôle la régularité
  formelle du titre (autorité compétente, pièces justificatives requises,
  exacte imputation) avant de le prendre en charge et d'engager le
  recouvrement — un titre irrégulier peut être rejeté par le comptable au même
  titre qu'un mandat (→ `execution-depense.md` §5.3 pour la méthode, transposée
  ici au titre).
- **Recouvrement** : diligences engagées par le comptable pour obtenir le
  paiement, d'abord amiables puis, à défaut, contentieuses (§5.3).

### 5.2 Mentions obligatoires du titre et voies de recours

- Un titre de recettes exécutoire doit comporter des **mentions obligatoires**
  fixées par un texte propre — a minima l'identification du débiteur, le
  fondement et le montant de la créance, l'autorité émettrice, et
  l'**indication des voies et délais de recours** contre le titre. Liste
  exacte et complète : **à vérifier**, jamais reconstituée de mémoire pour un
  titre destiné à être notifié.
- L'**absence ou l'inexactitude** d'une mention obligatoire, notamment relative
  aux voies de recours, peut faire obstacle à l'opposabilité des délais de
  recours au débiteur — signaler ce risque avant toute émission en série d'un
  titre nouveau.
- **Voies de recours** : le débiteur peut contester le bien-fondé de la
  créance (recours devant le juge compétent selon la nature de la créance) et,
  séparément, la régularité des actes de poursuite engagés pour la recouvrer —
  ces deux contentieux obéissent à des règles et des délais distincts, à
  vérifier au cas par cas.

### 5.3 Recouvrement amiable, recouvrement contentieux, actes de poursuite

- **Recouvrement amiable** : relance du débiteur par le comptable, sans acte
  de contrainte, dans un délai raisonnable après l'exigibilité de la créance.
- **Recouvrement contentieux** : à défaut de paiement amiable, le comptable
  peut engager des **actes de poursuite** (mise en demeure formelle,
  opposition à tiers détenteur, saisie selon la nature de la créance et du
  patrimoine du débiteur) — nature exacte des actes mobilisables et
  conditions de mise en œuvre **à vérifier**, variables selon la qualité du
  débiteur (personne privée, autre personne publique) et le montant en jeu.
- **Opposition** : le débiteur peut former **opposition** à un acte de
  poursuite, dans un délai et selon des formes à vérifier ; cette contestation
  ne suspend pas nécessairement la poursuite sauf décision contraire de
  l'autorité compétente.
- **Rôle de l'ordonnateur** : l'ordonnateur ne recouvre pas lui-même (c'est le
  monopole du comptable) mais **appuie** le recouvrement en produisant les
  éléments de fond nécessaires (justification de la créance, informations sur
  le débiteur) et en décidant, le cas échéant, d'une remise gracieuse dans les
  conditions où elle est possible.

### 5.4 Admissions en non-valeur et créances éteintes

- **Admission en non-valeur** : décision, prise par l'**assemblée
  délibérante** sur proposition du comptable, de sortir une créance non
  recouvrée des **restes à recouvrer**, faute de perspective réaliste de
  recouvrement (insolvabilité du débiteur, disparition, coût de poursuite
  disproportionné). Elle **ne libère pas juridiquement** le débiteur : si sa
  situation s'améliore, la créance reste en principe recouvrable tant que la
  prescription n'est pas acquise.
- **Créance éteinte** : situation dans laquelle la créance a **disparu
  juridiquement** (effacement de dette dans le cadre d'une procédure de
  traitement du surendettement ou d'une liquidation judiciaire clôturée pour
  insuffisance d'actif, notamment) : le comptable **ne peut plus** en
  poursuivre le recouvrement, quelle que soit l'évolution ultérieure de la
  situation du débiteur.
- **Distinction et compétence** : l'admission en non-valeur est une décision
  de gestion de l'**assemblée délibérante**, la créance éteinte est une
  **conséquence automatique** d'une décision extérieure (juridictionnelle ou
  d'une commission de surendettement) que l'ordonnateur **constate**, sans
  pouvoir d'appréciation sur le fond.
- **Effets** : dans les deux cas, la créance sort de la comptabilité des
  restes à recouvrer ; seule la créance éteinte emporte disparition
  définitive du droit de la collectivité, l'admission en non-valeur n'étant
  qu'une mesure d'ordre budgétaire et comptable.

### 5.5 Prescription de l'action en recouvrement

- L'action en recouvrement d'une créance publique se **prescrit** à
  l'expiration d'un délai fixé par un texte, propre à la nature de la créance
  (produit du domaine, produit de service, créance de droit commun) — durée
  exacte **à vérifier**, jamais présumée uniforme entre catégories de
  créances.
- La prescription peut être **interrompue** par un acte de poursuite régulier
  ou une reconnaissance de dette du débiteur, et **suspendue** dans des cas
  déterminés — conditions exactes à vérifier avant d'écarter ou d'invoquer une
  prescription.
- Une créance **prescrite** ne peut plus être recouvrée par le comptable : la
  laisser en restes à recouvrer sans traitement n'est pas une option neutre,
  c'est une carence de gestion à signaler.

### 5.6 Régies de recettes — principe

- Une **régie de recettes** permet à un agent habilité (le régisseur)
  d'encaisser directement certaines recettes, pour le compte de
  l'ordonnateur, sous le contrôle du comptable, par dérogation au circuit
  normal titre → prise en charge → recouvrement.
- **Acte constitutif**, **nomination du régisseur**, **cautionnement** et
  **contrôles** : mécanique détaillée et partagée avec la régie d'avances →
  `objets/regie.md` (pointer, ne pas dupliquer ici).
- La régie de recettes est la **seule voie régulière** pour qu'un agent autre
  que le comptable encaisse des fonds publics : tout encaissement direct hors
  régie régulièrement instituée déclenche le garde-fou ordonnateur/comptable
  (`SKILL.md` §5.2).

### 5.7 Tarification des services publics locaux

- **Compétence** : la fixation du tarif d'un service public local relève, en
  principe, de l'**assemblée délibérante**, sauf délégation régulièrement
  consentie à l'exécutif pour certaines catégories de tarifs — étendue de la
  délégation à vérifier au cas par cas.
- **Principe d'égalité** devant le service public : les usagers placés dans
  une situation identique au regard du service doivent être traités de
  manière identique. Ce principe **n'interdit pas** toute différenciation :
  il l'encadre.
- **Modulation admise**, sous conditions à documenter et à vérifier au cas
  d'espèce : différences de situation objectives entre usagers (résidence,
  quotient familial pour certains services, utilisation différenciée du
  service), nécessité d'intérêt général en rapport avec les conditions
  d'exploitation du service. Une modulation sans critère objectif et sans
  lien avec l'objet du service expose à une rupture d'égalité.
- **Méthode de contrôle d'un tarif envisagé** : identifier le critère de
  modulation proposé → vérifier qu'il repose sur une différence de situation
  objective ou un motif d'intérêt général en lien avec le service → vérifier
  que le tarif est fixé par l'autorité compétente → vérifier sa base légale
  ou réglementaire, et l'existence d'une délibération.

### 5.8 Produits des services, du domaine, redevances d'occupation

- **Produits des services** : recettes perçues en contrepartie d'un service
  rendu à l'usager (cantine, activités périscolaires, équipements sportifs et
  culturels), fixées selon le principe de tarification (§5.7).
- **Produits du domaine** : recettes tirées de la gestion du patrimoine de la
  collectivité (location, vente, produits d'exploitation d'un bien du domaine
  privé notamment) — régime distinct selon que le bien relève du domaine
  public ou du domaine privé, à qualifier avant toute recommandation.
- **Redevances d'occupation du domaine public** : dues par tout occupant
  privatif du domaine public en vertu d'un titre d'occupation (autorisation
  ou convention), fixées en tenant compte des avantages procurés à
  l'occupant — méthode et éventuels planchers/plafonds **à vérifier**, jamais
  chiffrés de mémoire.
- Dans les trois cas, l'existence d'un **fondement** (délibération tarifaire,
  titre d'occupation, convention) est un préalable à toute émission de titre :
  ne jamais liquider une recette sans identifier ce fondement.

### 5.9 Annulation et réduction de titre

- **Annulation de titre** : suppression totale d'un titre déjà émis, pour un
  motif tenant à l'absence de fondement de la créance (erreur de débiteur,
  double émission, créance inexistante) — donne lieu à une écriture
  d'annulation, distincte d'une remise gracieuse (qui suppose une créance
  fondée mais dont le recouvrement est abandonné pour un motif de gestion).
- **Réduction de titre** : diminution du montant d'un titre déjà émis, pour un
  motif tenant à une **erreur de liquidation** (montant erroné, tarif
  mal appliqué) ou à un **événement postérieur** justifiant une créance moins
  élevée que celle initialement émise.
- **Compétence et traçabilité** : annulation et réduction sont des actes de
  l'**ordonnateur**, documentés et transmis au comptable pour ajustement de la
  prise en charge — jamais une simple correction informelle sans trace dans
  la comptabilité des restes à recouvrer.
- Ne jamais confondre une réduction de titre justifiée par une erreur de
  liquidation avec un **abandon de créance déguisé** : si le motif réel est
  l'absence de perspective de recouvrement, la voie régulière est l'admission
  en non-valeur (§5.4), pas la réduction.

---

## 6. Calculs et procédures

### 6.1 Séquence normale d'une recette

Constatation du droit (fait générateur, fondement) → liquidation (montant
exact sur base documentée) → émission du titre (mentions obligatoires
complètes) → transmission au comptable → prise en charge après contrôle de
régularité → recouvrement amiable → à défaut, recouvrement contentieux (actes
de poursuite adaptés à la qualité du débiteur) → si échec documenté :
qualification non-valeur ou créance éteinte (§5.4), sous réserve de la
prescription (§5.5).

### 6.2 Méthode de qualification non-valeur / créance éteinte

Vérifier d'abord si un **événement juridique extérieur** (surendettement,
liquidation judiciaire clôturée) a **éteint** la créance : si oui, créance
éteinte, constatation sans marge d'appréciation. Sinon, apprécier si les
diligences de recouvrement ont été **épuisées ou disproportionnées** au
regard du montant et de la situation du débiteur : si oui, proposer
l'admission en non-valeur à l'assemblée délibérante, en identifiant
explicitement les diligences déjà menées. Ne jamais proposer une non-valeur
en l'absence de toute diligence de recouvrement documentée.

### 6.3 Méthode de contrôle d'un tarif de service public

Identifier l'autorité compétente pour fixer le tarif → identifier le critère
de modulation envisagé → tester sa conformité au principe d'égalité (§5.7) →
vérifier l'existence d'une délibération et sa publicité → vérifier la
cohérence entre le tarif et le fondement budgétaire de la recette (produit de
service, redevance).

---

## 7. Déclencheurs de vérification

Appliquer le socle-sources (`SKILL.md` §5.4, matrice §2.2) avant de conclure
dès que la question porte sur :

- les **mentions obligatoires exactes** d'un titre de recettes et les délais
  de recours applicables ;
- la **nature exacte des actes de poursuite** mobilisables selon la qualité du
  débiteur et le montant de la créance ;
- le **délai de prescription** applicable à une catégorie de créance
  déterminée, et les causes exactes d'interruption ou de suspension ;
- la **compétence exacte** pour une admission en non-valeur ou pour la
  fixation d'un tarif ;
- la **conformité au principe d'égalité** d'une modulation tarifaire
  contestée ou contestable ;
- le **régime exact** (planchers, plafonds, méthode de calcul) d'une redevance
  d'occupation du domaine public ;
- toute **réforme récente** touchant le recouvrement des créances publiques
  locales.

---

## 8. Pièges & confusions fréquentes

1. Confondre **admission en non-valeur** (mesure de gestion, créance
   juridiquement toujours due) et **créance éteinte** (disparition juridique
   de la dette).
2. Proposer une non-valeur **sans diligence de recouvrement documentée** au
   préalable.
3. Traiter une **réduction de titre** comme un moyen détourné d'abandonner une
   créance devenue irrécouvrable, au lieu de passer par l'admission en
   non-valeur.
4. Oublier les **mentions obligatoires** (notamment les voies de recours) lors
   de l'émission d'un titre, fragilisant l'opposabilité des délais.
5. Laisser une créance en restes à recouvrer sans traiter la **prescription**,
   par simple carence de suivi.
6. Moduler un tarif de service public sans **critère objectif** en lien avec
   le service, au risque d'une rupture d'égalité.
7. Confondre **domaine public** et **domaine privé** de la collectivité pour
   qualifier un produit ou une redevance, alors que les régimes diffèrent.
8. Laisser un agent hors régie régulièrement instituée **encaisser des
   fonds** : bascule immédiate vers le garde-fou ordonnateur/comptable
   (`SKILL.md` §5.2).
9. Présenter le rôle de l'ordonnateur dans le recouvrement contentieux comme
   actif, alors qu'il **appuie** sans détenir le monopole du recouvrement,
   réservé au comptable.
10. Citer un **délai de prescription, un plafond ou un taux** de mémoire au
    lieu de le marquer « à vérifier ».

---

## 9. Données / valeurs à vérifier

| Donnée | Statut |
|---|---|
| Liste exacte des mentions obligatoires d'un titre de recettes | **À vérifier** |
| Délais de recours contre un titre et contre un acte de poursuite | **À vérifier** |
| Nature exacte des actes de poursuite mobilisables selon la qualité du débiteur | **À vérifier** |
| Délai de prescription de l'action en recouvrement par catégorie de créance | **À vérifier** |
| Causes exactes d'interruption et de suspension de la prescription | **À vérifier** |
| Compétence exacte (assemblée/exécutif) pour une admission en non-valeur | **À vérifier** |
| Méthode et éventuels planchers/plafonds de calcul d'une redevance d'occupation du domaine public | **À vérifier** |
| Étendue exacte d'une délégation tarifaire consentie à l'exécutif | **À vérifier**, propre à chaque collectivité |
| Conditions précises de qualification d'une créance éteinte | **À vérifier** |

---

## 10. Écrits & livrables

| Écrit | Élément obligatoire | Générateur |
|---|---|---|
| Titre de recettes | Mentions obligatoires, fondement documenté, montant liquidé | Circuit métier / logiciel financier, hors gabarit `templates/` |
| Délibération d'admission en non-valeur | Liste des créances, diligences de recouvrement documentées, proposition du comptable | `references/templates/deliberation-budgetaire.md` |
| Délibération fixant ou modifiant un tarif de service public | Compétence, critère de modulation le cas échéant, publicité | `references/templates/deliberation-budgetaire.md` |
| Acte d'annulation ou de réduction de titre | Motif exact, traçabilité, transmission au comptable | `references/templates/fiche-procedure-financiere.md` |
| Note d'impact financier sur une évolution tarifaire | Hypothèses annoncées, données manquantes signalées | `references/templates/note-impact-financier.md` |

Le détail opérationnel d'une régie de recettes (acte constitutif, régisseur,
cautionnement) → `objets/regie.md`, ne pas le reproduire ici.

---

## 11. Double échelle [risque / confiance]

| Sous-domaine | Risque | Confiance |
|---|---|---|
| Constatation du droit et liquidation | Moyen | Stable dans la méthode |
| Mentions obligatoires du titre et voies de recours | Élevé | À vérifier |
| Actes de poursuite selon la qualité du débiteur | Élevé | À vérifier |
| Admission en non-valeur vs créance éteinte | Élevé | Stable dans la distinction, effets à vérifier |
| Prescription de l'action en recouvrement | Élevé | À vérifier |
| Régie de recettes hors cadre régulier | Critique | Bascule garde-fou ordonnateur/comptable |
| Tarification et principe d'égalité | Élevé | Stable dans le principe, critère à documenter |
| Domaine public vs domaine privé | Moyen à élevé | À qualifier au cas par cas |
| Annulation / réduction de titre | Moyen | Stable dans la méthode |

---

## 12. Checklist de branche

1. **Garde-fou ordonnateur/comptable (`SKILL.md` §5.2)** testé : un agent
   encaisse-t-il des fonds hors régie régulièrement instituée ? Si oui, STOP
   affiché avant tout contenu métier.
2. **Fondement de la créance** (délibération tarifaire, titre d'occupation,
   convention) identifié avant toute liquidation ?
3. **Mentions obligatoires** du titre et **voies de recours** traitées comme
   point de vigilance, non présumées complètes ?
4. Si non-recouvrement en cause : **admission en non-valeur** ou **créance
   éteinte** correctement distinguées, avec diligences documentées ?
5. **Prescription** de l'action en recouvrement vérifiée avant toute
   proposition d'abandon ou de poursuite ?
6. Si tarification en cause : **critère de modulation** testé au regard du
   principe d'égalité ?
7. **Domaine public / domaine privé** correctement qualifié si un produit
   domanial est en cause ?
8. **Réduction de titre** distinguée d'un abandon de créance déguisé ?
9. Renvoi fait vers `objets/regie.md` pour le détail opérationnel d'une régie
   de recettes, sans duplication ?
10. Renvoi fait vers `fiscalite-locale.md` / `dotations-perequation.md` si la
    question glisse vers la fiscalité ou les dotations ?
11. Couple **[risque / confiance]** (§11) indiqué quand utile à la décision ?
12. **Écrit** demandé effectivement produit ?
