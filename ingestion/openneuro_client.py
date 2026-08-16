"""Placeholder for the OpenNeuro ingestion client.

Real ingestion logic (confirming the exact access method, pulling study
files/metadata, and writing them to the MinIO raw layer) is built in a
later phase, once that access method has been verified. This module
exists now so `/ingestion` is a real, importable package rather than an
empty directory.
"""

from __future__ import annotations

import requests  # noqa: F401  -- exercised once real ingestion logic lands

OPENNEURO_BASE_URL = "https://openneuro.org"


def fetch_study_metadata(study_id: str) -> dict:
    """Fetch metadata for a single OpenNeuro study.

    Not implemented yet -- see docs/PROJECT_PLAN.md, Phase 1.
    """
    raise NotImplementedError("OpenNeuro ingestion is implemented in a later phase.")
