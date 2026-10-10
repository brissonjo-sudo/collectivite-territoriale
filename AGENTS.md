# Consignes de développement — Collectivité territoriale

Communiquer en français et respecter les conventions et la sécurité du projet.
Les six skills métier/juridiques restent des copies figées selon `upstream.json`.
Les scripts de synchronisation, les STOP, les frontières et les preuves de
qualification demeurent applicables.

## Ponytail : vérification obligatoire avant chaque utilisation

Le skill de développement local se trouve dans `.agents/skills/ponytail/`.
Avant chaque application de Ponytail, y compris à un nouveau tour d'une session
déjà active, exécuter depuis la racine du dépôt :

```text
python .agents/skills/ponytail/scripts/check_version.py
```

Appliquer les règles affichées seulement après un code de sortie 0 du contrôle
effectué pour cette utilisation. Ne jamais réutiliser un succès antérieur.
En cas de version obsolète, de fichiers altérés ou d'actualité non vérifiable,
**ne pas utiliser Ponytail** ; continuer avec les consignes normales du dépôt.
Ne pas lire `rules.md` directement ni activer les règles amont persistantes
pour contourner cette vérification.

Ponytail concerne uniquement le développement du dépôt, pas les réponses
métier du plugin. Aucun hook amont, réglage global, secret ou outil Ponytail
supplémentaire n'est installé. La mise à jour est explicite, jamais automatique.
