# Coactivation corrigée — r4 — 6 octobre 2026

**16 réponses achevées et 16 juges frais ; 0 refus de quota.**
La campagne comportementale est complète.
`release_ready=false`. Un échec technique de transport ou de sélection n'est pas
un score comportemental ; aucun verdict n'est inventé pour les refus de quota.

## Identité mesurée

- Commit plugin `b968c215e913457686b39718ebc9a2da9397663e` ; arbre `ba77dcc1f66493f97e52cc4610543494f34aa4f2`.
- 166 fichiers runtime ; 206 empreintes gelées vérifiées hors ligne.
- Modèle répondant `claude-sonnet-4-6` ; juges frais `gpt-6.1-sol` sans historique hérité.
- Suite inchangée : 16 scénarios, 124 invariants, 11 sélections forcées et 5 spontanées.
- Comparaison intégrale des paquets, écritures littérales, identités natives et spawns
  rejoués pour les seules réponses achevées. Le message initial chiffré du fournisseur
  n'est pas déclaré lisible ou vérifié.

## Résultats dérivés

Contrôles techniques : `{'passed': 13, 'failed': 3}`.
Verdicts sur réponses achevées : `{'bloque': 3, 'echec': 12, 'reussite': 1}`.
Statuts atomiques des jugements retenus : `{'true': 79, 'unknown': 16, 'false': 29}`.

| Cas | Contrôle technique | Exécution | Verdict indépendant |
|---|---|---|---|
| plugin-dsi-budget | passed | completed_response | bloque |
| plugin-dsi-incident-donnees | passed | completed_response | echec |
| plugin-dsi-reouverture | passed | completed_response | echec |
| plugin-dsi-reversibilite | passed | completed_response | echec |
| plugin-dsi-rssi-rh | passed | completed_response | echec |
| plugin-dsi-source-indisponible | passed | completed_response | echec |
| plugin-dsi-technique | passed | completed_response | bloque |
| plugin-dsi-videoprotection | passed | completed_response | echec |
| plugin-garde-fou-apja | passed | completed_response | echec |
| plugin-mcp-indisponible | passed | completed_response | reussite |
| plugin-prime-depart-retraite | passed | completed_response | echec |
| plugin-spontane-budget | failed | completed_response | echec |
| plugin-spontane-incident-donnees | failed | completed_response | echec |
| plugin-spontane-reversibilite | passed | completed_response | echec |
| plugin-spontane-rssi-rh | failed | completed_response | echec |
| plugin-violation-donnees | passed | completed_response | bloque |

## Limites et suite

Cette mesure antérieure porte sur le runtime dev.2. Ses résultats ne sont pas transférés au candidat dev.3.

Les retours primaires conservés établissent leur disponibilité, sans certifier
indépendamment chaque règle, son applicabilité ou sa vigueur. La revue juridique,
la recette DSI/RSSI et le smoke d'activation Codex restent ouverts. Les variantes
locales des six skills ne sont pas qualifiées par la mesure DSI autonome.
Les anciennes traces, tentatives de juges rejetées et scores restent conservés.
