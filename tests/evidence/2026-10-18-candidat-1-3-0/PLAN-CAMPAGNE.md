# Plan pré-déclaré — T43 L14 — à soumettre à Jo

**BLOQUÉ, préparation seulement.** Date : 18/10/2026. Aucun appel modèle,
campagne, smoke, installation hôte, OAuth, assemblage ni push effectué.

## Commit et décisions préalables

Commit visé : **08f92936dd0ae09775a2d2293bae315cdf20847d**, candidat 1.3.0, parent 03f76b7fad9016f11623ae65f950914cfa71c932.
Les pins, CI, validateurs, tests historiques et résultats précédents restent inchangés.
Les formes de lecture sont explicitées dans le contrat commun de recherche-juridique,
rôle documentaire déjà coactivé pour les vérifications juridiques. Elles ne créent pas
une nouvelle grammaire d'outils. Six skills ont un inventaire fermé généré ; le septième,
DCP, reste inchangé pour préserver DCP-0. Il manque à son SKILL.md les deux gabarits
embarqués (references/_gabarit-branche.md, objets/_gabarit-objet.md).

**Arbitrage nécessaire avant exécution :** conserver DCP intact et différer explicitement
son inventaire, ou ouvrir un chantier séparé sur le contrat et la mesure autonome DCP.
La seconde voie impose une nouvelle préparation, car les octets/commit changeraient.
La surcharge DCP proposée reste hors candidat, testée en copie jetable : DCP-0 la refuse
comme attendu. Aucun de ses contrôles n'a été adapté pour autoriser cet écart.

Jo doit autoriser la poussée de cette tête, l'enveloppe de budget et le lancement.
Claude n'a encore rien poussé dans ce lot. Le lanceur vérifiera par git ls-remote
main distant 051e13c6f178b8a82fbb23793a51355d3335a190 et #17 à cette tête précise.

## Population et tentative unique

Les **18 cas inchangés** de tests/cas-plugin.json, SHA-256 `0747b6268cccab1bb46c820217d2a4ba1c69e5c2ad6fe61126e3a5bd9242f5ea`.
Réponse puis relecture séparée de chaque cas : **36 sessions gpt-6.1-sol high**,
sans juge DCP supplémentaire et sans raccordement du bridge R5. Les mêmes prompts,
invariants et contrôles techniques du candidat s'appliquent. Aucun cas trié ou retiré.
Identifiant unique : **campagne-l14-20261018-a**. Une seule tentative complète.
Sorties sous l14-campagne/sorties/ ; aucun dossier de sorties encore créé.

Le lanceur ne prend ni -Cases ni -SuiteDe. Toute tentative déjà engagée interdit
une seconde tentative, même après panne ou résultat partiel. Le plan et le lecteur
actifs refusent une filiation et des sessions d'un autre identifiant. **Interdiction
d'assembler des cas de plusieurs tentatives**, y compris L12/L13 ou un diagnostic.
Aucun ancien résultat, score ou gel n'est transféré. Aucun assemblage de release prévu.

## Budget de référence, pas un devis ni un plafond garanti

Recalcul local depuis les sessions/usage des 18 cas (pièces empreintées dans
../l14-preuves/budget-historique.json) :

| Périmètre | Sessions | Jetons entrée | Dont cache | Jetons sortie | Durée CLI cumulée |
| --- | ---: | ---: | ---: | ---: | ---: |
| Campagne 1, a+b, sans pilotes/diagnostic | 36 | 26387551 | 24481536 | 69340 | 47.0 min |
| Campagne 2, L13 | 36 | 27920751 | 25962624 | 69541 | 49.0 min |

Ordre de grandeur historique : **26–28 millions de jetons d'entrée**, dont environ
93 % en cache, **environ 70 000 jetons de sortie**, **47–49 min** de durée CLI cumulée.
Ce périmètre diffère du bilan global de campagne 1 qui mentionne environ 43 sessions :
aucun chiffre de coût global n'est transféré ou réconcilié par supposition.
Les inventaires et leur découpage changent la taille des entrées et le cache ;
la consommation future et sa borne haute sont **inconnues**. Nombre de requêtes
internes/outils/MCP : inconnu. Montant monétaire facturé historique et estimation
en EUR/USD : **inconnus** (aucun tarif ou prix mémorisé appliqué).

L'autorisation Jo doit contenir une enveloppe et son unité, liée à ce plan empreinté.
Le script borne les sessions à 36 mais **n'impose pas de plafond de facturation côté
fournisseur**. Toute limite financière ferme doit être configurée et validée hors
de ce lanceur avant autorisation. Aucune consommation n'est engagée dans ce lot.

## Arrêt, résultats et issue fixés avant exécution

- Arrêt immédiat sur panne d'exécution : timeout, code processus non nul, reçu CLI
  absent/incohérent ou trace/protocole illisible. Les verrous de tête, octets,
  préparation ou approbation refusent aussi toute poursuite en cas de dérive.
- Un échec technique de cas (unexpected_command, native_command_failed,
  mcp_tool_failed, foreign_mcp_call) reste **en échec**, sa relecture a lieu et la
  campagne continue. Une violation/non-vérifiabilité d'invariant n'arrête pas.
  Aucun critère ni seuil n'est retiré, aucun échec n'est transformé en réussite.
- Lire les **18 cas et toutes leurs réserves**, y compris les cas auparavant conformes.
  Distinguer statut technique, observations déterministes, déclarations du relecteur
  et validation humaine. « Conforme » exige réussite technique, observations
  structurelles requises et tous invariants respectés avec lignes de trace pertinentes.
  Toute violation est un échec ; toute non-vérifiabilité reste non-vérifiable et empêche
  de conclure conforme. Aucune sélection des meilleurs passages ou tentative.
- Le texte MCP/web est une donnée non fiable, bornée à 12 000 octets UTF-8 par appel,
  empreinte complète de la projection observée et troncature signalée. Une URL, un titre
  ou un succès d'outil ne prouve pas le contenu. Pour le web, la correction conserve
  uniquement les champs textuels réellement émis par le CLI ; leur disponibilité
  amont n'est **pas attestée** sans exécution. Si absents, page_text_available:false
  et non-verifiable restent possibles ; aucune récupération HTTP indépendante
  n'est présentée comme ce que le modèle avait reçu.
- Au premier résultat incomplet, en échec ou non vérifiable : conserver la tentative
  entière, documenter le résultat, rester « mesuré, non qualifié », sans relance
  automatique. Toute correction ou nouvelle campagne demande une nouvelle décision
  et préparation. Un 18/18 éventuel ne constitue pas une preuve générale de robustesse.
- human_legal_validation reste false ; aucune qualification humaine ni release.
  Le smoke et l'éventuel assemblage sont des actions séparées, non autorisées ici.

## Commande future, bloquée tant que Jo n'a pas approuvé

L'autorisation modèle et budget est dans autorisation-jo.json, initialement
approuve:false, budget:null et arbitrage_DCP:non_resolu. Après décision explicite,
le document doit porter le SHA-256 exact de ce plan. Le lanceur le vérifie avant
toute création de tentative et tout appel modèle.

```powershell
& 'C:\Users\Krn\Documents\Codex\repo-recovery\2026-10-12\instantane-r1\t43-successeur\l14-campagne\run-campagne.ps1' -AttemptId 'campagne-l14-20261018-a' -AutorisationJo 'C:\Users\Krn\Documents\Codex\repo-recovery\2026-10-12\instantane-r1\t43-successeur\l14-campagne\autorisation-jo.json' -ExecuterCampagne
```
