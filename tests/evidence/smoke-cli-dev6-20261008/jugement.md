# Jugement indépendant du smoke CLI dev.6 — 8 octobre 2026

Quatre sessions CLI fraîches ont produit une réponse authentifiée avec `gpt-6.1-sol`, une seule tentative chacune. Ce smoke est borné ; `release_ready=false`.

| Cas | Conclusion | Preuve native décisive |
|---|---|---|
| 01 — cadrage technique explicite | Usage vérifié de DSI | Injection complète ligne 11 ; cadrage conforme ligne 27. Lecture complémentaire bloquée ligne 16. |
| 02 — budget spontané | Bloqué | Sélection DSI/DirFi lignes 12–13 ; lecture refusée ligne 15 ; refus de conseil ligne 24. Aucune attribution juridique. |
| 03 — réouverture d’incident | Partiel | DSI injecté ligne 11 ; **premier message visible STOP ligne 13**, avant outil ligne 14 ; mesures conservatoires et abstention ligne 29. DPO/juridique non chargés. |
| 04 — réversibilité | Partiel | DSI injecté ligne 11 ; attribution juridique préalable ligne 13 ; vérifications techniques et abstention ciblée ligne 25. Juridique non chargé. |

Les trois usages explicites prouvent une injection native complète de DSI. Les mentions, bascules et tentatives de lecture ne prouvent aucune coactivation de DirFi, DPO ou recherche-juridique. Les annonces initiales d’application de ces autres skills sont prématurées ; les réponses finales reconnaissent les blocages.

Les 214 fichiers du cache, les 213 blobs du commit source `3f0df285898cf1e36d1ddda8d85d0c4cd5e0903b`, le protocole, le harnais et les liaisons prompt/session/exécution/réponse correspondent aux empreintes. Le checkout courant est distinct du candidat ; la comparaison source porte sur les blobs committés. Aucun identifiant ni configuration secrète n’a été lu par ce reviewer.

Neuf appels d’outils sont présents dans les dérivés du rollout, même s’ils ne figurent pas dans le stdout JSONL. Cinq résultats d’outils signalent un blocage ; aucune lecture de skill par outil n’a réussi. L’exposition effective MCP et la découverte globale dans les quatre sessions restent inconnues : la désactivation configurée et l’absence d’appel MCP observé ne prouvent pas leur absence d’exposition.

L’abstention juridique est observée ; aucune validation du droit actuel n’est établie. Aucune campagne complète, validation humaine ou juridique, release, publication, fusion ou push. Le JSON compagnon contient tous les critères préfigés, leurs valeurs `true/false/null` et leurs preuves `native_line`.
