"""
graph_expansion.py — Graph traversal for allied standards.

Retrieves allied standards connected via normative references,
test methods, terminology, etc.
Deterministic BFS over GraphStore — no LLM involvement.
"""

from typing import Dict, List

from ai_core.interfaces.graph_store import GraphStore
from ai_core.interfaces.standards_repository import StandardsRepository


class GraphExpander:
    """Expands a standard to find allied/related standards."""

    def __init__(
        self,
        graph_store: GraphStore,
        standards_repo: StandardsRepository,
    ) -> None:
        """
        Parameters
        ----------
        graph_store : GraphStore
            Populated graph store for BFS.
        standards_repo : StandardsRepository
            To enrich the neighbor IDs with titles (if available).
        """
        self._graph = graph_store
        self._repo = standards_repo

    def get_allied_standards(
        self, standard_no: str, max_hops: int = 2
    ) -> List[Dict]:
        """
        BFS traversal returning related standards.

        Parameters
        ----------
        standard_no : str
            Base standard ID to start from (e.g. "IS 5504").
        max_hops : int
            Maximum traversal depth.

        Returns
        -------
        list[dict]
            List of related standards containing standard_id,
            relation_type, hop, and title (if available in repo).
        """
        neighbors = self._graph.get_neighbors(standard_no, max_hops=max_hops)
        
        enriched = []
        for n in neighbors:
            sid = n["standard_id"]
            record = self._repo.get(sid)
            
            # Use full standard_id if available, otherwise just use the base ID.
            full_id = record["standard_id"] if record else sid
            title = record.get("title", "N/A") if record else "N/A"
            
            enriched.append({
                "standard_id": full_id,
                "base_id": sid,
                "title": title,
                "relation_type": n["relation_type"],
                "hop": n["hop"]
            })
            
        return enriched
