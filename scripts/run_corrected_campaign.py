"""Mesure fraîche du candidat corrigé ; aucun score historique n'est importé."""
from corrected_candidate import PROFILE, measured_failures
from run_coactivation_v2 import main

if __name__ == '__main__':
    raise SystemExit(main(frozen_validator=measured_failures, candidate_profile=PROFILE))
