# ADR 0033 — Référence autonome DCP 0.1.7 (DCP-017)

Date : 8 novembre 2026. Décisions de Jo transmises par Claude : « 1.5.1 complète
(Recommandé) », puis « Go » pour l'étape 3 (re-pin du plugin).
Statut : intégration locale ; campagne du plugin 1.5.1 non exécutée.

Cette décision additive supersède la référence active DCP-014 de l'ADR 0016 et
le pin DCP de l'ADR 0030. Ces décisions et leurs preuves historiques restent
conservées. Aucun résultat plugin antérieur ne mesure les nouveaux octets.

## Motif

La réserve R6 de la relecture humaine de la 1.5.0 (cas
`plugin-dcp-acte-irreversible`) plaçait le contrôle de légalité après la
notification. Elle est corrigée en amont dans DCP-fpt 0.1.7 (PR 15), qui intègre
aussi la veille 0.1.6. Le runtime change : la référence DCP-014 ne couvre plus
ces octets, et une nouvelle mesure autonome était requise (ADR 0029).

## Mesure et pin

DCP-fpt 0.1.7 a été mesuré au commit `5debffd54a6d76e86c79ab261446f9123e564494`
(tentative `dcp-017-20261108-b`, 25/28, huit critiques réussis), puis relu par
Jo (non praticien) : 25 conformes et trois réserves sur la frontière
dirfi-fpt (cas-06, cas-08, cas-18). Les preuves publiques sont fusionnées dans
DCP-fpt (PR 16) au commit `f3be71f4d8feb7e00faabb69786d3b14c7280908`.

Comme pour DCP-014, le pin est le commit de preuve : `f3be71f`. Le commit mesuré
est consigné à part (`source_measured_commit`). Entre les deux, aucun fichier
runtime ne change ; les 30 fichiers mesurés sont égaux aux copies embarquées.
Les textes EUPL 1.2 sont déjà présents à ce commit : aucune exception de
licence (`distributed_upstream_commit`) n'est nécessaire.

## Référence DCP-017, même mécanisme fermé

La pièce `tests/evidence/2026-11-08-dcp-017/dcp-autonome.json` référence
`tests/runs/codex-web-v0.1.7-dcp-017-20261108-b` au pin ci-dessus. Synthèse,
avis daté, provenance et statut hors runtime sont copiés depuis les blobs Git
publics, avec leurs empreintes ; aucun n'est en CRLF, donc aucun gzip.
`scripts/dcp-protocol.json` épingle le pin, le fichier de preuve et la synthèse
sérialisée par SHA-256. `dcp_reference.py` et `check_dcp_protocol.py` ne
changent que la décision reconnue, désormais DCP-017 : vérifications,
sélection (LICENSE et LICENCE.fr.txt seuls hors mesure), seuils et refus des
liens redirigés sont inchangés. Aucune tolérance ni exclusion ajoutée.

DCP-014 et son pin `7874c62` sont refusés pour le candidat courant. Son contrat
est conservé dans `scripts/dcp-protocol-0014.json`. Sa batterie de mutations
reste exercée sur son runtime 0.1.4 exact, restauré depuis le dernier commit où
il était actif (`601157d`). La même batterie s'applique à DCP-017.

Les champs `human_legal_validation` et `publication_ready` restent faux ; le
scope est inchangé. La relecture autonome de Jo ne vaut ni relecture des cas du
plugin, ni validation du smoke, ni relecture praticien.

## Suite

La frontière dirfi-fpt reste à corriger en amont dans une version ultérieure ;
elle n'est pas modifiée localement (DCP reste une copie exacte, sans surcharge).
Le cycle 1.5.1 (contrat v4 lié, ADR 0031) et sa campagne restent à préparer et à
autoriser séparément.
