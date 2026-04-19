"""
SmartResume AI — Streamlit app (layout, inputs, PDF text, analysis results UI).
"""

from __future__ import annotations

import hashlib

import streamlit as st
from sentence_transformers import SentenceTransformer

from pdf_extract import extract_text_from_pdf_bytes
from semantic_match import MODEL_NAME, compute_match_percent
from feedback import improvements_message, strengths_message
from report import build_pdf_bytes, build_text_report
from skills import compare_resume_to_job, compute_skill_match_ratio


# Edge-case thresholds (tunable)
MIN_RESUME_CHARS = 50
MIN_JD_CHARS = 30
MIN_RESUME_WORDS = 20

SESSION_CACHE_KEY = "sr_analysis"
FAILED_FP_KEY = "sr_failed_fp"


@st.cache_resource(show_spinner="Loading language model…")
def load_embedding_model() -> SentenceTransformer:
    """Load once per session; MiniLM is small and fast for local use."""
    return SentenceTransformer(MODEL_NAME)


def fingerprint_inputs(pdf_bytes: bytes, job_text: str) -> str:
    """Stable hash so we can skip work when resume + job text are unchanged."""
    h = hashlib.sha256()
    h.update(pdf_bytes)
    h.update(b"\xff\xff")
    h.update(job_text.encode("utf-8"))
    return h.hexdigest()


def compute_analysis(cleaned: str, job_text: str) -> tuple[float, list[str], list[str]]:
    """Embedding match % + skill lists (heavy step — skipped when cache hits)."""
    try:
        with st.spinner("Computing embedding match…"):
            model = load_embedding_model()
            pct = compute_match_percent(cleaned, job_text, model)
    except Exception as err:
        raise RuntimeError("embedding_failed") from err
    matched_skills, missing_skills = compare_resume_to_job(cleaned, job_text)
    return pct, matched_skills, missing_skills


def configure_page() -> None:
    st.set_page_config(
        page_title="SmartResume AI",
        page_icon="📄",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.markdown(
        """
        <style>
            .main .block-container {
                max-width: 720px;
                padding-top: 1.5rem;
                padding-bottom: 2rem;
            }
            /* Make the input form feel like a clean “card” */
            div[data-testid="stForm"] {
                border: 1px solid #e6e6e6;
                border-radius: 12px;
                padding: 0.9rem 1rem 0.2rem;
                background: #ffffff;
            }
            div[data-testid="stForm"] label {
                font-weight: 600;
            }
            .match-highlight {
                text-align: center;
                padding: 1.1rem 1rem 1.25rem;
                background: linear-gradient(120deg, #e8f5e9 0%, #e3f2fd 100%);
                border-radius: 12px;
                border: 1px solid #c8e6c9;
                margin: 0.25rem 0 0.75rem;
            }
            .match-label {
                font-size: 0.95rem;
                font-weight: 600;
                color: #37474f;
                margin-bottom: 0.35rem;
            }
            .match-pct {
                font-size: 2.65rem;
                font-weight: 800;
                line-height: 1.1;
                color: #1b5e20;
                letter-spacing: -0.02em;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown("# SmartResume AI")
    st.markdown("### AI Resume Analyzer & Job Matcher")
    st.caption(
        "Upload your **PDF resume**, paste the **job description**, then run analysis. "
        "You’ll see a semantic score, skill overlap, strengths, and improvement ideas."
    )


def render_input_card() -> tuple:
    """
    Returns (uploaded_pdf_bytes_or_none, job_description_str, analyze_clicked).
    """
    st.markdown("#### Inputs")
    # `st.form` groups controls so the section feels like one “card” without fragile HTML nesting.
    with st.form("resume_inputs"):
        uploaded = st.file_uploader(
            "Resume (PDF)",
            type=["pdf"],
            help="Choose a single PDF file.",
        )

        job_text = st.text_area(
            "Job description",
            height=180,
            placeholder="Paste the full job posting here (role, requirements, skills)...",
        )

        analyze = st.form_submit_button(
            "Analyze match",
            type="primary",
            use_container_width=True,
        )

    pdf_bytes = uploaded.getvalue() if uploaded is not None else None
    return pdf_bytes, job_text.strip(), analyze


def validate_analyze_inputs(pdf_bytes: bytes | None, job_text: str) -> bool:
    """Require a PDF and non-empty job description before running analysis."""
    if not pdf_bytes:
        st.error("Please upload a PDF resume before analyzing.")
        return False
    if not job_text:
        st.error("Please enter a job description before analyzing.")
        return False
    return True


def render_analysis_results(
    cleaned: str,
    job_text: str,
    *,
    pct: float,
    matched_skills: list[str],
    missing_skills: list[str],
) -> None:
    """Structured results: big match score, two-column skills, strengths, improvements."""
    st.markdown("## Results")
    st.markdown("---")

    if not job_text:
        st.warning(
            "Add a job description to compute the match score, skills, strengths, and improvements."
        )
        return

    resume_word_count = len(cleaned.split())
    if resume_word_count < MIN_RESUME_WORDS:
        st.error(
            f"Insufficient content: only **{resume_word_count}** words found in the resume text. "
            "Upload a more complete, text-based PDF to get reliable results."
        )
        return

    resume_too_short = len(cleaned) < MIN_RESUME_CHARS
    jd_too_short = len(job_text.strip()) < MIN_JD_CHARS
    if resume_too_short or jd_too_short:
        notes: list[str] = []
        if resume_too_short:
            notes.append(
                "Resume text is very short — match score and skills may be unreliable "
                "(try a text-based PDF or check for scanned pages)."
            )
        if jd_too_short:
            notes.append(
                "Job description is very short — paste more of the posting for a fairer comparison."
            )
        st.warning(" ".join(notes))

    st.markdown(
        f'<div class="match-highlight">'
        f'<div class="match-label">Match score</div>'
        f'<div class="match-pct">{pct}%</div></div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Cosine similarity between MiniLM embeddings (resume vs. job text). "
        "Higher usually means closer wording and topics."
    )

    st.markdown("---")
    st.markdown("### Skill overlap")
    ratio, jd_skill_count = compute_skill_match_ratio(matched_skills, job_text)
    if ratio is None:
        st.caption(
            "**Skill match ratio:** *n/a* — no catalog skills detected in the job description."
        )
    else:
        pct_ratio = round(ratio * 100.0, 1)
        st.caption(
            f"**Skill match ratio:** **{pct_ratio}%** "
            f"— you cover **{len(matched_skills)}** of **{jd_skill_count}** catalog skills listed in the job."
        )

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("**Matched with job**")
        if matched_skills:
            st.success(", ".join(matched_skills))
        else:
            st.success("None detected from the catalog.")
    with col_right:
        st.markdown("**Missing vs. job**")
        if missing_skills:
            st.warning(", ".join(missing_skills))
        else:
            st.warning("None — good coverage for catalog skills.")

    st.markdown("---")
    st.markdown("### Strengths")
    st.success(strengths_message(matched_skills))

    st.markdown("---")
    st.markdown("### Improvements")
    st.info(improvements_message(missing_skills))

    st.markdown("---")
    st.markdown("### Download report")
    report_txt = build_text_report(pct, job_text, matched_skills, missing_skills)
    dl_left, dl_right = st.columns(2)
    with dl_left:
        st.download_button(
            "Download (.txt)",
            data=report_txt.encode("utf-8"),
            file_name="smartresume_report.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with dl_right:
        st.download_button(
            "Download (.pdf)",
            data=build_pdf_bytes(pct, job_text, matched_skills, missing_skills),
            file_name="smartresume_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


def main() -> None:
    configure_page()
    render_header()
    st.divider()

    pdf_bytes, job_text, analyze_clicked = render_input_card()

    # Show a retry button only if the last failure matches current inputs.
    retry_clicked = False
    if pdf_bytes and job_text:
        current_fp = fingerprint_inputs(pdf_bytes, job_text)
        if st.session_state.get(FAILED_FP_KEY) == current_fp:
            retry_clicked = st.button(
                "Retry analysis",
                type="secondary",
                use_container_width=True,
            )

    if analyze_clicked or retry_clicked:
        if validate_analyze_inputs(pdf_bytes, job_text):
            fp = fingerprint_inputs(pdf_bytes, job_text)
            cached = st.session_state.get(SESSION_CACHE_KEY)

            if cached and cached.get("key") == fp:
                cleaned = cached["cleaned"]
                pct = cached["pct"]
                matched_skills = cached["matched"]
                missing_skills = cached["missing"]
                st.session_state[FAILED_FP_KEY] = None
                st.success(
                    f"Extracted **{len(cleaned)}** characters from the resume. "
                    "**(Cached analysis — same PDF + job text.)**"
                )
                with st.expander("Preview extracted text", expanded=False):
                    st.text_area(
                        "Resume text (preview)",
                        value=cleaned if cleaned else "(empty)",
                        height=220,
                        disabled=True,
                        label_visibility="collapsed",
                    )
                st.divider()
                render_analysis_results(
                    cleaned,
                    job_text,
                    pct=pct,
                    matched_skills=matched_skills,
                    missing_skills=missing_skills,
                )
            else:
                with st.spinner("Reading your PDF…"):
                    try:
                        resume_text = extract_text_from_pdf_bytes(pdf_bytes)
                    except Exception as err:
                        st.error("Could not read that PDF. Try another file or re-export the PDF.")
                        st.caption(str(err))
                    else:
                        cleaned = resume_text.strip()
                        st.success(
                            f"Extracted **{len(cleaned)}** characters from the resume."
                        )
                        with st.expander("Preview extracted text", expanded=False):
                            st.text_area(
                                "Resume text (preview)",
                                value=cleaned if cleaned else "(empty)",
                                height=220,
                                disabled=True,
                                label_visibility="collapsed",
                            )

                        try:
                            pct, matched_skills, missing_skills = compute_analysis(cleaned, job_text)
                        except Exception:
                            st.error("Analysis failed. Please try again.")
                            st.session_state[FAILED_FP_KEY] = fp
                            return
                        st.session_state[FAILED_FP_KEY] = None
                        st.session_state[SESSION_CACHE_KEY] = {
                            "key": fp,
                            "cleaned": cleaned,
                            "pct": pct,
                            "matched": matched_skills,
                            "missing": missing_skills,
                        }

                        st.divider()
                        render_analysis_results(
                            cleaned,
                            job_text,
                            pct=pct,
                            matched_skills=matched_skills,
                            missing_skills=missing_skills,
                        )


if __name__ == "__main__":
    main()
