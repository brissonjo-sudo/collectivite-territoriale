"""Reconstruction des entrées depuis le gel dev.6 et la suite originale."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT / 'Collectivite-corrections-pr5'
RUN = ROOT / 'qualification-coactivation-dev6-codex-r1'
HEAD = '1a12b347448809864ba6d14d5501585a4a038206'
SOURCE = '3f0df285898cf1e36d1ddda8d85d0c4cd5e0903b'

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args: str) -> bytes:
    result = subprocess.run(['git', '-c', 'safe.directory=' + CANDIDATE.as_posix(), '-C', str(CANDIDATE), *args], capture_output=True, check=True)
    return result.stdout

def description(path: Path) -> str:
    """Lire intégralement les deux formes simples réellement présentes au gel.

    Scalaire folded >- ou plain multi-ligne, continuation de deux espaces.
    Pas de YAML général, tag, ancre, séquence, bloc littéral ou paragraphe vide.
    """
    text = path.read_bytes().decode('utf-8')
    frontmatter = re.match(r'^---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if frontmatter is None:
        raise ValueError('Frontmatter absent')
    lines = frontmatter[1].splitlines()
    starts = [number for number, line in enumerate(lines) if line.startswith('description:')]
    if len(starts) != 1:
        raise ValueError('Description absente ou ambiguë')
    start = starts[0]
    first = lines[start][len('description:'):].strip()
    rest = []
    for line in lines[start + 1:]:
        if line and not line[0].isspace():
            break
        if not re.fullmatch(r'  \S[^\r\n]*', line) or line.startswith('   '):
            raise ValueError('Continuation description hors grammaire simple')
        rest.append(line[2:])
    if first == '>-':
        if not rest:
            raise ValueError('Scalaire folded sans contenu')
        parts = rest
    else:
        if not first or first[0] in '|>!&*[{\"\'':
            raise ValueError('Scalaire description non autorisé')
        parts = [first, *rest]
    result = ' '.join(parts)
    if len(result) < 40 or result in ('>-', '>', '|'):
        raise ValueError('Description incomplète')
    return result

def manifest_and_inputs() -> tuple[dict, dict]:
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD, 'HEAD candidat changé'
    gel_path = CANDIDATE / 'docs/qualification/gel-dev6-non-mesure.json'
    gel = json.loads(gel_path.read_text(encoding='utf-8'))
    assert gel['candidate_commit'] == SOURCE and gel['plugin_version'] == '1.2.0-dev.6'
    assert len(gel['files']) == 213
    for relative, digest in gel['files'].items():
        assert sha(CANDIDATE / relative) == digest, 'Octets gelés modifiés : ' + relative
        for revision in (SOURCE, HEAD):
            assert hashlib.sha256(git('show', revision + ':' + relative)).hexdigest() == digest, 'Blob Git divergent : ' + relative
    suite_path = CANDIDATE / 'tests/cas-coactivation-v2.json'
    protocol_path = CANDIDATE / 'docs/protocole-coactivation-v2.md'
    original = ROOT / 'qualification-coactivation-dev5-codex-r1'
    assert suite_path.read_bytes() == (original / 'suite.json').read_bytes()
    assert protocol_path.read_bytes() == (original / 'protocole-original.md').read_bytes()
    cases = json.loads(suite_path.read_text(encoding='utf-8'))
    assert len(cases) == 16 and sum(len(c['invariant_objects']) for c in cases) == 124
    runtime = {(CANDIDATE / relative).resolve().as_posix(): digest for relative, digest in gel['files'].items() if relative.startswith('skills/')}
    assert len(runtime) == 166
    catalogue = []
    for path in sorted((CANDIDATE / 'skills').glob('*/SKILL.md')):
        catalogue.append({'name': path.parent.name, 'description': description(path), 'runtime_path': path.resolve().as_posix(), 'runtime_sha256': sha(path)})
    inputs = {}
    # Only stable question/mode/scope fields are copied; no old response or oracle.
    fields = ('schema_version', 'case_id', 'case_number', 'host', 'activation_mode', 'question', 'mcp_mode', 'web_mode', 'legal_mode', 'official_source_hosts', 'context_rule', 'source_rule')
    for case in cases:
        prior = json.loads((original / case['id'] / 'input.json').read_text(encoding='utf-8'))
        entry = {field: prior[field] for field in fields}
        assert entry['question'] == case['prompt']
        entry.update(candidate_commit=HEAD, runtime_source_commit=SOURCE, candidate_version='1.2.0-dev.6',
                     allowed_runtime_root=(CANDIDATE / 'skills').resolve().as_posix(), allowed_runtime_files=runtime,
                     execution_mode='runtime_file_load_fragments', response_path=(RUN / case['id'] / 'response.md').resolve().as_posix(),
                     loading_rule='Lecture complète native par fragments ; aucune activation plugin attestée.')
        if entry['activation_mode'] == 'forced':
            entry['runtime_load_sequence'] = prior['runtime_load_sequence']
            assert all(path in runtime for path in entry['runtime_load_sequence'])
        else:
            entry['runtime_catalogue'] = catalogue
        inputs[case['id']] = entry
    import grammaire_codex_dev6 as grammar
    manifest = {'schema_version': 1, 'run': 'codex-dev6-native-r1', 'host': 'Codex', 'plugin_version': '1.2.0-dev.6',
        'candidate_commit': HEAD, 'runtime_source_commit': SOURCE, 'candidate_tree': git('rev-parse', HEAD + '^{tree}').decode().strip(),
        'original_frozen_manifest_sha256': sha(gel_path), 'runtime_files': 166, 'files': gel['files'],
        'suite_sha256': sha(suite_path), 'protocol_sha256': sha(protocol_path), 'case_count': 16, 'atomic_count': 124,
        'grammar_sha256': grammar.fingerprint(), 'configuration_sha256': sha(Path(__file__)),
        'git_blob_bytes_verified': True, 'verified_blob_revisions': [SOURCE, HEAD],
        'historical_scores_reused': False, 'actual_plugin_activation_verified': False, 'codex_plugin_smoke': 'not_established', 'release_ready': False,
        'capacity_grammar': 'optional exact max_output_tokens=55000 for literal source or literal unique patch; source and patch bodies unchanged'}
    return manifest, inputs
