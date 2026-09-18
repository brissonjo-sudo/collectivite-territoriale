# Brique posture — RETEX (retour d'expérience) (v0.1.0)

> Brique transverse, pas une branche métier. Les 12 sections du gabarit
> `_gabarit-branche.md` sont conservées et numérotées dans l'ordre ; certaines
> n'ont pas d'objet pour un outil de méthode et le signalent en une ligne.
> **Aucune base légale propre** : le RETEX analyse un cas déjà traité sous le
> fondement mobilisé au moment des faits — ce fondement se vérifie et se cite
> dans la branche de fond concernée, jamais ici.

## 1. Périmètre / Exclusions

- **Périmètre** : capitaliser sur un **cas financier déjà traité** —
  incident, lacune méthodologique, cas nouveau, écrit récurrent — pour
  alimenter `JOURNAL.md` et, le cas échéant, `CHANGELOG.md` ; structurer la
  **revue annuelle** du skill (`SKILL.md` §9).
- **Exclusions** : la **procédure de contrôle budgétaire** →
  `controle-budgetaire.md`. La **responsabilité financière et la gestion de
  fait** → `contentieux-financier.md`. Le **fond** de chaque règle traversée
  par le cas analysé → la branche métier concernée. La **procédure
  disciplinaire** individuelle → `drh-fpt`.

---

## 2. Questions couvertes

- « Ce cas mérite-t-il une entrée `JOURNAL.md` ? »
- « Comment analyser un rejet du comptable qui se répète ? Un dépassement de
  crédit ? Un retard de mandatement ? Une subvention mal qualifiée ? Un écart
  de prospective ? »
- « Comment faire remonter un enseignement du `JOURNAL.md` vers
  `CHANGELOG.md` ? »
- « Que couvre la revue de janvier ? Et celle du 1er septembre ? »
- « Comment anonymiser un cas avant de le consigner ? »

---

## 3. Arbre de traitement

`cas clos → qualifier s'il est journalisable (§5.1) → dérouler la grille
d'analyse si c'est un incident (§6.1) → rédiger l'entrée `JOURNAL.md` au
format imposé (§6.2), anonymisée (§5.2) → apprécier si l'enseignement dépasse
le cas d'espèce (§6.3) → le cas échéant, ouvrir `CHANGELOG.md` (et une ADR si
structurant) → verser le cas à la prochaine revue annuelle (§6.4)`

Ne jamais consigner un cas sans être passé par l'anonymisation (§5.2) : la
capitalisation n'autorise aucune exception.

---

## 4. Variables à lever

- **Nature du cas** : incident récurrent, lacune identifiée dans une branche,
  cas nouveau non couvert, ou écrit produit de façon répétée gagnant à
  devenir un gabarit.
- **Caractère isolé ou répété** : un incident isolé peut rester une note
  interne ; un incident qui se répète devient journalisable de plein droit.
- **Portée de l'enseignement** : correction ponctuelle ou évolution de
  méthode — oriente vers `JOURNAL.md` seul ou vers `JOURNAL.md` **et**
  `CHANGELOG.md`.
- **Présence de données sensibles** : montant précis, nom d'un agent, d'un
  élu, d'un administré ou d'un bénéficiaire — à traiter avant rédaction.

---

## 5. Règles métier

### 5.1 Ce qui mérite une entrée `JOURNAL.md`

Journaliser dès que l'une de ces conditions est réunie : une **lacune** du
skill est apparue (branche muette, règle absente, renvoi manquant) ; une
**erreur** a été produite (mauvaise autorité, mauvaise section, valeur non
vérifiée pourtant citée) ; un **cas nouveau** non couvert s'est présenté ; un
**écrit récurrent** signale un gabarit à formaliser dans
`references/templates/`. Ne pas journaliser un cas parfaitement couvert et
traité sans écart : la valeur du `JOURNAL.md` est dans l'écart, pas la
routine.

### 5.2 Règles d'anonymisation

**Aucune donnée nominative** : ni agent, ni élu, ni administré, ni
bénéficiaire nommé, y compris en exemple. **Montants** : ordre de grandeur
(faible, significatif, majeur) plutôt que montant exact d'un dossier
identifiable, sauf si indispensable à la cause et non recoupable. **Dates** :
mois et exercice, sauf si la chronologie fine est l'objet même de
l'enseignement. **Structure** : éviter de nommer un service ou un satellite
d'une manière permettant, par recoupement, d'identifier les personnes.

---

## 6. Calculs et procédures

### 6.1 Grille d'analyse d'un incident financier

| Étape | Contenu |
|---|---|
| 1. Chronologie factuelle | Faits datés : détection, décision, échange avec le comptable ou la CRC, issue. Distinguer établi et incertain. |
| 2. Catégorisation | Rejet du comptable répété, dépassement de crédit, retard de mandatement, subvention mal qualifiée, écart de prospective, ou autre. |
| 3. Cause | Imputation erronée, absence de crédit ouvert, délai de circuit interne, qualification insuffisante d'une convention, hypothèse non actualisée. |
| 4. Ce qui a fonctionné | Ce qui a permis de détecter ou limiter l'incident. |
| 5. Risque résiduel | La cause est-elle susceptible de se reproduire, sur quel autre dossier ? |
| 6. Action correctrice | Objet précis, pilote (fonction), échéance, critère de vérification. |

**Repères par type** : rejet répété → pièce manquante ou imputation erronée
récurrente, ou dialogue insuffisant avec le comptable ; dépassement de crédit
→ distinguer engagement sans crédit ouvert (`controle-budgetaire.md`) et
simple retard de DM ; retard de mandatement → risque d'intérêt moratoire
(`references/commande-publique-financiere.md`) ; subvention mal qualifiée →
risque de requalification (garde-fou `SKILL.md` §5.2) ; écart de prospective
→ hypothèse dépassée ou erreur de méthode (`references/prospective-analyse.md`).

### 6.2 Format d'une entrée de journal

Champs a minima : **Date** ; **Type** (incident récurrent / lacune / cas
nouveau / écrit récurrent) ; **Branche(s) concernée(s)** (pointeur) ;
**Constat** (1 à 3 phrases anonymisées) ; **Cause identifiée** (1 phrase) ;
**Action** (correction du skill ou interne, pilote-fonction, échéance) ;
**Suite** (`CHANGELOG.md` vX.Y.Z / ADR-xxxx / sans suite versionnée). Une
entrée sans **action** ni **suite** reste incomplète.

### 6.3 La boucle `JOURNAL.md` → `CHANGELOG.md`

Toute entrée révélant une **lacune de méthode** (pas seulement une erreur
d'espèce) est candidate à une évolution versionnée (MAJEUR.MINEUR.PATCH,
`SKILL.md` §9) d'une branche ou d'une brique, consignée dans `CHANGELOG.md`.
Une décision structurante (nouvelle frontière, nouveau garde-fou, refonte)
donne lieu, en plus, à une **ADR** dans `docs/adr/`. Chaque entrée
`CHANGELOG.md` issue d'un RETEX pointe vers l'entrée `JOURNAL.md` d'origine.

### 6.4 Revue annuelle

| Revue | Période | Contenu |
|---|---|---|
| **Revue de loi de finances** | Janvier | Dispositions fiscales et de dotations de l'année, seuils de la commande publique, taux du FCTVA, évolutions M57. |
| **Revue de rentrée** | 1er septembre | CGCT (volet budgétaire et comptable), CJF, instruction M57, jurisprudence financière de l'année ; revue systématique du `JOURNAL.md` accumulé. |

**Méthode** : reparcourir les entrées de la période, regrouper celles qui
pointent vers la même branche ou la même lacune, et arbitrer si une évolution
versionnée est nécessaire ou si le constat reste isolé.

---

## 7. Déclencheurs de vérification

**Sans objet en propre** : le RETEX n'a pas de base légale à vérifier pour
lui-même. Il **traverse** en revanche des sujets qui en ont : dès qu'un cas
analysé touche une qualification juridique, un délai ou un seuil, appliquer
le socle-sources (`SKILL.md` §5.4) dans la **branche de fond concernée**, pas
dans le RETEX lui-même.

---

## 8. Pièges & confusions fréquentes

1. Journaliser un cas sans écart réel — noie les cas significatifs ; ou à
   l'inverse laisser une entrée sans **action** ni **suite** (§6.2) — un
   constat seul n'est pas exploitable.
2. Aller directement aux actions correctrices sans chronologie factuelle
   (§6.1, étape 1) — perte de valeur probante.
3. Oublier l'**anonymisation** (§5.2), y compris pour un cas jugé « sans
   enjeu ».
4. Confondre le RETEX avec `contentieux-financier.md` ou
   `controle-budgetaire.md` : il ne tranche aucune de ces procédures, il
   capitalise après coup — et cite une base légale de mémoire au lieu de
   renvoyer à la branche de fond (§7).

---

## 9. Données / valeurs à vérifier

**Sans objet, par construction** : aucune valeur chiffrée ni aucun numéro
d'article n'est cité dans cette brique. Un point de droit traversé par un cas
se vérifie et se cite dans la branche de fond concernée.

---

## 10. Écrits & livrables

- **Entrée `JOURNAL.md`** — livrable principal, au format imposé (§6.2).
- **Entrée `CHANGELOG.md`** — quand l'enseignement dépasse le cas d'espèce
  (§6.3).
- **ADR** (`docs/adr/`) — quand la décision qui en découle est structurante.

Aucun de ces écrits n'est destiné à un tiers extérieur au skill.

---

## 11. Double échelle [risque / confiance]

- **Cas sans écart, versé pour mémoire** : [risque faible / confiance stable]
  — aucune vérification de source nécessaire.
- **Incident récurrent (rejet, dépassement, retard, subvention, prospective)** :
  [risque moyen / confiance stable sur la méthode, à vérifier sur tout point
  de droit traversé].
- **Cas touchant un volet contentieux ou disciplinaire** : [risque élevé / à
  vérifier] — cloisonner le RETEX (méthode) du volet procédure
  (`contentieux-financier.md`, `drh-fpt`) ; ne jamais y trancher une
  responsabilité.

---

## 12. Checklist de branche

1. Le cas a-t-il été qualifié comme journalisable (§5.1) ?
2. La **chronologie factuelle** a-t-elle précédé toute préconisation (§6.1) ?
3. L'incident a-t-il été catégorisé parmi les types repérés, ou explicitement
   qualifié d'« autre » (§6.1) ?
4. L'entrée respecte-t-elle le **format imposé** (§6.2), avec action et
   suite renseignées ?
5. La bascule vers `CHANGELOG.md` (et, si besoin, une ADR) a-t-elle été
   envisagée pour tout enseignement dépassant le cas d'espèce (§6.3) ?
6. Le cas a-t-il été situé par rapport à la prochaine **revue annuelle**
   (§6.4) ?
7. L'**anonymisation** (§5.2) a-t-elle été appliquée sans exception ?
8. Aucune base légale n'a-t-elle été citée de mémoire, tout point de droit
   étant renvoyé à la branche de fond (§7) ?
9. La distinction avec `contentieux-financier.md` et `controle-budgetaire.md`
   a-t-elle été maintenue, sans que le RETEX ne tranche à leur place ?
10. Couple **[risque / confiance]** (§11) indiqué selon le sous-cas ?

[risque / confiance] : risque variable selon le déclencheur (faible à élevé,
§11) — confiance stable sur la méthode ; vérification obligatoire dès que le
RETEX traverse un point de droit ou de procédure relevant d'une autre
branche.
