# ADR 0012 — DCP-0 : référencer la mesure autonome au pin inchangé

Date : 2026-10-18. Décision de l'orchestrateur sur L9 ; application locale L10.
Statut : accepté pour l'outillage ; candidat 1.3.0 non mesuré, non qualifié.

## Décision et portée

DCP-0 remplace, pour cette préparation, l'exigence d'une nouvelle campagne DCP
et le couple répondant Codex / juge Claude envisagé en L9. DCP-A et DCP-B ne
sont pas retenues. Aucun juge Claude n'est désormais requis. Le protocole amont,
ses seuils et ses limites restent inchangés ; aucun bridge natif R5 n'est raccordé.

La pièce `tests/evidence/2026-10-08-candidat-013/dcp-autonome.json` référence la
mesure du **skill autonome**, publiée dans DCP-fpt au commit
`ff35b7af38f2e03bf39a1244ebdae292b53daccd`, pour le runtime
`129f374e6ab8ea3b47bcfd9de9ddd52a2d3d9498`. Ce pin et ses octets embarqués
sont inchangés. Cela ne transfère aucune mesure d'un runtime plugin antérieur.
Les dix-huit cas plugin, leur relecture séparée et les deux sessions de smoke
doivent toujours être produits pour le commit exact du nouveau candidat.

## Conditions fermées d'acceptation

- Le pin de la preuve doit être celui de `upstream.json` et du contrat DCP-0.
- Les 30 entrées de `summary.runtime_sha256` doivent correspondre octet pour
  octet aux fichiers de `skills/dcp-fpt/`. Le seul fichier embarqué supplémentaire
  admis est `LICENSE`, fichier de distribution absent du runtime mesuré. Aucun
  autre manque, ajout ou écart inexpliqué n'est permis ; aucune surcharge DCP
  n'est admise implicitement.
- La synthèse sérialisée en UTF-8 (`ensure_ascii=False`, indentation 2, LF final)
  doit avoir l'empreinte `source_summary_sha256` attendue :
  `37c9f6ca8f66eb60c9840ec03f62b618840067d7287404ae633787cc2388d4a6`.
- Le fichier de preuve entier doit avoir l'empreinte SHA-256
  `9b23cd811ee4aef6cebfae129e6baa006f7269b76d623f7e7fc6a994dff61375`.
  Ces empreintes sont versionnées dans `scripts/dcp-protocol.json`, sans option
  CLI de remplacement. La provenance publique et les conditions de seuil de la
  synthèse autorisée sont également vérifiées.

## Réserves conservées

L'assembleur copie cette pièce à l'identique, vérifie aussi la copie et n'ajoute
aucun `plugin_commit` à la mesure autonome. Son `scope` reste exactement :
« Seuil automatique de mesure ; relecture juridique et provenance distinctes. »
La note reste « Relecture praticien et validation du plugin à établir séparément. »
Ses deux indicateurs `publication_ready` et `human_legal_validation` restent faux.
La mesure n'est pas revendiquée comme relue par un praticien.

L'ADR 0007 et la séparation validate/release demeurent. Aucune preuve plugin
n'est fabriquée, aucune ancienne preuve plugin n'est transférée, aucun seuil,
saut ou filtre de CI n'est ajouté. L'assembleur conserve la revue humaine à
`false` ; le qualificateur inchangé refuse une preuve absente ou d'un autre
runtime. L'interdiction de transférer gels, caches et scores plugin des ADR 0010
et 0011 reste entière.

## Autorisations encore nécessaires

Jo doit autoriser les appels Codex et leur budget (18 réponses + 18 relectures),
l'installation isolée et les deux sessions de smoke, la transmission des prompts,
et, si nécessaire, l'authentification MCP/OAuth séparée. La relecture humaine,
une éventuelle publication des commits sur #17 et toute campagne restent des
actions distinctes. Aucun appel ni installation n'est exécuté dans L10.
