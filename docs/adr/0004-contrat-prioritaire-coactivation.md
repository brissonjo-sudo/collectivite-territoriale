# ADR 0004 — Contrat prioritaire de coactivation

Date : 2026-10-06. Statut : accepté pour le candidat de qualification.

La campagne dev.2 comporte des réponses qui annoncent leur méthode avant le
STOP, omettent la recherche juridique en sélection spontanée, ou présentent
une synthèse d'outil comme une source vérifiée. Des références non récupérées
restent utilisées après une réserve. Le transport réussi ne couvre pas ces
écarts de comportement ou de preuve.

Les six skills du plugin reçoivent un contrat commun en tête du corps,
avant les métadonnées historiques et les exemples. Les cinq métiers ont des
descriptions bornées précisant le STOP applicable et le chargement réel de la
recherche juridique. Les instructions ne déduisent aucune règle juridique de
la mémoire : elles exigent le texte pertinent pour chaque affirmation ou son
retrait intégral du livrable.

Le mécanisme reste celui des ADR 0002 et 0003 : insertion à ancre unique hors
frontmatter, remplacement du seul champ description folded, empreintes exactes
de base et de correction. Aucun outil, serveur, hook ou accès n'est ajouté.
Les commits amont ne changent pas ; DSI et DirFi deviennent aussi des variantes
locales déclarées. La mesure autonome du DSI source ne qualifie pas sa variante
dans ce plugin.

La documentation officielle recommande de placer les instructions importantes
en tête du skill et décrit les limites de la description de découverte :
[Claude Code — skills](https://code.claude.com/docs/en/skills).

Les traces dev.2 sont conservées, y compris les échecs. Dev.3 exige un nouveau
gel et seize nouvelles conversations. La suite, ses 124 exigences et le barème
ne changent pas. Aucune répétition ne remplace silencieusement une tentative.
Une mesure positive restera distincte des revues humaines et du smoke Codex.
