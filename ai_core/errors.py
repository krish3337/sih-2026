class DomainError(Exception):
    """Base exception for AI Core domain errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class LLMError(DomainError):
    """Base exception for all LLM-related errors."""
    pass

class LLMUnavailableError(LLMError):
    """Raised when the LLM service is unavailable, timeouts, or fails after retries."""
    pass

class LLMInvalidOutputError(LLMError):
    """Raised when the LLM output is malformed, not valid JSON, or missing required keys."""
    pass

class VectorStoreError(DomainError):
    """Base exception for VectorStore errors."""
    pass

class EmbedderMismatchError(VectorStoreError):
    """Raised when the vector store detects a mismatch with the current embedder model."""
    pass
