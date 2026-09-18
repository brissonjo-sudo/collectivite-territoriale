# Branche — Contrôle interne financier (v1.0.0)

> Structure conforme à `_gabarit-branche.md`. Aucune valeur datée (délai,
> seuil de contrôle hiérarchisé) n'est citée de mémoire : seules les
> **règles** et la consigne de vérifier la valeur en vigueur figurent ici.

## 1. Périmètre / Exclusions

**Périmètre** : principe de **séparation de l'ordonnateur et du
comptable** ; rôles respectifs et **comptable public assignataire** ;
**contrôles du comptable** sur la dépense et la recette, rejet et
régularisation, **réquisition** de l'ordonnateur ; **conventions de
partenariat** avec la DGFiP (contrôle allégé en partenariat, contrôle
hiérarchisé de la dépense) ; démarche de **contrôle interne financier**
(cartographie des risques, plan d'action, organisation, traçabilité,
habilitations) ; **dématérialisation** de la chaîne comptable ;
**prévention de la gestion de fait** ; **qualité comptable** ; relations
avec les **satellites** et organismes subventionnés.

**Exclusions** :
- La **procédure devant le juge des comptes** (mise en jeu de la
  responsabilité, instruction, jugement) → `references/contentieux-financier.md`.
  Cette branche prévient et détecte, elle ne traite pas le contentieux.
- La **procédure de contrôle budgétaire** exercée par le représentant de
  l'État (saisine de la chambre régionale des comptes pour déséquilibre ou
  non-vote du budget) → `references/controle-budgetaire.md`.
- Le **fond des règles d'exécution** de la dépense et de la recette
  (engagement, liquidation, mandatement, titres) → `references/execution-depense.md`
  et `references/execution-recette.md`. Cette branche traite le
  **contrôle** de ces opérations, pas leur déroulement lui-même.

---

## 2. Questions couvertes

- Que signifie exactement la séparation de l'ordonnateur et du comptable,
  et qu'interdit-elle concrètement ?
- Quels contrôles le comptable exerce-t-il sur une dépense ou une recette,
  et que se passe-t-il en cas de rejet ?
- Dans quelles conditions l'ordonnateur peut-il réquisitionner le
  comptable, et quand celui-ci doit-il refuser de déférer ?
- Que change une convention de partenariat avec la DGFiP, et qu'est-ce que
  le contrôle hiérarchisé de la dépense ?
- Comment structurer une démarche de contrôle interne financier
  (cartographie, plan d'action, organisation) ?
- Comment sécuriser la dématérialisation de la chaîne comptable ?
- Comment reconnaître et prévenir un risque de gestion de fait ?
- Comment apprécier la qualité comptable d'une collectivité ?
- Comment organiser le contrôle des satellites et des organismes
  subventionnés ?

---

## 3. Arbre de traitement

`question → variables à lever (§4) → décision → vérification (§7) →
écrit/livrable (§10)`

Avant toute analyse d'une situation de contrôle, lever : **qui a détecté le
problème** (comptable au moment du contrôle, service ordonnateur en
interne, audit), **la nature de l'anomalie** (irrégularité formelle,
absence de pièce justificative, maniement de fonds suspect, risque
statistique de qualité comptable), et **le stade de la chaîne** concerné
(engagement, liquidation, mandatement/titre, paiement/encaissement). Sans
ces trois éléments, marquer l'analyse `[INCOMPLET]`.

---

## 4. Variables à lever

- **Nature de la relation avec le comptable** : existe-t-il une convention
  de partenariat (service comptable et financier, contrôle allégé en
  partenariat), ou le régime de contrôle de droit commun s'applique-t-il ?
- **Stade de la chaîne comptable concerné** : engagement, liquidation,
  mandatement ou émission de titre, paiement ou encaissement.
- **Nature exacte de l'anomalie détectée** : pièce justificative manquante
  ou irrégulière, absence de service fait, dépassement de crédit,
  incompatibilité entre fonctions, flux financier hors circuit du
  comptable.
- **Origine de la détection** : contrôle du comptable lors du visa, audit
  interne, signalement, contrôle externe.
- **Degré de dématérialisation** de la chaîne concernée (flux PES,
  signature électronique, archivage) et son incidence sur la
  traçabilité disponible.
- **Existence d'une cartographie des risques et d'un plan d'action** déjà
  formalisés pour le processus concerné, ou absence de démarche
  structurée à ce stade.
- **Implication d'un satellite** (association, SEM, SPL, budget annexe,
  CCAS) dans le flux analysé.

---

## 5. Règles métier

### 5.1 Séparation de l'ordonnateur et du comptable

- **Fondement** : principe cardinal de la comptabilité publique française
  (décret relatif à la gestion budgétaire et comptable publique — décret
  GBCP, déjà nommé au `SKILL.md` — à confirmer en version consolidée).
  L'**ordonnateur** décide, prescrit, engage et constate les droits et les
  obligations ; le **comptable public** est seul habilité à manier les
  fonds — encaisser, décaisser, tenir la caisse et les comptes.
- **Portée** : cette séparation des fonctions n'est pas une simple règle
  d'organisation interne, elle est **une garantie de régularité** : elle
  empêche qu'une même autorité décide de la dépense ou de la recette **et**
  en manie matériellement les fonds, ce qui limiterait tout contrôle
  indépendant sur le maniement des deniers publics.
- **Incompatibilités** : les fonctions d'ordonnateur et de comptable sont
  **personnellement incompatibles** — une même personne ne peut cumuler les
  deux qualités pour une même collectivité. Le comptable est un agent
  distinct, relevant d'un statut et d'une hiérarchie propres (direction
  générale des finances publiques), non subordonné à l'ordonnateur.
- **Ce que cela interdit concrètement** : à l'ordonnateur, de manier
  lui-même ou de faire manier par ses services les fonds publics
  (encaissement direct, paiement de la main à la main, caisse parallèle) ;
  au comptable, de porter une appréciation sur l'**opportunité** des
  décisions de l'ordonnateur — son contrôle est un contrôle de
  **régularité**, pas de fond politique ou budgétaire d'opportunité.
- Toute situation où cette frontière est franchie — quel qu'en soit le
  motif invoqué (urgence, simplification, rendre service) — est un
  déclencheur immédiat du **garde-fou ordonnateur/comptable**
  (`SKILL.md` §5.2, détaillé au §5.6 ci-après pour la gestion de fait).

### 5.2 Rôles respectifs et comptable public assignataire

- **Ordonnateur** (exécutif de la collectivité ou son délégataire régulier) :
  engage la dépense dans la limite des crédits ouverts, constate le service
  fait, liquide, émet le mandat ou le titre, transmet au comptable.
- **Comptable public assignataire** : celui auprès duquel les opérations de
  la collectivité sont, par affectation, retracées et payées ou
  recouvrées. Il exerce le contrôle de régularité (§5.3) avant tout
  paiement ou avant toute prise en charge d'une recette, et tient la
  comptabilité de la collectivité en miroir de celle de l'ordonnateur.
- Le comptable engage sa **responsabilité personnelle et pécuniaire** sur
  les contrôles qu'il exerce : c'est ce qui justifie l'indépendance de sa
  fonction et l'impossibilité, pour l'ordonnateur, de lui imposer un
  paiement irrégulier hors la voie de la réquisition (§5.4).

### 5.3 Contrôles du comptable, rejet et régularisation

- **Sur la dépense** : le comptable vérifie notamment la qualité de
  l'ordonnateur ou de son délégataire, la disponibilité des crédits,
  l'exacte imputation, la validité de la créance (pièces justificatives,
  service fait, exactitude des calculs) et le caractère libératoire du
  paiement.
- **Sur la recette** : il vérifie l'autorisation de percevoir la recette,
  la mise en recouvrement régulière (titre exécutoire) et l'exactitude de
  l'imputation.
- **Rejet** : en cas d'irrégularité ou de pièce manquante, le comptable
  **suspend le paiement** (ou la prise en charge) et notifie les motifs
  précis à l'ordonnateur.
- **Régularisation** : l'ordonnateur complète ou corrige le dossier et le
  retransmet ; chaque rejet doit être **motivé et précis**, pour permettre
  une régularisation ciblée.
- Documenter systématiquement les rejets et leur régularisation : indicateur
  de **qualité comptable** (§5.9) et point de contrôle interne à part
  entière.

### 5.4 Réquisition de l'ordonnateur

- Lorsque le comptable **persiste dans son refus** de payer après un motif
  de rejet que l'ordonnateur estime infondé, ce dernier peut, dans les cas
  et selon la procédure prévus par les textes (à vérifier), lui adresser un
  **ordre de réquisition** : un acte formel par lequel l'ordonnateur prend
  la responsabilité du paiement à sa place.
- **Procédure** : acte écrit et motivé, notifié au comptable, qui en
  accuse réception. Modalités précises (forme, délai, destinataire d'une
  copie) à vérifier avant toute mise en œuvre, jamais présentées de
  mémoire.
- **Cas où le comptable doit refuser de déférer** : certains motifs de
  rejet sont **exclus du champ de la réquisition** — le comptable ne peut
  se voir imposer d'obtempérer notamment lorsque le contrôle porte sur
  l'absence de disponibilité des crédits, l'absence de justification du
  service fait, le caractère non libératoire du règlement, ou plus
  généralement sur des motifs touchant à la sincérité même de la dépense.
  La liste exacte et les motifs précis relèvent d'un texte à vérifier
  systématiquement avant toute conclusion sur un cas d'espèce.
- **Effet** : réquisition régulière suivie par le comptable → sa
  **responsabilité personnelle est dégagée** au profit de celle de
  l'ordonnateur, qui répond de sa décision devant l'assemblée et, le cas
  échéant, devant le juge compétent.
- **Traçabilité** : conserver l'acte de réquisition, sa motivation, la
  correspondance échangée avec le comptable, et en rendre compte selon les
  modalités internes de contrôle (§5.5). Un usage répété de la réquisition
  sur un même motif est un signal à faire remonter : il traduit soit une
  irrégularité récurrente de l'ordonnateur, soit un point de désaccord de
  fond à clarifier avec le comptable assignataire.

### 5.5 Conventions de partenariat avec la DGFiP

- Une collectivité peut conclure avec la direction départementale ou
  régionale des finances publiques une **convention de partenariat**
  organisant les modalités de travail entre l'ordonnateur et le comptable,
  au-delà du droit commun.
- **Service comptable et financier (SCF)** : organisation renforcée
  associant les équipes de l'ordonnateur et du comptable, pour fluidifier
  la chaîne de la dépense et de la recette tout en maintenant la
  séparation des fonctions (§5.1).
- **Contrôle allégé en partenariat** : sur la base d'une évaluation
  partagée du niveau de maîtrise des risques, le comptable adapte
  l'intensité de ses contrôles a priori sur certaines catégories de flux,
  en contrepartie d'un contrôle interne renforcé côté ordonnateur
  (cartographie, plan d'action, §5.6).
- **Contrôle hiérarchisé de la dépense (CHD)** : le comptable module
  lui-même l'intensité et la fréquence de ses contrôles selon la nature, le
  montant et le risque de chaque catégorie de dépense, plutôt que
  d'appliquer un contrôle exhaustif uniforme.
- Ces dispositifs **ne suppriment jamais** la séparation (§5.1) ni la
  responsabilité du comptable : ils **modulent l'intensité** du contrôle a
  priori.

### 5.6 Démarche de contrôle interne financier

- **Cartographie des risques** : recenser, pour chaque processus (dépense,
  recette, paie, régies, subventions, dette), les points de vulnérabilité
  (erreur, fraude, gestion de fait, perte de pièce, incompatibilité de
  fonctions) et les hiérarchiser selon probabilité et impact.
- **Plan d'action** : pour chaque risque significatif, définir la mesure de
  maîtrise (contrôle supplémentaire, séparation de tâches, habilitation
  restreinte, procédure écrite), son responsable et son échéance.
- **Organisation en trois niveaux** : un premier niveau intégré à
  l'exécution (auto-contrôle de l'agent, supérieur hiérarchique direct), un
  deuxième niveau indépendant du service opérationnel mais interne à la
  collectivité (contrôle ou audit interne), un troisième niveau externe ou
  très en amont (audit externe, inspection). Documenter à quel niveau se
  rattache chaque contrôle existant.
- **Traçabilité** : chaque contrôle (visa, validation, rapprochement) doit
  laisser une trace exploitable (date, auteur, objet). **Séparation des
  tâches** : distinguer, au sein des services de l'ordonnateur, les
  fonctions d'engagement, de liquidation et de validation du mandatement,
  pour qu'aucun agent ne cumule seul un processus sensible.
- **Habilitations dans le SI financier** : les droits d'accès doivent
  refléter exactement la séparation des tâches définie, être revus
  périodiquement, et retirés sans délai à tout changement de fonction.

### 5.7 Dématérialisation de la chaîne comptable

- **Protocole d'échange (PES V2 ou protocole en vigueur)** : format
  d'échange dématérialisé entre l'ordonnateur et le comptable pour les
  mandats, titres et bordereaux. Vérifier la version en vigueur et son
  degré d'obligation selon la taille de la collectivité.
- **Pièces justificatives dématérialisées** : leur valeur et leur
  conservation suivent des règles à vérifier (formats acceptés, durée,
  modalités d'archivage probant).
- **Signature électronique** : niveau de fiabilité technique et juridique
  à vérifier selon le type d'acte, avant de le présenter comme suffisant.
- **Archivage** : la dématérialisation ne dispense pas d'une politique
  d'archivage probant (intégrité, disponibilité, traçabilité dans le
  temps), y compris pour la durée couvrant un éventuel contrôle ultérieur
  du juge des comptes (renvoi `references/contentieux-financier.md`).
- La dématérialisation **facilite** la traçabilité (§5.6) mais **ne
  remplace pas** la vérification de fond du service fait ou de la
  régularité de la créance.

### 5.8 Prévention de la gestion de fait

- La **gestion de fait** consiste, pour une personne qui n'a pas la qualité
  de comptable public, à manier irrégulièrement des deniers publics
  (encaissement ou décaissement hors du circuit régulier). Elle engage la
  responsabilité personnelle de son auteur devant le juge des comptes.
- **Cas typiques** : encaissement direct de recettes par un service sans
  régie régulièrement instituée ; conservation de recettes par un service
  au lieu de leur versement au comptable ; association ou organisme tiers
  servant de simple caisse à la collectivité ; paiement direct d'une
  dépense par un agent hors du circuit du mandatement.
- **Signaux d'alerte** : caisse ou compte bancaire non identifié dans la
  comptabilité de la collectivité ; flux récurrents vers une association
  dont l'objet ou la gouvernance sont étroitement liés à la collectivité ;
  avance de fonds à un service sans base régulière ; recette perçue par un
  agent sans émission de titre correspondant.
- **Conduite à tenir** : dès qu'un de ces signaux apparaît, appliquer sans
  délai le **garde-fou ordonnateur/comptable** du `SKILL.md` §5.2 — afficher
  le STOP avant tout autre contenu, ne concevoir aucun montage alternatif,
  et orienter vers la saisine du comptable public assignataire ou, selon
  le cas, vers la régularisation par une **régie** régulièrement instituée
  (renvoi `../objets/regie.md`).
- La prévention passe par l'intégration de ce risque dans la cartographie
  (§5.6) : tout processus impliquant un maniement potentiel de fonds hors
  circuit budgétaire classique (buvette, caisse de manifestation, avance à
  une régie) doit être identifié et sécurisé en amont.

### 5.9 Qualité comptable et indicateurs

- La **qualité comptable** se mesure par la fiabilité, l'exhaustivité et la
  rapidité de traitement des opérations : taux et délai de rejet par le
  comptable, taux de rattachement correct des charges et produits, délai
  global de paiement, taux d'anomalies détectées en contrôle interne,
  qualité de l'inventaire et concordance avec l'état de l'actif.
- Ces indicateurs alimentent le dialogue de gestion avec le comptable
  (notamment dans le cadre d'une convention de partenariat, §5.5) et la
  démarche de contrôle interne (§5.6). Ne jamais présenter un taux ou un
  délai précis comme acquis sans l'avoir vérifié dans les données
  effectivement disponibles de la collectivité.

### 5.10 Relations avec les satellites et contrôle des organismes subventionnés

- Un **satellite** (association, SEM, SPL, budget annexe, CCAS) qui gère
  des fonds ou des missions pour le compte de la collectivité appelle une
  vigilance particulière : vérifier que les flux respectent le circuit du
  comptable public et ne contournent pas la séparation ordonnateur/comptable
  (renvoi `../objets/satellites.md`).
- Le **contrôle des organismes subventionnés** (justification de l'emploi
  des fonds, compte rendu financier, contrôle sur place) relève de
  `references/subventions.md` pour le fond ; cette branche n'en traite que
  l'angle du **contrôle interne** (traçabilité des versements, absence de
  confusion entre subvention et achat de prestation).

---

## 6. Calculs et procédures

1. **Cycle rejet / régularisation** : contrôle du comptable → motif de
   rejet notifié et précis → correction par l'ordonnateur → nouvelle
   présentation. Documenter chaque itération.
2. **Réquisition** : constater le rejet → vérifier que le motif n'entre pas
   dans les cas d'exclusion (§5.4) → établir l'acte écrit et motivé →
   notifier au comptable → tracer l'accusé de réception et l'effet sur la
   responsabilité respective.
3. **Cartographie des risques** : lister les processus → identifier les
   points de vulnérabilité → coter probabilité et impact → prioriser →
   décliner en plan d'action daté et attribué.
4. **Habilitations SI financier** : établir la matrice fonctions/droits
   souhaitée à partir de la séparation des tâches définie → comparer aux
   habilitations réellement actives → corriger les écarts → revoir
   périodiquement.
5. **Détection d'une gestion de fait potentielle** : identifier le signal
   d'alerte → appliquer immédiatement le garde-fou (`SKILL.md` §5.2) →
   qualifier la voie de régularisation possible (régie) ou l'absence de
   voie régulière → orienter vers le comptable assignataire.

---

## 7. Déclencheurs de vérification

Appliquer le socle-sources (matrice §2.2 du `SKILL.md`) dès que :
- la **procédure exacte de réquisition** (forme, délai, cas d'exclusion)
  doit être appliquée à un cas concret ;
- le **périmètre exact** d'une convention de partenariat DGFiP ou du
  contrôle hiérarchisé de la dépense est invoqué pour justifier un niveau
  de contrôle allégé ;
- la **version en vigueur** du protocole d'échange dématérialisé (PES V2 ou
  successeur) ou le niveau exigé de signature électronique est en cause ;
- un **délai** (régularisation, archivage, conservation de pièces) est
  invoqué pour justifier une décision ;
- un signal d'alerte de **gestion de fait** est identifié : la
  vérification porte alors sur la voie de régularisation, jamais sur une
  tentative de justifier le montage en l'état.

---

## 8. Pièges & confusions fréquentes

1. Croire que le comptable peut apprécier l'**opportunité** d'une dépense :
   son contrôle porte sur la **régularité**, pas sur le fond politique.
2. Considérer la réquisition comme un moyen systématique de **passer
   outre** un rejet, sans vérifier les cas où le comptable doit refuser de
   déférer (§5.4).
3. Penser qu'une **convention de partenariat** ou un contrôle hiérarchisé
   de la dépense **supprime** le contrôle du comptable : il en module
   seulement l'intensité.
4. Négliger la **traçabilité** des habilitations dans le système
   d'information financier lors d'un changement de poste ou de service.
5. Considérer la **dématérialisation** comme une garantie suffisante de
   régularité, sans contrôle de fond sur le service fait.
6. Ne pas reconnaître un **signal de gestion de fait** parce que le montage
   est présenté comme temporaire, exceptionnel ou motivé par l'urgence.
7. Confondre le **contrôle interne** de la collectivité sur un satellite ou
   un organisme subventionné avec le contrôle de fond de la subvention
   elle-même (renvoi `references/subventions.md`).
8. Traiter une anomalie de **qualité comptable** comme un simple indicateur
   statistique sans l'intégrer à la cartographie des risques.

---

## 9. Données / valeurs à vérifier

- **Jamais de mémoire** : forme et délai exacts de la réquisition, liste
  précise des motifs de rejet exclus de son champ, seuils du contrôle
  hiérarchisé de la dépense, version en vigueur du protocole d'échange
  dématérialisé, durée de conservation et modalités d'archivage des pièces
  justificatives, niveau exigé de signature électronique selon l'acte.
- **Références structurelles stables, citables avec la réserve « à
  confirmer en version consolidée »** : le **décret GBCP**, pour le
  principe de séparation et le cadre des contrôles ; le **code des
  juridictions financières**, pour la responsabilité du comptable et la
  gestion de fait (fond détaillé dans `references/contentieux-financier.md`) ;
  les textes relatifs aux **pièces justificatives** exigibles par catégorie
  de dépense.
- **Aucun numéro d'article ni identifiant Légifrance
  (LEGIARTI/JORFTEXT/NOR)** n'est cité de mémoire dans cette branche : à
  défaut de vérification dans la session, s'en tenir au nom du texte et à
  la réserve.

---

## 10. Écrits & livrables

| Écrit | Nature | Compétence | Générateur / renvoi |
|---|---|---|---|
| Ordre de réquisition du comptable | Acte décisionnel de l'ordonnateur | Exécutif (ordonnateur) | Hors générateurs couche 4 à ce stade ; motivation et traçabilité selon §5.4 |
| Fiche de procédure interne (cartographie des risques, plan d'action, habilitations SI) | Écrit de procédure | DirFi | `references/templates/fiche-procedure-financiere.md` |
| Note d'impact financier sur une convention de partenariat DGFiP | Écrit de pilotage | DirFi | `references/templates/note-impact-financier.md` |
| Convention de partenariat avec la DGFiP (SCF, contrôle allégé) | Écrit conventionnel | Exécutif, après validation de l'assemblée si requis | Convention spécifique, cf. `references/ecrits-financiers.md` §10 |
| Compte rendu de contrôle interne (cartographie actualisée, suivi du plan d'action) | Écrit de pilotage | DirFi | `references/templates/note-impact-financier.md` ou fiche interne selon destinataire |

---

## 11. Double échelle [risque / confiance]

| Sous-domaine | Risque | Confiance | Repère |
|---|---|---|---|
| Principe de séparation ordonnateur/comptable | Critique | Stable sur le principe | Rappel systématique, aucune exception construite |
| Procédure de réquisition | Élevé | À vérifier (forme, délai, cas d'exclusion) | Citation obligatoire avant mise en œuvre |
| Contrôle allégé en partenariat / CHD | Moyen | À vérifier selon la convention en vigueur | Vérification ponctuelle du périmètre exact |
| Dématérialisation (PES, signature électronique, archivage) | Moyen à élevé selon l'acte | À vérifier | Citation de la version en vigueur avant affirmation |
| Signal de gestion de fait | Critique | Stable sur la conduite à tenir | STOP immédiat, aucune exception (`SKILL.md` §5.2) |
| Qualité comptable et indicateurs | Faible à moyen | Stable sur la méthode, à vérifier sur les données | Vérification des données réelles avant tout chiffre |
| Contrôle des satellites et organismes subventionnés | Moyen à élevé | À vérifier selon la nature du satellite | Renvoi systématique aux branches de fond |

---

## 12. Checklist de branche

1. **Séparation ordonnateur/comptable** rappelée et respectée dans toute
   recommandation, sans aucune exception construite ?
2. **Signal de gestion de fait** testé explicitement (§5.8) ? Si présent,
   **STOP** (`SKILL.md` §5.2) affiché avant tout autre contenu, aucune
   voie alternative construite hors régie régulière.
3. **Contrôles du comptable** (dépense, recette) correctement distingués
   d'une appréciation d'opportunité ?
4. En cas de **rejet** : motif précis identifié, régularisation orientée
   plutôt que contournement ?
5. En cas de **réquisition envisagée** : cas d'exclusion vérifiés avant
   toute recommandation de l'utiliser ?
6. **Convention de partenariat DGFiP** ou contrôle hiérarchisé de la
   dépense : présentés comme modulant l'intensité du contrôle, jamais
   comme le supprimant ?
7. **Cartographie des risques et plan d'action** proposés avec
   responsable et échéance, pas comme une simple liste ?
8. **Séparation des tâches et habilitations SI financier** vérifiées pour
   tout processus sensible évoqué ?
9. **Dématérialisation** : version du protocole et niveau de signature
   électronique signalés comme à vérifier, jamais affirmés de mémoire ?
10. **Satellites et organismes subventionnés** : renvoi fait aux branches
    de fond (`../objets/satellites.md`, `references/subventions.md`) sans
    duplication ?
11. Toute référence citée porte-t-elle sa provenance ou la réserve « à
    confirmer en version consolidée » (§9) ?
12. Couple **[risque / confiance]** (§11) indiqué quand utile à la
    décision ?
