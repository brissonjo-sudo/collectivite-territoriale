# Objet métier — Immobilisation (v1.0.0)

> **Situation type** : Un bien entre dans le patrimoine de la collectivité
> (acquisition, production, mise à disposition, don) ou en sort (cession,
> réforme) ; il faut l'inventorier, l'amortir ou le déprécier le cas échéant,
> et vérifier son éligibilité au FCTVA.
> **[Risque / Confiance]** : Risque **moyen**, plus élevé si le bien est un
> bien de retour de délégation de service public ou si la concordance
> inventaire / actif fait défaut. Confiance **stable** sur l'architecture des
> écritures ; **à vérifier** sur les durées d'amortissement, les seuils
> d'éligibilité au FCTVA et les catégories de biens dispensées
> d'amortissement.

---

## 1. Acteurs et autorités compétentes

| Acteur | Rôle | Compétence |
|---|---|---|
| **Exécutif (ordonnateur)** | Constate et gère | Tient l'**inventaire physique et comptable** en lien avec les services gestionnaires ; propose l'entrée ou la sortie d'un bien |
| **Assemblée délibérante** | Fixe le cadre | Fixe, par délibération, les **durées d'amortissement** applicables par catégorie de biens, dans les fourchettes réglementaires |
| **Comptable public assignataire** | Tient l'état de l'actif | Tient l'**état de l'actif** et le compte financier unique ; passe les écritures d'amortissement et de sortie sur la base des éléments transmis par l'ordonnateur |
| **Service gestionnaire** | Suit le bien physiquement | Signale les mouvements physiques (mise en service, mise au rebut) déclenchant les écritures |

**Point de vigilance central** : l'**inventaire** (tenu par l'ordonnateur) et
l'**état de l'actif** (tenu par le comptable) sont deux documents distincts
qui doivent être **concordants**. Une divergence non résolue fragilise la
fiabilité du bilan et retarde la clôture de l'exercice.

---

## 2. Textes applicables (pointeurs)

> Le fond n'est pas reproduit ici.

- **`../references/nomenclature-m57.md`** §5.5 (amortissements), §5.6
  (provisions et dépréciations), §5.9 (immobilisations, inventaire et
  opérations d'ordre / réelles), §5.10 (état de l'actif et compte financier
  unique) — branche de fond principale.
- **`../references/execution-depense.md`** et
  **`../references/commande-publique-financiere.md`** — acquisition ou
  production d'un bien par la commande publique.
- **`../references/execution-recette.md`** — cession d'un bien, encaissement
  du produit.
- **`../references/dotations-perequation.md`** §5.6 (FCTVA) — éligibilité et
  calendrier de versement.
- **`../objets/operation-investissement.md`** — entrée à l'actif d'un bien
  issu d'une opération pluriannuelle.
- **`../objets/satellites.md`** — biens de retour dans le cadre d'une
  délégation de service public.

**Réserve systématique** : durées d'amortissement par catégorie de biens,
seuils de dispense d'amortissement, taux et modalités du FCTVA, seuils de
valorisation des dons — aucune de ces valeurs ne se cite de mémoire.

---

## 3. Procédures

### 3.1 Entrée à l'actif

1. **Acquisition onéreuse** : valorisation au coût d'acquisition (prix
   d'achat, frais accessoires directement rattachables) — vérifier le
   périmètre exact des frais à intégrer.
2. **Production immobilisée** : valorisation au coût de production (bien
   créé par les moyens propres de la collectivité) — méthode de calcul à
   documenter.
3. **Mise à disposition** entre budgets ou entre collectivités (transfert de
   compétence) : valorisation et écritures spécifiques, distinctes d'une
   cession — vérifier le régime applicable avant toute écriture.
4. **Affectation** : changement d'usage d'un bien déjà inscrit à l'actif,
   sans acquisition nouvelle — tracer le changement dans l'inventaire.
5. **Don ou legs** : valorisation à la valeur vénale ou à défaut à une
   valeur estimée, à documenter précisément (acte, expertise le cas
   échéant).

### 3.2 Inventaire et état de l'actif

1. Tenir un **inventaire physique et comptable** exhaustif, mis à jour à
   chaque mouvement (entrée, sortie, changement d'affectation).
2. Le comptable tient en parallèle l'**état de l'actif** — document distinct
   retraçant les mêmes biens sous l'angle comptable.
3. Organiser un **rapprochement périodique** entre inventaire et état de
   l'actif ; documenter et régulariser toute divergence avant la clôture de
   l'exercice.

### 3.3 Amortissement

1. Identifier les **biens concernés** par l'amortissement selon la nature de
   la collectivité et la catégorie du bien — certaines catégories peuvent
   être dispensées, à vérifier sans présumer.
2. Faire fixer par l'assemblée délibérante la **durée d'amortissement**
   applicable à chaque catégorie de biens, dans les fourchettes fixées par
   le texte applicable — jamais de durée citée de mémoire.
3. Faire courir l'amortissement à compter de la **date de début** prévue
   (typiquement la mise en service du bien) — vérifier la règle exacte de
   point de départ avant toute écriture.
4. Passer l'écriture d'amortissement en opération d'ordre budgétaire
   (`nomenclature-m57.md` §5.9), à chaque exercice, jusqu'à extinction de la
   valeur nette comptable.

### 3.4 Dépréciation

1. Distinguer la **dépréciation** (perte de valeur constatée, réversible ou
   non, hors plan d'amortissement) de l'amortissement (consommation
   planifiée de la valeur du bien).
2. Vérifier le caractère obligatoire ou facultatif de la dépréciation dans
   la situation rencontrée (`nomenclature-m57.md` §5.6) — l'absence d'une
   dépréciation obligatoire est un déclencheur potentiel du **garde-fou
   budgétaire** (`SKILL.md` §5.3).

### 3.5 Sortie

1. **Cession** : constater la recette de cession
   (`../references/execution-recette.md`), sortir le bien de l'actif pour sa
   valeur nette comptable, et passer l'écriture de sortie correspondante
   (plus ou moins-value).
2. **Réforme ou mise au rebut** : sortir le bien de l'actif sans recette,
   pour sa valeur nette comptable résiduelle, par une opération d'ordre.
3. Dans les deux cas, mettre à jour simultanément l'inventaire et signaler
   la sortie au comptable pour ajustement de l'état de l'actif.

### 3.6 Éligibilité au FCTVA

1. Vérifier la **nature de la dépense** (immobilisation, entretien de
   voirie ou de bâtiments selon le régime applicable) et le
   **bénéficiaire** au regard des conditions d'éligibilité au FCTVA
   (`dotations-perequation.md` §5.6).
2. Vérifier le **calendrier** de perception (immédiat ou différé selon le
   régime applicable à la collectivité).
3. Ne jamais présumer l'éligibilité d'une dépense sans vérification —
   certaines dépenses d'investissement en sont exclues.

### 3.7 Biens de retour en délégation de service public

1. Vérifier, dans le contrat de délégation, le régime des **biens de
   retour** : propriété de la collectivité dès l'origine, ou seulement en
   fin de contrat, selon la clause contractuelle applicable.
2. Identifier qui, du délégataire ou de la collectivité, porte
   l'amortissement du bien pendant la durée du contrat — cette répartition
   dépend du contrat et ne se présume pas.
3. À l'échéance du contrat, organiser l'entrée à l'actif de la collectivité
   des biens de retour non encore inscrits, sur la base de leur valeur
   contractuellement définie.

---

## 4. Écrits associés

- **Fiche d'inventaire** : support de suivi physique et comptable du bien
  (identification, valeur d'entrée, date de mise en service, durée
  d'amortissement, valeur nette comptable).
- **Délibération fixant les durées d'amortissement** — `../references/templates/deliberation-budgetaire.md`.
- **Décision de sortie (cession, réforme)** : acte de l'ordonnateur,
  formalisme à adapter localement, à archiver avec la fiche d'inventaire.
- **Tableau de rapprochement inventaire / état de l'actif** : à produire à
  chaque clôture d'exercice (`../objets/cloture-exercice.md`).

**Acte soumis au contrôle de légalité** : délibération fixant les durées
d'amortissement — vérifier compétence et mentions obligatoires via
`../references/controle-budgetaire.md`.

---

## 5. Jurisprudence clé

> Pointeur uniquement — voir **`recherche-juridique`**. Aucune décision n'est
> citée ici par son nom d'usage, son millésime ou son numéro.

Thèmes appelant une recherche avant conclusion :
- Conséquences d'une **discordance persistante** entre inventaire et état de
  l'actif sur la fiabilité des comptes.
- Contentieux relatifs à la **qualification des biens de retour** en
  délégation de service public.
- Conditions d'**éligibilité au FCTVA** contestées par le représentant de
  l'État.
- Régime de responsabilité en cas d'**absence d'amortissement obligatoire**.

---

## 6. Check-list opérationnelle

- [ ] Modalité d'entrée à l'actif identifiée (acquisition, production, mise
      à disposition, affectation, don) et valorisée selon la méthode
      correspondante ?
- [ ] Inventaire mis à jour et **rapproché de l'état de l'actif** tenu par le
      comptable, toute divergence documentée et régularisée ?
- [ ] Bien identifié comme relevant ou non de l'amortissement, sans
      présomption ?
- [ ] Durée d'amortissement fixée par délibération, jamais citée de mémoire ?
- [ ] Point de départ de l'amortissement vérifié avant toute écriture ?
- [ ] Dépréciation obligatoire non omise — sinon **garde-fou budgétaire**
      (`SKILL.md` §5.3) à envisager ?
- [ ] Sortie (cession ou réforme) traitée par l'écriture correspondante et
      répercutée sur l'inventaire ?
- [ ] Éligibilité au FCTVA vérifiée avant toute annonce de recette attendue ?
- [ ] Régime des biens de retour en DSP vérifié dans le contrat avant toute
      affirmation sur la propriété ou l'amortissement ?
- [ ] Couple [risque / confiance] indiqué si utile à la décision.
- [ ] Cas journalisable (discordance récurrente, éligibilité FCTVA
      contestée) → proposé pour `JOURNAL.md`.

---

## Références et remontées

**Branches mobilisées** : `nomenclature-m57.md` (fond), `execution-depense.md`
et `commande-publique-financiere.md` (acquisition), `execution-recette.md`
(cession), `dotations-perequation.md` (FCTVA).

**Objets liés** : `../objets/operation-investissement.md` (entrée à l'actif
d'une opération pluriannuelle), `../objets/satellites.md` (biens de retour en
DSP), `../objets/cloture-exercice.md` (rapprochement de fin d'exercice).

**Point de mise à jour requis** : fourchettes de durées d'amortissement par
catégorie de biens, catégories dispensées d'amortissement, taux et
calendrier du FCTVA — valeurs et seuils à réviser à chaque évolution
réglementaire.
