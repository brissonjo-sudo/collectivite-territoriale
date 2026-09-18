# Générateur interactif — Délibération budgétaire (v1.0.0)

> Couche 4 (`references/templates/`), piloté par `references/ecrits-financiers.md`
> et par `SKILL.md` §6. Mécanique de dialogue alignée sur les générateurs du
> skill frère dpm-fpt : questions posées **une à une**, aucune donnée inventée,
> règle `[INCOMPLET]` stricte, checklist finale avant remise. Le contenu métier
> propre aux finances locales est développé ici.
>
> **Nature de l'écrit** : la délibération budgétaire est un **acte
> administratif** de l'assemblée délibérante, susceptible de **faire grief**
> et **soumis au contrôle de légalité** dès qu'elle relève de la liste des
> actes transmissibles. Ce générateur est **subordonné** à
> `../controle-budgetaire.md` : la compétence de l'organe, l'équilibre réel et
> les conditions de régularité doivent être vérifiées **avant** toute
> rédaction. Branches de rattachement : `../budget-cycle.md` (fond de l'acte
> budgétaire concerné) et `../controle-budgetaire.md` (régularité, saisine,
> régularisation).
>
> **Ce fichier ne tranche jamais seul** l'imputation comptable de fond
> (renvoi `../nomenclature-m57.md`), ni la régularité d'un acte déjà pris
> (renvoi `../controle-budgetaire.md`) : il **assemble** le document à partir
> de données vérifiées et **signale** les points non levés.

---

## 0. Quand utiliser ce générateur

Une **délibération budgétaire ou financière** est l'acte par lequel
l'assemblée délibérante (ou l'exécutif par délégation régulière) décide en
matière de budget : budget primitif, décision modificative, budget
supplémentaire, affectation du résultat, garantie d'emprunt, admission en
non-valeur, création d'une régie, attribution d'une subvention, virement de
crédits relevant de sa compétence.

**Avant d'ouvrir ce générateur**, vérifier que l'écrit demandé est bien une
délibération et non un autre document :

1. **S'agit-il d'éclairer une décision sans la formaliser (note d'aide à la
   décision) ?** Oui → `note-impact-financier.md`, pas ce générateur.
2. **S'agit-il du rapport préalable au débat d'orientation budgétaire, sans
   dispositif décisionnel ?** Oui → `rapport-orientation-budgetaire.md`, pas
   ce générateur.
3. **S'agit-il d'une convention avec un tiers (organisme bénéficiaire d'une
   subvention) ?** Oui → `convention-subvention.md`. La délibération
   d'attribution reste toutefois nécessaire en amont ou en parallèle : les
   deux écrits sont complémentaires, pas substituables l'un à l'autre.
4. **La situation décrit-elle un maniement de deniers publics hors circuit du
   comptable (§5.2 `SKILL.md`) ou un acte budgétaire déjà irrégulier
   (§5.3 `SKILL.md`) ?** Oui → afficher le **STOP** ou l'**ALERTE
   BUDGÉTAIRE** correspondant **avant tout autre contenu**, puis orienter vers
   `../controle-budgetaire.md`. Ne jamais rédiger de délibération destinée à
   couvrir a posteriori un tel montage.

Si aucun de ces cas ne redirige ailleurs : la **délibération budgétaire** est
le bon écrit. Poursuivre au §1.

---

## 1. Séquence interactive obligatoire

**Principe directeur** (`SKILL.md` §6) : les questions sont posées **une à
une**, jamais en bloc. Confirmer chaque réponse avant de passer au champ
suivant. Ne jamais pré-remplir un champ non fourni : appliquer la règle
`[INCOMPLET]` (§4).

### Étape 1 — Objet exact de la délibération
- Q1 : « Quel est l'objet précis de cette délibération (budget primitif,
  décision modificative, affectation du résultat, garantie d'emprunt,
  admission en non-valeur, création de régie, attribution de subvention,
  autre) ? »
- Pourquoi : l'objet commande le régime juridique applicable (formalisme,
  majorité requise, transmission) — renvoi `../budget-cycle.md` selon le cas.
- Si la réponse manque : impossible d'assembler quoi que ce soit d'utile ;
  marquer `[INCOMPLET — préciser : objet de la délibération]` et redemander
  en priorité avant de poursuivre les autres étapes.

### Étape 2 — Organe compétent et quorum
- Q2 : « Quel est l'organe appelé à délibérer (conseil municipal,
  communautaire, départemental, régional, autre assemblée), et l'objet
  relève-t-il d'une délégation déjà consentie à l'exécutif ? »
- Pourquoi : la compétence de l'organe est une ligne « Oui » de la matrice
  `SKILL.md` §2.2 — jamais présumée. Une délibération prise par un organe
  incompétent, ou par l'exécutif sans délégation régulière, est entachée
  d'incompétence.
- Si la délégation est incertaine : marquer `[INCOMPLET — préciser :
  existence et périmètre de la délégation]` et signaler le risque
  d'incompétence plutôt que de la présumer.

### Étape 3 — Date de la séance et convocation
- Q3 : « Quelle est la date de la séance, et la convocation a-t-elle été
  adressée dans le délai applicable, avec la note de synthèse ou le rapport
  requis pour ce type d'objet ? »
- Pourquoi : un vice de convocation ou l'absence de note explicative expose
  la délibération à l'annulation pour vice de procédure.
- Si la date ou les conditions de convocation manquent : `[INCOMPLET —
  préciser : date de séance / conditions de convocation]`.

### Étape 4 — Visas
- Q4 : « Quels textes souhaitez-vous viser (CGCT, code applicable au budget
  concerné, délibération antérieure sur le même objet, avis ou rapport
  préalable) ? »
- Pourquoi : chaque visa engage une provenance vérifiée. Ce générateur ne
  complète **jamais** un visa de mémoire.
- Chaque texte cité sans vérification dans la session est marqué `[Vu ... —
  à confirmer en version consolidée]`. Refuser tout visa générique du type
  « vu le CGCT » sans article précis.

### Étape 5 — Exposé des motifs
- Q5 : « Quel est le contexte et le motif de cette délibération (situation
  budgétaire, événement déclencheur, obligation réglementaire, projet à
  financer) ? »
- Pourquoi : l'exposé des motifs éclaire le contrôle de légalité et
  l'assemblée elle-même ; son absence ou son caractère stéréotypé fragilise
  l'acte, notamment s'il fait grief.

### Étape 6 — Dispositif article par article
- Q6 : « Que doit décider précisément chaque article (montant, affectation,
  bénéficiaire, condition, entrée en vigueur) ? Formulez la mesure exacte de
  chaque article envisagé. »
- Pourquoi : le dispositif est la seule partie opposable de la délibération ;
  toute imprécision (montant arrondi, bénéficiaire non identifié, condition
  implicite) est un risque contentieux ou d'exécution.

### Étape 7 — Incidence financière
- Q7 : « Quelle est l'incidence financière de cette délibération : section
  concernée (fonctionnement ou investissement), chapitre, article,
  imputation précise, montant ? »
- Pourquoi : la section et l'imputation conditionnent l'équilibre réel du
  budget (`../controle-budgetaire.md`) et la régularité de l'exécution qui
  suivra (`../nomenclature-m57.md`).
- **Aucun montant ni imputation ne se déduit ni ne s'arrondit** : si la
  donnée manque, marquer `[INCOMPLET — préciser : montant / imputation]` et
  ne jamais proposer un chiffre de substitution, même « pour l'exemple ».
- **Contrôle de cohérence obligatoire** : si des annexes chiffrées
  accompagnent la délibération (état de la dette, tableau des effectifs,
  liste des subventions, annexes du budget), le montant figurant dans le
  corps de la délibération doit être **strictement cohérent** avec celui des
  annexes. Signaler tout écart identifié et ne jamais le corriger de
  sa propre initiative.

### Étape 8 — Transmission au contrôle de légalité
- Q8 : « Cette délibération figure-t-elle dans la liste des actes soumis à
  transmission obligatoire au représentant de l'État, et par quel circuit
  (dématérialisé ou autre) ? »
- Pourquoi : le caractère exécutoire de l'acte est conditionné à sa
  publicité et, pour les actes concernés, à sa transmission — vérifier via
  `../controle-budgetaire.md`, jamais présumer une dispense.
- Si la réponse est incertaine : rappeler que la posture la plus sûre reste
  de transmettre, sans affirmer l'obligation comme acquise si elle n'a pas
  été vérifiée.

### Étape 9 — Voies et délais de recours (si l'acte fait grief)
- Q9 : « Cette délibération fait-elle grief à un tiers identifié ou à une
  catégorie de tiers (par exemple un bénéficiaire évincé, un contribuable
  local pour une délibération fiscale) ? »
- Pourquoi : si oui, les voies et délais de recours sont **obligatoires**
  dans l'acte ; leur omission empêche le délai de recours contentieux de
  courir contre le tiers concerné.
- Si la réponse reste incertaine : signaler le risque pratique plutôt que de
  trancher à la place de l'utilisateur.

**À l'issue de l'étape 9** : si toutes les réponses nécessaires ont été
recueillies, passer à l'assemblage (§2). Sinon, appliquer la règle
`[INCOMPLET]` (§4).

---

## 2. Gabarit d'assemblage

> Champs à compléter entre `[ ]`. Aucune collectivité, aucun nom de personne
> ou d'organisme réel ne figure dans ce canevas. Tout visa porte sa réserve
> de vérification tant qu'il n'a pas été confirmé dans la session en cours.

```
[COLLECTIVITÉ — en-tête]

DÉLIBÉRATION N° [numéro] / [année]
[Organe délibérant — étape 2] — Séance du [date — étape 3]

Objet : [intitulé synthétique — étape 1]

Le [organe délibérant], convoqué le [date de convocation — étape 3, dans le
délai applicable — à confirmer en version consolidée],

VU [le CGCT, article exact fondant la compétence de l'organe — étape 2, à
   confirmer en version consolidée] ;
VU [le texte spécial applicable à l'objet précis de la délibération —
   étape 4, ⚠️ à confirmer en version consolidée si non vérifié dans la
   session] ;
VU [la délibération ou l'acte antérieur sur le même objet, le cas
   échéant] ;
VU [le rapport ou la note de synthèse annexée à la convocation — étape 3] ;

CONSIDÉRANT [le contexte et le motif de la délibération — étape 5] ;
CONSIDÉRANT [le lien avec l'équilibre réel du budget ou avec la procédure
   budgétaire en cours, le cas échéant — renvoi ../controle-budgetaire.md] ;

Après en avoir délibéré,

DÉCIDE :

Article 1er — [dispositif précis — étape 6].
Article 2 — [incidence financière : section [fonctionnement /
   investissement], chapitre [ ], article [ ], imputation [ ], montant
   [ ] — étape 7. Si un doute de cohérence avec une annexe a été relevé, le
   signaler ici explicitement plutôt que de le corriger.]
Article 3 — [Si l'acte fait grief — étape 9 positive] La présente
   délibération peut faire l'objet, dans un délai de DEUX MOIS à compter de
   sa publication et de sa transmission, d'un recours contentieux devant le
   tribunal administratif de [ville], précédé le cas échéant d'un recours
   gracieux auprès de [autorité].
   [Si l'acte ne fait pas grief : « Article 3 — Sans objet », en signalant ce
   choix comme point à confirmer si un doute subsiste.]
Article 4 — [Autorité chargée de l'exécution] est chargé(e) de l'exécution
   de la présente délibération, qui sera publiée et [transmise au contrôle
   de légalité selon le circuit précisé à l'étape 8, ou « non soumise à
   transmission obligatoire — à confirmer en version consolidée »].

Fait à [lieu], le [date].
[Signature de l'autorité exécutive]

Annexes le cas échéant : [état de la dette / tableau des effectifs / liste
des subventions / autre — vérifier la cohérence des montants avec le corps
de l'acte, étape 7].
```

---

## 3. Mentions obligatoires et contrôles de cohérence

Avant d'assembler le document final, vérifier que chacun des points suivants
est renseigné ou explicitement marqué `[INCOMPLET]` :

- [ ] Organe compétent identifié, délégation vérifiée si l'acte est pris par
  l'exécutif (étape 2).
- [ ] Visas précis (texte + article exact), aucun visa générique.
- [ ] Exposé des motifs présent, non stéréotypé.
- [ ] Dispositif formulé précisément, article par article.
- [ ] **Section** (fonctionnement / investissement) qualifiée pour chaque
  incidence financière.
- [ ] **Imputation** (chapitre, article) renseignée ou marquée
  `[INCOMPLET]` — jamais déduite.
- [ ] **Montant du corps de l'acte cohérent avec les annexes** le cas
  échéant — tout écart signalé, jamais corrigé silencieusement.
- [ ] Équilibre réel du budget non remis en cause par cette délibération, ou
  renvoi explicite à `../controle-budgetaire.md` si un doute existe.
- [ ] Transmission au contrôle de légalité qualifiée (obligatoire /
  non soumise à confirmer) et circuit précisé.
- [ ] Voies et délais de recours mentionnés si l'acte fait grief.
- [ ] Autorité chargée de l'exécution identifiée.

---

## 4. Règle `[INCOMPLET]` — application stricte

**Interdiction absolue d'halluciner une donnée manquante** : montant,
imputation, date de séance, numéro de délibération, visa, organe compétent.

Si une information nécessaire n'a pas été fournie à l'issue de la séquence
de questions (§1) :

1. Produire le brouillon avec les champs disponibles ; un champ manquant ne
   bloque pas la rédaction des autres articles.
2. Marquer chaque champ manquant `[INCOMPLET — préciser : <nom du champ>]`
   directement à l'endroit où l'information devrait figurer.
3. En fin de document, si au moins un champ est marqué `[INCOMPLET]`,
   ajouter :

```
---
## CHAMPS MANQUANTS — DÉLIBÉRATION NON FINALISABLE EN L'ÉTAT

Les informations suivantes sont requises avant inscription à l'ordre du
jour et vote :
- [champ manquant 1 — étape correspondante]
- [champ manquant 2 — étape correspondante]
- [...]

Cette délibération ne doit être ni présentée en séance, ni transmise au
contrôle de légalité, tant que ces champs ne sont pas renseignés.
```

4. **Demander explicitement** ces données à l'utilisateur, en reprenant la
   formulation de la question d'étape correspondante (§1).
5. Ne jamais marquer le document comme « prêt à voter » ou « prêt à
   transmettre » tant qu'une mention `[INCOMPLET]` subsiste.
6. **Cas particulier — montant ou imputation incertains (étape 7)** : ne
   jamais estimer, arrondir ou déduire une valeur non fournie ; marquer
   `[INCOMPLET — préciser : montant exact / imputation exacte]` et signaler
   que ce point doit être levé avant tout vote.

---

## 5. Articulation avec les garde-fous et le contrôle budgétaire

- Si, à n'importe quelle étape du recueil, il apparaît un **maniement de
  deniers publics hors circuit du comptable** (`SKILL.md` §5.2) : interrompre
  la séquence, afficher le **STOP** avant toute chose, et orienter vers la
  voie régulière (régie, qualification du flux, satellite) avant de
  poursuivre l'assemblage, s'il reste pertinent.
- Si la délibération porte sur un **budget non voté, un déséquilibre réel,
  un déficit excessif ou une dépense obligatoire non inscrite**
  (`SKILL.md` §5.3) : afficher l'**ALERTE BUDGÉTAIRE** avant tout contenu et
  renvoyer à `../controle-budgetaire.md` pour qualifier le cas et la marge de
  régularisation avant toute rédaction définitive.
- Si l'objet touche une mesure de **masse salariale ou de régime
  indemnitaire** : rester au niveau de l'enveloppe et de l'imputation ;
  dès que la question porte sur le droit individuel de l'agent, émettre le
  bloc **BASCULE `drh-fpt`** (`SKILL.md` §5.5) avant tout contenu statutaire.

---

## 6. Double échelle [risque / confiance]

| Point | Risque | Confiance |
|---|---|---|
| Compétence de l'organe / délégation | Élevé | À vérifier systématiquement |
| Imputation et section | Élevé | À vérifier — jamais déduite |
| Équilibre réel du budget | Critique | Renvoi impératif `../controle-budgetaire.md` en cas de doute |
| Transmission au contrôle de légalité | Élevé | À vérifier — la posture la plus sûre est de transmettre en cas de doute |
| Voies et délais de recours si l'acte fait grief | Élevé | À vérifier au cas par cas |
| Cohérence corps / annexes | Élevé | Signalement obligatoire de tout écart, jamais de correction silencieuse |
| Donnée manquante | Élevé | N/A — `[INCOMPLET]` obligatoire |

---

## 7. Checklist avant remise

1. Garde-fous testés en premier (§5) : aucun montage de gestion de fait
   couvert, aucun acte budgétaire irrégulier présenté comme régularisable
   sans passage par `../controle-budgetaire.md`.
2. Toutes les étapes du §1 parcourues une à une, avec confirmation à chaque
   étape.
3. Organe compétent et délégation vérifiés (étape 2) — jamais présumés.
4. Visas précis, chacun portant sa provenance ou sa réserve « à confirmer en
   version consolidée » (étape 4).
5. Section, chapitre, article et imputation renseignés ou marqués
   `[INCOMPLET]` (étape 7) — aucun montant déduit ou arrondi.
6. Cohérence entre le montant du corps de l'acte et celui des annexes
   vérifiée ; tout écart signalé explicitement (§3).
7. Transmission au contrôle de légalité qualifiée et circuit précisé
   (étape 8), ou marquée à vérifier.
8. Voies et délais de recours mentionnés si l'acte fait grief (étape 9), ou
   signalés comme point incertain.
9. Aucune donnée manquante comblée par supposition — règle `[INCOMPLET]`
   (§4) appliquée et champs listés explicitement si nécessaire.
10. Aucune donnée nominative, aucun nom d'organisme ou de collectivité réel
    dans le document produit.
11. Mention finale claire : délibération **prête à inscription à l'ordre du
    jour** ou marquée **`[INCOMPLET]`** avec demande explicite des champs
    manquants — jamais d'état intermédiaire ambigu.
