# ADR 0020 — Contrat v2 dans le qualificateur de distribution

Date : 20 octobre 2026. Décision de Jo, T43-L33 : « Aligner sur le v2 ».

Cette décision additive étend les ADR 0017, 0018 et 0019. La campagne
`campagne-l24-20261020-d`, mesurée au commit
`13b4e1e537e5a8097a004ee913abcc9d079114a7`, utilise le contrat v2 de SHA-256
`65593a1c46bd31b403c5b83344f14951cbc3455f456eefcde2c6853fa68a9478`.
Ce contrat ajoute notamment `stop_first:true` aux trois cas APJA, égalité DCP
et acte irréversible DCP. Le refus L32 provenait de la comparaison de leurs
empreintes v2 aux scénarios historiques de `tests/cas-plugin.json`.

Le qualificateur lit le commit mesuré dans l'index source lié par SHA-256
depuis `review.linked_sources`. `cli_toolchains.measurement_contract` choisit
le contrat par ce commit exact. La pièce de contrat liée depuis cet index
doit avoir l'empreinte épinglée ; un lien absent ou altéré pour d est refusé.
Ni `measurement_commit`, ni une version ou un chemin proposés dans la preuve
de release ne choisissent le contrat. Sans lien vers d, le contrôle v1 reste
inchangé. Le contrat copié dans le bundle source permet la même vérification
dans la sortie de staging, sans modifier l'assembleur.

La liste fermée de transition ajoute uniquement
`scripts/qualify_distribution.py`. Le manifeste existant
`scripts/toolchain-transition-0017.json` lie son empreinte source lue dans
l'objet Git du commit mesuré et son empreinte cible exacte. Les empreintes
cibles du lecteur de transition et du CHANGELOG sont renouvelées. Aucun
autre chemin permis, modification des sources liées ou tolérance d'empreinte
n'est ajouté. Une dérive ultérieure du qualificateur est refusée.

Les contre-tests distinguent le contrat v2 lié, son altération, le refus de
la même projection contre v1 et la conservation de v1 sans lien vers d.
Ce sont des contrôles logiciels sur fixtures explicitement synthétiques,
pas une nouvelle campagne. L'assembleur, le smoke, STOP, les autres contrôles
du qualificateur, les seuils et la CI restent inchangés. Le succès de
l'assemblage complet, de la qualification et des tests reste nécessaire
avant tout commit des pièces de release. Aucun appel modèle ni push autorisé.
