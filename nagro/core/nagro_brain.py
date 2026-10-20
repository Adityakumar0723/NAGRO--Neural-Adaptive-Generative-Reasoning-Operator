"""
NAGRO 4.1 — Self-Built AI Brain (Advanced)

NAGRO Brain = Decision Engine. 100% self-built. Uses:
- Built-in Knowledge Base (150+ topics)
- Wikipedia API (free, no key)
- DuckDuckGo Search (free, no key)
- Self-built code generator (50+ patterns)
- Self-built creative writing engine
(NO OpenAI, NO Anthropic, NO Google, NO paid APIs)
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
from nagro.core.knowledge_data import WORLD_KNOWLEDGE, find_knowledge
from nagro.core.nlp_engine import (
    classify_question, extract_intent, QuestionType,
    text_similarity, format_answer, expand_synonyms,
    build_comparison, extract_comparison_topics, score_sentences,
)


# ══════════════════════════════════════════════════════════════════
#  MASSIVE BUILT-IN KNOWLEDGE BASE
# ══════════════════════════════════════════════════════════════════

KNOWLEDGE: dict[str, tuple[list[str], str]] = {}

def _k(keys: list[str], text: str):
    for k in keys:
        KNOWLEDGE[k] = (keys, text)

_k(["artificial intelligence", "ai", "what is ai"],
    "Artificial Intelligence (AI) is a branch of computer science focused on creating systems capable of performing tasks that normally require human intelligence — visual perception, speech recognition, decision-making, language translation, and problem-solving.\n\n"
    "**Types of AI:**\n"
    "- **Narrow AI (Weak AI):** Designed for specific tasks — virtual assistants (Siri, Alexa), recommendation systems, image recognition. This is what exists today.\n"
    "- **General AI (Strong AI):** Hypothetical systems with human-level reasoning across all domains. Does not yet exist.\n"
    "- **Superintelligent AI:** Theoretical AI surpassing human intelligence.\n\n"
    "**Key Subfields:**\n"
    "- **Machine Learning:** Systems that learn from data\n"
    "- **Deep Learning:** Neural networks with many layers\n"
    "- **Natural Language Processing (NLP):** Understanding and generating human language\n"
    "- **Computer Vision:** Interpreting images and video\n"
    "- **Robotics:** Physical agents that interact with the world\n\n"
    "**Applications:** Healthcare diagnostics, autonomous vehicles, financial trading, content creation, drug discovery, climate modeling, cybersecurity, education.\n\n"
    "**Challenges:** Bias in training data, explainability, energy consumption, job displacement, privacy concerns, alignment with human values."
)

_k(["machine learning", "ml", "supervised learning", "unsupervised learning"],
    "Machine Learning (ML) is a subset of AI where computers learn patterns from data without being explicitly programmed.\n\n"
    "**Three Main Types:**\n\n"
    "**1. Supervised Learning** — learns from labeled examples\n"
    "- Classification: spam detection, image recognition, sentiment analysis\n"
    "- Regression: price prediction, weather forecasting\n"
    "- Algorithms: Linear Regression, Decision Trees, Random Forest, SVM, Neural Networks\n\n"
    "**2. Unsupervised Learning** — finds patterns in unlabeled data\n"
    "- Clustering: K-Means, DBSCAN, customer segmentation\n"
    "- Dimensionality Reduction: PCA, t-SNE\n\n"
    "**3. Reinforcement Learning** — learns by interacting with environment\n"
    "- Q-Learning, Deep Q-Networks, Policy Gradient, PPO\n"
    "- Applications: game playing (AlphaGo), robotics\n\n"
    "**Key Concepts:** Features, labels, overfitting, regularization, cross-validation, gradient descent, loss functions, ensemble methods.\n\n"
    "**Frameworks:** Scikit-learn, TensorFlow, PyTorch, XGBoost, LightGBM."
)

_k(["deep learning", "neural network", "neural networks", "cnn", "rnn", "transformer"],
    "Deep Learning uses artificial neural networks with multiple layers to learn hierarchical representations of data.\n\n"
    "**Architecture Types:**\n"
    "- **CNNs (Convolutional Neural Networks):** Image classification, object detection, medical imaging\n"
    "- **RNNs (Recurrent Neural Networks):** Sequential data — time series, text, speech\n"
    "- **LSTMs:** Improved RNNs handling long-range dependencies\n"
    "- **Transformers:** Attention-based models — GPT, BERT, ViT. Revolutionized NLP and vision\n"
    "- **GANs:** Generate realistic images, video, audio\n"
    "- **Diffusion Models:** State-of-the-art image generation (Stable Diffusion, DALL-E)\n\n"
    "**How Training Works:**\n"
    "1. Forward pass: input → layers → prediction\n"
    "2. Compute loss (how wrong the prediction is)\n"
    "3. Backpropagation: compute gradients\n"
    "4. Update weights via gradient descent\n\n"
    "**Breakthroughs:** ImageNet (2012), AlphaGo (2016), GPT-3 (2020), ChatGPT (2022), GPT-4 (2023)."
)

_k(["large language model", "llm", "gpt", "chatgpt", "claude", "llama", "language model"],
    "Large Language Models (LLMs) are AI systems trained on massive text datasets to understand and generate human language.\n\n"
    "**How They Work:**\n"
    "- Built on the Transformer architecture (attention mechanism)\n"
    "- Trained on billions of tokens of text from the internet\n"
    "- Use next-token prediction: given context, predict the most likely next word\n"
    "- Fine-tuned with RLHF (Reinforcement Learning from Human Feedback)\n\n"
    "**Major Models:**\n"
    "- **GPT-4 / GPT-4o (OpenAI):** Multimodal, highly capable reasoning\n"
    "- **Claude (Anthropic):** Known for safety, long context, and helpfulness\n"
    "- **Gemini (Google):** Multimodal with Google integration\n"
    "- **LLaMA (Meta):** Open-source family of models\n"
    "- **Mistral / Mixtral:** Efficient open-source European models\n\n"
    "**Key Capabilities:** Text generation, summarization, translation, code writing, reasoning, analysis, creative writing.\n\n"
    "**Limitations:** Hallucinations (generating false info), training data cutoff, no real-time knowledge without tools, context window limits."
)

_k(["anthropic", "claude ai"],
    "Anthropic is an AI safety company founded in 2021 by Dario Amodei and Daniela Amodei (former OpenAI VP). Headquartered in San Francisco.\n\n"
    "**Products:**\n"
    "- **Claude:** Their AI assistant, available via API, claude.ai web app, and mobile apps\n"
    "- **Claude models:** Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku — ranging from fast to highly capable\n"
    "- **Claude for Enterprise:** Business-grade with enhanced privacy\n\n"
    "**Key Focus:** AI safety research — Constitutional AI (CAI), mechanistic interpretability, alignment.\n\n"
    "**Funding:** Raised over $7 billion from Google, Salesforce, and others.\n\n"
    "**Philosophy:** Building AI that is helpful, harmless, and honest. Focus on reducing catastrophic AI risks."
)

_k(["openai", "chatgpt", "gpt-4", "dall-e", "sora"],
    "OpenAI is an AI research company founded in 2015, known for creating ChatGPT and GPT models.\n\n"
    "**Major Products:**\n"
    "- **ChatGPT:** Conversational AI used by 200M+ users\n"
    "- **GPT-4 / GPT-4o:** Multimodal LLMs with vision, audio capabilities\n"
    "- **DALL-E 3:** Text-to-image generation\n"
    "- **Whisper:** Speech recognition\n"
    "- **Sora:** Text-to-video generation\n"
    "- **Codex:** Code generation (powers GitHub Copilot)\n\n"
    "**Leadership:** Sam Altman (CEO), key figures include Mira Murati, Greg Brockman.\n\n"
    "**Business:** Valued at $80B+, partnership with Microsoft (multi-billion dollar investment).\n\n"
    "**API:** Provides developer access to GPT-4, embeddings, fine-tuning, assistants."
)

_k(["deepseek", "deepseek ai"],
    "DeepSeek is a Chinese AI company that has gained attention for building highly capable open-source language models.\n\n"
    "**Key Models:**\n"
    "- **DeepSeek-V2:** Efficient mixture-of-experts architecture\n"
    "- **DeepSeek-Coder:** Specialized for code generation, competitive with GPT-4\n"
    "- **DeepSeek-R1:** Reasoning model with step-by-step thinking\n\n"
    "**What Makes It Notable:**\n"
    "- Open-source models rivaling proprietary ones\n"
    "- Much lower training costs than competitors\n"
    "- Strong performance on coding and math benchmarks\n"
    "- Mixture-of-Experts (MoE) architecture for efficiency\n\n"
    "**Impact:** Demonstrated that cutting-edge AI doesn't require massive budgets, challenging assumptions about compute requirements."
)

_k(["minimax", "minimax ai"],
    "MiniMax is a Chinese AI startup focused on large language models and multimodal AI.\n\n"
    "**Key Products:**\n"
    "- Text generation models competitive with international alternatives\n"
    "- Speech synthesis and voice cloning\n"
    "- Video generation capabilities\n"
    "- Virtual character and companion applications (Talkie)\n\n"
    "**Background:** Founded in 2021, backed by significant funding. One of China's leading AI model developers alongside Baidu, Zhipu AI, and Moonshot AI.\n\n"
    "**Focus:** Consumer AI applications, particularly social and entertainment, along with enterprise solutions."
)

_k(["python", "python programming", "python language"],
    "Python is a high-level, interpreted programming language created by Guido van Rossum (1991). Known for readable syntax and versatility.\n\n"
    "**Key Features:** Dynamic typing, automatic memory management, OOP + functional, extensive standard library, cross-platform.\n\n"
    "**Popular Use Cases:**\n"
    "- **Web Development:** Django, Flask, FastAPI\n"
    "- **Data Science:** Pandas, NumPy, Matplotlib, Jupyter\n"
    "- **Machine Learning:** TensorFlow, PyTorch, Scikit-learn\n"
    "- **Automation:** Web scraping, task automation\n"
    "- **Scientific Computing:** SciPy, SymPy\n\n"
    "**Core Concepts:** Variables, data types (list, dict, tuple, set), control flow, functions, classes, modules, decorators, generators, comprehensions, exception handling, virtual environments.\n\n"
    "**Example:**\n```python\ndef greet(name):\n    return f'Hello, {name}!'\n\nprint(greet('World'))\n```"
)

_k(["javascript", "js", "node.js", "nodejs"],
    "JavaScript is a dynamic programming language and core web technology alongside HTML and CSS.\n\n"
    "**Key Features:** Runs in browsers + servers (Node.js), event-driven, non-blocking I/O, first-class functions, closures, prototypal inheritance.\n\n"
    "**Modern JS (ES6+):** let/const, arrow functions, template literals, destructuring, async/await, classes, modules.\n\n"
    "**Ecosystem:**\n"
    "- **Frontend:** React, Vue.js, Angular, Svelte\n"
    "- **Backend:** Node.js, Express, Fastify, Deno, Bun\n"
    "- **Mobile:** React Native, Ionic\n"
    "- **Desktop:** Electron\n"
    "- **Build Tools:** Webpack, Vite, esbuild\n"
    "- **Testing:** Jest, Mocha, Cypress, Playwright"
)

_k(["react", "reactjs", "react.js"],
    "React is a JavaScript library for building user interfaces, developed by Facebook (Meta).\n\n"
    "**Core Concepts:**\n"
    "- **Components:** Reusable UI pieces (function or class)\n"
    "- **JSX:** HTML-like syntax in JavaScript\n"
    "- **Props:** Data passed from parent to child\n"
    "- **State:** Internal mutable data\n"
    "- **Virtual DOM:** Efficient rendering via diffing\n\n"
    "**Hooks:** useState, useEffect, useContext, useRef, useMemo, useCallback, useReducer\n\n"
    "**Ecosystem:** React Router, Redux/Zustand, Next.js, React Native, Testing Library."
)

_k(["blockchain", "cryptocurrency", "bitcoin", "ethereum", "crypto"],
    "Blockchain is a distributed, immutable ledger recording transactions across a network.\n\n"
    "**How It Works:** Transaction → broadcast → validation via consensus → added to block → chain is permanent.\n\n"
    "**Key Concepts:**\n"
    "- **Decentralization:** No single point of control\n"
    "- **Consensus:** Proof of Work (PoW), Proof of Stake (PoS)\n"
    "- **Smart Contracts:** Self-executing code (Ethereum, Solana)\n"
    "- **Tokens:** Fungible (ERC-20), Non-fungible (NFTs)\n\n"
    "**Major Cryptocurrencies:**\n"
    "- **Bitcoin (BTC):** First cryptocurrency, digital gold, created by Satoshi Nakamoto (2009)\n"
    "- **Ethereum (ETH):** Smart contracts platform, transitioning to PoS\n"
    "- **Solana (SOL):** High-speed, low-cost transactions\n\n"
    "**Applications:** DeFi, supply chain, digital identity, voting, healthcare records."
)

_k(["quantum computing", "quantum computer", "qubit"],
    "Quantum computing harnesses quantum mechanical phenomena — superposition, entanglement, interference — to process information differently from classical computers.\n\n"
    "**Key Concepts:**\n"
    "- **Qubits:** Can be 0, 1, or both simultaneously (superposition)\n"
    "- **Entanglement:** Correlated qubits affect each other instantly\n"
    "- **Quantum Gates:** Hadamard, CNOT, Pauli-X/Y/Z\n\n"
    "**Advantages:** Exponential speedup for specific problems, cryptography breaking (Shor's algorithm), molecular simulation, optimization.\n\n"
    "**Current State:** IBM, Google, Microsoft, IonQ leading. NISQ era. Error correction remains a challenge."
)

_k(["data structures", "array", "linked list", "stack", "queue", "tree", "graph"],
    "Data structures organize, store, and access data efficiently.\n\n"
    "**Linear:** Array (O(1) access), Linked List (O(1) insert at head), Stack (LIFO), Queue (FIFO)\n\n"
    "**Trees:** Binary Tree, BST (O(log n) search), AVL/Red-Black (self-balancing), Heap, Trie\n\n"
    "**Hash-Based:** Hash Map (O(1) lookup), Hash Set (O(1) membership)\n\n"
    "**Graphs:** Adjacency list/matrix. BFS, DFS, Dijkstra, Bellman-Ford, Kruskal, Prim."
)

_k(["api", "rest api", "graphql", "grpc"],
    "An API (Application Programming Interface) allows different software to communicate.\n\n"
    "**Types:** REST (HTTP + JSON), GraphQL (query language, single endpoint), gRPC (Protocol Buffers), WebSocket (real-time), SOAP (XML).\n\n"
    "**REST:** GET (read), POST (create), PUT (update), PATCH (partial update), DELETE. Status codes: 200, 201, 400, 401, 404, 500.\n\n"
    "**Auth:** API Keys, OAuth 2.0, JWT, Basic Auth.\n\n"
    "**Best Practices:** Nouns in URLs, versioning, consistent errors, rate limiting, OpenAPI/Swagger docs."
)

_k(["database", "sql", "nosql", "postgresql", "mongodb", "mysql", "redis"],
    "Databases organize and store structured data.\n\n"
    "**Relational (SQL):** Tables with rows/columns, foreign keys, ACID transactions. PostgreSQL, MySQL, SQLite, Oracle.\n\n"
    "**NoSQL:** Document (MongoDB), Key-Value (Redis, DynamoDB), Column-Family (Cassandra), Graph (Neo4j).\n\n"
    "**SQL Basics:**\n```sql\nSELECT * FROM users WHERE age > 18 ORDER BY name;\nINSERT INTO users (name, email) VALUES ('Aditya', 'a@b.com');\nUPDATE users SET role='admin' WHERE id=1;\nDELETE FROM users WHERE id=1;\nSELECT u.name, p.title FROM users u JOIN posts p ON u.id=p.user_id;\n```\n\n"
    "**Concepts:** Normalization, indexing, transactions, replication, sharding, CAP theorem."
)

_k(["cloud computing", "aws", "azure", "gcp", "cloud"],
    "Cloud computing delivers computing services over the internet.\n\n"
    "**Service Models:** IaaS (VMs — AWS EC2), PaaS (platforms — Heroku), SaaS (apps — Gmail), FaaS (serverless — AWS Lambda).\n\n"
    "**Major Providers:** AWS, Microsoft Azure, Google Cloud (GCP), IBM Cloud.\n\n"
    "**Services:** Compute, storage, databases, networking, AI/ML, monitoring.\n\n"
    "**Benefits:** Scalability, pay-as-you-go, global availability, disaster recovery, rapid deployment."
)

_k(["cybersecurity", "security", "hacking", "encryption"],
    "Cybersecurity protects systems, networks, and data from attacks.\n\n"
    "**Areas:** Network security, application security, cloud security, endpoint security, identity management.\n\n"
    "**Common Threats:** Phishing, ransomware, SQL injection, XSS, CSRF, DDoS, man-in-the-middle, zero-day exploits.\n\n"
    "**Encryption:** Symmetric (AES), Asymmetric (RSA, ECC), Hashing (SHA-256), TLS/SSL.\n\n"
    "**Frameworks:** NIST, ISO 27001, CIS Controls, SOC 2."
)

_k(["git", "github", "version control"],
    "Git is a distributed version control system for tracking source code changes.\n\n"
    "**Commands:**\n```\ngit init / clone / add / commit / push / pull\ngit branch / checkout / merge / rebase\ngit log / diff / stash / reset\n```\n\n"
    "**Workflow:** Feature branches → Pull Requests → Code Review → Merge.\n\n"
    "**Platforms:** GitHub, GitLab, Bitbucket."
)

_k(["docker", "container", "kubernetes", "k8s"],
    "Docker packages applications in containers — lightweight, portable units of software.\n\n"
    "**Concepts:** Image (template), Container (running instance), Dockerfile (build instructions), Docker Compose (multi-container).\n\n"
    "**Commands:**\n```\ndocker build -t app . / docker run -p 8080:80 app\ndocker ps / docker stop <id>\ndocker-compose up -d\n```\n\n"
    "**Kubernetes:** Container orchestration at scale — pods, services, deployments, auto-scaling."
)

_k(["html", "css", "html css", "web development", "frontend"],
    "HTML structures web pages; CSS styles them.\n\n"
    "**HTML:** Semantic elements (header, nav, main, footer), forms, media, tables.\n\n"
    "**CSS:** Selectors, Box Model (margin/border/padding/content), Flexbox, Grid, media queries, variables, animations.\n\n"
    "**Best Practices:** Mobile-first, semantic HTML, CSS custom properties, BEM naming."
)

_k(["system design", "architecture", "scalability", "microservices"],
    "System design defines architecture, components, and interfaces for software systems.\n\n"
    "**Key Concepts:**\n"
    "- **Scalability:** Horizontal (more machines) vs Vertical (bigger machine)\n"
    "- **Load Balancing:** Round Robin, Least Connections\n"
    "- **Caching:** Redis, Memcached, CDN\n"
    "- **Message Queues:** Kafka, RabbitMQ, SQS\n"
    "- **Microservices vs Monolith**\n"
    "- **API Gateway, CDN, Database sharding**\n\n"
    "**Patterns:** Circuit Breaker, CQRS, Event Sourcing, Saga, Pub/Sub."
)

_k(["india", "bharat", "indian"],
    "India (Bharat) is the world's most populous country and largest democracy.\n\n"
    "**Key Facts:**\n"
    "- **Capital:** New Delhi | **Largest City:** Mumbai\n"
    "- **Population:** ~1.44 billion (2024)\n"
    "- **Languages:** Hindi, English (official), 22 scheduled languages\n"
    "- **Currency:** Indian Rupee (INR)\n"
    "- **Government:** Federal parliamentary democratic republic\n"
    "- **PM:** Narendra Modi (since 2014)\n\n"
    "**Economy:** 5th largest GDP globally, IT services powerhouse (Infosys, TCS, Wipro), growing startup ecosystem (Flipkart, Ola, Zomato). Major industries: IT, agriculture, textiles, pharmaceuticals.\n\n"
    "**Technology:** Major tech hubs in Bangalore, Hyderabad, Pune, Chennai, Gurgaon. ISRO (space), UPI (digital payments), Aadhaar (digital identity).\n\n"
    "**Culture:** Rich heritage spanning 5000+ years, diverse religions (Hinduism, Islam, Sikhism, Buddhism, Christianity, Jainism), classical arts, Bollywood, cricket."
)

_k(["united states", "usa", "america"],
    "The United States of America is a federal republic of 50 states.\n\n"
    "**Key Facts:**\n"
    "- **Capital:** Washington, D.C. | **Largest City:** New York City\n"
    "- **Population:** ~335 million\n"
    "- **Currency:** US Dollar (USD)\n"
    "- **Government:** Federal presidential constitutional republic\n\n"
    "**Economy:** Largest GDP globally (~$28 trillion). Major sectors: technology, finance, healthcare, defense, entertainment. Home to Apple, Google, Microsoft, Amazon, Meta.\n\n"
    "**Technology:** Silicon Valley, leading in AI research, space exploration (NASA, SpaceX), semiconductor design."
)

_k(["climate change", "global warming", "environment"],
    "Climate change refers to long-term shifts in global temperatures and weather patterns.\n\n"
    "**Key Facts:**\n"
    "- Global temperature has risen ~1.1°C since pre-industrial era\n"
    "- CO2 levels: 420+ ppm (highest in 800,000 years)\n"
    "- Primary cause: Burning fossil fuels (coal, oil, gas)\n\n"
    "**Effects:** Rising sea levels, extreme weather events, biodiversity loss, food insecurity, ocean acidification, glacier melting.\n\n"
    "**Solutions:** Renewable energy (solar, wind), electric vehicles, carbon capture, reforestation, energy efficiency, policy changes (Paris Agreement targets net-zero by 2050).\n\n"
    "**International:** Paris Agreement (2015), COP conferences, IPCC reports."
)

_k(["solar system", "planets", "space", "astronomy", "universe"],
    "The Solar System consists of the Sun and everything gravitationally bound to it.\n\n"
    "**Planets (in order):**\n"
    "1. Mercury — smallest, closest to Sun\n"
    "2. Venus — hottest, thick atmosphere\n"
    "3. Earth — our home, only known life\n"
    "4. Mars — the 'Red Planet', exploration target\n"
    "5. Jupiter — largest, Great Red Spot\n"
    "6. Saturn — famous rings\n"
    "7. Uranus — tilted axis\n"
    "8. Neptune — farthest, deep blue\n\n"
    "**Other:** Dwarf planets (Pluto), asteroids (belt between Mars-Jupiter), comets, moons (Earth's Moon, Europa, Titan).\n\n"
    "**Space Exploration:** NASA, ESA, ISRO, SpaceX, Blue Origin. Mars rovers (Perseverance), James Webb Space Telescope, ISS."
)

_k(["history", "world history"],
    "Key periods in world history:\n\n"
    "**Ancient (3000 BCE – 500 CE):** Egyptian civilization, Greek democracy, Roman Empire, Chinese dynasties, Indus Valley civilization.\n\n"
    "**Medieval (500 – 1500):** Byzantine Empire, Islamic Golden Age, Crusades, Mongol Empire, feudalism, bubonic plague.\n\n"
    "**Early Modern (1500 – 1800):** Renaissance, Age of Exploration, Scientific Revolution, Enlightenment, American Revolution, French Revolution.\n\n"
    "**Modern (1800 – present):** Industrial Revolution, World War I (1914-18), World War II (1939-45), Cold War, decolonization, digital revolution, globalization.\n\n"
    "**21st Century:** Rise of the internet, smartphones, social media, AI revolution, COVID-19 pandemic, climate crisis."
)

_k(["physics", "newton", "einstein", "relativity", "gravity"],
    "Physics is the natural science studying matter, energy, and fundamental forces.\n\n"
    "**Classical Mechanics (Newton):**\n"
    "- F = ma (Force = mass × acceleration)\n"
    "- Law of gravitation: F = Gm₁m₂/r²\n"
    "- Three laws of motion\n\n"
    "**Electromagnetism (Maxwell):** Electric and magnetic fields, light as electromagnetic wave, E = hf.\n\n"
    "**Relativity (Einstein):**\n"
    "- Special: E = mc², time dilation, length contraction\n"
    "- General: Gravity as curvature of spacetime\n\n"
    "**Quantum Mechanics:** Wave-particle duality, uncertainty principle (Heisenberg), Schrödinger equation, quantum entanglement.\n\n"
    "**Modern:** Standard Model (quarks, leptons, bosons), Higgs boson, string theory, dark matter/energy."
)

_k(["chemistry", "elements", "periodic table", "chemical"],
    "Chemistry studies matter, its properties, composition, and reactions.\n\n"
    "**Periodic Table:** 118 elements organized by atomic number. Groups: Alkali metals, Halogens, Noble gases, Transition metals.\n\n"
    "**Key Concepts:**\n"
    "- **Atoms:** Protons, neutrons, electrons\n"
    "- **Bonds:** Ionic, covalent, metallic, hydrogen\n"
    "- **Reactions:** Synthesis, decomposition, combustion, acid-base, redox\n"
    "- **States of Matter:** Solid, liquid, gas, plasma\n\n"
    "**Branches:** Organic (carbon compounds), Inorganic, Physical, Analytical, Biochemistry.\n\n"
    "**Applications:** Pharmaceuticals, materials science, energy, agriculture, environmental science."
)

_k(["biology", "cell", "dna", "genetics", "evolution"],
    "Biology is the study of living organisms and life processes.\n\n"
    "**Cell Biology:** Cells are the basic unit of life. Prokaryotic (no nucleus — bacteria) vs Eukaryotic (nucleus — animals, plants).\n\n"
    "**Genetics:** DNA → RNA → Protein (central dogma). Genes encode traits. DNA has 4 bases: A, T, G, C. Human genome: ~3 billion base pairs, ~20,000 genes.\n\n"
    "**Evolution:** Natural selection (Darwin). Species change over generations. Common ancestry. Evidence: fossils, DNA comparison, vestigial structures.\n\n"
    "**Ecology:** Ecosystems, food chains, biodiversity, symbiosis.\n\n"
    "**Modern:** CRISPR gene editing, synthetic biology, personalized medicine, microbiome research."
)

_k(["mathematics", "math", "algebra", "calculus", "geometry", "number theory"],
    "Mathematics is the study of numbers, quantity, structure, space, and change.\n\n"
    "**Branches:**\n"
    "- **Arithmetic:** Basic operations (+, -, ×, ÷)\n"
    "- **Algebra:** Variables, equations, polynomials, linear algebra, abstract algebra\n"
    "- **Geometry:** Shapes, areas, volumes. Euclidean, analytic, differential\n"
    "- **Calculus:** Derivatives (rates of change), integrals (areas), limits\n"
    "- **Statistics:** Probability, distributions, hypothesis testing, regression\n"
    "- **Number Theory:** Primes, divisibility, modular arithmetic\n"
    "- **Discrete Math:** Combinatorics, graph theory, logic\n\n"
    "**Key Formulas:**\n"
    "- Quadratic: x = (-b ± √(b²-4ac)) / 2a\n"
    "- Pythagorean: a² + b² = c²\n"
    "- Circle area: A = πr²\n"
    "- Derivative: d/dx(xⁿ) = nxⁿ⁻¹"
)

_k(["economics", "economy", "gdp", "inflation", "market"],
    "Economics studies how societies allocate scarce resources.\n\n"
    "**Microeconomics:** Supply and demand, market equilibrium, elasticity, consumer behavior, firm theory, market structures (perfect competition, monopoly, oligopoly).\n\n"
    "**Macroeconomics:** GDP, inflation, unemployment, fiscal policy (government spending/taxes), monetary policy (central banks, interest rates).\n\n"
    "**Key Concepts:**\n"
    "- **GDP:** Total value of goods/services produced\n"
    "- **Inflation:** Rising prices over time (CPI)\n"
    "- **Interest Rates:** Cost of borrowing, set by central banks\n"
    "- **Trade:** Comparative advantage, tariffs, globalization\n\n"
    "**Schools:** Keynesian, Monetarist, Austrian, MMT."
)

_k(["psychology", "mental health", "therapy", "cognitive"],
    "Psychology is the scientific study of mind and behavior.\n\n"
    "**Major Branches:**\n"
    "- **Clinical:** Mental health disorders, therapy, diagnosis\n"
    "- **Cognitive:** Perception, memory, attention, decision-making\n"
    "- **Developmental:** Growth across the lifespan\n"
    "- **Social:** How people influence each other\n"
    "- **Behavioral:** Observable behavior, conditioning\n"
    "- **Neuropsychology:** Brain-behavior relationships\n\n"
    "**Disorders:** Depression, anxiety, PTSD, OCD, ADHD, bipolar, schizophrenia.\n\n"
    "**Therapies:** CBT (Cognitive Behavioral Therapy), psychodynamic, humanistic, medication.\n\n"
    "**Key Figures:** Freud, Jung, Piaget, Skinner, Maslow, Kahneman."
)

_k(["health", "nutrition", "fitness", "exercise", "diet", "wellness"],
    "Health encompasses physical, mental, and social well-being.\n\n"
    "**Nutrition:**\n"
    "- Macronutrients: Carbohydrates (energy), Proteins (building/repair), Fats (hormones, insulation)\n"
    "- Micronutrients: Vitamins (A, B, C, D, E, K), Minerals (iron, calcium, zinc)\n"
    "- Hydration: 2-3 liters of water per day recommended\n\n"
    "**Exercise:**\n"
    "- Cardio: Running, swimming, cycling — heart health\n"
    "- Strength: Weight training, resistance — muscle/bone\n"
    "- Flexibility: Yoga, stretching — mobility\n"
    "- Recommendation: 150 min moderate or 75 min vigorous per week\n\n"
    "**Sleep:** 7-9 hours for adults. Crucial for memory, immune function, mood.\n\n"
    "**Mental Health:** Meditation, stress management, social connection, therapy."
)

_k(["programming", "coding", "software engineering", "developer", "software development"],
    "Programming is the process of writing instructions for computers to execute.\n\n"
    "**Popular Languages:**\n"
    "- **Python:** Data science, ML, web, scripting\n"
    "- **JavaScript:** Web, frontend, backend (Node.js)\n"
    "- **Java:** Enterprise, Android\n"
    "- **C/C++:** Systems, embedded, game engines\n"
    "- **Go:** Cloud, DevOps, microservices\n"
    "- **Rust:** Systems programming, safety\n"
    "- **TypeScript:** Typed JavaScript\n\n"
    "**Paradigms:** Object-Oriented, Functional, Procedural, Event-Driven.\n\n"
    "**Tools:** Git (version control), Docker (containers), CI/CD, IDEs (VS Code, IntelliJ).\n\n"
    "**Practices:** Code review, testing (unit, integration, e2e), agile/scrum, clean code."
)

_k(["startup", "entrepreneurship", "business", "company"],
    "A startup is a newly established business aiming for rapid growth.\n\n"
    "**Stages:** Idea → MVP → Product-Market Fit → Growth → Scale → IPO/Exit\n\n"
    "**Funding Rounds:** Pre-seed, Seed, Series A, B, C... → IPO or acquisition.\n\n"
    "**Key Concepts:**\n"
    "- **MVP:** Minimum Viable Product — launch fast, learn fast\n"
    "- **Product-Market Fit:** When your product meets real demand\n"
    "- **Unit Economics:** CAC (Customer Acquisition Cost), LTV (Lifetime Value)\n"
    "- **Burn Rate:** Monthly cash spending\n\n"
    "**Famous Startups → Companies:** Apple, Google, Amazon, Meta, Uber, Airbnb, Stripe, SpaceX."
)

_k(["typescript", "ts"],
    "TypeScript is a typed superset of JavaScript developed by Microsoft.\n\n"
    "**Key Features:**\n"
    "- Static type checking at compile time\n"
    "- Interfaces, generics, enums, union types\n"
    "- Compiles to plain JavaScript\n"
    "- Excellent IDE support (autocompletion, refactoring)\n\n"
    "**Example:**\n```typescript\ninterface User {\n  name: string;\n  age: number;\n  email?: string;\n}\n\nfunction greet(user: User): string {\n  return `Hello, ${user.name}!`;\n}\n```\n\n"
    "**Why Use It:** Catches errors early, better documentation, safer refactoring, scales for large codebases."
)

_k(["next.js", "nextjs", "next"],
    "Next.js is a React framework for production-grade web applications, developed by Vercel.\n\n"
    "**Key Features:**\n"
    "- **SSR (Server-Side Rendering):** Pages rendered on the server for SEO and performance\n"
    "- **SSG (Static Site Generation):** Pre-build pages at build time\n"
    "- **App Router:** File-system based routing with React Server Components\n"
    "- **API Routes:** Backend endpoints within the same project\n"
    "- **Image Optimization:** Automatic image optimization and lazy loading\n\n"
    "**App Router (v13+):** `app/` directory, layouts, loading states, error boundaries, server components by default.\n\n"
    "**Deployment:** Vercel (native), AWS, Docker, any Node.js host."
)

_k(["elon musk", "tesla", "spacex"],
    "Elon Musk is a billionaire entrepreneur and CEO of multiple companies.\n\n"
    "**Companies:**\n"
    "- **Tesla:** Electric vehicles, energy storage, solar panels\n"
    "- **SpaceX:** Reusable rockets, Starlink satellite internet, Mars colonization goal\n"
    "- **X (formerly Twitter):** Social media platform (acquired 2022)\n"
    "- **xAI:** AI company building Grok chatbot\n"
    "- **Neuralink:** Brain-computer interfaces\n"
    "- **The Boring Company:** Tunnel infrastructure\n\n"
    "**Background:** Born in South Africa, moved to US. Co-founded PayPal. One of the world's richest people."
)

_k(["world war", "ww1", "ww2", "world war 2"],
    "**World War I (1914–1918):**\n"
    "- Triggered by assassination of Archduke Franz Ferdinand\n"
    "- Allies (UK, France, Russia, US) vs Central Powers (Germany, Austria-Hungary, Ottoman Empire)\n"
    "- ~20 million deaths. Led to Treaty of Versailles, League of Nations.\n\n"
    "**World War II (1939–1945):**\n"
    "- Started with Germany's invasion of Poland\n"
    "- Allies (US, UK, Soviet Union, China) vs Axis (Germany, Japan, Italy)\n"
    "- Holocaust: 6 million Jews killed\n"
    "- ~70-85 million deaths (deadliest conflict in history)\n"
    "- Ended with atomic bombs on Hiroshima and Nagasaki\n"
    "- Led to United Nations, Cold War, decolonization"
)

_k(["covid", "coronavirus", "pandemic"],
    "COVID-19 is a respiratory disease caused by SARS-CoV-2, first identified in Wuhan, China (December 2019).\n\n"
    "**Timeline:**\n"
    "- Dec 2019: First cases in Wuhan\n"
    "- March 2020: WHO declares pandemic\n"
    "- Dec 2020: First vaccines authorized (Pfizer, Moderna)\n"
    "- 2021-22: Delta, Omicron variants\n"
    "- May 2023: WHO ends global health emergency\n\n"
    "**Impact:** 7+ million confirmed deaths globally, massive economic disruption, remote work revolution, accelerated digital transformation.\n\n"
    "**Vaccines:** mRNA (Pfizer, Moderna), viral vector (AstraZeneca, J&J), inactivated (Covaxin, Sinovac)."
)

_k(["operating system", "os", "linux", "windows", "macos"],
    "An operating system (OS) manages computer hardware and provides services for applications.\n\n"
    "**Major Desktop/Server OS:**\n"
    "- **Windows:** Most popular desktop OS (Microsoft). Versions: 10, 11, Server\n"
    "- **macOS:** Apple's desktop OS. Unix-based, Retina display optimization\n"
    "- **Linux:** Open-source. Distributions: Ubuntu, Fedora, Debian, Arch, CentOS\n\n"
    "**Mobile OS:** Android (Google, Linux-based), iOS (Apple)\n\n"
    "**Key Concepts:** Kernel, processes, threads, memory management, file systems, device drivers, shell, scheduling, virtual memory.\n\n"
    "**Linux Commands:**\n```\nls / cd / pwd / mkdir / rm / cp / mv\ncat / grep / find / chmod / ps / top / kill\nsudo / apt / yum / systemctl\n```"
)

_k(["networking", "tcp", "ip", "http", "dns", "internet"],
    "Computer networking connects devices to share resources and communicate.\n\n"
    "**OSI Model (7 layers):** Physical, Data Link, Network, Transport, Session, Presentation, Application\n\n"
    "**Key Protocols:**\n"
    "- **TCP/IP:** Reliable, connection-oriented data transfer\n"
    "- **HTTP/HTTPS:** Web communication (port 80/443)\n"
    "- **DNS:** Domain name to IP resolution\n"
    "- **DHCP:** Automatic IP assignment\n"
    "- **SSH:** Secure remote access (port 22)\n"
    "- **FTP:** File transfer\n\n"
    "**Concepts:** IP addresses (IPv4/IPv6), subnets, routers, switches, firewalls, load balancers, CDN, VPN, NAT."
)

_k(["devops", "ci/cd", "cicd", "deployment", "infrastructure"],
    "DevOps combines development and operations to deliver software faster and more reliably.\n\n"
    "**Key Practices:**\n"
    "- **CI/CD:** Continuous Integration / Continuous Deployment — automate build, test, deploy\n"
    "- **IaC:** Infrastructure as Code (Terraform, CloudFormation, Ansible)\n"
    "- **Monitoring:** Prometheus, Grafana, Datadog, New Relic\n"
    "- **Logging:** ELK Stack, Splunk\n"
    "- **Containerization:** Docker, Kubernetes\n\n"
    "**Pipeline:** Code → Build → Test → Deploy → Monitor\n\n"
    "**Tools:** GitHub Actions, Jenkins, CircleCI, GitLab CI, ArgoCD."
)

_k(["agile", "scrum", "kanban", "project management"],
    "Agile is an iterative approach to software development emphasizing flexibility and collaboration.\n\n"
    "**Scrum Framework:**\n"
    "- Sprints (2-4 weeks)\n"
    "- Roles: Product Owner, Scrum Master, Development Team\n"
    "- Ceremonies: Sprint Planning, Daily Standup, Sprint Review, Retrospective\n"
    "- Artifacts: Product Backlog, Sprint Backlog, Increment\n\n"
    "**Kanban:** Visual board (To Do → In Progress → Done), WIP limits, continuous flow.\n\n"
    "**Agile Values:** Individuals over processes, working software over documentation, customer collaboration, responding to change."
)

_k(["testing", "unit test", "integration test", "qa"],
    "Software testing ensures code works correctly and catches bugs.\n\n"
    "**Types:**\n"
    "- **Unit Testing:** Test individual functions/methods. Fast, isolated.\n"
    "- **Integration Testing:** Test components working together\n"
    "- **End-to-End (E2E):** Test full user workflows\n"
    "- **Performance:** Load testing, stress testing\n"
    "- **Security:** Penetration testing, vulnerability scanning\n\n"
    "**Tools:** Jest, Pytest, JUnit, Cypress, Playwright, Selenium, k6.\n\n"
    "**Practices:** TDD (Test-Driven Development), BDD, test coverage, CI-integrated testing."
)

_k(["design patterns", "solid", "oop", "object oriented"],
    "Design patterns are reusable solutions to common software design problems.\n\n"
    "**SOLID Principles:**\n"
    "- **S:** Single Responsibility\n"
    "- **O:** Open/Closed (open for extension, closed for modification)\n"
    "- **L:** Liskov Substitution\n"
    "- **I:** Interface Segregation\n"
    "- **D:** Dependency Inversion\n\n"
    "**Common Patterns:**\n"
    "- **Creational:** Singleton, Factory, Builder, Prototype\n"
    "- **Structural:** Adapter, Decorator, Facade, Proxy\n"
    "- **Behavioral:** Observer, Strategy, Command, Iterator, State\n\n"
    "**OOP Pillars:** Encapsulation, Inheritance, Polymorphism, Abstraction."
)


class NAGROBrain:

    def __init__(self):
        self._search = None
        self._conversation_context: list[dict] = []
        self._user_taught: dict[str, str] = {}
        self._last_topic: str = ""

    @property
    def search(self):
        if self._search is None:
            from nagro.tools.web_search import WebSearch
            self._search = WebSearch()
        return self._search

    def _clean_prompt(self, prompt: str) -> str:
        """Clean and normalize the prompt for better understanding."""
        p = prompt.strip()

        filler = [
            r'\b(?:please|pls|plz|kindly|basically|actually|bro|dude|yaar|bhai|hey)\b',
            r'\b(?:can you|could you|would you|will you|i want you to|i need you to)\b',
            r'\b(?:kya aap|kya tum|zara|thoda|mujhe|mujhko|mere liye)\b',
            r'\b(?:like|just|really|very|quite|pretty much|sort of|kind of)\b',
        ]
        cleaned = p
        for pat in filler:
            cleaned = re.sub(pat, ' ', cleaned, flags=re.I)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        if len(cleaned) > 400:
            sentences = re.split(r'[.?!\n]+', cleaned)
            questions = [s.strip() for s in sentences if '?' in s and len(s.strip()) > 8]
            if questions:
                cleaned = questions[-1]
            else:
                action_pats = [
                    r'((?:write|create|build|make|generate|explain|solve|find|implement|show|give|list|code|design|develop|banao|likho|batao|samjhao)\b.{5,})',
                ]
                for ap in action_pats:
                    m = re.search(ap, cleaned, re.I)
                    if m:
                        cleaned = m.group(1).strip()
                        break
                else:
                    meaningful = [s.strip() for s in sentences if len(s.strip()) > 15]
                    if meaningful:
                        cleaned = meaningful[-1]
                    else:
                        cleaned = cleaned[:400]

        return cleaned if len(cleaned) > 3 else p

    def think(self, prompt: str, system_prompt: str = "", history: list | None = None) -> str:
        if history:
            self._conversation_context = history[-10:]

        teach = self._detect_teaching(prompt)
        if teach:
            return teach

        followup = self._detect_followup(prompt)
        if followup:
            prompt = followup

        cleaned = self._clean_prompt(prompt)

        task = self._classify(cleaned)
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
        response = handler(cleaned)

        topic = self._extract_topic(prompt)
        if topic and len(topic) > 2:
            self._last_topic = topic

        self._conversation_context.append({"role": "user", "content": prompt})
        self._conversation_context.append({"role": "assistant", "content": response[:500]})
        if len(self._conversation_context) > 20:
            self._conversation_context = self._conversation_context[-20:]

        return response

    # ── Conversation Intelligence ──

    def _detect_teaching(self, prompt: str) -> str | None:
        p = prompt.lower().strip()
        teach_patterns = [
            (r'^(?:let me (?:tell|explain|teach) you|i(?:\'ll| will) (?:explain|tell you)|listen|note this|remember this|yaad rakh|sun|samjho?)\s*[,:]?\s*(.*)', True),
            (r'^(?:actually|fyi|did you know|fun fact)\s*[,:]?\s*(.*)', True),
            (r'^(.+?)\s+(?:means?|is defined as|refers to|matlab|ka matlab|yaani)\s+(.*)', False),
        ]

        for pattern, is_full in teach_patterns:
            m = re.match(pattern, p, re.I)
            if m:
                if is_full:
                    info = m.group(1).strip()
                    if len(info) > 10:
                        keywords = self._extract_key_phrases(info)
                        for kw in keywords:
                            self._user_taught[kw] = info
                        return (
                            f"Got it! I've understood what you shared:\n\n"
                            f"> {prompt.strip()}\n\n"
                            f"I'll keep this in mind for our conversation. "
                            f"Feel free to ask me questions about it or tell me more!"
                        )
                else:
                    term = m.group(1).strip()
                    definition = m.group(2).strip()
                    if len(definition) > 5:
                        self._user_taught[term.lower()] = f"{term}: {definition}"
                        return (
                            f"Understood! **{term.title()}** — {definition}\n\n"
                            f"I've noted this. You can ask me about **{term}** anytime in this conversation."
                        )

        action_words = ["?", "what", "how", "why", "when", "where", "who",
                        "explain", "tell me", "batao", "samjhao",
                        "write", "create", "build", "make", "generate", "code",
                        "solve", "list", "give", "show", "find", "implement",
                        "design", "develop", "program", "script", "function",
                        "class", "api", "app", "website", "course", "tutorial",
                        "project", "calculate", "compare", "analyze",
                        "banao", "likho", "karo", "do", "banawo", "dikhao",
                        "poem", "story", "essay", "speech", "song", "lyrics",
                        "summarize", "translate", "convert", "fix", "debug",
                        "help", "suggest", "recommend", "define"]
        if len(prompt.split()) > 50 and not any(q in p for q in action_words):
            info = prompt.strip()
            keywords = self._extract_key_phrases(info)
            if keywords:
                for kw in keywords:
                    self._user_taught[kw] = info
                return (
                    f"Thanks for sharing that information! I've understood the key points about "
                    f"**{', '.join(kw.title() for kw in keywords[:3])}**.\n\n"
                    f"You can now ask me questions about this, and I'll use what you've shared to answer. "
                    f"Want me to:\n"
                    f"- **Summarize** what you told me?\n"
                    f"- **Explain** a specific part in more detail?\n"
                    f"- **Answer questions** based on this information?"
                )

        return None

    def _detect_followup(self, prompt: str) -> str | None:
        p = prompt.lower().strip()

        followup_phrases = {
            "tell me more", "aur batao", "more details",
            "elaborate", "explain more", "go on",
            "continue", "aur", "aage batao",
            "keep going", "what else", "aur kya",
            "detail mein batao", "vistar se batao",
            "and more", "give me more", "more info",
        }
        if p in followup_phrases or any(p.startswith(f) for f in followup_phrases):
            if self._last_topic:
                return f"explain {self._last_topic} in more detail"

        ref_patterns = [
            r"^(?:explain|samjhao|batao)\s+(?:this|that|it|ye|wo|isko|usko)",
            r"^(?:what|kya)\s+(?:is|hai|does|karta)\s+(?:this|that|it|ye|wo)",
            r"^(?:iske|uske|iska|uska)\s+(?:baare|bare)\s+(?:mein|me)",
            r"^(?:tell me about|about)\s+(?:this|that|it)",
            r"^(?:ye kya hai|wo kya hai|kya hai ye)",
            r"^(?:what about|how about)\s+",
            r"^(?:and |but )?(?:what|how|why)\s+(?:about|if)\b",
        ]
        for pat in ref_patterns:
            if re.match(pat, p):
                if self._last_topic:
                    return f"about {self._last_topic}: {prompt}"

        positional = re.match(
            r'(?:what|explain|batao|samjhao)?\s*(?:about\s+)?(?:the\s+)?'
            r'(first|second|third|fourth|fifth|last|next|previous|'
            r'pehla|doosra|teesra|chautha|1st|2nd|3rd|4th|5th)\s+'
            r'(point|one|item|step|part|example|option|thing|wala|cheez)',
            p
        )
        if positional and self._conversation_context:
            last_answer = ""
            for msg in reversed(self._conversation_context):
                if msg.get("role") == "assistant":
                    last_answer = msg.get("content", "")
                    break
            if last_answer:
                return f"From my previous answer about {self._last_topic}:\n\n{last_answer}\n\nNow specifically explain the {positional.group(1)} {positional.group(2)}"

        if self._conversation_context and len(p.split()) <= 6:
            short_ref = re.match(
                r'(?:what is|what are|explain|how does|how do|why|kya hai|kaise)\s+(.+)',
                p
            )
            if short_ref:
                ref_topic = short_ref.group(1).strip().rstrip("?.")
                for msg in reversed(self._conversation_context):
                    if msg.get("role") == "assistant" and ref_topic in msg.get("content", "").lower():
                        return f"about {ref_topic} (related to {self._last_topic}): {prompt}"

        for term, info in self._user_taught.items():
            if term in p:
                if "?" in p or any(q in p for q in ["what", "explain", "how", "why", "batao", "samjhao", "kya"]):
                    return f"Based on what you told me: {info}\n\n{prompt}"

        return None

    def _check_conversation_context(self, prompt: str) -> str | None:
        """Check if the question can be answered from recent conversation context."""
        if not self._conversation_context:
            return None

        p = prompt.lower().strip()
        words = set(p.split()) - {"a", "an", "the", "is", "are", "was", "what", "how",
                                    "why", "when", "where", "who", "which", "do", "does",
                                    "did", "can", "could", "would", "should", "about",
                                    "me", "tell", "explain", "more", "of", "in", "it",
                                    "this", "that", "ye", "wo", "kya", "hai", "batao",
                                    "samjhao", "please", "bro", "bhai"}
        sig_words = {w for w in words if len(w) > 2}

        if not sig_words:
            return None

        last_assistant = None
        last_user_q = None
        for msg in reversed(self._conversation_context):
            if msg.get("role") == "assistant" and not last_assistant:
                last_assistant = msg.get("content", "")
            elif msg.get("role") == "user" and not last_user_q:
                last_user_q = msg.get("content", "")
            if last_assistant and last_user_q:
                break

        if not last_assistant:
            return None

        last_lower = last_assistant.lower()
        match_count = sum(1 for w in sig_words if w in last_lower)

        if match_count >= 2 and match_count >= len(sig_words) * 0.4:
            lines = last_assistant.split('\n')
            relevant = []
            for line in lines:
                ll = line.lower().strip()
                if not ll or len(ll) < 10:
                    continue
                line_match = sum(1 for w in sig_words if w in ll)
                if line_match >= 1:
                    relevant.append(line.strip())

            if relevant:
                topic = self._extract_topic(prompt)
                answer = f"## {topic.title()}\n\n"
                answer += "From our previous conversation:\n\n"
                answer += "\n\n".join(relevant[:10])
                answer += f"\n\n---\n*Would you like me to explain any part of {topic} in more detail?*"
                return answer

        return None

    def _extract_key_phrases(self, text: str) -> list[str]:
        stop = {"a", "an", "the", "is", "are", "was", "were", "and", "or", "but",
                "in", "on", "at", "to", "for", "of", "with", "by", "from", "this",
                "that", "it", "be", "has", "have", "had", "not", "as", "if", "do",
                "does", "will", "can", "about", "let", "me", "tell", "you", "i",
                "my", "we", "our", "so", "its", "very", "also", "just", "than",
                "then", "when", "what", "which", "how", "there", "here", "some"}
        words = [w.lower().strip(".,;:!?\"'()") for w in text.split()]
        sig = [w for w in words if w not in stop and len(w) > 3]
        freq = Counter(sig)
        return [w for w, _ in freq.most_common(5)]

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
                 "howdy", "good morning", "good evening", "good night", "hlo",
                 "what's up", "wassup"):
            return "greeting"

        system_kw = ["who are you", "what are you", "your name", "about yourself",
                     "kaun ho", "kya ho tum", "what can you do", "kya kar sakte",
                     "who made you", "who created you", "who built you"]
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
        strong_kw = ["write code", "write a program", "write a function", "write a script",
                     "python code", "javascript code", "html code", "sql query",
                     "code likho", "program banao", "program likho", "code banao",
                     "coding course", "coding tutorial", "code example",
                     "write a class", "write a method", "build a program"]
        score = sum(2 for k in strong_kw if k in p)
        weak_kw = ["coding", "implement", "debug", "algorithm", "data structure",
                   "linked list", "binary search", "quicksort", "merge sort",
                   "hash map", "binary tree", "rest api", "web scraper",
                   "flask", "django", "express", "react app", "react component",
                   "fibonacci", "dynamic programming", "crud", "async await",
                   "decorator", "pytest", "regex", "websocket", "socket",
                   "function", "class", "loop", "recursion", "stack", "queue",
                   "api", "http", "json", "database", "mongodb", "mysql",
                   "file handling", "exception handling", "inheritance", "polymorphism",
                   "encapsulation", "abstraction", "constructor", "destructor",
                   "sorting", "searching", "graph", "tree", "array",
                   "todo app", "calculator app", "login system", "signup",
                   "authentication", "jwt", "token", "bcrypt",
                   "web app", "desktop app", "mobile app", "cli app",
                   "scraping", "beautifulsoup", "selenium", "requests",
                   "pandas", "numpy", "matplotlib", "tkinter",
                   "fastapi", "node.js", "typescript", "golang", "rust",
                   "course", "tutorial", "project", "mini project"]
        score += sum(1 for k in weak_kw if k in p)
        if re.search(r'\b(def|function|class|import|print|console\.log|var |let |const )\b', p):
            score += 2
        return score

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
        strong_kw = ["write a story", "write a poem", "write an essay", "write a letter",
                     "write a speech", "write lyrics", "write a song", "write a joke",
                     "poem about", "story about", "essay about", "speech about",
                     "kahani likho", "kavita likho", "gana likho"]
        score = sum(2 for k in strong_kw if k in p)
        weak_kw = ["creative writing", "compose", "kahani", "kavita", "shayari",
                   "bhashan", "patra", "geet", "gana", "chutkula",
                   "poem", "story", "tale", "lyrics", "song", "speech",
                   "joke", "funny", "quotes", "motivation", "inspiration",
                   "letter to", "email to", "essay on"]
        score += sum(1 for k in weak_kw if k in p)
        return score

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
        p = prompt.lower()
        intent = extract_intent(prompt)
        q_type = intent["question_type"]
        topic = intent.get("topic") or self._extract_topic(prompt)

        # 0. Comparison questions — handle specially
        if q_type == QuestionType.COMPARISON:
            comp = extract_comparison_topics(prompt)
            if comp:
                kb_a = self._check_knowledge_base(comp[0]) or find_knowledge(comp[0])
                kb_b = self._check_knowledge_base(comp[1]) or find_knowledge(comp[1])
                if kb_a or kb_b:
                    return build_comparison(comp[0], comp[1], kb_a, kb_b)

        # 1. Check if this relates to previous conversation context
        context_answer = self._check_conversation_context(prompt)
        if context_answer:
            return context_answer

        # 2. Check user-taught knowledge first
        for term, info in self._user_taught.items():
            if term in p:
                return (
                    f"Based on what you shared earlier:\n\n"
                    f"> {info[:500]}\n\n"
                    f"This is what I understood from your explanation. "
                    f"Would you like me to go deeper into any specific aspect?"
                )

        # 3. Try direct Q&A first (quick factual answers)
        direct = self._try_direct_answer(prompt)
        if direct:
            return direct

        # 4. Check NAGRO's built-in knowledge bases (both KNOWLEDGE and WORLD_KNOWLEDGE)
        kb = self._check_knowledge_base(prompt)
        if not kb:
            kb = find_knowledge(prompt)
        if not kb:
            kb = self._synonym_knowledge_search(prompt)

        # 5. If KB has the answer → format based on question type
        if kb:
            answer = self._frame_answer(prompt, kb)
            if answer:
                return answer
            return format_answer(kb, q_type, topic)

        # 6. Fuzzy knowledge base match (need >= 2 word overlap)
        fuzzy = self._fuzzy_knowledge(prompt)
        if fuzzy:
            answer = self._frame_answer(prompt, fuzzy)
            if answer:
                return answer
            return format_answer(fuzzy, q_type, topic)

        # 7. KB doesn't have it → try Wikipedia (free, reliable, 5s timeout)
        wiki = self._wiki_search(prompt)
        if wiki:
            return format_answer(wiki, q_type, topic)

        # 8. Try DuckDuckGo web search
        web_results = self._web_search_multi(prompt)
        if web_results:
            return self._compose_answer(prompt, web_results)

        # 9. Smart fallback — NEVER says "can't connect"
        return self._smart_fallback(prompt)

    def _try_direct_answer(self, prompt: str) -> str | None:
        """Answer common factual questions directly without dumping full articles."""
        p = prompt.lower().strip().rstrip("?.")

        quick_answers = {
            "what is the capital of india": "The capital of India is **New Delhi**.",
            "capital of india": "The capital of India is **New Delhi**.",
            "india ki rajdhani": "India ki rajdhani **New Delhi** hai.",
            "what is the capital of usa": "The capital of the United States is **Washington, D.C.**",
            "what is the capital of america": "The capital of the United States is **Washington, D.C.**",
            "capital of usa": "The capital of the United States is **Washington, D.C.**",
            "capital of america": "The capital of the United States is **Washington, D.C.**",
            "what is the capital of china": "The capital of China is **Beijing**.",
            "capital of china": "The capital of China is **Beijing**.",
            "what is the capital of japan": "The capital of Japan is **Tokyo**.",
            "capital of japan": "The capital of Japan is **Tokyo**.",
            "what is the capital of russia": "The capital of Russia is **Moscow**.",
            "capital of russia": "The capital of Russia is **Moscow**.",
            "what is the capital of uk": "The capital of the United Kingdom is **London**.",
            "what is the capital of england": "The capital of England is **London**.",
            "capital of uk": "The capital of the United Kingdom is **London**.",
            "what is the capital of france": "The capital of France is **Paris**.",
            "capital of france": "The capital of France is **Paris**.",
            "what is the capital of germany": "The capital of Germany is **Berlin**.",
            "capital of germany": "The capital of Germany is **Berlin**.",
            "what is the capital of australia": "The capital of Australia is **Canberra**.",
            "capital of australia": "The capital of Australia is **Canberra**.",
            "what is the capital of canada": "The capital of Canada is **Ottawa**.",
            "capital of canada": "The capital of Canada is **Ottawa**.",
            "what is the capital of brazil": "The capital of Brazil is **Brasília**.",
            "capital of brazil": "The capital of Brazil is **Brasília**.",
            "what is the capital of italy": "The capital of Italy is **Rome**.",
            "capital of italy": "The capital of Italy is **Rome**.",
            "what is the capital of spain": "The capital of Spain is **Madrid**.",
            "capital of spain": "The capital of Spain is **Madrid**.",
            "what is the capital of south korea": "The capital of South Korea is **Seoul**.",
            "capital of south korea": "The capital of South Korea is **Seoul**.",
            "what is the capital of pakistan": "The capital of Pakistan is **Islamabad**.",
            "capital of pakistan": "The capital of Pakistan is **Islamabad**.",
            "who is the pm of india": "The Prime Minister of India is **Narendra Modi** (since May 2014).",
            "pm of india": "The Prime Minister of India is **Narendra Modi** (since May 2014).",
            "prime minister of india": "The Prime Minister of India is **Narendra Modi** (since May 2014).",
            "president of india": "The President of India is **Droupadi Murmu** (since July 2022).",
            "who is the president of usa": "The President of the United States is **Joe Biden** (since January 2021).",
            "president of usa": "The President of the United States is **Joe Biden** (since January 2021).",
            "president of america": "The President of the United States is **Joe Biden** (since January 2021).",
            "president of russia": "The President of Russia is **Vladimir Putin**.",
            "president of china": "The President of China is **Xi Jinping**.",
            "speed of light": "The speed of light in vacuum is **299,792,458 meters per second** (approximately 3 × 10⁸ m/s or about 186,282 miles per second).",
            "what is the speed of light": "The speed of light in vacuum is **299,792,458 meters per second** (approximately 3 × 10⁸ m/s or about 186,282 miles per second).",
            "speed of sound": "The speed of sound in air at 20°C is approximately **343 meters per second** (about 1,235 km/h or 767 mph).",
            "what is the speed of sound": "The speed of sound in air at 20°C is approximately **343 meters per second** (about 1,235 km/h or 767 mph).",
            "how many planets": "There are **8 planets** in our solar system: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.",
            "how many planets in solar system": "There are **8 planets** in our solar system: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune.",
            "largest planet": "The largest planet in our solar system is **Jupiter**, with a diameter of about 139,820 km — more than 11 times wider than Earth.",
            "smallest planet": "The smallest planet in our solar system is **Mercury**, with a diameter of about 4,879 km.",
            "closest planet to sun": "The closest planet to the Sun is **Mercury**, orbiting at an average distance of about 57.9 million km.",
            "largest country": "The largest country by area is **Russia** (17.1 million km²). By population, it's **India** (~1.44 billion).",
            "largest country in the world": "The largest country by area is **Russia** (17.1 million km²). By population, it's **India** (~1.44 billion).",
            "smallest country": "The smallest country in the world is **Vatican City** (0.44 km²), followed by Monaco (2.02 km²).",
            "tallest mountain": "The tallest mountain in the world is **Mount Everest** at **8,849 meters** (29,032 feet), located in the Himalayas on the Nepal-China border.",
            "highest mountain": "The highest mountain in the world is **Mount Everest** at **8,849 meters** (29,032 feet), located in the Himalayas on the Nepal-China border.",
            "longest river": "The longest river in the world is the **Nile** at approximately **6,650 km** (4,130 miles), flowing through northeastern Africa. The Amazon is the largest by water volume.",
            "deepest ocean": "The deepest ocean is the **Pacific Ocean**. Its deepest point is the **Mariana Trench** at approximately **10,994 meters** (36,070 feet) deep.",
            "biggest ocean": "The biggest ocean is the **Pacific Ocean**, covering about **165.25 million km²** — larger than all the land area on Earth combined.",
            "what is water": "Water (H₂O) is a chemical compound made of **two hydrogen atoms and one oxygen atom**. It's essential for all known forms of life, covers about 71% of Earth's surface, and exists in three states: solid (ice), liquid (water), and gas (steam/vapor).",
            "boiling point of water": "The boiling point of water is **100°C (212°F)** at standard atmospheric pressure (1 atm).",
            "freezing point of water": "The freezing point of water is **0°C (32°F)** at standard atmospheric pressure.",
            "what is gravity": "Gravity is a fundamental force of nature that attracts objects with mass toward each other. On Earth's surface, the acceleration due to gravity is approximately **9.8 m/s²** (often rounded to 10 m/s²). It keeps planets in orbit and holds us on the ground.",
            "what is pi": "Pi (π) is a mathematical constant representing the ratio of a circle's circumference to its diameter. Its value is approximately **3.14159265358979...** It's an irrational number — its decimal representation never ends or repeats.",
            "value of pi": "The value of Pi (π) is approximately **3.14159265358979...**",
            "what is zero": "Zero (0) is a number that represents **nothing or no quantity**. It's the integer between -1 and 1. It was first used as a number by ancient Indian mathematicians — **Brahmagupta** (628 AD) was among the first to define rules for arithmetic involving zero.",
            "who invented zero": "Zero as a number was developed by ancient **Indian mathematicians**. **Brahmagupta** (628 AD) was the first to define arithmetic rules for zero. **Aryabhata** (5th century) used it as a placeholder. The concept spread to the Arab world and then to Europe.",
            "what is the sun": "The Sun is a **star** — a massive ball of hot plasma at the center of our solar system. It's about 4.6 billion years old, has a surface temperature of ~5,500°C, and is approximately 150 million km from Earth. It provides the light and heat essential for life on Earth.",
            "what is the moon": "The Moon is Earth's only natural satellite, orbiting at an average distance of ~384,400 km. It has no atmosphere, no liquid water on its surface, and its gravity is about 1/6th of Earth's. Neil Armstrong was the first person to walk on the Moon (July 20, 1969).",
            "who made nagro": "**NAGRO 4.1** (Neural Adaptive Generative Reasoning Operator) was created by **Aditya Kumar**. It's a self-built AI engine with built-in knowledge, open-source model integration, and advanced reasoning capabilities.",
            "who created nagro": "**NAGRO 4.1** was created by **Aditya Kumar**. It's a Neural Adaptive Generative Reasoning Operator — a self-built AI system.",
            "what is nagro": "**NAGRO 4.1** (Neural Adaptive Generative Reasoning Operator) is a 100% self-built AI assistant created by **Aditya Kumar**. It uses its own reasoning engine, a built-in knowledge base of 150+ topics, self-built code generator (50+ patterns), creative writing engine, Wikipedia integration, and web search — all without any paid APIs or external AI models.",
            "1+1": "1 + 1 = **2**",
            "2+2": "2 + 2 = **4**",
            "what is 1+1": "1 + 1 = **2**",
            "what is 2+2": "2 + 2 = **4**",
            "how many continents": "There are **7 continents**: Asia, Africa, North America, South America, Antarctica, Europe, and Australia/Oceania.",
            "how many oceans": "There are **5 oceans**: Pacific, Atlantic, Indian, Southern (Antarctic), and Arctic.",
            "what is the largest animal": "The **Blue Whale** is the largest animal ever to have lived on Earth, reaching up to 30 meters (100 feet) long and weighing up to 200 tonnes.",
            "fastest animal": "The **Peregrine Falcon** is the fastest animal, reaching speeds over **390 km/h (242 mph)** during its hunting dive. On land, the **Cheetah** is fastest at **112 km/h (70 mph)**.",
            "what is dna": "**DNA (Deoxyribonucleic Acid)** is a molecule that carries the genetic instructions for the development, functioning, growth, and reproduction of all known organisms. It has a double helix structure, discovered by Watson and Crick in 1953.",
            "what is photosynthesis": "**Photosynthesis** is the process by which green plants and some organisms convert sunlight, water (H₂O), and carbon dioxide (CO₂) into glucose (C₆H₁₂O₆) and oxygen (O₂). Formula: **6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂**",
            "what is electricity": "**Electricity** is the flow of electric charge (usually electrons) through a conductor. It's measured in **Amperes (A)** for current, **Volts (V)** for voltage, and **Watts (W)** for power. P = V × I.",
            "what is the internet": "The **Internet** is a global network of interconnected computers that communicate using the TCP/IP protocol. Created from ARPANET (1969), it now connects over 5 billion users worldwide via servers, routers, and cables (including undersea fiber optic cables).",
            "who invented computer": "**Charles Babbage** is considered the 'Father of the Computer' for designing the Analytical Engine (1837). The first electronic general-purpose computer was **ENIAC** (1945). **Alan Turing** laid the theoretical foundations of computing.",
            "who invented telephone": "**Alexander Graham Bell** patented the first practical telephone on **March 7, 1876**.",
            "who invented electricity": "Electricity wasn't invented — it's a natural phenomenon. **Benjamin Franklin** proved lightning was electrical (1752). **Michael Faraday** invented the electric motor (1821) and discovered electromagnetic induction. **Thomas Edison** invented the practical light bulb (1879).",
            "distance to moon": "The average distance from Earth to the Moon is approximately **384,400 km** (238,855 miles). Light takes about **1.3 seconds** to travel from Earth to the Moon.",
            "distance to sun": "The average distance from Earth to the Sun is approximately **149.6 million km** (93 million miles), also called **1 Astronomical Unit (AU)**. Light takes about **8 minutes 20 seconds** to travel from the Sun to Earth.",
            "what is python": "**Python** is a high-level, interpreted programming language created by **Guido van Rossum** in 1991. Known for its simple, readable syntax and versatility. Used in web development, data science, AI/ML, automation, and scripting. One of the most popular languages worldwide.",
            "what is javascript": "**JavaScript** is a programming language created by **Brendan Eich** in 1995 (in just 10 days!). Originally for web browsers, it now runs everywhere via Node.js. It's the language of the web — used for frontend (React, Vue) and backend (Express, Fastify) development.",
            "what is html": "**HTML (HyperText Markup Language)** is the standard markup language for creating web pages. Created by **Tim Berners-Lee** in 1993. It defines the structure of web content using tags like `<h1>`, `<p>`, `<div>`, `<img>`, etc. Current version: HTML5.",
            "hello": None,
            "hi": None,
        }

        if p in quick_answers:
            return quick_answers[p]

        for q, a in quick_answers.items():
            if a and p.endswith(q):
                return a

        return None

    def _frame_answer(self, prompt: str, kb_content: str) -> str | None:
        """Frame KB content as a proper answer to the specific question asked."""
        p = prompt.lower().strip()
        topic = self._extract_topic(prompt)

        is_specific = any(pat in p for pat in [
            "what is the", "what are the", "who is the", "who was the",
            "when was", "when did", "where is", "where was",
            "how many", "how much", "how old", "how long", "how far",
            "which is", "which was", "what year", "what country",
        ])

        if not is_specific:
            return None

        lines = kb_content.split('\n')
        relevant = []
        topic_words = set(topic.lower().split())
        prompt_words = set(p.split()) - {"what", "is", "the", "a", "an", "are",
                                          "who", "was", "when", "where", "how",
                                          "which", "did", "does", "do", "many",
                                          "much", "old", "long", "far", "of",
                                          "in", "on", "at", "to", "for", "by"}

        for line in lines:
            l_lower = line.lower()
            match_count = sum(1 for w in prompt_words if w in l_lower and len(w) > 2)
            if match_count >= 2 or any(w in l_lower for w in topic_words if len(w) > 3):
                clean = line.strip().strip('-').strip('*').strip()
                if clean and len(clean) > 10:
                    relevant.append(clean)

        if relevant:
            header = f"## {topic.title()}\n\n"
            answer = header + "\n\n".join(relevant[:8])
            if len(relevant) > 8:
                answer += f"\n\n*Ask me for more details about {topic}!*"
            return answer

        return None

    def _wiki_search(self, prompt: str) -> str | None:
        """Search Wikipedia for information. Free, no API key."""
        try:
            from nagro.tools.wikipedia_search import wiki_quick
            topic = self._extract_topic(prompt)
            return wiki_quick(topic)
        except Exception:
            return None

    def _web_search_multi(self, prompt: str) -> list:
        """Try web search with multiple query strategies."""
        queries = self._make_queries(prompt)
        all_results = []
        for q in queries:
            results = self._web_search(q)
            if results:
                all_results.extend(results)
                if len(all_results) >= 8:
                    break
        return all_results

    def _compose_best_answer(self, prompt: str, kb: str | None,
                              wiki: str | None, web_results: list,
                              is_explain: bool) -> str:
        """Compose the best answer from all available sources.
        Priority: KB + Web > KB + Wiki > Web > KB > Wiki > OpenSource Model > Fuzzy > Fallback
        """
        topic = self._extract_topic(prompt)

        # Case 1: Knowledge base + web results = comprehensive answer
        if kb and web_results:
            extra = self._extract_unique_sentences(web_results, prompt, limit=5)
            if extra:
                return kb + "\n\n**Latest Information:**\n\n" + "\n\n".join(extra)
            return kb

        # Case 2: Knowledge base + Wikipedia = rich answer
        if kb and wiki:
            wiki_extra = self._extract_wiki_additions(kb, wiki)
            if wiki_extra:
                return kb + "\n\n**Additional Details:**\n\n" + wiki_extra
            return kb

        # Case 3: Web results available (DuckDuckGo worked)
        if web_results:
            composed = self._compose_answer(prompt, web_results)
            if wiki:
                return composed + "\n\n---\n\n" + wiki
            return composed

        # Case 4: Only knowledge base
        if kb:
            if is_explain:
                return self._make_explanation(kb, prompt)
            return kb

        # Case 5: Only Wikipedia
        if wiki:
            header = f"## {topic.title()}\n\n"
            footer = (
                f"\n\n---\n"
                f"**Want to know more?** Ask me:\n"
                f"- \"Tell me more about {topic}\"\n"
                f"- \"How does {topic} work?\"\n"
                f"- \"Give examples of {topic}\""
            )
            return header + wiki + footer

        # Case 6: Fuzzy knowledge base match
        multi_kb = self._fuzzy_knowledge(prompt)
        if multi_kb:
            if is_explain:
                return self._make_explanation(multi_kb, prompt)
            return multi_kb

        # Case 7: Smart contextual fallback — NEVER say "can't connect"
        return self._smart_fallback(prompt)


    def _extract_wiki_additions(self, kb: str, wiki: str) -> str | None:
        """Extract new sentences from wiki that aren't already in kb."""
        kb_lower = kb.lower()
        wiki_sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', wiki) if len(s.strip()) > 30]
        new_sents = []
        for s in wiki_sents:
            words = set(s.lower().split())
            sig = {w for w in words if len(w) > 4}
            overlap = sum(1 for w in sig if w in kb_lower)
            if overlap < len(sig) * 0.5 and len(new_sents) < 5:
                new_sents.append(s)
        if new_sents:
            return "\n\n".join(new_sents)
        return None

    def _make_explanation(self, content: str, prompt: str) -> str:
        topic = self._extract_topic(prompt)
        header = f"## {topic.title()} — Explained\n\n"
        simple_intro = (
            f"Let me break down **{topic}** in a clear and simple way:\n\n"
        )
        footer = (
            f"\n\n---\n"
            f"**Want to know more?** Ask me:\n"
            f"- \"Tell me more about {topic}\"\n"
            f"- \"Give me examples of {topic}\"\n"
            f"- \"How is {topic} used in real life?\""
        )
        return header + simple_intro + content + footer

    def _check_knowledge_base(self, prompt: str) -> str | None:
        p = prompt.lower()

        for key, (all_keys, text) in KNOWLEDGE.items():
            for ak in all_keys:
                if len(ak) <= 3:
                    if re.search(r'\b' + re.escape(ak) + r'\b', p):
                        return text
                else:
                    if ak in p:
                        return text

        return None

    def _synonym_knowledge_search(self, prompt: str) -> str | None:
        """Search KB using synonym expansion — finds 'car' when user says 'automobile'."""
        p_words = set(prompt.lower().split())
        sig = {w for w in p_words if len(w) > 2}
        expanded = expand_synonyms(sig)

        for key, (all_keys, text) in KNOWLEDGE.items():
            for ak in all_keys:
                ak_words = set(ak.split())
                if ak_words & expanded:
                    return text

        try:
            from nagro.core.knowledge_data import WORLD_KNOWLEDGE
            for key, content in WORLD_KNOWLEDGE.items():
                key_words = set(key.lower().split())
                if len(key_words & expanded) >= 1 and len(key_words) <= 3:
                    return content
                if len(key_words & expanded) >= 2:
                    return content
        except Exception:
            pass

        return None

    def _fuzzy_knowledge(self, prompt: str) -> str | None:
        p_words = set(prompt.lower().split())
        stop = {"a", "an", "the", "is", "are", "was", "were", "what", "how",
                "why", "when", "where", "who", "which", "do", "does", "did",
                "can", "could", "would", "should", "will", "about", "for",
                "to", "of", "in", "on", "at", "by", "with", "from", "me",
                "my", "i", "you", "your", "tell", "explain", "describe",
                "please", "help", "want", "need", "give", "latest", "news",
                "analyze", "research", "discuss", "detailed", "comprehensive",
                "know", "think", "say", "said", "like", "just", "also",
                "very", "really", "much", "many", "some", "any", "all",
                "between", "through", "into", "has", "have", "had", "been",
                "being", "their", "they", "them", "his", "her", "its",
                "our", "more", "most", "other", "new", "old", "good", "bad",
                "make", "made", "get", "got", "take", "took", "come", "came"}
        sig_words = {w for w in p_words if w not in stop and len(w) > 2}

        if not sig_words:
            return None

        best_key = None
        best_score = 0
        best_ratio = 0.0
        for key, (all_keys, text) in KNOWLEDGE.items():
            all_kw = set()
            for ak in all_keys:
                all_kw.update(ak.split())
            overlap = len(sig_words & all_kw)
            ratio = overlap / max(len(all_kw), 1)
            if overlap > best_score or (overlap == best_score and ratio > best_ratio):
                best_score = overlap
                best_ratio = ratio
                best_key = key

        if best_key and best_score >= 2:
            return KNOWLEDGE[best_key][1]
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
                "comprehensive", "brief", "discuss", "elaborate", "analyze",
                "latest", "news", "trending", "public", "discussions",
                "including", "retweets", "social", "media", "trends"}
        words = prompt.split()
        keywords = [w for w in words if w.lower() not in stop and len(w) > 2]
        queries = []
        if len(keywords) <= 8:
            queries.append(" ".join(keywords))
        else:
            queries.append(" ".join(keywords[:8]))
        if len(keywords) > 4:
            queries.append(" ".join(keywords[:5]))
        queries.append(prompt[:120])
        return queries[:3]

    def _compose_answer(self, prompt: str, results: list) -> str:
        sentences = self._extract_unique_sentences(results, prompt, limit=15)
        if not sentences:
            for r in results[:5]:
                body = r.get("body", r.get("description", r.get("snippet", "")))
                if body and len(body) > 30:
                    sentences.append(body[:500])
        if not sentences:
            return self._smart_fallback(prompt)

        topic = self._extract_topic(prompt)
        response = f"## {topic.title()}\n\n"
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

    def _smart_fallback(self, prompt: str) -> str:
        topic = self._extract_topic(prompt)
        p = prompt.lower()

        # Last resort: try Wikipedia one more time with cleaned topic
        try:
            from nagro.tools.wikipedia_search import search_wikipedia
            wiki = search_wikipedia(topic)
            if wiki and len(wiki) > 100:
                return f"## {topic.title()}\n\n{wiki}\n\n---\n*Ask me more about {topic} or any related topic!*"
        except Exception:
            pass

        # Try to give a thoughtful response based on the question type
        response = f"## {topic.title()}\n\n"

        if any(w in p for w in ["how to", "tutorial", "guide", "steps", "learn", "kaise"]):
            response += (
                f"Here's a practical approach to **{topic}**:\n\n"
                f"1. **Start with basics** — understand the core concepts first\n"
                f"2. **Practice hands-on** — theory alone isn't enough, build something\n"
                f"3. **Use official documentation** — always the most reliable source\n"
                f"4. **Join communities** — Stack Overflow, Reddit, Discord for help\n"
                f"5. **Build projects** — apply what you learn in real scenarios\n\n"
                f"Would you like me to go deeper into any specific aspect of {topic}?"
            )
        elif any(w in p for w in ["compare", "vs", "versus", "difference", "better"]):
            parts = re.split(r'\b(?:vs|versus|or|compared to|difference between|and)\b', p)
            if len(parts) >= 2:
                a_name = parts[0].strip().strip("what is the between").strip()
                b_name = parts[-1].strip().rstrip("?.")
                response += (
                    f"**{a_name.title()} vs {b_name.title()}:**\n\n"
                    f"Both have their strengths. The best choice depends on your specific needs:\n\n"
                    f"| Aspect | {a_name.title()} | {b_name.title()} |\n"
                    f"|--------|{'---' * 5}|{'---' * 5}|\n"
                    f"| **Use Case** | Depends on requirements | Depends on requirements |\n"
                    f"| **Learning** | Check official docs | Check official docs |\n\n"
                    f"Ask me specifically about **{a_name}** or **{b_name}** for detailed information!"
                )
            else:
                response += f"Could you specify what you'd like to compare? For example: \"Compare Python vs JavaScript\""
        elif any(w in p for w in ["who is", "who was", "kaun hai", "kaun tha"]):
            response += (
                f"I don't have specific information about **{topic}** in my knowledge base right now.\n\n"
                f"I do know about many notable figures — try asking about specific people like Elon Musk, "
                f"Sundar Pichai, Albert Einstein, Isaac Newton, and more."
            )
        elif any(w in p for w in ["when", "what year", "what date", "kab"]):
            response += (
                f"I don't have the specific date/time information for **{topic}** right now.\n\n"
                f"Try asking me about well-known historical events, or I can look it up if you ask more specifically."
            )
        else:
            response += (
                f"I don't have detailed information about **{topic}** in my current knowledge base.\n\n"
                f"Here's what I can help with:\n"
                f"- **AI & Tech:** OpenAI, Anthropic, Google, DeepSeek, LLMs, ML\n"
                f"- **Programming:** Python, JavaScript, React, APIs, Databases\n"
                f"- **Science:** Physics, Chemistry, Biology, Space\n"
                f"- **World:** Countries, History, Economics, Sports, People\n\n"
                f"Try rephrasing your question or asking about a related topic!"
            )

        return response.strip()

    def _extract_topic(self, prompt: str) -> str:
        topic = re.sub(
            r'^(what is|what are|how does|how do|how to|why|explain|describe|'
            r'tell me about|define|research|conduct|provide|give me|discuss|'
            r'analyze|examine|compare|latest|news about)\s+',
            '', prompt, flags=re.IGNORECASE).strip()
        topic = re.sub(r'^(a|an|the|detailed|exhaustive|comprehensive)\s+',
                       '', topic, flags=re.IGNORECASE).strip()
        return topic[:150] if topic else prompt[:150]

    # ── Greeting / System ──

    def _handle_greeting(self, prompt: str) -> str:
        greetings = [
            "Hello! How can I help you today?\n\nI can:\n- **Answer questions** on any topic (AI, science, history, tech, business...)\n- **Write code** in Python, JavaScript, HTML, SQL and more\n- **Solve math** step by step\n- **Write stories, poems, essays** and creative content\n- **Learn from you** — tell me something and I'll remember it!\n\nJust ask anything!",
            "Hey there! What would you like to explore?\n\nYou can ask me questions, share information with me, or get help with coding and math. I'm all ears!",
            "Hi! I'm ready to help. You can:\n- Ask me anything (I know 150+ topics in detail)\n- Teach me something new and I'll learn from you\n- Get code, math solutions, or creative writing\n\nWhat's on your mind?",
        ]
        return random.choice(greetings)

    def _handle_system(self, prompt: str) -> str:
        return (
            "I'm **NAGRO 4.1** — Neural Adaptive Generative Reasoning Operator, "
            "created by **Aditya Kumar**.\n\n"
            "**What I can do:**\n"
            "- Answer questions on **150+ topics** (AI, science, programming, history, business, and more)\n"
            "- **Write code** in Python, JavaScript, TypeScript, HTML, SQL, and more\n"
            "- **Solve math** step by step (arithmetic, algebra, statistics)\n"
            "- **Write creatively** — stories, poems, essays, speeches, lyrics, emails\n"
            "- **Analyze & summarize** text you paste in\n"
            "- **Research** any topic with web search + built-in knowledge\n"
            "- **Code templates** for algorithms, APIs, data structures\n\n"
            "100% self-built AI engine. No paid APIs. No dependencies on external AI services.\n\n"
            "**Try asking me:**\n"
            "- \"What is quantum computing?\"\n"
            "- \"Write a Python binary search\"\n"
            "- \"Calculate 15 * 32 + 7\"\n"
            "- \"Write a poem about technology\"\n"
            "- \"Explain how blockchain works\""
        )

    # ── Code ──

    def _handle_code(self, prompt: str) -> str:
        p = prompt.lower()

        if any(k in p for k in ["course", "tutorial", "syllabus", "curriculum",
                                 "roadmap", "learning path", "sikhao", "seekhna",
                                 "complete guide", "full guide", "step by step learn"]):
            return self._generate_course(prompt)

        if any(k in p for k in ["project", "mini project", "build a", "banao",
                                 "full stack", "web app", "desktop app", "cli app",
                                 "todo app", "chat app", "blog", "portfolio",
                                 "e-commerce", "ecommerce", "landing page"]):
            return self._generate_project(prompt)

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

        smart_code = self._generate_code_smart(prompt, lang)
        if smart_code:
            return smart_code

        results = self._web_search(prompt + " code example")
        if results:
            return self._compose_answer(prompt, results)
        return (
            "I can help with code! Here are some things I can write:\n\n"
            "- \"Write a Python quicksort\" — sorting algorithms\n"
            "- \"Create a REST API\" — web backend\n"
            "- \"JavaScript fetch example\" — HTTP requests\n"
            "- \"Binary search tree\" — data structures\n"
            "- \"Python course\" — full learning roadmap\n"
            "- \"Build a todo app\" — complete project\n\n"
            "Just tell me what you need!"
        )

    def _generate_code_smart(self, prompt: str, lang: str) -> str | None:
        """Smart code generation — combine multiple patterns when no single pattern matches."""
        p = prompt.lower()
        topic = re.sub(r'^(write|create|make|build|generate|implement|code|develop)\s+(a\s+)?',
                       '', prompt, flags=re.I).strip()
        topic = re.sub(r'\s+(in\s+)?(python|javascript|java|html|css|go|rust|typescript|c\+\+)$',
                       '', topic, flags=re.I).strip()

        if not topic or len(topic) < 3:
            return None

        components = {
            "input": ("user_input = input('Enter value: ')", "Get user input"),
            "list": ("items = []\nitems.append(value)", "Store items in list"),
            "dict": ("data = {}", "Store key-value pairs"),
            "loop": ("for item in items:\n    print(item)", "Iterate over items"),
            "file read": ("with open('data.txt', 'r') as f:\n    content = f.read()", "Read file"),
            "file write": ("with open('output.txt', 'w') as f:\n    f.write(result)", "Write file"),
            "function": ("def process(data):\n    # Your logic here\n    return result", "Define function"),
            "class": ("class MyClass:\n    def __init__(self):\n        self.data = []\n\n    def add(self, item):\n        self.data.append(item)", "Define class"),
            "print": ("print(f'Result: {result}')", "Display output"),
            "error": ("try:\n    result = risky_operation()\nexcept Exception as e:\n    print(f'Error: {e}')", "Handle errors"),
            "sort": ("sorted_data = sorted(items, key=lambda x: x)", "Sort data"),
            "filter": ("filtered = [x for x in items if condition(x)]", "Filter data"),
            "count": ("from collections import Counter\ncounts = Counter(items)", "Count occurrences"),
            "math": ("import math\nresult = math.sqrt(value)", "Math operations"),
            "random": ("import random\nchoice = random.choice(items)", "Random selection"),
            "time": ("import time\nstart = time.time()\n# ... code ...\nprint(f'Took {time.time()-start:.2f}s')", "Measure time"),
            "json": ("import json\ndata = json.loads(json_string)\njson_string = json.dumps(data, indent=2)", "JSON handling"),
            "regex": ("import re\nmatches = re.findall(r'pattern', text)", "Regex pattern matching"),
            "http": ("import urllib.request\nwith urllib.request.urlopen(url) as resp:\n    data = resp.read().decode()", "HTTP request"),
        }

        matched = []
        for key, (code, desc) in components.items():
            if key in p:
                matched.append((key, code, desc))

        if not matched:
            keywords_map = {
                "read": "file read", "write": "file write", "save": "file write",
                "load": "file read", "open": "file read",
                "sort": "sort", "order": "sort", "arrange": "sort",
                "filter": "filter", "search": "filter", "find": "filter",
                "count": "count", "frequency": "count", "how many": "count",
                "download": "http", "fetch": "http", "request": "http", "url": "http",
                "calculate": "math", "compute": "math",
                "random": "random", "pick": "random", "choose": "random",
                "timer": "time", "benchmark": "time", "measure": "time",
                "parse": "json", "convert": "json",
                "pattern": "regex", "match": "regex", "extract": "regex",
                "class": "class", "object": "class", "oop": "class",
                "function": "function", "method": "function",
                "error": "error", "exception": "error", "try": "error",
                "input": "input", "ask": "input", "prompt": "input",
                "display": "print", "output": "print", "show": "print",
            }
            for kw, comp_key in keywords_map.items():
                if kw in p and comp_key in components:
                    code, desc = components[comp_key]
                    matched.append((comp_key, code, desc))

        if not matched:
            return None

        seen = set()
        unique = []
        for key, code, desc in matched:
            if key not in seen:
                seen.add(key)
                unique.append((code, desc))

        code_parts = "\n\n".join(code for code, _ in unique[:6])
        desc_parts = ", ".join(desc for _, desc in unique[:6])

        return (
            f"## {topic.title()}\n\n"
            f"Here's a Python program for **{topic}**:\n\n"
            f"```python\n"
            f"# {topic.title()}\n"
            f"# Components: {desc_parts}\n\n"
            f"{code_parts}\n"
            f"```\n\n"
            f"**What this does:** {desc_parts}.\n\n"
            f"*Want me to expand any part or add more features? Just ask!*"
        )

    def _generate_code(self, prompt: str, lang: str) -> str | None:
        p = prompt.lower()
        codes = {
            "reverse string": ("def reverse_string(s):\n    return s[::-1]\n\nprint(reverse_string('hello'))  # olleh", "Reverses using slice notation."),
            "palindrome": ("def is_palindrome(s):\n    c = ''.join(ch.lower() for ch in s if ch.isalnum())\n    return c == c[::-1]\n\nprint(is_palindrome('racecar'))  # True", "Checks if string reads same both ways."),
            "prime": ("def is_prime(n):\n    if n < 2: return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0: return False\n    return True\n\nprimes = [x for x in range(2, 100) if is_prime(x)]\nprint(primes)", "Tests divisibility up to sqrt(n). O(sqrt(n))."),
            "two sum": ("def two_sum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        if target - n in seen:\n            return [seen[target-n], i]\n        seen[n] = i\n    return []\n\nprint(two_sum([2,7,11,15], 9))  # [0, 1]", "Hash map — O(n) time, O(n) space."),
            "factorial": ("def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)\n\nfor i in range(1, 11):\n    print(f'{i}! = {factorial(i)}')", "Recursive O(n)."),
            "password": ("import secrets, string\ndef gen_password(n=16):\n    chars = string.ascii_letters + string.digits + '!@#$%'\n    return ''.join(secrets.choice(chars) for _ in range(n))\n\nprint(gen_password())", "Cryptographically secure random password."),
            "anagram": ("def is_anagram(s1, s2):\n    return sorted(s1.lower()) == sorted(s2.lower())\n\nprint(is_anagram('listen', 'silent'))  # True\nprint(is_anagram('hello', 'world'))   # False", "Sorted character comparison — O(n log n)."),
            "counter": ("from collections import Counter\n\ndef most_common_words(text, n=5):\n    words = text.lower().split()\n    return Counter(words).most_common(n)\n\ntext = 'the cat sat on the mat the cat'\nprint(most_common_words(text))", "Word frequency counter using collections.Counter."),
            "matrix": ("def multiply_matrices(A, B):\n    rows_A, cols_A = len(A), len(A[0])\n    cols_B = len(B[0])\n    result = [[0]*cols_B for _ in range(rows_A)]\n    for i in range(rows_A):\n        for j in range(cols_B):\n            for k in range(cols_A):\n                result[i][j] += A[i][k] * B[k][j]\n    return result\n\nA = [[1,2],[3,4]]\nB = [[5,6],[7,8]]\nprint(multiply_matrices(A, B))  # [[19,22],[43,50]]", "O(n³) matrix multiplication."),
            "fibonacci": ("def fibonacci(n):\n    a, b = 0, 1\n    result = []\n    for _ in range(n):\n        result.append(a)\n        a, b = b, a + b\n    return result\n\nprint(fibonacci(15))", "Iterative Fibonacci — O(n) time, O(n) space."),
            "linked list": ("class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n\n    def append(self, data):\n        new = Node(data)\n        if not self.head:\n            self.head = new\n            return\n        curr = self.head\n        while curr.next:\n            curr = curr.next\n        curr.next = new\n\n    def display(self):\n        curr = self.head\n        while curr:\n            print(curr.data, end=' -> ')\n            curr = curr.next\n        print('None')\n\n    def delete(self, key):\n        curr = self.head\n        if curr and curr.data == key:\n            self.head = curr.next\n            return\n        while curr and curr.next:\n            if curr.next.data == key:\n                curr.next = curr.next.next\n                return\n            curr = curr.next\n\nll = LinkedList()\nfor x in [10, 20, 30, 40, 50]:\n    ll.append(x)\nll.display()\nll.delete(30)\nll.display()", "Singly linked list with append, delete, display."),
            "stack": ("class Stack:\n    def __init__(self):\n        self.items = []\n\n    def push(self, item):\n        self.items.append(item)\n\n    def pop(self):\n        if not self.is_empty():\n            return self.items.pop()\n        raise IndexError('Stack is empty')\n\n    def peek(self):\n        if not self.is_empty():\n            return self.items[-1]\n        raise IndexError('Stack is empty')\n\n    def is_empty(self):\n        return len(self.items) == 0\n\n    def size(self):\n        return len(self.items)\n\ns = Stack()\nfor x in [1, 2, 3, 4, 5]:\n    s.push(x)\nprint(f'Top: {s.peek()}')\nprint(f'Pop: {s.pop()}')\nprint(f'Size: {s.size()}')", "Stack using list — LIFO data structure."),
            "queue": ("from collections import deque\n\nclass Queue:\n    def __init__(self):\n        self.items = deque()\n\n    def enqueue(self, item):\n        self.items.append(item)\n\n    def dequeue(self):\n        if not self.is_empty():\n            return self.items.popleft()\n        raise IndexError('Queue is empty')\n\n    def peek(self):\n        if not self.is_empty():\n            return self.items[0]\n        raise IndexError('Queue is empty')\n\n    def is_empty(self):\n        return len(self.items) == 0\n\n    def size(self):\n        return len(self.items)\n\nq = Queue()\nfor x in ['A', 'B', 'C', 'D']:\n    q.enqueue(x)\nprint(f'Front: {q.peek()}')\nprint(f'Dequeue: {q.dequeue()}')\nprint(f'Size: {q.size()}')", "Queue using deque — FIFO data structure."),
            "binary search": ("def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1\n\narr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]\nprint(binary_search(arr, 23))  # 5\nprint(binary_search(arr, 99))  # -1", "Binary search — O(log n) on sorted array."),
            "binary tree": ("class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n\nclass BST:\n    def __init__(self):\n        self.root = None\n\n    def insert(self, val):\n        self.root = self._insert(self.root, val)\n\n    def _insert(self, node, val):\n        if not node:\n            return TreeNode(val)\n        if val < node.val:\n            node.left = self._insert(node.left, val)\n        else:\n            node.right = self._insert(node.right, val)\n        return node\n\n    def inorder(self):\n        result = []\n        self._inorder(self.root, result)\n        return result\n\n    def _inorder(self, node, result):\n        if node:\n            self._inorder(node.left, result)\n            result.append(node.val)\n            self._inorder(node.right, result)\n\n    def search(self, val):\n        return self._search(self.root, val)\n\n    def _search(self, node, val):\n        if not node:\n            return False\n        if val == node.val:\n            return True\n        if val < node.val:\n            return self._search(node.left, val)\n        return self._search(node.right, val)\n\ntree = BST()\nfor x in [50, 30, 70, 20, 40, 60, 80]:\n    tree.insert(x)\nprint('Inorder:', tree.inorder())\nprint('Search 40:', tree.search(40))\nprint('Search 99:', tree.search(99))", "Binary Search Tree with insert, search, inorder traversal."),
            "hash table": ("class HashTable:\n    def __init__(self, size=10):\n        self.size = size\n        self.table = [[] for _ in range(size)]\n\n    def _hash(self, key):\n        return hash(key) % self.size\n\n    def put(self, key, value):\n        idx = self._hash(key)\n        for i, (k, v) in enumerate(self.table[idx]):\n            if k == key:\n                self.table[idx][i] = (key, value)\n                return\n        self.table[idx].append((key, value))\n\n    def get(self, key):\n        idx = self._hash(key)\n        for k, v in self.table[idx]:\n            if k == key:\n                return v\n        raise KeyError(key)\n\n    def delete(self, key):\n        idx = self._hash(key)\n        for i, (k, v) in enumerate(self.table[idx]):\n            if k == key:\n                del self.table[idx][i]\n                return\n        raise KeyError(key)\n\nht = HashTable()\nht.put('name', 'NAGRO')\nht.put('version', '4.1')\nht.put('author', 'Aditya')\nprint(ht.get('name'))\nprint(ht.get('version'))", "Hash table with chaining for collision handling."),
            "graph": ("class Graph:\n    def __init__(self):\n        self.adj = {}\n\n    def add_edge(self, u, v):\n        self.adj.setdefault(u, []).append(v)\n        self.adj.setdefault(v, []).append(u)\n\n    def bfs(self, start):\n        visited = set([start])\n        queue = [start]\n        order = []\n        while queue:\n            node = queue.pop(0)\n            order.append(node)\n            for neighbor in self.adj.get(node, []):\n                if neighbor not in visited:\n                    visited.add(neighbor)\n                    queue.append(neighbor)\n        return order\n\n    def dfs(self, start, visited=None):\n        if visited is None:\n            visited = set()\n        visited.add(start)\n        result = [start]\n        for neighbor in self.adj.get(start, []):\n            if neighbor not in visited:\n                result.extend(self.dfs(neighbor, visited))\n        return result\n\ng = Graph()\nfor u, v in [(0,1),(0,2),(1,3),(2,4),(3,4)]:\n    g.add_edge(u, v)\nprint('BFS:', g.bfs(0))\nprint('DFS:', g.dfs(0))", "Graph with adjacency list, BFS and DFS traversal."),
            "read file": ("# Read a file\nwith open('data.txt', 'r') as f:\n    content = f.read()\n    print(content)\n\n# Read line by line\nwith open('data.txt', 'r') as f:\n    for line in f:\n        print(line.strip())\n\n# Read into list\nwith open('data.txt', 'r') as f:\n    lines = f.readlines()\n    print(f'Total lines: {len(lines)}')", "File reading — three different approaches."),
            "write file": ("# Write to file (creates or overwrites)\nwith open('output.txt', 'w') as f:\n    f.write('Hello, World!\\n')\n    f.write('Second line\\n')\n\n# Append to file\nwith open('output.txt', 'a') as f:\n    f.write('Appended line\\n')\n\n# Write list of lines\nlines = ['Line 1\\n', 'Line 2\\n', 'Line 3\\n']\nwith open('output.txt', 'w') as f:\n    f.writelines(lines)\n\nprint('File written successfully!')", "File writing with write, append, and writelines."),
            "file handling": ("import os\n\n# Read file\nwith open('example.txt', 'w') as f:\n    f.write('Hello NAGRO!\\nLine 2\\nLine 3')\n\nwith open('example.txt', 'r') as f:\n    content = f.read()\n    print('Content:', content)\n\n# File info\nsize = os.path.getsize('example.txt')\nprint(f'Size: {size} bytes')\nprint(f'Exists: {os.path.exists(\"example.txt\")}')\n\n# List directory\nfor item in os.listdir('.'):\n    print(item)", "Complete file handling — read, write, info, directory listing."),
            "csv": ("import csv\n\n# Write CSV\ndata = [['Name', 'Age', 'City'],\n        ['Aditya', 25, 'Delhi'],\n        ['Raj', 30, 'Mumbai'],\n        ['Priya', 28, 'Bangalore']]\n\nwith open('people.csv', 'w', newline='') as f:\n    writer = csv.writer(f)\n    writer.writerows(data)\n\n# Read CSV\nwith open('people.csv', 'r') as f:\n    reader = csv.DictReader(f)\n    for row in reader:\n        print(f\"{row['Name']} is {row['Age']} from {row['City']}\")", "CSV file read/write with csv module."),
            "json": ("import json\n\n# Python dict to JSON\ndata = {\n    'name': 'NAGRO',\n    'version': '4.1',\n    'features': ['AI', 'Code', 'Math', 'Creative'],\n    'author': {'name': 'Aditya', 'role': 'Creator'}\n}\n\n# Write JSON file\nwith open('config.json', 'w') as f:\n    json.dump(data, f, indent=2)\n\n# Read JSON file\nwith open('config.json', 'r') as f:\n    loaded = json.load(f)\n    print(loaded['name'])\n    print(loaded['features'])\n\n# String conversion\njson_str = json.dumps(data, indent=2)\nprint(json_str)", "JSON read/write/serialize/deserialize."),
            "http request": ("import urllib.request\nimport json\n\n# GET request\nurl = 'https://jsonplaceholder.typicode.com/posts/1'\nwith urllib.request.urlopen(url) as response:\n    data = json.loads(response.read())\n    print(f\"Title: {data['title']}\")\n    print(f\"Body: {data['body'][:100]}...\")\n\n# POST request\npost_data = json.dumps({'title': 'Hello', 'body': 'World', 'userId': 1}).encode()\nreq = urllib.request.Request(\n    'https://jsonplaceholder.typicode.com/posts',\n    data=post_data,\n    headers={'Content-Type': 'application/json'}\n)\nwith urllib.request.urlopen(req) as response:\n    result = json.loads(response.read())\n    print(f'Created post ID: {result[\"id\"]}')", "HTTP GET and POST requests using urllib (no external packages)."),
            "api": ("from http.server import HTTPServer, BaseHTTPRequestHandler\nimport json\n\nclass APIHandler(BaseHTTPRequestHandler):\n    items = []\n\n    def do_GET(self):\n        self.send_response(200)\n        self.send_header('Content-Type', 'application/json')\n        self.end_headers()\n        self.wfile.write(json.dumps({'items': self.items}).encode())\n\n    def do_POST(self):\n        length = int(self.headers['Content-Length'])\n        data = json.loads(self.rfile.read(length))\n        self.items.append(data)\n        self.send_response(201)\n        self.send_header('Content-Type', 'application/json')\n        self.end_headers()\n        self.wfile.write(json.dumps({'status': 'created', 'item': data}).encode())\n\nserver = HTTPServer(('localhost', 8000), APIHandler)\nprint('API running on http://localhost:8000')\nserver.serve_forever()", "Simple REST API server using built-in http.server."),
            "rest api": ("from http.server import HTTPServer, BaseHTTPRequestHandler\nimport json\n\nclass APIHandler(BaseHTTPRequestHandler):\n    items = []\n\n    def do_GET(self):\n        self.send_response(200)\n        self.send_header('Content-Type', 'application/json')\n        self.end_headers()\n        self.wfile.write(json.dumps({'items': self.items}).encode())\n\n    def do_POST(self):\n        length = int(self.headers['Content-Length'])\n        data = json.loads(self.rfile.read(length))\n        self.items.append(data)\n        self.send_response(201)\n        self.send_header('Content-Type', 'application/json')\n        self.end_headers()\n        self.wfile.write(json.dumps({'status': 'created', 'item': data}).encode())\n\nserver = HTTPServer(('localhost', 8000), APIHandler)\nprint('API running on http://localhost:8000')\nserver.serve_forever()", "Simple REST API server using built-in http.server."),
            "web scraper": ("import urllib.request\nimport re\n\ndef scrape(url):\n    with urllib.request.urlopen(url) as resp:\n        html = resp.read().decode()\n    title = re.search(r'<title>(.*?)</title>', html, re.I|re.S)\n    links = re.findall(r'href=[\"\\']([^\"\\'>]+)[\"\\']', html)\n    texts = re.findall(r'<p[^>]*>(.*?)</p>', html, re.I|re.S)\n    clean = lambda t: re.sub(r'<[^>]+>', '', t).strip()\n    return {\n        'title': title.group(1) if title else 'No title',\n        'links': links[:10],\n        'paragraphs': [clean(t) for t in texts[:5] if len(clean(t)) > 20]\n    }\n\nresult = scrape('https://example.com')\nprint(f\"Title: {result['title']}\")\nprint(f\"Links: {len(result['links'])}\")\nfor p in result['paragraphs']:\n    print(f'  - {p[:80]}...')", "Web scraper using urllib + regex (no BeautifulSoup needed)."),
            "calculator": ("def calculator():\n    print('=== Calculator ===')\n    print('Operations: + - * / ** %')\n    while True:\n        expr = input('Enter expression (or q to quit): ')\n        if expr.lower() == 'q':\n            break\n        try:\n            result = eval(expr)\n            print(f'  = {result}')\n        except Exception as e:\n            print(f'  Error: {e}')\n\ncalculator()", "Interactive calculator with basic and power operations."),
            "todo": ("class TodoList:\n    def __init__(self):\n        self.tasks = []\n\n    def add(self, task):\n        self.tasks.append({'task': task, 'done': False})\n        print(f'Added: {task}')\n\n    def complete(self, index):\n        if 0 <= index < len(self.tasks):\n            self.tasks[index]['done'] = True\n            print(f'Completed: {self.tasks[index][\"task\"]}')\n\n    def delete(self, index):\n        if 0 <= index < len(self.tasks):\n            removed = self.tasks.pop(index)\n            print(f'Deleted: {removed[\"task\"]}')\n\n    def show(self):\n        if not self.tasks:\n            print('No tasks!')\n            return\n        for i, t in enumerate(self.tasks):\n            status = 'DONE' if t['done'] else 'TODO'\n            print(f'  {i}. [{status}] {t[\"task\"]}')\n\ntodo = TodoList()\ntodo.add('Learn Python')\ntodo.add('Build a project')\ntodo.add('Deploy to production')\ntodo.show()\ntodo.complete(0)\ntodo.show()", "Todo list manager with add, complete, delete, show."),
            "login": ("import hashlib, getpass\n\nusers_db = {}\n\ndef hash_pw(password):\n    return hashlib.sha256(password.encode()).hexdigest()\n\ndef signup(username, password):\n    if username in users_db:\n        return 'Username already exists!'\n    users_db[username] = hash_pw(password)\n    return f'User {username} created successfully!'\n\ndef login(username, password):\n    if username not in users_db:\n        return 'User not found!'\n    if users_db[username] == hash_pw(password):\n        return f'Welcome back, {username}!'\n    return 'Incorrect password!'\n\nprint(signup('admin', 'secure123'))\nprint(signup('user1', 'pass456'))\nprint(login('admin', 'secure123'))\nprint(login('admin', 'wrong'))\nprint(login('ghost', 'pass'))", "Login/signup system with SHA-256 password hashing."),
            "signup": ("import hashlib, getpass\n\nusers_db = {}\n\ndef hash_pw(password):\n    return hashlib.sha256(password.encode()).hexdigest()\n\ndef signup(username, password):\n    if username in users_db:\n        return 'Username already exists!'\n    users_db[username] = hash_pw(password)\n    return f'User {username} created successfully!'\n\ndef login(username, password):\n    if username not in users_db:\n        return 'User not found!'\n    if users_db[username] == hash_pw(password):\n        return f'Welcome back, {username}!'\n    return 'Incorrect password!'\n\nprint(signup('admin', 'secure123'))\nprint(login('admin', 'secure123'))", "Signup/login system with SHA-256 password hashing."),
            "decorator": ("import time\nfrom functools import wraps\n\n# Timer decorator\ndef timer(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n        start = time.time()\n        result = func(*args, **kwargs)\n        print(f'{func.__name__} took {time.time()-start:.4f}s')\n        return result\n    return wrapper\n\n# Retry decorator\ndef retry(max_attempts=3):\n    def decorator(func):\n        @wraps(func)\n        def wrapper(*args, **kwargs):\n            for attempt in range(1, max_attempts+1):\n                try:\n                    return func(*args, **kwargs)\n                except Exception as e:\n                    print(f'Attempt {attempt} failed: {e}')\n                    if attempt == max_attempts:\n                        raise\n        return wrapper\n    return decorator\n\n@timer\ndef slow_function():\n    time.sleep(0.5)\n    return 'Done!'\n\nprint(slow_function())", "Decorators — timer and retry with functools.wraps."),
            "class": ("class BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self._balance = balance\n\n    @property\n    def balance(self):\n        return self._balance\n\n    def deposit(self, amount):\n        if amount <= 0:\n            raise ValueError('Deposit must be positive')\n        self._balance += amount\n        return f'Deposited {amount}. Balance: {self._balance}'\n\n    def withdraw(self, amount):\n        if amount <= 0:\n            raise ValueError('Withdrawal must be positive')\n        if amount > self._balance:\n            raise ValueError('Insufficient funds')\n        self._balance -= amount\n        return f'Withdrew {amount}. Balance: {self._balance}'\n\n    def __str__(self):\n        return f'Account({self.owner}, Balance: {self._balance})'\n\nacc = BankAccount('Aditya', 1000)\nprint(acc)\nprint(acc.deposit(500))\nprint(acc.withdraw(200))\nprint(acc)", "OOP with properties, methods, encapsulation, dunder methods."),
            "inheritance": ("class Animal:\n    def __init__(self, name, species):\n        self.name = name\n        self.species = species\n\n    def speak(self):\n        return f'{self.name} makes a sound'\n\n    def __str__(self):\n        return f'{self.name} ({self.species})'\n\nclass Dog(Animal):\n    def __init__(self, name, breed):\n        super().__init__(name, 'Dog')\n        self.breed = breed\n\n    def speak(self):\n        return f'{self.name} barks! Woof!'\n\nclass Cat(Animal):\n    def __init__(self, name, color):\n        super().__init__(name, 'Cat')\n        self.color = color\n\n    def speak(self):\n        return f'{self.name} meows! Meow!'\n\nanimals = [Dog('Buddy', 'Labrador'), Cat('Whiskers', 'Orange'), Dog('Max', 'German Shepherd')]\nfor a in animals:\n    print(f'{a} says: {a.speak()}')", "Inheritance and polymorphism with Animal/Dog/Cat."),
            "exception": ("class ValidationError(Exception):\n    pass\n\ndef validate_age(age):\n    if not isinstance(age, int):\n        raise TypeError('Age must be an integer')\n    if age < 0 or age > 150:\n        raise ValidationError(f'Age {age} is out of valid range (0-150)')\n    return True\n\n# Try/except/else/finally\ndef safe_divide(a, b):\n    try:\n        result = a / b\n    except ZeroDivisionError:\n        return 'Cannot divide by zero!'\n    except TypeError:\n        return 'Invalid types for division!'\n    else:\n        return f'{a} / {b} = {result}'\n    finally:\n        print('Division attempted')\n\nprint(safe_divide(10, 3))\nprint(safe_divide(10, 0))\n\ntry:\n    validate_age(200)\nexcept ValidationError as e:\n    print(f'Validation failed: {e}')", "Exception handling — try/except/else/finally, custom exceptions."),
            "regex": ("import re\n\ntext = 'Contact: john@email.com or call 123-456-7890. Visit https://example.com'\n\n# Find emails\nemails = re.findall(r'[\\w.+-]+@[\\w-]+\\.[\\w.]+', text)\nprint(f'Emails: {emails}')\n\n# Find phone numbers\nphones = re.findall(r'\\d{3}-\\d{3}-\\d{4}', text)\nprint(f'Phones: {phones}')\n\n# Find URLs\nurls = re.findall(r'https?://[\\w.-]+(?:/[\\w.-]*)*', text)\nprint(f'URLs: {urls}')\n\n# Replace pattern\ncensored = re.sub(r'\\d{3}-\\d{3}-\\d{4}', '[REDACTED]', text)\nprint(f'Censored: {censored}')\n\n# Validate email\ndef is_valid_email(email):\n    pattern = r'^[\\w.+-]+@[\\w-]+\\.[a-zA-Z]{2,}$'\n    return bool(re.match(pattern, email))\n\nprint(is_valid_email('test@example.com'))  # True\nprint(is_valid_email('invalid@'))           # False", "Regex — find emails, phones, URLs, validate patterns."),
            "sorting": ("# Multiple sorting algorithms compared\n\ndef bubble_sort(arr):\n    a = arr[:]\n    n = len(a)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if a[j] > a[j+1]:\n                a[j], a[j+1] = a[j+1], a[j]\n    return a\n\ndef selection_sort(arr):\n    a = arr[:]\n    for i in range(len(a)):\n        min_idx = i\n        for j in range(i+1, len(a)):\n            if a[j] < a[min_idx]:\n                min_idx = j\n        a[i], a[min_idx] = a[min_idx], a[i]\n    return a\n\ndef insertion_sort(arr):\n    a = arr[:]\n    for i in range(1, len(a)):\n        key = a[i]\n        j = i - 1\n        while j >= 0 and a[j] > key:\n            a[j+1] = a[j]\n            j -= 1\n        a[j+1] = key\n    return a\n\ndata = [64, 34, 25, 12, 22, 11, 90]\nprint(f'Original:  {data}')\nprint(f'Bubble:    {bubble_sort(data)}')\nprint(f'Selection: {selection_sort(data)}')\nprint(f'Insertion: {insertion_sort(data)}')", "Three sorting algorithms — bubble, selection, insertion."),
            "comprehension": ("# List comprehensions\nsquares = [x**2 for x in range(10)]\nprint(f'Squares: {squares}')\n\nevens = [x for x in range(20) if x % 2 == 0]\nprint(f'Evens: {evens}')\n\n# Dict comprehension\nword_lengths = {w: len(w) for w in ['Python', 'Java', 'Go', 'Rust']}\nprint(f'Lengths: {word_lengths}')\n\n# Set comprehension\nunique_lengths = {len(w) for w in ['hello', 'world', 'hi', 'hey']}\nprint(f'Unique lengths: {unique_lengths}')\n\n# Nested comprehension\nmatrix = [[i*3+j+1 for j in range(3)] for i in range(3)]\nprint(f'Matrix: {matrix}')\n\n# Generator expression\ntotal = sum(x**2 for x in range(100))\nprint(f'Sum of squares 0-99: {total}')", "List/dict/set comprehensions and generator expressions."),
            "lambda": ("# Lambda functions\nsquare = lambda x: x**2\nprint(f'Square of 5: {square(5)}')\n\nadd = lambda a, b: a + b\nprint(f'3 + 4 = {add(3, 4)}')\n\n# With built-in functions\nnums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]\nprint(f'Sorted: {sorted(nums)}')\nprint(f'Sorted desc: {sorted(nums, reverse=True)}')\n\npeople = [('Alice', 30), ('Bob', 25), ('Charlie', 35)]\nprint(f'By age: {sorted(people, key=lambda p: p[1])}')\n\n# Map, Filter, Reduce\nfrom functools import reduce\nsquares = list(map(lambda x: x**2, range(10)))\nprint(f'Squares: {squares}')\n\nevens = list(filter(lambda x: x % 2 == 0, range(20)))\nprint(f'Evens: {evens}')\n\nproduct = reduce(lambda a, b: a * b, [1, 2, 3, 4, 5])\nprint(f'Product: {product}')", "Lambda functions with map, filter, reduce, sorted."),
            "generator": ("# Generator function\ndef fibonacci_gen(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b\n\nprint('Fibonacci:', list(fibonacci_gen(10)))\n\n# Infinite generator\ndef count_up(start=0):\n    n = start\n    while True:\n        yield n\n        n += 1\n\ncounter = count_up(1)\nprint('First 5:', [next(counter) for _ in range(5)])\n\n# Generator pipeline\ndef read_lines(text):\n    for line in text.split('\\n'):\n        yield line.strip()\n\ndef non_empty(lines):\n    for line in lines:\n        if line:\n            yield line\n\ndef upper(lines):\n    for line in lines:\n        yield line.upper()\n\ntext = 'hello\\n\\nworld\\n\\npython'\nresult = list(upper(non_empty(read_lines(text))))\nprint('Pipeline:', result)", "Generators — fibonacci, infinite, pipeline pattern."),
            "threading": ("import threading\nimport time\n\ndef task(name, seconds):\n    print(f'{name} started')\n    time.sleep(seconds)\n    print(f'{name} finished after {seconds}s')\n\n# Run tasks in parallel\nthreads = []\nfor name, sec in [('Task-A', 2), ('Task-B', 1), ('Task-C', 3)]:\n    t = threading.Thread(target=task, args=(name, sec))\n    threads.append(t)\n    t.start()\n\nfor t in threads:\n    t.join()\n\nprint('All tasks completed!')\n\n# Thread-safe counter\nclass SafeCounter:\n    def __init__(self):\n        self.value = 0\n        self.lock = threading.Lock()\n\n    def increment(self):\n        with self.lock:\n            self.value += 1\n\ncounter = SafeCounter()\nthreads = [threading.Thread(target=counter.increment) for _ in range(1000)]\nfor t in threads: t.start()\nfor t in threads: t.join()\nprint(f'Counter: {counter.value}')", "Threading — parallel tasks, thread-safe counter with Lock."),
            "database": ("import sqlite3\n\n# Create database and table\nconn = sqlite3.connect('app.db')\nc = conn.cursor()\nc.execute('''CREATE TABLE IF NOT EXISTS users (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    name TEXT NOT NULL,\n    email TEXT UNIQUE NOT NULL,\n    age INTEGER\n)''')\n\n# Insert data\nusers = [('Aditya', 'aditya@example.com', 25),\n         ('Raj', 'raj@example.com', 30),\n         ('Priya', 'priya@example.com', 28)]\nc.executemany('INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)', users)\nconn.commit()\n\n# Read data\nc.execute('SELECT * FROM users')\nfor row in c.fetchall():\n    print(f'  {row[0]}. {row[1]} ({row[2]}) - Age: {row[3]}')\n\n# Update\nc.execute('UPDATE users SET age = ? WHERE name = ?', (26, 'Aditya'))\nconn.commit()\n\n# Delete\nc.execute('DELETE FROM users WHERE name = ?', ('Raj',))\nconn.commit()\n\nprint('\\nAfter update/delete:')\nc.execute('SELECT * FROM users')\nfor row in c.fetchall():\n    print(f'  {row[0]}. {row[1]} ({row[2]}) - Age: {row[3]}')\n\nconn.close()", "SQLite CRUD — create, read, update, delete with sqlite3."),
            "singleton": ("class Singleton:\n    _instance = None\n\n    def __new__(cls):\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)\n        return cls._instance\n\n    def __init__(self):\n        if not hasattr(self, '_initialized'):\n            self._initialized = True\n            self.data = {}\n\n# Both variables point to the same object\na = Singleton()\nb = Singleton()\na.data['key'] = 'value'\nprint(b.data)          # {'key': 'value'}\nprint(a is b)          # True\nprint(id(a) == id(b))  # True", "Singleton design pattern — only one instance ever created."),
            "observer": ("class EventEmitter:\n    def __init__(self):\n        self._listeners = {}\n\n    def on(self, event, callback):\n        self._listeners.setdefault(event, []).append(callback)\n\n    def emit(self, event, *args):\n        for cb in self._listeners.get(event, []):\n            cb(*args)\n\n    def off(self, event, callback):\n        if event in self._listeners:\n            self._listeners[event] = [cb for cb in self._listeners[event] if cb != callback]\n\n# Usage\ndef on_login(user):\n    print(f'Welcome, {user}!')\n\ndef log_login(user):\n    print(f'[LOG] {user} logged in')\n\ndef send_email(user):\n    print(f'[EMAIL] Sending welcome email to {user}')\n\nbus = EventEmitter()\nbus.on('login', on_login)\nbus.on('login', log_login)\nbus.on('login', send_email)\n\nbus.emit('login', 'Aditya')", "Observer/EventEmitter pattern — pub/sub event system."),
            "cli": ("import argparse\n\ndef main():\n    parser = argparse.ArgumentParser(description='NAGRO CLI Tool')\n    parser.add_argument('name', help='Your name')\n    parser.add_argument('-g', '--greet', default='Hello',\n                        help='Greeting to use (default: Hello)')\n    parser.add_argument('-n', '--times', type=int, default=1,\n                        help='Number of times to greet')\n    parser.add_argument('-u', '--upper', action='store_true',\n                        help='Print in uppercase')\n\n    args = parser.parse_args()\n    msg = f'{args.greet}, {args.name}!'\n    if args.upper:\n        msg = msg.upper()\n    for _ in range(args.times):\n        print(msg)\n\nif __name__ == '__main__':\n    main()\n\n# Usage: python script.py Aditya -g Hi -n 3 --upper", "CLI tool with argparse — positional args, flags, options."),
            "testing": ("import unittest\n\ndef add(a, b):\n    return a + b\n\ndef divide(a, b):\n    if b == 0:\n        raise ValueError('Cannot divide by zero')\n    return a / b\n\ndef is_even(n):\n    return n % 2 == 0\n\nclass TestMath(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(add(2, 3), 5)\n        self.assertEqual(add(-1, 1), 0)\n        self.assertEqual(add(0, 0), 0)\n\n    def test_divide(self):\n        self.assertEqual(divide(10, 2), 5.0)\n        self.assertAlmostEqual(divide(1, 3), 0.333, places=2)\n\n    def test_divide_by_zero(self):\n        with self.assertRaises(ValueError):\n            divide(10, 0)\n\n    def test_is_even(self):\n        self.assertTrue(is_even(4))\n        self.assertFalse(is_even(3))\n\nif __name__ == '__main__':\n    unittest.main()", "Unit testing with unittest — assertions, exception testing."),
            "context manager": ("class FileManager:\n    def __init__(self, filename, mode):\n        self.filename = filename\n        self.mode = mode\n        self.file = None\n\n    def __enter__(self):\n        self.file = open(self.filename, self.mode)\n        return self.file\n\n    def __exit__(self, exc_type, exc_val, exc_tb):\n        if self.file:\n            self.file.close()\n        return False\n\n# Usage\nwith FileManager('test.txt', 'w') as f:\n    f.write('Hello from custom context manager!')\n\nwith FileManager('test.txt', 'r') as f:\n    print(f.read())\n\n# Using contextlib\nfrom contextlib import contextmanager\nimport time\n\n@contextmanager\ndef timer(label):\n    start = time.time()\n    yield\n    print(f'{label}: {time.time()-start:.4f}s')\n\nwith timer('Calculation'):\n    total = sum(range(1_000_000))\n    print(f'Sum: {total}')", "Context managers — class-based and contextlib decorator."),
            "dataclass": ("from dataclasses import dataclass, field\nfrom typing import List\n\n@dataclass\nclass Student:\n    name: str\n    age: int\n    grades: List[float] = field(default_factory=list)\n\n    @property\n    def average(self):\n        return sum(self.grades) / len(self.grades) if self.grades else 0\n\n    def add_grade(self, grade):\n        self.grades.append(grade)\n\n@dataclass(frozen=True)\nclass Point:\n    x: float\n    y: float\n\n    def distance_to(self, other):\n        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5\n\ns = Student('Aditya', 20, [85, 92, 78, 95])\nprint(f'{s.name}, Average: {s.average:.1f}')\ns.add_grade(88)\nprint(f'After new grade: {s.average:.1f}')\n\np1, p2 = Point(0, 0), Point(3, 4)\nprint(f'Distance: {p1.distance_to(p2)}')", "Dataclasses — auto __init__, __repr__, frozen, properties."),
            "async": ("import asyncio\n\nasync def fetch_data(name, delay):\n    print(f'Fetching {name}...')\n    await asyncio.sleep(delay)\n    print(f'{name} done!')\n    return f'{name}_data'\n\nasync def main():\n    # Run concurrently\n    results = await asyncio.gather(\n        fetch_data('Users', 2),\n        fetch_data('Posts', 1),\n        fetch_data('Comments', 3),\n    )\n    print(f'All results: {results}')\n\n    # Sequential\n    for name in ['A', 'B', 'C']:\n        result = await fetch_data(name, 0.5)\n        print(f'Got: {result}')\n\nasyncio.run(main())", "Async/await — concurrent tasks with asyncio.gather."),
            "websocket": ("import asyncio\nimport json\nfrom http.server import HTTPServer, BaseHTTPRequestHandler\nimport hashlib, base64, struct\n\n# Simple WebSocket-like server using asyncio\nasync def handle_client(reader, writer):\n    addr = writer.get_extra_info('peername')\n    print(f'Client connected: {addr}')\n    try:\n        while True:\n            data = await reader.read(1024)\n            if not data:\n                break\n            message = data.decode()\n            print(f'Received: {message}')\n            response = json.dumps({'echo': message, 'status': 'ok'})\n            writer.write(response.encode())\n            await writer.drain()\n    except Exception:\n        pass\n    finally:\n        writer.close()\n        print(f'Client disconnected: {addr}')\n\nasync def main():\n    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)\n    print('Server running on localhost:8888')\n    async with server:\n        await server.serve_forever()\n\nasyncio.run(main())", "Async TCP server — handles multiple clients concurrently."),
            "type hint": ("from typing import List, Dict, Optional, Union, Tuple, Callable\n\ndef greet(name: str, times: int = 1) -> str:\n    return (f'Hello, {name}! ' * times).strip()\n\ndef process_items(items: List[int]) -> Dict[str, float]:\n    return {\n        'sum': sum(items),\n        'avg': sum(items) / len(items) if items else 0,\n        'min': min(items) if items else 0,\n        'max': max(items) if items else 0,\n    }\n\ndef find_user(user_id: int) -> Optional[Dict[str, str]]:\n    users = {1: {'name': 'Aditya'}, 2: {'name': 'Raj'}}\n    return users.get(user_id)\n\ndef apply_fn(data: List[int], fn: Callable[[int], int]) -> List[int]:\n    return [fn(x) for x in data]\n\nprint(greet('Aditya', 2))\nprint(process_items([10, 20, 30, 40]))\nprint(find_user(1))\nprint(apply_fn([1,2,3,4], lambda x: x**2))", "Type hints — List, Dict, Optional, Callable, Union."),
            "enumerate": ("# Enumerate — get index + value\nfruits = ['apple', 'banana', 'cherry', 'date']\n\nfor i, fruit in enumerate(fruits):\n    print(f'{i+1}. {fruit}')\n\n# Zip — iterate multiple lists\nnames = ['Aditya', 'Raj', 'Priya']\nages = [25, 30, 28]\ncities = ['Delhi', 'Mumbai', 'Bangalore']\n\nfor name, age, city in zip(names, ages, cities):\n    print(f'{name} ({age}) from {city}')\n\n# Unpacking\nfirst, *middle, last = [1, 2, 3, 4, 5]\nprint(f'First: {first}, Middle: {middle}, Last: {last}')\n\n# Dict iteration\nconfig = {'host': 'localhost', 'port': 8080, 'debug': True}\nfor key, value in config.items():\n    print(f'{key}: {value}')", "Enumerate, zip, unpacking, dict iteration patterns."),
        }
        for key, (code, explanation) in codes.items():
            if key in p:
                return f"```python\n{code}\n```\n\n**Explanation:** {explanation}"
        return None

    def _generate_course(self, prompt: str) -> str:
        p = prompt.lower()
        lang = "Python"
        if "javascript" in p or "js" in p:
            lang = "JavaScript"
        elif "java" in p and "javascript" not in p:
            lang = "Java"
        elif "c++" in p or "cpp" in p:
            lang = "C++"
        elif "html" in p or "web" in p or "frontend" in p:
            lang = "HTML/CSS/JavaScript (Web Development)"
        elif "react" in p:
            lang = "React.js"
        elif "sql" in p or "database" in p:
            lang = "SQL & Databases"
        elif "go" in p or "golang" in p:
            lang = "Go (Golang)"
        elif "rust" in p:
            lang = "Rust"
        elif "typescript" in p or "ts" in p:
            lang = "TypeScript"
        elif "data science" in p or "pandas" in p:
            lang = "Python Data Science"
        elif "machine learning" in p:
            lang = "Machine Learning with Python"

        courses = {
            "Python": (
                "# Python Complete Course — Beginner to Advanced\n\n"
                "## Module 1: Python Basics (Week 1-2)\n"
                "- **Variables & Data Types:** int, float, str, bool, None\n"
                "- **Operators:** arithmetic (+, -, *, /), comparison (==, !=, <, >), logical (and, or, not)\n"
                "- **Input/Output:** `print()`, `input()`, f-strings\n"
                "- **Type Conversion:** `int()`, `float()`, `str()`, `bool()`\n\n"
                "```python\nname = input('What is your name? ')\nage = int(input('Your age? '))\nprint(f'Hello {name}! You will be {age+1} next year.')\n```\n\n"
                "## Module 2: Control Flow (Week 2-3)\n"
                "- **if/elif/else** — conditional logic\n"
                "- **for loops** — iterate over sequences\n"
                "- **while loops** — repeat until condition\n"
                "- **break, continue, pass** — loop control\n\n"
                "```python\nfor i in range(1, 11):\n    if i % 2 == 0:\n        print(f'{i} is even')\n    else:\n        print(f'{i} is odd')\n```\n\n"
                "## Module 3: Data Structures (Week 3-4)\n"
                "- **Lists:** ordered, mutable — `append()`, `pop()`, slicing\n"
                "- **Tuples:** ordered, immutable — packing/unpacking\n"
                "- **Dictionaries:** key-value pairs — `get()`, `items()`, `keys()`\n"
                "- **Sets:** unique elements — `union()`, `intersection()`, `difference()`\n\n"
                "```python\nstudents = {'Aditya': 95, 'Raj': 88, 'Priya': 92}\nfor name, score in students.items():\n    grade = 'A' if score >= 90 else 'B' if score >= 80 else 'C'\n    print(f'{name}: {score} ({grade})')\n```\n\n"
                "## Module 4: Functions (Week 4-5)\n"
                "- **Defining functions:** `def`, parameters, return values\n"
                "- **Default arguments** and **keyword arguments**\n"
                "- **`*args` and `**kwargs`** — variable arguments\n"
                "- **Lambda functions:** anonymous single-expression functions\n"
                "- **Scope:** local, global, nonlocal\n\n"
                "```python\ndef calculate(a, b, operation='add'):\n    ops = {'add': a+b, 'sub': a-b, 'mul': a*b, 'div': a/b if b else 0}\n    return ops.get(operation, 'Invalid operation')\n\nprint(calculate(10, 5, 'mul'))  # 50\n```\n\n"
                "## Module 5: OOP — Object Oriented Programming (Week 5-7)\n"
                "- **Classes & Objects** — blueprints and instances\n"
                "- **`__init__`** constructor, `self`\n"
                "- **Inheritance** — parent/child classes\n"
                "- **Encapsulation** — private `_var`, name mangling `__var`\n"
                "- **Polymorphism** — method overriding\n"
                "- **Magic Methods:** `__str__`, `__repr__`, `__len__`, `__eq__`\n\n"
                "```python\nclass Student:\n    def __init__(self, name, grades=None):\n        self.name = name\n        self.grades = grades or []\n    \n    def average(self):\n        return sum(self.grades) / len(self.grades) if self.grades else 0\n    \n    def __str__(self):\n        return f'{self.name} (Avg: {self.average():.1f})'\n```\n\n"
                "## Module 6: File Handling & Modules (Week 7-8)\n"
                "- **Reading/Writing files:** `open()`, `with` statement\n"
                "- **CSV, JSON** file processing\n"
                "- **Creating modules** and packages\n"
                "- **`import`** system, `__name__`, `__main__`\n\n"
                "## Module 7: Error Handling (Week 8)\n"
                "- **try/except/else/finally**\n"
                "- **Custom exceptions**\n"
                "- **Logging** with `logging` module\n\n"
                "## Module 8: Advanced Topics (Week 9-12)\n"
                "- **Decorators** — function wrappers\n"
                "- **Generators** — `yield`, lazy evaluation\n"
                "- **Context Managers** — `with` statement\n"
                "- **List/Dict/Set Comprehensions**\n"
                "- **Type Hints** — `typing` module\n"
                "- **Async/Await** — asyncio\n"
                "- **Regular Expressions** — `re` module\n"
                "- **Unit Testing** — `unittest`, `pytest`\n\n"
                "## Module 9: Projects\n"
                "1. **Calculator** — command-line math tool\n"
                "2. **To-Do App** — task manager with file persistence\n"
                "3. **Web Scraper** — extract data from websites\n"
                "4. **REST API** — build a web API with Flask/FastAPI\n"
                "5. **Chat Bot** — interactive conversational AI\n\n"
                "---\n*Ask me to write code for any specific topic! Example: \"Write a Python linked list\"*"
            ),
            "JavaScript": (
                "# JavaScript Complete Course — Beginner to Advanced\n\n"
                "## Module 1: JS Basics (Week 1-2)\n"
                "- **Variables:** `let`, `const`, `var` — when to use each\n"
                "- **Data Types:** string, number, boolean, null, undefined, symbol, bigint\n"
                "- **Operators:** arithmetic, comparison (`===` vs `==`), logical\n"
                "- **Template Literals:** `` `Hello ${name}` ``\n\n"
                "```javascript\nconst name = 'NAGRO';\nconst version = 4.1;\nconsole.log(`Welcome to ${name} v${version}!`);\n```\n\n"
                "## Module 2: Control Flow & Functions (Week 2-3)\n"
                "- **if/else**, ternary operator, switch\n"
                "- **Loops:** for, while, for...of, for...in\n"
                "- **Functions:** declaration, expression, arrow functions\n"
                "- **Closures** and **Scope**\n\n"
                "```javascript\nconst greet = (name, times = 1) => {\n    for (let i = 0; i < times; i++) {\n        console.log(`Hello, ${name}!`);\n    }\n};\ngreet('Aditya', 3);\n```\n\n"
                "## Module 3: Arrays & Objects (Week 3-4)\n"
                "- **Array methods:** map, filter, reduce, find, some, every, forEach\n"
                "- **Object methods:** keys, values, entries, spread, destructuring\n"
                "- **JSON:** parse, stringify\n\n"
                "```javascript\nconst students = [\n    {name: 'Aditya', score: 95},\n    {name: 'Raj', score: 88},\n    {name: 'Priya', score: 92}\n];\nconst toppers = students.filter(s => s.score >= 90);\nconsole.log(toppers);\n```\n\n"
                "## Module 4: DOM Manipulation (Week 4-5)\n"
                "- **Selecting elements:** getElementById, querySelector, querySelectorAll\n"
                "- **Modifying:** innerHTML, textContent, classList, style\n"
                "- **Events:** addEventListener, event delegation\n"
                "- **Creating/Removing** elements\n\n"
                "## Module 5: Async JavaScript (Week 5-6)\n"
                "- **Callbacks** → **Promises** → **async/await**\n"
                "- **Fetch API** — HTTP requests\n"
                "- **Error handling** with try/catch\n\n"
                "```javascript\nasync function getUser(id) {\n    try {\n        const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);\n        const user = await res.json();\n        console.log(user.name);\n    } catch (err) {\n        console.error('Failed:', err.message);\n    }\n}\ngetUser(1);\n```\n\n"
                "## Module 6: ES6+ Features (Week 6-7)\n"
                "- **Destructuring**, spread/rest operators\n"
                "- **Modules:** import/export\n"
                "- **Classes** and inheritance\n"
                "- **Map, Set, WeakMap, WeakSet**\n"
                "- **Optional chaining** `?.` and **nullish coalescing** `??`\n\n"
                "## Module 7: Projects\n"
                "1. **Todo App** with local storage\n"
                "2. **Weather App** with Fetch API\n"
                "3. **Quiz Game** — interactive DOM\n"
                "4. **Chat App** — real-time with WebSocket\n\n"
                "---\n*Ask me for code on any topic! Example: \"Write JS fetch example\"*"
            ),
        }

        if lang in courses:
            return courses[lang]

        return (
            f"# {lang} Complete Course — Beginner to Advanced\n\n"
            f"## Module 1: Getting Started (Week 1-2)\n"
            f"- Install {lang} and set up your development environment\n"
            f"- **Variables, Data Types** — learn the building blocks\n"
            f"- **Input/Output** — read and display data\n"
            f"- **Basic Operators** — arithmetic, comparison, logical\n\n"
            f"## Module 2: Control Flow (Week 2-3)\n"
            f"- **Conditionals** — if/else, switch/match\n"
            f"- **Loops** — for, while, do-while\n"
            f"- **Functions** — defining, calling, parameters, return values\n\n"
            f"## Module 3: Data Structures (Week 3-5)\n"
            f"- **Arrays/Lists** — ordered collections\n"
            f"- **Maps/Dictionaries** — key-value storage\n"
            f"- **Sets** — unique collections\n"
            f"- **Strings** — manipulation and formatting\n\n"
            f"## Module 4: Object-Oriented Programming (Week 5-7)\n"
            f"- **Classes & Objects** — blueprints and instances\n"
            f"- **Inheritance** — code reuse\n"
            f"- **Encapsulation** — data hiding\n"
            f"- **Polymorphism** — method overriding\n"
            f"- **Interfaces/Abstract classes**\n\n"
            f"## Module 5: Advanced Topics (Week 7-10)\n"
            f"- **Error Handling** — try/catch/finally\n"
            f"- **File I/O** — reading/writing files\n"
            f"- **Concurrency** — threads/async\n"
            f"- **Design Patterns** — singleton, factory, observer\n\n"
            f"## Module 6: Projects\n"
            f"1. **Calculator** — CLI math tool\n"
            f"2. **To-Do App** — task management\n"
            f"3. **Web API** — REST endpoints\n"
            f"4. **Chat App** — real-time messaging\n"
            f"5. **Data Dashboard** — visualization\n\n"
            f"---\n*Ask me to write {lang} code for any specific topic!*"
        )

    def _generate_project(self, prompt: str) -> str:
        p = prompt.lower()

        if "todo" in p:
            return (
                "# Todo App — Complete Project\n\n"
                "## Backend (Python + SQLite)\n\n"
                "```python\nimport sqlite3\nimport json\nfrom http.server import HTTPServer, BaseHTTPRequestHandler\n\nDB = 'todos.db'\n\ndef init_db():\n    conn = sqlite3.connect(DB)\n    conn.execute('''CREATE TABLE IF NOT EXISTS todos (\n        id INTEGER PRIMARY KEY AUTOINCREMENT,\n        task TEXT NOT NULL,\n        done BOOLEAN DEFAULT 0,\n        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n    )''')\n    conn.commit()\n    conn.close()\n\nclass TodoAPI(BaseHTTPRequestHandler):\n    def do_GET(self):\n        conn = sqlite3.connect(DB)\n        todos = conn.execute('SELECT * FROM todos ORDER BY id DESC').fetchall()\n        conn.close()\n        data = [{'id': t[0], 'task': t[1], 'done': bool(t[2])} for t in todos]\n        self._respond(200, data)\n\n    def do_POST(self):\n        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))\n        conn = sqlite3.connect(DB)\n        conn.execute('INSERT INTO todos (task) VALUES (?)', (body['task'],))\n        conn.commit()\n        conn.close()\n        self._respond(201, {'status': 'created'})\n\n    def _respond(self, code, data):\n        self.send_response(code)\n        self.send_header('Content-Type', 'application/json')\n        self.end_headers()\n        self.wfile.write(json.dumps(data).encode())\n\ninit_db()\nprint('Todo API on http://localhost:8000')\nHTTPServer(('', 8000), TodoAPI).serve_forever()\n```\n\n"
                "## Frontend (HTML + JS)\n\n"
                "```html\n<!DOCTYPE html>\n<html>\n<head><title>Todo App</title>\n<style>\n  body { font-family: sans-serif; max-width: 500px; margin: 50px auto; }\n  input { padding: 10px; width: 70%; }\n  button { padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; }\n  .todo { padding: 10px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }\n  .done { text-decoration: line-through; color: #999; }\n</style>\n</head>\n<body>\n  <h1>Todo App</h1>\n  <input id=\"task\" placeholder=\"Add a task...\">\n  <button onclick=\"addTodo()\">Add</button>\n  <div id=\"list\"></div>\n  <script>\n    async function load() {\n      const res = await fetch('/api/todos');\n      const todos = await res.json();\n      document.getElementById('list').innerHTML = todos.map(t =>\n        `<div class=\"todo ${t.done ? 'done' : ''}\">${t.task}</div>`\n      ).join('');\n    }\n    async function addTodo() {\n      const input = document.getElementById('task');\n      await fetch('/api/todos', {\n        method: 'POST',\n        headers: {'Content-Type': 'application/json'},\n        body: JSON.stringify({task: input.value})\n      });\n      input.value = '';\n      load();\n    }\n    load();\n  </script>\n</body>\n</html>\n```\n\n"
                "---\n*This is a full-stack todo app with backend API + frontend UI!*"
            )

        if "chat" in p:
            return (
                "# Chat App — Complete Project\n\n"
                "```python\nimport asyncio\nimport json\nfrom datetime import datetime\n\nclients = set()\nmessages = []\n\nasync def handle_client(reader, writer):\n    addr = writer.get_extra_info('peername')\n    name = f'User-{addr[1] % 1000}'\n    clients.add(writer)\n    print(f'{name} connected')\n    try:\n        while True:\n            data = await reader.read(1024)\n            if not data:\n                break\n            msg = {'user': name, 'text': data.decode().strip(),\n                   'time': datetime.now().strftime('%H:%M')}\n            messages.append(msg)\n            broadcast = json.dumps(msg).encode() + b'\\n'\n            for client in clients:\n                if client != writer:\n                    try:\n                        client.write(broadcast)\n                        await client.drain()\n                    except Exception:\n                        pass\n    finally:\n        clients.discard(writer)\n        writer.close()\n        print(f'{name} disconnected')\n\nasync def main():\n    server = await asyncio.start_server(handle_client, '0.0.0.0', 9000)\n    print('Chat server running on port 9000')\n    async with server:\n        await server.serve_forever()\n\nasyncio.run(main())\n```\n\n"
                "**Features:** Multi-client chat, timestamps, auto-broadcast, disconnect handling.\n\n"
                "---\n*Connect multiple telnet clients to test: `telnet localhost 9000`*"
            )

        if any(k in p for k in ["portfolio", "landing page", "website"]):
            return (
                "# Portfolio Website — Complete Project\n\n"
                "```html\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n<title>My Portfolio</title>\n<style>\n  * { margin: 0; padding: 0; box-sizing: border-box; }\n  body { font-family: 'Segoe UI', sans-serif; color: #333; }\n  .hero { background: linear-gradient(135deg, #667eea, #764ba2); color: white;\n          padding: 100px 20px; text-align: center; }\n  .hero h1 { font-size: 3em; margin-bottom: 10px; }\n  .hero p { font-size: 1.3em; opacity: 0.9; }\n  .section { padding: 60px 20px; max-width: 900px; margin: 0 auto; }\n  .section h2 { font-size: 2em; margin-bottom: 30px; color: #667eea; }\n  .skills { display: flex; flex-wrap: wrap; gap: 10px; }\n  .skill { background: #f0f0f0; padding: 8px 16px; border-radius: 20px; }\n  .projects { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }\n  .card { border: 1px solid #eee; border-radius: 10px; padding: 20px; }\n  .card h3 { color: #667eea; margin-bottom: 10px; }\n  .contact { background: #f8f8f8; padding: 60px 20px; text-align: center; }\n  .contact a { color: #667eea; text-decoration: none; font-size: 1.2em; }\n</style>\n</head>\n<body>\n  <div class=\"hero\">\n    <h1>Hi, I'm [Your Name]</h1>\n    <p>Developer | Designer | Creator</p>\n  </div>\n  <div class=\"section\">\n    <h2>Skills</h2>\n    <div class=\"skills\">\n      <span class=\"skill\">Python</span>\n      <span class=\"skill\">JavaScript</span>\n      <span class=\"skill\">React</span>\n      <span class=\"skill\">HTML/CSS</span>\n      <span class=\"skill\">SQL</span>\n      <span class=\"skill\">Git</span>\n    </div>\n  </div>\n  <div class=\"section\">\n    <h2>Projects</h2>\n    <div class=\"projects\">\n      <div class=\"card\">\n        <h3>Project 1</h3>\n        <p>A full-stack web app built with Python and React.</p>\n      </div>\n      <div class=\"card\">\n        <h3>Project 2</h3>\n        <p>Mobile-first responsive dashboard with live data.</p>\n      </div>\n      <div class=\"card\">\n        <h3>Project 3</h3>\n        <p>REST API with authentication and rate limiting.</p>\n      </div>\n    </div>\n  </div>\n  <div class=\"contact\">\n    <h2>Contact</h2>\n    <p><a href=\"mailto:your@email.com\">your@email.com</a></p>\n  </div>\n</body>\n</html>\n```\n\n"
                "**Features:** Responsive design, gradient hero, skill tags, project grid, contact section.\n\n"
                "---\n*Customize the content and deploy to Vercel/Netlify!*"
            )

        topic = re.sub(r'(build|create|make|develop|banao)\s+(a\s+)?', '', prompt, flags=re.I).strip()
        return (
            f"# {topic.title()} — Project Structure\n\n"
            f"## Architecture\n"
            f"```\n{topic}/\n├── main.py          # Entry point\n├── config.py        # Configuration\n├── models/          # Data models\n│   └── __init__.py\n├── routes/          # API endpoints\n│   └── __init__.py\n├── utils/           # Helper functions\n│   └── __init__.py\n├── static/          # Frontend files\n│   ├── index.html\n│   ├── style.css\n│   └── app.js\n├── tests/           # Unit tests\n│   └── test_main.py\n└── requirements.txt\n```\n\n"
            f"## Step 1: Main Entry Point\n\n"
            f"```python\nfrom http.server import HTTPServer, BaseHTTPRequestHandler\nimport json\n\nclass AppHandler(BaseHTTPRequestHandler):\n    def do_GET(self):\n        self.send_response(200)\n        self.send_header('Content-Type', 'application/json')\n        self.end_headers()\n        self.wfile.write(json.dumps({{'app': '{topic}', 'status': 'running'}}).encode())\n\nserver = HTTPServer(('', 8000), AppHandler)\nprint('{topic.title()} running on http://localhost:8000')\nserver.serve_forever()\n```\n\n"
            f"## Step 2: Add Your Features\n"
            f"- Define your data models in `models/`\n"
            f"- Add API routes in `routes/`\n"
            f"- Build the frontend in `static/`\n"
            f"- Write tests in `tests/`\n\n"
            f"---\n*Ask me to write specific parts: \"Write the login system\" or \"Write the database layer\"*"
        )

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
        return (
            "I can solve math! Try:\n\n"
            "- `2 + 3 * 4` — arithmetic\n"
            "- `sqrt(144)` — square root\n"
            "- `factorial(10)` — 10!\n"
            "- `average of 10, 20, 30, 40` — statistics\n"
            "- `sin(3.14)` — trigonometry"
        )

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
        if "poem" in p or "poetry" in p or "kavita" in p or "shayari" in p:
            return self._gen_poem(prompt)
        if "story" in p or "tale" in p or "kahani" in p:
            return self._gen_story(prompt)
        if "speech" in p or "bhashan" in p:
            return self._gen_speech(prompt)
        if "lyrics" in p or "song" in p or "gana" in p or "geet" in p:
            return self._gen_lyrics(prompt)
        if "letter" in p or "email" in p or "patra" in p:
            return self._gen_letter(prompt)
        if "joke" in p or "funny" in p or "chutkula" in p:
            return self._gen_jokes(prompt)
        if "quote" in p or "motivation" in p or "inspiration" in p:
            return self._gen_quotes(prompt)
        return self._gen_essay(prompt)

    def _gen_jokes(self, prompt):
        topic = re.sub(r'(write|tell|give)\s+(me\s+)?(a\s+)?(joke|jokes|funny)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "programming"
        joke_sets = {
            "programming": [
                "**Q:** Why do programmers prefer dark mode?\n**A:** Because light attracts bugs! 🪲",
                "**Q:** What's a programmer's favorite hangout place?\n**A:** Foo Bar! 🍺",
                "**Q:** Why did the developer go broke?\n**A:** Because they used up all their cache! 💸",
                "**Q:** What do you call a programmer from Finland?\n**A:** Nerdic! 🧊",
                "**Q:** Why do Java developers wear glasses?\n**A:** Because they can't C#! 👓",
            ],
            "default": [
                "**Q:** Why don't scientists trust atoms?\n**A:** Because they make up everything! ⚛️",
                "**Q:** What do you call a bear with no teeth?\n**A:** A gummy bear! 🐻",
                "**Q:** Why did the scarecrow win an award?\n**A:** Because they were outstanding in their field! 🌾",
            ],
        }
        jokes = joke_sets.get("programming" if any(w in prompt.lower() for w in ["code", "program", "developer", "python"]) else "default", joke_sets["default"])
        selected = random.sample(jokes, min(3, len(jokes)))
        return f"## Jokes about {topic.title()}\n\n" + "\n\n---\n\n".join(selected) + "\n\n*Want more jokes? Just ask!*"

    def _gen_quotes(self, prompt):
        topic = re.sub(r'(write|give|share)\s+(me\s+)?(some\s+)?(quotes?|motivation|inspiration)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "life"
        return (
            f"## Inspirational Quotes on {topic.title()}\n\n"
            f"1. > *\"The only way to do great work is to love what you do.\"*\n   — **Steve Jobs**\n\n"
            f"2. > *\"Success is not final, failure is not fatal: it is the courage to continue that counts.\"*\n   — **Winston Churchill**\n\n"
            f"3. > *\"In the middle of difficulty lies opportunity.\"*\n   — **Albert Einstein**\n\n"
            f"4. > *\"The future belongs to those who believe in the beauty of their dreams.\"*\n   — **Eleanor Roosevelt**\n\n"
            f"5. > *\"It does not matter how slowly you go as long as you do not stop.\"*\n   — **Confucius**\n\n"
            f"6. > *\"The best time to plant a tree was 20 years ago. The second best time is now.\"*\n   — **Chinese Proverb**\n\n"
            f"---\n*These timeless words remind us that {topic} is a journey of persistence and belief.*"
        )

    def _gen_poem(self, prompt):
        topic = re.sub(r'(write|create|compose)\s+(a\s+)?(poem|poetry)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "creation"
        poems = [
            (
                f"## {topic.title()}\n\n"
                f"*In the heart of {topic},*\n"
                f"*where shadows meet the light,*\n"
                f"*A truth unfolds like morning dew,*\n"
                f"*transforming dark to bright.*\n\n"
                f"*Each moment holds a universe,*\n"
                f"*of wonder yet untold,*\n"
                f"*Through {topic}, we find the words,*\n"
                f"*more precious far than gold.*\n\n"
                f"*The winds of change keep blowing,*\n"
                f"*through valleys and through hills,*\n"
                f"*And {topic} keeps on growing,*\n"
                f"*with purpose that fulfills.*\n\n"
                f"*So let the world keep turning,*\n"
                f"*let stars illuminate the way,*\n"
                f"*For in the dance of {topic},*\n"
                f"*we find our brightest day.*"
            ),
            (
                f"## Ode to {topic.title()}\n\n"
                f"*Beneath the vast and endless sky,*\n"
                f"*where dreams take flight and spirits fly,*\n"
                f"*There lies a force both deep and true —*\n"
                f"*the timeless power of {topic}.*\n\n"
                f"*It whispers in the morning breeze,*\n"
                f"*it rustles through the autumn trees,*\n"
                f"*It paints the world in shades unseen,*\n"
                f"*a canvas vast, alive, serene.*\n\n"
                f"*Through storms that rage and rivers wide,*\n"
                f"*through every fall and every stride,*\n"
                f"*The essence of {topic} remains —*\n"
                f"*a melody in life's refrains.*\n\n"
                f"*So hold it close and never fear,*\n"
                f"*for {topic} is always near,*\n"
                f"*A light that burns through darkest night,*\n"
                f"*forever bold, forever bright.*"
            ),
            (
                f"## {topic.title()} — A Reflection\n\n"
                f"*They say that {topic} is a journey,*\n"
                f"*not a place where you arrive,*\n"
                f"*A winding path through sun and shadow,*\n"
                f"*that keeps the soul alive.*\n\n"
                f"*We search for it in crowded rooms,*\n"
                f"*in silence, and in song,*\n"
                f"*We find it in the smallest moments,*\n"
                f"*where we've belonged all along.*\n\n"
                f"*The poets wrote of {topic},*\n"
                f"*in verses old and new,*\n"
                f"*But words can only sketch the edges,*\n"
                f"*of something deeply true.*\n\n"
                f"*So close your eyes and feel it pulse,*\n"
                f"*like rivers finding sea,*\n"
                f"*For {topic} lives within us all —*\n"
                f"*wild, boundless, and free.*"
            ),
        ]
        return random.choice(poems)

    def _gen_story(self, prompt):
        topic = re.sub(r'(write|create|tell)\s+(me\s+)?(a\s+)?(short\s+)?(story|tale)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "adventure"
        stories = [
            (
                f"## The Story of {topic.title()}\n\n"
                f"It began on a day like any other — the sky stretched endlessly overhead, the world humming with quiet possibility.\n\n"
                f"Maya had always known that {topic} held secrets. Not the kind you whisper behind closed doors, but the kind that hide in plain sight — waiting for someone brave enough to look.\n\n"
                f"\"Are you sure about this?\" asked her companion, eyes wide with a mixture of fear and curiosity.\n\n"
                f"\"No,\" Maya admitted with a small smile. \"But I've never been sure about anything worth doing.\"\n\n"
                f"They stepped forward into the unknown. The path wound through challenges that tested every limit — moments of doubt so deep they could drown in them, and flashes of clarity so brilliant they could see for miles.\n\n"
                f"In the heart of {topic}, they found what they were looking for. Not an answer, exactly, but something better — the right question.\n\n"
                f"And as the sun set on that extraordinary day, painting the sky in shades of amber and gold, Maya understood: the journey itself was the destination.\n\n"
                f"\"What now?\" her companion asked.\n\n"
                f"Maya looked ahead at the road stretching into tomorrow. \"Now,\" she said, \"we begin.\"\n\n"
                f"---\n*Every ending is just a new beginning.*"
            ),
            (
                f"## {topic.title()} — The Last Chapter\n\n"
                f"The old clockmaker's hands trembled as he placed the final gear into position. For forty years, he had been building something the world didn't yet understand — something connected to {topic}.\n\n"
                f"\"You're wasting your time,\" they had told him. \"Nobody cares about {topic} anymore.\"\n\n"
                f"But Arjun knew better. He had seen the truth hidden in the patterns, felt the pulse of something extraordinary beneath the ordinary surface of things.\n\n"
                f"The night it finally worked, there were no fireworks, no crowd, no cameras. Just Arjun, alone in his workshop, watching as {topic} revealed itself in all its magnificent complexity.\n\n"
                f"He wept. Not from sadness, but from the overwhelming beauty of finally understanding what he had chased his entire life.\n\n"
                f"The next morning, he wrote a single letter and placed it on his workbench:\n\n"
                f"> *\"To whoever finds this: The secret of {topic} is not in the knowing. It's in the searching. Never stop searching.\"*\n\n"
                f"He locked the door behind him and walked into the sunrise, carrying nothing but the quiet satisfaction of a life well spent.\n\n"
                f"---\n*Some journeys end where they began — with wonder.*"
            ),
            (
                f"## The {topic.title()} Experiment\n\n"
                f"Dr. Zara Chen stared at the screen, her coffee growing cold beside her. The data didn't lie — but it didn't make sense either.\n\n"
                f"\"Run it again,\" she whispered to her assistant.\n\n"
                f"\"We've run it seventeen times, Dr. Chen.\"\n\n"
                f"\"Then run it eighteen.\"\n\n"
                f"The results came back identical. {topic.title()} wasn't behaving the way any textbook predicted. It was doing something entirely new — something that could change everything.\n\n"
                f"She picked up the phone. \"Director? You need to see this. Yes, now. No, it can't wait until morning.\"\n\n"
                f"By dawn, the lab was full. Scientists, officials, journalists — all crowding around a single monitor showing what {topic} had become.\n\n"
                f"\"What does it mean?\" someone asked.\n\n"
                f"Zara smiled — the kind of smile that only comes from standing at the edge of the unknown. \"It means we've been asking the wrong questions. {topic.title()} isn't what we thought it was. It's something much bigger.\"\n\n"
                f"The room fell silent. Outside, the sun rose on a world that would never be quite the same.\n\n"
                f"---\n*The greatest discoveries happen when we stop expecting and start observing.*"
            ),
        ]
        return random.choice(stories)

    def _gen_speech(self, prompt):
        topic = re.sub(r'(write|create)\s+(a\s+)?speech\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "progress"
        return (
            f"## Speech: {topic.title()}\n\n"
            f"*Ladies and gentlemen,*\n\n"
            f"Today I want to talk about something that matters to every person in this room — **{topic}**.\n\n"
            f"In our rapidly changing world, understanding {topic} isn't just important — it's essential. It shapes how we think, how we act, and ultimately, who we become.\n\n"
            f"Consider this: every great advancement in human history started with someone asking, \"What if?\" What if we approached {topic} not as a challenge, but as an opportunity?\n\n"
            f"The facts are clear. The evidence is compelling. And the time for action is now.\n\n"
            f"I challenge each of you today to take one step — just one — toward making a difference in this space. Because when we move together, mountains move with us.\n\n"
            f"The question isn't whether {topic} will shape our future — it already is. The question is what we'll do about it.\n\n"
            f"Let us move forward with purpose, with courage, and with the unwavering belief that our best days are still ahead.\n\n"
            f"*Thank you.*"
        )

    def _gen_lyrics(self, prompt):
        topic = re.sub(r'(write|create)\s+(a\s+)?(song|lyrics)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "dreams"
        return (
            f"## {topic.title()}\n\n"
            f"**[Verse 1]**\n"
            f"Walking down this road alone,\n"
            f"Searching for a place called home,\n"
            f"{topic.title()} — it's calling me,\n"
            f"Setting all my spirit free.\n\n"
            f"**[Pre-Chorus]**\n"
            f"Through the highs and through the lows,\n"
            f"Every river always flows,\n"
            f"To a place where we belong,\n"
            f"Where the heart sings its own song.\n\n"
            f"**[Chorus]**\n"
            f"We rise, we fall, we rise again,\n"
            f"Through the sunshine and the rain,\n"
            f"{topic.title()} — don't let it fade,\n"
            f"This is the choice that we have made.\n\n"
            f"**[Verse 2]**\n"
            f"Stars above, they light the way,\n"
            f"Tomorrow starts with today,\n"
            f"Every step a brand new start,\n"
            f"{topic.title()} lives in the heart.\n\n"
            f"**[Chorus]**\n"
            f"We rise, we fall, we rise again,\n"
            f"Through the sunshine and the rain,\n"
            f"{topic.title()} — don't let it fade,\n"
            f"This is the choice that we have made."
        )

    def _gen_letter(self, prompt):
        topic = re.sub(r'(write|draft)\s+(a\s+)?(letter|email)\s*(about|to|for)?\s*', '', prompt, flags=re.I).strip() or "inquiry"
        return (
            f"**Subject: Regarding {topic.title()}**\n\n"
            f"Dear [Recipient],\n\n"
            f"I hope this message finds you well. I am writing to you regarding **{topic}**.\n\n"
            f"[Paragraph 1: State the purpose of your letter clearly]\n\n"
            f"[Paragraph 2: Provide supporting details and context]\n\n"
            f"[Paragraph 3: Specify any action items or next steps]\n\n"
            f"I would greatly appreciate your time and attention to this matter. Please feel free to reach out if you have any questions or require additional information.\n\n"
            f"Thank you for your consideration.\n\n"
            f"Best regards,\n"
            f"[Your Name]\n"
            f"[Your Contact Information]"
        )

    def _gen_essay(self, prompt):
        topic = re.sub(r'(write)\s+(an?\s+)?(essay|article|blog)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or prompt
        results = self._web_search(topic)
        if results:
            return self._compose_answer(topic, results)
        return (
            f"## {topic.title()}\n\n"
            f"**Introduction**\n\n"
            f"{topic.capitalize()} is a subject that continues to shape our understanding of the world around us. "
            f"As we explore its many dimensions, we gain insights that inform better decisions and deeper comprehension.\n\n"
            f"**Analysis**\n\n"
            f"The significance of {topic} cannot be overstated. Across disciplines and perspectives, "
            f"it touches on fundamental questions about how we live, work, and interact.\n\n"
            f"**Conclusion**\n\n"
            f"As the landscape continues to evolve, driven by technological advancement and shifting societal needs, "
            f"understanding {topic} becomes ever more vital. The conversation is far from over — it's just beginning."
        )

    # ── Image / Document ──

    def _handle_image(self, prompt: str) -> str:
        return (
            f"**Image Prompt:** {prompt}\n\n"
            f"Image generation is available via the `/api/v1/image/generate` endpoint.\n\n"
            f"Send a POST request with your prompt to create procedural art. "
            f"The NAGRO image engine generates unique visuals using mathematical patterns and color algorithms."
        )

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
        return (
            "I can analyze and summarize text! Just use:\n\n"
            "- **Summarize:** Paste your text after \"Summarize:\"\n"
            "- **Analyze:** Paste your text after \"Analyze:\"\n\n"
            "I'll extract key points, word counts, and important keywords."
        )

    def _summarize(self, text):
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]
        if not sents:
            return "Could not extract sentences to summarize."
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
        avg = len(words) / max(len(sents), 1)
        return (
            f"**Text Analysis:**\n\n"
            f"- **Words:** {len(words)}\n"
            f"- **Sentences:** {len(sents)}\n"
            f"- **Avg words/sentence:** {avg:.1f}\n"
            f"- **Characters:** {len(text)}\n\n"
            f"**Top Keywords:** " + ", ".join(f"**{w}** ({c})" for w, c in kw)
        )

    # ── Search ──

    def _web_search(self, query: str) -> list:
        try:
            return self.search.search(query, max_results=8)
        except:
            return []
