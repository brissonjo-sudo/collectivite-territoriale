# Objet métier — Clôture de l'exercice (v1.0.0)

> **Situation type** : L'exercice budgétaire touche à sa fin ; il faut
> rattacher les charges et produits, constater les restes à réaliser, ajuster
> provisions et opérations d'ordre, arrêter les comptes puis faire adopter le
> compte administratif / compte financier unique et affecter le résultat.
> **[Risque / Confiance]** : Risque **moyen**, **élevé** si un déficit ou un
> déséquilibre apparaît. Confiance **stable** sur l'enchaînement des étapes ;
> **à vérifier** systématiquement sur le calendrier, les seuils de déficit et
> les modalités précises de rattachement.

---

## 1. Acteurs et autorités compétentes

| Acteur | Rôle | Compétence |
|---|---|---|
| **Exécutif (ordonnateur)** | Arrête les comptes | Prépare et arrête le compte administratif ; organise le rattachement des charges et produits et la constatation des restes à réaliser |
| **Comptable public assignataire** | Produit le compte de gestion / CFU | Établit le compte de gestion (ou compte financier unique selon le calendrier de généralisation) ; sa concordance avec le compte administratif est une condition de validité |
| **Assemblée délibérante** | Vote | Arrête le compte administratif (ou le CFU selon le régime applicable), délibère sur l'affectation du résultat |
| **Représentant de l'État** | Contrôle | Saisit la chambre régionale des comptes en cas de compte administratif en déficit au-delà du seuil légal |

**Point de vigilance sur le vote** : l'exécutif ne prend pas part au vote du
compte administratif le concernant — vérifier les règles de quorum et de
présidence de séance applicables (`budget-cycle.md` §5.6).

---

## 2. Textes applicables (pointeurs)

> Le fond n'est pas reproduit ici.

- **`../references/budget-cycle.md`** §5.6 (compte administratif et compte
  financier unique), §5.7 (affectation du résultat), §5.10 (journée
  complémentaire).
- **`../references/nomenclature-m57.md`** §5.7 (rattachement des charges et
  produits à l'exercice), §5.8 (restes à réaliser), §5.6 (provisions et
  dépréciations), §5.9 (opérations d'ordre), §5.10 (état de l'actif et
  compte financier unique).
- **`../references/controle-budgetaire.md`** §4.1 (les quatre cas de
  saisine), §4.3 (le compte administratif en déficit) — dès qu'un risque de
  déficit apparaît.
- **`../references/execution-depense.md`** et **`../references/execution-recette.md`** — mandatements et titres de fin d'exercice, rattachements individuels.

**Réserve systématique** : dates limites du calendrier de clôture, durée de
la journée complémentaire, seuil de déficit déclenchant la saisine de la
chambre régionale des comptes, quote-part obligatoire d'affectation au
financement de la section d'investissement — aucune de ces valeurs ne se cite
de mémoire.

---

## 3. Procédures

### 3.1 Calendrier de fin d'exercice

1. Identifier les dates limites applicables : fin de la journée
   complémentaire, date limite de rattachement, date limite d'adoption du
   compte administratif / CFU — **toutes à vérifier**, elles varient selon
   le type de budget et le calendrier en vigueur.
2. Distinguer la temporalité de l'ordonnateur (arrêté des comptes) de celle
   du comptable (production du compte de gestion / CFU) et vérifier leur
   articulation.

### 3.2 Journée complémentaire

1. Vérifier si la collectivité relève d'un régime comportant une **journée
   complémentaire** en section de fonctionnement (période complémentaire
   permettant de rattacher certaines opérations à l'exercice clos).
2. Ne pas présumer son existence ni sa durée sans vérification — le régime
   varie selon la nature du budget.

### 3.3 Rattachement des charges et produits

1. Identifier les charges et produits **se rapportant à l'exercice clos**
   mais dont la pièce justificative (facture, titre) parvient après la
   clôture.
2. Les rattacher à l'exercice concerné par les écritures prévues à cet effet
   (`nomenclature-m57.md` §5.7), plutôt que de les reporter sur l'exercice
   suivant.
3. Documenter la méthode de recensement utilisée (relance des services,
   analyse des engagements non soldés).

### 3.4 Restes à réaliser

1. **Constatation** : recenser, en section d'investissement, les dépenses
   engagées non mandatées et les recettes certaines n'ayant pas donné lieu à
   l'émission d'un titre.
2. **Justification** : chaque reste à réaliser doit être adossé à une pièce
   probante (marché notifié, bon de commande, décision attributive de
   subvention) — ne jamais inscrire un reste à réaliser sur simple intention
   de dépense ou de recette.
3. **Reprise** : les restes à réaliser sont repris au budget de l'exercice
   suivant, dans les conditions prévues par `nomenclature-m57.md` §5.8.

### 3.5 Provisions et dépréciations

1. Examiner si des provisions doivent être constituées ou ajustées en fin
   d'exercice (risque identifié, litige, dépréciation d'un actif).
2. Vérifier le caractère **obligatoire ou facultatif** de la provision selon
   la situation (`nomenclature-m57.md` §5.6) — l'absence de provision
   obligatoire est un déclencheur du **garde-fou budgétaire** (`SKILL.md`
   §5.3).

### 3.6 Opérations d'ordre de fin d'exercice

1. Passer les écritures d'ordre de clôture : dotations aux amortissements de
   l'exercice, reprises de subventions d'équipement, autres opérations
   d'ordre budgétaire ou semi-budgétaire (`nomenclature-m57.md` §5.9).
2. Vérifier la cohérence entre ces opérations d'ordre et l'état de l'actif
   tenu par le comptable.

### 3.7 Arrêté des comptes

1. L'ordonnateur arrête le **compte administratif** (ou alimente le
   **compte financier unique** selon le régime applicable à la
   collectivité).
2. Le comptable produit le **compte de gestion** (ou sa partie du CFU).
3. Vérifier la **concordance stricte** entre les deux documents avant
   présentation à l'assemblée — toute discordance doit être résolue avant le
   vote.

### 3.8 Compte administratif / compte de gestion / compte financier unique

1. Présenter à l'assemblée le compte administratif (ou le CFU) accompagné du
   compte de gestion.
2. Respecter les règles de vote propres à ce compte (participation de
   l'ordonnateur, quorum) — `budget-cycle.md` §5.6.

### 3.9 Affectation du résultat

1. Une fois le compte adopté, faire délibérer l'assemblée sur
   **l'affectation du résultat de fonctionnement** : couverture prioritaire
   du besoin de financement de la section d'investissement, report en
   fonctionnement, ou combinaison des deux selon les règles applicables
   (`budget-cycle.md` §5.7).
2. Vérifier la cohérence entre le résultat affecté et les restes à réaliser
   constatés (§3.4), qui déterminent le besoin de financement de la section
   d'investissement.

### 3.10 Détection d'un risque de déficit

1. Si le compte administratif fait apparaître un **déficit au-delà du seuil
   légal** (seuil à vérifier, non chiffré de mémoire), ne pas poursuivre
   l'exécution en l'état.
2. Afficher l'**ALERTE BUDGÉTAIRE** (`SKILL.md` §5.3) avant tout contenu
   métier complémentaire, et orienter vers
   `../references/controle-budgetaire.md` §4.3 (le compte administratif en
   déficit) pour la qualification précise du cas et la procédure de
   saisine.

---

## 4. Écrits associés

- **Compte administratif / compte financier unique** — support d'adoption
  par l'assemblée ; mentions et annexes réglementaires à vérifier via
  `budget-cycle.md` §5.6.
- **Délibération d'affectation du résultat** — `../references/templates/deliberation-budgetaire.md`.
- **État des restes à réaliser** : document annexé, listant chaque reste
  avec sa pièce justificative.
- **Fiche de procédure fin d'exercice** — `../references/templates/fiche-procedure-financiere.md` : calendrier interne, répartition des tâches entre services.

**Acte soumis au contrôle de légalité** : compte administratif / CFU et
délibération d'affectation du résultat — vérifier compétence, mentions
obligatoires et transmission via `../references/controle-budgetaire.md`.

---

## 5. Jurisprudence clé

> Pointeur uniquement — voir **`recherche-juridique`**. Aucune décision n'est
> citée ici par son nom d'usage, son millésime ou son numéro.

Thèmes appelant une recherche avant conclusion :
- Conséquences d'une **discordance non résolue** entre compte administratif
  et compte de gestion.
- Conditions de régularité d'un **reste à réaliser** insuffisamment justifié.
- Contentieux relatifs à l'**affectation du résultat** non conforme aux
  règles de priorité applicables.
- Portée exacte du **seuil de déficit** déclenchant la saisine de la chambre
  régionale des comptes.

---

## 6. Check-list opérationnelle

### Garde-fou budgétaire (`SKILL.md` §5.3) — à vérifier en priorité

- [ ] Le compte administratif fait-il apparaître un **déficit au-delà du
      seuil légal** ? Si oui → **ALERTE BUDGÉTAIRE** affichée avant tout
      contenu, orientation vers `controle-budgetaire.md` §4.3.
- [ ] Une **provision obligatoire** a-t-elle été omise ? Si oui → même
      traitement.

### Rattachement, restes à réaliser, provisions

- [ ] Charges et produits de l'exercice rattachés selon la méthode prévue,
      sans report indu sur l'exercice suivant ?
- [ ] Restes à réaliser recensés et **chacun justifié par une pièce
      probante** ?
- [ ] Provisions et dépréciations examinées et, si obligatoires,
      constituées ?
- [ ] Opérations d'ordre de clôture passées et cohérentes avec l'état de
      l'actif ?

### Arrêté des comptes et affectation

- [ ] Concordance entre compte administratif et compte de gestion / CFU
      vérifiée avant présentation à l'assemblée ?
- [ ] Règles de vote respectées (participation de l'ordonnateur, quorum) ?
- [ ] Affectation du résultat conforme aux règles de priorité et cohérente
      avec les restes à réaliser ?
- [ ] Calendrier de clôture (journée complémentaire, dates limites) vérifié
      et non présumé ?
- [ ] Couple [risque / confiance] indiqué — risque élevé dès qu'un déficit
      ou une discordance apparaît.
- [ ] Cas journalisable (discordance persistante, reste à réaliser
      insuffisamment justifié, déficit détecté) → proposé pour `JOURNAL.md`.

---

## Références et remontées

**Branches mobilisées** : `budget-cycle.md` (calendrier, compte
administratif, affectation), `nomenclature-m57.md` (rattachement, restes à
réaliser, provisions, opérations d'ordre), `controle-budgetaire.md` (risque
de déficit), `execution-depense.md` et `execution-recette.md`
(mandatements et titres de fin d'exercice).

**Point de mise à jour requis** : calendrier légal de clôture, durée de la
journée complémentaire, seuil de déficit déclenchant la saisine de la
chambre régionale des comptes, calendrier de généralisation du compte
financier unique.
