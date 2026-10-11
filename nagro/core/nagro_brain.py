"""
NAGRO 4.1 — Self-Built AI Brain

100% built from scratch by Aditya Kumar.
No external AI models. No pretrained weights. No PyTorch. No Transformers.
Intelligence: Web Search + NLP + Reasoning + Code Gen + Math + Documents.
"""

from __future__ import annotations
import re
import math
import ast
import hashlib
import statistics
import random
from collections import Counter
from typing import Iterator


class NAGROBrain:

    def __init__(self):
        self._search = None
        self._conversation_context: list[dict] = []

    @property
    def search(self):
        if self._search is None:
            from nagro.tools.web_search import WebSearch
            self._search = WebSearch()
        return self._search

    def think(self, prompt: str, system_prompt: str = "", history: list | None = None) -> str:
        if history:
            self._conversation_context = history[-10:]

        task = self._classify(prompt)
        handlers = {
            "greeting": self._handle_greeting,
            "code": self._handle_code,
            "math": self._handle_math,
            "creative": self._handle_creative,
            "image": self._handle_image,
            "system": self._handle_system,
            "document": self._handle_document,
        }
        handler = handlers.get(task, self._handle_general)
        response = handler(prompt)

        self._conversation_context.append({"role": "user", "content": prompt})
        self._conversation_context.append({"role": "assistant", "content": response[:500]})
        if len(self._conversation_context) > 20:
            self._conversation_context = self._conversation_context[-20:]

        return response

    def think_stream(self, prompt: str, system_prompt: str = "", history: list | None = None) -> Iterator[str]:
        response = self.think(prompt, system_prompt, history)
        sentences = re.split(r'(?<=[.!?\n])\s+', response)
        for sentence in sentences:
            words = sentence.split()
            buf = ""
            for w in words:
                buf += w + " "
                if len(buf) >= 8:
                    yield buf
                    buf = ""
            if buf:
                yield buf

    # ── Classification ──

    def _classify(self, prompt: str) -> str:
        p = prompt.lower().strip()

        if p in ("hi", "hello", "hey", "namaste", "hii", "hola", "sup", "yo",
                 "howdy", "good morning", "good evening", "good night"):
            return "greeting"

        system_kw = ["who are you", "what are you", "your name", "about yourself",
                     "kaun ho", "kya ho tum", "what can you do", "kya kar sakte"]
        if any(k in p for k in system_kw):
            return "system"

        scores = {
            "code": self._score_code(p),
            "math": self._score_math(p),
            "creative": self._score_creative(p),
            "image": self._score_image(p),
            "document": self._score_document(p),
        }
        best = max(scores, key=scores.get)
        if scores[best] >= 2:
            return best
        if scores[best] >= 1 and best in ("code", "math", "image"):
            return best

        return "general"

    def _score_code(self, p: str) -> int:
        kw = ["code", "function", "class ", "program", "implement", "debug",
              "python", "javascript", "java ", "html", "css", "sql", "api",
              "algorithm", "sort", "binary search", "linked list", "stack",
              "queue", "tree", "graph algo", "regex", "script", "write code",
              "write a program", "write a function", "coding", "def ", "print(",
              "console.log", "for loop", "while loop", "array", "database",
              "rest api", "web scraper", "flask", "django", "express", "react",
              "async", "decorator", "pytest", "fibonacci", "dynamic programming",
              "hash map", "crud", "todo app", "cli", "websocket",
              "authentication", "login", "jwt", "dom", "promise", "fetch api",
              "typescript", "golang", "rust", "c++", "code likho", "program banao"]
        return sum(1 for k in kw if k in p)

    def _score_math(self, p: str) -> int:
        kw = ["calculate", "solve", "equation", "integral", "derivative",
              "probability", "formula", "compute", "evaluate", "simplify",
              "factorial", "square root", "percentage", "average", "median",
              "sin", "cos", "tan", "log", "matrix", "algebra", "geometry",
              "trigonometry", "calculus", "statistics", "sum of", "area",
              "volume", "perimeter", "radius", "mean", "mode", "variance"]
        score = sum(1 for k in kw if k in p)
        if re.search(r'\d+\s*[\+\-\*/\^%]\s*\d+', p):
            score += 2
        return score

    def _score_creative(self, p: str) -> int:
        kw = ["write a story", "poem", "essay", "letter", "email draft",
              "creative", "fiction", "narrative", "blog", "article", "speech",
              "lyrics", "dialogue", "haiku", "sonnet", "compose", "kahani",
              "kavita", "song", "rap"]
        return sum(1 for k in kw if k in p)

    def _score_image(self, p: str) -> int:
        kw = ["image", "picture", "draw", "generate image", "create image",
              "photo", "illustration", "art", "painting", "sketch",
              "wallpaper", "logo design", "icon design", "banner", "poster",
              "tasveer", "image banao"]
        return sum(1 for k in kw if k in p)

    def _score_document(self, p: str) -> int:
        kw = ["summarize", "summarise", "analyze this", "pdf", "extract",
              "document analysis", "text analysis", "word count", "key points from"]
        return sum(1 for k in kw if k in p)

    # ── General Handler — answers ANY question via web search + synthesis ──

    def _handle_general(self, prompt: str) -> str:
        queries = self._make_queries(prompt)
        all_results = []
        for q in queries[:3]:
            results = self._web_search(q)
            all_results.extend(results)

        if all_results:
            return self._compose_answer(prompt, all_results)

        return self._answer_without_search(prompt)

    def _make_queries(self, prompt: str) -> list[str]:
        queries = [prompt]
        stop = {"a", "an", "the", "is", "are", "was", "were", "what", "how",
                "why", "when", "where", "who", "which", "do", "does", "did",
                "can", "could", "would", "should", "will", "about", "for",
                "to", "of", "in", "on", "at", "by", "with", "from", "me",
                "my", "i", "you", "your", "tell", "explain", "describe",
                "please", "help", "want", "need", "give", "conduct",
                "exhaustive", "examination", "provide", "detailed"}
        words = prompt.lower().split()
        keywords = [w for w in words if w not in stop and len(w) > 2]
        if keywords:
            queries.append(" ".join(keywords[:8]))
        if len(keywords) > 3:
            queries.append(" ".join(keywords[:4]) + " overview")
        return queries

    def _compose_answer(self, prompt: str, results: list) -> str:
        sentences = []
        seen_hashes = set()

        for r in results:
            body = r.get("body", r.get("description", ""))
            title = r.get("title", "")
            if body:
                for s in self._split_sentences(body):
                    s = s.strip()
                    if len(s) < 25 or len(s) > 500:
                        continue
                    h = hashlib.md5(s[:60].lower().encode()).hexdigest()
                    if h in seen_hashes:
                        continue
                    seen_hashes.add(h)
                    score = self._relevance_score(s, prompt)
                    sentences.append((score, s, title))

        sentences.sort(key=lambda x: x[0], reverse=True)
        top = sentences[:15]

        if not top:
            return self._answer_without_search(prompt)

        topic = self._extract_topic(prompt)
        response = ""

        intro_sents = [s for _, s, _ in top[:3]]
        response += f"{intro_sents[0]}\n\n"

        if len(intro_sents) > 1:
            response += f"{intro_sents[1]}\n\n"

        remaining = top[3:12]
        if remaining:
            for _, s, _ in remaining:
                response += f"{s}\n\n"

        sources = []
        seen_titles = set()
        for r in results[:5]:
            title = r.get("title", "")
            link = r.get("href", r.get("url", ""))
            if title and title not in seen_titles and link:
                seen_titles.add(title)
                sources.append(f"- [{title}]({link})")

        if sources:
            response += "\n**Sources:**\n" + "\n".join(sources[:4])

        return response.strip()

    def _relevance_score(self, sentence: str, query: str) -> float:
        s_lower = sentence.lower()
        q_words = set(query.lower().split())
        s_words = set(s_lower.split())
        stop = {"a", "an", "the", "is", "are", "was", "were", "and", "or",
                "but", "in", "on", "at", "to", "for", "of", "with", "by",
                "from", "this", "that", "it", "its", "be", "has", "have",
                "had", "not", "no", "as", "if", "do", "does", "will", "can"}
        q_meaningful = q_words - stop
        s_meaningful = s_words - stop

        if not q_meaningful:
            return 0

        overlap = len(q_meaningful & s_meaningful) / len(q_meaningful)
        info_density = len(s_meaningful) / max(len(s_words), 1)
        has_numbers = 1.2 if re.search(r'\d', sentence) else 1.0
        length_bonus = min(len(sentence) / 200, 1.0)
        junk_penalty = 0.3 if any(j in s_lower for j in
            ["click here", "sign up", "subscribe", "cookie", "privacy policy",
             "log in", "register", "advertisement", "sponsored"]) else 1.0

        return overlap * info_density * has_numbers * length_bonus * junk_penalty

    def _answer_without_search(self, prompt: str) -> str:
        p = prompt.lower()
        topic = self._extract_topic(prompt)

        if any(w in p for w in ["what is", "what are", "define", "meaning of"]):
            return (
                f"**{topic.title()}** is a broad and important topic. "
                f"While I couldn't access web search results right now to provide the most current information, "
                f"here's a general framework for understanding it:\n\n"
                f"The concept of {topic} encompasses multiple dimensions — theoretical foundations, "
                f"practical applications, and ongoing developments. To get the most accurate and "
                f"up-to-date information, you might want to:\n\n"
                f"1. Check specialized databases and academic resources\n"
                f"2. Review recent publications in the field\n"
                f"3. Consult expert analyses and industry reports\n\n"
                f"Feel free to ask me a more specific question about {topic}, or try again "
                f"when web search is available for comprehensive, sourced answers."
            )

        if any(w in p for w in ["how to", "how do", "steps to", "guide"]):
            return (
                f"Here's a general approach to **{topic}**:\n\n"
                f"1. **Research & Planning** — Understand the requirements and scope\n"
                f"2. **Preparation** — Gather necessary resources and tools\n"
                f"3. **Execution** — Follow established best practices step by step\n"
                f"4. **Review** — Validate your results and iterate\n\n"
                f"For detailed, specific steps, please try again when web search is available, "
                f"or ask me about coding, math, or creative writing tasks that I can handle offline."
            )

        return (
            f"I'd like to give you a thorough answer about **{topic}**, but I couldn't reach "
            f"web search right now. My knowledge engine works best with internet access for "
            f"real-time information.\n\n"
            f"**What I can do right now:**\n"
            f"- Write code in Python, JavaScript, HTML, SQL, and more\n"
            f"- Solve math problems step by step\n"
            f"- Create stories, poems, essays, and speeches\n"
            f"- Analyze and summarize text you paste\n\n"
            f"Please try your question again, or ask me something from the categories above."
        )

    def _extract_topic(self, prompt: str) -> str:
        topic = re.sub(
            r'^(what is|what are|how does|how do|how to|why does|why do|explain|'
            r'describe|tell me about|define|research|search for|find|conduct|'
            r'provide|give me|write about|discuss|analyze|examine|compare)\s+',
            '', prompt, flags=re.IGNORECASE
        ).strip()
        topic = re.sub(r'^(a|an|the|detailed|exhaustive|comprehensive|brief)\s+',
                       '', topic, flags=re.IGNORECASE).strip()
        return topic[:100] if topic else prompt[:100]

    def _split_sentences(self, text: str) -> list[str]:
        parts = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        result = []
        for p in parts:
            p = p.strip()
            if len(p) > 20:
                result.append(p.rstrip('.') + '.')
        return result

    # ── Greeting ──

    def _handle_greeting(self, prompt: str) -> str:
        greetings = [
            "Hello! How can I help you today? I can assist with coding, research, math, creative writing, and much more.",
            "Hey there! What would you like to work on? Ask me anything — coding, research, analysis, creative tasks, you name it.",
            "Hi! I'm ready to help. What's on your mind?",
        ]
        return random.choice(greetings)

    # ── System Info ──

    def _handle_system(self, prompt: str) -> str:
        return (
            "I'm **NAGRO 4.1** — Neural Adaptive Generative Reasoning Operator, "
            "a self-built AI created by Aditya Kumar.\n\n"
            "**What I can do:**\n"
            "- Answer questions on any topic (powered by real-time web search)\n"
            "- Write and debug code in 8+ languages\n"
            "- Solve math problems with step-by-step explanations\n"
            "- Write stories, poems, essays, speeches, and more\n"
            "- Analyze and summarize documents\n"
            "- Generate images with a procedural engine\n\n"
            "100% self-built. No external AI models. 200K context window."
        )

    # ── Code ──

    def _handle_code(self, prompt: str) -> str:
        from nagro.core.code_templates import find_template, detect_language
        lang = detect_language(prompt)
        template = find_template(prompt, lang)

        if template:
            resp = f"```{template['lang']}\n{template['code']}\n```\n\n"
            resp += f"**Explanation:** {template['explanation']}\n"
            if "complexity" in template:
                resp += f"\n**Complexity:** {template['complexity']}"
            return resp

        code = self._generate_code_from_description(prompt, lang)
        if code:
            return code

        results = self._web_search(prompt + " code example")
        if results:
            return self._compose_answer(prompt, results)

        return (
            f"I can help with code! Try asking for specific things like:\n\n"
            f"- \"Write a Python quicksort\"\n"
            f"- \"Create a REST API in Flask\"\n"
            f"- \"JavaScript fetch API example\"\n"
            f"- \"HTML login form\"\n"
            f"- \"SQL CRUD operations\""
        )

    def _generate_code_from_description(self, prompt: str, lang: str) -> str | None:
        p = prompt.lower()

        generators = [
            (["reverse string", "reverse a string"], self._code_reverse_string),
            (["palindrome"], self._code_palindrome),
            (["prime", "is prime", "prime number"], self._code_prime),
            (["two sum", "twosum"], self._code_two_sum),
            (["anagram"], self._code_anagram),
            (["password generator", "generate password"], self._code_password),
            (["matrix multiply", "matrix product"], self._code_matrix),
            (["factorial"], self._code_factorial),
        ]

        for keywords, gen_fn in generators:
            if any(k in p for k in keywords):
                return gen_fn(lang)
        return None

    def _code_reverse_string(self, lang: str) -> str:
        if lang == "javascript":
            code = "const reverseString = (s) => s.split('').reverse().join('');\nconsole.log(reverseString('hello'));  // olleh"
        else:
            code = "def reverse_string(s):\n    return s[::-1]\n\nprint(reverse_string('hello'))  # olleh"
        return f"```{lang}\n{code}\n```\n\n**Explanation:** Reverses a string using {'slice notation' if lang == 'python' else 'split/reverse/join'}."

    def _code_palindrome(self, lang: str) -> str:
        if lang == "javascript":
            code = "function isPalindrome(s) {\n  const cleaned = s.toLowerCase().replace(/[^a-z0-9]/g, '');\n  return cleaned === cleaned.split('').reverse().join('');\n}\n\nconsole.log(isPalindrome('racecar'));  // true"
        else:
            code = "def is_palindrome(s):\n    cleaned = ''.join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]\n\nprint(is_palindrome('racecar'))  # True\nprint(is_palindrome('A man a plan a canal Panama'))  # True"
        return f"```{lang}\n{code}\n```\n\n**Explanation:** Checks if a string reads the same forwards and backwards, ignoring case and special characters."

    def _code_prime(self, lang: str) -> str:
        if lang == "javascript":
            code = "function isPrime(n) {\n  if (n < 2) return false;\n  for (let i = 2; i <= Math.sqrt(n); i++) {\n    if (n % i === 0) return false;\n  }\n  return true;\n}\n\nconsole.log([...Array(30).keys()].filter(n => isPrime(n)));"
        else:
            code = "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nprint([i for i in range(2, 31) if is_prime(i)])"
        return f"```{lang}\n{code}\n```\n\n**Explanation:** Tests divisibility up to sqrt(n). Time: O(sqrt(n)) per check."

    def _code_two_sum(self, lang: str) -> str:
        code = "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        complement = target - n\n        if complement in seen:\n            return [seen[complement], i]\n        seen[n] = i\n    return []\n\nprint(two_sum([2, 7, 11, 15], 9))  # [0, 1]"
        return f"```python\n{code}\n```\n\n**Explanation:** Hash map approach — for each number, check if (target - number) was seen. O(n) time, O(n) space."

    def _code_anagram(self, lang: str) -> str:
        code = "from collections import Counter\n\ndef is_anagram(s1, s2):\n    return Counter(s1.lower().replace(' ', '')) == Counter(s2.lower().replace(' ', ''))\n\nprint(is_anagram('listen', 'silent'))  # True"
        return f"```python\n{code}\n```\n\n**Explanation:** Compares character frequency counts. Two strings are anagrams if they have identical character distributions."

    def _code_password(self, lang: str) -> str:
        code = "import secrets\nimport string\n\ndef generate_password(length=16):\n    chars = string.ascii_letters + string.digits + '!@#$%^&*'\n    return ''.join(secrets.choice(chars) for _ in range(length))\n\nfor _ in range(5):\n    print(generate_password())"
        return f"```python\n{code}\n```\n\n**Explanation:** Cryptographically secure password generator using the `secrets` module."

    def _code_matrix(self, lang: str) -> str:
        code = "def matrix_multiply(A, B):\n    rows_a, cols_a = len(A), len(A[0])\n    cols_b = len(B[0])\n    result = [[0] * cols_b for _ in range(rows_a)]\n    for i in range(rows_a):\n        for j in range(cols_b):\n            for k in range(cols_a):\n                result[i][j] += A[i][k] * B[k][j]\n    return result\n\nA = [[1, 2], [3, 4]]\nB = [[5, 6], [7, 8]]\nprint(matrix_multiply(A, B))  # [[19, 22], [43, 50]]"
        return f"```python\n{code}\n```\n\n**Explanation:** Triple nested loop multiplication. O(n^3) time complexity."

    def _code_factorial(self, lang: str) -> str:
        code = "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\ndef factorial_iter(n):\n    result = 1\n    for i in range(2, n + 1):\n        result *= i\n    return result\n\nprint(factorial(10))       # 3628800\nprint(factorial_iter(10))  # 3628800"
        return f"```python\n{code}\n```\n\n**Explanation:** Recursive and iterative approaches. Both O(n) time."

    # ── Math ──

    def _handle_math(self, prompt: str) -> str:
        result = self._solve_math(prompt)
        if result:
            return result

        stats_result = self._solve_statistics(prompt)
        if stats_result:
            return stats_result

        results = self._web_search(prompt + " solution step by step")
        if results:
            return self._compose_answer(prompt, results)

        return "Please provide a math expression like `2 + 3 * 4`, `sqrt(16)`, `factorial(5)`, or `average of 10, 20, 30`."

    def _solve_math(self, prompt: str) -> str | None:
        expr = self._extract_math_expression(prompt)
        if not expr:
            return None

        safe_names = {
            "sqrt": math.sqrt, "abs": abs, "round": round,
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "log": math.log, "log2": math.log2, "log10": math.log10,
            "exp": math.exp, "pow": pow, "factorial": math.factorial,
            "ceil": math.ceil, "floor": math.floor,
            "pi": math.pi, "e": math.e, "tau": math.tau,
            "degrees": math.degrees, "radians": math.radians,
            "gcd": math.gcd,
        }

        try:
            tree = ast.parse(expr, mode='eval')
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id not in safe_names:
                        return None
                elif isinstance(node, ast.Attribute):
                    return None

            result = eval(expr, {"__builtins__": {}}, safe_names)

            response = f"**Expression:** `{expr}`\n\n"
            response += f"**Result: `{result}`**\n\n"

            if isinstance(result, float):
                if result == int(result):
                    response += f"Integer: {int(result)}\n"
                response += f"Decimal: {result:.10f}\n"

            return response
        except Exception:
            return None

    def _solve_statistics(self, prompt: str) -> str | None:
        p = prompt.lower()
        numbers = re.findall(r'[-+]?\d*\.?\d+', prompt)
        if len(numbers) < 2:
            return None

        nums = [float(n) for n in numbers]

        if any(w in p for w in ["average", "mean"]):
            result = statistics.mean(nums)
            return f"**Numbers:** {nums}\n\n**Mean (Average):** `{result}`\n\nFormula: {sum(nums)} / {len(nums)} = {result}"

        if "median" in p:
            result = statistics.median(nums)
            return f"**Numbers:** {nums}\n**Sorted:** {sorted(nums)}\n**Median:** `{result}`"

        if "mode" in p:
            try:
                result = statistics.mode(nums)
                return f"**Numbers:** {nums}\n**Mode:** `{result}`"
            except statistics.StatisticsError:
                return f"**Numbers:** {nums}\n\nNo unique mode found."

        if any(w in p for w in ["standard deviation", "std dev", "stdev"]):
            result = statistics.stdev(nums)
            return f"**Numbers:** {nums}\n\n**Standard Deviation:** `{result:.6f}`\n**Variance:** `{statistics.variance(nums):.6f}`"

        if "variance" in p:
            result = statistics.variance(nums)
            return f"**Numbers:** {nums}\n\n**Variance:** `{result:.6f}`"

        return None

    def _extract_math_expression(self, prompt: str) -> str | None:
        prompt = prompt.replace("×", "*").replace("÷", "/").replace("^", "**").replace("√", "sqrt")
        patterns = [
            r'(?:calculate|compute|solve|evaluate|what is|find|what\'s)\s+([\d\s\+\-\*/\.\(\)\*\w]+)',
            r'([\d]+[\s\+\-\*/\.\(\)\*\d\w]+[\d\)]+)',
            r'(sqrt\([^)]+\))',
            r'(factorial\(\d+\))',
            r'(\d+\s*\!\s*)',
        ]
        for pattern in patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                expr = match.group(1).strip()
                expr = re.sub(r'(\d+)\s*\!', r'factorial(\1)', expr)
                return expr
        return None

    # ── Creative ──

    def _handle_creative(self, prompt: str) -> str:
        p = prompt.lower()
        if "poem" in p or "poetry" in p or "haiku" in p or "kavita" in p:
            return self._generate_poem(prompt)
        elif "story" in p or "tale" in p or "kahani" in p:
            return self._generate_story(prompt)
        elif "speech" in p or "address" in p:
            return self._generate_speech(prompt)
        elif "lyrics" in p or "song" in p or "rap" in p:
            return self._generate_lyrics(prompt)
        elif "letter" in p or "email" in p:
            return self._generate_letter(prompt)
        else:
            return self._generate_essay(prompt)

    def _generate_poem(self, prompt: str) -> str:
        topic = re.sub(r'(write|create|make|compose|generate)\s+(a\s+)?(poem|poetry|haiku|kavita)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "the beauty of creation"

        results = self._web_search(f"{topic} poetry inspiration")
        extra = ""
        if results:
            pts = self._extract_key_points(results[:2])
            if pts:
                extra = f"\n\n*Inspired by: {pts[0][:80]}*"

        poem = (
            f"*In the heart of {topic},*\n"
            f"*where shadows meet the light,*\n"
            f"*A truth unfolds like morning dew,*\n"
            f"*transforming dark to bright.*\n\n"
            f"*Each moment holds a universe,*\n"
            f"*of wonder yet untold,*\n"
            f"*Through {topic}, we find the words,*\n"
            f"*more precious far than gold.*\n\n"
            f"*So let the world keep turning,*\n"
            f"*let stars illuminate the way,*\n"
            f"*For in the dance of {topic},*\n"
            f"*we find our brightest day.*"
        )
        return f"## {topic.title()}\n\n{poem}{extra}"

    def _generate_story(self, prompt: str) -> str:
        topic = re.sub(r'(write|create|tell|generate)\s+(me\s+)?(a\s+)?(short\s+)?(story|tale|kahani)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "an unexpected adventure"

        results = self._web_search(f"{topic} story ideas")
        details = self._extract_key_points(results[:3]) if results else []

        r = f"## {topic.title()}\n\n"
        r += (
            f"It began on a day like any other — the kind where the sky stretches endlessly "
            f"and the world hums with quiet possibility. But beneath the ordinary, something "
            f"extraordinary was stirring.\n\n"
        )

        if details:
            r += f"What no one expected was the discovery that changed everything. {details[0]}.\n\n"
            r += (
                f"The implications were staggering. Every assumption was thrown into question. "
                f"And yet, within the chaos, a pattern emerged — a path forward that required "
                f"not just intelligence, but courage.\n\n"
            )
        else:
            r += (
                f"In the heart of {topic}, a truth emerged hidden in plain sight. "
                f"The kind of revelation that makes you question everything.\n\n"
            )

        r += (
            f"Through challenges that tested every limit and moments of clarity that "
            f"illuminated the way forward, the journey proved to be not just a destination "
            f"but a transformation.\n\n"
            f"They say every ending is just a new beginning. And in this story, "
            f"that truth resonated louder than ever."
        )
        return r

    def _generate_speech(self, prompt: str) -> str:
        topic = re.sub(r'(write|create|give|prepare)\s+(a\s+)?(speech|address)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "progress"

        results = self._web_search(f"{topic} facts statistics")
        facts = self._extract_key_points(results[:3]) if results else []

        r = f"## Speech: {topic.title()}\n\n"
        r += f"*Ladies and gentlemen,*\n\n"
        r += f"Today I want to talk about **{topic}**. In our rapidly changing world, understanding this isn't just important — it's essential.\n\n"

        if facts:
            r += "Consider this:\n\n"
            for f in facts[:3]:
                r += f"> {f}\n\n"

        r += (
            f"The question isn't whether {topic} will shape our future — it already is. "
            f"The question is what we'll do about it.\n\n"
            f"I believe the answer lies in action. Not tomorrow — today. "
            f"Each one of us can make a difference.\n\n"
            f"Let us move forward with purpose. Let us embrace this as an opportunity.\n\n"
            f"*Thank you.*"
        )
        return r

    def _generate_lyrics(self, prompt: str) -> str:
        topic = re.sub(r'(write|create|compose)\s+(a\s+)?(song|lyrics|rap)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "chasing dreams"

        return (
            f"## {topic.title()}\n\n"
            f"**[Verse 1]**\n"
            f"Walking down this road alone,\n"
            f"Searching for a place called home,\n"
            f"{topic.title()} — it's calling me,\n"
            f"Setting all my spirit free.\n\n"
            f"**[Chorus]**\n"
            f"We rise, we fall, we rise again,\n"
            f"Through the sunshine and the rain,\n"
            f"{topic.title()} — don't let it fade,\n"
            f"This is the choice that we have made.\n\n"
            f"**[Verse 2]**\n"
            f"Every step a story told,\n"
            f"Every heart a world of gold,\n"
            f"In the silence, find your voice,\n"
            f"{topic.title()} — it is your choice.\n\n"
            f"**[Bridge]**\n"
            f"When the world says give up now,\n"
            f"We'll find another way somehow.\n\n"
            f"**[Outro]**\n"
            f"Yeah, {topic}... it's our song."
        )

    def _generate_letter(self, prompt: str) -> str:
        topic = re.sub(r'(write|create|draft)\s+(a\s+)?(letter|email)\s*(about|on|for|to)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "a professional inquiry"

        return (
            f"**Subject: Regarding {topic.title()}**\n\n"
            f"Dear [Recipient],\n\n"
            f"I hope this message finds you well. I am writing regarding **{topic}**.\n\n"
            f"[Your main points here]\n\n"
            f"I would appreciate the opportunity to discuss this further at your "
            f"earliest convenience.\n\n"
            f"Thank you for your time.\n\n"
            f"Best regards,\n[Your Name]"
        )

    def _generate_essay(self, prompt: str) -> str:
        topic = re.sub(r'(write|create)\s+(an?\s+)?(essay|article|blog)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or prompt

        results = self._web_search(topic)
        points = self._extract_key_points(results) if results else []

        r = f"## {topic.title()}\n\n"
        r += (
            f"{topic.capitalize()} is a subject that continues to shape our understanding "
            f"of the world. As we explore its dimensions, we gain insights that help us "
            f"make better decisions.\n\n"
        )

        if points:
            r += "### Key Insights\n\n"
            for i, point in enumerate(points[:5], 1):
                r += f"**{i}.** {point}.\n\n"

        r += "### Analysis\n\n"
        if results:
            extra = self._extract_key_points(results[3:])
            for pt in extra[:3]:
                r += f"{pt}.\n\n"
        else:
            r += f"The landscape of {topic} continues to evolve, driven by technology and shifting needs.\n\n"

        r += (
            f"### Conclusion\n\n"
            f"{topic.capitalize()} remains dynamic and important. Staying informed and engaged "
            f"will be key to harnessing its full potential."
        )
        return r

    # ── Image ──

    def _handle_image(self, prompt: str) -> str:
        return (
            f"**Prompt:** {prompt}\n\n"
            f"Image generation is available via the `/api/v1/image/generate` endpoint. "
            f"NAGRO uses a procedural engine to create geometric art, gradients, "
            f"abstract patterns, and themed compositions.\n\n"
            f"Send a POST request to generate your image."
        )

    # ── Document ──

    def _handle_document(self, prompt: str) -> str:
        p = prompt.lower()
        if "summarize" in p or "summary" in p or "summarise" in p:
            text = re.sub(r'(summarize|summarise|summary of|give me a summary)\s*:?\s*',
                          '', prompt, flags=re.IGNORECASE).strip()
            if text and len(text) > 50:
                return self._summarize_text(text)
        if "analyze" in p or "analysis" in p:
            text = re.sub(r'(analyze|analysis of|analyse)\s*:?\s*',
                          '', prompt, flags=re.IGNORECASE).strip()
            if text and len(text) > 50:
                return self._analyze_text(text)
        if "key points" in p or "extract" in p:
            text = re.sub(r'(key points|extract key points|extract from)\s*:?\s*',
                          '', prompt, flags=re.IGNORECASE).strip()
            if text and len(text) > 50:
                return self._extract_from_text(text)

        return (
            "I can analyze documents! Use these formats:\n\n"
            "- **Summarize:** `Summarize: [your text]`\n"
            "- **Analyze:** `Analyze: [your text]`\n"
            "- **Key points:** `Key points: [your text]`\n\n"
            "Paste your text after the command."
        )

    def _summarize_text(self, text: str) -> str:
        sentences = self._split_sentences(text)
        if not sentences:
            return "Could not extract meaningful sentences from the text."

        word_freq = Counter(text.lower().split())
        scored = []
        for i, sent in enumerate(sentences):
            words = sent.lower().split()
            score = sum(word_freq.get(w, 0) for w in words if len(w) > 3) / (len(words) + 1)
            if i == 0:
                score *= 1.5
            scored.append((score, sent))

        scored.sort(reverse=True)
        top = [s for _, s in scored[:5]]
        ordered = [s for s in sentences if s in top]

        wc = len(text.split())
        r = f"**Original:** {wc} words | **Summary:** {len(ordered)} key sentences\n\n---\n\n"
        for s in ordered:
            r += f"{s}\n\n"
        return r

    def _analyze_text(self, text: str) -> str:
        words = text.split()
        sentences = self._split_sentences(text)
        word_freq = Counter(w.lower() for w in words if len(w) > 3)
        stop = {"that", "this", "with", "from", "they", "have", "been", "were",
                "will", "what", "when", "your", "their", "about", "which", "would",
                "there", "could", "other", "some", "more", "also", "than", "each"}
        keywords = [(w, c) for w, c in word_freq.most_common(20) if w not in stop][:10]

        avg_len = len(words) / max(len(sentences), 1)
        unique = len(set(w.lower() for w in words))
        diversity = unique / max(len(words), 1)

        r = "### Statistics\n\n"
        r += f"| Metric | Value |\n|---|---|\n"
        r += f"| Words | {len(words)} |\n"
        r += f"| Unique Words | {unique} |\n"
        r += f"| Sentences | {len(sentences)} |\n"
        r += f"| Avg Words/Sentence | {avg_len:.1f} |\n"
        r += f"| Lexical Diversity | {diversity:.0%} |\n\n"
        r += "### Top Keywords\n\n"
        for word, count in keywords:
            r += f"- **{word}** ({count})\n"
        r += "\n### Readability\n\n"
        if avg_len < 15:
            r += "Short, simple sentences — easy to read.\n"
        elif avg_len < 25:
            r += "Moderate sentence length — good readability.\n"
        else:
            r += "Long, complex sentences — may be harder to read.\n"
        return r

    def _extract_from_text(self, text: str) -> str:
        sentences = self._split_sentences(text)
        if not sentences:
            return "Could not extract key points."

        word_freq = Counter(text.lower().split())
        scored = []
        for sent in sentences:
            words = sent.lower().split()
            score = sum(word_freq.get(w, 0) for w in words if len(w) > 3) / (len(words) + 1)
            scored.append((score, sent))

        scored.sort(reverse=True)
        r = "### Key Points\n\n"
        for i, (_, sent) in enumerate(scored[:8], 1):
            r += f"{i}. {sent.strip()}\n\n"
        return r

    # ── Search Utilities ──

    def _web_search(self, query: str) -> list:
        try:
            results = self.search.search(query, max_results=8)
            return results if results else []
        except Exception:
            return []

    def _extract_key_points(self, results: list) -> list[str]:
        all_text = " ".join(r.get("body", r.get("description", "")) for r in results)
        sentences = self._split_sentences(all_text)

        seen = set()
        unique = []
        for s in sentences:
            key = s[:40].lower()
            if key not in seen and len(s) > 30:
                seen.add(key)
                unique.append(s.strip().rstrip('.'))
        return unique[:8]
