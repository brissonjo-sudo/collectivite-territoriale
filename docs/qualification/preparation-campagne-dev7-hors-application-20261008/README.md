# Préparation dev.7 pour trois tentatives hors application

Le setup officiel et une lecture synthétique readOnly ont réussi le 8 octobre
à 17:33 UTC lorsque Codex était fermé. Le reçu readiness reste `notConfigured` ;
ce statut contradictoire n'est pas présenté comme une qualification. La preuve
opérationnelle est le résultat réel de lecture, exitCode 0, sentinelle et SHA
DSI exacts. Après réouverture de Codex, une nouvelle lecture sans modèle échoue
avec `helper_unknown_error: setup refresh had errors`. Le runtime actif retrouve
le verrou déjà observé. Aucun nouveau modèle n'est lancé pour contourner cet échec.

Le harnais a été corrigé avant toute inférence : résolution des alias `rN` du
catalogue et clés CLI sans guillemets littéraux dans les identifiants de plugins.
L'API config/read atteste les véritables clés : anciens dev.6/dev.7 désactivés,
nouveau candidat r3 actif, trois MCP locaux désactivés, web désactivé et sandbox
Windows elevated en lecture seule. Les préparations r1/r2 refusées restent locales,
sans tentative modèle ni remplacement de preuve. Les 32 fixtures passent.

La préparation r3 installe officiellement 214 blobs du commit dev.7 figé, dont
213 gelés et 166 runtime. Le cache dev.6 reste intact. Les évolutions de config
ont été effectuées par l'installation officielle et config/batchWrite dans le
seul profil isolé ; aucun secret lu ou copié. Catalogue, protocole, questions,
oracles, outils et reçus sont gelés avant les modèles. L'observation globale
des outils reste imparfaitement isolée ; aucune exposition MCP globale complète
n'est prétendue. Le catalogue ne prouve pas une activation de skill.

Le lanceur hors application attend un terminal indépendant et la fermeture
complète de Codex. Il refuse un runtime actif, un chemin inaccessible, un manifest
divergent ou une tentative existante. Une nouvelle lecture réelle sans modèle,
avec permissions effectives contrôlées, précède trois appels distincts séquentiels,
tentative unique de 240 secondes chacun, suivis de leurs exports. Aucun setup,
nouvelle authentification, override de modèle, jugement ou reprise automatique.
Le plafond total est de 15 minutes. Après la fin du terminal, les paquets pourront
être jugés par des sous-agents nouveaux sans contexte parent. Les autres treize cas
exigent des sources primaires et restent bloqués au précontrôle ; la suite conserve
16 cas et 124 atomes. Les trois tentatives ne valent pas campagne complète.

À cet instant : zéro répondant et zéro juge dev.7. Aucun score ancien transféré.
La présentation v8 et les anciennes preuves restent conservées, publication non prête.
Les scripts fournis dans outillage sont des copies documentaires ; les lanceurs
prêts à exécuter sont à la racine de la session avec les mêmes voisins Python.

Documentation officielle : [App Server](https://learn.chatgpt.com/docs/app-server).
