# Branche — Retours d'expérience

## 1. Périmètre / Exclusions

Conduire un retour d'expérience après incident, panne, exercice ou projet
pour comprendre les écarts et décider des améliorations. Relier la
chronologie et les constats à un plan d'action vérifiable, puis capitaliser
sans donnée identifiante dans `JOURNAL.md`.

Incident en cours ou récent → garde-fou `SKILL.md` §5.2 avant toute analyse,
puis `references/crise-cyber-continuite.md` et `objets/incident-securite.md`.
Qualification RGPD et notification → `dpo-ct` ; responsabilité statutaire et
disciplinaire → `drh-fpt` ; budgets → `dirfi-fpt`, selon les bascules de
`SKILL.md` §5.5–5.6, sans illustration. Passation, archivage électronique et
ouverture des données → hors périmètre. Le RETEX ne remplace ni l'expertise
de réponse à incident ni une procédure contentieuse.

## 2. Questions couvertes

- Comment organiser le RETEX après une panne majeure ?
- Comment distinguer cause démontrée, facteur contributif et hypothèse ?
- Pourquoi un projet n'a-t-il pas produit le résultat attendu ?
- Comment passer des constats à des actions suivies et testées ?
- Que capitaliser sans exposer des personnes ou un SI identifiable ?

## 3. Arbre de traitement

Passer par `references/analyse-situation.md`. Appliquer les garde-fous
`SKILL.md` §5.2–5.3 avant toute collecte ou instruction technique s'ils sont
déclenchés. Une activité encore non stabilisée revient à sa branche de gestion
avant d'être traitée comme un dossier clos.

`événement ou projet → état actuel, impact, mode d'exercice et faits disponibles
→ périmètre du RETEX et hypothèses → vérification des preuves, engagements et
obligations invoquées → constats, décisions et plan d'action`.

`leçon significative → dépersonnalisation et retrait des détails exploitables
→ généralisation utile → contrôle des limites de la conclusion → entrée
dans JOURNAL.md proposée et suivi de l'action`.

## 4. Variables à lever

- Mode internalisé, mutualisé ou externalisé ; collectivité, service mutualisé
  et prestataire impliqués, décrits par leur rôle.
- Catégorie et taille si un texte en dépend ; date de référence ; événement
  en cours, stabilisé ou clôturé et preuve de cet état.
- Services concernés, criticité, impact constaté, fonctionnement dégradé et
  critères de retour au service.
- Nature et sensibilité des données ; exigences reçues du DPO ; documents
  exploitables sans noms, secrets ni architecture identifiable.
- Contrat et engagements en place, résultats attendus du projet ou exercice,
  constats techniques, décisions prises et éléments manquants.
- Responsables du RETEX, des actions et de leur validation ; capacité réelle
  de réalisation et dépendances entre corrections.

## 5. Règles métier

### Établir les faits

Construire une chronologie à partir des éléments disponibles, en indiquant
pour chacun sa provenance et son degré de certitude. Distinguer détection,
début supposé, effets constatés, mesures prises et retour au service. Une
coïncidence temporelle n'établit pas une cause ; l'absence de journal ne prouve
pas l'absence d'événement. Ne pas lancer une extraction nominative :
`SKILL.md` §5.3 s'applique avant tout accès aux traces d'une personne.

Pour un incident récent, le garde-fou de `SKILL.md` §5.2 reste premier même
si le demandeur parle de RETEX. Préserver les preuves et renvoyer les
investigations à l'appui compétent ; ne pas conseiller une reproduction
offensive ni une modification du système touché pour démontrer une cause.

### Analyser sans chercher un coupable

Comparer fonctionnement attendu et observé. Séparer cause établie, facteur
contributif, difficulté de détection, obstacle à la reprise et information
manquante. Examiner les interfaces entre métiers, DSI, service mutualisé et
prestataire ; relever aussi ce qui a limité l'impact. Une action exécutée par
une personne n'est pas, à elle seule, une explication suffisante.

Pour un projet, comparer résultat métier attendu, résultat obtenu et
conditions initiales : périmètre, dépendances, recette, adoption, charge et
capacité d'exploitation. Confier les arbitrages à
`references/gouvernance-strategie.md`, le fond applicatif à
`references/applications-interoperabilite.md` et les écarts d'engagements à
`references/contrats-prestataires.md`. Ne pas réécrire leur méthode.

### Décider des actions

Pour chaque constat, choisir une correction, une mesure de réduction du
risque ou une vérification complémentaire. Définir résultat attendu,
responsable par rôle, dépendance, preuve de réussite et point de réexamen.
Prioriser selon effet sur la continuité et le risque ; une liste longue sans
responsables ni contrôle ne constitue pas un plan d'action.

Faire distinguer par le décideur identifié les actions engagées et les
risques résiduels acceptés. La DSI instruit et exécute son volet ; elle ne
décide pas seule d'un arrêt de service ou d'une communication publique.
Les exigences du DPO restent sur son périmètre. Tester l'efficacité d'une
correction avec la branche compétente : sécurité →
`references/securite-si.md`, reprise →
`references/crise-cyber-continuite.md`, infrastructures →
`references/infrastructures-reseaux.md`.

### Capitaliser

Présenter la méthode de RETEX comme une bonne pratique de pilotage, sans
affirmer d'obligation générale de format ou de périodicité. Vérifier tout
engagement de rapport ou de suivi tiré d'un contrat ou d'un texte avant de
le présenter comme opposable.

Pour `JOURNAL.md`, garder seulement situation générique, raisonnement,
décision, limite et leçon réutilisable. Retirer noms, lieux précis, détails
contractuels identifiants et architecture exploitable ; remplacer les
acteurs par des rôles. Si cette transformation laisse identifier la
collectivité ou révèle une faiblesse utilisable, ne pas journaliser le cas.
Une leçon observée dans une situation ne devient pas une règle universelle.

## 6. Procédures

Confirmer d'abord l'état du service avec la branche compétente et identifier
les réserves encore ouvertes. Annoncer le périmètre et les hypothèses du
RETEX ; demander les faits qui manquent sans demander de données nominatives.
Préparer une chronologie et soumettre ses écarts aux acteurs métiers et
techniques concernés, décrits par rôle.

Séparer les points confirmés des contradictions. Faire instruire les
questions sans preuve suffisante plutôt que les attribuer à un responsable.
Proposer les actions, obtenir l'arbitrage, puis faire vérifier leur efficacité
par un contrôle distinct de leur simple réalisation. Clore chaque action sur
un résultat démontré ou un risque résiduel explicitement soumis au décideur.
Proposer la capitalisation anonymisée dans `JOURNAL.md`. Les échéances de suivi
se décident selon le risque ; les délais contractuels ou légaux se vérifient.

## 7. Déclencheurs de vérification

Appliquer `references/socle-sources-verification.md` avant d'affirmer une
obligation de rapport, un destinataire obligatoire, un délai, une durée de
conservation, une responsabilité ou une conformité. Vérifier texte,
applicabilité à la collectivité et contrat concerné avant la conclusion.
La disponibilité d'un kit ANSSI établit un outil de doctrine, pas une
obligation. Les questions de notification basculent vers `dpo-ct`.

## 8. Pièges et confusions fréquentes

- Traiter un incident comme clos parce que le service est accessible.
- Confondre cause, symptôme, facteur contributif et responsabilité personnelle.
- Prendre une déclaration du prestataire pour une preuve indépendante.
- Déduire une conformité d'un exercice réussi ou d'un RETEX rédigé.
- Transformer une recommandation ANSSI ou une doctrine de l'État en obligation
  pour une collectivité.
- Fermer les actions à l'achat d'un outil plutôt qu'au contrôle du résultat.
- Utiliser le journal comme un rapport d'incident contenant personnes ou
  architecture ; l'anonymisation des noms seule ne suffit pas.
- Esquisser une sanction, notification, procédure de passation ou décision
  budgétaire après signalement de la frontière.

## 9. Données et valeurs à vérifier

Consulter `references/references-verifiees.md` pour les textes invoqués par
la branche de fond et les outils de doctrine identifiés. Vérifier l'état de
la transposition en cybersécurité si une obligation de RETEX ou de rapport
en est déduite ; ne pas transposer une obligation de l'État par analogie.

Relire les délais d'engagement contractuel, échéances imposées par une
autorité, exigences de conservation, version des guides utilisés et régime
de signalement réellement applicable. `references/cache-valeurs.md` sert de
carte de vérification, sans reprise de ses valeurs. Toute règle non
confirmée reste réservée ; aucune conclusion juridique n'en est tirée.

## 10. Écrits et livrables

Produire un RETEX avec périmètre, état du service, impact, chronologie,
faits confirmés, hypothèses ouvertes, facteurs contributifs, points efficaces
et décisions. Joindre un plan d'action : résultat attendu, rôle responsable,
dépendances, preuve de réussite, point de réexamen et statut. Ces éléments
sont une structure utile, pas un contenu légal obligatoire sans vérification.

Le rapport factuel d'incident utilise
`references/templates/rapport-incident.md` via
`references/ecrits-numerique.md`. Pour la capitalisation, proposer une entrée
de `JOURNAL.md` séparée et dépersonnalisée ; ne pas y recopier le rapport.
Si les causes ou la chronologie ne sont pas établies, produire `[INCOMPLET]`
et nommer les vérifications encore nécessaires.

## 11. Double échelle [risque / confiance]

Appliquer `SKILL.md` §5.1. Une leçon de projet sans effet engageant peut
relever de [faible / stable]. Une panne majeure et des dépendances mal
connues appellent [élevé / à vérifier]. Des preuves fragiles, un incident
récent ou une mise en cause de responsabilités peuvent rendre le risque
critique : ne pas trancher la cause ou la responsabilité sans éléments
suffisants. La stabilisation du service n'établit pas la cause ni la confiance.

## 12. Checklist de branche

- Garde-fous `SKILL.md` §5.2–5.3 appliqués avant toute analyse concernée ?
- État actuel du service confirmé ; réserves de clôture explicites ?
- Mode d'exercice, acteurs par rôle et dépendances identifiés ?
- Chronologie sourcée ; faits, hypothèses et facteurs contributifs séparés ?
- Obligations éventuelles vérifiées avec applicabilité avant conclusion ?
- Plan d'action associé à des résultats contrôlables et à un décideur ?
- Frontières `dpo-ct`, `drh-fpt`, `dirfi-fpt`, passation respectées sans
  illustration ?
- Aucun nom, secret ni détail d'architecture ; journal réellement non identifiant ?
- Livrable produit ou `[INCOMPLET]` ; chemins des branches mobilisées cités ?
