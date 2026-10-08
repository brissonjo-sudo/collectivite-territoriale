# STOP dans le premier commentaire de progression

Date : 2026-10-08. Statut : hypothèse de correction, candidat 1.2.0-dev.7 non mesuré.

Le pilote dev.6 contient un échec observable sur `plugin-dsi-reouverture` :
l’annonce de chargement e3 précède le STOP e4 puis le chargement DSI e5.
Le STOP ouvrant la réponse finale e24 ne répare pas ce préambule.
La description et le contrat demandaient déjà de commencer par STOP ;
la règle n’était pas absente et la cause de sa non-application n’est pas établie.

Le candidat dev.7 précise, dans la description disponible avant le chargement
et dans les deux overlays DSI, que le STOP constitue le premier commentaire
de progression avant outils. Les annonces de chargement viennent ensuite.
Les mesures conservatoires, les frontières métier, les six commits amont et
les exigences de preuve primaire ou d’abstention restent identiques.
Seul le SKILL DSI généré change parmi les 166 fichiers runtime.

La génération est ciblée depuis les blobs Git du pin DSI, avec les opérations
bornées déjà déclarées dans `upstream.json`. Les autres runtimes et les preuves
historiques, gels et release dev.6 ne sont pas réécrits. L’installation isolée
dev.6 utilisée pour le smoke n’est pas modifiée.

Cette formulation est une hypothèse jusqu’à une nouvelle mesure sur les octets
dev.7 committés et gelés, avec répondants et juges frais. Aucun résultat dev.6,
dev.5 ou DSI autonome n’est transféré. Contrôler le premier événement assistant
visible, y compris les commentaires avant outils ; une annonce puis un STOP
reste un échec. Distinguer lecture de fichier, sélection et activation réelle,
réception de source primaire et abstention. La release reste bloquée tant que
la campagne, le smoke propre au candidat et les avis humains restent ouverts.
