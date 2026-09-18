# Objet métier — Opération d'investissement (v1.0.0)

> **Situation type** : La collectivité monte un projet d'investissement
> (construction, réhabilitation, équipement) qui dépasse un seul exercice ; il
> faut le définir, l'inscrire en autorisation de programme, bâtir son plan de
> financement, l'articuler avec la programmation pluriannuelle, l'exécuter
> puis le clôturer.
> **[Risque / Confiance]** : Risque **moyen**, croissant avec la durée et le
> nombre de financeurs externes mobilisés. Confiance **stable** sur
> l'architecture AP/CP et le phasage ; **à vérifier** sur les taux de
> subvention, le taux du FCTVA et les délais de notification des financeurs.

---

## 1. Acteurs et autorités compétentes

| Acteur | Rôle | Compétence |
|---|---|---|
| **Assemblée délibérante** | Décide | Vote l'autorisation de programme (AP) et ses crédits de paiement (CP) annuels ; adopte le plan de financement ; vote les révisions de l'AP |
| **Exécutif (ordonnateur)** | Exécute | Engage la dépense dans l'enveloppe de l'AP et les CP ouverts ; pilote le phasage ; signe les actes d'exécution du marché |
| **Comptable public assignataire** | Paie | Paie sur mandat après contrôle du service fait ; procède aux écritures d'entrée du bien à l'actif |
| **Financeurs externes** (État, région, département, Europe, FCTVA) | Cofinancent | Notifient une décision attributive conditionnant tout ou partie du plan de financement |
| **Services techniques (maîtrise d'ouvrage)** | Exécutent le projet | Suivent l'exécution physique et transmettent les éléments de service fait à l'ordonnateur — hors périmètre financier de cette fiche |

---

## 2. Textes applicables (pointeurs)

> Le fond n'est pas reproduit ici.

- **`../references/budget-cycle.md`** §5.9 bis (AP/CP et AE/CP) — inscription,
  vote, gestion pluriannuelle des crédits.
- **`../references/prospective-analyse.md`** §5.6 (programmation
  pluriannuelle des investissements) — articulation de l'opération avec la
  PPI d'ensemble.
- **`../references/subventions.md`** §5.13 (subventions reçues) — recherche
  de financement, dossier, notification, autofinancement minimal, caducité.
- **`../references/dotations-perequation.md`** §5.6 (FCTVA) et §5.5
  (dotations d'investissement) — financement externe de l'opération.
- **`../references/dette-tresorerie.md`** — financement par emprunt, voir
  `../objets/emprunt.md`.
- **`../references/commande-publique-financiere.md`** — exécution financière
  du marché support de l'opération (avances, acomptes, révision) ; voir
  `../objets/marche-public.md` pour le suivi détaillé du volet financier —
  **la passation reste hors périmètre** (`SKILL.md` §5.6).
- **`../references/nomenclature-m57.md`** §5.9 (immobilisations, inventaire,
  opérations d'ordre) — entrée du bien à l'actif ; voir
  `../objets/immobilisation.md` pour le détail.

**Réserve systématique** : taux de subvention, taux du FCTVA, plafonds de
dotations d'investissement, délais de caducité des financements notifiés —
aucune de ces valeurs ne se cite de mémoire.

---

## 3. Procédures

### 3.1 Définition de l'opération

1. Délimiter le périmètre de l'opération comme un **ensemble homogène** de
   travaux, d'études ou d'acquisitions concourant à un même objectif, sur
   plusieurs exercices.
2. Distinguer l'opération des simples crédits d'investissement annuels sans
   caractère pluriannuel — seule une opération pluriannuelle relève d'une
   gestion en AP/CP.

### 3.2 Inscription en AP/CP

1. Faire voter par l'assemblée le **montant total de l'autorisation de
   programme** (enveloppe globale, plafond de la dépense pouvant être
   engagée juridiquement sur la durée de l'opération).
2. Faire voter, chaque exercice, les **crédits de paiement** correspondant
   à l'échéancier prévisionnel de décaissement.
3. Vérifier la cohérence entre le cumul des CP votés sur la durée et le
   montant total de l'AP — tout dépassement suppose une révision (§3.7).

### 3.3 Plan de financement

1. Identifier l'ensemble des ressources mobilisables : autofinancement
   (épargne dégagée par la section de fonctionnement), subventions
   d'investissement notifiées ou sollicitées, FCTVA, emprunt.
2. Construire le plan de financement en distinguant montants **acquis**
   (décision attributive notifiée) et montants **sollicités** (dossier
   déposé, non encore notifié) — ne jamais présenter un montant sollicité
   comme acquis.
3. Vérifier le respect d'un éventuel **taux d'autofinancement minimal**
   (`subventions.md` §5.13) — valeur à vérifier avant toute conclusion.
4. Actualiser le plan de financement à chaque notification ou évolution du
   coût de l'opération.

### 3.4 Articulation avec la programmation pluriannuelle

1. Vérifier la cohérence de l'opération avec la **programmation
   pluriannuelle des investissements (PPI)** de la collectivité
   (`prospective-analyse.md` §5.6) : priorité, calendrier, impact sur la
   capacité de désendettement.
2. Signaler tout écart significatif entre l'opération et la trajectoire
   financière prévue par la PPI.

### 3.5 Phasage

1. Découper l'opération en phases (études préalables, études de conception,
   travaux, réception, mise en service) et associer un échéancier financier
   à chaque phase.
2. Ajuster les CP annuels sur la base de l'avancement réel, non sur la
   seule prévision initiale.

### 3.6 Exécution financière du marché

1. Suivre le volet financier du ou des marchés supports de l'opération
   (engagement, avances, acomptes, révision de prix, décompte général et
   définitif) — voir `../objets/marche-public.md` pour le détail complet.
2. Rappeler que la **passation** du marché (choix du titulaire,
   allotissement, critères) reste **hors périmètre** de ce skill
   (`SKILL.md` §5.6) et doit être signalée comme telle si la question
   glisse vers ce terrain.

### 3.7 Révisions de l'autorisation de programme

1. Toute variation significative du coût total de l'opération (aléas de
   chantier, avenants, actualisation des prix) impose de faire délibérer
   l'assemblée sur une **révision de l'AP**, à la hausse ou à la baisse.
2. Documenter le motif de la révision et son impact sur le plan de
   financement et sur les CP des exercices restants.

### 3.8 Entrée du bien à l'actif

1. À l'achèvement de l'opération (ou de chaque tranche fonctionnelle), faire
   procéder à l'**entrée du bien à l'actif** — voir
   `../objets/immobilisation.md` pour la procédure complète (valorisation,
   inventaire, amortissement).
2. Vérifier la concordance entre la valeur d'entrée à l'actif et le coût
   total effectivement mandaté sur l'opération.

### 3.9 Clôture de l'opération

1. Constater l'achèvement physique et financier de l'opération.
2. Solder les crédits de paiement non consommés (annulation) ou traiter les
   éventuels restes à réaliser (`../objets/cloture-exercice.md`).
3. Clore l'AP par délibération, en cohérence avec le montant définitivement
   exécuté.
4. Archiver le dossier complet (délibérations d'AP/CP et de révision, plan
   de financement actualisé, décision attributive des financeurs, pièces
   d'entrée à l'actif).

---

## 4. Écrits associés

- **Délibération d'ouverture ou de révision d'AP/CP** — `../references/templates/deliberation-budgetaire.md`.
- **Note d'impact financier** de l'opération (coût global, plan de
  financement, impact sur la prospective) — `../references/templates/note-impact-financier.md`.
- **Plan de financement prévisionnel** actualisé à chaque notification de
  financeur.
- **Fiche de clôture d'opération** : bilan financier final, écart avec la
  prévision, entrée à l'actif — formalisme à adapter localement.

**Acte soumis au contrôle de légalité** : délibération d'AP/CP et de
révision — vérifier compétence, mentions obligatoires et transmission via
`../references/controle-budgetaire.md`.

---

## 5. Jurisprudence clé

> Pointeur uniquement — voir **`recherche-juridique`**. Aucune décision n'est
> citée ici par son nom d'usage, son millésime ou son numéro.

Thèmes appelant une recherche avant conclusion :
- Conséquences d'un **engagement au-delà du montant de l'AP** non révisée.
- Portée d'une **décision attributive de subvention non notifiée** sur la
  régularité de l'engagement de la dépense.
- Contentieux liés à la **valorisation d'entrée à l'actif** d'un bien issu
  d'une opération pluriannuelle.

---

## 6. Check-list opérationnelle

- [ ] Opération définie comme un ensemble homogène et pluriannuel, distinct
      de crédits d'investissement courants ?
- [ ] AP votée et CP annuels cohérents avec l'échéancier prévisionnel ?
- [ ] Plan de financement distinguant montants acquis et montants sollicités,
      sans présentation trompeuse ?
- [ ] Taux d'autofinancement minimal vérifié, jamais chiffré de mémoire ?
- [ ] Cohérence avec la programmation pluriannuelle des investissements
      vérifiée ?
- [ ] Phasage et échéancier des CP ajustés sur l'avancement réel ?
- [ ] Volet financier du marché suivi via `../objets/marche-public.md`, et
      **passation signalée comme hors périmètre** si la question l'aborde ?
- [ ] Toute variation significative du coût traitée par une **révision d'AP**
      délibérée, avant poursuite de l'engagement ?
- [ ] Entrée du bien à l'actif organisée et cohérente avec le coût mandaté ?
- [ ] Clôture de l'opération formalisée (AP soldée, restes à réaliser
      traités, dossier archivé) ?
- [ ] Couple [risque / confiance] indiqué si utile à la décision.
- [ ] Cas journalisable (dépassement d'AP non révisé, financement caduc
      découvert tardivement) → proposé pour `JOURNAL.md`.

---

## Références et remontées

**Branches mobilisées** : `budget-cycle.md` (AP/CP), `prospective-analyse.md`
(PPI), `subventions.md` et `dotations-perequation.md` (financement externe),
`dette-tresorerie.md` (emprunt), `commande-publique-financiere.md` (volet
financier du marché), `nomenclature-m57.md` (entrée à l'actif).

**Objets liés** : `../objets/emprunt.md` (financement par emprunt),
`../objets/marche-public.md` (volet financier du marché support),
`../objets/immobilisation.md` (entrée à l'actif), `../objets/cloture-exercice.md` (restes à réaliser en fin d'exercice).

**Point de mise à jour requis** : taux du FCTVA, taux de subvention par
financeur, plafonds des dotations d'investissement (DETR, DSIL, DPV) —
valeurs volatiles à réviser à chaque loi de finances.
