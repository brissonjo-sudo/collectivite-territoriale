# Branche — Dette & trésorerie (v1.0.0)

> Structure conforme à `_gabarit-branche.md`. Aucune valeur datée (taux,
> plafond, quotité, seuil prudentiel) n'est citée de mémoire : seules les
> **règles**, les **formules** et la consigne de vérifier la valeur en
> vigueur figurent ici.

## 1. Périmètre / Exclusions

**Périmètre** : compétence pour recourir à l'**emprunt** et sa délégation ;
nature de l'emprunt comme recette d'**investissement** ; typologie des
produits d'emprunt et lecture de la **charte de bonne conduite** (dite
charte Gissler) ; **consultation bancaire** et comparaison des offres ;
**gestion active de la dette** (renégociation, refinancement, remboursement
anticipé) et instruments de **couverture** ; **ligne de trésorerie** ;
**gestion de la trésorerie** au quotidien et obligation de dépôt des fonds
au Trésor ; annexes obligatoires relatives à la dette ; **garanties
d'emprunt** accordées à des tiers.

**Exclusions** :
- **Ratios d'endettement et capacité de désendettement** (lecture,
  méthode, seuils d'alerte) → `references/prospective-analyse.md`. Cette
  branche traite la **dette elle-même** (compétence, produits, gestion,
  trésorerie), pas sa lecture prospective.
- **Imputation comptable** des mouvements de dette et de trésorerie
  (comptes de tiers, chapitres, opérations d'ordre) → `references/nomenclature-m57.md`.
- **Procédure de contrôle budgétaire** en cas de déséquilibre lié à la
  dette → `references/controle-budgetaire.md`.
- **Contrôle interne** sur les flux de trésorerie et relations avec le
  comptable public → `references/controle-interne-financier.md`.

---

## 2. Questions couvertes

- Qui décide de recourir à l'emprunt, et jusqu'où l'exécutif peut-il agir
  seul par délégation ?
- Un emprunt peut-il financer une dépense de fonctionnement ?
- Comment qualifier un produit d'emprunt (taux fixe, variable, structuré) et
  le situer dans la classification de la charte Gissler ?
- Comment organiser une consultation bancaire et comparer des offres de
  façon homogène ?
- Dans quelles conditions renégocier, refinancer ou rembourser par
  anticipation un emprunt, et à quel coût ?
- Un contrat de couverture de taux est-il un acte autonome ou l'accessoire
  d'un emprunt ?
- Qu'est-ce qu'une ligne de trésorerie, en quoi diffère-t-elle d'un
  emprunt, et comment la mobiliser ?
- Quelles sont les règles de dépôt des fonds des collectivités et leurs
  dérogations ?
- Que doit contenir l'annexe « état de la dette » du budget ?
- Sous quelles conditions accorder une garantie d'emprunt à un tiers ?

---

## 3. Arbre de traitement

`question → variables à lever (§4) → décision → vérification (§7) →
écrit/livrable (§10)`

Ne jamais qualifier une opération de dette ou de trésorerie sans avoir levé
au préalable : la **nature exacte de l'opération** (emprunt nouveau, ligne
de trésorerie, renégociation, couverture, garantie), l'**autorité
compétente** pour la décider, et l'**imputation budgétaire** de principe
(recette d'investissement, opération de trésorerie hors budget, ou
engagement hors bilan pour une garantie). Si l'une de ces trois données
manque, la demander et marquer l'analyse `[INCOMPLET]` avant de conclure.

---

## 4. Variables à lever

- **Délégation consentie à l'exécutif** : nature, montant, durée. Sans
  délégation, l'exécutif ne peut agir seul.
- **Objet du financement** : dépense d'**investissement** confirmée ? Un
  doute sur la section impose la vérification avant tout engagement.
- **Nature du produit** : taux fixe, variable simple, indexé ou
  structuré ; niveau de risque au sens de la charte Gissler.
- **Encours de dette existant** : répartition par type de taux, durée
  résiduelle moyenne, prêteurs.
- **Ligne de trésorerie déjà ouverte** : plafond autorisé, taux
  d'utilisation.
- **Régime de dépôt des fonds** : droit commun (Trésor) ou dérogation
  identifiée (nature à confirmer).
- **Tiers bénéficiaire d'une garantie** : nature de l'organisme, objet du
  prêt garanti, quotité sollicitée, encours déjà garanti.
- **Instrument de couverture envisagé** : adossé à un emprunt existant ou
  autonome — distinction déterminante pour sa qualification.

---

## 5. Règles métier

### 5.1 Compétence pour recourir à l'emprunt

- Le recours à l'emprunt est, par principe, une compétence de
  l'**assemblée délibérante**, dans le cadre de l'autorisation budgétaire
  (inscription de la recette d'emprunt au budget).
- L'assemblée peut **déléguer** à l'exécutif tout ou partie des attributs de
  cette compétence (souscription et gestion de la dette), dans un cadre
  qu'elle fixe elle-même (CGCT, dispositions relatives aux délégations
  consenties à l'exécutif — à confirmer en version consolidée).
- Toute délégation doit être **encadrée** : nature des opérations
  déléguées, plafonds éventuels, types de produits autorisés (notamment
  exclusion ou encadrement des produits structurés les plus risqués).
  L'absence d'encadrement explicite est un point de vigilance à signaler,
  jamais à combler par supposition.
- **Compte rendu obligatoire** : l'exécutif rend compte à l'assemblée des
  décisions prises par délégation, selon une périodicité et des modalités
  à vérifier. L'absence de compte rendu ne rend pas la décision nulle par
  elle-même mais constitue un point de vigilance de contrôle interne
  (renvoi `references/controle-interne-financier.md`) et de régularité
  procédurale à signaler.
- Sans délégation régulière, toute décision de recourir à l'emprunt prise
  par le seul exécutif est **irrégulière** : orienter vers le garde-fou
  budgétaire (`SKILL.md` §5.3) si l'opération est déjà engagée.

### 5.2 L'emprunt, recette d'investissement non affectée

- L'emprunt est une **recette de la section d'investissement**. Il ne peut,
  par principe, financer une dépense de **fonctionnement**.
- L'emprunt est une ressource **non affectée** : il finance l'équilibre
  global de la section d'investissement, pas une dépense d'investissement
  nommément désignée, sauf mention contraire prévue par un texte
  spécifique (à vérifier au cas par cas).
- Toute présentation d'un emprunt comme finançant du fonctionnement, ou
  comme substitut à une recette de fonctionnement manquante, est un
  déclencheur du **garde-fou budgétaire** (`SKILL.md` §5.3) : signaler
  l'irrégularité avant toute autre recommandation.
- L'emprunt s'inscrit dans le respect de l'**équilibre réel du budget** :
  vérifier que le remboursement en capital de la dette (dépense
  d'investissement) est bien couvert par des recettes définitives, hors
  nouvel emprunt (règle de non-recours à l'emprunt pour rembourser du
  capital d'emprunt).

### 5.3 Typologie des produits et charte de bonne conduite

- **Taux fixe** : constant sur toute la durée, exposition nulle après
  souscription — produit le plus simple à piloter.
- **Taux variable simple** : indexé sur un indice usuel, sans effet de
  structure — exposition directe à la variation de l'indice.
- **Index complexe / produit structuré** : combinaison de composantes
  (barrières, effets de levier, formules multi-indices) — risque
  potentiellement sans plafond, complexité de valorisation.
- La **charte de bonne conduite** entre établissements bancaires et
  collectivités (dite **charte Gissler** — à confirmer en version
  consolidée) classe les produits en croisant le **risque d'indice** et le
  **risque de structure**, dans une grille à double entrée dont chaque
  case qualifie un niveau de risque croissant. **Lecture** : plus l'indice
  est complexe et plus la structure comporte de leviers, plus la case est
  risquée. Ne jamais qualifier un produit sans le **descriptif contractuel
  complet** (indice, formule, barrières, levier) : sans lui, l'analyse
  reste une esquisse conditionnelle.
- La charte est un engagement de place, pas un texte de loi : vérifier son
  statut exact avant toute conclusion juridique ferme.
- **Principe de prudence** : privilégier les catégories les moins risquées
  de la grille pour toute nouvelle souscription ; documenter tout écart
  dans l'acte de délégation ou la délibération.

### 5.4 Consultation bancaire et comparaison des offres

- Fixer, avant l'envoi des demandes de prix, un **cahier des charges
  homogène** : montant, durée, profil d'amortissement (linéaire,
  progressif, in fine), type de taux attendu, périodicité des échéances.
- Comparer les offres sur une base **strictement comparable** : le **taux
  effectif global** (TEG, qui intègre l'ensemble des frais et commissions
  obligatoires, pas le seul taux nominal), les **commissions**
  (engagement, non-utilisation, gestion) et leur mode de calcul, les
  **frais annexes** (garantie, dossier), les **clauses de remboursement
  anticipé** et leur coût potentiel (§5.5).
- Ne jamais comparer sur le seul taux nominal : deux offres identiques sur
  ce point peuvent avoir un coût global très différent une fois frais et
  commissions intégrés.
- Documenter la consultation (établissements sollicités, critères et motif
  du choix) pour la traçabilité, utile en contrôle interne ou en cas de
  question de l'assemblée.

### 5.5 Gestion active de la dette

- **Renégociation** : modification des conditions d'un emprunt existant
  avec le même prêteur (taux, durée, profil), sans changement de
  contrepartie.
- **Refinancement** : souscription d'un nouvel emprunt, éventuellement
  auprès d'un autre prêteur, servant à rembourser un ou plusieurs emprunts
  existants.
- **Remboursement anticipé** : remboursement total ou partiel d'un capital
  restant dû avant l'échéance contractuelle.
- Ces opérations peuvent donner lieu à une **indemnité compensatrice** due
  au prêteur, dont le principe de calcul (méthode actuarielle usuelle :
  différentiel entre le taux du contrat et un taux de marché de référence,
  appliqué au capital restant dû sur la durée résiduelle) doit être
  **vérifié dans le contrat lui-même**, jamais supposé.
- Comparer systématiquement le **coût total de l'opération** (indemnité +
  frais de la nouvelle opération) au **gain actualisé attendu** (économie
  d'intérêts sur la durée résiduelle) avant toute décision : un coût
  supérieur au gain n'est rationnel que si un objectif autre que financier
  est explicitement assumé (sécurisation du profil de risque, par ex.).
- Compétence : même régime que pour emprunter (§5.1) — assemblée ou
  exécutif par délégation expressément encadrée.

### 5.6 Instruments de couverture

- Un instrument de **couverture de taux** (échange de taux, plafonnement)
  a pour objet de modifier l'exposition au risque de taux d'un encours
  existant, sans changer le capital emprunté lui-même.
- Distinguer la couverture **adossée** à un emprunt identifié (qui en
  modifie le profil de risque) de tout produit qui s'apparenterait à une
  opération spéculative autonome, exclue pour une collectivité.
- L'encadrement de ces instruments suit la même logique de classification
  que les produits d'emprunt eux-mêmes (§5.3, charte Gissler) et la même
  exigence de compétence (§5.1).
- Ne jamais recommander un instrument de couverture sans en avoir fait
  vérifier la qualification exacte au regard des textes applicables aux
  contrats financiers des collectivités : point à vérification obligatoire
  (§7).

### 5.7 Ligne de trésorerie

- La **ligne de trésorerie** est une ouverture de crédit à court terme
  destinée à couvrir des besoins **temporaires**, jamais un besoin de
  financement durable.
- Elle se distingue de l'**emprunt** sur trois points : sa **finalité**
  (décalage temporaire, non un investissement durable), son
  **imputation** (opération de trésorerie retracée en comptabilité de
  tiers, détail renvoyé à `references/nomenclature-m57.md`) et sa
  **réversibilité** (tirages et remboursements multiples dans la limite
  d'un plafond, sans nouvel acte à chaque mouvement).
- La ligne est ouverte dans la limite d'un **plafond** fixé par la
  décision qui l'autorise (délibération ou exécutif par délégation), non
  dépassable sans nouvelle décision.
- **Mobilisation** : tirages et remboursements dans la limite du plafond,
  selon les modalités du contrat (préavis, montant minimal). Documenter
  chaque mouvement pour la traçabilité et le suivi du plan de trésorerie
  (§5.8).
- Une ligne utilisée pour financer un **besoin structurel** (déficit
  récurrent de fonctionnement) est un signal d'alerte : elle masque un
  déséquilibre et peut relever du garde-fou budgétaire (`SKILL.md` §5.3).

### 5.8 Gestion de la trésorerie au quotidien

- Principe de l'**obligation de dépôt des fonds** des collectivités
  auprès du Trésor (unité de caisse de l'État) : la collectivité ne place
  pas librement ses excédents sur le marché bancaire ordinaire, sauf
  **dérogation** prévue par un texte. Le périmètre exact de ces
  dérogations est **à vérifier avant toute conclusion**, jamais énoncé de
  mémoire.
- Le **plan de trésorerie** projette, sur un horizon court (infra-annuel),
  les encaissements et décaissements attendus, pour anticiper les besoins
  de tirage et éviter tout décalage non couvert.
- **Méthode de construction** :
  1. Recenser les flux **certains et datés** (échéances de dette,
     dotations connues, paie, gros marchés).
  2. Estimer les flux **probables** (recouvrement fiscal, calendrier de
     mandatement).
  3. Positionner chaque flux sur l'échéancier (semaine ou décade).
  4. Identifier les **points bas** prévisionnels et déterminer le tirage
     nécessaire, dans la limite du plafond ouvert.
  5. Réviser le plan à échéance régulière au vu des réalisations.
- **Tirages et remboursements** : documenter chaque tirage (motif, montant,
  échéance de remboursement) et rapprocher régulièrement l'encours mobilisé
  du plan actualisé.
- Une gestion de trésorerie qui recourt à un encaissement ou un
  décaissement hors du circuit du comptable public pour gagner du temps
  déclenche immédiatement le garde-fou ordonnateur/comptable
  (`SKILL.md` §5.2).

### 5.9 Garanties d'emprunt accordées à des tiers

- La collectivité peut, sous conditions, **garantir** l'emprunt souscrit
  par un tiers (bailleur social, organisme, association selon les cas), en
  s'engageant à se substituer à lui en cas de défaillance.
- **Compétence** : délibération de l'**assemblée délibérante**. Elle ne se
  délègue pas dans les mêmes conditions qu'une opération de dette propre :
  vérifier le régime exact et l'éventuelle interdiction de délégation.
- **Ratios prudentiels** : l'octroi est encadré par des règles de
  plafonnement du **risque hors bilan** cumulé, exprimées usuellement par
  un ratio `encours garanti (ou annuité garantie) / recettes réelles de
  fonctionnement` et par une règle de **division du risque** entre
  bénéficiaires (aucune contrepartie ne doit en concentrer une part
  excessive). **Ne jamais citer le seuil chiffré de mémoire** : poser la
  formule et renvoyer à la vérification de la valeur en vigueur.
- **Risque** : engagement **hors bilan** qui ne pèse sur le budget qu'en
  cas d'appel, mais à suivre comme un risque financier à part entière et à
  faire figurer dans l'état récapitulatif (§10) et la lecture prospective
  (`references/prospective-analyse.md`).
- Avant tout octroi, vérifier la **capacité de remboursement** du
  bénéficiaire, sans se substituer à l'analyse de solvabilité du prêteur.

---

## 6. Calculs et procédures

1. **TEG** — actualisation de l'ensemble des flux du prêt (capital versé,
   échéances, commissions et frais obligatoires) au taux qui les égalise ;
   ne jamais comparer sur le seul taux nominal (§5.4).
2. **Coût d'une gestion active** — `coût total = indemnité de
   remboursement anticipé + frais de la nouvelle opération` à comparer au
   `gain = économie d'intérêts actualisée sur la durée résiduelle`.
3. **Plan de trésorerie** — méthode en cinq étapes (§5.8) ; toute donnée
   manquante se signale, ne se comble jamais par estimation silencieuse.
4. **Ratio prudentiel de garantie** — `encours garanti (ou annuité
   garantie) / recettes réelles de fonctionnement`, plus la règle de
   division du risque par bénéficiaire ; jamais de seuil chiffré non
   vérifié (§7, §9).
5. **Suivi de l'encours de dette** — pour chaque emprunt : capital restant
   dû, taux, durée résiduelle, prêteur, classification (charte Gissler),
   pour alimenter l'annexe budgétaire et `references/prospective-analyse.md`.
6. **Tirage sur ligne de trésorerie** — vérifier préavis contractuel et
   montant minimal, exécuter dans la limite du plafond, tracer chaque
   mouvement.

---

## 7. Déclencheurs de vérification

Appliquer le socle-sources (matrice §2.2 du `SKILL.md`) dès que :
- la **compétence** exacte de délégation en matière d'emprunt ou de
  garantie est en cause ;
- un **plafond**, une **quotité** ou un **ratio prudentiel** de garantie
  d'emprunt est cité ;
- le **plafond** d'une ligne de trésorerie ou ses conditions de
  mobilisation conditionnent une décision ;
- une **dérogation** à l'obligation de dépôt des fonds au Trésor est
  invoquée ;
- la **classification** exacte d'un produit dans la grille de la charte
  Gissler est disputée ou sert de fondement à une décision de souscription ;
- un **délai** (compte rendu de délégation, transmission au contrôle de
  légalité d'une délibération de garantie) conditionne la régularité de
  l'acte ;
- une **indemnité de remboursement anticipé** est calculée pour servir de
  base à une décision.

---

## 8. Pièges & confusions fréquentes

1. Confondre **ligne de trésorerie** et **emprunt** : la première ne
   finance pas un investissement durable et ne relève pas du même régime
   d'imputation.
2. Présenter un emprunt comme finançant une dépense de **fonctionnement** :
   garde-fou budgétaire immédiat (§5.2).
3. Comparer des offres bancaires sur le seul **taux nominal**, en ignorant
   commissions, frais et TEG (§5.4).
4. Qualifier un produit structuré dans la grille de la charte Gissler sans
   disposer du **descriptif contractuel complet** de la formule
   d'indexation.
5. Décider d'une opération de gestion active sans avoir chiffré
   **l'indemnité compensatrice**, ou en la supposant nulle par défaut.
6. Accorder une garantie d'emprunt sans vérifier le **ratio prudentiel**
   applicable et la **division du risque** entre bénéficiaires.
7. Omettre le **compte rendu à l'assemblée** des décisions de dette prises
   par délégation.
8. Utiliser durablement une ligne de trésorerie pour couvrir un déficit
   structurel plutôt qu'un besoin ponctuel : signal de déséquilibre à
   traiter comme tel (renvoi §5.7 et `references/controle-budgetaire.md`).
9. Recourir à un encaissement ou un décaissement hors du circuit du
   comptable pour lisser une tension de trésorerie : gestion de fait
   (`SKILL.md` §5.2).
10. Oublier l'annexe **état de la dette** ou la produire incomplète (encours
    par type de produit, garanties données non recensées).

---

## 9. Données / valeurs à vérifier

- **Jamais de mémoire** : taux d'intérêt proposés ou légaux, TEG d'une
  offre, commissions et frais, plafond d'une ligne de trésorerie, quotité
  et ratios prudentiels de garantie, liste exacte des dérogations au dépôt
  des fonds au Trésor, délai de compte rendu des décisions par délégation,
  délai de transmission au contrôle de légalité d'une délibération de
  garantie.
- **Références structurelles stables, citables avec la réserve « à
  confirmer en version consolidée »** : le **CGCT** (compétence d'emprunt,
  délégation, garanties) ; le **décret relatif à la gestion budgétaire et
  comptable publique** (décret GBCP, déjà nommé au `SKILL.md`) ; la
  **charte de bonne conduite entre les établissements bancaires et les
  collectivités locales** (charte Gissler), pour son nom et l'architecture
  de sa grille ; le principe de l'**obligation de dépôt des fonds au
  Trésor**, dont le périmètre exact des dérogations reste à confirmer.
- **Aucun numéro d'article, identifiant Légifrance (LEGIARTI/JORFTEXT/NOR)
  ni valeur chiffrée** n'est avancé sans vérification préalable dans la
  session : à défaut, s'en tenir à la règle et signaler le point à
  vérifier.

---

## 10. Écrits & livrables

| Écrit | Nature | Compétence | Générateur / renvoi |
|---|---|---|---|
| Délibération autorisant le recours à l'emprunt, ou déléguant cette compétence | Acte décisionnel | Assemblée délibérante | `references/templates/deliberation-budgetaire.md` |
| Délibération de garantie d'emprunt | Acte décisionnel, acte faisant grief potentiel | Assemblée délibérante | `references/templates/deliberation-budgetaire.md` ; passer par `references/controle-budgetaire.md` avant production |
| Contrat de prêt / avenant de renégociation | Acte conventionnel signé par l'exécutif (dans le cadre de sa délégation ou d'une autorisation spécifique) | Exécutif (délégation vérifiée) | Hors générateurs couche 4 ; pièce annexée au dossier de délibération |
| Convention de garantie avec l'organisme bénéficiaire | Écrit conventionnel | Exécutif, sur habilitation de la délibération | `references/templates/convention-subvention.md` non adapté ; convention spécifique, cf. `references/ecrits-financiers.md` §10 |
| Note d'impact financier sur une opération de dette (nouvel emprunt, gestion active, garantie) | Écrit de pilotage | DirFi | `references/templates/note-impact-financier.md` |
| Fiche de procédure interne (plan de trésorerie, tirage sur ligne, suivi de l'encours garanti) | Écrit de procédure | DirFi | `references/templates/fiche-procedure-financiere.md` |
| État de la dette (annexe budgétaire) et état des garanties d'emprunt | Annexe obligatoire | Services financiers | Contenu détaillé renvoyé à `references/nomenclature-m57.md` pour l'imputation ; forme renvoyée à `references/ecrits-financiers.md` |

Objet métier associé : `../objets/emprunt.md` (situation type, acteurs,
procédures détaillées, sans duplication du fond ici). Il couvre aussi la
**garantie d'emprunt** accordée à un tiers. La **ligne de trésorerie** n'a pas
d'objet dédié en v1.0.0 : son régime est traité ici, en §5.

---

## 11. Double échelle [risque / confiance]

| Sous-domaine | Risque | Confiance | Repère |
|---|---|---|---|
| Distinction emprunt / ligne de trésorerie | Moyen | Stable | Réponse directe, rappel de la règle |
| Interdiction de financer du fonctionnement par l'emprunt | Élevé | Stable | Garde-fou budgétaire si franchi (§5.2 SKILL) |
| Classification d'un produit (charte Gissler) | Élevé | À vérifier selon le descriptif contractuel | Citation + réserve, jamais de qualification sans descriptif complet |
| Comparaison d'offres bancaires (TEG, commissions) | Moyen | Stable sur la méthode | Vérification ponctuelle des chiffres transmis par les banques |
| Gestion active (renégociation, remboursement anticipé) | Élevé | À vérifier (indemnité contractuelle) | Chiffrage obligatoire avant décision |
| Plafond et mobilisation de la ligne de trésorerie | Élevé | Stable sur le principe, à vérifier sur le plafond retenu | Citation du plafond en vigueur obligatoire |
| Garantie d'emprunt à un tiers | Critique | À vérifier systématiquement | Citation du ratio prudentiel + vérification de la division du risque |
| Dépôt des fonds au Trésor et dérogations | Élevé | À vérifier | Abstention si dérogation invoquée sans confirmation |

---

## 12. Checklist de branche

1. **Compétence** vérifiée : assemblée délibérante ou exécutif par
   délégation régulière et encadrée, pour l'opération concernée ?
2. Emprunt bien qualifié comme **recette d'investissement non affectée**,
   jamais présenté comme finançant du fonctionnement ? Sinon, garde-fou
   budgétaire (§5.2 SKILL) affiché avant tout contenu.
3. **Classification du produit** (charte Gissler) posée seulement si le
   descriptif contractuel complet est connu, sinon signalée comme à
   compléter ?
4. Comparaison d'offres bancaires effectuée sur **TEG, commissions et
   frais**, pas sur le seul taux nominal ?
5. Opération de gestion active chiffrée (**indemnité vs gain actualisé**)
   avant toute recommandation ?
6. **Ligne de trésorerie** distinguée de l'emprunt, plafond et modalités de
   mobilisation identifiés, usage non structurel vérifié ?
7. **Dépôt des fonds au Trésor** : dérogation éventuelle signalée comme à
   vérifier, jamais affirmée de mémoire ?
8. **Garantie d'emprunt** : compétence de l'assemblée, ratio prudentiel et
   division du risque vérifiés avant tout octroi ?
9. Un maniement de fonds hors circuit du comptable public a-t-il été
   identifié ? Si oui, **STOP** (`SKILL.md` §5.2) affiché en premier.
10. **Annexe état de la dette** et état des garanties évoqués si l'écrit
    produit est un acte budgétaire ?
11. Toute référence citée porte-t-elle sa provenance ou la réserve « à
    confirmer en version consolidée » (§9) ?
12. Couple **[risque / confiance]** (§11) indiqué quand utile à la
    décision ?
