# Dataset Selection

Status: decided ahead of Phase 1. No ingestion code exists yet — this records which datasets the project targets and why, verified directly against the source platforms rather than assumed from search results. For a column-by-column breakdown of what's actually inside each dataset, see [DATASET_ANATOMY.html](DATASET_ANATOMY.html).

## Methodology

- OpenNeuro's search UI is a JS-rendered single-page app and returns nothing to a plain fetch, so candidates were verified directly against OpenNeuro's own public, anonymously-listable S3 bucket (`s3://openneuro.org/`, confirmed public via the [AWS Open Data registry](https://registry.opendata.aws/openneuro/)) — exact file counts, byte sizes, and the real `dataset_description.json` / `participants.tsv` / `*_eeg.json` sidecar contents were pulled per candidate, not estimated.
- PhysioNet's dataset pages are server-rendered and were fetched directly for size, format, channel, and license facts.
- One early candidate surfaced by a search engine (`ds001512`) returned an empty S3 listing when checked directly and was dropped rather than included on an unverified assumption.

## Candidates compared

| Dataset | Source | Subjects | Format | Channels | Rate | Raw size | License |
|---|---|---|---|---|---|---|---|
| **`ds002778`** | OpenNeuro | 31 (16 healthy, 15 Parkinson's) | BDF | 40 | 512 Hz | **0.53 GB** | CC0 |
| `ds004504` | OpenNeuro | 88 (36 AD, 23 FTD, 29 healthy) | EEGLAB `.set` | 19 | 500 Hz | 2.64 GB | CC0 |
| **`eegmat`** | PhysioNet | 36 (24/12 performance groups) | EDF | 23 | 500 Hz | **0.175 GB** | ODC-BY 1.0 |
| `eegmmidb` | PhysioNet | 109 | EDF+ | 64 | 160 Hz | 3.4 GB (1.9 GB zipped) | ODC-BY 1.0 |
| `auditory-eeg` | PhysioNet | 20 | CSV/WFDB (non-standard) | 4 | 200 Hz | 2.9 GB | More restrictive-sounding license |
| `siena-scalp-eeg` | PhysioNet | 14 (clinical epilepsy) | EDF | ~29, variable | 512 Hz | 20.3 GB | CC-BY 4.0 |
| `chbmit` | PhysioNet | 22 (pediatric epilepsy) | EDF | ~23–26 | 256 Hz | 42.6 GB | ODC-BY 1.0 |

## Recommendation: `ds002778` + `eegmat`

Combined raw footprint: **≈720 MB**.

- **`ds002778` over `ds004504`:** despite fewer subjects, `ds002778` has real `events.tsv` files and multi-session structure (some subjects recorded on and off medication) — it exercises the Event and Session entities in the [data model](PROJECT_PLAN.md#5-data-model) that `ds004504`'s single resting-state task never touches, and it's a fifth the size.
- **`eegmat` over `eegmmidb`:** PhysioNet data isn't BIDS-structured, which is precisely the point of including a second source — pairing it with a BIDS OpenNeuro dataset makes "heterogeneous schemas need standardization" a real problem the pipeline has to solve, not a formality. `eegmat`'s small size keeps Phase 1–4 iteration fast; `eegmmidb` remains a reasonable upgrade later if more scale is wanted.
- **Rejected — `siena-scalp-eeg` / `chbmit`:** 20–42 GB is disproportionate to course scope; `chbmit`'s pediatric clinical population also adds ethical review overhead the project doesn't need.
- **Rejected — `auditory-eeg`:** non-standard CSV/WFDB format complicates the single allowed EEG-parsing-library decision, and its license reads more restrictively than the CC0/ODC-BY terms on every other candidate.

## Verified specifics

### `ds002778` — UC San Diego Resting-State EEG (OpenNeuro)

- **License / DOI:** CC0, `doi:10.18112/openneuro.ds002778.v1.0.4` (from the dataset's real `dataset_description.json`)
- **Subjects:** 31 total — `sub-hc*` (healthy control) and `sub-pd*` (Parkinson's disease), confirmed by counting `participants.tsv` rows
- **Participant metadata columns:** `participant_id, age, gender, hand, MMSE, NAART, disease_duration, rl_deficits, notes`
- **Recording:** single `rest` task, BDF format, `EEGChannelCount: 40`, `SamplingFrequency: 512.0`, ~192s duration (from a real `*_eeg.json` sidecar)
- **Layout:** `sub-XX/ses-hc|pd/eeg/` containing `_channels.tsv`, `_eeg.bdf`, `_eeg.json`, `_events.tsv` per recording
- **Verified size:** 264 raw files, 0.53 GB

### `eegmat` — EEG During Mental Arithmetic Tasks (PhysioNet)

- **License:** Open Data Commons Attribution License v1.0
- **Subjects:** 36 — grouped `G` (24, good task performance) and `B` (12, poor performance)
- **Recording:** Neurocom 23-channel monopolar system, 10/20 placement, 500 Hz (confirmed against the original data descriptor paper, not just the PhysioNet page)
- **Files:** 72 EDF files total — one baseline and one arithmetic-task recording per subject
- **Verified size:** 175 MB

## Still open for Phase 1

- Exact programmatic access method for each source. OpenNeuro's anonymous S3 listing (used to verify this document) is a strong signal that bulk sync is straightforward, but no ingestion code has been written or tested against it yet. PhysioNet's HTTPS bulk download vs. its own API is still to be decided.
- Formal confirmation that both datasets meet the "properly de-identified, licensed for non-clinical educational use" bar beyond their publishers' license declarations.
