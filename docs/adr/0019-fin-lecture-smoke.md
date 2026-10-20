# ADR 0019 — Fin de fichier déterministe pour les lectures du smoke

Date : 20 octobre 2026. Décision de Jo, T43-L30 : « Corriger + tentative c ».

La tentative `smoke-l29-20261020-b` est consommée : une session
activation-implicite. Avec une longueur inconnue, le modèle a découpé les
319 lignes de l'entrée en 90, 90, 90 et 49 lignes, puis demandé un segment
au-delà de la fin (`-Skip 360 -First 90`). La sortie vide a été refusée
par `read_events`, conformément au contrôle existant. L29 ne précisait pas
le critère de fin. L'archive b reste intacte ; a et b comptent chacune
une session consommée, séparément, sans assemblage avec c.

Une seule règle remplace les branches courte/longue dans `smoke_prompt` :
toute entrée ou référence du cache est lue par segments contigus de N = 85,
avec `Get-Content -LiteralPath 'chemin' -Encoding utf8 | Select-Object -Skip M -First N`.
M commence à zéro puis vaut M + N. Dès qu'un segment renvoie moins de N lignes,
le fichier est terminé : aucune lecture suivante, aucune relecture, aucune
lecture intégrale. STOP, MCP sans web, aucune autre commande, signalement
des limites sans rien affirmer des lignes absentes restent inchangés.
Aucun nom de skill n'est injecté dans le cas implicite.

Choix calculé : les objets Git de la tête `0e4e80e2a18a63f6ecf031ad911d265837d9a2a3`
contiennent 183 Markdown dans les sept skills. Aucun n'est vide. Les seuls
entiers admissibles entre 2 et 90 sont 85, 84 et 62 ; 85 est le plus grand.
Leur nombre de lignes est toujours non multiple de 85 : le dernier segment
est donc toujours court. Les 197 fichiers runtime sont identiques à
`13b4e1e537e5a8097a004ee913abcc9d079114a7`. N reste inférieur aux 90 lignes
du segment vérifié de d documenté par l'ADR 0018 ; aucune limite CLI générale
n'est déduite de cette observation.

`tests/test_smoke_eof.py` énumère tous les Markdown présents, y compris tout
futur fichier, et échoue sur une longueur nulle ou multiple de 85. Il vérifie
sur des fixtures explicitement diagnostiques la série complète, son dernier
segment court, les doublons refusés et le refus inchangé d'une lecture vide
ou tronquée. Les chemins et SHA-256 de chaque Markdown, son nombre de lignes
et le reste modulo 85 sont conservés hors candidat dans
`t43-successeur/l30-preuves/preuve-N.json`, liés aux objets Git source.

Limite connue : cette fin sans sonde vide est une propriété du runtime figé,
pas un détecteur EOF universel. Toute évolution qui rend un fichier vide ou
multiple de N bloque les tests et exige une nouvelle décision de découpage.
Une restitution raccourcie par le transport ne prouve pas à elle seule EOF :
`read_events` exige toujours le contenu attendu du segment et refuse toute
troncature. Le prompt ne garantit pas l'obéissance du modèle ; le smoke réel
reste nécessaire. Aucun validateur, seuil d'acceptation ou fichier runtime
n'est modifié pour absorber une sortie incorrecte.

La liste fermée ADR 0017/0018 reste exactement la même. Son manifeste
`scripts/toolchain-transition-0017.json` actualise uniquement les empreintes
cibles exactes du runner et du CHANGELOG ; les empreintes sources liées au
commit mesuré demeurent inchangées. La campagne d et l'avis humain restent
acceptables, sans nouveau chemin permis ni option de contournement.
Un smoke réel réussi sur la nouvelle tête reste obligatoire avant assemblage.

Tentative c préparée séparément : `smoke-l30-20261020-c`, deux cas, au plus
deux sessions. Aucun appel modèle, installation, connexion MCP, ACL/UAC,
poussée ou release dans ce lot.
