"""Crée un nouveau gel explicite du candidat corrigé déjà committé."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from corrected_candidate import build_manifest


def main() -> int:
    """Conserve les gels existants et refuse tout état non committé."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Gel existant conservé')
    try:
        frozen = build_manifest()
    except (ValueError, OSError) as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(frozen, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({key: frozen[key] for key in ('profile', 'candidate_commit', 'candidate_tree',
                                                  'runtime_files', 'historical_scores_reused')}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
