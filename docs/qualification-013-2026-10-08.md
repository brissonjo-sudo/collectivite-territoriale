# Qualification du candidat avec DCP 0.1.3 — 2026-10-08

Baseline plugin : `e26e84bdfbfae697d657b95217e1865df4d84cc2`.
DCP amont : `129f374e6ab8ea3b47bcfd9de9ddd52a2d3d9498`.
Les cinq autres bases amont restent inchangées ; la surcharge DPO demande
explicitement une validation humaine avant communication externe.

Les 28 cas DCP donnent 27 réussites, une demi-réussite au cas-06, zéro échec
et huit critiques réussis. Le seuil automatique est atteint. Quinze alertes
de provenance couvrent treize articles relus après exécution ; leur lecture
dans la session initiale et leur application au dossier restent à relire.
La copie de synthèse est empreintée et confrontée aux trente fichiers DCP.

La campagne native v5 utilise le protocole v4 : **neuf cas techniquement
réussis**, sept avec MCP, deux sans accès aux sources. Les entrées sont lues
par segments ordonnés dont les contenus sont vérifiés. Les références
complémentaires ne sont pas toutes couvertes intégralement. Neuf premières
réponses conservées, sans remplacement par des reprises.

La relecture de chaque réponse par un processus séparé ne relève aucune
violation textuelle des invariants examinés. Les assertions qui exigent
les textes sources ou une analyse juridique sont déclarées non vérifiables.
Cela ne certifie ni l'exactitude juridique ni un avis praticien. La réponse
DPO distingue les conditions de notification et d'information et exige
la relecture/validation par le DPO humain avant envoi.

Le smoke installe le candidat depuis une source Git épinglée à la branche
candidate et à son SHA, dans un espace sans compte. Seul le cache est
répliqué pour un profil Codex distinct utilisant l'authentification existante.
Aucun secret copié ; configuration utilisateur principale inchangée.
Les 167 fichiers de skills, les manifestes, le MCP et l'asset sont comparés
aux blobs du commit. Les six noms qualifiés sont visibles dans le contexte
modèle, sans copies natives ajoutées au workspace.

Deux réponses modèle réussissent : une demande sans nom de skill lit les
entrées DCP et juridique du cache et produit un STOP contre le fractionnement ;
l'autre lit ces entrées et récupère l'article pertinent via le MCP installé.
Les lectures, appels, métadonnées et réponses sont empreintés. Le contrôle
des lectures du smoke n'atteste pas une couverture intégrale des entrées.
Les instructions, la mémoire et les skills système restent présents : aucun
effet causal exclusif du candidat n'est déduit. Le premier transport Git a
échoué sur la longueur de chemin Windows ; `core.longpaths=true` limité au
processus a permis la reprise, sans modification Git globale.

Le catalogue public v1.1.1 demeure distinct de cette source Git candidate.
La nouvelle distribution reste à qualifier lors de la publication.

L'essai v4 historique conserve sept réussites et deux rejets Select-String
en lecture seule, sans blanchiment du statut. Le protocole suivant explicite
les formes de lecture acceptées ; les réponses sont remesurées. Un chemin
personnel a été assaini dans une preuve v4, avec original privé empreinté.

Preuves : `tests/evidence/2026-10-07-codex-natif-v5/` et
`tests/evidence/2026-10-08-candidat-013/`. Le manifeste
`tests/evidence/release-1.2.0.json` garde `release_ready: false` et distingue
les contrôles techniques réussis des invariants non attestés humainement.
La [grille praticien](relecture-candidat-013-2026-10-08.md) reste vierge.
La barrière de publication doit rester en échec jusqu'aux avis requis.

Contrôles locaux : soixante tests logiciels réussis, un contrôle de publication
écarté de l'intégration candidate. La synchronisation des six skills réussit.
