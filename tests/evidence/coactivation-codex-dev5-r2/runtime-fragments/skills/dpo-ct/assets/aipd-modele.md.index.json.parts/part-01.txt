# Générateur — AIPD (analyse d'impact, méthode CNIL)

## 1. Objet et cas d'usage

Produire la **trame d'une analyse d'impact relative à la protection des
données** (art. 35 RGPD — à confirmer en version consolidée) selon la
**méthode CNIL en 4 parties** : contexte, principes fondamentaux, risques,
validation. Le document appartient au responsable de traitement ; le DPO y
émet un avis mais ne la valide pas.

## 2. Questions à poser une à une

> Poser ces questions **une à une**, jamais en questionnaire massif.

0. **Préalable obligatoire — l'AIPD est-elle requise ?** Vérifier via
   `references/aipd.md` (listes CNIL obligatoire/dispensée, critères CEPD —
   matrice §2.2 : vérification de source requise). — *Pourquoi* : ne pas
   produire une AIPD inutile ni en omettre une obligatoire. — *Si doute* :
   instruire l'opportunité d'abord et le documenter ; une AIPD volontaire
   reste possible, le dire explicitement.
1. **Quel est le traitement concerné ?** (description, finalité, service
   porteur) — *Pourquoi* : objet de l'analyse. — *Si inconnu* : arrêter et
   demander les documents du projet.
2. **STOP RÉGIME — finalité pénale ?** — *Pourquoi* : garde-fou §5.2.b ; le
   régime Police-Justice change l'analyse. — *Si doute* :
   `references/analyse-situation.md` §2.
3. **Qui est le responsable de traitement, qui sont les sous-traitants ?**
   — *Pourquoi* : la partie « validation » leur revient. — *Défaut* :
   `[À COMPLÉTER]`, signalé bloquant.
4. **Quelles données, quelles personnes, quels supports ?** (données
   sensibles, mineurs, NIR ; matériels, logiciels, canaux, personnes ayant
   accès) — *Pourquoi* : matière première du contexte et des risques. —
   *Défaut* : `[INCOMPLET]`.
5. **Quel cycle de vie des données ?** (collecte → conservation → destruction,
   flux, durées avec leur source) — *Pourquoi* : partie « contexte » de la
   méthode CNIL. — *Si inconnu* : lister les étapes à documenter, sans
   inventer de durée.
6. **Quelles mesures existantes ou prévues ?** (juridiques : information,
   droits, contrats art. 28 ; techniques : chiffrement, traçabilité,
   sauvegardes, contrôle d'accès) — *Pourquoi* : nourrit « principes
   fondamentaux » et l'évaluation des risques. — *Défaut* : « aucune mesure
   communiquée » = constat, pas invention.
7. **Pour chacun des 3 risques (accès illégitime, modification non désirée,
   disparition) : quelles sources de risque, quels impacts redoutés ?**
   — *Pourquoi* : cœur de la partie « risques ». — *Si inconnu* : proposer
   des scénarios types du secteur, marqués « hypothèse à valider ».
8. **Le point de vue des personnes concernées a-t-il été recueilli ?**
   (ou motif de ne pas le recueillir) — *Pourquoi* : attendu de la méthode
   CNIL. — *Défaut* : « non recueilli — à motiver par le responsable de
   traitement ».
9. **L'outil PIA de la CNIL est-il utilisé ?** — *Pourquoi* : la CNIL fournit
   un logiciel PIA gratuit qui structure la même démarche ; la présente trame
   peut y être reportée. — *Défaut* : trame markdown seule.

## 3. Gabarit du document final

```
ANALYSE D'IMPACT RELATIVE À LA PROTECTION DES DONNÉES (AIPD)
[COLLECTIVITÉ] — Traitement : [NOM] — Version [N°] du [DATE]
Responsable de traitement : [RT] — DPO : [NOM] — Rédacteur : [NOM/SERVICE]
Caractère de l'AIPD : [OBLIGATOIRE (motif + source datée) / VOLONTAIRE]
Régime : [RGPD / Police-Justice — à confirmer]

PARTIE 1 — CONTEXTE
1.1 Vue d'ensemble : [finalités, enjeux, responsable, sous-traitants]
1.2 Données, traitements, supports : [catégories de données et de personnes,
    cycle de vie, matériels et logiciels, personnes ayant accès]

PARTIE 2 — PRINCIPES FONDAMENTAUX
2.1 Proportionnalité et nécessité : [finalité déterminée ; base légale ;
    minimisation ; exactitude ; durées de conservation AVEC SOURCE]
2.2 Mesures protectrices des droits : [information ; consentement le cas
    échéant ; accès et portabilité ; rectification et effacement ; opposition
    et limitation ; sous-traitance (art. 28) ; transferts hors UE]

PARTIE 3 — RISQUES LIÉS À LA SÉCURITÉ DES DONNÉES
Pour chaque risque : sources de risque, menaces, impacts potentiels sur les
personnes, mesures existantes ou prévues, puis cotation.
3.1 Accès illégitime aux données : gravité [négligeable / limitée /
    importante / maximale] × vraisemblance [idem] → [NIVEAU]
3.2 Modification non désirée des données : gravité [x] × vraisemblance [x] → [NIVEAU]
3.3 Disparition des données : gravité [x] × vraisemblance [x] → [NIVEAU]

PARTIE 4 — VALIDATION
4.1 Cartographie des risques : [synthèse gravité × vraisemblance, avant/après mesures]
4.2 Plan d'action : | Mesure | Responsable | Échéance | Coût/charge | Avancement |
4.3 Avis du DPO : [avis motivé — recommandation, réserves éventuelles ;
    consultation préalable de la CNIL si risque résiduel élevé (art. 36 —
    à confirmer)]
4.4 Décision du responsable de traitement : [VALIDE / VALIDE AVEC CONDITIONS /
    REFUSE — la décision lui appartient ; date et signature]
4.5 Point de vue des personnes concernées : [RECUEILLI (modalités) /
    NON RECUEILLI (motif)]
Révision prévue le : [DATE — l'AIPD est un document vivant]
```

## 4. Règles de production

- **Ne jamais produire l'AIPD sans avoir tranché la question préalable**
  (requise ou non), source CNIL/CEPD datée à l'appui — sinon marquer
  « caractère obligatoire à confirmer ».
- **Jamais de donnée inventée** : cotation gravité × vraisemblance uniquement
  à partir d'éléments fournis ou d'hypothèses explicitement marquées
  « hypothèse à valider ». Champs essentiels manquants → brouillon
  `[INCOMPLET]` listant les champs à compléter.
- **Rôle consultatif** : le DPO émet l'avis (4.3), le responsable de
  traitement décide (4.4). Ne jamais fusionner les deux.
- **Références** : socle-sources — durées de conservation avec source
  (texte sectoriel, référentiel CNIL daté, décision locale documentée) ;
  articles cités avec « à confirmer en version consolidée » si non vérifiés
  en session ; doctrine CNIL/CEPD toujours datée.
- Personnes vulnérables (mineurs, action sociale) ou données sensibles →
  relever la gravité en conséquence (échelle §5.1).
- Mentionner l'outil PIA de la CNIL (cnil.fr) comme support possible.

## 5. Checklist finale avant remise

- [ ] Caractère obligatoire/volontaire de l'AIPD documenté avec source datée ?
- [ ] Régime applicable affiché ?
- [ ] Les 4 parties de la méthode CNIL présentes et remplies (ou `[INCOMPLET]`) ?
- [ ] Les 3 risques cotés en gravité × vraisemblance, avant/après mesures ?
- [ ] Durées de conservation sourcées (jamais inventées) ?
- [ ] Avis DPO distinct de la décision du responsable de traitement ?
- [ ] Consultation préalable CNIL évoquée si risque résiduel élevé ?
- [ ] Point de vue des personnes traité (recueilli ou motif) ?
- [ ] Date de révision prévue ?
