# Branche — retex

## 1. Périmètre / Exclusions

Capitaliser une consultation infructueuse, un contentieux ou une modification
contestée, en méthode anonymisée. La branche compétente reste responsable du
fond ; aucune règle juridique nouvelle, qualification pénale ou justification
après coup n'est produite par le retour d'expérience.

## 2. Questions couvertes

Qu'apprendre d'une consultation sans offre ? Comment distinguer erreur de
conception, difficulté de marché et lacune du skill ? Comment tracer une
correction sans conserver une consultation identifiable ?

## 3. Arbre de traitement

Événement → risque actuel et STOP → faits abstraits → branche responsable
→ source de l'écart → cause démontrée ou hypothèse → action et vérification
→ proposition d'entrée de maintenance, sans score comportemental inventé.

## 4. Variables à lever

Mode d'exercice, stade, nature et procédure sans valeur réelle, objectif,
écart observé, preuves accessibles, résultat effectif, règle/source utilisée,
facteur externe, impact et correction testable. Retirer personnes, entreprises,
dates de consultation et toute combinaison identifiante ; garder seulement
la date de capitalisation lorsqu'une entrée est autorisée.

## 5. Règles métier

**Méthode, non obligation de droit** : séparer fait établi, interprétation,
cause supposée et action. Un contentieux perdu ne démontre pas que toute
la méthode est fausse ; une procédure non contestée ne prouve pas sa légalité.
Un retour d'expérience ne vaut pas nouvelle lecture de source officielle.

Infructuosité → `references/candidatures-offres.md` pour qualifier les offres,
puis `references/procedures.md` pour la voie de relance. Ne pas transformer
« infructueux » en dispense automatique. Besoin mal calibré →
`references/besoin-strategie-achat.md` ; diffusion insuffisante →
`references/publicite-consultation.md` ; avenant contesté →
`references/modifications.md` ; contentieux → `references/contentieux.md`.
Le fond reste dans ces branches, il n'est pas recopié dans le journal.

Correction juridique → vérifier champ, version et source avant ajout au lot
et au registre ; correction de rédaction → modifier le seul emplacement
responsable ; changement d'architecture → ADR. Maintenir la distinction entre
contrôle statique, test unitaire, mesure des réponses et relecture praticien.
Les scores logiciels factices ne qualifient pas le skill.

**Anonymisation obligatoire** : ne conserver ni noms ni pseudonymes réversibles,
ni entreprise candidate, montant, offre ou calendrier identifiable. Si une
abstraction suffisante détruit la compréhension, ne pas journaliser le cas ;
conserver seulement l'apprentissage général. Aucun copier-coller de pièces.

**Fait déjà commis** : l'analyse des causes n'autorise pas à dissimuler ni à
reconstituer une motivation fictive. Appliquer `SKILL.md` §5.2 et les frontières
quand déontologie ou suites sont en jeu.

## 6. Procédures

1. Vérifier si un risque exige encore un arrêt ou l'appui du conseil.
2. Reconstituer un scénario abstrait et indiquer le résultat observé.
3. Relier l'écart à une branche et distinguer manque de source et erreur de méthode.
4. Proposer une correction étroite avec critère de vérification.
5. Avec accord, consigner hors runtime l'apprentissage sans données du cas.

## 7. Déclencheurs de vérification

Conclusion juridique tirée d'un retour, décision de justice non identifiée,
nouvelle valeur, exigence supposée, erreur de seuil, changement de frontière.
Lire le socle ; `recherche-juridique` pour la conclusion juridique, jamais
la seule mémoire d'un résultat.

## 8. Pièges et confusions fréquentes

Remplir le journal avec une offre réelle ; rechercher un responsable nominatif ;
généraliser depuis un cas ; présenter tests verts comme mesure ; recopier
le droit dans plusieurs branches ; corriger un résultat en masquant l'échec.

## 9. Données et valeurs à vérifier

Résultat effectivement observé, version du skill, source/date/statut et
contrôle de la correction. Seuils et délais ne sont jamais ajoutés ici.
Aucune conclusion statistique depuis des exemples exploratoires.

## 10. Écrits et livrables

Fiche abstraite : situation → écart → cause prouvée/hypothèse → branche →
correction → contrôle → limite. Journal de maintenance hors paquet, avec
accord et date ; aucune nouvelle fiche d'objet ou gabarit sans besoin justifié.

## 11. Double échelle [risque / confiance]

Capitalisation de forme : faible/stable. Conclusion de droit : élevé/à vérifier.
Fait orienté ou dissimulation : critique/STOP. Incertitude factuelle : la cause
reste hypothèse, pas décision durable.

## 12. Checklist de branche

- [ ] Faits, causes, recommandations et limites séparés.
- [ ] Branche responsable nommée, contenu unique.
- [ ] Aucune donnée ou combinaison identifiable.
- [ ] Source nouvelle vérifiée avant registre, pas de score fictif.
- [ ] Accord avant journalisation, correction et contrôle explicites.
