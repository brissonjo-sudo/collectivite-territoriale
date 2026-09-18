# Générateur interactif — Convention de subvention (v1.0.0)

> Couche 4 (`references/templates/`), piloté par `references/ecrits-financiers.md`
> et par `SKILL.md` §6. Mécanique de dialogue alignée sur les générateurs du
> skill frère `Dpm-fpt` (questions posées **une à une**, aucune donnée
> inventée, règle `[INCOMPLET]` stricte, checklist finale). Le contenu
> métier est propre aux finances locales. Branche de rattachement :
> `../subventions.md`.
>
> **Garde-fou §5.2 `SKILL.md` — à dérouler avant toute rédaction.** Une
> subvention qui rémunère en réalité une prestation, ou versée à une
> association transparente servant de caisse à la collectivité, caractérise
> un risque de **gestion de fait** ou de **requalification en marché
> public**. Ce générateur **refuse de produire une convention de subvention**
> tant que la qualification préalable du flux (§0) n'a pas écarté ce risque,
> et **le dit explicitement** à l'utilisateur.

---

## 0. Contrôle préalable obligatoire — qualification du flux

**Avant toute question de rédaction**, poser et trancher cette question,
seule et en premier, conformément à `../subventions.md` §5.1 :

> « Qui est à l'initiative du projet financé, et qui en définit le
> contenu — le bénéficiaire, ou la collectivité ? La collectivité impose-t-
> elle un cahier des charges, des spécifications précises, un calendrier
> d'exécution détaillé, en échange du versement ? »

**Grille de décision** :

| Constat | Qualification | Suite |
|---|---|---|
| Le bénéficiaire est à l'initiative de son action, la collectivité n'impose pas de spécifications précises | **Subvention** | Poursuivre au §1 |
| La collectivité définit le besoin (cahier des charges, spécifications techniques ou fonctionnelles) et rémunère une prestation déterminée | **Commande publique** | **Refuser** de rédiger une convention de subvention (voir bloc ci-dessous) |
| Incertain après une relance | Indéterminé | Ne pas trancher soi-même ; marquer `[INCOMPLET — préciser : nature du flux, à qualifier avant toute rédaction]` et renvoyer à `../subventions.md` §5.1 et `../commande-publique-financiere.md` |

**Si la qualification est « commande publique »**, afficher, avant tout
autre contenu :

```
REFUS — Ce flux qualifie une commande publique, pas une subvention.
La collectivité définit le besoin et rémunère une prestation déterminée :
rédiger une convention de subvention exposerait à une requalification en
marché public, avec les conséquences d'une procédure de passation non
suivie.
Je ne rédige pas de convention de subvention pour ce flux.
Orientez-vous vers ../commande-publique-financiere.md pour le support
contractuel adapté (marché, bon de commande, ou procédure adaptée selon le
montant).
```

**Signal d'alerte propre à la subvention à une association** (`../subventions.md`
§5.12) : si l'association bénéficiaire présente un risque d'**association
transparente** (dirigeants, financement ou activité la confondant avec un
service de la collectivité), suspendre également l'assemblage et renvoyer à
`../../objets/satellites.md` avant de poursuivre — ce risque relève au fond
du garde-fou `SKILL.md` §5.2.

**Seulement si la qualification est confirmée « subvention »** : poursuivre
au §1.

---

## 1. Séquence interactive obligatoire

**Principe directeur** (`SKILL.md` §6) : questions posées **une à une**,
jamais en bloc. Confirmer chaque réponse avant de passer au champ suivant.
Ne jamais pré-remplir un champ non fourni : appliquer la règle `[INCOMPLET]`
(§5).

### Étape 1 — Bénéficiaire et nature juridique
- Q1 : « Quel est le bénéficiaire (nature juridique : association loi 1901,
  fondation, autre organisme de droit privé, établissement public) ? »
- Pourquoi : la nature juridique conditionne le régime applicable — renvoi
  `../subventions.md` §5.9 à §5.11 selon le cas (association, entreprise,
  personne privée).

### Étape 2 — Objet précis de la subvention
- Q2 : « Quel est l'objet précis de l'action ou du projet soutenu ? »
- Pourquoi : l'objet doit rester formulé comme le **soutien à une action du
  bénéficiaire**, jamais comme la commande d'une prestation à livrer
  (`../subventions.md` §5.4) — cohérence à revérifier avec le §0.

### Étape 3 — Montant et pluriannualité
- Q3 : « Quel est le montant envisagé, et s'agit-il d'une subvention
  annuelle ou pluriannuelle (auquel cas, sur combien d'exercices et selon
  quelle répartition) ? »
- Pourquoi : le montant cumulé par bénéficiaire et par exercice détermine si
  la convention est **obligatoire** (au-delà du seuil réglementaire, à
  vérifier) ou seulement une **faculté** (`../subventions.md` §5.3). Ne
  jamais énoncer ce seuil de mémoire.

### Étape 4 — Compétence et acte d'attribution
- Q4 : « Une délibération d'attribution existe-t-elle ou est-elle à
  produire en parallèle (`deliberation-budgetaire.md`) ? L'assemblée a-t-elle
  délégué l'attribution des subventions à l'exécutif, et dans quelles
  limites ? »
- Pourquoi : l'attribution relève de la compétence de l'assemblée délibérante
  sauf délégation régulière (`../subventions.md` §5.2) — jamais présumée.

### Étape 5 — Modalités de versement
- Q5 : « Le versement intervient-il en une fois ou en plusieurs fractions
  (acompte, solde après justification) ? Une avance est-elle prévue, et sur
  quelle base ? »
- Pourquoi : une avance ne se présume jamais de droit commun ; elle doit
  être expressément prévue par la convention ou la délibération
  (`../subventions.md` §5.5).

### Étape 6 — Obligations du bénéficiaire
- Q6 : « Quelles obligations le bénéficiaire doit-il respecter (réalisation
  de l'action dans les conditions annoncées, mention de la collectivité dans
  sa communication, restitution en cas de non-exécution) ? »

### Étape 7 — Justificatifs et compte rendu financier
- Q7 : « Quels justificatifs le bénéficiaire doit-il produire (compte rendu
  financier, bilan d'activité, comptes annuels), et selon quelle
  périodicité ? »
- Pourquoi : renvoi `../subventions.md` §5.6 et §5.7 ; l'absence de contrôle
  effectif affaiblit la défense de la collectivité en cas de contestation.

### Étape 8 — Contrôle et droit de visite
- Q8 : « La collectivité doit-elle pouvoir exercer un contrôle sur place de
  l'utilisation des fonds (droit de visite), en plus du contrôle sur
  pièces ? »

### Étape 9 — Reversement
- Q9 : « En cas de non-exécution, de non-conformité à l'objet, ou de
  dissolution du bénéficiaire, la convention prévoit-elle une clause de
  reversement ? Selon quelles modalités et quel délai ? »
- Pourquoi : renvoi `../subventions.md` §5.8 ; le délai d'action en
  reversement doit être vérifié, notamment si la convention resterait
  silencieuse.

### Étape 10 — Durée
- Q10 : « Quelle est la durée de la convention (annuelle, pluriannuelle avec
  reconduction expresse ou tacite) ? »

### Étape 11 — Résiliation
- Q11 : « Dans quels cas et selon quelles modalités (préavis, motif) la
  convention peut-elle être résiliée par l'une ou l'autre partie ? »

### Étape 12 — Assurances
- Q12 : « Le bénéficiaire doit-il justifier d'une couverture d'assurance
  pour l'activité financée (responsabilité civile notamment) ? »

### Étape 13 — Communication
- Q13 : « Quelles obligations de communication ou de visibilité de la
  collectivité sont attendues du bénéficiaire (logo, mention dans les
  supports, événement) ? » — vigilance : cette mention reste une
  contrepartie de **communication**, pas une prestation qui requalifierait le
  flux en commande publique (renvoi §0).

**À l'issue de l'étape 13** : si toutes les réponses nécessaires ont été
recueillies, passer à l'assemblage (§2). Sinon, appliquer la règle
`[INCOMPLET]` (§5).

---

## 2. Gabarit d'assemblage

> Champs à compléter entre `[ ]`. Aucun nom d'organisme réel, aucune donnée
> nominative dans ce canevas.

```
[COLLECTIVITÉ — en-tête]

CONVENTION DE SUBVENTION N° [numéro] / [année]

Entre :
[COLLECTIVITÉ], représentée par [autorité habilitée, en vertu de
[délibération ou délégation identifiée — étape 4]],
d'une part,

Et :
[Bénéficiaire — nature juridique précisée à l'étape 1],
d'autre part,

Il est convenu ce qui suit :

Préambule
[Rappel de la qualification du flux opérée au §0 : « la présente convention
a pour objet de soutenir une action à l'initiative du bénéficiaire, sans
contrepartie directe équivalente au bénéfice de la collectivité » —
formulation à adapter, jamais supprimée.]

Article 1er — Objet
[Objet précis de l'action soutenue — étape 2, formulé comme un soutien,
jamais comme une commande de prestation.]

Article 2 — Montant et pluriannualité
[Montant [ ] au titre de l'exercice [ ] — étape 3. Si pluriannuel :
répartition par exercice, sous réserve du vote annuel des crédits
correspondants par l'assemblée délibérante.]

Article 3 — Références de l'acte d'attribution
[Délibération n° [ ] du [date], ou délégation à l'exécutif référencée
[ ] — étape 4.]

Article 4 — Modalités de versement
[Versement en une fois / en plusieurs fractions, avance le cas échéant et
sa base — étape 5.]

Article 5 — Obligations du bénéficiaire
[Réalisation de l'action dans les conditions annoncées, mention de la
collectivité, autres obligations précisées — étape 6.]

Article 6 — Justificatifs et compte rendu financier
[Nature des pièces, périodicité — étape 7.]

Article 7 — Contrôle et droit de visite
[Modalités de contrôle sur pièces et, le cas échéant, sur place — étape 8.]

Article 8 — Reversement
[Cas et modalités de reversement en cas de non-exécution, non-conformité ou
dissolution — étape 9.]

Article 9 — Durée
[Durée de la convention, reconduction éventuelle — étape 10.]

Article 10 — Résiliation
[Cas et modalités de résiliation — étape 11.]

Article 11 — Assurances
[Obligation de couverture d'assurance du bénéficiaire — étape 12.]

Article 12 — Communication
[Obligations de communication du bénéficiaire — étape 13.]

Article 13 — Litiges
[Juridiction compétente en cas de litige — [INCOMPLET] si non précisée.]

Fait à [lieu], en [nombre] exemplaires, le [date].

Pour [COLLECTIVITÉ] : [autorité habilitée]
Pour [Bénéficiaire] : [représentant habilité]
```

---

## 3. Mentions obligatoires et contrôles de cohérence

- [ ] Qualification du flux (subvention / commande publique) tranchée en
  premier (§0), avec refus explicite si la réponse est « commande
  publique ».
- [ ] Risque d'association transparente testé et écarté ou signalé (§0,
  renvoi `../../objets/satellites.md`).
- [ ] Nature juridique du bénéficiaire précisée (étape 1).
- [ ] Objet formulé comme un soutien à l'action du bénéficiaire, jamais
  comme une commande de prestation (étape 2, cohérence avec §0).
- [ ] Montant et durée cohérents entre l'article 2 (montant) et l'article 9
  (durée) — pas de contradiction entre un montant présenté comme annuel et
  une durée présentée comme pluriannuelle sans répartition.
- [ ] Compétence et acte d'attribution référencés (délibération ou
  délégation) — jamais présumés (étape 4).
- [ ] Clause de reversement présente si le montant ou la durée le
  justifient (étape 9).
- [ ] Justificatifs et modalités de contrôle précisés (étapes 7 et 8).
- [ ] Aucune contrepartie directe équivalente au bénéfice de la
  collectivité ne figure dans le corps de la convention (au-delà de la
  communication, étape 13) — tout ajout de ce type est un signal de
  requalification à revérifier au §0.

---

## 4. Renvoi à `deliberation-budgetaire.md`

La convention **ne se substitue jamais** à la délibération d'attribution.
Si celle-ci n'existe pas encore, le signaler explicitement et proposer de
l'assembler en parallèle via `deliberation-budgetaire.md`, avec vérification
de la compétence de l'assemblée et, au-delà du seuil de conventionnement, de
la transmission au contrôle de légalité (`../controle-budgetaire.md`).

---

## 5. Règle `[INCOMPLET]` — application stricte

**Interdiction absolue d'halluciner une donnée manquante** : montant, seuil
de conventionnement, référence de délibération, délai de reversement, durée.

1. Produire le brouillon avec les champs disponibles ; un champ manquant ne
   bloque pas la rédaction des autres articles.
2. Marquer chaque champ manquant `[INCOMPLET — préciser : <nom du champ>]`.
3. En fin de document, si au moins un champ est marqué `[INCOMPLET]`,
   ajouter :

```
---
## CHAMPS MANQUANTS — CONVENTION NON FINALISABLE EN L'ÉTAT

Les informations suivantes sont requises avant signature :
- [champ manquant 1 — étape correspondante]
- [champ manquant 2 — étape correspondante]
- [...]

Cette convention ne doit être ni signée, ni transmise, tant que ces champs
ne sont pas renseignés — et tant que la qualification du flux (§0) n'est
pas confirmée « subvention ».
```

4. **Demander explicitement** ces données à l'utilisateur, en reprenant la
   formulation de la question d'étape correspondante (§1).
5. Ne jamais marquer le document comme « prêt à signer » tant qu'une mention
   `[INCOMPLET]` subsiste, ou tant que le §0 n'a pas été explicitement
   tranché en faveur de la qualification « subvention ».

---

## 6. Double échelle [risque / confiance]

| Point | Risque | Confiance |
|---|---|---|
| Qualification subvention / commande publique | Critique | À trancher avant toute rédaction — jamais présumée |
| Risque d'association transparente | Critique | Renvoi impératif `SKILL.md` §5.2 et `../../objets/satellites.md` |
| Compétence de l'assemblée / délégation | Élevé | À vérifier systématiquement |
| Seuil de conventionnement obligatoire | Élevé | Jamais cité de mémoire — à vérifier |
| Clause de reversement | Moyen à élevé | Délai à vérifier si convention silencieuse |
| Aides à une entreprise (le cas échéant) | Élevé | Renvoi `../subventions.md` §5.10 — compétence régionale, encadrement européen |

---

## 7. Checklist avant remise

1. **Contrôle préalable de qualification (§0)** effectué en premier, avant
   toute autre question — refus explicite si le flux qualifie une commande
   publique.
2. Risque d'association transparente testé (§0) — renvoi
   `../../objets/satellites.md` si un doute subsiste.
3. Toutes les étapes du §1 parcourues une à une, avec confirmation à chaque
   étape.
4. Nature juridique du bénéficiaire précisée (étape 1).
5. Objet formulé comme un soutien, jamais comme une commande de prestation
   (étape 2).
6. Compétence et acte d'attribution référencés, ou renvoi explicite vers
   `deliberation-budgetaire.md` si l'acte reste à produire (§4).
7. Montant, versement, justificatifs, contrôle et reversement tous traités
   (étapes 3, 5, 7, 8, 9).
8. Aucune donnée manquante comblée par supposition — règle `[INCOMPLET]`
   (§5) appliquée et champs listés explicitement si nécessaire.
9. Aucune donnée nominative, aucun nom d'organisme réel dans le document
   produit.
10. Mention finale claire : convention **prête à signer** ou marquée
    **`[INCOMPLET]`**, ou **refusée** si la qualification du §0 l'impose —
    jamais d'état intermédiaire ambigu.
