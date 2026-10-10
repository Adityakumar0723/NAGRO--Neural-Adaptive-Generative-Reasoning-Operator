<div align="center">

# NAGRO 4.1

### Neural Adaptive Generative Reasoning Operator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Self Built](https://img.shields.io/badge/100%25-Self--Built-purple?style=for-the-badge)]()
[![No APIs](https://img.shields.io/badge/External_APIs-ZERO-red?style=for-the-badge)]()

**A powerful, fully self-built AI platform with advanced reasoning, agentic task execution, RAG, and multi-modal capabilities.**

**No OpenAI. No Anthropic. No Google. No API keys. Everything runs on YOUR machine.**

Built by [Aditya Kumar](https://github.com/Adityakumar0723)

---

</div>

## Why NAGRO?

Most "AI products" are just thin wrappers around someone else's API. **NAGRO 4.1 is built from the ground up.**

- **100% Self-Built** — Every component runs locally on your machine
- **Zero External APIs** — No data ever leaves your system
- **No API Keys** — Download, run, done. Free forever
- **Advanced Reasoning** — Chain-of-thought, tree-of-thought, self-reflection, internal debate
- **Agentic System** — Multi-step autonomous task execution with tool use
- **RAG Pipeline** — Ingest documents and retrieve context for smarter answers
- **Local Image Generation** — Stable Diffusion on your GPU/CPU
- **Free Web Search** — DuckDuckGo, no API key needed
- **Full Privacy** — Your data stays on your machine. Period.

## Architecture

```
NAGRO 4.1 — Fully Self-Built AI Platform
│
├── Core Engine
│   ├── Task Classifier        → Understands user intent automatically
│   ├── Agent Router           → Routes to specialized agents
│   └── Pipeline Orchestrator  → Manages the full request lifecycle
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
│   ├── Local Embeddings       → sentence-transformers (MiniLM)
│   ├── Vector Store           → Custom cosine-similarity search
│   └── Context Retrieval      → Augments prompts with relevant info
│
├── Specialized Agents
│   ├── Reasoning Agent        → Chat, logic, analysis
│   ├── Coding Agent           → Code generation, debugging, review
│   ├── Research Agent         → DuckDuckGo search + LLM synthesis
│   ├── Image Agent            → Local Stable Diffusion (SDXL Turbo)
│   ├── Math Agent             → Step-by-step problem solving
│   └── Creative Agent         → Writing, poetry, content
│
├── Local Inference Engine
│   ├── llama.cpp backend      → Runs GGUF models efficiently
│   ├── CPU + GPU support      → Works on any hardware
│   └── Streaming generation   → Token-by-token output
│
├── Tools (All Self-Built)
│   ├── Web Search             → DuckDuckGo (free, no API key)
│   ├── Calculator             → Safe math expression evaluator
│   ├── Code Executor          → Sandboxed Python execution
│   └── Document Processor     → Read text, code, CSV files
│
├── FastAPI Backend            → REST API + SSE streaming
└── Web UI                     → Modern dark-theme chat interface
```

## Capabilities

| Capability | Description | External API? |
|---|---|---|
| Chat & Reasoning | Deep chain-of-thought reasoning | **No** |
| Code Generation | Write, debug, review, optimize any language | **No** |
| Image Generation | Stable Diffusion SDXL locally | **No** |
| Web Research | DuckDuckGo + LLM synthesis | **No** |
| Mathematics | Step-by-step with verification | **No** |
| Creative Writing | Stories, poetry, content | **No** |
| Agentic Tasks | Multi-step autonomous execution | **No** |
| RAG | Document ingestion + retrieval | **No** |
| Code Execution | Safe Python sandbox | **No** |
| Calculator | Math expression evaluation | **No** |
| Self-Reflection | Output quality improvement | **No** |
| Task Planning | Complex task decomposition | **No** |

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

### 3. Download a Model (~4 GB, one-time)

```bash
python download_model.py
```

| Size | Model | Download | RAM |
|---|---|---|---|
| **small** | Phi-3 Mini 3.8B | ~2.4 GB | 4 GB |
| **medium** | Mistral 7B Instruct | ~4.4 GB | 8 GB |
| **large** | LLaMA 3.1 8B | ~4.9 GB | 8 GB |
| **xl** | Qwen2.5 14B | ~8.7 GB | 16 GB |

### 4. Run

```bash
python run.py
```

Open **http://localhost:8000** and start using NAGRO 4.1!

### Optional: Image Generation

```bash
pip install torch diffusers transformers accelerate
```

### Docker

```bash
docker-compose up --build
```

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

### Research
```bash
POST /api/v1/research
{"query": "Latest AI breakthroughs 2024"}
```

### Models
```bash
GET /api/v1/models
GET /api/v1/health
GET /api/v1/info
```

## Project Structure

```
NAGRO-AI/
├── nagro/
│   ├── core/
│   │   ├── engine.py            # Main orchestration engine
│   │   ├── inference.py         # Local LLM inference (llama.cpp)
│   │   ├── image_engine.py      # Local Stable Diffusion
│   │   ├── model_manager.py     # Model download & management
│   │   ├── config.py            # Configuration
│   │   ├── models.py            # Data models
│   │   └── prompts.py           # Optimized system prompts
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
│   │   ├── agentic.py           # Agentic loop system
│   │   └── router.py            # Agent routing
│   ├── memory/                  # Conversation context
│   └── tools/
│       ├── web_search.py        # DuckDuckGo search
│       ├── calculator.py        # Safe math evaluator
│       ├── code_executor.py     # Python sandbox
│       └── document_processor.py # File processing
├── api/                         # FastAPI backend
├── web/                         # Frontend UI
├── tests/                       # Test suite
├── download_model.py            # Model downloader
├── run.py                       # Launch script
└── requirements.txt             # Dependencies
```

## GPU Acceleration

```env
NAGRO_GPU_LAYERS=35   # Offload model layers to GPU
```

For image generation, CUDA-enabled PyTorch uses GPU automatically.

## Running Tests

```bash
pytest tests/ -v
```

## What Makes NAGRO Different

| | NAGRO 4.1 | ChatGPT Wrappers | Other "AI Tools" |
|---|---|---|---|
| Runs locally | Yes | No | Sometimes |
| API keys needed | **None** | Yes | Yes |
| Data privacy | **100% local** | Cloud | Cloud |
| Cost | **Free forever** | Pay per token | Subscription |
| Advanced reasoning | **CoT + ToT + Reflection** | Basic | Basic |
| Agentic tasks | **Yes (ReAct)** | No | Some |
| RAG pipeline | **Built-in** | No | External |
| Image generation | **Local SD** | API call | API call |
| Tool use | **Self-built** | API-dependent | API-dependent |
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

**NAGRO 4.1** — 100% Self-Built. Zero External APIs. Advanced Reasoning. Your AI, Your Machine.

Built by [Aditya Kumar](https://github.com/Adityakumar0723)

*Neural Adaptive Generative Reasoning Operator*

</div>
