# Nouvelle campagne native r2 : lectures bornées et contextes frais

Les 16 questions et le barème de 124 invariants sont identiques au candidat
dev.5. Les entrées et 166 fichiers runtime sont conservés en fragments exacts
UTF-8 de 8 000 caractères maximum. Le contrôle reconstitue leurs octets et SHA,
sans modifier le candidat. Chaque rôle r2 est créé sans historique et possède
une identité native, un modèle réel, un début et une fin propres.

La campagne r1 est conservée comme exploratoire. Une sortie native enregistrée
intégralement pouvait être tronquée dans le contexte visible du modèle. Le
contrôle expérimental d'une lecture de recherche-juridique/SKILL.md a montré un
marqueur explicite de troncature malgré le budget 55000. Il ne permet donc pas
d'attester une lecture contextuelle intégrale des premières réponses r1. Aucun
score, réponse, source reçue ou jugement r1 n'est transféré à r2.

Les répondants r2 lisent d'abord les six fragments complets de leur entrée,
puis les descripteurs et tous les fragments des fichiers qu'ils choisissent
dans le runtime autorisé. Les groupements sont liés aux véritables call_id.
Les exports datés et SHA précèdent les créations des répondants et des juges.
L'ordre, les sorties exactes et l'écriture littérale unique sont contrôlés.
Les seuls suffixes de présentation acceptés sont un LF ou un CRLF terminal,
sans modifier le journal natif brut.

Le runtime est chargé par fichier : `activation_kind=file_read_fragments`.
`full_runtime_context_verified=true` atteste les lectures bornées observées,
pas une installation ou une activation native Skill. Toute exigence littérale
« via Skill » reste sans preuve native. Les STOP et frontières de rôles sont
évalués sur les textes effectivement visibles, dans leur ordre réel.

Les appels MCP et web sont effectués dans chaque nouveau contexte r2. Les
retours web texte sont capturés et assainis. Une recherche reste une recherche ;
une page de conseils reste un résumé. Un extrait normatif de document officiel
ouvert puis recherché dans cette session peut être primaire lorsque toutes
les lignes entre deux titres consécutifs d'articles sont reçues, sans trou ni
réduction. Sa méthode, URL, référence d'outil et plage de lignes restent
explicitement conservées. `full_document_received=false` et aucune vigueur
juridique n'est inférée de cette présence.

Chaque juge frais lit le paquet complet par fragments et applique le même
barème aux seules preuves du cas. Une tentative de création refusée avant
création reste conservée séparément. Les rapports rejouent les jugements
retenus et leur liaison aux SHA ; la revue native indépendante du coordinateur
complète cette vérification.

L'activation réelle d'un plugin Codex et son smoke d'installation ne sont pas
attestés. Les revues humaines, juridique/métier et DSI/RSSI restent ouvertes.
La release garde `release_ready=false`.
