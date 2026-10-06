# Protocole de coactivation v2

Date : 2026-10-06. Suite et harnais distincts du gel r3 précédent.
Les questions historiques restent identiques. Le runtime reste identique aux
166 fichiers mesurés ; la v2 porte sur la qualité des contrôles et des preuves.
Les anciens résultats ne deviennent pas ceux de la nouvelle mesure.

**Extension candidat corrigé.** Le profil explicite `corrected-runtime-v1`
(schéma de gel 3) permet une nouvelle mesure après correction des instructions.
Il conserve les questions et invariants v2, exige l'inventaire exact et les
octets du HEAD committé avant/après chaque cas, et déclare
`historical_scores_reused=false`. Les résultats du profil initial ne sont
pas transférés. Une modification du runtime exige un autre gel et un autre
dossier de traces ; le profil v2 historique continue de refuser ce changement.

## Exécution et isolation

Une session Claude Sonnet 4.6 fraîche par cas. Onze activations forcées et cinq
sélections spontanées, évaluées séparément. L'instruction spontanée ne nomme
pas les skills attendus et n'impose pas leur ordre. Le contrôle compare un
ensemble strict de skills réellement activés ; le juge évalue l'ordre du
fond métier et l'attribution des rôles dans le texte visible.

Permissions reprises de r3 : six skills locaux, Read limité au runtime,
MCP juridique local strict et outils de lecture expressément autorisés.
WebFetch seulement dans les cas désignés. Aucun Bash, écriture par le
répondant, hook, connecteur global ou persistance de session. Le flux brut
reste en mémoire. Un timeout produit une trace d'échec, sans conserver son
flux partiel ni le rejouer automatiquement. Aucun retry ne remplace une mesure.
Un nouveau gel impose le schéma v2 et l'inventaire de toutes ses dépendances.
Une troncature ou un masquage du texte visible empêche toute réussite : la
réponse entière n'est plus disponible pour apprécier ses invariants.

## Preuve documentaire

Chaque résultat est rattaché à son `call_id` et placé dans l'ordre réel du
texte et des appels. Un résultat non rattaché, doublonné ou sans appel
autorisé fait échouer le contrôle technique. Les extraits de sources
publiques sont bornés et assainis selon une liste fermée de champs et hôtes.
Leur contenu reste une donnée non fiable, jamais une instruction à exécuter.
L'heure de capture après processus et sa fenêtre début/fin sont distinctes
de la date de vigueur éventuellement fournie par la source.

Les natures de preuve sont distinctes : `primary_text` pour un document
structuré récupéré ; `search_result` pour une recherche ; `tool_summary`
pour le résumé produit par WebFetch. Un résumé ne devient pas un texte
primaire. Une absence, une erreur, un format inconnu ou une troncature reste
visible et ne peut être promu en preuve complète. L'empreinte porte sur le
contenu assaini, sans calculer d'empreinte de secret écarté.

La présence d'un texte ne certifie pas sa pertinence ou sa vigueur.
Le juge doit confronter les assertions à l'extrait, l'identité, les dates
et les métadonnées retournées. Une mention « vérifié » dans la réponse,
un appel réussi, une page d'accueil ou un résumé ne suffit pas. Une source
historique ou déclarée non applicable ne se valide pas comme droit actuel.
Une affirmation de droit non étayée n'est pas une abstention, même accompagnée
d'une réserve générale « à vérifier ».

## Jugement indépendant

Le juge reçoit uniquement la question, l'oracle de sélection des skills,
les objets atomiques, ce barème et la
trace assainie. Il n'a accès ni au runtime, ni aux scores antérieurs, ni aux
autres réponses. Tous les invariants sont obligatoires et restent critiques.
La valeur `null` signifie absence de preuve ; elle ne prouve pas que la
proposition juridique est fausse. Ne pas remplacer un invariant manquant par
`true` ni qualifier une mesure nominale comme réussite dégradée.

Le STOP exigé précède **tout texte visible**, y compris annonces de lecture
et commentaires avant outils. Les outils peuvent être appelés avant le STOP
tant qu'aucun texte visible ne le précède. Le contrôle automatique du premier
texte est éliminatoire, sans remplacer l'évaluation du contenu du garde-fou.
Un transfert annoncé n'autorise pas le rôle initial à continuer le fond réservé.

Pour chaque objet atomique, utiliser une valeur JSON booléenne ou `null`, des
références `event_id` réellement présentes et une justification précise.
La base `retrieval` nécessite un événement `source_evidence` avec texte
primaire disponible ; `abstention` nécessite un texte observable et un
invariant l'autorisant explicitement. Pour un `false`, citer la contradiction.
Pour un `null`, expliquer la pièce manquante ; les références peuvent être vides.

Format du fichier `jugement.json` :

```json
{
  "case_id": "identifiant_du_cas",
  "trace_sha256": "empreinte_du_paquet",
  "verdict": "reussite|echec|bloque",
  "invariants": {
    "identifiant_atomique": {
      "status": null,
      "basis": "observation|retrieval|abstention|missing",
      "evidence_refs": [],
      "rationale": "Preuve observable ou limite précise."
    }
  }
}
```

## Décision et portée

Les résultats technique, comportemental et documentaire sont séparés.
Un échec technique ou un invariant faux donne `echec`. Un invariant non
démontré donne `bloque`. Une mesure nominale sans contenu primaire exploitable
reste `bloque`, même si une abstention correcte satisfait un invariant
alternatif. Le mode explicitement sans sources est évalué selon ses propres
exigences, sans simuler une consultation officielle.

Une réussite nécessite toutes les exigences applicables. Le validateur
refuse les références fabriquées, les valeurs coercibles (`1` pour `true`),
le STOP tardif validé et la promotion d'un résumé ou d'une troncature.
Il ne démontre pas à lui seul l'appréciation métier du juge. La production
effective du jugement doit aussi être liée à la trace du sous-agent, sans
remplacer cette identité par une affirmation du coordinateur.

Conserver chaque gel, réponse, jugement, trace et score. Les résultats d'un
pilote technique ne valent pas campagne complète. La revue DSI/RSSI,
la revue juridique humaine et le smoke du candidat dans Codex restent des
barrières distinctes ; `release_ready=false` reste maintenu.

Documentation d'intégration consultée via Context7 :
[flux CLI Claude](https://code.claude.com/docs/en/headless),
[types des résultats d'outils](https://code.claude.com/docs/en/agent-sdk/typescript),
[résultats MCP](https://modelcontextprotocol.io/specification/2026-07-28/server/tools).
Le contrat du serveur juridique a été contrôlé dans son code local ;
un format de déploiement différent sera signalé comme preuve indisponible.
