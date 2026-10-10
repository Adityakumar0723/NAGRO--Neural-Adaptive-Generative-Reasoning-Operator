"""NAGRO 4.1 - FastAPI Application."""

from __future__ import annotations
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from nagro.core.config import settings
from nagro.core.engine import NAGROEngine
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
    print(f"\n{'='*50}")
    print(f"  NAGRO 4.1 - Neural Adaptive Generative")
    print(f"  Reasoning Operator")
    print(f"  Version: {engine.version}")
    print(f"  Provider: {settings.nagro_llm_provider}")
    print(f"  Status: Operational")
    print(f"{'='*50}\n")
    yield
    print("\nNAGRO 4.1 shutting down...")


app = FastAPI(
    title="NAGRO 4.1",
    description="Neural Adaptive Generative Reasoning Operator - A multi-modal AI platform",
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
    return {"status": "operational", "model": "NAGRO 4.1", "version": "4.1.0"}


@app.get("/api/v1/info")
async def info():
    return app.state.engine.info
