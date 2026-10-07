# GINI-code

Staging copy of the code proposed for the paper's public GitHub repository.

## Contents

- `scripts/All_podtec.py`, `scripts/pod2xr.py`: COSMIC-2 POD/STEC extraction and gridding.
- `scripts/test_bylyx/`: three historical 5-channel training/evaluation candidates.
- `scripts/IONPPP/`: PPP STEC processing and CODE/model validation programs.
- `scripts/plots/`: selected validation and paper-plot scripts.
- `plots/`: additional plotting scripts copied for the GitHub release.
- `scripts/test_bylyx/train_save/`: the 5-channel `LAST_TEST` candidate weights at the path expected by the candidate scripts.
- `data/examples/`: small single-day CODE/model sample grids.

## Not yet a finalized release

The three training candidates differ. They are kept separately rather than
guessing which one generated the paper's final results. Select and document
the canonical training entry point and matching checkpoint before publication.
The source scripts also contain machine-specific paths and assumptions that
must be changed to configuration or relative paths before claiming that the
repository runs out of the box.

Several scripts under `plots/` also contain absolute paths to local data and
output directories. They are included as source only; provide the corresponding
Zenodo data and update paths before running them.

The source project's README describes an older 4-channel, 2022 experiment,
whereas the included gridding/training candidates use 5 channels. Replace or
update it with the final paper method, exact data versions, metrics, random
seeds, environment, and reproducible commands before publication.

The small sample grids and model weights are copied for staging only. Confirm
their correspondence to the paper and verify upstream data-product
redistribution terms before making this directory public. No code or data
license is asserted by this staging copy.
