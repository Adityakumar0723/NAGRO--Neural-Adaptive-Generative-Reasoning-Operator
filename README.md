<div align="center">

# NAGRO 4.1

### Neural Adaptive Generative Reasoning Operator

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Version](https://img.shields.io/badge/Version-4.1.0-purple?style=for-the-badge)]()

**A powerful multi-modal AI platform for reasoning, coding, research, image generation, and more.**

Built by [Aditya Kumar](https://github.com/Adityakumar0723)

---

</div>

## What is NAGRO?

**NAGRO 4.1** (Neural Adaptive Generative Reasoning Operator) is an advanced AI platform that combines multiple specialized AI agents into a single, unified system. It automatically understands your intent and routes your request to the best-suited agent for optimal results.

### Key Capabilities

| Capability | Description |
|---|---|
| **Chat & Reasoning** | Multi-step logical reasoning with chain-of-thought analysis |
| **Code Generation** | Write, debug, review, and optimize code in any language |
| **Image Generation** | Create images via DALL-E 3, Stable Diffusion, or Replicate |
| **Deep Research** | Web search with source synthesis and fact-checking |
| **Mathematics** | Step-by-step problem solving, calculus, algebra, statistics |
| **Creative Writing** | Stories, poetry, content, scripts, and more |

## Architecture

```
NAGRO 4.1
├── Core Engine          → Task classification & orchestration
├── Agent Router         → Routes to specialized agents
├── Agents
│   ├── Reasoning Agent  → General chat & logical reasoning
│   ├── Coding Agent     → Code generation, debugging, review
│   ├── Research Agent   → Web search & information synthesis
│   ├── Image Agent      → Image generation (DALL-E, SD, Replicate)
│   ├── Math Agent       → Mathematical problem solving
│   └── Creative Agent   → Creative writing & content
├── Memory Manager       → Conversation context & history
├── Tools
│   ├── Web Search       → Google Search via Serper API
│   ├── Code Executor    → Safe Python code execution
│   └── File Handler     → File processing utilities
├── FastAPI Backend      → REST API with streaming support
└── Web UI               → Modern dark-theme chat interface
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Adityakumar0723/NAGRO--Neural-Adaptive-Generative-Reasoning-Operator.git
cd NAGRO--Neural-Adaptive-Generative-Reasoning-Operator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Run NAGRO

```bash
python run.py
```

Open your browser at **http://localhost:8000** to start using NAGRO 4.1!

### Docker (Alternative)

```bash
docker-compose up --build
```

## API Reference

### Chat

```bash
POST /api/v1/chat
{
    "message": "Write a Python quicksort function",
    "stream": false
}
```

### Image Generation

```bash
POST /api/v1/image/generate
{
    "prompt": "A futuristic city at night with neon lights",
    "size": "1024x1024"
}
```

### Code Assistance

```bash
POST /api/v1/code
{
    "prompt": "Sort a linked list",
    "language": "python",
    "action": "generate"
}
```

### Research

```bash
POST /api/v1/research
{
    "query": "Latest AI developments in 2024",
    "depth": "deep"
}
```

### Health Check

```bash
GET /api/v1/health
→ {"status": "operational", "model": "NAGRO 4.1", "version": "4.1.0"}
```

## Supported LLM Providers

| Provider | Models | Setup |
|---|---|---|
| **Anthropic** | Claude Sonnet 4 | `ANTHROPIC_API_KEY` |
| **OpenAI** | GPT-4o, DALL-E 3 | `OPENAI_API_KEY` |
| **Groq** | LLaMA 3.3 70B | `GROQ_API_KEY` |

## Supported Image Providers

| Provider | Models | Setup |
|---|---|---|
| **OpenAI** | DALL-E 3 | `OPENAI_API_KEY` |
| **Stability AI** | SDXL 1.0 | `STABILITY_API_KEY` |
| **Replicate** | SDXL | `REPLICATE_API_KEY` |

## Project Structure

```
NAGRO-AI/
├── nagro/                  # Core NAGRO engine
│   ├── core/               # Engine, config, models, prompts
│   ├── agents/             # Specialized AI agents
│   ├── memory/             # Context & conversation management
│   ├── tools/              # Web search, code execution
│   └── utils/              # Helper utilities
├── api/                    # FastAPI backend
│   ├── routes/             # API endpoints
│   └── middleware/         # Auth middleware
├── web/                    # Frontend UI
│   ├── index.html          # Main page
│   ├── css/style.css       # Styling
│   └── js/app.js           # Frontend logic
├── tests/                  # Test suite
├── run.py                  # Launch script
├── requirements.txt        # Dependencies
├── Dockerfile              # Container config
└── docker-compose.yml      # Docker Compose
```

## Running Tests

```bash
pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**NAGRO 4.1** — Built with purpose by [Aditya Kumar](https://github.com/Adityakumar0723)

*Neural Adaptive Generative Reasoning Operator*

</div>
