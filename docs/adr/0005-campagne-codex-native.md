# ADR 0005 — Exécuter la coactivation candidate sur Codex

- Date : 2026-10-07.
- Statut : accepté pour les essais autorisés.
- Autorisation : l'utilisateur demande une campagne sur Codex sans connexion Claude.

## Décision

Conserver les neuf cas et invariants de `tests/cas-plugin.json`. Le lanceur
`scripts/run_codex_campaign.py` copie les six skills du candidat dans le
dossier natif `.agents/skills` d'un dossier neuf pour chaque processus Codex.
Il demande la lecture intégrale et ordonnée des points d'entrée. Les traces
enregistrent les chemins des commandes de lecture et leur statut ; une
mention textuelle ou une lecture bloquée ne constitue pas une preuve.

Le serveur `droit-francais` est déclaré explicitement à partir de la
configuration publique du dépôt, avec les six outils juridiques autorisés.
La configuration personnelle des serveurs n'est pas importée. Le magasin
OAuth existant de Codex est utilisé sans copie de secrets ni changement de
connexion. Le serveur est requis au démarrage pour les sept cas nominaux ;
chaque cas doit aussi présenter au moins un appel effectivement réussi.
Les deux cas dégradés ne déclarent aucun MCP et désactivent le web. Seul
le cas RGPD autorise des ouvertures sur EUR-Lex ou la CNIL.

Sandbox en lecture seule, backend Windows explicite, délai borné par cas,
exécution séquentielle et refus d'écraser une preuve existante. Les flux
bruts sont filtrés en mémoire ; aucune signature ni raisonnement conservé.

## Portée des preuves

Le profil `codex-copies-natives-mcp-v1` atteste les commandes de lecture et
appels d'outils observés. Les commandes shell ne disposent pas d'une liste
de permissions aussi fine que Read dans Claude : la restriction de chemins
est une consigne et un contrôle de trace, pas une isolation complète du poste.
Le contrôle des chemins et du statut ne prouve pas à lui seul la lecture
intégrale de chaque fichier par le modèle. La disponibilité globale de
skills imposés par l'environnement peut influencer le contexte.

Ce profil n'atteste ni les appels de l'outil Skill de Claude, ni une
installation marketplace, ni un chargement par le gestionnaire de plugins.
Les résultats restent distincts des preuves Claude historiques et des
28 cas DCP autonomes. Les invariants métier doivent être relus par un humain.
La barrière de publication et la distribution v1.1.1 restent inchangées.

## Complément du 2026-10-07 — restitution par segments

Le profil v2 vérifie le contenu complet dans la sortie brute, mais le
répondant signale une troncature de la sortie visible. Cet essai est arrêté
après deux cas complets et conservé séparément ; il ne qualifie pas la
lecture intégrale des points d'entrée.

Le profil `codex-copies-natives-mcp-v3` remplace cette lecture monolithique
par une partition contiguë de lignes de 6000 octets maximum par segment.
Chaque segment fait l'objet d'un appel séparé. Ordre, contenu et couverture
doivent correspondre à la partition calculée sur les fichiers figés ; trou,
doublon, extrait différent ou pipeline non généré font échouer le contrôle.
Les seules nouvelles expressions shell admises sont les pipelines de lecture
Get-Content / Select-Object explicitement construits. Ce contrôle reste une
vérification de restitution, sans preuve d'attention du modèle.

L'installation locale par le gestionnaire de plugins est mesurée dans un
CODEX_HOME distinct, sans compte ni copie d'identifiants. Six skills qualifiés
avec pluginId sont découverts ; leurs 167 fichiers restent identiques. Aucun
modèle ni MCP n'est appelé dans ce smoke. Cette preuve et la campagne avec
copies natives conservent des portées distinctes, sans être présentées comme
un test complet du plugin installé.

Le contrôle v3 initial rejette aussi les pipelines de sélection de références.
Cette restriction ne correspond pas au contrat de lecture des références
utiles. Le vérificateur corrigé admet uniquement Get-Content / Select-Object
sur un fichier Markdown de references/ ou objets/, sans commande additionnelle
ni traversée de chemins. Pour les traces déjà produites, un audit distinct
exige la correspondance exacte du SHA-256 de la sortie avec le segment du
runtime figé. Les rapports initiaux restent inchangés ; aucun score métier
n'est déduit de cette correction du contrôle technique.

Les processus Codex ont conservé leurs journaux locaux. Le lanceur filtre
ses sorties en mémoire et aucune pensée, signature ou sortie brute n'entre
dans les artefacts publics. L'extracteur ne retient que les commandes de
lecture des sessions identifiées par le workspace, le prompt et la fenêtre
temporelle. Les identifiants de connexion ne sont ni copiés ni exportés.
