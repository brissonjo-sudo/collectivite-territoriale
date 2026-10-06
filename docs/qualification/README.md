# Qualification des corrections

Dernier runtime dev.4 : `36cbbd67fa02240cb723f4236c25d4340bcd85ee`,
entièrement non mesuré. `tests/evidence/coactivation-corrigee/gel-dev4.json`
sert seulement de référence d'empreintes pour la reprise ; ce n'est pas une mesure.
Les pins amont sont inchangés, mais les six variantes locales sont distinctes.

R4 dev.2 : 16 jugements frais, une réussite, douze échecs, trois bloqués.
R5 : trois erreurs réseau achevées ; autres processus interrompus, aucune notation.
R6 dev.3 : un APJA achevé puis échoué documentaire, quinze refus de quota.
Les deux tentatives de lecture tronquée sont conservées et exclues des scores.
Les synthèses, rapports et traces restent dans `tests/evidence/coactivation-corrigee`.
Le dernier correctif dev.4 ne reçoit aucun de ces scores.

La PR DSI #5 porte la présentation et l'archive portable des mesures DSI/r6 :
https://github.com/brissonjo-sudo/DSI-fpt/pull/5

Après le 7 octobre 2026 à 03 h 31 Europe/Paris, depuis la racine du dépôt :

```powershell
& '.\docs\qualification\Reprendre-coactivation-corrigee.ps1' -PluginRoot (Get-Location).Path -Revision r7
```

Le script refuse un dossier existant, contrôle les empreintes dev.4, fige le HEAD
courant et lance seize nouvelles conversations. Chaque réponse achevée exige
ensuite un juge frais. Il s'arrête si le quota persiste et ne programme aucune tâche.

Outillage de preuve archivé dans `outillage/` : les scripts des traces sont
interprétés par une grammaire fermée, jamais exécutés. Les tests se lancent dans
des processus distincts pour éviter les adaptations globales d'import :

```powershell
Set-Location '.\docs\qualification\outillage'
python -m unittest test_lie_jugements_corriges_bruts
python -m unittest test_verifier_archive_corrigee
python -m unittest test_portable_adapter
```

La lecture brute complète conserve les véritables appels et retours natifs.
L'adaptateur d'export 02c historique est conservé séparément de la correction
du parseur qui accepte un retour ligne final, sans autoriser d'instruction ajoutée.
Avis humains et smoke Codex ouverts. `release_ready=false`.
