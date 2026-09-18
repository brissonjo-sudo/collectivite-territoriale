# Branche — Gouvernance & registre

## 1. Périmètre / Exclusions

Cette branche couvre la désignation et le positionnement du DPO (art. 37 à
39 RGPD — à confirmer en version consolidée), le registre des activités de
traitement (art. 30 — à confirmer en version consolidée), l'accountability et
la documentation de conformité, la politique de protection des données, la
sensibilisation des agents et des élus, et le pilotage de la conformité (plan
d'action, bilan annuel au responsable de traitement).

**Exclusions** — renvoyer par pointeur, ne pas traiter ici :
- réalisation et opportunité d'une **AIPD** → `aipd.md` ;
- mesures de **sécurité** de fond (art. 32) → `securite-traitements.md` ;
- encadrement de la **sous-traitance** et transferts →
  `sous-traitance-transferts.md` ;
- qualification initiale d'une situation → routeur `analyse-situation.md`.

## 2. Questions couvertes

- « Devons-nous désigner un DPO ? Qui peut l'être ? Où le rattacher ? »
- « Que doit contenir le registre ? Comment le structurer ? »
- « Comment créer / mettre à jour une fiche de registre pour ce projet ? »
- « Comment prouver notre conformité (accountability) ? »
- « Comment sensibiliser les agents et les élus ? »
- « Que mettre dans le bilan annuel et le plan d'action ? »

## 3. Arbre de traitement

1. **Question** : gouvernance (DPO, politique, pilotage) ou registre
   (fiche, mise à jour, structure) ?
2. **Variables à lever** (§4) : responsable de traitement, entités
   satellites, régime, traitement nouveau ou existant.
3. **Décision** : appliquer les règles métier (§5) ; distinguer obligation
   et bonne pratique.
4. **Vérification** : déclencheurs §7 → socle-sources avant de conclure.
5. **Livrable** : fiche de registre, avis DPO, ou plan d'action (§10).

## 4. Variables à lever

- **Responsable de traitement** : commune, EPCI, CCAS (personne morale
  distincte), syndicat, caisse des écoles ? Chaque personne morale tient
  **son propre registre**.
- **Régime** : RGPD ou Police-Justice (STOP RÉGIME, `SKILL.md` §5.2.b) ?
  Les traitements Police-Justice figurent au registre avec leurs
  particularités.
- **Rôle** : la collectivité agit-elle en responsable de traitement ou en
  sous-traitant (ex. prestation pour une autre collectivité) ? Le registre
  du sous-traitant est **distinct** (contenu propre — à vérifier).
- **Traitement nouveau ou modifié** : impact registre immédiat ; impact
  AIPD → `aipd.md`.
- **Existence** d'un DPO désigné, de ses moyens, de son rattachement.
- Traitements **papier** et traitements portés par des tiers (logiciels
  métiers, téléservices mutualisés) inclus dans l'inventaire ?

## 5. Règles métier

### 5.1 Désignation du DPO

- **Obligation** : tout organisme public désigne un DPO (art. 37 RGPD — à
  confirmer en version consolidée). Aucune commune, aucun EPCI, aucun CCAS
  n'y échappe, quelle que soit sa taille.
- Le DPO peut être **interne, mutualisé ou externe**. La posture de DPO
  mutualisé n'est pas couverte par ce skill (`SKILL.md` §8) ; signaler la
  limite si le cas se présente.
- **Publier** les coordonnées du DPO (site, mentions) et les **communiquer
  à la CNIL** via le téléservice de désignation (procédure à vérifier en
  ligne, version datée).
- Une même personne peut être DPO de plusieurs personnes morales
  (commune + CCAS + caisse des écoles) : une **désignation par entité**.

### 5.2 Positionnement et moyens

- **Indépendance** : le DPO ne reçoit aucune instruction sur l'exercice de
  ses missions et ne peut être sanctionné pour les avoir exercées
  (art. 38 RGPD — à confirmer en version consolidée).
- **Absence de conflit d'intérêts** : le DPO ne détermine ni les finalités
  ni les moyens des traitements. Écarter les cumuls à risque : DSI
  décisionnaire, DGS, porteur du projet analysé. La liste des fonctions
  incompatibles types figure dans les lignes directrices DPO du G29/CEPD
  (WP243 — dater la version) ; le « responsable du service informatique »
  y est cité expressément. Signaler tout conflit (garde-fou `SKILL.md`
  §5.2.a).
- **Précédents de sanction** : des autorités de contrôle européennes ont
  déjà sanctionné des organismes pour conflit d'intérêts du DPO, et la
  CJUE a précisé les critères d'appréciation du cumul. Quand la question
  se pose, **signaler que ces précédents existent et les rechercher en
  session** (registre des sanctions CNIL/CEPD, jurisprudence CJUE) — ne
  jamais citer un numéro de décision ou d'arrêt de mémoire : l'attribution
  erronée d'une jurisprudence est l'erreur la plus dommageable dans un
  avis (règle de provenance, socle §6).
- **Rattachement** : accès direct au niveau le plus élevé — maire ou
  président de l'exécutif, responsable de traitement.
- **Moyens** : temps dédié, formation, accès aux services et aux données
  nécessaires. L'absence de moyens se documente et se signale au
  responsable de traitement.
- Le DPO **conseille, informe, contrôle** — il ne décide pas. Rappel
  systématique dans les livrables (garde-fou §5.2.a).

### 5.3 Registre des activités de traitement

- **Obligation** pour tout responsable de traitement public, y compris les
  petites communes : la dérogation « moins de 250 employés » ne couvre pas
  les traitements non occasionnels (art. 30.5 — à confirmer en version
  consolidée). En pratique : registre requis.
- **Unité de base : la finalité.** Un traitement = une finalité principale.
  Une fiche par finalité, pas par logiciel : un même logiciel peut porter
  plusieurs traitements ; une même finalité peut mobiliser plusieurs outils.
- **Contenu obligatoire d'une fiche** (art. 30.1 — à confirmer en version
  consolidée) : finalités ; catégories de personnes concernées et de
  données ; destinataires ; durées de conservation ; description générale
  des mesures de sécurité ; transferts hors UE le cas échéant ; identité du
  responsable de traitement et coordonnées du DPO.
- **Registre du sous-traitant** : document distinct, contenu propre
  (art. 30.2 — à confirmer). Le tenir si la collectivité traite pour le
  compte d'un tiers.
- Inclure les traitements **papier** et les traitements Police-Justice
  (avec le régime signalé sur la fiche).
- **Mise à jour** : à chaque projet nouveau ou modifié. Brancher le réflexe
  registre sur les circuits existants (marchés, délibérations, projets
  DSI) : aucun projet ne passe sans question registre.
- Le modèle de registre CNIL est une **bonne pratique**, pas une forme
  imposée (version à dater si citée).

### 5.4 Accountability et documentation

- Principe : **prouver** la conformité, pas seulement l'affirmer
  (art. 5.2 et 24 RGPD — à confirmer en version consolidée).
- Dossier de conformité type : registre + AIPD (→ `aipd.md`) + mentions
  d'information (→ `droits-personnes.md`) + contrats art. 28
  (→ `sous-traitance-transferts.md`) + procédures internes (violations,
  droits, habilitations) + preuves de sensibilisation.
- **Politique de protection des données** : document-chapeau validé par le
  responsable de traitement ; engagement, organisation, rôles, procédures.
  Bonne pratique structurante, à distinguer des obligations.

### 5.5 Sensibilisation et pilotage

- **Sensibiliser** agents et élus : sessions ciblées par métier (accueil,
  état civil, action sociale, DSI, PM), tracées (dates, présents, supports)
  au titre de l'accountability.
- **Plan d'action** : priorisation par le risque pour les personnes
  (échelle `SKILL.md` §5.1), échéances, porteurs. Livrable de pilotage.
- **Bilan annuel** au responsable de traitement : état du registre, AIPD
  menées, violations, demandes de droits, actions réalisées et restantes.
  Formalise le rôle de contrôle du DPO ; la décision sur les suites reste
  au responsable de traitement.

## 6. Procédures et délais

- **Désignation CNIL** : formalité en ligne à la prise de fonction et à
  chaque changement de DPO ; modalités à vérifier sur cnil.fr (version
  datée).
- **Mise à jour du registre** : au fil de l'eau, avant la mise en œuvre du
  traitement nouveau ou modifié ; revue globale au moins annuelle,
  adossée au bilan.
- **Communication du registre** : tenu à la disposition de la CNIL sur
  demande. Son statut au regard du droit d'accès aux documents
  administratifs (CRPA) est à vérifier avant toute communication à un
  tiers.
- Aucun autre délai réglementaire propre à cette branche : les délais
  cités ailleurs (72 h, 1 mois) relèvent de `violations.md` et
  `droits-personnes.md`.

## 7. Déclencheurs de vérification

Appliquer le socle-sources (`socle-sources-verification.md`) avant de
conclure sur :

- contenu **obligatoire** d'une fiche de registre ou du registre
  sous-traitant (matrice §2.2 : contenu obligatoire d'un document) ;
- portée exacte de la **dérogation art. 30.5** ;
- règles d'**incompatibilité** et de positionnement du DPO (art. 38, lignes
  directrices CEPD sur les DPO — à dater) ;
- **procédure de désignation** CNIL en vigueur ;
- communicabilité du registre (CRPA, doctrine CADA/CNIL — à dater) ;
- toute question de base légale ou de durée portée par une fiche (matrice
  §2.2).

## 8. Pièges & confusions fréquentes

- **DPO porteur de projet** : conflit d'intérêts. Le DPO ne peut pas
  rendre un avis sur un traitement dont il détermine finalités ou moyens.
  Signaler, proposer un portage alternatif.
- **Registre = inventaire d'applications** : non. L'inventaire technique
  est un intrant utile ; le registre recense des **traitements par
  finalité**, y compris papier et hors logiciel.
- **Une fiche par logiciel** : erreur symétrique. Repartir de la finalité.
- **« Petite commune, registre facultatif »** : faux en pratique (§5.3).
- **Oublier le CCAS** : personne morale distincte, responsable de ses
  traitements, **son propre registre**, sa propre désignation de DPO. Même
  vigilance pour la caisse des écoles.
- **Oublier les traitements papier** (cahiers, dossiers, listes) : le RGPD
  couvre les fichiers manuels structurés.
- **Confondre registre et AIPD** : le registre décrit, l'AIPD évalue le
  risque → `aipd.md`.
- **Avis DPO présenté comme une autorisation** : reformuler (garde-fou
  §5.2.a).

## 9. Données / références à vérifier

Ne jamais citer de mémoire sans réserve :

- Art. 30, 37, 38, 39, 5.2, 24 RGPD — structure stable, citer avec
  « à confirmer en version consolidée » sauf vérification en session.
- Loi 78-17 : **aucun article de mémoire** (numérotation remaniée) —
  vérifier en session toute disposition nationale invoquée.
- Lignes directrices CEPD (ex-G29) sur les délégués à la protection des
  données : **dater la version**.
- Modèles, guides et téléservice de désignation CNIL : vérifier en ligne,
  **dater**.
- Doctrine CADA / CNIL sur la communicabilité du registre : à dater.

## 10. Livrables

- **Fiche de registre** (création ou mise à jour) →
  `assets/fiche-registre-modele.md`. Éléments obligatoires : ceux de
  l'art. 30.1 (§5.3), régime signalé, date de mise à jour.
- **Avis DPO** (désignation, organisation, arbitrage de gouvernance) →
  `assets/avis-dpo-modele.md`. Comporte toujours : rappel du rôle
  consultatif, analyse, niveau de risque, recommandation au responsable de
  traitement.
- **Plan d'action / bilan annuel** : pas de générateur dédié ; structurer
  selon §5.5 (état des lieux, priorités par risque, échéances, porteurs).
- Cas incomplet → ne jamais halluciner : produire un brouillon marqué
  `[INCOMPLET]` listant les champs manquants (`SKILL.md` §6).

## 11. Double échelle [risque / confiance]

- **Structure du registre, pédagogie accountability** : risque faible à
  moyen, confiance stable → réponse directe.
- **Contenu obligatoire d'une fiche, dérogations art. 30** : risque moyen,
  confiance « à vérifier » → vérification avant usage.
- **Conflit d'intérêts du DPO, positionnement contesté** : risque élevé
  (exposition de la collectivité et du DPO) → citation de source, réserve
  « à confirmer ».
- **Registre absent lors d'un contrôle CNIL** : risque élevé →
  croiser `relations-cnil.md`.

## 12. Checklist de branche

1. Responsable de traitement nommé — CCAS et satellites traités comme
   personnes morales distinctes ?
2. Régime identifié pour chaque traitement inscrit (STOP RÉGIME si
   frontière proche) ?
3. Fiche construite **par finalité**, pas par logiciel ?
4. Contenu obligatoire complet ou champs manquants listés `[INCOMPLET]` ?
5. Traitements papier et sous-traitances couverts ?
6. Registre sous-traitant distinct si la collectivité traite pour un tiers ?
7. Conflit d'intérêts DPO vérifié et signalé le cas échéant (§5.2.a) ?
8. Références citées avec réserve « à confirmer en version consolidée » ;
   doctrine CNIL/CEPD datée ?
9. Sortie formulée en **recommandation** au responsable de traitement,
   jamais en décision ?
10. Renvois AIPD / sécurité / sous-traitance faits par pointeur, sans
    duplication ?
