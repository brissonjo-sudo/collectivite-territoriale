# Historique des versions

## 1.4.0 — Qualifiée — non publiée

Actualisation du 2026-10-23 : campagne `campagne-l140-d` 18/18, avis de Jo du
22/10 avec réserve DCP au cas `plugin-dcp-frontiere-dsi-externe`, smoke réel
`smoke-l140-a` 2/2 et preuve `tests/evidence/release-1.4.0.json` assemblée en H3.
La publication et les deux catalogues restent sur 1.3.0 jusqu’à la procédure
prévue. Réserve DCP maintenue (ADR 0029), correction prévue dans DCP-fpt 0.1.5.
L’entrée RJ installée, surcharges comprises, compte 527 lignes / 32 129 caractères LF.
Les entrées datées ci-dessous restent l’historique de leur étape préparatoire ;
leurs décisions, tailles et résultats ne sont pas réécrits.

Lot B12c du 2026-10-22 (ADR 0029), décision Jo « Retirer la surcharge DCP » :
retour aux octets DCP-014, retrait du seul invariant de chemin du cas DCP
externe ; invariant DSI et F2 conservés. Lien local du cas 9 maintenu en réserve,
correction à la source dans DCP-fpt 0.1.5 avec la relecture praticien.
Aucun test historique ni mécanisme de validation modifié.

Lot B12b du 2026-10-22 (ADR 0028) : contrat v4 à empreinte fermée, web Sénat
limité au cas retraite, citation par nom et section pour les sept rôles et
surcharge DCP autorisée à pin constant. Contrats et transitions v2/v3 conservés.
Contrôle de chemins additif et matrice de satisfiabilité ; préparation de d
sans modèle, publication ou modification des archives.

Lot B8 du 2026-10-21, décision de Jo (ADR 0027) : consigne explicite de lecture
d’une seule entrée à la fois, sans segments parallèles, dans behavior_prompt
uniquement. Validateur, smoke, cas et seuils inchangés. Tentative a consommée
archivée sur place ; nouvelle tentative complète b sur H1b, sans résultat repris.
Aucun modèle ni poussée dans ce lot ; preuve 1.3.0 conservée dans son contexte.

Lot B5 du 2026-10-21, décision de Jo (ADR 0026) : branche de transition 1.4.0
fermée sur le seul H1 explicitement lié, v3, la CLI 0.163 et ses compagnons.
Seuls le lecteur, le verrou de mesure et le manifeste peuvent changer en H2.
Les empreintes source/cible sont vérifiées, les sources relues dans les objets
Git H1 et le contenu limité aux seules données de liaison. Le manifeste reste
non fermé avant la campagne ; aucune transition historique n'est modifiée.
Le pré-vol est rejoué dans une copie non probante, sans modèle ni Docker.

Lot B3 du 2026-10-21 (ADR 0025) : contrat de cycle v3, avec un seul invariant
ajouté au cas `plugin-prime-depart-retraite` sur l'absence d'indemnité de départ,
la consultation de la réponse ministérielle du 22/05/2025 (question n° 01222,
senat.fr) et le CIA strictement conditionnel. V2 et la preuve 1.3.0 restent
intacts ; aucun autre cas, attendu STOP ou seuil ne change. L'empreinte v3 est
fermée. Sa liaison au commit mesuré reste à réaliser au gel B4 ; toute mesure
1.4.0 non liée est refusée. Le lanceur charge v3 en préparation à blanc,
sans appel modèle. Les contre-épreuves passent par l'API publique, y compris
la projection CI, et ne constituent aucune mesure réelle.

Lot B2c du 2026-10-21 : réépinglage de DRH 0.7.0 (`002f74b`), DirFi 1.0.5
(`9c81531`) et recherche-juridique 3.6.0 (`f3ddffb`). Les autres pins sont
inchangés. Les copies sont régénérées depuis les blobs Git et les surcharges
déclarées ; aucune édition manuelle des fichiers embarqués.

Arbitrages B2b/B2c : réancrage sur les nouveaux titres, ajout des seuls sept
chemins constatés aux inventaires DRH/RJ, rappel CIA strictement conditionnel
après bascule et activation DRH dans les cinq contrats concernés, et règle de
citation des ressources de skill par nom et section dans le contrat commun RJ.
Une seule ligne blanche supplémentaire, autorisée en B2c, porte l'entrée RJ
embarquée à 511 lignes et 31 230 caractères LF ; N = 85 reste inchangé.
Le seul attendu de version du test d'autonomie RJ passe de 3.5.0 à 3.6.0,
conformément au pin explicitement décidé par Jo le 21/10 ; aucun seuil changé.
Deux fixtures de version sont isolées ou alignées sur le candidat ; leurs
assertions et les contrôles d'installation restent inchangés.

Les manifestes portent le candidat 1.4.0 non mesuré, non qualifié. Les deux
catalogues continuent à distribuer l'étiquette publiée 1.3.0 : ni étiquette
1.4.0 ni preuve de release ne sont inventées. La liaison du contrat v3 au gel,
le pré-vol complet et les exécutions réelles restent les lots suivants.
Voir l'[état d'avancement](docs/preparation-1-4-0.md).

Lot B1 du 2026-10-21 (ADR 0024) : le qualificateur recalcule les empreintes
du fichier de cas, d'`upstream.json` et de l'inventaire d'outillage du smoke.
Seules les exceptions d'assemblage et les transitions fermées existantes de
`human_resolution.compatible()` sont conservées. Les deux verrous CLI et les
reçus de campagne, de relecture et de smoke sont revérifiés, y compris dans la
vue de projection CI. Le staging de l'assembleur copie l'outillage inventorié.

Les fixtures temporaires des tests sont explicitement synthétiques ; les
preuves sources, assertions, seuils, verrous et manifestes de transition ne
sont pas modifiés. La preuve `release-1.3.0.json` est conservée : elle est
refusée par la nouvelle règle sur cette branche, à cause de l'outillage modifié.
La barrière de release restera rouge jusqu'à l'assemblage 1.4.0. `main` ne
recevra la règle qu'avec la release 1.4.0. Aucune campagne, aucun smoke réel,
appel modèle, push ou publication ne fait partie de B1.

## 1.3.0 — Candidat d'intégration DSI — non mesuré, non qualifié

Préparation locale du 2026-10-17, selon l'ADR 0010.

Actualisation locale du 2026-10-20 (T43-L40, ADR 0023, décision de Jo
« Consigne + smoke ce soir ») : ajout au seul prompt de l'obligation de lire
chaque entrée SKILL.md sélectionnée jusqu'au premier segment court. Une
restitution perçue comme tronquée impose de poursuivre au segment M + 85,
sans relire ni interrompre la série ; la limite est ensuite signalée dans
la réponse. Toutes les règles précédentes, les validateurs, N, la sonde EOF,
STOP, MCP sans web, les seuils et les sept skills sont inchangés. Pré-vol et
nouveau smoke préparés ; aucun modèle, Docker ou push exécuté dans ce lot.

Actualisation locale du 2026-10-20 (T43-L39, ADR 0022, décision de Jo
« Préciser le validateur ») : au plus une sonde EOF vide et réussie par fichier,
après couverture complète contiguë dans la même session. Les sondes sont tracées
dans `eof_probes`, séparées du contenu et de sa couverture. Lectures vides ailleurs,
troncatures, doublons, secondes sondes et commandes hors contrat restent refusés.
Prompt, STOP, seuils, campagne d et sept skills inchangés. Replays diagnostiques
L29-b/L38-d et pré-vol locaux ; aucun nouveau smoke réel, Docker ou push exécuté.

Actualisation locale du 2026-10-20 (T43-L37, décision de Jo « Oui aux deux ») :
les deux tests qui lisent le binaire smoke Windows local épinglé sont sautés
uniquement hors Windows, avec motif explicite. Sous Windows ils demeurent
obligatoires, y compris si le binaire manque. Leurs assertions et les tests
portables sur fixtures sont inchangés. Pré-vol Linux/Python 3.11 préparé pour
Claude ; aucune validation Linux, session modèle ou poussée acquise dans ce lot.

Actualisation locale du 2026-10-20 (T43-L35, ADR 0021) : les contrôles
d'absence de release utilisent leurs fixtures isolées, sans retrait d'assertion.
L'assembleur conserve les originaux hors dépôt et produit une projection
publique déterministe, sa table d'empreintes et une re-dérivation locale liée.
La CI contrôle le graphe des projections et refuse homes, identifiants de
session non hachés et secrets. Aucun nouvel appel modèle ni push dans ce lot.

Actualisation locale du 2026-10-20 (T43-L33, ADR 0020) : le qualificateur
sélectionne le contrat v2 exact de d depuis le commit de l'index humain lié,
avec empreinte épinglée. Sans ce lien, le contrôle historique v1 demeure.
Transition fermée étendue au seul qualificateur ; aucun autre contrôle changé.
Qualification et assemblage restent à vérifier ; aucune action externe.

Actualisation locale du 2026-10-20 (T43-L30, ADR 0019) : toute entrée ou
référence du cache est lue uniquement par segments contigus de 85 lignes.
Un segment court termine le fichier, sans lecture au-delà ni relecture.
Les 183 Markdown sont non vides et non multiples de 85 ; test régressif
obligatoire pour tous les fichiers futurs. Validateurs et runtime inchangés,
transition fermée réépinglée ; smoke c préparé seulement, a et b consommées
et conservées séparément. Aucun modèle, installation, push ni release.

Actualisation locale du 2026-10-20 (T43-L29, ADR 0018) : seule la consigne de
lecture du prompt smoke change : lecture unique jusqu'à 319 lignes, sinon
segments contigus d'au plus 90 lignes dès le départ, aucune relecture.
Ces valeurs sont un choix prudent fondé sur les restitutions observées de la
CLI 0.163, pas un plafond technique établi. Transition d étendue au seul
runner smoke, par empreintes source/cible exactes. Validateurs, STOP, absence
de web et sept skills inchangés. Tentative L28 a consommée ; nouveau smoke
préparé séparément, sans installation, appel modèle, push ni release.

Actualisation locale du 2026-10-20 (T43-L27, ADR 0017) : CLI de la campagne d
verrouillée au commit mesuré, version 0.163 et trois compagnons exacts ;
les reçus 0.162 restent historiques et sont refusés pour d. Aucun smoke ni release.
Le lecteur humain et l'assembleur relisent le contrat de cycle v2 exact de d ;
les empreintes v1 des trois cas STOP ne sont pas équivalentes. Réserves au format
L14, réponses exactes dans la fiche et décision globale restent exigées.

Actualisation locale du 2026-10-20 (T43-L24, ADR 0016) : DCP 0.1.4 au pin
`414cd4ecf41ba8b296908b738224355069b1890f`, sans surcharge DCP. Référence
autonome 28/28 et relecture Jo liées aux octets ; aucune mesure plugin transférée.
RJ prévoit les segments bornés dès le départ pour une entrée longue, sans
interrompre toute la réponse si une restitution reste incomplète. Nouveau cycle
plugin préparé seulement ; contrat v2, smoke durci et barrière release conservés.

- Union de sept skills : DSI 0.2.1 au pin `704e5dd6a3d15994ed431b23585aabd72086ca75`
  (30 fichiers) ; DPO 0.2.2 au pin `58ea45c4d12812da10ace5f1486deea96b8534fa`.
- DCP 0.1.3 conservé sans modification ; routage juridique des marchés vers DCP,
  technique vers DSI, protection des données vers DPO et preuve vers recherche-juridique.
- Surcharges ordonnées et vérifiées : priorité STOP, activation réelle forcée ou
  spontanée, abstention sans source primaire et transferts persistants.
- Neuf cas historiques conservés ; huit cas DSI ajoutés pour des contrôles
  locaux de structure uniquement, sans jugement ni campagne.
- Manifestes locaux en 1.3.0 ; catalogues inchangés, toujours épinglés `v1.2.0`.
- Aucun ancien gel ou score transféré. Preuves et tests historiques inchangés ;
  absence de mesure 1.3.0 et hypothèse ancienne « DSI externe » à traiter en L6.

## Préparation de distribution open source — 2026-10-08

- DCP 0.1.3 et les six skills restent identiques au runtime mesuré.
- Distribution technique séparée du déploiement opérationnel en collectivité
  ou dans une structure tierce, à la demande de l'auteur ; ADR 0007.
- Relecture praticien différée, note et grilles conservées, réserves inchangées.
- Barrière de distribution recalculée sur les preuves et empreintes ; avis
  humains et qualification métier restent non acquis.
- Aucune nouvelle étiquette ni bascule de marketplace dans ce changement.

## Correctif candidat — 2026-10-07

- DCP 0.1.1 épinglé au commit `caef7fd` : seul son point d'entrée change,
  pour préciser les frontières financières et l'ordre BASCULE/intertitre.
- Preuves 0.1.0 et qualification initiale conservées comme historiques ;
  aucune reprise de leur score pour le correctif.
- DCP 0.1.1 mesuré autonomement : 27 réussites, une demi-réussite (cas-24),
  aucun échec. Vingt alertes de citations dans huit cas ; relecture ouverte.
- Essai Codex v2 conservé après deux cas : contenu brut complet mais
  restitution tronquée déclarée par le modèle, visibilité non attestée.
- Profil Codex v3 : segments contigus de 6000 octets maximum, ordre,
  couverture et contenu contrôlés ; trous, doublons et pipelines libres refusés.
- Neuf contrôles techniques vérifiés après audit de sept lectures ciblées
  rejetées à tort ; cinq rapports initiaux réussis et quatre faux positifs
  conservés. Reprise APJA supplémentaire, aucun remplacement des réponses.
- Réserve de l'assistant sur la revue humaine avant notification externe
  dans le cas DPO ; contrôle des sources et avis praticien toujours ouverts.
- Lien personnel de dossier temporaire assaini avec original privé et
  empreintes des deux réponses. 55 tests réussis hors verrou de publication.
- Installation locale isolée et découverte des six skills avec pluginId
  réussies, 167 fichiers de skills comparés. Aucun compte ni appel modèle/MCP
  dans ce smoke ; distribution et installation habituelle inchangées.

## Qualification candidate — 2026-10-07

- Mesure autonome DCP complète : 26 réussites, une demi-réussite, un échec
  selon le juge ; huit cas critiques réussis. Relecture et sources réservées.
- Précontrôle MCP Codex réussi avec connexion existante. Nouveau lanceur
  séquentiel pour les neuf cas, copies natives et preuves d'outils filtrées.
- Profil Codex distinct de l'activation Skill de Claude et de l'installation
  marketplace ; ADR 0005. Timeout, mode dégradé explicite, preuves sans
  écrasement ni raisonnement. Barrière de publication inchangée.

## Distribution — 2026-10-06 — Marketplaces épinglées (sans changement de version)

- Les marketplaces Claude Code et Codex distribuent l'étiquette `v1.1.1`
  (`cad8bbd`), et non plus `main` : une fusion ne publie plus rien.
- `v1.1.1` est consignée comme non qualifiée, distribuée par défaut jusqu'à
  la qualification de la version suivante.
- Procédure de publication et registre des étiquettes : `docs/publication.md` ;
  décision : `docs/adr/0004-distribution-epinglee.md`.
- CI : vérification obligatoire que l'étiquette distribuée existe et désigne
  le commit épinglé.

## 1.2.0 — 2026-10-06 — Candidat d'intégration DCP

- Ajout de `dcp-fpt` 0.1.0 au commit de fusion amont
  `eeb1cb14a3ad94d78631661dce5ae11f1e071308`, sans surcharge locale.
- Copie des 30 fichiers runtime et de la licence ; cache de valeurs,
  conception, outillage et preuves amont exclus.
- Conservation des cinq autres bases, des trois surcharges et du MCP unique.
- Manifestes Claude/Codex et présentation adaptés aux six skills.
- Cinq scénarios DCP ajoutés au contrat de campagne : égalité, acte
  irréversible, frontières financières/données, DSI externe et mode dégradé.
- Nouvelle preuve de candidat avec `release_ready=false`. Mesure, smoke et
  relecture praticien restent à faire après l'intégration candidate.
- Les preuves historiques conservent leur inventaire d'origine ; elles
  n'attestent aucune activation DCP.
- Reprise du candidat 1.1.1 abandonné (`drh-fpt` 0.6.0) : la qualification
  1.2.0 couvre aussi cet alignement.

## 1.1.1 — 2026-10-03 — Candidat d'alignement DRH (cible de qualification abandonnée, distribution gelée)

- **Abandonné comme cible de qualification le 2026-10-06** par décision du propriétaire ;
  ses changements restent à qualifier dans 1.2.0. L'étiquette `v1.1.1`
  demeure distribuée par défaut, non qualifiée, jusqu'à une nouvelle distribution.

- Mise à jour de `drh-fpt` vers 0.6.0 depuis `main`, au commit
  `f81c9b955f7ebb47df7e93bdc41ac743d85a2973` : dix fichiers modifiés et
  ajout de `references/contrat-execution.md`.
- Conservation des quatre autres bases et des trois surcharges déclarées.
- Clarification de la référence DPM : `main` en 1.0.5, distinct de la branche
  par défaut et du checkout local en 1.0.3 au jour du contrôle.
- Nouvelle barrière de release liée à la 1.1.1 ; les preuves historiques de
  la 1.1.0 ne valent pas qualification de cette mise à jour.

## 1.1.0 — 2026-09-20

- Corrections locales traçables des instructions DPM, DPO et recherche
  juridique : provenance de session, abstention, absence de pouvoir d'attente
  et calcul des délais uniquement à partir de faits connus. Les bases amont
  restent figées ; surcharges contrôlées par SHA-256 et ancre unique.

- Ajout de `recherche-juridique` v3.5.0 comme cinquième skill, figé sur le
  commit amont `e437d10a2d4bbf66ba7a9c1e9fb49e773166054e`.
- Conservation d'un unique serveur MCP `droit-francais` : le skill apporte la
  méthode de vérification, le serveur apporte l'accès aux sources.
- Extension du synchroniseur pour les racines amont, les noms de dépôts locaux
  distincts et les fichiers additionnels attribués.
- Ajout de cas de co-activation DPM/juridique et DPO/juridique, et renforcement
  du cas DirFi/DRH/juridique.
- Ajout de la licence CC-BY-SA-4.0 au runtime juridique embarqué.
- Adoption de CC-BY-SA-4.0 comme licence globale du plugin et de ses cinq
  contenus embarqués.
- Ajout de l'identité visuelle du plugin pour les surfaces Codex et ChatGPT.
- Publication d'une politique de confidentialité propre au plugin, avec renvoi
  vers la politique détaillée du serveur MCP `droit-francais`.
- Déclaration du client OAuth public Claude Code et de son callback local fixe,
  sans secret distribué dans le plugin.
- Ajout d'un lanceur de campagne isolé qui exige les coactivations qualifiées,
  exclut les connecteurs juridiques globaux et assainit les traces avant revue.

## 1.0.1 — 2026-09-19

- Mise à jour de `dirfi-fpt` vers la v1.0.4, figée sur le commit amont
  `d970fe530d3f50f6b4c330e3cfb85db35b7126ab`.
- Clarification de la co-activation DirFi/DRH dans le plugin agrégateur.
- Ajout d'un cas de non-régression ChatGPT/Codex sur une gratification de
  départ à la retraite sans base juridique préalable.

## Distribution Codex — 2026-09-19

- Ajout du manifeste Codex, sans modification des quatre skills ni du serveur MCP partagé.
- Ajout de contrôles automatiques pour les skills exposés, le serveur juridique et l'identité du plugin.
- Ajout d'une marketplace Codex pointant vers la racine Git du dépôt, sans duplication des skills.

## 1.0.0 — 2026-09-18

- Première distribution des quatre skills `dpm-fpt`, `drh-fpt`, `dpo-ct` et `dirfi-fpt` depuis des commits amont figés.
- Déclaration du serveur MCP juridique Légifrance/Judilibre.
- Ajout de `upstream.json`, des scripts de synchronisation et du contrôle CI des copies.
- Le contenu métier des skills reste identique aux dépôts amont.
