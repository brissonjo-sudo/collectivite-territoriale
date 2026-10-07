Je propose de partir des usages pour définir trois zones fonctionnelles — administrative, pédagogique et invités — puis de justifier chaque échange entre elles. C’est une hypothèse de conception à instruire ; aucune configuration n’est figée.

Faits fournis : réseau des écoles, informatique interne, trois familles d’usages, absence d’incident et demande purement technique. L’inventaire, les dépendances et les capacités d’exploitation ne sont pas connus.

Avant de choisir une solution, les questions à lever sont :

- Quels services et équipements utilise chaque famille, notamment les imprimantes ou équipements partagés ?
- Qui possède et exploite chaque équipement : informatique interne, partenaire éducatif ou autre intervenant ?
- Quels échanges entre usages sont nécessaires, et qui valide leur utilité ?
- Quel fonctionnement reste acceptable si Internet, une liaison entre sites ou un service central devient indisponible ?
- Qui assure le support, reçoit les alertes et peut intervenir pendant les périodes d’utilisation ?

Le cadrage suivant reprend `dsi-fpt/SKILL.md`, `references/infrastructures-reseaux.md` et `objets/site-reseau.md`. Les responsables proposés sont à désigner ; aucune validation n’est présumée.

| Volet | Inconnues à lever | Preuves à réunir | Recette attendue | Responsable proposé |
|---|---|---|---|---|
| Périmètre, actifs et dépendances | Sites, familles d’équipements, services communs, exploitants | Inventaire fonctionnel et matrice des échanges nécessaires, sans identifiants réels | Chaque usage et chaque dépendance disposent d’un responsable ; les besoins sont confirmés | Référent informatique avec les responsables des écoles et partenaires concernés |
| Support et exploitation | Couverture du support, maintenabilité, capacité d’intervention | Dossier d’exploitation, état du support des équipements, circuit d’alerte et de changement | Une panne de service est détectée, attribuée et prise en charge lors d’un essai prévu | Responsable d’exploitation à désigner |
| Continuité | Pannes communes, services prioritaires, moyens de repli disponibles | Carte des dépendances et scénario de fonctionnement dégradé validé par les utilisateurs | Essai autorisé de perte d’une dépendance, puis retour au fonctionnement normal | Informatique pour l’essai ; responsables métiers pour l’acceptation |
| Attribution des actions | Qui prépare, autorise, exécute et réceptionne un changement | Liste des rôles, critères de réception et réserves attribuées | Chaque action et chaque écart ont un responsable ; possibilité de retour à l’état précédent documentée | Pilote du projet à désigner |

Pour la continuité, `references/crise-cyber-continuite.md` conduit à faire définir les besoins par les métiers, puis à les confronter aux capacités démontrées. Une liaison supplémentaire ne constitue pas une protection si elle partage la même panne.

L’option fonctionnelle à comparer, selon `references/infrastructures-reseaux.md`, est la suivante :

- **Administratif** : accès aux services nécessaires au travail administratif.
- **Pédagogique** : accès aux ressources et équipements nécessaires aux activités pédagogiques.
- **Invités** : accès Internet séparé des ressources internes, selon le besoin validé.
- **Administration technique** : fonctions de gestion des équipements séparées des usages ordinaires.

Les échanges entre zones seraient limités aux besoins explicitement validés. Un équipement partagé serait traité comme une dépendance à examiner, sans créer automatiquement un accès général entre zones. Des noms de réseaux différents ne prouvent pas une séparation effective.

La réception future vérifierait, dans un périmètre autorisé, que chaque service nécessaire fonctionne, que les accès non prévus restent bloqués et que le support et le repli sont utilisables. La supervision porterait ici sur la disponibilité et l’état des services, sans analyse de l’activité des personnes.

Le livrable attendu est un dossier de site : inventaire fonctionnel, zones et échanges proposés, responsabilités, support, dépendances, critères de réception et réserves. La méthode est exploitable ; la faisabilité locale reste à vérifier par l’inventaire et les essais.
