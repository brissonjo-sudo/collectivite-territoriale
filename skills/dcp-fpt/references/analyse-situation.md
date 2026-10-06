# Analyse de situation — routeur commande publique

## Séquence imposée

1. Repérer les déclencheurs et afficher les STOP de `SKILL.md` §5.2/§5.3
   **avant** tout questionnaire, écrit ou conseil métier.
2. Détecter les frontières : BASCULE nommée puis arrêt du volet concerné ;
   concession ou délégation de service public : arrêt de la demande.
3. Lever le mode d'exercice (intégré, mutualisé, groupement de commandes,
   centrale d'achat, assistance externe), la catégorie d'acheteur et les
   responsabilités prévues par convention ou délégation.
4. Qualifier travaux/fournitures/services, procédure adaptée/formalisée,
   stade, date de lancement et enjeu. Demander seulement les données
   anonymisées qui modifient la décision. Ne jamais réclamer une offre réelle.
5. Lire la branche principale ; les compléments portent uniquement sur le
   point de jonction. Charger l'objet pour une situation qui traverse le cycle.
6. Lire le socle et les lignes du registre pertinentes : champ, version,
   statut, réserve. Une valeur nécessite une source officielle en session.
7. Produire méthode, option conditionnelle, autorité, contrôle et écrit ;
   préciser ce qui reste non conclu. Nommer les chemins effectivement utilisés.
8. Appliquer l'auto-vérification de `SKILL.md` §7.

## Signaux → branche

| Signal | Point d'entrée | Complément si nécessaire |
|---|---|---|
| Fournitures homogènes, opération de travaux, sourcing, lots | `references/besoin-strategie-achat.md` | `references/procedures.md` après estimation |
| Petit achat, appel d'offres, urgence, négociation comme procédure | `references/procedures.md` | `references/techniques-achat.md` pour le montage |
| Avis, dossier, question candidat, modification avant remise | `references/publicite-consultation.md` | `references/candidatures-offres.md` pour les critères |
| Pièce absente, capacité, exclusion, offre basse, classement | `references/candidatures-offres.md` | `references/ecrits-commande-publique.md` |
| Commission, candidat rejeté, signature, notification | `references/attribution-signature.md` | `references/contentieux.md` si recours |
| Accord-cadre, bons, centrale, groupement, marché réservé/global | `references/techniques-achat.md` | `references/procedures.md` |
| Ordre de service, sous-traitant, réception, cession | `references/execution-juridique.md` | `references/modifications.md` si changement |
| Avenant, prestations ajoutées, changement de titulaire | `references/modifications.md` | `references/ecrits-commande-publique.md` |
| Abandon, mise en demeure, imprévision, force majeure | `references/resiliation-difficultes.md` | `references/contentieux.md` |
| Saisine du juge, recours tiers/parties, amiable | `references/contentieux.md` | branche du stade contesté |
| Rédige, prépare une lettre, un rapport ou une décision | `references/ecrits-commande-publique.md` | branche de fond **avant** le gabarit |
| Infructuosité, erreur à capitaliser, retour d'expérience | `references/retex.md` | branche ayant porté la décision |

## Frontières

Reprendre les blocs de `SKILL.md` §5.5 : finance → `dirfi-fpt` ; contenu
informatique → `dsi-fpt` ; données personnelles → `dpo-ct` ; agent → `drh-fpt` ;
besoin opérationnel PM → `dpm-fpt` ; vigueur et portée → `recherche-juridique`.
Ne pas transformer la disponibilité d'un autre skill en autorisation de
traiter sa matière. Une frontière ne s'illustre pas.

## Objets → parcours

| Situation | Objet |
|---|---|
| Travaux, du besoin à la réception | `objets/marche-travaux.md` |
| Renouvellement d'un service récurrent | `objets/marche-services-recurrent.md` |
| Achat annoncé « sous seuil » | `objets/achat-sous-seuil.md` |
| Montage et exécution à bons de commande | `objets/accord-cadre.md` |
| Contestation d'un candidat évincé | `objets/candidat-evince.md` |
| Défaillance en exécution | `objets/titulaire-defaillant.md` |

## Écrits

La branche `references/ecrits-commande-publique.md` choisit le gabarit et
organise les champs manquants. Une lettre de rejet dépend du stade et du
régime ; un projet d'avenant dépend d'un fondement vérifié ; une mise en
demeure dépend des pièces contractuelles. Un écrit ne régularise pas un choix
illégal ni une compétence absente. Produire [INCOMPLET] si nécessaire.

## Pièges de routage

- « Sous seuil » n'établit ni la valeur du besoin ni une dispense.
- Une centrale, un groupement ou un marché global n'est pas une procédure.
- L'agrément juridique des conditions de paiement du sous-traitant ne permet
  pas de traiter son paiement : `dirfi-fpt`.
- Une modification de prix se qualifie juridiquement ici ; son calcul ne se
  traite pas ici. Un niveau de service informatique relève de `dsi-fpt`.
- Une urgence d'organisation n'établit pas une urgence de droit.
- Une fiche doctrinale, un texte propre à l'État ou une décision concernant
  une concession ne démontre pas une obligation d'un marché de collectivité.
- Aucun traitement pénal ou disciplinaire par la branche contentieux ;
  appliquer les frontières et conserver le STOP pertinent.
