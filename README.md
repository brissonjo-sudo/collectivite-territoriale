# Collectivité territoriale

[![Validation du plugin](https://github.com/brissonjo-sudo/collectivite-territoriale/actions/workflows/ci.yml/badge.svg)](https://github.com/brissonjo-sudo/collectivite-territoriale/actions/workflows/ci.yml)

Plugin Claude Code et Codex destiné aux collectivités territoriales françaises.
Le candidat local **1.3.0 — Candidat d'intégration DSI — non mesuré, non qualifié**
réunit six expertises métier et une méthode de recherche juridique sourcée,
avec un accès optionnel à Légifrance/Judilibre.

> **Statut du candidat :** aucune mesure ni qualification de ce runtime à sept skills.
> Aucun ancien gel, score ou avis n'est transférable. Les deux catalogues restent
> épinglés sur `v1.2.0` et distribuent les six skills historiques, sans DSI.
> Les preuves de cette distribution sont historiques et ne qualifient pas 1.3.0.
> Voir le [contrat du candidat](docs/adr/0010-contrat-candidat-1-3-0.md),
> la [publication](docs/publication.md) et la [note praticien](docs/deploiement-collectivite.md).

Ce plugin aide à qualifier une situation, identifier les expertises à mobiliser et produire une réponse traçable. Il ne remplace ni la validation d'un juriste, ni le contrôle de l'autorité compétente, ni la vérification des textes officiels en vigueur.

## Contenu du candidat 1.3.0

| Skill | Domaine | Version embarquée |
|---|---|---:|
| `collectivite-territoriale:dpm-fpt` | Police municipale et limites APJA | 1.0.5 |
| `collectivite-territoriale:drh-fpt` | Ressources humaines territoriales | 0.6.0 |
| `collectivite-territoriale:dpo-ct` | Protection des données | 0.2.2 |
| `collectivite-territoriale:dirfi-fpt` | Finances locales | 1.0.4 |
| `collectivite-territoriale:dcp-fpt` | Commande publique | 0.1.3 |
| `collectivite-territoriale:dsi-fpt` | Systèmes d’information et sécurité technique | 0.2.1 |
| `collectivite-territoriale:recherche-juridique` | Recherche et vérification du droit français | 3.5.0 |

L'étiquette distribuée `v1.2.0` contient les six skills, dont DCP 0.1.3.
Les deux marketplaces récupèrent le même commit figé. Une mise à jour
de la marketplace permet d'installer cette version historique, pas le candidat local 1.3.0.

Le serveur MCP `droit-francais`, déclaré une seule fois dans `.mcp.json`, fournit l'accès aux sources Légifrance/Judilibre. Le skill `recherche-juridique` apporte la méthode de vérification de vigueur, de provenance et de citation. Le serveur et la méthode sont complémentaires.

## Exemples d'usage

- Sécuriser une réponse de police municipale et arrêter l'analyse avant tout acte réservé à un OPJ.
- Examiner une prime ou une décision RH avec les dimensions budgétaire, statutaire et juridique.
- Qualifier une violation de données, apprécier le risque et vérifier le délai applicable.
- Cadrer un marché public, appliquer les STOP égalité et acte irréversible, puis orienter les volets financiers et données vers leurs skills.
- Rechercher le droit en vigueur, citer les sources retrouvées et signaler explicitement ce qui n'a pas pu être vérifié.

L'activation simultanée de plusieurs skills dépend de la question posée. Une réponse métier correcte ne constitue pas, à elle seule, une preuve que la méthode juridique ou le serveur MCP ont été utilisés.

## Prérequis et limites

- Claude Code ou Codex avec prise en charge des plugins et marketplaces Git.
- Accès réseau au serveur MCP pour les recherches juridiques en mode nominal.
- Autorisation OAuth si le client la demande. Claude Code utilise le client
  public préenregistré déclaré dans `.mcp.json`, avec PKCE et un callback local
  fixe ; aucun secret OAuth ou PISTE n'est distribué dans ce dépôt.
- En cas d'indisponibilité du MCP, le plugin doit signaler la voie dégradée et ne pas inventer de référence.

`dsi-fpt` est embarqué dans le candidat 1.3.0. DCP conserve la passation et
l'exécution juridique du marché ; DSI prend les spécifications, niveaux de
service, réversibilité et exécution technique. Le chargement effectif d'un rôle
reste nécessaire avant son fond : sa présence installée ne vaut pas activation.
Si le rôle requis est indisponible, ce volet s'arrête explicitement. La frontière
DSI externe des anciens cas reste un scénario où ce rôle n'est pas chargé dans
la session ; elle ne décrit plus l'inventaire du candidat.

Le plugin traite le droit français et l'aide à la décision dans le contexte des collectivités territoriales. Toute conclusion sensible doit être confrontée à la source officielle et aux circonstances du dossier.

La collecte et la transmission éventuelles de données sont décrites dans la [politique de confidentialité](PRIVACY.md). Le serveur MCP peut être désactivé lorsque la transmission d'une requête juridique au service distant n'est pas souhaitée.

Les commandes de marketplace ci-dessous installent la distribution `v1.2.0` ;
le candidat 1.3.0 reste local et non publié.

## Installation dans Claude Code

```text
/plugin marketplace add brissonjo-sudo/collectivite-territoriale
/plugin install collectivite-territoriale@collectivite-territoriale
```

Après une nouvelle version publiée (nouvelle étiquette distribuée, voir [docs/publication.md](docs/publication.md)) :

```text
/plugin marketplace update collectivite-territoriale
/plugin update collectivite-territoriale@collectivite-territoriale
```

Ouvrir une nouvelle session après l'installation ou la mise à jour afin de charger les skills et les outils du plugin.

À la première utilisation dans Claude Code, lancer `/mcp`, sélectionner
`droit-francais` puis suivre l'autorisation dans le navigateur. Le client OAuth
est public : aucun secret client ne doit être demandé ou ajouté localement.

## Installation dans Codex

La marketplace Codex est déclarée dans `.agents/plugins/marketplace.json`. Le catalogue est lu sur `main`, mais le plugin est récupéré à l'étiquette publiée qu'il désigne :

```text
codex plugin marketplace add brissonjo-sudo/collectivite-territoriale --ref main
codex plugin add collectivite-territoriale@collectivite-territoriale
```

Pour actualiser la marketplace :

```text
codex plugin marketplace upgrade collectivite-territoriale
```

Le plugin peut aussi être installé depuis le répertoire des plugins de l'application de bureau après ajout de la marketplace. Ouvrir une nouvelle conversation après installation ou mise à jour.

Cette marketplace Git sert au développement, aux tests et à la distribution directe. Elle ne publie pas automatiquement le plugin dans l'annuaire public universel. Dans un espace de travail ChatGPT, l'import et les autorisations restent administrés par l'organisation.

> **Compte de l'auteur :** ne pas installer ce plugin en parallèle de ses sept skills individuels. Les deux jeux coexistent sous des noms distincts et peuvent doubler le contexte chargé.

## Sources et reproductibilité

### Outil de développement local

[Ponytail](https://github.com/DietrichGebert/ponytail) 5.1.0 est installé dans
`.agents/skills/ponytail/` pour développer ce dépôt uniquement. Il n'est pas
un skill distribué du plugin. Son point d'entrée vérifie la dernière release
stable publiée, le commit de son étiquette et les empreintes locales avant
chaque utilisation, puis affiche les règles seulement en cas de succès :

```text
python .agents/skills/ponytail/scripts/check_version.py
```

Version dépassée, fichiers modifiés ou contrôle réseau/API impossible :
**ne pas utiliser Ponytail**. Aucun cache de succès ni mise à jour automatique.
Les consignes de [AGENTS.md](AGENTS.md) imposent aussi le recontrôle à chaque
tour où il serait appliqué. Les règles de développement restent soumises aux
instructions utilisateur et à la sécurité du projet. [Décision](docs/adr/0008-ponytail-developpement-verifie.md).

### Runtimes métier du plugin

Chaque dossier `skills/<nom>/` provient des fichiers d'exécution d'un commit
amont figé. `upstream.json` fixe dépôt, commit, version et chemins inclus.
`dcp-fpt` reste une copie exacte, sans surcharge. Les six autres skills sont
des variantes locales du plugin, avec leurs surcharges dans `overlays/` et
leur chaîne ordonnée déclarée dans `instruction_overlays`.

Chaque étape vérifie l'empreinte SHA-256 exacte de son entrée et de sa surcharge.
Les insertions gardent leur ancre unique ; les remplacements sont bornés au
champ folded complet de description ou à la section `###` complète de même
titre, hors frontmatter. Toute dérive de base, d'ordre, de texte ou d'ancre
bloque la synchronisation. Les versions internes identifient les bases amont,
pas de nouvelles releases de ces dépôts. Le commit du plugin identifie la
variante complète. Aucun dépôt amont n'est modifié.

DSI 0.2.1 est figé à `704e5dd6a3d15994ed431b23585aabd72086ca75` :
30 fichiers runtime, sélection de #11, sans cache de valeurs. DPO 0.2.2 reste
figé à `58ea45c4d12812da10ace5f1486deea96b8534fa` (18 fichiers).
Les renvois DCP, les STOP et l'abstention sans source primaire sont conservés ;
les transferts imposent l'activation effective et une attribution persistante.

Pour `recherche-juridique`, la racine canonique `skill/` est aplatie dans `skills/recherche-juridique/`. Sa licence est copiée avec le runtime ; aucun manifeste, serveur MCP, fichier `.env` ou autre fichier de dépôt amont n'est dupliqué. Le fichier `references/cache-taux-seuils.md` de `dirfi-fpt`, exclu de son propre paquet de distribution, n'est pas embarqué.

Pour DCP 0.1.3, le commit correctif est figé :
`129f374e6ab8ea3b47bcfd9de9ddd52a2d3d9498`. Les 30 fichiers de son paquet
runtime et sa licence sont copiés ; le cache `references/cache-valeurs.md`,
la conception, les scripts d'évaluation et les preuves amont sont exclus.
Le registre daté reste une piste de recherche, jamais une preuve de lecture
officielle dans la session. Aucun correctif local du contenu DCP n'est appliqué.

Pour reproduire les copies depuis des dépôts locaux placés côte à côte :

```text
python scripts/sync_skills.py --local-repos C:\chemin\vers\repos
python scripts/check_sync.py --local-repos C:\chemin\vers\repos
```

Sans `--local-repos`, les scripts clonent les dépôts GitHub et vérifient les commits figés, puis appliquent uniquement les surcharges déclarées et vérifiées. La CI échoue si un fichier embarqué diffère du résultat reproductible, manque ou apparaît en plus. Une mise à jour d'un skill exige de modifier son commit et sa version dans `upstream.json`, de relancer la synchronisation et d'incrémenter la version du plugin dans les deux manifestes. Une correction locale exige de revoir ses empreintes et son ancre, de régénérer les copies et de refaire la campagne comportementale.

## Validation

```text
python scripts/check_sync.py
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

Pour contrôler l'intégration candidate sans qualifier une publication :

```powershell
$env:CT_EXIGER_ETIQUETTE="1"
$env:CT_SAUTER_BARRIERE="1"
python -m unittest discover -s tests
$env:CT_SAUTER_BARRIERE="0"
python -m unittest discover -s tests -k ReleaseGateTests
```

La CI découvre tous les tests dans le job **Intégration candidate** et ne
saute que `ReleaseGateTests`. Le job **Qualification de distribution open source**
force `CT_SAUTER_BARRIERE=0` et contrôle les preuves techniques, leurs empreintes,
le runtime et la configuration installée. Sans cette variable, la découverte
complète exécute aussi ce contrôle.

Sous un shell Unix, l'équivalent pour l'intégration est
`CT_EXIGER_ETIQUETTE=1 CT_SAUTER_BARRIERE=1 python -m unittest discover -s tests`.

Le manifeste Codex est également contrôlé avec le validateur du skill système `plugin-creator`. Les cas de `tests/cas-plugin.json` couvrent notamment :

- le garde-fou APJA sur une demande d'acte réservé à l'OPJ ;
- une gratification de départ mobilisant finances, RH et recherche juridique ;
- une violation de données mobilisant DPO et recherche juridique ;
- le comportement dégradé lorsque le MCP juridique est désactivé.
- les deux STOP DCP, les frontières financières et données, la dépendance DSI
  externe et le comportement DCP sans accès aux sources officielles.

Les preuves historiques de la distribution open source 1.2.0 exigent des traces comportementales en
conversations fraîches, le seuil de mesure DCP et un smoke installé réussi.
Le statut de cette distribution historique est conservé dans `tests/evidence/release-1.2.0.json` :
`distribution.ready` concerne cette distribution ; `deployment.ready` et
le champ historique `release_ready` restent faux sans qualification métier.
La relecture praticien devient une condition du déploiement opérationnel
dans une collectivité ou une structure tierce, selon l'[ADR 0007](docs/adr/0007-distribution-open-source-et-deploiement.md).
Les preuves historiques et avis humains non réalisés restent inchangés.

Le lanceur `scripts/run_plugin_campaign.py` exécute les neuf scénarios dans
des sessions non persistées, impose les activations qualifiées attendues,
désactive les connecteurs juridiques globaux et ne conserve qu'une trace JSONL
assainie dans `tests/evidence/.work/`. La revue humaine des invariants métier
reste distincte et requise avant le déploiement opérationnel chez un tiers.

Pour la distribution historique 1.2.0, la campagne utilise Codex et
`scripts/run_codex_campaign.py` : copies natives en workspace frais,
lectures ordonnées par segments vérifiés, MCP juridique propre au processus
dans les sept cas nominaux, MCP absent dans les deux cas dégradés. La connexion
Codex existante suffit ; aucune connexion Claude n'est requise pour ce profil.
La campagne native ne teste pas le déclenchement implicite ou l'activation
Skill de Claude. Un smoke distinct installe le candidat exact depuis Git,
vérifie les six skills dans le contexte modèle et leurs octets, puis mesure
des réponses et appels MCP depuis ce cache, sans copie native en workspace.
Une demande sans nom de skill déclenche des lectures DCP/juridique et un STOP ;
la mémoire et les instructions utilisateur restent présentes, sans attribution
causale exclusive. La mesure autonome DCP avec web/MCP garde son profil distinct.

Ces résultats et avertissements historiques ne s'appliquent pas au candidat
1.3.0. Aucune preuve `release-1.3.0.json` n'est fabriquée. Les tests de preuve
restent inchangés et signalent cette absence ainsi que la divergence du runtime.
Un ancien test exige encore l'absence de DSI : il reste inchangé, en attente
de l'arbitrage L6. ADR 0007, séparation validate/release et seuils sont conservés.

`tests/cas-plugin.json` conserve ses neuf cas historiques, dont les cinq DCP.
`tests/cas-coactivation-dsi.json` ajoute huit cas locaux de structure (six
activations forcées, deux spontanées), sans jugement ni mesure. Les quatre tests
de structure associés ne prouvent aucun comportement du modèle. Ce fichier
n'est pas raccordé aux lanceurs historiques : leur activation forcée systématique
ne permet pas d'évaluer les nouveaux cas spontanés en l'état. Aucune campagne,
installation, qualification ou requête modèle n'accompagne cette intégration.

## Architecture et décisions

- `.codex-plugin/plugin.json` : manifeste de compatibilité Codex.
- `.claude-plugin/plugin.json` : manifeste Claude Code.
- `.agents/plugins/marketplace.json` et `.claude-plugin/marketplace.json` : catalogues de distribution.
- `.mcp.json` : unique déclaration du serveur `droit-francais`.
- `skills/` : sept runtimes figés et synchronisés.
- `upstream.json` et `scripts/` : provenance et contrôle de dérive.

Le format de compatibilité actuel reste volontairement utilisé pour le candidat 1.3.0. La migration vers le manifeste portable Agent Plugins fera l'objet d'un chantier séparé. Le plan de construction et les décisions d'architecture sont conservés dans `docs/`, dont l'[ADR DCP](docs/adr/0003-integration-candidate-dcp.md) et le [relevé d'intégration](docs/integration-dcp-2026-10-06.md).

## Licences

L'outil de développement Ponytail conserve sa licence MIT propre dans
`.agents/skills/ponytail/LICENSE` ; il ne fait pas partie des sept contenus
métier/juridiques embarqués ci-dessous.

Le plugin et ses sept contenus embarqués sont distribués sous licence [CC-BY-SA-4.0](LICENSE), avec attribution à `brissonjo-sudo`. Cette licence globale couvre notamment `dpm-fpt` et `dpo-ct`, qui ne disposaient pas auparavant d'une licence explicite dans leur dépôt amont. La licence DCP accompagne également sa copie.

Les textes, décisions et métadonnées récupérés depuis Légifrance ou Judilibre restent soumis aux droits, licences et conditions de réutilisation de leurs producteurs. Le texte CC-BY-SA-4.0 accompagne également la copie du runtime `recherche-juridique` dans `skills/recherche-juridique/LICENSE`.
