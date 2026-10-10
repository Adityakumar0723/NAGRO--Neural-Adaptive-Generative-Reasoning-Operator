#!/usr/bin/env python3
"""
NAGRO 4.1 — Model Downloader
Downloads open-source LLM models to run locally.
No API keys needed. Everything runs on YOUR machine.
NAGRO's own inference engine. 200K context window.
"""

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


def main():
    console.print("\n[bold cyan]NAGRO 4.1 — Model Downloader[/bold cyan]")
    console.print("[dim]Download free, open-source AI models to run locally.[/dim]")
    console.print("[dim]NAGRO's own inference engine. No compilation. No APIs.[/dim]\n")

    from nagro.core.model_manager import (
        RECOMMENDED_MODELS, download_model, list_available_models
    )

    downloaded = list_available_models()
    if downloaded:
        console.print("[green]Already downloaded:[/green]")
        for m in downloaded:
            console.print(f"  [green]✓[/green] {m['name']}")
        console.print()

    table = Table(title="Available Models (128K Native Context)", show_header=True)
    table.add_column("Key", style="cyan", width=10)
    table.add_column("Model", style="white", width=50)
    table.add_column("Size", style="yellow", width=10)
    table.add_column("RAM", style="green", width=8)
    table.add_column("Context", style="magenta", width=8)

    for key, info in RECOMMENDED_MODELS.items():
        table.add_row(key, info["name"], info["size"], info["ram"], info["context"])

    console.print(table)
    console.print()
    console.print("[dim]Recommendations:[/dim]")
    console.print("  • [cyan]tiny[/cyan]      — Minimal RAM, quick responses")
    console.print("  • [cyan]small[/cyan]     — Best balance for most users (default)")
    console.print("  • [cyan]coder[/cyan]     — Optimized for programming tasks")
    console.print("  • [cyan]reasoning[/cyan] — Maximum quality (needs 16GB RAM)")
    console.print()

    choice = Prompt.ask(
        "Which model to download?",
        choices=list(RECOMMENDED_MODELS.keys()),
        default="small",
    )

    console.print()
    model_id = download_model(choice)

    console.print(f"\n[bold green]Done![/bold green]")
    console.print(f"Model ready: [cyan]{model_id}[/cyan]")
    console.print(f"\nUpdate your [cyan].env[/cyan] file:")
    console.print(f"  NAGRO_LLM_MODEL={model_id}")
    console.print(f"\nThen start NAGRO:")
    console.print(f"  [cyan]python run.py[/cyan]        — Web UI at http://localhost:8000")
    console.print(f"  [cyan]python cli.py[/cyan]        — Terminal chat interface\n")


if __name__ == "__main__":
    main()
