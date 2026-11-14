# Décisions d'architecture (ADR)

Index des ADR du plugin, par numéro. Un ADR accepté n'est jamais réécrit : une décision nouvelle prend un nouveau numéro et cite celle qu'elle remplace.

## Numéros en double

Deux numéros ont été attribués deux fois le même jour, avant cet index. Les fichiers ne sont pas renommés, pour ne casser aucun lien ni aucune pièce liée par empreinte. Chaque décision s'identifie par son chemin complet, comme le prévoit `0012-resolution-humaine-liee.md`.

- **0005**
  - `0005-campagne-codex-native.md` : profil natif Codex. C'est celui que citent `CHANGELOG.md` (qualification candidate du 2026-10-07) et `docs/qualification-dcp-2026-10-07.md`.
  - `0005-reserves-dcp-dpo.md` : réserves DCP 0.1.2 et contrôle humain DPO.
- **0012**
  - `0012-reference-mesure-dcp-autonome.md` : DCP-0, mesure autonome au pin inchangé. C'est celui que citent `docs/mesure-candidat-1-3-0.md` et l'ADR 0016.
  - `0012-resolution-humaine-liee.md` : résolution humaine des invariants `non_verifiable`. C'est celui que citent l'ADR 0013, les fiches de relecture et les avis humains des campagnes.

Le prochain ADR prend le numéro qui suit le plus grand de la liste.

## Liste

| N° | Fichier | Objet |
|---|---|---|
| 0001 | [`0001-integration-recherche-juridique.md`](0001-integration-recherche-juridique.md) | Embarquer `recherche-juridique` dans le plugin territorial |
| 0002 | [`0002-surcharges-instructions-locales.md`](0002-surcharges-instructions-locales.md) | Corrections d'instructions locales et reproductibles |
| 0003 | [`0003-integration-candidate-dcp.md`](0003-integration-candidate-dcp.md) | Intégration candidate de la commande publique |
| 0004 | [`0004-distribution-epinglee.md`](0004-distribution-epinglee.md) | Distribution épinglée sur une étiquette publiée |
| 0005 | [`0005-campagne-codex-native.md`](0005-campagne-codex-native.md) | Exécuter la coactivation candidate sur Codex |
| 0005 | [`0005-reserves-dcp-dpo.md`](0005-reserves-dcp-dpo.md) | Traiter les réserves DCP et DPO |
| 0006 | [`0006-protocole-lectures-codex.md`](0006-protocole-lectures-codex.md) | Protocole de lecture explicite |
| 0007 | [`0007-distribution-open-source-et-deploiement.md`](0007-distribution-open-source-et-deploiement.md) | Distribution open source et déploiement opérationnel |
| 0008 | [`0008-ponytail-developpement-verifie.md`](0008-ponytail-developpement-verifie.md) | Ponytail local avec vérification avant utilisation |
| 0009 | [`0009-reprise-selective-dsi-et-sources.md`](0009-reprise-selective-dsi-et-sources.md) | Reprise sélective DSI depuis main |
| 0010 | [`0010-contrat-candidat-1-3-0.md`](0010-contrat-candidat-1-3-0.md) | Contrat du candidat 1.3.0 |
| 0011 | [`0011-reprise-r5-portable.md`](0011-reprise-r5-portable.md) | Récupération publique et contrôles portables de R5 |
| 0012 | [`0012-reference-mesure-dcp-autonome.md`](0012-reference-mesure-dcp-autonome.md) | DCP-0 : référencer la mesure autonome au pin inchangé |
| 0012 | [`0012-resolution-humaine-liee.md`](0012-resolution-humaine-liee.md) | Résolution humaine liée des invariants non vérifiables |
| 0013 | [`0013-cli-distinct-smoke.md`](0013-cli-distinct-smoke.md) | CLI distinct pour le smoke installé |
| 0014 | [`0014-acl-plugin-smoke.md`](0014-acl-plugin-smoke.md) | Lecture du seul plugin installé par le sandbox Windows |
| 0015 | [`0015-diagnostic-refus-lecture-smoke.md`](0015-diagnostic-refus-lecture-smoke.md) | Diagnostic public des refus de lecture du smoke |
| 0016 | [`0016-dcp-014-et-nouveau-cycle.md`](0016-dcp-014-et-nouveau-cycle.md) | Référence autonome DCP 0.1.4 et nouveau cycle |
| 0017 | [`0017-assemblage-campagne-d.md`](0017-assemblage-campagne-d.md) | Contrat exact d'assemblage de la campagne d |
| 0018 | [`0018-consigne-lecture-smoke.md`](0018-consigne-lecture-smoke.md) | Consigne de lecture unique avant le smoke |
| 0019 | [`0019-fin-lecture-smoke.md`](0019-fin-lecture-smoke.md) | Fin de fichier déterministe pour les lectures du smoke |
| 0020 | [`0020-qualification-contrat-v2.md`](0020-qualification-contrat-v2.md) | Contrat v2 dans le qualificateur de distribution |
| 0021 | [`0021-projection-publique-et-tests.md`](0021-projection-publique-et-tests.md) | Projection publique et tests isolés |
| 0022 | [`0022-sondes-fin-fichier-smoke.md`](0022-sondes-fin-fichier-smoke.md) | Distinguer contenu et sonde de fin de fichier du smoke |
| 0023 | [`0023-lecture-entrees-smoke-jusqua-fin.md`](0023-lecture-entrees-smoke-jusqua-fin.md) | Poursuivre la lecture des entrées sélectionnées jusqu'à leur fin |
| 0024 | [`0024-qualificateur-distribution-et-smoke.md`](0024-qualificateur-distribution-et-smoke.md) | Lier la distribution à l'outillage et aux CLI du smoke |
| 0025 | [`0025-contrat-cycle-v3.md`](0025-contrat-cycle-v3.md) | Contrat de cycle v3 pour la mesure 1.4.0 |
| 0026 | [`0026-transition-fermee-1-4-0.md`](0026-transition-fermee-1-4-0.md) | Transition fermée de liaison 1.4.0 |
| 0027 | [`0027-lecture-sequentielle-entrees-et-tentative-b.md`](0027-lecture-sequentielle-entrees-et-tentative-b.md) | Lecture séquentielle des entrées et nouvelle tentative 1.4.0 |
| 0028 | [`0028-contrat-v4-et-tentative-d.md`](0028-contrat-v4-et-tentative-d.md) | Contrat v4, surcharge DCP et tentative d |
| 0029 | [`0029-retrait-surcharge-dcp-et-reserve-0-1-5.md`](0029-retrait-surcharge-dcp-et-reserve-0-1-5.md) | Retrait de la surcharge DCP et réserve 0.1.5 |
| 0030 | [`0030-adoption-eupl-1-2.md`](0030-adoption-eupl-1-2.md) | Adoption de l'EUPL 1.2 |
| 0031 | [`0031-mesure-1-5-0-contrat-v4.md`](0031-mesure-1-5-0-contrat-v4.md) | Mesure 1.5.0 sous contrat v4 et nouveau pin de CLI |
| 0032 | [`0032-relecture-attestee-et-statuts-definis.md`](0032-relecture-attestee-et-statuts-definis.md) | Relecture attestée et statuts définis |
| 0033 | [`0033-dcp-017-reference-autonome.md`](0033-dcp-017-reference-autonome.md) | Référence autonome DCP 0.1.7 (DCP-017) |
| 0034 | [`0034-mesure-1-5-1-contrat-v4.md`](0034-mesure-1-5-1-contrat-v4.md) | Mesure 1.5.1 sous contrat v4, même CLI que la 1.5.0 |
| 0035 | [`0035-dcp-019-reference-autonome.md`](0035-dcp-019-reference-autonome.md) | Référence autonome DCP 0.1.9 (DCP-019) |
| 0036 | [`0036-mesure-1-5-2-contrat-v4.md`](0036-mesure-1-5-2-contrat-v4.md) | Mesure 1.5.2 sous contrat v4, même CLI que la 1.5.0 |
