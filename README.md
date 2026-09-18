# Collectivité territoriale

Plugin Claude Code destiné aux collectivités territoriales françaises. Une installation donne accès à quatre skills métier :

| Skill | Domaine | Version embarquée |
|---|---|---|
| `collectivite-territoriale:dpm-fpt` | Police municipale et limites APJA | 1.0.5 |
| `collectivite-territoriale:drh-fpt` | Ressources humaines territoriales | 0.5.1 |
| `collectivite-territoriale:dpo-ct` | Protection des données | 0.2.1 |
| `collectivite-territoriale:dirfi-fpt` | Finances locales | 1.0.3 |

Le serveur MCP `droit-francais` est déclaré dans `.mcp.json` pour interroger Légifrance/Judilibre. Son utilisation peut demander une autorisation OAuth dans Claude Code. Le skill indépendant `recherche-juridique` n'est pas inclus.

## Installation et mise à jour

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

**Compte de l'auteur :** si ces quatre skills sont déjà synchronisés individuellement, ne pas installer ce plugin en plus. Les deux jeux coexistent sous des noms distincts et peuvent doubler le contexte chargé. Le plugin est prévu pour la distribution à d'autres collectivités.

## Sources et synchronisation

Chaque dossier `skills/<nom>/` est une copie exacte des fichiers d'exécution de son dépôt amont. `upstream.json` fige le dépôt, le commit, la version et les chemins inclus. Le fichier `references/cache-taux-seuils.md` de `dirfi-fpt`, exclu de son propre paquet de distribution, n'est pas embarqué.

Pour reproduire les copies depuis les dépôts locaux placés côte à côte :

```text
python scripts/sync_skills.py --local-repos C:\chemin\vers\repos
python scripts/check_sync.py --local-repos C:\chemin\vers\repos
```

Sans `--local-repos`, les scripts clonent les dépôts GitHub et vérifient les commits figés. La CI exécute `check_sync.py` et échoue si un fichier embarqué diffère, manque ou apparaît en plus. Une mise à jour d'un skill exige de changer son commit et sa version dans `upstream.json`, de relancer la synchronisation et d'incrémenter la version du plugin dans les deux manifestes.

## Validation locale

```text
claude plugin validate . --strict
python scripts/check_sync.py
```

Le plan de construction et l'historique des audits préalables sont conservés dans `docs/plan-plugin.md`. Les licences et conditions d'utilisation des contenus métier restent celles de leurs dépôts amont ; ce dépôt ne leur attribue pas une licence nouvelle.
