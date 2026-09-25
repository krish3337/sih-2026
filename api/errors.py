from fastapi import Request, status
from fastapi.responses import JSONResponse

from ai_core.errors import DomainError, LLMUnavailableError, LLMInvalidOutputError

# API-level custom exceptions
class APIError(Exception):
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code

class InvalidInputError(APIError):
    def __init__(self, message: str):
        super().__init__("INVALID_INPUT", message, status.HTTP_422_UNPROCESSABLE_ENTITY)

class FileTooLargeError(APIError):
    def __init__(self, message: str):
        super().__init__("FILE_TOO_LARGE", message, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

class UnsupportedFileTypeError(APIError):
    def __init__(self, message: str):
        super().__init__("UNSUPPORTED_FILE_TYPE", message, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

class PDFNoExtractableTextError(APIError):
    def __init__(self, message: str):
        super().__init__("PDF_NO_EXTRACTABLE_TEXT", message, status.HTTP_422_UNPROCESSABLE_ENTITY)

# Global exception handlers for FastAPI
def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message}
    )

def llm_unavailable_handler(request: Request, exc: LLMUnavailableError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"code": "LLM_UNAVAILABLE", "message": exc.message}
    )

def llm_invalid_output_handler(request: Request, exc: LLMInvalidOutputError):
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"code": "LLM_INVALID_OUTPUT", "message": exc.message}
    )

def request_timeout_handler(request: Request, exc: TimeoutError):
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content={"code": "REQUEST_TIMEOUT", "message": "The request timed out."}
    )

def internal_error_handler(request: Request, exc: Exception):
    # In production, we log the exc stacktrace here
    print(f"INTERNAL ERROR: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code": "INTERNAL_ERROR", "message": "An unexpected internal error occurred."}
    )

def setup_exception_handlers(app):
    app.add_exception_handler(APIError, api_error_handler)
    app.add_exception_handler(LLMUnavailableError, llm_unavailable_handler)
    app.add_exception_handler(LLMInvalidOutputError, llm_invalid_output_handler)
    app.add_exception_handler(TimeoutError, request_timeout_handler)
    app.add_exception_handler(Exception, internal_error_handler)
