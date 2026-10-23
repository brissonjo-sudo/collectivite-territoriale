# Collectivité 1.4.0 — qualifiée, non publiée

État au **23 octobre 2026**. La qualification 1.4.0 repose sur le cycle propre
à cette version ; la publication et les deux catalogues restent sur **1.3.0**
jusqu’à la [procédure prévue](publication.md).

## Qualification constatée

- Campagne `campagne-l140-d` : **18/18 cas**.
- Avis humain de Jo du **22 octobre 2026** : réserve maintenue au cas
  `plugin-dcp-frontiere-dsi-externe`.
- Smoke réel `smoke-l140-a` : **2/2 cas**.
- Preuve : [tests/evidence/release-1.4.0.json](../tests/evidence/release-1.4.0.json),
  assemblée sur H2 puis commise en H3 `f2382f3a0be40bd7337240adaf2ffeac264717b7`.
- Copies figées, qualificateur, barrière de release et 414 tests réussis en
  cp1252 puis UTF-8, sans saut, sur H3. Les résultats ne constituent pas un déploiement.

La réserve DCP porte sur le lien local absolu vers le skill DCP. Elle reste
maintenue selon l’[ADR 0029](adr/0029-retrait-surcharge-dcp-et-reserve-0-1-5.md) ;
la correction est prévue dans **DCP-fpt 0.1.5**. Elle n’est pas présentée comme levée.

## Entrée recherche-juridique installée

L’entrée `skills/recherche-juridique/SKILL.md`, **surcharges comprises**, compte
**527 lignes / 32 129 caractères LF**. Recompte du 23 octobre : décodage UTF-8 et
normalisation LF, caractère LF final inclus ; les octets de l’installation du
smoke sont identiques à ceux de l’entrée du candidat. Cette mesure de taille
est distincte des preuves comportementales ci-dessus.

## Conservation de l’état préparatoire

L’état du 21 octobre ci-dessous est conservé comme historique : ses statuts
« non mesuré, non qualifié », ses décisions et ses tailles décrivent cette étape,
pas la qualification constatée le 23 octobre. Les transitions v3/v4 et leurs
décisions restent dans leurs ADR ; aucune décision passée n’est réécrite.

<details>
<summary>État préparatoire historique du 21 octobre 2026</summary>

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
| B5 (transition) | Branche fermée 1.4.0 préparée avant gel, décision Jo du 21/10 ; manifeste non fermé jusqu'à H2 et procédure exacte dans l'ADR 0026. Pré-vol non probant rejoué. |
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

</details>
