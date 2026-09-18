# Générateur interactif — Note d'impact financier (v1.0.0)

> Couche 4 (`references/templates/`), piloté par `references/ecrits-financiers.md`
> et par `SKILL.md` §6. Mécanique de dialogue alignée sur les générateurs du
> skill frère `Dpm-fpt` (questions posées **une à une**, aucune donnée
> inventée, règle `[INCOMPLET]` stricte, checklist finale). Le contenu
> métier est propre aux finances locales.
>
> **Nature de l'écrit** : la note d'impact financier est une **note d'aide à
> la décision** — **pas un acte administratif**. Elle ne produit aucun effet
> de droit par elle-même, ne fait pas grief, et n'est donc **ni motivée au
> sens du CRPA, ni soumise à transmission au contrôle de légalité**. Elle
> chiffre l'impact d'un projet pour éclairer un décideur, sans décider à sa
> place. Branches de rattachement : `../prospective-analyse.md` (impact sur
> l'épargne et les ratios), `../nomenclature-m57.md` (rattachement comptable
> des coûts et recettes évoqués).
>
> **Ce fichier ne tranche jamais seul** la faisabilité budgétaire définitive
> d'un projet : il **chiffre** et **qualifie le degré de certitude** de
> chaque donnée, la décision appartenant au destinataire.

---

## 0. Quand utiliser ce générateur

La note d'impact financier sert à **chiffrer l'impact d'un projet** avant
une décision : investissement envisagé, création d'un service, recrutement
significatif, projet de mutualisation, acquisition, aide financière reçue ou
versée d'ampleur significative.

**Avant d'ouvrir ce générateur**, vérifier que l'écrit demandé est bien une
note d'impact et non un autre document :

1. **S'agit-il de formaliser une décision de l'assemblée (vote de crédits,
   affectation) ?** Oui → `deliberation-budgetaire.md`, pas ce générateur.
2. **S'agit-il du cadrage global de l'exercice, pas d'un projet précis ?**
   Oui → `rapport-orientation-budgetaire.md`, pas ce générateur.
3. **Le projet implique-t-il un maniement de deniers publics hors circuit du
   comptable (`SKILL.md` §5.2) ?** Oui → afficher le **STOP** avant tout
   autre contenu et orienter vers la voie régulière, avant de chiffrer quoi
   que ce soit.

Si aucun de ces cas ne redirige ailleurs : la **note d'impact financier**
est le bon écrit. Poursuivre au §1.

---

## 1. Séquence interactive obligatoire

**Principe directeur** (`SKILL.md` §6) : questions posées **une à une**,
jamais en bloc. Confirmer chaque réponse avant de passer au champ suivant.
Ne jamais pré-remplir un champ non fourni : appliquer la règle `[INCOMPLET]`
(§4).

### Étape 1 — Projet et porteur
- Q1 : « Quel est le projet précis à chiffrer, et quel service ou quelle
  direction le porte ? »
- Pourquoi : cadre l'ensemble de la note ; sans objet précis, aucun chiffrage
  n'a de sens.

### Étape 2 — Décideur destinataire
- Q2 : « À qui cette note est-elle destinée (maire, exécutif, assemblée en
  amont d'une délibération, direction générale) ? »
- Pourquoi : conditionne le niveau de synthèse attendu et l'éventuel
  enchaînement vers `deliberation-budgetaire.md`.

### Étape 3 — Horizon
- Q3 : « Sur quel horizon temporel l'impact doit-il être apprécié
  (ponctuel, pluriannuel — préciser le nombre d'exercices) ? »
- Pourquoi : un coût de fonctionnement induit se lit sur plusieurs exercices,
  jamais sur le seul exercice de mise en œuvre (voir étape 5).

### Étape 4 — Coût d'investissement
- Q4 : « Quel est le coût d'investissement envisagé (montant, nature des
  dépenses, phasage si pluriannuel) ? Ce montant est-il un devis ferme, une
  estimation de programmiste, ou un ordre de grandeur ? »
- Pourquoi : le degré de certitude du montant doit être qualifié dès sa
  collecte (voir §2 — colonne certain / à vérifier / hypothétique).

### Étape 5 — Coûts de fonctionnement induits
- Q5 : « Une fois le projet réalisé, quels coûts de fonctionnement
  récurrents génère-t-il (personnel, maintenance, énergie, contrats,
  assurances, renouvellement de matériel) ? »
- **Point d'insistance obligatoire** : c'est le point **le plus souvent
  oublié**. Si la réponse est « aucun » ou reste vague, **relancer
  explicitement** : « Un projet d'investissement génère presque toujours un
  coût de fonctionnement récurrent — êtes-vous certain qu'aucun n'est
  attendu, ou ce point reste-t-il à chiffrer ? » Si le doute persiste après
  relance, marquer `[INCOMPLET — préciser : coûts de fonctionnement induits]`
  plutôt que de retenir un impact nul.

### Étape 6 — Recettes attendues
- Q6 : « Le projet génère-t-il des recettes attendues (tarification,
  subvention reçue, économie de charge documentée) ? Avec quel degré de
  certitude ? »
- Pourquoi : une recette hypothétique ne compense jamais un coût certain
  dans la présentation — les deux sont distingués, jamais nets l'un de
  l'autre par défaut.

### Étape 7 — Plan de financement
- Q7 : « Comment le coût d'investissement est-il financé (autofinancement,
  emprunt, subvention reçue, cession) ? Chaque source est-elle acquise,
  sollicitée, ou seulement envisagée ? »
- Pourquoi : distinction stricte entre financement acquis et financement
  sollicité — renvoi `../dette-tresorerie.md` si emprunt, `../subventions.md`
  si subvention reçue.

### Étape 8 — Impact sur l'épargne et les ratios
- Q8 : « Disposez-vous des données permettant d'apprécier l'impact sur
  l'épargne brute/nette et sur la capacité de désendettement (ou faut-il les
  demander à la prospective) ? »
- Pourquoi : renvoi `../prospective-analyse.md` §5.1 et §5.2 pour la méthode
  de calcul ; cette note ne recalcule pas la prospective, elle en mobilise le
  résultat si disponible, ou signale son absence.

### Étape 9 — Alternatives comparées
- Q9 : « Quelles alternatives ont été envisagées (dont l'option de ne pas
  réaliser le projet), et quel est leur ordre de grandeur comparé ? »
- Pourquoi : une note à option unique n'éclaire pas la décision ; au moins
  une alternative, y compris le statu quo, doit être présentée pour
  comparaison.

### Étape 10 — Points de vigilance
- Q10 : « Quels risques ou incertitudes identifiez-vous (calendrier,
  dépassement de coût, dépendance à une subvention non encore notifiée,
  évolution réglementaire) ? »
- Pourquoi : nourrit la colonne « Soutenable ? » du tableau d'options (§2) et
  le couple [risque / confiance].

**À l'issue de l'étape 10** : si toutes les réponses nécessaires ont été
recueillies, passer à l'assemblage (§2). Sinon, appliquer la règle
`[INCOMPLET]` (§4).

---

## 2. Discipline de qualification des chiffres — obligatoire

**Chaque valeur chiffrée de la note porte une qualification explicite**,
placée immédiatement après le montant, parmi les trois seules catégories
suivantes :

- **certain** : donnée constatée ou contractualisée (facture, marché signé,
  taux réglementaire vérifié à la source).
- **à vérifier** : donnée plausible mais non confirmée dans la session
  (devis non définitif, estimation à recouper, taux non vérifié).
- **hypothétique** : donnée de projection ou de simulation, sans engagement
  ferme (hypothèse de fréquentation, hypothèse de taux futur, subvention
  seulement sollicitée).

**Aucun montant n'apparaît sans cette qualification.** Une valeur non
qualifiée dans la réponse de l'utilisateur est marquée par défaut
`hypothétique` et signalée pour confirmation.

---

## 3. Gabarit d'assemblage

> Champs à compléter entre `[ ]`. Chaque valeur chiffrée est suivie de sa
> qualification entre parenthèses : `(certain)`, `(à vérifier)` ou
> `(hypothétique)`.

```
[COLLECTIVITÉ — en-tête / direction des finances]

NOTE D'IMPACT FINANCIER
Projet : [intitulé — étape 1]
Porteur : [service / direction — étape 1]
Destinataire : [décideur — étape 2]
Date : [date de rédaction]
Horizon d'appréciation : [ponctuel / pluriannuel, nombre d'exercices —
étape 3]

I. COÛT D'INVESTISSEMENT
[Montant [ ] ([qualification]) — nature des dépenses, phasage si
pluriannuel — étape 4]

II. COÛTS DE FONCTIONNEMENT INDUITS
[Détail par nature (personnel, maintenance, énergie, contrats, assurances,
renouvellement) — étape 5, chaque montant qualifié. Si aucun coût de
fonctionnement n'a été identifié après relance : le mentionner explicitement
avec la mise en garde reprise du §1 étape 5, jamais un silence sur ce
point.]

III. RECETTES ATTENDUES
[Détail par source (tarification, subvention, économie documentée) — étape
6, chaque montant qualifié, distinct des coûts, jamais présenté en net par
défaut]

IV. PLAN DE FINANCEMENT
[Sources de financement du coût d'investissement — étape 7, chacune
qualifiée acquise / sollicitée / envisagée. Renvoi ../dette-tresorerie.md si
emprunt, ../subventions.md si subvention reçue.]

V. IMPACT SUR L'ÉPARGNE ET LES RATIOS
[Impact sur l'épargne brute/nette et sur la capacité de désendettement —
étape 8, méthode renvoyée à ../prospective-analyse.md §5.1-§5.2. Si les
données ne sont pas disponibles : « [INCOMPLET — préciser : données de
prospective nécessaires au calcul] », jamais une valeur substituée.]

VI. TABLEAU DES OPTIONS COMPARÉES

| Option | Coût d'investissement | Coût de fonctionnement annuel | Recettes attendues | Impact épargne/dette | Soutenable ? |
|---|---|---|---|---|---|
| [Option retenue] | [montant] ([qualif.]) | [montant] ([qualif.]) | [montant] ([qualif.]) | [impact] ([qualif.]) | [Oui / Non / Sous condition — préciser laquelle] |
| [Alternative 1, dont statu quo] | [montant] ([qualif.]) | [montant] ([qualif.]) | [montant] ([qualif.]) | [impact] ([qualif.]) | [Oui / Non / Sous condition] |
| [Alternative 2 si pertinente] | [ ] | [ ] | [ ] | [ ] | [ ] |

[La colonne « Soutenable ? » ne se remplit jamais par défaut à « Oui » :
elle reflète l'appréciation croisée du coût de fonctionnement induit et de
l'impact sur l'épargne, avec la réserve « sous condition » chaque fois
qu'une donnée reste `à vérifier` ou `hypothétique`.]

VII. ALTERNATIVES COMPARÉES — COMMENTAIRE
[Commentaire qualitatif sur les alternatives du tableau — étape 9]

VIII. POINTS DE VIGILANCE
[Risques et incertitudes identifiés — étape 10 : calendrier, dépassement de
coût, dépendance à une recette hypothétique, évolution réglementaire]

Fait à [lieu], le [date].
[Signature du rédacteur — direction des finances]
```

---

## 4. Mentions obligatoires et contrôles de cohérence

- [ ] Chaque valeur chiffrée qualifiée `certain` / `à vérifier` /
  `hypothétique` — aucune exception.
- [ ] **Coûts de fonctionnement induits** explicitement traités, même en cas
  de réponse « aucun » — jamais une section absente ou muette.
- [ ] Recettes attendues présentées séparément des coûts, jamais nettées par
  défaut.
- [ ] Plan de financement : chaque source qualifiée acquise / sollicitée /
  envisagée.
- [ ] Impact sur l'épargne et les ratios renvoyé à la méthode de
  `../prospective-analyse.md`, jamais recalculé de façon autonome sans les
  données sources.
- [ ] Tableau d'options comportant au moins une alternative, dont le statu
  quo si pertinent, avec une colonne « Soutenable ? » renseignée pour
  chaque ligne.
- [ ] Cohérence entre le total du tableau d'options et le détail des
  sections I à IV — tout écart signalé, jamais corrigé silencieusement.

---

## 5. Règle `[INCOMPLET]` — application stricte

**Interdiction absolue d'halluciner une donnée manquante** : montant de
coût ou de recette, qualification d'une valeur, impact sur l'épargne, part
de financement acquise.

1. Produire le brouillon avec les champs disponibles ; une section
   incomplète ne bloque pas la rédaction des autres.
2. Marquer chaque champ manquant `[INCOMPLET — préciser : <nom du champ>]`.
3. En fin de document, si au moins un champ est marqué `[INCOMPLET]`,
   ajouter :

```
---
## CHAMPS MANQUANTS — NOTE NON FINALISABLE EN L'ÉTAT

Les informations suivantes sont requises avant transmission au décideur :
- [champ manquant 1 — étape correspondante]
- [champ manquant 2 — étape correspondante]
- [...]

Cette note ne doit être ni transmise, ni présentée comme définitive tant
que ces champs ne sont pas renseignés.
```

4. **Demander explicitement** ces données à l'utilisateur, en reprenant la
   formulation de la question d'étape correspondante (§1).
5. Ne jamais marquer le document comme « prêt à transmettre » tant qu'une
   mention `[INCOMPLET]` subsiste.
6. **Cas particulier — coûts de fonctionnement induits (étape 5)** : ne
   jamais retenir un impact nul par défaut faute de réponse ; marquer
   `[INCOMPLET — préciser : coûts de fonctionnement induits, à chiffrer
   avant décision]`.

---

## 6. Double échelle [risque / confiance]

| Point | Risque | Confiance |
|---|---|---|
| Coût d'investissement | Moyen à élevé | Selon qualification (devis ferme vs estimation) |
| Coûts de fonctionnement induits omis | Élevé | Point d'insistance obligatoire (§1 étape 5) |
| Recettes hypothétiques présentées comme acquises | Élevé | À corriger systématiquement — qualification stricte |
| Impact sur l'épargne et la dette | Élevé | Renvoi impératif `../prospective-analyse.md` |
| Financement par emprunt ou subvention non encore acquis | Élevé | Qualifier acquis / sollicité / envisagé |
| Absence d'alternative présentée | Moyen | Au moins une alternative exigée |
| Donnée manquante | Élevé | N/A — `[INCOMPLET]` obligatoire |

---

## 7. Checklist avant remise

1. Toutes les étapes du §1 parcourues une à une, avec confirmation à chaque
   étape.
2. **Coûts de fonctionnement induits** traités explicitement, avec la
   relance obligatoire en cas de réponse absente ou vague (étape 5).
3. Chaque valeur chiffrée du document porte sa qualification `certain` /
   `à vérifier` / `hypothétique` — vérification exhaustive, pas seulement
   sur les montants principaux.
4. Recettes distinguées des coûts, jamais présentées en net par défaut.
5. Plan de financement qualifié source par source (acquis / sollicité /
   envisagé).
6. Impact sur l'épargne et les ratios renvoyé à `../prospective-analyse.md`,
   jamais recalculé sans les données sources disponibles.
7. Tableau d'options comparant au moins deux options (dont le statu quo si
   pertinent), colonne « Soutenable ? » renseignée pour chacune, sans
   défaut optimiste.
8. Aucune donnée manquante comblée par supposition — règle `[INCOMPLET]`
   (§5) appliquée et champs listés explicitement si nécessaire.
9. Aucune donnée nominative, aucun nom d'organisme ou de collectivité réel
   dans le document produit.
10. Mention finale claire : note **prête à transmettre** ou marquée
    **`[INCOMPLET]`** avec demande explicite des champs manquants — jamais
    d'état intermédiaire ambigu.
