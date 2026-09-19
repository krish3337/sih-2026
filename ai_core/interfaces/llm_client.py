"""
LLMClient interface — abstract contract for language-model operations.

The pipeline makes exactly two LLM calls per query:
  1. extract()  — query understanding (structured attribute extraction)
  2. generate() — final synthesis (evidence-constrained explanation)

Everything else (retrieval, graph traversal, metadata lookup) is deterministic
code with no LLM involvement.

Pipeline modules depend on this interface, never on a concrete implementation.
"""

from abc import ABC, abstractmethod
from typing import Dict


class LLMClient(ABC):
    """Wrapper around a language model for structured extraction and
    free-text generation."""

    @abstractmethod
    def extract(self, prompt: str) -> Dict:
        """Send a prompt and parse the response as structured JSON.

        Used by query_understanding.py to extract product_type, grade,
        form, application, etc. from a raw user query.

        Parameters
        ----------
        prompt : str
            Full prompt including instructions and the raw query text.

        Returns
        -------
        dict
            Parsed structured data from the LLM response.

        Raises
        ------
        RuntimeError
            If the LLM call fails or the response cannot be parsed as
            valid JSON.
        """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Send a prompt and return the raw text response.

        Used by synthesizer.py to produce a human-readable explanation
        grounded in the structured data supplied in the prompt context.

        Parameters
        ----------
        prompt : str
            Full prompt including context data and generation
            instructions.

        Returns
        -------
        str
            The LLM's text response.

        Raises
        ------
        RuntimeError
            If the LLM call fails.
        """
