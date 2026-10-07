# Triage ordinaire des écarts Codex R2 — 2026-10-07

Cette analyse est **hors mesure**. Elle ne remplace aucun répondant ni aucun juge, ne recalcule aucun score et ne modifie aucun runtime, jugement ou élément de preuve. Elle porte sur le candidat `1.2.0-dev.5`, commit de campagne `3f0d34bd068e3427edc9335a4f1415aaf1c7c98d`, source runtime `ebeee944e878b11177d5ccb85d9043c4c97260a9`. Aucun outil Claude n'a été exécuté.

## Conclusion de triage

La campagne dev.5 peut être achevée et archivée honnêtement avec ses échecs et ses limites. Elle ne qualifie pas une activation native de Skill ou du plugin : les événements déclarent `activation_kind=file_read_fragments` et `actual_plugin_activation_verified=false`.

Un **correctif candidat distinct** est néanmoins nécessaire pour traiter complètement le défaut textuel confirmé au §5.2 DSI : le STOP prescrit des démarches externes sans preuve, alors que le contrat prioritaire impose de retirer chaque instruction juridique non étayée. Il serait utile d'y joindre une clarification du passage de responsabilité DirFi dans les commentaires intermédiaires. Ces changements doivent suivre l'archivage du gel dev.5. Les résultats dev.5 restent associés à leurs SHAs ; aucun score n'est transféré au nouveau candidat. La release demeure bloquée.

L'échec de transfert juridique du cas09 mérite une clarification limitée ; il ne justifie ni d'inventer un droit contractuel ni de transformer une abstention correcte en consultation contractuelle réalisée. Le cas16 montre que le même invariant peut être satisfait par une attribution préalable et une abstention explicitement tenue par le rôle juridique, sans pièces absentes présentées comme examinées.

## Pièces consultées

- `qualification-coactivation-dev5-codex-r2/manifest.json` et `suite.json` : candidat et attentes originales.
- Réponses, jugements et traces JSONL des cas09 `plugin-dsi-reversibilite`, cas10 `plugin-dsi-reouverture`, cas15 `plugin-spontane-budget`, cas16 `plugin-spontane-reversibilite`.
- `Collectivite-corrections-pr5/overlays/dsi-fpt.md` : contrat prioritaire, dont garde-fou d'abord, preuve par affirmation et abstention.
- `Collectivite-corrections-pr5/skills/dsi-fpt/SKILL.md` : copie candidate, §3, §5.2, §5.6 et §5.7.

Les faits ci-dessous viennent de ces pièces actuelles. Le triage ne certifie pas les sources juridiques elles-mêmes et ne complète pas des retours tronqués. Le jugement retenu reste celui du juge frais original, même si cette analyse relève une ambiguïté.

## Cas09 — réversibilité forcée

**Jugement conservé : échec, `volet_juridique_attribue=false`.** Les neuf autres invariants sont vrais. L'événement e8 attribue déjà « la qualification du refus et les suites contractuelles » au volet recherche-juridique. La réponse e20 contient ensuite une section « Analyse recherche-juridique : vérification non aboutie » et une abstention ciblée sur l'obligation de restitution, les frais, délais, sanctions et conditions d'une mise en demeure. Cependant, son premier paragraphe confie l'examen effectif des pièces et droits au service juridique avant la décision ; le juge distingue cet examen futur d'un volet contractuel effectivement tenu dans la réponse.

**Classement : attribution insuffisamment explicite dans la synthèse, avec absence documentaire ; défaut de comportement observé, défaut du candidat non établi à lui seul.** Le §5.7 impose déjà l'attribution des conclusions contractuelles à un volet recherche-juridique, y compris en abstention. Les pièces ne sont pas fournies et l'événement e13 rapporte une troncature native du retour `get_decision` : transport réussi, intégrité du contenu non vérifiée, aucune preuve primaire disponible. Les abstentions sont donc nécessaires. Il serait incorrect de demander une conclusion contractuelle affirmative pour réparer cet invariant.

**Correction minimale utile :** préciser dans le contrat prioritaire que le rôle recherche-juridique porte, avant toute synthèse contractuelle, les constats documentaires, limites des sources, questions restant ouvertes et abstentions. La revue humaine complète ensuite ce volet ; elle n'en tient pas lieu. Une formule d'attribution doit identifier le responsable et le point exact qu'il ne peut confirmer, sans annoncer d'activation native absente. Le défaut reste ouvert pour la mesure suivante ; le score actuel ne change pas.

## Cas10 — réouverture d'incident

**Jugement conservé : échec**, avec `stop_premier=false`, `source_ou_abstention=false`, et `bascule_dpo=null`.

Le retard du STOP est directement observable : e3 commence par « Le nouvel indice impose » et annonce les chargements ; e4 émet ensuite le STOP. e24 confirme `first_visible_text_ref=e3` et `stop_first=false`. Un STOP dans la réponse finale e22 ne corrige pas ce préambule. Le contrat prioritaire et le §3 prescrivent déjà un STOP comme premier texte visible avant annonces et lectures. La cause unique n'est pas établie : il s'agit d'un comportement non conforme dans ce transport, malgré la règle et l'instruction initiale.

**Clarification utile :** inclure expressément dans les déclencheurs le nouvel indice concernant un incident ancien ou administrativement clos. Cela améliore la couverture descriptive ; cela ne prouve pas que le modèle suivra le garde-fou au prochain essai et ne remplace pas un contrôle du premier texte visible.

Le défaut de source est plus directement relié au candidat. Le §5.2 impose comme premier livrable le bloc STOP contenant : « signaler l'incident dans les circuits prévus (autorité territoriale, assureur, plainte, autorités compétentes) ; les délais se vérifient à la source ». Juste après ce bloc, il exige qu'une obligation de plainte, signalement ou notification ait une source et une date, ou ne soit pas citée. L'overlay prioritaire exige également le retrait de toute règle non récupérée, même assortie d'une réserve. **Ces instructions locales entrent en tension : le modèle est poussé à reproduire le bloc avant de pouvoir établir les obligations externes.**

La réponse e22 reproduit précisément le signalement externe impératif. e20 et e22 déclarent pourtant qu'aucun primaire pertinent n'a été reçu et réservent obligations, conditions et délais de notification. Le juge constate correctement que cette réserve tardive ne couvre pas l'instruction précise encore affichée.

**Correction nécessaire :** conserver dans le STOP les mesures conservatoires, la préservation des preuves, l'alerte opérationnelle aux responsables désignés et l'attribution des volets. Retirer l'ordre automatique de saisir assureur, plainte ou autorités externes. Attribuer ensuite l'examen des démarches externes au rôle juridique et, pour les données personnelles, au rôle DPO, avec preuve pertinente ou abstention ciblée. Le STOP ne fixe aucune obligation, aucun destinataire externe, aucune compétence ni aucun délai juridique. La correction porte sur l'ordre donné par le texte local ; elle ne prétend pas établir le droit.

`bascule_dpo=null` relève d'une autre limite : le rôle DPO et son attribution sont observables, mais les lectures de fragments ne prouvent pas une activation réelle du plugin. Une correction rédactionnelle ne peut fournir cette preuve d'hôte.

## Cas15 — budget spontané

**Jugement conservé : échec, `bascule_dirfi=false`.** Les huit autres invariants sont vrais, dont la sélection des seuls rôles attendus au sens du transport observé. Le passage de responsabilité explicite « BASCULE dirfi-fpt » apparaît dans la réponse finale e26. Les commentaires e6 et e14 discutent déjà la documentation des crédits, de l'autorité d'engagement et la portée de l'absence d'arbitrage. Le juge retient donc un transfert tardif, même si le fichier DirFi a été lu auparavant et que l'engagement reste suspendu.

**Classement : défaut de comportement observable ; clarification candidate utile, sans preuve de causalité exclusive.** Le §5.6 et le §5.7 prescrivent déjà le bloc BASCULE avant le fond réservé. L'overlay développe précisément la persistance de la bascule RH, mais ne donne pas la même portée explicite aux commentaires financiers intermédiaires. Le commentaire initial de suspension conservatoire ne doit pas devenir un diagnostic de crédits, d'imputation ou de pouvoirs attribué à la DSI.

**Correction minimale utile :** exiger explicitement BASCULE DirFi avant toute appréciation budgétaire ou financière, y compris dans le cadrage, les commentaires, tableaux et conclusions. Tant que le rôle compétent n'est pas activé, la DSI peut conserver le besoin, les faits fournis et les questions sans qualifier les crédits ni l'autorité d'engagement. Ne pas ajouter de droit, de seuil ou de procédure. Cette clarification ne résout pas l'absence d'activation native du plugin.

## Cas16 — réversibilité spontanée

**Jugement conservé : échec, `selection_spontanee=false`.** Les dix autres invariants sont vrais, dont `volet_juridique_attribue`. L'introduction e21 attribue l'examen contractuel à recherche-juridique, puis au service juridique ; la section consacrée à ce rôle porte effectivement les limites de recherche et les abstentions. Cette observation aide à préciser le cas09, sans annuler son jugement.

Les seuls rôles sélectionnés et lus correspondent à DSI et recherche-juridique, sans injonction nominative dans la question. Le juge applique cependant littéralement l'exigence de skills réellement activés : les événements e4/e5 sont des lectures de fragments et la réponse le reconnaît. **Classement : incompatibilité de preuve entre l'exigence d'activation et l'hôte de mesure choisi ; ce n'est pas une sélection métier supplémentaire ou manquante démontrée.** Les autres juges peuvent retenir un statut inconnu pour une attente comparable ; ces décisions restent inchangées.

e19 fournit un document primaire déclaré tronqué, et e23 ne retient aucun primaire exploitable. Même une attribution et une sélection satisfaisantes ne rendraient donc pas ce cas nominal réussi. L'abstention sur restitution, frais, droits, pénalités et résiliation est un comportement conservatoire correct ; une troncature ne doit jamais être reconstruite pour obtenir une réussite.

## Fin de campagne et correctif distinct

Achever les seize cas et leur audit natif, publier le rapport complet et archiver le gel dev.5 est compatible avec une campagne concluante au sens **exécutée et traçable**, malgré une qualification bloquée. Il faut conserver chaque échec, les nuances false/null et la preuve manquante d'activation native.

Après cet archivage, le correctif distinct devrait rester limité à : supprimer le signalement externe automatique du STOP ; expliciter la réouverture parmi ses déclencheurs ; rendre le transfert DirFi préalable explicite dans toute la session ; clarifier le volet juridique d'abstention avant la synthèse. Synchroniser les copies et overlays par le mécanisme existant, puis geler le nouveau candidat et maintenir `release_ready=false`. Des contrôles statiques et, si réalisés, des essais ciblés doivent être rattachés à ce nouveau SHA, sans transfert des scores dev.5.

La preuve d'activation native, les sources primaires absentes, la vigueur non établie et les revues humaines demeurent des travaux distincts. Un texte de skill ne peut pas les fabriquer. La présentation DSI peut restituer dès maintenant la campagne achevée et les corrections distinctes, en indiquant séparément ce qui est mesuré et ce qui reste à qualifier.
