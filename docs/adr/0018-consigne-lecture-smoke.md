# ADR 0018 — Consigne de lecture unique avant le smoke

Date : 20 octobre 2026. Décision de Jo, T43-L29 : « Préciser la consigne ».

La tentative `smoke-l28-20261020-a` sur `af6fa13` est consommée : une session,
210 868 jetons d'entrée. STOP premier et MCP installé réussissent. Le contrôle
`complete_entry` refuse les deux lectures complètes de l'entrée juridique,
chacune de 1 162 lignes (départ 0). Le modèle signale une restitution tronquée
après la première ; les deux lectures portent cependant `content_verified:true`.
Ce signalement ne démontre donc pas un plafond de restitution de la CLI.
L'original reste intact, compté à part, jamais assemblé avec une autre tentative.

La consigne apparaît avant tout outil dans `smoke_prompt`, sans nommer les
skills. Jusqu'à 319 lignes incluses : une lecture intégrale unique. Au-delà,
ou si la longueur est inconnue : une seule série de segments contigus, au plus
90 lignes par commande `-Skip M -First N`, dès le départ et jusqu'à la fin.
Aucune relecture, même après un signalement de troncature. La réponse signale
les limites sans affirmer le contenu absent et sans s'interrompre pour ce motif.
Le modèle n'a pas à relire le fichier pour en compter les lignes.

Justification empirique, non garantie générale : avec la CLI exacte
0.163.0-alpha.10.2, le smoke a restitue intégralement l'entrée de 319 lignes
avec contenu vérifié, alors que la lecture de 1 162 lignes provoque le signalement
ci-dessus. Le seuil 319 retient cette borne intégrale effectivement réussie,
sans interpoler une limite entre les deux longueurs. Dans la campagne d,
`l8-dcp-vers-dsi-disponible/reponse/trace.jsonl`, lignes 28 à 47, dix segments
consécutifs vérifiés couvrent les 1 162 lignes : 92, 90, 127, 107, 141, 120,
112, 118, 118, 137. Le segment de 90 lignes (départ 92, ligne de trace 30,
5 995 octets source) est la plus petite de ces restitutions réussies ; la
consigne adopte ce maximum prudent, sans prétendre mesurer un plafond CLI.
Le découpage fixe reste à éprouver par le prochain smoke réel.

Preuve smoke : `l28-smoke/sorties/smoke-l28-20261020-a/mesure/activation-implicite.json`.
Les empreintes des originaux et les segments publics sélectionnés sont consignés
dans `t43-successeur/l29-preuves/restitution-observee.json`, hors candidat.

La transition fermée de l'ADR 0017 ajoute seulement
`scripts/run_codex_smoke.py` à sa liste de chemins. Le manifeste existant
`scripts/toolchain-transition-0017.json` lie aussi ses empreintes source exacte
(commit mesuré `13b4e1e537e5a8097a004ee913abcc9d079114a7`) et cible exacte.
Les nouvelles empreintes du lecteur de transition et du CHANGELOG sont liées
de la même manière. Toute autre dérive d'outillage reste refusée. La campagne d
et son avis humain doivent rester recevables ; un smoke réel lié à la nouvelle
tête reste obligatoire, et aucune release n'est produite ici.

Seul `smoke_prompt` change dans le runner. `complete_entry`, le validateur,
STOP, l'interdiction du web, les deux cas, tous les autres contrôles et les
197 fichiers des sept skills restent inchangés depuis le runtime mesuré.
Aucun appel modèle, installation, connexion MCP, poussée ni smoke dans ce lot.
