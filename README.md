<p align="center"><img src="assets/banner.svg" width="800" alt="Dessin au trait : six agents de la collectivité posent devant une mairie pavoisée (un policier municipal qui salue, une responsable RH, un directeur financier, une déléguée à la protection des données, une acheteuse publique qui tamponne un contrat et un informaticien), avec au-dessus d'eux une luciole qui porte un Code rouge. Toute la mairie autour de votre question."></p>

# Collectivité territoriale : six métiers, un droit vérifié

**Un plugin Claude Code et Codex pour les agents des collectivités : police municipale, ressources humaines, finances, données personnelles, commande publique et informatique, avec le droit vérifié sur les sources officielles.**

[![Validation du plugin](https://github.com/brissonjo-sudo/collectivite-territoriale/actions/workflows/ci.yml/badge.svg)](https://github.com/brissonjo-sudo/collectivite-territoriale/actions/workflows/ci.yml)
[![Version](https://img.shields.io/github/v/tag/brissonjo-sudo/collectivite-territoriale?filter=v*&label=version)](docs/publication.md)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/license-CC%20BY--SA%204.0-blue)](LICENSE)

En mairie, une question touche souvent plusieurs services. Une prime engage
les RH et le budget ; une caméra engage la police municipale, la protection
des données et l'informatique. Le plugin mobilise chaque métier concerné :
chacun traite son volet et passe la main pour le reste. Les règles de droit
sont vérifiées sur Légifrance et Judilibre pendant la session, et ce qui n'a
pas pu l'être est signalé.

> Outil d'aide à la décision, pas un avis juridique. Il ne remplace ni la
> validation d'un juriste, ni le contrôle de l'autorité compétente, ni la
> lecture des textes officiels en vigueur.

## Exemple

Question posée lors de la campagne de qualification de la version 1.4.0 :

> *« Le DGS me demande de verser dès ce mois-ci une prime exceptionnelle de
> 800 € à un agent qui part à la retraite la semaine prochaine, pour le
> remercier de son investissement. Le chapitre 012 a des crédits disponibles et
> le maire est d'accord oralement. La délibération instaurant cette prime n'a
> pas encore été votée par le conseil municipal, mais le DGS me dit qu'on
> régularisera après coup au prochain conseil. Je peux engager le
> mandatement ? »*

La réponse devait remplir huit critères, et les a remplis (relecture humaine
du 22 octobre 2026) :

- elle refuse le mandatement en l'état ;
- les finances (`dirfi-fpt`) passent explicitement la main aux RH (`drh-fpt`)
  avant d'analyser la prime ;
- une délibération ne suffit pas à créer une gratification pour un seul agent,
  et une régularisation après coup est écartée ;
- aucun régime indemnitaire (CIA, RIFSEEP, ISFE) n'est présumé avant de
  connaître la situation de l'agent ;
- l'absence d'indemnité de départ à la retraite est établie sur la
  [réponse ministérielle du 22/05/2025](https://www.senat.fr/questions/base/2024/qSEQ241001222.html),
  consultée pendant la session ; le CIA n'est évoqué que sous condition ;
- les références sont vérifiées sur une source officielle en vigueur, avec la
  méthode `recherche-juridique`.

## Les sept skills

| Skill | Pour quoi faire | Version |
|---|---|---:|
| `dpm-fpt` | Police municipale : pouvoirs du maire, limites des agents (APJA), doctrine de terrain | 1.0.5 |
| `drh-fpt` | Ressources humaines : carrière, paie, régime indemnitaire, instances | 0.7.0 |
| `dirfi-fpt` | Finances locales : budget, exécution, régies, dette, fiscalité | 1.0.5 |
| `dpo-ct` | Données personnelles : registre, AIPD, violations, droits des personnes | 0.2.2 |
| `dcp-fpt` | Commande publique : passation et exécution juridique des marchés | 0.1.4 |
| `dsi-fpt` | Informatique : sécurité, continuité, cloud, contrats techniques | 0.2.1 |
| `recherche-juridique` | Méthode commune : recherche, vigueur et citation du droit français | 3.6.0 |

`dsi-fpt` est embarqué depuis la 1.3.0. DCP garde la passation et l'exécution
juridique du marché ; DSI prend les spécifications, les niveaux de service, la
réversibilité et l'exécution technique.

Chaque skill est publié dans son propre dépôt. Le plugin en embarque une copie
figée, dont la provenance est vérifiée à chaque intégration : voir la
[maintenance du dépôt](docs/maintenance.md).

## Démarrage rapide

### Dans Claude Code

```text
/plugin marketplace add brissonjo-sudo/collectivite-territoriale
/plugin install collectivite-territoriale@collectivite-territoriale
```

Ouvrez une nouvelle session, lancez `/mcp`, choisissez `droit-francais` et
autorisez l'accès dans le navigateur. Le client OAuth est public : aucun secret
n'est à saisir.

Pour passer à une nouvelle version publiée :

```text
/plugin marketplace update collectivite-territoriale
/plugin update collectivite-territoriale@collectivite-territoriale
```

### Dans Codex

```text
codex plugin marketplace add brissonjo-sudo/collectivite-territoriale --ref main
codex plugin add collectivite-territoriale@collectivite-territoriale
```

Le catalogue est lu sur `main`, mais le plugin est récupéré à l'étiquette
publiée qu'il désigne. Mise à jour : `codex plugin marketplace upgrade collectivite-territoriale`.
Le plugin s'installe aussi depuis le répertoire des plugins de l'application
de bureau, une fois la marketplace ajoutée. Dans un espace de travail ChatGPT,
l'import et les autorisations relèvent de l'organisation.

## Ce que vous obtenez

- Face à un acte réservé à un officier de police judiciaire, un incident cyber
  ou une surveillance, la réponse commence par un STOP, avant toute autre
  analyse.
- Chaque métier traite son volet et nomme le skill qui prend le reste. Un
  skill installé mais non chargé n'est pas présumé actif : si le rôle requis
  manque, la réponse s'arrête sur ce volet.
- Une règle de droit n'est conclue qu'après lecture du texte primaire dans la
  session. Sans source, la règle et sa référence sont retirées, même
  présentées avec réserve.
- Les garde-fous propres à chaque métier restent actifs : limites des APJA,
  gestion de fait et régularité budgétaire, égalité de traitement et actes
  irréversibles en commande publique.
- Si le serveur juridique est indisponible, la réponse le dit et n'invente
  aucune référence.

## Questions fréquentes

**Où vont mes questions ?** Les requêtes juridiques passent par le serveur MCP
`droit-francais`. Voir la [politique de confidentialité](PRIVACY.md). Le
serveur peut être désactivé si vous ne voulez pas transmettre vos requêtes.

**Et sans le serveur juridique ?** Les skills métier fonctionnent. La réponse
signale qu'elle n'a pas pu vérifier le droit et ne cite rien de mémoire.

**J'ai déjà installé certains skills séparément.** N'installez pas le plugin en
plus des skills individuels : les deux jeux coexistent sous des noms
différents et doublent le contexte chargé.

**Puis-je le déployer dans ma collectivité ?** La distribution est libre. Avant
un usage opérationnel dans une autre structure, une relecture par un praticien
reste recommandée : voir la [note praticien](docs/deploiement-collectivite.md).

## État du projet

| Composant | État au 26 octobre 2026 | Détail |
|---|---|---|
| Plugin | 1.4.0, publiée le 23/10/2026 (étiquette `v1.4.0`) | Distribuée par les marketplaces Claude Code et Codex |
| Qualification | Campagne 18/18, smoke d'installation 2/2 | Relecture humaine avec une réserve : un lien local dans un cas DCP, correction prévue dans DCP-fpt 0.1.5 ([ADR 0029](docs/adr/0029-retrait-surcharge-dcp-et-reserve-0-1-5.md)) |

## Mesure de la qualité

Avant sa publication, la 1.4.0 a passé une campagne de dix-huit cas métier.
Pour chaque cas, des critères sont fixés à l'avance ; un modèle répond, un
autre relit, puis l'auteur relit chaque réponse. Un smoke installe ensuite
le plugin depuis Git et vérifie l'activation et les appels au serveur
juridique. Les résultats et leurs empreintes sont dans
[`release-1.4.0.json`](tests/evidence/release-1.4.0.json) ; la procédure est
décrite dans la [publication](docs/publication.md).

## Pour aller plus loin

- [Publication et registre des versions](docs/publication.md)
- [Maintenance, reproductibilité et validation](docs/maintenance.md)
- [Décisions d'architecture](docs/adr/)
- [Historique des versions](CHANGELOG.md)

## Licence et contribution

Le plugin et ses sept skills sont distribués sous licence
[CC BY-SA 4.0](LICENSE), avec attribution à `brissonjo-sudo`. Les textes,
décisions et métadonnées récupérés depuis Légifrance ou Judilibre restent
soumis aux conditions de réutilisation de leurs producteurs.

Questions, erreurs, propositions : ouvrir une
[issue](https://github.com/brissonjo-sudo/collectivite-territoriale/issues).
