# ADR 0021 — Projection publique et tests isolés

Date : 20 octobre 2026. Décision de Jo, T43-L35 : « Projection publique + tests ».

Les trois assertions d'absence de release identifiées en L34 portent désormais
sur leurs dossiers temporaires. Leur résultat attendu et les refus sans smoke
restent identiques ; aucune assertion n'est supprimée et la barrière reste active.

`public_projection.py` porte une règle fixe versionnée, sans configuration
appelante : remplacement des préfixes absolus home et installation par
`<HOME>` et `<INSTALL>`, hachage SHA-256 des identifiants explicites de thread,
session ou conversation, y compris leurs occurrences dans les textes. Aucun
autre octet textuel n'est changé : pas de normalisation JSON, d'avis, de réponse,
de jugement, de verdict, d'usage ou de fin de ligne. Les contenus gzip sont lus
avec une borne ; inchangés si aucune substitution, sinon recompressés de façon
déterministe après les seules substitutions. Un secret résiduel est refusé,
jamais effacé pour obtenir un succès.

L'assembleur conserve sa sortie brute dans un dossier frère `-originaux`, hors
du candidat. Il contrôle d'abord toutes les entrées et la qualification privée,
puis produit la seule sortie publique. Les sources originelles ne sont jamais
écrites. `projection-publique.json` contient, pour chaque pièce, les empreintes
et tailles originales et publiques et le graphe des références par empreinte.
Les empreintes inscrites dans les avis restent celles de la fiche et du résumé
originaux ; la table les relie aux projections correspondantes sans réécrire
l'avis. Les champs techniques d'intégrité des originaux gardent leur sens.
Le lecteur traduit les liens source par cette table après contrôle des octets
publics ; il ne compare pas une projection au hash brut de l'original.

La vérification locale exige tous les originaux, recalcule la règle depuis eux
et compare chaque octet public. Son résultat, lié à la table et à la politique,
est lui-même lié par SHA-256 dans la release. La CI ne requiert aucun original :
elle contrôle l'inventaire exhaustif, les empreintes publiques, le graphe,
l'attestation locale liée, et refuse tout home, chemin d'installation, UUID
résiduel, identifiant de session non haché ou motif de secret reconnu. La release
est l'enveloppe de ces liens, pas une pièce incluse récursivement dans sa propre
table. Table et attestation sont de nouvelles métadonnées, pas des avis humains.

Les empreintes établissent l'intégrité de la chaîne, pas une signature externe
du résultat local. La CI ne peut re-dériver des octets privés qu'elle ne possède
pas ; cette opération reste explicitement locale. La détection de secrets
repose sur des motifs versionnés et des champs de credentials, sans prétendre
identifier toute chaîne arbitraire inconnue comme secret. Les formats opaques
dans les pièces sont refusés ; aucun fichier n'est exclu silencieusement.

La transition ADR 0017/0018/0019/0020 ajoute uniquement le nouveau module
`scripts/public_projection.py` (source absente au commit mesuré, cible exacte).
Les cibles exactes de l'assembleur, du qualificateur, du lecteur et du CHANGELOG
sont renouvelées ; toute autre dérive reste refusée. Runtime, configuration,
scénarios, STOP, seuils, campagne d et avis de Jo ne sont pas modifiés.

Le diagnostic est jetable et non probant (`release_evidence:false`). Seules
les liaisons du smoke ancien sont simulées ; aucun résultat n'est transféré au
nouveau candidat. La préparation d'une nouvelle tentative dépend de ce résultat.
Aucune installation, connexion, session modèle, poussée ou autorisation de Jo
n'est acquise par cette ADR.

## Addendum du 20 octobre 2026 — T43-L36

Arbitrage transmis par Claude : « pas de gzip », et mécanisme Git standard
`-whitespace` limité aux pièces approuvées par empreinte. La fiche projetée
`tests/evidence/mesure-courante/source-l14/FICHE-RELECTURE-17-D.md` conserve
ses octets, y compris les espaces de la fiche humaine originale. Aucune
normalisation ni compression supplémentaire n'est appliquée. Son seul chemin
exact reçoit cet attribut ; `git diff --check` continue à contrôler tous les
autres chemins, notamment le code et la documentation.

La transition fermée ADR 0017 ajoute `.gitattributes`, avec empreinte source
issue de l'objet Git du commit mesuré et empreinte cible exacte du fichier.
Comme pour le CHANGELOG, cette vérification explicite couvre un fichier hors
inventaire Python/JSON d'outillage. La cible de `cli_toolchains.py` est renouvelée
uniquement pour cette extension. Toute autre modification du fichier, de sa
portée ou de la transition demeure refusée.

L'intégration jetable vérifie l'identité des octets de travail et d'index ainsi
que le maintien du refus d'espaces finaux dans le code et la documentation.
Le diagnostic complet reste non probant ; seul le rattachement du smoke L30c
à la nouvelle tête y est simulé. La préparation finale de L35d ne vaut toujours
pas autorisation de Jo pour Install ou Run ; Claude doit la demander.
