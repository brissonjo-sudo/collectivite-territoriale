# Politique de confidentialité — Collectivité territoriale

Dernière mise à jour : 7 octobre 2026

## Responsable et contact

Le plugin **Collectivité territoriale** est édité par le mainteneur du dépôt
public [`brissonjo-sudo/collectivite-territoriale`](https://github.com/brissonjo-sudo/collectivite-territoriale).

Pour toute question relative à la confidentialité, utiliser la
[page de support du dépôt](https://github.com/brissonjo-sudo/collectivite-territoriale/issues)
en demandant, si nécessaire, un canal privé. Ne jamais publier de donnée
personnelle, de secret ou de pièce confidentielle dans une issue publique.

## Objet et périmètre

Le plugin fournit cinq skills d'aide à la décision pour les collectivités
territoriales et un accès optionnel au serveur MCP `droit-francais`. Les skills
sont des fichiers statiques exécutés par le client de l'utilisateur. Ils
n'exploitent aucune base de données propre et n'ajoutent aucune télémétrie.

Le client utilisé, notamment ChatGPT, Codex, Claude Code ou Mistral Vibe, peut traiter et
conserver la conversation selon les paramètres, la politique et les conditions
du compte de l'utilisateur. Ces traitements sont distincts de ceux du présent
plugin.

L'adaptation Vibe génère un profil local dédié et peut enregistrer, à la
demande de l'utilisateur, des preuves d'essai assainies : paramètres du test,
empreintes, noms d'outils, état des appels et réponse produite. Ces preuves
doivent être revues avant tout versement au dépôt public. Le profil généré
désactive la télémétrie et la persistance des conversations Vibe ; cela ne
détermine pas la conservation côté fournisseur du modèle. Il ne copie aucun
secret ni fichier `.env` et ne modifie pas les réglages du profil habituel.

## Données traitées

Lorsque seuls les skills locaux sont utilisés, le dépôt du plugin ne reçoit ni
ne conserve la question, les documents ou la réponse de l'utilisateur.

Lorsque le serveur MCP `droit-francais` est activé et appelé, il peut recevoir :

- la requête juridique, les filtres et les identifiants de sources nécessaires
  à la recherche demandée ;
- les textes et métadonnées publics retournés par Légifrance ou Judilibre ;
- les métadonnées techniques nécessaires aux échanges HTTPS et MCP ;
- le jeton OAuth présenté à l'appel et l'identifiant de sujet nécessaire à
  l'authentification et à la prévention des abus.

L'utilisateur ne doit transmettre que les informations strictement nécessaires
et doit éviter les noms, coordonnées, pièces confidentielles et autres données
personnelles lorsque la recherche peut être formulée sans elles.

## Finalités

Les données sont traitées pour :

- exécuter la recherche juridique demandée et restituer les sources officielles ;
- authentifier les accès au serveur MCP ;
- assurer la sécurité, la disponibilité, le diagnostic et la prévention des abus.

Le mainteneur n'utilise pas les requêtes pour la publicité, le profilage ou
l'entraînement d'un modèle.

## Destinataires et prestataires

Selon les fonctionnalités utilisées, les données nécessaires peuvent être
traitées par :

- le fournisseur du client conversationnel choisi par l'utilisateur ;
- Auth0/Okta pour l'authentification du serveur MCP ;
- Render Services, Inc. pour l'hébergement du serveur MCP ;
- PISTE/DILA pour Légifrance ;
- PISTE et la Cour de cassation pour Judilibre.

Les clés PISTE restent côté serveur. Elles ne sont ni demandées à l'utilisateur
ni incluses dans les réponses.

## Conservation

Le plugin statique ne possède aucun stockage propre et ne conserve aucune
requête. Le serveur MCP ne conserve pas les requêtes ou les résultats dans une
base de données. Son journal métier peut conserver le nom de l'opération,
l'état, la durée et, pour un appel réussi, une empreinte pseudonymisée du sujet
authentifié ; il exclut les arguments, résultats, identifiants bruts, jetons et
secrets.

À la date de la présente politique, les journaux de l'hébergeur Render sont
conservés sept jours pour l'espace utilisé. Les fournisseurs du client et de
l'authentification peuvent conserver séparément leurs propres journaux selon
leurs politiques et les paramètres du compte de l'utilisateur.

La politique détaillée et tenue à jour du serveur MCP est disponible dans le
dépôt [`droit-francais-skill`](https://github.com/brissonjo-sudo/droit-francais-skill/blob/main/docs/privacy-policy.md).

## Choix et droits des utilisateurs

L'utilisateur peut désactiver le serveur MCP et continuer à utiliser les skills
en mode dégradé. Dans ce cas, le plugin doit signaler qu'une référence ou sa
vigueur n'a pas pu être vérifiée et ne doit pas inventer de source.

Lorsque le RGPD ou la loi Informatique et Libertés s'applique, une personne peut
demander l'accès, la rectification, l'effacement ou la limitation de ses
données et, selon la base juridique, s'opposer au traitement. Elle peut aussi
saisir la [CNIL](https://www.cnil.fr/). Une demande portant sur le compte, la
conversation ou l'authentification peut devoir être adressée directement au
fournisseur concerné.

## Sécurité et mises à jour

Les échanges avec le serveur MCP utilisent HTTPS. Les secrets d'accès restent
dans l'environnement du serveur et ne sont pas distribués avec le plugin.

Cette politique peut évoluer si le fonctionnement, les prestataires ou les
durées de conservation changent. Sa date de mise à jour est indiquée en tête du
document.
