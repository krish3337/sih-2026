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
        
        # Certification might be empty dict or populated dict
        cert_data = pipeline_result.get("certification_info", {})
        cert_info = None
        if cert_data:
            cert_info = CertificationInfo(
                certification_name=cert_data.get("certification_name"),
                mandatory=cert_data.get("mandatory"),
                qco_reference=cert_data.get("qco_reference"),
                hs_code=cert_data.get("hs_code")
            )
            
        status_data = pipeline_result.get("status_info", {})

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
                certification=cert_info
            )
        )

    # 2. Map Allied Standards
    mapped_allied = []
    grouped_allied = pipeline_result.get("allied_standards", {})
    for relation_type, stds in grouped_allied.items():
        for std in stds:
            mapped_allied.append(
                AlliedStandard(
                    standard_id=std.get("standard_id", ""),
                    title=std.get("title"),
                    relation_type=relation_type
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
        allied_standards=mapped_allied,
        explanation=pipeline_result.get("explanation", ""),
        detected_language=detected_lang,
        warnings=warnings,
        meta=meta_info
    )
