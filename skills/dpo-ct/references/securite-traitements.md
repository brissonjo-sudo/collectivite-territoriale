# Branche — Sécurité des traitements

## 1. Périmètre / Exclusions

**Couvre** : les exigences de conformité en matière de sécurité des
traitements (art. 32 RGPD — à confirmer en version consolidée) : sécurité
proportionnée au risque pour les personnes, mesures organisationnelles et
techniques attendues côté conformité, habilitations, traçabilité, sécurité
dès la conception et par défaut, prévention des violations.

**Exclut** : la **mise en œuvre technique** (architecture, PSSI, choix
d'outils, paramétrage) → futur skill **DSI** — cette branche fixe les
**exigences** de conformité, pas les solutions techniques ; la gestion d'une
violation avérée → `violations.md` ; les clauses de sécurité contractuelles
et la chaîne de sous-traitance → `sous-traitance-transferts.md` ; le fond
des référentiels ANSSI → doctrine d'appui seulement
(`socle-sources-verification.md` §1).

## 2. Questions couvertes

- Quelles mesures exiger pour ce traitement, ce logiciel, ce téléservice ?
- Le niveau de sécurité actuel est-il proportionné au risque ?
- Comment organiser habilitations et revues d'accès ? Départ d'un agent ?
- Quelle traçabilité pour les accès aux données sensibles ?
- Qui fait quoi entre DPO, RSSI et DSI ?
- Que regarde la CNIL en contrôle ? Comment intégrer la sécurité dès la
  conception d'un projet ?

## 3. Arbre de traitement

1. **Question** : quel traitement, quelles données, quel risque pour les
   **personnes** ?
2. **Variables à lever** (§4) : sensibilité, échelle, vulnérabilité,
   existant sécurité, acteurs (DSI, RSSI, prestataires).
3. **Décision** : évaluer le risque pour les personnes → confronter aux
   mesures socles (doctrine CNIL datée) → identifier les écarts → formuler
   les **exigences** (pas les solutions) → répartir : le DPO exige et
   contrôle, la DSI met en œuvre.
4. **Vérification** : matrice §2.2 du `SKILL.md` — art. 32, référentiels
   CNIL/ANSSI, obligations sectorielles : socle-sources.
5. **Livrable** : avis DPO (§10) ; projet nouveau à risque → `aipd.md`.

## 4. Variables à lever

- **Régime applicable** : RGPD ou Police-Justice (STOP RÉGIME, `SKILL.md`
  §5.2.b) — les exigences de journalisation diffèrent notamment.
- **Responsable de traitement** et opérateur technique (DSI interne, EPCI
  mutualisé, prestataire → `sous-traitance-transferts.md`).
- **Données** : catégories, données sensibles, NIR, données pénales ?
- **Personnes** : mineurs, bénéficiaires de l'action sociale, agents ?
- **Échelle et supports** : SI, postes nomades, **papier**, messagerie.
- **Existant** : mots de passe, comptes, sauvegardes, journalisation,
  sensibilisation — état réel, pas déclaré.
- **Obligations sectorielles** : téléservice (RGS — à vérifier), santé,
  social ?

## 5. Règles métier

### 5.1 Proportionnalité au risque pour les personnes

- Évalue la sécurité au regard du **risque pour les droits et libertés des
  personnes concernées**, pas seulement du risque pour le SI ou la
  collectivité. Un fichier modeste en volume mais sensible (action sociale,
  santé scolaire) exige un niveau élevé.
- Croise vraisemblance et gravité des impacts (accès illégitime,
  modification, disparition des données) : c'est la grille qui fonde
  l'exigence, et celle que la CNIL applique.
- L'art. 32 impose une **obligation de moyens renforcée et documentée** :
  état de l'art, coûts, nature du traitement — l'arbitrage se justifie par
  écrit (accountability).

### 5.2 Référentiels d'appui

- **Guide sécurité CNIL** : référence pivot des attentes de conformité —
  **dater la version** citée, vérifier s'il en existe une plus récente.
- **Référentiels ANSSI** (hygiène informatique, guides sectoriels) : appui
  technique, jamais suffisant seul pour fonder une affirmation normative.
- **Obligations sectorielles** : téléservices soumis au **RGS** (champ et
  version à vérifier) ; exigences propres aux téléservices →
  `secteur-collectivites.md`.

### 5.3 Mesures socles attendues en contrôle

Présente ces mesures comme la **doctrine CNIL datée** (guide sécurité,
version à préciser), pas comme une liste réglementaire figée :

- **Authentification** : comptes individuels, mots de passe robustes
  (valeurs chiffrées : recommandation CNIL en vigueur, jamais de mémoire),
  authentification renforcée pour les accès sensibles ou distants.
- **Habilitations par profil** : droits alignés sur les missions, pas sur le
  statut hiérarchique.
- **Journalisation** des accès et des opérations, proportionnée.
- **Chiffrement des postes nomades** et supports mobiles.
- **Sauvegardes** testées, dont une déconnectée.
- **Sensibilisation** régulière des agents et élus, documentée.
- Ajoute le **papier** : armoires fermant à clé, circuits de parapheurs,
  destruction sécurisée — le RGPD couvre les fichiers papier structurés.

### 5.4 Habilitations et traçabilité

- Applique le **besoin d'en connaître** : nul n'accède à des données parce
  que sa fonction est élevée, mais parce que sa mission l'exige — y compris
  la hiérarchie et les élus.
- Impose une **revue périodique** des habilitations ; documente-la.
- **Départs et mobilités d'agents** : désactivation des comptes sans
  délai ; intègre ce point au circuit RH (fond statutaire → `drh-fpt`).
- **Traçabilité des accès aux données sensibles** (social, santé, pénal) :
  journalisation exploitable et contrôlée, pas seulement activée. Durées de
  conservation des journaux : recommandation CNIL en vigueur, à dater.

### 5.5 Rôles : le DPO exige, la DSI met en œuvre

- Le DPO **conseille et contrôle** le niveau de sécurité ; le RSSI et la
  DSI **choisissent et déploient** les solutions. Coopération obligatoire,
  rôles distincts : jamais d'avis DPO prescrivant un outil.
- Formalise le dialogue : le DPO transmet les exigences et le niveau de
  risque pour les personnes ; la DSI répond par des mesures ; le DPO évalue
  la couverture du risque, pas la qualité technique intrinsèque.
- Mise en œuvre technique, architecture, PSSI → futur skill **DSI**
  (`SKILL.md` §5.4).

### 5.6 Sécurité dès la conception et par défaut

- Intègre les exigences de protection **dès la conception** du projet et
  **par défaut** (art. 25 RGPD — à confirmer en version consolidée) :
  minimisation native, paramétrages les plus protecteurs par défaut,
  sécurité pensée avant le choix de l'outil.
- Fais intervenir le DPO **en amont** des projets (cahier des charges, DCE
  → `sous-traitance-transferts.md` §5.3), pas à la mise en service.
- Projet à risque élevé probable → vérifier l'obligation d'AIPD → `aipd.md`.

## 6. Procédures et délais

- **Projet nouveau** : exigences de sécurité au cahier des charges → avis
  DPO avant décision → contrôle avant mise en service.
- **Cycle de vie** : revue périodique des habilitations, tests de
  restauration des sauvegardes, campagnes de sensibilisation — planifier et
  tracer ces échéances (la preuve compte autant que la mesure).
- **Incident de sécurité** : atteinte possible à des données personnelles
  → basculer immédiatement vers `violations.md` (délais propres, dont les
  72 h de notification — vérifiés dans cette branche).
- Aucune valeur chiffrée (mot de passe, journaux) citée de mémoire.

## 7. Déclencheurs de vérification

Socle-sources obligatoire (matrice §2.2 du `SKILL.md`) pour : contenu et
portée des art. 25 et 32 RGPD ; version en vigueur du guide sécurité CNIL et
de toute recommandation chiffrée (mots de passe, journalisation) ;
applicabilité du RGS à un téléservice ; exigences propres au régime
Police-Justice ; obligation d'AIPD (→ `aipd.md`) ; toute sanction CNIL
invoquée comme précédent (→ `relations-cnil.md`).

## 8. Pièges & confusions fréquentes

- Confondre **conformité RGPD et sécurité informatique** : la sécurité est
  nécessaire mais pas suffisante — un SI sûr peut porter un traitement illicite.
- **DPO transformé en RSSI de fait** : rédiger la PSSI ou choisir les
  outils place le DPO en conflit d'intérêts (art. 38.6 RGPD — à confirmer).
- **Mot de passe partagé « pour aller vite »** en mairie (compte commun
  d'accueil, session ouverte) : rend toute traçabilité impossible.
- Accès de la hiérarchie « **parce que chef** » sans besoin d'en connaître :
  le grade n'est pas une habilitation.
- **Oublier le papier** : armoires ouvertes, parapheurs en circulation,
  dossiers sociaux en libre accès.
- Présenter les mesures socles CNIL comme des **obligations réglementaires
  figées** : doctrine datée, à distinguer de l'exigence de proportionnalité.
- Croire la sécurité réglée parce qu'un prestataire est « certifié » : la
  conformité du responsable reste entière (→ `sous-traitance-transferts.md`).

## 9. Données / références à vérifier

- Art. 25 et 32 RGPD — « à confirmer en version consolidée ».
- Dispositions correspondantes de la **loi 78-17** (dont Police-Justice,
  journalisation) — jamais de mémoire, vérification en session obligatoire.
- **Guide sécurité CNIL** — version à dater à chaque citation.
- **Recommandations CNIL chiffrées** (mots de passe, journaux) — valeur et
  version à vérifier.
- **RGS** et textes d'application aux téléservices — champ et vigueur à vérifier.
- **Référentiels ANSSI** mobilisés — version à dater, valeur non normative.
- Toute **sanction CNIL** citée en illustration — à rechercher en session.

## 10. Livrables

- **Avis DPO** (exigences de sécurité, écarts, recommandations) →
  `assets/avis-dpo-modele.md`.
- Éléments obligatoires : rappel du risque pour les **personnes**, écarts
  constatés vs mesures socles (doctrine datée), exigences hiérarchisées,
  répartition DPO / DSI, niveau de risque, recommandation au responsable de
  traitement — jamais de prescription d'outil (garde-fou §5.2.a du
  `SKILL.md`).
- Besoin d'AIPD ou de fiche de registre → `aipd.md` / `gouvernance-registre.md`.

## 11. Double échelle [risque / confiance]

- **Risque critique** : données sensibles ou personnes vulnérables sans
  mesure socle (accès non tracés aux dossiers sociaux, poste nomade non
  chiffré) → citation obligatoire, abstention si doute.
- **Risque élevé** : téléservice sans authentification robuste, comptes
  partagés sur un SI métier, absence de sauvegarde testée.
- **Risque moyen** : écart ponctuel sur un traitement peu sensible, revue
  d'habilitations en retard.
- **Confiance** : « stable » sur la proportionnalité ; « à vérifier » sur
  toute valeur chiffrée ou version de référentiel ; « jurisprudentiel » sur
  l'appréciation du « niveau adapté » en sanction.

## 12. Checklist de branche

1. Risque évalué pour les **personnes**, pas seulement pour le SI ?
2. STOP RÉGIME appliqué si finalité pénale possible (`SKILL.md` §5.2.b) ?
3. Responsable de traitement et opérateur technique identifiés ?
4. Mesures socles présentées comme **doctrine datée**, version du guide CNIL
   précisée ou marquée « à vérifier » ?
5. Aucune valeur chiffrée citée de mémoire ?
6. Habilitations : besoin d'en connaître, revue, départs traités ?
7. Le **papier** a-t-il été couvert ?
8. Frontière DPO / DSI respectée : exigences formulées, aucune solution
   technique prescrite (§5.4 du `SKILL.md`) ?
9. Violation possible → `violations.md` ? AIPD requise → `aipd.md` ?
10. Avis conclu par une **recommandation** au responsable de traitement
    (garde-fou §5.2.a) ?
