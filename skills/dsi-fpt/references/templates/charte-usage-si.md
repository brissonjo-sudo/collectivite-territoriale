# Gabarit interactif — Charte d'usage du SI (v0.2.0)

> **Usage** : préparer le contenu technique des règles d'usage et de sécurité.
> **Statut du produit** : brouillon technique ; adoption, opposabilité et sanctions relèvent de `drh-fpt`.

## Préalables impératifs

Lire `../analyse-situation.md` avant toute question technique. Un incident en
cours ou récent impose le garde-fou incident du SKILL §5.2 comme premier
livrable. Une demande d'accès aux contenus ou traces d'une personne, ou de
surveillance, impose l'affichage intégral du garde-fou §5.3 avant technique :
aucune commande, extraction ni paramétrage avant base et conditions établies.
Effectuer `BASCULE dpo-ct` et `BASCULE drh-fpt` sur leurs volets ; arrêter le
fond concerné. Appliquer les autres frontières si déclenchées, sans illustration.

Lire `../ecrits-numerique.md`, `../securite-si.md` et les branches pertinentes.
Poser les questions **une par une** et attendre chaque réponse ; réutiliser
les faits connus. Ne collecter aucune donnée nominative, aucun secret ou détail
d'architecture réelle. Les rôles et catégories d'équipements suffisent.

## Questions à poser dans l'ordre

1. Quels usages et publics la charte technique doit-elle couvrir ?
2. Quel est le mode d'exercice et quels rôles assurent support et sécurité ?
3. Quelles catégories de postes, comptes et services sont concernées ?
4. Quelles règles techniques sont déjà validées, et lesquelles sont proposées ?
5. Quelles consignes d'authentification, de protection des accès et de manipulation des informations sont attendues ?
6. Quel circuit d'alerte et d'assistance est réellement organisé ?
7. Quels usages distants, services en ligne ou outils d'IA doivent être cadrés techniquement ?
8. Quels éléments ont été communiqués par les skills compétents sur les conditions de contrôle ?
9. Quels points techniques restent à arbitrer ou à vérifier ?

Ne rédiger aucun dispositif de surveillance tant que sa base et ses
conditions ne sont pas établies. Ne pas rédiger de clause d'adoption,
d'opposabilité, de sanction, ni de délai de conservation de mémoire.

## Trame d'assemblage

```text
[INCOMPLET] Charte d'usage du SI — Brouillon technique
Objet et périmètre technique : [à renseigner]
Publics et moyens concernés, par catégories : [à renseigner]
Mode d'exercice et rôles de support : [à renseigner]
Règles techniques validées : [à renseigner]
Règles proposées, soumises à arbitrage : [à renseigner]
Protection des comptes et accès : [à renseigner]
Protection des informations et équipements : [à renseigner]
Usages distants, services en ligne et IA : [à renseigner selon les branches]
Signalement d'un incident et assistance : [circuit confirmé par rôle]
Conditions de contrôle : [éléments établis par les skills compétents, ou volet suspendu]
Adoption / opposabilité / sanctions : [BASCULE drh-fpt ; volet non rédigé]
Fond des données personnelles : [BASCULE dpo-ct ; volet non rédigé]
Sources mobilisées et dates de consultation : [à renseigner]
Points à arbitrer et champs manquants : [liste explicite]
```

## Vérification avant livraison

Conserver `[INCOMPLET]` si un élément nécessaire manque. Distinguer règles
validées et propositions ; ne pas affirmer que la charte est adoptée ou
opposable. Vérifier les conclusions juridiques selon
`../socle-sources-verification.md` et `../references-verifiees.md`.

Fond technique : `../securite-si.md`, `../infrastructures-reseaux.md`,
`../cloud-hebergement.md` et `../ia-donnees.md` selon les usages. Lire chaque
branche mobilisée et citer son chemin au point d'usage. Toute frontière est
nommée, puis son volet arrêté.
