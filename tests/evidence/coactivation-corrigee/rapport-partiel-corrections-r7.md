# Coactivation corrigée — mesure partielle r7 — 7 octobre 2026

**Six réponses capturées et six juges frais sur seize scénarios.**
Trois nominaux signalent `needs-auth` pour `droit-francais` dans leurs événements init.
Le lanceur nominal a été interrompu sur le cinquième cas : aucune réponse de ce cas
n’est capturée. Neuf autres cas ne sont pas exécutés, selon le reçu de l’orchestrateur.
La campagne comportementale est inachevée ; `release_ready=false`.

## Identité et portée vérifiées

- Commit plugin `d1ab287376c8ae3605b0459850210be4a4e91bf9` ; arbre `c3439f3b31d24a159b6bd93c4c40c6f042c709f4`.
- 166 fichiers runtime ; 211 empreintes gelées vérifiées hors ligne.
- Réponses mesurées : ordres 1, 2, 3, 4, 11 et 12 de la suite inchangée.
- Six paquets intégraux reconstruits, six écritures de jugements et six sessions
  natives rejouées ; parent filtré limité aux six spawns sans historique.
- Les dix scénarios sans réponse capturée restent non jugés. Aucun score antérieur
  n’est transféré et aucun message initial opaque du fournisseur n’est déclaré lisible.

## Résultats dérivés

Contrôles techniques sur les six réponses : `{'failed': 4, 'passed': 2}`.
Verdicts des six juges : `{'echec': 5, 'reussite': 1}`.
Statuts atomiques retenus : `{'true': 28, 'false': 5, 'unknown': 10}`.
Observations `needs-auth` : `['plugin-prime-depart-retraite', 'plugin-garde-fou-apja', 'plugin-violation-donnees']`.

| Cas | Contrôle technique | Exécution | Verdict indépendant |
|---|---|---|---|
| plugin-prime-depart-retraite | failed | completed_response | echec |
| plugin-garde-fou-apja | failed | completed_response | echec |
| plugin-violation-donnees | failed | completed_response | echec |
| plugin-mcp-indisponible | passed | completed_response | reussite |
| plugin-dsi-incident-donnees | not_measured | controlled_interruption_without_response | non jugé |
| plugin-dsi-rssi-rh | not_measured | not_executed | non jugé |
| plugin-dsi-videoprotection | not_measured | not_executed | non jugé |
| plugin-dsi-budget | not_measured | not_executed | non jugé |
| plugin-dsi-reversibilite | not_measured | not_executed | non jugé |
| plugin-dsi-reouverture | not_measured | not_executed | non jugé |
| plugin-dsi-technique | failed | completed_response | echec |
| plugin-dsi-source-indisponible | passed | completed_response | echec |
| plugin-spontane-incident-donnees | not_measured | not_executed | non jugé |
| plugin-spontane-rssi-rh | not_measured | not_executed | non jugé |
| plugin-spontane-budget | not_measured | not_executed | non jugé |
| plugin-spontane-reversibilite | not_measured | not_executed | non jugé |

## Limites et suite

Les trois réponses nominales sans primaire ne deviennent pas des réussites dégradées.
Les trois scénarios qui désactivent volontairement MCP conservent leur propre barème.
Le reçu `interruption-controlee-r7.json` distingue le cas interrompu des neuf cas non
exécutés ; il est une déclaration de l’orchestrateur, sans réponse reconstruite.
La disponibilité d’un texte primaire ne certifie pas indépendamment son applicabilité
ou sa vigueur. La revue juridique, la recette DSI/RSSI et le smoke d’activation Codex
restent ouverts. Les variantes locales des six skills ne sont pas qualifiées par
la mesure DSI autonome. Les anciennes traces et tentatives restent conservées.
