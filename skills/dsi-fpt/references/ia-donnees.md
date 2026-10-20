# Branche — IA et données

## 1. Périmètre / Exclusions

Organiser la gouvernance technique des données et encadrer l'usage de l'IA,
y compris générative, par la collectivité. Préparer l'analyse d'un usage,
la maîtrise du système et la transparence des traitements algorithmiques
dans le champ de la DSI.

**Exclusions** : base légale, AIPD et droit des données personnelles →
`BASCULE dpo-ct` ; fond RH, adoption et opposabilité d'une charte →
`BASCULE drh-fpt` ; vidéoprotection algorithmique → garde-fou surveillance
de `SKILL.md` et `BASCULE dpm-fpt`. Ouverture des données → service compétent,
hors périmètre ; passation → service de la commande publique, hors périmètre.
Arrêter ces volets sans les illustrer. Hébergement →
`references/cloud-hebergement.md` ; interfaces et données de référence →
`references/applications-interoperabilite.md`.

## 2. Questions couvertes

- Encadrer l'usage d'un assistant génératif par les agents.
- Évaluer un pilote avant d'en faire un outil de production.
- Déterminer ce qu'il faut vérifier avant de qualifier un système à haut risque.
- Préparer les informations techniques nécessaires à la transparence d'un
  traitement algorithmique intervenant dans une décision individuelle.
- Préserver la maîtrise des données et de l'outil face à l'éditeur.
- Définir une charte technique, les rôles et les conditions d'arrêt d'un usage.

## 3. Arbre de traitement

Lire `references/analyse-situation.md` avant l'analyse. Surveillance de
personnes ou incident suspecté impose le garde-fou de `SKILL.md` en premier ;
le caractère « expérimental » ne le suspend pas.

| Question | Variables à lever | Décision | Vérification | Livrable |
|---|---|---|---|---|
| Assistant génératif pour rédiger | Finalité, données envoyées, diffusion du résultat, fournisseur | Usage borné sur données fictives ou autorisées, avec contrôle humain ; différer si les conditions manquent | Conditions de service, sécurité et exigences de `dpo-ct` | Fiche d'usage et charte technique |
| Trier ou recommander sur des demandes | Effet sur l'usager, autonomie, service public, rôle de l'humain | Réserver le déploiement tant que risque et conditions ne sont pas établis | Usage réel, catégorie réglementaire et régime en vigueur | Dossier d'évaluation et décision de déploiement |
| Qualifier le haut risque | Destination du système, rôle de la collectivité, personnes affectées, date | Décrire la qualification à instruire, sans déduire du nom commercial | Règlement publié et modificatifs applicables | Fiche de qualification sourcée ou réservée |
| Expliquer une décision algorithmique | Contribution de l'outil, paramètres, données et opérations | Réunir les éléments techniques pour le service responsable | CRPA, portée de l'obligation et limites légales | Dossier technique de transparence |

## 4. Variables à lever

- Mode internalisé, mutualisé ou externalisé ; responsable métier, exploitant,
  décideur du déploiement et capacité à arrêter l'outil.
- Catégorie de collectivité, service et personnes concernés ; taille si une
  obligation en dépend ; date de référence.
- Finalité réelle, système utilisé, rôle de la collectivité, degré d'autonomie
  et influence du résultat sur une action ou une décision.
- Origine, qualité et sensibilité des données ; données transmises au
  fournisseur, réutilisation annoncée et exigences de `dpo-ct`.
- Criticité, possibilité d'une reprise humaine, erreurs acceptables définies
  par le métier et mécanisme de contestation à faire traiter au bon niveau.
- Prestataire, contrat, hébergement, documentation, changement du modèle ou
  des règles et moyens de vérifier le résultat sans dépendre de l'éditeur.

## 5. Règles métier

### Décider à partir de l'usage

Décrire **entrée → traitement → résultat → destinataire → effet réel**.
Ne qualifier ni le système ni le risque à partir de l'étiquette « assistant »
ou « simple recommandation ». Vérifier si l'humain comprend, peut corriger
et peut écarter le résultat : une validation systématique ne démontre pas
un contrôle effectif.

Pour la qualification réglementaire, partir de
`references/references-verifiees.md` : règlement européen sur l'IA,
**à confirmer en version consolidée**. Le registre rattache le déployeur à
une autorité publique ; l'applicabilité d'une obligation particulière dépend
ensuite du rôle, du système, de l'usage et de la date. La collectivité peut
avoir d'autres rôles qu'un déployeur selon sa contribution : les faire
instruire avant de conclure. Ne pas généraliser depuis un seul cas d'annexe.

Relire l'acte publié et les éventuels modificatifs pour les catégories et
calendriers ; la consolidation et la lecture historique ne prouvent pas
l'état du droit dans la session. L'analyse d'impact sur les droits
fondamentaux ne se confond pas avec l'AIPD, dont le fond relève de `dpo-ct`.
La DSI fournit la description technique au responsable de l'analyse requise.

### IA générative et maîtrise des données

Définir les usages autorisés et les données admises avant d'ouvrir l'outil.
Ne pas transmettre de donnée nominative, secret ou architecture réelle à
l'assistant pour obtenir la réponse de ce skill. Pour un usage de production,
faire établir les exigences de données par `dpo-ct`, puis traduire celles-ci
en configuration technique et contrôles.

Prévoir vérification du contenu, références et calculs par une personne
compétente avant utilisation. Tester les réponses inventées, les documents
contenant des instructions parasites et la divulgation indue, avec données
fictives et sans mode opératoire offensif. Ne pas exposer un résultat à
l'usager ou déclencher une action à conséquence avant que les conditions de
validation et d'arrêt soient démontrées.

Exiger de la documentation sur accès, réutilisation des entrées, évolution
du service et restitution des éléments utiles. Dépendances d'hébergement →
`references/cloud-hebergement.md` ; engagements exécutables →
`references/contrats-prestataires.md`. Ces contrôles sont des bonnes
pratiques ; ne pas les présenter comme une liste d'obligations réglementaires.

### Gouvernance et évaluation

Désigner le propriétaire métier des données et le responsable de qualité ;
renvoyer la source faisant autorité à
`references/applications-interoperabilite.md`. Évaluer le système sur des
situations représentatives, avec résultats attendus et erreurs recensées.
Faire décider la mise en production sur cette preuve et le risque résiduel,
pas sur une démonstration commerciale. Refaire l'évaluation pertinente quand
modèle, données, règles ou finalité changent.

### Transparence algorithmique

Distinguer l'information relative à une décision individuelle et la
publication des règles des principaux traitements. Le registre contient
les entrées CRPA correspondantes, **à confirmer en version consolidée**, avec
une réserve sur le seuil de publication non vérifié. Ne pas inventer le seuil
ni conclure qu'il dispense d'information sur une décision individuelle.

Recueillir contribution du traitement, données utilisées, paramètres et
opérations décrites par le système pour préparer la réponse du service
responsable. Ne promettre ni publication intégrale ni refus de communication
sans vérifier le champ et les limites du texte ; la résolution juridique
relève de `recherche-juridique`. L'ouverture générale des données reste hors
périmètre. Ne transposer aucune charte de l'État à la collectivité comme une
obligation.

## 6. Procédures

**Hypothèse : nouveau pilote sans données réelles, sans incident ni surveillance.**

1. Le métier exprime la finalité, l'effet du résultat et le fonctionnement
   sans l'outil. Demander les variables manquantes avant de recommander son
   déploiement ; une finalité inconnue empêche la qualification.
2. La DSI décrit système, données et dépendances ; le responsable compétent
   fait instruire rôle, catégorie et obligations sur source officielle.
   Transmettre le volet de conformité des données à `dpo-ct`.
3. Définir les critères de réussite et d'arrêt, la validation humaine et la
   reprise du service ; intégrer les engagements du fournisseur.
4. Évaluer sur des jeux fictifs, documenter erreurs et limites ; ne pas
   annoncer de performance sans résultats démontrés.
5. La direction compétente décide de poursuivre, corriger ou arrêter sur les
   preuves disponibles. La DSI met en œuvre les mesures retenues, sans se
   substituer au métier pour la décision à effet sur l'usager.
6. Suivre les changements, incidents et conditions d'arrêt. Pour une charte,
   limiter le livrable au contenu technique ; adoption → `drh-fpt`.
   Les dates d'application et échéances se vérifient à la source.

## 7. Déclencheurs de vérification

Appliquer `references/socle-sources-verification.md` avant de qualifier le
système, un rôle, une catégorie de haut risque, une pratique interdite,
une analyse requise, une obligation de transparence, un seuil ou une échéance.
Sources : EUR-Lex pour règlement et modificatifs, Légifrance pour le CRPA.
Les chartes et guides publics sont de la doctrine sauf texte qui les rend
opposables à la collectivité.

Si la source ou le champ ne peut être confirmé, réserver la qualification et
livrer le dossier à instruire. Aucun calendrier contenu dans le registre ou
un cache ne vaut une vérification de session.

## 8. Pièges et confusions fréquentes

- Déclarer un outil à faible risque parce qu'il est génératif ou expérimental.
- Croire qu'un résultat validé mécaniquement par un agent est sous contrôle.
- Autoriser les données réelles parce que le fournisseur promet de ne pas
  les réutiliser, sans exigences établies ni contrôle du contrat.
- Confondre l'AIPD et l'analyse d'impact sur les droits fondamentaux.
- Assimiler toutes les décisions algorithmisées à une même obligation.
- Inventer le seuil de publication ou recopier un calendrier ancien.
- Mesurer ou surveiller les personnes avec l'IA : garde-fou surveillance
  avant tout contenu technique et bascules de `SKILL.md`.
- Une divulgation suspecte via l'assistant relève d'abord du garde-fou
  incident ; ne pas effacer les traces pour désactiver rapidement l'outil.

## 9. Données et valeurs à vérifier

Catégories réglementaires, rôles, obligations du déployeur public, analyses
requises, actes modificatifs, calendrier d'application, seuil de publication
des règles algorithmiques et contenu de l'information sur une décision.
Nommer sans valeurs ; consulter `references/references-verifiees.md` puis
les sources officielles. Une entrée limitée à un passage lu ne prouve pas
toutes les pratiques interdites ni toutes les catégories de haut risque.

## 10. Écrits et livrables

- Fiche d'usage : finalité, données, résultat, effet, responsable, limites et
  contrôles avant utilisation.
- Dossier d'évaluation : cas fictifs, résultats, erreurs, conditions d'arrêt,
  changement nécessitant réévaluation et décision du responsable compétent.
- Dossier technique de transparence : contribution du traitement, origine des
  données, paramètres et opérations, limites de documentation ; contenu légal
  obligatoire vérifié avant toute publication ou réponse.
- Fiche projet → `references/templates/fiche-projet-si.md` ; exigences →
  `references/templates/cahier-des-charges-technique.md` ; charte technique
  → `references/templates/charte-usage-si.md`, avec
  `references/ecrits-numerique.md`.

Marquer `[INCOMPLET]` finalité, catégorie, documentation ou preuve manquante.
N'insérer ni données nominatives, ni secret, ni exemples de surveillance.

## 11. Double échelle [risque / confiance]

| Situation | Repère |
|---|---|
| Essai borné sur données fictives, sans effet externe | [faible / stable] sur les conditions de l'essai |
| Assistance avec validation humaine démontrée | [moyen / à vérifier] sur qualité et conditions du fournisseur |
| Influence sur une décision individuelle ou service essentiel | [élevé / à vérifier] ; qualification et preuves avant déploiement |
| Finalité, régime ou calendrier non confirmés | [élevé / abstention] sur la qualification juridique |
| Surveillance ou divulgation suspecte | [critique / à vérifier] ; garde-fou correspondant en premier |

Adapter à `SKILL.md` ; une sortie convaincante ne constitue ni preuve de
fiabilité ni source de droit.

## 12. Checklist de branche

- Incident et surveillance recherchés ; garde-fou en premier si déclenché ?
- Bascules `dpo-ct`, `drh-fpt`, `dpm-fpt` et hors périmètre tenus ?
- Mode d'exercice, finalité, effet réel et responsable du déploiement établis ?
- Rôle et catégorie instruits sur les textes applicables à la date demandée ?
- Calendrier, actes modificatifs et seuils vérifiés ou réservés ?
- Données admises, fournisseur, hébergement et conditions d'arrêt documentés ?
- Contrôle humain et reprise démontrés, erreurs recensées sur cas fictifs ?
- Transparence sur décision et publication générale distinguées ?
- Obligation, doctrine et collectivité distinctes ; aucun contenu d'État importé ?
- Provenance datée visible, aucune auto-attestation de lecture de session ?
- Livrable complet ou `[INCOMPLET]`, sans secret ni donnée nominative ?
- Chemins des fichiers mobilisés cités à l'endroit utile ?
