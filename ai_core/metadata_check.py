"""
metadata_check.py — Direct lookup of standard version, status, and amendments.

Deterministic metadata lookup via StandardsRepository — no LLM involvement.
"""

from typing import Dict, Optional

from ai_core.interfaces.standards_repository import StandardsRepository


class MetadataChecker:
    """Checks version, status, and amendment history for a standard."""

    def __init__(self, standards_repo: StandardsRepository) -> None:
        """
        Parameters
        ----------
        standards_repo : StandardsRepository
            Populated repository for metadata lookup.
        """
        self._repo = standards_repo

    def check_status(self, standard_no: str) -> Optional[Dict]:
        """
        Retrieve metadata for a given standard.

        Parameters
        ----------
        standard_no : str
            Base or full standard ID.

        Returns
        -------
        dict or None
            A dictionary containing status, current_version_year, 
            superseded_by, superseding_is, and amendments list.
            Returns None if the standard is not found.
        """
        record = self._repo.get(standard_no)
        if not record:
            return None

        return {
            "status": record.get("status", "N/A"),
            "current_version_year": record.get("current_version_year", "N/A"),
            "superseded_by": record.get("superseded_by", "N/A"),
            "superseding_is": record.get("superseding_is", "N/A"),
            "amendments": record.get("amendments", []),
        }
