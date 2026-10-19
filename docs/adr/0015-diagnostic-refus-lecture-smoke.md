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
