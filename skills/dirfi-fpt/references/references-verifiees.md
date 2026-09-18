# Références vérifiées sur Légifrance

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
> Vérifications effectuées le **2026-09-15**, par consultation directe de
> légifrance.gouv.fr (`WebFetch`) et par recherche ciblée renvoyant une page
> Légifrance nommément identifiée (`WebSearch`). Un statut `vérifié` signifie
> que l'identifiant a été **lu**, à cette date, sur une page ou un résultat de
> recherche pointant explicitement vers cette page — jamais reconstitué. Un
> statut `⚠️ non vérifié` signifie que la tentative n'a pas abouti à un
> identifiant univoque : la référence reste utilisable **par son objet et sa
> désignation usuelle**, mais son identifiant Légifrance doit être revérifié
> avant toute citation dans un acte.

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
| Définition de l'équilibre réel du budget | CGCT, art. **L. 1612-4** | LEGIARTI000006389562 | 2026-09-15 | vérifié |
| Saisine de la chambre régionale des comptes — budget non adopté | CGCT, art. **L. 1612-2** | LEGIARTI000051731704 | 2026-09-15 | vérifié (cf. §1) |
| Saisine de la chambre régionale des comptes — budget non voté en équilibre réel | CGCT, art. **L. 1612-5** | LEGIARTI000006389622 | 2026-09-15 | vérifié — article ouvert directement sur Légifrance |
| Saisine de la chambre régionale des comptes — compte administratif arrêté en déficit | CGCT, art. **L. 1612-14** | LEGIARTI000006389570 | 2026-09-15 | vérifié |
| Saisine de la chambre régionale des comptes — dépense obligatoire non inscrite ou insuffisamment inscrite | CGCT, art. **L. 1612-15** | LEGIARTI000006389571 | 2026-09-15 | vérifié |

> **Note méthode** : la série L. 1612-* forme un mécanisme unique (saisine du
> préfet → délai d'un mois de la CRC → proposition → arrêté préfectoral motivé
> en cas d'écart). **Ne pas déduire** l'identifiant d'un article de la série à
> partir d'un autre déjà vérifié : chaque article a été recherché
> individuellement, et **L. 1612-5 reste non vérifié** malgré la confirmation
> de ses voisins immédiats — c'est exactement le cas que la règle de
> non-héritage (`socle-sources-verification.md` §8) vise à couvrir.

---

## 3. Compétences et délégations

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| Dépenses obligatoires des communes (liste) | CGCT, art. **L. 2321-2** | LEGIARTI000049312829 | 2026-09-15 | vérifié |
| Délégations que le conseil municipal peut consentir au maire, dont le recours à l'emprunt (3°) dans les limites fixées par l'assemblée | CGCT, art. **L. 2122-22** | LEGIARTI000045212383 | 2026-09-15 | vérifié — voir réserve ci-dessous |

> **Réserve L. 2122-22** : la recherche a fait apparaître **deux identifiants
> distincts** pour cet article — `LEGIARTI000045212383` (domaine
> `www.legifrance.gouv.fr`, retenu ici) et `LEGIARTI000037666566` (renvoyé par
> un sous-domaine `circulaire.legifrance.gouv.fr`, probablement une version
> antérieure ou un miroir de cache). **Le second n'est pas retenu.** À
> reconfirmer par ouverture directe de la page lors de la prochaine revue —
> même précaution que celle documentée dans le registre du skill frère
> (`Dpm-fpt`) pour un cas structurellement identique.
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
| Infractions et sanctions du régime unifié de responsabilité financière, codifiées au code des juridictions financières (section 2, chapitre Ier, titre III) | Code des juridictions financières, art. **L. 131-9 et suivants** (numérotation à confirmer précisément) | — | 2026-09-15 | ⚠️ non vérifié — à confirmer en version consolidée |
| Définition de la gestion de fait (maniement de deniers publics sans qualité de comptable public) | Code des juridictions financières, art. **L. 131-15** (candidat le plus probable, non confirmé comme article définitoire unique) | LEGIARTI000045400562 (identifiant vu, portée exacte non confirmée) | 2026-09-15 | ⚠️ non vérifié — à confirmer en version consolidée |

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

Aucune décision de chambre régionale des comptes, de la Cour des comptes ou du
Conseil d'État n'a été vérifiée par consultation directe lors de cette passe
(le périmètre demandé portait sur des articles-pivots, pas sur la
jurisprudence). Toute décision citée dans une réponse du skill doit donc, en
l'état de ce registre, être **réservée** :

| Objet | Référence | Identifiant | Date de vérification | Statut |
|---|---|---|---|---|
| — | — | — | — | ⚠️ non vérifié — section à alimenter à la première vérification effective d'une décision |

> Rappel de méthode (aligné sur le registre du skill frère `Dpm-fpt`, §7) :
> une décision juridictionnelle se cite **comme un article** — juridiction,
> formation, date, numéro de requête ou de décision, identifiant, et date de
> vérification — jamais par son seul nom d'usage.

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
cohérente (L. 1612-2, L. 1612-4, L. 1612-14 et L. 1612-15 sont vérifiés ; leur
voisin immédiat **L. 1612-5 ne l'est pas** — voir §2). Chaque identifiant
inscrit dans ce fichier a été lu individuellement à la date indiquée ; aucune
extrapolation de série, de section de code ou de millésime n'est admise.

---

## Alertes de vigueur

- **Code des juridictions financières — réforme de la responsabilité
  financière (ordonnance n° 2022-408, décret n° 2022-1605)** : la
  recodification des articles relatifs aux infractions, aux sanctions et à la
  gestion de fait n'a pas pu être stabilisée dans ce registre (§5). C'est le
  point de vigilance prioritaire du skill : ne jamais citer un numéro
  d'article précis de cette matière sans revérification immédiate.
- **CGCT, série L. 1612-\*** : plusieurs articles de cette section portent une
  date « en vigueur depuis le 01/01/2026 », signe d'une recodification ou
  renumérotation récente touchant tout le chapitre. Revérifier l'ensemble de
  la section (pas seulement les articles isolément cités ici) à la prochaine
  revue, y compris les articles non repris dans ce registre.
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
