# Utiliser le runtime commun avec Mistral Vibe

## Statut

Adaptation expérimentale pour **Vibe Code CLI 2.26.0**, Python 3.12.
Le smoke local charge les cinq skills et valide la configuration OAuth avec
Vibe réellement installé. Les appels MCP authentifiés et les huit réponses
comportementales ne sont pas encore qualifiés. Il ne s'agit pas d'une release
Vibe ou d'une validation de la 1.1.1 Claude/Codex.

Le dépôt complet est rejeté par l'inspecteur Vibe pour formats multiples.
Les adaptateurs Claude et Codex perdent les paramètres OAuth du MCP. La voie
ci-dessous configure donc directement les skills communs et un seul MCP dans
un profil dédié. Voir [ADR 0003](adr/0003-adaptation-vibe-par-configuration.md).

## Préparation

Dans un environnement Python 3.12, installer la version contrôlée :

```bash
python -m pip install mistral-vibe==2.26.0
vibe --version
python scripts/check_vibe.py
```

Depuis une copie du dépôt au commit choisi, créer un **nouveau** profil :

```bash
python scripts/configure_vibe.py --home ~/.vibe-collectivite
```

Le générateur pointe vers les fichiers de cette copie : la conserver et
regénérer dans un nouveau dossier si son emplacement ou sa configuration
change. Il refuse d'écraser une configuration différente ou un dossier
non vide. Les cinq noms de skills sont sans préfixe de plugin dans cette voie.

La configuration reprend le client public et le port de `.mcp.json` comme
candidats, sans affirmer leur compatibilité côté Auth0. Pour un client public
préenregistré propre à Vibe :

```bash
python scripts/configure_vibe.py --home ~/.vibe-collectivite \
  --client-id IDENTIFIANT_PUBLIC_VIBE --callback-port 44956
```

Le callback exact de Vibe est `http://127.0.0.1:44956/callback`, avec le port
choisi. Il doit être autorisé sur l'application OAuth, ainsi que l'accès à
l'API et la connexion de l'utilisateur. `localhost` et `127.0.0.1` ne sont
pas interchangeables dans une allow-list de callback. Ne pas ouvrir la DCR
ni désactiver l'authentification pour contourner un refus de client.

Sur un poste doté d'un trousseau système fonctionnel, lancer :

```bash
VIBE_HOME="$HOME/.vibe-collectivite" vibe
```

Dans Vibe, utiliser `/mcp`, puis `/mcp login ct_vibe_droit_francais` si
nécessaire. L'identifiant de client est public ; aucun secret client ou clé
PISTE ne doit être saisi dans le générateur. Le compte Vibe ou la clé Mistral
se configure dans le parcours normal du client, hors de ce dépôt.

Avant de conclure au succès : vérifier les cinq skills, charger une référence,
puis rechercher **et récupérer** un article avec une provenance et une version.
Un statut connecté ou une liste d'outils ne prouve pas la récupération.

## Mode sans MCP

```bash
python scripts/configure_vibe.py --home ~/.vibe-collectivite-offline --without-mcp
VIBE_HOME="$HOME/.vibe-collectivite-offline" vibe
```

Le MCP est absent de ce profil. En usage interactif, `web_fetch` reste soumis
à autorisation ; cette voie n'est pas le scénario de campagne qui interdit
également le Web.

## Campagne guidée et naturelle

Le lanceur `scripts/run_vibe_campaign.py` utilise les API publiques du runtime
Vibe 2.26.0. La voie par commandes publiques `vibe -p` refuse automatiquement
les callbacks en mode non interactif ; le lanceur dédié répond donc seulement
aux callbacks de lecture internes et, pour le cas RGPD, aux deux origines
officielles autorisées. Il ne donne aucune autorisation générale d'exécution.

Prérequis supplémentaires : clé Mistral disponible dans l'environnement,
trousseau OAuth fonctionnel pour les cas nominaux et authentification préalable
de l'alias MCP avec le même client public. Le lanceur ne copie pas les fichiers
`.env` et ne lance pas de connexion OAuth interactive. Les portées OAuth sont
vides, conformément à la déclaration actuelle ; leur adéquation au service
reste à vérifier lors de l'appel réel.

Exemple de **pilote**, dont le plafond de coût reste à calibrer :

```bash
python scripts/run_vibe_campaign.py \
  --case plugin-garde-fou-apja --mode guided \
  --model mistral-medium-3.5 --max-price 1 \
  --output tests/evidence/.work/vibe-apja-guided.json
```

Reprendre le même cas en `--mode natural`, puis les trois autres IDs :

- `plugin-prime-depart-retraite`
- `plugin-violation-donnees`
- `plugin-mcp-indisponible`

Le mode naturel transmet exactement la demande métier, sans imposer les
skills. Les modes nominal/dégradé et les restrictions Web restent effectifs.
Exécuter les huit runs séquentiellement, dans de nouveaux fichiers. Une
configuration de client différente doit être passée avec les mêmes options
`--client-id` et `--callback-port` que le profil authentifié.

Les prix du modèle utilisés pour le plafond sont ceux de la configuration
Vibe installée ; vérifier leur actualité. L'alias de l'exemple désigne
`mistral-vibe-cli-latest`, pas une version serveur immuable. Le lanceur
consigne la configuration et, si disponible, le modèle observé ; il ne
certifie pas la version servie. Ne pas comparer des campagnes comme si cette
version était figée sans preuve supplémentaire.

Le lanceur filtre les outils, désactive le sampling MCP, utilise un profil
temporaire sans persistance de conversation, borne les tours/tokens/coût/durée
et refuse les callbacks hors périmètre. `web_fetch` vérifie les redirections
dans Vibe 2.26.0 et refuse un changement d'origine. Ne pas ajouter `--yolo`.

Les traces conservées contiennent les états utiles, les activations, chemins
relatifs des références, sources officielles sans paramètres et texte de la
réponse. Les sorties d'outils, arguments MCP, erreurs brutes et raisonnements
ne sont pas conservés. Les métriques indisponibles restent `null`.

Un échec de prérequis produit `blocked` et un code de sortie 2 ; une limite
ou erreur technique produit `interrupted`. Un run techniquement conforme
produit `technical_passed_pending_review`, **jamais** un verdict métier ou
une autorisation de release. Relire la réponse et la pertinence des sources,
renseigner les invariants et consigner la revue humaine séparément.

## Validation et mise à jour

```bash
python -m unittest discover -s tests -p test_vibe.py
python scripts/check_vibe.py
python scripts/check_sync.py
```

La CI Vibe contrôle la version installée et la configuration sans appeler de
modèle ni le serveur juridique. La suite globale garde sa barrière de release
1.1.1 : son échec préexistant ne doit pas être masqué par l'adaptation Vibe.

Les fichiers `skills/`, `upstream.json`, `.mcp.json`, les overlays et les
manifestes Claude/Codex ne sont pas modifiés par cette adaptation. Les
corrections métier ou un paquet natif feront l'objet d'un chantier distinct.

Sources : [skills Vibe](https://docs.mistral.ai/vibe/code/cli/skills),
[MCP Vibe](https://docs.mistral.ai/vibe/code/cli/mcp-servers),
[release 2.26.0](https://github.com/mistralai/mistral-vibe/releases/tag/v2.26.0),
[documentation intégrée](https://github.com/mistralai/mistral-vibe/blob/v2.26.0/vibe/plugins/builtins/vibe/skills/vibe/SKILL.md).
