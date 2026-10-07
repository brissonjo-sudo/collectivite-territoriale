# Outillage de la mesure partielle r7

Copies exactes des sources utilisées dans le workspace d'orchestration, avec les
tests négatifs. Les modules de liaison historiques se trouvent dans le dossier
parent. Les chemins de lecture natifs et le workspace d'origine font partie des
preuves : ces copies documentent le producteur et ne constituent pas une archive
portable autonome à exécuter depuis ce sous-dossier.

`generer_rapport_partiel_r7.py` contrôle les six réponses, les six juges, les 211
empreintes et le reçu d'interruption. Il refuse les réponses sans liaison native,
les scores nominaux sans primaire et les reçus incomplets. Le générateur complet
et `verifier_archive_r7.py` restent réservés à une campagne complète ; ils n'ont
pas été utilisés pour déclarer r7 qualifiée.

Contrôles dans le workspace d'origine : onze tests de preuve, quatre tests
négatifs du rapport partiel, puis reconstruction indépendante exacte du rapport
et de la synthèse, hors horodatage de production. Aucun runtime gelé modifié.
L'archive DSI/r6 du 6 octobre reste distincte et ne contient pas r7.
