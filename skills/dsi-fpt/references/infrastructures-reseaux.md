# Branche — Infrastructures et réseaux

## 1. Périmètre / Exclusions

Couvrir réseaux, sites distants, écoles, téléphonie, interconnexions, postes,
parc, salle serveur et alimentation. Aider à choisir un socle exploitable,
maîtriser ses dépendances et organiser la sobriété matérielle et la fin de
vie des équipements.

Choix d'hébergement externe → `references/cloud-hebergement.md` ; politique
de sécurité, comptes, sauvegardes → `references/securite-si.md` ; continuité
et ordre de reprise → `references/crise-cyber-continuite.md`. Doctrine des
équipements de vidéoprotection → `dpm-fpt`. Budget → `dirfi-fpt` ; passation
des marchés hors périmètre. Ne pas développer ces frontières.

Incident en cours ou récent → afficher d'abord le garde-fou `SKILL.md` §5.2.
Accès aux contenus ou traces d'une personne, ou dispositif de surveillance →
afficher d'abord `SKILL.md` §5.3. Aucun secret ni plan d'architecture réelle
exploitable ne doit être demandé ou reproduit.

## 2. Questions couvertes

- Comment séparer les usages d'une école et garder un réseau administrable ?
- Comment choisir les liaisons et les dépendances de sites distants ?
- Quand une redondance protège-t-elle réellement le service ?
- Comment prioriser le renouvellement et maintenir un parc hétérogène ?
- Comment organiser la sortie d'un équipement sans perte ni divulgation ?

## 3. Arbre de traitement

`besoin de site ou de parc → garde-fous → usages, responsabilité et
dépendances → options exploitables → contrôles de service et de sécurité →
choix documenté → réception et dossier d'exploitation`.

| Situation | Variables déterminantes | Décision / vérification | Livrable |
|---|---|---|---|
| Réseau d'école | Usages pédagogiques, administratifs et invités, acteurs exploitants, équipements partagés | Séparer les zones de confiance et limiter les échanges au besoin validé ; contrôler le fonctionnement de chaque usage | `objets/site-reseau.md` et fiche de choix |
| Site distant | Applications nécessaires, liaison, identité, capacité locale, conséquence d'une coupure | Choisir un fonctionnement compatible avec les dépendances et le mode dégradé acceptable | Dossier de site |
| Redondance | Points communs de liaison, alimentation, administration, localisation et prestataire | Ne retenir une protection qu'après identification des défaillances communes et essai de bascule autorisé | Analyse de dépendances et preuve de bascule |
| Parc à renouveler | Support éditeur, maintenabilité, usage, état et exposition | Traiter d'abord les équipements devenus non maîtrisables ; prolonger ceux dont le service reste démontré | Plan de parc et écarts attribués |
| Fin de vie | Destination, stockage local, récupération métier, traçabilité | Contrôler la sortie après validation de la récupération et du traitement des données ; réserver le régime non vérifié | Bordereau de sortie et preuve de traitement |

## 4. Variables à lever

- Mode internalisé, mutualisé ou externalisé ; responsable de chaque site
  et frontière d'exploitation entre collectivité et partenaires.
- Catégorie et taille seulement si un texte en dépend ; date de référence.
- Services publics soutenus, utilisateurs par familles d'usage, criticité et
  fonctionnement dégradé acceptable.
- Nature et sensibilité des données ; flux nécessaires décrits abstraitement,
  sans adresse, identifiant ou configuration réelle.
- Dépendances communes : accès, identité, résolution de noms, énergie,
  équipements de liaison, maintenance et outils d'administration.
- Prestataires et contrats en place ; qui possède les équipements, les
  configurations, les accès et la documentation d'exploitation ?
- Support et disponibilité de remplacement, capacité d'intervention locale,
  conditions physiques d'exploitation et preuves d'essais.

## 5. Règles métier

### Réseaux et sites

Partir des usages et du propriétaire du service, puis définir des zones de
confiance. Séparer les usages publics ou invités des usages administratifs
et des fonctions d'administration ; justifier les échanges nécessaires.
Un réseau distinct de nom ne démontre pas une séparation effective : faire
contrôler les limites et leur exploitation sans fournir de configuration
réelle dans le skill.

Pour une école, ne pas supposer que tous les équipements ou tous les usages
relèvent du même exploitant. Établir les responsabilités et dépendances avec
les acteurs compétents avant de proposer la séparation. Faire valider les
besoins de service sans traiter les règles de surveillance ou de données
personnelles.

Pour un site distant, déterminer ce qui reste utilisable quand une liaison
ou une dépendance centrale manque. Une liaison supplémentaire n'améliore
pas la continuité si elle partage la même défaillance. Contrôler les
dépendances de bout en bout et le retour au fonctionnement normal. Les
objectifs et priorités de continuité sont instruits par
`references/crise-cyber-continuite.md`.

### Exploitabilité et téléphonie

Exiger un propriétaire d'exploitation, une documentation à jour, une
procédure de changement autorisée et la possibilité de récupérer les
configurations. Éviter une architecture que seul un intervenant sait
administrer. Les accès et droits d'administration relèvent de
`references/securite-si.md` ; les engagements d'intervention relèvent de
`references/contrats-prestataires.md`.

Pour la téléphonie, analyser ensemble liaison, alimentation, équipements,
service d'appel et moyens alternatifs. Faire vérifier les fonctions requises
et le fonctionnement dégradé par un essai autorisé. Ne pas promettre un
appel disponible parce que les terminaux s'allument ; ne pas inventer
d'obligation sectorielle sur les appels ou leur enregistrement.

### Parc, énergie et conditions physiques

Tenir un inventaire utile : famille d'équipement, usage, responsable,
maintenance, état de support et destination envisagée. Prioriser selon la
maintenabilité et l'effet d'une panne ; ne pas déduire la fin de vie d'un âge
uniforme. Standardiser quand cela simplifie l'entretien sans bloquer les
besoins métiers.

Identifier les dépendances physiques : alimentation, refroidissement,
contrôle des accès et incidents environnementaux. Dimensionner selon le
service attendu et faire vérifier la capacité réelle ; une alimentation de
secours sans essai ne constitue pas une preuve de continuité. Ces repères
sont des **bonnes pratiques techniques**, pas un régime réglementaire
automatique ; les règles spécialisées non vérifiées restent réservées.

### Sobriété et fin de vie

Comparer prolongation, réparation, réaffectation et remplacement selon
l'utilité métier, le support et la possibilité de sécuriser l'équipement.
La sobriété ne justifie pas de conserver sans traitement un équipement
non maintenable. Orienter la stratégie globale vers
`references/gouvernance-strategie.md`.

Avant une sortie, faire valider la récupération des données utiles et des
configurations autorisées, le retrait des accès et le traitement des supports
par des acteurs habilités. Demander une preuve adaptée au type de support et
à sa destination ; un écran réinitialisé n'est pas une preuve d'absence de
données. En présence d'un incident, ne pas lancer d'effacement et revenir
au garde-fou. Ne fournir ni commande d'effacement ni geste irréversible.

La réglementation des déchets d'équipements électriques et électroniques
et les obligations de réemploi des achats publics ne sont pas vérifiées
dans le socle actuel. Ne pas en énoncer les règles : nommer le besoin de
vérification officielle et maintenir la frontière de passation.

## 6. Procédures

Pour un choix de site, supposer un besoin de conception ou de modification
sans incident actif ; sinon appliquer le STOP en premier.

1. Décrire les usages, services, responsables et dépendances, en termes
   abstraits ; demander le mode d'exercice s'il change l'option.
2. Dessiner les zones fonctionnelles et les échanges nécessaires sans
   architecture identifiable ; faire valider le besoin par les métiers.
3. Comparer les options sur exploitabilité, panne commune, accès,
   maintenabilité et capacité de retour à l'état précédent.
4. Planifier une modification réversible, ses contrôles et les personnes
   qui autorisent l'intervention et valident le service.
5. Réceptionner avec des essais de fonctionnement et, si prévu, de bascule
   dans un périmètre autorisé ; consigner les réserves.
6. Remettre le dossier d'exploitation et attribuer les écarts non levés.

Pour la fin de vie, établir destination et présence de supports, faire
valider la récupération et le traitement des données par les personnes
compétentes, contrôler les preuves puis mettre à jour l'inventaire. Vérifier
à la source toute obligation invoquée et ses délais avant de conclure.

## 7. Déclencheurs de vérification

Appliquer `references/socle-sources-verification.md` lorsqu'une réponse
invoque réemploi, déchets, règle de sécurité physique, prescription de
téléphonie ou exigence sectorielle. Ne pas étendre une doctrine de l'État à
la collectivité ni transformer un conseil ANSSI en obligation.

Pour les références absentes de `references/references-verifiees.md`, ne
pas affirmer le régime. Fournir le point à faire vérifier sur la source
officielle et l'analyse technique indépendante de ce régime. Les versions
de référentiels et qualifications citées déclenchent aussi une vérification.

## 8. Pièges et confusions fréquentes

- Assimiler noms de réseaux différents et séparation effective des usages.
- Supposer que tous les équipements d'une école ont le même responsable.
- Appeler « redondance » deux moyens dépendant d'une même panne.
- Ajouter du matériel sans prévoir maintenance et accès de secours.
- Déduire une capacité de bascule d'une documentation commerciale.
- Prolonger un équipement non maintenable au seul nom de la sobriété.
- Confondre réinitialisation d'un poste et traitement démontré des supports.
- Inventer des taux de réemploi ou un régime DEEE sans source lue.
- Développer la doctrine de vidéoprotection ou la passation d'un marché.
- Demander un plan réseau réel ou une extraction nominative pour cadrer un besoin.

## 9. Données et valeurs à vérifier

Consulter `references/references-verifiees.md` pour les sources autorisées
de doctrine et la stratégie de numérique responsable. Les textes DEEE,
réemploi et prescriptions sectorielles non présents au registre restent à
vérifier avant usage. Vérifier seuils, taux, échéances, périmètre des
équipements et versions de référentiels à leur source, sans les produire de
mémoire. `references/cache-valeurs.md` indique où reprendre une vérification.

Les capacités techniques et dates de fin de support se contrôlent auprès
de leur source compétente et du dossier d'exploitation ; ne pas en déduire
un délai légal de remplacement.

## 10. Écrits et livrables

- Dossier de site via `objets/site-reseau.md` : usages, responsables,
  dépendances, zones fonctionnelles et critères de réception abstraits.
- Fiche de choix → `references/templates/fiche-projet-si.md` : options,
  exploitabilité, panne commune, risques et décision attendue.
- Exigences et contrôles de réception →
  `references/templates/cahier-des-charges-technique.md` ; exécution du
  contrat → `references/contrats-prestataires.md`.
- Plan de parc : équipements par familles, maintien, remplacement,
  réaffectation et preuve de sortie, sans détails identifiants.
- Dossier d'exploitation : responsabilités, changements, essais et réserves ;
  les informations sensibles restent dans les circuits internes autorisés.

Ce contenu est opérationnel ; vérifier séparément tout élément présenté
comme obligatoire.

## 11. Double échelle [risque / confiance]

Appliquer `SKILL.md` §5.1. Inventaire et choix de parc courant : risque
**moyen**, confiance **stable** sur la méthode. Modification d'un réseau
soutenant plusieurs services ou dépendance partagée : risque **élevé**,
confiance **à vérifier** sans cartographie et essais. Sortie de supports
sensibles ou service essentiel sans solution de repli : risque **élevé** ou
**critique** selon l'effet ; ne pas autoriser un geste irréversible sur un
constat incomplet. Régime sectoriel non sourcé : abstention sur le droit.

## 12. Checklist de branche

- [ ] Garde-fous `SKILL.md` §5.2 et §5.3 testés et affichés avant le contenu si déclenchés.
- [ ] Mode d'exercice, responsabilités de site et besoins métier levés.
- [ ] Frontières cloud, sécurité, crise et `dpm-fpt` respectées ; passation exclue.
- [ ] Dépendances et pannes communes examinées ; exploitabilité démontrable.
- [ ] Contrôles, réception, réserves et retour au fonctionnement normal prévus.
- [ ] Fin de vie précédée d'une validation et de preuves, sans geste irréversible ici.
- [ ] Doctrine distinguée d'obligation ; DEEE/réemploi non vérifiés réservés.
- [ ] Aucun secret, détail d'architecture identifiable ou donnée nominative.
- [ ] Livrable, responsable et chemins internes nommés.
