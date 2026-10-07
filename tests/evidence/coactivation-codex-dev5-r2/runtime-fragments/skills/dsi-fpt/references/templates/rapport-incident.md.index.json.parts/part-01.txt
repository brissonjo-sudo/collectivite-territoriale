# Gabarit interactif — Rapport d'incident (v0.2.0)

> **Usage** : documenter un incident en cours, sa reprise ou sa clôture.
> **Statut du produit** : rapport factuel évolutif ; clôture et absence de données touchées jamais présumées.

## Préalables impératifs

Lire `../analyse-situation.md`. Pour un incident en cours ou récent, afficher
intégralement le garde-fou incident du SKILL §5.2 **comme premier livrable,
avant toute aide métier**. Si la demande vise des contenus ou traces de
personnes, afficher aussi le garde-fou surveillance §5.3 avant technique.
`BASCULE dpo-ct` dès que des données personnelles peuvent être concernées ;
arrêter qualification, notification et information des personnes. Effectuer
les autres bascules de frontière si déclenchées, sans les illustrer.

Lire `../ecrits-numerique.md`, `../crise-cyber-continuite.md`,
`../securite-si.md` et `../retex.md`. Poser les questions **une par une**,
attendre chaque réponse et exploiter les informations déjà données. Ne jamais
demander des journaux bruts, des captures nominatives, des secrets ou un détail
d'architecture réelle ; les preuves restent dans le circuit sécurisé compétent.

## Questions à poser dans l'ordre

1. Le rapport décrit-il un incident encore actif, une reprise ou une clôture à instruire ?
2. Quels faits anonymisés sont établis, et quelles inconnues subsistent ?
3. Quel est le mode d'exercice de la fonction SI et quels rôles pilotent l'incident ?
4. Quels repères chronologiques sont confirmés, avec leur origine ?
5. Quels services sont affectés et quels impacts sont effectivement constatés ?
6. Des données personnelles peuvent-elles être concernées, ou cela reste-t-il inconnu ?
7. Quelles mesures ont réellement été prises, par quels rôles, et quelles preuves ont été préservées ?
8. Quelles décisions et quels signalements ont été effectués dans les circuits prévus ?
9. Quelles conditions et preuves de reprise ont été validées, par quel rôle ?
10. Quelles réserves, actions et conditions de clôture restent ouvertes ?

Si une réponse révèle un garde-fou ou une frontière, appliquer le bloc avant
de poursuivre la rédaction. Ne pas présenter une hypothèse de cause comme un fait.

## Trame d'assemblage

```text
[INCOMPLET] Rapport d'incident — [intitulé anonymisé]
État du rapport : [incident actif / reprise / clôture à instruire]
Mode d'exercice et rôles : [à renseigner]
Périmètre connu et impacts constatés : [à renseigner]
Chronologie : [repère confirmé / fait / origine / rôle]
Faits établis : [à renseigner]
Hypothèses et inconnues : [à renseigner]
Données personnelles possiblement concernées : [état factuel / BASCULE dpo-ct]
Mesures réellement prises : [à renseigner, sans mode opératoire offensif]
Preuves préservées : [références anonymisées, sans contenu brut]
Décisions : [objet / rôle décisionnaire / confirmation]
Signalements : [circuit / état factuel / source si obligation invoquée]
Reprise : [critères / preuves / validation communiquée / réserves]
Clôture : [décision communiquée, ou non établie]
Actions restant ouvertes : [action / rôle / échéance confirmée ou à définir]
Sources mobilisées et dates de consultation : [à renseigner]
Champs manquants : [liste explicite]
```

## Vérification avant livraison

Conserver `[INCOMPLET]` si un élément nécessaire manque. Un statut « inconnu »
ne devient pas « aucune donnée touchée » ; une restauration ne vaut pas preuve
d'absence de compromission. Vérifier obligations et délais selon
`../socle-sources-verification.md` et `../references-verifiees.md`.
Identifier les décisions de l'exécutif et citer les chemins de branches au
point d'usage. Préparer le RETEX selon `../retex.md`, sans cas identifiable.
