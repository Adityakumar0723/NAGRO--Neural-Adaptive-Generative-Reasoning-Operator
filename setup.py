"""NAGRO 4.1 — Setup configuration. Fully self-built, zero external APIs."""

from setuptools import setup, find_packages

setup(
    name="nagro",
    version="4.1.0",
    author="Aditya Kumar",
    author_email="aditya@schoolhack.ai",
    description="NAGRO 4.1 — Neural Adaptive Generative Reasoning Operator. Fully self-built, no external APIs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Adityakumar0723/NAGRO--Neural-Adaptive-Generative-Reasoning-Operator",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.115.0",
        "uvicorn[standard]>=0.34.0",
        "pydantic>=2.10.0",
        "pydantic-settings>=2.7.0",
        "python-dotenv>=1.0.0",
        "transformers>=4.47.0",
        "torch>=2.1.0",
        "accelerate>=1.2.0",
        "safetensors>=0.4.0",
        "huggingface-hub>=0.27.0",
        "sentencepiece>=0.2.0",
        "httpx>=0.28.0",
        "duckduckgo-search>=7.0.0",
        "beautifulsoup4>=4.12.0",
        "rich>=13.9.0",
        "aiofiles>=24.1.0",
        "sse-starlette>=2.2.0",
        "psutil>=6.1.0",
    ],
    extras_require={
        "image": [
            "diffusers>=0.31.0",
            "torchvision>=0.16.0",
            "Pillow>=11.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
