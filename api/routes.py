import asyncio
from fastapi import APIRouter, Request, UploadFile, File, Form, Depends
from fastapi.concurrency import run_in_threadpool

from ai_core.pipeline import RecommendationPipeline
from api.schemas import RecommendRequest, RecommendResponse, HealthResponse, MetaInfo, WarningMessage
from api.settings import settings
from api.mapper import map_pipeline_response
from api.errors import (
    InvalidInputError, 
    FileTooLargeError, 
    UnsupportedFileTypeError, 
    PDFNoExtractableTextError
)

router = APIRouter(prefix=settings.API_PREFIX)

def get_pipeline(request: Request) -> RecommendationPipeline:
    return request.app.state.pipeline

def get_meta_info(request: Request) -> MetaInfo:
    return request.app.state.meta_info

async def execute_pipeline_with_timeout(pipeline: RecommendationPipeline, method: str, *args) -> dict:
    """Executes a pipeline method in a threadpool with a strict timeout."""
    loop = asyncio.get_running_loop()
    func = getattr(pipeline, method)
    
    try:
        # Run synchronous pipeline in threadpool to avoid blocking event loop
        return await asyncio.wait_for(
            run_in_threadpool(func, *args),
            timeout=settings.REQUEST_TIMEOUT_SECONDS
        )
    except asyncio.TimeoutError:
        raise TimeoutError()

@router.get("/health", response_model=HealthResponse)
async def health_check(
    pipeline: RecommendationPipeline = Depends(get_pipeline),
    meta: MetaInfo = Depends(get_meta_info)
):
    """Checks system health and returns loaded models and data version."""
    return HealthResponse(
        status="ok",
        pipeline_loaded=pipeline is not None,
        embedder_model_id=meta.embedder_model_id,
        llm_model_id=meta.llm_model_id,
        data_version=meta.data_version
    )

@router.post("/recommend", response_model=RecommendResponse)
async def recommend(
    req: RecommendRequest,
    pipeline: RecommendationPipeline = Depends(get_pipeline),
    meta: MetaInfo = Depends(get_meta_info)
):
    """Processes a plain-text query and returns recommendations."""
    text = req.text.strip()
    if not text:
        raise InvalidInputError("Query text cannot be empty or whitespace.")

    warnings = []
    
    # Input Truncation
    if len(text) > settings.MAX_INPUT_CHARS:
        text = text[:settings.MAX_INPUT_CHARS]
        warnings.append(WarningMessage(
            code="INPUT_TRUNCATED",
            message=f"Input exceeded maximum allowed length ({settings.MAX_INPUT_CHARS} characters) and was truncated."
        ))

    # Append language hint if provided
    if req.language_hint:
        text += f"\n[User Language Hint: {req.language_hint}]"

    result = await execute_pipeline_with_timeout(pipeline, "recommend", text)
    return map_pipeline_response(result, meta, warnings)

@router.post("/recommend/pdf", response_model=RecommendResponse)
async def recommend_from_pdf(
    file: UploadFile = File(...),
    query: str = Form(None),
    pipeline: RecommendationPipeline = Depends(get_pipeline),
    meta: MetaInfo = Depends(get_meta_info)
):
    """
    Processes a PDF file. If query is provided, the PDF text is used as supporting context.
    """
    if not file.filename.lower().endswith(".pdf") or file.content_type != "application/pdf":
        raise UnsupportedFileTypeError("Uploaded file must be a PDF document.")
        
    # Read file content safely
    content = await file.read()
    
    # Validate PDF magic bytes (%PDF)
    if not content.startswith(b"%PDF"):
        raise UnsupportedFileTypeError("File does not have a valid PDF signature.")
        
    if len(content) > (settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024):
        raise FileTooLargeError(f"PDF exceeds the {settings.MAX_UPLOAD_SIZE_MB}MB limit.")

    # Save to temp file for the pipeline to read
    import tempfile
    import os
    
    warnings = []
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # Extract text via pipeline's internal PDFInput (inthread to avoid blocking)
        pdf_text = await run_in_threadpool(pipeline._pdf.extract_text, tmp_path)
        
        if not pdf_text or not pdf_text.strip():
            raise PDFNoExtractableTextError("No readable text found in PDF (might be scanned or empty).")
            
        # Truncate PDF text if too long
        if len(pdf_text) > settings.MAX_INPUT_CHARS:
            pdf_text = pdf_text[:settings.MAX_INPUT_CHARS]
            warnings.append(WarningMessage(
                code="INPUT_TRUNCATED",
                message=f"PDF text exceeded {settings.MAX_INPUT_CHARS} characters and was truncated."
            ))

        # Default Assumption handling:
        # If query is provided, it is the primary text and the extracted PDF text is appended as labelled supporting context
        if query and query.strip():
            final_text = f"Primary Query: {query.strip()}\n\nSupporting Context (from PDF):\n{pdf_text}"
        else:
            final_text = pdf_text
            
        result = await execute_pipeline_with_timeout(pipeline, "recommend", final_text)
        return map_pipeline_response(result, meta, warnings)
        
    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
