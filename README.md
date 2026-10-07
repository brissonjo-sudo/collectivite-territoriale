# Collectivité territoriale

[![Validation du plugin](https://github.com/brissonjo-sudo/collectivite-territoriale/actions/workflows/ci.yml/badge.svg)](https://github.com/brissonjo-sudo/collectivite-territoriale/actions/workflows/ci.yml)

Plugin Claude Code et Codex destiné aux collectivités territoriales françaises.
Le dépôt prépare cinq expertises métier, une méthode de recherche juridique
sourcée et un accès optionnel à Légifrance/Judilibre. La distribution gelée
1.1.1 expose encore quatre expertises métier et la méthode juridique.

> **Statut :** DCP 0.1.1 mesuré sur 28 cas autonomes : 27 réussites et une demi-réussite selon le juge automatique. Neuf contrôles de coactivation Codex vérifiés après correction de faux positifs du lanceur ; **non relu par un praticien**. Réserve DPO et sources à relire. Installation locale et découverte des six skills vérifiées séparément. Les catalogues distribuent toujours `v1.1.1`, **non qualifiée**. [Qualification du correctif](docs/qualification-correctif-2026-10-07.md) et [conditions de publication](docs/publication.md).

Ce plugin aide à qualifier une situation, identifier les expertises à mobiliser et produire une réponse traçable. Il ne remplace ni la validation d'un juriste, ni le contrôle de l'autorité compétente, ni la vérification des textes officiels en vigueur.

## Contenu du candidat 1.2.0

| Skill | Domaine | Version embarquée |
|---|---|---:|
| `collectivite-territoriale:dpm-fpt` | Police municipale et limites APJA | 1.0.5 |
| `collectivite-territoriale:drh-fpt` | Ressources humaines territoriales | 0.6.0 |
| `collectivite-territoriale:dpo-ct` | Protection des données | 0.2.1 |
| `collectivite-territoriale:dirfi-fpt` | Finances locales | 1.0.4 |
| `collectivite-territoriale:dcp-fpt` | Commande publique, mesuré autonomement, à relire | 0.1.1 |
| `collectivite-territoriale:recherche-juridique` | Recherche et vérification du droit français | 3.5.0 |

L'étiquette distribuée `v1.1.1` contient les cinq skills déjà présents,
sans DCP. Les essais DCP doivent charger le checkout candidat local ; une
mise à jour de la marketplace continue de récupérer le runtime gelé 1.1.1.

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

`dsi-fpt` reste externe au plugin : la frontière DCP sur les spécifications,
niveaux de service, réversibilité et exécution technique d'un achat informatique
est un renvoi vers cette compétence. Sa disponibilité et son activation ne
doivent pas être présumées. En son absence, DCP signale la frontière et arrête
ce volet. Aucune copie de DSI ni modification des autres skills n'accompagne
cette intégration candidate.

Le plugin traite le droit français et l'aide à la décision dans le contexte des collectivités territoriales. Toute conclusion sensible doit être confrontée à la source officielle et aux circonstances du dossier.

La collecte et la transmission éventuelles de données sont décrites dans la [politique de confidentialité](PRIVACY.md). Le serveur MCP peut être désactivé lorsque la transmission d'une requête juridique au service distant n'est pas souhaitée.

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

> **Compte de l'auteur :** ne pas installer ce plugin en parallèle de ses six skills individuels. Les deux jeux coexistent sous des noms distincts et peuvent doubler le contexte chargé.

## Sources et reproductibilité

Chaque dossier `skills/<nom>/` provient des fichiers d'exécution d'un commit amont figé. `upstream.json` fixe le dépôt, le commit, la version de base et les chemins inclus. `dirfi-fpt`, `drh-fpt` et `dcp-fpt` restent des copies exactes. `dpm-fpt`, `dpo-ct` et `recherche-juridique` sont des **variantes locales du plugin**, avec les corrections de méthode conservées dans `overlays/` et déclarées dans `instruction_overlays`.

Chaque surcharge est liée à l'empreinte SHA-256 exacte de son fichier amont et de son texte local ; elle est insérée une seule fois à une ancre unique. Tout changement de base, de correction ou d'ancre bloque la synchronisation tant qu'il n'a pas été revu. Les versions internes identifient la base amont, pas une nouvelle release de ces dépôts. Le commit du plugin identifie la variante complète. Aucun dépôt amont n'est modifié par ces surcharges.

Pour `recherche-juridique`, la racine canonique `skill/` est aplatie dans `skills/recherche-juridique/`. Sa licence est copiée avec le runtime ; aucun manifeste, serveur MCP, fichier `.env` ou autre fichier de dépôt amont n'est dupliqué. Le fichier `references/cache-taux-seuils.md` de `dirfi-fpt`, exclu de son propre paquet de distribution, n'est pas embarqué.

Pour DCP 0.1.1, le commit correctif est figé :
`caef7fd9e680dc28056998532d24befa0e8680ec`. Les 30 fichiers de son paquet
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
saute que `ReleaseGateTests`. Le job **Qualification de publication** force
`CT_SAUTER_BARRIERE=0` et conserve le verrou en échec pour une version non
qualifiée. Sans cette variable, la découverte complète exécute aussi le verrou.

Sous un shell Unix, l'équivalent pour l'intégration est
`CT_EXIGER_ETIQUETTE=1 CT_SAUTER_BARRIERE=1 python -m unittest discover -s tests`.

Le manifeste Codex est également contrôlé avec le validateur du skill système `plugin-creator`. Les cas de `tests/cas-plugin.json` couvrent notamment :

- le garde-fou APJA sur une demande d'acte réservé à l'OPJ ;
- une gratification de départ mobilisant finances, RH et recherche juridique ;
- une violation de données mobilisant DPO et recherche juridique ;
- le comportement dégradé lorsque le MCP juridique est désactivé.
- les deux STOP DCP, les frontières financières et données, la dépendance DSI
  externe et le comportement DCP sans accès aux sources officielles.

La release 1.2.0 exige des traces comportementales en conversations fraîches,
la mesure DCP et la relecture praticien. Le statut courant est conservé dans
`tests/evidence/release-1.2.0.json`. Les preuves historiques ne qualifient pas
le correctif. Le test `test_barriere_de_release_comportementale` reste en
échec tant que `release_ready` est faux ; les autres tests doivent réussir.

Le lanceur `scripts/run_plugin_campaign.py` exécute les neuf scénarios dans
des sessions non persistées, impose les activations qualifiées attendues,
désactive les connecteurs juridiques globaux et ne conserve qu'une trace JSONL
assainie dans `tests/evidence/.work/`. Cette sortie reste soumise à une revue
humaine des invariants métier avant d'être promue en preuve de release.

À la demande de l'auteur, la campagne actuelle utilise Codex et
`scripts/run_codex_campaign.py` : copies natives en workspace frais,
lectures ordonnées par segments vérifiés, MCP juridique propre au processus
dans les sept cas nominaux, MCP absent dans les deux cas dégradés. La connexion
Codex existante suffit ; aucune connexion Claude n'est requise pour ce profil.
Le profil ne teste pas le déclenchement implicite ou l'activation Skill de
Claude. L'installation locale avec CODEX_HOME distinct a été testée sans
compte ; la réponse modèle/MCP depuis le plugin installé reste à qualifier.
La mesure autonome DCP avec web garde son profil distinct.

## Architecture et décisions

- `.codex-plugin/plugin.json` : manifeste de compatibilité Codex.
- `.claude-plugin/plugin.json` : manifeste Claude Code.
- `.agents/plugins/marketplace.json` et `.claude-plugin/marketplace.json` : catalogues de distribution.
- `.mcp.json` : unique déclaration du serveur `droit-francais`.
- `skills/` : six runtimes figés et synchronisés.
- `upstream.json` et `scripts/` : provenance et contrôle de dérive.

Le format de compatibilité actuel reste volontairement utilisé pour le candidat 1.2.0. La migration vers le manifeste portable Agent Plugins fera l'objet d'un chantier séparé. Le plan de construction et les décisions d'architecture sont conservés dans `docs/`, dont l'[ADR DCP](docs/adr/0003-integration-candidate-dcp.md) et le [relevé d'intégration](docs/integration-dcp-2026-10-06.md).

## Licences

Le plugin et ses six contenus embarqués sont distribués sous licence [CC-BY-SA-4.0](LICENSE), avec attribution à `brissonjo-sudo`. Cette licence globale couvre notamment `dpm-fpt` et `dpo-ct`, qui ne disposaient pas auparavant d'une licence explicite dans leur dépôt amont. La licence DCP accompagne également sa copie.

Les textes, décisions et métadonnées récupérés depuis Légifrance ou Judilibre restent soumis aux droits, licences et conditions de réutilisation de leurs producteurs. Le texte CC-BY-SA-4.0 accompagne également la copie du runtime `recherche-juridique` dans `skills/recherche-juridique/LICENSE`.
