# ADR 0038 — Référence autonome DCP 0.2.0 (DCP-020)

Date : 16 novembre 2026. Décisions de Jo transmises par Claude : lot unique 1.5.3
(15 novembre, phase 3 : ré-épinglage sur la preuve DCP-020), « Réussite + réserves »
puis « Oui, scelle » (avis sur la mesure DCP-020), fusion de la PR 23 de DCP-fpt,
puis « lance le pré-vol H1 1.5.3 ».
Statut : intégration locale ; campagne et smoke du plugin non exécutés.

Cette décision additive supersède la référence active DCP-019 de l'ADR 0035. Ces
décisions et leurs preuves historiques restent conservées. Aucun résultat plugin
antérieur ne mesure les nouveaux octets.

## Motif

Cinq réserves de Jo (DCP-019 cas-07, cas-12, cas-18 ; campagne 1.5.2 : favoritisme et
commission d'appel d'offres sans référence) ont été corrigées en amont dans DCP-fpt
0.2.0 (PR 22) : acte refusé nommé après le STOP égalité, référence lue ou « non
vérifié » pour chaque risque nommé par un bloc STOP, délai décisif indiqué, trois voies
face à la défaillance distinguées. `SKILL.md` et `references/resiliation-difficultes.md`
changent entre 0.1.9 et 0.2.0. Le runtime change : la référence DCP-019 ne couvre plus
ces octets, et une nouvelle mesure autonome était requise (ADR 0029).

## Mesure et pin

DCP-fpt 0.2.0 a été mesuré au commit `c810d109e043065282c3549bad5192205a8f41eb`
(tentative `dcp-020-20261116-a`) : 27 RÉUSSITE, un ÉCHEC non critique (cas-06), huit
critiques et six contrôles STOP réussis ; seuil atteint. Jo (non praticien) a relu les
28 réponses : 21 conformes et sept réserves (cas-05, cas-06, cas-07, cas-12, cas-17,
cas-18, cas-21). Le verdict du juge sur le cas 06 est conservé ; la réserve de Jo vise
le bloc BASCULE imposé par le §5.5 du skill. Les preuves publiques sont fusionnées dans
DCP-fpt (PR 23) au commit `cad02591e844d0f995b975b1dfc3e9fdc66f8cfa`.

Comme pour DCP-014, DCP-017 et DCP-019, le pin est le commit de preuve : `cad0259`. Le
commit mesuré est consigné à part (`source_measured_commit`). Entre les deux, aucun
fichier runtime ne change ; les 30 fichiers mesurés sont égaux aux copies embarquées
(`SKILL.md` : SHA-256 `4345b253…`, 353 lignes). Les textes EUPL 1.2 sont déjà présents
à ce commit : aucune exception de licence n'est nécessaire.

## Référence DCP-020, même mécanisme fermé

La pièce `tests/evidence/2026-11-16-dcp-020/dcp-autonome.json` référence
`tests/runs/codex-web-v0.2.0-dcp-020-20261116-a` au pin ci-dessus. Synthèse, avis daté,
provenance et statut hors runtime sont copiés depuis les blobs Git publics, avec leurs
empreintes ; aucun n'est en CRLF, donc aucun gzip. `scripts/dcp-protocol.json` épingle
le pin, le fichier de preuve et la synthèse sérialisée par SHA-256. `dcp_reference.py`
et `check_dcp_protocol.py` ne changent que la décision reconnue, désormais DCP-020 :
vérifications, sélection (LICENSE et LICENCE.fr.txt seuls hors mesure), seuils et refus
des liens redirigés sont inchangés. Les quatre empreintes de sources du contrat
(`eval_suite`, `mesure_locale`, cas de test, barème) sont identiques à celles de 0.2.0.
Aucune tolérance ni exclusion ajoutée.

DCP-019 et son pin `8b10549` sont refusés pour le candidat courant. Son contrat est
conservé dans `scripts/dcp-protocol-0019.json`. Sa batterie de mutations reste exercée
sur son runtime 0.1.9 exact, restauré depuis le dernier commit publié où il était actif
(`155704f`). Il en va de même pour DCP-014 (`601157d`) et DCP-017 (`b2d6f68`). La même
batterie s'applique à DCP-020.

Les champs `human_legal_validation` et `publication_ready` restent faux ; le scope est
inchangé. La relecture autonome de Jo ne vaut ni relecture des cas du plugin, ni
validation du smoke, ni relecture praticien.

## Conséquences et suite

- L'entrée DCP passe de 343 à 353 lignes : les tests de lecture installée
  (`test_smoke_eof*`) suivent ; les sondes de fin de fichier (offsets 360 et 425) restent
  au-delà de la fin. Le harnais externe de campagne et de smoke devra être réarmé sur ce
  nombre.
- Les pièces de la 1.5.2 (`tests/evidence/mesure-courante/`, `release-1.5.2.json`)
  restent liées à DCP 0.1.9 et ne sont pas modifiées. Deux tests échouent tant que le
  cycle 1.5.3 ne les remplace pas : `test_preuve_courante_correspond_au_runtime` et
  `test_barriere_de_release_comportementale`.
- Réserves de Jo à porter dans une version ultérieure de DCP-fpt, pas avant la
  qualification 1.5.3 : liste « À reprendre » du §5.5, déclenchement et point 2 du STOP
  égalité, BASCULE dirfi-fpt trop large, codes d'erreur absents de la trace, compléments
  de fond (cas 07, 17, 18, 21). Détail dans `docs/qualification-0.2.0-2026-11-16.md` de
  DCP-fpt.
- Le cycle 1.5.3 du plugin (contrat v4, ADR 0031), sa campagne et son smoke restent à
  préparer et à autoriser séparément. Les cas du plugin touchant DCP
  (`plugin-dcp-egalite`, `plugin-dcp-acte-irreversible`,
  `plugin-dcp-frontieres-finance-donnees`, `l8-*`) ne sont compatibles avec 0.2.0 que
  par lecture : seule la campagne le confirmera.
