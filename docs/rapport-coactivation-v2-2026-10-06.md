# Coactivation v2 — contrôles renforcés

Date : 2026-10-06. Branche locale `codex/coactivation-v2`.
Gel mesuré : `198a26afae192c8bbb4b592ba135895fcf8a04e6` ; 189 empreintes, dont les
166 fichiers des six skills inchangés. Les fichiers historiques du harnais et
de configuration ont leurs octets r3 conservés ; aucun résultat précédent
n'est remplacé. Aucun changement des instructions des skills dans ce lot.

## Suite et portée

16 cas : les 12 questions historiques sont conservées, avec 124 invariants
atomiques ; quatre variantes spontanées supplémentaires sont appariées.
Onze cas ont une activation forcée, cinq demandent la sélection spontanée
des skills. L'oracle de sélection est transmis uniquement au juge.
Les scores v1/v2 ne sont pas directement comparables.

Les sources primaires, recherches et résumés d'outils sont distingués.
Chaque preuve porte son appel d'origine, une capture UTC, les dates retournées
et l'empreinte du contenu assaini. Un résumé, une recherche, une troncature
ou un succès d'appel ne certifient pas la règle juridique.

## Vérifications

58 nouveaux tests réussis : 34 sur le harnais, le routage et le jugement ;
24 sur les sources et l'assainissement. Suite locale complète : 89/90 réussites.
Le seul échec attendu est la barrière de release comportementale, conservée.
Les nouveaux tests couvrent les défauts reproduits par la relecture : ancien
gel incomplet, chemin sensible, recherche promue en texte primaire, texte
tronqué accepté et preuve non liée à son appel hors jugement.

## Pilote réel

Trois premières tentatives ont reçu uniquement le message Claude de quota
atteint, à coût nul. Elles sont conservées dans `pilote`, sous leur propre
gel, et ne fournissent aucune réponse métier. Le MCP y était connecté.
La reprise après la réinitialisation annoncée est conservée séparément dans
`pilote-r3`, sans écraser ni remplacer les premières tentatives.

| Cas | Technique | Texte primaire disponible | STOP premier texte | Natures capturées |
| --- | --- | --- | --- | --- |
| plugin-dsi-source-indisponible | passed | False | None | aucune |
| plugin-prime-depart-retraite | passed | True | None | primary_text, search_result |
| plugin-spontane-incident-donnees | failed | False | False | aucune |

Le cas spontané d'incident active DSI et DPO mais omet recherche-juridique.
Aucun appel MCP ni WebFetch ne réussit ou n'est observé ; le premier texte
est une annonce d'activation, donc le STOP n'est pas premier. Ce défaut de
sélection apparaît sans que le prompt ait fourni les skills attendus.

Ces trois résultats contrôlent le transport et la capture. Aucun jugement
indépendant du fond métier n'est attribué dans ce pilote. La campagne complète
de 16 cas, les corrections éventuelles des skills, la revue DSI/RSSI et
juridique humaine et le smoke Codex restent à réaliser.
`release_ready=false` reste maintenu. La présentation DSI précédente conserve
ses résultats historiques ; elle n'est pas requalifiée par cette préparation.

## Reproduction

Sous PowerShell, depuis ce dépôt, utiliser le Python du runtime Codex :

```powershell
$env:PYTHONUTF8='1'
& 'C:\Users\Krn\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/run_coactivation_v2.py --claude 'C:\Users\Krn\.local\bin\claude.exe' --frozen-manifest tests/evidence/coactivation-v2/gel-v2-r3.json --output-dir tests/evidence/coactivation-v2/campagne-complete-r1
```

Le répertoire doit être neuf ; les fichiers de gel ne doivent pas être modifiés.
Le harnais refuse un gel incomplet, divergent ou une trace déjà existante.
Vérifier les preuves sans réseau ni Git :

```powershell
& 'C:\Users\Krn\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' scripts/verify_coactivation_v2.py --manifest tests/evidence/coactivation-v2/gel-v2-r3.json --traces tests/evidence/coactivation-v2/pilote-r3
```

Ce vérificateur contrôle l'intégrité des preuves ; il ne certifie pas à lui
seul l'identité d'un juge, le droit actuel ou l'aptitude à une release.
Le filtre de secrets est prudent ; il ne garantit pas la détection d'une
valeur secrète arbitraire non étiquetée. Les sources restent des données
non fiables, sans autorité pour modifier les instructions de l'agent.
