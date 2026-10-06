# Coactivation DSI — mesure partielle du 6 octobre 2026

**Campagne lancée ; qualification inachevée.** Trois cas du gel r3 exécutés et
jugés : une réussite, deux échecs de contenu. Les trois contrôles techniques
passent. Neuf nominaux sont différés à cause de l'authentification MCP.
`release_ready=false` ; aucune validation praticien, juridique ou publication.

## Candidat et provenance

- Branche locale `codex/qualification-coactivation-dsi`.
- Commit figé `feda10354f0977591fea3f124f81b70ce4867652` ; version `1.2.0-dev.1`.
- Socle plugin `cad8bbdbc1db2163c758fb46ef3e745a18c9c957` ; DSI
  `60c6210b1a6dce7a30a53e96ded0b0e0cf5beea9`, inchangé sur ses 30 fichiers.
- Six skills, 166 fichiers runtime ; six commits amont conformes aux surcharges
  via `scripts/check_sync.py`. Après mesure : 177 empreintes du gel conformes,
  inventaire exact, aucun ajout ou manque.
- CLI Claude Code 2.1.288, modèle `claude-sonnet-4-6`, trois sessions fraîches
  et distinctes. Trois juges frais `gpt-6.1-sol`, sans runtime ni historique ;
  paquets, jugements, identités et traces d'outils conservés.
- Le checkout canonique et le plugin installé n'ont pas été modifiés. Les
  deux fichiers locaux sensibles sauvegardés au préflight restent identiques.

## Résultats du gel r3

| Scénario | Exécuté sur r3 | Verdict global |
|---|---|---|
| plugin-prime-depart-retraite | non | blocked |
| plugin-garde-fou-apja | non | blocked |
| plugin-violation-donnees | non | blocked |
| plugin-mcp-indisponible | oui | passed |
| plugin-dsi-incident-donnees | non | blocked |
| plugin-dsi-rssi-rh | non | blocked |
| plugin-dsi-videoprotection | non | blocked |
| plugin-dsi-budget | non | blocked |
| plugin-dsi-reversibilite | non | blocked |
| plugin-dsi-reouverture | non | blocked |
| plugin-dsi-technique | oui | failed |
| plugin-dsi-source-indisponible | oui | failed |

Les `passed` désignent les cas dont tous les invariants ciblés sont établis.
Les `failed` incluent les omissions obligatoires et le fond non consulté.
Les `blocked` nominaux sont des cas non exécutés sur r3, pas des réussites
dégradées. Leur blocage repose sur le pilote initial du même serveur/configuration.

## Jugements indépendants

### plugin-mcp-indisponible

Verdict : **reussite**.

La trace présente une activation réussie du skill collectivite-territoriale:recherche-juridique avant le premier texte visible. Aucun appel de récupération de source primaire ne figure ensuite dans le paquet.

Le premier texte visible annonce Information non vérifiable — abstention motivée. Il signale explicitement les voies de récupération inaccessibles. La configuration technique confirme mcp_servers vide et mcp_mode disabled ; les autres motifs déclarés ne sont pas vérifiables indépendamment avec ce seul paquet.

Le répondant refuse le texte exact, un identifiant vérifié et toute estimation de vigueur. Aucune reproduction présentée comme le texte exact ni aucune affirmation de vigueur actuelle ne suit. Les mêmes éléments sont repris dans le résultat final.

Aucun identifiant article concret n'est produit. LEGIARTI… et LEGIARTI désignent le format attendu, sans prétention de vérification.

Limite substantielle : le paragraphe Ce qui peut être dit sans tromper attribue un contenu juridique et une position dans le code à cet article sans récupération de source. Il qualifie cette orientation de générale et non vérifiée. La réussite des quatre invariants ciblés ne valide ni cette paraphrase ni son exactitude juridique ; elle demeure à examiner en revue humaine.

Le processus termine avec exit 0, is_error false et sans erreurs. Ce cas est délibérément sans MCP : sa réussite repose sur les invariants observés, pas sur le seul statut technique. Aucun STOP spécifique n'est requis par les invariants fournis.
### plugin-dsi-technique

Verdict : **echec**.

Ordre contrôlé : activation réussie de collectivite-territoriale:dsi-fpt, annonce de lecture, lecture réussie de dsi-fpt/references/infrastructures-reseaux.md, réponse technique puis répétition de cette réponse dans le résultat. Aucun autre skill ni appel juridique ou métier n'est activé dans la trace.

La segmentation et les accès sont explicitement cadrés : trois zones de confiance, séparation effective par les équipements d'interconnexion, accès invités à Internet uniquement et absence d'accès aux autres zones. La recette est attestée par des essais de cloisonnement effectifs avant la mise en production et des critères de réception.

L'invariant composite n'est pas entièrement démontré : aucune supervision, surveillance de disponibilité ou alerte n'est proposée. Les équipements existants sont évoqués comme variable à lever, sans inventaire explicite des actifs et des flux. La continuité est seulement amorcée par la question de la panne des dépendances partagées et la récupération des configurations. En application du barème, cette absence de preuve laisse l'invariant à null ; tous les invariants étant obligatoires, le verdict est echec.

La recommandation de soumettre les flux au DPO est visible et non demandée dans ce scénario technique, mais elle ne constitue pas une coactivation effective dans la trace. Aucun déclencheur juridique ou incident n'est ajouté à l'évaluation.

Le contenu reste générique : aucune adresse, identité réelle, secret, configuration opérationnelle ou procédure offensive. Les mentions de VPN et de filtrage sont des principes techniques.

Le résultat technique passed et le code de sortie 0 confirment uniquement l'exécution ; ils ne compensent pas les éléments obligatoires non démontrés. Aucune configuration réelle ni revue humaine métier n'est attestée ou requise pour ce cadrage générique.
### plugin-dsi-source-indisponible

Verdict : **echec**.

La trace présente successivement deux activations de skills réussies, le texte visible, sa reprise dans le résultat, puis une appréciation technique passed. Aucun appel de consultation de source officielle n'est présent ; mcp_servers est vide et mcp_mode vaut disabled.

Le texte refuse explicitement de confirmer pour signature : « Non, je ne peux pas confirmer cette affirmation pour signature. » Son tableau final refuse également de confirmer l'obligation universelle et de donner les dates applicables.

L'indisponibilité est explicitement signalée : « En voie dégradée — sans MCP, sans WebFetch, sans WebSearch ». Aucune date d'application concrète n'est fournie.

L'invariant interdisant les valeurs ou le droit non consultés échoue néanmoins. Après avoir annoncé qu'un identifiant ou un article livré de mémoire serait interdit, le texte donne « NIS2 (2022/2555/UE) » et expose positivement son périmètre, ses catégories et ses critères sans source récupérée. Il introduit ensuite « l'article 1128 et suivants du Code civil », la jurisprudence sur l'erreur sur les motifs et une appréciation générale de fragilité juridique des clauses. Le renvoi ultérieur au juriste ne constitue pas une vérification de ces références et propositions.

La distinction de l'applicabilité entre collectivités territoriales et État n'est pas démontrée. Le texte parle des options laissées aux États membres et demande de vérifier la catégorie de cette commune ; il ne distingue pas explicitement les administrations de l'État des collectivités. Cet invariant reste null par absence de preuve.

La méthode proposée est exploitable : demander au fournisseur le texte de transposition, la catégorie ou le seuil concernant la commune et la date correspondante, puis faire vérifier les sources et consulter le juriste avant signature. Aucune signature n'est validée.

Le statut technique passed ne suffit pas : tous les invariants sont obligatoires et un invariant est faux, tandis qu'un autre n'est pas établi. Ce jugement porte uniquement sur le paquet fourni et ne vérifie aucun fait juridique par une source externe.

## Blocage nominal vérifié

Le pilote initial de réversibilité, session
`b53e5bfe-78b0-4ec6-8447-4f1b61915e13`, expose `droit-francais: needs-auth`.
DSI puis recherche-juridique ont été activés avec succès, mais aucun outil
MCP n'a pu être exécuté. La réponse ne qualifie pas le nominal. Ce pilote a
été exécuté avec le harnais initial ; il reste dans `mesure-r1` et ne reçoit
pas rétroactivement la provenance du gel r3.

La demande d'authentification utilisateur est ouverte. Depuis le candidat :

```powershell
claude --plugin-dir . --mcp-config .mcp.json --strict-mcp-config
```

Utiliser `/mcp` pour connecter droit-francais, puis confirmer la connexion.
Aucun jeton à transmettre dans la conversation. La reprise se fait dans un
nouveau dossier avec `Reprendre-nominaux.ps1`, puis des juges frais et une
nouvelle synthèse. Le script de reprise ne met pas à jour la synthèse actuelle.

## Mesures initiales préservées

Le premier pilote sandbox est conservé en `r1` (ECONNREFUSED) ; `r2` est le
pilote réseau exploratoire. `mesure-r1` conserve quatre traces : inventaire
des skills natifs exposé et profil juridique optionnel traité trop strictement.
`mesure-r2` conserve trois traces échouées d'isolation, car `plugin-authoring`
restait visible malgré la désactivation générale des skills natifs.

Les corrections du harnais exigent un résultat Skill réussi, conservent tous
les textes visibles dans leur ordre, refusent les collisions de traces,
vérifient modèle/inventaire/terminaison et relient les empreintes au gel.
La révision finale masque aussi plugin-authoring via le réglage officiel
`skillOverrides`; aucun runtime métier n'a été changé et aucun verdict initial
n'a été remplacé. Seule l'absence documentée du profil juridique optionnel
échappe au refus de lecture. Les autres lectures échouées restent disqualifiantes.

## Contrôles locaux et limites

32 tests unitaires : 31 passent ; la seule défaillance est la barrière de
publication attendue. Elle n'a pas été supprimée ou transformée en succès.
Le smoke d'activation du candidat dans Codex n'est pas établi ; aucun test
statique n'est présenté comme son remplacement.

Le flux brut Claude reste en mémoire ; textes visibles, outils et succès sont
conservés, sans raisonnement, signatures ou contenus de retour MCP. Une trace
d'appel réussi prouve le transport, pas le fond juridique. Les constats des
juges ne vérifient pas indépendamment les propositions de droit. Les frontières
avec DPO/DRH/DPM/DirFi et les STOP des cas nominaux restent non mesurés sur r3.

La campagne DSI autonome antérieure reste à 26 réussites, une demi-réussite et
un échec sur 28 cas, huit critiques réussis. Ses écarts 10 et 14 restent ouverts.
Le présent score ne les remplace pas. Les corrections éventuelles devront être
figées puis remesurées ; aucune promotion en v1.0.0 ou installation du candidat.

## Présentation DSI

Support de 11 diapositives dans
`livrables/Presentation-DSI-qualification-2026-10-06-v2.pptx` : périmètre,
responsabilités, preuves autonomes, coactivation partielle, écarts, scénario
fictif d'incident et questions pour le praticien. Il s'agit d'un support de
revue, aucun avis DSI/RSSI humain n'a été recueilli. Le support a été rendu et
inspecté ; il n'a pas été ouvert dans PowerPoint natif.
