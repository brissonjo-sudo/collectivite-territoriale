# Collectivité territoriale

Source des plugins Claude Code et Codex destinés aux collectivités territoriales françaises. Elle regroupe quatre skills métier et une méthode juridique transverse :

| Skill | Domaine | Version embarquée |
|---|---|---|
| `collectivite-territoriale:dpm-fpt` | Police municipale et limites APJA | 1.0.5 |
| `collectivite-territoriale:drh-fpt` | Ressources humaines territoriales | 0.5.1 |
| `collectivite-territoriale:dpo-ct` | Protection des données | 0.2.1 |
| `collectivite-territoriale:dirfi-fpt` | Finances locales | 1.0.4 |
| `collectivite-territoriale:recherche-juridique` | Recherche et vérification du droit français | 3.5.0 |

Le serveur MCP `droit-francais` est déclaré dans `.mcp.json` pour interroger Légifrance/Judilibre. Son utilisation peut demander une autorisation OAuth dans Claude Code. Le skill `recherche-juridique` complète ce serveur par la méthode de vérification de vigueur, de provenance et de citation ; l'accès au MCP et la méthode ne se substituent pas l'un à l'autre.

## Claude Code : installation et mise à jour

Dans Claude Code :

```text
/plugin marketplace add brissonjo-sudo/collectivite-territoriale
/plugin install collectivite-territoriale@collectivite-territoriale
```

Pour actualiser une installation existante après une nouvelle version publiée :

```text
/plugin marketplace update collectivite-territoriale
/plugin update collectivite-territoriale@collectivite-territoriale
```

Les mises à jour automatiques peuvent être désactivées pour une marketplace tierce. Vérifier la version affichée après la mise à jour.

**Compte de l'auteur :** si ces cinq skills sont déjà synchronisés individuellement, ne pas installer ce plugin en plus. Les deux jeux coexistent sous des noms distincts et peuvent doubler le contexte chargé. Le plugin est prévu pour la distribution à d'autres collectivités.

## Codex / ChatGPT

La version Codex est décrite par `.codex-plugin/plugin.json`. Elle réutilise les mêmes dossiers `skills/` et le même serveur juridique `.mcp.json` que la version Claude Code. Les cinq skills sont exposés sous le nom `collectivite-territoriale:<nom>`.

La marketplace Codex est déclarée dans `.agents/plugins/marketplace.json`. Elle référence la racine de ce même dépôt via Git : aucune seconde copie des skills n'est nécessaire. Pour l'ajouter et installer le plugin dans Codex :

```text
codex plugin marketplace add brissonjo-sudo/collectivite-territoriale
codex plugin add collectivite-territoriale@collectivite-territoriale
```

Pour les mises à jour ultérieures, utiliser `codex plugin marketplace upgrade collectivite-territoriale`, puis mettre à jour le plugin dans Codex. Ouvrir une nouvelle conversation après installation ou mise à jour afin de charger ses skills et outils. L'accès au serveur MCP juridique peut nécessiter une autorisation.

Cette marketplace Git est destinée à Codex CLI et à l'application de bureau ChatGPT ; elle ne publie pas le plugin dans l'annuaire public universel. Pour un espace de travail ChatGPT, un administrateur doit importer la marketplace depuis l'URL du dépôt. Comme le plugin déclare un serveur MCP, un tel import est utilisable dans l'application de bureau uniquement.

**Compte de l'auteur :** les cinq skills sont déjà présents individuellement. Ne pas installer aussi ce plugin, afin d'éviter les doublons et le surcoût de contexte. L'ajout de la marketplace seule n'installe pas le plugin.

## Sources et synchronisation

Chaque dossier `skills/<nom>/` est une copie exacte des fichiers d'exécution de son dépôt amont. `upstream.json` fige le dépôt, le commit, la version et les chemins inclus. Le fichier `references/cache-taux-seuils.md` de `dirfi-fpt`, exclu de son propre paquet de distribution, n'est pas embarqué. Pour `recherche-juridique`, la racine canonique `skill/` est aplatie dans `skills/recherche-juridique/` et la licence amont est copiée avec le runtime ; aucun manifeste, serveur MCP ou fichier `.env` du dépôt juridique n'est dupliqué.

Pour reproduire les copies depuis les dépôts locaux placés côte à côte :

```text
python scripts/sync_skills.py --local-repos C:\chemin\vers\repos
python scripts/check_sync.py --local-repos C:\chemin\vers\repos
```

Sans `--local-repos`, les scripts clonent les dépôts GitHub et vérifient les commits figés. La CI exécute `check_sync.py` et échoue si un fichier embarqué diffère, manque ou apparaît en plus. Une mise à jour d'un skill exige de changer son commit et sa version dans `upstream.json`, de relancer la synchronisation et d'incrémenter la version du plugin dans les deux manifestes.

## Validation locale

```text
claude plugin validate .
python -m unittest discover -s tests
python scripts/check_sync.py
```

Le manifeste Codex est aussi vérifié localement avec le validateur du skill système `plugin-creator`.

Le cas de non-régression `tests/cas-plugin.json` vérifie la coordination
DirFi/DRH/juridique sur une gratification de départ à la retraite, le garde-fou
APJA sur une demande d'acte réservé à l'OPJ et la réponse DPO à une violation
de données.

Le plan de construction et l'historique des audits préalables sont conservés dans `docs/plan-plugin.md`. Les licences et conditions d'utilisation des contenus métier restent celles de leurs dépôts amont ; ce dépôt ne leur attribue pas une licence nouvelle. Le runtime de `recherche-juridique` est attribué à `brissonjo-sudo` et reste distribué sous CC-BY-SA-4.0, dont le texte accompagne sa copie dans `skills/recherche-juridique/LICENSE`.
