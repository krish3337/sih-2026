"""
GeminiClient — wraps Google Gemini API for extract() and generate().

Implements the LLMClient interface.  Swappable to a local model
(Ollama) or another hosted API without changing any pipeline code.

The pipeline makes exactly two LLM calls per query:
  1. extract()  — query understanding (structured attribute extraction)
  2. generate() — final synthesis (evidence-constrained explanation)
"""

import json
import os
import re
from typing import Dict

from ai_core.interfaces.llm_client import LLMClient


class GeminiClient(LLMClient):
    """Google Gemini API wrapper implementing the LLMClient interface."""

    def __init__(
        self,
        model_name: str = "gemini-3.6-flash",
        api_key: str | None = None,
    ) -> None:
        """Initialise the Gemini client.

        Parameters
        ----------
        model_name : str
            Gemini model identifier.
        api_key : str or None
            API key.  If ``None``, read from the ``GEMINI_API_KEY``
            environment variable.  Never hardcoded or logged.
        """
        self._model_name = model_name
        self._api_key = api_key or os.environ.get("GEMINI_API_KEY", "")

        if not self._api_key:
            raise ValueError(
                "Gemini API key not provided. Set the GEMINI_API_KEY "
                "environment variable or pass api_key= to GeminiClient()."
            )

        # Lazy import — avoids hard crash if google-genai isn't installed
        # until the client is actually instantiated.
        try:
            from google import genai
            self._client = genai.Client(api_key=self._api_key)
        except ImportError as exc:
            raise ImportError(
                "google-genai package is required for GeminiClient. "
                "Install with:  pip install google-genai"
            ) from exc

    # ── LLMClient interface ──────────────────────────────────────────────

    def extract(self, prompt: str) -> Dict:
        """Send *prompt*, parse the response as structured JSON.

        Raises RuntimeError if the call fails or the response is not
        valid JSON.
        """
        raw_text = self._call(prompt)
        return self._parse_json(raw_text)

    def generate(self, prompt: str) -> str:
        """Send *prompt*, return the raw text response.

        Raises RuntimeError if the call fails.
        """
        return self._call(prompt)

    # ── Internal helpers ─────────────────────────────────────────────────

    def _call(self, prompt: str) -> str:
        """Make a single Gemini API call and return the text response.
        Includes exponential backoff for 429/503 rate limits (5 req/min).
        """
        import time
        max_retries = 5
        base_delay = 15  # 15s base wait time handles the 5 requests/minute limit
        
        for attempt in range(max_retries):
            try:
                response = self._client.models.generate_content(
                    model=self._model_name,
                    contents=prompt,
                )
                text = response.text
                if not text:
                    raise RuntimeError("Gemini returned an empty response.")
                return text.strip()
            except Exception as exc:
                err_str = str(exc)
                is_rate_limit = any(code in err_str for code in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE"])
                
                if is_rate_limit and attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"\n[GeminiClient] Rate limit hit (429/503). Retrying in {delay} seconds...")
                    time.sleep(delay)
                    continue
                
                raise RuntimeError(f"Gemini API call failed: {exc}") from exc

    @staticmethod
    def _parse_json(text: str) -> Dict:
        """Extract and parse JSON from an LLM response.

        Handles common cases: response wrapped in ```json fences,
        response with leading/trailing prose around a JSON block, etc.
        """
        # Try direct parse first
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Strip markdown code fences
        cleaned = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
        cleaned = re.sub(r"```\s*$", "", cleaned, flags=re.MULTILINE)
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # Last resort: find the first { ... } block
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        raise RuntimeError(
            f"Could not parse JSON from LLM response:\n{text[:500]}"
        )
