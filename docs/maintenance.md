# Maintenance du dépôt

Sections reprises de l'ancien README le 26/10/2026, sans changement de fond.
Elles s'adressent aux mainteneurs ; le [README](../README.md) s'adresse aux
utilisateurs du plugin.

## Sources et reproductibilité

### Outil de développement local

[Ponytail](https://github.com/DietrichGebert/ponytail) 5.1.0 est installé dans
`.agents/skills/ponytail/` pour développer ce dépôt uniquement. Il n'est pas
un skill distribué du plugin. Son point d'entrée vérifie la dernière release
stable publiée, le commit de son étiquette et les empreintes locales avant
chaque utilisation, puis affiche les règles seulement en cas de succès :

```text
python .agents/skills/ponytail/scripts/check_version.py
```

Version dépassée, fichiers modifiés ou contrôle réseau/API impossible :
**ne pas utiliser Ponytail**. Aucun cache de succès ni mise à jour automatique.
Les consignes de [AGENTS.md](../AGENTS.md) imposent aussi le recontrôle à chaque
tour où il serait appliqué. Les règles de développement restent soumises aux
instructions utilisateur et à la sécurité du projet. [Décision](adr/0008-ponytail-developpement-verifie.md).

### Runtimes métier du plugin

Chaque dossier `skills/<nom>/` provient des fichiers d'exécution d'un commit
amont figé. `upstream.json` fixe dépôt, commit, version et chemins inclus.
`dcp-fpt` reste une copie exacte, sans surcharge. Les six autres skills sont
des variantes locales du plugin, avec leurs surcharges dans `overlays/` et
leur chaîne ordonnée déclarée dans `instruction_overlays`.

Chaque étape vérifie l'empreinte SHA-256 exacte de son entrée et de sa surcharge.
Les insertions gardent leur ancre unique ; les remplacements sont bornés au
champ folded complet de description ou à la section `###` complète de même
titre, hors frontmatter. Toute dérive de base, d'ordre, de texte ou d'ancre
bloque la synchronisation. Les versions internes identifient les bases amont,
pas de nouvelles releases de ces dépôts. Le commit du plugin identifie la
variante complète. Aucun dépôt amont n'est modifié.

DSI 0.2.1 est figé à `704e5dd6a3d15994ed431b23585aabd72086ca75` :
30 fichiers runtime, sélection de #11, sans cache de valeurs. DPO 0.2.2 reste
figé à `58ea45c4d12812da10ace5f1486deea96b8534fa` (18 fichiers).
Les renvois DCP, les STOP et l'abstention sans source primaire sont conservés ;
les transferts imposent l'activation effective et une attribution persistante.

Pour `recherche-juridique`, la racine canonique `skill/` est aplatie dans `skills/recherche-juridique/`. Sa licence est copiée avec le runtime ; aucun manifeste, serveur MCP, fichier `.env` ou autre fichier de dépôt amont n'est dupliqué. Le fichier `references/cache-taux-seuils.md` de `dirfi-fpt`, exclu de son propre paquet de distribution, n'est pas embarqué.

Pour DCP 0.1.4, le commit correctif est figé :
`414cd4ecf41ba8b296908b738224355069b1890f`. Les 30 fichiers de son paquet
runtime et sa licence sont copiés ; le cache `references/cache-valeurs.md`,
la conception, les scripts d'évaluation et les preuves amont sont exclus.
Le registre daté reste une piste de recherche, jamais une preuve de lecture
officielle dans la session. Aucun correctif local du contenu DCP n'est appliqué.
Le statut de mesure autonome et la relecture de Jo sont documentés hors runtime
dans l'amont ; l'avertissement historique de l'entrée reste copié à l'identique.

Pour reproduire les copies depuis des dépôts locaux placés côte à côte :

```text
python scripts/sync_skills.py --local-repos C:\chemin\vers\repos
python scripts/check_sync.py --local-repos C:\chemin\vers\repos
```

Sans `--local-repos`, les scripts clonent les dépôts GitHub et vérifient les commits figés, puis appliquent uniquement les surcharges déclarées et vérifiées. La CI échoue si un fichier embarqué diffère du résultat reproductible, manque ou apparaît en plus. Une mise à jour d'un skill exige de modifier son commit et sa version dans `upstream.json`, de relancer la synchronisation et d'incrémenter la version du plugin dans les deux manifestes. Une correction locale exige de revoir ses empreintes et son ancre, de régénérer les copies et de refaire la campagne comportementale.

## Validation

```text
python scripts/check_sync.py
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
```

Pour contrôler l'intégration candidate sans qualifier une publication :

```powershell
$env:CT_EXIGER_ETIQUETTE="1"
$env:CT_SAUTER_BARRIERE="1"
python -m unittest discover -s tests
$env:CT_SAUTER_BARRIERE="0"
python -m unittest discover -s tests -k ReleaseGateTests
```

La CI découvre tous les tests dans le job **Intégration candidate** et ne
saute que `ReleaseGateTests`. Le job **Qualification de distribution open source**
force `CT_SAUTER_BARRIERE=0` et contrôle les preuves techniques, leurs empreintes,
le runtime et la configuration installée. Sans cette variable, la découverte
complète exécute aussi ce contrôle.

Sous un shell Unix, l'équivalent pour l'intégration est
`CT_EXIGER_ETIQUETTE=1 CT_SAUTER_BARRIERE=1 python -m unittest discover -s tests`.

Le manifeste Codex est également contrôlé avec le validateur du skill système `plugin-creator`. Les cas de `tests/cas-plugin.json` couvrent notamment :

- le garde-fou APJA sur une demande d'acte réservé à l'OPJ ;
- une gratification de départ mobilisant finances, RH et recherche juridique ;
- une violation de données mobilisant DPO et recherche juridique ;
- le comportement dégradé lorsque le MCP juridique est désactivé.
- les deux STOP DCP, les frontières financières et données, la dépendance DSI
  externe et le comportement DCP sans accès aux sources officielles.

Les preuves historiques de la distribution open source 1.2.0 exigent des traces comportementales en
conversations fraîches, le seuil de mesure DCP et un smoke installé réussi.
Le statut de cette distribution historique est conservé dans `tests/evidence/release-1.2.0.json` :
`distribution.ready` concerne cette distribution ; `deployment.ready` et
le champ historique `release_ready` restent faux sans qualification métier.
La relecture praticien devient une condition du déploiement opérationnel
dans une collectivité ou une structure tierce, selon l'[ADR 0007](adr/0007-distribution-open-source-et-deploiement.md).
Les preuves historiques et avis humains non réalisés restent inchangés.

Le lanceur `scripts/run_plugin_campaign.py` exécute les neuf scénarios dans
des sessions non persistées, impose les activations qualifiées attendues,
désactive les connecteurs juridiques globaux et ne conserve qu'une trace JSONL
assainie dans `tests/evidence/.work/`. La revue humaine des invariants métier
reste distincte et requise avant le déploiement opérationnel chez un tiers.

Pour la distribution historique 1.2.0, la campagne utilise Codex et
`scripts/run_codex_campaign.py` : copies natives en workspace frais,
lectures ordonnées par segments vérifiés, MCP juridique propre au processus
dans les sept cas nominaux, MCP absent dans les deux cas dégradés. La connexion
Codex existante suffit ; aucune connexion Claude n'est requise pour ce profil.
La campagne native ne teste pas le déclenchement implicite ou l'activation
Skill de Claude. Un smoke distinct installe le candidat exact depuis Git,
vérifie les six skills dans le contexte modèle et leurs octets, puis mesure
des réponses et appels MCP depuis ce cache, sans copie native en workspace.
Une demande sans nom de skill déclenche des lectures DCP/juridique et un STOP ;
la mémoire et les instructions utilisateur restent présentes, sans attribution
causale exclusive. La mesure autonome DCP avec web/MCP garde son profil distinct.

Ces résultats et avertissements historiques ne s'appliquent pas au candidat
1.3.0. Aucune preuve `release-1.3.0.json` n'est fabriquée. Les tests de preuve
restent inchangés et signalent cette absence ainsi que la divergence du runtime.
Un ancien test exige encore l'absence de DSI : il reste inchangé, en attente
de l'arbitrage L6. ADR 0007, séparation validate/release et seuils sont conservés.

`tests/cas-plugin.json` conserve ses neuf cas historiques, dont les cinq DCP.
`tests/cas-coactivation-dsi.json` ajoute huit cas locaux de structure (six
activations forcées, deux spontanées), sans jugement ni mesure. Les quatre tests
de structure associés ne prouvent aucun comportement du modèle. Ce fichier
n'est pas raccordé aux lanceurs historiques : leur activation forcée systématique
ne permet pas d'évaluer les nouveaux cas spontanés en l'état. Aucune campagne,
installation, qualification ou requête modèle n'accompagne cette intégration.

## Architecture et décisions

- `.codex-plugin/plugin.json` : manifeste de compatibilité Codex.
- `.claude-plugin/plugin.json` : manifeste Claude Code.
- `.agents/plugins/marketplace.json` et `.claude-plugin/marketplace.json` : catalogues de distribution.
- `.mcp.json` : unique déclaration du serveur `droit-francais`.
- `skills/` : sept runtimes figés et synchronisés.
- `upstream.json` et `scripts/` : provenance et contrôle de dérive.

Le format de compatibilité actuel reste volontairement utilisé pour le candidat 1.4.0. La migration vers le manifeste portable Agent Plugins fera l'objet d'un chantier séparé. Le plan de construction et les décisions d'architecture sont conservés dans `docs/`, dont l'[ADR DCP](adr/0003-integration-candidate-dcp.md) et le [relevé d'intégration](integration-dcp-2026-10-06.md).

## Licences

L'outil de développement Ponytail conserve sa licence MIT propre dans
`.agents/skills/ponytail/LICENSE` ; il ne fait pas partie des sept contenus
métier/juridiques embarqués.

La licence DCP accompagne sa copie. Le texte CC-BY-SA-4.0 accompagne également
la copie du runtime `recherche-juridique` dans `skills/recherche-juridique/LICENSE`.
