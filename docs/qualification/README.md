# Qualification des corrections

Dernier candidat : dev.5, entièrement non mesuré. Il précise l'activation DSI,
le STOP conservatoire, le transfert RH persistant et la voie sans source.
Le runtime dev.4 précédent est `36cbbd67fa02240cb723f4236c25d4340bcd85ee`.
Mesure partielle r7 au HEAD `d1ab287376c8ae3605b0459850210be4a4e91bf9` :
six réponses achevées et six juges frais, une réussite et cinq échecs.
Trois nominaux indiquent `needs-auth` ; un autre cas est interrompu sans réponse
capturée et neuf ne sont pas exécutés. Les 211 empreintes gelées sont intactes.
Voir [rapport partiel r7](../../tests/evidence/coactivation-corrigee/rapport-partiel-corrections-r7.md)
et [synthèse](../../tests/evidence/coactivation-corrigee/synthese-partielle-r7.json).
`tests/evidence/coactivation-corrigee/gel-dev5.json`
sert seulement de référence d'empreintes pour la reprise de dev.5 ; ce n'est pas une mesure.
Les pins amont sont inchangés, mais les six variantes locales sont distinctes.

R4 dev.2 : 16 jugements frais, une réussite, douze échecs, trois bloqués.
R5 : trois erreurs réseau achevées ; autres processus interrompus, aucune notation.
R6 dev.3 : un APJA achevé puis échoué documentaire, quinze refus de quota.
Les deux tentatives de lecture tronquée sont conservées et exclues des scores.
Les synthèses, rapports et traces restent dans `tests/evidence/coactivation-corrigee`.
Le dernier correctif dev.5 ne reçoit aucun score de ces campagnes ni de r7.

La PR DSI #5 porte la présentation et l'archive portable des mesures DSI/r6 :
https://github.com/brissonjo-sudo/DSI-fpt/pull/5

Après le 7 octobre 2026 à 03 h 31 Europe/Paris, depuis la racine du dépôt :

```powershell
& '.\docs\qualification\Reprendre-coactivation-corrigee.ps1' -PluginRoot (Get-Location).Path -Revision r8
```

Le script refuse un dossier existant, contrôle les empreintes du candidat déclaré, fige le HEAD
courant et lance seize nouvelles conversations. Chaque réponse achevée exige
ensuite un juge frais. Il s'arrête si le quota persiste ou si un cas nominal
constate que le MCP n'est pas connecté ; il ne programme aucune tâche.
R7 est conservée et ne doit pas être complétée après réauthentification.
Avant la reprise, lancer Claude Code dans ce dépôt, valider le serveur
`droit-francais`, puis utiliser `/mcp` pour renouveler OAuth. Aucun secret n'est
à copier dans les preuves. Les corrections de STOP, BASCULE RH, activation DSI et
abstention de dev.5 restent à mesurer dans ce candidat distinct.

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
