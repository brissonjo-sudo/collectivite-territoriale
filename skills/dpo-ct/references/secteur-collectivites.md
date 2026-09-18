# Branche — Traitements sectoriels des collectivités

> **Table des matières** — fichier long (350 lignes) : lire le §1 (périmètre)
> puis aller **directement** à la sous-famille concernée en §5 plutôt que de
> tout relire. Les §6 à 12 (procédures, pièges, livrables, checklist)
> s'appliquent transversalement à toutes les familles.
>
> §1 Périmètre/exclusions · §2 Questions couvertes · §3 Arbre de traitement ·
> §4 Variables à lever · **§5 Règles métier par famille** : 5.1 état civil ·
> 5.2 élections · 5.3 scolaire/périscolaire · 5.4 action sociale (CCAS) ·
> 5.5 urbanisme/GRU · 5.6 vidéoprotection · 5.7 RH · 5.8 cimetières ·
> 5.9 téléservices/communication · 5.10 open data · 5.11 archives ·
> §6 Procédures et délais · §7 Déclencheurs de vérification · §8 Pièges ·
> §9 Données à vérifier · §10 Livrables · §11 [risque/confiance] ·
> §12 Checklist.

## 1. Périmètre / Exclusions

**Couvre** : la conformité des familles de traitements communaux — état
civil, élections, scolaire, action sociale, urbanisme et GRU,
vidéoprotection (volet données), RH (volet conformité), funéraire,
téléservices et communication, open data, archives. Branche « terrain » :
elle applique les branches transverses aux métiers de la collectivité.

**Exclut** : le fond des obligations transverses (registre →
`gouvernance-registre.md` ; AIPD → `aipd.md` ; droits et information →
`droits-personnes.md` ; sous-traitance → `sous-traitance-transferts.md` ;
sécurité → `securite-traitements.md`) ; le volet autorisation et doctrine
d'emploi de la vidéoprotection → skill **dpm-fpt** ; le fond statutaire RH →
skill **drh-fpt** ; la qualification du régime → `analyse-situation.md`.

---

## 2. Questions couvertes

- « Ce traitement communal est-il conforme ? Que régulariser ? »
- « Qui est responsable de traitement (commune, CCAS, État) ? »
- « Peut-on publier / transmettre / réutiliser ces données d'administrés ? »
- « Faut-il une AIPD ? Quelle durée de conservation ? »
- « Le maire / un élu peut-il utiliser ce fichier pour communiquer ? »

---

## 3. Arbre de traitement

`question → variables à lever → décision → vérification → livrable`

1. Passer par le routeur (`analyse-situation.md`) : données personnelles ?
   finalité ? **régime** ? **responsable de traitement** ?
2. Identifier la **famille sectorielle** (§5) et lire sa sous-section.
3. Repérer le **texte sectoriel** qui impose ou encadre le traitement : il
   peut fixer base légale, durées, destinataires, publicité.
4. Dérouler les points de conformité (base légale, registre, information,
   durées, destinataires, sécurité, AIPD) ; vérifier les points de la
   matrice §2.2 du `SKILL.md` (déclencheurs §7).
5. Conclure par le livrable adapté (§10) — recommandation, jamais décision
   (garde-fou §5.2.a du `SKILL.md`).

---

## 4. Variables à lever

- **Responsable de traitement réel** : commune, EPCI, CCAS (personne morale
  distincte), État (maire agissant en son nom), responsabilité conjointe —
  point décisif, source de la moitié des erreurs sectorielles.
- **Régime** : RGPD ou Police-Justice → `analyse-situation.md` §2.
- **Texte sectoriel applicable** et ce qu'il fixe (durée, publicité,
  destinataires, caractère obligatoire).
- **Personnes concernées** : mineurs, bénéficiaires de l'action sociale,
  personnes âgées → risque relevé, AIPD probable.
- **Catégories de données** : sensibles, infractions, NIR.
- **Sous-traitants** : éditeur métier, portail familles, prestataire de
  paiement, hébergeur — et localisation.
- **Diffusion envisagée** : publication, transmission, open data →
  occultation ou anonymisation préalable ?

---

## 5. Règles métier — par famille de traitements

### 5.1 État civil et affaires générales

- Le maire agit comme **officier d'état civil au nom de l'État** :
  répartition des responsabilités État / commune à **vérifier au cas par
  cas** — ne pas inscrire d'office la commune comme responsable unique.
- Registres d'état civil : **textes propres** — code civil et IGREC
  (durées, publicité, délivrance), à vérifier en version en vigueur. Le
  RGPD ne les écrase pas (*lex specialis*, socle §1).
- **COMEDEC** : dispositif national encadré — vérifier la convention et le
  rôle de la commune. **Recensement citoyen** : traitement imposé, base
  légale et transmission au ministère à situer dans les textes (à vérifier).
- Vigilances : délivrance d'actes à des tiers (conditions strictes, à
  vérifier), généalogistes (§5.8), sécurité des registres. Accès aux
  actes ≠ droit d'accès RGPD → `droits-personnes.md`.

### 5.2 Élections

- **Listes électorales** : tenues via le répertoire électoral unique (REU) ;
  répartition des rôles **INSEE / commune** à vérifier avant de qualifier.
- **Communication des listes** : droit de communication organisé par le
  code électoral (électeurs, candidats) sous conditions — finalité
  électorale, non-usage commercial — à vérifier en version consolidée. Ce
  régime spécial prime le raisonnement générique.
- **Frontière stricte fichiers collectivité / usage politique** : les
  fichiers de la collectivité (administrés, GRU, invités) ne servent
  **jamais** la propagande d'un candidat ou d'un élu — **détournement de
  finalité**. Doctrine CNIL élections : à citer **avec sa date de version**.
- Vigilances : période préélectorale (tracer les demandes de listes) ; la
  prospection par les candidats relève de leur propre conformité.

### 5.3 Scolaire, périscolaire, petite enfance

- **Mineurs = personnes vulnérables** : risque relevé d'office ; **AIPD
  fréquente** — vérifier les listes CNIL → `aipd.md`.
- Points de conformité : inscriptions, transports, cantine (régimes
  alimentaires = données révélatrices possibles de convictions ou de
  santé), **portails familles** et **paiement en ligne**
  (→ `sous-traitance-transferts.md`).
- **PAI et données de santé** : données sensibles (art. 9 RGPD — à
  confirmer en version consolidée) ; accès limité au personnel habilité,
  pas de diffusion large des protocoles.
- **Photos des enfants** : autorisation parentale distincte par usage ;
  cumul droit à l'image + données personnelles (§5.9, piège §8).
- **Base élèves / ONDE** : traitement de l'Éducation nationale — la commune
  reste responsable de ses fichiers et de ses transmissions (à vérifier).
- Renvois : information des familles → `droits-personnes.md` ; durées →
  référentiels CNIL datés + archives §5.11.

### 5.4 Action sociale (CCAS / CIAS)

- **Le CCAS est une personne morale distincte** : responsable de traitement
  à part entière (registre, mentions propres) ; ne pas le fondre dans la
  commune.
- **Données sensibles par nature** (santé, précarité, vie familiale) :
  risque élevé par défaut ; AIPD à examiner systématiquement → `aipd.md`.
- **Registre canicule / personnes vulnérables** : base légale propre, CGCT
  et textes du plan d'alerte — à vérifier. Information obligatoire ;
  destinataires limités (transmission au préfet encadrée — à vérifier).
- **Domiciliation** : procédure CASF (à vérifier) ; population très
  vulnérable, confidentialité renforcée. **Aide sociale légale /
  facultative** : distinguer — textes, destinataires et durées diffèrent.
- **Secret professionnel des travailleurs sociaux** : s'ajoute au RGPD ; le
  partage d'informations obéit à ses propres règles (CASF — à vérifier).
  Les deux cadres se cumulent.
- Renvois : demandes de tiers → `droits-personnes.md` ; logiciels métier
  → `sous-traitance-transferts.md`.

### 5.5 Urbanisme, logement, GRU

- **Autorisations d'urbanisme** : téléservice SVE et dématérialisation ADS —
  obligations issues du CRPA et des textes de dématérialisation, à
  vérifier. Qualifier les rôles (commune, centre instructeur, plateformes).
- **Publicité vs données des pétitionnaires** : documents publics dans les
  conditions des textes, mais la mise en ligne impose l'**occultation des
  données personnelles** non nécessaires (coordonnées, signatures) —
  doctrine CNIL/CADA à dater. Ne jamais publier un dossier brut.
- **Signalements des administrés** : données sur l'auteur ET la personne
  visée ; information des deux à examiner (art. 14 — à confirmer) ; durées
  courtes ; finalité répressive → STOP RÉGIME (`analyse-situation.md` §2).
- **GRU et courriers** : minimiser les champs libres (proscrire les
  commentaires subjectifs) ; durées liées à la demande, référentiels CNIL
  datés ; formulaires et hébergement → §5.9.

### 5.6 Vidéoprotection et sécurité

- **Renvoi principal** : autorisation préfectorale (CSI), doctrine d'emploi,
  déport aux forces de l'État → skill **dpm-fpt**. Ne pas dérouler ici.
- Volet données traité ici : **registre** (→ `gouvernance-registre.md`) ;
  **information du public** (panneaux + mention complète — doctrine CNIL, à
  dater) ; **durées** (fixées par l'autorisation et les textes — aucune
  valeur de mémoire) ; **droits des personnes filmées**
  (→ `droits-personnes.md`) ; **AIPD** (surveillance systématique d'un lieu
  public = risque élevé, listes CNIL à vérifier → `aipd.md`).
- **Caméras-piétons et vidéoverbalisation** : régime **Police-Justice**
  probable → `analyse-situation.md` §2 ; opérationnel → **dpm-fpt**. Un
  même parc peut relever de **deux régimes selon la finalité** : découper.

### 5.7 Ressources humaines

- **Renvoi principal** : fond statutaire (carrière, paie, discipline) →
  skill **drh-fpt**. Ne pas dérouler ce fond ici.
- Conformité RH traitée ici : **SIRH et dossiers agents** (registre,
  durées — référentiels CNIL datés + archives §5.11, habilitations) ;
  **badgeage** (finalité, proportionnalité) ; **géolocalisation des
  véhicules** (finalités admises limitées, désactivation hors service —
  doctrine CNIL à dater) ; **vidéosurveillance des locaux** (pas de
  surveillance permanente des postes) ; **données syndicales** = **données
  sensibles** (art. 9 — à confirmer) — cloisonner, hors dossier de carrière.
- Tout dispositif de contrôle : **information individuelle des agents** et
  consultation des instances compétentes (compétence exacte → **drh-fpt**).
  Accès de l'agent à son dossier → `droits-personnes.md`.

### 5.8 Cimetières et funéraire

- **Concessions et registres** : encadrés par le CGCT (à vérifier) ; durées
  longues (concessions + archives §5.11) — pas de minimisation standard.
- Le RGPD protège les **vivants** ; les données des défunts relèvent d'un
  régime particulier (directives post-mortem, loi 78-17 — à vérifier) et
  révèlent souvent des données sur les vivants (filiation).
- **Généalogistes** : distinguer archives publiques communicables (délais
  du code du patrimoine — à vérifier) et fichiers vivants de gestion.
  Tracer les communications.

### 5.9 Téléservices, site web, communication

- **Cookies et traceurs** : consentement préalable sauf exemptions —
  doctrine CNIL à citer **avec sa date de version** ; auditer le site réel,
  pas la promesse de l'éditeur.
- **Formulaires en ligne** : minimisation, mention d'information (art. 13 —
  à confirmer) au point de collecte, champs facultatifs signalés.
- **Newsletters** : cas où le **consentement est la bonne base légale**
  (exception au socle §4) — inscription libre, pas de pré-cochage.
- **Photos et vidéos d'événements** : **droit à l'image ET protection des
  données cumulés** (piège §8) ; autorisation par support ; mineurs → §5.3.
- **Réseaux sociaux de la commune** : la commune répond de ses pages
  (statistiques d'audience — jurisprudence CJUE via `recherche-juridique`) ;
  modérer les commentaires nominatifs ; aucun ciblage depuis les fichiers.
- **Bulletin municipal** : publications nominatives à fonder ; la rubrique
  état civil suppose l'accord des intéressés — doctrine à vérifier et dater.
- Renvois : hébergeur, éditeur, emailing → `sous-traitance-transferts.md` ;
  sécurité du site → `securite-traitements.md`.

### 5.10 Open data et réutilisation

- **Obligation d'ouverture** : CRPA et loi pour une République numérique —
  périmètre et seuils à vérifier. L'ouverture ne neutralise **jamais** la
  protection des données ; les deux corpus s'articulent.
- **Règle d'or avant publication** : anonymisation réelle (démontrable —
  doctrine CNIL/CEPD à dater), occultation, ou texte permettant la
  diffusion — à vérifier au cas par cas.
- **Délibérations et actes en ligne** : occulter les données personnelles
  avant mise en ligne — doctrine CNIL/CADA à dater. La transparence de
  l'acte n'exige pas l'exposition des personnes.
- **Subventions** : publication des données essentielles encadrée par des
  textes propres (à vérifier) ; distinguer personnes morales et physiques.
- Vigilance : un jeu « pseudonymisé » reste personnel ; la réidentification
  par croisement est le risque central à l'échelle communale.

### 5.11 Archives

- **Renvoi sans duplication** : appliquer le réflexe « archives publiques »
  du socle (`socle-sources-verification.md` §4) — effacement RGPD articulé
  avec le code du patrimoine et le visa d'élimination (à confirmer).
- Une seule consigne ici : **aucune conclusion « supprimer / purger » sans
  ce croisement**. Une durée d'utilité courante débouche sur un sort final
  (élimination visée ou versement), pas sur une suppression sèche.

---

## 6. Procédures et délais

- Pas de délai propre : 72 h, 1 mois, consultation → branches transverses.
- Séquence **mise en conformité d'un service existant** : cartographier →
  registre → bases légales et durées (textes sectoriels d'abord) →
  information → sous-traitants et sécurité → prioriser par risque (§11).
  Annoncer les hypothèses ; demander ce qui manque.

---

## 7. Déclencheurs de vérification

Appliquer le socle-sources (matrice §2.2 du `SKILL.md`) avant de conclure
sur :

- la **base légale** et toute **durée de conservation** d'un traitement
  sectoriel (texte imposant le traitement, référentiel CNIL daté) ;
- le **régime de publicité ou de communication** d'un document (état civil,
  listes électorales, urbanisme, actes en ligne) ;
- la **répartition des responsabilités** commune / État / CCAS / EPCI ;
- le caractère **obligatoire d'une AIPD** (listes CNIL en vigueur) ;
- toute **doctrine CNIL ou CADA** mobilisée (version à dater) ;
- la **qualification de régime** aux frontières PM (`analyse-situation.md`).

---

## 8. Pièges & confusions fréquentes

- **« Traitement imposé par l'État = commune dispensée »** : faux. La
  commune conserve des obligations sur son périmètre (registre, sécurité,
  information). Déterminer qui fait quoi, jamais « personne ».
- **Publier des délibérations ou arrêtés nominatifs sans occultation**
  (§5.10) : transparence de l'acte ≠ exposition des personnes.
- **Réutiliser un fichier de service pour la communication ou les vœux du
  maire** : détournement de finalité, aggravé en période électorale (§5.2).
  Bloquer ; proposer la voie licite (consentement dédié).
- **Confondre droit à l'image et protection des données** : les deux
  s'appliquent — une autorisation d'image ne vaut pas conformité RGPD, et
  inversement.
- **Fondre le CCAS dans la commune** (§5.4) : registres, mentions et
  réponses aux personnes erronés en cascade.
- **Retenir le consentement pour un service public obligatoire** :
  requalifier (socle §4) ; pertinent pour le seul facultatif.
- **Conclure « supprimer » sans le croisement archives** (§5.11).
- **Analyser la vidéoverbalisation sous le seul RGPD** : erreur de régime →
  `analyse-situation.md` §2.

---

## 9. Données / références à vérifier

Ne jamais citer de mémoire ; vérifier en version consolidée ou dater :

- Code civil et IGREC (état civil : tenue, publicité, délivrance).
- Code électoral (REU, communication des listes, conditions).
- Code de l'éducation (transmissions scolaires, ONDE).
- CGCT (registre canicule, cimetières, publicité des actes).
- CASF (domiciliation, aide sociale, partage d'informations).
- Code de l'urbanisme + CRPA (SVE, ADS, publicité, open data) ; loi pour
  une République numérique (seuils).
- CSI (vidéoprotection, caméras-piétons — via `dpm-fpt`).
- Code du patrimoine (communicabilité, élimination).
- Référentiels et durées CNIL sectoriels (collectivités, GRU, RH, vidéo) ;
  doctrine élections, cookies et traceurs, publication des documents
  administratifs (CNIL/CADA) ; listes AIPD — **toujours dater la version**.

---

## 10. Livrables

- **Avis DPO sectoriel** → `assets/avis-dpo-modele.md`.
- **Fiche de registre** par traitement → `assets/fiche-registre-modele.md`.
- **AIPD** (scolaire, action sociale, vidéo) → `assets/aipd-modele.md`.
- **Mention d'information** → `assets/mention-information-modele.md`.
- **Réponse à une demande de droits** → `assets/reponse-droits-modele.md`.
- Éléments obligatoires communs : responsable de traitement exact, régime,
  base légale sourcée ou « à vérifier », renvois aux branches mobilisées,
  recommandation finale au responsable de traitement.

---

## 11. Double échelle [risque / confiance]

Repères par famille (cf. `SKILL.md` §5.1) :

- **Critique** : action sociale (données sensibles + personnes
  vulnérables), données de santé scolaires (PAI), régime mal qualifié.
- **Élevé** : scolaire et petite enfance (mineurs, grande échelle),
  vidéoprotection, publication non occultée, fichiers en période
  électorale, données syndicales.
- **Moyen** : GRU, urbanisme courant, téléservices standard, funéraire.
- **Faible** : traitements internes sans donnée sensible ni diffusion.
- **Confiance** : « stable » pour les principes ; « à vérifier » pour toute
  durée, publicité, répartition État/commune et doctrine non datée en
  session ; « jurisprudentiel » pour réseaux sociaux et open data fins.

---

## 12. Checklist de branche

1. Routeur passé : régime et **responsable de traitement** (commune, CCAS,
   État, EPCI) désignés ?
2. Texte sectoriel identifié — « à confirmer en version consolidée » si
   non vérifié en session ?
3. Base légale sans consentement par défaut (sauf facultatif réel) ?
4. Personnes vulnérables ou données sensibles → risque relevé, AIPD
   examinée ?
5. Publication ou transmission → occultation / anonymisation traitée ?
6. Frontière fichiers de service / usage politique vérifiée si élu en cause ?
7. Cumul droit à l'image + données personnelles traité si images ?
8. Croisement archives fait avant toute conclusion d'effacement ?
9. Doctrine CNIL / CADA citée **avec sa date** ?
10. Renvois `dpm-fpt` / `drh-fpt` et branches transverses sans duplication ?
11. Sortie = recommandation au responsable de traitement, pas décision
    (garde-fou §5.2.a) ?
