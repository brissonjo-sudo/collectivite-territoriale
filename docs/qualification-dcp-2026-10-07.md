# Qualification candidate 1.2.0 — 2026-10-07

## Périmètre contrôlé

Candidat fusionné `85011f7f86b488330fe00ff7a30ce42d6dbe9a84` : six skills,
DCP 0.1.0 figé à `eeb1cb1`, DRH 0.6.0. Les neuf scénarios de coactivation,
la mesure autonome DCP, le smoke et la relecture métier restent distincts.
La distribution reste v1.1.1 sur cad8bbd ; aucun nouveau tag ni installation.

## Contrôles réels

Claude Code 2.1.288 et Codex CLI 0.160.0 : options contrôlées sur leur aide.
Une recherche du MCP juridique réussit dans la session Codex principale.
Le premier cas Claude (`plugin-dcp-egalite`) charge les six skills du
candidat, sans skill juridique autonome, mais le MCP indique `needs-auth`
et la sortie modèle signale une limite de session. Aucun outil MCP ne
réussit, aucune activation n'est mesurée et le coût déclaré est nul.
Ce précontrôle est conservé, sans le promouvoir en cas qualifié.

Le smoke Codex en dossier neuf vérifie les six copies natives et versions,
le manifeste, les STOP DCP et le contrat DRH. Lectures locales réussies,
sans web ni MCP. Il ne valide pas l'installation marketplace ni le
chargement complet du plugin avec MCP. Sa portée est indiquée dans la preuve.

Preuves assainies : `tests/evidence/2026-10-07-candidat/`.
La sortie brute du précontrôle est éliminée en mémoire ; la trace ne conserve
ni raisonnement ni signature. Le lanceur dispose désormais d'un timeout et
d'un arrêt explicite au premier échec pour éviter une campagne nominale
répétée sur un accès indisponible.

## Suite autonome DCP

Le dépôt DCP a achevé les 28 cas du cadrage, avec répondant Codex web et juge
sans web, dans des processus séparés et une campagne séquentielle.
La correction Windows rétablit le backend sandbox en lecture seule malgré
`--ignore-user-config`. Le premier essai sans lecture des branches est écarté.
Les réponses, jugements et empreintes du nouveau kit sont conservés côté DCP.
Résultat du juge : 26 réussites, une demi-réussite (cas-16), un échec (cas-01),
aucun échec critique. Seuil automatique atteint. Les cas-01 et 16 appellent
une relecture de la frontière financière ; douze citations sur sept cas
n'ont pas d'ouverture explicite correspondante dans la trace. Ce signal
demande une relecture des sources, sans requalifier silencieusement le score.
Preuves amont dans la PR DCP #6, commit `1c13431`. Ce résultat ne remplace pas
les neuf cas de coactivation du plugin.

## Profil Codex retenu

À la demande de l'utilisateur, Claude est écarté de cette campagne. Aucune
connexion Claude supplémentaire n'est nécessaire. Un processus Codex neuf
a confirmé un appel MCP réussi avec la connexion OAuth existante. La preuve
est propre à ce processus ; elle ne repose pas sur la connexion du chat.

Le profil natif Codex est défini dans l'ADR 0005. Le premier cas DCP égalité
a réussi les contrôles de lectures ordonnées et d'appel MCP. Le lanceur
suivant exécute les neuf cas, séquentiellement, avec copies natives et
configuration d'outils explicite :

```powershell
python scripts/run_codex_campaign.py --timeout 360 --output-dir tests/evidence/.work/codex-natif-nouvel-essai
```

Les preuves retenues sont dans `tests/evidence/2026-10-07-codex-natif/`.
Le lanceur refuse d'écraser un dossier de cas existant. Le cas égalité initial
conserve seulement le nom, statut et empreinte du résultat MCP ; les cas
suivants ajoutent les arguments documentaires publics et identifiants du
résultat, sans contenu juridique brut ni donnée de partie. Aucun appel
Claude n'est déduit de ces lectures natives.

Le profil dégradé reste distinct et ne remplace aucun des sept cas nominaux.
Les neuf réponses doivent ensuite être relues sur leurs invariants ; une
réussite technique n'est pas une validation juridique humaine. La grille
praticien DCP et les réserves du socle font partie du dossier à examiner.
`release_ready=false` reste en place.

## Résultat du profil Codex

Les neuf cas ont terminé et réussi les contrôles techniques : chemins de
lecture ordonnés, appels MCP réussis pour les sept nominaux, absence de MCP
et de web pour les deux dégradés, ouvertures officielles du cas RGPD.
Leurs empreintes de runtime correspondent toutes aux copies figées du
candidat `85011f7`. Les contrats métier sont inchangés. La séquence de
skills est imposée par le prompt ; le déclenchement implicite n'est pas testé.

Les 43 tests sont découverts : 42 réussissent, seule la barrière de publication
est ignorée dans le contrôle d'intégration. `check_sync.py` confirme les six
copies amont et l'étiquette distribuée reste contrôlée. Les contre-épreuves
vérifient aussi timeout, refus d'une fausse réussite MCP, absence de preuve
par simple mention, mode dégradé et rattachement des preuves aux cas/runtime.

La [grille de relecture](relecture-codex-2026-10-07.md) est prête et vierge.
Une réserve de présentation est déjà observée par l'assistant sur le cas
`plugin-dcp-frontieres-finance-donnees` : les BASCULE dirfi et DPO apparaissent
après leurs intertitres dédiés, alors que les invariants exigent l'ordre
inverse. Elle est rattachée à l'empreinte de la réponse dans
`relecture-assistant.json`, sans transformer cette observation en avis
praticien ni changer le statut technique. La réponse n'est pas réécrite.
`native_campaign` conserve ces résultats distinctement des `runs` qualifiés :
aucun invariant humain n'est renseigné automatiquement. La mesure DCP complète
est référencée avec contrôle des octets embarqués, au statut
`completed_pending_review`. Installation du plugin, sources et relecture
praticien restent ouvertes. La CI de publication doit encore échouer tant
que la barrière n'est pas satisfaite.
