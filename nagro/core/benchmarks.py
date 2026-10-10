"""
NAGRO 4.1 — Self-Built Benchmark Suite.

Tests model performance across reasoning, coding, math, and knowledge tasks.
Run: python -m nagro.core.benchmarks
"""

from __future__ import annotations
import time
from dataclasses import dataclass, field


@dataclass
class BenchmarkResult:
    name: str
    category: str
    passed: bool
    score: float
    time_seconds: float
    expected: str = ""
    actual: str = ""


BENCHMARK_SUITE = {
    "reasoning": [
        {
            "name": "Logical Deduction",
            "prompt": "If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly? Explain your reasoning.",
            "check": lambda r: "cannot conclude" in r.lower() or "not necessarily" in r.lower() or "no" in r.lower()[:50],
        },
        {
            "name": "Causal Reasoning",
            "prompt": "A rooster crows before sunrise every day. Does the rooster cause the sun to rise? Explain why or why not.",
            "check": lambda r: "correlation" in r.lower() or "does not cause" in r.lower() or "no" in r.lower()[:20],
        },
        {
            "name": "Analogical Reasoning",
            "prompt": "Complete the analogy: Book is to Reading as Fork is to ___. Explain your reasoning.",
            "check": lambda r: "eating" in r.lower(),
        },
    ],
    "coding": [
        {
            "name": "FizzBuzz",
            "prompt": "Write a Python function fizzbuzz(n) that returns 'Fizz' for multiples of 3, 'Buzz' for 5, 'FizzBuzz' for both, else the number as string.",
            "check": lambda r: "def fizzbuzz" in r and ("Fizz" in r) and ("Buzz" in r),
        },
        {
            "name": "Reverse String",
            "prompt": "Write a Python function to reverse a string without using slicing or built-in reverse.",
            "check": lambda r: "def " in r and ("for" in r or "while" in r),
        },
        {
            "name": "Binary Search",
            "prompt": "Implement binary search in Python that returns the index of target or -1.",
            "check": lambda r: "def " in r and "mid" in r and ("low" in r or "left" in r),
        },
    ],
    "math": [
        {
            "name": "Basic Algebra",
            "prompt": "Solve for x: 3x + 7 = 22. Show your work.",
            "check": lambda r: "5" in r,
        },
        {
            "name": "Quadratic",
            "prompt": "Solve: x^2 - 5x + 6 = 0. Show your work.",
            "check": lambda r: "2" in r and "3" in r,
        },
        {
            "name": "Percentage",
            "prompt": "What is 15% of 240? Show calculation.",
            "check": lambda r: "36" in r,
        },
    ],
    "knowledge": [
        {
            "name": "Science",
            "prompt": "What is the chemical formula for water?",
            "check": lambda r: "h2o" in r.lower(),
        },
        {
            "name": "Geography",
            "prompt": "What is the capital of France?",
            "check": lambda r: "paris" in r.lower(),
        },
        {
            "name": "Computing",
            "prompt": "What does CPU stand for?",
            "check": lambda r: "central processing unit" in r.lower(),
        },
    ],
}


async def run_benchmarks(engine) -> dict:
    """Run the full benchmark suite against the NAGRO engine."""
    from nagro.core.models import ChatRequest

    results: list[BenchmarkResult] = []
    total_time = 0.0

    for category, tests in BENCHMARK_SUITE.items():
        for test in tests:
            start = time.time()
            try:
                request = ChatRequest(message=test["prompt"])
                response = await engine.process(request)
                actual = response.message
                elapsed = time.time() - start
                passed = test["check"](actual)

                results.append(BenchmarkResult(
                    name=test["name"],
                    category=category,
                    passed=passed,
                    score=1.0 if passed else 0.0,
                    time_seconds=round(elapsed, 3),
                    expected="Pass check function",
                    actual=actual[:200],
                ))
            except Exception as e:
                elapsed = time.time() - start
                results.append(BenchmarkResult(
                    name=test["name"],
                    category=category,
                    passed=False,
                    score=0.0,
                    time_seconds=round(elapsed, 3),
                    actual=str(e),
                ))
            total_time += elapsed

    # Calculate scores
    by_category = {}
    for r in results:
        by_category.setdefault(r.category, []).append(r)

    category_scores = {}
    for cat, cat_results in by_category.items():
        passed = sum(1 for r in cat_results if r.passed)
        total = len(cat_results)
        category_scores[cat] = {
            "passed": passed,
            "total": total,
            "score": round(passed / total * 100, 1),
        }

    total_passed = sum(1 for r in results if r.passed)
    total_tests = len(results)

    return {
        "model": "NAGRO 4.1",
        "overall_score": round(total_passed / total_tests * 100, 1),
        "passed": total_passed,
        "total": total_tests,
        "total_time": round(total_time, 2),
        "categories": category_scores,
        "results": [
            {
                "name": r.name,
                "category": r.category,
                "passed": r.passed,
                "time": r.time_seconds,
            }
            for r in results
        ],
    }
