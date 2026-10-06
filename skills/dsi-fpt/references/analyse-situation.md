# Routeur — analyse de situation (couche 1)

> Premier fichier à lire pour toute situation composée. Il **qualifie** la
> demande, **détecte** les garde-fous et les frontières, puis **oriente**. Il ne
> contient pas de fond : le fond est dans les branches, les objets et les
> gabarits, cités par leur chemin.

---

## 1. Séquence imposée

Dérouler dans cet ordre. Examiner tous les garde-fous déclenchés et les
frontières, sans arrêter cet examen au premier bloc. Si un déclencheur est
déjà visible dans la demande, son STOP ouvre le premier message visible,
avant toute annonce. Les blocs limitent le contenu permis ; la suite est
traitée par le rôle compétent selon `SKILL.md` §5.7, ou reste en abstention.

| Étape | Question | Si oui |
|---|---|---|
| 1 | Un **incident de sécurité** est-il en cours ou récent ? | **STOP incident** (`SKILL.md` §5.2), puis `crise-cyber-continuite.md` et `objets/incident-securite.md` |
| 2 | La demande vise-t-elle à **accéder aux contenus ou aux traces d'une personne**, ou à **surveiller des personnes** ? | **STOP surveillance** (`SKILL.md` §5.3) et bascule |
| 3 | La question relève-t-elle d'une **frontière** ? | Bloc `BASCULE` ou signalement hors périmètre (§3 ci-dessous) |
| 4 | Le **mode d'exercice** de la fonction SI change-t-il la réponse ? | Le demander s'il n'est pas donné (`SKILL.md` §2.4) |
| 5 | Quelle est la **nature** de la question ? | Orienter vers la branche (§2) |
| 6 | S'agit-il d'une **situation récurrente** qui traverse plusieurs branches ? | Orienter vers l'objet (§4) |
| 7 | Un **écrit** est-il attendu ? | Orienter vers le gabarit (§5) |
| 8 | Une ligne « Oui » de la **matrice de vérification** est-elle concernée ? | Activer `recherche-juridique`, récupérer la source primaire et vérifier l'applicabilité (`socle-sources-verification.md`) |
| 9 | Quel est le **niveau de risque** ? | Double échelle (`SKILL.md` §5.1) |

---

## 2. Signaux → branche

| Signaux dans la demande | Branche |
|---|---|
| schéma directeur, gouvernance, comité, RSSI, rôles, mutualisation, EPCI, syndicat informatique, numérique responsable, sobriété, indicateurs | `references/gouvernance-strategie.md` |
| PSSI, analyse de risques, comptes, droits, mots de passe, authentification, sauvegardes, mises à jour, sensibilisation, homologation, attestation de sécurité, journalisation | `references/securite-si.md` |
| PCA, PRA, continuité, reprise, exercice de crise, cellule de crise (hors incident en cours) | `references/crise-cyber-continuite.md` |
| réseau, site distant, école, téléphonie, fibre, interconnexion, parc, salle serveur, fin de vie du matériel | `references/infrastructures-reseaux.md` |
| cloud, hébergement, SaaS, souveraineté, qualification d'une offre, localisation des données, sortie d'un hébergeur | `references/cloud-hebergement.md` |
| logiciel métier, éditeur, cartographie applicative, référentiel de données, interopérabilité, échanges avec l'État (état civil, élections, contrôle de légalité, comptabilité, factures électroniques) | `references/applications-interoperabilite.md` |
| téléservice, saisine par voie électronique, formulaire en ligne, signature électronique, parapheur, identification des usagers | `references/dematerialisation-teleservices.md` |
| accessibilité, RGAA, déclaration d'accessibilité, schéma pluriannuel, handicap, sanction | `references/accessibilite-numerique.md` |
| intelligence artificielle, IA générative, assistant, algorithme, décision automatisée, mention explicite, publication des algorithmes, gouvernance des données | `references/ia-donnees.md` |
| contrat, niveau de service, pénalités, réversibilité, restitution des données, licence, maintenance, infogérance, éditeur défaillant, fin de contrat | `references/contrats-prestataires.md` |
| note, rapport, cahier des charges, charte, note d'homologation, communication interne de la DSI | `references/ecrits-numerique.md` |
| retour d'expérience, leçons d'un incident ou d'un projet | `references/retex.md` |

Une demande peut mobiliser plusieurs branches : les lire toutes et **signaler
le lien**, sans dupliquer.

---

## 3. Frontières à détecter

| Signal | Traitement |
|---|---|
| base légale, AIPD, registre, information des personnes, notification d'une violation, délai de notification, sous-traitance au sens du RGPD, transfert hors Union | `BASCULE dpo-ct` (`SKILL.md` §5.5) |
| sanction d'un agent, procédure disciplinaire, adoption ou opposabilité d'une charte, consultation des instances, télétravail (statut), paie, carrière | `BASCULE drh-fpt` (`SKILL.md` §5.6) |
| autorisation de vidéoprotection, doctrine d'emploi, centre de supervision, vidéoprotection algorithmique, police municipale | `BASCULE dpm-fpt` (`SKILL.md` §5.6) |
| inscription au budget, imputation, amortissement, financement, subvention | `BASCULE dirfi-fpt` (`SKILL.md` §5.6) |
| choix de la procédure de marché, critères de sélection, publicité, recours | **Hors périmètre** : signaler, nommer le service de la commande publique, s'arrêter |
| archivage électronique, ouverture des données publiques | **Hors périmètre de cette version** : signaler |
| vigueur d'un texte, conflit de normes, jurisprudence | `recherche-juridique` |

---

## 4. Situations récurrentes → objet

| Situation | Objet |
|---|---|
| Lancer ou conduire un projet applicatif | `objets/projet-si.md` |
| Gérer un incident de sécurité de bout en bout (après le STOP) | `objets/incident-securite.md` |
| Ouvrir un téléservice aux usagers | `objets/teleservice.md` |
| Choisir, contractualiser ou quitter une solution en ligne | `objets/solution-saas.md` |
| Équiper ou sécuriser un site (mairie annexe, école) | `objets/site-reseau.md` |
| Arrivée, mobilité ou départ d'un agent : comptes, accès, poste | `objets/compte-poste-agent.md` |

---

## 5. Écrits → gabarit

| Écrit | Gabarit |
|---|---|
| Fiche projet | `references/templates/fiche-projet-si.md` |
| Rapport d'incident | `references/templates/rapport-incident.md` |
| Cahier des charges technique | `references/templates/cahier-des-charges-technique.md` |
| Charte d'usage du SI | `references/templates/charte-usage-si.md` |
| Note d'homologation de sécurité | `references/templates/note-homologation.md` |

---

## 6. Pièges de qualification

- **Incident ou pas ?** Une panne n'est pas un incident de sécurité, mais une
  indisponibilité **inexpliquée** doit être traitée comme suspecte jusqu'à
  preuve du contraire : appliquer le STOP incident par prudence.
- **Surveillance déguisée.** « Vérifier que les agents ne perdent pas de
  temps », « récupérer les mails d'un agent absent », « savoir qui a fuité le
  document » : ce sont des demandes de surveillance → STOP §5.3.
- **Obligation ou bonne pratique ?** Une recommandation de l'ANSSI, une
  doctrine de l'État ou un projet de loi n'oblige pas la collectivité. Le
  vérifier avant d'écrire « doit ».
- **Qui décide ?** La DSI exécute et conseille ; l'exécutif décide ; le DPO
  exige et contrôle. Une réponse qui fait décider la DSI à la place de
  l'exécutif est fausse, même techniquement juste.
- **Mode mutualisé.** Quand le SI est porté par un service commun ou un
  prestataire, la collectivité reste responsable : la réponse dit ce qu'elle
  doit exiger et contrôler, pas seulement ce que fait le prestataire.
