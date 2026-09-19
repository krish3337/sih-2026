# MVP Folder Structure — Project K

As we move from a standalone AI prototype to a fully fledged MVP that includes a **Frontend** (User Interface) and a **Backend** (Web API Server), organizing the codebase properly is critical. 

Below is the recommended folder structure. It follows a **Monorepo** pattern, keeping the frontend, backend, and AI pipeline in the same repository for rapid MVP development while maintaining strict separation of concerns.

## Proposed Directory Layout

```text
SIH DEMO/
│
├── .env                       # Environment variables (API keys, ports)
├── .gitignore                 # Ignores venv, node_modules, .env, __pycache__
├── requirements.txt           # Python dependencies for Backend + AI
│
├── frontend/                  # 🟢 FRONTEND: User Interface (e.g., React, Next.js, or HTML/JS)
│   ├── package.json           # Frontend dependencies (NPM)
│   ├── public/                # Static assets (images, logos)
│   └── src/
│       ├── components/        # Reusable UI elements (Buttons, Chat bubbles)
│       ├── pages/             # Main screens (Home, Results)
│       └── services/          # Functions that make HTTP calls to our Backend API
│
├── backend/                   # 🔵 BACKEND: REST API Server (e.g., FastAPI)
│   ├── main.py                # Server entry point (Starts the web server)
│   ├── routers/               # API endpoints (e.g., POST /api/recommend)
│   └── schemas/               # Data validation models (Pydantic) to ensure clean inputs
│
├── ai_core/                   # 🟣 AI SYSTEM: (This is our current 'src' folder!)
│   ├── interfaces/            # Abstract classes (LLMClient, VectorStore)
│   ├── impl/                  # Concrete implementations (GeminiClient)
│   ├── config.py              # Configuration and dependency wiring
│   └── pipeline.py            # The RecommendationPipeline orchestrator
│
├── data/                      # 🗄️ DATA: Processed JSON stores (standards, relations)
├── docs/                      # 📄 DOCS: Architecture, PRD, SRS, Development Plans
├── scripts/                   # ⚙️ UTILITIES: Standalone scripts (e.g., adapter.py, run_evaluation.py)
│
└── tests/                     # 🧪 TESTING: Unit tests for backend and AI logic
```

---

## Why this structure?

1. **Clear Separation of Concerns (Frontend vs Backend)**
   The AI system shouldn't know anything about HTML/CSS, and the Frontend shouldn't know anything about Vector Embeddings. The `backend/` folder acts as the bridge. The frontend talks to the backend via HTTP, and the backend imports the `ai_core/pipeline.py` to do the heavy lifting.

2. **Protecting the AI Core (`ai_core/`)**
   Our current `src` folder (renamed to `ai_core` here for clarity) remains untouched. Because we built it cleanly using interfaces, the `backend/main.py` can simply import `RecommendationPipeline`, pass in the user's text from a web request, and return the JSON response. 

3. **Scalability**
   If the MVP grows and you want to deploy the frontend to Vercel/Netlify and the backend to AWS/Google Cloud, this structure makes it very easy to split them apart later. 

4. **Cleaner Root Directory**
   Right now, our root directory has scripts like `adapter.py`, `run_demo.py`, and `test_api.py` floating around. Moving them into a `scripts/` folder keeps the root clean and focused only on configuration files (like `.env` and `requirements.txt`).
