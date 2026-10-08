# Setup autorisé : verrou du runtime Windows

La reprise manuelle du 8 octobre à 15:06 UTC a franchi l'UAC. Le journal
confirme la fin du provisionnement et 12 filtres WFP installés. Le contrôle
suivant échoue sur `node_repl.exe`, avec `os error 32` (fichier utilisé par
un autre processus), puis `helper_unknown_error: setup refresh had errors`.
Le setup complet reste en échec et l'API signale `notConfigured`.

Des effets système ont donc eu lieu malgré `success=false`. Les octets de
configuration et les 214 fichiers du cache dev.6 restent inchangés ; aucun
audit complet des effets système n'est prétendu. Huit processus utilisent le
runtime concerné. Le détenteur exact du verrou n'est pas établi. Aucun
processus n'a été arrêté et aucun secret lu ou copié.

`outillage/reprendre-sandbox-hors-codex.ps1` vérifie ces processus avant
toute reprise officielle. Fermer Codex complètement et conserver un terminal
PowerShell indépendant ouvert, puis invoquer le lanceur depuis ce terminal.
Il refuse la reprise si le runtime est encore utilisé ou si l'inspection
échoue. Il ne ferme pas l'application, ne contourne aucune protection et
ne lance pas de modèle. Une absence de processus ne garantit pas la réussite
du setup : seuls les nouveaux reçus et la lecture synthétique le confirmeront.

La syntaxe est vérifiée sous PowerShell 7 et Windows PowerShell 5.1. Le
précontrôle a effectivement refusé le setup avec les huit processus actifs.
Les quatre scripts sont fournis ensemble. Le lanceur prêt à utiliser se
trouve également à la racine de la session.

Dev.7 reste non mesuré. Aucun nouveau résultat de coactivation n'est ajouté,
la présentation v8 et les preuves historiques restent conservées. Les trois
cas sans sources attendent une lecture opérationnelle ; les treize autres
restent bloqués au précontrôle avec web/MCP désactivés. Publication non prête.

Documentation : [sandbox Windows](https://learn.chatgpt.com/docs/windows/windows-sandbox)
et [API App Server](https://learn.chatgpt.com/docs/app-server).
