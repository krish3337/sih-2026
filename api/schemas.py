from typing import List, Optional, Any
from pydantic import BaseModel, Field

class CertificationInfo(BaseModel):
    certification_name: Optional[str] = None
    mandatory: Optional[bool] = None
    qco_reference: Optional[str] = None
    hs_code: Optional[str] = None

class Recommendation(BaseModel):
    standard_id: str
    base_id: str
    title: str = "N/A"
    similarity_score: float = Field(..., description="Raw cosine similarity (not a probability or percentage)")
    low_confidence: bool
    status: str = "N/A"
    current_version_year: str = "N/A"
    superseded_by: Optional[str] = None
    superseding_is: Optional[str] = None
    amendments: List[str] = Field(default_factory=list)
    certification: Optional[CertificationInfo] = None

class AlliedStandard(BaseModel):
    standard_id: str
    title: Optional[str] = None
    relation_type: Optional[str] = None

class WarningMessage(BaseModel):
    code: str
    message: str

class MetaInfo(BaseModel):
    embedder_model_id: str
    llm_model_id: str
    data_version: str

class RecommendRequest(BaseModel):
    text: str = Field(..., min_length=1)
    language_hint: Optional[str] = None

class RecommendResponse(BaseModel):
    recommendations: List[Recommendation]
    allied_standards: List[AlliedStandard]
    explanation: str
    detected_language: Optional[str] = None
    warnings: List[WarningMessage] = Field(default_factory=list)
    meta: MetaInfo

class HealthResponse(BaseModel):
    status: str
    pipeline_loaded: bool
    embedder_model_id: str
    llm_model_id: str
    data_version: str
