# Mesure du candidat 1.3.0 — outillage L10, non exécuté

Les dix-huit cas comprennent les neuf scénarios historiques inchangés et les
neuf propositions DSI acceptées par Claude les 17–18 octobre 2026. Aucun budget
n'est ajouté aux propositions qui n'en avaient pas. Le schéma v2 rend explicites
`stop_first`, `activation_mode`, `expected_skills` et `invariants_observables`.
`invariants` conserve ces mêmes attendus pour le qualificateur existant.

## Contrôle observable

Le protocole Codex v5 permet un message STOP avant toute lecture ou annonce.
Le contrôle porte sur les événements JSONL : premier texte visible, débuts
d'outils même avortés, complétion du mot STOP avant le premier outil, entrées
complètes lues par segments vérifiés. Une simple mention de skill ne suffit pas.
Un début d'outil absent empêche de prouver sa chronologie et produit un refus.
Un raisonnement interne n'est pas un texte visible. Les événements d'action
inconnus ou incomplets sont refusés. Ces contrôles ne jugent pas le droit.

En mode forcé, l'ordre des entrées complétées doit égaler `activation_sequence`.
En mode spontané, cette séquence reste vide : le catalogue des sept entrées est
disponible sans sélectionner les attendus à la place du modèle. Tous les skills
attendus doivent être observés, sans doublon ni entrée partielle ; aucun ordre
supplémentaire n'est inventé pour ces deux cas. L'observation est une lecture
native complète, pas l'outil Skill de Claude ni la preuve d'un mécanisme causal
exclusif. Les neuf scénarios historiques gardent leurs contrôles précédents.
Le lanceur Claude historique refuse un lot contenant du v2 avant tout appel ;
ces nouveaux contrats sont réservés à la chronologie Codex, sans voie dégradée.

## Chaîne logicielle préparée

Les commandes suivantes sont des formes à compléter **après autorisation Jo**,
avec un SHA complet du nouveau candidat et des dossiers neufs hors checkout :

```powershell
python -B scripts/run_codex_campaign.py --plugin-commit <sha40> --codex <cli-epingle> --model gpt-6.1-sol --output-dir <campagne-neuve> --stop-on-failure --authorize-model-calls
python -B scripts/review_codex_campaign.py --plugin-commit <sha40> --campaign-dir <campagne> --codex <cli-epingle> --model gpt-6.1-sol --output-dir <relecture-neuve> --authorize-model-calls
python -B scripts/run_codex_smoke.py --plugin-commit <sha40> --codex <cli-epingle> --phase install --output-dir <installation-neuve> --authorize-install
python -B scripts/run_codex_smoke.py --plugin-commit <sha40> --codex <cli-epingle> --phase run --prepared-env <installation> --output-dir <smoke-neuf> --authorize-model-calls
python -B scripts/assemble_release_evidence.py --plugin-commit <sha40> --campaign-dir <campagne> --review-dir <relecture> --smoke <smoke/installation-codex.json> --dcp tests/evidence/2026-10-08-candidat-013/dcp-autonome.json --output-dir <distribution-neuve>
```

Le runner campagne accepte également `--dry-run`, le reviewer et les deux phases
smoke aussi. Aucun de ces dry-runs n'appelle de processus modèle, n'installe de
plugin ou ne crée une pièce qualifiable. Ils sont marqués synthétiques.

Chaque mesure réelle vérifie HEAD, l'arbre propre et les octets du runtime,
des configurations, des cas et de l'outillage. Le binaire Codex est épinglé par
SHA-256 dans `scripts/measurement-cli.json` : un simulateur ou une autre version
est refusé avant exécution. Changer cette CLI exige un arbitrage et une nouvelle
baseline, sans substitution automatique. Les reçus CLI contiennent les
empreintes du binaire, des arguments, de l'entrée et des flux bruts, ainsi que
l'identifiant de thread observé. Les flux bruts/raisonnements restent en mémoire.
Les réponses et traces utiles sont liées par SHA-256. Aucun ancien gel, score,
cache, profil ou état R4/R5 n'est importé. Les tests historiques relisent les
cas au commit effectivement mesuré, sans supprimer d'assertion ou de cas.

## Smoke isolé et authentification séparée

La phase install extrait seulement les fichiers publics du commit et installe
dans un `CODEX_HOME` temporaire neuf, conservé sous la tentative. Le catalogue
temporaire utilise `ON_USE` afin de séparer installation et connexion. Les
catalogues distribués restent inchangés ; leur parcours `ON_INSTALL` n'est donc
pas prétendu testé. Aucun credential ou profil existant n'est copié.

Jo doit connecter ce nouveau home séparément, si nécessaire, avant la phase run.
Le lanceur ne fait que `login status` et refuse l'absence de connexion ; il ne
lance jamais `login`, `mcp login` ni un flux OAuth. Les deux réponses modèle
utilisent uniquement le plugin installé, sans copies natives de skills ajoutées
au workspace, sans surcharge MCP globale. `skills/list` vérifie la visibilité
réelle des sept entrées et leur chemin installé ; la présence des fichiers seule
ne la démontre pas. Ce petit client neuf de métadonnées n'importe aucun bridge R5
et n'appelle ni thread/start ni turn/start.

Le smoke exige les cas `activation-implicite` et `mcp-installe`, les entrées DCP
et juridique entièrement lues, un MCP installé réussi et STOP en premier dans
le premier cas. Les empreintes installées et la configuration principale sont
comparées avant/après. Une erreur produit un refus, jamais une synthèse positive.
Les homes temporaires éventuellement authentifiés ne sont pas des pièces à
archiver : l'assembleur ne copie que ses liens publics explicites.

## DCP-0 — décision du 18 octobre 2026

L'ADR 0012 consigne le choix de l'orchestrateur : référencer la mesure autonome
DCP existante au pin inchangé, sans nouvelle campagne DCP ni juge Claude.
Les options DCP-A / DCP-B de L9 sont remplacées par cette décision. Les limites
du protocole amont restent constatées dans `scripts/dcp-protocol.json`, sans
aucune modification de son moteur, de son barème ou de ses seuils.

`python -B scripts/check_dcp_protocol.py` vérifie sans modèle le pin, les 30
empreintes runtime contre les fichiers embarqués, la provenance publique,
`source_summary_sha256` et l'empreinte du fichier entier de la pièce autorisée.
Seul `LICENSE`, embarqué pour la distribution mais absent de la mesure autonome,
est exclu ; tout autre écart est refusé. L'assembleur refait ces contrôles et
copie la preuve à l'identique, réserves et `scope` d'origine compris, sans y
ajouter de commit plugin. La copie est elle aussi contrôlée.

Ce contrôle ne mesure pas le plugin : les 18 cas, leurs 18 relectures séparées
et les deux sessions de smoke restent liés au commit exact du candidat. Le
lanceur préparé hors dépôt `l10-preuves/run-mesure.ps1` prévoit **38 sessions
Codex gpt-6.1-sol et zéro session Claude**, hors reprises et requêtes d'outils.
Coût, quota disponible et durée future : inconnus ; budget Jo à fixer avant appel.
Il n'est pas exécuté. Les preuves historiques plugin/R4/R5 ne sont pas transférées.

## Assemblage et limites de preuve

L'assembleur refuse campagne incomplète/doublonnée, commit divergent, pièce
synthétique ou dry-run, reçu réel absent, empreinte altérée, DCP absent et smoke
ou relecture non liés. Il recalcule les contrôles de campagne. Il ne propose
aucune option d'acceptation des fixtures ou d'avis humain automatique.

La sortie est une distribution indépendante avec `release-<version>.json`,
jamais une écriture dans `tests/evidence` du candidat. La qualification existante
est recalculée dans cette copie avant écriture du manifeste final. Le
qualificateur et la CI ne sont pas modifiés. Une intégration ultérieure de vraies
pièces reste un lot autorisé et revu. DCP-0 permet de référencer la mesure
autonome ; l'absence des nouvelles campagnes plugin et du smoke empêche toujours
la finalisation. Les essais sur fixtures ne produisent aucune preuve courante.

`review.human_legal_validation` vaut toujours false à l'assemblage ; seul Jo
peut décider de la passer à true hors script, après avis réel. Les invariants
métier non relus restent faux/bloqués et `deployment.ready`/`release_ready`
restent false. ADR 0007 sépare toujours la distribution technique et l'avis métier.

Des empreintes et reçus locaux ne constituent pas une attestation indépendante
contre un opérateur qui fabriquerait toute une chaîne avec de faux reçus et de
nouvelles empreintes. Les contre-épreuves refusent les fixtures déclarées, les
reçus incomplets et les altérations ; elles ne revendiquent pas cette garantie
cryptographique plus forte. Aucun avis juridique n'est produit ; les règles
juridiques éventuelles restent à vérifier par un praticien sur source officielle.

Sources techniques consultées : [JSONL Codex](https://learn.chatgpt.com/docs/non-interactive-mode),
[commandes CLI](https://learn.chatgpt.com/docs/developer-commands?surface=cli),
[métadonnées skills/list](https://learn.chatgpt.com/docs/app-server), aides du
binaire local 0.162.0-alpha.17.2. Context7 a été tenté mais son quota était épuisé ;
la documentation officielle a été consultée en remplacement. Le protocole DCP
est lu au pin public exact, sans exécuter son lanceur.
