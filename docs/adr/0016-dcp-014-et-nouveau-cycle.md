# ADR 0016 — Référence autonome DCP 0.1.4 et nouveau cycle

Date : 20 octobre 2026. Décision de Jo transmise par Claude : « go 17 », T43-L24.
Statut : intégration et préparation locales ; nouvelle campagne plugin non exécutée.

Cette décision additive supersède le pin DCP de l'ADR 0010, la référence active
DCP-0 de l'ADR 0012 et la surcharge DCP option b décidée en L22. Ces décisions
et leurs preuves historiques restent conservées. Aucun résultat plugin antérieur
ne mesure les nouveaux octets.

## Pin source et lecture RJ

DCP-fpt 0.1.4 est figé au commit
`414cd4ecf41ba8b296908b738224355069b1890f`, tête de DCP-fpt#8 vérifiée en lecture.
Les 30 fichiers runtime et LICENSE sont copiés selon la sélection d'upstream.json.
Les deux surcharges DCP et leur déclaration sont retirées : STOP en tête et
frontières proviennent désormais exclusivement de la source.

La surcharge recherche-juridique conserve STOP avant toute annonce ou outil et
une seule lecture intégrale ou série contiguë couvrant chaque entrée. Pour une
entrée longue, elle impose les segments bornés dès le départ. Une restitution
incomplète est signalée ; aucune affirmation ne porte sur les lignes non reçues,
sans interrompre toute la réponse ni prétendre l'activation acquise. Les refus
de lecture échouée, tronquée, hors contrat, trouée ou doublonnée sont inchangés.

Context7 a refusé la résolution documentaire pour quota mensuel épuisé.
La syntaxe est vérifiée dans les documentations officielles
[Get-Content](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-content?view=powershell-7.5)
et [Select-Object](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/select-object?view=powershell-7.5).

## Nouvelle référence DCP-014, même mécanisme fermé

La pièce `tests/evidence/2026-10-20-dcp-014/dcp-autonome.json` référence
`tests/runs/codex-web-v0.1.4-dcp-stop-20261020-a` dans DCP-fpt#8 au pin ci-dessus.
Elle contient la synthèse autonome exacte (28 réussites sur 28), et distingue
la relecture de Jo, non praticien, de la validation juridique et du plugin.
La synthèse, l'avis humain, la provenance et le statut hors runtime sont copiés
depuis les blobs Git publics, avec leurs empreintes dans la pièce.

Le commit effectivement mesuré est
`071737280debb275549647ffc8c1340cab544a18`. Pour chacun des 30 fichiers,
l'intégration vérifie l'égalité entre le runtime mesuré, le pin de preuve
`414cd4e…`, la synthèse et la copie embarquée. Les commits de preuve n'ont
pas modifié ces octets. Le texte historique « non mesuré » du SKILL.md reste
copié sans correction locale ; le statut actuel est porté hors runtime en amont.

`scripts/dcp-protocol.json` épingle le pin, le commit public, le fichier entier
de preuve et la synthèse sérialisée UTF-8/indentation 2/LF par SHA-256.
`dcp_reference.py` et l'assembleur conservent le même mécanisme : vérification
du pin, de la provenance, des empreintes, des 30 octets de fichiers mesurés,
de la sélection exacte (LICENSE seul hors mesure), des seuils et des liens
non redirigés ; copie exclusive identique puis nouvelle vérification.
Aucun paramètre CLI de remplacement, nouvelle exclusion ou tolérance ajoutée.
La nouvelle décision reconnue est DCP-014. DCP-0 et son ancien pin sont refusés
pour le candidat courant ; son contrat historique est conservé dans
`scripts/dcp-protocol-0012.json` et sa batterie de mutations reste exercée.
La même batterie s'applique aussi à la nouvelle référence.

Les champs `human_legal_validation` et `publication_ready` restent faux.
Le scope et la note de réserve praticien sont inchangés. La relecture autonome
de Jo ne vaut ni relecture des 18 cas plugin ni validation du smoke.

## Nouveau cycle séparé

Le contrat `scripts/cas-plugin-cycle-v2.json`, ses 18 demandes/invariants,
ses STOP déterministes et le smoke durci de L22 restent inchangés. L'outillage
L12b/L12c de L14 est repris hors candidat pour une seule tentative neuve,
36 sessions maximum (18 réponses et 18 relectures), liée à la nouvelle tête,
aux octets du runtime, aux scripts, aux cas et à l'autorisation par empreintes.
Aucune session, résolution humaine, transition d'outillage ou qualification
historique n'est transférée.

L24 prépare sans exécuter. L'autorisation du présent lot couvre l'intégration
et la préparation seulement ; elle n'invente aucun budget d'appel. Le lanceur
refuse l'exécution en l'absence d'une autorisation Jo liée au plan et d'un
budget explicite. Le smoke est une phase distincte après relecture humaine.
L'ADR 0007, les validateurs, les seuils et la séparation validate/release
demeurent. Aucune release, installation, campagne, poussée ou action GitHub
en écriture n'est réalisée dans ce lot.
