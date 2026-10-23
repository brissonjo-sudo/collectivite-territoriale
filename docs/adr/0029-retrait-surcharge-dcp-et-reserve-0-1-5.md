# ADR 0029 — Retrait de la surcharge DCP et réserve 0.1.5

Date : 2026-10-22. Décision de Jo, lot B12c : « Retirer la surcharge DCP ».
Cette décision supersède la surcharge R1 de l'ADR 0028 ; son historique reste
conservé, sans réécriture des commits.

## DCP mesuré et réserve humaine

La surcharge DCP, sa déclaration et son insertion sont retirées. Le runtime
DCP 0.1.4 retrouve l'entrée amont de 319 lignes et son SHA-256 exact
49e04e18203cc6472c35ab595d8f0a9a30671a51bd946d8a03f6b936041ff3b3.
Le pin 414cd4ecf41ba8b296908b738224355069b1890f, la preuve DCP-014, ses
contrôles et tous les tests historiques restent inchangés.

Le lien local du cas 9 reste maintenu en réserve :
plugin-dcp-frontiere-dsi-externe. Sa correction appartient à la source
DCP-fpt 0.1.5 avec la relecture praticien. Cette version future n'est ni
épinglée ni déclarée livrée ou qualifiée ici. La réserve ne devient pas
une conformité juridique ni une correction effectuée.

## Contrat v4 révisé avant mesure

Seul l'invariant d'interdiction des liens/chemins est retiré de ce cas DCP.
Il reste exigé sur l8-dsi-technique-spontanee et son contrôle déterministe
reste intact. La liste V4_PATH_CASES est la donnée du contrat révisée ; les
fonctions du chargeur, du validateur et les tests ne changent pas.
Les six autres surcharges conservent les consignes communes, sans la mention
spécifique étendant leur primauté à DCP. Aucune surcharge ne les transmet à DCP.
F2 reste identique : consigne Sénat du cas retraite, www.senat.fr et liste
RGPD CNIL/EUR-Lex. Les autres cas, invariants, modes et pins sont inchangés.
La matrice de sources perd uniquement l'invariant retiré ; elle couvre les
81 invariants restants des 18 cas. Son résultat est structurel, sans modèle.

L'empreinte v4 est recalculée et épinglée dans CYCLE_V4, le cycle préparé,
le manifeste 0028 et la matrice. Le mécanisme de fermeture de l'ADR 0028
reste inchangé et son champ adr est conservé. H1d n'est pas une mesure de H1c.
Dans le candidat, MEASUREMENT_140_V4 et les empreintes source/cible restent
None/null. Une copie jetable ferme seule le H2 diagnostique, puis assemble
et qualifie H3 avec les artefacts coûteux explicitement simulés. Aucune
preuve réelle n'est fabriquée et aucune sortie diagnostique n'est importée.

## Copies adoptées et limites

Claude confirme l'adoption de suivis/l140-campagne-B12b et suivis/l37-ci-B12b.
Les archives t43-successeur restent intactes. Le manifeste et l'accord de d
seront liés au nouveau H1d. prevol_passed ne passe à true qu'après contrôles
réussis ; tout autre refus exige un blocage et une proposition.
Les commandes Docker sont préparées pour Claude, sans exécution dans ce lot.
Aucun modèle, smoke, OAuth, push, PR ou publication n'est exécuté.
