# Références vérifiées — Légifrance et doctrine officielle

> **Veille du 2026-11-03** — 12 identifiants recontrôlés par l'API Légifrance
> (outil MCP, lecture de l'article et de son historique) ; 5 versions
> remplacées en 2026 corrigées (CGCT L. 1612-4, L. 1612-5, L. 1612-14 et
> L. 1612-15 au 01/01/2026 par l'ordonnance n° 2025-526 du 12 juin 2025,
> art. 1 ; L. 2321-2 au 21/02/2026 par la loi n° 2026-103 du 19 février 2026,
> art. 198) ; 3 décisions intégrées (§7). Identifiants ajoutés à cette date :
> CGCT L. 1612-12 et L. 1612-16, ordonnance n° 2025-526 art. 12, CJF L. 131-2,
> L. 131-3, L. 131-4 et L. 131-14.

> **Ce fichier est le seul du dépôt autorisé à contenir des identifiants
> Légifrance en dur** (`LEGIARTI`, `JORFTEXT`, `NOR`, numéro de décision) — parce
> qu'ils y sont **vérifiés et datés** (règle de provenance, `socle-sources-verification.md`
> §8). Toute référence à un identifiant qui ne figure pas ici doit être
> **réservée** (« à confirmer en version consolidée ») ou **retirée** de toute
> réponse produite par le skill : un identifiant ne se reconstitue jamais de
> mémoire.
>
> **Ce registre ne contient aucune valeur chiffrée.** Taux, seuils, montants de
> dotation, plafonds et durées relèvent exclusivement de `cache-taux-seuils.md`
> et de sa propre procédure de vérification.
>
> Vérifications initiales effectuées le **2026-09-15**, par consultation directe de
> légifrance.gouv.fr (`WebFetch`) et par recherche ciblée renvoyant une page
> Légifrance nommément identifiée (`WebSearch`). Un statut `vérifié` signifie
> que l'identifiant a été **lu**, à cette date, sur une page ou un résultat de
> recherche pointant explicitement vers cette page — jamais reconstitué. Un
> statut `⚠️ non vérifié` signifie que la tentative n'a pas abouti à un
> identifiant univoque : la référence reste utilisable **par son objet et sa
> désignation usuelle**, mais son identifiant Légifrance doit être revérifié
> avant toute citation dans un acte.
>
> Les lignes datées du **2026-11-03** ont été lues par l'API Légifrance
> (outil MCP) : texte de l'article, état `VIGUEUR` et date de début de la
> version applicable à cette date.

---

## 1. Budget et cycle budgétaire

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| Date limite de vote du budget (15 avril / 30 avril année de renouvellement) ; conséquence en cas de non-adoption | CGCT, art. **L. 1612-2** | LEGIARTI000051731704 (en vigueur depuis le 01/01/2026) | 2026-09-15 | vérifié |
| Débat d'orientation budgétaire (DOB) des communes ≥ 3 500 habitants ; rapport d'orientation budgétaire | CGCT, art. **L. 2312-1** | LEGIARTI000051731867 (en vigueur depuis le 01/01/2026) | 2026-09-15 | vérifié |
| Contenu réglementaire détaillé du rapport d'orientation budgétaire | Décret n° 2016-841 du 24 juin 2016 | — | 2026-09-15 | ⚠️ non vérifié — identifiant JORFTEXT/LEGIARTI non confirmé lors de cette passe (texte repéré, non ouvert) |

> **Effet de la saisine — règle vérifiée le 2026-09-15, opposable.** Les deux
> cas de saisine n'ont **pas** le même effet sur la compétence de l'assemblée,
> et c'est le contraire de ce que le skill affirmait jusqu'à la v1.0.1 :
>
> - **L. 1612-2 (budget non voté)**, al. 2 — *« À compter de la saisine de la
>   chambre régionale des comptes et jusqu'au règlement du budget par le
>   représentant de l'État, l'organe délibérant ne peut adopter de délibération
>   sur le budget de l'exercice en cours. »* L'assemblée est donc **dessaisie
>   dès la saisine**. Un alinéa 3 écarte le mécanisme lorsque le défaut
>   d'adoption tient à l'absence de communication d'informations indispensables.
> - **L. 1612-5 (budget en déséquilibre réel)** — **aucune clause de
>   dessaisissement**. La chambre **demande une nouvelle délibération** à
>   l'assemblée, qui reste pleinement compétente ; le règlement préfectoral est
>   subsidiaire.
>
> Une règle unique énoncée pour « toute saisine de la CRC » est fausse dans un
> sens ou dans l'autre. Détail opérationnel → `controle-budgetaire.md` §6.2.

> **Note L. 1612-2** : la version consultée (en vigueur au 01/01/2026) confirme
> le mécanisme complet — saisine de la chambre régionale des comptes par le
> représentant de l'État, proposition sous un mois, règlement du budget par le
> préfet, suspension des délibérations du conseil sur le budget de l'exercice
> jusqu'au règlement, et le cas particulier de l'absence de communication des
> informations essentielles avant le 31 mars (délai de 15 jours).

---

## 2. Contrôle budgétaire et équilibre réel

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| Définition de l'équilibre réel du budget | CGCT, art. **L. 1612-4** | LEGIARTI000051731697 (en vigueur depuis le 01/01/2026 ; remplace LEGIARTI000006389562, version 1996-2025, texte identique) | 2026-11-03 | vérifié |
| Saisine de la chambre régionale des comptes — budget non adopté | CGCT, art. **L. 1612-2** | LEGIARTI000051731704 | 2026-09-15 | vérifié (cf. §1) |
| Saisine de la chambre régionale des comptes — budget non voté en équilibre réel | CGCT, art. **L. 1612-5** | LEGIARTI000051731690 (en vigueur depuis le 01/01/2026 ; texte identique à la version 1996-2025, LEGIARTI000006389623) | 2026-11-03 | vérifié |
| Approbation des comptes : vote de l'organe délibérant sur le **compte financier unique** ; rejet et avis de la CRC | CGCT, art. **L. 1612-12** | LEGIARTI000051731724 (en vigueur depuis le 01/01/2026 ; la version 2015-2025, LEGIARTI000027574298, visait l'« arrêté des comptes » par le vote du compte administratif) | 2026-11-03 | vérifié |
| Saisine de la chambre régionale des comptes — **comptes approuvés** faisant apparaître un déficit | CGCT, art. **L. 1612-14** | LEGIARTI000051731712 (en vigueur depuis le 01/01/2026 ; remplace LEGIARTI000006389570 : « arrêté des comptes » devient « approbation des comptes », seuils et délais inchangés) | 2026-11-03 | vérifié |
| Saisine de la chambre régionale des comptes — dépense obligatoire non inscrite ou insuffisamment inscrite | CGCT, art. **L. 1612-15** | LEGIARTI000051731664 (en vigueur depuis le 01/01/2026 ; texte identique à LEGIARTI000006389571) | 2026-11-03 | vérifié |
| Mandatement d'office d'une dépense obligatoire par le représentant de l'État après mise en demeure | CGCT, art. **L. 1612-16** | LEGIARTI000051731660 (en vigueur depuis le 01/01/2026) | 2026-11-03 | vérifié |
| Application de la réforme budgétaire et comptable « à compter de l'exercice budgétaire 2026 » | Ordonnance n° **2025-526** du 12 juin 2025, **art. 12** | LEGIARTI000051725685 (en vigueur depuis le 14/06/2025) ; article modificateur du CGCT : art. 1, LEGIARTI000051725663 | 2026-11-03 | vérifié |

> **Note méthode** : la série L. 1612-* forme un mécanisme unique (saisine du
> préfet → délai d'un mois de la CRC → proposition → arrêté préfectoral motivé
> en cas d'écart). **Ne pas déduire** l'identifiant d'un article de la série à
> partir d'un autre déjà vérifié : chaque article a été recherché
> individuellement (règle de non-héritage, `socle-sources-verification.md`
> §8).
>
> **Correction du 2026-11-03** : jusqu'à cette date, le registre affichait
> L. 1612-5 à la fois « vérifié » (tableau) et « non vérifié » (cette note).
> L'identifiant alors consigné (LEGIARTI000006389622) désignait en réalité la
> version du 24/02 au 13/04/1996. La version applicable a été lue le
> 2026-11-03 : la contradiction est levée, L. 1612-5 est **vérifié**.
>
> **Réforme au 01/01/2026 (ordonnance n° 2025-526, art. 1 et 12)** : l'article
> 1 modifie L. 1612-1 à L. 1612-20, crée une section « Dispositions
> budgétaires et comptables » (L. 1612-21 à L. 1612-41) et abroge notamment,
> pour les communes, L. 2311-6, L. 2311-7, L. 2312-2, L. 2312-4, L. 2322-1,
> L. 2322-2, L. 2341-1, L. 2342-1, L. 2342-2 et L. 2343-2 ; l'article 12 la
> rend applicable à compter de l'exercice 2026. Comparaison des versions lue
> le 2026-11-03 : L. 1612-4, L. 1612-5 et L. 1612-15 inchangés ; L. 1612-14
> est déclenché par l'**approbation des comptes** ; selon L. 1612-12,
> l'approbation des comptes est le vote sur le **compte financier unique**.
> Le régime des comptes de l'exercice 2025 votés en 2026 n'est pas tranché
> par ces textes : **à vérifier**. Les articles L. 1612-21 à L. 1612-41 n'ont
> pas été lus.

---

## 3. Compétences et délégations

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| Dépenses obligatoires des communes (liste) | CGCT, art. **L. 2321-2** | LEGIARTI000053550550 (en vigueur depuis le 21/02/2026, loi n° 2026-103 art. 198 ; remplace LEGIARTI000049312829 : ajout d'un 3° bis relatif aux attributions exercées par le maire au nom de l'État, L. 2122-27-1 ; autres points inchangés) | 2026-11-03 | vérifié |
| Délégations que le conseil municipal peut consentir au maire, dont le recours à l'emprunt (3°) dans les limites fixées par l'assemblée | CGCT, art. **L. 2122-22** | LEGIARTI000045212383 (en vigueur depuis le 23/02/2022, loi n° 2022-217) | 2026-11-03 | vérifié |

> **Réserve L. 2122-22 — close le 2026-11-03** : l'historique de l'article
> confirme que `LEGIARTI000037666566` est une **version antérieure** du même
> article (du 25/11/2018 au 23/02/2022), et non un miroir. La version
> applicable est `LEGIARTI000045212383`, en vigueur depuis le 23/02/2022.
> **Portée** : la délégation d'emprunt cesse à l'ouverture de la campagne
> électorale pour le renouvellement du conseil municipal ; les décisions
> prises sur ce fondement obéissent aux mêmes règles que les délibérations du
> conseil sur le même objet.

---

## 4. Exécution, ordonnateur et comptable

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| Décret relatif à la gestion budgétaire et comptable publique (texte fondateur, GBCP) | Décret n° **2012-1246** du 7 novembre 2012 | JORFTEXT000026597003 | 2026-09-15 | vérifié |
| Incompatibilité des fonctions d'ordonnateur et de comptable public | Décret n° 2012-1246, **art. 9** | (au sein de JORFTEXT000026597003) | 2026-09-15 | vérifié |
| Contrôles exercés par le comptable public (contrôle de la dépense, pièces justificatives) | Décret n° 2012-1246, art. non identifié avec certitude lors de cette passe | — | 2026-09-15 | ⚠️ non vérifié — à confirmer en version consolidée |
| Obligation de dépôt des fonds des collectivités au Trésor — champ d'application du régime des dérogations | CGCT, art. **L. 1618-1** | LEGIARTI000006389606 | 2026-09-15 | vérifié — voir §6 |
| Obligation de dépôt des fonds des collectivités au Trésor — conditions générales des dérogations | CGCT, art. **L. 1618-2** | LEGIARTI000042194908 | 2026-09-15 | vérifié — voir §6 |

> **Note art. 9** : la vérification directe de la page du décret confirme le
> principe de séparation (« les fonctions d'ordonnateur et de comptable public
> sont incompatibles »), étendu à l'interdiction pour un conjoint ou partenaire
> de pacs de l'ordonnateur d'exercer comme comptable dans le même organisme.
> **Le ou les articles précis sur les contrôles du comptable** (contrôle de la
> validité de la créance, exactitude des calculs, pièces justificatives) n'ont
> **pas** été atteints lors de cette passe — ne pas les citer sans nouvelle
> vérification.

---

## 5. Responsabilité financière et gestion de fait

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| Ordonnance portant réforme du régime de responsabilité financière des gestionnaires publics | Ordonnance n° **2022-408** du 23 mars 2022 | JORFTEXT000045398055 | 2026-09-15 | vérifié |
| Décret d'application de l'ordonnance n° 2022-408 (comptables publics) | Décret n° **2022-1605** du 22 décembre 2022 | JORFTEXT000046778725 | 2026-09-15 | vérifié |
| Infractions et sanctions du régime unifié de responsabilité financière, codifiées au code des juridictions financières (section 2, chapitre Ier, titre III) | Code des juridictions financières, art. **L. 131-9 à L. 131-14** (renvoi lu dans L. 131-15) ; sanctions à la section 3 | — (L. 131-9 à L. 131-13 et section 3 non lus) | 2026-11-03 | ⚠️ non vérifié — seuls L. 131-14 et L. 131-15 sont lus |
| Justiciables exclus au titre des infractions de la section 2, notamment les **maires** (8°) et, dans les cas visés, adjoints et conseillers municipaux | CJF, art. **L. 131-2** | LEGIARTI000052092800 (en vigueur depuis le 01/01/2026) | 2026-11-03 | vérifié |
| Les personnes de L. 131-2 sont justiciables de la Cour des comptes au titre de la **gestion de fait** (L. 131-15) | CJF, art. **L. 131-3** | LEGIARTI000045404187 (en vigueur depuis le 01/01/2023) | 2026-11-03 | vérifié |
| Les personnes des 2° à 15° de L. 131-2, dont les maires, sont justiciables au titre de **L. 131-14** | CJF, art. **L. 131-4** | LEGIARTI000045404184 (en vigueur depuis le 01/01/2023) | 2026-11-03 | vérifié |
| Infraction : agissements entraînant une **astreinte** pour inexécution ou exécution tardive d'une décision de justice (1°) ; manquement à l'article 1er, I et II, de la loi n° 80-539 du 16 juillet 1980 (2°) | CJF, art. **L. 131-14** | LEGIARTI000045400558 (en vigueur depuis le 01/01/2023) | 2026-11-03 | vérifié |
| Définition de la gestion de fait : ingérence dans le recouvrement de recettes publiques sans qualité de comptable public ; maniement de fonds **extraits irrégulièrement** de la caisse d'un organisme public ; opérations réservées aux comptables publics | CJF, art. **L. 131-15** | LEGIARTI000045400562 (en vigueur depuis le 01/01/2023) | 2026-11-03 | vérifié — article définitoire lu ; la justiciabilité relève de L. 131-1 à L. 131-4 |

> **Mise à jour du 2026-11-03** : L. 131-15 a été lu ; c'est l'article qui
> définit la gestion de fait et la rend passible des sanctions de la section 3.
> La réserve ci-dessous, rédigée le 2026-09-15, reste valable pour les
> articles **non lus** (L. 131-9 à L. 131-13, section 3 des sanctions). Selon
> les arrêts du §7, les sanctions ont été modifiées par la loi n° 2026-103 ;
> constat non relu sur l'article : **à vérifier** avant toute citation.
>
> **Pourquoi la prudence ici, alors que des identifiants ont été « vus »** :
> le code des juridictions financières a été profondément recodifié à
> l'occasion de l'ordonnance n° 2022-408 (entrée en vigueur 2023). Les
> résultats de recherche ont renvoyé plusieurs articles concurrents
> (**L. 131-11**, **L. 131-15**) traitant chacun d'un aspect de la gestion de
> fait (amende, usage de fonds irrégulièrement détenus) sans qu'aucun ne se
> soit dégagé, lors de cette passe, comme **l'article définitoire** à citer
> seul. Face à ce doute, la règle du socle s'applique : **abstention motivée**
> plutôt qu'identifiant probable présenté comme certain. À lever par
> `recherche-juridique` avant toute prochaine citation de cette notion dans un
> acte ou une note.

---

## 6. Trésorerie

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| Régime général des dérogations à l'obligation de dépôt des fonds des collectivités auprès de l'État — champ d'application | CGCT, art. **L. 1618-1** | LEGIARTI000006389606 | 2026-09-15 | vérifié |
| Régime général des dérogations à l'obligation de dépôt — conditions générales, compétence de l'assemblée délibérante | CGCT, art. **L. 1618-2** | LEGIARTI000042194908 | 2026-09-15 | vérifié |
| Principe même de l'obligation de dépôt des fonds au Trésor (hors régime des dérogations) | Texte fondateur non identifié avec certitude lors de cette passe (principe historique de l'unité de caisse du Trésor ; ne pas confondre avec les seuls articles de dérogation ci-dessus) | — | 2026-09-15 | ⚠️ non vérifié — à confirmer en version consolidée |

> **Point de vigilance** : le chapitre VIII du titre Ier du livre VI du CGCT
> (L. 1618-1 et L. 1618-2) organise les **dérogations** à l'obligation de
> dépôt, non l'obligation elle-même. Ne pas citer L. 1618-1/L. 1618-2 comme
> fondant l'obligation de principe : ils en organisent seulement les
> exceptions et les conditions. Le texte posant l'obligation elle-même reste à
> identifier précisément (candidats usuels : principes généraux de la
> comptabilité publique, décret GBCP n° 2012-1246, ou dispositions plus
> anciennes non recodifiées) — à traiter par `recherche-juridique`.

---

## 7. Jurisprudence financière vérifiée

Décisions lues en texte intégral par l'API Légifrance (fonds JUFI et CETAT).
Toute autre décision citée dans une réponse du skill reste **réservée**. Les
deux arrêts de la Cour des comptes sont susceptibles d'appel devant la Cour
d'appel financière (mention de leur texte) : leur caractère définitif n'est
pas vérifié.

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| Gestion de fait par **mandat fictif** : fausse facture sans service fait, émise pour conserver une subvention ; le maire est justiciable (CJF L. 131-3) ; prescription de dix ans pour L. 131-15 (CJF L. 142-1-3, cité par l'arrêt) ; ni l'absence d'enrichissement ni le remboursement ultérieur de la subvention n'écartent la qualification | Cour des comptes, chambre du contentieux, arrêt du 16/10/2026, n° **S-2026-1111** | JUFITEXT000055005642 (publication « C ») | 2026-11-03 | vérifié — texte intégral lu |
| CJF L. 131-14 : **mandatement tardif** de sommes dues en exécution de décisions de justice (2°) et exécution tardive ayant entraîné une **astreinte** (1°) ; le maire et le directeur général des services sont tous deux sanctionnés | Cour des comptes, chambre du contentieux, arrêt du 22/10/2026, n° **S-2026-1144** | JUFITEXT000055019898 (publication « C ») | 2026-11-03 | vérifié — visas, cadre juridique et dispositif lus ; motivation lue en partie |
| TEOM : taux **manifestement disproportionné** ; dépenses prises en compte au vote du taux = fonctionnement réel + soit dotations aux amortissements, soit investissement réel, selon l'**option retenue par la collectivité au moment du vote** (CGI, art. 1520, I, 2° et 3°), déduction faite des recettes non fiscales ; une option invoquée seulement en cours d'instance est inopérante | CE, 8e et 3e ch. réunies, 23/10/2026, n° **507100** | CETATEXT000055013111 (publication « B » selon la métadonnée) | 2026-11-03 | vérifié — texte intégral lu |

> Rappel de méthode (aligné sur le registre du skill frère `Dpm-fpt`, §7) :
> une décision juridictionnelle se cite **comme un article** — juridiction,
> formation, date, numéro de requête ou de décision, identifiant, et date de
> vérification — jamais par son seul nom d'usage.

---

## 8. Doctrine administrative consultée hors Légifrance

Cette section consigne une consultation de doctrine officielle, distincte des
vérifications d'identifiants Légifrance des sections précédentes. Une réponse
ministérielle ne prime jamais sur la loi ou le décret ; son utilisation pour
un agent relève de `drh-fpt` (renvoi de `SKILL.md` §5.5).

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| Absence d'indemnité de départ à la retraite instituée ; repère CIA strictement conditionnel et renvoi vers drh-fpt | Réponse du ministère de l'action publique, de la fonction publique et de la simplification du 22/05/2025 à la question écrite n° 01222 — [Sénat](https://www.senat.fr/questions/base/2024/qSEQ241001222.html) | sans identifiant Légifrance, senat.fr | 2026-10-21 | consultée — doctrine administrative ; vérifications d'applicabilité à reprendre côté drh-fpt |

---

## Procédure de mise à jour

**Quand recontrôler**

- **Revue de loi de finances (janvier)** : la loi de finances de l'année et la
  loi de programmation des finances publiques modifient chaque année des
  pans entiers du droit budgétaire local. Revérifier en priorité les articles
  du §1 et du §2 (dates, seuils procéduraux, éventuelle renumérotation).
- **Revue de rentrée (1er septembre)** : contrôler l'état des textes non
  encore stabilisés — en particulier la codification définitive du régime de
  responsabilité financière issu de l'ordonnance n° 2022-408 (§5) et tout
  décret d'application publié dans l'intervalle.
- **Sur signalement** : toute mention, dans une source primaire consultée
  pour un autre besoin, d'une modification ou abrogation d'un texte de ce
  registre déclenche une revérification immédiate de cet article précis.

**Comment recontrôler**

- Toujours par **appel d'outil** sur Légifrance (recherche ciblée puis lecture
  de la page d'article), **jamais de mémoire** — y compris pour un article
  déjà présent ici : ce registre documente une vérification **datée**, pas une
  vérité permanente.
- Consigner systématiquement : identifiant, date « en vigueur depuis » lue sur
  la page, et date du jour de la vérification.
- En cas d'identifiants concurrents pour un même article (cf. §3, note
  L. 2122-22), retenir celui du domaine officiel `www.legifrance.gouv.fr` et
  signaler l'écart au lieu de le taire.

**Règle de non-héritage**

Tracer un article **ne trace pas son voisin**, même dans une même série très
cohérente : jusqu'au 2026-11-03, L. 1612-5 a été affiché « vérifié » sous un
identifiant de 1996 (§2). Chaque identifiant
inscrit dans ce fichier a été lu individuellement à la date indiquée ; aucune
extrapolation de série, de section de code ou de millésime n'est admise.

---

## Alertes de vigueur

- **Code des juridictions financières — réforme de la responsabilité
  financière (ordonnance n° 2022-408, décret n° 2022-1605)** : L. 131-2,
  L. 131-3, L. 131-4, L. 131-14 et L. 131-15 sont lus (§5) ; les autres
  articles d'infractions et la section 3 des sanctions, modifiée par la loi
  n° 2026-103, ne le sont pas. Ne jamais citer un numéro non lu de cette
  matière sans revérification immédiate.
- **CGCT, série L. 1612-\*** : cause identifiée le 2026-11-03 :
  ordonnance n° 2025-526, art. 1, applicable à compter de l'exercice 2026
  (§2). Les nouveaux articles L. 1612-21 à L. 1612-41 et le sort des articles
  communaux abrogés (dont L. 2322-1 et L. 2322-2, dépenses imprévues) restent
  à lire avant toute citation.
- **Obligation de dépôt des fonds au Trésor** : le texte posant le principe
  lui-même (par opposition aux seuls articles de dérogation L. 1618-1 et
  L. 1618-2) reste à identifier avec certitude (§6). Ne pas présumer qu'il
  s'agit du décret n° 2012-1246 sans vérification spécifique.
- **Décret n° 2016-841 du 24 juin 2016** (contenu du rapport d'orientation
  budgétaire) : texte repéré mais non ouvert lors de cette passe ; son
  identifiant n'est pas encore consigné ici (§1).

Aucune date d'évolution future n'est avancée pour ces points : seule
l'existence du doute est actée, conformément à la règle de provenance — un
registre honnêtement incomplet vaut mieux qu'un registre plausible et faux.
