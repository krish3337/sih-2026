"""
StandardsRepository interface — abstract contract for structured standard
metadata access.

Covers: standard details, status/version, amendments, certification.
All lookups are direct data access — no LLM involvement — so they can never
return fabricated metadata.

Pipeline modules depend on this interface, never on a concrete implementation.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class StandardsRepository(ABC):
    """Read-only access to the verified standards knowledge base."""

    @abstractmethod
    def get(self, standard_id: str) -> Optional[Dict]:
        """Retrieve a single standard record by base_id.

        Parameters
        ----------
        standard_id : str
            The normalised base_id (e.g. ``"IS 5504"``).

        Returns
        -------
        dict or None
            Full standard record including amendments, or ``None`` if
            the ID is not found in the repository.
        """

    @abstractmethod
    def get_all(self) -> List[Dict]:
        """Return every standard record in the repository.

        Returns
        -------
        list[dict]
            All standard records.
        """

    @abstractmethod
    def search_by_status(self, status: str) -> List[Dict]:
        """Return all standards matching *status*.

        Parameters
        ----------
        status : str
            One of: ``Active``, ``Withdrawn``, ``Superseded``,
            ``Under Revision``.

        Returns
        -------
        list[dict]
            Standards whose ``status`` field matches.
        """

    @abstractmethod
    def get_certification(self, standard_id: str) -> Optional[Dict]:
        """Retrieve certification info for a standard.

        Parameters
        ----------
        standard_id : str
            The full ``standard_id`` (e.g. ``"IS 5504:2025"``) as used
            in certification_rules.json keys.

        Returns
        -------
        dict or None
            Certification record, or ``None`` if no certification data
            exists for this standard.
        """
