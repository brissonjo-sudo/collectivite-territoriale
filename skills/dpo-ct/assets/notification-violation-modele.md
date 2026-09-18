# Générateur — Violation de données : registre interne, notification CNIL, communication aux personnes

## 1. Objet et cas d'usage

Produire, en situation de violation de données (art. 33-34 RGPD — à confirmer
en version consolidée), jusqu'à trois livrables : **(a)** la fiche du registre
interne des violations, **(b)** le contenu de la notification à la CNIL,
**(c)** le squelette de communication aux personnes concernées si le risque
est élevé. Contexte souvent urgent : aller à l'essentiel, le délai de 72 h
court depuis la **connaissance** de la violation.

## 2. Questions à poser une à une

> Une question à la fois — mais en cas d'urgence, commencer par la question 2
> (horloge des 72 h) avant tout le reste.

1. **Que s'est-il passé ?** (faits, nature : confidentialité, intégrité,
   disponibilité — un même incident peut cumuler) — *Pourquoi* : qualifier la
   violation. — *Si flou* : lister les faits certains vs incertains.
2. **Quand la violation a-t-elle été CONNUE de la collectivité ?** (date et
   heure de connaissance ≠ date des faits) — *Pourquoi* : c'est la
   connaissance qui déclenche le délai de 72 h de notification (à confirmer —
   matrice §2.2 : délai à vérifier). — *Si inconnu* : établir la chronologie
   avec l'utilisateur ; en l'absence de certitude, retenir la date la plus
   ancienne plausible et le documenter.
3. **Quelles données et combien de personnes sont concernées ?** (catégories,
   volumes approximatifs, données sensibles, mineurs) — *Pourquoi* : fonde
   l'évaluation du risque et le contenu de la notification. — *Si inconnu* :
   « en cours de qualification » — la notification par étapes le permet.
4. **Qui est le responsable de traitement du traitement touché ?** —
   *Pourquoi* : c'est lui qui notifie et décide. — *Défaut* : `[À COMPLÉTER]`.
5. **Quelles sont les conséquences probables pour les personnes ?**
   (usurpation, discrimination, perte de contrôle, préjudice moral...) —
   *Pourquoi* : détermine risque / risque élevé, donc notification et
   communication. — *Si inconnu* : proposer une évaluation type, marquée
   « hypothèse à valider ».
6. **Quelles mesures ont été prises ou sont proposées ?** (containment,
   correction, prévention) — *Pourquoi* : registre + notification. —
   *Défaut* : « aucune mesure communiquée » = constat signalé, pas invention.
7. **Un sous-traitant est-il à l'origine ou informé ?** — *Pourquoi* : le
   sous-traitant notifie le responsable de traitement sans délai indu (art. 33.2
   — à confirmer) ; tracer les dates. — *Défaut* : sans objet.
8. **Le traitement touché relève-t-il du régime Police-Justice ?** —
   *Pourquoi* : garde-fou §5.2.b, formalités spécifiques (titre III loi
   78-17 — à confirmer). — *Si doute* : le signaler avant de conclure.

## 3. Gabarits des documents finaux

### (a) Fiche de registre interne des violations

```
REGISTRE DES VIOLATIONS — FICHE N° [N°] — [COLLECTIVITÉ]
Faits et nature : [DESCRIPTION — confidentialité / intégrité / disponibilité]
Date des faits : [DATE] — Date de découverte : [DATE]
Date de CONNAISSANCE par le responsable de traitement : [DATE + HEURE]
  → échéance 72 h (à confirmer) : [DATE + HEURE]
Origine : [interne / sous-traitant [NOM], informé le [DATE] / externe / indéterminée]
Données concernées : [CATÉGORIES, dont sensibles : OUI/NON]
Personnes concernées : [CATÉGORIES — VOLUME APPROXIMATIF]
Conséquences probables : [ANALYSE]
Mesures prises : [LISTE + DATES] — Mesures proposées : [LISTE]
Évaluation du risque pour les personnes : [ABSENT / RISQUE / RISQUE ÉLEVÉ — motifs]
DÉCISION (responsable de traitement, sur avis du DPO) :
  - Notification CNIL : [OUI le [DATE] / NON] — MOTIVATION : [MOTIFS —
    obligatoire aussi en cas de non-notification]
  - Communication aux personnes : [OUI / NON] — MOTIVATION : [MOTIFS]
Avis du DPO : [RECOMMANDATION] — Clôture de la fiche : [DATE]
```

### (b) Contenu de la notification CNIL

À déposer sur le **téléservice de notification de la CNIL** (cnil.fr).
Si toutes les informations ne sont pas disponibles sous 72 h : **notification
par étapes** (notification initiale puis compléments), en l'indiquant.

```
NOTIFICATION DE VIOLATION — [COLLECTIVITÉ] — [INITIALE / COMPLÉMENTAIRE]
1. Nature de la violation : [FAITS, TYPE, DATES — dont date de connaissance ;
   si > 72 h : motifs du retard]
2. Catégories et nombre approximatif de personnes concernées : [X]
   Catégories et volume approximatif d'enregistrements : [X]
3. Coordonnées du DPO (point de contact) : [NOM, FONCTION, TÉL., COURRIEL]
4. Conséquences probables de la violation : [ANALYSE]
5. Mesures prises ou proposées pour remédier et atténuer : [LISTE]
[SI PAR ÉTAPES : informations manquantes et échéance prévisionnelle des compléments]
```

### (c) Communication aux personnes concernées (si risque élevé)

Langage **clair et simple**, sans jargon juridique ni technique.

```
Objet : information importante concernant vos données personnelles
Madame, Monsieur,
Nous vous informons qu'un incident de sécurité survenu le [DATE] a concerné
[DONNÉES CONCERNÉES, en termes simples]. Concrètement : [CE QUI S'EST PASSÉ,
2-3 phrases sans jargon].
Ce que cela peut impliquer pour vous : [CONSÉQUENCES POSSIBLES, simplement].
Ce que nous avons fait : [MESURES, simplement].
Ce que vous pouvez faire : [RECOMMANDATIONS CONCRÈTES : vigilance,
changement de mot de passe...].
Pour toute question : [DPO — COORDONNÉES]. Vous pouvez également adresser
une réclamation à la CNIL (cnil.fr).
[SIGNATURE — RESPONSABLE DE TRAITEMENT]
```

## 4. Règles de production

- **Jamais de donnée inventée** : dates, volumes et catégories uniquement
  d'après les éléments fournis ; l'incertitude s'écrit (« volume approximatif »,
  « en cours de qualification »). Éléments essentiels manquants → brouillon
  `[INCOMPLET]` listant les champs manquants — sans jamais retarder l'alerte
  sur l'échéance des 72 h.
- **Rôle consultatif** : le DPO recommande de notifier ou non ; la **décision
  de notification appartient au responsable de traitement** et se motive dans
  les deux sens (notifier / ne pas notifier).
- La fiche de registre (a) se remplit **même si** la CNIL n'est pas notifiée.
- **Références** : délai de 72 h, seuils de risque et contenu de la
  notification = lignes « Oui » de la matrice §2.2 → vérifier en session ou
  assortir de « à confirmer en version consolidée » ; doctrine CNIL/CEPD
  (lignes directrices violations) datée.
- Régime Police-Justice → signaler que les formalités diffèrent (titre III
  loi 78-17 — à confirmer) avant d'utiliser les gabarits RGPD.
- Communication aux personnes : aucune donnée personnelle d'un tiers, aucun
  détail technique exploitable par un attaquant.

## 5. Checklist finale avant remise

- [ ] Date de connaissance établie et échéance 72 h calculée et affichée ?
- [ ] Les trois livrables nécessaires identifiés (registre toujours ;
      CNIL si risque ; personnes si risque élevé) ?
- [ ] Décision de notifier / ne pas notifier motivée, attribuée au
      responsable de traitement, distincte de l'avis du DPO ?
- [ ] Notification par étapes proposée si informations incomplètes ?
- [ ] Téléservice CNIL mentionné ?
- [ ] Communication aux personnes en langage clair, sans jargon ?
- [ ] Coordonnées du DPO présentes dans (b) et (c) ?
- [ ] Références (72 h, art. 33-34) vérifiées ou « à confirmer » ?
- [ ] Champs manquants listés si `[INCOMPLET]` ?
