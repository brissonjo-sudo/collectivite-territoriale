# ADR 0028 — Contrat v4, surcharge DCP et tentative d

Date : 2026-10-22. Décisions du lot B12b : Jo « Surcharge DCP locale »
et « Corriger puis tentative d » ; F2 décidée par Claude dans le périmètre B12.
Sources de décision : consigne B12 et reprise B12b ; preuves de blocage B12.

## Surcharge et sources

Les sept surcharges reçoivent la prescription retraite et la règle de citation
par nom du skill et section. Cette règle prime dans les réponses sur la
traçabilité locale par chemin ; les chemins de lecture internes restent permis.
DCP reçoit seulement le contrat commun et le routage, sans inventaire emprunté.
Insertion avant « ## 1. Déclenchement », base SHA-256
49e04e18203cc6472c35ab595d8f0a9a30671a51bd946d8a03f6b936041ff3b3.
Les autres octets DCP et tous les pins amont sont conservés. La régénération
passe exclusivement par sync_skills, avec empreintes source et bases de chaîne.

La prescription retraite reprend l'invariant v3 existant et le brief : la RM
du 22/05/2025, question 01222, exige consultation en session sur Sénat avant
citation ; sinon abstention balisée. Le CIA reste conditionnel. Aucune nouvelle
assertion de vigueur n'est apportée par cette modification d'instructions.
La piste officielle est celle du précontrôle existant :
https://www.senat.fr/questions/base/2024/qSEQ241001222.html.

## Contrat et sélection fermée

v2 et v3, leurs empreintes, les ADR et les transitions historiques restent
conservés. v4 modifie seulement le web du cas retraite (www.senat.fr et sa
consigne), puis ajoute l'invariant de citation aux deux cas nommés par B12.
Leurs invariants antérieurs restent identiques. Le contrôle déterministe de
chemins est additif et activé par le nouvel invariant ; aucun seuil ne baisse.
La consigne RGPD et ses deux hôtes restent inchangés pour le cas violation.
Une matrice fermée examine chaque invariant des 18 cas selon les outils permis.
Ce contrôle structurel ne prouve ni succès de récupération ni conformité
juridique d'une réponse future.

La nouvelle branche v4 utilise CYCLE_V4, MEASUREMENT_140_V4 et
prepared_cycles["1.4.0-v4"]. Le point d'entrée générique demande --cycle-v4 ;
le lanceur d charge directement le fichier v4 exact. Les lecteurs historiques
v3 restent disponibles et leurs tests ne changent pas. Aucun champ de preuve,
version, HEAD ou empreinte recalculée ne sélectionne une mesure inconnue.

## H1c → H2 → H3

En H1c, MEASUREMENT_140_V4 et les liaisons restent None/null. Après mesure réelle,
H2 remplace seulement cette affectation littérale par le SHA complet de H1c,
lie prepared_cycles["1.4.0-v4"].measurement_commit et ajoute
campaign_measurements[H1c] au verrou. Fermer ensuite le manifeste 0028 avec
ce SHA, les deux empreintes d'objets Git H1c et les deux empreintes cibles.
Le contrat v4 exact et CAMPAIGN_140_CLI complet restent ceux de H1c.
Le périmètre est exactement cli_toolchains.py, measurement-cli.json et
toolchain-transition-0028.json, sous scripts/. Aucun autre fichier, test,
lecteur, seuil ou pin ne peut changer dans cette fermeture. Les trois contrats
v2/v3/v4 sont vérifiés depuis Git H1c, le snapshot et le checkout H2.
H3 contient seulement la projection publique, après smoke autorisé sur H2.

## Pré-vol et préparation extérieure au dépôt

Les sorties simulées portent release_evidence: false et restent hors candidat.
La tentative c consommée ne doit pas être assemblée ; ses sources restent en
archive et sont indexées sans reprise de résultat dans d. d prévoit 18 cas,
36 sessions, high, plafond de suivi de 40 M jetons entre rôles. Le précontrôle
CNIL et Sénat 200 reste obligatoire avant le lancement réel.
Le lot ne lance ni modèle, OAuth, smoke, Docker, poussée ou publication.
Les copies actualisées du harnais et de la CI restent dans suivis/, conformément
à la règle de conservation des archives t43-successeur du brief.
Tout test historique incompatible est rapporté, sans changer son attendu.

## Refus constatés pendant B12b

La surcharge autorisée rend la référence autonome DCP-014 incompatible avec
les octets de SKILL.md. dcp_reference.reference refuse « Octets DCP mesurés
divergents : SKILL.md » et le qualificateur exige encore l'égalité de tout le
runtime DCP mesuré. Ces deux contrôles restent intacts. La campagne plugin
ne remplace pas implicitement cette référence autonome.
Les tests de distribution exigent aussi l'absence de instruction_overlays
pour DCP ; les replays EOF utilisent encore l'entrée DCP de 319 lignes.
Leur attendu et leur code restent inchangés. Aucune préparation de d ne vaut
levée de ces refus. Le lot rapporte un blocage et des propositions pour Jo.
