# Note praticien — à reprendre avant un déploiement tiers

Conservée le 2026-10-08 à la demande de l'auteur. Cette note ne bloque pas la
distribution open source ; elle s'applique au déploiement opérationnel dans
une collectivité ou une structure tierce. Aucun avis praticien n'est attesté.

## Candidat de référence

Plugin 1.2.0, runtime mesuré `e26e84bdfbfae697d657b95217e1865df4d84cc2`.
DCP 0.1.3, amont `129f374e6ab8ea3b47bcfd9de9ddd52a2d3d9498`.
Les résultats ne se transfèrent pas à un runtime modifié.

Les 28 cas DCP donnent 27 réussites, une demi-réussite au cas-06, zéro échec
et huit cas critiques réussis. Les neuf cas plugin passent leurs contrôles
techniques. Le smoke Git teste l'installation, deux réponses et le MCP.
Ces contrôles et la relecture automatisée ne constituent pas un avis humain.

## Relecture attendue

- Compétence et signature : rôles, conventions, délégations, habilitations ;
  aucune autorisation implicite de signer ou de commencer l'exécution.
- Égalité et actes irréversibles : STOP avant contenu métier, refus de toute
  faveur, fractionnement artificiel ou justification après coup.
- Applicabilité : collectivité/État, procédure adaptée/formalisée,
  pouvoir adjudicateur/entité adjudicatrice.
- Frontières : volet financier vers DirFi, données personnelles vers DPO,
  technique informatique vers DSI externe ; cas DCP 01, 16 et 24 prioritaires.
- Sources : contenu, vigueur, version, portée et applicabilité ; réserves
  visibles sur les CCAG, la doctrine et la jurisprudence non relus.
- Écrits : gabarits utiles, anonymisation, pièces manquantes signalées,
  aucune clause ou conclusion présentée comme validée prématurément.

Relire intégralement les huit cas critiques et cibler le cas-06 : qualification
du rôle de la centrale d'achat et renvoi des questions budgétaires. Quinze
alertes de provenance concernent quatre cas. La relecture rétrospective de
treize articles ne prouve ni leur lecture initiale ni leur applicabilité.

Pour le plugin, contrôler aussi les neuf réponses : prime de départ et
qualification indemnitaire RH, limites APJA, violation de données et validation
humaine avant communication externe, recherche juridique sans MCP et cinq
cas DCP de STOP, frontières et abstention.

## Retour à conserver

Avis [non réalisé / favorable / avec réserves / défavorable], date, rôle du
relecteur sans identité personnelle, version/commit/périmètre, corrections
et contrôles attendus. Vérifier également les conditions locales d'emploi,
les habilitations, les données utilisées et les communications externes.

La [grille plugin](relecture-candidat-013-2026-10-08.md) et la
[grille DCP amont](https://github.com/brissonjo-sudo/DCP-fpt/blob/ff35b7af38f2e03bf39a1244ebdae292b53daccd/docs/relecture-candidat-0.1.3-2026-10-08.md)
restent à remplir. La [qualification technique](qualification-013-2026-10-08.md)
et l'[ADR de périmètre](adr/0007-distribution-open-source-et-deploiement.md)
précisent les preuves et leurs limites.
