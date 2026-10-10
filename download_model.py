#!/usr/bin/env python3
"""
NAGRO 4.1 — Self-Built AI Platform

No model downloads needed! NAGRO uses its own self-built engine.
No PyTorch. No Transformers. No external AI models.
"""

from rich.console import Console
from rich.panel import Panel

console = Console()


def main():
    console.print()
    console.print(Panel(
        "[bold cyan]NAGRO 4.1[/bold cyan]\n"
        "[dim]Neural Adaptive Generative Reasoning Operator[/dim]\n\n"
        "[green]No model download needed![/green]\n\n"
        "NAGRO uses its own [bold]self-built AI engine[/bold]:\n"
        "• NAGRO Brain — Custom NLP + reasoning\n"
        "• Web Search — DuckDuckGo (free, no API key)\n"
        "• Code Engine — Template + AST based\n"
        "• Math Solver — Symbolic computation\n"
        "• Image Engine — Procedural generation\n"
        "• RAG System — TF-IDF based retrieval\n\n"
        "[bold]No PyTorch. No Transformers. No external models.[/bold]\n"
        "[bold]100% self-built. Zero borrowed intelligence.[/bold]",
        title="[bold white]Ready to Use[/bold white]",
        border_style="cyan",
        padding=(1, 4),
    ))
    console.print()
    console.print("Start NAGRO:")
    console.print("  [cyan]python run.py[/cyan]    — Web UI at http://localhost:8000")
    console.print("  [cyan]python cli.py[/cyan]    — Terminal chat interface")
    console.print()


if __name__ == "__main__":
    main()
