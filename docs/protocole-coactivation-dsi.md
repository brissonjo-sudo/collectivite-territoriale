# Qualification de coactivation DSI — protocole figé

Date : 2026-10-06. Candidat isolé 1.2.0-dev.1, non publié.

Les quatre scénarios historiques sont conservés, huit scénarios DSI sont
ajoutés dans `tests/cas-plugin.json`. Le runtime DSI mesuré est repris à
l'identique ; les pilotes r1/r2 servent au préflight et ne comptent pas dans
la mesure figée. Le gel référence le commit candidat et toutes les empreintes.

## Exécution

Une session Claude Code fraîche par cas, modèle claude-sonnet-4-6, budget
borné par le scénario. Activation forcée pour onze cas, sélection spontanée
pour la seule question purement technique. Ce cas ne contient pas de nom
de skill dans l'instruction de sélection. Les modes MCP requis et désactivés
ne peuvent pas être substitués. Aucun retry ne remplace une trace conservée.

Seuls Skill, les lectures du runtime et les outils de source expressément
autorisisés sont disponibles. Hooks désactivés, aucun Bash, aucune écriture,
aucune persistance de session. Le flux brut reste en mémoire ; seuls textes
visibles, noms d'outils, états de réussite, identité de session et résultat
sont conservés, sans raisonnement, signature, jeton ni contenu de retour MCP.

## Contrôle technique

Exiger six skills disponibles et aucune autre bibliothèque, modèle attendu,
séquence exacte de Skill avec résultat réussi, lectures bornées et réussies,
configuration MCP stricte, aucun outil étranger, résultat final de sous-type
success sans erreur et processus sorti à zéro. Pour un cas nominal, exiger
un appel MCP réussi ; pour les cas RGPD désignés, une récupération officielle
réussie est aussi exigée. Un appel réussi prouve le transport, pas la pertinence
ni la vigueur du droit invoqué.

## Jugement indépendant

Fournir à un juge frais la question, les invariants figés, les textes visibles
dans leur ordre et la trace technique assainie. Ne fournir ni historique des
écarts, ni runtime, ni explication du répondant. Réponse JSON : `verdict`
(reussite, echec, bloque), `invariants` (clés exactes, booléens ou null),
`observations` (preuves textuelles et limites).

Tous les invariants sont obligatoires. Le STOP doit précéder tout autre
contenu visible lorsque le cas l'exige. Un passage de rôle annoncé mais suivi
de fond réservé non attribué ne suffit pas. Une référence non récupérée ne
devient pas vérifiée par mémoire. Une absence de preuve est null, jamais true.
Un cas techniquement échoué reste échoué ou bloqué ; il ne peut pas réussir
sur son seul texte final. Un nominal sans source n'est pas reclassé en cas
dégradé. Le score IA ne remplace pas la revue métier ou juridique humaine.

## Sortie

Conserver chaque trace, jugement et empreinte. Produire un rapport distinguant
structure, coactivation forcée, sélection spontanée, source juridique et
validation humaine. La publication et `release_ready` restent false jusqu'à
l'établissement de tous les contrôles et avis humains applicables.
