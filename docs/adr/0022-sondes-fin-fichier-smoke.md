# ADR 0022 — Distinguer contenu et sonde de fin de fichier du smoke

Date : 20 octobre 2026. Décision de Jo transmise par Claude, T43-L39 :
« Préciser le validateur ». Claude, session principale, orchestre seul #17 ;
la session fork n'agit plus sur cette PR. La consigne L38-pwsh7-et-fixture
n'est pas appliquée.

Le refus L38-d porte sur une référence de 79 lignes lue par un segment de
85 lignes depuis zéro, puis une commande de même chemin depuis 85 renvoyant
une sortie vide, code zéro et statut completed. Ce deuxième événement est
une sonde de fin de fichier : il n'ajoute aucune ligne au contenu déjà reçu.
Le rejeu diagnostique L29-b couvre aussi l'entrée DCP de 319 lignes par segments
de 90, suivis d'une sonde depuis 360. Ces replays ne requalifient aucune ancienne
tentative, aucun ancien résultat ni aucune session réelle.

`read_events` reconnaît une sonde seulement si son début atteint ou dépasse
le nombre réel de lignes du même fichier, sa sortie normalisée CRLF/LF puis
espaces périphériques est vide, son code vaut zéro, son statut vaut completed,
et les lectures précédentes de cette même session couvrent le même fichier
intégralement, dans l'ordre, de zéro à sa longueur, sans trou ni chevauchement.
Les autres lectures vides, tronquées, échouées ou hors contrat restent refusées.

Au plus une sonde par fichier et par session est acceptée. Une deuxième sonde,
même à un autre offset, n'apporte aucune preuve supplémentaire et serait un
rejeu inutile ; elle est refusée. Les répétitions ou chevauchements de contenu
sont refusés, références comprises. Une couverture d'un autre fichier ou d'une
autre session ne peut jamais autoriser la sonde.

Les sondes sont consignées séparément dans `eof_probes`, avec chemin relatif,
offset, nombre demandé, longueur réelle et empreinte de la source. Elles ne
figurent pas dans `entry_reads`, ne comptent ni comme contenu, ni comme couverture,
ni comme doublon de contenu. `complete_entry` conserve son calcul sur les seules
lectures de contenu. Chaque preuve de cas scellée conserve la liste des sondes.

La grammaire des commandes, le prompt, STOP, les seuils, MCP installé sans web,
les sept skills, les scénarios, la campagne d et les avis restent inchangés.
La transition fermée ADR 0017 renouvelle seulement les cibles exactes du runner
smoke et du CHANGELOG, sans ajouter de chemin autorisé ni modifier ses sources.
Tout autre outillage divergent demeure refusé.

Le diagnostic complet sur copie isolée ne simule que les liaisons commit et
outillage du smoke L30-c ; il reste non probant. Le commit de release simulé
et les projections publiques servent uniquement au pré-vol. Aucune ancienne
réussite n'est transférée à la nouvelle tête réelle, qui doit passer un smoke
neuf, avec autorisation explicite de Jo demandée par Claude.

Pour la tentative L39-e, Claude placera `C:\Program Files\PowerShell\7` en tête
du PATH du seul processus de smoke. Aucun PATH global, profil, binaire ou fixture
de CI n'est modifié par ce lot. Docker, modèles, poussée et publication ne sont
pas exécutés ici.
