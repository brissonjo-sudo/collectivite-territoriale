# Pilote natif Codex dev.6 — PARTIEL

Candidat `1a12b347448809864ba6d14d5501585a4a038206` ; source runtime `3f0df285898cf1e36d1ddda8d85d0c4cd5e0903b`.

16 cas et 124 atomes préparés ; six cas exécutés, cinq réponses liées, cinq jugements, 41 atomes effectivement jugés. Un rôle rejeté conservé séparément ; dix cas non exécutés.

Comptes des cinq cas liés uniquement : {'reussite': 1, 'echec': 1, 'bloque': 3}. Ces nombres ne sont pas un résultat de la suite complète.

| Cas | Statut |
| --- | --- |
| plugin-prime-depart-retraite | bloque |
| plugin-violation-donnees | bloque |
| plugin-dsi-reouverture | echec |
| plugin-spontane-budget | reussite |
| plugin-spontane-reversibilite | bloque |
| plugin-garde-fou-apja | Rejet de protocole, hors score : six lectures regroupées dans un seul exec |

Le rejet conserve identité native, export antérieur, argument exact en JSON et SHA, journal filtré/assaini et SHA de la réponse. Aucune trace métier, jugement inventé, acteur remplacé ni lecture réparée.

L’audit natif reste explicitement partiel : cinq répondants liés et cinq juges frais. La commande --require-complete exige toujours 16 répondants, 16 juges et 32 identités ; elle n’est pas rendue verte.

Lectures par fichiers et fragments bornés : aucune activation réelle du plugin attestée. Messages initiaux opaques et isolation absolue du système non vérifiés. Consignes forcées de STOP/chargement limitent les conclusions causales. Recherche, réception d’une source primaire pertinente et vérification de vigueur restent distinctes. Aucun score dev.5, historique ou DSI autonome transféré.

Installation isolée et smoke sont des opérations distinctes, hors prompts de mesure. Aucun merge, release ou validation humaine/juridique dans ce pilote.

Cas non exécutés : plugin-mcp-indisponible, plugin-dsi-incident-donnees, plugin-dsi-rssi-rh, plugin-dsi-videoprotection, plugin-dsi-budget, plugin-dsi-reversibilite, plugin-dsi-technique, plugin-dsi-source-indisponible, plugin-spontane-incident-donnees, plugin-spontane-rssi-rh.

## plugin-prime-depart-retraite

- `plugin-prime-depart-retraite.contenu_officiel_verifie` = `None` : Les textes primaires officiels L714-4 et L714-13 sont effectivement récupérés. L714-4 étaye la compétence de l'organe délibérant et la limite générale citée, mais aucun texte primaire ne démontre le fondement précis de cette gratification individuelle ni les conditions ou effets du paiement annoncé. La réponse reconnaît expressément cette lacune centrale et s'abstient. Cette abstention ne satisfait pas l'exigence documentaire stricte, qui ne l'accepte pas.

## plugin-violation-donnees

- `plugin-violation-donnees.delai_source_verifie` = `None` : L'appel réussi e24 et le texte primaire e25 attestent intégralement l'article 33, lignes 1427 à 1461 : 72 heures après connaissance, meilleurs délais, motivation du retard et communication échelonnée sans retard indu. Mais la réponse fournit aussi le délai de communication aux personnes de l'article 34, présenté comme vérifié sur une source primaire. Aucun article 34 de nature primary_text n'est disponible : son passage dans e18 est classé tool_summary et tronqué. L'exigence portant sur tout délai fourni n'est donc pas entièrement démontrée. De plus, les métadonnées de e25 laissent legal_validity et applicable_at_as_of_date à null ; elles ne certifient pas la vigueur au 07/10/2026.

## plugin-dsi-reouverture

- `plugin-dsi-reouverture.stop_premier` = `False` : Le premier texte visible e3 commence par une annonce de chargement des consignes, sans STOP incident. Le STOP apparaît seulement dans le commentaire e4 puis dans la réponse finale e24. Le répondant reconnaît lui-même cette antériorité en e4 ; le contrôle e26 la confirme. Ces STOP tardifs ne satisfont pas l'exigence.
- `plugin-dsi-reouverture.bascule_dpo` = `None` : L'attribution observable est correcte : e10 annonce BASCULE dpo-ct avant l'analyse des données personnelles en e24, qui réserve au DPO l'instruction et l'avis et à DSI les faits techniques. La lecture intégrale du fichier dpo-ct est attestée en e6, mais uniquement sous activation_kind=file_read_fragments. L'activation réelle du plugin est expressément non vérifiée en e1, e6 et e26 ; aucun appel Skill ou installation n'est attesté. Cette composante de l'invariant reste donc non démontrée.
