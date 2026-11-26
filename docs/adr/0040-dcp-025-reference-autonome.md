# ADR 0040 — Référence autonome DCP 0.2.2 (DCP-025)

Date : 26 novembre 2026. Décisions de Jo transmises par Claude : cycle groupé
(« Groupée », dcp-fpt + drh-fpt 0.8.0 + recherche-juridique 3.7.0), correctif
« Correctif 0.2.2 », « Autoriser la mesure » (DCP-025), avis « 15, 12, 07 », fusion
de la PR 26 de DCP-fpt, puis « go » pour la préparation du plugin.
Statut : intégration locale ; campagne et smoke du plugin non exécutés.

Cette décision additive supersède la référence active DCP-020 de l'ADR 0038. Ces
décisions et leurs preuves historiques restent conservées. Aucun résultat plugin
antérieur ne mesure les nouveaux octets.

## Motif

La tentative c de la campagne 1.5.3 a montré un STOP égalité émis à la place du STOP
acte irréversible, avant toute lecture. DCP-fpt 0.2.1 (PR 24) a placé les deux en-têtes
STOP exacts en tête de la description, chacun avec son déclencheur. Sa mesure DCP-021 a
ensuite échoué sur des références nommées après un échec de lecture (Légifrance en 403
pour les clients automatisés). DCP-fpt 0.2.2 (PR 25) impose l'abstention après échec de
lecture et réduit le bloc BASCULE dirfi-fpt sans liste illustrative. Seul `SKILL.md`
change entre 0.2.0 et 0.2.2 : la référence DCP-020 ne couvre plus ces octets (ADR 0029).

## Mesure et pin

DCP-fpt 0.2.2 a été mesuré au commit `d9da5db8165ee858b57c10f543a504861926011e`
(tentative `dcp-025-20261126-a`) : 27 RÉUSSITE, une DEMI-RÉUSSITE non critique (cas-15),
aucun ÉCHEC, huit critiques et six contrôles STOP réussis ; seuil atteint. Les tentatives
DCP-022 à DCP-024 sur la même tête, interrompues sans score complet, ne sont pas
retenues. Jo (non praticien) a relu les 28 réponses : 25 conformes et trois réserves
(cas-07, cas-12, cas-15). Les preuves publiques sont fusionnées dans DCP-fpt (PR 26) au
commit `86d9896a9e72f0e5e9a5700e813ea60034f2191f`.

Comme pour les références précédentes, le pin est le commit de preuve : `86d9896`. Le
commit mesuré est consigné à part (`source_measured_commit`). Entre les deux, aucun
fichier runtime ne change ; les 30 fichiers mesurés sont égaux aux copies embarquées
(`check_dcp_protocol` : 30 fichiers vérifiés ; `SKILL.md`, 355 lignes).

## Référence DCP-025, même mécanisme fermé

La pièce `tests/evidence/2026-11-26-dcp-025/dcp-autonome.json` référence
`tests/runs/codex-web-v0.2.2-dcp-025-20261126-a` au pin ci-dessus. Synthèse, avis daté,
provenance et statut hors runtime sont copiés depuis les blobs Git publics, avec leurs
empreintes. La pièce est produite par le même gabarit que DCP-020 : régénérée par ce
gabarit depuis `cad0259`, la preuve DCP-020 est identique à l'octet. `scripts/dcp-protocol.json`
épingle le pin, le fichier de preuve et la synthèse sérialisée par SHA-256.
`dcp_reference.py` et `check_dcp_protocol.py` ne changent que la décision reconnue,
désormais DCP-025. Les quatre empreintes de sources du contrat (`eval_suite`,
`mesure_locale`, cas de test, barème) sont identiques à 0.2.2. Aucune tolérance ni
exclusion ajoutée.

DCP-020 et son pin `cad0259` sont refusés pour le candidat courant. Son contrat est
conservé dans `scripts/dcp-protocol-0020.json` ; sa batterie de mutations reste exercée
sur son runtime 0.2.0 exact, restauré depuis le dernier commit où il était actif
(`c1659bf`, H1 abandonné de la 1.5.3). La même batterie s'applique à DCP-025.

Les champs `human_legal_validation` et `publication_ready` restent faux ; le scope est
inchangé. La relecture autonome de Jo ne vaut ni relecture des cas du plugin, ni
validation du smoke, ni relecture praticien.

## Conséquences et suite

- L'entrée DCP passe de 353 à 355 lignes : les tests de lecture installée
  (`test_smoke_eof*`) suivent ; les sondes de fin de fichier restent au-delà de la fin.
  Le harnais externe devra être réarmé sur ce nombre.
- Sur 28 réponses, une seule ouverture de page officielle a abouti : la mesure autonome
  porte surtout sur l'abstention. La campagne du plugin passe par le serveur MCP, pas par
  le site Légifrance.
- Réserves de Jo pour une version ultérieure de DCP-fpt : STOP égalité seulement sur une
  demande de faveur (cas 12), régime du paiement direct signalé comme lacune (cas 07),
  principes et interdiction du fractionnement malgré une dispense (cas 15), « texte
  intégral lu » seulement si la trace le montre (cas 09). Détail dans
  `docs/qualification-0.2.2-2026-11-26.md` de DCP-fpt.
- Le nouveau H1 de la 1.5.3 est décidé par l'[ADR 0041](0041-mesure-1-5-3-h1-groupe.md).
