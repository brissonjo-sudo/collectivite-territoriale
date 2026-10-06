# Branche — Écrits de la DSI

## 1. Périmètre / Exclusions

Produire une note de décision, un rapport d'incident, un cahier des charges
technique, une charte d'usage, une note d'homologation ou une communication
interne de la DSI. Choisir le destinataire, la décision ou l'action attendue,
recueillir les informations et assembler un écrit traçable.

Délibérations et budgets → `dirfi-fpt` ; actes RH, adoption et opposabilité
d'une charte → `drh-fpt` ; contenus RGPD → `dpo-ct`. Appliquer les bascules de
`SKILL.md` §5.5–5.6 et arrêter le volet concerné, sans illustration.
Passation → hors périmètre, service de la commande publique. Communication
publique de crise → exécutif, à nommer sans la traiter. Le fond métier reste
dans sa branche ; cet écrit ne le remplace pas.

## 2. Questions couvertes

- Comment présenter au DGS un arbitrage entre plusieurs options ?
- Comment écrire avec des informations encore incomplètes ?
- Quel gabarit utiliser pour un projet, un incident ou une exigence technique ?
- Comment distinguer faits, hypothèses, recommandation et décision ?
- Comment diffuser un écrit utile sans données nominatives ni secrets ?

## 3. Arbre de traitement

Passer par `references/analyse-situation.md`. Si l'écrit concerne un incident
en cours ou récent, appliquer `SKILL.md` §5.2 avant le rapport. Si la demande
vise les contenus ou traces d'une personne, appliquer `SKILL.md` §5.3 avant
toute rédaction technique.

`écrit demandé → destinataire, objectif, mode d'exercice et faits disponibles
→ type d'écrit et branche de fond → sources, applicabilité et compétence
vérifiées → brouillon puis version relue`.

Information essentielle absente → poser la question utile, une à une selon
`SKILL.md` §6. Si elle reste inconnue, livrer un brouillon `[INCOMPLET]` avec
champs à compléter et réserves ; ne pas transformer une hypothèse en fait.

## 4. Variables à lever

- Type d'écrit, destinataire, lecteur secondaire, décision ou action attendue.
- Mode d'exercice : internalisé, mutualisé, externalisé ; rédacteur technique,
  validateur métier et acteur habilité à décider.
- Catégorie et taille de collectivité si le droit en dépend ; date de
  référence et situation actuelle ou passée.
- Service concerné, criticité, impact sur les usagers et fonctionnement dégradé.
- Nature et sensibilité des données ; exigences reçues du DPO ; niveau de
  diffusion compatible avec le contrat de `SKILL.md`.
- Prestataire et contrat en place, éléments probants, sources officielles
  réellement consultées, incertitudes et pièces indisponibles.

## 5. Règles métier

### Écrit destiné à décider

Ouvrir par la décision attendue et la recommandation, puis expliquer le
problème de service. Comparer des options réalisables, y compris maintien ou
report lorsque pertinents. Pour chaque option, donner résultat attendu,
dépendances, risques résiduels, besoins et condition de réussite. Ne pas
noyer le décideur dans la description des produits ; rattacher chaque détail
technique à son effet sur le service.

La DSI prépare les faits et les options. Elle ne signe pas à la place de
l'acteur compétent ni ne présente un arbitrage demandé comme déjà acquis.
Le fond d'une note d'arbitrage relève de
`references/gouvernance-strategie.md` ; l'expression financière reste à
`dirfi-fpt`.

### Preuve et provenance

Séparer visiblement faits constatés, déclarations de tiers, hypothèses,
propositions et décisions confirmées. Pour une incertitude, indiquer son
effet sur la recommandation et ce qui la lèverait. Réserver les références
juridiques à la partie effectivement vérifiée selon
`references/socle-sources-verification.md`, avec source, point d'entrée et
date de consultation. Nommer la branche mobilisée par son chemin à l'endroit
où sa règle est utilisée.

Ne pas appeler « contenu obligatoire » une bonne pratique de présentation.
Avant d'insérer un contenu imposé par un texte, vérifier ce texte, sa vigueur
et son applicabilité à la collectivité. Une réserve dans une annexe ne
corrige pas une affirmation engageante dans le corps du document.

### Écrits spécialisés

Pour un rapport d'incident, distinguer impact confirmé, chronologie factuelle,
mesures autorisées et questions ouvertes ; renvoyer la gestion à
`references/crise-cyber-continuite.md`, la sécurité à
`references/securite-si.md` et la notification à `dpo-ct`. Un rapport n'est
ni une preuve de conformité ni une clôture automatique de l'incident.

Pour un cahier des charges technique, exprimer le résultat attendu, les
interfaces, conditions d'exploitation, contrôles de réception et sortie.
Le contenu applicatif relève de
`references/applications-interoperabilite.md`, les exigences contractuelles
de `references/contrats-prestataires.md`. Ne pas traiter la passation.

Pour une charte, décrire les usages techniques autorisés, les consignes de
sécurité, les contacts fonctionnels et la gestion des accès ; renvoyer le
fond à `references/securite-si.md`. Adoption, opposabilité et suites RH
relèvent de `drh-fpt` ; surveillance et droit des données restent soumis aux
garde-fous et à `dpo-ct`.

Pour une note d'homologation, reprendre le périmètre, les risques, les mesures,
les éléments de contrôle et les risques résiduels instruits par
`references/securite-si.md`. Vérifier auparavant si le régime s'applique au
système. Le registre `references/references-verifiees.md` distingue
attestation formelle par l'autorité et démarche d'homologation décrite par le
RGS, à confirmer en version applicable. Ne jamais présenter l'ANSSI comme
l'autorité qui homologue le SI de la collectivité, ni le brouillon comme une
attestation déjà prononcée.

### Diffusion

Respecter `SKILL.md` §6 : aucun secret, aucune donnée nominative ni détail
d'architecture exploitable dans l'écrit produit. Utiliser des rôles et des
descriptions fonctionnelles ; ne pas déplacer un contenu interdit vers une
annexe. Pour un fait sensible indispensable au dossier réel, signaler le
besoin d'une pièce conservée dans le circuit autorisé sans la reproduire ici.
En communication interne, indiquer l'effet concret, l'action autorisée et le
contact fonctionnel ; ne pas prétendre que le service est rétabli sans preuve.

## 6. Procédures

Identifier le type d'écrit et lire la branche de fond puis le gabarit associé.
Annoncer les informations connues et demander une à une les données qui
changent le résultat, en commençant par destinataire et objectif s'ils manquent.
Assembler un brouillon ; garder les absences explicites plutôt que les
compléter par défaut.

Contrôler les faits avec le responsable métier, les aspects techniques avec la
DSI ou le prestataire autorisé et les exigences de sécurité avec le RSSI.
Vérifier source, applicabilité et compétence avant toute formulation
engageante ; demander une validation externe sur le seul point hors
périmètre, sans le rédiger. Livrer le document et les points ouverts avec le
statut adapté. Tout délai légal ou contractuel de rédaction, de décision ou
de diffusion doit être vérifié avant d'être annoncé.

## 7. Déclencheurs de vérification

Appliquer `references/socle-sources-verification.md` pour contenu obligatoire,
mention légale, signature compétente, opposabilité, attestation, qualification
ou délai. Relire les références propres à la branche mobilisée. Vérifier
d'abord que le régime vise cette collectivité et ce système ; distinguer
obligation, doctrine technique et choix de présentation.

## 8. Pièges et confusions fréquentes

- Remplir une date, un prestataire, un niveau de service ou une architecture
  par défaut pour donner l'apparence d'un document achevé.
- Présenter une hypothèse d'incident comme sa cause démontrée.
- Reproduire le fond d'une branche plutôt que le mobiliser par son chemin.
- Confondre demande d'arbitrage, décision et preuve de réalisation.
- Appeler un modèle « conforme » sans examiner ses mentions et son périmètre.
- Diffuser noms, journaux nominatifs, secrets ou architecture dans une annexe.
- Esquisser une partie RH, RGPD, budgétaire ou de passation après bascule.
- Commencer le rapport avant les garde-fous applicables de `SKILL.md`.

## 9. Données et valeurs à vérifier

Vérifier les sources de la branche de fond dans
`references/references-verifiees.md`, leurs limites et leur applicabilité.
Pour une note d'homologation, consulter le rattachement officiel au RGS et
son vocabulaire ; pour un engagement contractuel, le contrat effectivement
incorporé. Confirmer versions, dates d'application, mentions exigées,
signataire habilité, délais et niveaux de service avant de les écrire.

Le registre livré fournit des pistes à relire sur la source primaire ; le cache
de maintenance est exclu du paquet runtime et ne se charge pas. Aucune valeur
ne se recopie sans une source datée. Si la source manque, retirer la conclusion
engageante et marquer le point `⚠️ non vérifié`.

## 10. Écrits et livrables

Choisir le gabarit selon l'objectif :

- Projet → `references/templates/fiche-projet-si.md`.
- Incident → `references/templates/rapport-incident.md`.
- Besoin technique → `references/templates/cahier-des-charges-technique.md`.
- Usages du SI → `references/templates/charte-usage-si.md`.
- Sécurité à soumettre à décision → `references/templates/note-homologation.md`.

Pour une note de décision ou une communication interne, appliquer les règles
de cette branche sans inventer un gabarit supplémentaire. Les éléments
présentés comme obligatoires doivent être vérifiés ; les autres sont les
éléments utiles à la décision. Livrer le texte demandé, son statut et les
champs encore manquants, sans le qualifier d'acte validé.

## 11. Double échelle [risque / confiance]

Appliquer `SKILL.md` §5.1 à l'usage de l'écrit, pas à sa seule forme. Une
information interne courante peut relever de [faible / stable]. Un arbitrage
de continuité ou une note d'homologation appelle [élevé / à vérifier] si des
preuves manquent. Un rapport portant sur un incident actif ou une pièce
engageant fortement la collectivité peut être critique. Une rédaction
fluide n'augmente pas la confiance ; l'absence de vérification impose réserve
ou abstention sur le point concerné.

## 12. Checklist de branche

- Garde-fous de `SKILL.md` §5.2–5.3 affichés avant contenu si déclenchés ?
- Destinataire, objectif, décideur et mode d'exercice identifiés ?
- Branche de fond et gabarit lus puis cités par chemin ?
- Faits, déclarations, hypothèses et décisions distingués ?
- Données manquantes explicites ; brouillon `[INCOMPLET]` si nécessaire ?
- Source et applicabilité contrôlées avant toute affirmation engageante ?
- Frontières respectées sans illustration ni annexe de contournement ?
- Aucun secret, aucune donnée nominative ni architecture exploitable ?
- Écrit demandé effectivement livré avec son statut et ses points ouverts ?
