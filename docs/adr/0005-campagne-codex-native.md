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
