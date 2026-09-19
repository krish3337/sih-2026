"""
InMemoryStandardsRepository — reads from data/standards.json and
data/certification_rules.json, serves lookups from memory.

Implements the StandardsRepository interface; swappable to a Postgres-
backed implementation without changing any pipeline code.

All lookups are direct data access — no LLM involvement — so they can
never return fabricated metadata.
"""

import json
import os
from typing import Dict, List, Optional

from ai_core.interfaces.standards_repository import StandardsRepository


class InMemoryStandardsRepository(StandardsRepository):
    """In-memory repository backed by JSON files loaded at init time."""

    def __init__(
        self,
        standards_path: str = os.path.join("data", "standards.json"),
        certification_path: str = os.path.join(
            "data", "certification_rules.json"
        ),
    ) -> None:
        # ── Load standards ───────────────────────────────────────────
        with open(standards_path, "r", encoding="utf-8") as fh:
            standards_list: List[Dict] = json.load(fh)

        # Index by base_id for fast lookup (graph uses base_id)
        self._by_base_id: Dict[str, Dict] = {}
        # Also index by full standard_id (certification uses full ID)
        self._by_standard_id: Dict[str, Dict] = {}

        for record in standards_list:
            base_id = record.get("base_id", "")
            standard_id = record.get("standard_id", "")
            self._by_base_id[base_id] = record
            self._by_standard_id[standard_id] = record

        self._all_standards: List[Dict] = standards_list

        # ── Load certifications ──────────────────────────────────────
        self._certifications: Dict[str, Dict] = {}
        if os.path.exists(certification_path):
            with open(certification_path, "r", encoding="utf-8") as fh:
                self._certifications = json.load(fh)

    # ── StandardsRepository interface ────────────────────────────────────

    def get(self, standard_id: str) -> Optional[Dict]:
        """Retrieve by base_id first, fall back to full standard_id.

        This allows both ``get("IS 5504")`` (graph/relation lookup)
        and ``get("IS 5504:2025")`` (direct lookup) to work.
        """
        record = self._by_base_id.get(standard_id)
        if record is None:
            record = self._by_standard_id.get(standard_id)
        return record

    def get_all(self) -> List[Dict]:
        """Return every standard record."""
        return list(self._all_standards)

    def search_by_status(self, status: str) -> List[Dict]:
        """Return all standards matching *status* (case-insensitive)."""
        target = status.strip().lower()
        return [
            s for s in self._all_standards
            if str(s.get("status", "")).strip().lower() == target
        ]

    def get_certification(self, standard_id: str) -> Optional[Dict]:
        """Retrieve certification info by full standard_id.

        Falls back to searching by base_id match against certification
        keys if a direct key lookup fails.
        """
        # Direct lookup by full standard_id key
        cert = self._certifications.get(standard_id)
        if cert is not None:
            return cert

        # Fallback: the caller may have passed a base_id — try to find
        # the matching full-ID key
        for key, value in self._certifications.items():
            if key.startswith(standard_id):
                return value

        return None

    # ── Utility ──────────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        """Number of standards in the repository."""
        return len(self._all_standards)
