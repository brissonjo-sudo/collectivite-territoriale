# Objet métier — Solution SaaS (v0.2.0)

> **Situation type** : choisir, exploiter ou quitter une solution en ligne utilisée par la collectivité.
> **[Risque / Confiance]** : [Élevé / À vérifier]

Lire `../references/analyse-situation.md` avant tout contenu technique.
Afficher les garde-fous incident et surveillance si déclenchés ; traiter les
frontières avant d'instruire les options.

## 1. Acteurs et autorités compétentes

| Rôle | Acteur et contrôle attendu |
|---|---|
| Décide | Autorité compétente selon délégations vérifiées ; arbitrage des risques par la collectivité |
| Porte le besoin | Service métier ; usages, interfaces et continuité attendue |
| Exécute | DSI interne, service mutualisé ou prestataire ; préciser qui administre, qui contrôle et ce que prévoit le contrat |
| Exige et contrôle | RSSI pour la sécurité ; DPO via `BASCULE dpo-ct` pour le fond des données personnelles |
| Paie | Circuit financier compétent ; `BASCULE dirfi-fpt` pour budget et financement |

La responsabilité de la collectivité se traite dans
`../references/gouvernance-strategie.md`, quel que soit le mode d'exercice.

## 2. Textes applicables

- Cloud, qualifications et éventuels régimes particuliers d'hébergement → `../references/cloud-hebergement.md` : qualification d'une offre à confirmer, doctrine de l'État sans applicabilité automatique.
- RGS et règles de sécurité selon le système → `../references/securite-si.md` : instruire le champ.
- Exécution contractuelle et éventuel CCAG-TIC → `../references/contrats-prestataires.md` : vérifier les documents applicables ; passation hors périmètre.
- Sous-traitance et transferts de données personnelles : `BASCULE dpo-ct` ; arrêter le volet.
- Vérification → `../references/socle-sources-verification.md` et `../references/references-verifiees.md`.

## 3. Procédures

1. Qualifier le besoin, le mode d'exercice et la phase : choix, exploitation ou sortie → `../references/gouvernance-strategie.md`.
2. Instruire l'hébergement et le périmètre exact de l'offre → `../references/cloud-hebergement.md`.
3. Faire instruire les risques et exigences de sécurité → `../references/securite-si.md` ; faire les bascules de frontière.
4. Vérifier engagements, accès conservés et réversibilité → `../references/contrats-prestataires.md`.
5. Préparer les preuves de restitution et la continuité de transition → `../references/contrats-prestataires.md` et `../references/applications-interoperabilite.md`.
6. Documenter la décision et les réserves → `../references/gouvernance-strategie.md` ; aucun préavis ni délai de mémoire.

## 4. Écrits associés

- Arbitrage → `../references/templates/fiche-projet-si.md` : phase, alternatives, dépendances et inconnues.
- Exigences d'hébergement, exploitation et sortie → `../references/templates/cahier-des-charges-technique.md` : preuves de réalisation et responsabilités.
- Si le champ de sécurité le justifie → `../references/templates/note-homologation.md` ; la qualification d'une offre ne vaut pas homologation du système.

## 5. Jurisprudence clé

Mobiliser `recherche-juridique` si un différend contractuel ou une question de
droit conditionne la sortie. Ne pas citer de décision de mémoire ; appliquer
`../references/socle-sources-verification.md` avant toute conclusion.

## 6. Check-list opérationnelle

- [ ] Garde-fous examinés avant le contenu technique.
- [ ] Phase et mode d'exercice établis ; pilote de la collectivité identifié.
- [ ] Offre, périmètre et preuves de qualification confirmés à la date de décision.
- [ ] Doctrine de l'État distinguée des obligations applicables à la collectivité.
- [ ] `BASCULE dpo-ct` faite pour le fond des données personnelles.
- [ ] Contrat applicable lu ; passation signalée hors périmètre.
- [ ] Accès, restitution, réversibilité et continuité instruits par les branches.
- [ ] `BASCULE dirfi-fpt` faite sur budget et financement.
- [ ] Écrits sans secret ni architecture réelle exploitable ; inconnues explicites.

## Références et remontées

Cloud → `../references/cloud-hebergement.md` ; contrats →
`../references/contrats-prestataires.md` ; sécurité →
`../references/securite-si.md` ; applications →
`../references/applications-interoperabilite.md`.
Skills de frontière : `dpo-ct`, `dirfi-fpt`, `drh-fpt`, `dpm-fpt` selon le volet.
Remonter les évolutions des qualifications et régimes d'hébergement au registre
`../references/references-verifiees.md` ; ne pas stocker de contrats réels ici.
