"""
Strengths and improvement text derived from skill overlap (keyword catalog).
"""


def strengths_message(matched_skills: list[str]) -> str:
    """Strengths follow the matched-skill list."""
    if not matched_skills:
        return (
            "No overlapping catalog skills yet — add honest keywords from the job "
            "where they match your experience."
        )
    listed = ", ".join(matched_skills)
    return f"Strengths (overlap with the job): **{listed}**."


def improvements_message(missing_skills: list[str]) -> str:
    """Improvements combine missing skills plus short, actionable suggestions."""
    if not missing_skills:
        return (
            "No catalog gaps vs. the job text. Refine bullets to echo the posting "
            "and quantify outcomes.\n\n"
            "**Suggestions:**\n"
            "- Highlight measurable results from recent projects.\n"
            "- Mirror important job-description wording where it is accurate.\n"
            "- Move the strongest matching skills closer to the top of the resume."
        )

    lines = ["**Suggestions:**"]
    for skill in missing_skills:
        lines.append(f"- Add projects using **{skill}**.")
        lines.append(f"- Include certifications related to **{skill}**.")
        lines.append(f"- Highlight experience with **{skill}** in your resume.")

    return "\n".join(lines)
