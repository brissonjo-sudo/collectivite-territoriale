# Qualification actuelle : dev.6 PARTIEL

Le pilote dev.6 est **PARTIEL** : seize cas et 124 exigences préparés,
six cas exécutés, cinq réponses liées et cinq juges frais (dix rôles retenus).
Le cas APJA est rejeté hors score : six lectures ont été regroupées dans un
seul appel. Sa réponse et son journal natif sont conservés sans remplacement.
Dix cas ne sont pas exécutés. Les seuls cinq cas jugés donnent
1 réussites, 1 échecs et 3 bloqués.
41 exigences sont effectivement jugées :
37 vraies, 1 fausses et 3 indéterminées.
Ce bilan ne constitue pas un résultat de la suite complète.

Candidat mesuré : `1a12b347448809864ba6d14d5501585a4a038206` ; source runtime : `3f0df285898cf1e36d1ddda8d85d0c4cd5e0903b`,
version `1.2.0-dev.6`. L'audit partiel contrôle cinq répondants et cinq juges,
pas seize paires. Le contrôle complet reste non satisfait. Les acteurs chargent
des fichiers candidats par fragments ; l'activation réelle du plugin n'est
pas démontrée. Messages initiaux opaques, isolation absolue, sélections forcées,
source primaire pertinente et vérification de vigueur restent distingués.
Aucun score dev.5 ni DSI autonome n'est transféré.

Le contrôle isolé, hors campagne, a installé et comparé 214 fichiers, dont
166 runtime. `codex debug prompt-input` a construit le catalogue contenant
les six descriptions complètes du plugin. Cette découverte native ne démontre
ni sélection ni chargement par un modèle, ni réponse métier. L'observation
datée de `login status` indique `Not logged in` dans cet état isolé ; elle ne
prouve pas un état d'authentification futur. Aucun modèle ni smoke d'usage n'a
été lancé. Le MCP est configuré désactivé et son exposition effective reste
non vérifiée. Le stdout développeur brut, l'état Codex et les fichiers
d'authentification/configuration ne sont pas publiés. Une pièce dérivée ne
contient que les six descriptions et chemins du plugin, reliés au SHA local.

La campagne utilise les sous-agents natifs Codex, sans lancement de Claude.
Avis humains DSI/RSSI et juridiques, smoke d'usage et suite complète restent
ouverts ; `release_ready=false`. Les PR restent brouillon, sans fusion ni release.

[Rapport partiel](../../tests/evidence/coactivation-codex-dev6-PARTIEL/rapport-PARTIEL.md) · [Synthèse partielle](../../tests/evidence/coactivation-codex-dev6-PARTIEL/synthese-PARTIELLE.json)

Le [bilan dev.5 historique](README-dev5-r2-historique.md) conserve sa portée : 16 réponses/16 juges, 4 réussites, 6 échecs, 6 bloqués ; 107/6/11 atomes. Les preuves dev.4/r7 et antérieures restent conservées.

Le diagnostic explicite du 7 octobre à 21:47 UTC conserve le marqueur `$collectivite-territoriale:dsi-fpt` comme texte utilisateur. Aucun bloc contenant les instructions complètes DSI n’est attesté ; seule la découverte est confirmée. Aucune inférence ni connexion demandée. Voir les pièces distinctes `smoke-dev6-explicite-diagnostic-2026-10-07.md/json`. Les reçus antérieurs restent des snapshots datés.
