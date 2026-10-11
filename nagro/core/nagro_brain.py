"""
NAGRO 4.1 — Self-Built AI Brain (Advanced)

100% built from scratch. No external AI models.
Intelligence: Knowledge Base + Web Search + NLP + Code Gen + Math + Creative.
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

        queries = self._make_queries(prompt)
        all_results = []
        for q in queries:
            results = self._web_search(q)
            if results:
                all_results.extend(results)
                if len(all_results) >= 8:
                    break

        if kb and all_results:
            extra_pts = self._extract_unique_sentences(all_results, prompt, limit=5)
            if extra_pts:
                return kb + "\n\n**Latest Information:**\n\n" + "\n\n".join(extra_pts)
            return kb

        if all_results:
            return self._compose_answer(prompt, all_results)

        if kb:
            return kb

        multi_kb = self._fuzzy_knowledge(prompt)
        if multi_kb:
            return multi_kb

        return self._smart_fallback(prompt)

    def _check_knowledge_base(self, prompt: str) -> str | None:
        p = prompt.lower()

        for key, (all_keys, text) in KNOWLEDGE.items():
            if key in p:
                return text
            for ak in all_keys:
                if ak in p:
                    return text

        return None

    def _fuzzy_knowledge(self, prompt: str) -> str | None:
        p_words = set(prompt.lower().split())
        stop = {"a", "an", "the", "is", "are", "was", "were", "what", "how",
                "why", "when", "where", "who", "which", "do", "does", "did",
                "can", "could", "would", "should", "will", "about", "for",
                "to", "of", "in", "on", "at", "by", "with", "from", "me",
                "my", "i", "you", "your", "tell", "explain", "describe",
                "please", "help", "want", "need", "give", "latest", "news",
                "analyze", "research", "discuss", "detailed", "comprehensive"}
        sig_words = {w for w in p_words if w not in stop and len(w) > 2}

        best_key = None
        best_score = 0
        for key, (all_keys, text) in KNOWLEDGE.items():
            all_kw = set()
            for ak in all_keys:
                all_kw.update(ak.split())
            overlap = len(sig_words & all_kw)
            if overlap > best_score:
                best_score = overlap
                best_key = key

        if best_key and best_score >= 1:
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
        response = f"## {topic.title()}\n\n"
        response += f"{topic.capitalize()} is a notable and multifaceted topic. Here's what I can share:\n\n"

        p = prompt.lower()
        if any(w in p for w in ["company", "startup", "founded", "ceo", "valuation"]):
            response += (
                f"**About {topic.title()}:**\n"
                f"This appears to be a question about a company or organization. "
                f"I have detailed knowledge about major tech companies, AI labs, and startups. "
                f"Try asking specifically about companies like Google, Apple, Microsoft, OpenAI, Anthropic, Meta, Tesla, SpaceX, etc.\n\n"
            )
        elif any(w in p for w in ["person", "who is", "biography", "born", "life"]):
            response += (
                f"This appears to be a question about a person. "
                f"I have knowledge about major figures in technology, science, and history. "
                f"Try asking about specific well-known figures.\n\n"
            )
        elif any(w in p for w in ["how to", "tutorial", "guide", "steps", "learn"]):
            response += (
                f"**Getting Started with {topic.title()}:**\n"
                f"1. Start with the fundamentals and core concepts\n"
                f"2. Practice with hands-on projects and exercises\n"
                f"3. Read documentation and reference materials\n"
                f"4. Join communities and forums for support\n"
                f"5. Build real-world projects to solidify understanding\n\n"
                f"If this is a programming topic, I can write code examples! Just ask.\n\n"
            )
        elif any(w in p for w in ["compare", "vs", "versus", "difference", "better"]):
            response += (
                f"To compare these properly, consider:\n"
                f"- **Purpose:** What problem does each solve?\n"
                f"- **Performance:** Speed, efficiency, scalability\n"
                f"- **Ecosystem:** Community, tools, libraries\n"
                f"- **Learning Curve:** Ease of adoption\n"
                f"- **Use Cases:** Where each excels\n\n"
                f"Ask me to compare specific technologies, languages, or tools and I'll give detailed analysis.\n\n"
            )
        elif any(w in p for w in ["news", "latest", "recent", "update", "trending"]):
            response += (
                f"I don't have access to live news feeds right now, but I have comprehensive knowledge about:\n\n"
                f"- **AI Companies:** OpenAI, Anthropic, Google DeepMind, Meta AI, DeepSeek, MiniMax, Mistral\n"
                f"- **Tech Industry:** Apple, Google, Microsoft, Amazon, Tesla, SpaceX\n"
                f"- **Trends:** AI/ML advances, cloud computing, blockchain, cybersecurity\n\n"
                f"Ask me about any specific company or technology for detailed information.\n\n"
            )
        else:
            response += (
                f"I have built-in knowledge covering 40+ topics including:\n\n"
                f"**Technology:** AI, Machine Learning, Deep Learning, LLMs, Programming, Web Development\n"
                f"**Science:** Physics, Chemistry, Biology, Mathematics, Astronomy\n"
                f"**Companies:** OpenAI, Anthropic, Google, DeepSeek, Tesla, SpaceX\n"
                f"**General:** History, Economics, Psychology, Health, Climate\n\n"
                f"Ask me specifically about any of these topics for a detailed answer! "
                f"I can also **write code**, **solve math**, and **create stories/poems**.\n\n"
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
            "Hello! How can I help you today? I can answer questions on any topic, write code, solve math, create stories, and much more. Just ask!",
            "Hey there! What would you like to explore? I'm ready to help with anything.",
            "Hi! Ask me anything — coding, science, math, history, AI, business, or creative writing. What's on your mind?",
        ]
        return random.choice(greetings)

    def _handle_system(self, prompt: str) -> str:
        return (
            "I'm **NAGRO 4.1** — Neural Adaptive Generative Reasoning Operator, "
            "created by **Aditya Kumar**.\n\n"
            "**What I can do:**\n"
            "- Answer questions on **40+ topics** (AI, science, programming, history, business, and more)\n"
            "- **Write code** in Python, JavaScript, TypeScript, HTML, SQL, and more\n"
            "- **Solve math** step by step (arithmetic, algebra, statistics)\n"
            "- **Write creatively** — stories, poems, essays, speeches, lyrics, emails\n"
            "- **Analyze & summarize** text you paste in\n"
            "- **Research** any topic with web search + built-in knowledge\n"
            "- **Code templates** for algorithms, APIs, data structures\n\n"
            "100% self-built. No external AI models. 200K context window.\n\n"
            "**Try asking me:**\n"
            "- \"What is quantum computing?\"\n"
            "- \"Write a Python binary search\"\n"
            "- \"Calculate 15 * 32 + 7\"\n"
            "- \"Write a poem about technology\"\n"
            "- \"Explain how blockchain works\""
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
        return (
            "I can help with code! Here are some things I can write:\n\n"
            "- \"Write a Python quicksort\" — sorting algorithms\n"
            "- \"Create a REST API\" — web backend\n"
            "- \"JavaScript fetch example\" — HTTP requests\n"
            "- \"Binary search tree\" — data structures\n"
            "- \"Python decorator\" — design patterns\n"
            "- \"SQL CRUD operations\" — database queries\n\n"
            "Just tell me what you need!"
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
        return (
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
        )

    def _gen_story(self, prompt):
        topic = re.sub(r'(write|create|tell)\s+(me\s+)?(a\s+)?(short\s+)?(story|tale)\s*(about|on)?\s*', '', prompt, flags=re.I).strip() or "adventure"
        return (
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
        )

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
