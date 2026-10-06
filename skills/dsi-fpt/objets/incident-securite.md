# Objet métier — Incident de sécurité (v0.2.0)

> **Situation type** : organiser la gestion d'un incident de sécurité, de sa découverte à sa clôture.
> **[Risque / Confiance]** : [Critique pendant l'incident / À vérifier]

**Préalable impératif** : lire `../references/analyse-situation.md` et afficher
intégralement le garde-fou incident du SKILL §5.2 comme premier livrable, avant
le contenu métier. Afficher aussi le garde-fou surveillance §5.3 si déclenché.
Ne jamais conclure à l'absence de données touchées faute d'éléments.

## 1. Acteurs et autorités compétentes

| Rôle | Acteur et contrôle attendu |
|---|---|
| Décide | Exécutif pour les décisions qui lui reviennent ; cellule de crise selon les pouvoirs vérifiés |
| Exécute | DSI interne, service mutualisé ou prestataire de réponse à incident ; préciser convention ou contrat et pilote de la collectivité |
| Exige et contrôle | RSSI pour les éléments techniques ; DPO pour le volet données personnelles, avec `BASCULE dpo-ct` dès qu'elles peuvent être concernées |
| Appuie | CSIRT territorial ou intervenant qualifié selon le circuit prévu ; ne pas lui attribuer les décisions de l'exécutif |
| Paie | Circuit financier compétent ; `BASCULE dirfi-fpt` pour le fond financier |

Organisation et limites → `../references/crise-cyber-continuite.md`.

## 2. Textes applicables

- Identifier les circuits de signalement et le régime d'assurance → `../references/crise-cyber-continuite.md` : obligations et conditions seulement après vérification du cas.
- Examiner les règles de sécurité et l'éventuel régime sectoriel, dont la transposition de NIS2 → `../references/securite-si.md` : aucune applicabilité générale présumée aux collectivités.
- Protection des données personnelles : `BASCULE dpo-ct` ; arrêter qualification, notification et information des personnes.
- Sources et délais → `../references/socle-sources-verification.md` et `../references/references-verifiees.md`.

## 3. Procédures

1. Après affichage du STOP, orienter la préservation des preuves et l'appui spécialisé → `../references/crise-cyber-continuite.md`.
2. Établir les faits, inconnues, responsabilités et décisions attendues → `../references/crise-cyber-continuite.md`.
3. Faire instruire le périmètre touché et la sécurité de reprise → `../references/securite-si.md` ; basculer vers `dpo-ct` si nécessaire.
4. Documenter les circuits de signalement, leur source et les décisions prises → `../references/crise-cyber-continuite.md` ; aucun délai de mémoire.
5. Soumettre les critères de reprise et les réserves au décideur identifié → `../references/crise-cyber-continuite.md`.
6. Faire constater la clôture documentée et préparer le plan d'amélioration → `../references/retex.md` ; ne pas transformer une reprise technique en preuve d'absence de compromission.

## 4. Écrits associés

Rapport évolutif → `../references/templates/rapport-incident.md` : chronologie,
faits et hypothèses séparés, décisions attribuées par rôle, preuves référencées
sans les reproduire, incertitudes et conditions de clôture explicites.
Plan d'amélioration → `../references/retex.md`.

## 5. Jurisprudence clé

Ne pas déduire une responsabilité ou citer une décision de mémoire. Mobiliser
`recherche-juridique` si une question de droit conditionne la clôture ; vérifier
la décision intégrale selon `../references/socle-sources-verification.md`.
La plainte et la procédure pénale sont nommées, sans être déroulées.

## 6. Check-list opérationnelle

- [ ] STOP incident affiché avant tout contenu métier ; STOP surveillance si déclenché.
- [ ] Preuves préservées ; aucun acte irréversible proposé sans ce préalable.
- [ ] Aucune contre-mesure offensive ni accès à un système tiers.
- [ ] Mode d'exercice, cellule de crise et appui spécialisé identifiés.
- [ ] Décisions de l'exécutif distinguées des actions de la DSI.
- [ ] `BASCULE dpo-ct` effectuée dès que des données peuvent être concernées.
- [ ] Signalements et délais confirmés par sources, ou laissés à vérifier.
- [ ] Rapport anonymisé ; faits établis, hypothèses et inconnues séparés.
- [ ] Reprise et clôture étayées ; réserves et actions suivies.

## Références et remontées

Crise → `../references/crise-cyber-continuite.md` ; sécurité →
`../references/securite-si.md` ; RETEX → `../references/retex.md`.
Skills de frontière : `dpo-ct`, `drh-fpt`, `dpm-fpt`, `dirfi-fpt` selon le volet.
Remonter les changements de signalement, d'assurance et de régime sectoriel
au registre `../references/references-verifiees.md`, sans donnée d'incident.
