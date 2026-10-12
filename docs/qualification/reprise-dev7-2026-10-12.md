# Reprise DSI dev.7 — 12 octobre 2026

La reprise R5 est préparée et ses six profils passent les précontrôles réels.
Aucun répondant R5 n'a commencé. La campagne attend une autorisation explicite
de transmission des scénarios au service Codex et de consommation du quota.
`release_ready` reste faux. Cette préparation ne qualifie ni les réponses,
ni l'activation spontanée, ni le déploiement métier.

## État récupéré

La tâche ponctuelle du 9 octobre a expiré pendant l'attente de fermeture de
Codex. Son état final indique `expired`, sans lancement de campagne R4.
Le binaire figé `codex-cli 0.162.0-alpha.2` a ensuite disparu du disque.
Ces constats expliquent l'absence de campagne complète ; les preuves historiques
et les trois réponses R3 sont conservées, sans transfert de score.

Le candidat reste `fb186b4951b95adabf05904f8a34995720588be3`, arbre
`367440f629417bd33b6a52a0f4af261bae4a971f`. Les 214 fichiers installés ont
été comparés au manifeste R3 et aux blobs Git du candidat. Les questions,
les 124 atomes, les oracles, les modes de sources et le runtime sont inchangés.

## Correctif et contrôles

Le lanceur `scripts/reprise_dev7.py` crée une copie vérifiée des dépendances R4
dans un nouveau dossier. Il refuse les divergences, les gels contradictoires,
les traversées de chemin, un remplacement de destination et un lanceur
différent de celui figé. Aucun fichier de secret n'est copié et aucune
configuration utilisateur n'est réécrite.

Le CLI explicitement choisi pour R5 est `codex-cli 0.162.0-alpha.17.2`,
SHA-256 `d13914ced6c7af174d8d638db938284231227312104b06a25e9608c632a7daec`.
Aucun modèle n'est remplacé : la configuration du profil détermine le modèle,
dont l'identité effective devra être conservée dans chaque trace.

Une première préparation R5 a échoué sur les six lectures : `Get-FileHash`
n'était pas reconnu dans le PowerShell du sandbox. Le successeur calcule
le même SHA-256 avec `System.Security.Cryptography.SHA256` et
`System.IO.File.ReadAllBytes`. L'adaptation n'accepte que la commande exacte
de précontrôle, conserve `sandboxPolicy=readOnly`, puis exige le code de sortie
zéro et l'empreinte attendue. Les modules R4 sont conservés octet pour octet.
Les dossiers de l'échec initial et de la préparation intermédiaire restent
dans `.work`, distincts de la préparation finale R5c.

La préparation finale vérifie réellement les six profils : prime de départ,
APJA, violation de données, sources désactivées, incident DSI/données et
technique DSI. Pour chaque profil : configuration effective, inventaire des
capacités MCP avec `detail=full`, lecture sandbox, cache et configuration
persistante inchangés. Aucun appel modèle n'est réalisé par ces précontrôles.

| Vérification | Résultat du 12 octobre |
|---|---|
| Contre-épreuves R5 | 15 réussites |
| Tests historiques du harnais et du worker | 58 réussites, sans inférence |
| Suite locale du plugin | 147 réussites sur 148 |
| Échec conservé | `test_barriere_de_release_comportementale` |
| Ruff sur le nouveau lanceur et ses tests | Conforme |
| Profils natifs de la préparation finale | 6 sur 6 conformes |
| Campagne finale préparée | 16 cas, 124 atomes |
| Répondants et jugements nouveaux | 0 |

La suite du plugin reste volontairement bloquée sur les preuves comportementales
et avis humains manquants. Aucun résultat de CI distante n'est revendiqué pour
ces nouveaux fichiers locaux.

## Exécution soumise à autorisation

Les [16 prompts exacts](reprise-dev7-2026-10-12-cas.json) totalisent 10 325 octets
UTF-8. Leur fichier de relecture a pour SHA-256
`5fcfdf5b9c6b5f989543f6163b0fe9727195032b67ab3b90925d38e98635c88c`.
Ils décrivent des situations fictives, sans personne nommée, secret,
architecture réelle ni collectivité identifiable. Ils comprennent onze cas
avec activation imposée et cinq cas d'activation spontanée. Les entrées des
juges restent séparées des prompts des répondants.

L'autorisation demandée couvre les seize réponses via le service Codex puis
leur évaluation dans des sessions séparées. Les contenus des skills publics
lus par le modèle et les sources consultées font partie du contexte envoyé.
Les recherches web et MCP juridiques suivent exactement les modes de chaque
cas. L'exécution consomme le quota du compte configuré ; aucune estimation
financière n'est attestée. Aucun système métier réel n'est ciblé.

Limites du lancement préparé : lecture seule, politique `never`, aucun bypass,
aucun login automatique, aucun changement de modèle, une seule tentative de
240 secondes au maximum par répondant, budget global de 95 minutes pour les
répondants, arrêt au premier échec technique. Le fichier `ANNULER` dans le
dossier de campagne empêche le prochain cas. Un marqueur atomique empêche
une seconde exécution ; les bilans et tentatives restent conservés.
Les jugements séparés ne constituent pas une revue DSI/RSSI ou juridique humaine.

Le contrôle automatique d'approbation a rejeté la commande `run-all` :
transmission externe des cas et consommation de quota/coûts possibles sans
autorisation explicite de ce payload et de cette exécution multi-cas.
Aucun contournement ni lancement indirect n'a suivi ce rejet.

## Reprendre après autorisation

Le dossier préparé localement est
`tests/evidence/.work/reprise-dev7-20261012-r5c/` dans le worktree attaché.
Son manifeste de campagne a pour SHA-256
`409c96b5ad8b8c1367e8efe0c53cef26fb2fccd7cc754fb9168943e4a24e0138`.
Les captures RPC privées restent dans ce dossier ignoré par Git ; aucune
preuve privée ni état d'authentification n'est ajouté aux fichiers versionnés.

```powershell
python -B scripts/reprise_dev7.py check --folder tests/evidence/.work/reprise-dev7-20261012-r5c
# Après autorisation explicite seulement :
python -B scripts/reprise_dev7.py run-all --folder tests/evidence/.work/reprise-dev7-20261012-r5c
```

Après les réponses : contrôler les traces, sceller les paquets, réaliser les
seize jugements indépendants, documenter les échecs, puis effectuer le smoke
complet et les avis humains. Les conflits de la PR plugin avec `main` seront
traités sur un candidat distinct ; les mesures ne se transfèrent pas à un
runtime modifié. Aucune fusion, publication ou intégration DSI dans la release
1.2.0 n'est réalisée par cette reprise.

Référence technique : [documentation officielle Codex App Server](https://learn.chatgpt.com/docs/app-server),
consultée avec Context7 `/openai/codex` avant l'adaptation du protocole.
