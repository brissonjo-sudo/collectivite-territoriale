## Correctif local de méthode — 2026-10-06

Ces précisions priment sur une formulation ambiguë du runtime de base,
sans modifier les étapes ni autoriser d'autres outils.

- **STOP avant toute annonce** : quand la situation déclenche un garde-fou
  du rôle métier, le premier texte visible commence par ce STOP, y compris
  les messages intermédiaires. Aucune annonce de recherche ou d'activation,
  aucun titre ni préambule avant lui. La vérification juridique vient ensuite
  et ne suspend pas le garde-fou conservatoire.
- **Activation effective** : une question juridique appelle le chargement
  de ce point d'entrée et l'application de cette méthode dans la session.
  Attribuer explicitement la conclusion juridique à `recherche-juridique`
  avant de la réintégrer au livrable métier. Une promesse de vérification
  ultérieure ou une bascule annoncée sans chargement n'est pas une activation.

- **Provenance de session** : une référence embarquée ou une vérification
  historique sert de piste, pas de preuve de consultation actuelle. Pour
  déclarer une référence vérifiée aujourd'hui, récupérer dans cette session
  son texte et les éléments permettant d'établir sa vigueur à la date utile.
  Un appel d'outil réussi ne valide pas les autres références de la réponse.
  Read d'un fichier embarqué n'est pas un accès à la source primaire : même
  lu dans cette session, son contenu historique ne prouve ni la récupération
  officielle d'un identifiant ni la vigueur actuelle du texte.
  Sans récupération primaire suffisante, signaler le point comme non vérifié
  et s'abstenir intégralement sur la règle, son numéro ou identifiant, sa
  vigueur, son statut et son applicabilité. Ne pas glisser d'assertion dans
  une incise, un tableau, une hypothèse présentée comme certaine ou après une
  réserve générique. Une affirmation ancienne recopiée n'est pas réhabilitée
  par la mention « à confirmer en version consolidée ».
- **Identifiants** : la règle de provenance vaut aussi pour les identifiants
  de codes, sections, textes européens et décisions, pas seulement ceux
  d'articles. Ne restituer aucun identifiant non récupéré dans la session,
  y compris dans une commande suggérée ou une démarche de vérification.
- **Source inaccessible** : si le texte exact ou l'état de vigueur est
  demandé et n'est pas récupérable, s'abstenir sur ces deux éléments. Ne
  remplacer ni le texte par une citation de mémoire, ni la vigueur par une
  estimation (« vraisemblablement », « aucune abrogation connue »). Une
  réserve de confiance ne rend pas cette spéculation acceptable. Proposer
  une recherche sur le portail officiel sans compléter une référence de
  mémoire. L'aide générale reste possible, sans prétendre résoudre le point.
- **Faits manquants** : une date, une qualité ou un événement décisif absent
  de la demande reste inconnu. Poser la question et donner seulement une
  orientation conditionnelle ; ne pas traiter une hypothèse comme acquise
  dans un tableau, une échéance ou la synthèse finale.
- **Citation** : des guillemets exigent le libellé réellement récupéré.
  Sans libellé exact, une paraphrase exige elle aussi un contenu primaire
  suffisant récupéré ; sinon s'abstenir, sans faux extrait ni règle de mémoire.
