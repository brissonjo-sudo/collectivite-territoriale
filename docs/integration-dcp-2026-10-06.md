# Intégration candidate DCP — 2026-10-06

## Périmètre et provenance

Base plugin : `cad8bbdbc1db2163c758fb46ef3e745a18c9c957` (1.1.1).
Ajout DCP : `eeb1cb14a3ad94d78631661dce5ae11f1e071308` (0.1.0),
commit de fusion de la PR #4 dans `brissonjo-sudo/DCP-fpt`.
Candidat plugin : 1.2.0, branche `codex/integrer-dcp-candidate`.

Le checkout de travail est isolé du dépôt local habituel, qui contient des
preuves de qualification non commitées. Ces fichiers sont préservés ; aucune
preuve locale non versée n'est transformée en qualification du candidat.

Six skills et 167 fichiers runtime : les 136 fichiers existants restent
identiques ; 31 fichiers DCP s'ajoutent (30 du paquet amont et sa licence).
Le cache DCP, la conception et les outillages de campagne sont exclus.
Les bases et surcharges des cinq skills existants, ainsi que le MCP, sont
inchangées. Aucun nouveau résultat juridique n'est attesté par cette copie.

## Contrôles

Contrôles locaux Windows/PowerShell, Python embarqué 3.12.14 :

```text
python scripts/check_sync.py
python -m unittest discover -s tests -k SyncCheckTests -k CodexPluginTests -k InstructionOverlayTests
python -m unittest discover -s tests -k ReleaseGateTests
claude plugin validate .claude-plugin/plugin.json
claude plugin validate .claude-plugin/marketplace.json
git diff --check
```

- Six skills conformes à leurs commits et surcharges déclarés.
- 31 tests techniques réussis ; découverte complète : 32 tests, dont le seul
  échec attendu de barrière de publication. Aucun test technique en échec.
- Manifestes Claude du plugin et de sa marketplace valides avec Claude Code
  2.1.288. Le contrat Codex est contrôlé par les tests locaux.
- Aucun pointeur inter-dépôts cassé de la forme détectée par la CI ; aucun
  diff dans les cinq runtimes existants, les surcharges et `.mcp.json`.
- `git diff --check` sans erreur. Les fichiers de maintenance suivent LF ;
  les blobs runtime amont restent copiés sans conversion de fins de ligne.

La CI exécute ces contrôles dans deux jobs : intégration candidate et
qualification de publication. Le test de barrière doit rester en échec tant
que la preuve 1.2.0 contient `release_ready=false` ; tout autre échec est une
régression. Aucun résultat CI distant n'est encore attesté dans ce relevé.

L'aide de Claude Code 2.1.288 annonce les options `--restricted`,
`--strict-mcp-config`, `--tools`, `--allowedTools`, `--permission-prompts`,
`--setting-sources`, `--no-session-persistence` et `--plugin-dir`. Cette
présence dans l'aide ne prouve pas leur comportement en campagne réelle.

## Suite et limites

La relecture par un acheteur/juriste est différée après l'intégration
candidate par décision de l'utilisateur. Elle reste due avant qualification
et publication. Ni fusion du plugin, ni installation, ni tag, ni release,
ni campagne facturée ne sont effectués dans ce lot.

La suite métier DCP et sa mesure restent à préparer. Les neuf scénarios de
coactivation du plugin, dont cinq nouveaux DCP, restent non exécutés sur ce
candidat. Vérifier les CLI réelles, le MCP authentifié, les profils d'outils
et les traces avant mesure ; les résultats du lanceur autonome DCP sans MCP
ne sont pas automatiquement comparables à ceux du plugin.

`dsi-fpt` reste une compétence externe : le renvoi se termine au signalement
de cette frontière si le skill n'est pas disponible. Les frontières des
autres skills n'ont pas été modifiées dans cette intégration candidate.
