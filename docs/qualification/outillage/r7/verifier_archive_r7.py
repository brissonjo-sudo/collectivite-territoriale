"""Rejoue uniquement une archive r7 avec l’adaptateur brut courant attesté."""
from __future__ import annotations

from typing import Any

import lie_jugements_corriges_bruts as raw
import verifier_archive_corrigee as historical


def check_current_raw_export(exported: dict[str, Any]) -> None:
    """Un export r7 doit identifier exactement le code qui produit la lecture brute."""
    if (exported.get('raw_projection') != raw.PROJECTION
            or exported.get('raw_adapter_sha256') != historical.digest(historical.ROOT / 'lie_jugements_corriges_bruts.py')
            or exported.get('compact_packet') is not True
            or type(exported.get('external_read_output_tokens')) is not int
            or exported['external_read_output_tokens'] != 55000):
        raise ValueError('Adaptateur courant d’export r7 absent ou divergent')


def main() -> None:
    """Le contrôle historique demeure inchangé sur disque et pour toutes les autres mesures."""
    manifest = historical.load(historical.ROOT / 'archive-manifest.json')
    if manifest.get('coactivation_run') != 'campagne-r7' or manifest.get('frozen_manifest') != 'gel-r7.json':
        raise ValueError('Ce vérificateur est réservé au gel et à la campagne r7')
    old_check = historical.check_raw_export_adapter
    try:
        historical.check_raw_export_adapter = check_current_raw_export
        historical.main()
    finally:
        historical.check_raw_export_adapter = old_check


if __name__ == '__main__':
    main()
