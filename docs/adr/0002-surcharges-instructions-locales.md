# ADR 0002 — Corrections d'instructions locales et reproductibles

- Date : 2026-09-30
- Statut : accepté pour le candidat, validation comportementale encore requise
- Supersède partiellement : la contrainte de copies strictement identiques du plan initial ; l'ADR 0001 reste applicable

## Contexte et autorisation

Les essais frais du candidat 2bb7262 montrent des défauts de provenance,
de calcul de délai sur faits manquants et de contrainte APJA. Le 30 septembre,
l'utilisateur autorise le chantier de correction des instructions jusque-là
gelées. Cette autorisation n'est ni une validation humaine des sorties ni une
autorisation de publier un candidat en échec.

## Décision

Conserver les commits et les versions amont. Ajouter trois surcharges locales
dans les points d'entrée DPM, DPO et recherche juridique, suffisamment tôt
pour être chargées avec le skill. Elles clarifient des invariants déjà prévus,
sans ajouter de réponses aux prompts de test. Les dépôts amont et les deux
autres runtimes restent inchangés ; le MCP reste unique et inchangé.

Chaque surcharge est déclarée dans upstream.json avec un fichier source,
une cible, deux empreintes SHA-256 (base et correction) et une ancre unique.
Le synchroniseur insère le texte de façon déterministe après vérification.
Le contrôleur de dérive compare la variante complète, et non une copie
supposée identique à l'amont. Chemins dangereux, doublons, liens symboliques,
empreintes divergentes, cibles absentes et ancres ambiguës sont refusés.

## Conséquences

La version interne du skill désigne la base, le commit du plugin désigne la
variante. Le README distingue les trois variantes des deux copies exactes.
Une reprise dans les dépôts amont devra faire l'objet d'un chantier distinct,
puis permettre de retirer ces surcharges à un commit explicitement choisi.
La barrière de publication, la revue humaine et les essais frais restent dus.
