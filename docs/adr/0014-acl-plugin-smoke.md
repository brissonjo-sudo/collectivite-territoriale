# ADR 0014 — Lecture du seul plugin installé par le sandbox Windows

Date : 19 octobre 2026. Décision de Jo, T43-L18.
Statut : correctif et préparation locaux ; aucun modèle ni smoke exécuté par ce lot.

## Périmètre autorisé

Après installation et contrôle des octets, le runner Windows résout par nom
le groupe local `CodexSandboxUsers` avec `Get-LocalGroup`, puis accorde
`(OI)(CI)RX` au seul répertoire de version du plugin installé dans
`codex-home/plugins/cache/qualification-l9/collectivite-territoriale/`.
La commande `icacls <plugin> /grant *<SID-résolu>:(OI)(CI)RX` n'utilise ni
récursion, ni remplacement, ni modification de propriétaire ou d'héritage.
L'absence du groupe est un échec explicite, sans octroi de remplacement.
Les liens/jonctions et toute cible différente sont refusés avant la mutation.
Aucun octroi ne vise `codex-home`, ses parents ou les autres caches/profils.
Aucun octroi n'est exécuté hors Windows.

## Attestation et refus

La lecture structurée des ACL vérifie l'absence de toute autorisation du groupe
sur `codex-home`, avant et après l'octroi ; son DACL doit rester identique.
Sur le plugin, le seul ACE du groupe doit être explicite, Allow, héritable
sur objets et conteneurs, sans propagation restreinte, et limité à ReadAndExecute
(avec Synchronize ajouté par Windows). Une erreur ou un droit plus large refuse
la préparation ; aucune correction automatique d'une permission préexistante.

Le reçu scellé `prepared.json` consigne groupe/SID, commande, cible, code retour,
contrôle ACL et empreinte du DACL du home. Le statut du lanceur expose la même
attestation. Run exige ce reçu puis relit les ACL avant login et tout modèle ;
un reçu manquant/étranger ou une dérive conduit au refus. Run ne modifie aucune ACL.
Le contrôle préalable natif L17b demeure obligatoire et indépendant du smoke.

## Renouvellement exact de l'empreinte du runner

L'ADR 0013 continue d'imposer sa liste fermée et ses empreintes exactes. Ce lot
renouvelle uniquement l'entrée cible `scripts/run_codex_smoke.py` du manifeste
`scripts/toolchain-transition-0013.json`, du SHA-256
`a1db28258d202c49bf215c4ab83b181896c2bc716c2219b63b4bdf57eaaa99c5`
au SHA-256
`f84178ed42528c7cb89ce9b2812a4de77e8470ec40c4cdcf1a43b3d74bf8441d`.
Les deux empreintes sources L14, les cinq autres empreintes cibles, le verrou
campagne, les validateurs et leurs tests, les seuils et la CI sont inchangés.
Aucune exemption de chemin ou de contrôle n'est ajoutée. Toute autre modification
ultérieure de ce runner devra de nouveau être liée explicitement.

Ce renouvellement lie l'outillage ; il ne transfère aucun résultat de smoke ni
ne qualifie le candidat. La nouvelle tentative `smoke-l18-20261019-a` est préparée
pour la nouvelle tête ; anciennes tentatives intactes, aucun assemblage de release.

## Documentation et vérification

Context7 consulté en premier : quota mensuel dépassé, aucune réponse documentaire.
Repli vers les documentations officielles :
[icacls](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls),
[Get-Acl](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-acl?view=powershell-7.5),
[subprocess Python 3.13](https://docs.python.org/3.13/library/subprocess.html).
Les tests simulent les sous-processus ; une lecture locale distincte vérifie
Get-LocalGroup/Get-Acl sans aucune mutation de permission. Le PSModulePath hérité
de PowerShell 7 est retiré du seul environnement enfant PowerShell système 5.1,
pour que ses modules natifs se chargent ; aucun profil ni réglage global modifié.
