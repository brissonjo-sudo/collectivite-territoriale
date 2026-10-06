# ADR 0003 — Instructions de découverte avant activation

- Date : 2026-10-06
- Statut : retenu pour un nouveau candidat, mesure comportementale à refaire
- Complète : ADR 0002 ; ses insertions historiques restent reproductibles

## Constat

Le pilote du candidat `a786` est conservé. Des cas APJA et incident spontané
produisent une annonce visible avant le chargement du skill ; un cas de
notification DPO omet la recherche juridique. Les instructions du corps,
chargées à l'activation, arrivent trop tard pour ces décisions initiales.

## Décision

Permettre une surcharge explicite `replace-description` sur le seul champ
`description` du frontmatter de `SKILL.md`. La description de découverte
porte des règles générales de priorité des garde-fous et de routage vers la
recherche juridique lorsque la demande appelle une qualification de droit.
Elle ne contient ni réponse de test, ni identifiant de cas, ni rôle attendu
propre à une campagne. Les prompts, oracles et permissions du harnais restent
inchangés.

Le fichier source ne contient que `description: >-` et ses lignes de texte
indentées de deux espaces. L'ancre est l'ancien champ complet, unique et
strictement situé dans le frontmatter. Le nom, les métadonnées et le corps
restent identiques. Toute autre opération, champ ou structure YAML est refusé.

`insert-before` reste l'opération par défaut des déclarations existantes.
Une insertion et un remplacement peuvent viser successivement `SKILL.md` ;
chaque étape vérifie les empreintes exactes de son état d'entrée et de sa
source. L'ordre est déclaré, sans mise à jour implicite des empreintes.

## Qualification

Le commit du plugin identifie ces variantes locales, sans modification des
commits amont ni réécriture des preuves du pilote. La modification du runtime
impose un nouveau commit, un nouveau gel et des sessions fraîches. Les scores
précédents ne sont pas transférés ; les tests de transformation ne prouvent
pas que le modèle respectera les instructions avant activation.
