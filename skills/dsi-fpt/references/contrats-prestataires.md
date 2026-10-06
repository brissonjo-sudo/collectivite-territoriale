# Branche — Contrats et prestataires

## 1. Périmètre / Exclusions

Piloter l'exécution des contrats informatiques : niveaux de service,
maintenance, licences, réversibilité, propriété et restitution des données.
Organiser le traitement des écarts, d'un éditeur défaillant et d'une fin de
contrat avec des engagements contrôlables.

Passation, choix de procédure et critères → hors périmètre : nommer le
service de la commande publique et arrêter ce volet. Clauses RGPD → `dpo-ct` ;
aspects financiers → `dirfi-fpt`, selon les bascules de `SKILL.md` §5.5–5.6,
sans illustration. Choix d'hébergement → `references/cloud-hebergement.md` ;
migration applicative → `references/applications-interoperabilite.md` ;
sécurité → `references/securite-si.md`. Ne pas traiter l'archivage électronique.

## 2. Questions couvertes

- Comment constater que le prestataire ne respecte pas ses engagements ?
- Que conserver pour décider et documenter une réponse à un écart ?
- Comment exiger une réversibilité techniquement vérifiable ?
- Que faire lorsqu'un éditeur refuse de restituer les données ?
- Comment préparer la sortie et éviter une interruption de service ?

## 3. Arbre de traitement

Passer par `references/analyse-situation.md`. Incident ou accès aux traces de
personnes → garde-fous `SKILL.md` §5.2–5.3 avant tout contenu métier.

`écart de service → contrat opposable, faits, impact et criticité → réponse
proportionnée et continuité → clause, pouvoir et procédure vérifiés → dossier
d'écart et décision documentée`.

`refus de restitution ou fin de contrat → données, droits, formats, accès et
dépendances → plan de sortie → fondement contractuel et textes applicables
vérifiés → exigences de restitution et procès-verbal de contrôle technique`.

Si la demande relève de la passation, arrêter cette branche. Si le fondement
juridique manque, poursuivre uniquement le diagnostic technique, sans
annoncer un droit acquis ou une sanction.

## 4. Variables à lever

- Mode internalisé, mutualisé ou externalisé ; entité titulaire du contrat et
  interlocuteur habilité à agir.
- Catégorie de collectivité, taille seulement si un texte en dépend ; date
  de référence et état du contrat.
- Documents contractuels disponibles, ordre de priorité, clauses particulières,
  CCAG éventuellement incorporé et dérogations.
- Criticité du service, fonctionnement dégradé, dépendances et capacité de
  reprendre l'exploitation.
- Nature et sensibilité des données, exigences reçues du DPO ; formats et
  documentation utiles à leur exploitation.
- Prestataires, sous-traitants techniques, licences et composants tiers ;
  preuves des écarts et mesures déjà prises.

## 5. Règles métier

### Contrat opposable et niveaux de service

Lire le contrat avant d'appliquer une règle. Le CCAG relatif aux techniques de
l'information et de la communication n'est pas automatiquement applicable :
le registre `references/references-verifiees.md` le rattache à une référence
expresse du marché. Vérifier cette incorporation et les dérogations avant
d'utiliser ses dispositions, à confirmer en version consolidée.

Décrire un niveau de service par l'objet mesuré, la plage de fonctionnement,
la méthode de mesure, les exclusions, l'acteur qui constate et le traitement
des écarts. Séparer prise en charge, contournement, rétablissement et
résolution ; un ticket clos ne prouve pas un service rétabli. Vérifier les
engagements réellement souscrits ; ne pas inventer de disponibilité ou de
délai. Faire valider la reprise par le responsable métier concerné.

### Écarts, pénalités et modification

Constituer une chronologie factuelle non nominative, relier chaque écart à
une clause, faire constater ses effets sur le service et conserver les
échanges utiles. Demander au prestataire une analyse et un plan correctif
avec preuves attendues. Ne pas déduire d'un écart technique un droit
automatique à pénalité, résiliation ou suspension.

Avant toute proposition juridiquement engageante, faire vérifier clause,
compétence, forme de la demande et procédure par l'interlocuteur juridique
ou contractuel. Pour une modification, documenter le besoin technique et ses
effets ; ne pas annoncer qu'un avenant est légalement possible sans examiner
le régime applicable. `recherche-juridique` valide vigueur, conflit et
jurisprudence ; les effets financiers relèvent de `dirfi-fpt`.

### Attribution du fond juridique

Activer effectivement `recherche-juridique` avant toute conclusion sur les
droits, clauses opposables, frais ou obligations de restitution. Présenter
ces conclusions sous **Analyse recherche-juridique**, avec preuve primaire
récupérée, date et applicabilité. Une future relecture par le service juridique
ne remplace pas ce volet. Sans preuve, ce rôle formule les points à vérifier
et s'abstient ; la DSI poursuit seulement le diagnostic et les mesures techniques.

### Restitution et réversibilité

Distinguer accès à une interface, export brut et reprise exploitable. Exiger
un inventaire des données et configurations à restituer, les formats,
relations, pièces associées, documentation et moyens de vérifier intégrité
et complétude. Prévoir l'assistance technique, les dépendances de licence,
la continuité et la preuve de fin des accès. Le contenu RGPD relève de
`dpo-ct`.

Une clause technique doit définir un résultat contrôlable : périmètre de
sortie, responsabilités, éléments remis, contrôle de reprise et traitement
des écarts. Tester un export puis une reprise dans un environnement autorisé,
avec données fictives ou préparées selon les exigences reçues. Une mention
« données appartenant à la collectivité » ne prouve ni le droit de tout
réutiliser ni la capacité de sortir. Vérifier contrat et droits de licence.

Pour le changement de fournisseur cloud, le règlement européen sur les
données est une piste à confirmer en version consolidée, identifiée dans
`references/references-verifiees.md`. Vérifier qualification du service,
dispositions concernées et calendrier avant d'annoncer un droit ou l'absence
de frais ; renvoyer le choix technique à `references/cloud-hebergement.md`.

### Maintenance, licences et défaillance

Clarifier correctifs, évolution, assistance et maintien de compatibilité.
Documenter les composants dont le droit d'usage ou le support peut s'arrêter.
Ne pas supposer qu'un abonnement, un développement payé ou une remise de code
transfère tous les droits. Exiger les pièces qui établissent ce qui peut être
utilisé, modifié, transmis ou exploité après la fin du service.

Face à un éditeur défaillant, traiter en parallèle continuité, conservation
des éléments utiles et capacité de reprise. Faire vérifier la situation
juridique par le service compétent ; ne pas improviser une procédure de
recouvrement ou un accès non autorisé. Le plan technique de reprise relève
de `references/crise-cyber-continuite.md`.

## 6. Procédures

Pour un écart, demander d'abord la clause et les faits disponibles ; annoncer
les pièces manquantes. Faire confirmer l'impact par le métier, rassembler les
constats non nominatifs et demander la correction par le canal contractuel.
Vérifier les conditions de toute mesure proposée avant décision de l'acteur
habilité. Contrôler le résultat obtenu, puis fermer le dossier sur une preuve
de retour au service, pas sur une déclaration du prestataire.

Pour une sortie, inventorier les éléments à reprendre, confirmer les accès
autorisés et organiser un test de restitution. Vérifier complétude, cohérence,
lisibilité et capacité d'exploitation. Préparer le basculement et son retour
arrière avec `references/applications-interoperabilite.md` ; faire valider le
service métier. Obtenir les éléments de clôture exigibles sans supprimer
prématurément les preuves. Vérifier chaque délai contractuel ou légal avant
de fixer le calendrier.

## 7. Déclencheurs de vérification

Appliquer `references/socle-sources-verification.md` avant d'affirmer un droit
de propriété, restitution, pénalité, modification, résiliation ou changement
de fournisseur ; avant d'imposer un délai ou un contenu obligatoire.
Vérifier l'applicabilité du texte à la collectivité et au type de contrat,
puis son incorporation éventuelle. Une fiche commerciale et un guide ne
remplacent ni le contrat ni un texte officiel.

## 8. Pièges et confusions fréquentes

- Appliquer le CCAG sans référence contractuelle ni lecture des dérogations.
- Confondre engagement annoncé, engagement souscrit et résultat constaté.
- Confondre propriété des données, droits de licence et export exploitable.
- Accepter une réversibilité sans test ou sans documentation de reprise.
- Annoncer une pénalité ou une résiliation sur le seul constat d'une panne.
- Traiter une passation ou une clause RGPD après un renvoi : arrêter le volet.
- Collecter des journaux nominatifs pour démontrer un écart sans appliquer
  `SKILL.md` §5.3 ; restaurer après un incident sans `SKILL.md` §5.2.

## 9. Données et valeurs à vérifier

Consulter `references/references-verifiees.md` pour le CCAG informatique,
le code de la commande publique limité à l'exécution et la modification, et
le règlement européen sur les données. Confirmer la version applicable,
les dispositions effectivement vérifiées et les limites signalées.

Relire les délais de réclamation, correction et sortie, conditions de
pénalité, frais, préavis, durées de maintenance et calendrier des droits
invoqués. Ne citer aucune valeur sans source datée ;
`references/cache-valeurs.md` indique les points officiels à consulter.

## 10. Écrits et livrables

Produire selon le besoin : dossier d'écart, exigences techniques de
réversibilité, plan de sortie, inventaire des éléments remis ou compte rendu
de contrôle de reprise. Séparer faits établis, pièces manquantes, engagements
contractuels et exigences proposées. Une exigence nouvelle n'est pas un
engagement déjà opposable.

Utiliser `references/templates/cahier-des-charges-technique.md` via
`references/ecrits-numerique.md` pour formaliser le besoin technique,
sans traiter la passation. Pour une solution en ligne, mobiliser
`objets/solution-saas.md`. Produire `[INCOMPLET]` si contrat ou éléments
essentiels manquent ; ne pas simuler une mise en demeure définitive.

## 11. Double échelle [risque / confiance]

Appliquer `SKILL.md` §5.1. Le suivi technique d'un service non critique peut
relever de [moyen / stable]. Le refus de restitution ou une sortie sans
solution de reprise appelle [élevé / à vérifier]. Un service public essentiel
menacé et une décision contractuelle incertaine peuvent être critiques :
double vérification, puis abstention sur le droit si le doute persiste.
Le constat technique fiable ne donne pas une confiance juridique stable.

## 12. Checklist de branche

- Garde-fous incident et surveillance appliqués en premier si déclenchés ?
- Contrat, incorporation du CCAG et dérogations effectivement lus ?
- Écart relié à un engagement et à une preuve, sans données nominatives ?
- Décideur et canal contractuel identifiés ; mesure engageante vérifiée ?
- Applicabilité et calendrier des textes vérifiés avant annonce d'un droit ?
- Sortie testable, données exploitables, licences et continuité prises en compte ?
- Frontières passation, `dpo-ct`, `dirfi-fpt` respectées sans illustration ?
- Livrable produit ou `[INCOMPLET]` ; références internes nommées par chemin ?
