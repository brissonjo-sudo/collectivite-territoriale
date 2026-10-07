# Objet métier — Site et réseau (v0.2.0)

> **Situation type** : équiper ou sécuriser un site de la collectivité, dont une mairie annexe ou une école.
> **[Risque / Confiance]** : [Moyen, à relever selon le service / À vérifier]

Avant tout contenu technique, lire `../references/analyse-situation.md`.
Afficher les garde-fous incident et surveillance si déclenchés ; ne pas
recueillir de plan d'adressage ou de détail d'architecture exploitable.

## 1. Acteurs et autorités compétentes

| Rôle | Acteur et contrôle attendu |
|---|---|
| Décide | Autorité compétente selon les délégations vérifiées ; arbitrages de continuité avec la DGS |
| Porte le besoin | Responsable du site et services utilisateurs ; usages et disponibilité attendue |
| Exécute | DSI interne, service mutualisé selon convention, ou prestataire selon contrat ; préciser les responsabilités d'exploitation |
| Exige et contrôle | RSSI pour la sécurité ; DPO via `BASCULE dpo-ct` pour le fond des données personnelles |
| Paie | Circuit financier compétent ; `BASCULE dirfi-fpt` pour budget et financement |

Organisation → `../references/gouvernance-strategie.md` ; équipements de
vidéoprotection : `BASCULE dpm-fpt` sur l'autorisation et la doctrine.

## 2. Textes applicables

- Cadre des équipements, réemploi et fin de vie → `../references/infrastructures-reseaux.md` : vérifier les obligations visant la collectivité et la catégorie d'équipement.
- RGS et sécurité des systèmes → `../references/securite-si.md` : vérifier le champ avant de présenter une obligation.
- Engagements des prestataires → `../references/contrats-prestataires.md` : lire les documents applicables ; passation hors périmètre.
- Vérification et provenance → `../references/socle-sources-verification.md` et `../references/references-verifiees.md`.

## 3. Procédures

1. Qualifier les services du site, leur criticité et le mode d'exercice → `../references/gouvernance-strategie.md`.
2. Cadrer équipements et dépendances sans publier l'architecture réelle → `../references/infrastructures-reseaux.md`.
3. Faire instruire sécurité et accès → `../references/securite-si.md` ; appliquer les bascules avant tout volet de surveillance.
4. Préparer les conditions de réception et d'exploitation → `../references/infrastructures-reseaux.md` et `../references/contrats-prestataires.md`.
5. Relier les besoins de continuité à la branche compétente → `../references/crise-cyber-continuite.md`.
6. Documenter arbitrage, réserves et fin de vie → `../references/gouvernance-strategie.md` et `../references/infrastructures-reseaux.md` ; vérifier les échéances citées.

## 4. Écrits associés

- Arbitrage du besoin → `../references/templates/fiche-projet-si.md` : fonctions du site, dépendances décrites par catégories et exploitation.
- Exigences et réception → `../references/templates/cahier-des-charges-technique.md` : aucune adresse interne ni schéma réel exploitable.
- Si incident découvert → `../references/templates/rapport-incident.md`, après le garde-fou.

## 5. Jurisprudence clé

Ne pas citer de décision de mémoire. Mobiliser `recherche-juridique` si la
compétence, la responsabilité ou l'exécution contractuelle est contestée ;
appliquer `../references/socle-sources-verification.md` avant de conclure.

## 6. Check-list opérationnelle

- [ ] Garde-fous incident et surveillance examinés avant technique.
- [ ] Mode d'exercice et responsabilités d'exploitation identifiés.
- [ ] Services du site et criticité cadrés, sans identifiants réels.
- [ ] Sécurité et continuité rattachées aux branches compétentes.
- [ ] `BASCULE dpo-ct` ou `BASCULE dpm-fpt` faite sur leur fond.
- [ ] Budget et financement : `BASCULE dirfi-fpt` ; passation hors périmètre.
- [ ] Exigences de réception et d'exploitation reliées à des preuves.
- [ ] Réemploi et fin de vie instruits ; aucune obligation de mémoire.
- [ ] Écrits anonymisés et sans architecture exploitable.

## Références et remontées

Infrastructures → `../references/infrastructures-reseaux.md` ; sécurité →
`../references/securite-si.md` ; continuité →
`../references/crise-cyber-continuite.md` ; contrats →
`../references/contrats-prestataires.md`.
Skills de frontière : `dpo-ct`, `dpm-fpt`, `dirfi-fpt`, `drh-fpt` selon le volet.
Remonter les évolutions de réemploi et de fin de vie au registre
`../references/references-verifiees.md` avant de modifier la branche.
