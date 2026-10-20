# T43-L24e — correction de l'arrêt sur relecture et tentative d

20 octobre 2026. Décision de Jo : « Corriger + tentative d ».
Tête plugin inchangée : 13b4e1e537e5a8097a004ee913abcc9d079114a7. Tentative unique : campagne-l24-20261020-d.
Harnais dérivé de l24c-campagne, décision L24d de retrait de la barrière MCP incluse.

## Constat et conservation de c

La tentative campagne-l24-20261020-c est consommée : six sessions ouvertes,
4 679 266 jetons d'entrée observés, arrêt review_incomplete_or_unfavorable après
la relecture de plugin-violation-donnees : deux non_verifiable, aucune violation.
Ces chiffres sont vérifiés dans son run-campagne.status et les six usages.
Son dossier et ses sorties sont conservés intégralement ; l'index SHA-256
l24e-preuves/archive-c-consommee/index.json constitue son archive sur place.
Aucun fichier de c n'est déplacé, réécrit ou repris dans d. Les tentatives a et b
sont des pannes avant modèle à zéro jeton déclaré ; c est comptée séparément.
Le budget de d n'absorbe aucun usage ni résultat des tentatives antérieures.

La condition héritée arrêtait sur tout statut autre que respecte. Elle empêchait
la résolution humaine prévue par docs/adr/0012-resolution-humaine-liee.md.
Selon le constat Claude transmis par Jo, la CLI 0.163 ne restitue pour open_page
que domaine, titre, extrait et URL, sans texte de page. web_review.py continue
de refuser les titres et extraits comme preuve du texte ; ses octets sont inchangés.
Le précédent L14 cité par Jo ne constitue aucune validation transférable à d.

## Correction et limite

Une relecture arrête le run si au moins un invariant est violation.
Un échec technique, de cas ou de processus arrête toujours immédiatement.
Un non_verifiable poursuit ; le statut automatique original reste inchangé,
sa liste est consignée dans le journal des rôles, human_resolution_applied=false.
Il n'est jamais compté respecte par l'outillage. Le résumé conserve observe=non
et statut_relecteur=non_verifiable ; human_legal_validation reste false.

La résolution relève exclusivement d'un avis daté de Jo conforme à l'ADR 0012,
lié aux sessions, traces et résumé exacts par empreintes. Aucun avis n'est créé
ni inféré ici. Une violation ou un échec technique n'est jamais résolu ainsi.
Achever le run signifie execute_a_relire, pas une qualification ou une release.

## Règles conservées

Dix-huit cas complets, contrat v2 et STOP déterministes inchangés. Trente-six
sessions maximum : réponse et relecture distinctes, gpt-6.1-sol/high, 360 s/rôle.
CLI campagne/relecture 0.163.0-alpha.10.2 et compagnons verrouillés ; précontrôle
natif des sept skills 180 s et ACL (OI)(CI)RX au seul runtime copié conservés.
Aucun octroi à un home. 1223 arrête : Jo configure, aucune sonde modèle substituée.
La barrière MCP sans modèle demeure retirée par décision L24d ; mcp-capability.json
reste une trace, sans appel depuis le lanceur. La sonde distincte reste écartée.

Une panne de démarrage explicitement attestée avant modèle, sans thread ni
événement modèle, avec zéro jeton attesté et code non nul, arrête sans consommer
la tentative. Les conditions conservatrices L24c et l'archivage manuel restent
inchangés. Une session ouverte ou une consommation inconnue consomme la tentative.
Une panne MCP après un premier rôle consommé rend la tentative consommée.
Aucune reprise d'une tentative consommée, aucun assemblage entre tentatives.

## Autorisation

Jo, 20/10 : « Corriger + tentative d ». Autorisation liée par empreintes au plan,
au manifeste, au contrat, à la tête et à la décision : 36 sessions, suivi de
40 000 000 jetons d'entrée, budget_policy=between_roles, cache déjà inclus.
Aucun nouveau rôle au plafond ; aucune garantie de plafond strict pendant
un rôle ni de limite fournisseur. Aucune session de sonde supplémentaire.

Ce lot prépare seulement : aucun appel modèle, connexion MCP, octroi ACL,
précontrôle natif réel, poussée, gel, assemblage, smoke ou qualification.
La commande exacte est fournie séparément ; elle n'est pas exécutée dans ce lot.
