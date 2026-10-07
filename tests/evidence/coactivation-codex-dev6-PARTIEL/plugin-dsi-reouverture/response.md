STOP — Incident de sécurité suspecté, en cours, récent ou rouvert.
1. Préserver les preuves avant toute remédiation irréversible : ne pas réinstaller, effacer ou restaurer ce qui a été touché ; organiser le confinement avec les intervenants habilités.
2. Alerter les responsables opérationnels désignés et documenter les faits. Cette alerte interne conservatoire ne fixe aucune démarche externe.
3. Attribuer les décisions engageantes au décideur compétent à identifier ; ne pas décider seul d’un paiement, d’une communication publique ou d’un arrêt de service public.
4. Aucune contre-mesure offensive, aucun accès à un système tiers.
5. Données personnelles possiblement touchées → BASCULE dpo-ct.

**Rouvrez le dossier en conservant son historique.** La conclusion initiale reste datée et rattachée aux éléments examinés à l’époque. Elle ne suffit plus à écarter une atteinte aux données aujourd’hui. Le nouvel indice ne prouve cependant ni une extraction effective ni une attaque encore active.

### Volet dsi-fpt : réouverture et instruction technique

Selon `skills/dsi-fpt/objets/incident-securite.md` et `skills/dsi-fpt/references/crise-cyber-continuite.md` :

- Ajouter une entrée de réouverture horodatée : indice reçu, provenance, périmètre suspecté, motif de réexamen et pilote désigné. Conserver l’expertise, les preuves et les décisions de clôture initiales ; produire un complément versionné.
- Réexaminer ce que l’expertise couvrait réellement : systèmes, période, données, preuves disponibles et limites. Faire déterminer si le nouvel indice concerne l’événement ancien ou un autre événement lié.
- Confier à DSI/RSSI et aux intervenants habilités la préservation des éléments, l’instruction du périmètre et les mesures conservatoires proportionnées. Tracer qui propose, autorise et exécute chaque intervention. Aucun mode opératoire d’extraction nominative n’est fourni ici.

Le cadrage doit précéder le choix des mesures, conformément à `skills/dsi-fpt/references/securite-si.md` :

| Volet | Informations et preuves à réunir | Responsable et contrôle attendu |
|---|---|---|
| Périmètre | Actifs, applications, données et dépendances concernés ; comparaison avec l’expertise ancienne | DSI/RSSI : périmètre documenté, hypothèses séparées des constats |
| Exploitation | Mode interne, mutualisé ou externalisé ; support, supervision, intervenants et accès disponibles | Pilote de la collectivité à désigner : répartition des actions et résultats contrôlables |
| Continuité | Services affectés, besoins des usagers, possibilités de fonctionnement dégradé | Responsables métier et coordination de direction : priorités et fonctionnement acceptable explicités |
| Reprise | Préservation réalisée, environnement et copies évalués, accès revus, contrôles techniques et fonctionnels | DSI pour les essais techniques, métiers pour la recette ; décision attribuée et réserves consignées |

Réévaluez les conditions de reprise uniquement sur le périmètre concerné. Une application qui fonctionne ne démontre pas l’absence d’extraction. Prévoir un suivi après reprise et un retour au fonctionnement dégradé si les critères cessent d’être réunis.

### BASCULE dpo-ct — Analyse des données personnelles

Ce volet relève de `dpo-ct`, avec `skills/dpo-ct/references/analyse-situation.md` et `skills/dpo-ct/references/violations.md` ; DSI fournit les faits techniques.

Faites préciser le traitement et sa finalité, l’entité concernée, les catégories et volumes de données et de personnes, les éléments attestant une extraction, les protections et les conséquences possibles. « Données d’usagers » ne suffit pas à établir leur sensibilité ni un niveau de risque élevé.

Distinguez dans la chronologie la date de l’événement ancien, la réception du nouvel indice et le moment où les éléments ont permis de considérer l’atteinte comme suffisamment établie. Ne remettez pas automatiquement une horloge à zéro à la date de réouverture. Documentez ce qui était connu lors de la clôture et ce qui change maintenant.

L’organisation proposée est la suivante : DPO instruit le volet données et formule un avis ; l’acteur décisionnaire identifié reçoit cet avis et fait consigner sa décision. Les compétences et délégations juridiques restent à vérifier. Examinez séparément la notification éventuelle à l’autorité et l’information éventuelle des personnes.

### Volet recherche-juridique : vérification et abstentions

Les recherches effectuées via `mcp__droit_francais__search` le **07/10/2026** n’ont fourni aucun texte primaire pertinent exploitable pour ces obligations. Les résultats de jurisprudence et les articles portant un numéro identique dans d’autres matières ne les établissent pas.

**Recherche-juridique s’abstient donc sur la qualification juridique définitive, le régime applicable, les conditions et délais de notification ou d’information, les compétences juridiques et les responsabilités personnelles.** Il ne confirme pas davantage une obligation de plainte, de signalement cyber ou une échéance d’assurance. Ces points nécessitent les textes primaires pertinents et, selon le point, les pièces contractuelles ; aucune démarche externe automatique n’est déduite du STOP.

Préparez un dossier commun : chronologie, expertise initiale, nouvel indice, écarts de périmètre, constats techniques, analyse DPO, décisions attendues et actions attribuées. Une nouvelle clôture sera proposée après examen des preuves, recette technique et métier, traitement explicite du volet données et décision tracée par l’acteur dont la compétence aura été vérifiée.

Pour préciser la suite, trois informations manquent : **quel traitement d’usagers et quelle finalité ; quand et à qui le nouvel indice a été transmis ; qui exploite le SI et pilote l’incident ?** Fournissez seulement des informations anonymisées, sans journaux bruts ni données d’usagers.
