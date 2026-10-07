STOP — Incident de sécurité en cours ou récent.

1. Ne rien faire d’irréversible avant de préserver les preuves : ne pas réinstaller, effacer, restaurer ni rallumer ce qui a été touché ; isoler.
2. Ne rien taire : signaler l’incident dans les circuits prévus ; les obligations et délais de signalement, de plainte et d’assurance restent à vérifier pour ce cas.
3. Ne pas décider seul de ce qui revient à l’exécutif : paiement d’une rançon, communication publique, arrêt d’un service public.
4. Aucune contre-mesure offensive, aucun accès à un système tiers.
5. Données personnelles possiblement touchées → BASCULE dpo-ct.

Organiser trois travaux en parallèle : **DSI/RSSI pour contenir et préserver, dpo-ct pour qualifier les données et le risque, recherche-juridique pour vérifier les obligations et leurs conditions.** La fin de l’investigation technique ne doit pas devenir un préalable automatique à l’examen des notifications.

Date d’analyse : **07/10/2026**. Dates de l’intrusion et de prise de connaissance : inconnues. Champ : scénario fictif de collectivité française. Niveau : note express, mode A standard. Les fichiers candidats `dsi-fpt/SKILL.md`, `dpo-ct/SKILL.md` et `recherche-juridique/SKILL.md` ont été lus par fragments ; cela ne constitue pas une activation native de plugin.

**Volet dsi-fpt — organisation technique proposée**

L’alerte de l’hébergeur et les indices d’accès sont les seuls faits fournis. Ils ne démontrent ni l’étendue de la compromission, ni une exfiltration, ni l’absence d’atteinte à l’intégrité ou à la disponibilité. Le cadrage suit `dsi-fpt/references/analyse-situation.md`, `dsi-fpt/references/crise-cyber-continuite.md` et `dsi-fpt/objets/incident-securite.md`.

| Axe | Inconnues et preuves à réunir | Responsable et contrôle attendu |
|---|---|---|
| Périmètre | Services, actifs, comptes techniques et dépendances concernés ; rapport factuel horodaté de l’hébergeur, distinction entre accès possible et accès observé | DSI/RSSI avec l’hébergeur ; périmètre documenté et limites explicites |
| Support et exploitation | Mode interne, mutualisé ou externalisé ; intervenants habilités, appui spécialisé et moyens de coordination fiables | Pilote technique à désigner ; chaque intervention attribuée et son résultat tracé |
| Préservation et confinement | Éléments disponibles, risque de disparition des traces, mesures conservatoires possibles et effets sur le service | RSSI et intervenant compétent ; preuve de conservation, traçabilité des détenteurs et des opérations, contrôle du confinement |
| Continuité et reprise | Services sociaux prioritaires, fonctionnement dégradé, copies récupérables et dépendances de reprise | Métier pour la priorité et la recette fonctionnelle ; DSI pour les contrôles techniques ; autorité habilitée pour l’arbitrage |

Faire cadrer la conservation des preuves par l’appui compétent, avec copies de travail séparées et accès maîtrisés. Tenir un journal des constats, hypothèses, décisions, acteurs et résultats ; conserver les pièces sensibles dans un espace autorisé, sans les reproduire dans la communication courante. Aucune commande d’extraction nominative n’est proposée ici.

La reprise exige des éléments contrôlables : traces préservées, périmètre instruit, environnement de reprise maîtrisé, copies évaluées et contrôles techniques et métier réussis. Une application redevenue disponible ne prouve pas la clôture de l’incident. Ces repères viennent de `dsi-fpt/references/securite-si.md` et `dsi-fpt/references/crise-cyber-continuite.md`.

**BASCULE dpo-ct — Cette question porte sur le droit des données personnelles. La DSI ne tranche pas cette qualification. À reprendre côté dpo-ct : données effectivement touchées, risque pour les personnes, notification et communication.**

**Analyse dpo-ct — qualification à instruire**

Avec le service social et l’hébergeur, relever les catégories exactes de données, les personnes et volumes concernés, les accès observés, les copies éventuelles et les protections effectivement appliquées. « Dossiers sociaux » ne suffit pas à établir la présence de données de santé ni un risque élevé. Examiner les conséquences possibles et les mesures d’atténuation, sans présumer leur efficacité (`dpo-ct/references/analyse-situation.md` et `dpo-ct/references/violations.md`).

Un accès non autorisé à des données personnelles entre dans la définition de la violation ; les indices fournis appellent donc une vérification factuelle, sans qualification définitive. Identifier aussi l’organisme qui détermine les finalités et moyens et le rôle réel de l’hébergeur : ne pas désigner automatiquement la commune ou son maire. Le DPO conseille et contrôle ; il ne remplace pas le responsable du traitement. **Fondements : RGPD, articles 4 et 39, version consolidée présentée comme courante par EUR-Lex, consultée le 07/10/2026.** [Texte EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02016R0679-20160504).

**Vérification attribuée à recherche-juridique — cadre conditionnel**

Pour un traitement relevant du RGPD :

- **Autorité de contrôle :** l’article 33 prévoit une notification dans les meilleurs délais et, si possible, au plus tard 72 heures après la prise de connaissance, sauf si la violation n’est pas susceptible d’engendrer un risque pour les droits et libertés. Un retard est motivé ; des informations peuvent être fournies progressivement sans autre retard indu. Toute violation est documentée, même sans notification. Si l’hébergeur est sous-traitant, il avertit le responsable dans les meilleurs délais après sa prise de connaissance. [Article 33 reproduit par la CNIL, consulté le 07/10/2026](https://www.cnil.fr/fr/reglement-europeen-protection-donnees/chapitre4).
- **Personnes concernées :** l’article 34 prévoit une communication dans les meilleurs délais lorsque la violation est susceptible d’engendrer un risque élevé, sous réserve de ses exceptions démontrées. Évaluer cette branche séparément, sans attendre automatiquement la notification à l’autorité. [Articles 33 et 34, texte consolidé EUR-Lex consulté le 07/10/2026](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02016R0679-20160504).

**T0 reste inconnu : aucune échéance calendaire n’est calculable.** Distinguer l’heure de l’intrusion, la découverte par l’hébergeur, son alerte et la prise de connaissance par le responsable du traitement. Le portail CNIL décrit le canal de notification pour les organismes publics ou privés ; aucun envoi n’est effectué ici. [Portail officiel, consulté le 07/10/2026](https://www.cnil.fr/fr/services-en-ligne/notifier-une-violation-de-donnees-personnelles).

Pour arrêter la décision, préciser : **quel organisme porte le traitement et pour quelle finalité ; quelles données et personnes sont effectivement touchées ; quand cet organisme a pris connaissance de la violation ?** En attendant, préparer un dossier évolutif : chronologie, périmètre, preuves référencées, analyse du risque, mesures prises et recommandation du DPO, puis décision tracée du responsable. Toute communication externe nécessite une revue humaine.

**Limites :** la recherche MCP réelle a fourni des résultats hors sujet, qui ont été écartés. Les passages primaires pertinents ont ensuite été reçus sur CNIL et EUR-Lex ; cela ne vérifie pas les autres obligations sectorielles, contractuelles, de plainte ou d’assurance. Abstention sur ces obligations et sur la décision concrète de notifier tant que les faits manquants ne sont pas établis. Risque opérationnel : critique ; confiance sur le périmètre réel : à vérifier. Aucun module spécialisé ni source informelle n’a été mobilisé.
