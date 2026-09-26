"""
GroqClient — wraps Groq API for extract() and generate().

Implements the LLMClient interface. Swappable to a local model
(Ollama) or another hosted API without changing any pipeline code.
"""

import json
import os
import re
from typing import Dict

from ai_core.interfaces.llm_client import LLMClient
from ai_core.errors import LLMUnavailableError, LLMInvalidOutputError


class GroqClient(LLMClient):
    """Groq API wrapper implementing the LLMClient interface."""

    def __init__(
        self,
        model_name: str = "llama-3.3-70b-versatile",
        api_key: str | None = None,
    ) -> None:
        """Initialise the Groq client.

        Parameters
        ----------
        model_name : str
            Groq model identifier.
        api_key : str or None
            API key.  If ``None``, read from the ``GROQ_API_KEY``
            environment variable.  Never hardcoded or logged.
        """
        self._model_name = model_name
        self._api_key = api_key or os.environ.get("GROQ_API_KEY", "")

        if not self._api_key:
            raise ValueError(
                "Groq API key not provided. Set the GROQ_API_KEY "
                "environment variable or pass api_key= to GroqClient()."
            )

        # Lazy import — avoids hard crash if groq isn't installed
        try:
            import groq
            self._client = groq.Groq(api_key=self._api_key)
        except ImportError as exc:
            raise ImportError(
                "groq package is required for GroqClient. "
                "Install with:  pip install groq"
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
        """Make a single Groq API call and return the text response.
        Includes exponential backoff for rate limits.
        """
        import time
        max_retries = 3
        base_delay = 5
        
        for attempt in range(max_retries):
            try:
                response = self._client.chat.completions.create(
                    model=self._model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                )
                text = response.choices[0].message.content
                if not text:
                    raise LLMInvalidOutputError("Groq returned an empty response.")
                return text.strip()
            except Exception as exc:
                err_str = str(exc)
                is_rate_limit = any(code in err_str for code in ["429", "503", "rate limit"])
                
                if is_rate_limit and attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"\n[GroqClient] Rate limit hit. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    continue
                
                raise LLMUnavailableError(f"Groq API call failed: {exc}") from exc

    @staticmethod
    def _parse_json(text: str) -> Dict:
        """Extract and parse JSON from an LLM response."""
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

        raise LLMInvalidOutputError(
            f"Could not parse JSON from LLM response:\n{text[:500]}"
        )
