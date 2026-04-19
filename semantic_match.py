"""
Semantic match score: sentence embeddings + cosine similarity → percentage.
Uses model: sentence-transformers/all-MiniLM-L6-v2
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def compute_match_percent(
    resume_text: str,
    job_text: str,
    model: SentenceTransformer,
) -> float:
    """
    Embed resume and job description, then cosine similarity (0–1) → 0–100%.
    With normalize_embeddings=True, dot product equals cosine similarity.
    """
    a = resume_text.strip()
    b = job_text.strip()
    if not a or not b:
        return 0.0

    vectors = model.encode(
        [a, b],
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    sim = float(np.dot(vectors[0], vectors[1]))
    sim = max(0.0, min(1.0, sim))
    return round(sim * 100.0, 1)
