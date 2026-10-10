"""
NAGRO 4.1 — Code Analyzer.

AST-based code analysis for Python — complexity, structure, issues.
Self-built, no external linters needed.
"""

from __future__ import annotations
import ast
import re
from dataclasses import dataclass, field


@dataclass
class CodeAnalysis:
    """Complete analysis of a code snippet."""
    language: str
    lines_of_code: int = 0
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    complexity: int = 0
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    summary: str = ""


class CodeAnalyzer:
    """Analyzes code structure, complexity, and potential issues."""

    def analyze_python(self, code: str) -> CodeAnalysis:
        """Deep analysis of Python code using AST."""
        analysis = CodeAnalysis(language="python")
        lines = code.strip().split("\n")
        analysis.lines_of_code = len([l for l in lines if l.strip() and not l.strip().startswith("#")])

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            analysis.issues.append(f"Syntax error at line {e.lineno}: {e.msg}")
            return analysis

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                analysis.functions.append(node.name)
                complexity = self._function_complexity(node)
                analysis.complexity += complexity
                if complexity > 10:
                    analysis.issues.append(
                        f"Function '{node.name}' has high complexity ({complexity}). Consider refactoring."
                    )
                if len(node.args.args) > 5:
                    analysis.suggestions.append(
                        f"Function '{node.name}' has {len(node.args.args)} parameters. Consider using a dataclass or dict."
                    )

            elif isinstance(node, ast.ClassDef):
                analysis.classes.append(node.name)
                methods = [n for n in ast.walk(node) if isinstance(n, ast.FunctionDef)]
                if len(methods) > 20:
                    analysis.suggestions.append(
                        f"Class '{node.name}' has {len(methods)} methods. Consider splitting."
                    )

            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis.imports.append(alias.name)
                else:
                    analysis.imports.append(f"{node.module}")

        # Check for common issues
        self._check_common_issues(code, analysis)

        analysis.summary = (
            f"{analysis.lines_of_code} lines | "
            f"{len(analysis.functions)} functions | "
            f"{len(analysis.classes)} classes | "
            f"Complexity: {analysis.complexity} | "
            f"{len(analysis.issues)} issues"
        )

        return analysis

    def _function_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.comprehension):
                complexity += 1
                complexity += len(child.ifs)
        return complexity

    def _check_common_issues(self, code: str, analysis: CodeAnalysis):
        """Check for common code issues."""
        if "eval(" in code:
            analysis.issues.append("SECURITY: eval() is dangerous. Use ast.literal_eval() or a safe parser.")
        if "exec(" in code:
            analysis.issues.append("SECURITY: exec() can execute arbitrary code. Avoid in production.")
        if re.search(r"except\s*:", code):
            analysis.issues.append("Bare 'except:' catches all exceptions including SystemExit. Be specific.")
        if "password" in code.lower() and ("=" in code or "'" in code or '"' in code):
            analysis.issues.append("SECURITY: Possible hardcoded password detected.")
        if re.search(r"TODO|FIXME|HACK|XXX", code):
            analysis.suggestions.append("Code contains TODO/FIXME/HACK comments — address before production.")
        if "import *" in code:
            analysis.issues.append("'import *' pollutes namespace. Import specific names.")
        if "global " in code:
            analysis.suggestions.append("Global variables found. Consider using class attributes or passing parameters.")

    def analyze_any(self, code: str, language: str = "") -> CodeAnalysis:
        """Analyze code in any language (basic analysis for non-Python)."""
        if language.lower() in ("python", "py", "") and not any(
            kw in code for kw in ["function ", "const ", "let ", "var ", "public class"]
        ):
            try:
                return self.analyze_python(code)
            except Exception:
                pass

        analysis = CodeAnalysis(language=language or "unknown")
        lines = code.strip().split("\n")
        analysis.lines_of_code = len([l for l in lines if l.strip()])

        # Generic pattern matching
        func_patterns = [
            r"def\s+(\w+)",          # Python
            r"function\s+(\w+)",     # JS
            r"func\s+(\w+)",         # Go
            r"fn\s+(\w+)",           # Rust
            r"public\s+\w+\s+(\w+)\s*\(", # Java/C#
        ]
        for pattern in func_patterns:
            analysis.functions.extend(re.findall(pattern, code))

        class_patterns = [r"class\s+(\w+)", r"struct\s+(\w+)", r"interface\s+(\w+)"]
        for pattern in class_patterns:
            analysis.classes.extend(re.findall(pattern, code))

        analysis.complexity = sum(
            len(re.findall(pattern, code))
            for pattern in [r"\bif\b", r"\bfor\b", r"\bwhile\b", r"\bcatch\b", r"\bcase\b"]
        )

        analysis.summary = (
            f"{analysis.lines_of_code} lines | "
            f"{len(analysis.functions)} functions | "
            f"{len(analysis.classes)} classes | "
            f"Complexity: {analysis.complexity}"
        )

        return analysis
