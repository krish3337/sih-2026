"""
certification_check.py — Direct lookup of certification requirements.

Deterministic certification lookup via StandardsRepository — no LLM involvement.
Preserves "not verified" and "N/A" placeholders exactly as stored.
"""

from typing import Dict, Optional

from ai_core.interfaces.standards_repository import StandardsRepository


class CertificationChecker:
    """Checks mandatory certification requirements for a standard."""

    def __init__(self, standards_repo: StandardsRepository) -> None:
        """
        Parameters
        ----------
        standards_repo : StandardsRepository
            Populated repository for certification lookup.
        """
        self._repo = standards_repo

    def get_certification_requirements(self, standard_no: str) -> Optional[Dict]:
        """
        Retrieve certification info for a given standard.

        Parameters
        ----------
        standard_no : str
            Full standard ID (e.g. "IS 5504:2025") or base ID.

        Returns
        -------
        dict or None
            A dictionary containing certification_name, mandatory, 
            qco_reference, and hs_code. Returns None if no data is found.
        """
        cert = self._repo.get_certification(standard_no)
        if not cert:
            return None

        return {
            "certification_name": cert.get("certification_name", "N/A"),
            "mandatory": cert.get("mandatory", "N/A"),
            "qco_reference": cert.get("qco_reference", "N/A"),
            "hs_code": cert.get("hs_code", "N/A"),
        }
