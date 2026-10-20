# ADR 0017 — Contrat exact d'assemblage de la campagne d

Date : 20 octobre 2026. Décision de Jo, T43-L27. Préparation locale uniquement.

La mesure `campagne-l24-20261020-d` appartient au commit
`13b4e1e537e5a8097a004ee913abcc9d079114a7`. Ses originaux restent inchangés.
Le contrat CLI de cette mesure est déclaré dans `measurement-cli.json`, sous
la clé exacte de ce commit : 0.163.0-alpha.10.2, SHA-256
`f6dbf48cb70f62649c645f26c87dc9bf84cc36986202dfad8e12fb5b8ca70312`, avec les
trois compagnons exacts du verrou smoke. Le verrou historique 0.162 demeure
réservé aux preuves historiques ; il n'est jamais recevable pour d.
Le lecteur sélectionne par le commit lié de la mesure, jamais par le reçu.
Aucune plage de versions, option de contournement ou comparaison partielle.
Les deux identités de phase de l'ADR 0013 demeurent obligatoires, même identiques.

Le contrat de cas déjà utilisé par d est `scripts/cas-plugin-cycle-v2.json`,
SHA-256 `65593a1c46bd31b403c5b83344f14951cbc3455f456eefcde2c6853fa68a9478`.
Il ajoute STOP en tête aux trois cas APJA, égalité et acte irréversible.
Le lecteur du bundle d doit lier ce fichier exact ; aucune empreinte v1 n'est
acceptée comme équivalente. Les cas et skills eux-mêmes ne sont pas modifiés.

Le manifeste `toolchain-transition-0017.json` lie, pour cette seule mesure,
les empreintes sources et cibles exactes du verrou CLI, de son lecteur,
du contrôle des reçus, du lecteur humain, de l'assembleur et du CHANGELOG.
La liste de chemins est fermée dans le lecteur ; sa propre empreinte est
contrôlée dans le snapshot cible. Tout autre outillage différent est refusé.
Le CHANGELOG source est relu dans l'objet Git du commit mesuré. Runtime,
configuration, scénarios, upstream et contrôles humains demeurent vérifiés.
Cette transition est une liaison d'outillage ; elle ne fabrique aucune mesure.

Les réserves de Jo emploient le format L14 `reserve` plus `reserves` et
`decision_globale.reserve_maintenue:true`. Le commentaire du cas 1 ne transforme
pas son verdict conforme en réserve. La résolution humaine, la couverture
globale, les dates et empreintes, les refus des fixtures et la présence des
réponses exactes dans la fiche restent inchangés.

Aucun modèle, push, smoke ou release dans L27. Le smoke doit être réel, lié
à la nouvelle tête et réussi avant tout assemblage de release. Les anciens
manifestes de préparation des campagnes et smoke ne sont pas réépinglés ici.
