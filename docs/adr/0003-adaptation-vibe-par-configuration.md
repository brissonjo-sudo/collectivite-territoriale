# ADR 0003 : adaptation Vibe par configuration dédiée

- Date : 2026-10-07
- Statut : accepté pour l'adaptation expérimentale ; qualification nominale à réaliser
- Base étudiée : candidat 1.1.1, commit cad8bbdbc1db2163c758fb46ef3e745a18c9c957
- Hôte contrôlé : Mistral Vibe 2.26.0, Python 3.12

## Problème reproduit

L'inspecteur et le résolveur réels de Vibe refusent le dépôt comme ambigu :
il contient `.claude-plugin/plugin.json` et `.codex-plugin/plugin.json`.
Les deux adaptateurs pris séparément acceptent les skills ou leur racine,
mais traduisent le MCP en authentification statique vide. Les paramètres
`oauth.clientId` et `oauth.callbackPort` ne sont pas repris.

Ajouter un fichier `.vibe-plugin/plugin.json` ne correspond pas au format
natif documenté. Ajouter un manifeste natif à la racine serait un chantier
de migration de distribution et de validation des trois hôtes. Il n'est
pas nécessaire pour tester les capacités métier dans Vibe.

## Décision

Générer un profil utilisateur Vibe dédié, avec `skill_paths` pointant vers
la racine commune `skills/`, une allow-list des cinq noms et une déclaration
MCP OAuth explicite dérivée de `.mcp.json`. Aucun runtime métier n'est copié
ou modifié. Le profil habituel n'est pas fusionné ou écrasé.

L'identifiant et le port du client public sont traduits sans secret. Un
client Vibe distinct et un port différent peuvent être fournis explicitement.
Le callback émis par Vibe est `http://127.0.0.1:PORT/callback` ; il doit être
autorisé côté serveur d'identité. La traduction locale ne prouve pas cette
autorisation ni le succès de l'échange OAuth.

L'alias MCP propre à cette adaptation évite la réutilisation implicite du
stockage de jetons sous l'alias d'une autre intégration. Le sampling MCP est
désactivé. Un profil de test peut supprimer intégralement le MCP.

Les compétences s'appellent `dpm-fpt`, `drh-fpt`, `dpo-ct`, `dirfi-fpt` et
`recherche-juridique` dans cette voie : pas de namespace de plugin. Le nom
qualifié utilisé par Claude/Codex reste inchangé.

## Mesure et limites

Un smoke avec Vibe installé valide la configuration, le chargement des cinq
instructions et la lisibilité des références. Les essais comportementaux
utilisent le runtime public de Vibe, en sessions isolées, avec traces
assainies et permissions limitées. Les modes guidé et naturel restent séparés.
Les quatre demandes et leurs invariants sont conservés.

Le code du runtime est figé sur Vibe 2.26.0. Toute mise à jour exige de
rejouer le smoke et de revoir les événements et permissions. Un run interrompu
ou bloqué ne devient pas un succès. Le verdict juridique demeure soumis à
revue humaine, et aucune preuve Vibe ne clôt la barrière Claude/Codex 1.1.1.

Le profil dédié est une adaptation de configuration des skills et du MCP,
pas une installation native du paquet plugin Vibe. Un paquet natif pourra
être étudié après la qualification des usages, si la distribution l'exige.
