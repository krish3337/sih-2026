"""
pipeline.py — The main orchestration layer (Phase 6).

Wires together Query Understanding, Retrieval, Graph Expansion, 
Metadata, Certification, and Synthesizer modules into a unified flow.
"""

from typing import Dict

from ai_core.query_understanding import QueryUnderstanding
from ai_core.retriever import Retriever
from ai_core.graph_expansion import GraphExpander
from ai_core.metadata_check import MetadataChecker
from ai_core.certification_check import CertificationChecker
from ai_core.synthesizer import Synthesizer
from ai_core.pdf_input import PDFInput


class RecommendationPipeline:
    """End-to-end pipeline for Indian Standards recommendation."""

    def __init__(
        self,
        query_understanding: QueryUnderstanding,
        retriever: Retriever,
        graph_expander: GraphExpander,
        metadata_checker: MetadataChecker,
        certification_checker: CertificationChecker,
        synthesizer: Synthesizer,
        pdf_input: PDFInput,
    ) -> None:
        """Inject all dependencies."""
        self._qu = query_understanding
        self._retriever = retriever
        self._expander = graph_expander
        self._meta = metadata_checker
        self._cert = certification_checker
        self._synth = synthesizer
        self._pdf = pdf_input

    def recommend(self, text: str) -> Dict:
        """
        Runs the full recommendation pipeline on raw text.

        Parameters
        ----------
        text : str
            Raw user query or text from a document.

        Returns
        -------
        dict
            The final structured payload and generated explanation.
        """
        # 1. Query Understanding (LLM Call 1)
        qu_result = self._qu.extract_query_attributes(text)
        retrieval_query = qu_result.get("retrieval_query", text)

        # 2. Retrieval (Deterministic Semantic Search)
        candidates = self._retriever.retrieve_candidates(retrieval_query, top_k=5)
        
        # 3. Data Check (Deterministic Graph, Metadata, Certification)
        # We fetch allied standards and status for the top candidate for the LLM synthesizer,
        # but fetch certification, status, and allied for EACH candidate for the UI mapper.
        top_candidate = candidates[0] if candidates else None
        
        top_allied = []
        top_status = {}

        if top_candidate:
            base_id = top_candidate["base_id"]
            top_allied = self._expander.get_allied_standards(base_id, max_hops=1)
            top_status = self._meta.check_status(base_id) or {}

        # Fetch data for EACH candidate individually
        for candidate in candidates:
            base_id = candidate["base_id"]
            full_id = candidate["standard_id"]
            candidate["certification_info"] = self._cert.get_certification_requirements(full_id) or {}
            candidate["status_info"] = self._meta.check_status(base_id) or {}
            candidate["allied_standards"] = self._expander.get_allied_standards(base_id, max_hops=1)

        # 4. Synthesizer (LLM Call 2 - Evidence Constrained)
        response = self._synth.synthesize_response(
            query=text,
            primary_candidates=candidates,
            allied_standards=top_allied,
            status_info=top_status,
        )

        # Attach extraction result for inspection/debugging downstream
        response["query_understanding"] = qu_result

        return response

    def recommend_from_pdf(self, pdf_path: str) -> Dict:
        """
        Extracts text from a PDF and runs the recommendation pipeline.

        Parameters
        ----------
        pdf_path : str
            Path to the PDF file.

        Returns
        -------
        dict
            The final structured payload and generated explanation.
        """
        text = self._pdf.extract_text(pdf_path)
        if not text:
            raise ValueError(f"No readable text found in PDF: {pdf_path}")
        
        return self.recommend(text)
