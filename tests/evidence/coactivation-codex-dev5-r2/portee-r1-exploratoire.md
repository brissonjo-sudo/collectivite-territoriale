# Statut exploratoire, contexte intégral non établi

2026-10-07. Ce dossier conserve les premières tentatives Codex dev.5.

Le test de lecture intégrale de `recherche-juridique/SKILL.md` a affiché
une coupure de 2 363 tokens dans le contexte visible du contrôleur.
Les entrées volumineuses présentent le même risque. Les traces natives
conservent des sorties complètes qui ne suffisent pas à certifier les octets
effectivement présentés au modèle.

La relecture par fragments du juge APJA établit ses observations sur la
réponse reçue. Elle n'établit pas rétroactivement la présentation complète
des instructions à son répondant. Son jugement reste exploratoire.

Les réponses, traces, sources, paquets et jugements déjà produits restent
conservés. Le répondant 08 a été interrompu avant achèvement après découverte
du défaut. Les cas 09 à 16 n'ont pas de répondant créé dans cette tentative.
Les cas non jugés ne reçoivent aucun score inventé.

La nouvelle campagne `qualification-coactivation-dev5-codex-r2` doit
fragmenter les entrées, les instructions et les paquets de jugement avant
création des rôles. Chaque fragment est borné à 8 000 caractères, reçu
intégralement, puis confronté aux octets du fichier original.
Elle utilise de nouveaux répondants et juges sans historique, ni réponse,
source ou score transféré de cette tentative.

Le runtime dev.5 et les 124 exigences restent figés. Ce changement concerne
la présentation des données à Codex. `release_ready=false` demeure.
