"""
Keyword-based skill detection using a fixed catalog (case-insensitive, token-aware).
"""

from __future__ import annotations

import re

# Curated list; longer phrases are matched first (see ``SKILL_MATCH_ORDER``).
SKILL_CATALOG: tuple[str, ...] = (
    "machine learning",
    "deep learning",
    "computer vision",
    "natural language processing",
    "data science",
    "ci/cd",
    "scikit-learn",
    "power bi",
    "node.js",
    "react.js",
    "vue.js",
    "angular.js",
    "rest api",
    "object oriented",
    "tensorflow",
    "pytorch",
    "kubernetes",
    "javascript",
    "typescript",
    "postgresql",
    "mongodb",
    "fastapi",
    "django",
    "flask",
    "spring boot",
    "react",
    "angular",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "keras",
    "spark",
    "kafka",
    "hadoop",
    "airflow",
    "docker",
    "jenkins",
    "ansible",
    "terraform",
    "graphql",
    "microservices",
    "statistics",
    "python",
    "java",
    "scala",
    "go",
    "rust",
    "c++",
    "c#",
    "sql",
    "mysql",
    "redis",
    "aws",
    "azure",
    "gcp",
    "linux",
    "bash",
    "git",
    "github",
    "gitlab",
    "nlp",
    "ml",
    "dl",
    "agile",
    "scrum",
    "excel",
    "tableau",
    "dbt",
    "vue",
)

# Longest-first so phrases like "machine learning" beat "learning" if both existed.
SKILL_MATCH_ORDER: tuple[str, ...] = tuple(sorted(SKILL_CATALOG, key=len, reverse=True))

# Display order for results (original catalog order, unique).
_DISPLAY_ORDER: dict[str, int] = {}
for _i, _name in enumerate(SKILL_CATALOG):
    if _name not in _DISPLAY_ORDER:
        _DISPLAY_ORDER[_name] = _i


def find_skills_in_text(text: str) -> list[str]:
    """Return catalog skills that appear in ``text``."""
    if not text or not text.strip():
        return []

    lowered = text.lower()
    found: set[str] = set()

    for skill in SKILL_MATCH_ORDER:
        # Token-ish boundaries: avoid matching inside unrelated words.
        pattern = r"(?<![a-z0-9+/\-#])" + re.escape(skill.lower()) + r"(?![a-z0-9+/\-#])"
        if re.search(pattern, lowered):
            found.add(skill)

    return sorted(found, key=lambda s: _DISPLAY_ORDER.get(s, 999))


def compare_resume_to_job(resume_text: str, job_text: str) -> tuple[list[str], list[str]]:
    """
    Matched = skills present in both resume and job text.
    Missing = skills found in the job description but not on the resume.
    """
    resume_skills = set(find_skills_in_text(resume_text))
    job_skills = set(find_skills_in_text(job_text))

    matched = sorted(resume_skills & job_skills, key=lambda s: _DISPLAY_ORDER.get(s, 999))
    missing = sorted(job_skills - resume_skills, key=lambda s: _DISPLAY_ORDER.get(s, 999))
    return matched, missing


def compute_skill_match_ratio(
    matched_skills: list[str],
    job_text: str,
) -> tuple[float | None, int]:
    """
    Evaluation metric: len(matched_skills) / len(catalog skills found in the job text).

    Returns ``(ratio, jd_skill_count)``. ``ratio`` is ``None`` if the job has no catalog skills.
    """
    jd_skills = find_skills_in_text(job_text)
    jd_count = len(jd_skills)
    if jd_count == 0:
        return None, 0
    return len(matched_skills) / jd_count, jd_count
