# Branche — Sous-traitance & transferts

## 1. Périmètre / Exclusions

**Couvre** : la qualification des acteurs (responsable de traitement,
sous-traitant, responsables conjoints — art. 26 RGPD, à confirmer en version
consolidée —, destinataire), le contrat art. 28 et ses clauses obligatoires,
la chaîne de sous-traitance, les transferts hors UE (chap. V RGPD) et les
clauses RGPD dans la commande publique.

**Exclut** : la sécurité de fond (mesures, habilitations, traçabilité) →
`securite-traitements.md` ; la violation chez un sous-traitant →
`violations.md` ; le fond du droit de la commande publique → hors skill,
signaler la limite ; vigueur des textes et jurisprudence CJUE de fond →
`recherche-juridique`.

## 2. Questions couvertes

- Ce prestataire est-il sous-traitant, responsable conjoint ou destinataire ?
- Que doit contenir le contrat art. 28 ? Notre marché est-il conforme ?
- Le sous-traitant peut-il recruter un sous-traitant ultérieur ?
- Cet hébergement (cloud, SaaS) emporte-t-il un transfert hors UE ?
  Quelles garanties exiger d'un éditeur américain ?
- Comment encadrer un échange entre administrations
  (dites-le-nous-une-fois) ? Quelle convention entre commune et CCAS ?

## 3. Arbre de traitement

1. **Question** : qui intervient sur les données, et à quel titre ?
2. **Variables à lever** (§4) : acteurs, rôle réel, localisation, droit
   applicable à l'hébergeur, stade du marché.
3. **Décision** : qualifier chaque acteur → instrument requis (contrat
   art. 28, accord art. 26, convention, mention de destinataire) →
   transfert hors UE ? → outil et mesures supplémentaires éventuelles.
4. **Vérification** : matrice §2.2 du `SKILL.md` — contenu du contrat,
   régime des transferts, jurisprudence CJUE : socle-sources.
5. **Livrable** : avis DPO avec checklist contractuelle (§10).

## 4. Variables à lever

Avant de trancher, clarifier :

- **Qui détermine finalités et moyens** ? Qui exécute sur instructions ?
- **Responsable de traitement** : commune, EPCI, CCAS (personne morale
  distincte), syndicat, État ? → réflexe `socle-sources-verification.md` §4.
- **Régime applicable** : RGPD ou Police-Justice (STOP RÉGIME, `SKILL.md`
  §5.2.b) — les règles de sous-traitance et de transfert diffèrent.
- **Nature de la prestation** : hébergement, édition, maintenance avec
  accès aux données, prestation sans accès ?
- **Localisation** : lieu de stockage, lieux d'**accès** (support, admin à
  distance), droit applicable à la société mère.
- **Stade de la commande publique** : DCE, marché notifié, en exécution ?
- **Chaîne** : sous-traitants ultérieurs déclarés ? Liste disponible ?
- **Données et personnes** : données sensibles, mineurs, action sociale →
  relève le risque (§11).

## 5. Règles métier

### 5.1 Qualification des acteurs

- Applique le critère unique : **qui détermine les finalités et les moyens
  essentiels ?** Celui-là est responsable de traitement.
- Traite comme **sous-traitant** celui qui agit **uniquement sur
  instructions documentées**, pour le compte du responsable de traitement.
- Qualifie de **responsables conjoints** (art. 26 RGPD — à confirmer) ceux
  qui codéterminent finalités ou moyens : exige un **accord de
  responsabilité conjointe**, pas un contrat art. 28.
- Qualifie de **destinataire** l'organisme qui reçoit les données pour ses
  propres besoins : pas de contrat art. 28, mais une base juridique de
  transmission et une mention au registre.
- Requalifie d'après les **faits**, pas d'après l'intitulé du contrat : un
  « sous-traitant » qui réutilise les données pour son compte (statistiques,
  amélioration produit, IA) devient responsable pour ces réutilisations.
- Commune et **CCAS** : deux responsables de traitement distincts. Tout
  partage de moyens ou de données s'encadre par convention. Même réflexe
  avec l'EPCI et les syndicats.

### 5.2 Contrat art. 28 — contenu obligatoire

- Vérifie **chaque élément obligatoire** (art. 28 RGPD — à confirmer en
  version consolidée) : objet, durée, nature et finalité, type de données,
  catégories de personnes ; puis les clauses : **instructions documentées**
  uniquement, **confidentialité** des personnes autorisées, **sécurité**
  (exigences → `securite-traitements.md`), **sous-traitance ultérieure**
  soumise à autorisation écrite avec information préalable de tout
  changement, **assistance** au responsable (droits, sécurité, violations,
  AIPD), **sort des données** en fin de contrat (suppression ou restitution,
  au choix du responsable), **audit** et preuves de conformité.
- Un élément obligatoire manquant = **non-conformité du contrat**, pas une
  simple faiblesse. Dis-le dans l'avis.
- Chaîne : exige la **liste à jour** des sous-traitants ultérieurs et la
  répercussion des mêmes obligations ; une chaîne non tracée = risque en soi.

### 5.3 Commande publique

- Intègre les clauses RGPD **dès le DCE** (CCAP ou annexe dédiée) : après
  notification, l'ajout suppose un avenant, position de faiblesse.
- Fais des exigences RGPD un élément d'**analyse des offres** quand le
  traitement le justifie (hébergement, localisation, certifications).
- Marché en cours sans clause : avenant sans attendre ; documente (accountability).
- Le fond des procédures de marché reste hors skill : signale la limite.

### 5.4 Transferts hors UE (chap. V RGPD)

- Raisonne en trois temps : **1)** y a-t-il transfert (stockage, mais aussi
  simple **accès** depuis un pays tiers, maintenance comprise) ? **2)** quel
  **outil** : décision d'adéquation, clauses contractuelles types (CCT —
  version en vigueur à dater), règles d'entreprise contraignantes,
  dérogations résiduelles ? **3)** l'outil suffit-il en pratique ?
- Post-**Schrems II** (jurisprudence CJUE — à vérifier en session avant
  citation) : les CCT n'exonèrent pas d'une **évaluation du droit du pays
  tiers** ni, si besoin, de **mesures supplémentaires** (chiffrement à clés
  maîtrisées côté UE, pseudonymisation...) — recos CEPD, version à dater.
- Hébergeur soumis à des **lois extraterritoriales** (éditeurs américains) :
  un stockage « en Europe » ne clôt pas l'analyse si la société reste
  soumise à un droit tiers permettant l'accès. Évalue le risque réel,
  documente-le, propose alternatives ou mesures.
- Secteur public : mobilise la doctrine **SecNumCloud / « cloud de
  confiance »** et les circulaires cloud de l'État — à **dater et vérifier**
  en session (versions et champ évolutifs).
- Décisions d'adéquation (dont cadre UE–États-Unis) : **validité à vérifier
  en session** — ne jamais affirmer de mémoire qu'un cadre est en vigueur.

### 5.5 Échanges entre administrations

- Un échange entre administrations (API, dites-le-nous-une-fois, CRPA — à
  vérifier) reste un **traitement à encadrer** : base juridique, finalité,
  minimisation, information des personnes, registre des deux côtés.
- Qualifie l'administration destinataire : le plus souvent **responsable de
  traitement** pour son propre traitement, pas sous-traitant.
- Formalise : convention d'échange ou cadre réglementaire de l'API ;
  textes fondant l'échange (CRPA et application) — à vérifier.

## 6. Procédures et délais

- **Avant contractualisation** : qualification des acteurs → analyse de
  l'offre (localisation, chaîne) → avis DPO → décision du responsable.
- **Marché public** : clauses au DCE → vérification à l'attribution → suivi
  en exécution (sous-traitants ultérieurs, audits).
- **Fin de contrat** : sort des données exécuté, attestation de suppression
  ou restitution ; croiser avec les archives publiques
  (→ `socle-sources-verification.md` §4).
- Aucun délai chiffré cité de mémoire : vérifier à la source.

## 7. Déclencheurs de vérification

Socle-sources obligatoire (matrice §2.2 du `SKILL.md`) pour : contenu
obligatoire du contrat art. 28 ; régime et outils de transfert (chap. V,
CCT, adéquation) ; jurisprudence CJUE (Schrems II et suites, responsabilité
conjointe) ; recommandations CEPD (mesures supplémentaires) ; doctrine
SecNumCloud / cloud de confiance ; textes CRPA sur les échanges entre
administrations ; toute réforme récente du cadre des transferts.

## 8. Pièges & confusions fréquentes

- Qualifier « sous-traitant » un **responsable conjoint** : éditeur qui
  réutilise les données pour son compte, plateforme mutualisée codécidée.
- **Contrat art. 28 absent du marché public** : la clause se prévoit au DCE,
  pas après notification.
- Croire qu'un hébergement « **en Europe** » d'une société américaine règle
  la question du transfert : le droit applicable à la société compte autant
  que la localisation des serveurs.
- **Chaîne non tracée** : découvrir un sous-traitant ultérieur hors UE en
  cours d'exécution.
- **Convention absente entre commune et CCAS** : partage de SI ou d'agents
  entre deux responsables de traitement distincts, sans encadrement.
- Confondre **destinataire** et sous-traitant : imposer un contrat art. 28
  à un organisme qui traite pour son propre compte.
- Retenir une dérogation (art. 49 RGPD — à confirmer) comme outil
  **structurel** : les dérogations restent résiduelles.

## 9. Données / références à vérifier

Ne jamais citer de mémoire ; vérifier en session ou assortir de la réserve :

- Art. 26, 28, 44 et s. (chap. V) RGPD — « à confirmer en version consolidée ».
- **Loi 78-17** et décret 2019-536 — jamais de mémoire, vérification en session.
- **CCT** : décision d'exécution applicable et version — à dater.
- **Décisions d'adéquation** (dont cadre UE–États-Unis) — validité en session.
- **Jurisprudence CJUE** transferts, responsabilité — via `recherche-juridique`.
- **Recommandations CEPD** mesures supplémentaires — version à dater.
- **SecNumCloud / circulaires cloud de l'État** — version et champ à dater.
- **CRPA** et textes dites-le-nous-une-fois — à vérifier.

## 10. Livrables

- **Avis DPO** (qualification, conformité contractuelle, transferts) →
  `assets/avis-dpo-modele.md`. Intègre la **checklist contractuelle** du
  §5.2 : chaque élément coché conforme / absent / à négocier.
- Éléments obligatoires : qualification motivée de chaque acteur, analyse
  de transfert (existence, outil, mesures), écarts contractuels, niveau de
  risque, recommandation au responsable de traitement (garde-fou §5.2.a du
  `SKILL.md`).

## 11. Double échelle [risque / confiance]

- **Risque élevé par défaut** : transfert hors UE sans outil identifié,
  droit extraterritorial sur données sensibles ou d'action sociale, contrat
  art. 28 absent d'un marché en cours.
- **Risque critique** : données sensibles ou personnes vulnérables + chaîne
  non tracée hors UE → citation obligatoire, abstention si doute persistant.
- **Risque moyen** : qualification d'un prestataire classique, clause à
  compléter avant notification.
- **Confiance** : « à vérifier » sur toute version de CCT, adéquation ou
  doctrine cloud non confirmée en session ; « jurisprudentiel » sur Schrems II.

## 12. Checklist de branche

1. Chaque acteur qualifié d'après les **faits**, pas l'intitulé du contrat ?
2. Responsable de traitement nommé (commune / EPCI / CCAS / État) ?
3. STOP RÉGIME appliqué si finalité pénale possible (`SKILL.md` §5.2.b) ?
4. Checklist art. 28 passée intégralement, manquants listés ?
5. **Transfert** analysé (stockage ET accès) ; outil et mesures
   supplémentaires identifiés, versions datées ou « à vérifier » ?
6. Chaîne de sous-traitance tracée ou signalée comme non tracée ?
7. Commande publique : stade identifié, clauses au DCE ?
8. Conventions inter-entités (CCAS, EPCI) vérifiées ?
9. Sécurité de fond renvoyée à `securite-traitements.md`, sans duplication ?
10. Avis conclu par une **recommandation** au responsable de traitement,
    jamais par une autorisation (garde-fou §5.2.a) ?
