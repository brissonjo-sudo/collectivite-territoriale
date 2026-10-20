# ADR 0023 — Poursuivre la lecture des entrées sélectionnées jusqu'à leur fin

Date : 20 octobre 2026. Décision de Jo transmise par Claude, T43-L40 :
« Consigne + smoke ce soir ».

Le smoke L39-e a consommé une session. Le constat transmis par Claude décrit
un STOP correct, un MCP installé réussi et une sonde EOF acceptée ; l'entrée
recherche-juridique n'a cependant été reçue que jusqu'à 510 lignes sur 1162.
Les lectures reçues sont vérifiées ; selon Claude, l'interprétation de la phrase
sur une restitution incomplète a fait arrêter la série. Ce constat historique
ne vaut ni nouveau smoke ni qualification du candidat L40.

Le seul changement fonctionnel est l'ajout suivant au prompt, sans retirer
aucune phrase ni aucune règle existante :

> Chaque entrée SKILL.md sélectionnée doit être lue jusqu'à sa fin, marquée par le premier segment de moins de 85 lignes. Une restitution perçue comme tronquée ne permet ni de relire ni d'interrompre la série : poursuis avec le segment suivant (M + 85), puis signale la limite dans la réponse.

Il distingue la poursuite de la série de lectures de la restitution finale :
une impression de troncature impose le segment suivant, sans relecture, puis
la limite est signalée dans la réponse. Le premier segment court demeure la
borne de fin ; aucune nouvelle commande, sonde ou tentative n'est demandée.

Le texte exact est vérifié pour les deux cas. Tous les autres corps de fonction
du runner, notamment les validateurs, `read_events`, `complete_entry`, la règle
d'au plus une sonde EOF, STOP et MCP installé sans web, restent identiques.
N demeure 85. Les sept skills, les scénarios et les seuils restent inchangés.

La transition fermée ADR 0017 renouvelle seulement les empreintes cibles exactes
du runner et du CHANGELOG ; ses sources et son ensemble de chemins sont inchangés.
La campagne d et ses avis restent acceptés par les contrôles existants ; aucun
autre écart d'outillage n'est autorisé.

Le pré-vol sur copie isolée ne simule que le rattachement commit/outillage du
smoke L30-c, puis les sceaux et liens qui en dépendent. La release simulée,
la projection publique et son diagnostic sont non probants. Ils ne transfèrent
aucun succès au nouveau candidat, qui doit passer la tentative neuve L40-f.

Claude, session principale, demande à Jo l'autorisation Install puis Run de
cette tentative, au plus deux sessions. Le PATH PowerShell 7 reste limité au
seul processus de smoke, comme L39. Aucun appel modèle, Docker, push ou accord
d'exécution du smoke n'est acquis dans ce lot de préparation.
