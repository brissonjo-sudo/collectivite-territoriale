# Réception MCP native tronquée — enveloppe distincte

Date : 2026-10-07. Cas initial : `plugin-dsi-reversibilite` (09).

Le deuxième appel juridique natif, `get_decision`, a un transport Codex achevé
et un retour commençant exactement par `Warning: truncated output (original
token count: 27195)`. La charge reçue compte 38 722 caractères. Cette observation
ne démontre pas une erreur du fournisseur et ne permet pas de lire un résultat
JSON complet.

`controler_codex_dev5_r2_mcp_tronque.py` ajoute une enveloppe distincte sans
modifier les adaptateurs antérieurs, le candidat, la réponse ou le barème. Elle
reconnaît uniquement le préfixe natif strict, une sortie achevée et un appel
juridique littéral autorisé réellement présent dans la session. Elle ne parse
ni ne reconstruit le JSON incomplet. Le marqueur interne typé est une attestation
de réception native, jamais une réponse fournisseur fabriquée.

La projection conserve l'appel original et ses identités. `succeeded=true`
concerne le transport ; `payload_integrity_verified=false`,
`payload_status=truncated` et `source_provider_error_verified=false` explicitent
ses limites. La preuve documentaire est `missing`, motif
`native_mcp_payload_truncated`, avec `documents=[]`. Aucun texte primaire,
pertinence, applicabilité ou vigueur n'en est déduit. La capture conservée est
le texte réellement reçu, assaini et borné par le filtre existant ; les champs
de réception indiquent la troncature native et une éventuelle réduction par ce
filtre. Aucun texte écarté pour confidentialité n'est haché.

Le protocole v2 laisse une absence ou une troncature visible sans promotion en
preuve complète. Les contrôles techniques existants vérifient le transport,
les liaisons et le routage : ils restent inchangés. Le défaut documentaire ne
devient pas une fausse erreur fournisseur ou un faux appel non autorisé. Tout
échec technique effectivement constaté demeure dans le bilan. Le juge frais
évalue séparément les assertions de la réponse et les preuves indisponibles.

`audit_natif_codex_dev5_r2_mcp_tronque.py` réutilise l'audit indépendant initial
intact et ajoute la reconstruction locale des réceptions tronquées. Il vérifie
les octets assainis, les appels, les métadonnées de transport et leurs empreintes
avec les journaux natifs réels, sans appel réseau ni écrasement de pièce. Les
reçus antérieurs demeurent inchangés. L'audit complet exige 16 répondants,
16 juges et 32 identités retenues distinctes.

Cette campagne mesure des lectures de fichiers fragmentées dans Codex. Elle
n'atteste pas une activation native Skill, une installation de plugin, un smoke
Claude ou une qualification juridique. `release_ready=false` reste obligatoire.
