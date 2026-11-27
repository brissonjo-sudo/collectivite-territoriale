# ADR 0042 : mesure 1.5.4 sous contrat v4, bascule du serveur MCP vers le pont

Date : 2026-11-27. Décisions de Jo du 2026-11-27 : « Assumer et signaler
(Recommandé) », « Ouvrir à tout compte vérifié » et « Oui, cycle complet
(Recommandé) ». Préparation H1 ; aucun modèle, aucune campagne, aucun smoke ni aucune
preuve dans ce lot.

## Contexte

Jusqu'à la 1.5.3, le serveur MCP `droit-francais` du plugin pointe vers le service
historique `https://droit-francais-skill.onrender.com/mcp`, qui consomme les clés PISTE
de l'exploitant. Les CGU PISTE (§ 3.1.1, § 3.1.2) réservent les clés à une application
donnée et en interdisent le partage hors de son organisation ; la question est ouverte
en amont ([ADR 0001](https://github.com/brissonjo-sudo/droit-francais-skill/blob/main/docs/adr/0001-pont-identifiants-appelant.md)
du dépôt `droit-francais-skill`).

En amont, le service `https://droit-francais-pont.onrender.com/mcp` fonctionne en mode
`account` ([ADR 0002](https://github.com/brissonjo-sudo/droit-francais-skill/blob/main/docs/adr/0002-comptes-cles-piste.md)
amont, `docs/oauth.md` § « Comptes à clés PISTE personnelles ») : l'utilisateur se
connecte par OAuth Auth0 (même émetteur `https://dev-7soa32jfmxpejzhs.eu.auth0.com/`),
enregistre **ses** clés PISTE avec l'outil `configurer_cles_piste` (lien signé, usage
unique, 10 minutes) et peut les supprimer avec `oublier_cles_piste`. Aucune clé
d'exploitant n'est utilisée.

## Décisions de Jo (2026-11-27)

- « Assumer et signaler (Recommandé) » : la question CGU PISTE § 3.1.2 reste ouverte et
  doit être signalée aux utilisateurs.
- « Ouvrir à tout compte vérifié » : le pont acceptera tout compte à e-mail vérifié. Ce
  changement se fait dans l'Action Auth0 par Jo, hors de ce dépôt.
- « Oui, cycle complet (Recommandé) » : nouveau cycle complet (campagne 18 cas contrat
  v4, relecture, H2, smoke, H3).

## Décision

1. **Bascule MCP.** Dans `.mcp.json` (Claude Code, Codex) et `mcp_config.json`
   (Antigravity), seule l'URL change : `https://droit-francais-skill.onrender.com/mcp`
   devient `https://droit-francais-pont.onrender.com/mcp`. Le `clientId` public
   `tpc_gCoyj4qPSuyrg1ZZWDyp4D` et le `callbackPort` 44956 restent. Selon `docs/oauth.md`
   amont, le client prédéfini doit être autorisé sur l'API du pont : à vérifier par Jo
   dans Auth0.
2. La 1.5.4 est mesurée avec le **contrat de cycle v4 à l'identique**
   (`scripts/cas-plugin-cycle-v4.json`, empreinte
   `be70f64b4650a72c15a33e477c81f84c61c602ceb22ad23cc1783c3412888f24`, mêmes 18 cas) et
   la **même CLI figée** que les versions 1.5.0 à 1.5.3 (`CAMPAIGN_150_CLI`,
   `codex-cli 0.164.0-alpha.11.1`).
3. Le mécanisme des [ADR 0031](0031-mesure-1-5-0-contrat-v4.md),
   [0034](0034-mesure-1-5-1-contrat-v4.md), [0036](0036-mesure-1-5-2-contrat-v4.md) et
   [0039](0039-mesure-1-5-3-contrat-v4.md) est réutilisé tel quel ; seule une entrée de
   version est ajoutée :

| Version | Commit lié | Transition | CLI |
|---|---|---|---|
| 1.5.4 | `MEASUREMENT_154_V4` (`None` en H1) | `toolchain-transition-0042.json` | `CAMPAIGN_150_CLI` |

   - `scripts/cli_toolchains.py` : constantes `MEASUREMENT_154_V4`,
     `TRANSITION_154_V4`, `MIGRATION_154_V4`, `ADR_154_V4`, entrée `1.5.4` de
     `v4_measurements()` ; la 1.5.4 rejoint `SMOKE_FOLLOWS_MEASUREMENT`.
   - `scripts/measurement-cli.json` : `prepared_cycles["1.5.4-v4"]`, non lié.
   - `scripts/toolchain-transition-0042.json` : préparé non fermé.
4. Les trois manifestes (`.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
   `plugin.json`) passent en 1.5.4.
5. Aucun assouplissement. Les entrées, preuves et transitions antérieures ne changent
   pas. Le commit mesuré de la 1.5.3 (`e8f42719e90e5fdf69458cf9960bf04ee6560f84`) est
   refusé comme H1 de la 1.5.4, comme tout commit déjà lié à une autre mesure.

## Conséquences

- **Cycle complet obligatoire.** `.mcp.json` fait partie de `CONFIGURATION`
  (`scripts/measurement_common.py`) : le changer modifie
  `plugin_configuration_sha256`, donc les mesures de la 1.5.3 ne couvrent pas ce runtime.
- **Compte vérifié et clés propres.** Chaque utilisateur doit disposer d'un compte à
  e-mail vérifié accepté par le pont et enregistrer ses propres clés PISTE
  (`configurer_cles_piste`). Sans clés, le serveur invite à les enregistrer ; les skills
  métier restent utilisables, sans vérification du droit.
- **Question CGU PISTE § 3.1.2 ouverte.** Elle n'est pas tranchée ; elle est signalée aux
  utilisateurs (README, CHANGELOG) comme l'a décidé Jo. Le pont stocke les clés
  chiffrées côté Auth0 ; l'exploitant détient la clé de déchiffrement (ADR 0002 amont).
- **Service historique.** Le plugin ne l'utilise plus. Il n'est pas arrêté par ce dépôt.
- **Changement visible pour les utilisateurs existants** : nouvelle connexion OAuth sur
  l'API du pont, puis saisie des clés.
- **Politique de confidentialité.** `PRIVACY.md` renvoie à la politique du dépôt amont ;
  son contenu relatif au pont n'a pas été revu dans ce lot.

## Tests

`tests/test_transition_154_v4.py` calque la contre-épreuve 1.5.3 et ajoute le refus du
commit mesuré de la 1.5.3 comme H1. `tests/test_cli_toolchains.py` simule la liaison de
la version courante du plugin. Les tests de manifestes ne figeaient pas l'ancienne URL
(`https://` seulement, `mcp_config.json` aligné sur `.mcp.json`) : aucun n'a changé.

`tests/test_codex_plugin.py`, `test_preuve_courante_correspond_au_runtime` (branche
« non mesuré ») supposait qu'un candidat change toujours les skills (« Runtime différent
du plugin installé » et commits amont différents). La 1.5.4 ne change que la
configuration installée. Décision de Jo du 2026-11-27, « Accepter la correction
(Recommandé) » : le test exige toujours « Version non mesurée », et accepte un runtime
**ou** une configuration différents de la preuve publiée ; la comparaison des commits
amont est retirée.

## Hébergement du pont (complément du 2026-11-27)

Une migration du pont vers un autre hébergeur et un domaine propre avait été proposée
le 2026-11-26 en amont (ADR 0003, non adoptée), avec « pas d'ouverture sur Render » en
attendant. Décision de Jo du 2026-11-27, « Ouvrir Render maintenant » : la 1.5.4 garde
l'URL `droit-francais-pont.onrender.com` et l'Action Auth0 est ouverte sur le tenant
actuel ; cette migration est reportée. Si elle a lieu, l'URL du plugin changera et un
nouveau cycle de mesure sera nécessaire.

## Points ouverts pour Jo

- **Action Auth0 du pont** : l'ouvrir à tout compte à e-mail vérifié (hors de ce dépôt) ;
  l'API historique reste réservée au mainteneur.
- **Clés PISTE** : déjà enregistrées dans le compte du mainteneur sur le pont (parcours
  validé le 2026-11-26, web et mobile, selon le journal amont).
- **Client Auth0 du plugin** : `tpc_gCoyj4qPSuyrg1ZZWDyp4D` n'est pas le client du
  connecteur claude.ai. Il doit être admis sur l'API du pont (accès délégué par
  l'utilisateur pour les applications tierces), et l'URI de rappel Antigravity doit
  rester admise.
- **Budget** : campagne 18 cas (36 sessions) et smoke (2 sessions), à autoriser après
  pré-vol.
- **Gel du serveur** : le commit déployé du pont doit figurer dans la provenance de la
  campagne ; les fusions sont gelées pendant la mesure.
- **Poussée, fusion et publication** restent des décisions de Jo.
