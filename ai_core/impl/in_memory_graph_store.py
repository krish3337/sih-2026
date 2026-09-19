"""
InMemoryGraphStore — adjacency dict with BFS traversal.

Sufficient at the current edge count (130 edges).  Implements the
GraphStore interface; swappable to Postgres recursive CTE or a
dedicated graph store without changing any pipeline code.

Graph traversal is always deterministic BFS — no LLM involvement —
so it can never hallucinate a relationship that isn't in the data.
"""

from collections import deque
from typing import Dict, List, Set, Tuple

from ai_core.interfaces.graph_store import GraphStore


class InMemoryGraphStore(GraphStore):
    """Directed graph stored as an adjacency dict with BFS traversal."""

    def __init__(self) -> None:
        # adjacency: { from_id: [ (to_id, relation_type), ... ] }
        self._adjacency: Dict[str, List[Tuple[str, str]]] = {}
        self._edge_count: int = 0

    # ── GraphStore interface ─────────────────────────────────────────────

    def add_edge(
        self, from_id: str, to_id: str, relation_type: str
    ) -> None:
        """Add a directed edge from *from_id* to *to_id*.

        Duplicate edges (same from, to, and type) are silently ignored.
        """
        neighbors = self._adjacency.setdefault(from_id, [])

        # Avoid duplicate edges
        edge = (to_id, relation_type)
        if edge not in neighbors:
            neighbors.append(edge)
            self._edge_count += 1

    def get_neighbors(
        self, standard_id: str, max_hops: int = 2
    ) -> List[Dict]:
        """BFS from *standard_id* up to *max_hops* depth.

        Returns all reachable standards with their relation type and
        hop distance.  The starting node is never included in the
        results.
        """
        results: List[Dict] = []
        visited: Set[str] = {standard_id}

        # BFS queue: (current_node, current_hop)
        queue: deque[Tuple[str, int]] = deque()
        queue.append((standard_id, 0))

        while queue:
            node, hop = queue.popleft()

            if hop >= max_hops:
                continue

            for neighbor_id, rel_type in self._adjacency.get(node, []):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    next_hop = hop + 1
                    results.append({
                        "standard_id": neighbor_id,
                        "relation_type": rel_type,
                        "hop": next_hop,
                    })
                    queue.append((neighbor_id, next_hop))

        return results

    # ── Utility ──────────────────────────────────────────────────────────

    @property
    def edge_count(self) -> int:
        """Total number of unique directed edges."""
        return self._edge_count

    @property
    def node_count(self) -> int:
        """Number of distinct nodes that appear as edge sources."""
        return len(self._adjacency)
