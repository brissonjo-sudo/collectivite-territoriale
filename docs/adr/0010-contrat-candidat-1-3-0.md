# ADR 0010 — Contrat du candidat 1.3.0

Date : 17 octobre 2026. Statut : décidé par l’orchestrateur pour T43-L1.

## Objet

Fixer le contrat du candidat d’intégration DSI 1.3.0, construit depuis la tête
préparatoire issue de main. Le statut du candidat est **non mesuré,
non qualifié**. « dev.7 » désigne le plugin historique de la reprise R5 ; ce
n’est ni la version du skill DSI ni le nom du nouveau candidat.

Cette ADR est additive. Elle consigne les décisions D1 à D5 données le
17 octobre 2026 et supersède explicitement, pour le test R5 décrit en D4,
la restriction de portée de l’ADR 0009. Elle ne réécrit pas l’ADR 0009.

## Décisions retenues

### D1 — Version et distribution

Le candidat porte la version **1.3.0**, sous le libellé « Candidat
d’intégration DSI », sur le modèle de « 1.2.0 — Candidat d’intégration DCP »
du CHANGELOG. Aucun suffixe `dev.N` n’est ajouté. Les deux catalogues restent
épinglés à `v1.2.0` : aucun repointage ni changement de publication n’est
autorisé par cette décision.

### D2 — Runtime et coactivation

La cible est l’union des six skills de main et de DSI-fpt 0.2.1, au commit
`704e5dd6a3d15994ed431b23585aabd72086ca75` : DPM, DRH, DPO, DirFi, DCP,
recherche-juridique et DSI. DCP-fpt 0.1.3 reste au commit
`129f374e6ab8ea3b47bcfd9de9ddd52a2d3d9498`, avec son contenu et ses renvois
actuels. DPO-CT 0.2.2 est retenue au commit
`58ea45c4d12812da10ace5f1486deea96b8534fa`. Les autres pins de main restent
inchangés.

Reprendre sélectivement les changements de coactivation de #11 nécessaires
pour l’ordre STOP, l’activation forcée et spontanée, l’abstention sans source
et les transferts persistants. Préserver les surcharges actuelles sans en
affaiblir aucune. Ne reprendre aucune suppression de #11, notamment celles
de DCP, de Ponytail, du qualificateur ou des preuves.

### D3 — CI et preuves

L’ADR 0007 et la séparation des jobs `validate` et `release` sont conservées.
Ne diminuer aucun seuil, ne sauter aucun contrôle et n’ajouter aucun filtre.
Le traitement de `test_preuve_courante_correspond_au_runtime`, lorsqu’aucune
mesure de 1.3.0 n’existe, est différé à L6. L6 présentera les options et leur
diff de test pour arbitrage ; aucune option ne sera appliquée dans ce lot.
Jusqu’à cet arbitrage, un échec de `validate` limité à ce test est accepté et
signalé. Il n’est ni masqué ni contourné.

### D4 — Reprise R5

L5 est autorisé à réintégrer `tests/test_reprise_dev7.py` et à rendre
récupérables les dépendances publiques de R5. Cette décision supersède
uniquement la limitation correspondante de l’ADR 0009 ; cette ADR reste
intacte dans l’historique.

La reprise exclut profils, OAuth, gels et état privé. Elle ne lance ni `init`,
ni `preflight`, ni `prepare`, ni `run-all`. Le test R5 réintégré peut être
exécuté comme contrôle logiciel local ; il ne démarre aucune préparation ni
campagne. Les identités, les chemins et les preuves doivent appartenir au
nouveau candidat ; aucun ancien gel ou score ne lui est transférable.

### D5 — Patchs DPM autonomes

Les patchs de `eval_suite.py` et `package_skill.py` du dépôt DPM autonome
restent hors de T43. Ils sont conservés dans leur emplacement d’archive ;
aucun de leurs changements n’est transposé au plugin.

## Lots suivants et critères de fin

Les lots restent séquentiels. Chaque lot apporte un objectif cohérent dans un
commit distinct sur la branche du successeur. Les critères ci-dessous ne
valident pas à l’avance l’implémentation ou une qualification.

| Lot | Objectif | Critère de fin observable | Risque principal |
|---|---|---|---|
| L2 | Porter le moteur de surcharges nécessaire à DSI. | Insertions et remplacements strictement liés aux hashes/ancres ; contre-tests actuels et nouveaux négatifs passent cp1252 puis UTF-8. | Rendre permissive une dérive ou appliquer deux remplacements dans le mauvais ordre. |
| L3 | Intégrer DPO 0.2.2 au pin retenu. | 18 fichiers sources sélectionnés plus surcharge revue, hashes/ancres corrects, `check_sync` exact et validation humaine conservée. | Recopier les surcharges 0.2.1 ou perdre une frontière. |
| L4 | Intégrer DSI et réconcilier la coactivation avec DCP. | Sept skills reproductibles ; DCP 0.1.3 inchangé ; STOP/transferts/source abstention couverts localement ; manifestes candidat cohérents et catalogues distribués inchangés. | Recopier la suppression DCP de #11 ou annoncer une qualification absente. |
| L5 | Rendre R5 récupérable et tester son outillage sans inférence. | Dépendances publiques identifiées par commit/hash, tests R5 restaurés selon L1 ; aucun chemin privé imposé ; aucun profil/OAuth ni gel copié ; aucune préparation native lancée. | Lier nouveau runtime à `candidate_commit`/cache historiques ou copier un état privé. |
| L6 | Adapter le contrat de preuve et la CI au candidat non mesuré. | Tests historiques conservés, preuve de non-qualification explicite ; contrôles techniques exécutables, release refuse les preuves d’un autre runtime ; cas DCP et DSI préservés, aucun seuil diminué. | Contourner la barrière pour obtenir du vert ou transférer les anciens résultats. |
| L7 | Recette finale locale et dossier de proposition à Jo. | Petits commits vérifiés, cp1252 puis UTF-8, `check_sync`/packaging/CI locale, arbre propre, provenance et bundle candidat vérifié ; écarts de qualification listés ; aucune action externe. | Présenter tests locaux comme qualification, avis humain ou release. |

## Non-transférabilité et limites

Un gel, un score, une campagne, une lecture ou un avis historique ne qualifie
pas le runtime 1.3.0. Tout changement de runtime exige des preuves liées aux
octets et au candidat effectivement contrôlés. Les contrôles logiciels locaux,
la CI, une campagne, une qualification et les avis humains sont des états
distincts.

Cette ADR n’autorise aucune campagne, appel modèle, qualification, fusion,
fermeture de #11 ou #16, poussée, publication, ni repointage des catalogues.
