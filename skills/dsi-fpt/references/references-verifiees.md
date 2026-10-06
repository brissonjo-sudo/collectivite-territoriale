# Références vérifiées

> **Ce fichier est le seul du dépôt autorisé à contenir des identifiants
> officiels en dur** (`LEGIARTI`, `JORFTEXT`, numéros CELEX), parce qu'ils y
> sont **vérifiés et datés**. Toute référence absente d'ici se **réserve**
> (« à confirmer en version consolidée ») ou se **retire** d'une réponse : un
> identifiant ne se reconstitue jamais de mémoire.
>
> **Aucune valeur chiffrée ici** (montant, seuil, délai, date d'échéance) :
> elles sont dans `cache-valeurs.md`, avec leur date de lecture.
>
> **Vérification du 2026-10-05.** Droit français : API Légifrance (outils
> `Droit_Francais`, `search_articles` et `get_article`), texte de chaque article
> lu. Textes entiers non codifiés (`JORFTEXT`) : page Légifrance lue par
> WebFetch, signalé. Droit de l'Union : textes officiels en français lus sur
> CELLAR (Office des publications de l'Union européenne). Les fichiers de
> travail détaillés sont dans `docs/socle/`.
>
> **Colonne « Collectivités »** : `oui` · `non` · `sous conditions`, avec le
> fondement lu. `inférence` signale une applicabilité déduite d'un terme
> général (« personnes morales de droit public », « autorités
> administratives ») et non d'une mention expresse.
>
> **Statuts** : `vérifié` (lu à la date indiquée) · `⚠️ non vérifié` (la
> référence reste utilisable par son objet, jamais par un identifiant ou un
> contenu non lu).

---

## 1. Administration, usagers et saisine par voie électronique (CRPA)

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Définition de l'« administration » pour tout le code | CRPA, art. L. 100-3 | LEGIARTI000031367308 | 2016-01-01 | vérifié | **Oui, expressément** : « les collectivités territoriales, leurs établissements publics administratifs » |
| Droit de saisir une administration par voie électronique | CRPA, art. L. 112-8 | LEGIARTI000031367348 | 2016-01-01 | vérifié | Oui, sauf démarches exclues (décret 2016-1491) |
| Téléservices ; le téléservice dédié devient la voie régulière de saisine | CRPA, art. L. 112-9 | LEGIARTI000031367350 | 2016-01-01 | vérifié | Oui, sauf démarches exclues |
| Exclusion de certaines démarches par décret en Conseil d'État | CRPA, art. L. 112-10 | LEGIARTI000033221175 | 2018-05-25 | vérifié | Oui (base des exceptions) |
| Identification de la personne qui saisit par voie électronique | CRPA, art. R. 112-9-1 | LEGIARTI000033288123 | 2016-11-07 | vérifié | Oui |
| Information du public sur les téléservices ; à défaut, tout envoi électronique vaut saisine | CRPA, art. R. 112-9-2 | LEGIARTI000033288120 | 2016-11-07 | vérifié | Oui |
| Accusé de réception électronique de tout envoi et paiement par téléservice | CRPA, art. L. 112-11 | LEGIARTI000033219980 | 2016-10-09 | vérifié | Oui ; exception pour envois abusifs ou menaçant la sécurité du SI |
| Exceptions à la saisine électronique propres aux collectivités | Décret n° 2016-1491 du 4 novembre 2016, art. 1 ; annexe 1 (exceptions définitives) ; annexe 2 (transitoires, échues) | JORFTEXT000033342129 (WebFetch) ; art. 1 : LEGIARTI000033343854 ; annexe 1 : LEGIARTI000033343812 ; annexe 2 : LEGIARTI000037563558 | 2016-11-07 (annexe 2 : 2018-11-07) | vérifié (articles) ; texte entier par WebFetch | **Sous conditions** : seules les démarches listées en annexe 1 restent exclues |

## 2. Algorithmes publics et documents communicables (CRPA)

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Mention explicite sur une décision individuelle fondée sur un traitement algorithmique ; communication des règles sur demande | CRPA, art. L. 311-3-1 | LEGIARTI000033205535 | 2016-10-09 | vérifié | Oui ; réserve des secrets protégés (L. 311-5, 2°) |
| Contenu de la mention explicite | CRPA, art. R. 311-3-1-1 | LEGIARTI000034195878 | 2017-09-01 | vérifié | Oui |
| Informations communiquées sur demande (contribution du traitement, données, paramètres, opérations) | CRPA, art. R. 311-3-1-2 | LEGIARTI000034195881 | 2017-09-01 | vérifié | Oui ; réserve des secrets protégés |
| Publication en ligne des règles des principaux traitements algorithmiques | CRPA, art. L. 312-1-3 | LEGIARTI000033205516 | 2016-10-09 | vérifié (article) ; **⚠️ seuil d'effectif non vérifié** | **Sous conditions** : exception sous un seuil d'agents fixé par décret, **décret non identifié** |
| Documents administratifs communicables, dont les codes sources | CRPA, art. L. 300-2 | LEGIARTI000033218936 | 2016-10-09 | vérifié | **Oui, expressément** : documents produits ou reçus « par l'Etat, les collectivités territoriales » |

## 3. Échanges de données entre administrations (CRPA)

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Échange des données nécessaires entre administrations (« dites-le-nous une fois ») | CRPA, art. L. 114-8 | LEGIARTI000045213315 | 2022-02-23 | vérifié | Oui, avec dérogation en cas d'impossibilité technique |
| Modalités des échanges renvoyées à un décret en Conseil d'État | CRPA, art. L. 114-9 | LEGIARTI000045213308 | 2022-02-23 | vérifié | Oui |
| Données fournies par la personne quand l'échange est impossible | CRPA, art. L. 114-10 | LEGIARTI000037313148 | 2018-08-12 | vérifié | Oui |

## 4. Sécurité des systèmes d'information des autorités administratives (RGS)

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Ordonnance sur les échanges électroniques (texte) | Ordonnance n° 2005-1516 du 8 décembre 2005 | JORFTEXT000000636232 (WebFetch) | — | vérifié par WebFetch ; ⚠️ LEGITEXT non confirmé | — |
| Définition des « autorités administratives » | Ordonnance n° 2005-1516, art. 1 | LEGIARTI000033974978 | 2017-01-29 | vérifié | **Oui, expressément** : « les collectivités territoriales » |
| Création du RGS ; l'autorité qui met en place un SI en détermine les fonctions de sécurité et respecte le RGS | Ordonnance n° 2005-1516, art. 9 | LEGIARTI000006317203 | 2005-12-09 | vérifié | Oui (via art. 1) |
| Décret RGS (texte) | Décret n° 2010-112 du 2 février 2010 | JORFTEXT000021779444 (WebFetch) | — | vérifié par WebFetch | — |
| Objet du RGS | Décret n° 2010-112, art. 1 | LEGIARTI000021780146 | 2010-02-05 | vérifié | Oui (inférence) |
| Approbation du RGS par arrêté du Premier ministre | Décret n° 2010-112, art. 2 | LEGIARTI000039286010 | 2019-10-28 | vérifié | Sans objet direct |
| Analyse de risques, objectifs et fonctions de sécurité, réexamen régulier | Décret n° 2010-112, art. 3 | LEGIARTI000021780150 | 2010-02-05 | vérifié | Oui (inférence) |
| Recours à des produits et prestataires qualifiés ou conformes | Décret n° 2010-112, art. 4 | LEGIARTI000021780154 | 2010-02-05 | vérifié | Oui (inférence) |
| **Attestation formelle** de sécurité par l'autorité elle-même ; rendue accessible aux usagers d'un téléservice | Décret n° 2010-112, art. 5 | LEGIARTI000033232490 | 2016-03-19 | vérifié | **Oui (inférence)** : c'est la collectivité qui atteste ; voir encadré |
| Qualification des produits de sécurité par l'ANSSI | Décret n° 2010-112, art. 6 et 9 | LEGIARTI000021780156 ; LEGIARTI000039353401 | 2010-02-05 ; 2019-11-09 | vérifié | Sans objet direct (produits, pas systèmes) |

> **Vocabulaire opposable, à deux niveaux.** Le **décret** n° 2010-112 (articles
> lus) prévoit que l'autorité administrative **atteste formellement** la
> sécurité de son système (art. 5). Le **référentiel** RGS (document approuvé
> par arrêté, publié par l'ANSSI, section 15) décrit la démarche qui y conduit
> sous le nom d'**homologation de sécurité**. Les deux termes sont exacts à leur
> niveau ; c'est la collectivité qui homologue et atteste pour ses propres
> systèmes. L'ANSSI **qualifie des produits** : elle n'homologue pas les
> systèmes d'une collectivité. Les articles 7, 8 et 10 à 24 du décret n'ont pas
> été relus (⚠️). L'art. 5 renvoie à l'art. L. 112-10 du CRPA pour la décision
> de création d'un téléservice, objet que cet article ne traite plus : renvoi à
> ne pas relayer.

## 5. Accessibilité numérique

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Loi pour l'égalité des droits et des chances (texte) | Loi n° 2005-102 du 11 février 2005 | JORFTEXT000000809647 (WebFetch) | — | vérifié par WebFetch | — |
| Obligation d'accessibilité des services en ligne ; déclaration, schéma pluriannuel, mention en page d'accueil | Loi n° 2005-102, art. 47 | LEGIARTI000048050213 | 2023-09-08 | vérifié | **Oui (inférence)** : « personnes morales de droit public » ; exception de charge disproportionnée (II) |
| Contrôle et sanction par l'Arcom, après mise en demeure publique | Loi n° 2005-102, art. 47-1 | LEGIARTI000048050174 | 2023-09-08 | vérifié | Oui (inférence) ; montants dans le cache |
| Décret accessibilité (texte) | Décret n° 2019-768 du 24 juillet 2019 | JORFTEXT000038811937 (WebFetch) | — | vérifié par WebFetch | — |
| Accessibilité selon les normes harmonisées de l'Union | Décret n° 2019-768, art. 1 | LEGIARTI000054748661 | 2026-08-27 | vérifié | Oui (inférence) |
| Seuil de chiffre d'affaires des entreprises soumises | Décret n° 2019-768, art. 2 | LEGIARTI000038956842 | 2019-07-26 | vérifié | **Non** (entreprises seulement) |
| Référentiel d'accessibilité arrêté par les ministres | Décret n° 2019-768, art. 5 | LEGIARTI000054748666 | 2026-08-27 | vérifié | Oui (inférence) |
| Publication et contenu de la déclaration d'accessibilité | Décret n° 2019-768, art. 6 | LEGIARTI000038956852 | 2019-07-26 | vérifié | Oui |
| Définition de l'« organisme du secteur public » | Directive (UE) 2016/2102, art. 3, point 1 | CELEX 32016L2102 | — | vérifié | **Oui, expressément** : « les autorités régionales ou locales » |

> Les articles 1 et 5 du décret n° 2019-768 ont été modifiés le 2026-08-27 :
> revérifier le référentiel en vigueur avant de citer une version du RGAA.

## 6. Atteintes aux systèmes de traitement automatisé de données

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Accès ou maintien frauduleux | Code pénal, art. 323-1 | LEGIARTI000047052655 | 2023-01-26 | vérifié | Oui (protection des systèmes de la collectivité) ; l'aggravation vise les systèmes à caractère personnel « mis en œuvre par l'Etat » |
| Entrave ou altération du fonctionnement | Code pénal, art. 323-2 | LEGIARTI000030939443 | 2015-07-27 | vérifié | Oui |
| Introduction, extraction, modification frauduleuse de données | Code pénal, art. 323-3 | LEGIARTI000030939448 | 2015-07-27 | vérifié | Oui |
| Outils d'attaque, sauf motif légitime (recherche, sécurité informatique) | Code pénal, art. 323-3-1 | LEGIARTI000028345220 | 2013-12-20 | vérifié | Sous conditions : la réserve de motif légitime couvre les audits et tests commandés |
| Association en vue de commettre ces infractions | Code pénal, art. 323-4 | LEGIARTI000006418325 | 2004-06-22 | vérifié | Oui |
| Bande organisée | Code pénal, art. 323-4-1 | LEGIARTI000047052660 | 2023-01-26 | vérifié | Oui |
| Peines complémentaires des personnes physiques | Code pénal, art. 323-5 | LEGIARTI000006418326 | 1994-03-01 | vérifié | Oui (agents ou prestataires auteurs) |
| Peines des personnes morales | Code pénal, art. 323-6 | LEGIARTI000020630782 | 2009-05-14 | vérifié | Sous conditions (art. 121-2) |
| Tentative | Code pénal, art. 323-7 | LEGIARTI000006418329 | 2004-06-22 | vérifié | Oui |
| Exclusion des mesures des services de renseignement de l'État | Code pénal, art. 323-8 | LEGIARTI000030938304 | 2015-07-27 | vérifié | **Non** |
| Responsabilité pénale des personnes morales ; collectivités limitées aux activités délégables | Code pénal, art. 121-2 | LEGIARTI000006417204 | 2005-12-31 | vérifié | **Sous conditions**, expressément |

## 7. Assurance du risque cyber

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| L'indemnisation d'une atteinte à un système de traitement automatisé est subordonnée à une plainte de la victime dans un délai fixé | Code des assurances, art. L12-10-1 | LEGIARTI000047048152 | 2023-04-24 | vérifié | **Sous conditions** : personnes morales et activité professionnelle ; seulement si le contrat contient une telle garantie. **Le texte ne mentionne pas la rançon.** |

## 8. Directive NIS2 et transposition

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Option nationale d'appliquer la directive aux entités de l'administration publique au niveau local | Directive (UE) 2022/2555, art. 2 § 5 | CELEX 32022L2555 | — | vérifié | **Sous conditions** : dépend du choix de la loi française |
| Délai de transposition | Directive (UE) 2022/2555, art. 41 | CELEX 32022L2555 | — | vérifié | Sans effet direct |
| Loi française de transposition (projet « résilience des infrastructures critiques et renforcement de la cybersécurité ») | Dossier législatif de l'Assemblée nationale | — | — | **⚠️ non publiée au 2026-10-05** | **Non applicable à ce jour** |

> **Règle opposable.** Ne jamais écrire qu'une collectivité « est soumise à
> NIS2 ». Au 2026-10-05, aucune loi de transposition n'est publiée et la
> directive laisse le niveau local à l'option de chaque État. Les seuils de
> population figurant dans les versions du projet divergent : aucun n'est
> retenu. À revérifier à chaque revue du socle.

## 9. Organisation, mutualisation et numérique responsable

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Services communs entre un EPCI à fiscalité propre et ses communes | CGCT, art. L5211-4-2 | LEGIARTI000045213577 | 2022-02-23 | vérifié | **Sous conditions** : EPCI à fiscalité propre et communes membres ; convention, fiche d'impact, avis des comités sociaux territoriaux |
| Biens partagés entre un EPCI à fiscalité propre et ses communes | CGCT, art. L5211-4-3 | LEGIARTI000023260130 | 2010-12-18 | vérifié | Sous conditions, même périmètre |
| Stratégie numérique responsable de certaines communes et EPCI | Loi n° 2021-1485 du 15 novembre 2021, art. 35 | LEGIARTI000044328507 ; loi : JORFTEXT000044327272 (WebFetch) | 2021-11-17 | vérifié | **Sous conditions** : seuil de population (cache) ; ⚠️ décret d'application non vérifié |

## 10. Cloud et hébergement

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Critères de sécurité et de protection contre l'accès d'autorités d'États tiers pour les données sensibles hébergées en cloud | Loi n° 2024-449 du 21 mai 2024 (SREN), art. 31 | LEGIARTI000049565888 ; loi : JORFTEXT000049563368 (lu dans une URL) | 2024-05-23 | vérifié (article) | **Non** : vise « les administrations de l'Etat, ses opérateurs » et certains GIP ; ⚠️ décret d'application non vérifié |
| Définition du « client » d'un fournisseur de services de traitement de données | Règlement (UE) 2023/2854 (Data Act), art. 2, point 30 | CELEX 32023R2854 | — | vérifié | **Oui** : « une personne physique ou morale » sous contrat, sans exclusion des personnes publiques |
| Suppression progressive des frais de changement de fournisseur | Règlement (UE) 2023/2854, art. 29 | CELEX 32023R2854 | — | vérifié | **Oui (bénéficiaire)** ; dates dans le cache |

> **Règle opposable.** La loi SREN (art. 31) et la doctrine « cloud au centre »
> visent l'État. Elles ne s'imposent pas à une collectivité. Le skill peut les
> citer comme **référence de bonne pratique**, jamais comme obligation.

## 11. Intelligence artificielle

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Définition du « déployeur » | Règlement (UE) 2024/1689, art. 3, point 4 | CELEX 32024R1689 | — | vérifié | **Oui, expressément** : « une autorité publique » |
| Analyse d'impact sur les droits fondamentaux avant déploiement de certains systèmes à haut risque | Règlement (UE) 2024/1689, art. 27 | CELEX 32024R1689 ; consolidé 02024R1689-20260727 | selon art. 113 | vérifié | **Sous conditions** : « déployeurs qui sont des organismes de droit public » |
| Haut risque : éligibilité aux prestations et services d'aide sociale essentiels | Règlement (UE) 2024/1689, annexe III, point 5 a) | CELEX 32024R1689 | selon art. 113 | vérifié | **Sous conditions** : systèmes « utilisés par les autorités publiques ou en leur nom » |
| Calendrier d'application, tel que modifié | Règlement (UE) 2024/1689, art. 113 (version consolidée au 2026-07-27) | consolidé 02024R1689-20260727 | — | vérifié | Commun ; dates dans le cache |
| Règlement modificatif (« omnibus numérique sur l'IA ») ; échéance propre aux systèmes à haut risque des autorités publiques | Règlement (UE) 2026/1744 du 8 juillet 2026 | CELEX 32026R1744 | publié le 2026-07-24 | vérifié | **Oui, sous conditions** ; date dans le cache |
| Identification biométrique à distance en temps réel à des fins répressives : autorisation préalable | Règlement (UE) 2024/1689, art. 5 | CELEX 32024R1689 | selon art. 113 | vérifié (ce passage) ; ⚠️ liste complète non relue | **Frontière** : sert au garde-fou surveillance et au renvoi `dpm-fpt`, jamais de mode d'emploi |

> Une version consolidée de l'Union « n'a aucun effet juridique » : la
> référence opposable reste le règlement 2024/1689 et ses modificatifs.

## 12. Contrats informatiques et facturation électronique

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| CCAG des marchés de techniques de l'information et de la communication (arrêté d'approbation) | Arrêté du 30 mars 2021 | JORFTEXT000043310689 (WebFetch) ; art. 39 : LEGIARTI000043320046 | 2021-04-01 | vérifié | **Sous conditions** : applicable seulement si le marché s'y réfère |
| Référence facultative aux CCAG dans les clauses du marché | CCP, art. R2112-2 | LEGIARTI000037730993 | 2019-04-01 | vérifié | Oui |
| Pouvoirs adjudicateurs | CCP, art. L1211-1 | LEGIARTI000037703308 | 2019-04-01 | vérifié | Oui (« personnes morales de droit public ») |
| Modification d'un marché sans nouvelle mise en concurrence | CCP, art. L2194-1 | LEGIARTI000037703841 | 2019-04-01 | vérifié | Oui |
| Résiliation : principe, force majeure, faute ou intérêt général, cas d'exclusion | CCP, art. L2195-1 à L2195-4 | LEGIARTI000037703847 ; LEGIARTI000037703849 ; LEGIARTI000037703851 ; LEGIARTI000042657215 | 2019-04-01 (L2195-4 : 2020-12-09) | vérifié | Oui (L2195-3 : contrat administratif) |
| Factures électroniques transmises par les titulaires de marchés | CCP, art. L. 2192-1 | LEGIARTI000046195587 | 2024-07-01 | vérifié | Oui (inférence) : obligation **des fournisseurs** |
| Acceptation des factures électroniques par les personnes publiques | CCP, art. L. 2192-2 | LEGIARTI000046195584 | 2024-07-01 | vérifié | Oui (inférence) : obligation **de la collectivité** |
| Acceptation des factures conformes à la norme | CCP, art. L. 2192-3 | LEGIARTI000038541739 | 2019-07-22 | vérifié | Oui (inférence) |
| Portail public de facturation (version en vigueur jusqu'au changement de version) | CCP, art. L. 2192-5 | LEGIARTI000053546705 | 2026-02-21 | vérifié | **Oui, expressément** : « les collectivités territoriales » |
| Portail public de facturation (version future) | CCP, art. L. 2192-5 | LEGIARTI000054567709 | version future (date dans le cache) | vérifié | Oui, expressément |
| Exclusions du dispositif | CCP, art. L. 2192-6 | LEGIARTI000038960975 | 2020-01-01 | vérifié | Aucune exclusion ne vise une collectivité |

> **Frontière.** Ces références servent l'**exécution** des contrats. La
> passation (procédure, critères, publicité) est hors périmètre et ne
> s'illustre pas.

## 13. Identification électronique et interopérabilité (Union)

| Objet | Référence | Identifiant | En vigueur depuis | Statut | Collectivités |
|---|---|---|---|---|---|
| Identification électronique et services de confiance | Règlement (UE) n° 910/2014 (eIDAS), modifié par le règlement (UE) 2024/1183 | CELEX 32014R0910 ; 32024R1183 | — | vérifié (existence et objet) ; **⚠️ obligations des organismes publics et dates non relues** | ⚠️ non vérifié |
| Définition de l'« organisme du secteur public » par renvoi à la directive (UE) 2019/1024 | Règlement (UE) 2024/903, art. 2, point 6 | CELEX 32024R0903 | ⚠️ dates non relues | vérifié (définition) | ⚠️ non vérifié (directive 2019/1024 non lue) |

## 14. Frontière avec `dpo-ct` (pointeurs seulement)

| Objet | Référence | Identifiant | Statut | Traitement |
|---|---|---|---|---|
| Sécurité du traitement | RGPD, art. 32 | CELEX 32016R0679 | vérifié (intitulé) | Régime traité par `dpo-ct` |
| Notification à l'autorité de contrôle d'une violation de données | RGPD, art. 33 | CELEX 32016R0679 | vérifié (intitulé) | Régime traité par `dpo-ct` |

## 15. Doctrine d'appui et référentiels

> **Doctrine d'appui : non normative, sauf texte contraire cité.** Versions et
> dates de publication : `cache-valeurs.md`. Lus le 2026-10-05 sur les sites
> officiels (détail et URL : `docs/socle/lot-4-doctrine.md`).

### 15.1 Référentiels rendus obligatoires par un texte

| Référentiel | Éditeur | Texte qui le rend opposable | Statut | Collectivités |
|---|---|---|---|---|
| Référentiel général de sécurité (RGS) | ANSSI, avec la DINUM | Ordonnance n° 2005-1516 et décret n° 2010-112 (§4) ; arrêté d'approbation cité par la page ANSSI (⚠️ arrêté non relu sur Légifrance) | vérifié (page ANSSI et document) | **Oui** : la page ANSSI cite expressément « les collectivités territoriales ». Démarche d'homologation de sécurité et analyse de risques exigées ; le reste est présenté comme recommandations |
| Référentiel général d'amélioration de l'accessibilité (RGAA) | DINUM | Loi n° 2005-102, art. 47, et décret n° 2019-768, art. 5 (§5) : méthode technique de vérification | vérifié (version) ; ⚠️ date propre de la version et références de l'arrêté non affichées | **Oui** (personnes morales de droit public) ; une nouvelle version majeure est annoncée, à revérifier |
| Référentiel général d'interopérabilité (RGI) | DINUM | Officialisé par arrêté (via WebFetch, ⚠️ arrêté non relu sur Légifrance) | vérifié (document) | **Sous conditions** : le document se déclare applicable à « l'ensemble des autorités administratives », dont les collectivités ; portée exacte de ses règles à qualifier |

### 15.2 Doctrine non normative

| Document | Éditeur | Statut | Portée pour une collectivité |
|---|---|---|---|
| Guide d'hygiène informatique | ANSSI | vérifié | Bonne pratique ; aucun texte ne le rend obligatoire |
| Méthode EBIOS Risk Manager | ANSSI | vérifié | Bonne pratique ; méthode d'analyse de risques au libre choix de la collectivité |
| Référentiel SecNumCloud (exigences des prestataires) | ANSSI | vérifié | **S'impose aux prestataires qui demandent la qualification, pas aux acheteurs** ; préconisé pour les données sensibles |
| Catalogue des offres qualifiées | ANSSI | vérifié (mis à jour chaque mois) | Outil de vérification avant achat, à consulter à la date de la décision |
| Doctrine « cloud au centre » (circulaire du Premier ministre) | Premier ministre, DINUM | vérifié via WebFetch | **Vise l'État** (destinataires : membres du gouvernement). Bonne pratique seulement pour une collectivité. **Piège** : la traduction anglaise de la règle R5 dit « local authorities » là où le français dit « l'administration » ; se référer au texte français |
| CERT-FR | ANSSI | vérifié | Périmètre prioritaire : État, opérateurs d'importance vitale et de services essentiels ; pas l'interlocuteur de première ligne d'une collectivité |
| CSIRT territoriaux et centres de ressources cyber | ANSSI ; liste sur le site du CERT-FR | vérifié | **Nomment expressément les collectivités** ; réponse à incident de premier niveau gratuite ; aucune obligation de recours. Citer la liste nominative, pas un décompte (les pages officielles se contredisent) |
| Plateforme d'assistance aux victimes | dispositif national | ⚠️ non vérifié (site inaccessible) | Ne rien affirmer de son offre sans lecture directe |
| Guide « Cybersécurité : toutes les communes et intercommunalités sont concernées » | ANSSI et AMF | vérifié | Bonne pratique ; guide daté, à croiser avec le droit en vigueur |
| Guide « Sécurité numérique des collectivités territoriales : l'essentiel de la réglementation » | ANSSI | vérifié | Synthèse datée : ne reflète pas le droit actuel, textes à revérifier |
| Guide sur les obligations et responsabilités des collectivités en cybersécurité | Cybermalveillance.gouv.fr et CNIL | vérifié (titre) ; ⚠️ date non lue | Informe, ne crée pas d'obligation |
| Guide de sensibilisation au RGPD pour les collectivités | CNIL | vérifié (titre) ; ⚠️ date non lue | Périmètre `dpo-ct` |
| Kit d'exercice de crise cyber pour les collectivités | ANSSI | vérifié (existence) | Outil d'entraînement, emploi libre |
