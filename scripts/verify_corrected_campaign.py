"""Recalcule l'archive corrigée hors ligne, sans Git ni transfert de scores."""
from corrected_candidate import PROFILE, frozen_failures_corrected
from verify_coactivation_v2 import main

if __name__ == '__main__':
    raise SystemExit(main(frozen_validator=frozen_failures_corrected, candidate_profile=PROFILE))
