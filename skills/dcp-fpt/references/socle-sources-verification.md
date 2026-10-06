# Socle — sources et vérification (commande publique)

> Méthode de vérification du skill. Elle dit **où** chercher, **dans quel
> ordre**, et **quand s'abstenir**. Les identifiants vérifiés sont dans
> `references/references-verifiees.md` ; les valeurs datées (seuils, délais,
> pourcentages) dans `references/cache-valeurs.md`, hors runtime. Rien dans ce
> fichier ne dispense de lire la source en session.

---

## 1. Hiérarchie des sources

| Rang | Source | Portée pour la collectivité |
|---|---|---|
| 1 | Droit de l'Union : directives marchés, règlements délégués de révision des seuils | S'impose ; transposé par le code de la commande publique |
| 2 | Loi : code de la commande publique (partie législative), code pénal, code de justice administrative, CGCT | S'impose |
| 3 | Règlement : code de la commande publique (partie réglementaire), avis relatif aux seuils, arrêtés (CCAG, modèles d'avis) | S'impose dans son champ |
| 4 | Contrat : CCAG **si le marché s'y réfère**, CCAP, CCTP | S'impose aux parties |
| 5 | Jurisprudence : Conseil d'État, cours administratives d'appel, Cour de cassation (pénal) | Fait autorité ; se cite par juridiction, date et numéro |
| 6 | Doctrine : fiches et guides de la direction des affaires juridiques de Bercy, Observatoire économique de la commande publique | **Non normative** : éclaire, n'oblige pas |

Un CCAG n'est pas un règlement applicable de plein droit : il ne lie les
parties que si le marché y fait référence, et dans la mesure des dérogations
écrites.

## 2. Sources officielles à privilégier

- **Légifrance**, par les outils `Droit_Francais` : `search_articles` puis
  `get_article` (texte, statut, date de version) ; `search_case_law` puis
  `get_decision` pour la jurisprudence.
- **Textes non codifiés** (avis relatif aux seuils, arrêtés CCAG) : page
  Légifrance par WebFetch, à signaler comme un repli (le résultat est un
  résumé, pas une copie littérale).
- **Droit de l'Union** : texte officiel en français sur CELLAR (Office des
  publications de l'Union européenne). EUR-Lex bloque les robots.
- **Doctrine** : site de la direction des affaires juridiques des ministères
  économiques et financiers, avec la date de mise à jour de la fiche.

## 3. Noyau minimal embarqué

Le registre `references-verifiees.md` couvre, au 2026-10-06 : définitions et
principes ; besoin, valeur, allotissement ; procédures ; publicité ;
candidatures et offres ; information des candidats et signature ;
techniques d'achat ; exécution, sous-traitance, modifications, résiliation ;
CCAG ; organes de la collectivité ; référés ; probité ; seuils ;
jurisprudence ; doctrine. Tout ce qui n'y figure pas se vérifie en session ou
se réserve.

## 4. Les sept réflexes propres à la commande publique

1. **Qui achète ?** Une collectivité agit comme **pouvoir adjudicateur** ; elle
   n'est entité adjudicatrice que pour une activité d'opérateur de réseaux.
   Ce n'est pas une **autorité publique centrale**. Le code ne nomme pas
   toujours les collectivités : leur qualité se déduit des définitions
   générales, et se signale comme une inférence.
2. **Quel seuil, pour qui ?** Les seuils de fournitures et services diffèrent
   entre l'État et les collectivités. Ne jamais présenter le seuil de l'État
   comme celui d'une commune. Les seuils sont révisés tous les deux ans : la
   valeur se lit au cache daté, puis se revérifie.
3. **Quelle version ?** Plusieurs articles ont changé récemment (offre
   économiquement la plus avantageuse, besoin de faible montant, profil
   d'acheteur, sous-traitance). Vérifier la version applicable à la date de
   lancement de la consultation, et les dispositions transitoires du texte
   modificatif.
4. **Procédure adaptée ou formalisée ?** Plusieurs obligations (délai de
   suspension, motivation détaillée du rejet, compétence de la commission
   d'appel d'offres) sont écrites pour les procédures formalisées. Ne pas les
   étendre à la procédure adaptée, ni les en exclure, sans le texte.
5. **Marché ou concession ?** Les concessions relèvent d'un autre régime et
   sont hors périmètre : signaler, s'arrêter.
6. **Obligation ou doctrine ?** Une fiche de la direction des affaires
   juridiques ou un guide de l'Observatoire n'oblige pas. Le dire.
7. **Jurisprudence citée par son numéro.** Juridiction, date, numéro. Jamais
   par son seul nom d'usage, jamais de mémoire.

## 5. Régime des valeurs — deux vitesses

### Valeurs volatiles — jamais de mémoire, jamais sans date

Seuils de procédure, montants de faible montant, délais de réception, délai
de suspension, délais de recours, pourcentages de modification, peines. Elles
sont au cache, datées ; elles se revérifient à la source avant d'être données,
avec leur date de lecture.

### Références structurelles stables — citables sous réserve

Les articles du registre se citent par leur objet et leur numéro, avec la
réserve « version à confirmer en vigueur à la date de la consultation ».

### Ce que l'on peut toujours donner

La **règle** et la **méthode** (comment calculer la valeur du besoin, quelle
condition vérifier avant de signer), sans la valeur.

## 6. Quand appeler `recherche-juridique`

- Vigueur d'un texte incertaine, version modifiée récemment.
- Jurisprudence à citer ou à confirmer.
- Conflit apparent entre le code, un CCAG et le contrat.
- Question pénale (favoritisme, prise illégale d'intérêts, signalement).

## 7. Résolution des conflits de normes

Le droit de l'Union prime ; la loi prime sur le règlement ; le contrat déroge
au CCAG dans la mesure où il le dit expressément. En cas de doute, ne pas
trancher : nommer le conflit et basculer vers `recherche-juridique`.

## 8. Règle de provenance des identifiants

Un identifiant (`LEGIARTI`, `JORFTEXT`, `CETATEXT`, CELEX) n'apparaît que dans
`references-verifiees.md`, vérifié et daté. Dans une réponse, la provenance
d'une référence tient en trois éléments : **source**, **date de lecture**,
**statut** (vérifié en session, ou tiré du registre et daté). Un identifiant
ne se reconstitue jamais de mémoire.

## 9. Abstention motivée

Si la source ne peut pas être lue (outil indisponible, texte introuvable),
le skill **ne conclut pas** sur le point concerné : il dit ce qui manque, ce
qu'il faudrait vérifier et où, et donne seulement la méthode. Une réponse
incomplète et honnête vaut mieux qu'un seuil faux.
