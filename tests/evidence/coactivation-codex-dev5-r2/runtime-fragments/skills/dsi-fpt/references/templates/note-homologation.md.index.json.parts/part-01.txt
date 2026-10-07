# Gabarit interactif — Note d'homologation de sécurité (v0.2.0)

> **Usage** : préparer l'instruction d'une décision de sécurité et les éléments de son attestation formelle.
> **Statut du produit** : note préparatoire ; aucune homologation ni attestation ne résulte de ce gabarit.

## Préalables impératifs

Lire `../analyse-situation.md` avant toute aide technique. Afficher
intégralement le garde-fou incident du SKILL §5.2 comme premier livrable si
incident en cours ou récent. Afficher le garde-fou surveillance §5.3 avant
technique si déclenché. Effectuer les bascules pertinentes vers `dpo-ct`,
`drh-fpt`, `dpm-fpt`, `dirfi-fpt`, puis arrêter le volet de fond concerné.

Lire `../ecrits-numerique.md` et `../securite-si.md`. **Avant de présenter
l'homologation comme requise**, instruire le champ du système et l'applicabilité
à la collectivité à partir de `../references-verifiees.md` et
`../socle-sources-verification.md`. Pour un téléservice, lire aussi
`../dematerialisation-teleservices.md`. Sans source disponible ou champ
confirmé, laisser ce point à vérifier et ne pas conclure à une obligation.

Le décret relatif au RGS emploie **attestation formelle** par l'autorité
administrative ; le référentiel décrit la démarche d'**homologation de
sécurité**. C'est la collectivité qui homologue et atteste pour ses systèmes.
L'ANSSI qualifie des produits ; elle n'homologue pas le système de la
collectivité. Source et conditions → `../references-verifiees.md`.

## Questions à poser dans l'ordre

Poser **une seule question à la fois**, attendre la réponse et réutiliser les
faits connus. Ne demander ni donnée nominative, ni secret, ni architecture
réelle exploitable ; les preuves restent dans le circuit sécurisé compétent.

1. Quel système et quels échanges administratifs ou services aux usagers sont concernés, décrits par catégories ?
2. Quel est le mode d'exercice et quelle autorité compétente est identifiée, avec quelles délégations vérifiées ?
3. Quel périmètre de sécurité et quelle décision faut-il instruire : ouverture, évolution ou réexamen ?
4. Quelles sources et conclusions d'applicabilité ont effectivement été vérifiées ?
5. Quelle analyse de risques est disponible, avec quelles limites et inconnues ?
6. Quels objectifs de sécurité et quelles mesures ont réellement été définis et mis en œuvre ?
7. Quelles preuves ou évaluations sont disponibles, avec quels résultats et réserves ?
8. Quels risques résiduels et actions ouvertes doivent être présentés au décideur ?
9. Quelles conditions de maintien en sécurité et de réexamen sont proposées ou confirmées ?
10. Une décision a-t-elle déjà été prise et communiquée, ou reste-t-elle à instruire ?

Ne pas inventer une analyse, un résultat d'audit, une acceptation de risque,
une signature, une échéance ou une décision favorable. Qualifier explicitement
les éléments déclarés, documentés et restant à vérifier.

## Trame d'assemblage

```text
[INCOMPLET] Note préparatoire d'homologation de sécurité — [système anonymisé]
Objet de l'instruction : [à renseigner]
Périmètre fonctionnel et de sécurité : [à renseigner par catégories]
Mode d'exercice et responsabilités : [à renseigner]
Autorité compétente et délégations vérifiées : [à renseigner ou à vérifier]
Champ du RGS et applicabilité : [conclusion sourcée, ou à vérifier]
Analyse de risques : [référence anonymisée / état / limites]
Objectifs et mesures de sécurité : [déclarés / documentés / non vérifiés]
Évaluations et preuves : [références anonymisées / résultats établis / réserves]
Risques résiduels et actions ouvertes : [à renseigner]
Conditions de maintien et de réexamen : [proposées / confirmées / à définir]
Décision soumise à l'autorité : [à instruire ; aucune conclusion présumée]
Décision effectivement communiquée : [objet / portée / réserves, ou non établie]
Attestation formelle : [à établir par l'autorité, ou état effectivement communiqué]
Modalités d'accessibilité aux usagers si téléservice : [exigence vérifiée / modalités à confirmer]
Sources mobilisées et dates de consultation : [à renseigner]
Champs manquants et vérifications bloquantes : [liste explicite]
```

## Vérification avant livraison

Conserver `[INCOMPLET]` tant que les éléments nécessaires manquent. Une
qualification de produit ou une certification de prestataire ne remplace ni
l'analyse du système, ni la décision de la collectivité. Ne pas écrire
« système homologué », « conforme » ou « risque accepté » sans la décision ou
la preuve correspondante effectivement fournie.

Vérifier l'autorité, le champ, le contenu requis et la provenance avant une
conclusion engageante. Citer `../securite-si.md`,
`../dematerialisation-teleservices.md` et le registre au point d'usage ; aucun
identifiant officiel ni version de référentiel recopié dans cette note.
