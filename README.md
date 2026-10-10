<div align="center">

# NAGRO 4.1

### Neural Adaptive Generative Reasoning Operator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Self Built](https://img.shields.io/badge/100%25-Self--Built-purple?style=for-the-badge)]()
[![No APIs](https://img.shields.io/badge/External_APIs-ZERO-red?style=for-the-badge)]()
[![Context](https://img.shields.io/badge/Context-200K_Tokens-orange?style=for-the-badge)]()

**A powerful, 100% self-built AI platform. No external AI models. No PyTorch. No Transformers. NAGRO's own brain.**

**No OpenAI. No Anthropic. No Google. No LLaMA. No Qwen. No borrowed intelligence. Everything built from scratch.**

Built by [Aditya Kumar](https://github.com/Adityakumar0723)

---

</div>

## Why NAGRO?

Most "AI products" are just thin wrappers around someone else's API. **NAGRO 4.1 is built from the ground up.**

- **100% Self-Built AI Brain** — NAGRO's own intelligence, not a wrapper around GPT/LLaMA/Qwen
- **Zero External AI Models** — No PyTorch, no Transformers, no HuggingFace, no pretrained weights
- **200K Context Window** — Massive context support
- **Zero External APIs** — No data ever leaves your system
- **No API Keys** — Install, run, done. Free forever
- **Advanced Reasoning** — Chain-of-thought, tree-of-thought, self-reflection, internal debate
- **Agentic System** — Multi-step autonomous task execution with tool use
- **RAG Pipeline** — TF-IDF based document retrieval (self-built, no neural embeddings)
- **Persistent Memory** — SQLite-backed memory that survives across sessions
- **Plugin System** — Extensible architecture for custom tools and agents
- **Procedural Image Generation** — NAGRO's own image engine (no Stable Diffusion)
- **Multi-Language Code Execution** — Sandboxed Python + JavaScript (Node.js)
- **AST Code Analysis** — Complexity metrics, security checks, issue detection
- **Free Web Search** — DuckDuckGo, no API key needed
- **CLI + Web UI + WebSocket** — Three ways to interact
- **Benchmark Suite** — Test reasoning, coding, math, knowledge
- **Lightweight** — No GPU needed, runs on any machine with Python
- **Full Privacy** — Your data stays on your machine. Period.

## Architecture

```
NAGRO 4.1 — Fully Self-Built AI Platform (200K Context)
│
├── Core Engine
│   ├── Task Classifier        → Understands user intent automatically
│   ├── Agent Router           → Routes to specialized agents
│   ├── Pipeline Orchestrator  → Manages the full request lifecycle
│   ├── Prompt Optimizer       → Auto-enhances prompts per task type
│   └── Context Optimizer      → Smart context compression for 200K window
│
├── Advanced Reasoning Systems
│   ├── Chain-of-Thought       → Step-by-step logical reasoning
│   ├── Tree-of-Thought        → Explores multiple solution paths
│   ├── Multi-Perspective      → Analyzes from different angles
│   ├── Internal Debate        → Advocate vs Critic vs Judge
│   ├── Self-Reflection        → Evaluates and improves own outputs
│   └── Task Planner           → Decomposes complex tasks into steps
│
├── Agentic Loop (ReAct Pattern)
│   ├── Think → Act → Observe → Repeat
│   ├── Tool Use (search, calculate, code_run, analyze)
│   └── Autonomous multi-step task execution
│
├── RAG Pipeline (Self-Built)
│   ├── Document Chunking      → Splits docs into searchable pieces
│   ├── Local Embeddings       → Self-built TF-IDF vectors
│   ├── Vector Store           → Custom cosine-similarity search
│   └── Context Retrieval      → Augments prompts with relevant info
│
├── Persistent Memory (SQLite)
│   ├── Conversations          → Save/load full conversations
│   ├── Memories               → Remember/recall/forget user facts
│   ├── Learned Facts          → Auto-learns from interactions
│   └── User Preferences       → Persists settings across sessions
│
├── Specialized Agents
│   ├── Reasoning Agent        → Chat, logic, analysis
│   ├── Coding Agent           → Code generation, debugging, review
│   ├── Research Agent         → DuckDuckGo search + LLM synthesis
│   ├── Image Agent            → Procedural image engine (self-built)
│   ├── Math Agent             → Step-by-step problem solving
│   └── Creative Agent         → Writing, poetry, content
│
├── NAGRO Brain (Self-Built AI Engine)
│   ├── Custom NLP Engine      → NAGRO's own text understanding
│   ├── Web-Augmented AI       → DuckDuckGo search + synthesis
│   ├── Code Generation        → Template + AST based
│   ├── Math Solver            → Symbolic computation
│   ├── 200K context window    → Massive context support
│   └── Streaming generation   → Chunk-by-chunk output
│
├── Tools (All Self-Built)
│   ├── Web Search             → DuckDuckGo (free, no API key)
│   ├── Calculator             → Safe math expression evaluator
│   ├── Code Executor          → Sandboxed Python + JavaScript
│   ├── Code Analyzer          → AST-based complexity & security
│   └── Document Processor     → Read text, code, CSV files
│
├── Plugin System              → Extensible plugin architecture
├── Benchmark Suite            → Reasoning, coding, math, knowledge tests
├── System Monitor             → CPU, RAM, GPU, performance tracking
│
├── FastAPI Backend            → REST API + SSE streaming + WebSocket
├── Web UI                     → Modern dark-theme chat interface
└── CLI                        → Rich terminal chat interface
```

## Capabilities

| Capability | Description | External API? |
|---|---|---|
| 200K Context Window | Matches Opus 5.5 level context length | **No** |
| Chat & Reasoning | Deep chain-of-thought reasoning | **No** |
| Code Generation | Write, debug, review, optimize any language | **No** |
| Code Execution | Sandboxed Python + JavaScript (Node.js) | **No** |
| Code Analysis | AST complexity, security, issue detection | **No** |
| Image Generation | Procedural engine (self-built) | **No** |
| Web Research | DuckDuckGo + LLM synthesis | **No** |
| Mathematics | Step-by-step with verification | **No** |
| Creative Writing | Stories, poetry, content | **No** |
| Agentic Tasks | Multi-step autonomous execution | **No** |
| RAG | Document ingestion + retrieval | **No** |
| Persistent Memory | SQLite-backed cross-session memory | **No** |
| Plugin System | Extensible tool/agent architecture | **No** |
| File Upload & Analysis | Process text, code, CSV with RAG | **No** |
| Calculator | Math expression evaluation | **No** |
| Self-Reflection | Output quality improvement | **No** |
| Task Planning | Complex task decomposition | **No** |
| Prompt Optimization | Auto-enhances prompts per task type | **No** |
| Benchmarks | Test reasoning, coding, math, knowledge | **No** |
| System Monitoring | CPU, RAM, GPU, performance tracking | **No** |

## Quick Start

### 1. Clone

```bash
git clone https://github.com/Adityakumar0723/NAGRO--Neural-Adaptive-Generative-Reasoning-Operator.git
cd NAGRO--Neural-Adaptive-Generative-Reasoning-Operator
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Run (No model download needed!)

**Web UI (recommended):**
```bash
python run.py
```
Open **http://localhost:8000** and start using NAGRO 4.1!

**CLI (terminal chat):**
```bash
python cli.py
```

### Docker

```bash
docker-compose up --build
```

## Three Ways to Interact

### Web UI
Modern dark-theme chat interface at `http://localhost:8000` with capability cards, markdown rendering, code syntax highlighting, and conversation history.

### CLI
Rich terminal chat with commands:
- `/help` — Show commands
- `/clear` — Clear conversation
- `/info` — System info
- `/stats` — Memory & performance stats
- `/models` — List downloaded models
- `/analyze <file>` — Analyze a code file
- `/agent <task>` — Run agentic task
- `/exit` — Quit

### WebSocket
Real-time bidirectional chat at `ws://localhost:8000/ws/chat` for integration with custom frontends.

## API Reference

### Chat
```bash
POST /api/v1/chat
{"message": "Write a Python quicksort", "stream": false}
```

### Agentic Task (Multi-Step with Tool Use)
```bash
POST /api/v1/agent
{"task": "Research the top 3 Python web frameworks and compare them", "max_steps": 10}
```

### Ingest Document (RAG)
```bash
POST /api/v1/knowledge/ingest
{"doc_id": "my-doc", "content": "Full document text here..."}
```

### Image Generation
```bash
POST /api/v1/image/generate
{"prompt": "A cyberpunk city at night"}
```

### Code Help
```bash
POST /api/v1/code
{"prompt": "Implement a red-black tree", "language": "python", "action": "generate"}
```

### Code Execution (Python + JavaScript)
```bash
POST /api/v1/code/execute
{"code": "print('hello')", "language": "python"}
```

### Research
```bash
POST /api/v1/research
{"query": "Latest AI breakthroughs 2024"}
```

### File Upload & Analysis
```bash
POST /api/v1/files/upload       # Upload with auto-analysis + RAG ingestion
POST /api/v1/files/analyze      # Analyze file content
POST /api/v1/files/execute      # Execute code files
```

### System & Models
```bash
GET  /api/v1/health            # Health check
GET  /api/v1/info              # Engine info
GET  /api/v1/models            # Available models
GET  /api/v1/system            # System monitor (CPU, RAM, GPU)
GET  /api/v1/plugins           # Loaded plugins
GET  /api/v1/memory/stats      # Memory store statistics
GET  /api/v1/memory/conversations  # Saved conversations
POST /api/v1/benchmark         # Run benchmark suite
```

## Project Structure

```
NAGRO-AI/
├── nagro/
│   ├── core/
│   │   ├── engine.py            # Main orchestration engine
│   │   ├── inference.py         # NAGRO self-built inference engine
│   │   ├── nagro_brain.py       # NAGRO AI Brain (100% self-built)
│   │   ├── image_engine.py      # Procedural image engine (self-built)
│   │   ├── model_manager.py     # Engine status management
│   │   ├── config.py            # Configuration (200K context, no models)
│   │   ├── models.py            # Pydantic data models
│   │   ├── prompts.py           # Optimized system prompts
│   │   ├── memory_store.py      # Persistent SQLite memory
│   │   ├── context_optimizer.py # Smart context compression
│   │   ├── prompt_optimizer.py  # Auto prompt enhancement
│   │   ├── plugin_system.py     # Extensible plugin architecture
│   │   ├── system_monitor.py    # CPU/RAM/GPU/performance tracking
│   │   └── benchmarks.py        # Reasoning/coding/math benchmarks
│   ├── reasoning/
│   │   ├── chain_of_thought.py  # CoT & ToT reasoning
│   │   ├── self_reflection.py   # Output self-evaluation
│   │   └── planner.py           # Task decomposition
│   ├── rag/
│   │   ├── vector_store.py      # Self-built vector store
│   │   └── retriever.py         # Document retrieval pipeline
│   ├── agents/
│   │   ├── base.py              # Base agent (local inference)
│   │   ├── reasoning.py         # Reasoning agent
│   │   ├── coding.py            # Coding agent
│   │   ├── research.py          # Research agent
│   │   ├── image.py             # Image agent
│   │   ├── math_agent.py        # Math agent
│   │   ├── creative.py          # Creative agent
│   │   ├── agentic.py           # Agentic loop system (ReAct)
│   │   └── router.py            # Agent routing
│   └── tools/
│       ├── web_search.py        # DuckDuckGo search
│       ├── calculator.py        # Safe math evaluator
│       ├── code_executor.py     # Multi-language sandbox (Python + JS)
│       ├── code_analyzer.py     # AST complexity & security analysis
│       └── document_processor.py # File processing
├── api/
│   ├── main.py                  # FastAPI app with all routes
│   ├── routes/
│   │   ├── chat.py              # Chat & agentic endpoints
│   │   ├── image.py             # Image generation
│   │   ├── code.py              # Code generation & execution
│   │   ├── research.py          # Research endpoint
│   │   ├── files.py             # File upload & analysis
│   │   └── websocket.py         # WebSocket streaming
│   └── middleware/
│       └── auth.py              # Optional API key auth
├── web/
│   ├── index.html               # Main UI page
│   ├── css/style.css            # Dark theme styles
│   └── js/app.js                # Chat application
├── plugins/                     # Custom plugins directory
├── tests/                       # Test suite
├── cli.py                       # Rich terminal chat interface
├── download_model.py            # Status check (no download needed)
├── run.py                       # Launch script
├── Dockerfile                   # Container support
├── docker-compose.yml           # Docker orchestration
└── requirements.txt             # Dependencies (zero AI model packages)
```

## Configuration

All settings via `.env` file (copy `.env.example`):

```env
# Context & Generation — 200K context (Opus 5.5 level)
NAGRO_CONTEXT_LENGTH=200000
NAGRO_MAX_TOKENS=16384
NAGRO_BATCH_SIZE=512
NAGRO_TEMPERATURE=0.7
NAGRO_TOP_P=0.9
NAGRO_TOP_K=40
NAGRO_REPEAT_PENALTY=1.1

# GPU Acceleration
NAGRO_GPU_LAYERS=35   # Offload model layers to GPU (0 = CPU only)
NAGRO_THREADS=4

# Image Generation
NAGRO_IMAGE_STEPS=4
NAGRO_IMAGE_WIDTH=1024
NAGRO_IMAGE_HEIGHT=1024
```

## Plugin System

Drop Python files into the `plugins/` directory. Each plugin can register tools and hooks:

```python
# plugins/my_plugin.py
PLUGIN_NAME = "my_plugin"
PLUGIN_DESCRIPTION = "My custom plugin"
PLUGIN_VERSION = "1.0.0"

TOOLS = {
    "my_tool": {
        "description": "What my tool does",
        "handler": lambda args: {"result": "done"},
    }
}

HOOKS = {
    "on_message": lambda msg: print(f"Got: {msg}"),
}
```

## Benchmark Suite

Test NAGRO's capabilities across 12 benchmarks:

```bash
curl -X POST http://localhost:8000/api/v1/benchmark
```

Tests reasoning, coding, mathematics, and knowledge tasks, producing a comprehensive score report.

## Running Tests

```bash
pytest tests/ -v
```

## What Makes NAGRO Different

| | NAGRO 4.1 | ChatGPT Wrappers | Other "AI Tools" |
|---|---|---|---|
| AI Engine | **100% self-built** | External model | External model |
| External AI models | **ZERO** | GPT/Claude/Gemini | Various |
| PyTorch/Transformers | **Not needed** | Required | Required |
| GPU needed | **No** | Yes | Usually |
| Runs locally | **Yes** | No | Sometimes |
| API keys needed | **None** | Yes | Yes |
| Data privacy | **100% local** | Cloud | Cloud |
| Cost | **Free forever** | Pay per token | Subscription |
| Advanced reasoning | **CoT + ToT + Reflection** | Basic | Basic |
| Agentic tasks | **Yes (ReAct)** | No | Some |
| RAG pipeline | **Self-built TF-IDF** | No | External |
| Persistent memory | **SQLite** | Session only | Cloud |
| Image generation | **Procedural (self-built)** | API call | API call |
| Code execution | **Python + JS** | API-dependent | API-dependent |
| Docker deploy | **Instant (no build issues)** | Complex | Complex |
| Open source | **Fully** | No | Partially |

## Contributing

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push and open a PR

## License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

**NAGRO 4.1** — 100% Self-Built AI. Zero External Models. Zero APIs. NAGRO's Own Brain. Your Machine.

Built by [Aditya Kumar](https://github.com/Adityakumar0723)

*Neural Adaptive Generative Reasoning Operator*

</div>
