# Coactivation r5 — interruption réseau

Le candidat dev.3 f002356ab68282fab21fe713cf71098a6a1d0bf0 a été lancé dans
le contexte réseau sandbox. Trois tentatives achevées (prime de départ,
garde-fou APJA, violation de données) ont rencontré ECONNREFUSED ; aucun
score comportemental n'en est déduit. Les autres processus de cette tentative
ont été interrompus, leurs traces partielles conservées. La liste assainie
des processus vérifiés figure dans interruption-reseau-campagne-r5.json.

La reprise r6 utilise le contexte réseau autorisé. Elle reste une mesure
distincte, sans remplacer les traces r5. `release_ready=false`.
