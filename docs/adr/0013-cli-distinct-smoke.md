# ADR 0013 — CLI distinct pour le smoke installé

Date : 19 octobre 2026. Décision de Jo, T43-L17 : règle B de L16.
Statut : accepté ; préparation et tests logiciels uniquement dans ce lot.

## Deux toolchains explicites

La preuve de release doit exposer deux identités obligatoires :

- `campaign_cli` : version et SHA-256, partagés par la campagne et sa relecture.
  Le verrou `scripts/measurement-cli.json` reste inchangé :
  `codex-cli 0.162.0-alpha.17.2`, SHA-256
  `e98c516f1c8935789aabe9122ee7e05ec4c3efd1ba6acf179242e031c495b99e`.
- `smoke_cli` : version, SHA-256 et empreintes des trois compagnons dans
  `scripts/smoke-cli.json`. CLI : `codex-cli 0.163.0-alpha.10.2`, SHA-256
  `f6dbf48cb70f62649c645f26c87dc9bf84cc36986202dfad8e12fb5b8ca70312`.
  Compagnons obligatoires : `codex-code-mode-host.exe`,
  `codex-command-runner.exe`, `codex-windows-sandbox-setup.exe`.

Ces CLI peuvent différer. Chaque reçu doit correspondre au verrou de sa phase,
jamais à une CLI choisie d'après son contenu ou trouvée dans le PATH. Campagne
et relecture ne peuvent pas utiliser deux CLI différentes. Installation et
exécution d'un smoke doivent utiliser la même identité complète. Une identité
absente, non épinglée, de mauvaise phase ou divergente est refusée.

Le binaire smoke et ses compagnons sont vérifiés dans le même dossier avant
les phases, avant les réponses et à la fin des phases. Le lanceur contrôle aussi
la version annoncée. Les reçus smoke exposent explicitement `cli_phase` et
`cli_toolchain`. Les reçus L14 antérieurs à ce champ restent acceptés seulement
comme campagne/relecture au SHA **et** à la version exacts de leur verrou.

## Motif et limite

La campagne mesure le comportement du plugin ; le smoke vérifie son installation
dans l'hôte courant. Selon le constat de Claude transmis par Jo, la mise à jour
automatique de l'application du 18 octobre à 23:17, heure de Paris, a retiré les
compagnons de l'ancien dossier CLI. Le smoke b a échoué au démarrage des outils.
La présence de la nouvelle CLI ne constitue pas un nouveau résultat de campagne.

Cette décision supersède la seule obligation de CLI globale unique constatée en
L16. Elle ne déclare pas les comportements des deux versions équivalents. Les
événements, lectures, STOP, visibilité des skills, MCP et autres contrôles restent
appliqués ; toute trace incompatible doit conduire au refus existant.

## Transition bornée des preuves L14

Les sessions, traces, résumé, plans et avis Jo L14 restent octet pour octet
inchangés, au commit mesuré `08f92936dd0ae09775a2d2293bae315cdf20847d`.
Le runtime, sa configuration, les cas et le verrou campagne restent identiques.
La réserve humaine et les liens de l'ADR 0012 sont conservés.

La modification de `measurement_common.py` et du lanceur smoke ne constitue
pas une exemption générale d'identité d'outillage. Le manifeste versionné
`scripts/toolchain-transition-0013.json` lie les empreintes sources L14 aux
empreintes exactes des fichiers de transition. La liste de chemins est fermée
dans le lecteur. Toute modification ultérieure d'un fichier lié, d'un autre
élément du protocole ou du verrou campagne est refusée. Le diff Git reste borné
à ces chemins, à l'assemblage, aux ADR, aux tests et aux pièces déjà autorisées.

## Barrières conservées

L'assembleur exige les deux verrous, relit tous les reçus selon leur phase et
rend les deux identités visibles dans la preuve. Un smoke absent ou échoué ne
peut pas être remplacé par cette décision. Le qualificateur, les tests historiques,
les seuils, l'ADR 0007 et la séparation validate/release restent inchangés.
Aucune preuve `release-1.3.0.json` n'est créée en L17.

Les tests positifs sur les CLI valident uniquement cette propriété sur des données
synthétiques explicitement signalées ; ils ne constituent aucune mesure ou preuve
de release. Les tentatives smoke a/b restent intactes. Le nouveau smoke est préparé
sur la nouvelle tête attendue après poussée de Claude, sans exécution dans ce lot.
