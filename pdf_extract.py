"""
Extract plain text from PDF bytes using PyMuPDF (import name: fitz).
"""

import fitz


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Return all page text from a PDF represented as bytes."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    try:
        parts: list[str] = []
        for page in doc:
            parts.append(page.get_text())
        return "\n".join(parts)
    finally:
        doc.close()
