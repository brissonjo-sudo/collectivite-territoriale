# Candidat 1.4.0 — non mesuré, non qualifié

État local au 2026-10-21. La distribution reste épinglée sur la release 1.3.0.

## Réépinglage et décisions appliquées

Les décisions de Jo du 21/10 limitent le réépinglage à trois sources. Les
arbitrages B2b autorisent les nouveaux ancrages, les sept ajouts aux inventaires
DRH/RJ et le rappel CIA conditionnel commun aux cinq surcharges DirFi, DRH,
recherche-juridique, DPM et DSI. L'arbitrage B2c autorise une seule ligne blanche
supplémentaire après le paragraphe de citation RJ, sans changement de son texte.

| Source | Version | Commit épinglé |
|---|---|---|
| Drh-fpt | 0.7.0 | `002f74b07b5b31557a75ecfeda838d4126a1b1fd` |
| DirFi-fpt | 1.0.5 | `9c81531592cc83e6b41156f21494f3bc2d64a9db` |
| recherche-juridique | 3.6.0 | `f3ddffb520cb7a9ffe70860d0dd119d2bbca272d` |

DCP 0.1.4, DSI 0.2.1, DPO 0.2.2 et DPM 1.0.5 conservent leurs pins.
Le rappel CIA n'attribue à DirFi ni qualification du régime ni autorisation
de paiement : il reste conditionnel et les vérifications sont attribuées à DRH.
Les ressources locales se citent par nom de skill et section ; seules les
sources officielles prennent la forme d'un lien dans la réponse.

Les copies sont produites par `sync_skills` à partir des blobs Git exacts.
Les bases des surcharges sont recalculées dans leur ordre d'application,
puis revérifiées par `instruction_overlays` et `check_sync`. Aucun validateur,
seuil, manifeste de transition ni test N = 85 n'est modifié. Le test de version
RJ attend explicitement 3.6.0, conséquence du pin décidé par Jo.
La fixture de preuve absente conserve sa version historique 1.3.0, et la
simulation d'installation déclare la version du manifeste candidat ; leurs
assertions ne changent pas avec le réépinglage.

## État d'avancement

| Lot | État et limite |
|---|---|
| B1 | Qualificateur renforcé localement ; ADR 0024. |
| B2/B2b/B2c | Réépinglage, surcharges et candidat 1.4.0 préparés localement. |
| B3 | Contrat v3 préparé, un invariant ajouté au seul cas prime-départ ; v2 intact. Liaison au commit mesuré fermée en attente du gel B4 (ADR 0025). |
| B4 | Pré-vol complet, notamment Docker, à exécuter avant gel. |
| B5 | Campagne, avis humain, smoke réel, assemblage et publication non exécutés. |

Le lanceur vérifie v3 à blanc pour préparer 1.4.0. Aucune exécution réelle ni
qualification 1.4.0 n'est autorisée tant que le commit mesuré exact n'est pas
lié au verrou v3 au gel. L'ADR 0025 décrit cette étape, notamment l'impossibilité
pour un commit de contenir son propre SHA. Aucun commit provisoire ni choix de
contrat par un champ de preuve ne remplace cette liaison.

L'entrée RJ embarquée passe de 1 162 lignes / 57 588 caractères LF à
511 lignes / 31 230 caractères LF. Les 190 Markdown installables sont non
vides et non multiples de 85 ; le test existant conserve ses assertions.
Ces mesures documentaires et les tests locaux ne sont pas une qualification
comportementale, humaine ou juridique.

## Distribution et barrière de release

Les manifestes du candidat annoncent 1.4.0, avec « non mesuré, non qualifié ».
La description du catalogue distingue ce candidat de sa distribution effective.
Le champ de version publié et les deux références d'installation restent sur
1.3.0 : `docs/publication.md` impose une étiquette publiée et les tests vérifient
qu'elle existe. Aucune étiquette 1.4.0 n'est créée par ce lot.

La preuve `release-1.4.0.json` est absente. La barrière reste donc rouge jusqu'à
l'assemblage autorisé d'une nouvelle preuve ; celle de 1.3.0 n'est ni modifiée
ni transférée. Les vérifications locales sont archivées hors dépôt ; aucune
poussée ni exécution d'évaluation modèle n'accompagne cette préparation.
