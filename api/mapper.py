from typing import Dict, Any, List
from api.schemas import (
    RecommendResponse,
    Recommendation,
    AlliedStandard,
    CertificationInfo,
    MetaInfo,
    WarningMessage
)

def map_pipeline_response(
    pipeline_result: Dict[str, Any], 
    meta_info: MetaInfo,
    warnings: List[WarningMessage]
) -> RecommendResponse:
    """
    Maps the internal pipeline dictionary to the public Pydantic RecommendResponse schema.
    """
    # 1. Map Recommendations
    mapped_recs = []
    for rec in pipeline_result.get("primary_recommendations", []):
        
        # Certification is now per-candidate, attached directly to each rec
        cert_data = rec.get("certification_info", {})
        cert_info = None
        if cert_data:
            cert_info = CertificationInfo(
                certification_name=cert_data.get("certification_name"),
                mandatory=cert_data.get("mandatory"),
                qco_reference=cert_data.get("qco_reference"),
                hs_code=cert_data.get("hs_code")
            )
            
        status_data = rec.get("status_info", {})
        
        # Map per-candidate allied standards
        rec_allied = []
        for a in rec.get("allied_standards", []):
            rec_allied.append(
                AlliedStandard(
                    standard_id=a.get("standard_id", ""),
                    title=a.get("title"),
                    relation_type=a.get("relation_type", "Other")
                )
            )

        mapped_recs.append(
            Recommendation(
                standard_id=rec.get("standard_id", ""),
                base_id=rec.get("base_id", ""),
                title=rec.get("title", "N/A"),
                similarity_score=rec.get("score", 0.0),
                low_confidence=rec.get("low_confidence", False),
                status=rec.get("status", "N/A"),
                current_version_year=str(rec.get("current_version_year", "N/A")),
                superseded_by=status_data.get("superseded_by"),
                superseding_is=status_data.get("superseding_is"),
                amendments=status_data.get("amendments", []),
                certification=cert_info,
                allied_standards=rec_allied
            )
        )

    # 3. Extract detected language from query_understanding (LLM Call 1)
    detected_lang = None
    if "query_understanding" in pipeline_result:
        detected_lang = pipeline_result["query_understanding"].get("detected_language")
        
    # Check for low confidence in top candidate
    if mapped_recs and mapped_recs[0].low_confidence:
        warnings.append(WarningMessage(
            code="NO_CONFIDENT_MATCH", 
            message="No highly confident match was found for your query. Showing best available results."
        ))

    return RecommendResponse(
        recommendations=mapped_recs,
        explanation=pipeline_result.get("explanation", ""),
        detected_language=detected_lang,
        warnings=warnings,
        meta=meta_info
    )
