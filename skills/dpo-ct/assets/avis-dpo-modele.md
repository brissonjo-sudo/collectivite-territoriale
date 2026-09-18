# Générateur — Avis DPO sur un projet ou un traitement

## 1. Objet et cas d'usage

Produire un **avis formel du DPO** sur un projet, un traitement, une convention,
un marché ou un logiciel de la collectivité. C'est le livrable central du rôle
de conseil (art. 39 RGPD — à confirmer en version consolidée) : il analyse la
conformité, hiérarchise les recommandations et laisse la décision au
responsable de traitement.

## 2. Questions à poser une à une

> **Logique interactive obligatoire** : poser ces questions **une à une**,
> jamais en bloc. Passer à la suivante seulement après réponse (ou « je ne
> sais pas » acté). Si l'utilisateur a déjà fourni l'information, ne pas la
> redemander.

1. **Quel est le projet ou le traitement à analyser ?** (description libre)
   — *Pourquoi* : sans objet, pas d'avis. — *Si inconnu* : demander tout
   document disponible (cahier des charges, convention, note) ; sinon arrêter.
2. **Qui demande l'avis, et pour quelle échéance ?** (service, élu, DGS...)
   — *Pourquoi* : cadre l'en-tête et le niveau d'urgence. — *Défaut* :
   demandeur `[À COMPLÉTER]`, sans échéance.
3. **Quelle est la finalité précise du traitement ?** — *Pourquoi* : la
   finalité conditionne tout (base légale, régime, minimisation). — *Si
   inconnu* : reformuler à partir de la description et faire valider.
4. **STOP RÉGIME — le traitement poursuit-il une finalité pénale ?**
   (prévention, détection, poursuite d'infractions : PM, vidéoverbalisation...)
   — *Pourquoi* : garde-fou §5.2.b du SKILL — une analyse sous le mauvais
   régime est fausse. — *Si doute* : appliquer `references/analyse-situation.md`
   §2 avant de poursuivre.
5. **Qui est le responsable de traitement ?** (commune, EPCI, CCAS, État...)
   — *Pourquoi* : l'avis lui est adressé ; les obligations en dépendent. —
   *Si inconnu* : proposer une qualification argumentée, marquée « à valider ».
6. **Quelles catégories de données et de personnes ?** (dont sensibles,
   mineurs, bénéficiaires action sociale, NIR) — *Pourquoi* : fixe le niveau
   de risque (§5.1) et l'opportunité d'une AIPD. — *Défaut* : `[INCOMPLET]`.
7. **Quelle base légale est envisagée par le service ?** — *Pourquoi* : à
   requalifier si besoin (jamais le consentement par défaut pour une mission
   de service public). — *Si inconnu* : proposer mission d'intérêt public ou
   obligation légale, à vérifier (matrice §2.2).
8. **Y a-t-il des sous-traitants, un hébergement, des transferts hors UE ?**
   — *Pourquoi* : déclenche l'analyse art. 28 et chapitre V. — *Défaut* :
   « non communiqué » signalé comme point de vigilance.
9. **Quelles durées de conservation et mesures de sécurité sont prévues ?**
   — *Pourquoi* : deux points de contrôle systématiques. — *Si inconnu* :
   non-conformité potentielle relevée, pas de valeur inventée.
10. **Le DPO est-il impliqué dans le projet analysé ?** — *Pourquoi* :
    détecter un conflit d'intérêts (art. 38.6 RGPD — à confirmer). —
    *Défaut* : non ; si oui, le signaler dans l'avis.

## 3. Gabarit du document final

```
AVIS DU DÉLÉGUÉ À LA PROTECTION DES DONNÉES
[COLLECTIVITÉ] — [DATE]
Objet : [OBJET DE L'AVIS]
Demandeur : [SERVICE / PERSONNE] — Échéance : [DATE OU « SANS OBJET »]

1. RAPPEL DU RÔLE DU DPO
Le DPO informe, conseille et contrôle (art. 39 RGPD — à confirmer en version
consolidée). Le présent avis est consultatif : il ne vaut ni autorisation ni
refus. La décision appartient au responsable de traitement : [RESPONSABLE DE
TRAITEMENT — maire / président / autre].

2. DESCRIPTION DU TRAITEMENT ANALYSÉ
[DESCRIPTION : finalité, personnes, données, acteurs, outils]
Régime applicable : [RGPD / Police-Justice (titre III loi 78-17 — à confirmer)]

3. ANALYSE DE CONFORMITÉ PAR PRINCIPE
3.1 Licéité — base légale : [ANALYSE]
3.2 Finalité (déterminée, explicite, légitime) : [ANALYSE]
3.3 Minimisation des données : [ANALYSE]
3.4 Durées de conservation (avec source) : [ANALYSE]
3.5 Information et droits des personnes : [ANALYSE]
3.6 Sous-traitance (art. 28) et transferts hors UE : [ANALYSE]
3.7 Sécurité (art. 32) : [ANALYSE]
3.8 AIPD : [REQUISE / NON REQUISE / À INSTRUIRE — motif, cf. references/aipd.md]

4. POINTS DE NON-CONFORMITÉ RELEVÉS
| N° | Constat | Criticité (critique / majeure / mineure) |
|----|---------|------------------------------------------|
| 1  | [CONSTAT] | [CRITICITÉ] |

5. RECOMMANDATIONS HIÉRARCHISÉES
- BLOQUANT (à traiter avant toute mise en œuvre) : [RECOMMANDATIONS]
- À CORRIGER (sous délai raisonnable) : [RECOMMANDATIONS]
- BONNE PRATIQUE (recommandé, non obligatoire) : [RECOMMANDATIONS]

6. CONCLUSION
Niveau : [RISQUE / CONFIANCE] (échelle §5.1 du skill).
Avis du DPO : [FAVORABLE / FAVORABLE AVEC RÉSERVES / DÉFAVORABLE EN L'ÉTAT] —
cet avis recommande ; la décision de mettre en œuvre, d'ajourner ou de
renoncer appartient au responsable de traitement.
[LE CAS ÉCHÉANT : signalement d'un risque de conflit d'intérêts du DPO]

Fait à [LIEU], le [DATE]
[NOM], Délégué(e) à la Protection des Données
```

## 4. Règles de production

- **Jamais de donnée inventée** : tout champ sans réponse reste
  `[À COMPLÉTER]` ; si des champs essentiels manquent (finalité, responsable,
  données), livrer un brouillon marqué `[INCOMPLET]` avec la liste précise
  des champs manquants.
- **Rôle consultatif** : l'avis recommande, jamais « le DPO autorise / valide /
  refuse ». Reformuler toute demande en ce sens (garde-fou §5.2.a).
- **Références juridiques** : appliquer
  `references/socle-sources-verification.md` — article structurellement stable
  cité avec « à confirmer en version consolidée » si non vérifié en session ;
  identifiant officiel jamais reconstitué de mémoire ; obligation ≠ bonne
  pratique.
- **Distinguer** dans l'analyse ce qui est obligatoire (se cite) de ce qui est
  recommandé (s'argumente).
- Aucune donnée personnelle réelle reproduite inutilement dans l'avis.

## 5. Checklist finale avant remise

- [ ] Régime applicable identifié et affiché (STOP RÉGIME si frontière proche) ?
- [ ] Responsable de traitement nommé, avis adressé à lui ?
- [ ] Rappel du rôle consultatif présent en §1 ET en conclusion ?
- [ ] Base légale vérifiée ou marquée « à vérifier » — pas de consentement
      par défaut pour une mission de service public ?
- [ ] Chaque non-conformité a une criticité ; chaque recommandation est classée ?
- [ ] Couple [risque / confiance] indiqué ?
- [ ] Références citées conformes au socle-sources (réserve ou vérification) ?
- [ ] Question AIPD tranchée ou renvoyée à instruction ?
- [ ] Champs manquants listés si brouillon `[INCOMPLET]` ?
