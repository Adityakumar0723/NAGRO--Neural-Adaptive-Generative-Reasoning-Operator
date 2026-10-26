"""NAGRO 4.1 — Fully Self-Built FastAPI Application. 200K context, zero APIs."""

from __future__ import annotations
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from nagro.core.config import settings
from nagro.core.engine import NAGROEngine
from nagro.core.model_manager import is_model_downloaded
from nagro.core.system_monitor import SystemMonitor
from nagro.core.plugin_system import PluginManager
from api.routes.chat import router as chat_router
from api.routes.image import router as image_router
from api.routes.code import router as code_router
from api.routes.research import router as research_router
from api.routes.files import router as files_router
from api.routes.websocket import router as ws_router
from api.routes.openai_compat import router as openai_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = NAGROEngine()
    monitor = SystemMonitor()
    plugins = PluginManager()
    plugins.load_all()

    app.state.engine = engine
    app.state.monitor = monitor
    app.state.plugins = plugins

    model_status = "Ready" if is_model_downloaded() else "Run: python download_model.py"

    print(f"\n{'='*60}")
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
    print(f"  Engine       : NAGRO Self-Built Brain (Zero External AI)")
    print(f"  Context      : {settings.nagro_context_length:,} tokens (200K)")
    print(f"  Max Output   : {settings.nagro_max_tokens:,} tokens")
    print(f"  AI Models    : None (100% self-built)")
    print(f"  Image Engine : NAGRO Procedural (self-built)")
    print(f"  Status       : Ready")
    print(f"  Plugins      : {len(plugins.list_plugins())} loaded")
    print(f"  Web UI       : http://localhost:{settings.nagro_port}")
    print(f"  WebSocket    : ws://localhost:{settings.nagro_port}/ws/chat")
    print(f"  API Docs     : http://localhost:{settings.nagro_port}/docs")
    print(f"{'='*60}\n")
    yield
    print("\nNAGRO 4.1 shutting down...")


app = FastAPI(
    title="NAGRO 4.1",
    description=(
        "Neural Adaptive Generative Reasoning Operator — "
        "Fully self-built AI platform. 200K context. Zero external APIs. "
        "Advanced reasoning, coding, research, image generation, agentic tasks, "
        "RAG, file processing, and more."
    ),
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

# Register all routes
app.include_router(chat_router, prefix="/api/v1", tags=["Chat & Agent"])
app.include_router(image_router, prefix="/api/v1", tags=["Image Generation"])
app.include_router(code_router, prefix="/api/v1", tags=["Code"])
app.include_router(research_router, prefix="/api/v1", tags=["Research"])
app.include_router(files_router, prefix="/api/v1", tags=["Files & Code Analysis"])
app.include_router(ws_router, tags=["WebSocket"])
app.include_router(openai_router, prefix="/v1", tags=["OpenAI Compatible"])
# Mount OpenAI-compatible endpoint at multiple prefixes so BYOI platforms
# (OnDemand, LiteLLM, LangChain, etc.) can reach it regardless of how their
# proxy forwards paths.
app.include_router(openai_router, prefix="", tags=["OpenAI Compatible (root)"])
app.include_router(openai_router, prefix="/apps/nagro/v1", tags=["OpenAI Compatible (ondemand)"])
app.include_router(openai_router, prefix="/apps/nagro", tags=["OpenAI Compatible (ondemand-root)"])
app.include_router(openai_router, prefix="/openai/v1", tags=["OpenAI Compatible (openai-style)"])
app.include_router(openai_router, prefix="/api/openai/v1", tags=["OpenAI Compatible (api-openai)"])

# Static files
app.mount("/css", StaticFiles(directory="web/css"), name="css")
app.mount("/js", StaticFiles(directory="web/js"), name="js")
app.mount("/assets", StaticFiles(directory="web/assets"), name="assets")


@app.get("/")
async def root():
    return FileResponse("web/index.html")


@app.get("/_debug/routes")
async def debug_routes():
    """List every registered route — handy when a BYOI 404s and you need
    to see what paths NAGRO actually serves."""
    routes = []
    for r in app.routes:
        methods = getattr(r, "methods", None)
        path = getattr(r, "path", None)
        if path and methods:
            for m in methods:
                routes.append(f"{m} {path}")
    return {"count": len(routes), "routes": sorted(routes)}


@app.get("/api/v1/health")
async def health():
    return {
        "status": "operational",
        "model": "NAGRO 4.1",
        "version": "4.1.0",
        "inference": "100% local",
        "context_length": settings.nagro_context_length,
        "max_output_tokens": settings.nagro_max_tokens,
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
        "active": "NAGRO 4.1 Self-Built Brain",
        "context_length": settings.nagro_context_length,
        "external_models": "none",
    }


@app.get("/api/v1/system")
async def system_status():
    """Full system status — resources, performance, GPU, model info."""
    monitor = app.state.monitor
    return monitor.get_full_report()


@app.get("/api/v1/plugins")
async def list_plugins():
    """List loaded plugins."""
    return {"plugins": app.state.plugins.list_plugins()}


@app.get("/api/v1/memory/stats")
async def memory_stats():
    """Get persistent memory statistics."""
    from nagro.core.memory_store import MemoryStore
    store = MemoryStore()
    return store.get_stats()


@app.get("/api/v1/memory/conversations")
async def list_saved_conversations():
    """List saved conversations from persistent memory."""
    from nagro.core.memory_store import MemoryStore
    store = MemoryStore()
    return {"conversations": store.list_conversations()}


@app.post("/api/v1/benchmark")
async def run_benchmark():
    """Run the NAGRO benchmark suite."""
    from nagro.core.benchmarks import run_benchmarks
    engine = app.state.engine
    results = await run_benchmarks(engine)
    return results
