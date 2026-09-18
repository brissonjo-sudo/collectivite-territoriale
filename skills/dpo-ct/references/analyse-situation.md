# Couche 1 — Decision Engine (routeur DPO CT)

> Point d'entrée obligatoire pour toute situation composée. Ce fichier
> qualifie la situation, identifie le régime et le responsable de traitement,
> puis oriente vers la branche (couche 2) et le livrable (couche 3). Il ne
> contient pas le fond des branches : il pointe vers elles.

---

## 1. Séquence de raisonnement imposée

Dérouler dans cet ordre, sans sauter d'étape :

1. **Y a-t-il des données personnelles ?** Toute information se rapportant à
   une personne physique identifiée ou identifiable (art. 4.1 RGPD — à
   confirmer). Pseudonymisé = personnel. Vraiment anonymisé = hors champ,
   mais l'anonymisation se démontre (doctrine CNIL/CEPD à vérifier).
   → Si non : le skill se désactive sur ce point ; le signaler.
2. **Quel traitement, quelle finalité ?** Décrire l'opération (collecte,
   enregistrement, diffusion, croisement...) et sa ou ses finalités
   déterminées, explicites, légitimes. Une finalité floue est le premier
   signal de non-conformité.
3. **Quel régime ?** — garde-fou §5.2.b du `SKILL.md` :
   - finalité de prévention, détection, poursuite d'infractions pénales ou
     d'exécution de sanctions → **régime Police-Justice** (titre III loi
     78-17 — à confirmer) ;
   - toute autre finalité → **RGPD** (+ titre II loi 78-17) ;
   - dispositif mixte (ex. vidéoprotection tranquillité publique +
     vidéoverbalisation) → **découper par finalité** et traiter chaque volet
     sous son régime.
   Afficher le régime retenu en tête d'analyse dès que la frontière est
   proche. En cas de doute : matrice §2.2 → vérification.
4. **Qui est responsable de traitement ?** Commune, EPCI, CCAS (personne
   morale distincte), syndicat mixte, État (état civil, élections : le maire
   agit au nom de l'État — rôles à vérifier au cas par cas), responsabilité
   conjointe (art. 26 — à confirmer). Puis : **qui est sous-traitant ?**
   (éditeur, hébergeur, prestataire — art. 28).
5. **Quelle base légale ?** Pour une collectivité, dans l'ordre de
   probabilité : obligation légale, mission d'intérêt public ; par exception
   contrat, intérêt légitime (indisponible pour les missions de service
   public — à confirmer), consentement (réflexe anti-consentement du socle
   §4). Données sensibles → exception art. 9 en plus. Régime Police-Justice
   → logique propre (nécessité, texte).
6. **Quelles obligations déclenchées ?**
   - inscription au **registre** (toujours) → `gouvernance-registre.md` ;
   - **information** des personnes (art. 13/14) → `droits-personnes.md` ;
   - **AIPD** si risque élevé probable (listes CNIL, critères CEPD) →
     `aipd.md` ;
   - **encadrement de la sous-traitance** / transferts → 
     `sous-traitance-transferts.md` ;
   - **sécurité** proportionnée (art. 32) → `securite-traitements.md` ;
   - formalités sectorielles éventuelles (autorisation CSI, NIR, santé...)
     → branche sectorielle + skill compétent.
7. **Quel niveau de risque ?** (échelle §5.1) — données sensibles ou
   d'infraction, personnes vulnérables, grande échelle, surveillance,
   croisement de fichiers, décision automatisée → risque élevé ou critique.
8. **Quelle orientation ?** Branche(s) de couche 2 à lire + livrable de
   couche 3 à proposer.

---

## 2. Arbre de qualification du régime (frontières fréquentes)

| Dispositif | Régime probable | Vigilance |
|---|---|---|
| Vidéoprotection voie publique (tranquillité) | RGPD + CSI | Autorisation préfectorale → `dpm-fpt` |
| Vidéoverbalisation | Police-Justice | Découpage par finalité si dispositif mixte |
| Main courante / rapports PM | Police-Justice | Contenu opérationnel → `dpm-fpt` |
| Caméras-piétons PM | Police-Justice (texte propre CSI — à vérifier) | Croiser `dpm-fpt` |
| Contrôle d'accès bâtiments | RGPD | Badgeage agents → volet RH |
| Stationnement payant (FPS) | RGPD (post-dépénalisation — à vérifier) | Ne pas présumer Police-Justice |
| Fichiers scolaires / périscolaires | RGPD | Mineurs → risque relevé |
| Action sociale (CCAS) | RGPD | RT = CCAS, pas la commune ; données sensibles |

Tableau indicatif : **toujours vérifier** la qualification en cas d'enjeu
(matrice §2.2).

---

## 3. Variables à lever avant de trancher

- Régime applicable (§1.3) et responsable de traitement (§1.4).
- Catégories de données (ordinaires / sensibles art. 9 / infractions art. 10
  / NIR) et de personnes (agents, administrés, mineurs, vulnérables).
- Échelle du traitement et durée envisagée.
- Existence d'un sous-traitant, localisation de l'hébergement.
- Traitement nouveau ou modification d'un existant (impact registre + AIPD).
- Texte sectoriel imposant ou encadrant le traitement.

Variable manquante qui fait basculer la réponse → la **demander** ou répondre
en **conditionnel borné**.

---

## 4. Sorties types du routeur

- **Question simple, une branche** → lire la branche, répondre, proposer le
  livrable pertinent.
- **Projet nouveau** (téléservice, logiciel, dispositif) → dérouler §1 en
  entier ; livrable naturel : **avis DPO** (`assets/avis-dpo-modele.md`),
  nourri des branches registre + AIPD + sous-traitance + sécurité.
- **Incident** (« on a perdu / envoyé / exposé des données ») → réflexe
  immédiat `violations.md` : l'horloge des 72 h court depuis la
  **connaissance** de la violation. Traiter l'urgence avant la pédagogie.
- **Demande d'un administré** (accès, effacement...) → `droits-personnes.md` ;
  délai d'un mois — à confirmer — qui court dès réception par la
  collectivité, pas par le DPO.
- **Contrôle ou courrier CNIL** → `relations-cnil.md` ; risque élevé par
  défaut.

---

## 5. Checklist du routeur

1. Données personnelles confirmées (ou hors champ signalé) ?
2. Finalité(s) explicitée(s) ?
3. Régime identifié — STOP RÉGIME affiché si frontière proche ?
4. Responsable de traitement et sous-traitants nommés ?
5. Base légale pressentie sans consentement par défaut ?
6. Obligations déclenchées listées ?
7. Risque coté et branches + livrable annoncés ?
