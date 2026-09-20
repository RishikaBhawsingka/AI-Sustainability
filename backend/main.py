from fastapi import FastAPI
from backend.models.model_loader import gpu_model, tlhc_model
from backend.routes.gpu import router as gpu_router
from backend.routes.thermal import router as thermal_router
from backend.routes.analyze import router as analyze_router
from backend.routes.cooling import router as cooling_router
from backend.routes.rag import router as rag_router
from backend.routes.llm import router as llm_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Aquatherma AI",
    description="AI-based data center cooling intelligence system",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(gpu_router)
app.include_router(thermal_router)
app.include_router(analyze_router)
app.include_router(cooling_router)
app.include_router(rag_router)
app.include_router(llm_router)

@app.get("/")
def home():
    return {
        "message": "Aquatherma AI Backend is running",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "gpu_model": "loaded",
        "tlhc_model": "loaded"
    }