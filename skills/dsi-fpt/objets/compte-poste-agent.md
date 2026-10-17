# Objet métier — Compte et poste d'agent (v0.2.0)

> **Situation type** : préparer l'arrivée, la mobilité ou le départ d'un agent pour ses comptes, accès et équipements.
> **[Risque / Confiance]** : [Élevé / À vérifier]

Lire `../references/analyse-situation.md` avant toute aide technique. Toute
demande d'accès aux contenus ou traces d'une personne déclenche le garde-fou
surveillance du SKILL §5.3, affiché intégralement avant le contenu technique.
Un incident en cours ou récent déclenche d'abord le garde-fou incident §5.2.

## 1. Acteurs et autorités compétentes

| Rôle | Acteur et contrôle attendu |
|---|---|
| Décide | Autorité compétente selon les délégations vérifiées ; habilitations validées par le responsable compétent |
| Porte l'événement | Circuit RH et encadrement ; `BASCULE drh-fpt` sur le fond statutaire et disciplinaire |
| Exécute | DSI interne, service mutualisé ou prestataire selon convention ou contrat ; préciser le circuit de demandes autorisées |
| Exige et contrôle | RSSI pour les habilitations ; DPO via `BASCULE dpo-ct` pour le fond des données et les conditions d'accès aux personnes |
| Paie | Circuit financier compétent ; `BASCULE dirfi-fpt` sur budget et financement |

Responsabilités → `../references/gouvernance-strategie.md`.

## 2. Textes applicables

- Sécurité et gestion des habilitations → `../references/securite-si.md` : instruire le champ du RGS et des règles applicables au système.
- Équipement et fin de vie → `../references/infrastructures-reseaux.md` : vérifier les obligations visant la collectivité.
- Accès aux contenus, contrôle des personnes, adoption et opposabilité d'une charte : `BASCULE dpo-ct` et `BASCULE drh-fpt` selon le volet ; arrêter le fond concerné.
- Vérification → `../references/socle-sources-verification.md` et `../references/references-verifiees.md` ; ne pas citer de durée de conservation de mémoire.

## 3. Procédures

1. Après les garde-fous et frontières, qualifier arrivée, mobilité ou départ et mode d'exercice → `../references/gouvernance-strategie.md`.
2. Confirmer la demande autorisée et les rôles à habiliter, sans donnée nominative → `../references/securite-si.md`.
3. Rattacher la gestion des accès à la branche sécurité → `../references/securite-si.md` ; ne donner aucun mode opératoire de surveillance avant base et conditions établies.
4. Rattacher remise, retour et gestion des équipements à la branche infrastructures → `../references/infrastructures-reseaux.md`.
5. Faire documenter les validations et le contrôle de réalisation → `../references/securite-si.md`.
6. Préparer les règles techniques d'usage → `../references/ecrits-numerique.md` ; fond RH et données arrêtés après bascule.

## 4. Écrits associés

Charte technique → `../references/templates/charte-usage-si.md` : règles d'usage
et sécurité, sans clause d'adoption ou de sanction. La traçabilité des
habilitations reste décrite dans `../references/securite-si.md`, sans publier
de compte réel. Si incident découvert →
`../references/templates/rapport-incident.md`, après le STOP.

## 5. Jurisprudence clé

Ne jamais reconstituer une décision sur la messagerie ou les fichiers d'un
agent. Le fond relève de `dpo-ct` et `drh-fpt`. Mobiliser
`recherche-juridique` pour vérifier une décision lorsque le skill compétent le
requiert ; méthode → `../references/socle-sources-verification.md`.

## 6. Check-list opérationnelle

- [ ] STOP surveillance affiché avant contenu technique si accès aux contenus, traces ou surveillance.
- [ ] STOP incident affiché en premier si incident en cours ou récent.
- [ ] Aucune commande, extraction ni paramétrage avant base et conditions établies.
- [ ] `BASCULE dpo-ct` et `BASCULE drh-fpt` faites sur leurs volets ; aucune illustration de la frontière.
- [ ] Événement, mode d'exercice et demande autorisée confirmés.
- [ ] Gestion des droits et équipements rattachée aux branches, sans duplication.
- [ ] Validation et contrôle décrits par rôle, sans identifiant de personne.
- [ ] Charte technique distincte de son adoption et de son opposabilité.
- [ ] Aucune donnée nominative, aucun secret ni durée de mémoire.

## Références et remontées

Sécurité → `../references/securite-si.md` ; infrastructures →
`../references/infrastructures-reseaux.md` ; écrits →
`../references/ecrits-numerique.md`.
Skills de frontière : `dpo-ct`, `drh-fpt`, `dirfi-fpt` ; `dpm-fpt` si le volet
l'exige. Remonter une évolution juridique au registre
`../references/references-verifiees.md` via le skill compétent ; ne jamais
consigner de cas individuel dans cette fiche.
