# Générateur interactif — Fiche de procédure financière (v1.0.0)

> Couche 4 (`references/templates/`), piloté par `references/ecrits-financiers.md`
> et par `SKILL.md` §6. Mécanique de dialogue alignée sur les générateurs du
> skill frère `Dpm-fpt` (questions posées **une à une**, aucune donnée
> inventée, règle `[INCOMPLET]` stricte, checklist finale). Le contenu
> métier est propre aux finances locales. Branche de rattachement :
> `../controle-interne-financier.md`.
>
> **Nature de l'écrit** : la fiche de procédure financière est un document
> **interne** de la direction des finances — **pas un acte administratif**,
> ni un écrit destiné à un tiers. Elle sert le **contrôle interne** : elle
> doit rendre visible, pour tout processus financier récurrent, **qui fait
> quoi et qui contrôle quoi**. Une fiche qui ne distingue pas clairement
> l'acteur qui exécute de l'acteur qui contrôle manque son objet, même si
> elle est par ailleurs complète.

---

## 0. Quand utiliser ce générateur

La fiche de procédure sert à documenter un **processus interne récurrent**
de la direction des finances : circuit de la dépense, fonctionnement d'une
régie, traitement d'un rejet du comptable, clôture d'exercice, ou tout autre
processus financier répété dans le temps.

**Avant d'ouvrir ce générateur**, vérifier que l'écrit demandé est bien une
fiche de procédure et non un autre document :

1. **S'agit-il de chiffrer un projet ponctuel ?** Oui →
   `note-impact-financier.md`, pas ce générateur — la fiche de procédure ne
   chiffre pas, elle décrit un processus répété.
2. **S'agit-il de décider ou d'acter quelque chose (vote, convention) ?**
   Oui → `deliberation-budgetaire.md` ou `convention-subvention.md`, pas ce
   générateur — la fiche de procédure est descriptive, pas décisionnelle.
3. **Le processus décrit fait-il apparaître un maniement de deniers publics
   hors circuit du comptable (`SKILL.md` §5.2), par exemple une régie non
   régulièrement instituée ou un encaissement conservé par un service ?**
   Oui → afficher le **STOP** avant tout autre contenu et orienter vers la
   voie régulière ; la fiche de procédure ne documente jamais un circuit
   irrégulier comme s'il était une pratique normale.

Si aucun de ces cas ne redirige ailleurs : la **fiche de procédure
financière** est le bon écrit. Poursuivre au §1.

---

## 1. Séquence interactive obligatoire

**Principe directeur** (`SKILL.md` §6) : questions posées **une à une**,
jamais en bloc. Confirmer chaque réponse avant de passer au champ suivant.
Ne jamais pré-remplir un champ non fourni : appliquer la règle `[INCOMPLET]`
(§4).

### Étape 1 — Processus visé
- Q1 : « Quel processus précis cette fiche doit-elle documenter (circuit de
  la dépense, fonctionnement d'une régie, traitement d'un rejet du
  comptable, clôture d'exercice, ou autre) ? »
- Pourquoi : cadre l'ensemble de la fiche ; un processus mal délimité produit
  une fiche inutilisable en contrôle interne.

### Étape 2 — Périmètre
- Q2 : « Quel est le périmètre exact de la procédure (quels types de
  dépenses ou de recettes, quels services concernés, quels seuils de montant
  éventuels qui changent le circuit) ? »
- Pourquoi : un même processus (ex. circuit de la dépense) peut avoir des
  variantes selon le montant ou la nature de la dépense — les préciser évite
  une fiche trop générale pour être opérante.

### Étape 3 — Acteurs et rôles
- Q3 : « Quels sont les acteurs intervenant dans ce processus (service
  demandeur, service financier, ordonnateur ou son délégataire, comptable
  public, autre), et quel est le rôle précis de chacun ? »
- Pourquoi : c'est le socle de la fiche — sans acteurs identifiés
  précisément, aucune séparation des tâches ne peut être documentée (§3 de ce
  gabarit).

### Étape 4 — Déclencheur
- Q4 : « Qu'est-ce qui déclenche ce processus (réception d'une facture,
  demande d'un service, événement calendaire de fin d'exercice, notification
  d'un rejet) ? »
- Pourquoi : identifie le point d'entrée, nécessaire pour situer chaque
  étape suivante dans le temps.

### Étape 5 — Étapes, avec responsable et délai
- Q5 : « Pouvez-vous décrire chaque étape du processus, dans l'ordre, en
  précisant pour chacune : qui la réalise, et le délai attendu (si
  applicable) ? »
- Pourquoi : c'est le cœur de la fiche. Poser cette question **étape par
  étape** si le processus est complexe : ne pas exiger une réponse
  exhaustive en un seul bloc si l'utilisateur préfère décrire une étape à la
  fois — confirmer chaque étape avant de passer à la suivante.

### Étape 6 — Points de contrôle et séparation des tâches
- Q6 : « À quelles étapes un contrôle est-il exercé, par qui, et cette
  personne est-elle bien distincte de celle qui a réalisé l'étape
  contrôlée ? »
- **Point d'insistance obligatoire** : si un même acteur apparaît comme
  exécutant et contrôleur d'une même étape, **relancer explicitement** :
  « Cette étape est-elle réellement contrôlée par une personne différente de
  celle qui l'exécute ? Si non, s'agit-il d'un point de fragilité du
  contrôle interne à signaler ? » Ne jamais euphémiser une absence de
  séparation des tâches : la nommer comme telle dans la fiche (§5 de ce
  gabarit, points de vigilance).

### Étape 7 — Pièces produites
- Q7 : « Quelles pièces sont produites à chaque étape ou en sortie du
  processus (bon de commande, certification du service fait, titre,
  mandat, état de rapprochement, autre) ? »

### Étape 8 — Cas particuliers
- Q8 : « Existe-t-il des cas particuliers ou des exceptions à ce processus
  (urgence, montant dérogatoire, absence d'un acteur habituel, période de
  transition d'exercice) ? Comment sont-ils traités ? »
- Pourquoi : une procédure qui ne documente que le cas général laisse les
  cas de dérogation sans contrôle identifié — risque de contournement du
  contrôle interne.

### Étape 9 — Indicateurs
- Q9 : « Quels indicateurs permettent de suivre le bon fonctionnement de ce
  processus (délai moyen, taux de rejet, nombre d'anomalies constatées,
  autre) ? »

### Étape 10 — Date de révision
- Q10 : « À quelle échéance ou selon quel déclencheur cette fiche doit-elle
  être révisée (périodicité fixe, changement réglementaire, changement
  d'organisation) ? »
- Pourquoi : une fiche de procédure non révisée devient une source
  d'erreur ; la date ou le déclencheur de révision est une mention
  obligatoire, pas une option.

**À l'issue de l'étape 10** : si toutes les réponses nécessaires ont été
recueillies, passer à l'assemblage (§2). Sinon, appliquer la règle
`[INCOMPLET]` (§4).

---

## 2. Gabarit d'assemblage

> Champs à compléter entre `[ ]`. Aucun nom d'agent réel dans ce canevas :
> désigner les acteurs par leur **fonction** (« le service financier »,
> « l'ordonnateur », « le comptable public »), jamais par leur identité.

```
[COLLECTIVITÉ — direction des finances]

FICHE DE PROCÉDURE FINANCIÈRE N° [numéro / référence interne]
Version [numéro], applicable à compter du [date]

Processus : [intitulé précis — étape 1]
Périmètre : [types de dépenses/recettes, services, seuils de montant
concernés — étape 2]

I. ACTEURS ET RÔLES

| Acteur (fonction) | Rôle dans le processus |
|---|---|
| [Acteur 1] | [rôle précis] |
| [Acteur 2] | [rôle précis] |
| [...] | [...] |

II. DÉCLENCHEUR
[Événement déclenchant le processus — étape 4]

III. DÉROULÉ DES ÉTAPES

| N° | Étape | Responsable | Délai | Pièce produite |
|---|---|---|---|---|
| 1 | [description] | [acteur] | [délai ou « non fixé »] | [pièce] |
| 2 | [description] | [acteur] | [délai ou « non fixé »] | [pièce] |
| [...] | [...] | [...] | [...] | [...] |

IV. POINTS DE CONTRÔLE ET SÉPARATION DES TÂCHES

| Étape contrôlée | Contrôleur | Distinct de l'exécutant ? | Point de vigilance |
|---|---|---|---|
| [étape n°] | [acteur contrôleur] | [Oui / Non] | [si Non : signaler explicitement la fragilité, ne jamais l'euphémiser] |
| [...] | [...] | [...] | [...] |

V. CAS PARTICULIERS
[Exceptions et leur traitement — étape 8 ; si un cas particulier échappe à
tout contrôle identifié, le signaler explicitement comme un point de
vigilance, pas seulement le décrire.]

VI. INDICATEURS DE SUIVI
[Indicateurs retenus — étape 9]

VII. RÉVISION
Prochaine révision : [date ou déclencheur — étape 10]
Fondement de la procédure (renvoi de fond, non recopié ici) :
`../controle-interne-financier.md`, et branche métier du processus concerné
(ex. `../execution-depense.md`, `../execution-recette.md`,
`../budget-cycle.md` selon l'objet — à préciser).

Rédigée par : [fonction du rédacteur]
Validée par : [fonction du validateur, distincte du rédacteur si possible]
Date : [date]
```

---

## 3. Mentions obligatoires et contrôles de cohérence

- [ ] Processus et périmètre précisément délimités (étapes 1 et 2).
- [ ] Chaque acteur identifié par sa **fonction**, jamais par son identité
  (étape 3).
- [ ] Chaque étape du déroulé associée à un responsable et, si pertinent, un
  délai (étape 5) — aucune étape sans responsable identifié.
- [ ] **Chaque point de contrôle** de la table IV comporte une réponse
  explicite « Oui » ou « Non » à la colonne « Distinct de l'exécutant ? » —
  jamais laissée vide.
- [ ] Toute réponse « Non » à cette colonne est accompagnée d'un point de
  vigilance rédigé, jamais silencieuse.
- [ ] Cas particuliers traités avec leur propre circuit de contrôle, ou
  signalés comme non couverts (étape 8).
- [ ] Date ou déclencheur de révision renseigné — jamais absent (étape 10).
- [ ] Rédacteur et validateur distingués lorsque l'organisation le permet,
  cohérent avec la logique de séparation des tâches portée par la fiche
  elle-même.

---

## 4. Règle `[INCOMPLET]` — application stricte

**Interdiction absolue d'halluciner une donnée manquante** : responsable
d'une étape, délai, nature du contrôle, date de révision.

1. Produire le brouillon avec les champs disponibles ; une étape ou une
   section incomplète ne bloque pas la rédaction des autres.
2. Marquer chaque champ manquant `[INCOMPLET — préciser : <nom du champ>]`.
3. En fin de document, si au moins un champ est marqué `[INCOMPLET]`,
   ajouter :

```
---
## CHAMPS MANQUANTS — FICHE NON FINALISABLE EN L'ÉTAT

Les informations suivantes sont requises avant validation et diffusion :
- [champ manquant 1 — étape correspondante]
- [champ manquant 2 — étape correspondante]
- [...]

Cette fiche ne doit être ni validée, ni diffusée comme procédure applicable,
tant que ces champs ne sont pas renseignés.
```

4. **Demander explicitement** ces données à l'utilisateur, en reprenant la
   formulation de la question d'étape correspondante (§1).
5. Ne jamais marquer le document comme « validé » tant qu'une mention
   `[INCOMPLET]` subsiste.
6. **Cas particulier — séparation des tâches non renseignée (étape 6)** : ne
   jamais présumer qu'un contrôle est distinct de l'exécution faute de
   précision ; marquer `[INCOMPLET — préciser : contrôleur distinct de
   l'exécutant, à confirmer]` plutôt que de cocher « Oui » par défaut.

---

## 5. Ce que la fiche doit rendre visible — rappel

La fiche de procédure sert le **contrôle interne**. Elle échoue à son objet
si, à la lecture, il n'est pas possible de répondre immédiatement à deux
questions pour chaque étape sensible :
- **Qui fait ?** (colonne « Responsable » du tableau III)
- **Qui contrôle ?**, et **est-ce une personne différente ?** (tableau IV)

Une fiche qui décrit un processus sans jamais répondre à la seconde
question n'est pas une fiche de contrôle interne, seulement un mode
opératoire — le générateur ne la considère pas complète tant que le tableau
IV n'est pas rempli pour chaque étape identifiée comme sensible en séance
(étape 6).

---

## 6. Double échelle [risque / confiance]

| Point | Risque | Confiance |
|---|---|---|
| Absence de séparation des tâches sur une étape sensible | Élevé | Signalement obligatoire, jamais euphémisé |
| Cas particulier sans circuit de contrôle identifié | Moyen à élevé | À traiter explicitement ou signaler l'absence de couverture |
| Délai non fixé sur une étape critique | Moyen | Signaler l'absence de délai plutôt que d'en inventer un |
| Fiche non révisée au-delà de sa date prévue | Moyen | Vérifier la date de révision avant tout usage |
| Processus touchant une régie ou un circuit de recette | Élevé | Renvoi `../controle-interne-financier.md` et vérification du garde-fou `SKILL.md` §5.2 |

---

## 7. Checklist avant remise

1. Garde-fou testé en premier (§0) : le processus décrit ne documente pas un
   circuit de maniement de fonds irrégulier.
2. Toutes les étapes du §1 parcourues une à une, avec confirmation à chaque
   étape, y compris le déroulé détaillé (étape 5) traité pas à pas si le
   processus est complexe.
3. Chaque acteur désigné par sa fonction, jamais par son identité.
4. Tableau des étapes complet : chaque étape a un responsable, et un délai
   ou la mention explicite de son absence.
5. **Tableau de séparation des tâches** rempli pour chaque étape sensible
   identifiée, avec un point de vigilance rédigé pour chaque réponse
   « Non ».
6. Cas particuliers traités ou signalés comme non couverts (étape 8).
7. Date ou déclencheur de révision renseigné (étape 10) — jamais absent.
8. Aucune donnée manquante comblée par supposition — règle `[INCOMPLET]`
   (§4) appliquée et champs listés explicitement si nécessaire.
9. Aucune donnée nominative, aucun nom d'agent réel dans le document
   produit.
10. Mention finale claire : fiche **prête à validation** ou marquée
    **`[INCOMPLET]`** avec demande explicite des champs manquants — jamais
    d'état intermédiaire ambigu.
