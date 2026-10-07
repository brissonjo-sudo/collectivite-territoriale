# Filtre web natif par hôte littéral

Le contrat répondant impose les hôtes autorisés, sans imposer le paramètre
`domains` de web__run. Une recherche sans ce champ est donc recevable uniquement
si `q` commence par `site:<hôte exactement autorisé> `, avec un seul filtre site,
sans OR, exclusion de site, URL, autre hôte, saut de ligne ni syntaxe d'injection.

L'enveloppe distincte `controler_codex_dev5_r2_site_literal.py` dérive le domaine
pour son contrôle interne. Elle conserve l'objet `actual_arguments` original,
sans y ajouter un champ qui n'a pas été envoyé par le répondant. Les receipts et
preuves portent le SHA de cette enveloppe et `basis=literal_site` pour ces appels.

Les URLs retournées restent filtrées sur les hôtes autorisés. Une recherche
reste `search_result`. L'enveloppe ne récupère aucune nouvelle source et ne
réécrit ni réponse, runtime, suite, barème ni script déjà gelé. Un vrai appel
hors scope produit une trace techniquement échouée qui conserve l'identité,
les lectures intégrales et la réponse ; les sources non autorisées ne deviennent
jamais primaires.

Le PDF EUR-Lex reçu dans le cas 03 reste documenté comme résumé ou contenu
partiel lorsque le passage normatif complet n'est pas attesté par le parseur.
Cette limite documentaire n'est pas transformée en preuve juridique ou en
succès. La qualification comportementale revient au juge frais, sur les seuls
contenus effectivement capturés. `release_ready=false`.
