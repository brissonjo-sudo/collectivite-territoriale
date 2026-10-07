# Objet métier — Téléservice (v0.2.0)

> **Situation type** : préparer l'ouverture ou l'évolution d'un téléservice destiné aux usagers.
> **[Risque / Confiance]** : [Élevé / À vérifier]

Avant toute aide technique, lire `../references/analyse-situation.md` : afficher
les garde-fous incident et surveillance s'ils sont déclenchés, puis effectuer
les bascules de frontière.

## 1. Acteurs et autorités compétentes

| Rôle | Acteur et contrôle attendu |
|---|---|
| Décide | Autorité administrative compétente ; vérifier les délégations et la décision d'ouverture |
| Porte le service | Service métier ; périmètre de la démarche et modalités de traitement |
| Exécute | DSI interne, service mutualisé selon convention ou prestataire selon contrat ; pilotage conservé par la collectivité |
| Exige et contrôle | RSSI pour la sécurité ; responsable d'accessibilité selon l'organisation ; DPO via `BASCULE dpo-ct` pour le fond des données personnelles |
| Paie | Circuit financier compétent ; `BASCULE dirfi-fpt` pour budget et financement |

Compétences et organisation → `../references/gouvernance-strategie.md`.

## 2. Textes applicables

- CRPA, saisine électronique et services de confiance → `../references/dematerialisation-teleservices.md` : vérifier le régime de la démarche et les exceptions avant de conclure.
- RGS, attestation formelle et démarche d'homologation → `../references/securite-si.md` : collectivités visées, champ du système à instruire.
- Textes d'accessibilité des services publics en ligne et RGAA → `../references/accessibilite-numerique.md` : vérifier le champ et les exigences du service.
- Provenance et applicabilité → `../references/socle-sources-verification.md` et `../references/references-verifiees.md` ; aucune version ou échéance de mémoire.

## 3. Procédures

1. Qualifier la démarche, les usagers et le mode d'exercice → `../references/dematerialisation-teleservices.md`.
2. Cadrer les échanges et la réception des demandes → `../references/dematerialisation-teleservices.md` ; archivage hors périmètre.
3. Faire instruire les exigences de sécurité et le champ du RGS → `../references/securite-si.md` ; données personnelles : `BASCULE dpo-ct`.
4. Faire vérifier le parcours et les livrables d'accessibilité → `../references/accessibilite-numerique.md`.
5. Préparer la décision d'ouverture avec les preuves, réserves et conditions de maintien → `../references/dematerialisation-teleservices.md` et `../references/securite-si.md`.
6. Organiser exploitation et réexamen → `../references/gouvernance-strategie.md` ; vérifier les délais et la version des référentiels avant de les écrire.

## 4. Écrits associés

- Périmètre et décision attendue → `../references/templates/fiche-projet-si.md`.
- Exigences techniques et réception → `../references/templates/cahier-des-charges-technique.md`.
- Dossier de sécurité et décision à instruire → `../references/templates/note-homologation.md` : distinguer note préparatoire, homologation et attestation formelle.
- Écrits d'accessibilité → `../references/accessibilite-numerique.md` ; aucune conformité préremplie.

## 5. Jurisprudence clé

Si la validité d'une saisine ou d'un échange est contestée, mobiliser
`recherche-juridique`. Ne citer aucune décision de mémoire ; appliquer
`../references/socle-sources-verification.md` et arrêter le volet non vérifié.

## 6. Check-list opérationnelle

- [ ] Garde-fous examinés avant toute aide technique.
- [ ] Mode d'exercice, service métier et autorité compétente identifiés.
- [ ] Champ de la démarche et régime de saisine vérifiés.
- [ ] `BASCULE dpo-ct` effectuée sur le fond des données personnelles.
- [ ] Accessibilité instruite ; état réel et réserves documentés.
- [ ] Champ du RGS, analyse de risques et décision de sécurité instruits.
- [ ] Aucune attestation formelle ni homologation réputée acquise.
- [ ] Exploitation, continuité et réexamen rattachés aux branches compétentes.
- [ ] Écrit sans secret, donnée nominative ni architecture exploitable.

## Références et remontées

Dématérialisation → `../references/dematerialisation-teleservices.md` ;
accessibilité → `../references/accessibilite-numerique.md` ; sécurité →
`../references/securite-si.md`. Skills de frontière : `dpo-ct`, `dirfi-fpt` ;
`drh-fpt` ou `dpm-fpt` si le volet l'exige.
Remonter les évolutions du CRPA, des services de confiance et des référentiels
au registre `../references/references-verifiees.md` avant leur usage.
