# ADR 0027 — Lecture séquentielle des entrées et nouvelle tentative 1.4.0

Date : 2026-10-21. Décision de Jo, lot B8 : « Préciser la consigne + tentative b ».

## Constat et changement exact

Le bilan de campagne-l140-a atteste 25 sessions et 17 048 191 jetons d'entrée,
une tentative consommée et l'arrêt first_case_or_process_failure au treizième
cas, l8-dsi-incident-ancien-spontane. Les deux erreurs observées sont
activation_entry_order_mismatch et activation_missing_or_unexpected. Les douze
premières relectures ne portent aucune violation ; elles ne sont pas transférées.
Le bilan et ses traces restent archivés sur place dans le harnais externe,
avec l'index archives/campagne-l140-a/index.json, sans assemblage de cette tentative.

Dans behavior_prompt seulement, après la consigne se terminant par
« max_output_tokens=8000 ; », ajouter exactement :

> Lis une seule entrée à la fois : termine tous ses segments avant d'ouvrir une autre entrée, sans lectures en parallèle.

Le texte restant est inchangé, y compris la sélection forcée ou spontanée,
la priorité STOP, le catalogue, les outils et les consignes de sources.
Le validateur codex_event_contract.py reste strict et inchangé ; le smoke,
les cas, les attendus STOP, les pins et les seuils restent inchangés.

## Protection du protocole et conservation de l'historique

run_codex_campaign.py est protégé par runner_sha256 dans le qualificateur et
par l'inventaire d'outillage dans compatible(). Il ne fait pas partie des
fichiers autorisés en H2 par l'ADR 0026. Ce changement impose donc une nouvelle
mesure complète sur H1b ; il n'est pas une équivalence avec H1 consommée.
Aucune transition d'équivalence n'est ajoutée pour réutiliser a, ou pour faire
passer une ancienne campagne avec le nouveau prompt. Les transitions 0013,
0017 et 0026 restent inchangées ; 0026 peut être fermée après la nouvelle
campagne sur le seul SHA H1b réellement mesuré, suivant sa procédure existante.
La modification du prompt se fait avant ce gel, jamais pendant la liaison H2.

La preuve 1.3.0 et son contrat v2 restent conservés et vérifiables dans leur
contexte Git historique. Ils ne qualifient pas le runtime 1.4.0 réépinglé :
la barrière de release de la branche, déjà rouge depuis B1, reste rouge tant
que release-1.4.0.json n'est pas assemblée. Accepter 1.3.0 comme preuve de H1b
contournerait les contrôles de version, de runtime et de protocole ; aucune
exemption de ce type n'est créée. Les tests historiques continuent sans changement.

## Préparation de b

campagne-l140-b est une tentative unique neuve : 18 cas v3, 36 sessions
réponse/relecture gpt-6.1-sol/high, suivi de 40 M jetons d'entrée entre rôles,
arrêt sur violation ou échec technique. Aucun résultat de a n'entre dans b.
Le home de campagne déjà connecté reste en place, sans lecture ni copie de
credentials. Jo a autorisé b avec la citation ci-dessus ; aucun modèle,
aucune connexion ni poussée n'est exécuté par B8. Au lancement futur, la tête
distante de la branche et refs/pull/20/head doivent correspondre à H1b ;
la poussée correspondante appartient à Claude.

Le diagnostic non probant H1b→H2→H3 reprend seulement les écarts D0–D3 du
pré-vol B5. Aucun artefact de a n'est assemblé. La fermeture diagnostique de
0026 se limite aux trois fichiers prévus ; la projection H3 reste publique
seulement. Docker est préparé, sans être exécuté dans ce lot.
