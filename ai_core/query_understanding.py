"""
query_understanding.py — Query Understanding module (LLM Call 1).

Extracts structured attributes from raw text and builds a clean
retrieval query. Uses the LLMClient interface.
"""

import json
from typing import Dict

from ai_core.interfaces.llm_client import LLMClient


class QueryUnderstanding:
    """Extracts structured entities and builds semantic search queries."""

    def __init__(self, llm_client: LLMClient) -> None:
        """
        Parameters
        ----------
        llm_client : LLMClient
            Interface instance for making extraction calls.
        """
        self._llm = llm_client

    def extract_query_attributes(self, raw_query: str) -> Dict:
        """
        Extracts structured attributes from a raw user query.

        Parameters
        ----------
        raw_query : str
            The raw text input from the user or extracted from a PDF.

        Returns
        -------
        dict
            Contains product_type, material_grade, product_form, application,
            explicit_standard_numbers, detected_language, and retrieval_query.
        """
        prompt = f"""
You are an expert in industrial procurement and standards.
Extract structured attributes from the following user query.

Query: "{raw_query}"

Return a JSON object with EXACTLY these keys. Use null if a value is not present:
- "product_type": (string or null)
- "material_grade": (string or null)
- "product_form": (string or null)
- "application": (string or null)
- "explicit_standard_numbers": (list of strings, e.g. ["IS 17876"] or [])
- "detected_language": (string, e.g. "English", "Hindi")

Do not include any other text or markdown formatting besides the JSON block.
"""
        extracted = self._llm.extract(prompt)

        # Build clean retrieval query from structured fields
        parts = []
        for key in ["product_type", "material_grade", "product_form", "application"]:
            val = extracted.get(key)
            if val and str(val).lower() not in ("null", "none", "n/a", ""):
                parts.append(str(val))

        retrieval_query = " ".join(parts).strip()
        # Fallback to the raw query if extraction yielded nothing searchable
        if not retrieval_query:
            retrieval_query = raw_query.strip()

        extracted["retrieval_query"] = retrieval_query
        return extracted
