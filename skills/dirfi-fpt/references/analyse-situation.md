# Decision Engine — analyse d'une situation financière

> **Couche 1 du skill `dirfi-fpt`.** Routeur appelé **en premier** pour toute
> situation un peu composée. Il ne contient pas de règle de fond : il
> **qualifie**, **détecte les garde-fous** et **oriente** vers la branche
> (couche 2), l'objet (couche 3) ou le générateur d'écrit (couche 4).

---

## 0. Réflexe d'entrée — deux questions avant tout le reste

Avant d'analyser quoi que ce soit, passer les deux détecteurs. Ils sont
**prioritaires sur la réponse métier** et leur sortie s'affiche **avant** tout
autre contenu.

### Détecteur A — maniement de fonds hors circuit du comptable

La situation décrit-elle l'un de ces cas ?

- un **service encaisse ou décaisse** directement, sans régie régulièrement
  instituée ;
- une **association** (comité des fêtes, amicale, office, association support)
  reçoit, conserve ou redistribue des fonds pour le compte de la collectivité ;
- une **subvention** rémunère en réalité une prestation commandée par la
  collectivité ;
- un **mandat est émis sans service fait**, ou pour un objet fictif ;
- une **avance de trésorerie** est consentie hors texte ;
- des **recettes sont conservées** par un service au lieu d'être versées au
  comptable ;
- une **caisse** fonctionne hors comptabilité, quelle que soit sa justification.

**Si oui** → appliquer le **hard stop** `SKILL.md` §5.2, puis son routeur en
4 points (régie → qualification du flux → satellite → abstention motivée).
Ne pas poursuivre l'analyse métier avant d'avoir affiché le STOP.

### Détecteur B — irrégularité budgétaire

La situation décrit-elle l'un de ces cas ?

- budget **non voté** à la date limite ;
- budget voté **en déséquilibre réel** ;
- **compte administratif en déficit** au-delà du seuil légal ;
- **dépense obligatoire** non inscrite ou sous-inscrite ;
- **exécution sans crédit ouvert** ;
- **provision obligatoire** absente ;
- charge reportée pour masquer un déséquilibre.

**Si oui** → appliquer l'**alerte budgétaire** `SKILL.md` §5.3, puis orienter
vers `controle-budgetaire.md`.

> Les deux détecteurs peuvent se déclencher ensemble. Dans ce cas, afficher le
> **STOP** (A) d'abord, puis l'**ALERTE BUDGÉTAIRE** (B), puis la réponse.

---

## 1. Qualifier la nature de l'opération

| Question | Ce qu'elle détermine |
|---|---|
| S'agit-il d'une **dépense** ou d'une **recette** ? | Branche d'exécution applicable |
| Relève-t-elle du **fonctionnement** ou de l'**investissement** ? | Section, règles d'amortissement, financement possible par emprunt |
| Est-ce un **acte budgétaire** (prévision) ou un **acte d'exécution** ? | Autorité compétente, formalisme, contrôle applicable |
| Y a-t-il un **tiers bénéficiaire** ? | Qualification du flux (subvention / achat / participation) |
| L'opération est-elle **ponctuelle** ou **pluriannuelle** ? | AP/CP ou AE/CP, programmation |
| Quel **exercice** est concerné ? | Date de référence (`SKILL.md` §5.4 réflexe 3) |

**Piège de section** : une dépense n'est d'investissement que si elle augmente
la valeur du patrimoine ou en prolonge la durée de vie. L'entretien courant
reste en fonctionnement. En cas de doute, renvoyer à `nomenclature-m57.md`
plutôt que de trancher.

---

## 2. Identifier l'autorité compétente

Trois niveaux, à ne jamais confondre :

| Autorité | Compétence type | Limite |
|---|---|---|
| **Assemblée délibérante** | Vote du budget, des taux, des tarifs, des subventions, du recours à l'emprunt, des garanties | Ne peut pas exécuter |
| **Exécutif (ordonnateur)** | Engage, liquide, mandate, émet les titres ; exerce les délégations consenties | Ne manie aucun fonds ; rend compte de ses délégations |
| **Comptable public assignataire** | Contrôle, paie, encaisse, recouvre, tient la comptabilité générale | Ne se substitue pas à l'ordonnateur ; ne juge pas l'opportunité |

**Questions à lever** : une **délégation** a-t-elle été consentie à l'exécutif,
et dans quelles limites ? La décision prise par délégation a-t-elle fait l'objet
du **compte rendu** à l'assemblée ? L'acte relève-t-il d'une compétence que
l'assemblée ne peut pas déléguer ?

**Si la réponse implique un acte du comptable** (rejet, réquisition, admission
en non-valeur), passer par `controle-interne-financier.md` avant de conclure.

---

## 3. Détecter un conflit ou une frontière

| Signal dans la demande | Conduite |
|---|---|
| Droit individuel d'un agent, régime indemnitaire, procédure statutaire | **Bloc BASCULE `drh-fpt`** (`SKILL.md` §5.5) **avant** tout contenu |
| Passation d'un marché (allotissement, critères, publicité, recours) | Signaler la limite : **hors périmètre**. S'en tenir au volet financier (`commande-publique-financiere.md`) |
| Doctrine ou pouvoirs de police municipale | → `dpm-fpt` (le budget du service reste ici) |
| Conformité RGPD d'un traitement | → `dpo-ct` (le coût reste ici) |
| Vigueur d'un texte, jurisprudence, identifiant traçable | → `recherche-juridique` |

**Règle de non-autorisation** : qu'un skill délégataire soit mobilisable dans la
session ne vaut **pas** autorisation de traiter à sa place.

---

## 4. Orienter vers la branche (couche 2)

| Si la demande porte sur… | Lire |
|---|---|
| Vote, calendrier, DOB, DM, compte administratif, AP/CP | `budget-cycle.md` |
| Imputation, amortissement, provision, rattachement, inventaire | `nomenclature-m57.md` |
| Engagement, service fait, mandatement, délai de paiement, pièces justificatives | `execution-depense.md` |
| Titre, recouvrement, non-valeur, régie de recettes, tarif | `execution-recette.md` |
| Taux, bases, abattements, exonérations, états fiscaux | `fiscalite-locale.md` |
| DGF, péréquation, DETR/DSIL, FCTVA, compensations | `dotations-perequation.md` |
| Emprunt, ligne de trésorerie, gestion active, garantie d'emprunt | `dette-tresorerie.md` |
| Épargne, ratios, capacité de désendettement, PPI, prospective | `prospective-analyse.md` |
| Subvention versée ou reçue, convention, contrôle du bénéficiaire | `subventions.md` |
| Avance, acompte, révision, retenue de garantie, pénalité, DGD | `commande-publique-financiere.md` |
| Séparation ordonnateur/comptable, rejet, contrôle interne, dématérialisation | `controle-interne-financier.md` |
| Quel écrit produire et comment | `ecrits-financiers.md` |

**Briques posture** (à mobiliser en plus, jamais à la place) :
`controle-budgetaire.md`, `contentieux-financier.md`, `retex.md`.

> Une situation croise souvent plusieurs branches. Lire **chacune** des branches
> mobilisées et **signaler le lien** plutôt que de dupliquer.

---

## 5. Orienter vers l'objet métier (couche 3)

Quand la demande porte sur une **situation type récurrente** plutôt que sur une
règle isolée, la fiche objet donne le chemin complet (acteurs, textes,
procédure, écrits, checklist) :

| Situation | Fiche |
|---|---|
| Verser une subvention à une association | `../objets/subvention-association.md` |
| Créer ou faire fonctionner une régie | `../objets/regie.md` |
| Contracter ou gérer un emprunt | `../objets/emprunt.md` |
| Monter une opération d'investissement | `../objets/operation-investissement.md` |
| Clôturer l'exercice | `../objets/cloture-exercice.md` |
| Piloter un satellite (budget annexe, CCAS, SEM, SPL, DSP) | `../objets/satellites.md` |
| Gérer une immobilisation (entrée, amortissement, sortie) | `../objets/immobilisation.md` |
| Suivre le volet financier d'un marché | `../objets/marche-public.md` |

---

## 6. Déterminer le niveau de vérification

Croiser la demande avec la **matrice §2.2 du `SKILL.md`**. Dès qu'une ligne
« Oui » est touchée, la vérification intervient **avant la première réponse
chiffrée ou juridiquement engageante**.

Points qui déclenchent systématiquement la vérification dans ce métier :

- toute **valeur** (taux, seuil, plafond, montant, barème, index) ;
- tout **délai** ou date limite ;
- toute **règle d'imputation** M57 ;
- toute **condition d'éligibilité** à une dotation, une subvention, le FCTVA ;
- toute **compétence** d'organe ;
- toute **mention obligatoire** d'un acte.

**Aucune valeur volatile ne se cite de mémoire.** Si elle n'a pas été vérifiée
en séance, elle ne figure pas dans la réponse — ou elle y figure marquée
`⚠️ non vérifié`.

---

## 7. Fixer le couple [risque / confiance]

Le **risque** se lit sur l'enjeu, pas sur la difficulté :

| Enjeu présent | Risque plancher |
|---|---|
| Question de méthode, aucun acte en jeu | Faible |
| Acte interne, régularisable sans tiers | Moyen |
| Acte faisant grief, engagement d'un tiers, montant significatif | Élevé |
| Responsabilité personnelle, gestion de fait, saisine CRC, équilibre du budget | **Critique** |

Appliquer ensuite la grille `SKILL.md` §5.1 et indiquer le couple en sortie
quand il est utile à la décision.

---

## 8. Hiérarchiser l'urgence et le calendrier

Les finances locales sont un métier de **dates**. Avant de conclure, situer la
demande dans le calendrier :

1. Y a-t-il une **date limite légale** (vote, transmission, notification,
   déclaration) ? Si oui, la nommer et la faire vérifier.
2. Y a-t-il un **délai de paiement** en cours qui court ?
3. L'opération doit-elle être rattachée à l'**exercice** en cours ou au
   suivant ?
4. La **journée complémentaire** est-elle encore ouverte ?
5. Une **délibération préalable** est-elle nécessaire, et l'assemblée se
   réunit-elle à temps ?

Signaler tout risque de forclusion **avant** de dérouler la solution technique.

---

## 9. Orienter vers l'écrit (couche 4)

Si la demande appelle un livrable, passer par `ecrits-financiers.md` qui route
vers le bon générateur de `templates/`. Appliquer la **logique interactive** :
poser les questions **une à une**, ne jamais inventer un montant, une imputation
ou une date ; à défaut, produire un brouillon marqué `[INCOMPLET]` listant les
champs manquants.

---

## 10. Sortie du routeur — ordre imposé

1. **STOP** gestion de fait (§5.2) si détecteur A ;
2. **ALERTE BUDGÉTAIRE** (§5.3) si détecteur B ;
3. **BASCULE `drh-fpt`** (§5.5) si frontière statutaire touchée ;
4. réponse métier, sourcée selon §6 ci-dessus ;
5. couple **[risque / confiance]** si utile ;
6. **écrit** ou brouillon `[INCOMPLET]` si demandé ;
7. proposition d'entrée `JOURNAL.md` si le cas est journalisable.
