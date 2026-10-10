"""NAGRO 4.1 — Launch Script. Fully self-built, no external APIs."""

import uvicorn
from nagro.core.config import settings


def main():
    uvicorn.run(
        "api.main:app",
        host=settings.nagro_host,
        port=settings.nagro_port,
        reload=settings.nagro_debug,
    )


if __name__ == "__main__":
    main()
