# Branche — Crise cyber et continuité

## 1. Périmètre / Exclusions

Organiser la gestion de crise cyber : cellule de crise, décisions,
traçabilité, communication interne et reprise contrôlée. Préparer les plans
de continuité d'activité (PCA), de reprise d'activité (PRA) et les exercices.

Tester systématiquement le garde-fou `SKILL.md` §5.2 ; pour un incident en
cours ou récent, l'afficher intégralement **avant tout autre contenu**, puis
utiliser `objets/incident-securite.md`. Ne pas le reformuler ni le rendre
conditionnel après son déclenchement. Accès aux contenus ou traces d'une
personne → `SKILL.md` §5.3, avant tout contenu technique.

Exclure qualification et notification de violation de données, information
des personnes → `dpo-ct`. Nommer les décisions de communication publique,
d'arrêt du service et de rançon comme relevant de l'exécutif, sans les
traiter. Nommer la plainte et la procédure pénale sans les dérouler. Aucun
mode opératoire offensif ni intervention sur un système tiers.

## 2. Questions couvertes

- Comment organiser une collectivité dont les outils habituels sont indisponibles ?
- Comment éviter qu'une reprise détruise les preuves ou réintroduise la compromission ?
- Quels services reprendre en priorité, avec quelles dépendances ?
- Comment préparer un PCA/PRA exploitable par une équipe réduite ou un prestataire ?
- Comment éprouver la chaîne de décision avec un exercice ?

## 3. Arbre de traitement

`incident ou préparation → garde-fous → mode d'exercice, service et autorité →
organisation et priorités métier → preuve de maîtrise → décision de reprise →
journal et dossier de retour d'expérience`.

| Situation | Variables à lever | Décision / vérification | Livrable |
|---|---|---|---|
| Incident actif ou récent | Faits confirmés, services affectés, appui disponible, moyens de coordination fiables | Après le STOP, mobiliser les acteurs habilités, préserver les preuves et documenter le périmètre sans geste irréversible | Journal et `references/templates/rapport-incident.md` |
| Reprise envisagée | Conservation des preuves, environnement de reprise, état des copies, dépendances, validation métier | Autoriser seulement le périmètre dont les conditions sont réunies ; maintenir les autres en attente | Fiche de décision de reprise |
| Préparation PCA/PRA | Service essentiel, fonctionnement dégradé possible, capacité réelle d'exploitation | Faire arbitrer les objectifs métier puis démontrer une reprise et son ordre | Plan opérationnel attribué |
| Exercice | Objectif d'apprentissage, participants, périmètre sans effet sur la production | Tester coordination et arbitrages ; mesurer les écarts constatés | Compte rendu → `references/retex.md` |

## 4. Variables à lever

- Mode internalisé, mutualisé ou externalisé ; capacité d'astreinte et appui
  spécialisé ; contrat ou convention qui répartit les interventions.
- Catégorie et taille si le régime invoqué en dépend ; date de référence.
- Services atteints ou menacés, conséquences pour les usagers, dépendances
  partagées et priorité métier validée.
- Faits observés et incertitudes ; distinguer constat, hypothèse et décision.
- Données possiblement touchées, sans les analyser juridiquement ; bascule
  `dpo-ct` dès que la situation l'appelle.
- Disponibilité de moyens de coordination hors du SI suspect, du dossier de
  continuité, des sauvegardes et des accès de reprise.
- Prestataire, garantie d'assurance éventuelle, contacts fonctionnels et
  autorité habilitée à décider. Ne jamais demander leur identité réelle ici.

## 5. Règles métier

### Gouverner la crise

Après affichage du garde-fou, séparer pilotage, coordination technique et
information interne. L'exécutif porte les décisions qui lui reviennent ;
la DGS coordonne les services selon l'organisation retenue ; la DSI/RSSI
documente et propose les actions ; l'appui spécialisé instruit la réponse
technique dans son mandat. Un prestataire ne décide pas à la place de la
collectivité.

Tenir un journal : moment du constat, source du fait, décision, autorité,
acteur, périmètre et résultat. Ne pas y déposer de secret, donnée nominative
ou architecture identifiable. Conserver séparément les éléments sensibles
dans les circuits autorisés ; le skill ne les collecte pas.

Choisir un moyen de coordination dont la fiabilité est établie ; ne pas
supposer sûrs les comptes et outils du SI touché. Donner aux services une
instruction interne cohérente sur le fonctionnement dégradé et le canal
d'alerte, sans anticiper la communication publique de l'exécutif.

### Préserver et se faire appuyer

La préservation des preuves précède les opérations irréversibles, selon
`SKILL.md` §5.2. Faire tracer qui autorise et qui exécute les interventions ;
faire cadrer la collecte par les personnes compétentes. Ne fournir ici ni
commande d'extraction, ni investigation nominative, ni procédure pénale.

Les CSIRT territoriaux constituent un point d'orientation documenté dans
`references/references-verifiees.md`. Vérifier l'interlocuteur et son champ
d'intervention sur la liste officielle ; ne pas faire du CERT-FR le guichet
automatique de toute collectivité ni promettre une prise en charge.

### Continuer et reprendre

Le PCA organise le maintien d'un service acceptable en mode dégradé ; le PRA
organise le rétablissement du SI qui le soutient. Faire définir par les
métiers les conséquences acceptables d'une interruption et d'une perte de
données ; confronter ces objectifs aux capacités réellement démontrées.
Ne pas les fixer par une durée générique ni par la seule fiche d'un éditeur.

Construire l'ordre de reprise à partir des dépendances : accès de confiance,
socle technique, application, données, interfaces et validation métier.
La première application demandée n'est pas nécessairement la première à
restaurer. L'état des sauvegardes relève de
`references/securite-si.md` ; l'architecture du socle relève de
`references/infrastructures-reseaux.md`.

Conditionner chaque ouverture à des preuves : conservation des éléments
nécessaires, périmètre de compromission instruit, environnement de reprise
maîtrisé, copies évaluées, accès revus, contrôles techniques et métier
réussis. Prévoir surveillance de service et retour à un fonctionnement
dégradé si les critères ne tiennent plus. Ne pas assimiler reprise partielle
et fin d'incident.

### Obligations et assurance

Ne pas déduire un signalement légal d'un guide ou d'une directive non
transposée. Vérifier le régime réellement applicable à l'entité dans
`references/references-verifiees.md`, puis la source à la date de la demande.
Pour une garantie cyber, distinguer condition légale d'indemnisation,
conditions du contrat et instruction de l'assureur. Le code des assurances
prévoit une condition de plainte pour certaines garanties et victimes,
**à confirmer en version consolidée** ; vérifier ces conditions sans
présumer la garantie et sans en déduire une règle sur la rançon.

## 6. Procédures

Pour un incident, suivre l'organisation ci-dessous **après le STOP**, avec
appui compétent ; elle ne constitue pas un mode d'investigation technique.

1. Consigner les faits connus et les services affectés ; marquer les
   hypothèses et les informations manquantes.
2. Activer les responsables et les circuits prévus ; vérifier l'appui
   technique disponible et le canal de coordination.
3. Faire documenter la préservation et les mesures conservatoires par les
   acteurs habilités ; éviter toute action irréversible non instruite.
4. Faire arbitrer les services prioritaires et organiser leur mode dégradé.
5. Préparer les conditions de reprise et le contrôle de chaque lot ; garder
   en attente le lot dont les conditions ne sont pas réunies.
6. Consigner la décision d'ouverture, les validations et les écarts ; suivre
   le service rétabli puis conduire `references/retex.md`.

Pour préparer les plans, supposer l'absence d'incident actif : recenser
services et dépendances, convenir des objectifs métier, attribuer les rôles,
préparer un dossier accessible si le SI est indisponible, puis éprouver une
reprise autorisée. Faire un exercice de coordination sans effet réel sur les
services ; le kit ANSSI est une **doctrine d'appui, non normative**.

Les délais de plainte, d'assureur ou de signalement se vérifient à la source
et dans le contrat ; ceux relevant de `dpo-ct` restent à cette frontière.

## 7. Déclencheurs de vérification

Appliquer `references/socle-sources-verification.md` pour toute obligation de
signalement, condition d'assurance, délai, compétence de décision ou régime
NIS2 invoqué. Vérifier la publication et le champ de la transposition ; ne
pas traiter une version de projet comme applicable.

Vérifier les dispositifs d'assistance sur leur source officielle à la date
du besoin. Sans source accessible, nommer ce qu'il reste à vérifier et
continuer l'organisation opérationnelle sans promettre un droit à assistance.

## 8. Pièges et confusions fréquentes

- Restaurer rapidement avant conservation des preuves ou évaluation des copies.
- Rallumer un système touché pour « voir si cela fonctionne ».
- Utiliser automatiquement la messagerie compromise pour coordonner la crise.
- Confondre indisponibilité technique et décision d'arrêt d'un service public.
- Déduire une obligation de plainte ou un délai d'un contrat non lu.
- Affirmer que l'assurance autorise ou impose un paiement de rançon.
- Dérouler une notification de données ou la procédure pénale dans cette branche.
- Présenter un plan jamais exercé comme une capacité de reprise démontrée.
- Fermer l'incident parce qu'une application fonctionne à nouveau.

## 9. Données et valeurs à vérifier

Consulter `references/references-verifiees.md` pour la condition d'assurance,
les régimes de signalement et les sources des dispositifs d'assistance.
Revérifier délais de plainte et de signalement, échéances contractuelles,
calendriers de transposition et édition des guides utilisés à leur source.
Le cache de maintenance est exclu du paquet runtime ; ne pas le charger ni
en reproduire une valeur. Les objectifs de continuité propres au service
sont des arbitrages à obtenir et à tester, pas des valeurs légales présumées.

## 10. Écrits et livrables

- Journal de crise : faits, incertitudes, décisions, acteurs fonctionnels,
  autorisations et résultats, sans données sensibles.
- Rapport factuel → `references/templates/rapport-incident.md` ; ne pas
  qualifier juridiquement une violation ni présumer son contenu obligatoire.
- PCA/PRA : service, mode dégradé, dépendances, responsables, moyens,
  conditions de déclenchement, validation de reprise et essais.
- Fiche de reprise : périmètre, preuves réunies, réserves, validation métier,
  décision attendue et possibilité de retour au mode dégradé.
- Plan d'amélioration après exercice ou incident → `references/retex.md`.

## 11. Double échelle [risque / confiance]

Appliquer `SKILL.md` §5.1. Incident actif, preuves ou reprise de service
essentiel : risque **critique** ; confiance **à vérifier** tant que les faits
ou les conditions de reprise sont incomplets, avec abstention sur les
décisions non instruites. Préparation d'un plan : risque **élevé** si son
échec interrompt un service essentiel ; confiance **stable** sur la méthode,
pas sur une capacité non testée. Une obligation non confirmée conduit à une
abstention précise sur ce point.

## 12. Checklist de branche

- [ ] `SKILL.md` §5.2 systématiquement testé ; STOP intégral en premier pour un incident en cours ou récent.
- [ ] `SKILL.md` §5.3 appliqué avant toute demande sur les traces d'une personne.
- [ ] Frontière `dpo-ct` tenue ; décisions de l'exécutif et procédure pénale seulement nommées.
- [ ] Faits séparés des hypothèses ; mode d'exercice et acteurs identifiés.
- [ ] Preuves préservées avant irréversible ; aucune intervention offensive.
- [ ] Priorités métier et conditions de reprise explicites et démontrables.
- [ ] Sources, applicabilité et délais vérifiés sans valeurs de mémoire.
- [ ] Journal et rapport sans secret, donnée nominative ou architecture identifiable.
- [ ] Livrable et chemins internes nommés ; écarts à traiter attribués.
