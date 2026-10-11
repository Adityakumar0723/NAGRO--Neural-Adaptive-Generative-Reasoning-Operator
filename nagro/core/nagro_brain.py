"""
NAGRO 4.1 — Self-Built AI Brain (Advanced)

100% built from scratch. No external AI models.
Intelligence: Web Search + Knowledge Base + NLP + Code Gen + Math + Creative.
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


# ══════════════════════════════════════════════════════════════════
#  BUILT-IN KNOWLEDGE BASE — offline answers for common topics
# ══════════════════════════════════════════════════════════════════

KNOWLEDGE = {
    "artificial intelligence": (
        "Artificial Intelligence (AI) is a branch of computer science focused on creating systems capable of performing tasks that normally require human intelligence. These tasks include visual perception, speech recognition, decision-making, language translation, and problem-solving.\n\n"
        "**Types of AI:**\n"
        "- **Narrow AI (Weak AI):** Designed for specific tasks — virtual assistants (Siri, Alexa), recommendation systems, image recognition. This is what exists today.\n"
        "- **General AI (Strong AI):** Hypothetical systems with human-level reasoning across all domains. Does not yet exist.\n"
        "- **Superintelligent AI:** Theoretical AI surpassing human intelligence. A topic of research and philosophical debate.\n\n"
        "**Key Subfields:**\n"
        "- **Machine Learning:** Systems that learn from data (supervised, unsupervised, reinforcement learning)\n"
        "- **Deep Learning:** Neural networks with many layers, powering breakthroughs in vision, language, and generation\n"
        "- **Natural Language Processing (NLP):** Understanding and generating human language\n"
        "- **Computer Vision:** Interpreting images and video\n"
        "- **Robotics:** Physical agents that interact with the world\n\n"
        "**Applications:** Healthcare diagnostics, autonomous vehicles, financial trading, content creation, drug discovery, climate modeling, cybersecurity, and education.\n\n"
        "**Challenges:** Bias in training data, explainability, energy consumption, job displacement, privacy concerns, and alignment with human values."
    ),
    "machine learning": (
        "Machine Learning (ML) is a subset of AI where computers learn patterns from data without being explicitly programmed for each task.\n\n"
        "**Three Main Types:**\n\n"
        "**1. Supervised Learning** — Model learns from labeled examples (input → output pairs)\n"
        "- Classification: spam detection, image recognition, sentiment analysis\n"
        "- Regression: price prediction, weather forecasting, demand estimation\n"
        "- Algorithms: Linear Regression, Decision Trees, Random Forest, SVM, Neural Networks\n\n"
        "**2. Unsupervised Learning** — Model finds patterns in unlabeled data\n"
        "- Clustering: customer segmentation, anomaly detection\n"
        "- Dimensionality Reduction: PCA, t-SNE for data visualization\n"
        "- Algorithms: K-Means, DBSCAN, Hierarchical Clustering, Autoencoders\n\n"
        "**3. Reinforcement Learning** — Agent learns by interacting with an environment\n"
        "- Reward-based: game playing (AlphaGo), robot control, resource management\n"
        "- Algorithms: Q-Learning, Deep Q-Networks, Policy Gradient, PPO\n\n"
        "**Key Concepts:** Features, labels, training/validation/test splits, overfitting, regularization, cross-validation, hyperparameter tuning, gradient descent, loss functions, ensemble methods.\n\n"
        "**Popular Frameworks:** Scikit-learn, TensorFlow, PyTorch, XGBoost, LightGBM."
    ),
    "deep learning": (
        "Deep Learning is a subset of Machine Learning using artificial neural networks with multiple layers (hence 'deep'). These networks can learn hierarchical representations of data.\n\n"
        "**Architecture Types:**\n"
        "- **CNNs (Convolutional Neural Networks):** Image classification, object detection, medical imaging\n"
        "- **RNNs (Recurrent Neural Networks):** Sequential data — time series, text, speech\n"
        "- **LSTMs (Long Short-Term Memory):** Improved RNNs that handle long-range dependencies\n"
        "- **Transformers:** Attention-based models revolutionizing NLP and vision (GPT, BERT, ViT)\n"
        "- **GANs (Generative Adversarial Networks):** Generate realistic images, video, and audio\n"
        "- **Diffusion Models:** State-of-the-art image generation (Stable Diffusion, DALL-E)\n"
        "- **Autoencoders / VAEs:** Data compression, anomaly detection, generation\n\n"
        "**Training Process:** Forward pass → compute loss → backpropagation → update weights via gradient descent. Requires large datasets and significant compute (GPUs/TPUs).\n\n"
        "**Breakthroughs:** ImageNet (2012), AlphaGo (2016), GPT-3 (2020), ChatGPT (2022), GPT-4 (2023), Multimodal models."
    ),
    "python": (
        "Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum, first released in 1991. Known for its readable syntax and versatility.\n\n"
        "**Key Features:**\n"
        "- Dynamically typed with automatic memory management\n"
        "- Supports procedural, object-oriented, and functional programming\n"
        "- Extensive standard library ('batteries included')\n"
        "- Huge ecosystem of third-party packages (PyPI)\n"
        "- Cross-platform (Windows, macOS, Linux)\n\n"
        "**Popular Use Cases:**\n"
        "- **Web Development:** Django, Flask, FastAPI\n"
        "- **Data Science:** Pandas, NumPy, Matplotlib, Jupyter\n"
        "- **Machine Learning:** TensorFlow, PyTorch, Scikit-learn\n"
        "- **Automation/Scripting:** OS automation, web scraping (Beautiful Soup, Scrapy)\n"
        "- **DevOps:** Ansible, infrastructure automation\n"
        "- **Scientific Computing:** SciPy, SymPy\n\n"
        "**Core Concepts:** Variables, data types (list, dict, tuple, set), control flow (if/elif/else, for, while), functions, classes, modules, decorators, generators, context managers, comprehensions, exception handling, virtual environments."
    ),
    "javascript": (
        "JavaScript is a dynamic, interpreted programming language and one of the core technologies of the World Wide Web, alongside HTML and CSS.\n\n"
        "**Key Features:**\n"
        "- Runs in browsers (client-side) and on servers (Node.js)\n"
        "- Event-driven, non-blocking I/O\n"
        "- First-class functions, closures, prototypal inheritance\n"
        "- Dynamic typing with optional TypeScript for static types\n\n"
        "**Modern JavaScript (ES6+):**\n"
        "- `let`/`const` block scoping, arrow functions, template literals\n"
        "- Destructuring, spread/rest operators, default parameters\n"
        "- Promises, async/await for asynchronous programming\n"
        "- Classes, modules (import/export), iterators/generators\n"
        "- Map, Set, WeakMap, WeakRef\n\n"
        "**Ecosystem:**\n"
        "- **Frontend Frameworks:** React, Vue.js, Angular, Svelte\n"
        "- **Backend:** Node.js, Express, Fastify, Deno, Bun\n"
        "- **Mobile:** React Native, Ionic\n"
        "- **Desktop:** Electron\n"
        "- **Build Tools:** Webpack, Vite, esbuild\n"
        "- **Package Manager:** npm, yarn, pnpm\n"
        "- **Testing:** Jest, Mocha, Cypress, Playwright"
    ),
    "blockchain": (
        "Blockchain is a distributed, immutable ledger technology that records transactions across a network of computers.\n\n"
        "**How It Works:**\n"
        "1. A transaction is initiated\n"
        "2. The transaction is broadcast to a peer-to-peer network\n"
        "3. Network nodes validate the transaction using consensus algorithms\n"
        "4. The verified transaction is combined with others into a block\n"
        "5. The new block is added to the existing chain — permanent and unalterable\n\n"
        "**Key Concepts:**\n"
        "- **Decentralization:** No single point of control or failure\n"
        "- **Immutability:** Once recorded, data cannot be altered retroactively\n"
        "- **Consensus Mechanisms:** Proof of Work (PoW), Proof of Stake (PoS), DPoS\n"
        "- **Smart Contracts:** Self-executing code on the blockchain (Ethereum, Solana)\n"
        "- **Tokens:** Fungible (ERC-20) and non-fungible (NFTs, ERC-721)\n\n"
        "**Applications:**\n"
        "- Cryptocurrencies (Bitcoin, Ethereum, Solana)\n"
        "- Decentralized Finance (DeFi) — lending, borrowing, DEXs\n"
        "- Supply chain tracking and verification\n"
        "- Digital identity and voting systems\n"
        "- Healthcare records, real estate, intellectual property"
    ),
    "quantum computing": (
        "Quantum computing is a type of computation that harnesses quantum mechanical phenomena — superposition, entanglement, and interference — to process information in fundamentally different ways from classical computers.\n\n"
        "**Key Concepts:**\n"
        "- **Qubits:** Unlike classical bits (0 or 1), qubits can exist in a superposition of both states simultaneously\n"
        "- **Entanglement:** Qubits can be correlated so the state of one instantly affects the other, regardless of distance\n"
        "- **Quantum Gates:** Operations that manipulate qubits (Hadamard, CNOT, Pauli-X/Y/Z, Toffoli)\n"
        "- **Quantum Circuits:** Sequences of quantum gates that form algorithms\n\n"
        "**Advantages Over Classical Computing:**\n"
        "- Exponential speedup for specific problems\n"
        "- Breaking certain cryptographic systems (Shor's algorithm)\n"
        "- Molecular simulation for drug discovery\n"
        "- Optimization problems (logistics, portfolio)\n"
        "- Machine learning acceleration\n\n"
        "**Current State:**\n"
        "- IBM, Google, Microsoft, IonQ, Rigetti are leading players\n"
        "- Google's 'quantum supremacy' demonstration (2019)\n"
        "- Noisy Intermediate-Scale Quantum (NISQ) era\n"
        "- Error correction remains a major challenge\n"
        "- Practical quantum advantage for real-world problems is still emerging"
    ),
    "react": (
        "React is a JavaScript library for building user interfaces, developed by Facebook (Meta). It uses a component-based architecture and a virtual DOM for efficient rendering.\n\n"
        "**Core Concepts:**\n"
        "- **Components:** Reusable, self-contained UI pieces (function or class)\n"
        "- **JSX:** Syntax extension that lets you write HTML-like code in JavaScript\n"
        "- **Props:** Read-only data passed from parent to child components\n"
        "- **State:** Internal, mutable data managed within a component\n"
        "- **Virtual DOM:** In-memory representation of the real DOM for efficient updates\n\n"
        "**Hooks (introduced in React 16.8):**\n"
        "- `useState` — manage component state\n"
        "- `useEffect` — side effects (data fetching, subscriptions)\n"
        "- `useContext` — consume context without nesting\n"
        "- `useRef` — persist values across renders\n"
        "- `useMemo` / `useCallback` — performance optimization\n"
        "- `useReducer` — complex state logic\n\n"
        "**Ecosystem:** React Router (routing), Redux/Zustand (state management), Next.js (SSR/SSG framework), React Native (mobile), Testing Library."
    ),
    "data structures": (
        "Data structures are specialized formats for organizing, storing, and accessing data efficiently.\n\n"
        "**Linear Data Structures:**\n"
        "- **Array:** Fixed-size contiguous memory — O(1) access, O(n) insert/delete\n"
        "- **Linked List:** Nodes with pointers — O(1) insert/delete at head, O(n) access\n"
        "- **Stack:** LIFO (Last In, First Out) — push, pop, peek — O(1) operations\n"
        "- **Queue:** FIFO (First In, First Out) — enqueue, dequeue — O(1) operations\n\n"
        "**Tree Data Structures:**\n"
        "- **Binary Tree:** Each node has at most 2 children\n"
        "- **BST (Binary Search Tree):** Left < Root < Right — O(log n) average search\n"
        "- **AVL/Red-Black Trees:** Self-balancing BSTs — O(log n) guaranteed\n"
        "- **Heap:** Complete binary tree — max-heap or min-heap — O(log n) insert/extract\n"
        "- **Trie:** Prefix tree for strings — O(m) where m is string length\n\n"
        "**Hash-Based:**\n"
        "- **Hash Map/Table:** Key-value pairs — O(1) average lookup\n"
        "- **Hash Set:** Unique elements — O(1) membership test\n\n"
        "**Graph:**\n"
        "- Adjacency list or matrix representation\n"
        "- BFS, DFS, Dijkstra, Bellman-Ford, Kruskal, Prim algorithms"
    ),
    "api": (
        "An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other.\n\n"
        "**Types of APIs:**\n"
        "- **REST (Representational State Transfer):** HTTP-based, stateless, uses JSON/XML. Most common web API style.\n"
        "- **GraphQL:** Query language letting clients request exactly the data they need. Single endpoint.\n"
        "- **gRPC:** High-performance RPC framework using Protocol Buffers. Great for microservices.\n"
        "- **WebSocket:** Full-duplex persistent connection for real-time communication.\n"
        "- **SOAP:** XML-based, enterprise-grade, with strict standards.\n\n"
        "**REST API Concepts:**\n"
        "- HTTP Methods: GET (read), POST (create), PUT (update), PATCH (partial update), DELETE (remove)\n"
        "- Status Codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 404 (Not Found), 500 (Server Error)\n"
        "- Headers: Content-Type, Authorization (Bearer tokens, API keys)\n"
        "- Pagination, filtering, versioning\n\n"
        "**Authentication:** API Keys, OAuth 2.0, JWT (JSON Web Tokens), Basic Auth.\n\n"
        "**Best Practices:** Use nouns in URLs, version your API, handle errors consistently, implement rate limiting, document with OpenAPI/Swagger."
    ),
    "database": (
        "A database is an organized collection of structured data stored and accessed electronically.\n\n"
        "**Relational Databases (SQL):**\n"
        "- Data in tables with rows and columns, relationships via foreign keys\n"
        "- ACID transactions (Atomicity, Consistency, Isolation, Durability)\n"
        "- Examples: PostgreSQL, MySQL, SQLite, Microsoft SQL Server, Oracle\n"
        "- Language: SQL (Structured Query Language) — SELECT, INSERT, UPDATE, DELETE, JOIN\n\n"
        "**NoSQL Databases:**\n"
        "- **Document:** MongoDB, CouchDB — JSON-like documents\n"
        "- **Key-Value:** Redis, DynamoDB — fast cache and simple lookups\n"
        "- **Column-Family:** Cassandra, HBase — wide-column stores for big data\n"
        "- **Graph:** Neo4j, ArangoDB — relationships between entities\n\n"
        "**Key Concepts:**\n"
        "- Normalization (1NF, 2NF, 3NF) vs Denormalization\n"
        "- Indexing (B-Tree, Hash, Full-text) for query performance\n"
        "- Transactions and concurrency control\n"
        "- Replication, sharding, partitioning for scalability\n"
        "- CAP Theorem: Consistency, Availability, Partition tolerance (pick 2)"
    ),
    "cloud computing": (
        "Cloud computing delivers computing services — servers, storage, databases, networking, software, analytics — over the internet ('the cloud').\n\n"
        "**Service Models:**\n"
        "- **IaaS (Infrastructure as a Service):** Virtual machines, storage, networking. Examples: AWS EC2, Google Compute Engine, Azure VMs\n"
        "- **PaaS (Platform as a Service):** Development platforms. Examples: Heroku, Google App Engine, AWS Elastic Beanstalk\n"
        "- **SaaS (Software as a Service):** Complete applications. Examples: Gmail, Salesforce, Slack, Dropbox\n"
        "- **FaaS (Functions as a Service):** Serverless computing. Examples: AWS Lambda, Google Cloud Functions, Azure Functions\n\n"
        "**Major Providers:** Amazon Web Services (AWS), Microsoft Azure, Google Cloud Platform (GCP), IBM Cloud, Oracle Cloud\n\n"
        "**Key Services:** Compute (VMs, containers, serverless), storage (object, block, file), databases (managed SQL/NoSQL), networking (VPC, CDN, load balancing), AI/ML, monitoring, security.\n\n"
        "**Benefits:** Scalability, cost efficiency (pay-as-you-go), global availability, disaster recovery, rapid deployment."
    ),
    "cybersecurity": (
        "Cybersecurity is the practice of protecting systems, networks, and data from digital attacks, unauthorized access, and damage.\n\n"
        "**Key Areas:**\n"
        "- **Network Security:** Firewalls, IDS/IPS, VPNs, network segmentation\n"
        "- **Application Security:** Secure coding, input validation, OWASP Top 10\n"
        "- **Cloud Security:** IAM, encryption, compliance, shared responsibility\n"
        "- **Endpoint Security:** Antivirus, EDR, device management\n"
        "- **Identity & Access Management:** MFA, SSO, RBAC, zero trust\n\n"
        "**Common Threats:**\n"
        "- Phishing and social engineering\n"
        "- Ransomware and malware\n"
        "- SQL injection, XSS, CSRF\n"
        "- Man-in-the-middle attacks\n"
        "- DDoS attacks\n"
        "- Supply chain attacks\n"
        "- Zero-day exploits\n\n"
        "**Frameworks:** NIST Cybersecurity Framework, ISO 27001, CIS Controls, SOC 2.\n\n"
        "**Encryption:** Symmetric (AES), Asymmetric (RSA, ECC), Hashing (SHA-256), TLS/SSL for transport security."
    ),
    "git": (
        "Git is a distributed version control system designed for tracking changes in source code during software development.\n\n"
        "**Core Concepts:**\n"
        "- **Repository:** A project folder tracked by Git\n"
        "- **Commit:** A snapshot of changes with a message\n"
        "- **Branch:** An independent line of development\n"
        "- **Merge:** Combining changes from different branches\n"
        "- **Remote:** A shared repository (GitHub, GitLab, Bitbucket)\n\n"
        "**Essential Commands:**\n"
        "```\ngit init              # Initialize a new repo\ngit clone <url>       # Clone a remote repo\ngit add .             # Stage all changes\ngit commit -m \"msg\"   # Commit staged changes\ngit push origin main  # Push to remote\ngit pull              # Fetch and merge remote changes\ngit branch feature    # Create a branch\ngit checkout feature  # Switch branches\ngit merge feature     # Merge a branch\ngit log --oneline     # View commit history\ngit stash             # Temporarily save changes\ngit diff              # View unstaged changes\n```\n\n"
        "**Workflow:** Feature branches → Pull Requests → Code Review → Merge to main\n\n"
        "**Platforms:** GitHub, GitLab, Bitbucket, Azure DevOps"
    ),
    "docker": (
        "Docker is a platform for developing, shipping, and running applications in containers — lightweight, portable, self-sufficient units of software.\n\n"
        "**Core Concepts:**\n"
        "- **Image:** A read-only template with application code, runtime, libraries, and dependencies\n"
        "- **Container:** A running instance of an image — isolated, lightweight process\n"
        "- **Dockerfile:** Instructions to build an image\n"
        "- **Docker Compose:** Multi-container application orchestration (YAML)\n"
        "- **Registry:** Image storage (Docker Hub, ECR, GCR)\n\n"
        "**Key Commands:**\n"
        "```\ndocker build -t myapp .        # Build image\ndocker run -p 8080:80 myapp    # Run container\ndocker ps                       # List running containers\ndocker stop <id>               # Stop container\ndocker-compose up -d           # Start multi-container app\n```\n\n"
        "**Benefits:** Consistency across environments, rapid deployment, resource efficiency, microservices architecture, CI/CD integration.\n\n"
        "**Orchestration:** Kubernetes (K8s) for managing containers at scale — pods, services, deployments, auto-scaling."
    ),
    "html css": (
        "HTML (HyperText Markup Language) and CSS (Cascading Style Sheets) are the foundational technologies for building web pages.\n\n"
        "**HTML — Structure:**\n"
        "- Semantic elements: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`\n"
        "- Forms: `<input>`, `<select>`, `<textarea>`, `<button>`\n"
        "- Media: `<img>`, `<video>`, `<audio>`, `<canvas>`\n"
        "- Tables: `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<td>`\n\n"
        "**CSS — Styling:**\n"
        "- Selectors: element, class (`.btn`), ID (`#header`), attribute, pseudo-class\n"
        "- Box Model: margin, border, padding, content\n"
        "- Layout: Flexbox (`display: flex`), Grid (`display: grid`), float, position\n"
        "- Responsive: Media queries (`@media`), viewport units (`vw`, `vh`), `clamp()`\n"
        "- Modern: CSS Variables, animations/transitions, `container` queries\n\n"
        "**Best Practices:** Mobile-first design, semantic HTML for accessibility, CSS custom properties for theming, BEM naming convention."
    ),
    "sql": (
        "SQL (Structured Query Language) is the standard language for managing and querying relational databases.\n\n"
        "**Core Operations (CRUD):**\n"
        "```sql\n-- Create\nINSERT INTO users (name, email) VALUES ('Aditya', 'aditya@example.com');\n\n-- Read\nSELECT name, email FROM users WHERE id = 1;\nSELECT * FROM users ORDER BY name LIMIT 10;\n\n-- Update\nUPDATE users SET name = 'Aditya Kumar' WHERE id = 1;\n\n-- Delete\nDELETE FROM users WHERE id = 1;\n```\n\n"
        "**Joins:**\n"
        "- `INNER JOIN` — matching rows in both tables\n"
        "- `LEFT JOIN` — all rows from left + matching from right\n"
        "- `RIGHT JOIN` — all rows from right + matching from left\n"
        "- `FULL OUTER JOIN` — all rows from both tables\n\n"
        "**Advanced:**\n"
        "- Aggregations: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, `HAVING`\n"
        "- Subqueries, CTEs (`WITH` clause), Window Functions (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`)\n"
        "- Indexes, views, stored procedures, triggers, transactions"
    ),
    "system design": (
        "System design is the process of defining the architecture, components, and interfaces of a system to satisfy specified requirements.\n\n"
        "**Key Concepts:**\n"
        "- **Scalability:** Horizontal (more machines) vs Vertical (bigger machine) scaling\n"
        "- **Load Balancing:** Distribute traffic across servers (Round Robin, Least Connections, IP Hash)\n"
        "- **Caching:** Redis, Memcached, CDN caching — reduce database load\n"
        "- **Database Design:** SQL vs NoSQL, sharding, replication, read replicas\n"
        "- **Message Queues:** Kafka, RabbitMQ, SQS — async communication, decoupling\n"
        "- **Microservices:** Independent services vs monolithic architecture\n"
        "- **API Gateway:** Single entry point for multiple services\n"
        "- **CDN:** Content Delivery Network for static assets\n\n"
        "**Design Patterns:** Circuit Breaker, CQRS, Event Sourcing, Saga Pattern, Pub/Sub.\n\n"
        "**Reliability:** Redundancy, failover, health checks, monitoring (Prometheus, Grafana), alerting, chaos engineering."
    ),
}


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
        words = response.split(' ')
        buf = ""
        for w in words:
            buf += w + " "
            if len(buf) >= 6:
                yield buf
                buf = ""
        if buf:
            yield buf

    # ── Classification ──

    def _classify(self, prompt: str) -> str:
        p = prompt.lower().strip()

        if p in ("hi", "hello", "hey", "namaste", "hii", "hola", "sup", "yo",
                 "howdy", "good morning", "good evening", "good night", "hlo"):
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
              "linked list", "binary search", "quicksort", "merge sort",
              "hash map", "binary tree", "rest api", "web scraper",
              "flask", "django", "express", "react app",
              "fibonacci", "dynamic programming", "crud", "async await",
              "decorator", "pytest", "regex", "websocket",
              "program banao", "code likho"]
        return sum(1 for k in kw if k in p)

    def _score_math(self, p: str) -> int:
        long_kw = ["calculate", "solve", "equation", "derivative",
                   "probability", "compute", "evaluate", "simplify",
                   "factorial", "square root", "percentage",
                   "standard deviation"]
        short_kw = ["sin", "cos", "tan"]
        score = sum(1 for k in long_kw if self._word_match(k, p))
        score += sum(1 for k in short_kw if self._word_match(k, p))
        if re.search(r'\d+\s*[\+\-\*/\^%]\s*\d+', p):
            score += 3
        if re.search(r'(?:average|mean|median|mode|variance)\s+of\s+\d', p):
            score += 3
        return score

    def _score_creative(self, p: str) -> int:
        kw = ["write a story", "write a poem", "write an essay", "write a letter",
              "write a speech", "write lyrics", "write a song",
              "poem about", "story about", "essay about",
              "creative writing", "compose", "kahani", "kavita"]
        return sum(1 for k in kw if k in p)

    def _score_image(self, p: str) -> int:
        kw = ["generate image", "create image", "draw a", "generate a picture",
              "create a picture", "make an image", "image banao", "tasveer"]
        return sum(1 for k in kw if k in p)

    def _score_document(self, p: str) -> int:
        kw = ["summarize:", "summarise:", "analyze:", "key points:",
              "summarize this", "analyze this text", "word count of"]
        return sum(1 for k in kw if k in p)

    # ══════════════════════════════════════════════
    #  GENERAL HANDLER — answers ANY question
    # ══════════════════════════════════════════════

    def _handle_general(self, prompt: str) -> str:
        kb = self._check_knowledge_base(prompt)
        if kb:
            return kb

        queries = self._make_queries(prompt)
        all_results = []
        for q in queries:
            results = self._web_search(q)
            if results:
                all_results.extend(results)
                if len(all_results) >= 8:
                    break

        if all_results:
            return self._compose_answer(prompt, all_results)

        return self._fallback(prompt)

    def _check_knowledge_base(self, prompt: str) -> str | None:
        p = prompt.lower()
        best_key = None
        best_score = 0
        for key in KNOWLEDGE:
            key_words = set(key.split())
            prompt_words = set(p.split())
            overlap = len(key_words & prompt_words)
            if overlap >= len(key_words) and overlap > best_score:
                best_score = overlap
                best_key = key
            elif key in p and len(key) > best_score * 4:
                best_key = key
                best_score = len(key) // 4

        if best_key:
            extra = ""
            results = self._web_search(prompt)
            if results:
                extra_pts = self._extract_unique_sentences(results, prompt, limit=4)
                if extra_pts:
                    extra = "\n\n**Latest Information:**\n\n" + "\n\n".join(extra_pts)
            return KNOWLEDGE[best_key] + extra

        return None

    def _make_queries(self, prompt: str) -> list[str]:
        stop = {"a", "an", "the", "is", "are", "was", "were", "what", "how",
                "why", "when", "where", "who", "which", "do", "does", "did",
                "can", "could", "would", "should", "will", "about", "for",
                "to", "of", "in", "on", "at", "by", "with", "from", "me",
                "my", "i", "you", "your", "tell", "explain", "describe",
                "please", "help", "want", "need", "give", "conduct",
                "exhaustive", "examination", "provide", "detailed", "gather",
                "organize", "into", "including", "remaining", "overall",
                "comprehensive", "brief", "discuss", "elaborate"}
        words = prompt.split()
        keywords = [w for w in words if w.lower() not in stop and len(w) > 2]
        queries = []
        if len(keywords) <= 8:
            queries.append(" ".join(keywords))
        else:
            queries.append(" ".join(keywords[:8]))
        if len(keywords) > 4:
            queries.append(" ".join(keywords[:5]))
        queries.append(prompt[:150])
        return queries[:3]

    def _compose_answer(self, prompt: str, results: list) -> str:
        sentences = self._extract_unique_sentences(results, prompt, limit=15)
        if not sentences:
            for r in results[:5]:
                body = r.get("body", r.get("description", r.get("snippet", "")))
                if body and len(body) > 30:
                    sentences.append(body[:500])
        if not sentences:
            return self._fallback(prompt)

        response = ""
        for s in sentences:
            if not s.endswith('.'):
                s += '.'
            response += s + "\n\n"

        sources = []
        seen = set()
        for r in results[:5]:
            t = r.get("title", "")
            l = r.get("href", r.get("url", r.get("link", "")))
            if t and t not in seen:
                seen.add(t)
                sources.append(f"- [{t}]({l})" if l else f"- {t}")
        if sources:
            response += "---\n**Sources:**\n" + "\n".join(sources[:4])
        return response.strip()

    def _extract_unique_sentences(self, results: list, prompt: str, limit: int = 12) -> list[str]:
        all_sentences = []
        seen = set()
        for r in results:
            body = r.get("body", r.get("description", r.get("snippet", "")))
            if not body:
                continue
            for s in re.split(r'(?<=[.!?])\s+', body):
                s = s.strip()
                if len(s) < 30 or len(s) > 600:
                    continue
                h = hashlib.md5(s[:50].lower().encode()).hexdigest()
                if h in seen:
                    continue
                seen.add(h)
                score = self._relevance(s, prompt)
                if score > 0.03:
                    all_sentences.append((score, s))

        all_sentences.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in all_sentences[:limit]]

    def _relevance(self, sentence: str, query: str) -> float:
        stop = {"a", "an", "the", "is", "are", "was", "were", "and", "or",
                "but", "in", "on", "at", "to", "for", "of", "with", "by",
                "from", "this", "that", "it", "be", "has", "have", "had",
                "not", "as", "if", "do", "does", "will", "can", "about"}
        q_words = set(query.lower().split()) - stop
        s_words = set(sentence.lower().split()) - stop
        q_sig = {w for w in q_words if len(w) > 2}
        s_sig = {w for w in s_words if len(w) > 2}
        if not q_sig:
            return 0.1
        overlap = len(q_sig & s_sig) / max(len(q_sig), 1)
        junk = ["click", "subscribe", "cookie", "privacy", "sign up", "newsletter", "advertisement"]
        if any(j in sentence.lower() for j in junk):
            return 0
        return overlap * min(len(sentence) / 100, 1.5)

    def _fallback(self, prompt: str) -> str:
        topic = self._extract_topic(prompt)
        if len(prompt.split()) > 15:
            return (
                f"I attempted to search for comprehensive information about this topic but "
                f"couldn't connect to web search at this moment.\n\n"
                f"**Your question covers:** {topic[:200]}\n\n"
                f"Please try again in a moment for a thorough, sourced response.\n\n"
                f"**What I can do right now:**\n"
                f"- Write code in Python, JavaScript, HTML, SQL\n"
                f"- Solve math problems step by step\n"
                f"- Write stories, poems, essays, speeches\n"
                f"- Summarize and analyze text you paste in"
            )
        return (
            f"I couldn't connect to web search to answer about **{topic}**. "
            f"Please try again shortly.\n\n"
            f"I can help with **coding**, **math**, **creative writing**, "
            f"and **text analysis** right now."
        )

    def _extract_topic(self, prompt: str) -> str:
        topic = re.sub(
            r'^(what is|what are|how does|how do|how to|why|explain|describe|'
            r'tell me about|define|research|conduct|provide|give me|discuss|'
            r'analyze|examine|compare)\s+',
            '', prompt, flags=re.IGNORECASE).strip()
        topic = re.sub(r'^(a|an|the|detailed|exhaustive|comprehensive)\s+',
                       '', topic, flags=re.IGNORECASE).strip()
        return topic[:150] if topic else prompt[:150]

    # ── Greeting / System ──

    def _handle_greeting(self, prompt: str) -> str:
        return random.choice([
            "Hello! How can I help you today? I can answer questions, write code, solve math, create stories, and research any topic.",
            "Hey there! What would you like to work on?",
            "Hi! I'm ready to help. Ask me anything.",
        ])

    def _handle_system(self, prompt: str) -> str:
        return (
            "I'm **NAGRO 4.1** — Neural Adaptive Generative Reasoning Operator, "
            "created by Aditya Kumar.\n\n"
            "**Capabilities:**\n"
            "- Answer questions on any topic (real-time web search)\n"
            "- Write code in Python, JavaScript, HTML, SQL, and more\n"
            "- Solve math step by step\n"
            "- Write stories, poems, essays, speeches\n"
            "- Analyze and summarize documents\n"
            "- Generate images (procedural engine)\n"
            "- RAG (document ingestion and retrieval)\n"
            "- Multi-step agentic reasoning\n\n"
            "100% self-built. No external AI models. 200K context window."
        )

    # ── Code ──

    def _handle_code(self, prompt: str) -> str:
        from nagro.core.code_templates import find_template, detect_language
        lang = detect_language(prompt)
        template = find_template(prompt, lang)
        if template:
            r = f"```{template['lang']}\n{template['code']}\n```\n\n"
            r += f"**Explanation:** {template['explanation']}"
            if "complexity" in template:
                r += f"\n\n**Complexity:** {template['complexity']}"
            return r

        code = self._generate_code(prompt, lang)
        if code:
            return code

        results = self._web_search(prompt + " code example")
        if results:
            return self._compose_answer(prompt, results)
        return "I can help with code! Try: \"Write a Python quicksort\", \"Create a REST API\", \"JavaScript fetch example\"."

    def _generate_code(self, prompt: str, lang: str) -> str | None:
        p = prompt.lower()
        codes = {
            "reverse string": ("def reverse_string(s):\n    return s[::-1]\n\nprint(reverse_string('hello'))  # olleh", "Reverses using slice notation."),
            "palindrome": ("def is_palindrome(s):\n    c = ''.join(ch.lower() for ch in s if ch.isalnum())\n    return c == c[::-1]\n\nprint(is_palindrome('racecar'))  # True", "Checks if string reads same both ways."),
            "prime": ("def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0: return False\n    return True\n\nprint([x for x in range(2,50) if is_prime(x)])", "Tests divisibility up to sqrt(n). O(sqrt(n))."),
            "two sum": ("def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target-n], i]\n        seen[n] = i\n    return []\n\nprint(two_sum([2,7,11,15], 9))", "Hash map — O(n) time."),
            "factorial": ("def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)\n\nprint(factorial(10))  # 3628800", "Recursive O(n)."),
            "password": ("import secrets, string\ndef gen_password(n=16):\n    chars = string.ascii_letters + string.digits + '!@#$%'\n    return ''.join(secrets.choice(chars) for _ in range(n))\n\nprint(gen_password())", "Cryptographically secure."),
        }
        for key, (code, explanation) in codes.items():
            if key in p:
                return f"```python\n{code}\n```\n\n**Explanation:** {explanation}"
        return None

    # ── Math ──

    def _handle_math(self, prompt: str) -> str:
        result = self._solve_math(prompt)
        if result:
            return result
        stats = self._solve_stats(prompt)
        if stats:
            return stats
        results = self._web_search(prompt + " step by step solution")
        if results:
            return self._compose_answer(prompt, results)
        return "Provide a math expression like `2 + 3 * 4`, `sqrt(16)`, or `average of 10, 20, 30`."

    def _solve_math(self, prompt: str) -> str | None:
        expr = self._extract_expr(prompt)
        if not expr:
            return None
        safe = {"sqrt": math.sqrt, "abs": abs, "round": round,
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "log": math.log, "log2": math.log2, "log10": math.log10,
                "exp": math.exp, "pow": pow, "factorial": math.factorial,
                "ceil": math.ceil, "floor": math.floor,
                "pi": math.pi, "e": math.e}
        try:
            tree = ast.parse(expr, mode='eval')
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id not in safe:
                    return None
                if isinstance(node, ast.Attribute):
                    return None
            result = eval(expr, {"__builtins__": {}}, safe)
            r = f"**Expression:** `{expr}`\n\n**Result:** `{result}`"
            if isinstance(result, float) and result != int(result):
                r += f"\n\nDecimal: {result:.10f}"
            return r
        except:
            return None

    def _solve_stats(self, prompt: str) -> str | None:
        p = prompt.lower()
        nums = [float(n) for n in re.findall(r'[-+]?\d*\.?\d+', prompt)]
        if len(nums) < 2:
            return None
        if self._word_match("average", p) or self._word_match("mean", p) or "average of" in p or "mean of" in p:
            return f"**Numbers:** {nums}\n**Mean:** `{statistics.mean(nums)}`\nFormula: {sum(nums)} / {len(nums)} = {statistics.mean(nums)}"
        if self._word_match("median", p) or "median of" in p:
            return f"**Numbers:** {nums}\n**Sorted:** {sorted(nums)}\n**Median:** `{statistics.median(nums)}`"
        return None

    def _extract_expr(self, prompt: str) -> str | None:
        p = prompt.replace("×", "*").replace("÷", "/").replace("^", "**").replace("√", "sqrt")
        m = re.search(r'(?:calculate|compute|solve|evaluate|what is|what\'s|find)\s+([\d\s\+\-\*/\.\(\)\w]+)', p, re.I)
        if m:
            e = m.group(1).strip()
            e = re.sub(r'(\d+)\s*!', r'factorial(\1)', e)
            if re.search(r'\d', e) and len(e) < 80:
                return e
        m = re.search(r'(\d+(?:\.\d+)?\s*[\+\-\*/\*]{1,2}\s*\d+(?:\.\d+)?(?:\s*[\+\-\*/\*]{1,2}\s*\d+(?:\.\d+)?)*)', p)
        if m:
            return m.group(1).strip()
        m = re.search(r'((?:sqrt|factorial|log|log10|sin|cos|tan)\(\s*[\d.]+\s*\))', p, re.I)
        if m:
            return m.group(1)
        return None

    # ── Creative ──

    def _handle_creative(self, prompt: str) -> str:
        p = prompt.lower()
        if "poem" in p or "poetry" in p:
            return self._gen_poem(prompt)
        if "story" in p or "tale" in p:
            return self._gen_story(prompt)
        if "speech" in p:
            return self._gen_speech(prompt)
        if "lyrics" in p or "song" in p:
            return self._gen_lyrics(prompt)
        if "letter" in p or "email" in p:
            return self._gen_letter(prompt)
        return self._gen_essay(prompt)

    def _gen_poem(self, prompt):
        topic = re.sub(r'(write|create|compose)\s+(a\s+)?(poem|poetry)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "creation"
        return f"## {topic.title()}\n\n*In the heart of {topic},*\n*where shadows meet the light,*\n*A truth unfolds like morning dew,*\n*transforming dark to bright.*\n\n*Each moment holds a universe,*\n*of wonder yet untold,*\n*Through {topic}, we find the words,*\n*more precious far than gold.*\n\n*So let the world keep turning,*\n*let stars illuminate the way,*\n*For in the dance of {topic},*\n*we find our brightest day.*"

    def _gen_story(self, prompt):
        topic = re.sub(r'(write|create|tell)\s+(me\s+)?(a\s+)?(short\s+)?(story|tale)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "adventure"
        return f"## {topic.title()}\n\nIt began on a day like any other — the sky stretched endlessly, the world humming with quiet possibility.\n\nIn the heart of {topic}, a truth emerged hidden in plain sight — the kind of revelation that makes you question everything.\n\nThrough challenges that tested every limit and moments of clarity illuminating the way forward, the journey proved to be not just a destination but a transformation.\n\nThey say every ending is just a new beginning. And in this story, that truth resonated louder than ever."

    def _gen_speech(self, prompt):
        topic = re.sub(r'(write|create)\s+(a\s+)?speech\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "progress"
        return f"## Speech: {topic.title()}\n\n*Ladies and gentlemen,*\n\nToday I want to talk about **{topic}**. In our rapidly changing world, understanding this isn't just important — it's essential.\n\nThe question isn't whether {topic} will shape our future — it already is. The question is what we'll do about it.\n\nLet us move forward with purpose and embrace this as an opportunity.\n\n*Thank you.*"

    def _gen_lyrics(self, prompt):
        topic = re.sub(r'(write|create)\s+(a\s+)?(song|lyrics)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "dreams"
        return f"## {topic.title()}\n\n**[Verse 1]**\nWalking down this road alone,\nSearching for a place called home,\n{topic.title()} — it's calling me,\nSetting all my spirit free.\n\n**[Chorus]**\nWe rise, we fall, we rise again,\nThrough the sunshine and the rain,\n{topic.title()} — don't let it fade,\nThis is the choice that we have made."

    def _gen_letter(self, prompt):
        topic = re.sub(r'(write|draft)\s+(a\s+)?(letter|email)\s*(about|to)?\s*', '', prompt, flags=re.I).strip() or "inquiry"
        return f"**Subject: {topic.title()}**\n\nDear [Recipient],\n\nI hope this message finds you well. I am writing regarding **{topic}**.\n\n[Your main points]\n\nThank you for your time.\n\nBest regards,\n[Your Name]"

    def _gen_essay(self, prompt):
        topic = re.sub(r'(write)\s+(an?\s+)?(essay|article|blog)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or prompt
        results = self._web_search(topic)
        if results:
            return self._compose_answer(topic, results)
        return f"## {topic.title()}\n\n{topic.capitalize()} is a subject that continues to shape our understanding of the world. As we explore its dimensions, we gain insights for better decisions.\n\nThe landscape continues to evolve, driven by technology and shifting societal needs."

    # ── Image / Document ──

    def _handle_image(self, prompt: str) -> str:
        return f"**Prompt:** {prompt}\n\nImage generation available via `/api/v1/image/generate` endpoint. Send a POST request to create procedural art."

    def _handle_document(self, prompt: str) -> str:
        p = prompt.lower()
        if "summarize" in p or "summarise" in p:
            text = re.sub(r'(summarize|summarise)\s*:?\s*', '', prompt, flags=re.I).strip()
            if len(text) > 50:
                return self._summarize(text)
        if "analyze" in p:
            text = re.sub(r'analyze\s*:?\s*', '', prompt, flags=re.I).strip()
            if len(text) > 50:
                return self._analyze(text)
        return "Use: `Summarize: [text]` or `Analyze: [text]`"

    def _summarize(self, text):
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]
        if not sents:
            return "Could not extract sentences."
        freq = Counter(text.lower().split())
        scored = sorted([(sum(freq.get(w, 0) for w in s.lower().split() if len(w) > 3) / (len(s.split()) + 1), s) for s in sents], reverse=True)
        top = [s for _, s in scored[:5]]
        ordered = [s for s in sents if s in top]
        return f"**Summary ({len(text.split())} words → {sum(len(s.split()) for s in ordered)} words):**\n\n" + "\n\n".join(ordered)

    def _analyze(self, text):
        words = text.split()
        sents = [s for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]
        freq = Counter(w.lower() for w in words if len(w) > 4)
        kw = [(w, c) for w, c in freq.most_common(10)]
        return f"**Words:** {len(words)} | **Sentences:** {len(sents)} | **Avg words/sentence:** {len(words)/max(len(sents),1):.1f}\n\n**Keywords:** " + ", ".join(f"{w} ({c})" for w, c in kw)

    # ── Search ──

    def _web_search(self, query: str) -> list:
        try:
            return self.search.search(query, max_results=8)
        except:
            return []
