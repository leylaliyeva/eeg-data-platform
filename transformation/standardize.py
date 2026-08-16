"""Placeholder for metadata/signal standardization logic.

Real logic (parsing EEG binary files and mapping per-study metadata into
the common data model in docs/PROJECT_PLAN.md) is built in a later
phase, once real dataset formats have been inspected and the one
allowed additional tool -- an EEG file-parsing library -- is chosen.
"""

from __future__ import annotations


def standardize_recording_metadata(raw_metadata: dict) -> dict:
    """Map a source-specific metadata record to the common data model.

    Not implemented yet -- see docs/PROJECT_PLAN.md, Phase 3.
    """
    raise NotImplementedError("Standardization logic is implemented in a later phase.")
