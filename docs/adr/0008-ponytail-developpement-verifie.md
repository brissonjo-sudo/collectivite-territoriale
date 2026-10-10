# ADR 0008 — Ponytail local avec vérification avant utilisation

Date : 2026-10-10. Statut : accepté, demande explicite de l'auteur.

Ponytail est installé comme outil de développement propre au dépôt dans
`.agents/skills/ponytail/`. Il n'est pas ajouté aux six skills distribués
du plugin, à `upstream.json`, aux manifestes ou aux marketplaces.

La source officielle est `DietrichGebert/ponytail`, release stable 5.1.0,
commit `9cc65d03aa2da1db7121b912d03596409ee340b8`. Les règles amont et leur
licence MIT sont conservées avec leurs empreintes. Le point d'entrée local
impose la vérification ; les règles amont ne sont pas chargées auparavant.

« À jour » signifie identique à la dernière release stable publiée, selon
`GET /repos/DietrichGebert/ponytail/releases/latest`, avec résolution de
l'étiquette jusqu'au commit exact. Les changements non publiés de `main`
ne constituent pas une nouvelle release. La documentation GitHub est utilisée
après indisponibilité de Context7 (quota mensuel atteint).

Chaque utilisation déclenche de nouvelles lectures publiques GitHub, sans
token, sans cache positif et avec un délai borné. Version différente, étiquette
déplacée, fichier altéré, réseau indisponible, quota/API en erreur ou réponse
incomplète : code de sortie 1 et aucune règle affichée. Les règles de session
persistante amont ne dispensent pas d'un nouveau contrôle à chaque tour.

Le contrôle protège le chemin d'entrée prévu ; son respect par l'assistant
est imposé par `AGENTS.md`. Ce n'est pas une restriction système empêchant un
lecteur de fichiers de contourner les consignes. Aucun hook global ni service
de surveillance n'est installé. La mise à jour requiert de revoir la nouvelle
release, remplacer les règles et la licence, réviser le verrou et les tests.

La distribution open source 1.2.0 et ses preuves restent inchangées. Cette
installation ne vaut pas qualification d'une nouvelle version du plugin.

Vérification du 2026-10-10 : release 5.1.0 confirmée par le contrôle réel,
point d'entrée validé par `quick_validate.py`, dix tests ciblés réussis et
82 tests du dépôt réussis. Ce constat daté n'est pas un cache d'autorisation.

Sources : [releases GitHub](https://docs.github.com/en/rest/releases/releases#get-the-latest-release),
[références Git](https://docs.github.com/en/rest/git/refs#get-a-reference),
[tags annotés](https://docs.github.com/en/rest/git/tags#get-a-tag).
