import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Use absolute imports from root module
from ai_core.config import create_embedder, create_llm_client
from scripts.run_demo import init_pipeline
from api.routes import router
from api.settings import settings
from api.errors import setup_exception_handlers
from api.schemas import MetaInfo
from api.utils import get_data_version

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle hook. 
    Builds the pipeline ONCE at startup and assigns it to app.state.
    Also extracts model IDs and data version for health metrics.
    """
    print("Starting API Server... Initializing Pipeline (this may take a minute).")
    
    # 1. Init pipeline
    try:
        pipeline = init_pipeline()
    except Exception as e:
        print(f"FATAL: Could not initialize pipeline: {e}")
        raise RuntimeError(f"Pipeline initialization failed: {e}")
        
    # 2. Get embedder ID & LLM ID
    embedder = create_embedder()
    try:
        llm = create_llm_client()
        llm_model = getattr(llm, "_model_name", type(llm).__name__)
    except:
        llm_model = "unknown"
        
    # 3. Calculate data version
    data_ver = get_data_version(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"))
    
    # Attach to app state
    app.state.pipeline = pipeline
    app.state.meta_info = MetaInfo(
        embedder_model_id=embedder.model_id,
        llm_model_id=llm_model,
        data_version=data_ver
    )
    
    print("Pipeline loaded successfully.")
    yield
    # Teardown (if necessary)
    print("Shutting down API server.")

def create_app() -> FastAPI:
    app = FastAPI(
        title="Project K Recommendation API",
        description="Versioned HTTP API on top of the Project K Recommendation Pipeline.",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Set up CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register exception handlers and routes
    setup_exception_handlers(app)
    app.include_router(router)
    
    return app

app = create_app()
