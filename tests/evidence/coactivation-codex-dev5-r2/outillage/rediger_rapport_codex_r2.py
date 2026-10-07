"""Rapport des seules observations de r2 ; conserve les jugements indépendants."""
from pathlib import Path
import json
import jugements_codex_dev5_r2 as judges
import campagne_codex_dev5_r2 as campaign

def main():
    summary = judges.report()
    assert summary['judged_count'] == 16
    counts, atoms = summary['counts'], summary['atomic_results']
    lines = [
        '# Coactivation dev.5 — campagne native Codex r2', '',
        'Mesure du 7 octobre 2026 sur des sous-agents Codex frais, sans lancement de Claude Code.', '',
        f"{summary['completed_respondents']} réponses, {summary['judged_count']} juges et {summary['retained_unique_role_count']} rôles distincts. "
        f"Verdicts : {counts['reussite']} réussites, {counts['echec']} échecs, {counts['bloque']} bloqués. "
        f"Les 124 invariants donnent {atoms['true']} vrais, {atoms['false']} faux et {atoms['null']} non démontrés.", '',
        f"Candidat lu : `{summary['candidate_commit']}`. Source runtime : `{summary['runtime_source_commit']}`. "
        '166 fichiers runtime et 211 empreintes gelées. Barème original conservé : 11 cas forcés, 5 sélections spontanées.', '',
        '## Résultats', '',
        '| Cas | Verdict | Technique | Comportement | Documentation | Primaire reçu |',
        '|---|---|---|---|---|---|',
    ]
    for result in summary['results']:
        lines.append('| ' + ' | '.join(str(result[key]) for key in
            ('case_id', 'verdict', 'technical_status', 'behavior_status', 'documentary_status', 'primary_content_available')) + ' |')
    lines += ['', '## Chargements réellement observés', '',
              'Ce tableau décrit les lectures de fichiers et le premier texte. Il ne remplace aucun invariant du juge.', '',
              '| Cas | Fichiers complets lus | Rôles chargés dans l’ordre | STOP premier |',
              '|---|---|---|---|']
    for result in summary['results']:
        identifier = result['case_id']
        proof = json.loads((campaign.RUN / identifier / 'liaison/execution-repondant.json').read_text(encoding='utf-8'))
        technical = json.loads((campaign.RUN / (identifier + '.jsonl')).read_text(encoding='utf-8').splitlines()[-1])
        stop = technical['observables']['stop_first']
        lines.append('| ' + identifier + ' | ' + str(len(proof['runtime_fragment_groups'])) + ' | '
                     + ' → '.join(proof['loaded_skills']) + ' | '
                     + ('sans exigence STOP' if stop is None else ('oui' if stop else 'non')) + ' |')
    lines += ['', '## Écarts et preuves manquantes', '']
    for result in summary['results']:
        identifier = result['case_id']
        document = json.loads((campaign.RUN / (identifier + '.jugement.json')).read_text(encoding='utf-8'))
        missing = [(key, item) for key, item in document['invariants'].items() if item['status'] is not True]
        if missing:
            lines += ['### ' + identifier, '']
            for key, item in missing:
                lines.append(f"- `{key}` — {'faux' if item['status'] is False else 'non démontré'} : {item['rationale']}")
            lines.append('')
    lines += [
        '## Portée et limites', '',
        'Les six fragments de chaque entrée, les descripteurs et tous les fragments runtime sélectionnés, puis tous les fragments du paquet juge, '
        'sont contrôlés contre les sorties natives réellement reçues et les octets du candidat. Chaque réponse et jugement retenu provient d’un patch littéral réussi. '
        'Chaque rôle dispose d’un premier tour propre et achevé, sans historique partagé ; l’identité et le modèle proviennent des métadonnées natives. '
        'Le message initial opaque n’est pas attesté en clair : la lecture effective de l’entrée complète l’est. '
        'La fraîcheur des sessions ne certifie pas l’isolation du contexte système partagé par l’hôte.', '',
        'Le cas 14 conserve également une tentative de patch hors du dossier de campagne, refusée par Windows avant création du fichier. '
        'Elle est liée au journal natif et impose un échec technique ; elle n’est ni effacée ni promue en conformité. '
        'Un juge du cas 13 a été interrompu après une erreur de chemin dans les instructions de lecture ; son tour n’est pas retenu. '
        'Un nouvel export antérieur à une nouvelle création fournit les mêmes pièces au juge frais retenu, sans communiquer de score.', '',
        'Le chargement attesté est `file_read_fragments`. Il ne prouve ni installation, ni appel Skill, ni smoke du plugin. '
        'Les exigences littérales d’activation peuvent donc rester non démontrées dans cette portée. Les jugements indépendants sont conservés sans relance destinée à améliorer le score.', '',
        'Les instructions de campagne rappellent STOP en premier et, pour les cas forcés, l’ordre des rôles. '
        'Ces résultats caractérisent cette exécution dirigée ; ils ne démontrent pas à eux seuls un effet causal du correctif ou une activation spontanée du plugin installé.', '',
        'Les appels juridiques et web sont réels. Recherche, résumé, page de conseils, extrait normatif reçu et métadonnées de vigueur restent distincts. '
        'Un extrait disponible ne prouve pas la réception de la page entière. Les retours web peuvent être tronqués ; aucun contexte web intégral n’est revendiqué. '
        'Les filtres de domaine explicites et les filtres site littéraux bornés conservent les arguments natifs originaux. Aucun domaine n’est inventé dans les traces.', '',
        'La première tentative r1 conserve ses pièces mais reste exploratoire : des lectures visibles étaient tronquées. '
        'Ses jugements, dont les résultats non retenus, ne sont pas transférés à r2. Aucun score dev.2/dev.3/dev.4 ou DSI autonome n’est transféré à dev.5.', '',
        'Les 28/28 DSI autonomes restent attachés à la source `704e5dd6a3d15994ed431b23585aabd72086ca75` et à leur propre campagne.', '',
        '**Release non qualifiée : `release_ready=false`.** Relecture DSI/RSSI et juridique humaine, smoke du candidat dans Codex et résolution des écarts restent ouverts. '
        'Les PR #11 et #5 demeurent des brouillons. Aucun merge ni déploiement n’est réalisé.', '',
        'Les journaux parent privés restent locaux. Les traces de test publiées sont filtrées ; les extraits sources assainis et les empreintes sont conservés. '
        'Le contrôle natif local et le contrôle portable des pièces archivées ont des portées distinctes.', '',
    ]
    path = campaign.RUN / 'rapport.md'
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write('\n'.join(lines))
    print(path)

if __name__ == '__main__':
    main()
