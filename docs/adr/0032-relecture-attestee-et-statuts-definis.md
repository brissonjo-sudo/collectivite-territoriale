# ADR 0032 : relecture attestée et statuts définis

Date : 2026-11-07. Décision de Jo, après l'audit du candidat 87b6dac et
l'arrêt de la tentative i. Aucun modèle, aucune poussée, aucune fusion ni
aucune preuve dans ce lot. Cette décision complète l'ADR 0031 sans la
réécrire : le contrat de cycle v4 et le pin `CAMPAIGN_150_CLI` restent ceux
qu'elle fixe.

## Contexte

Les tentatives a à i de la mesure 1.5.0 ont été arrêtées sans campagne
complète. L'audit a relevé, côté relecture, des statuts appliqués sans
définition écrite et des invariants que le code du harnais vérifie déjà
(STOP, séquence d'activation, appels MCP et web, chemins de skill) mais que
le modèle relecteur pouvait abaisser. Côté candidat, il a relevé des
contradictions entre l'amont de dsi-fpt et sa surcouche, et trois règles
présentes dans la seule surcouche dsi-fpt.

## Décision de Jo du 2026-11-07

1. **Statuts du relecteur définis par écrit** dans la consigne du harnais :
   `respecte`, `violation`, `non_verifiable`, avec la règle des invariants
   composés (pire statut des parties, partie en cause nommée).
2. **Invariants mécaniques non abaissables.** Ce que le code du harnais a
   vérifié sur la trace complète reçoit le statut `respecte`, quel que soit
   l'avis du modèle, dont la trace est conservée. Familles exactes :
   - STOP premier texte (cas `stop_first`, invariant commençant par
     « STOP est le premier texte visible ») ;
   - séquence d'activation (cas à `activation_sequence` non vide, invariant
     commençant par « Activation de » ou « Trace d'activation de ») ;
   - absence d'appel MCP ou web (cas `mcp_mode` ou `web_mode` désactivé),
     fournie au relecteur comme fait attesté ;
   - absence de lien ou de chemin de skill (`V4_PATH_INVARIANT`).
3. **Champ `mechanical_attestations`** dans chaque session de relecture : la
   liste des relèvements appliqués, chacun `{invariant, model_statut,
   model_motif}` ; liste vide si aucun.
4. **Invariants et fichier de cas inchangés** :
   `scripts/cas-plugin-cycle-v4.json` garde son empreinte
   `be70f64b4650a72c15a33e477c81f84c61c602ceb22ad23cc1783c3412888f24`. Aucun
   nouveau contrat de cycle, aucune nouvelle version de `cas-plugin-cycle`.
5. **Sonde amont et garde de fenêtre côté harnais** : un appel Légifrance réel
   et une fenêtre d'usage suffisante sont exigés avant tout rôle ; leur reçu
   figure dans `run-campagne.status` (`upstream_probe`, `usage_window`).
6. **Harnais versionné** : commit `c1c3315` du dépôt local du harnais.

## Adaptations du dépôt

- `scripts/human_resolution.py` : `load_bundle` comparait le rapport retenu au
  dernier texte tracé du relecteur ; un relèvement mécanique le faisait donc
  refuser. `traced_report` vérifie chaque attestation (famille mécanique du
  cas, schéma exact, statut retenu `respecte`, motif retenu dérivé du motif du
  modèle, aucun doublon), l'annule, puis exige l'égalité avec le texte tracé.
  Le champ est conservé dans la relecture projetée ; une attestation non
  conforme est refusée, jamais ignorée.
- `run-campagne.status` n'est lu par aucun script du dépôt : `upstream_probe`
  et `usage_window` n'y rencontrent aucun refus.
- `assemble_release_evidence.py` et `qualify_distribution.py` ne fixent pas
  l'ensemble des clés d'une relecture : le champ y est accepté et conservé.
- Outillage du même lot : rechaînage des surcouches
  (`scripts/rehash_overlays.py`), plusieurs `replace-block` par skill (une fois
  par section), projection publique étendue aux chemins absolus quelconques,
  e-mails et IPv4 (politique historique gardée pour les seules 1.3.0 et
  1.4.0), timeout tolérant une dernière ligne coupée (`truncated_tail`). Cette
  ADR remplace, pour `measurement_common.py` et `public_projection.py`, la
  mention « ne changent pas » de l'ADR 0031.
- Quatrième correction de comportement (voir `CHANGELOG.md`) : dsi-fpt sans
  contradiction amont ; trois règles portées dans les cinq autres surcouches.
  dcp-fpt reste sans surcouche : ses octets sont liés à la mesure DCP-014
  (ADR 0029) et une surcouche invaliderait cette référence.

## Conséquences

- **Nouvelle série de tentatives** sur un nouveau candidat H1 ; aucun résultat
  des tentatives a à i n'est repris.
- **Comparaison avec a à i perdue** : consigne de relecture, statuts et
  candidat changent ensemble ; un écart de résultat ne se rapporte à aucun
  d'eux isolément.
- Transition H1 vers H2 inchangée (ADR 0031) : après H1, tout fichier de
  `scripts/`, des tests ou de la documentation modifié invalide la mesure.
