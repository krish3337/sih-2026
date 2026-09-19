"""
synthesizer.py — Response Synthesis module (LLM Call 2).

Generates a human-readable explanation based strictly on the retrieved
deterministic data context. Enforces the evidence-only constraint to 
prevent hallucination.
"""

from typing import Dict, List, Any

from ai_core.interfaces.llm_client import LLMClient


class Synthesizer:
    """Synthesizes the final output response using structured context."""

    def __init__(self, llm_client: LLMClient) -> None:
        """
        Parameters
        ----------
        llm_client : LLMClient
            Interface instance for making generation calls.
        """
        self._llm = llm_client

    def synthesize_response(
        self,
        query: str,
        primary_candidates: List[Dict],
        allied_standards: List[Dict],
        status_info: Dict[str, Any],
        certification_info: Dict[str, Any]
    ) -> Dict:
        """
        Generates a human-readable explanation and formats the final response.

        Parameters
        ----------
        query : str
            The raw user query.
        primary_candidates : list[dict]
            Top retrieved candidates from Retriever.
        allied_standards : list[dict]
            Related standards for the top candidate from GraphExpansion.
        status_info : dict
            Status, version, and amendments for the top candidate.
        certification_info : dict
            Certification requirements for the top candidate.

        Returns
        -------
        dict
            The final structured payload containing the deterministic data
            plus the LLM-generated plain-language explanation.
        """
        # Group allied standards by relation type for cleaner output/context
        grouped_allied: Dict[str, List[Dict]] = {}
        for a in allied_standards:
            rt = a.get("relation_type", "Other")
            grouped_allied.setdefault(rt, []).append({
                "standard_id": a.get("standard_id", ""),
                "title": a.get("title", "N/A")
            })

        # Build the strict context string for the LLM
        context_str = f"USER QUERY: {query}\n\n"
        context_str += "PRIMARY CANDIDATES:\n"
        if not primary_candidates:
            context_str += "  None found.\n"
        for i, c in enumerate(primary_candidates):
            confidence_state = "LOW CONFIDENCE" if c.get("low_confidence") else "CONFIDENT"
            context_str += f"  {i+1}. {c.get('standard_id', '')} - {c.get('title', '')} [{confidence_state}, Score: {c.get('score')}]\n"
            context_str += f"     Scope Snippet: {c.get('scope_description', '')}\n"

        context_str += "\nALLIED STANDARDS (For Top Candidate):\n"
        if not grouped_allied:
            context_str += "  None found.\n"
        for rt, stds in grouped_allied.items():
            context_str += f"  {rt}:\n"
            for s in stds:
                context_str += f"    - {s['standard_id']}: {s['title']}\n"

        context_str += f"\nVERSION & STATUS (For Top Candidate):\n"
        if status_info:
            for k, v in status_info.items():
                context_str += f"  {k}: {v}\n"
        else:
            context_str += "  Not available.\n"

        context_str += f"\nCERTIFICATION REQUIREMENTS (For Top Candidate):\n"
        if certification_info:
            for k, v in certification_info.items():
                context_str += f"  {k}: {v}\n"
        else:
            context_str += "  Not available.\n"

        # CRITICAL CONSTRAINT enforces no hallucinations
        prompt = f"""
You are an AI assistant helping procurement officials find the correct Indian Standard.
Write a plain-language explanation of the findings based ONLY on the following context.

CRITICAL CONSTRAINTS: 
1. Only reference standard numbers, titles, and relationships present in the supplied context. 
2. Never invent or guess a standard number. If evidence is insufficient, say so explicitly.
3. Always include a summary of the certification requirements and version/amendment status.
4. When describing the Scope of a recommended standard, you MUST include a literal quoted excerpt from the provided "Scope Snippet". Do not paraphrase the scope. Format it exactly as: Scope: "[exact quote from snippet]"
5. Always include the match relevance state and confidence score for the primary standard (e.g., Match Relevance: CONFIDENT, Score: 0.9235).

CONTEXT:
{context_str}

EXPLANATION:
"""
        explanation = self._llm.generate(prompt)

        # Assemble the deterministic JSON payload with the generated text
        return {
            "primary_recommendations": primary_candidates,
            "allied_standards": grouped_allied,
            "status_info": status_info,
            "certification_info": certification_info,
            "explanation": explanation
        }
