"""NAGRO 4.1 - Launch Script."""

import uvicorn
from nagro.core.config import settings


def main():
    print(r"""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║     ███╗   ██╗ █████╗  ██████╗ ██████╗  ██████╗  ║
    ║     ████╗  ██║██╔══██╗██╔════╝ ██╔══██╗██╔═══██╗ ║
    ║     ██╔██╗ ██║███████║██║  ███╗██████╔╝██║   ██║ ║
    ║     ██║╚██╗██║██╔══██║██║   ██║██╔══██╗██║   ██║ ║
    ║     ██║ ╚████║██║  ██║╚██████╔╝██║  ██║╚██████╔╝ ║
    ║     ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ║
    ║                                              ║
    ║     Version 4.1 — Neural Adaptive Generative ║
    ║     Reasoning Operator                       ║
    ║     Built by Aditya Kumar                    ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
    """)

    uvicorn.run(
        "api.main:app",
        host=settings.nagro_host,
        port=settings.nagro_port,
        reload=settings.nagro_debug,
    )


if __name__ == "__main__":
    main()
