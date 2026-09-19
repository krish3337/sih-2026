"""
GraphStore interface — abstract contract for the cross-reference graph.

Edges connect standards by relation type (Normative Reference, Test Method,
Terminology, Related Product, Safety, Installation).  Graph traversal is
always deterministic BFS — no LLM involvement — so it can never hallucinate
a relationship that isn't in the data.

Pipeline modules depend on this interface, never on a concrete implementation.
"""

from abc import ABC, abstractmethod
from typing import Dict, List


class GraphStore(ABC):
    """Store and traverse the standards cross-reference graph."""

    @abstractmethod
    def add_edge(
        self, from_id: str, to_id: str, relation_type: str
    ) -> None:
        """Add a directed edge between two standards.

        Parameters
        ----------
        from_id : str
            Source standard base_id.
        to_id : str
            Target standard base_id.
        relation_type : str
            One of: Normative Reference, Test Method, Terminology,
            Related Product, Safety, Installation.
        """

    @abstractmethod
    def get_neighbors(
        self, standard_id: str, max_hops: int = 2
    ) -> List[Dict]:
        """BFS traversal returning all standards reachable within *max_hops*.

        Parameters
        ----------
        standard_id : str
            Starting node (standard base_id).
        max_hops : int
            Maximum graph distance to traverse.

        Returns
        -------
        list[dict]
            Each dict contains:
            - ``standard_id``: the neighbour's base_id
            - ``relation_type``: edge label
            - ``hop``: distance from the starting node (1-based)
        """
