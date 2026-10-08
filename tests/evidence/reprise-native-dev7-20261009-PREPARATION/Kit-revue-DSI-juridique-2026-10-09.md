# Kit de revue DSI/RSSI et juridique — 9 octobre 2026

Le candidat plugin `1.2.0-dev.7`, commit
`fb186b4951b95adabf05904f8a34995720588be3`, reste non qualifié pour la
distribution. Les PR sont brouillon ; aucune revue humaine n'est acquise.
Ce document fournit les pièces et les questions de revue, sans signer d'avis.

## Pièces à examiner

- [PR plugin #11](https://github.com/brissonjo-sudo/collectivite-territoriale/pull/11).
- [PR DSI #5](https://github.com/brissonjo-sudo/DSI-fpt/pull/5).
- Présentation DSI v10 du 9 octobre, 11 diapositives ; preuves natives partielles
  dans `dev7-cli-r3-PARTIEL` du dépôt DSI et
  `coactivation-codex-dev7-cli-r3-PARTIEL` du dépôt plugin.
- Questions et 124 atomes de la suite v2, barème et gel source dev.7.
- Réponses, jugements et événements expurgés des trois cas ; leurs inventaires
  SHA relient les jugements aux projections des traces natives privées.

La mesure partielle comprend deux réussites et un échec : 16 atomes vrais,
1 faux, 6 non vérifiables sur 23. Les deux réussites concernent la méthode et
l'abstention attendues sans sources disponibles. Elles ne valident aucun
texte ni applicabilité juridique. L'injection native complète de DSI et
recherche juridique est attestée dans le cas explicite source indisponible.
L'activation DSI spontanée du cas technique n'est pas attestée.

Le contrôle de réouverture STOP critique n'est pas couvert par ces trois cas.
Treize cas nominaux restent sans mesure. Les scores historiques DSI 28/28 et
dev.5/dev.6 appartiennent à d'autres mesures et ne sont pas transférés.

Le diagnostic du 9 octobre relie les quatre échecs de lecture R3 au
rafraîchissement ACL Windows, erreur 32 sur `node.exe`. Le précontrôle MCP
juridique observe séparément `notLoggedIn`, zéro outil et « Auth required ».
Le flux officiel a expiré sans callback utilisateur. Le nouvel outillage
prépare une reprise à froid ; ni cette lecture ni une campagne complète
ne sont encore établies. Le candidat et les preuves historiques sont préservés.

## Revue DSI/RSSI

Le praticien examine les garde-fous avant toute annonce ou contenu métier,
la préservation des éléments utiles avant une remédiation irréversible et
la réouverture dès qu'un nouvel indice change la qualification antérieure.
Il distingue les besoins techniques du fond RGPD, RH, police municipale,
financier et contractuel attribué aux rôles compétents. Une annonce de bascule
doit précéder le premier contenu réservé et être suivie d'une attribution réelle.

Pour le cadrage technique, examiner segmentation, inventaire, accès,
supervision, continuité et critères de recette. Le cas technique courant
ne fournit pas ces six volets : ils restent non vérifiables, pas validés par
l'absence de détails sensibles. Examiner ensuite les réponses incident,
vidéoprotection, RSSI/RH, budget, réversibilité et réouverture lorsque la nouvelle
campagne aura produit leurs preuves.

## Revue juridique

Le juriste contrôle la correspondance entre chaque assertion et le texte
primaire effectivement récupéré, son identité, sa version, sa date et son
périmètre. Une recherche, un résumé, une référence embarquée ou une mention
« vérifié » ne remplacent pas cette pièce. Les obligations de l'État et des
collectivités sont distinguées, et les faits statutaires ou contractuels
absents restent inconnus.

Examiner notamment les bénéficiaires et conditions des dispositions invoquées
dans le cas APJA, les limites d'appréhension ou de rétention, les violations
de données et les pièces contractuelles manquantes. Ce kit ne fournit ni
identifiant juridique non consulté, ni délai, ni conclusion de droit.

## Enregistrement des avis

Pour chaque avis, conserver la date, le rôle du relecteur, le commit et les
cas examinés, les références aux preuves, les réserves et le verdict explicite.
Éviter les données nominatives et les détails d'architecture d'une collectivité
identifiable dans les pièces publiques. L'absence d'avis reste `pending`.

| Contrôle | État actuel | Pièce nécessaire pour changer cet état |
| --- | --- | --- |
| Revue DSI/RSSI | pending | Avis humain explicite sur les pièces exactes |
| Revue juridique | pending | Avis humain explicite et confrontation aux primaires |
| Campagne complète dev.7 | pending | Seize réponses et seize jugements liés au nouveau gel |
| Réouverture STOP critique | pending | Chronologie native, premier texte visible et jugement |
| Smoke complet du candidat | pending | Usage réel du candidat et preuves distinctes |
| Ouverture PowerPoint native | pending | Vérification dans PowerPoint du livrable exact |
| Distribution | blocked | Contrôles applicables et décision humaine de publication |

Même une campagne complète automatisée ne produit pas ces avis humains.
`release_ready=false` reste la conclusion actuelle.
