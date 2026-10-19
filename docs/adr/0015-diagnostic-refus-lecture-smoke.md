# ADR 0015 — Diagnostic public des refus de lecture du smoke

Date : 19 octobre 2026. Décision de Jo, lot T43-L19.
Statut : correctif local ; aucun appel modèle ni smoke exécuté dans ce lot.

Avant chacun des trois refus existants de read_events, le runner écrit sous
la sortie de mesure un fichier <cas>.read-refusal.json, diagnostic-only.
Il conserve le texte de la commande après le masquage L12b, borné à 2 000
caractères, avec indication de coupure et SHA-256 du texte masqué complet.
Code de sortie, statut natif reconnu et longueurs en caractères/octets UTF-8
sont présents ; aucun contenu de sortie n'est conservé dans ce diagnostic.
Un statut arbitraire est remplacé par un libellé non reconnu. L'écriture est
exclusive : une pièce existante n'est jamais écrasée.

Les messages « Commande hors contrat de lecture installé », « Lecture hors
skill installé » et « Lecture installée tronquée ou échouée » sont inchangés.
La grammaire de commande, la frontière du skill, la preuve de contenu, le
code zéro et le statut completed restent exigés. Le diagnostic n'est ni une
preuve positive, ni une mesure reconstituée de la commande perdue en L18b.

Le masquage est repris de l'outil public command_trace.py du lot L12b :
chemins de credentials, clés/jetons, affectations/options, Bearer/JWT,
identifiants dans les URL et clés privées ; il précède la troncature.
Aucun secret réel n'est utilisé dans les tests.

L'ADR 0013 conserve sa liste fermée et tous ses contrôles. Seule l'empreinte
cible scripts/run_codex_smoke.py dans toolchain-transition-0013.json passe de
f84178ed42528c7cb89ce9b2812a4de77e8470ec40c4cdcf1a43b3d74bf8441d
à
428f33ca15451867d930299d1d8324f38921627cfcfa66fe096f260073b4f569.
Les sources L14, cinq autres cibles, verrous CLI/campagne, validateurs, tests
existants, seuils et CI restent inchangés. Aucun score ou résultat ancien
n'est transféré au candidat par ce renouvellement.

Le smoke L19 est pré-déclaré séparément pour une seule tentative,
smoke-l19-20261019-a, sur la nouvelle tête. Le précontrôle natif conserve
180 secondes et le réarmement des seuls refus attestés avant modèle ; toute
session modèle consomme la tentative. Aucun rejeu ni assemblage entre
tentatives n'est permis. La tentative L18b consommée est conservée telle quelle.


## Addendum — 19 octobre 2026, décision de Jo, T43-L22

Cet addendum complète l'ADR 0015 sans réécrire la décision L19 ci-dessus.
Jo retient les options **b + a + durcissement** du diagnostic L20 depuis
87afc049f70b7900bc670b5f683a033724cae136. Aucun appel modèle ni push dans L22.

Les patches L20 sont vérifiés contre leur MANIFESTE-SHA256.json, puis
appliqués sans modification : option b (SHA-256
240bf1d0e0e880465dd6cf9c8f2c2c8d57f4ac04f794961761e4f6fb4b153fd2)
pour la surcharge DCP avant le titre et la description frontchargée ;
option a (SHA-256
7dedfb4e36e83bf1b341f7675a46053a27b7cac2b18f1d2524694401495d8240)
pour STOP métier et lecture unique dans la surcharge recherche-juridique.
Les sources et empreintes déclarées régénèrent exactement les deux entrées.

**DCP-0 ne s'applique plus à ces octets DCP.** dcp_reference.py,
check_dcp_protocol.py et dcp-protocol.json restent inchangés. La référence
historique est conservée ; son emploi pour ce candidat doit être refusé
avec « Octets DCP mesurés divergents : SKILL.md » et le contrôle CLI retourne 2.
Les tests conservent leur témoin historique positif et toutes les mutations
refusées ; ils exigent aussi le refus du candidat surchargé. Une nouvelle
preuve autonome DCP au runtime exact est requise en L23, sans transfert
d'ancien score ni modification du contrôle DCP-0 pour accepter cette preuve.

Le fichier tests/cas-plugin.json reste historique et inchangé. Le contrat
de cycle distinct scripts/cas-plugin-cycle-v2.json conserve les 18 demandes
et invariants et migre trois cas vers schema_version=2 / stop_first=true :
plugin-garde-fou-apja, plugin-dcp-egalite, plugin-dcp-acte-irreversible.
Les neuf cas comportementaux déjà v2 restent inchangés ; les six autres
historiques restent v1. Le chargeur refuse toute autre dérive et tout repli
en l'absence du fichier. Il ne suffit pas d'ajouter true en v1.

La campagne Codex utilise ce contrat, le journalise et applique le contrôle
déterministe existant : STOP comme premier texte visible, avant tout outil.
Le relecteur utilise le même contrat. Le fichier de cycle est sous scripts/
pour être inclus sans exception dans toolchain_sha256 ; le hash du contrat
historique reste distinct. Le runner smoke prend aussi ses cas sources
dans ce contrat : STOP est éliminatoire pour les deux cas lorsqu'il est
requis, indépendamment de leur nom. Les tests négatifs couvrent absence,
annonce préalable et outil préalable ; les doublons de lecture restent refusés.

Les fixtures de relecture et DCP-0 historiques sont testées sur leurs octets
Git mesurés, pas sur le runtime courant. Un test supplémentaire interdit
explicitement le transfert de l'avis L14 au candidat surchargé. Les deux
anciennes assertions d'absence de surcharge DCP sont remplacées par
l'exigence des deux seules surcharges décidées par Jo, avec empreintes exactes.
Aucun seuil, refus de production ou contrôle CI n'est réduit.

L23 prépare seulement un plan autonome DCP, hors candidat, depuis
brissonjo-sudo/DCP-fpt au commit
129f374e6ab8ea3b47bcfd9de9ddd52a2d3d9498. Le protocole empreinte le runtime
fourni ; il permet donc de mesurer les nouveaux octets avec une nouvelle
tentative. Le profil de l'ADR 0002 amont impose Codex, gpt-6.1-sol aux deux
rôles, web au répondant et aucun web au juge, processus/dossiers distincts,
sans MCP implicite. Les 28 cas et leur barème ne sont pas modifiés :
28 × 2 sessions au maximum. Une tentative, arrêt selon PLAN-CYCLE.md,
revue humaine requise et autorisation Jo séparée avant tout appel.

Aucune mesure, preuve, transition d'outillage L14/L19, résolution humaine,
qualification, installation ou gel historique n'est transféré. Les outils
d'assemblage/release conservent leur refus : la reconnaissance éventuelle
d'une nouvelle référence DCP devra être décidée séparément après L23.
