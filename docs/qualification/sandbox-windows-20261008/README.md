# Sandbox Windows autorisé : initialisation annulée par UAC

L'utilisateur a explicitement autorisé le setup Windows elevated du profil
isolé après examen de la proposition. L'API officielle de Codex
`windowsSandbox/setupStart` a démarré une tentative. La notification finale
est `success=false` :

```text
orchestrator_helper_launch_canceled: ShellExecuteExW failed to launch setup helper: 1223
```

Windows signale l'annulation de l'invite administrateur UAC. Le profil reste
`notConfigured`. Les octets de configuration et les 214 fichiers du cache dev.6
sont inchangés. La lecture synthétique et la campagne dev.7 ne sont pas lancées.
Les comptes techniques, règles pare-feu et ACL sélectionnées avant/après sont
identiques ; ce contrôle borné n'est pas un audit de tous les effets système.

Le lanceur de reprise est préparé et sa syntaxe vérifiée sous PowerShell 7 et
Windows PowerShell 5.1. Il utilise le CLI installé, le même profil authentifié,
une tentative nouvelle et un reçu distinct. Il ne copie aucun identifiant.
Il vérifie la lecture synthétique sans modèle uniquement après setup confirmé.
L'utilisateur doit accepter l'invite UAC sur le PC ; le lanceur ne la contourne pas.

Le protocole dev.7 prépare 16 scénarios et 124 atomes inchangés. MCP et web
restant désactivés, 13 cas nominaux sont bloqués au précontrôle. Les trois cas
déjà prévus sans sources sont exécutables seulement après preuve de lecture
opérationnelle. Dev.7 demeure non mesuré, sans reprise des scores antérieurs.
Les pièces v8 et leurs 22 empreintes restent un instantané publié antérieur.

Les scripts ci-joints sont des copies documentaires. Le lanceur prêt à utiliser
reste dans la racine de la session, avec ses deux modules Python voisins.

Documentation officielle : [sandbox Windows](https://learn.chatgpt.com/docs/windows/windows-sandbox)
et [API App Server](https://learn.chatgpt.com/docs/app-server).
