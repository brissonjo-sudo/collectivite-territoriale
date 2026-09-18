# Branche — AIPD (analyse d'impact relative à la protection des données)

## 1. Périmètre / Exclusions

Cette branche couvre l'**opportunité** d'une AIPD (obligatoire, recommandée
ou dispensée), sa **réalisation** selon la méthode CNIL (PIA), et la
**consultation préalable** de la CNIL (art. 36 RGPD — à confirmer en version
consolidée).

**Exclusions** — renvoyer par pointeur, ne pas traiter ici :
- mesures de **sécurité** de fond (art. 32) → `securite-traitements.md` ;
  l'AIPD les évalue, elle ne les définit pas ;
- contenu et tenue du **registre** → `gouvernance-registre.md` ;
- encadrement du sous-traitant qui participe à l'AIPD →
  `sous-traitance-transferts.md` ;
- qualification initiale (régime, responsable de traitement) → routeur
  `analyse-situation.md`.

## 2. Questions couvertes

- « Faut-il une AIPD pour ce projet (vidéoprotection, téléservice,
  logiciel social, dispositif scolaire...) ? »
- « Comment mener l'AIPD ? Avec quel outil, quelle méthode ? »
- « Le prestataire fournit une AIPD : suffit-elle ? »
- « Le risque résiduel reste élevé : que faire ? »
- « Le traitement a évolué : faut-il refaire l'AIPD ? Quel rôle pour le
  DPO ? »

## 3. Arbre de traitement

1. **Question** : opportunité, réalisation, ou consultation préalable ?
2. **Variables à lever** (§4) : régime, responsable de traitement, critères
   de risque, état d'avancement du projet.
3. **Décision opportunité** : listes CNIL (obligatoire / dispensée)
   → sinon critères CEPD (règle des 2 critères) → sinon appréciation
   « risque élevé probable » (art. 35 — à confirmer).
4. **Vérification** : listes et critères jamais tranchés de mémoire (§7).
5. **Livrable** : trame AIPD, avis DPO, ou note d'opportunité (§10).

## 4. Variables à lever

- **Régime** : RGPD ou Police-Justice ? Le régime Police-Justice comporte
  une **analyse d'impact spécifique** (titre III loi 78-17 — à vérifier en
  session) : ne pas dérouler l'AIPD RGPD sans ce contrôle (STOP RÉGIME,
  `SKILL.md` §5.2.b).
- **Responsable de traitement** : commune, EPCI, CCAS ? L'AIPD est **sa**
  responsabilité, pas celle du DPO ni du sous-traitant.
- **État du projet** : pas encore déployé (situation nominale) ou déjà en
  production (AIPD de régularisation, à signaler comme telle) ?
- **Critères de risque** présents : données sensibles, mineurs ou personnes
  vulnérables, grande échelle, surveillance, croisement, décision
  automatisée, usage innovant (§5.2).
- **Traitement figurant sur une liste CNIL** (obligatoire ou dispensée) ?
- **Sous-traitant** impliqué et éléments qu'il doit fournir (assistance
  art. 28 — à confirmer) ; AIPD existante à réviser ou première analyse ?

## 5. Règles métier

### 5.1 Logique de l'obligation (art. 35)

- Une AIPD s'impose quand le traitement est **susceptible d'engendrer un
  risque élevé** pour les droits et libertés des personnes (art. 35 RGPD —
  à confirmer en version consolidée).
- Ordre d'analyse : **liste CNIL « AIPD obligatoire »** (dispense de
  raisonner) → **liste CNIL « AIPD dispensée »** (dispense inverse) →
  **critères CEPD** hors listes. Les deux listes se vérifient en ligne à
  chaque usage, versions **datées** (délibérations CNIL — identifiants à
  récupérer en session, jamais de mémoire).
- Dans le doute, la CNIL recommande de mener l'AIPD : bonne pratique à
  distinguer de l'obligation.

### 5.2 Les 9 critères G29/CEPD — règle des 2 critères

Lignes directrices sur l'AIPD du G29, endossées par le CEPD (**version et
date à vérifier avant usage**). Les 9 critères, de mémoire de structure —
libellés exacts à confirmer sur la version en vigueur :

1. évaluation ou notation de personnes ;
2. décision automatisée avec effet juridique ou similaire ;
3. surveillance systématique ;
4. données sensibles ou hautement personnelles ;
5. traitement à grande échelle ;
6. croisement ou combinaison d'ensembles de données ;
7. personnes vulnérables (mineurs, bénéficiaires de l'action sociale...) ;
8. usage innovant ou nouvelles technologies ;
9. exclusion du bénéfice d'un droit, d'un service ou d'un contrat.

**Règle des 2 critères** : deux critères remplis → AIPD en principe
requise. Un seul critère peut suffire si le risque est manifeste :
l'appréciation se motive, dans un sens comme dans l'autre.

### 5.3 Cas fréquents en collectivité qui déclenchent

- **Vidéoprotection étendue** (surveillance systématique de la voie
  publique, souvent grande échelle) — volet autorisation → `dpm-fpt`.
- **Téléservices avec comptes ou profils** d'usagers (évaluation +
  grande échelle possibles).
- **Action sociale** (CCAS : données sensibles + personnes vulnérables —
  souvent 2 critères d'emblée).
- **Dispositifs scolaires et périscolaires** (mineurs + échelle ; ENT,
  portails familles, biométrie de cantine — régime spécifique à vérifier).
- **Géolocalisation** (véhicules, agents, applications) : surveillance
  systématique probable ; volet RH → frontière `drh-fpt`.

Confronter chaque cas aux listes CNIL en vigueur avant de conclure.

### 5.4 Réalisation — méthode CNIL (PIA)

- **Quatre parties** : contexte (description du traitement) ; principes
  fondamentaux (finalité, minimisation, durées, information, droits —
  conformité de fond) ; risques (sécurité : accès illégitime, modification
  non désirée, disparition — vraisemblance × gravité) ; validation
  (décision du responsable de traitement).
- **Outil PIA de la CNIL** : logiciel libre recommandé, non obligatoire.
  Version à dater si citée.
- L'AIPD se mène **AVANT la mise en œuvre** du traitement. Projet déjà
  déployé : AIPD de régularisation, l'écart se signale au responsable de
  traitement.
- **Avis du DPO formalisé dans l'AIPD** (art. 35.2 — à confirmer) : le
  DPO conseille et rend un avis écrit ; il ne rédige pas l'AIPD à la place
  du responsable de traitement et ne la « valide » pas (garde-fou
  `SKILL.md` §5.2.a).
- Mesures de sécurité évaluées ici, définies ailleurs →
  `securite-traitements.md`.
- **Révision** : à chaque évolution substantielle du traitement (finalité,
  périmètre, technologie, sous-traitant) et à échéance régulière (bonne
  pratique : revue périodique, à intégrer au plan d'action →
  `gouvernance-registre.md`).

### 5.5 Consultation préalable de la CNIL (art. 36)

- Déclencheur : le **risque résiduel reste élevé** malgré les mesures
  prévues (art. 36 — à confirmer en version consolidée).
- La consultation précède la mise en œuvre ; le traitement attend. Contenu
  du dossier et délais de réponse CNIL : à vérifier en ligne.
- Alternative à instruire d'abord : renforcer les mesures pour ramener le
  risque résiduel à un niveau acceptable.

## 6. Procédures et délais

1. **Opportunité** : dérouler §5.1-§5.3 ; tracer la conclusion même
   négative (accountability → `gouvernance-registre.md`).
2. **Cadrage** : responsable de traitement désigné, équipe (métier, DSI,
   sous-traitant), calendrier **avant mise en œuvre**.
3. **Réalisation** : quatre parties (§5.4) ; éléments du sous-traitant
   exigés au titre de l'assistance art. 28 —
   → `sous-traitance-transferts.md`.
4. **Avis du DPO** : écrit, joint à l'AIPD.
5. **Validation** : décision du responsable de traitement (accepter les
   risques résiduels, renforcer, renoncer).
6. **Si risque résiduel élevé** : consultation préalable CNIL (§5.5).
7. **Vie du traitement** : révision sur évolution ; lien registre
   (→ `gouvernance-registre.md`) et sécurité (→ `securite-traitements.md`).

Aucun délai chiffré de cette branche ne se cite de mémoire.

## 7. Déclencheurs de vérification

Appliquer le socle-sources (`socle-sources-verification.md`) avant de
conclure sur :

- **caractère obligatoire** d'une AIPD (matrice §2.2 : ligne dédiée —
  vérification systématique des listes CNIL, versions datées) ;
- libellé et portée des **critères CEPD** (version des lignes directrices) ;
- **régime Police-Justice** et son analyse d'impact spécifique (loi 78-17,
  jamais de mémoire) ;
- procédure et délais de la **consultation préalable** art. 36 ;
- régimes sectoriels particuliers (biométrie scolaire, vidéoprotection —
  textes à vérifier) ;
- toute base légale ou durée reprise dans l'AIPD (matrice §2.2).

## 8. Pièges & confusions fréquentes

- **AIPD faite après le déploiement** : contraire à la logique de
  l'art. 35. Régulariser, le dire, et corriger le circuit projet pour la
  suite.
- **AIPD confondue avec la fiche de registre** : la fiche décrit, l'AIPD
  évalue les risques → `gouvernance-registre.md`.
- **« On a toujours fait comme ça »** : l'ancienneté d'un traitement ne
  dispense de rien ; les traitements antérieurs à 2018 restent soumis à
  l'obligation si le risque est élevé.
- **AIPD générique du sous-traitant** : un document éditeur non
  contextualisé ne vaut pas AIPD du responsable de traitement. Il sert
  d'intrant ; l'analyse se refait sur le traitement réel de la
  collectivité.
- **Oublier le régime Police-Justice** : analyse d'impact spécifique du
  titre III (à vérifier) — ne pas plaquer la trame RGPD.
- **DPO rédacteur-valideur** : cumul à écarter ; le DPO conseille et rend
  un avis, le responsable de traitement porte et valide (§5.2.a).
- **« Pas d'AIPD » sans trace écrite** : l'absence d'AIPD se motive et se
  documente.

## 9. Données / références à vérifier

Ne jamais citer de mémoire sans réserve :

- Art. 35 et 36 RGPD — structure stable, citer avec « à confirmer en
  version consolidée » sauf vérification en session.
- Loi 78-17 (analyse d'impact Police-Justice, titre III) : **aucun article
  de mémoire** — vérification en session obligatoire.
- **Listes CNIL** AIPD obligatoire / dispensée : délibérations à récupérer
  en session (règle de provenance des identifiants), version **datée**.
- **Lignes directrices G29/CEPD sur l'AIPD** : version et date à confirmer
  avant d'invoquer les 9 critères.
- Outil PIA et guides CNIL : version à dater.
- Délais et modalités de la consultation préalable art. 36.

## 10. Livrables

- **Trame AIPD** (méthode CNIL, quatre parties) → `assets/aipd-modele.md`.
  Éléments obligatoires : description, nécessité et proportionnalité,
  risques, mesures, **avis du DPO**, décision du responsable de traitement.
- **Avis DPO** (opportunité ou avis formalisé dans l'AIPD) →
  `assets/avis-dpo-modele.md`. Comporte toujours : rappel du rôle
  consultatif, analyse, niveau de risque, recommandation au responsable de
  traitement.
- **Note d'opportunité** (AIPD requise ou non) : pas de générateur dédié ;
  motiver par listes CNIL datées + critères CEPD + conclusion tracée. Cas
  incomplet → brouillon `[INCOMPLET]`, champs manquants listés
  (`SKILL.md` §6).

## 11. Double échelle [risque / confiance]

- **Pédagogie de la méthode, outil PIA** : risque faible, confiance
  stable → réponse directe.
- **Opportunité d'une AIPD** : risque moyen à élevé (une AIPD manquante
  expose à sanction), confiance « à vérifier » → listes CNIL vérifiées et
  datées avant conclusion.
- **AIPD sur données sensibles, mineurs, action sociale, surveillance** :
  risque élevé → citation de source, réserve « à confirmer ».
- **Consultation préalable, frontière Police-Justice** : risque critique →
  double vérification ; abstention si le doute persiste ; croiser
  `relations-cnil.md` et `recherche-juridique`.


## 12. Checklist de branche

1. Régime identifié — analyse d'impact Police-Justice envisagée si finalité
   pénale (STOP RÉGIME) ?
2. Responsable de traitement désigné — l'AIPD portée par lui, pas par le
   DPO ni le sous-traitant ?
3. Listes CNIL consultées et **datées** avant conclusion d'opportunité ?
4. Critères CEPD comptés, version des lignes directrices datée ?
5. Conclusion d'opportunité **tracée**, y compris négative ?
6. AIPD menée (ou replanifiée) **avant** mise en œuvre — régularisation
   signalée sinon ?
7. Avis du DPO formalisé, distinct de la validation (garde-fou §5.2.a) ?
8. Risque résiduel élevé → consultation préalable art. 36 envisagée,
   modalités à vérifier ?
9. Personnes vulnérables ou données sensibles → niveau de risque relevé
   (échelle §5.1) ?
10. Renvois registre / sécurité / sous-traitance faits par pointeur ;
    références avec réserve « à confirmer en version consolidée » ; aucune
    délibération CNIL citée sans récupération en session ?
