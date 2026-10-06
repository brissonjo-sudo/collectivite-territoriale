# Branche — Cloud et hébergement

## 1. Périmètre / Exclusions

Comparer hébergement interne, mutualisé et cloud selon le service attendu,
les risques et la capacité d'exploitation. Traiter qualification des offres,
localisation, souveraineté, réversibilité et repérage des exigences liées à
des données particulières.

Transferts hors Union européenne et sous-traitance au sens du RGPD →
`dpo-ct` ; clauses et exécution du contrat →
`references/contrats-prestataires.md`. Budget → `dirfi-fpt` ; passation des
marchés hors périmètre. Ne pas développer ces frontières ni conclure à une
conformité générale. Incident en cours ou récent → `SKILL.md` §5.2,
affiché avant tout contenu ; demande sur contenus ou traces d'une personne
→ `SKILL.md` §5.3, affiché avant tout contenu technique.

## 2. Questions couvertes

- Quel mode d'hébergement la collectivité peut-elle réellement maîtriser ?
- Comment apprécier une offre cloud sans confondre localisation et maîtrise ?
- Que prouve une qualification et comment vérifier son périmètre ?
- Quand faut-il réserver la décision pour des données particulières ?
- Comment démontrer que les données et le service peuvent sortir de l'offre ?

## 3. Arbre de traitement

`service à héberger → garde-fous et frontières → données, criticité et mode
d'exercice → comparaison des offres exactes → vérifications officielles et
preuves → arbitrage de la collectivité → dossier et essai de sortie`.

| Situation | Variables décisives | Décision / vérification | Livrable |
|---|---|---|---|
| Choix d'hébergement | Service, équipe exploitable, responsabilités, dépendances, données | Retenir l'option dont la maîtrise et la continuité sont démontrables ; attribuer les risques restants | Fiche de comparaison |
| Offre dite souveraine ou qualifiée | Service exact, périmètre, exploitation, administration, conditions de qualification | Vérifier les preuves officielles ; faire préciser ce que l'étiquette ne couvre pas | Fiche de qualification |
| Données particulières | Nature, activité et usage, exigence reçue, cadre applicable | Réserver le choix si le régime nécessaire n'est pas vérifié ; orienter le fond des données vers `dpo-ct` | Liste des points bloquants à lever |
| Sortie d'une offre | Données, formats, métadonnées, dépendances, destination et moyens d'export | Exiger un essai autorisé de récupération puis d'usage dans la cible | Plan de réversibilité → `references/contrats-prestataires.md` |

Une origine géographique du fournisseur ou une localisation de stockage ne
suffit pas à décider. Demander les caractéristiques de l'offre précise,
sans solliciter de données ni d'architecture réelle identifiante.

## 4. Variables à lever

- Mode internalisé, mutualisé ou externalisé ; responsable métier et
  responsabilité de la collectivité ; capacités internes de contrôle.
- Catégorie et taille si un texte invoqué en dépend ; date de référence.
- Service public soutenu, criticité, interruptions acceptables, fonctionnement
  dégradé et dépendances d'accès ou d'intégration.
- Nature et sensibilité des données, exigences transmises par les
  interlocuteurs compétents, sans qualification juridique du traitement.
- Offre exacte, service utilisé, périmètre de qualification revendiqué,
  acteurs d'exploitation et accès d'administration.
- Localisation documentée du stockage, des copies et de l'exploitation ;
  éléments factuels à transmettre aux interlocuteurs compétents.
- Prestataire, contrat en place, durée d'engagement à examiner, capacités de
  sauvegarde, restitution et reprise dans une autre solution.

## 5. Règles métier

### Choisir un mode exploitable

Comparer les options sur le même service et les mêmes exigences. L'interne
suppose une équipe, des moyens physiques, une maintenance et une continuité
réelles ; le mutualisé suppose une convention et une frontière de décision
claire ; le cloud suppose des responsabilités et preuves d'exécution
explicites. Aucun mode n'est sûr par son seul nom.

La collectivité conserve la décision sur son SI. Distinguer ce que fournit
l'offre de ce que la DSI doit configurer, exploiter et contrôler : accès,
protection des données, copies, détection, incidents, continuité et sortie.
Ne pas prendre une disponibilité du fournisseur pour une continuité de
l'application ou du service public. Pour sauvegardes et accès, renvoyer à
`references/securite-si.md` ; pour reprise, à
`references/crise-cyber-continuite.md`.

### Qualification et applicabilité

SecNumCloud est une qualification d'offres selon un référentiel ANSSI :
contrôler l'offre exacte, son périmètre et son statut sur le catalogue
officiel à la date de la décision. Le référentiel impose ses exigences aux
prestataires qui demandent la qualification ; il ne crée pas, par lui-même,
une obligation générale d'achat pour les collectivités. Une offre en cours
de qualification n'est pas une offre qualifiée.

La doctrine « cloud au centre » et la disposition de la loi visant à
sécuriser et réguler l'espace numérique sur les données sensibles des
administrations de l'État ne constituent pas une obligation cloud générale
de la collectivité : le socle vérifié indique leur champ de destinataires.
Ces références peuvent éclairer un choix comme **doctrine ou référence de
bonne pratique**, sans transfert de leur caractère obligatoire. Vérifier
le statut de l'entité si elle invoque un champ particulier ; les textes
structurels se citent **à confirmer en version consolidée**.

La qualification apporte une preuve délimitée, pas une garantie de sécurité
du service complet : configuration, identité, terminal, intégration et
exploitation de la collectivité restent à examiner.

### Localisation et maîtrise

Séparer localisation physique, acteurs d'exploitation, accès techniques,
chaîne contractuelle et dépendances. Demander des pièces décrivant l'offre
et les accès possibles ; ne pas conclure à la maîtrise par la seule mention
« hébergé en France » ou « européen ». Documenter les faits nécessaires à
la décision ; le droit des transferts et de la sous-traitance reste à
`dpo-ct`, sans illustration de ce régime.

Pour une messagerie ou une application SaaS, utiliser
`objets/solution-saas.md`. La question de nationalité du fournisseur ne se
résout pas par un oui/non global : vérifier les caractéristiques de l'offre
et les exigences établies avant l'arbitrage.

### Données particulières

Ne pas appliquer un régime spécialisé sur le seul nom d'un service métier.
L'hébergement de données de santé n'est pas vérifié dans le socle actuel :
réserver l'applicabilité, le champ de certification et les obligations.
Indiquer le besoin de vérification sur la source officielle compétente
avant de conclure ; ne pas produire de règle, d'exception ou de calendrier.
Poursuivre la comparaison technique sur les points indépendants de ce régime.

### Réversibilité

Distinguer récupération des données et reconstitution d'un service utilisable.
Identifier données, métadonnées, formats, configurations utiles,
interfaces, identité et fonctionnalités dont dépend l'usage dans la cible.
Une exportation lisible n'est pas nécessairement complète ni importable.
Faire tester un jeu synthétique dans un périmètre autorisé ; demander une
preuve de complétude et de réutilisation.

Le règlement européen sur les données peut bénéficier à une collectivité
cliente de services de traitement de données, selon le champ consigné au
registre. Vérifier la disposition et la date applicables avant de conclure
sur les frais de changement ; ne pas en déduire que toute migration est sans
coût. L'organisation de la sortie et l'exécution des engagements relèvent
de `references/contrats-prestataires.md`.

## 6. Procédures

Supposer un choix prospectif ou une évolution sans incident actif. Si un
incident apparaît, appliquer le STOP avant cette procédure.

1. Établir le service attendu et les exigences métier ; lever mode
   d'exercice, données et criticité.
2. Comparer interne, mutualisé et offre cloud exacte sur accès, maintenance,
   continuité, dépendances et capacité de contrôle.
3. Dresser la matrice des responsabilités : collectivité, service mutualisé,
   fournisseur et intervenants ; identifier les tâches sans responsable.
4. Vérifier qualification, champs juridiques invoqués et pièces de
   localisation ; réserver tout régime non confirmé.
5. Éprouver récupération et réutilisation de données synthétiques,
   récupération des accès et fonctionnement dégradé dans un cadre autorisé.
6. Présenter options, risques résiduels, points bloquants et décision attendue ;
   transmettre les engagements à `references/contrats-prestataires.md`.

Pour une sortie, obtenir la cible et les dépendances, vérifier les engagements
applicables, contrôler l'essai puis faire valider la bascule par le métier.
Ne pas supprimer la source avant validation de la récupération et de la
reprise par les personnes compétentes. Les échéances se vérifient dans le
texte applicable et le contrat ; ne pas inventer un délai de sortie.

## 7. Déclencheurs de vérification

Appliquer `references/socle-sources-verification.md` pour toute obligation
de localisation, qualification, certification spécialisée, compétence,
restriction ou règle sur les frais de changement. Vérifier la catégorie de
l'entité et les destinataires du texte avant « la collectivité doit ».

Vérifier sur l'ANSSI le statut de l'offre exacte ; sur les sources officielles
des textes, la portée et la date des dispositions cloud invoquées. Sans
preuve accessible, ne pas qualifier l'offre ni valider un régime spécialisé.
Les points de fond des données personnelles restent à `dpo-ct`.

## 8. Pièges et confusions fréquentes

- Présenter « cloud au centre » comme une obligation des collectivités.
- Déduire une obligation SecNumCloud de son référentiel de qualification.
- Confondre fournisseur qualifié, offre qualifiée et service de la collectivité sécurisé.
- Assimiler candidature à une qualification obtenue.
- Confondre stockage localisé et maîtrise de tous les accès.
- Déduire le droit des données de la nationalité du fournisseur.
- Traiter une réplication fournie par le cloud comme une sauvegarde indépendante.
- Croire qu'un fichier exporté démontre la reprise dans une autre application.
- Affirmer un régime de données de santé absent du socle vérifié.
- Confondre suppression de certains frais de changement et absence de coût de migration.

## 9. Données et valeurs à vérifier

Consulter `references/references-verifiees.md` pour le champ des dispositions
cloud, le règlement européen sur les données et les sources ANSSI/DINUM.
Vérifier version de SecNumCloud, validité et périmètre de qualification,
dates d'application des frais de changement, textes modificatifs et
échéances contractuelles. Le régime de données de santé reste non vérifié.
Ne pas recopier les valeurs de `references/cache-valeurs.md` ; reprendre
la source à la date du besoin.

## 10. Écrits et livrables

- Fiche de choix → `references/templates/fiche-projet-si.md` : même besoin,
  options, responsabilités, preuves, risques résiduels et décision attendue.
- Fiche d'offre via `objets/solution-saas.md` : périmètre exact, qualification
  vérifiée, localisation documentée, dépendances et points restant à lever.
- Exigences techniques →
  `references/templates/cahier-des-charges-technique.md` ; leur exécution
  et la réversibilité contractuelle → `references/contrats-prestataires.md`.
- Compte rendu d'essai de sortie : jeu synthétique, données attendues,
  récupération obtenue, réutilisation contrôlée et écarts attribués.

Vérifier avant de qualifier un élément de contenu obligatoire. Ne pas
produire de conclusion de conformité générale ou de document de frontière.

## 11. Double échelle [risque / confiance]

Appliquer `SKILL.md` §5.1. Comparaison technique exploratoire :
**[moyen / stable]** sur la méthode si les hypothèses sont explicites.
Service essentiel, accès privilégiés ou sortie difficile : risque **élevé**,
confiance **à vérifier** sans pièces ni essais. Données particulières et
régime non vérifié : abstention sur l'obligation ; ne pas valider le choix
si ce point est bloquant. Une qualification revendiquée reste **à vérifier**
tant que l'offre exacte n'est pas confirmée officiellement.

## 12. Checklist de branche

- [ ] Garde-fous `SKILL.md` §5.2 et §5.3 testés et affichés avant le contenu si déclenchés.
- [ ] Mode d'exercice, service, données et responsabilité de la collectivité levés.
- [ ] Frontières `dpo-ct`, contrats, budget et passation tenues sans développement.
- [ ] État / collectivité et obligation / doctrine distingués explicitement.
- [ ] Offre exacte et qualification contrôlées ; aucune conclusion sur une étiquette.
- [ ] Localisation et accès documentés ; régime spécialisé non vérifié réservé.
- [ ] Responsabilités, dépendances, sauvegarde et reprise identifiées par renvoi.
- [ ] Réversibilité démontrable ; règle sur les frais vérifiée sans valeur de mémoire.
- [ ] Aucun secret, donnée nominative ou détail d'architecture identifiable.
- [ ] Options, point bloquant, preuve et livrable nommés avec leurs chemins.
