#!/usr/bin/env python3
"""
NAGRO 4.1 — Model Downloader
Downloads open-source LLM models to run locally.
No API keys needed. Everything runs on YOUR machine.
"""

import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()


def main():
    console.print("\n[bold cyan]NAGRO 4.1 — Model Downloader[/bold cyan]")
    console.print("[dim]Download free, open-source AI models to run locally.[/dim]\n")

    from nagro.core.model_manager import (
        RECOMMENDED_MODELS, download_model, list_available_models, ensure_models_dir
    )

    ensure_models_dir()

    # Show downloaded models
    downloaded = list_available_models()
    if downloaded:
        console.print("[green]Already downloaded:[/green]")
        for m in downloaded:
            console.print(f"  • {m['name']} ({m['size_mb']} MB)")
        console.print()

    # Show available models
    table = Table(title="Available Models", show_header=True)
    table.add_column("Key", style="cyan", width=8)
    table.add_column("Model", style="white", width=40)
    table.add_column("Size", style="yellow", width=10)
    table.add_column("RAM Needed", style="green", width=10)

    for key, info in RECOMMENDED_MODELS.items():
        table.add_row(key, info["name"], info["size"], info["ram"])

    console.print(table)
    console.print()

    choice = Prompt.ask(
        "Which model to download?",
        choices=list(RECOMMENDED_MODELS.keys()),
        default="medium",
    )

    console.print()
    path = download_model(choice)

    console.print(f"\n[bold green]Done![/bold green]")
    console.print(f"Model saved to: [cyan]{path}[/cyan]")
    console.print(f"\nUpdate your [cyan].env[/cyan] file:")
    console.print(f"  NAGRO_LLM_MODEL={path.name}")
    console.print(f"\nThen start NAGRO:")
    console.print(f"  [cyan]python run.py[/cyan]\n")


if __name__ == "__main__":
    main()
