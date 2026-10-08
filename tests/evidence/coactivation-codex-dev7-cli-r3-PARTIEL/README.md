# Mesure native dev.7 partielle — 8 octobre 2026

Le candidat `fb186b4951b95adabf05904f8a34995720588be3` a été exécuté dans
trois sessions CLI distinctes, puis jugé par trois agents nouveaux sans contexte
parent après exports v2 scellés. Deux réussites, un échec ; sur 23 atomes :
16 vrais, 1 faux, 6 non vérifiables. La suite complète reste de 16 cas / 124
atomes : treize cas exigeant des sources primaires n'ont pas été exécutés.

| Cas | Verdict | Atomes vrais / faux / non vérifiables |
| --- | --- | --- |
| MCP indisponible | Réussite | 5 / 0 / 0 |
| DSI technique spontané | Échec | 3 / 1 / 6 |
| Source indisponible explicite | Réussite | 8 / 0 / 0 |

Les deux réussites valident la méthode et les abstentions attendues lorsque
les sources manquent. Elles n'établissent aucune règle de droit. Le cas source
indisponible atteste l'injection native des deux SKILL complets DSI et recherche
juridique, aux empreintes installées. Le cas technique annonce DSI mais sa lecture
échoue ; aucune injection complète ne prouve son activation.

La lecture de santé préalable réussit hors application. Quatre lectures pendant
les répondants échouent au démarrage avec `helper_unknown_error: setup refresh
had errors`. Aucun refus automatique d'approbation ni code Windows précis n'est
déduit de ces événements. CLI 0.162.0-alpha.2, modèle observé gpt-6.1-sol,
lecture seule, web et MCP juridique locaux désactivés. L'exposition globale MCP
reste inconnue. La configuration effective a changé par les API officielles
dans le profil isolé ; les caches dev.6 et les octets du candidat sont préservés.

Le réexport v2 corrige exclusivement une fausse alerte de comparaison dans le
cas technique : les finales brutes concordent avant remplacement d'un chemin
local. Il ajoute les constats minimaux des erreurs natives. Questions, oracles,
atomes, rubrique, cinq modules figés, réponses et traces brutes restent inchangés.
Aucun répondant réexécuté. Les exports v1 historiques restent locaux et scellés.

Les références des juges sont liées aux événements et aux SHA des lignes natives.
Les identités d'agents proviennent des résultats hôte de création et d'inventaire ;
la borne d'horloge précédant les créations est distinguée des heures de fin
rapportées. Le système de fichiers partagé n'est pas présenté comme isolé.
Les contextes natifs complets, stderr et inventaires d'outils ne sont pas publiés.
Les sélections d'exécution gardent leurs SHA, sans les chemins privés.

`release_ready=false` : STOP critique de réouverture non couvert, treize cas
non exécutés, activation DSI spontanée en échec, smoke complet et avis DSI/RSSI
et juridique humains ouverts. Les scores DSI autonomes 28/28 et dev.5/dev.6
restent historiques, sans transfert. Cette mesure succède à l'instantané de
préparation zéro modèle, dont les preuves restent conservées.

Les scripts d'outillage sont des copies documentaires du contrôle effectué dans
la session locale ; leur accès aux traces natives privées reste nécessaire.
La présentation v9 et ses contrôles figurent dans la PR DSI brouillon #5.
