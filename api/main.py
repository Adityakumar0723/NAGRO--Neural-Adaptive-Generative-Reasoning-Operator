"""NAGRO 4.1 — Fully Self-Built FastAPI Application."""

from __future__ import annotations
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from nagro.core.config import settings
from nagro.core.engine import NAGROEngine
from nagro.core.model_manager import is_model_downloaded
from api.routes.chat import router as chat_router
from api.routes.image import router as image_router
from api.routes.code import router as code_router
from api.routes.research import router as research_router


engine: NAGROEngine | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    engine = NAGROEngine()
    app.state.engine = engine

    model_status = "Ready" if is_model_downloaded() else "No model — run: python download_model.py"

    print(f"\n{'='*55}")
    print(f"  ███╗   ██╗ █████╗  ██████╗ ██████╗  ██████╗ ")
    print(f"  ████╗  ██║██╔══██╗██╔════╝ ██╔══██╗██╔═══██╗")
    print(f"  ██╔██╗ ██║███████║██║  ███╗██████╔╝██║   ██║")
    print(f"  ██║╚██╗██║██╔══██║██║   ██║██╔══██╗██║   ██║")
    print(f"  ██║ ╚████║██║  ██║╚██████╔╝██║  ██║╚██████╔╝")
    print(f"  ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝")
    print(f"")
    print(f"  Version 4.1 — Neural Adaptive Generative")
    print(f"  Reasoning Operator")
    print(f"")
    print(f"  Inference : 100% Local (No External APIs)")
    print(f"  LLM Model: {settings.nagro_llm_model}")
    print(f"  Status   : {model_status}")
    print(f"  Web UI   : http://localhost:{settings.nagro_port}")
    print(f"{'='*55}\n")
    yield
    print("\nNAGRO 4.1 shutting down...")


app = FastAPI(
    title="NAGRO 4.1",
    description="Neural Adaptive Generative Reasoning Operator — Fully self-built AI platform. No external APIs.",
    version="4.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])
app.include_router(image_router, prefix="/api/v1", tags=["Image"])
app.include_router(code_router, prefix="/api/v1", tags=["Code"])
app.include_router(research_router, prefix="/api/v1", tags=["Research"])

app.mount("/css", StaticFiles(directory="web/css"), name="css")
app.mount("/js", StaticFiles(directory="web/js"), name="js")
app.mount("/assets", StaticFiles(directory="web/assets"), name="assets")


@app.get("/")
async def root():
    return FileResponse("web/index.html")


@app.get("/api/v1/health")
async def health():
    return {
        "status": "operational",
        "model": "NAGRO 4.1",
        "version": "4.1.0",
        "inference": "local",
        "external_apis": "none",
    }


@app.get("/api/v1/info")
async def info():
    return app.state.engine.info


@app.get("/api/v1/models")
async def list_models():
    from nagro.core.model_manager import list_available_models, RECOMMENDED_MODELS
    return {
        "downloaded": list_available_models(),
        "recommended": RECOMMENDED_MODELS,
        "active": settings.nagro_llm_model,
    }
