"""
Build downloadable analysis reports (plain text + PDF via ReportLab Platypus).
"""

from __future__ import annotations

import re
from io import BytesIO
from xml.sax.saxutils import escape

from feedback import improvements_message, strengths_message
from skills import compute_skill_match_ratio

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def _plain(text: str) -> str:
    """Strip simple markdown markers for plain-text / PDF export."""
    return text.replace("**", "").replace("*", "")


def _break_long_tokens(text: str, *, chunk: int = 40) -> str:
    """
    Prevent layout overflow from very long unbroken strings (URLs, hashes, etc.)
    by inserting spaces periodically.
    """
    def _split(match: re.Match[str]) -> str:
        s = match.group(0)
        return " ".join(s[i : i + chunk] for i in range(0, len(s), chunk))

    return re.sub(r"\S{80,}", _split, text)


def _para_safe(text: str) -> str:
    """
    Make text safe for ReportLab Paragraph:
    - escape XML special chars
    - keep newlines as <br/>
    - soften long tokens to avoid 'Not enough horizontal space...' errors
    """
    t = _break_long_tokens(_plain(text))
    return escape(t).replace("\n", "<br/>")


def build_text_report(
    pct: float,
    job_text: str,
    matched_skills: list[str],
    missing_skills: list[str],
) -> str:
    """Single string suitable for a .txt download."""
    ratio, jd_n = compute_skill_match_ratio(matched_skills, job_text)
    sep = "-" * 46
    lines: list[str] = [
        "SmartResume AI — Analysis Report",
        sep,
        "",
        f"Semantic match score: {pct}%",
        "",
        "Skill match ratio (catalog skills in job vs. covered on resume)",
    ]
    if ratio is None:
        lines.append("  n/a — no catalog skills detected in the job text")
    else:
        lines.append(
            f"  {round(ratio * 100.0, 1)}%  ({len(matched_skills)} of {jd_n} JD skills)"
        )

    lines.extend(
        [
            "",
            "Matched skills",
            ", ".join(matched_skills) if matched_skills else "(none)",
            "",
            "Missing skills (vs. job)",
            ", ".join(missing_skills) if missing_skills else "(none)",
            "",
            "Strengths",
            _plain(strengths_message(matched_skills)),
            "",
            "Improvements / suggestions",
            _plain(improvements_message(missing_skills)),
            "",
            sep,
            "End of report",
        ]
    )
    return "\n".join(lines)


def build_pdf_bytes(
    pct: float,
    job_text: str,
    matched_skills: list[str],
    missing_skills: list[str],
) -> bytes:
    """
    ReportLab Platypus PDF with automatic wrapping and spacing.
    Uses SimpleDocTemplate + Paragraph + Spacer (+ bullet lists).
    """
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="SmartResume AI Report",
        author="SmartResume AI",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "SRTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=12,
    )
    h_style = ParagraphStyle(
        "SRHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "SRBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        spaceAfter=6,
        wordWrap="CJK",  # allows wrapping even for long tokens
    )

    story: list[object] = []

    # Title
    story.append(Paragraph("SmartResume AI Report", title_style))

    # Match score
    story.append(Paragraph("Match Score", h_style))
    story.append(Paragraph(f"<b>{escape(str(pct))}%</b>", body_style))

    # Skills
    story.append(Spacer(1, 6))
    story.append(Paragraph("Matched Skills", h_style))
    if matched_skills:
        story.append(
            ListFlowable(
                [ListItem(Paragraph(escape(s), body_style)) for s in matched_skills],
                bulletType="bullet",
                leftIndent=16,
            )
        )
    else:
        story.append(Paragraph("(none detected from the catalog)", body_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Missing Skills", h_style))
    if missing_skills:
        story.append(
            ListFlowable(
                [ListItem(Paragraph(escape(s), body_style)) for s in missing_skills],
                bulletType="bullet",
                leftIndent=16,
            )
        )
    else:
        story.append(Paragraph("(none)", body_style))

    # Strengths & Improvements
    story.append(Spacer(1, 8))
    story.append(Paragraph("Strengths", h_style))
    story.append(Paragraph(_para_safe(strengths_message(matched_skills)), body_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Improvements", h_style))
    story.append(Paragraph(_para_safe(improvements_message(missing_skills)), body_style))

    doc.build(story)
    return buf.getvalue()
