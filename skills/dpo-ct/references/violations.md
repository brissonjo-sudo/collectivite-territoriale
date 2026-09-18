# Branche — Violations de données

> **Branche d'URGENCE.** L'horloge des 72 h prime tout le reste : commencer
> par l'arbre de traitement (§3), qualifier ensuite. Dater chaque étape.

---

## 1. Périmètre / Exclusions

**Couvre** : la qualification d'une violation de données (atteinte à la
confidentialité, à l'intégrité ou à la disponibilité), le registre interne
des violations (art. 33.5 RGPD — à confirmer en version consolidée), la
notification à la CNIL sous 72 h (art. 33 — à confirmer), la communication
aux personnes concernées (art. 34 — à confirmer) et le plan de remédiation.

**Exclut** :
- les mesures techniques et organisationnelles de fond (art. 32) →
  `references/securite-traitements.md` ;
- les suites données par la CNIL (contrôle, mise en demeure, sanction) →
  `references/relations-cnil.md`.

---

## 2. Questions couvertes

- « Est-ce une violation de données ? Faut-il notifier ? »
- « Un agent a envoyé un mail collectif en CC : que faire ? »
- « Ransomware sur le SI : quelles obligations, dans quel ordre ? »
- « Le prestataire nous signale un incident : qui notifie ? »
- « Faut-il prévenir les personnes concernées ? »
- « Comment tenir le registre des violations ? »

---

## 3. Arbre de traitement (urgence — dérouler dans cet ordre)

```
1. FIGER LES FAITS — que s'est-il passé, quand, sur quelles données,
   qui sait quoi ? Dater précisément le moment de CONNAISSANCE par le
   responsable de traitement : l'horloge des 72 h court à partir de là.
2. QUALIFIER — incident de sécurité ou violation de données personnelles ?
   Si violation : confidentialité, intégrité, disponibilité (cumul possible).
3. ÉVALUER LE RISQUE — grille §5.4 (nature des données, volume, personnes,
   conséquences, mesures d'atténuation).
4. REGISTRE INTERNE — inscrire la violation. TOUJOURS, même sans notification.
5. NOTIFIER LA CNIL — si risque pour les droits et libertés : téléservice
   CNIL, dans les 72 h de la connaissance. Notification par étapes si
   informations incomplètes. Justifier tout retard.
6. COMMUNIQUER AUX PERSONNES — si risque ÉLEVÉ : sans délai indu,
   en termes clairs.
7. REMÉDIER — contenir, corriger, articuler avec ANSSI / plainte /
   assurance (§5.6).
8. RETEX — retour d'expérience, mise à jour des mesures (renvoi
   securite-traitements.md), entrée JOURNAL.md.
```

À chaque étape : rappeler que la **décision** de notifier ou de communiquer
appartient au **responsable de traitement** ; le DPO instruit, évalue et
recommande (garde-fou §5.2.a du `SKILL.md`).

---

## 4. Variables à lever

- **Date et heure de connaissance** par le responsable de traitement — pas
  par le DPO, pas par le prestataire. Point de départ des 72 h.
- **Responsable de traitement** concerné : commune, CCAS (personne morale
  distincte), EPCI, État (état civil, élections) ?
- **Régime** : RGPD ou Police-Justice (fichier PM, vidéoverbalisation) ?
  Les obligations de notification diffèrent — vérifier le titre III de la
  loi 78-17 avant de conclure (STOP RÉGIME, `SKILL.md` §5.2.b).
- **Nature de l'atteinte** : confidentialité / intégrité / disponibilité.
- **Catégories de données** : sensibles (art. 9 — à confirmer), sociales,
  NIR, données de mineurs ?
- **Personnes concernées** : nombre, vulnérabilité (mineurs, bénéficiaires
  CCAS, personnes âgées).
- **Sous-traitant impliqué** ? A-t-il notifié la collectivité ? Quand ?
- **Données chiffrées ou pseudonymisées** ? Sauvegardes intactes ?
- **Faits continus** (exfiltration en cours) ou clos ?

Donnée manquante = la demander. Ne jamais présumer la date de connaissance.

---

## 5. Règles métier

### 5.1 Définition large de la violation
Retenir une définition **large** : perte de clé USB, envoi au mauvais
destinataire, mail collectif en CC au lieu de CCI, ransomware, divulgation
orale, perte de dossiers papier (CCAS), accès non autorisé d'un agent,
destruction accidentelle sans sauvegarde. Une violation est une atteinte à
la sécurité entraînant destruction, perte, altération, divulgation ou accès
non autorisés — accidentelle ou illicite. Ne pas exiger de malveillance.

### 5.2 L'horloge des 72 h
Le délai court dès la **connaissance par le responsable de traitement** —
pas par le DPO, pas par la DSI, pas par le sous-traitant. « Connaissance » :
degré raisonnable de certitude qu'une violation s'est produite. La
**notification par étapes** est possible si les informations sont
incomplètes : notifier d'abord ce qui est su, compléter ensuite. Ne jamais
attendre d'avoir « tout compris ». Un dépassement se **justifie** dans la
notification. Week-ends et jours fériés comptent.

### 5.3 Deux seuils distincts
- **Notification CNIL** : risque pour les droits et libertés des personnes.
  Pas de notification si le risque est **improbable** — mais inscrire quand
  même la violation et l'analyse au **registre interne** (art. 33.5 — à
  confirmer).
- **Communication aux personnes** : risque **ÉLEVÉ** seulement. Seuil plus
  haut que la notification. Exceptions possibles (données chiffrées, mesures
  prises rendant le risque improbable, effort disproportionné → information
  publique) — vérifier l'art. 34 en version consolidée avant de les invoquer.

### 5.4 Grille d'évaluation du risque
Croiser : **nature des données** (sensibles, sociales, identifiants),
**volume et nombre de personnes**, **caractéristiques des personnes**
(vulnérabilité), **conséquences possibles** (usurpation d'identité,
discrimination, atteinte à la réputation, perte financière, détresse),
**facilité d'identification**, **mesures d'atténuation** (chiffrement,
révocation, récupération). S'appuyer sur la **méthodologie ENISA et la
doctrine CNIL d'évaluation de gravité — citer la version datée**, ne pas
restituer un barème de mémoire.

### 5.5 Rôle du sous-traitant
Le sous-traitant notifie le responsable de traitement **sans délai indu**
(clause art. 28 — renvoi `references/sous-traitance-transferts.md`). Il ne
notifie **jamais la CNIL à la place** de la collectivité : la notification
appartient au responsable de traitement. Exiger du sous-traitant les
éléments factuels (périmètre, données, chronologie, mesures).

### 5.6 Canal et articulations
- **Téléservice CNIL** de notification des violations : canal officiel —
  vérifier l'URL et le formulaire en vigueur au moment de l'usage.
- **ANSSI / dispositifs cyber** : déclaration d'incident selon les régimes
  applicables à la collectivité (à vérifier au cas d'espèce) ; l'appui
  technique (CSIRT régional, cybermalveillance.gouv.fr) ne remplace pas la
  notification CNIL — obligations **cumulatives**.
- **Dépôt de plainte** : recommander au responsable de traitement en cas
  d'origine malveillante ; utile à l'assurance et à l'enquête.
- **Assurance cyber** : déclarer dans les délais contractuels de la police.
- **Rançon** : ne **JAMAIS** conseiller de payer. Position constante
  ANSSI/CNIL : le paiement n'apporte aucune garantie et entretient la menace.

### 5.7 Cas fréquents en collectivité
- **Ransomware sur le SI mairie** : souvent triple atteinte
  (confidentialité si exfiltration, intégrité, disponibilité) ; risque
  souvent élevé ; dérouler §5.6 en parallèle des 72 h.
- **Mail collectif en CC au lieu de CCI** : violation de confidentialité ;
  risque à évaluer selon la liste (ex. destinataires d'un service social →
  risque relevé).
- **Perte de dossiers CCAS** : données sociales, personnes vulnérables →
  risque élevé probable ; responsable de traitement = **CCAS**, pas la
  commune.

---

## 6. Procédures et délais

| Étape | Acteur | Échéance | Point de contrôle |
|---|---|---|---|
| Connaissance datée | Responsable de traitement | T0 | Trace écrite horodatée |
| Qualification + évaluation | DPO + DSI | Immédiat | Grille §5.4 documentée |
| Registre interne | DPO | Sans délai | Toujours, même sans notification |
| Notification CNIL | Responsable de traitement | **72 h** après T0 | Téléservice ; par étapes si besoin ; retard justifié |
| Complément de notification | Responsable de traitement | Dès que possible | Sans délai indu |
| Communication aux personnes | Responsable de traitement | Sans délai indu | Seulement si risque élevé |
| RETEX + remédiation | DPO + DSI | À froid | Renvoi securite-traitements.md |

Délais et exceptions : à vérifier en version consolidée avant tout usage en
acte (matrice §2.2 du `SKILL.md`).

---

## 7. Déclencheurs de vérification (socle-sources)

Vérifier la source officielle avant de conclure sur :
- le contenu obligatoire de la notification et du registre interne ;
- les exceptions à la communication aux personnes (art. 34) ;
- le régime de notification en Police-Justice (titre III loi 78-17 —
  **jamais de mémoire**) ;
- les obligations de déclaration cyber applicables à la collectivité ;
- la version en vigueur de la méthodologie ENISA / doctrine CNIL de gravité.

---

## 8. Pièges & confusions fréquentes

- **Attendre d'avoir « tout compris »** et dépasser les 72 h : notifier par
  étapes.
- **Confondre incident de sécurité et violation** : un scan de ports sans
  accès aux données n'est pas une violation ; une clé USB perdue en est une.
- **Sur-notifier** (tout envoyer à la CNIL sans évaluation) ou
  **sous-notifier** (ne jamais notifier « pour ne pas s'exposer ») : les
  deux sont fautifs. Évaluer, documenter, décider.
- **Oublier le registre interne** quand on ne notifie pas : l'absence de
  notification se **documente**.
- **Laisser le sous-traitant notifier « à la place »** de la collectivité.
- Faire courir le délai depuis la connaissance par le **DPO** au lieu du
  responsable de traitement.
- Communiquer aux personnes sans évaluation du seuil « risque élevé » — ou
  refuser de communiquer alors qu'il est atteint.
- Oublier que le CCAS est un responsable de traitement distinct.

---

## 9. Données / références à vérifier

- Art. 33, 33.5, 34 RGPD : citables avec la réserve « à confirmer en
  version consolidée ».
- Titre III loi 78-17 (violations en régime Police-Justice) : **jamais de
  mémoire** — vérification en session obligatoire.
- Formulaire et téléservice CNIL de notification : vérifier l'état en ligne.
- Méthodologie ENISA de gravité et doctrine CNIL violations : **dater la
  version citée**.
- Lignes directrices CEPD sur la notification des violations : dater la
  version.
- Régimes de déclaration d'incident cyber (ANSSI) applicables : à vérifier
  au cas d'espèce.

---

## 10. Livrables

- **Notification de violation + registre des violations** →
  `assets/notification-violation-modele.md`. Éléments obligatoires :
  chronologie datée (dont T0 de connaissance), nature de la violation,
  catégories et volumes de données et de personnes, conséquences probables,
  mesures prises et proposées, coordonnées du DPO, évaluation du risque
  documentée, décision du responsable de traitement.
- Communication aux personnes : langage clair, mêmes éléments adaptés.

---

## 11. Double échelle [risque / confiance]

- Qualification « violation ou non » : risque moyen — vérification
  ponctuelle ; en cas de doute, traiter comme violation et documenter.
- Décision de notifier / ne pas notifier : risque **élevé** — citation de
  source et évaluation documentée obligatoires.
- Communication aux personnes (données sensibles, CCAS, mineurs) : risque
  **critique** — abstention si doute persistant : recommander la notification
  et signaler le point à trancher par le responsable de traitement.
- Régime Police-Justice : confiance « à vérifier » systématique.

---

## 12. Checklist de branche

1. T0 de connaissance daté et tracé ?
2. Régime identifié (RGPD / Police-Justice) — STOP RÉGIME affiché si
   frontière proche ?
3. Responsable de traitement correctement désigné (commune / CCAS / EPCI) ?
4. Registre interne alimenté, **même sans notification** ?
5. Les deux seuils (notification / communication) évalués séparément et
   documentés ?
6. Sous-traitant : notification reçue, éléments factuels exigés, pas de
   notification « à la place » ?
7. Articulations traitées : ANSSI/cyber, plainte, assurance — et aucun
   conseil de paiement de rançon ?
8. Décision formellement renvoyée au responsable de traitement
   (garde-fou §5.2.a) ?
9. Renvois faits : securite-traitements.md (fond technique),
   relations-cnil.md (suites) ?
10. RETEX proposé + entrée `JOURNAL.md` si cas significatif ?
