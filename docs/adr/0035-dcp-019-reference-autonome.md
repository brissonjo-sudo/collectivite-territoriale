# ADR 0035 — Référence autonome DCP 0.1.9 (DCP-019)

Date : 11 novembre 2026. Décisions de Jo transmises par Claude : « Recommandations
validées » (avis sur la mesure DCP-019), « Merge ok » (PR 21 de DCP-fpt), puis
« Repin ok » pour le re-pin du plugin.
Statut : intégration locale ; campagne et smoke du plugin non exécutés.

Cette décision additive supersède la référence active DCP-017 de l'ADR 0033. Ces
décisions et leurs preuves historiques restent conservées. Aucun résultat plugin
antérieur ne mesure les nouveaux octets.

## Motif

La relecture de Jo sur DCP-018 (0.1.8) avait relevé trois réserves (cas-03, cas-06,
cas-18), corrigées en amont dans DCP-fpt 0.1.9 : STOP égalité adapté aux faits,
bloc BASCULE dirfi-fpt recopié sans développement, échec de lecture décrit tel que
la trace le montre. Seul `SKILL.md` change entre 0.1.7 et 0.1.9. Le runtime change :
la référence DCP-017 ne couvre plus ces octets, et une nouvelle mesure autonome
était requise (ADR 0029).

## Mesure et pin

DCP-fpt 0.1.9 a été mesuré au commit `e9e32a592af83b8a70033b412050be955b6073ab`
(tentative `dcp-019-20261111-a`, 28/28, huit critiques réussis, six contrôles STOP
réussis), puis relu par Jo (non praticien) : 25 conformes et trois réserves de
formulation (cas-07, cas-12, cas-18). Les preuves publiques sont fusionnées dans
DCP-fpt (PR 21) au commit `8b105490592185fc3b96373ba277da8b0f323c67`.

Comme pour DCP-014 et DCP-017, le pin est le commit de preuve : `8b10549`. Le commit
mesuré est consigné à part (`source_measured_commit`). Entre les deux, aucun fichier
runtime ne change ; les 30 fichiers mesurés sont égaux aux copies embarquées
(`SKILL.md` : SHA-256 `91719ec1…`, 343 lignes). Les textes EUPL 1.2 sont déjà présents
à ce commit : aucune exception de licence n'est nécessaire.

## Référence DCP-019, même mécanisme fermé

La pièce `tests/evidence/2026-11-11-dcp-019/dcp-autonome.json` référence
`tests/runs/codex-web-v0.1.9-dcp-019-20261111-a` au pin ci-dessus. Synthèse, avis
daté, provenance et statut hors runtime sont copiés depuis les blobs Git publics,
avec leurs empreintes ; aucun n'est en CRLF, donc aucun gzip.
`scripts/dcp-protocol.json` épingle le pin, le fichier de preuve et la synthèse
sérialisée par SHA-256. `dcp_reference.py` et `check_dcp_protocol.py` ne changent
que la décision reconnue, désormais DCP-019 : vérifications, sélection (LICENSE et
LICENCE.fr.txt seuls hors mesure), seuils et refus des liens redirigés sont
inchangés. Les quatre empreintes de sources du contrat (`eval_suite`,
`mesure_locale`, cas de test, barème) sont identiques à celles de 0.1.9. Aucune
tolérance ni exclusion ajoutée.

DCP-017 et son pin `f3be71f` sont refusés pour le candidat courant. Son contrat est
conservé dans `scripts/dcp-protocol-0017.json`. Sa batterie de mutations reste
exercée sur son runtime 0.1.7 exact, restauré depuis le dernier commit où il était
actif (`b2d6f68`). Il en va de même pour DCP-014 (`601157d`). La même batterie
s'applique à DCP-019.

Les champs `human_legal_validation` et `publication_ready` restent faux ; le scope
est inchangé. La relecture autonome de Jo ne vaut ni relecture des cas du plugin, ni
validation du smoke, ni relecture praticien.

## Conséquences et suite

- L'entrée DCP passe de 322 à 343 lignes : les tests de lecture installée
  (`test_smoke_eof*`) suivent, et les sondes de fin de fichier passent de l'offset 340
  à 425. Le harnais externe de campagne et de smoke devra être réarmé sur ce nombre.
- Les pièces de la 1.5.1 (`tests/evidence/mesure-courante/`, `release-1.5.1.json`)
  restent liées à DCP 0.1.7 et ne sont pas modifiées. Deux tests échouent tant que le
  prochain cycle ne les remplace pas : `test_preuve_courante_correspond_au_runtime` et
  `test_barriere_de_release_comportementale`.
- Réserves de Jo à porter dans une version ultérieure de DCP-fpt, pas avant la
  prochaine qualification du plugin : délai décisif lu mais non indiqué (cas-07), STOP
  égalité trop affirmatif (cas-12), voies d'exécution non distinguées (cas-18).
- Le cycle suivant du plugin (contrat v4 lié, ADR 0031), sa campagne et son smoke
  restent à préparer et à autoriser séparément. Les cas du plugin touchant DCP
  (`plugin-dcp-egalite`, `plugin-dcp-frontieres-finance-donnees`, `l8-*`) ne sont
  compatibles avec 0.1.9 que par lecture : seule la campagne le confirmera.
