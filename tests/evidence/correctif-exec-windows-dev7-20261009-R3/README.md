# Correctif du précontrôle Windows r3 — 9 octobre 2026

La tentative r2 à froid du 9 octobre à 10:09 UTC passe l’inventaire des
processus et découvre le MCP juridique authentifié avec huit outils.
La RPC command/exec est ensuite refusée avant lecture : code -32600,
custom outputBytesCap is not supported with windows sandbox.
Le run r2 n’est pas créé, aucun modèle ni répondant lancé. Preuves conservées.

## Correctif et validation

La nouvelle version r3 omet outputBytesCap et conserve le défaut serveur.
Les captures du client restent bornées à 8 MiB. La réponse de lecture doit
comporter un code entier strictement égal à zéro, stdout/stderr de type
chaîne et chacun limité à 4096 octets UTF-8. Le SHA normalisé doit être
exactement celui du skill installé, stderr vide, sans marqueur de troncature.
Le délai commande reste 20 secondes et le délai RPC 35 secondes.
Backend elevated, sandbox read-only, approbation never restent inchangés.

31 tests passent, dont la régression simulant le refus Windows du paramètre
et les négatifs de capture, code de sortie et empreinte. Ruff, parseur
PowerShell et contrôle statique passent. Les seize questions, 124 atomes,
oracles et modes de sources restent intacts. Le normaliseur r2 est réutilisé
sans modification. Quatre nouveaux fichiers et cette dépendance forment
l’outillage r3 ; les empreintes des versions antérieures sont vérifiées.

Une sonde native sans cap personnalisé atteint le backend Windows, sans
rejet de paramètre. Avec l’application ouverte, elle échoue au rafraîchissement
du sandbox, code -32603. Ce résultat ne prouve pas une lecture réussie à froid.
Les RPC privées, journaux bruts, identifiants OAuth et corps juridiques sont
exclus de cette archive. Le diagnostic rapporte seulement l’erreur ciblée.

## Exécution depuis le terminal de la session

Les copies outillage sont documentaires et dépendent du workspace, de ses
preuves historiques et du profil isolé. Elles n’installent rien.
Fermer complètement Codex, garder le terminal Windows ouvert et exécuter :

```powershell
& 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -NoLogo -NoProfile -File 'C:\Users\Krn\Documents\Codex\2026-10-06\reprends-le-travail-de-cette-session\lancer-campagne-native-dev7-complet-20261009-r3.ps1'
```

Le run cible qualification-coactivation-dev7-complet-20261009-r3 est neuf.
Les précontrôles passent avant préparation puis avant chaque tentative.
Une seule tentative par cas, arrêt au premier échec technique, aucune relance
automatique ni terminaison de processus préexistant. Après sortie du lanceur,
revenir à la session pour juger les paquets scellés avec des sous-agents frais.

Le bilan R3 historique reste partiel à trois cas sur seize. La lecture à froid,
les seize réponses et jugements, STOP critique, smoke et avis humains restent
ouverts. Aucune nouvelle mesure transférée. PR brouillon, release_ready=false.
