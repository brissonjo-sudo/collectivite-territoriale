# Socle — sources et vérification (DPO CT)

> Lire ce fichier dès qu'une réponse repose sur un texte, une doctrine ou une
> jurisprudence. La **méthode de vérification détaillée** (primarité, date de
> référence, hiérarchie des normes, citation traçable, abstention motivée)
> **n'est pas redéfinie ici** : elle relève du skill `recherche-juridique`. Ce
> fichier fournit la **carte des sources propres à la protection des données**
> et les **réflexes spécifiques** au métier de DPO en collectivité.
>
> **Accès rapide** — cas courant (une seule référence à qualifier) : lire
> seulement **§6** (règle de provenance) + **§7** (abstention). Cas de fond
> (nouveau traitement, avis complet) : lire **§1** (hiérarchie) + le réflexe
> concerné en **§4**. §2 (sources officielles) et §3 (textes structurants) se
> consultent en cas de doute sur *où* chercher, pas systématiquement.

---

## 1. Hiérarchie et articulation des sources

1. **Charte des droits fondamentaux de l'UE** (art. 7 et 8 — vie privée,
   protection des données — à confirmer) et **Constitution** : plancher de
   toute analyse touchant aux libertés.
2. **RGPD** (règlement (UE) 2016/679) — **effet direct**, s'applique sans
   transposition. Texte pivot du régime général.
3. **Directive (UE) 2016/680 « Police-Justice »** — traitements à finalité
   pénale, transposée en droit interne (voir 4). Ne s'applique jamais
   directement à un traitement communal : passer par la loi de transposition.
4. **Loi n° 78-17 « Informatique et Libertés »** (version consolidée) —
   marges de manœuvre nationales du RGPD (titre II), transposition
   Police-Justice (titre III), dispositions particulières. **Toujours lire le
   RGPD et la loi 78-17 ensemble** : la loi précise, complète ou déroge dans
   les marges permises.
5. **Décret n° 2019-536** (application de la loi 78-17) — procédures,
   modalités d'exercice des droits — à confirmer en version consolidée.
6. **Textes sectoriels** croisant le droit des données : CGCT, code du
   patrimoine (archives publiques, durées), CSI (vidéoprotection), code
   électoral, code de l'action sociale et des familles, code de l'éducation,
   CRPA (téléservices, open data), code général de la fonction publique
   (données RH). Le texte sectoriel peut fixer une durée ou une obligation
   qui s'impose au raisonnement RGPD.
7. **Jurisprudence CJUE** — interprétation authentique du RGPD (transferts,
   responsabilité conjointe, notion de traitement). Prime sur toute doctrine.
8. **Jurisprudence CE / juridictions françaises** — légalité des actes,
   contentieux CNIL, application aux personnes publiques.
9. **Décisions et sanctions CNIL (formation restreinte)** — portée
   individuelle mais valeur d'orientation forte.
10. **Doctrine CNIL** (référentiels, recommandations, lignes directrices,
    listes AIPD, FAQ) et **lignes directrices CEPD/EDPB** — non créatrices de
    droit mais structurantes en pratique : s'en écarter s'argumente. **Toujours
    dater la version.**
11. **Doctrine institutionnelle** (ANSSI, DINUM, AATF, associations de DPO,
    CNFPT) — utile pour la pratique, **jamais** suffisante pour fonder seule
    une affirmation normative.

**Règle de conflit** : norme supérieure prime ; à niveau égal, texte spécial
prime (*lex specialis* — ex. une durée fixée par le code du patrimoine prime
un raisonnement générique de minimisation) ; à défaut, texte le plus récent.
La doctrine ne prime jamais un texte ou la CJUE. **Signaler explicitement**
tout conflit détecté plutôt que de le masquer.

---

## 2. Sources officielles à privilégier

- **Légifrance** (legifrance.gouv.fr) — loi 78-17, décret 2019-536, codes
  sectoriels, version consolidée datée. Source des identifiants `LEGIARTI` /
  `JORFTEXT` / `NOR`.
- **EUR-Lex** (eur-lex.europa.eu) — RGPD et directive 2016/680 en version
  authentique, identifiants `CELEX`.
- **CNIL** (cnil.fr) — référentiels, recommandations, listes AIPD
  (obligatoire / dispensée), registre des sanctions, outil PIA, doctrine
  collectivités territoriales.
- **CEPD/EDPB** (edpb.europa.eu) — lignes directrices, avis, décisions
  contraignantes.
- **Curia** (curia.europa.eu) — jurisprudence CJUE.
- **conseil-etat.fr / Légifrance jurisprudence** — contentieux administratif
  des données.
- **ANSSI** (cyber.gouv.fr) — référentiels sécurité, en appui de l'art. 32.
- **DINUM / service-public.fr** — téléservices, échanges entre
  administrations (dites-le-nous-une-fois).

---

## 3. Noyau minimal embarqué (textes structurants à toujours situer)

Ces textes forment le socle de référence du métier. Ils ne dispensent
**jamais** de vérifier la version en vigueur à la date utile : ils indiquent
**où chercher**, pas la valeur figée du droit.

| Texte | Objet | Réflexe |
|---|---|---|
| **RGPD** | Régime général : principes (art. 5), bases légales (art. 6), données sensibles (art. 9), droits (art. 12 à 23), responsabilités (art. 24 à 31), sécurité et violations (art. 32 à 34), AIPD (art. 35-36), DPO (art. 37 à 39), transferts (chap. V) | Structure stable ; citer avec « à confirmer en version consolidée » si non vérifié en session |
| **Loi 78-17** | Marges nationales (mineurs, données sensibles, NIR), titre III Police-Justice | Numérotation remaniée en 2018-2019 : **ne jamais citer un article de mémoire** |
| **Décret 2019-536** | Modalités procédurales | À confirmer à chaque usage |
| **Code du patrimoine** | Archives publiques : le sort final des documents des collectivités relève du régime des archives | Croiser toute question de durée / effacement |
| **CSI** | Vidéoprotection (voie publique) | Volet autorisation → `dpm-fpt` ; volet données ici |
| **Référentiels et listes CNIL** | Durées sectorielles, AIPD obligatoire/dispensée | Vérifier la version en ligne, dater la citation |

---

## 4. Réflexes spécifiques DPO en collectivité

### Identifier le régime avant le fond
RGPD (régime général) ou titre III loi 78-17 (finalité pénale : prévention,
détection, poursuite d'infractions) ? La police municipale et la
vidéoverbalisation basculent souvent en Police-Justice ; la vidéoprotection
« tranquillité publique » reste généralement RGPD. Un même dispositif peut
relever des **deux régimes selon la finalité poursuivie**. En cas de doute :
vérifier (matrice §2.2), et afficher le STOP RÉGIME (`SKILL.md` §5.2.b).

### Désigner le responsable de traitement avant de conclure
Commune, EPCI, CCAS (personne morale distincte !), syndicat, État (maire
agissant au nom de l'État : état civil, élections — la répartition des rôles
diffère) : ne jamais analyser un traitement sans avoir nommé son responsable.
Les obligations, le registre et les réponses aux personnes en dépendent.

### Ne jamais retenir le consentement par défaut
Pour une personne publique, la base légale naturelle est la **mission
d'intérêt public** ou l'**obligation légale** (art. 6 RGPD — à confirmer).
Le consentement, rarement libre vis-à-vis d'une administration, ne se retient
que pour des traitements réellement facultatifs (newsletter, photos...).
Requalifier systématiquement un « consentement » annoncé.

### Suivre le renvoi jusqu'à la source qui contient la règle
Le RGPD renvoie à la loi nationale, la loi au décret, la CNIL à ses
référentiels. Une durée de conservation opposable vient d'un texte sectoriel,
d'un référentiel CNIL daté ou d'une décision locale documentée — pas d'une
intuition.

### Distinguer obligation et bonne pratique
Beaucoup de mesures recommandées par la CNIL sont des bonnes pratiques, pas
des obligations. Ne jamais présenter l'une pour l'autre : la recommandation
s'argumente, l'obligation se cite.

### Toujours dater la doctrine
Les référentiels CNIL et lignes directrices CEPD sont révisés régulièrement.
Citer « le référentiel CNIL [nom] dans sa version du [date] » ; signaler
qu'une version postérieure peut exister.

### Penser « personnes vulnérables » et « grande échelle »
Mineurs (scolaire, périscolaire), bénéficiaires de l'action sociale, personnes
âgées : la vulnérabilité des personnes élève le risque (échelle §5.1) et pèse
sur l'obligation d'AIPD. Une commune traite vite « à grande échelle » à
l'échelle de sa population.

### Croiser avec le régime des archives publiques
Tout document d'une collectivité est une archive publique : l'effacement
RGPD s'articule avec le code du patrimoine (visa du directeur des archives
départementales pour l'élimination — à confirmer). Ne jamais conclure
« supprimer » sans ce croisement.

---

## 5. Quand appeler `recherche-juridique`

- **Réforme récente** touchant la loi 78-17, le décret d'application ou un
  texte sectoriel.
- **Doctrine non stabilisée** : lignes directrices CEPD en consultation,
  référentiel CNIL en révision.
- **Jurisprudence complexe** : CJUE (transferts, responsabilité), CE
  (contentieux CNIL, actes des collectivités).
- **Identifiant officiel non récupéré** en session (`LEGIARTI`, `CELEX`,
  n° de délibération CNIL) : ne jamais le reconstituer de mémoire.
- **Doute sur le champ d'application** d'un texte sectoriel à un cas
  particulier.

---

## 6. Règle de provenance des identifiants

Tout identifiant officiel (`LEGIARTI`, `JORFTEXT`, `NOR`, `CELEX`, n° de
délibération CNIL, n° de requête) cité dans une sortie du skill **provient
obligatoirement d'un appel d'outil effectué dans la session**. Un identifiant
jamais récupéré :
- **ne se reconstitue jamais de mémoire** ;
- est **omis**, ou marqué `⚠️ non vérifié — identifiant non récupéré` ;
- **interdit** l'usage du gabarit de citation pour acte
  (cf. `recherche-juridique`, règle de provenance).

Un numéro d'article structurellement stable (ex. « art. 30 RGPD ») peut être
cité sans appel d'outil **uniquement** assorti de la réserve « à confirmer en
version consolidée », sauf s'il a été vérifié dans la session en cours
(mention « vérifié le JJ/MM/AAAA »). Pour la **loi 78-17**, dont la
numérotation a été profondément remaniée, la vérification en session est la
règle.

---

## 7. Abstention motivée

- Référence non vérifiable à la date utile → ne pas citer de mémoire ;
  signaler « à vérifier ».
- Régime applicable (RGPD / Police-Justice) indéterminable avec les éléments
  fournis → poser la question, ne pas présumer.
- Durée de conservation sans source identifiée → proposer la démarche
  (texte sectoriel ? référentiel CNIL ? décision locale documentée ?) sans
  inventer de valeur.
- Doctrine CNIL et texte en tension apparente → signaler la tension, ne pas
  arbitrer seul ; suggérer `recherche-juridique`.

L'abstention est **ciblée** : elle porte sur le point incertain et n'empêche
pas de livrer le reste de l'analyse.
