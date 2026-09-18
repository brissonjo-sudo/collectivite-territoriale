# Branche — Droits des personnes

---

## 1. Périmètre / Exclusions

**Couvre** : l'information des personnes (art. 13 et 14 RGPD — à confirmer
en version consolidée), les droits d'accès, de rectification, d'effacement,
de limitation, d'opposition et de portabilité, les directives post-mortem
(loi 78-17 — à vérifier en session), l'encadrement des décisions
individuelles automatisées (art. 22 — à confirmer) et l'instruction des
demandes d'exercice de droits reçues par la collectivité.

**Exclut** :
- la plainte d'une personne auprès de la CNIL et ses suites →
  `references/relations-cnil.md` ;
- la rédaction des clauses d'information dans les contrats de
  sous-traitance → `references/sous-traitance-transferts.md`.

---

## 2. Questions couvertes

- « Un administré demande la copie de son dossier : que lui remettre ? »
- « Peut-on refuser un effacement ? Une opposition ? »
- « Quelle mention d'information sur ce formulaire / téléservice ? »
- « Un avocat / un parent / un héritier demande pour un tiers : valide ? »
- « Quel délai pour répondre ? Peut-on le prolonger ? »
- « Faut-il exiger une pièce d'identité ? »
- « CADA ou RGPD : quel régime pour cette demande de documents ? »

---

## 3. Arbre de traitement

```
1. QUALIFIER LA DEMANDE — quel(s) droit(s) invoqué(s) ? Demande RGPD,
   demande CADA/CRPA, ou les deux (§5.8) ?
2. DATER LA RÉCEPTION — le délai d'un mois court dès réception par la
   collectivité, quel que soit le service destinataire.
3. IDENTIFIER — régime applicable (RGPD / Police-Justice), responsable
   de traitement concerné, traitements visés.
4. VÉRIFIER L'IDENTITÉ — de façon proportionnée (§5.6) ; tiers → §5.7.
5. INSTRUIRE — conditions et limites du droit invoqué en contexte
   public (§5.2 à §5.5).
6. DÉCIDER — faire droit, partiellement, ou refuser (motivé + voies de
   recours). Décision du responsable de traitement ; le DPO instruit
   et recommande.
7. RÉPONDRE — dans le délai, sans divulguer de données de tiers →
   assets/reponse-droits-modele.md.
8. TRACER — registre des demandes, RETEX si lacune d'information.
```

---

## 4. Variables à lever

- **Droit(s) invoqué(s)** — la personne ne cite pas toujours le bon :
  requalifier d'après ce qu'elle veut obtenir.
- **Régime** : RGPD ou Police-Justice (fichier PM, vidéoverbalisation) ?
  L'exercice des droits peut y être **indirect** (via la CNIL) — à vérifier
  au titre III de la loi 78-17, jamais de mémoire (STOP RÉGIME).
- **Responsable de traitement** : commune, CCAS, EPCI, État (état civil,
  élections) ? La réponse en dépend.
- **Date de réception** par la collectivité (tout canal, tout service).
- **Demandeur** : personne concernée, parent d'un mineur, mandataire,
  héritier ?
- **Traitement visé** : base légale (conditionne opposition et
  portabilité), statut d'archive publique (conditionne l'effacement).
- Demande **manifestement infondée ou excessive** (répétitive) ?

---

## 5. Règles métier

### 5.1 Information à deux niveaux (art. 13/14 — à confirmer)
Informer **au moment de la collecte** (art. 13) ou dans un délai raisonnable
si collecte indirecte (art. 14). Pratiquer l'information **à deux niveaux** :
mention courte sur le support de collecte (finalité, responsable, droits,
renvoi) + notice complète accessible (site, affichage, document remis).
Contenus obligatoires : vérifier la liste des articles en version
consolidée. Générateur → `assets/mention-information-modele.md`.

### 5.2 Chaque droit avec ses limites en contexte public
- **Accès** : confirmation du traitement + copie des données + informations
  associées. Ne pas confondre avec la communication de documents (§5.8).
- **Rectification** : données inexactes ou incomplètes. Attention aux actes
  authentiques (état civil) : procédures sectorielles propres — vérifier.
- **Effacement** : cède devant l'**obligation légale** et l'**archivage
  public**. Tout document de la collectivité est une archive publique :
  aucune élimination sans croisement avec le code du patrimoine et le visa
  du directeur des archives départementales — à vérifier (renvoi
  `references/socle-sources-verification.md` §4).
- **Limitation** : gel temporaire, notamment pendant la vérification d'une
  contestation d'exactitude.
- **Opposition** : suppose des « raisons tenant à la situation
  particulière » et **ne s'applique pas aux traitements obligatoires**
  (obligation légale). Pour les traitements en mission d'intérêt public,
  elle s'examine — elle ne s'accorde pas d'office.
- **Portabilité** : vise les bases **consentement** et **contrat**, avec
  traitement automatisé — **rare en collectivité**, où la base dominante est
  la mission d'intérêt public. Ne pas la promettre par défaut.
- **Directives post-mortem** et droits des héritiers : régime propre à la
  loi 78-17 — **à vérifier en session**, jamais de mémoire.
- **Décision individuelle automatisée** (art. 22 — à confirmer) : interdiction
  de principe avec exceptions ; garanties (intervention humaine) à vérifier
  avant tout téléservice à décision automatique.

### 5.3 Délais
Réponse dans **un mois** à compter de la réception par la collectivité,
**prolongeable de deux mois** en cas de complexité ou de nombre de demandes
— à confirmer en version consolidée. La prolongation s'annonce au demandeur
**dans le premier mois**, motivée. Le délai court même si la demande arrive
au mauvais service : organiser le circuit interne de remontée au DPO.

### 5.4 Gratuité
Réponse **gratuite**. Facturation ou refus possibles uniquement pour les
demandes **manifestement infondées ou excessives** (notamment répétitives) —
charge de la démonstration côté collectivité, à documenter.

### 5.5 Refus
Tout refus (total ou partiel) est **motivé** et mentionne les **voies de
recours** : réclamation auprès de la CNIL et recours juridictionnel. Le
refus est une décision du **responsable de traitement**, sur avis du DPO.

### 5.6 Vérification d'identité proportionnée
Pas de pièce d'identité **systématique** — doctrine CNIL, **à dater lors de
la citation**. Proportionner au doute raisonnable et à la sensibilité des
données : un usager connu répondant depuis son compte de téléservice n'a
pas à rejustifier son identité ; une demande portant sur un dossier social
justifie plus de précaution. Si une pièce est demandée : la strictement
nécessaire, non conservée au-delà du besoin.

### 5.7 Demande d'un tiers
- **Parent / représentant légal d'un mineur** : vérifier la qualité et
  l'autorité parentale ; attention aux situations familiales conflictuelles.
- **Avocat / mandataire** : exiger un mandat exprès de la personne.
- **Héritier** : pas de droit d'accès général aux données du défunt ;
  régime des directives post-mortem et exceptions loi 78-17 — à vérifier
  en session avant toute réponse.

### 5.8 RGPD ≠ CADA
Ne pas confondre le **droit d'accès RGPD** (la personne accède à **ses**
données) et l'**accès aux documents administratifs** (CADA/CRPA : accès à
des **documents**, y compris par des tiers, avec occultations). Les deux
régimes **coexistent** : qualifier la demande d'après son objet, orienter
vers le bon régime — ou traiter les deux si la demande les mêle. En régime
CRPA, saisir le circuit PRADA/CADA de la collectivité. Dans tous les cas,
**occulter les données de tiers** dans les documents communiqués.

### 5.9 Droits en régime Police-Justice
Pour les traitements relevant du titre III de la loi 78-17 (fichiers à
finalité pénale), les droits peuvent s'exercer de façon **indirecte** (via
la CNIL) et connaître des restrictions propres — **à vérifier en session**,
jamais de mémoire. Afficher le STOP RÉGIME dès qu'un fichier PM est visé.

---

## 6. Procédures et délais

| Étape | Acteur | Échéance | Point de contrôle |
|---|---|---|---|
| Réception + horodatage | Tout service → DPO | Immédiat | Circuit interne formalisé |
| Vérification d'identité / mandat | DPO | Sans retarder l'instruction | Proportionnée (§5.6) |
| Instruction | DPO + service métier | Dans le mois | Limites du droit en contexte public |
| Prolongation éventuelle | Responsable de traitement | Annoncée dans le 1er mois | Motivée — à confirmer |
| Réponse | Responsable de traitement | 1 mois (+2 si complexité — à confirmer) | Pas de données de tiers ; refus motivé + recours |
| Traçage | DPO | Au fil de l'eau | Registre des demandes |

---

## 7. Déclencheurs de vérification (socle-sources)

Vérifier la source officielle avant de conclure sur :
- le contenu obligatoire des mentions d'information (art. 13/14) ;
- le délai exact et les conditions de prolongation ;
- les directives post-mortem et droits des héritiers (loi 78-17 — jamais
  de mémoire) ;
- l'exercice des droits en régime Police-Justice (titre III) ;
- la procédure d'élimination d'archives publiques (code du patrimoine) ;
- la doctrine CNIL sur la vérification d'identité (version datée) ;
- la frontière CADA/CRPA au cas d'espèce.

---

## 8. Pièges & confusions fréquentes

- **Exiger systématiquement une pièce d'identité** : contraire à la
  proportionnalité (doctrine CNIL — à dater).
- **Laisser courir le délai** parce que « c'est le DPO qui gère » : le délai
  engage la collectivité dès réception, par n'importe quel service.
- **Effacer des archives publiques sans visa** des archives
  départementales : l'effacement RGPD ne prime pas le code du patrimoine.
- **Confondre CADA et RGPD** — ou répondre sous un seul régime à une demande
  qui relève des deux.
- **Divulguer des données de tiers** dans les documents communiqués :
  occulter avant remise.
- Promettre la **portabilité** pour un traitement en mission d'intérêt
  public, ou accorder l'**opposition** contre un traitement obligatoire.
- Refuser sans **motivation ni voies de recours**.
- Répondre sur un fichier Police-Justice comme s'il relevait du RGPD.
- Oublier que le CCAS répond pour ses propres traitements.

---

## 9. Données / références à vérifier

- Art. 13, 14, 15 à 22 RGPD : citables avec la réserve « à confirmer en
  version consolidée ».
- Loi 78-17 (post-mortem, titre III, modalités nationales) : **jamais de
  mémoire** — vérification en session obligatoire.
- Décret 2019-536 (modalités d'exercice des droits) : à confirmer.
- Code du patrimoine (élimination, visa) et CRPA (CADA) : à vérifier au
  cas d'espèce.
- Doctrine CNIL (vérification d'identité, droit d'accès, modèles de
  mentions) et lignes directrices CEPD (droit d'accès, transparence) :
  **dater la version citée**.

---

## 10. Livrables

- **Réponse à une demande d'exercice de droits** →
  `assets/reponse-droits-modele.md`. Éléments obligatoires : rappel de la
  demande et de sa date de réception, droit(s) instruit(s), réponse
  motivée, occultation des tiers, voies de recours (CNIL, juge) en cas de
  refus, signature du responsable de traitement.
- **Mention d'information** (deux niveaux) →
  `assets/mention-information-modele.md`.

---

## 11. Double échelle [risque / confiance]

- Mention d'information standard : risque faible — réponse directe, contenu
  obligatoire vérifié avant usage en acte.
- Instruction d'un droit courant (accès, rectification) : risque moyen —
  vérifier délais et limites avant réponse.
- Refus opposé à une personne, effacement d'archives, demande d'héritier :
  risque **élevé** — citation de source obligatoire, réserve « à
  confirmer » sinon.
- Fichier Police-Justice, dossier social, mineur en contexte familial
  conflictuel : risque **critique** — abstention si doute persistant,
  vérification en session de la loi 78-17.

---

## 12. Checklist de branche

1. Demande qualifiée (droit(s) réellement visé(s), RGPD / CADA / les deux) ?
2. Régime identifié — STOP RÉGIME affiché si fichier PM ou finalité pénale ?
3. Responsable de traitement correctement désigné (commune / CCAS / EPCI /
   État) ?
4. Date de réception tracée, délai calculé, prolongation motivée si besoin ?
5. Identité / mandat vérifiés de façon **proportionnée** ?
6. Limites du droit en contexte public appliquées (opposition, portabilité,
   effacement vs archives) ?
7. Aucune donnée de tiers divulguée dans la réponse ?
8. Refus motivé + voies de recours mentionnées ?
9. Décision formellement portée par le responsable de traitement
   (garde-fou §5.2.a) ?
10. Références loi 78-17 vérifiées en session (jamais de mémoire) ;
    doctrine CNIL datée ?
11. Livrable produit via le bon générateur (ou brouillon `[INCOMPLET]`) ?
12. Cas significatif → entrée `JOURNAL.md` proposée ?
