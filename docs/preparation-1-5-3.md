# Collectivité 1.5.3 : candidat préparé en H1, non mesuré, non qualifié

État au **16 novembre 2026**, H1 préparé localement. Décision de Jo du 2026-11-15 : la 1.5.3 forme
un **lot unique**. Elle porte la distribution Antigravity
([ADR 0037](adr/0037-distribution-antigravity.md)) et les six réserves non
bloquantes relevées après DCP-019 et la campagne 1.5.2. La version publiée et
les deux catalogues restent sur **1.5.2** jusqu'à la
[procédure prévue](publication.md).

## Contenu du lot

| Réserve | Origine | Correction | Où |
|---|---|---|---|
| Délai décisif lu sans être donné | DCP-019 cas-07 | Un délai lu en session qui commande l'urgence s'indique avec sa valeur, sa source et sa date de lecture | dcp-fpt 0.2.0, §5.4 |
| STOP égalité trop affirmatif | DCP-019 cas-12 | Après le bloc, une phrase nomme l'acte précis qui rompt l'égalité ; les voies régulières recensées ensuite ne sont pas exclues | dcp-fpt 0.2.0, §5.2 |
| Voies d'exécution confondues | DCP-019 cas-18 | Exécution aux frais et risques, résiliation et marché de substitution nommés séparément, chacun avec sa condition | dcp-fpt 0.2.0, branche résiliation |
| Risque pénal sans référence | campagne 1.5.2, `plugin-dcp-egalite` | Chaque risque ou compétence nommé par un bloc STOP porte ensuite sa référence lue en session, ou « non vérifié » | dcp-fpt 0.2.0, §5.3 |
| CAO sans référence | campagne 1.5.2, `plugin-dcp-acte-irreversible` | Même règle | dcp-fpt 0.2.0, §5.3 |
| Provenance affirmée trop fort | campagne 1.5.2, `plugin-prime-depart-retraite` | « Texte récupéré » seulement si le libellé a été reçu ; sinon « page officielle consultée » | surcharge locale `recherche-juridique` |

Les en-têtes et les blocs STOP ne changent pas ; leur ajout se place après
eux. Aucune règle de droit, valeur ni identifiant n'est ajouté : les trois
références en cause (R. 2193-4 du CCP, L. 1414-2 du CGCT, 432-14 du code
pénal) figurent déjà au registre daté de dcp-fpt. La version 0.2.0 donne la
référence DCP-020 (choix de Jo du 2026-11-15).

## État des corrections

- **dcp-fpt 0.2.0** : fusionné en amont (PR 22, `c810d10`), mesuré
  DCP-020 (27/28, un ÉCHEC non critique au cas-06), relu par Jo avec sept
  réserves ; preuves fusionnées (PR 23, `cad0259`). Paquet
  `5baff7a6b9cff6bb3f476443cee4cface80e5367034dbd144b04a70f4e431cff`.
  Plugin ré-épinglé sur `cad0259` ([ADR 0038](adr/0038-dcp-020-reference-autonome.md)).
- **Surcharge `recherche-juridique`** : sur cette branche ; empreintes
  rechaînées dans `upstream.json` et copie resynchronisée, `check_sync` OK.
- **Antigravity** : déjà sur `main` (PR 44). `plugin.json` et
  `mcp_config.json` restent hors des jeux de configuration comparés au
  smoke ; `plugin.json` passe en 1.5.3 avec les deux autres manifestes.
- **H1** : cycle 1.5.3 préparé ([ADR 0039](adr/0039-mesure-1-5-3-contrat-v4.md)),
  contrat v4 et CLI de la 1.5.0 inchangés, transition 0039 non fermée.

## Phases et verrous

Chaque étape coûteuse passe d'abord par un pré-vol à blanc
(skill `pre-vol-avant-execution-couteuse`), puis attend l'accord exprès de Jo.

1. **Relecture du diff dcp-fpt par Jo** (§5.2, §5.3, §5.4, branche
   résiliation), puis poussée, PR et fusion sur le dépôt amont.
2. **Mesure autonome DCP-020** : 28 cas, 56 sessions Codex, même lanceur,
   même barème et même seuil que DCP-019. Ensuite : avis daté de Jo, et
   preuves commitées en amont.
3. **H1 plugin** : ré-épinglage de dcp-fpt sur le pin de preuve DCP-020
   (ADR de référence autonome, `dcp-protocol.json`, `dcp_reference.py`). Les
   manifestes Claude Code, Codex et Antigravity passent en 1.5.3. ADR de
   mesure 1.5.3 sous contrat v4, sur le modèle de l'[ADR 0036](adr/0036-mesure-1-5-2-contrat-v4.md) :
   `MEASUREMENT_153_V4`, transition préparée non fermée, `CAMPAIGN_150_CLI`.
   Les catalogues restent sur 1.5.2.
4. **Campagne plugin** : 18 cas du contrat v4 sur H1, puis avis daté de Jo.
5. **H2** (liaison du seul H1 mesuré), puis **smoke** réel 2/2 (connexion
   Codex et OAuth du MCP par Jo).
6. **H3** : `tests/evidence/release-1.5.3.json`. La barrière de release
   repasse au vert ; PR vers `main` en merge commit.
7. **Étiquette `v1.5.3`** annotée, sur accord de Jo, puis PR de distribution
   (deux catalogues et registre).
8. **Recette Antigravity depuis l'étiquette** : clone propre de `v1.5.3`,
   7 skills visibles, authentification, appels `search` puis `fetch`. Le
   README retire alors la mention « à venir ».

## Limites connues

- Tant que H3 n'existe pas, la barrière de release échoue sur cette branche :
  le runtime de `recherche-juridique` diffère de celui de la preuve 1.5.2.
  Ne pas fusionner la branche avant H3.
- Ces corrections ne sont pas mesurées. Aucun score de DCP-019 ni de la
  campagne 1.5.2 n'est transféré.
