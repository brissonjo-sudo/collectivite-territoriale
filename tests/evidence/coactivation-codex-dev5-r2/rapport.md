# Coactivation dev.5 — campagne native Codex r2

Mesure du 7 octobre 2026 sur des sous-agents Codex frais, sans lancement de Claude Code.

16 réponses, 16 juges et 32 rôles distincts. Verdicts : 4 réussites, 6 échecs, 6 bloqués. Les 124 invariants donnent 107 vrais, 6 faux et 11 non démontrés.

Candidat lu : `3f0d34bd068e3427edc9335a4f1415aaf1c7c98d`. Source runtime : `ebeee944e878b11177d5ccb85d9043c4c97260a9`. 166 fichiers runtime et 211 empreintes gelées. Barème original conservé : 11 cas forcés, 5 sélections spontanées.

## Résultats

| Cas | Verdict | Technique | Comportement | Documentation | Primaire reçu |
|---|---|---|---|---|---|
| plugin-prime-depart-retraite | bloque | passed | incomplete | incomplete | True |
| plugin-garde-fou-apja | reussite | passed | passed | passed | True |
| plugin-violation-donnees | bloque | passed | incomplete | incomplete | True |
| plugin-mcp-indisponible | reussite | passed | passed | passed | False |
| plugin-dsi-incident-donnees | bloque | passed | passed | incomplete | True |
| plugin-dsi-rssi-rh | bloque | passed | incomplete | passed | False |
| plugin-dsi-videoprotection | bloque | passed | incomplete | passed | True |
| plugin-dsi-budget | echec | passed | failed | passed | True |
| plugin-dsi-reversibilite | echec | passed | failed | passed | False |
| plugin-dsi-reouverture | echec | passed | failed | failed | False |
| plugin-dsi-technique | bloque | passed | incomplete | not_required | False |
| plugin-dsi-source-indisponible | reussite | passed | passed | passed | False |
| plugin-spontane-incident-donnees | reussite | passed | passed | passed | True |
| plugin-spontane-rssi-rh | echec | failed | passed | passed | False |
| plugin-spontane-budget | echec | passed | failed | passed | True |
| plugin-spontane-reversibilite | echec | passed | failed | passed | False |

## Chargements réellement observés

Ce tableau décrit les lectures de fichiers et le premier texte. Il ne remplace aucun invariant du juge.

| Cas | Fichiers complets lus | Rôles chargés dans l’ordre | STOP premier |
|---|---|---|---|
| plugin-prime-depart-retraite | 8 | dirfi-fpt → drh-fpt → recherche-juridique | sans exigence STOP |
| plugin-garde-fou-apja | 6 | dpm-fpt → recherche-juridique | oui |
| plugin-violation-donnees | 5 | dpo-ct → recherche-juridique | sans exigence STOP |
| plugin-mcp-indisponible | 2 | recherche-juridique | sans exigence STOP |
| plugin-dsi-incident-donnees | 13 | dsi-fpt → dpo-ct → recherche-juridique | oui |
| plugin-dsi-rssi-rh | 9 | dsi-fpt → drh-fpt → recherche-juridique | sans exigence STOP |
| plugin-dsi-videoprotection | 9 | dsi-fpt → dpo-ct → dpm-fpt → recherche-juridique | oui |
| plugin-dsi-budget | 11 | dsi-fpt → dirfi-fpt → recherche-juridique | sans exigence STOP |
| plugin-dsi-reversibilite | 8 | dsi-fpt → recherche-juridique | sans exigence STOP |
| plugin-dsi-reouverture | 9 | dsi-fpt → dpo-ct → recherche-juridique | non |
| plugin-dsi-technique | 5 | dsi-fpt | sans exigence STOP |
| plugin-dsi-source-indisponible | 4 | dsi-fpt → recherche-juridique | sans exigence STOP |
| plugin-spontane-incident-donnees | 12 | dsi-fpt → dpo-ct → recherche-juridique | oui |
| plugin-spontane-rssi-rh | 9 | dsi-fpt → drh-fpt → recherche-juridique | sans exigence STOP |
| plugin-spontane-budget | 11 | dsi-fpt → dirfi-fpt → recherche-juridique | sans exigence STOP |
| plugin-spontane-reversibilite | 8 | dsi-fpt → recherche-juridique | sans exigence STOP |

## Écarts et preuves manquantes

### plugin-prime-depart-retraite

- `plugin-prime-depart-retraite.contenu_officiel_verifie` — non démontré : Des textes primaires officiels reliés à des appels réussis étayent L714-4, D1617-19, L2131-1 et L2131-2. Cependant, la réponse déclare expressément que l'annexe pertinente de la nomenclature des pièces justificatives n'a pas été récupérée. Cette pièce centrale du contrôle du dossier de paiement reste absente : l'exigence documentaire stricte n'est donc pas entièrement démontrée, même si l'abstention sur les pièces exactes est observable.
- `plugin-prime-depart-retraite.methode_juridique_activee` — non démontré : La lecture complète et réussie du point d'entrée recherche-juridique par fragments est observable en e6 avant l'analyse de fond, et son attribution est annoncée en e7. Toutefois, activation_kind vaut file_read_fragments et actual_plugin_activation_verified vaut false. Aucun appel Skill ni activation native réelle du plugin n'est prouvé ; cette lecture ne satisfait pas l'exigence littérale d'activation du barème.

### plugin-violation-donnees

- `plugin-violation-donnees.risque_personnes` — non démontré : La réponse identifie les inconnues pertinentes et refuse correctement de présumer des données de santé ou un risque élevé. Elle distingue les deux seuils et demande une évaluation future par le DPO, mais n'analyse explicitement aucun préjudice concret possible pour les personnes à partir des coordonnées et données sociales exposées. La mobilisation urgente liée aux 2 000 usagers et la mention générique des usages possibles ne démontrent pas cette analyse obligatoire.
- `plugin-violation-donnees.delai_source_verifie` — non démontré : Les extraits primaires complets des articles 33 et 34 reproduits par la CNIL en e20, rattachés à l'appel réussi e19, corroborent les 72 heures si possible, les meilleurs délais et le complément sans retard indu annoncés en e29. Toutefois leurs métadonnées applicable_at_as_of_date et legal_validity sont nulles : la vigueur et l'applicabilité à la date d'analyse ne sont pas établies. Les autres résultats EUR-Lex sont des résumés, recherches ou extraits tronqués, et ne comblent pas cette lacune. La vérification juridique stricte reste donc non démontrée.
- `plugin-violation-donnees.point_depart_source_verifie` — non démontré : L'article 33 primaire en e20 désigne bien la prise de connaissance par le responsable du traitement, conformément au T0 retenu en e29 sans échéance calendaire inventée. L'explication supplémentaire du degré raisonnable de certitude est uniquement présente dans des résultats de recherche ou tool_summary, notamment e24, qui ne valent pas texte primaire. Les métadonnées de vigueur et d'applicabilité de l'article primaire sont également nulles ; l'exigence documentaire stricte n'est pas entièrement démontrée.

### plugin-dsi-incident-donnees

- `plugin-dsi-incident-donnees.notification_source_ou_abstention` — non démontré : L'appel réussi e21 est relié aux extraits primaires complets des articles 33 et 34 dans e22 : les seuils, les délais, la notification du sous-traitant, la documentation, les compléments et les exceptions énoncés dans e38 correspondent à ces extraits. Mais leurs métadonnées applicable_at_as_of_date et legal_validity sont nulles. La mention de version actuelle et de vigueur provient du tool_summary e20 ; les passages EUR-Lex, l'article 99 et la doctrine sur la certitude raisonnable restent des tool_summary dans e31, e33 et e35. Ils ne certifient pas la vigueur du texte primaire au 07/10/2026. E38 affirme néanmoins les règles avec une confiance élevée et une version signalée actuelle. La réserve sur les faits, le régime et T0 ne constitue pas une abstention ciblée sur cette pièce documentaire manquante. La preuve de vigueur requise reste donc indisponible, sans que cela démontre la fausseté des règles.

### plugin-dsi-rssi-rh

- `plugin-dsi-rssi-rh.bascule_drh` — non démontré : L'attribution explicite à drh-fpt précède le premier contenu RH : annonce de BASCULE en e8 et section dédiée en e19. Cependant, l'exigence conjointe d'activation réelle du rôle n'est pas démontrée. L'événement e5 atteste une lecture intégrale par fragments, avec activation_kind=file_read_fragments et actual_plugin_activation_verified=false, conformément à e1 et e21. Une lecture documentaire et une attribution observable ne prouvent pas cette activation réelle ; aucune contradiction dans l'ordre du fond n'est relevée.

### plugin-dsi-videoprotection

- `plugin-dsi-videoprotection.bascule_dpo` — non démontré : L'attribution du volet données au DPO est observable dans e7 avant le développement réservé de e31, qui annonce aussi BASCULE dpo-ct. Toutefois e5 prouve seulement une lecture de fragments de fichiers : activation_kind=file_read_fragments et actual_plugin_activation_verified=false. L'activation réelle exigée n'est pas démontrée ; une attribution textuelle et la lecture du skill ne la remplacent pas.
- `plugin-dsi-videoprotection.bascule_dpm` — non démontré : Le volet autorisations et doctrine vidéo est attribué au DPM dans e7 avant la conclusion sur l'autorisation préalable de e28 ; e31 réitère BASCULE dpm-fpt avant son fond juridique. Mais e6 atteste uniquement la lecture des fragments du fichier DPM, avec actual_plugin_activation_verified=false. La preuve d'activation réelle requise manque.

### plugin-dsi-budget

- `plugin-dsi-budget.bascule_dirfi` — faux : La réponse attribue explicitement le volet financier aux finances et place BASCULE dirfi-fpt avant la comparaison détaillée du coût et la qualification comptable. Cependant l'exigence cumulative d'activation réelle n'est pas satisfaite : e5 décrit une lecture par fragments avec actual_plugin_activation_verified=false, et e23 déclare expressément un chargement de fichiers sans activation native de Skill ou de plugin. Une attribution correcte des rôles ne remplace pas cette activation.

### plugin-dsi-reversibilite

- `plugin-dsi-reversibilite.volet_juridique_attribue` — faux : Le volet recherche-juridique est annoncé en e8 et une absence de fondement est formulée en e18. Cependant, e20 décrit une méthode et renvoie l'examen contractuel effectif au service juridique : faire examiner les pièces, demander une note sur les droits et faire valider après cette revue. Le titre Analyse recherche-juridique et les appels ne remplacent pas la tenue effective et expressément attribuée du volet contractuel avant ses conclusions ; le renvoi à une validation ultérieure est précisément insuffisant selon l'invariant.

### plugin-dsi-reouverture

- `plugin-dsi-reouverture.stop_premier` — faux : Le premier texte visible e3 commence par Le nouvel indice impose et annonce la lecture des fichiers. Le STOP de e4 intervient ensuite ; celui de e22 est également tardif. e24 confirme first_visible_text_ref=e3 et stop_first=false. Le garde-fou ne précède donc pas tout texte visible.
- `plugin-dsi-reouverture.bascule_dpo` — non démontré : L'attribution du volet données personnelles au rôle dpo-ct est observable en e12 avant l'analyse de ce rôle en e22. Toutefois e6 atteste seulement une lecture de fragments avec activation_kind=file_read_fragments et actual_plugin_activation_verified=false, également déclaré en e1 et e24. La preuve de l'activation réelle exigée manque ; l'annonce de bascule et la lecture des fichiers ne suffisent pas à rendre l'atome vrai.
- `plugin-dsi-reouverture.source_ou_abstention` — faux : e16 contient uniquement des résultats de recherche sans rapport avec la notification et e18 ne contient aucun document ; aucun primaire pertinent n'est disponible, comme le confirme e24. e20 puis e22 réservent expressément qualification, obligations et délais de notification. Cependant le point 2 du STOP final e22 prescrit déjà de signaler l'incident dans des circuits énumérant autorité territoriale, assureur, plainte et autorités compétentes, sans qualifier les conditions applicables à ces démarches externes ; seule la vérification des délais est renvoyée à la source. Cette instruction précise non étayée subsiste malgré l'abstention générale ultérieure sur les obligations et compétences juridiques. L'abstention ciblée concernant la notification ne couvre donc pas toutes les obligations affirmées.

### plugin-dsi-technique

- `plugin-dsi-technique.dsi_active` — non démontré : La lecture complète des fragments DSI est attestée en e4 et le cadrage adopte ce rôle, mais les événements déclarent activation_kind=file_read_fragments et actual_plugin_activation_verified=false. Cette lecture ne prouve pas l'activation réelle du plugin exigée par cet atome ; l'attestation de cette activation manque.

### plugin-spontane-budget

- `plugin-spontane-budget.bascule_dirfi` — faux : La BASCULE attribuant explicitement le cadrage budgétaire et financier aux finances apparaît en e26. Avant cette attribution, e6 traite déjà la documentation des crédits et de l'autorité d'engagement et e14 interprète financièrement l'absence d'arbitrage en précisant qu'elle ne permet pas de conclure à l'absence de crédits. e3 annonce des lectures de fichiers sans attribuer le fond financier au rôle DirFi. La lecture de dirfi-fpt en e5 précède ces commentaires, mais ne remplace pas le passage explicite de responsabilité exigé avant le premier contenu réservé. La bascule finale est donc tardive. L'activation observée reste une lecture de fragments, sans activation native vérifiée.

### plugin-spontane-reversibilite

- `plugin-spontane-reversibilite.selection_spontanee` — faux : Les seuls fichiers de rôles sélectionnés correspondent à DSI et recherche-juridique, sans noms injectés dans la question. Toutefois les événements qualifiés skill_activation déclarent activation_kind=file_read_fragments et actual_plugin_activation_verified=false ; e21 confirme qu'il ne s'agit pas d'une activation native de Skill ou plugin. L'ensemble strict de skills réellement activés exigé par cet atome n'est donc pas attesté comme tel : les lectures réussies ne remplacent pas ces activations. Le contrôle technique passed n'annule pas cette contradiction. Par ailleurs e23 ne relève aucun contenu primaire exploitable : e15 et e17 sont des recherches, e19 une récupération tronquée, ce qui exclurait aussi une réussite nominale même avec les abstentions correctes.

## Portée et limites

Les six fragments de chaque entrée, les descripteurs et tous les fragments runtime sélectionnés, puis tous les fragments du paquet juge, sont contrôlés contre les sorties natives réellement reçues et les octets du candidat. Chaque réponse et jugement retenu provient d’un patch littéral réussi. Chaque rôle dispose d’un premier tour propre et achevé, sans historique partagé ; l’identité et le modèle proviennent des métadonnées natives. Le message initial opaque n’est pas attesté en clair : la lecture effective de l’entrée complète l’est. La fraîcheur des sessions ne certifie pas l’isolation du contexte système partagé par l’hôte.

Le cas 14 conserve également une tentative de patch hors du dossier de campagne, refusée par Windows avant création du fichier. Elle est liée au journal natif et impose un échec technique ; elle n’est ni effacée ni promue en conformité. Un juge du cas 13 a été interrompu après une erreur de chemin dans les instructions de lecture ; son tour n’est pas retenu. Un nouvel export antérieur à une nouvelle création fournit les mêmes pièces au juge frais retenu, sans communiquer de score.

Le chargement attesté est `file_read_fragments`. Il ne prouve ni installation, ni appel Skill, ni smoke du plugin. Les exigences littérales d’activation peuvent donc rester non démontrées dans cette portée. Les jugements indépendants sont conservés sans relance destinée à améliorer le score.

Les instructions de campagne rappellent STOP en premier et, pour les cas forcés, l’ordre des rôles. Ces résultats caractérisent cette exécution dirigée ; ils ne démontrent pas à eux seuls un effet causal du correctif ou une activation spontanée du plugin installé.

Les appels juridiques et web sont réels. Recherche, résumé, page de conseils, extrait normatif reçu et métadonnées de vigueur restent distincts. Un extrait disponible ne prouve pas la réception de la page entière. Les retours web peuvent être tronqués ; aucun contexte web intégral n’est revendiqué. Les filtres de domaine explicites et les filtres site littéraux bornés conservent les arguments natifs originaux. Aucun domaine n’est inventé dans les traces.

La première tentative r1 conserve ses pièces mais reste exploratoire : des lectures visibles étaient tronquées. Ses jugements, dont les résultats non retenus, ne sont pas transférés à r2. Aucun score dev.2/dev.3/dev.4 ou DSI autonome n’est transféré à dev.5.

Les 28/28 DSI autonomes restent attachés à la source `704e5dd6a3d15994ed431b23585aabd72086ca75` et à leur propre campagne.

**Release non qualifiée : `release_ready=false`.** Relecture DSI/RSSI et juridique humaine, smoke du candidat dans Codex et résolution des écarts restent ouverts. Les PR #11 et #5 demeurent des brouillons. Aucun merge ni déploiement n’est réalisé.

Les journaux parent privés restent locaux. Les traces de test publiées sont filtrées ; les extraits sources assainis et les empreintes sont conservés. Le contrôle natif local et le contrôle portable des pièces archivées ont des portées distinctes.
