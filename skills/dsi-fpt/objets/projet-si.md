# Objet métier — Projet SI (v0.2.0)

> **Situation type** : lancer et conduire un projet applicatif dans une collectivité.
> **[Risque / Confiance]** : [Moyen, à relever selon l'enjeu / À vérifier]

Avant le cadrage technique, lire `../references/analyse-situation.md` : afficher
les garde-fous incident et surveillance dès leur déclenchement, puis traiter les
frontières. Cet objet agrège les branches ; il ne les remplace pas.

## 1. Acteurs et autorités compétentes

| Rôle | Acteur et contrôle attendu |
|---|---|
| Décide | Exécutif et autorités compétentes selon les délégations vérifiées ; arbitrages préparés avec la DGS |
| Porte le besoin | Service métier ; validation du besoin et des critères de réception |
| Exécute | DSI interne, service mutualisé selon la convention, ou prestataire selon le contrat ; nommer le pilote conservé par la collectivité |
| Exige et contrôle | RSSI pour la sécurité ; DPO pour les exigences de protection des données, avec `BASCULE dpo-ct` sur le fond |
| Paie | Circuit financier compétent ; `BASCULE dirfi-fpt` pour budget et financement |

Répartition des responsabilités → `../references/gouvernance-strategie.md`.

## 2. Textes applicables

- Identifier les échanges et traitements du projet → `../references/applications-interoperabilite.md` : RGI et règles des échanges administratifs, selon le système concerné ; ne pas généraliser une obligation de l'État.
- Examiner le champ du RGS pour le système de la collectivité → `../references/securite-si.md`.
- Vérifier les règles d'exécution du contrat et les documents effectivement applicables → `../references/contrats-prestataires.md` ; passation hors périmètre.
- Vérifier chaque conclusion de droit et son applicabilité avant usage → `../references/socle-sources-verification.md` et `../references/references-verifiees.md`.

## 3. Procédures

1. Qualifier le besoin, le mode d'exercice et les décisions à obtenir → `../references/gouvernance-strategie.md`.
2. Cadrer le périmètre, les interfaces et la continuité du service → `../references/applications-interoperabilite.md`.
3. Faire instruire les risques et les exigences de sécurité → `../references/securite-si.md` ; suspendre le volet de fond relevant de `dpo-ct`.
4. Définir les engagements et preuves de réception → `../references/contrats-prestataires.md`.
5. Préparer l'arbitrage et le passage en exploitation avec les réserves explicites → `../references/gouvernance-strategie.md`.
6. Organiser le retour d'expérience → `../references/retex.md` ; vérifier à la source les délais invoqués.

## 4. Écrits associés

- Cadrage et arbitrage → `../references/templates/fiche-projet-si.md` : distinguer besoin, options, décision attendue et hypothèses.
- Exigences et réception → `../references/templates/cahier-des-charges-technique.md` : relier chaque exigence à une preuve.
- Si l'analyse du champ le requiert → `../references/templates/note-homologation.md` ; aucune décision favorable présumée.

## 5. Jurisprudence clé

Ne pas ajouter de décision de mémoire. Si une contestation de compétence ou
d'exécution contractuelle conditionne l'arbitrage, mobiliser
`recherche-juridique` avec les faits anonymisés ; appliquer
`../references/socle-sources-verification.md` avant toute citation.

## 6. Check-list opérationnelle

- [ ] Garde-fous incident et surveillance examinés avant contenu technique.
- [ ] Mode internalisé, mutualisé ou externalisé et pilote désignés.
- [ ] Besoin, périmètre, exclusions et décision attendue confirmés.
- [ ] Branches compétentes lues et citées là où elles sont mobilisées.
- [ ] Bascules `dpo-ct`, `drh-fpt`, `dpm-fpt`, `dirfi-fpt` faites si nécessaires ; passation signalée hors périmètre.
- [ ] Applicabilité du RGS instruite ; aucune homologation réputée acquise.
- [ ] Exigences de réception, exploitation et sortie reliées à des preuves.
- [ ] Informations manquantes signalées ; aucun secret ni détail exploitable.

## Références et remontées

Gouvernance → `../references/gouvernance-strategie.md` ; applications →
`../references/applications-interoperabilite.md` ; sécurité →
`../references/securite-si.md` ; contrats →
`../references/contrats-prestataires.md` ; RETEX → `../references/retex.md`.
Skills de frontière : `dpo-ct`, `drh-fpt`, `dpm-fpt`, `dirfi-fpt`.
Remonter toute évolution des échanges obligatoires ou des référentiels au
registre `../references/references-verifiees.md` avant de modifier la branche.
