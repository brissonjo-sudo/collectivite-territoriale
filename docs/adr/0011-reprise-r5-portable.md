# ADR 0011 — Récupération publique et contrôles portables de R5

Date : 17 octobre 2026. Statut : périmètre logiciel autorisé par ADR 0010 D4 ;
portage de l'exécution native en attente d'arbitrage.

## Portée de la supersession

Cette ADR additive supersède **uniquement** la limitation de l'ADR 0009 qui
gardait `tests/test_reprise_dev7.py` en archive sans ajout ni exécution.
L'autorisation vient de l'ADR 0010, D4, et du lot T43-L5. L'ADR 0009 n'est
pas réécrite. Aucune autre décision de cette ADR n'est annulée.

## Récupération et identités

`scripts/r5-dependencies.json` décrit la fermeture des imports publics du
lanceur historique et les cinq modules déclarés par son socle : sept fichiers
Python au commit public complet de #16, avec chemins et SHA-256. Le manifeste
distingue les imports publics des imports de la bibliothèque standard ; aucune
dépendance Python tierce n'est ajoutée.

`scripts/r5_portable.py` récupère exclusivement ces blobs depuis un dépôt Git
local ou un bundle dont le SHA-256 explicite est vérifié avant clonage bare
temporaire et vérification Git. Aucune récupération implicite par chemin privé,
aucun profil, OAuth, protocole, gel, reçu, cache ou état n'est matérialisé avec
les modules. Toutes les empreintes sont contrôlées avant création exclusive de
la destination. Une destination existante, un chemin traversant et des
empreintes contradictoires sont refusés.

La racine source, le commit candidat complet, les chemins d'état et
d'installation future ainsi que le chemin et le SHA-256 du CLI sont explicites.
Le commit doit être HEAD d'une source propre ; l'état et l'installation doivent
être neufs, séparés de la source et cohérents entre eux. Aucun état existant
n'est ouvert. Le CLI est vérifié par ses octets ; son libellé de version est
déclaratif, sans exécution ni détection de profil. Le contrat portable lie ces
paramètres, les outils publics et le lanceur ; son empreinte est fournie
indépendamment par l'appelant. Il ne peut hériter de l'identité ou du gel R4.

Les permissions lecture seule/never, une tentative, 240 secondes par cas et
5 700 secondes globales restent strictes. Le statut reste non mesuré ; aucun
score ou avis ancien n'est transférable.

## Contre-épreuves sans préparation

Les quinze contre-épreuves de #16 sont réintégrées. Celles qui initialisaient
un successeur du protocole R4 emploient désormais un plan pur et des fixtures
synthétiques locales, avec une nouvelle identité explicite. Aucun appel à
`initialiser`, `init`, `preflight`, `prepare` ou `run-all` n'est nécessaire.
Les tests de commande SHA-256 et de boucle bornée conservent leur corps #16 ;
la boucle reçoit uniquement un faux harnais local sans répondant.

Les contrôles nouveaux vérifient les paramètres manquants, le CLI divergent,
l'état historique, le cache hors état, HEAD divergent ou modifié et le bundle
sans empreinte. Cela teste l'outillage, sans constituer une mesure de modèle,
une qualification ou un gel du candidat.

## Limite constatée et arbitrage requis

La récupération des modules publics n'en fait pas un harnais natif portable
pour 1.3.0 : `validate_protocol` exige encore `1.2.0-dev.7`, `inputs` exige le
manifeste/cache R3 de 214 fichiers, et `socle.source_blobs` exige son candidat
et son inventaire gelé historiques. Les identifiants de plugin natif sont aussi
historiques. Les remplacer ne relève pas d'une simple substitution de chemins.

Ces validateurs sont récupérés **inchangés**, sans import ni appel. Le lanceur
offre `recover` et `check` ; il refuse explicitement les actions natives plutôt
que de réutiliser ces identités ou de contourner leurs contrôles. La fonction
de boucle bornée reste conservée pour ses contre-épreuves, sans raccordement
CLI à une campagne.

**Question à Claude :** autoriser un lot de portage du bridge natif et de ses
validateurs vers un nouveau contrat 1.3.0, en conservant toutes les propriétés
de preuve, d'inventaire exact, de permissions et de limites, ou limiter R5 à
la récupération et aux contrôles logiciels jusqu'à un chantier distinct ?
Cette ADR constate la limite ; elle ne tranche pas cet arbitrage.

La séparation validate/release et les quatre échecs L4 restent inchangés pour
L6. Aucune campagne, inférence, préparation native, installation, publication
ou poussée n'est autorisée ou exécutée par ce lot. Les preuves R4/R5 restent
des archives historiques, sans lien d'exécution avec le nouveau candidat.
