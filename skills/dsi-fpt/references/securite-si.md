# Branche — Sécurité du SI

## 1. Périmètre / Exclusions

Couvrir la politique de sécurité du SI (PSSI), l'analyse de risques, les
comptes et droits, l'authentification, les sauvegardes, les mises à jour et la
sécurité des postes. Préparer les choix de sécurité et le dossier permettant à
la collectivité de décider de l'homologation et d'attester la sécurité dans le
périmètre applicable.

Exclure le fond de conformité des données personnelles → `dpo-ct` ; les
questions statutaires ou disciplinaires → `drh-fpt`. Incident en cours ou
récent → appliquer **avant tout contenu** `SKILL.md` §5.2 puis
`references/crise-cyber-continuite.md` ; accès aux contenus ou traces d'une
personne → appliquer **avant tout contenu** `SKILL.md` §5.3. Ne pas développer
ces frontières. Aucun mode opératoire offensif.

## 2. Questions couvertes

- Par quoi commencer une PSSI avec peu de moyens internes ?
- Comment décider des priorités de protection et des exceptions ?
- Comment maîtriser les comptes, les droits et les accès des prestataires ?
- Comment démontrer qu'une sauvegarde permet une reprise ?
- Qui décide de la sécurité d'un système et sur quelle preuve ?

## 3. Arbre de traitement

`demande → garde-fous et frontières → mode d'exercice et service concerné →
scénarios de risque et maîtrise actuelle → mesure prioritaire ou décision
d'acceptation → vérification de l'applicabilité → dossier et responsable`.

| Situation | Variables décisives | Décision et contrôle | Livrable |
|---|---|---|---|
| Première PSSI | Services essentiels, responsable, équipements connus, capacité d'exploitation | Fixer un socle réalisable puis traiter les écarts selon leur effet sur le service | PSSI courte et plan d'actions attribué |
| Compte ou droit | Rôle métier, responsable habilitant, privilèges, dépendances | Accorder le minimum justifié ; supprimer les accès devenus inutiles après contrôle des dépendances | Matrice des droits et trace de validation |
| Sauvegarde | Données nécessaires, scénario de perte, accès d'administration, restauration démontrée | Préférer une copie protégée d'une compromission commune et une reprise testée à un volume de copies non éprouvées | Dossier de sauvegarde et résultat d'essai |
| Mise en service | Périmètre, risques résiduels, preuves, autorité compétente | Lever les écarts bloquants ; faire décider explicitement les risques restant ouverts | `references/templates/note-homologation.md` |

Si une information manque, proposer une mesure conservatoire réversible et
nommer la décision qui reste impossible. Ne pas déduire la sécurité d'une
certification commerciale ou d'une absence d'incident connu.

## 4. Variables à lever

- Mode internalisé, mutualisé ou externalisé ; responsabilité de la
  collectivité et répartition contractuelle ou conventionnelle des actions.
- Catégorie et taille de la collectivité si un texte invoqué en dépend ; date
  de référence de la décision.
- Service public soutenu, conséquences d'indisponibilité, données nécessaires
  et sensibilité qualifiée par les interlocuteurs compétents.
- Périmètre du système, dépendances applicatives et d'identité, maintenance,
  accès privilégiés et accès distants.
- Prestataires, contrat, preuves disponibles et capacité effective à vérifier
  leurs prestations.
- État actuel : inventaire utilisable, propriétaire métier, protections
  existantes, écarts connus et essais de restauration réalisés.

Demander uniquement des informations abstraites ou anonymisées. Aucun secret,
compte nominatif ni détail d'architecture réelle identifiable.

## 5. Règles métier

### Politique et risques

Faire partir la PSSI des services à maintenir et des scénarios redoutés :
indisponibilité, altération, divulgation, perte d'accès ou dépendance à un
acteur. Pour chaque scénario, relier une mesure, un responsable, une preuve
et le risque résiduel. Le RSSI instruit ; la DSI met en œuvre ; l'autorité
compétente décide de l'acceptation selon les délégations vérifiées.

Employer le guide d'hygiène ANSSI et EBIOS Risk Manager comme **doctrine,
non normative**, sans imposer une méthode à toute collectivité. Une mesure
non exploitable par l'équipe n'est pas une maîtrise durable : prévoir son
administration, le remplacement du responsable et la vérification.

### Comptes, droits et postes

Séparer les usages ordinaires et l'administration. Donner un propriétaire aux
comptes techniques ; borner les accès prestataires au besoin et au périmètre
autorisés. Faire valider les droits par le responsable du besoin, les revoir
aux changements de fonction et rendre leur retrait vérifiable. Pour une
arrivée, une mobilité ou un départ, utiliser
`objets/compte-poste-agent.md` ; ne pas traiter le fond RH.

Prioriser les protections des accès distants et privilégiés. Organiser la
mise à jour selon l'exposition, la criticité et la capacité de retour à un
état de service ; traiter l'équipement non maintenable comme un écart à
arbitrer. Laisser à `references/infrastructures-reseaux.md` les choix de parc
et de segmentation. La journalisation protège et rend les opérations
traçables ; son existence n'autorise jamais l'accès aux traces d'une personne.

### Sauvegardes et reprise

Définir ce qu'il faut récupérer : données, configurations, dépendances et
moyens d'accès. Distinguer synchronisation, disponibilité et sauvegarde.
Une suppression ou compromission propagée aux copies peut rendre leur nombre
sans effet. Contrôler la séparation des accès d'administration et la protection
des copies ; exiger une preuve de restauration sur un périmètre autorisé.
Les priorités métier et la séquence de reprise relèvent de
`references/crise-cyber-continuite.md`.

### Homologation et attestation

Pour un SI d'échanges électroniques entrant dans le champ du RGS, partir de
l'ordonnance sur les échanges électroniques et du décret relatif au RGS,
**à confirmer en version consolidée** ; le registre établit l'inclusion des
collectivités parmi les autorités administratives. Vérifier le système et
les fonctions concernés avant de conclure à une obligation.

Le décret prévoit une **attestation formelle** par l'autorité ; le référentiel
décrit une démarche d'**homologation de sécurité**. Ne pas confondre ces
niveaux, ni étendre cette obligation indistinctement à tout équipement.
La collectivité décide pour son système ; une qualification ANSSI concerne
des produits, prestations ou offres dans leur périmètre, pas l'homologation
de son SI. Fournir les risques, écarts, preuves et conditions de réexamen ;
vérifier la compétence et les délégations avant de nommer le signataire.

## 6. Procédures

Pour établir un premier socle, supposer un besoin de prévention et aucun
incident actif ; sinon revenir immédiatement au garde-fou.

1. Faire valider par les métiers les services essentiels et les conséquences
   d'une perte, sans recueillir de données identifiantes.
2. Rapprocher inventaire, droits, maintenance et sauvegardes ; identifier les
   écarts qui rendent une reprise impossible ou exposent l'administration.
3. Proposer des actions ordonnées par réduction du risque, dépendances et
   capacité d'exploitation ; attribuer chacune à un acteur.
4. Faire décider les exceptions : justification, compensation, responsable,
   condition de réexamen. Un silence n'est pas une acceptation.
5. Vérifier les mesures par une preuve adaptée : revue de droits, état de
   maintenance, restauration autorisée, contrôle des accès prestataires.
6. Mettre à jour le dossier et déclencher son réexamen après un changement
   important. Les délais légaux éventuels se vérifient à la source.

Pour l'homologation, délimiter le système, vérifier le champ du texte,
réunir l'analyse et les preuves, instruire les risques résiduels puis
soumettre le dossier à l'autorité compétente. Ne pas promettre une
homologation sur une simple checklist technique.

## 7. Déclencheurs de vérification

Appliquer `references/socle-sources-verification.md` dès qu'une réponse
conclut à une obligation, désigne un signataire, invoque le RGS, une
qualification, un calendrier ou une sanction. Vérifier la transposition
française et ses catégories avant toute conclusion fondée sur NIS2 ; un
projet législatif ne crée pas d'obligation.

Toute qualification revendiquée se vérifie sur la source ANSSI pour l'offre
exacte, à la date de la décision. Le périmètre d'un certificat ne se déduit
pas du nom du fournisseur.

## 8. Pièges et confusions fréquentes

- Présenter toutes les recommandations d'hygiène comme du droit positif.
- Dire que toutes les collectivités sont soumises à NIS2 sans texte applicable.
- Confondre audit favorable, qualification de produit et décision d'homologation.
- Confier au prestataire l'acceptation des risques de la collectivité.
- Retirer un compte technique sans identifier les services qui en dépendent.
- Assimiler sauvegarde réussie et restauration réussie.
- Justifier une extraction nominative par le seul objectif de sécurité :
  le garde-fou `SKILL.md` §5.3 reste préalable.
- Donner des instructions de remise en état à partir d'un signal d'incident
  sans afficher d'abord `SKILL.md` §5.2.

## 9. Données et valeurs à vérifier

Consulter `references/references-verifiees.md` pour le champ du RGS,
l'attestation et les catégories éventuellement soumises à un régime cyber.
Vérifier la version du RGS, du guide d'hygiène et d'EBIOS Risk Manager,
la validité et le périmètre des qualifications, les délais de réexamen
invoqués et les calendriers de transposition. Ne pas recopier les valeurs
de `references/cache-valeurs.md` ; retourner à la source officielle.

## 10. Écrits et livrables

- PSSI : périmètre, responsabilités, règles d'accès, protection, contrôle,
  exceptions et réexamen ; distinguer exigences textuelles et choix internes.
- Plan de traitement : risque, action, responsable, dépendances, preuve et
  décision sur l'écart restant.
- Dossier d'homologation : périmètre, analyse, preuves, risques résiduels,
  décision attendue → `references/templates/note-homologation.md`.
- Exigences de sécurité à mettre en œuvre par un prestataire →
  `references/templates/cahier-des-charges-technique.md`, puis
  `references/contrats-prestataires.md` pour leur exécution.
- Règles d'usage et d'alerte → `references/templates/charte-usage-si.md`.

Ne qualifier un élément d'« obligatoire » qu'après vérification de son
fondement et de son applicabilité. Les choix de contenu ci-dessus sont des
repères opérationnels, pas un inventaire légal présumé.

## 11. Double échelle [risque / confiance]

Appliquer `SKILL.md` §5.1. Organisation préventive sans texte invoqué :
**[moyen / stable]** si le périmètre est connu. Droits privilégiés,
sauvegardes d'un service essentiel ou mise en production : risque **élevé**,
confiance **à vérifier** sans preuves. Attestation engageante ou incident :
risque **critique** selon l'enjeu ; ne pas trancher si la compétence, la
source ou le constat reste douteux. La simplicité technique ne réduit pas
l'enjeu.

## 12. Checklist de branche

- [ ] Garde-fous `SKILL.md` §5.2 et §5.3 testés et affichés en premier si déclenchés.
- [ ] Frontières `dpo-ct` et `drh-fpt` tenues sans développement.
- [ ] Mode d'exercice, service et responsabilité de la collectivité explicités.
- [ ] Obligation distinguée de doctrine ; champ RGS et compétence vérifiés.
- [ ] Qualification contrôlée sur l'offre exacte ; aucune présomption NIS2.
- [ ] Action prioritaire, responsable, preuve et risque résiduel indiqués.
- [ ] Aucune donnée nominative, aucun secret, aucun mode offensif.
- [ ] Chemins des branches, objets et gabarits nommés là où ils sont mobilisés.
