# Reprise native dev.7 — préparation du 9 octobre 2026

Cette archive ajoute un diagnostic et des outils de reprise au candidat
`fb186b4951b95adabf05904f8a34995720588be3`. Elle ne produit aucune nouvelle
réponse ni mesure. La mesure R3 reste de trois cas sur seize : deux réussites,
un échec ; 16 atomes vrais, 1 faux, 6 non vérifiables sur 23.

## Blocages observés

Quatre sorties natives R3 « setup refresh had errors » sont corrélées au
journal Windows : erreur 32 au rafraîchissement ACL de `node.exe`, fichier
utilisé par un autre processus. Les écarts temporels sont inférieurs à 0,1 s.
Le diagnostic fournit les SHA des lignes, sans attribuer un PID propriétaire
historique. Le premier export local est conservé ; le v2 harmonise uniquement
la convention de SHA des lignes, hors fins de ligne, avec celle des traces R3.
Les traces et jugements R3 ne sont pas modifiés.

Quatre sondes sans modèle ont essayé des overrides de capacités, le service
sandbox, un chemin Node disponible et la désactivation des dépendances.
Toutes ont échoué dans l'application ouverte. Permissions `elevated`,
`read-only`, `never`, configuration persistée et cache préservés.
La correction à froid reste à vérifier ; aucun sandbox moins protecteur
n'est proposé et aucun processus préexistant n'est terminé.

Le précontrôle réel du serveur candidat `droit-francais` observe
`authStatus=notLoggedIn`, zéro outil et « Auth required ». La connexion Codex
réussie ne valide pas cette connexion MCP. Le flux OAuth officiel a reçu une
URL d'autorisation puis expiré sans callback utilisateur ; aucun retry,
secret lu ou copié, ni modèle lancé. Les URL d'autorisation, RPC privées,
contextes natifs complets et journaux bruts ne sont pas publiés.

## Outillage contrôlé

30 tests passent : 24 fixtures du harnais/normaliseur, 6 contrats OAuth.
Ruff, AST Python et parseur PowerShell ont été contrôlés. Les seize questions,
124 atomes, oracles, barème et cinq modules historiques sont préservés.
Un extrait, un résumé, une erreur, une troncature ou une sortie imprimée par
`functions.exec` ne deviennent pas un primaire natif complet. STOP porte
sur le premier texte visible, commentaires inclus. Le validateur de jugement
contrôle bool/null, atomes exacts et références réelles, sans simuler de revue.

Le nouveau harnais vérifie les deux binaires CUA (`node.exe` et
`node_repl.exe`), bloque les chemins inconnus, contrôle la configuration
effective et les schémas MCP avant préparation puis avant chaque tentative.
Le MCP n'est activé que pour les treize cas requis ; le web seulement pour
les trois cas `official_source`. Les capacités ordinateur/navigateur/apps et
`code_mode_host` sont désactivées ponctuellement. La campagne s'arrête au
premier échec technique, sans retry, reprise ou remplacement de preuve.
Les exports sont destinés à seize juges nouveaux créés ensuite ; aucun juge
n'est créé par le lanceur. Les tests synthétiques ne valident pas le runtime.

## Exécution dans la session locale

Les copies `outillage/` sont documentaires : elles dépendent du checkout,
profil isolé authentifié et preuves historiques de la session Windows.
Elles n'installent ni ne configurent automatiquement ces dépendances.
Le dossier de campagne complète n'a pas encore été préparé.

Terminer d'abord une connexion interactive officielle, déclenchée
explicitement depuis un terminal Windows, avec le compagnon local :

```powershell
& 'C:\Users\Krn\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -B 'C:\Users\Krn\Documents\Codex\2026-10-06\reprends-le-travail-de-cette-session\connexion_juridique_dev7_20261009.py' --ouvrir
```

Après un reçu `success=true`, fermer complètement l'application Codex,
puis lancer les contrôles, la préparation et les seize répondants depuis
le terminal Windows resté ouvert :

```powershell
& 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' -NoLogo -NoProfile -File 'C:\Users\Krn\Documents\Codex\2026-10-06\reprends-le-travail-de-cette-session\lancer-campagne-native-dev7-complet-20261009.ps1'
```

Revenir ensuite à la session pour juger les paquets scellés par des sous-agents
sans historique parent. Une lecture à froid réussie, les seize réponses,
les seize jugements, le STOP critique et le smoke complet ne sont pas acquis.
Les avis DSI/RSSI et juridique ainsi que l'ouverture PowerPoint native restent
à recueillir. Les deux PR restent brouillon ; `release_ready=false`.
