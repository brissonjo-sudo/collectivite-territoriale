# Branche — Dématérialisation et téléservices

## 1. Périmètre / Exclusions

Organiser les circuits dématérialisés et les téléservices depuis l'entrée de
la demande jusqu'à sa prise en charge par le service compétent. Choisir les
moyens d'identification, d'authentification et de signature selon l'opération
et ses risques.

**Exclusions** : mentions d'information, base légale et droit des données →
`BASCULE dpo-ct` ; fond de la démarche et validité de l'acte → service métier
et `recherche-juridique` pour l'analyse du texte. Archivage électronique →
service compétent, hors périmètre ; passation → service de la commande
publique, hors périmètre. Arrêter ces volets sans les illustrer.
Accessibilité → `references/accessibilite-numerique.md` ; sécurité et
homologation → `references/securite-si.md` ; interfaces métiers →
`references/applications-interoperabilite.md`.

## 2. Questions couvertes

- Une demande reçue par messagerie doit-elle entrer dans le circuit ?
- Comment ouvrir un téléservice sans perdre des demandes ou des pièces ?
- Quel niveau d'identification ou d'authentification pour une opération ?
- Comment organiser un circuit de signature et de délégation technique ?
- Quelles preuves de fonctionnement réunir avant l'ouverture ?
- Comment maintenir le service lors d'une indisponibilité du portail ?

## 3. Arbre de traitement

Passer d'abord par `references/analyse-situation.md`. Un incident de portail
ou une demande de surveillance impose le garde-fou de `SKILL.md` avant le
contenu technique. Une question composée d'ouverture de service mobilise
`objets/teleservice.md`.

| Question | Variables à lever | Décision | Vérification | Livrable |
|---|---|---|---|---|
| Courriel reçu d'un usager | Démarche, canal dédié porté à connaissance, exclusion éventuelle | Préserver la réception et orienter ; ne pas rejeter juridiquement sans analyse | CRPA et exceptions applicables à la démarche | Circuit de prise en charge et réponse bornée au service |
| Ouvrir un portail | Parcours, service responsable, données, criticité | Ouvrir quand prise en charge, sécurité et accessibilité sont démontrées | Recette du parcours, textes applicables et décisions requises | Dossier d'ouverture |
| Imposer un compte | Opération, niveau de risque, besoin de preuve | Choisir le moyen proportionné au besoin établi | Exigence du texte et capacités du mécanisme | Justification du dispositif d'identification |
| Signer un acte | Nature de l'acte, qualité du signataire, délégation, destinataire | Réserver le niveau requis tant que la validité n'est pas établie | Texte applicable, règlement sur les services de confiance et preuve de signature | Spécification du circuit de signature |

## 4. Variables à lever

- Mode internalisé, mutualisé ou externalisé ; propriétaire du portail et
  responsable de la prise en charge métier.
- Catégorie de collectivité et compétence concernée ; nature exacte de la
  démarche, public visé et date de référence.
- Canaux déjà annoncés, fonctionnement dégradé, criticité de l'interruption.
- Données et pièces demandées, sensibilité, exigences transmises par `dpo-ct`.
- Prestataire, contrat, interfaces métier, capacité à restituer la demande
  et à corriger un échec de transmission.
- Opération à identifier ou signer, qualité et habilitation de l'acteur,
  destinataire et éléments de preuve attendus.

## 5. Règles métier

### Réception et saisine

Ne pas décider sur la seule apparence du canal. Identifier la démarche,
l'existence d'un téléservice dédié porté à connaissance et les exceptions
applicables. Le registre `references/references-verifiees.md` fournit les
entrées CRPA concernant la saisine, les téléservices, l'information du public
et les accusés, **à confirmer en version consolidée**. Il rattache les
collectivités à la définition d'administration ; ce rattachement ne dispense
pas de vérifier l'exception propre à la démarche.

Tant que le régime n'est pas confirmé, conserver la demande reçue dans le
circuit autorisé et solliciter le service compétent. Ne présenter ni un
courriel comme toujours valable, ni un portail comme toujours exclusif.
Les effets juridiques et délais de la demande nécessitent une source.

### Parcours complet

Tester **déposer → constater la réception → transmettre au métier → traiter
les anomalies → permettre le suivi**. Prévoir les pièces invalides, demandes
en doublon, interruptions de session et échec de l'interface métier. Un
message « envoyé » ne suffit pas à prouver que la demande est prise en charge.
Attribuer chaque anomalie à un responsable ; distinguer accusé technique,
accusé juridique et état d'instruction.

### Identification et signature

Distinguer identifier l'usager, authentifier son accès et exprimer un
consentement ou une signature. Ne pas rendre le compte obligatoire par
habitude technique. Définir le besoin avec le métier puis vérifier ce que
prescrit le régime applicable.

Pour le parapheur, séparer préparation, validation et signature. La DSI
configure les habilitations à partir des décisions du responsable compétent ;
elle ne crée ni compétence de signature ni délégation. Recetter la preuve de
signature et sa vérification par le destinataire. Une image de signature ne
permet pas à elle seule de conclure à la validité d'un acte.

L'entrée du registre sur l'identification électronique et les services de
confiance n'atteste que l'existence et l'objet des textes : elle ne permet
pas d'affirmer leurs obligations publiques ni leur calendrier. Relire le
texte officiel avant toute conclusion, **à confirmer en version consolidée**.

### Sécurité et responsabilités

La collectivité conserve la décision d'ouverture, y compris si le prestataire
héberge le service. Confier la démarche d'homologation et le vocabulaire
d'attestation formelle à `references/securite-si.md`. L'ANSSI ne valide pas
le téléservice à la place de la collectivité. Les contrôles de parcours sont
des bonnes pratiques ; les prescriptions RGS se qualifient par leur texte
et leur applicabilité, sans transposer la doctrine de l'État.

## 6. Procédures

**Hypothèse : préparation d'une ouverture, sans incident actif.**

1. Le métier fixe la démarche, les états de traitement, l'interlocuteur des
   usagers et le fonctionnement en cas d'indisponibilité. Demander les
   informations manquantes, sans inventer de canal de repli.
2. Vérifier les sources pour saisine, identification et règles applicables ;
   transmettre le volet données à `dpo-ct`.
3. La DSI et le prestataire définissent le parcours et les interfaces ; le
   métier valide les preuves de prise en charge.
4. Recetter avec des données fictives les parcours nominaux et en échec,
   notamment le dépôt interrompu et l'interface indisponible.
5. Faire traiter la sécurité par `references/securite-si.md` et
   l'accessibilité par `references/accessibilite-numerique.md` ; réunir les
   décisions et réserves dans le dossier d'ouverture.
6. Le responsable compétent décide l'ouverture ; l'exploitant suit les
   demandes non remises au métier et les anomalies. Les délais légaux ou
   contractuels restent à vérifier à la source.

## 7. Déclencheurs de vérification

Appliquer `references/socle-sources-verification.md` pour la validité d'une
saisine, une exception, l'effet d'un canal dédié, un accusé juridiquement
requis, une compétence de signature, un niveau de service de confiance,
une homologation ou un calendrier applicable.

Consulter les sources officielles Légifrance, EUR-Lex et ANSSI selon l'objet.
Le registre fournit une provenance datée, jamais une lecture de la session.
Sans source accessible, livrer le circuit opérationnel et le point à vérifier,
sans trancher la validité ni produire un délai ou une version.

## 8. Pièges et confusions fréquentes

- Refuser une demande reçue hors portail sans vérifier la démarche et
  l'information donnée au public.
- Assimiler connexion, identification et signature.
- Déclarer un acte valide à partir du seul outil ou certificat utilisé.
- Appeler « accusé de réception » tout écran de confirmation.
- Ouvrir le portail sans service responsable des demandes en erreur.
- Reprendre une exigence destinée à l'État sans test d'applicabilité locale.
- Mesurer individuellement l'activité des agents à partir des traces du
  parapheur : garde-fou surveillance avant tout contenu technique.
- Réinitialiser un portail compromis pour le remettre rapidement en service :
  garde-fou incident avant toute action irréversible.

## 9. Données et valeurs à vérifier

Délais et contenu des accusés, exceptions à la saisine, effets de la démarche,
versions du RGS, niveaux de signature et d'identification requis, calendrier
du règlement sur les services de confiance et modalités de publication des
décisions de sécurité. Nommer ces points sans valeurs ; partir de
`references/references-verifiees.md`, puis relire les sources officielles.
Ne pas extrapoler depuis une référence dont seules l'existence et l'objet
ont été lus.

## 10. Écrits et livrables

- Fiche de parcours : service responsable, états, réception, transfert,
  anomalies, preuves et repli validé.
- Dossier d'ouverture : résultats de recette, décisions de sécurité,
  accessibilité, réserves, exploitation et décision du responsable compétent.
- Exigences techniques →
  `references/templates/cahier-des-charges-technique.md` ; fiche projet →
  `references/templates/fiche-projet-si.md` ; dossier de sécurité →
  `references/templates/note-homologation.md` via la branche sécurité.

Les champs opérationnels ne remplacent pas un contenu légal obligatoire :
vérifier celui-ci avant rédaction. Produire `[INCOMPLET]` si la démarche, le
signataire ou le mode de prise en charge ne sont pas établis.

## 11. Double échelle [risque / confiance]

| Situation | Repère |
|---|---|
| Maquette sans données réelles ni effet sur une demande | [faible / stable] sur le parcours technique |
| Ouverture avec responsabilité métier ou repli non établis | [élevé / à vérifier] ; compléter avant décision |
| Validité d'une saisine ou signature engageant un usager | [élevé / à vérifier] ; source avant conclusion |
| Demandes perdues ou portail suspectement indisponible | [critique / à vérifier] si incident suspecté ; garde-fou en premier |

Suivre `SKILL.md` : la confiance sur l'outil ne prouve ni compétence de
signature ni validité juridique de la démarche.

## 12. Checklist de branche

- Garde-fous incident et surveillance affichés en premier si déclenchés ?
- Bascule `dpo-ct` et autres frontières respectées, sans illustration ?
- Mode d'exercice, métier et responsable de l'ouverture identifiés ?
- Démarche, canaux annoncés et exceptions vérifiés avant conclusion ?
- Identification, authentification, signature et habilitation distinguées ?
- Réception et prise en charge démontrées, anomalies et repli attribués ?
- Accessibilité et sécurité renvoyées à leurs branches ?
- Obligation, bonne pratique, État et collectivité distingués ?
- Sources datées et applicables ; valeurs relues en session ou réservées ?
- Livrable complet ou `[INCOMPLET]`, sans donnée nominative ni secret ?
- Chemins des fichiers mobilisés cités à l'endroit utile ?
