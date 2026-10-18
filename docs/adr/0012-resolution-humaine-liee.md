# ADR 0012 — Résolution humaine liée des invariants non vérifiables

Date : 2026-10-18. Décision de Jo, lot T43-L15.
Statut : accepté pour l'assemblage ; smoke et preuve de release encore absents.

Ce fichier est additif. L'ADR `0012-reference-mesure-dcp-autonome.md` demeure
intacte ; les deux décisions sont identifiées par leur chemin complet.

## Règle fermée

Un invariant automatique `non_verifiable` ne peut être compté comme respecté
que si un avis humain daté du décideur **Jo**, lié par SHA-256 à la session du
run, à sa trace et au résumé de la campagne exacte, juge ce cas **conforme**.
Une `violation` ou un échec technique ne sont jamais résolubles par cet avis.
Les statuts automatiques originaux ne sont ni écrasés ni réécrits. La preuve
dérivée expose séparément statut automatique, résolution humaine et liens.

Les deux avis existants lient le résumé et les fiches effectivement relues.
L'index technique `liaisons-humaines.json` ajoute les empreintes des sessions
et traces. L'assembleur contrôle aussi que la réponse finale exacte du run
figure dans la section du cas de la fiche dont Jo a approuvé l'empreinte.
Cet index n'est ni un nouvel avis humain, ni une signature indépendante.
Un changement de décideur, date absente, session, commit mesuré, campagne,
résumé, fiche ou empreinte est refusé. Les fixtures et diagnostics restent refusés.

## Réserve et décision globale

La réserve de Jo sur `plugin-prime-depart-retraite` est conservée textuellement
dans la preuve, la revue et le run concernés. Elle ne modifie pas les constats
automatiques. Elle ne permet pas de résoudre un `non_verifiable` : seul le
verdict humain `conforme` le permet. La décision globale explicite de Jo est
nécessaire pour représenter `human_legal_validation:true`, avec couverture
des dix-huit cas et maintien visible de toute réserve. L'assembleur ne crée
jamais cet avis et ne l'infère pas d'une relecture modèle.

## Commit mesuré et tête de packaging

La campagne conservée reste mesurée sur
`08f92936dd0ae09775a2d2293bae315cdf20847d`. Les sessions, traces, résumé,
plan, autorisation et avis sont copiés octet pour octet ; aucun commit mesuré
n'est remplacé dans une pièce originale. Le lot ne change aucun octet des
skills, de la configuration distribuée, des cas ou du protocole de campagne.

La qualification d'une tête descendante de packaging distingue explicitement
`measurement_commit` et commit cible. L'assembleur exige identité intégrale
du runtime, de la configuration, des cas, d'upstream et de tout l'outillage
mesuré, à l'exception fermée de l'assembleur lui-même et du nouveau module
de résolution. Le diff Git doit rester limité à cet assemblage, l'ADR, les
tests et les pièces de preuve. Tout autre runtime, changement du protocole
ou nouveau scénario exige une nouvelle mesure ; aucune mesure n'est transférée
à un runtime différent. Les projections dérivées indiquent leur provenance,
conservent les pièces originales et ne se présentent pas comme de nouveaux runs.

## Barrières maintenues

Les contrôles automatiques, les seuils, l'ADR 0007 et la séparation validate/
release restent inchangés. Le qualificateur de release et
`test_preuve_courante_correspond_au_runtime` ne sont pas modifiés. L'assemblage
reste refusé tant que le smoke réel isolé sur la tête cible n'est pas complet,
lié et réussi. Aucune preuve `release-1.3.0.json` n'est créée en L15.
L'installation, l'authentification séparée et les deux appels smoke doivent
être autorisés avant exécution. Aucun appel modèle ni push dans ce lot.
