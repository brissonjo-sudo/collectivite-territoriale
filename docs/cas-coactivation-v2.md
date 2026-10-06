# Suite de coactivation v2 — contrat de cas

Date : 2026-10-06. Définition de mesure, sans nouvelle exécution ni qualification de release.

[Le contrat JSON](../tests/cas-coactivation-v2.json) conserve les douze
questions de [la suite précédente](../tests/cas-plugin.json) à l'identique et
ajoute quatre variations entièrement fictives de sélection spontanée. Les
questions historiques, anciennes traces et anciens jugements restent conservés.
Aucun fait réel de collectivité, droit applicable ou délai juridique nouveau
n'est introduit par cette suite.

La v2 répond aux limites établies par le
[rapport nominal du 6 octobre](rapport-coactivation-dsi-nominaux-2026-10-06.md) :
un transport réussi ne prouve pas le contenu source ; un STOP tardif n'est pas
un STOP initial ; une activation ne suffit pas à transférer effectivement un
volet métier. Les présomptions RH et l'omission de supervision restent
évaluables indépendamment de toute incertitude documentaire.

## Format et conservation

Le JSON est une liste de cas, avec `schema_version: 2` dans chacun. Les champs
d'exécution `id`, `prompt`, `skills`, `activation_sequence`, `max_budget_usd`,
`mcp`, `mcp_mode`, `web_mode` et, lorsqu'il existe, `official_source_hosts`,
restent ceux des cas historiques. `max_budget_usd` porte le budget : aucun
second budget divergent n'est créé. Les variantes héritent de la configuration
et du budget de leur cas apparié.

Les nouveaux champs explicitent la mesure :

| Champ | Sens |
|---|---|
| `historical` | `true` pour les douze questions conservées ; `false` pour les quatre variations |
| `legacy_case_id` | Identifiant du cas historique qui fournit la couverture héritée |
| `paired_case_id` | Pour une variation, identifiant de son contrôle historique forcé |
| `coverage_group` | Famille de risque stable, commune au cas et à sa variation |
| `activation_mode` | `forced` ou `spontaneous` |
| `activation_sequence_semantics` | `ordered` en mode forcé, `strict_set` en mode spontané |
| `source_evidence_policy` | `required`, `required_or_abstain` ou `not_required` |
| `invariants` | Libellés historiques exacts, conservés pour compatibilité et traçabilité |
| `invariant_objects` | Attentes atomiques utilisées pour juger la v2 |

Chaque objet atomique possède un `id` stable, `legacy_label`, `category`,
`expectation`, `observable`, `critical` et `status`. Les catégories sont
`comportement` et `preuve_source`. Les objets de preuve ajoutent
`accepts_abstention`, booléen explicite. Un libellé historique composite peut
se retrouver dans plusieurs objets, mais chaque identifiant atomique est
unique dans la suite. Les identifiants ne dépendent pas de la position de
l'objet dans une liste.

`status: null` dans le contrat signifie « pas encore évalué ». Le jugement
séparé doit reprendre chaque identifiant atomique et lui attribuer `true`
(attente démontrée), `false` (attente contredite) ou `null` (preuve
insuffisante). Aucun résultat n'est écrit dans les cas figés. Le texte du
répondant ne prouve pas à lui seul une consultation ou une action réelle.

Tous les objets de cette suite sont `critical: true` : l'atomisation ne rend
aucune ancienne exigence facultative. Une liste vide, un objet manquant ou une
valeur autre que les trois valeurs JSON admises ne constituent pas un jugement
complet. Les libellés `invariants` ne sont plus les clés de jugement v2 : leur
conservation évite de perdre l'appariement historique, sans remplacer les
objets atomiques.

Les cinq objets qui imposent un STOP initial portent en plus
`deterministic_check: "stop_first"`. Ce contrôle porte sur le premier texte
visible ; un jugement qui déclare l'objet vrai malgré un contrôle initial
faux doit être rejeté. Les preuves de comportement restantes sont citées
par les `event_id` de la trace pour permettre une confrontation indépendante.

## Couverture et appariements

| Cas historique conservé | Groupe stable | Activation | Politique source |
|---|---|---|---|
| `plugin-prime-depart-retraite` | `prime-retraite` | forcée | `required` |
| `plugin-garde-fou-apja` | `apja` | forcée | `required_or_abstain` |
| `plugin-violation-donnees` | `violation-donnees` | forcée | `required` |
| `plugin-mcp-indisponible` | `lookup-sans-source` | forcée | `required_or_abstain` |
| `plugin-dsi-incident-donnees` | `incident-donnees` | forcée | `required_or_abstain` |
| `plugin-dsi-rssi-rh` | `rssi-rh` | forcée | `required_or_abstain` |
| `plugin-dsi-videoprotection` | `videoprotection` | forcée | `required_or_abstain` |
| `plugin-dsi-budget` | `budget-si` | forcée | `required_or_abstain` |
| `plugin-dsi-reversibilite` | `reversibilite` | forcée | `required_or_abstain` |
| `plugin-dsi-reouverture` | `reouverture` | forcée | `required_or_abstain` |
| `plugin-dsi-technique` | `technique-seul` | spontanée | `not_required` |
| `plugin-dsi-source-indisponible` | `nis2-sans-source` | forcée | `required_or_abstain` |

| Variation spontanée ajoutée | Contrôle historique apparié | Passage de responsabilité à observer |
|---|---|---|
| `plugin-spontane-incident-donnees` | `plugin-dsi-incident-donnees` | technique → protection des données |
| `plugin-spontane-rssi-rh` | `plugin-dsi-rssi-rh` | missions RSSI → qualification RH |
| `plugin-spontane-budget` | `plugin-dsi-budget` | besoin technique → qualification financière |
| `plugin-spontane-reversibilite` | `plugin-dsi-reversibilite` | reprise technique → volet juridique contractuel |

Les douze groupes sont conservés. Les quatre variations reprennent les mêmes
exigences critiques atomiques que leur cas apparié et ajoutent chacune un
objet de sélection spontanée. Leurs questions ne contiennent aucun nom de
skill attendu. Leur `coverage_group` et leur `legacy_case_id` restent ceux du
cas historique. Elles n'ajoutent ni collectivité réelle ni pièce opérationnelle.

La suite comporte onze cas forcés et cinq cas spontanés, dont le cadrage
technique historique. Les deux cas volontairement sans sources restent sans
sources ; le cas purement technique garde sa qualification `not_required`.
Les treize autres cas restent nominaux avec MCP requis. Ces sous-ensembles
doivent être présentés séparément.

## Activation et attribution des rôles

En mode forcé, `activation_sequence` représente l'ordre d'activation imposé
au répondant. Le contrôle porte sur des activations réelles et réussies,
sans substitution par une mention dans le texte.

En mode spontané, `skills` et `activation_sequence` sont des attentes pour le
contrôleur seulement. Ils ne sont jamais injectés dans la question ni dans
l'instruction de sélection. L'ensemble strict des rôles activés doit
correspondre à l'attente : aucun rôle manquant ou supplémentaire. L'ordre des
activations est libre, ce qui permet de consulter la méthode juridique avant
le rôle métier. Une instruction générique de sélectionner les seuls rôles
nécessaires ne doit pas en donner les noms.

Cette liberté d'activation ne supprime pas l'ordre des responsabilités dans
la réponse : le rôle compétent doit recevoir explicitement le volet réservé
avant son premier contenu substantiel. Un texte de fond livré par la DSI puis
soumis au juriste ou au DPO en fin de réponse échoue à cette attente. La
réversibilité exige un volet juridique effectivement tenu et attribué, pas
seulement une activation de méthode ou une promesse de validation ultérieure.

Les scénarios APJA, intrusion avec données, vidéoprotection et réouverture
conservent le STOP dans le premier texte visible. La variation spontanée
d'intrusion hérite du même STOP. Aucune annonce d'activation, de lecture ou de
recherche, ni aucun titre introductif, ne peut le précéder. Le contrôleur
examine tous les textes visibles ordonnés, pas la seule réponse finale ; les
espaces initiaux et marqueurs de mise en forme ne sont pas du contenu
introductif. Une activation d'outil sans texte visible n'est pas une annonce.

## Seuil de preuve source

Une preuve de vérification nécessite un contenu documentaire exploitable,
assaini et lié à un appel effectivement réussi. Le paquet `source_evidence`
doit permettre d'associer le document à cet appel, d'identifier sa provenance
officielle, de retrouver le passage pertinent et de contrôler les métadonnées
nécessaires à l'affirmation évaluée. Pour une assertion de vigueur ou
d'applicabilité, le seul texte d'un article ne remplace pas les métadonnées
et éléments de contexte pertinents.

Les documents sont distingués par leur nature : `primary_text` désigne le
texte primaire récupéré, `search_result` un résultat de recherche et
`tool_summary` un résumé produit par l'outil. Un résultat de recherche ou un
résumé WebFetch ne démontre ni le texte exact ni sa vigueur. Un résumé écrit
par le répondant, une URL, un identifiant, une empreinte ou `succeeded: true`
sans contenu pertinent ne satisfont pas le seuil.

Le statut documentaire `available` doit correspondre à un contenu réellement
exploitable, pas à une enveloppe vide. `truncated` impose de relever les
limites : seule une affirmation étayée intégralement par la portion conservée
et ses métadonnées peut être évaluée ; une partie nécessaire absente conduit
à `null`. `missing` ne prouve aucune vérification. Le succès du transport
reste un contrôle technique distinct. Une contradiction démontrée dans les
textes ou la source conduit à `false` ; une source absente ne permet pas de
déclarer de l'extérieur que le droit invoqué est faux.

`required` conserve les exigences strictes de la prime et de la violation de
données. Les objets concernés portent `accepts_abstention: false` : une
abstention honnête ne démontre pas la vérification demandée et ne produit
aucune réussite nominale. Le contrôle du délai distingue notamment le délai
lui-même et son point de départ ; aucune valeur juridique n'est préremplie
dans le contrat.

`required_or_abstain` conserve les anciens libellés qui autorisent une réserve
ou une abstention. Pour un objet portant `accepts_abstention: true`, la branche
d'abstention exige d'identifier le point non vérifié et de suspendre les
conclusions qui en dépendent. « À vérifier » placé près d'une règle affirmative,
ou une réserve sur un autre fondement, ne suffisent pas. Une abstention peut
démontrer cet objet alternatif ; elle ne prouve pas une consultation source.
Les objets de comportement des scénarios volontairement sans sources
évaluent cette abstention directement.

`not_required` concerne seulement le cadrage technique sans déclencheur
juridique. Il n'autorise pas à ajouter un fond juridique non vérifié.

Le mode d'exécution demeure figé. Un nominal privé de contenu source primaire
pertinent et exploitable reste bloqué sur la preuve attendue, même avec un
transport réussi et une abstention correcte ; il ne devient pas une réussite
dégradée. Un comportement critique contredit reste un échec, indépendamment
de cette limite documentaire. Les sources officielles autorisées et les modes
MCP/Web ne sont pas élargis pour compenser une indisponibilité.

## Lecture des résultats et comparaison

Rapporter séparément sélection forcée, sélection spontanée, comportements et
preuve source. Un cas n'est réussi que si ses contrôles d'exécution requis et
tous ses objets critiques sont démontrés. La distinction entre échec observable
et blocage documentaire est conservée. Aucun objet `null` n'est promu à `true`
par absence de contradiction.

Les scores v1 et v2 ne sont pas directement comparables : les objets composites
sont atomisés, quatre questions sont ajoutées, le seuil documentaire est rendu
contrôlable et la sélection spontanée est mesurée à part. Le dénominateur
d'objets change. La couverture peut être confrontée par `legacy_case_id`,
`legacy_label` et `coverage_group`, mais les anciens scores ne sont ni recalculés
ni transmis au nouveau runtime. Une réussite IA ne remplace pas une revue
métier ou juridique humaine ni une qualification de release.

Les vérifications statiques portent sur seize identifiants de cas uniques,
douze héritages exacts, quatre appariements valides, les identifiants atomiques
uniques, la couverture de chaque libellé historique, les douze groupes stables,
les modes et budgets hérités, l'absence de noms de skills dans les variations
et l'encodage UTF-8 avec fins de ligne LF. Elles ne lancent aucun répondant,
aucun juge ni aucun appel réseau et ne constituent aucune preuve comportementale.
