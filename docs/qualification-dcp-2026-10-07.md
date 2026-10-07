# Qualification candidate 1.2.0 — 2026-10-07

## Périmètre contrôlé

Candidat fusionné `85011f7f86b488330fe00ff7a30ce42d6dbe9a84` : six skills,
DCP 0.1.0 figé à `eeb1cb1`, DRH 0.6.0. Les neuf scénarios de coactivation,
la mesure autonome DCP, le smoke et la relecture métier restent distincts.
La distribution reste v1.1.1 sur cad8bbd ; aucun nouveau tag ni installation.

## Contrôles réels

Claude Code 2.1.288 et Codex CLI 0.160.0 : options contrôlées sur leur aide.
Une recherche du MCP juridique réussit dans la session Codex principale.
Le premier cas Claude (`plugin-dcp-egalite`) charge les six skills du
candidat, sans skill juridique autonome, mais le MCP indique `needs-auth`
et la sortie modèle signale une limite de session. Aucun outil MCP ne
réussit, aucune activation n'est mesurée et le coût déclaré est nul.
Ce précontrôle est conservé, sans le promouvoir en cas qualifié.

Le smoke Codex en dossier neuf vérifie les six copies natives et versions,
le manifeste, les STOP DCP et le contrat DRH. Lectures locales réussies,
sans web ni MCP. Il ne valide pas l'installation marketplace ni le
chargement complet du plugin avec MCP. Sa portée est indiquée dans la preuve.

Preuves assainies : `tests/evidence/2026-10-07-candidat/`.
La sortie brute du précontrôle est éliminée en mémoire ; la trace ne conserve
ni raisonnement ni signature. Le lanceur dispose désormais d'un timeout et
d'un arrêt explicite au premier échec pour éviter une campagne nominale
répétée sur un accès indisponible.

## Suite autonome DCP

Le dépôt DCP prépare les 28 cas du cadrage, avec répondant Codex web et juge
sans web, dans des processus séparés et une campagne séquentielle.
La correction Windows rétablit le backend sandbox en lecture seule malgré
`--ignore-user-config`. Le premier essai sans lecture des branches est écarté.
Les réponses, jugements et empreintes du nouveau kit sont conservés côté DCP.
Le cas-01 appelle une relecture de la frontière estimation/calcul financier.
Aucun score partiel n'est transféré à la qualification du plugin.

## Prérequis restants

Depuis ce checkout, `claude mcp login droit-francais` permet à l'utilisateur
de terminer la connexion OAuth, sans fournir de secret dans le chat. Après
réinitialisation du quota et connexion, exécuter un cas nominal isolé avant
la suite :

```powershell
python scripts/run_plugin_campaign.py --claude claude --case plugin-dcp-egalite --timeout 300 --stop-on-failure --output-dir tests/evidence/.work/qualification-1.2.0
```

Le profil dégradé reste distinct et ne remplace aucun des sept cas nominaux.
Les neuf réponses doivent ensuite être relues sur leurs invariants ; une
réussite technique n'est pas une validation juridique humaine. La grille
praticien DCP et les réserves du socle font partie du dossier à examiner.
`release_ready=false` reste en place.
