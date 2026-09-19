"""
pdf_input.py — Extracts raw text from procurement documents (PDFs).
"""

import os


class PDFInput:
    """Utility to extract text from PDF files."""

    def extract_text(self, pdf_path: str) -> str:
        """Reads a PDF and returns all text.

        Parameters
        ----------
        pdf_path : str
            Path to the PDF file.

        Returns
        -------
        str
            Extracted text content.
        """
        try:
            import pypdf
        except ImportError as exc:
            raise ImportError(
                "pypdf is required for PDF parsing. "
                "Install with: pip install pypdf"
            ) from exc

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        text_parts = []
        with open(pdf_path, "rb") as fh:
            reader = pypdf.PdfReader(fh)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
                
        return "\n".join(text_parts).strip()
