# Générateur — Fiche de registre des activités de traitement (art. 30)

## 1. Objet et cas d'usage

Créer ou mettre à jour une **fiche du registre des activités de traitement**
(art. 30 RGPD — à confirmer en version consolidée) pour un traitement de la
collectivité. La fiche documente la conformité ; elle est tenue sous la
responsabilité du responsable de traitement, le DPO en assure généralement la
tenue matérielle.

## 2. Questions à poser une à une

> Poser ces questions **une à une**, jamais en bloc. Réutiliser toute
> information déjà fournie sans la redemander.

1. **Quel est le traitement à inscrire ?** (nom court + description) —
   *Pourquoi* : identifiant de la fiche. — *Si inconnu* : demander le
   service concerné et l'activité ; sinon arrêter.
2. **Quelle est sa finalité principale (et ses sous-finalités) ?** —
   *Pourquoi* : champ obligatoire ; conditionne base légale et durées. —
   *Si inconnu* : reformuler depuis la description, faire valider.
3. **STOP RÉGIME — finalité pénale ?** — *Pourquoi* : un traitement
   Police-Justice (titre III loi 78-17 — à confirmer) s'inscrit avec des
   mentions spécifiques. — *Si doute* : `references/analyse-situation.md` §2.
4. **Qui est le responsable de traitement (et son représentant) ?**
   (commune → maire ; EPCI → président ; CCAS → personne morale distincte ;
   maire agissant au nom de l'État pour état civil/élections) — *Pourquoi* :
   le registre est tenu par entité responsable. — *Si inconnu* : proposer une
   qualification « à valider ».
5. **Qui est le DPO ?** (nom ou entité, coordonnées) — *Pourquoi* : mention
   du registre. — *Défaut* : reprendre le DPO désigné de la collectivité,
   `[À COMPLÉTER]` sinon.
6. **Quelle base légale ?** — *Pourquoi* : champ structurant. **Attention :
   jamais le consentement par défaut pour une mission de service public** —
   base naturelle : mission d'intérêt public ou obligation légale (art. 6
   RGPD — à confirmer) ; requalifier tout « consentement » annoncé. —
   *Si inconnu* : proposer une base argumentée, marquée « à vérifier »
   (matrice §2.2).
7. **Quelles catégories de personnes concernées ?** (administrés, agents,
   élus, mineurs...) — *Pourquoi* : champ obligatoire ; les personnes
   vulnérables élèvent le risque. — *Défaut* : `[INCOMPLET]`.
8. **Quelles catégories de données ?** — *Pourquoi* : champ obligatoire.
   **Signaler expressément** : données sensibles (art. 9), données
   d'infractions (art. 10), NIR (encadrement spécifique loi 78-17 — à
   confirmer). — *Défaut* : `[INCOMPLET]` ; jamais de liste inventée.
9. **Qui sont les destinataires ?** (services internes, autres
   administrations, sous-traitants, partenaires) — *Pourquoi* : champ
   obligatoire. — *Défaut* : « à recenser », signalé.
10. **Y a-t-il des transferts hors UE ?** (hébergement, éditeur, cloud) —
    *Pourquoi* : mention obligatoire avec garanties (chap. V). — *Défaut* :
    « aucun transfert identifié — à confirmer auprès des prestataires ».
11. **Quelles durées de conservation, et quelle source pour chacune ?**
    (base active / archivage intermédiaire ; source : texte sectoriel,
    référentiel CNIL daté, décision locale documentée) — *Pourquoi* : une
    durée opposable a toujours une source ; croiser avec le régime des
    archives publiques (code du patrimoine). — *Si inconnu* : « durée à
    déterminer — démarche : [pistes] », **jamais de valeur inventée**.
12. **Quelles mesures de sécurité ?** (organisationnelles et techniques,
    description générale) — *Pourquoi* : champ obligatoire art. 30. —
    *Défaut* : renvoyer vers la DSI, champ `[À COMPLÉTER]`.
13. **Quels sous-traitants, avec contrat art. 28 ?** — *Pourquoi* : recenser
    et vérifier l'encadrement contractuel. — *Défaut* : « clause art. 28 à
    vérifier » par sous-traitant.

## 3. Gabarit du document final

```
FICHE DE REGISTRE DES ACTIVITÉS DE TRAITEMENT — ART. 30 RGPD
Fiche n° [N°] — [COLLECTIVITÉ]

Nom du traitement : [NOM]
Finalité(s) : [FINALITÉ PRINCIPALE] ; [SOUS-FINALITÉS]
Régime : [RGPD / Police-Justice — à confirmer]
Responsable de traitement : [ENTITÉ — REPRÉSENTANT (maire / président / ...)]
Délégué à la protection des données : [NOM / ENTITÉ — COORDONNÉES]
Base légale : [BASE — art. 6 RGPD, à confirmer en version consolidée ;
  justification : [MOTIF]]

Catégories de personnes concernées : [LISTE — signaler mineurs / vulnérables]
Catégories de données : [LISTE]
  - Données sensibles (art. 9) : [OUI — lesquelles + garantie / NON]
  - Données d'infractions (art. 10) : [OUI / NON]
  - NIR : [OUI — cadre d'autorisation / NON]

Destinataires : [INTERNES] ; [EXTERNES] ; [SOUS-TRAITANTS]
Transferts hors UE : [NON / OUI — pays, destinataire, garantie (chap. V)]

Durées de conservation :
| Données | Base active | Archivage intermédiaire | Source de la durée |
|---------|-------------|-------------------------|--------------------|
| [CATÉGORIE] | [DURÉE] | [DURÉE] | [TEXTE / RÉFÉRENTIEL CNIL daté / DÉCISION] |
Sort final : [ÉLIMINATION (visa archives départementales — à confirmer) /
  VERSEMENT] — croisement code du patrimoine effectué : [OUI/NON]

Mesures de sécurité (description générale) : [ORGANISATIONNELLES] ; [TECHNIQUES]
Sous-traitants : | Nom | Prestation | Contrat art. 28 : [OUI/À VÉRIFIER] |

AIPD : [REQUISE / NON REQUISE / À INSTRUIRE — cf. references/aipd.md]
Fiche créée le : [DATE] par [NOM] — Dernière mise à jour : [DATE] par [NOM]
```

## 4. Règles de production

- **Jamais de donnée inventée** : ni durée, ni liste de données, ni
  destinataire supposé. Tout champ sans réponse reste `[À COMPLÉTER]` ; si
  des champs obligatoires manquent, livrer la fiche marquée `[INCOMPLET]`
  avec la liste précise des champs manquants à collecter auprès du service.
- **Base légale** : requalification systématique d'un consentement annoncé
  pour une mission de service public ; base marquée « à vérifier » si non
  vérifiée en session (matrice §2.2 : vérification requise).
- **Durées** : chaque durée a une source citée conformément au socle-sources
  (référentiel CNIL daté, texte sectoriel avec réserve « à confirmer en
  version consolidée » si non vérifié). Croiser le sort final avec le régime
  des archives publiques — ne jamais conclure « supprimer » sans ce
  croisement.
- La fiche documente ; elle ne vaut pas avis de conformité. Si des
  non-conformités apparaissent en la remplissant, les signaler et proposer
  un avis DPO (`assets/avis-dpo-modele.md`) — la décision de mise en
  conformité appartient au responsable de traitement.
- Aucune donnée personnelle réelle dans la fiche (catégories uniquement).

## 5. Checklist finale avant remise

- [ ] Régime identifié (STOP RÉGIME si frontière proche) ?
- [ ] Responsable de traitement correctement désigné (attention CCAS, État) ?
- [ ] Base légale ≠ consentement par défaut ; vérifiée ou « à vérifier » ?
- [ ] Données sensibles / infractions / NIR expressément traitées ?
- [ ] Chaque durée a une source ; croisement archives publiques fait ?
- [ ] Transferts hors UE tranchés (ou « à confirmer auprès des prestataires ») ?
- [ ] Sous-traitants recensés avec statut du contrat art. 28 ?
- [ ] Dates de création et de mise à jour renseignées ?
- [ ] Champs manquants listés si `[INCOMPLET]` ?
