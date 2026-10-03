# ADR 0001 — Embarquer `recherche-juridique` dans le plugin territorial

- **Date** : 2026-09-20
- **Statut** : accepté
- **Supersède** : la décision « Ne pas embarquer `recherche-juridique` » du
  plan initial `docs/plan-plugin.md`

## Décision

Le plugin `collectivite-territoriale` distribue `recherche-juridique` comme
cinquième skill, en plus des quatre expertises métier. Le runtime canonique est
copié depuis le dossier `skill/` du dépôt `droit-francais-skill`, à un commit
figé dans `upstream.json`.

Le serveur MCP `droit-francais` déjà déclaré reste l'unique serveur juridique
du plugin. Il fournit les outils d'accès aux sources ; le skill fournit la
méthode de recherche, les règles de provenance, la vérification de vigueur et
les formats de citation.

## Motifs

Le plugin vise une installation autonome pour d'autres collectivités. La
présence du seul serveur MCP ne garantit ni la méthode anti-hallucination ni
la disponibilité du skill lors des routes DPM, DRH, DPO ou DirFi. Les campagnes
antérieures ont également montré qu'un résultat obtenu sans les skills de
co-activation attendus n'est pas interprétable comme une régression métier.

Le risque de dérive de version est maîtrisé par le commit figé, la copie
déterministe et `scripts/check_sync.py`.

## Conséquences

- Le plugin passe en version 1.1.0 et expose cinq skills.
- La licence amont de `recherche-juridique` accompagne sa copie.
- Le dépôt juridique, ses manifestes et son serveur MCP ne sont pas imbriqués.
- La co-installation ne prouve pas la co-activation : les scénarios de
  validation doivent tracer les skills réellement disponibles et activés.
