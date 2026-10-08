# Qualification actuelle : candidat dev.7 non mesuré

Le correctif dev.7 précise que le STOP constitue le premier commentaire de
progression avant outils. Source committée `fb186b4951b95adabf05904f8a34995720588be3`,
213 fichiers figés dont 166 runtime. Seul le SKILL DSI change dans le runtime.
Cette correction reste une hypothèse. Aucun résultat dev.6, dev.5 ou DSI
autonome n'est transféré. `release_ready=false`, `runs=[]`.

Le smoke CLI **dev.6** du 8 octobre exécute quatre sessions fraîches authentifiées,
avec Codex `0.162.0-alpha.2` et modèle observé `gpt-6.1-sol` : un usage DSI
vérifié, deux cas partiels et un bloqué. Trois invocations explicites injectent
les instructions DSI complètes. La réouverture explicite émet STOP comme premier
message visible. DPO, DirFi et recherche-juridique ne sont ni injectés ni lus
avec succès. Neuf appels custom existent dans les rollouts ; cinq résultats
signalent « blocked by policy ». Le stdout JSONL seul omet ces appels.

La découverte globale reste imparfaitement isolée ; la désactivation configurée
du MCP ne prouve pas l'absence d'exposition de connecteurs. Les rollouts bruts,
contextes développeur, inventaires complets d'outils, stderr et identifiants
restent locaux. Les extraits publics conservent les lignes, empreintes et
attestations d'injection. La cause du refus avant PowerShell demeure probable :
backend Windows non configuré. Aucun bypass n'a été demandé. Une demande d'aide au CLI a déclenché un helper de sandbox, qui a échoué ; aucune installation système réussie n'est attestée et les changements système n'ont pas été audités.

Le prochain contrôle demande un sandbox de lecture opérationnel, puis une
campagne nouvelle sur dev.7. Les avis DSI/RSSI et juridiques humains restent
ouverts. Le STOP correct de ce smoke ne répare pas l'échec du pilote historique.

[Jugement du smoke dev.6](../../tests/evidence/smoke-cli-dev6-20261008/jugement.md)
et [critères](../../tests/evidence/smoke-cli-dev6-20261008/jugement.json).
[Bilan du pilote dev.6 historique](README-dev6-partiel-historique.md).
