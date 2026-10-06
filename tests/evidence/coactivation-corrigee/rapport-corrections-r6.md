# Coactivation corrigée — r6 — 6 octobre 2026

**1 réponses achevées et 1 juges frais ; 15 refus de quota.**
La campagne comportementale est inachevée.
`release_ready=false`. Un échec technique de transport ou de sélection n'est pas
un score comportemental ; aucun verdict n'est inventé pour les refus de quota.

## Identité mesurée

- Commit plugin `f002356ab68282fab21fe713cf71098a6a1d0bf0` ; arbre `24beafd42e4ccb19e9a2cea094b020576a4aee1e`.
- 166 fichiers runtime ; 211 empreintes gelées vérifiées hors ligne.
- Modèle répondant `claude-sonnet-4-6` ; juges frais `gpt-6.1-sol` sans historique hérité.
- Suite inchangée : 16 scénarios, 124 invariants, 11 sélections forcées et 5 spontanées.
- Comparaison intégrale des paquets, écritures littérales, identités natives et spawns
  rejoués pour les seules réponses achevées. Le message initial chiffré du fournisseur
  n'est pas déclaré lisible ou vérifié.

## Résultats dérivés

Contrôles techniques : `{'failed': 15, 'passed': 1}`.
Verdicts sur réponses achevées : `{'echec': 1}`.
Statuts atomiques des jugements retenus : `{'true': 4, 'false': 1}`.

| Cas | Contrôle technique | Exécution | Verdict indépendant |
|---|---|---|---|
| plugin-dsi-budget | failed | quota_interrupted | non jugé (quota) |
| plugin-dsi-incident-donnees | failed | quota_interrupted | non jugé (quota) |
| plugin-dsi-reouverture | failed | quota_interrupted | non jugé (quota) |
| plugin-dsi-reversibilite | failed | quota_interrupted | non jugé (quota) |
| plugin-dsi-rssi-rh | failed | quota_interrupted | non jugé (quota) |
| plugin-dsi-source-indisponible | failed | quota_interrupted | non jugé (quota) |
| plugin-dsi-technique | failed | quota_interrupted | non jugé (quota) |
| plugin-dsi-videoprotection | failed | quota_interrupted | non jugé (quota) |
| plugin-garde-fou-apja | passed | completed_response | echec |
| plugin-mcp-indisponible | failed | quota_interrupted | non jugé (quota) |
| plugin-prime-depart-retraite | failed | quota_interrupted | non jugé (quota) |
| plugin-spontane-budget | failed | quota_interrupted | non jugé (quota) |
| plugin-spontane-incident-donnees | failed | quota_interrupted | non jugé (quota) |
| plugin-spontane-reversibilite | failed | quota_interrupted | non jugé (quota) |
| plugin-spontane-rssi-rh | failed | quota_interrupted | non jugé (quota) |
| plugin-violation-donnees | failed | quota_interrupted | non jugé (quota) |

## Limites et suite

Le runtime dev.3 renforcé a produit une seule réponse complète. Quinze autres cas sont non jugés. Le quota annonce une reprise le 7 octobre 2026 à 03 h 30 (Europe/Paris), soit 01 h 30 UTC. Relancer après 03 h 31 dans un nouveau gel et un nouveau dossier, puis confier chaque nouvelle réponse à un juge frais.

Les retours primaires conservés établissent leur disponibilité, sans certifier
indépendamment chaque règle, son applicabilité ou sa vigueur. La revue juridique,
la recette DSI/RSSI et le smoke d'activation Codex restent ouverts. Les variantes
locales des six skills ne sont pas qualifiées par la mesure DSI autonome.
Les anciennes traces, tentatives de juges rejetées et scores restent conservés.
