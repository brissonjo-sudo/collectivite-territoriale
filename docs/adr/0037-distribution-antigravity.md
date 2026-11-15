# ADR 0037 : distribution Antigravity par manifeste natif à la racine

Date : 2026-11-15. Décisions de Jo (Jonathan BRISSON, @brissonjo-sudo).

## Contexte

Le plugin est distribué pour Claude Code (`.claude-plugin/`) et Codex
(`.codex-plugin/`). Les deux lisent la même racine : `skills/` et `.mcp.json`.

Google Antigravity reconnaît comme plugin natif tout dossier qui contient un
`plugin.json`. Il charge alors `skills/` et `mcp_config.json` depuis la racine
de ce dossier. Source : documentation intégrée au produit,
`builtin/skills/agy-customizations/docs/plugins.md` et `mcp_servers.md`,
consultée le 2026-11-15.

Un prototype posé par Jo le 2026-11-15 a donné les résultats suivants. Il
s'agit d'un clone de `c63afc2` avec un `plugin.json` racine et un
`mcp_config.json` passant par `npx -y mcp-remote` :

- les sept skills sont visibles ;
- le serveur juridique ne se connecte pas.

Cause plausible : l'enregistrement dynamique de clients (DCR) est fermé sur le
locataire Auth0, et `mcp-remote` n'avait pas de client statique. Ce pont
exécutait en outre un paquet npm non épinglé à chaque démarrage.

Pour un serveur distant avec OAuth, Antigravity accepte `serverUrl` et un objet
`oauth` contenant `clientId`, éventuellement `clientSecret`. Sources :

- Google Workspace, « Configure the Docs MCP server » (adresse de retour
  `https://antigravity.google/oauth-callback`) ;
- CloudBees Unify, « Connect Google Antigravity » (client public, `clientId`
  seul).

Les deux pages ont été consultées le 2026-11-15. Ce sont des sources tierces :
la doc intégrée locale n'en parle pas.

## Décision

1. Le manifeste est un `plugin.json` à la racine : c'est le seul emplacement
   éprouvé par le prototype. Ses champs se limitent à ceux que lit
   Antigravity. Son identité et sa version suivent les deux autres
   manifestes, ce que vérifie `tests/test_antigravity_plugin.py`.
2. `mcp_config.json` déclare `droit-francais` par `serverUrl`, avec le client
   public `tpc_gCoyj4qPSuyrg1ZZWDyp4D`, celui de `.mcp.json`. Il n'a ni
   secret, ni `npx`, ni pont `mcp-remote`. Jo ajoute l'adresse de retour
   Antigravity à ce client dans Auth0.
3. La version ne change pas, et les deux nouveaux fichiers restent hors de la
   configuration comparée au smoke. Le runtime `skills/` et la preuve
   `release-1.5.2.json` sont donc inchangés, et la barrière reste verte.
4. L'installation se fait par un clone de l'étiquette publiée dans
   `~/.gemini/config/plugins/collectivite-territoriale`. La notice vise la
   prochaine étiquette, v1.5.3, et la marque « à venir » jusque-là.

## Recette du 2026-11-15

Recette faite sur le clone local de Jo, avec les deux fichiers de cette
branche.

1. Le premier essai a échoué en « Callback URL mismatch », d'après le journal
   Auth0. Antigravity envoyait bien `redirect_uri` =
   `https://antigravity.google/oauth-callback`, avec le client
   `tpc_gCoyj4…`, PKCE S256 et `resource` égal à l'URL du serveur MCP. Cette
   adresse manquait seulement à la liste du client.
2. Jo a ajouté cette adresse aux *Allowed Callback URLs* du client.
   L'authentification a ensuite **réussi**, selon le constat de Jo.

Ce qui reste à faire ou à surveiller :

- **Non vérifié** : un appel d'outil réel, `search` puis `fetch`, à consigner
  ici une fois fait.
- **À surveiller** : la requête d'autorisation part avec un `scope` vide, sans
  `offline_access`. Une reconnexion pourrait donc être demandée à
  l'expiration du jeton.

## Conséquences
- Un même client sert trois hôtes. Révoquer ce client coupe Claude Code, Codex
  et Antigravity en même temps.
- Le format est natif : aucune étape de conversion depuis le format Claude
  Code. Les hooks éventuels devraient être placés à la racine (`hooks.json`).
