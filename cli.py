#!/usr/bin/env python3
"""
NAGRO 4.1 — Command Line Interface.

Full-featured terminal chat interface with streaming, colors, and history.
Run: python cli.py
"""

import asyncio
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from nagro.core.config import settings
from nagro.core.engine import NAGROEngine
from nagro.core.models import ChatRequest
from nagro.core.model_manager import is_model_downloaded, RECOMMENDED_MODELS

console = Console()


def print_banner():
    console.print()
    console.print(Panel(
        "[bold cyan]NAGRO 4.1[/bold cyan]\n"
        "[dim]Neural Adaptive Generative Reasoning Operator[/dim]\n\n"
        "[green]100% Self-Built | Zero External APIs | Local Inference[/green]",
        title="[bold white]Welcome[/bold white]",
        border_style="cyan",
        padding=(1, 4),
    ))
    console.print()


def print_help():
    console.print(Panel(
        "[cyan]/help[/cyan]     — Show this help\n"
        "[cyan]/clear[/cyan]    — Clear conversation\n"
        "[cyan]/info[/cyan]     — Show model info\n"
        "[cyan]/stats[/cyan]    — Show system stats\n"
        "[cyan]/models[/cyan]   — List available models\n"
        "[cyan]/analyze[/cyan]  — Analyze code (paste after)\n"
        "[cyan]/agent[/cyan]    — Run agentic task\n"
        "[cyan]/exit[/cyan]     — Exit NAGRO\n",
        title="Commands",
        border_style="cyan",
    ))


async def main():
    print_banner()

    if not is_model_downloaded():
        console.print("[yellow]No model found![/yellow]")
        console.print("Run: [cyan]python download_model.py[/cyan] to download a model.\n")
        console.print("Available models:")
        for key, info in RECOMMENDED_MODELS.items():
            console.print(f"  [cyan]{key:8}[/cyan] — {info['name']} ({info['size']})")
        console.print()

    engine = NAGROEngine()
    conversation_id = None

    console.print("[dim]Type your message and press Enter. Type /help for commands.[/dim]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold green]You[/bold green]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break

        user_input = user_input.strip()
        if not user_input:
            continue

        # Handle commands
        if user_input.startswith("/"):
            cmd = user_input.lower().split()[0]

            if cmd == "/exit" or cmd == "/quit":
                console.print("[dim]Goodbye![/dim]")
                break

            elif cmd == "/help":
                print_help()
                continue

            elif cmd == "/clear":
                if conversation_id:
                    engine.clear_conversation(conversation_id)
                conversation_id = None
                console.clear()
                print_banner()
                console.print("[dim]Conversation cleared.[/dim]\n")
                continue

            elif cmd == "/info":
                info = engine.info
                console.print(Panel(
                    f"[cyan]Model:[/cyan] {info['model']}\n"
                    f"[cyan]Version:[/cyan] {info['version']}\n"
                    f"[cyan]Architecture:[/cyan] {info['architecture']}\n"
                    f"[cyan]Inference:[/cyan] {info['inference']}\n"
                    f"[cyan]LLM Model:[/cyan] {info['llm_model']}\n"
                    f"[cyan]Model Downloaded:[/cyan] {info['model_downloaded']}\n"
                    f"[cyan]Model Loaded:[/cyan] {info['model_loaded']}\n"
                    f"[cyan]External APIs:[/cyan] {info['external_apis']}\n"
                    f"[cyan]Capabilities:[/cyan] {len(info['capabilities'])}\n"
                    f"[cyan]Reasoning Systems:[/cyan] {len(info.get('reasoning_systems', []))}",
                    title="NAGRO 4.1 Info",
                    border_style="cyan",
                ))
                continue

            elif cmd == "/stats":
                from nagro.core.system_monitor import SystemMonitor
                monitor = SystemMonitor()
                sys_info = monitor.get_system_info()
                console.print(Panel(
                    f"[cyan]Platform:[/cyan] {sys_info['platform']}\n"
                    f"[cyan]Python:[/cyan] {sys_info['python_version']}\n"
                    f"[cyan]CPU Cores:[/cyan] {sys_info['cpu_cores']}\n"
                    f"[cyan]GPU:[/cyan] {sys_info['gpu'].get('name', 'Not available')}",
                    title="System Info",
                    border_style="cyan",
                ))
                continue

            elif cmd == "/models":
                from nagro.core.model_manager import list_available_models
                downloaded = list_available_models()
                if downloaded:
                    console.print("[green]Downloaded models:[/green]")
                    for m in downloaded:
                        console.print(f"  • {m['name']} ({m['size_mb']} MB)")
                else:
                    console.print("[yellow]No models downloaded.[/yellow]")
                console.print(f"\n[dim]Active: {settings.nagro_llm_model}[/dim]")
                continue

            elif cmd == "/agent":
                task = user_input[6:].strip()
                if not task:
                    task = Prompt.ask("[bold yellow]Task[/bold yellow]")
                console.print("[dim]Running agentic task...[/dim]")
                result = await engine.process_agentic(task)
                console.print(Panel(
                    Markdown(result.get("answer", "No answer")),
                    title=f"Agent Result ({result.get('total_steps', 0)} steps)",
                    border_style="magenta",
                ))
                continue

            elif cmd == "/analyze":
                code = user_input[8:].strip()
                if not code:
                    console.print("[dim]Paste code to analyze (Ctrl+D or empty line to finish):[/dim]")
                    lines = []
                    while True:
                        try:
                            line = input()
                            if not line and lines:
                                break
                            lines.append(line)
                        except EOFError:
                            break
                    code = "\n".join(lines)

                from nagro.tools.code_analyzer import CodeAnalyzer
                analyzer = CodeAnalyzer()
                analysis = analyzer.analyze_any(code)
                console.print(Panel(
                    f"[cyan]Language:[/cyan] {analysis.language}\n"
                    f"[cyan]Lines:[/cyan] {analysis.lines_of_code}\n"
                    f"[cyan]Functions:[/cyan] {', '.join(analysis.functions) or 'None'}\n"
                    f"[cyan]Classes:[/cyan] {', '.join(analysis.classes) or 'None'}\n"
                    f"[cyan]Complexity:[/cyan] {analysis.complexity}\n"
                    f"[cyan]Issues:[/cyan] {len(analysis.issues)}\n"
                    + ("\n".join(f"  [red]• {i}[/red]" for i in analysis.issues) if analysis.issues else "")
                    + ("\n" + "\n".join(f"  [yellow]• {s}[/yellow]" for s in analysis.suggestions) if analysis.suggestions else ""),
                    title="Code Analysis",
                    border_style="cyan",
                ))
                continue

            else:
                console.print(f"[dim]Unknown command: {cmd}. Type /help for commands.[/dim]")
                continue

        # Process message
        with console.status("[bold cyan]NAGRO 4.1 is thinking...[/bold cyan]"):
            request = ChatRequest(
                message=user_input,
                conversation_id=conversation_id,
                stream=False,
            )
            response = await engine.process(request)

        conversation_id = response.conversation_id

        console.print()
        console.print(Panel(
            Markdown(response.message),
            title=f"[bold cyan]NAGRO 4.1[/bold cyan] [dim]({response.task_type.value} • {response.processing_time}s)[/dim]",
            border_style="cyan",
            padding=(1, 2),
        ))
        console.print()


if __name__ == "__main__":
    asyncio.run(main())
