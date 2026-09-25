"""
query_understanding.py — Query Understanding module (LLM Call 1).

Extracts structured attributes from raw text and builds a clean
retrieval query. Uses the LLMClient interface.
"""

import json
import os
from typing import Dict, List, Optional
from pydantic import BaseModel, ValidationError

from ai_core.interfaces.llm_client import LLMClient
from ai_core.errors import LLMInvalidOutputError

class QueryAttributesSchema(BaseModel):
    product_type: Optional[str]
    material_grade: Optional[str]
    product_form: Optional[str]
    application: Optional[str]
    explicit_standard_numbers: List[str]
    detected_language: str


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
        prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "query_understanding_v1.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self._prompt_template = f.read()

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
        prompt = self._prompt_template.replace("{raw_query}", raw_query)
        extracted = self._llm.extract(prompt)

        # Validate with model-agnostic schema
        try:
            validated = QueryAttributesSchema(**extracted)
            extracted = validated.model_dump()
        except ValidationError as e:
            raise LLMInvalidOutputError(f"LLM output failed schema validation: {e}")

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
