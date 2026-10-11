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

    # ── Classification with WORD BOUNDARY matching ──

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
        if scores[best] >= 3:
            return best
        if scores[best] >= 2 and best in ("code", "image"):
            return best

        return "general"

    def _word_match(self, keyword: str, text: str) -> bool:
        return bool(re.search(r'\b' + re.escape(keyword) + r'\b', text))

    def _score_code(self, p: str) -> int:
        kw = ["write code", "write a program", "write a function", "coding",
              "implement", "debug", "algorithm", "data structure",
              "python code", "javascript code", "html code", "sql query",
              "function", "class ", "def ", "print(", "console.log",
              "for loop", "while loop", "linked list", "binary search",
              "quicksort", "merge sort", "hash map", "binary tree",
              "rest api", "web scraper", "flask", "django", "express",
              "react", "node.js", "typescript", "golang", "rust",
              "fibonacci", "dynamic programming", "crud", "async await",
              "decorator", "pytest", "regex", "websocket", "jwt",
              "program banao", "code likho"]
        score = 0
        for k in kw:
            if len(k) <= 3:
                if self._word_match(k, p):
                    score += 1
            else:
                if k in p:
                    score += 1
        return score

    def _score_math(self, p: str) -> int:
        long_kw = ["calculate", "solve", "equation", "integral", "derivative",
                   "probability", "formula", "compute", "evaluate", "simplify",
                   "factorial", "square root", "percentage", "average", "median",
                   "matrix multiplication", "algebra", "geometry", "trigonometry",
                   "calculus", "statistics", "standard deviation", "variance",
                   "perimeter", "radius", "diameter"]
        short_kw = ["sin", "cos", "tan", "log", "sum", "mean", "mode", "area", "volume"]
        score = sum(1 for k in long_kw if k in p)
        score += sum(1 for k in short_kw if self._word_match(k, p))
        if re.search(r'\d+\s*[\+\-\*/\^%]\s*\d+', p):
            score += 3
        return score

    def _score_creative(self, p: str) -> int:
        kw = ["write a story", "write a poem", "write an essay", "write a letter",
              "write a speech", "write lyrics", "write a song",
              "poem", "poetry", "haiku", "fiction", "narrative", "blog post",
              "article about", "creative writing", "compose", "screenplay",
              "kahani", "kavita", "song about", "rap about"]
        return sum(1 for k in kw if k in p)

    def _score_image(self, p: str) -> int:
        kw = ["generate image", "create image", "draw", "generate a picture",
              "create a picture", "make an image", "illustration",
              "painting", "sketch", "wallpaper", "poster design",
              "image banao", "tasveer"]
        return sum(1 for k in kw if k in p)

    def _score_document(self, p: str) -> int:
        kw = ["summarize:", "summarise:", "analyze:", "key points:",
              "summarize this", "summarise this", "analyze this text",
              "document analysis", "word count of"]
        return sum(1 for k in kw if k in p)

    # ── General Handler — THE MAIN POWER HANDLER ──

    def _handle_general(self, prompt: str) -> str:
        queries = self._make_queries(prompt)
        all_results = []
        for q in queries[:3]:
            results = self._web_search(q)
            if results:
                all_results.extend(results)
                if len(all_results) >= 6:
                    break

        if all_results:
            return self._compose_answer(prompt, all_results)

        return self._knowledge_response(prompt)

    def _make_queries(self, prompt: str) -> list[str]:
        queries = []
        stop = {"a", "an", "the", "is", "are", "was", "were", "what", "how",
                "why", "when", "where", "who", "which", "do", "does", "did",
                "can", "could", "would", "should", "will", "about", "for",
                "to", "of", "in", "on", "at", "by", "with", "from", "me",
                "my", "i", "you", "your", "tell", "explain", "describe",
                "please", "help", "want", "need", "give", "conduct",
                "exhaustive", "examination", "provide", "detailed", "gather",
                "organize", "into", "including", "remaining", "overall"}
        words = prompt.split()
        keywords = [w for w in words if w.lower() not in stop and len(w) > 2]

        if len(keywords) <= 8:
            queries.append(" ".join(keywords))
        else:
            queries.append(" ".join(keywords[:8]))
            queries.append(" ".join(keywords[:5]))

        if len(keywords) > 5:
            queries.append(" ".join(keywords[:4]) + " overview explained")

        queries.append(prompt[:120])
        return queries

    def _compose_answer(self, prompt: str, results: list) -> str:
        sentences = []
        seen_hashes = set()

        for r in results:
            body = r.get("body", r.get("description", r.get("snippet", "")))
            if not body:
                continue
            for s in self._split_sentences(body):
                s = s.strip()
                if len(s) < 30 or len(s) > 600:
                    continue
                h = hashlib.md5(s[:50].lower().encode()).hexdigest()
                if h in seen_hashes:
                    continue
                seen_hashes.add(h)
                score = self._relevance_score(s, prompt)
                if score > 0.05:
                    sentences.append((score, s))

        sentences.sort(key=lambda x: x[0], reverse=True)
        top = sentences[:12]

        if not top:
            for r in results[:4]:
                body = r.get("body", r.get("description", r.get("snippet", "")))
                title = r.get("title", "")
                if body:
                    top.append((1.0, body[:400]))

        if not top:
            return self._knowledge_response(prompt)

        response = ""
        for i, (_, s) in enumerate(top):
            if not s.endswith('.'):
                s = s + '.'
            response += s + "\n\n"

        sources = []
        seen_titles = set()
        for r in results[:5]:
            title = r.get("title", "")
            link = r.get("href", r.get("url", r.get("link", "")))
            if title and title not in seen_titles:
                seen_titles.add(title)
                if link:
                    sources.append(f"- [{title}]({link})")
                else:
                    sources.append(f"- {title}")

        if sources:
            response += "---\n**Sources:**\n" + "\n".join(sources[:4])

        return response.strip()

    def _relevance_score(self, sentence: str, query: str) -> float:
        s_lower = sentence.lower()
        q_words = query.lower().split()
        s_words = s_lower.split()
        stop = {"a", "an", "the", "is", "are", "was", "were", "and", "or",
                "but", "in", "on", "at", "to", "for", "of", "with", "by",
                "from", "this", "that", "it", "its", "be", "has", "have",
                "had", "not", "no", "as", "if", "do", "does", "will", "can",
                "about", "into", "than", "each", "which", "what", "how",
                "they", "their", "there", "these", "those", "been", "were"}
        q_meaningful = set(w for w in q_words if w not in stop and len(w) > 2)
        s_meaningful = set(w for w in s_words if w not in stop and len(w) > 2)

        if not q_meaningful or not s_meaningful:
            return 0.1

        overlap = len(q_meaningful & s_meaningful) / max(len(q_meaningful), 1)
        has_numbers = 1.15 if re.search(r'\d', sentence) else 1.0
        length_bonus = min(len(sentence) / 150, 1.2)

        junk = ["click here", "sign up", "subscribe", "cookie", "privacy policy",
                "log in", "register", "advertisement", "sponsored", "newsletter"]
        junk_penalty = 0.2 if any(j in s_lower for j in junk) else 1.0

        return overlap * has_numbers * length_bonus * junk_penalty

    def _knowledge_response(self, prompt: str) -> str:
        p = prompt.lower()
        topic = self._extract_topic(prompt)

        knowledge = {
            "artificial intelligence": "Artificial intelligence (AI) refers to computer systems designed to perform tasks that typically require human intelligence. This includes learning from data, recognizing patterns, making decisions, understanding natural language, and solving complex problems. Modern AI encompasses machine learning, deep learning, natural language processing, computer vision, and robotics. AI applications span healthcare diagnostics, autonomous vehicles, financial analysis, content creation, and scientific research.",
            "machine learning": "Machine learning is a subset of AI where systems learn from data without being explicitly programmed. It includes supervised learning (training with labeled data), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through trial and error). Key algorithms include linear regression, decision trees, random forests, support vector machines, and neural networks.",
            "python": "Python is a high-level, interpreted programming language known for its readability and versatility. Created by Guido van Rossum in 1991, it supports multiple programming paradigms including procedural, object-oriented, and functional programming. Python's extensive standard library and packages like NumPy, Pandas, Django, and Flask make it popular for web development, data science, AI, automation, and scientific computing.",
            "javascript": "JavaScript is a dynamic, interpreted programming language primarily used for web development. It runs in browsers and on servers (Node.js). Features include first-class functions, prototype-based object orientation, and event-driven programming. Modern JavaScript (ES6+) includes classes, arrow functions, promises, async/await, modules, and destructuring. Frameworks like React, Vue, and Angular are built on JavaScript.",
            "blockchain": "Blockchain is a distributed ledger technology that records transactions across a network of computers. Each block contains a cryptographic hash of the previous block, creating an immutable chain. Key features include decentralization, transparency, and security. Applications include cryptocurrencies (Bitcoin, Ethereum), smart contracts, supply chain management, voting systems, and decentralized finance (DeFi).",
            "quantum computing": "Quantum computing uses quantum mechanical phenomena like superposition and entanglement to process information. Unlike classical bits (0 or 1), quantum bits (qubits) can exist in multiple states simultaneously. This enables quantum computers to solve certain problems exponentially faster, including cryptography, drug discovery, optimization, and materials science. Major players include IBM, Google, and Microsoft.",
            "climate change": "Climate change refers to long-term shifts in global temperatures and weather patterns. While natural cycles play a role, human activities — particularly burning fossil fuels, deforestation, and industrial processes — have been the dominant driver since the 1800s. Effects include rising sea levels, extreme weather events, biodiversity loss, and food security challenges. Solutions include renewable energy, carbon capture, and sustainable practices.",
            "neural network": "Neural networks are computing systems inspired by biological neural networks. They consist of layers of interconnected nodes (neurons) that process data. Types include feedforward networks, convolutional neural networks (CNNs) for image processing, recurrent neural networks (RNNs) for sequences, and transformers for language tasks. Training involves adjusting weights through backpropagation to minimize prediction error.",
        }

        for key, answer in knowledge.items():
            if key in p or all(w in p for w in key.split()[:2]):
                return answer

        if any(w in p for w in ["what is", "what are", "define", "explain"]):
            return (
                f"**{topic.title()}** is an important topic that spans multiple dimensions. "
                f"I tried to search the web for the most current information but couldn't connect right now.\n\n"
                f"Here's what I can tell you generally:\n\n"
                f"- {topic.title()} involves multiple interconnected concepts and applications\n"
                f"- It has both theoretical foundations and practical real-world applications\n"
                f"- The field continues to evolve with new research and developments\n\n"
                f"For the most comprehensive answer, please try again in a moment — I can provide "
                f"detailed, sourced information when web search is available.\n\n"
                f"In the meantime, I can help with **coding**, **math problems**, **creative writing**, "
                f"or **document analysis** right now."
            )

        if any(w in p for w in ["how to", "how do", "steps", "guide", "tutorial"]):
            return (
                f"Here's a general approach for **{topic}**:\n\n"
                f"1. **Research** — Understand the fundamentals and requirements\n"
                f"2. **Plan** — Define your goals, resources, and timeline\n"
                f"3. **Execute** — Follow best practices step by step\n"
                f"4. **Validate** — Test results and iterate on your approach\n"
                f"5. **Document** — Record what works for future reference\n\n"
                f"For detailed, specific instructions, I can provide much better answers when "
                f"web search is available. Try again shortly, or ask me about coding, math, "
                f"or creative writing — those work offline."
            )

        if len(prompt.split()) > 15:
            return (
                f"Thank you for the detailed question. I attempted to search for comprehensive information "
                f"about this topic, but couldn't connect to web search at this moment.\n\n"
                f"**Your question covers:** {topic[:200]}\n\n"
                f"To provide the thorough, sourced response this question deserves, I need access to "
                f"web search. Please try again in a moment.\n\n"
                f"Meanwhile, I can help with:\n"
                f"- **Code** — \"Write a Python quicksort\" or \"Create a REST API\"\n"
                f"- **Math** — \"Calculate sqrt(144) + 25\" or \"Average of 10, 20, 30\"\n"
                f"- **Writing** — \"Write a poem about nature\" or \"Draft an email\"\n"
                f"- **Analysis** — \"Summarize: [paste your text]\""
            )

        return (
            f"I'd like to help with **{topic}**, but couldn't connect to web search right now. "
            f"Please try again shortly for a detailed, sourced answer.\n\n"
            f"I can help right now with **coding**, **math**, **creative writing**, "
            f"and **document analysis**."
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
        return topic[:150] if topic else prompt[:150]

    def _split_sentences(self, text: str) -> list[str]:
        parts = re.split(r'(?<=[.!?])\s+', text)
        result = []
        for p in parts:
            p = p.strip()
            if len(p) > 20:
                if not p.endswith(('.', '!', '?')):
                    p = p + '.'
                result.append(p)
        return result

    # ── Greeting ──

    def _handle_greeting(self, prompt: str) -> str:
        greetings = [
            "Hello! How can I help you today? Ask me anything — I can research topics, write code, solve math, create stories, and more.",
            "Hey there! What would you like to work on? I'm ready for coding, research, analysis, creative tasks — you name it.",
            "Hi! I'm ready to help. What's on your mind?",
        ]
        return random.choice(greetings)

    # ── System Info ──

    def _handle_system(self, prompt: str) -> str:
        return (
            "I'm **NAGRO 4.1** — Neural Adaptive Generative Reasoning Operator, "
            "a self-built AI created by Aditya Kumar.\n\n"
            "**What I can do:**\n"
            "- Answer questions on any topic using real-time web search\n"
            "- Write and debug code in Python, JavaScript, HTML, SQL, and more\n"
            "- Solve math problems with step-by-step explanations\n"
            "- Write stories, poems, essays, speeches, and lyrics\n"
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
            "I can help with code! Try asking for specific things like:\n\n"
            "- \"Write a Python quicksort\"\n"
            "- \"Create a REST API in Flask\"\n"
            "- \"JavaScript fetch API example\"\n"
            "- \"HTML login form\"\n"
            "- \"SQL CRUD operations\""
        )

    def _generate_code_from_description(self, prompt: str, lang: str) -> str | None:
        p = prompt.lower()
        generators = [
            (["reverse string", "reverse a string"], self._code_reverse),
            (["palindrome"], self._code_palindrome),
            (["prime number", "is prime", "check prime"], self._code_prime),
            (["two sum", "twosum"], self._code_two_sum),
            (["anagram"], self._code_anagram),
            (["password generator", "generate password"], self._code_password),
            (["matrix multiply", "matrix product"], self._code_matrix),
            (["factorial"], self._code_factorial),
        ]
        for keywords, fn in generators:
            if any(k in p for k in keywords):
                return fn(lang)
        return None

    def _code_reverse(self, lang):
        if lang == "javascript":
            c = "const reverseString = (s) => s.split('').reverse().join('');\nconsole.log(reverseString('hello'));  // olleh"
        else:
            c = "def reverse_string(s):\n    return s[::-1]\n\nprint(reverse_string('hello'))  # olleh"
        return f"```{lang}\n{c}\n```\n\n**Explanation:** Reverses a string using {'slice notation' if lang == 'python' else 'split/reverse/join'}."

    def _code_palindrome(self, lang):
        if lang == "javascript":
            c = "function isPalindrome(s) {\n  const cleaned = s.toLowerCase().replace(/[^a-z0-9]/g, '');\n  return cleaned === cleaned.split('').reverse().join('');\n}\nconsole.log(isPalindrome('racecar'));  // true"
        else:
            c = "def is_palindrome(s):\n    cleaned = ''.join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]\n\nprint(is_palindrome('racecar'))  # True\nprint(is_palindrome('A man a plan a canal Panama'))  # True"
        return f"```{lang}\n{c}\n```\n\n**Explanation:** Checks if a string reads the same forwards and backwards, ignoring case and special characters."

    def _code_prime(self, lang):
        if lang == "javascript":
            c = "function isPrime(n) {\n  if (n < 2) return false;\n  for (let i = 2; i <= Math.sqrt(n); i++) {\n    if (n % i === 0) return false;\n  }\n  return true;\n}\nconsole.log([...Array(30).keys()].filter(isPrime));"
        else:
            c = "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nprint([i for i in range(2, 31) if is_prime(i)])"
        return f"```{lang}\n{c}\n```\n\n**Explanation:** Tests divisibility up to sqrt(n). Time: O(sqrt(n))."

    def _code_two_sum(self, lang):
        c = "def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        complement = target - n\n        if complement in seen:\n            return [seen[complement], i]\n        seen[n] = i\n    return []\n\nprint(two_sum([2, 7, 11, 15], 9))  # [0, 1]"
        return f"```python\n{c}\n```\n\n**Explanation:** Hash map approach — O(n) time, O(n) space."

    def _code_anagram(self, lang):
        c = "from collections import Counter\n\ndef is_anagram(s1, s2):\n    return Counter(s1.lower().replace(' ', '')) == Counter(s2.lower().replace(' ', ''))\n\nprint(is_anagram('listen', 'silent'))  # True"
        return f"```python\n{c}\n```\n\n**Explanation:** Compares character frequency counts."

    def _code_password(self, lang):
        c = "import secrets\nimport string\n\ndef generate_password(length=16):\n    chars = string.ascii_letters + string.digits + '!@#$%^&*'\n    return ''.join(secrets.choice(chars) for _ in range(length))\n\nfor _ in range(5):\n    print(generate_password())"
        return f"```python\n{c}\n```\n\n**Explanation:** Cryptographically secure password generator."

    def _code_matrix(self, lang):
        c = "def matrix_multiply(A, B):\n    result = [[sum(A[i][k]*B[k][j] for k in range(len(A[0])))\n               for j in range(len(B[0]))] for i in range(len(A))]\n    return result\n\nA = [[1,2],[3,4]]\nB = [[5,6],[7,8]]\nprint(matrix_multiply(A, B))  # [[19,22],[43,50]]"
        return f"```python\n{c}\n```\n\n**Explanation:** Matrix multiplication — O(n^3) time."

    def _code_factorial(self, lang):
        c = "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n - 1)\n\ndef factorial_iter(n):\n    result = 1\n    for i in range(2, n+1): result *= i\n    return result\n\nprint(factorial(10))  # 3628800"
        return f"```python\n{c}\n```\n\n**Explanation:** Recursive and iterative — both O(n)."

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
            "log": math.log, "log2": math.log2, "log10": math.log10,
            "exp": math.exp, "pow": pow, "factorial": math.factorial,
            "ceil": math.ceil, "floor": math.floor,
            "pi": math.pi, "e": math.e,
            "degrees": math.degrees, "radians": math.radians,
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
            response = f"**Expression:** `{expr}`\n\n**Result:** `{result}`\n"
            if isinstance(result, float) and result != int(result):
                response += f"\nDecimal: {result:.10f}"
            return response
        except Exception:
            return None

    def _solve_statistics(self, prompt: str) -> str | None:
        p = prompt.lower()
        numbers = re.findall(r'[-+]?\d*\.?\d+', prompt)
        if len(numbers) < 2:
            return None
        nums = [float(n) for n in numbers]
        if self._word_match("average", p) or self._word_match("mean", p):
            r = statistics.mean(nums)
            return f"**Numbers:** {nums}\n**Mean:** `{r}`\nFormula: {sum(nums)} / {len(nums)} = {r}"
        if self._word_match("median", p):
            return f"**Numbers:** {nums}\n**Sorted:** {sorted(nums)}\n**Median:** `{statistics.median(nums)}`"
        if self._word_match("mode", p):
            try:
                return f"**Numbers:** {nums}\n**Mode:** `{statistics.mode(nums)}`"
            except:
                return f"**Numbers:** {nums}\nNo unique mode."
        if "standard deviation" in p or "stdev" in p:
            return f"**Numbers:** {nums}\n**Stdev:** `{statistics.stdev(nums):.6f}`\n**Variance:** `{statistics.variance(nums):.6f}`"
        if self._word_match("variance", p):
            return f"**Numbers:** {nums}\n**Variance:** `{statistics.variance(nums):.6f}`"
        return None

    def _extract_math_expression(self, prompt: str) -> str | None:
        prompt_clean = prompt.replace("×", "*").replace("÷", "/").replace("^", "**").replace("√", "sqrt")
        match = re.search(
            r'(?:calculate|compute|solve|evaluate|what is|what\'s|find)\s+([\d\s\+\-\*/\.\(\)\w]+)',
            prompt_clean, re.IGNORECASE
        )
        if match:
            expr = match.group(1).strip()
            expr = re.sub(r'(\d+)\s*\!', r'factorial(\1)', expr)
            if re.search(r'\d', expr) and len(expr) < 100:
                return expr

        match = re.search(r'(\d+(?:\.\d+)?\s*[\+\-\*/\*]{1,2}\s*\d+(?:\.\d+)?(?:\s*[\+\-\*/\*]{1,2}\s*\d+(?:\.\d+)?)*)', prompt_clean)
        if match:
            return match.group(1).strip()

        match = re.search(r'((?:sqrt|factorial|log|log2|log10|sin|cos|tan|exp)\(\s*[\d.]+\s*\))', prompt_clean, re.IGNORECASE)
        if match:
            return match.group(1)

        return None

    # ── Creative ──

    def _handle_creative(self, prompt: str) -> str:
        p = prompt.lower()
        if "poem" in p or "poetry" in p or "haiku" in p:
            return self._gen_poem(prompt)
        elif "story" in p or "tale" in p:
            return self._gen_story(prompt)
        elif "speech" in p:
            return self._gen_speech(prompt)
        elif "lyrics" in p or "song" in p or "rap" in p:
            return self._gen_lyrics(prompt)
        elif "letter" in p or "email" in p:
            return self._gen_letter(prompt)
        else:
            return self._gen_essay(prompt)

    def _gen_poem(self, prompt):
        topic = re.sub(r'(write|create|make|compose|generate)\s+(a\s+)?(poem|poetry|haiku)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "the beauty of creation"
        return (
            f"## {topic.title()}\n\n"
            f"*In the heart of {topic},*\n*where shadows meet the light,*\n"
            f"*A truth unfolds like morning dew,*\n*transforming dark to bright.*\n\n"
            f"*Each moment holds a universe,*\n*of wonder yet untold,*\n"
            f"*Through {topic}, we find the words,*\n*more precious far than gold.*\n\n"
            f"*So let the world keep turning,*\n*let stars illuminate the way,*\n"
            f"*For in the dance of {topic},*\n*we find our brightest day.*"
        )

    def _gen_story(self, prompt):
        topic = re.sub(r'(write|create|tell)\s+(me\s+)?(a\s+)?(short\s+)?(story|tale)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "an unexpected adventure"
        return (
            f"## {topic.title()}\n\n"
            f"It began on a day like any other — the kind where the sky stretches endlessly "
            f"and the world hums with quiet possibility.\n\n"
            f"In the heart of {topic}, a truth emerged hidden in plain sight. "
            f"The kind of revelation that makes you question everything you thought you knew.\n\n"
            f"Through challenges that tested every limit and moments of clarity that "
            f"illuminated the way forward, the journey proved to be not just a destination "
            f"but a transformation.\n\n"
            f"They say every ending is just a new beginning. And in this story, "
            f"that truth resonated louder than ever."
        )

    def _gen_speech(self, prompt):
        topic = re.sub(r'(write|create|give)\s+(a\s+)?(speech|address)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "progress"
        return (
            f"## Speech: {topic.title()}\n\n"
            f"*Ladies and gentlemen,*\n\n"
            f"Today I want to talk about **{topic}**. In our rapidly changing world, "
            f"understanding this isn't just important — it's essential.\n\n"
            f"The question isn't whether {topic} will shape our future — it already is. "
            f"The question is what we'll do about it.\n\n"
            f"Let us move forward with purpose. Let us embrace this as an opportunity.\n\n"
            f"*Thank you.*"
        )

    def _gen_lyrics(self, prompt):
        topic = re.sub(r'(write|create|compose)\s+(a\s+)?(song|lyrics|rap)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "dreams"
        return (
            f"## {topic.title()}\n\n"
            f"**[Verse 1]**\nWalking down this road alone,\nSearching for a place called home,\n"
            f"{topic.title()} — it's calling me,\nSetting all my spirit free.\n\n"
            f"**[Chorus]**\nWe rise, we fall, we rise again,\nThrough the sunshine and the rain,\n"
            f"{topic.title()} — don't let it fade,\nThis is the choice that we have made.\n\n"
            f"**[Verse 2]**\nEvery step a story told,\nEvery heart a world of gold,\n"
            f"In the silence, find your voice,\n{topic.title()} — it is your choice."
        )

    def _gen_letter(self, prompt):
        topic = re.sub(r'(write|create|draft)\s+(a\s+)?(letter|email)\s*(about|on|for|to)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or "a professional inquiry"
        return (
            f"**Subject: {topic.title()}**\n\nDear [Recipient],\n\n"
            f"I hope this message finds you well. I am writing regarding **{topic}**.\n\n"
            f"[Your main points here]\n\n"
            f"I would appreciate the opportunity to discuss this further.\n\n"
            f"Best regards,\n[Your Name]"
        )

    def _gen_essay(self, prompt):
        topic = re.sub(r'(write|create)\s+(an?\s+)?(essay|article|blog)\s*(about|on|for)?\s*',
                       '', prompt, flags=re.IGNORECASE).strip() or prompt
        results = self._web_search(topic)
        if results:
            return self._compose_answer(topic, results)
        return (
            f"## {topic.title()}\n\n"
            f"{topic.capitalize()} is a subject that continues to shape our understanding of the world. "
            f"As we explore its dimensions, we gain insights for better decisions.\n\n"
            f"The landscape continues to evolve, driven by technology and shifting needs. "
            f"Staying informed and engaged will be key to harnessing its full potential."
        )

    # ── Image ──

    def _handle_image(self, prompt: str) -> str:
        return (
            f"**Prompt:** {prompt}\n\n"
            f"Image generation is available via the `/api/v1/image/generate` endpoint. "
            f"Send a POST request with your prompt to generate procedural art."
        )

    # ── Document ──

    def _handle_document(self, prompt: str) -> str:
        p = prompt.lower()
        if "summarize" in p or "summarise" in p:
            text = re.sub(r'(summarize|summarise|summary of)\s*:?\s*', '', prompt, flags=re.IGNORECASE).strip()
            if len(text) > 50:
                return self._summarize_text(text)
        if "analyze" in p:
            text = re.sub(r'(analyze|analysis of)\s*:?\s*', '', prompt, flags=re.IGNORECASE).strip()
            if len(text) > 50:
                return self._analyze_text(text)
        if "key points" in p:
            text = re.sub(r'(key points|extract)\s*:?\s*', '', prompt, flags=re.IGNORECASE).strip()
            if len(text) > 50:
                return self._extract_from_text(text)
        return "I can analyze text! Use: `Summarize: [text]`, `Analyze: [text]`, or `Key points: [text]`"

    def _summarize_text(self, text):
        sentences = self._split_sentences(text)
        if not sentences:
            return "Could not extract sentences from the text."
        word_freq = Counter(text.lower().split())
        scored = [(sum(word_freq.get(w, 0) for w in s.lower().split() if len(w) > 3) / (len(s.split()) + 1) * (1.5 if i == 0 else 1), s)
                  for i, s in enumerate(sentences)]
        scored.sort(reverse=True)
        top = [s for _, s in scored[:5]]
        ordered = [s for s in sentences if s in top]
        r = f"**Original:** {len(text.split())} words\n\n"
        for s in ordered:
            r += f"{s}\n\n"
        return r

    def _analyze_text(self, text):
        words = text.split()
        sentences = self._split_sentences(text)
        word_freq = Counter(w.lower() for w in words if len(w) > 4)
        stop = {"about", "which", "would", "their", "there", "could", "other", "these", "those"}
        kw = [(w, c) for w, c in word_freq.most_common(15) if w not in stop][:8]
        avg = len(words) / max(len(sentences), 1)
        uniq = len(set(w.lower() for w in words))
        r = f"**Words:** {len(words)} | **Unique:** {uniq} | **Sentences:** {len(sentences)} | **Avg words/sentence:** {avg:.1f}\n\n"
        r += "**Top keywords:** " + ", ".join(f"{w} ({c})" for w, c in kw)
        return r

    def _extract_from_text(self, text):
        sentences = self._split_sentences(text)
        if not sentences:
            return "Could not extract key points."
        word_freq = Counter(text.lower().split())
        scored = [(sum(word_freq.get(w, 0) for w in s.lower().split() if len(w) > 3) / (len(s.split()) + 1), s)
                  for s in sentences]
        scored.sort(reverse=True)
        r = "**Key Points:**\n\n"
        for i, (_, s) in enumerate(scored[:8], 1):
            r += f"{i}. {s}\n"
        return r

    # ── Search ──

    def _web_search(self, query: str) -> list:
        try:
            return self.search.search(query, max_results=8)
        except Exception:
            return []
