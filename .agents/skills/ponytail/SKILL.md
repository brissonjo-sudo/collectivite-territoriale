---
name: ponytail
description: Simplifier le développement du dépôt Collectivité territoriale avec Ponytail, seulement après une vérification en ligne de sa version avant chaque utilisation. Ne concerne pas les réponses métier du plugin.
license: MIT
---

# Ponytail — développement du dépôt uniquement

Avant toute utilisation, exécuter depuis la racine de ce dépôt :

```text
python .agents/skills/ponytail/scripts/check_version.py
```

Le script vérifie la dernière release stable publiée de l'amont officiel,
le commit de son étiquette et l'intégrité des fichiers installés. Il ne charge
les règles que si tous les contrôles réussissent, avec un code de sortie 0.

Si le code de sortie est différent de 0, si le réseau est indisponible, si
l'API refuse la requête ou si le résultat est incomplet : **ne pas utiliser
Ponytail**. Ne pas lire ni appliquer `rules.md` directement pour contourner
ce contrôle ; poursuivre avec les consignes habituelles du projet.

Recommencer avant chaque nouveau tour ou tâche où Ponytail serait appliqué,
même après une activation réussie dans la même session. Aucun succès antérieur
ne vaut pour une utilisation suivante. La règle de session persistante amont
ne dispense jamais de ce contrôle.

Après succès, appliquer les règles affichées uniquement au développement
de ce dépôt. Les instructions utilisateur, le français, la sécurité et les
conventions du projet restent prioritaires. Ne pas appliquer Ponytail aux
analyses juridiques ou métier des six skills distribués.

La provenance et les empreintes figurent dans `upstream-lock.json` ; la
licence MIT amont est conservée dans `LICENSE`. Une version obsolète nécessite
une mise à jour explicite de ces fichiers et une nouvelle vérification.
Ne pas télécharger ni exécuter automatiquement une nouvelle version.
