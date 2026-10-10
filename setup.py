"""NAGRO 4.1 - Setup configuration."""

from setuptools import setup, find_packages

setup(
    name="nagro",
    version="4.1.0",
    author="Aditya Kumar",
    author_email="aditya@schoolhack.ai",
    description="NAGRO 4.1 - Neural Adaptive Generative Reasoning Operator",
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
        "anthropic>=0.40.0",
        "openai>=1.58.0",
        "httpx>=0.28.0",
        "sse-starlette>=2.2.0",
        "aiofiles>=24.1.0",
        "rich>=13.9.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
