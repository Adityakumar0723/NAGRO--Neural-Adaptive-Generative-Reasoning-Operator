"""
NAGRO 4.1 — World Knowledge Database
Massive built-in knowledge covering 150+ topics.
"""
from __future__ import annotations
import re
from collections import Counter

WORLD_KNOWLEDGE: dict[str, dict] = {}

def _add(keys: list[str], content: str):
    entry = {"keys": keys, "content": content}
    for k in keys:
        WORLD_KNOWLEDGE[k] = entry

# ═══════════════════════════════════════════════════════
#  AI & TECHNOLOGY
# ═══════════════════════════════════════════════════════

_add(["artificial intelligence", "ai", "what is ai"],
"Artificial Intelligence (AI) is a branch of computer science that aims to create systems capable of performing tasks requiring human intelligence.\n\n"
"**Types of AI:**\n"
"- **Narrow AI (ANI):** Task-specific — voice assistants, image recognition, recommendation engines. All current AI is narrow.\n"
"- **General AI (AGI):** Human-level reasoning across all domains. Does not exist yet.\n"
"- **Superintelligent AI (ASI):** Surpasses human intelligence. Theoretical.\n\n"
"**Core Subfields:**\n"
"- **Machine Learning:** Learning from data without explicit programming\n"
"- **Deep Learning:** Multi-layered neural networks\n"
"- **NLP:** Understanding and generating human language\n"
"- **Computer Vision:** Interpreting images and video\n"
"- **Robotics:** Physical AI agents\n"
"- **Expert Systems:** Rule-based decision systems\n\n"
"**Applications:** Healthcare (diagnosis, drug discovery), autonomous vehicles, finance (trading, fraud detection), content creation, education, cybersecurity, agriculture, manufacturing.\n\n"
"**History:** Alan Turing (1950, Turing Test) → Dartmouth Conference (1956, AI coined) → Expert Systems (1970s) → ML boom (2000s) → Deep Learning revolution (2012+) → LLMs and Generative AI (2020s).\n\n"
"**Challenges:** Bias, explainability (black box problem), energy consumption, job displacement, privacy, alignment, hallucinations in LLMs, copyright issues."
)

_add(["machine learning", "ml", "supervised learning", "unsupervised learning"],
"Machine Learning (ML) enables computers to learn patterns from data without explicit programming.\n\n"
"**Types:**\n\n"
"**1. Supervised Learning** — labeled input-output pairs\n"
"- Classification: spam filtering, disease diagnosis, sentiment analysis\n"
"- Regression: house price prediction, stock forecasting, demand estimation\n"
"- Algorithms: Linear/Logistic Regression, Decision Trees, Random Forest, SVM, KNN, Naive Bayes, Neural Networks, XGBoost, LightGBM\n\n"
"**2. Unsupervised Learning** — no labels, find hidden patterns\n"
"- Clustering: customer segmentation, anomaly detection, gene grouping\n"
"- Dimensionality Reduction: PCA, t-SNE, UMAP\n"
"- Algorithms: K-Means, DBSCAN, Hierarchical Clustering, Gaussian Mixture Models, Autoencoders\n\n"
"**3. Reinforcement Learning** — learn by trial and reward\n"
"- Game playing (AlphaGo, Atari), robot navigation, resource optimization\n"
"- Algorithms: Q-Learning, DQN, PPO, A3C, SAC\n\n"
"**4. Semi-Supervised & Self-Supervised** — mix of labeled/unlabeled data. Powers modern LLMs.\n\n"
"**Key Concepts:** Feature engineering, train/val/test split, overfitting (too specific) vs underfitting (too general), regularization (L1/L2), cross-validation, hyperparameter tuning, gradient descent, loss functions, bias-variance tradeoff.\n\n"
"**Workflow:** Data Collection → Cleaning → Feature Engineering → Model Selection → Training → Evaluation → Deployment → Monitoring."
)

_add(["deep learning", "neural network", "neural networks", "cnn", "rnn", "transformer"],
"Deep Learning uses multi-layered artificial neural networks to learn hierarchical data representations.\n\n"
"**Architectures:**\n"
"- **Feedforward (MLP):** Basic neural network. Input → Hidden layers → Output.\n"
"- **CNN (Convolutional):** Image processing — filters detect edges, textures, objects. Used in: ImageNet, face recognition, medical imaging, self-driving cars.\n"
"- **RNN (Recurrent):** Sequential data — text, time series, audio. Problem: vanishing gradients.\n"
"- **LSTM / GRU:** Improved RNNs with gates to handle long sequences. Used in translation, speech.\n"
"- **Transformer:** Attention mechanism replaces recurrence. Parallel processing. Foundation of GPT, BERT, ViT. Revolutionized NLP, vision, audio.\n"
"- **GAN (Generative Adversarial Network):** Generator vs Discriminator — creates realistic images, video, audio.\n"
"- **Diffusion Models:** Iteratively denoise random noise into images. Powers Stable Diffusion, DALL-E, Midjourney.\n"
"- **VAE (Variational Autoencoder):** Probabilistic generation and compression.\n\n"
"**Training:** Forward pass → Loss calculation → Backpropagation → Weight update (gradient descent). Needs GPUs/TPUs, large datasets.\n\n"
"**Key Concepts:** Activation functions (ReLU, sigmoid, tanh, GELU), dropout, batch normalization, learning rate scheduling, transfer learning, fine-tuning.\n\n"
"**Milestones:** AlexNet/ImageNet (2012), GANs (2014), ResNet (2015), Transformer (2017), BERT (2018), GPT-3 (2020), Diffusion Models (2021), ChatGPT (2022), GPT-4 (2023), Multimodal AI (2024)."
)

_add(["large language model", "llm", "language model", "gpt", "chatgpt"],
"Large Language Models (LLMs) are AI systems trained on massive text to understand and generate human language.\n\n"
"**How They Work:**\n"
"1. Trained on billions of tokens from internet text\n"
"2. Use Transformer architecture with self-attention\n"
"3. Learn to predict the next token given context\n"
"4. Fine-tuned with RLHF (Reinforcement Learning from Human Feedback)\n"
"5. Can follow instructions, answer questions, write code, reason\n\n"
"**Major Models:**\n"
"- **GPT-4 / GPT-4o (OpenAI):** Multimodal, strong reasoning, 128K context\n"
"- **Claude 3.5 Sonnet / Opus (Anthropic):** Safety-focused, 200K context, strong coding\n"
"- **Gemini (Google):** Multimodal, integrated with Google services\n"
"- **LLaMA 3 (Meta):** Open-source, various sizes (8B to 405B)\n"
"- **Mistral / Mixtral (Mistral AI):** Efficient European open-source models\n"
"- **DeepSeek-V2/R1 (DeepSeek):** Chinese open-source, strong in code/math\n"
"- **Command R+ (Cohere):** Enterprise-focused, RAG-optimized\n\n"
"**Capabilities:** Text generation, summarization, translation, coding, reasoning, analysis, creative writing, role-playing, tool use.\n\n"
"**Limitations:** Hallucinations (false info stated confidently), training cutoff (no real-time knowledge), context window limits, bias from training data, no true understanding.\n\n"
"**Key Techniques:** Prompt engineering, chain-of-thought, few-shot learning, RAG (Retrieval Augmented Generation), fine-tuning, RLHF, DPO."
)

_add(["openai", "sam altman"],
"OpenAI is an AI research company founded in December 2015. Originally a nonprofit, restructured with a capped-profit model.\n\n"
"**Founders:** Sam Altman, Elon Musk (later left board), Ilya Sutskever, Greg Brockman, others.\n"
"**CEO:** Sam Altman\n"
"**Headquarters:** San Francisco, California\n\n"
"**Products:**\n"
"- **ChatGPT:** Conversational AI. 200M+ weekly active users. Free (GPT-4o mini) and paid (GPT-4o, GPT-4) tiers.\n"
"- **GPT-4 / GPT-4o:** Flagship multimodal models — text, vision, audio\n"
"- **GPT-4o mini:** Fast, affordable model for everyday tasks\n"
"- **DALL-E 3:** Text-to-image generation\n"
"- **Whisper:** Open-source speech recognition\n"
"- **Sora:** Text-to-video generation model\n"
"- **Codex:** Powers GitHub Copilot for code generation\n"
"- **API Platform:** Developer access to all models\n\n"
"**Business:** Valued at $80-157B. Major investor: Microsoft ($13B+). Revenue ~$3.4B annually. ChatGPT Plus: $20/month.\n\n"
"**Notable Events:** GPT-3 launch (2020), ChatGPT launch (Nov 2022), GPT-4 (Mar 2023), Sam Altman firing/rehiring (Nov 2023), Sora reveal (Feb 2024)."
)

_add(["anthropic", "claude", "claude ai"],
"Anthropic is an AI safety company founded in 2021 by Dario Amodei (CEO) and Daniela Amodei (President), both former OpenAI executives.\n\n"
"**Headquarters:** San Francisco, California\n"
"**Mission:** Building reliable, interpretable, and steerable AI systems.\n\n"
"**Products:**\n"
"- **Claude:** AI assistant available via API, claude.ai, and mobile apps\n"
"- **Claude 3.5 Sonnet:** Fast, intelligent, best for most tasks\n"
"- **Claude 3 Opus:** Most capable for complex reasoning\n"
"- **Claude 3 Haiku:** Fastest, most affordable\n"
"- **200K context window** — can process ~150K words at once\n"
"- **Claude for Enterprise:** Business-grade with privacy guarantees\n\n"
"**Key Research:**\n"
"- **Constitutional AI (CAI):** Training AI with principles instead of human labels\n"
"- **Mechanistic Interpretability:** Understanding what's happening inside neural networks\n"
"- **RLHF/RLAIF:** Alignment techniques\n\n"
"**Funding:** Raised $7.6B+ from Google ($2B), Salesforce, Amazon, Spark Capital.\n"
"**Valuation:** ~$18B.\n\n"
"**Philosophy:** AI should be helpful, harmless, and honest. Focus on preventing catastrophic AI risks."
)

_add(["google", "google ai", "gemini", "deepmind", "google deepmind"],
"Google (Alphabet Inc.) is one of the world's largest technology companies, and a major AI research leader.\n\n"
"**Founded:** 1998 by Larry Page and Sergey Brin at Stanford University\n"
"**CEO:** Sundar Pichai\n"
"**Headquarters:** Mountain View, California\n"
"**Revenue:** ~$307B (2023)\n\n"
"**AI Products:**\n"
"- **Gemini (formerly Bard):** Google's AI assistant and model family\n"
"- **Gemini Ultra/Pro/Nano:** Different model sizes for different tasks\n"
"- **Google DeepMind:** Merged AI research lab (DeepMind + Google Brain)\n"
"- **AlphaFold:** Predicted structures of 200M+ proteins\n"
"- **AlphaGo:** First AI to beat world champion at Go (2016)\n"
"- **TensorFlow:** Open-source ML framework\n"
"- **TPU:** Custom AI chips (Tensor Processing Units)\n"
"- **Google Cloud AI:** Enterprise AI services\n\n"
"**Other Products:** Search, YouTube, Android, Chrome, Gmail, Google Maps, Google Cloud, Pixel phones, Waymo (self-driving cars).\n\n"
"**Impact on AI:** Invented the Transformer architecture (2017 paper 'Attention is All You Need'), which became the foundation of all modern LLMs."
)

_add(["deepseek", "deepseek ai"],
"DeepSeek is a Chinese AI company that has gained significant attention for building highly capable open-source language models at lower costs.\n\n"
"**Founded:** 2023, backed by the Chinese quantitative hedge fund High-Flyer.\n"
"**Headquarters:** Hangzhou, China\n\n"
"**Key Models:**\n"
"- **DeepSeek-V2:** 236B parameter Mixture-of-Experts (MoE) model. Only 21B active parameters per token — very efficient.\n"
"- **DeepSeek-V3:** Latest flagship model with improved performance\n"
"- **DeepSeek-Coder V2:** Specialized for code generation, competitive with GPT-4 on coding benchmarks\n"
"- **DeepSeek-R1:** Reasoning model with step-by-step chain-of-thought, rivaling OpenAI's o1\n"
"- **DeepSeek-Math:** Specialized for mathematical reasoning\n\n"
"**Why It Matters:**\n"
"- Open-source models rivaling proprietary ones from OpenAI and Google\n"
"- Trained at a fraction of the cost (reportedly $5.6M for V3 vs hundreds of millions for GPT-4)\n"
"- MoE architecture: huge total parameters but only a subset active per query → fast + cheap\n"
"- Strong on coding, math, and reasoning benchmarks\n"
"- Challenged Western assumptions about compute requirements for frontier AI\n\n"
"**Impact:** DeepSeek-R1's release caused tech stock drops in the US, raising questions about the AI compute arms race."
)

_add(["minimax", "minimax ai"],
"MiniMax is a Chinese AI startup focused on large language models and multimodal AI applications.\n\n"
"**Founded:** 2021 by Yan Junjie (former SenseTime researcher)\n"
"**Headquarters:** Shanghai/Beijing, China\n"
"**Funding:** Raised $600M+, valued at $2.5B+\n\n"
"**Products & Models:**\n"
"- **abab series:** MiniMax's family of large language models (abab-5, abab-6)\n"
"- **Talkie (Xingye):** AI companion app — virtual characters for chat, roleplay, storytelling. 30M+ users.\n"
"- **Hailuo AI:** Text-to-video generation platform\n"
"- **Speech synthesis:** High-quality voice cloning and text-to-speech\n"
"- **Music generation:** AI music creation capabilities\n\n"
"**What Makes It Notable:**\n"
"- One of China's 'AI Six Tigers' alongside Zhipu AI, Moonshot AI, Baichuan, 01.AI, and StepFun\n"
"- Strong in consumer-facing AI applications (entertainment, social)\n"
"- Multimodal capabilities: text, voice, video, music\n"
"- Early mover in AI companion and virtual character space\n\n"
"**Business Model:** B2C (consumer apps like Talkie) and B2B (enterprise API access). Growing international presence."
)

_add(["mistral", "mistral ai"],
"Mistral AI is a French AI startup building open-source and commercial language models.\n\n"
"**Founded:** 2023 by Arthur Mensch, Guillaume Lample, and Timothée Lacroix (former Meta/Google DeepMind researchers)\n"
"**Headquarters:** Paris, France\n"
"**Funding:** $415M Series A, valued at $2B+\n\n"
"**Models:**\n"
"- **Mistral 7B:** Open-source, outperformed LLaMA 2 13B despite being smaller\n"
"- **Mixtral 8x7B:** Mixture-of-Experts model — 46.7B total params, only 12.9B active per token\n"
"- **Mistral Large:** Proprietary frontier model for complex tasks\n"
"- **Mistral Small/Medium:** Optimized for different price-performance tradeoffs\n"
"- **Codestral:** Specialized for code generation\n\n"
"**Why It Matters:**\n"
"- Europe's leading AI model company\n"
"- Pioneered efficient MoE architectures for open-source\n"
"- Balance of open-source (community) and commercial (revenue)\n"
"- Shows that frontier AI isn't limited to US/China companies"
)

_add(["meta", "meta ai", "llama", "facebook"],
"Meta Platforms (formerly Facebook) is a major tech company and significant AI research contributor.\n\n"
"**Founded:** 2004 by Mark Zuckerberg\n"
"**CEO:** Mark Zuckerberg\n"
"**Revenue:** ~$135B (2023)\n\n"
"**AI Products:**\n"
"- **LLaMA (Large Language Model Meta AI):** Open-source LLM family\n"
"  - LLaMA 1 (2023): 7B to 65B parameters\n"
"  - LLaMA 2 (2023): Improved, commercially licensable\n"
"  - LLaMA 3 (2024): 8B, 70B, 405B sizes, very competitive\n"
"- **Meta AI:** Built-in assistant across Facebook, Instagram, WhatsApp\n"
"- **FAIR (Fundamental AI Research):** World-class research lab\n"
"- **PyTorch:** Most popular deep learning framework (originally by Meta)\n\n"
"**Social Platforms:** Facebook (3B users), Instagram (2B), WhatsApp (2.7B), Messenger, Threads.\n\n"
"**Metaverse:** Quest VR headsets, Reality Labs, virtual/augmented reality research. Spent $46B+ on metaverse.\n\n"
"**Open-Source Strategy:** Meta releases models openly to build ecosystem, unlike OpenAI's closed approach."
)

_add(["natural language processing", "nlp", "text processing"],
"Natural Language Processing (NLP) is a field combining AI and linguistics to help computers understand, interpret, and generate human language.\n\n"
"**Core NLP Tasks:**\n"
"- **Tokenization:** Splitting text into words/subwords\n"
"- **Named Entity Recognition (NER):** Identifying names, dates, places\n"
"- **Sentiment Analysis:** Determining positive/negative/neutral tone\n"
"- **Machine Translation:** Converting between languages\n"
"- **Text Classification:** Categorizing documents (spam, topic, intent)\n"
"- **Question Answering:** Extracting answers from text\n"
"- **Text Summarization:** Condensing long text\n"
"- **Text Generation:** Creating human-like text\n\n"
"**Evolution:**\n"
"1. Rule-based (1950s-80s): Handcrafted grammar rules\n"
"2. Statistical (1990s-2000s): ML on text features, n-grams, TF-IDF\n"
"3. Word Embeddings (2013+): Word2Vec, GloVe — words as vectors\n"
"4. Transformer era (2017+): BERT, GPT, T5 — attention-based models\n"
"5. LLM era (2022+): ChatGPT, Claude, Gemini — general-purpose language AI\n\n"
"**Tools:** spaCy, NLTK, Hugging Face Transformers, Stanford NLP, Gensim."
)

_add(["computer vision", "image recognition", "object detection"],
"Computer Vision enables machines to interpret and understand visual information from images and video.\n\n"
"**Core Tasks:**\n"
"- **Image Classification:** What is in this image? (cat, dog, car)\n"
"- **Object Detection:** Where are objects? (bounding boxes — YOLO, SSD, Faster R-CNN)\n"
"- **Semantic Segmentation:** Pixel-level classification\n"
"- **Instance Segmentation:** Detecting individual objects at pixel level (Mask R-CNN)\n"
"- **Face Recognition:** Identifying individuals from facial features\n"
"- **Pose Estimation:** Detecting human body positions\n"
"- **OCR:** Reading text from images\n"
"- **Image Generation:** Creating images from text (DALL-E, Stable Diffusion, Midjourney)\n\n"
"**Key Models:** AlexNet, VGG, ResNet, Inception, EfficientNet, ViT (Vision Transformer), CLIP, SAM (Segment Anything).\n\n"
"**Applications:** Self-driving cars, medical imaging (X-rays, MRI), security/surveillance, quality inspection, augmented reality, satellite imagery analysis, retail (visual search)."
)

_add(["generative ai", "genai", "ai art", "text to image"],
"Generative AI creates new content — text, images, audio, video, code — rather than just analyzing existing data.\n\n"
"**Types:**\n"
"- **Text Generation:** LLMs (ChatGPT, Claude) — conversations, writing, code\n"
"- **Image Generation:** Diffusion models (Stable Diffusion, DALL-E 3, Midjourney)\n"
"- **Video Generation:** Sora (OpenAI), Runway Gen-2, Pika Labs\n"
"- **Audio/Music:** Suno, Udio, AudioCraft, MusicLM\n"
"- **Voice/Speech:** ElevenLabs, Bark, XTTS\n"
"- **3D Generation:** Point-E, DreamFusion, NeRF\n"
"- **Code Generation:** GitHub Copilot, Cursor, CodeWhisperer\n\n"
"**How Diffusion Models Work:**\n"
"1. Training: progressively add noise to images until pure noise\n"
"2. Learning: model learns to reverse the process (denoise)\n"
"3. Generation: start with random noise → iteratively denoise → clean image\n"
"4. Conditioning: text prompt guides what image to generate (via CLIP)\n\n"
"**Impact:** Transforming creative industries, content creation, marketing, design, gaming, film. Raises copyright and ethical concerns."
)

_add(["prompt engineering", "prompting", "prompt"],
"Prompt engineering is the art and science of crafting inputs to get the best outputs from AI language models.\n\n"
"**Techniques:**\n"
"- **Zero-shot:** Just ask directly. \"Translate 'hello' to French.\"\n"
"- **Few-shot:** Give examples first, then ask. \"cat→gato, dog→perro, bird→?\"\n"
"- **Chain-of-Thought (CoT):** \"Think step by step\" — improves reasoning\n"
"- **Role-playing:** \"You are an expert Python developer...\"\n"
"- **System prompts:** Set behavior, constraints, personality\n"
"- **Output formatting:** \"Respond in JSON\", \"Use bullet points\"\n"
"- **Self-consistency:** Ask multiple times, take majority answer\n"
"- **Tree of Thought:** Explore multiple reasoning paths\n"
"- **ReAct:** Reasoning + Acting — think, then use tools\n\n"
"**Best Practices:**\n"
"1. Be specific and clear\n"
"2. Provide context and constraints\n"
"3. Break complex tasks into steps\n"
"4. Use examples for desired format\n"
"5. Iterate and refine\n\n"
"**Advanced:** RAG (retrieve relevant docs before answering), function calling, structured outputs, agentic workflows."
)

_add(["rag", "retrieval augmented generation"],
"RAG (Retrieval Augmented Generation) combines information retrieval with language generation for more accurate, up-to-date responses.\n\n"
"**How RAG Works:**\n"
"1. **Indexing:** Documents → split into chunks → convert to embeddings (vectors) → store in vector database\n"
"2. **Retrieval:** User query → convert to embedding → find similar chunks via cosine similarity\n"
"3. **Generation:** Retrieved chunks + user query → LLM generates answer grounded in the retrieved context\n\n"
"**Why RAG Matters:**\n"
"- Reduces hallucinations (answers grounded in real documents)\n"
"- Provides up-to-date information (no retraining needed)\n"
"- Keeps proprietary data private (no need to send to model training)\n"
"- Cites sources for verifiability\n\n"
"**Components:**\n"
"- **Embedding Models:** OpenAI ada-002, Cohere Embed, sentence-transformers\n"
"- **Vector Databases:** Pinecone, Weaviate, Chroma, Milvus, pgvector, FAISS\n"
"- **Chunking Strategies:** Fixed-size, sentence-based, semantic, recursive\n"
"- **Reranking:** Cross-encoder rerankers improve retrieval quality\n\n"
"**Frameworks:** LangChain, LlamaIndex, Haystack."
)

# ═══════════════════════════════════════════════════════
#  PROGRAMMING LANGUAGES
# ═══════════════════════════════════════════════════════

_add(["python", "python programming", "python language"],
"Python is a high-level, interpreted, general-purpose programming language. Created by Guido van Rossum, first released in 1991.\n\n"
"**Why Python is Popular:**\n"
"- Readable, clean syntax (indentation-based)\n"
"- Huge ecosystem (300,000+ PyPI packages)\n"
"- Versatile: web, data science, AI, automation, scripting\n"
"- Great for beginners and experts alike\n"
"- Cross-platform (Windows, macOS, Linux)\n\n"
"**Core Features:** Dynamic typing, garbage collection, OOP + functional, generators, decorators, context managers, comprehensions, async/await.\n\n"
"**Data Types:** int, float, str, bool, list, tuple, dict, set, frozenset, bytes, None\n\n"
"**Popular Libraries:**\n"
"- **Web:** Django, Flask, FastAPI\n"
"- **Data:** Pandas, NumPy, Polars\n"
"- **Visualization:** Matplotlib, Seaborn, Plotly\n"
"- **ML/AI:** TensorFlow, PyTorch, scikit-learn, Keras\n"
"- **Scraping:** Beautiful Soup, Scrapy, Selenium\n"
"- **Testing:** pytest, unittest\n"
"- **Async:** asyncio, aiohttp, httpx\n\n"
"**Example:**\n```python\ndef fibonacci(n):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b\n\nprint(list(fibonacci(10)))\n```\n\n"
"**Latest:** Python 3.12+ with improved error messages, f-strings, performance improvements."
)

_add(["javascript", "js", "ecmascript"],
"JavaScript is the world's most popular programming language, essential for web development.\n\n"
"**Created:** 1995 by Brendan Eich at Netscape (in 10 days!)\n\n"
"**Where It Runs:**\n"
"- **Browser:** Client-side interactivity, DOM manipulation\n"
"- **Server:** Node.js, Deno, Bun\n"
"- **Mobile:** React Native, Ionic, NativeScript\n"
"- **Desktop:** Electron (VS Code, Discord, Slack)\n\n"
"**ES6+ Features:** let/const, arrow functions (=>), template literals, destructuring, spread/rest, classes, modules (import/export), async/await, Map/Set, Symbol, Proxy, optional chaining (?.), nullish coalescing (??)\n\n"
"**Ecosystem:**\n"
"- **Frontend:** React, Vue.js, Angular, Svelte, Solid\n"
"- **Backend:** Express, Fastify, Nest.js, Hono\n"
"- **Full-Stack:** Next.js, Nuxt, Remix, Astro\n"
"- **Testing:** Jest, Vitest, Mocha, Cypress, Playwright\n"
"- **Build:** Webpack, Vite, esbuild, Rollup, Turbopack\n"
"- **Package Managers:** npm, yarn, pnpm, bun\n\n"
"**Runtime:** Single-threaded, event loop, non-blocking I/O. V8 engine (Chrome/Node.js), SpiderMonkey (Firefox), JavaScriptCore (Safari)."
)

_add(["typescript", "ts", "typescript language"],
"TypeScript is a statically typed superset of JavaScript, developed by Microsoft (2012).\n\n"
"**Why TypeScript:**\n"
"- Catches errors at compile time instead of runtime\n"
"- Better IDE support (autocomplete, refactoring)\n"
"- Self-documenting code through types\n"
"- Scales to large codebases\n"
"- Compiles to plain JavaScript\n\n"
"**Key Features:**\n"
"- Type annotations: `let name: string = 'NAGRO'`\n"
"- Interfaces: `interface User { name: string; age: number }`\n"
"- Generics: `function identity<T>(arg: T): T { return arg }`\n"
"- Enums: `enum Color { Red, Green, Blue }`\n"
"- Union types: `string | number`\n"
"- Type guards and narrowing\n"
"- Utility types: Partial, Required, Pick, Omit, Record\n"
"- Declaration files (.d.ts)\n\n"
"**Adoption:** Used by Angular, Vue 3, Next.js, Deno, most enterprise projects. 70%+ of npm packages now include TypeScript declarations."
)

_add(["java", "java programming", "jvm"],
"Java is a statically typed, object-oriented, platform-independent language. Created by James Gosling at Sun Microsystems (1995).\n\n"
"**Philosophy:** 'Write Once, Run Anywhere' — compiles to bytecode that runs on JVM.\n\n"
"**Key Features:** Strong typing, garbage collection, multithreading, rich standard library, platform independence via JVM, backward compatibility.\n\n"
"**Where It's Used:**\n"
"- Enterprise applications (banking, insurance, healthcare)\n"
"- Android app development\n"
"- Big data (Hadoop, Spark, Kafka)\n"
"- Web backends (Spring Boot, Jakarta EE)\n"
"- Microservices architecture\n\n"
"**Frameworks:** Spring Boot (most popular), Quarkus, Micronaut, Jakarta EE, Hibernate (ORM).\n\n"
"**JVM Languages:** Kotlin, Scala, Groovy, Clojure — all run on Java's virtual machine.\n\n"
"**Latest:** Java 21+ with virtual threads (Project Loom), pattern matching, records, sealed classes, text blocks."
)

_add(["c++", "cpp", "c plus plus"],
"C++ is a high-performance, general-purpose programming language. Created by Bjarne Stroustrup (1979) as an extension of C.\n\n"
"**Key Features:** Low-level memory control, OOP, templates (generics), STL (Standard Template Library), RAII (Resource Acquisition Is Initialization), operator overloading, multiple inheritance.\n\n"
"**Where It's Used:**\n"
"- Game engines (Unreal Engine, Unity internals)\n"
"- Operating systems (Windows, Linux kernel modules)\n"
"- Embedded systems and IoT\n"
"- High-frequency trading\n"
"- Browsers (Chrome, Firefox)\n"
"- Databases (MySQL, MongoDB)\n"
"- Scientific computing and simulations\n\n"
"**Modern C++ (C++11/14/17/20/23):** auto, lambda expressions, smart pointers (unique_ptr, shared_ptr), move semantics, constexpr, concepts, ranges, coroutines, modules.\n\n"
"**Performance:** Compiled to native machine code. No garbage collector — manual or smart pointer memory management. Zero-cost abstractions."
)

_add(["rust", "rust programming", "rust language"],
"Rust is a systems programming language focused on safety, speed, and concurrency. Created by Graydon Hoare at Mozilla (2010).\n\n"
"**Key Innovation — Ownership System:**\n"
"- Each value has one owner\n"
"- When owner goes out of scope, value is dropped (freed)\n"
"- Borrowing: references without taking ownership\n"
"- No null pointers, no data races, no dangling references\n"
"- All memory safety guaranteed at compile time — no garbage collector needed\n\n"
"**Where It's Used:**\n"
"- Systems programming (OS components, drivers)\n"
"- WebAssembly (Wasm)\n"
"- Command-line tools (ripgrep, fd, bat, exa)\n"
"- Web servers (Actix, Axum, Rocket)\n"
"- Blockchain (Solana)\n"
"- Cloud infrastructure (Cloudflare, AWS Firecracker)\n"
"- Linux kernel (second language after C)\n\n"
"**Loved by developers:** #1 most admired language on Stack Overflow survey for 8 years straight."
)

_add(["go", "golang", "go language"],
"Go (Golang) is a statically typed, compiled language created at Google (2009) by Robert Griesemer, Rob Pike, and Ken Thompson.\n\n"
"**Design Goals:** Simplicity, fast compilation, built-in concurrency, efficient garbage collection.\n\n"
"**Key Features:**\n"
"- **Goroutines:** Lightweight threads (thousands run concurrently)\n"
"- **Channels:** Communication between goroutines\n"
"- Fast compilation (compiles entire programs in seconds)\n"
"- Static binary (single file deployment, no dependencies)\n"
"- Interfaces (implicit implementation)\n"
"- Built-in testing and profiling\n\n"
"**Where It's Used:**\n"
"- Cloud/infrastructure: Docker, Kubernetes, Terraform, Prometheus\n"
"- Web services and APIs\n"
"- CLI tools\n"
"- Networking tools\n"
"- Microservices\n\n"
"**Popular at:** Google, Uber, Twitch, Dropbox, Cloudflare, SoundCloud."
)

# ═══════════════════════════════════════════════════════
#  WEB & SOFTWARE DEVELOPMENT
# ═══════════════════════════════════════════════════════

_add(["react", "reactjs", "react.js"],
"React is a JavaScript library for building user interfaces, developed by Facebook/Meta (2013).\n\n"
"**Core Concepts:**\n"
"- **Components:** Reusable UI building blocks (function or class)\n"
"- **JSX:** HTML-like syntax in JavaScript (`<Button onClick={...}>Click</Button>`)\n"
"- **Props:** Data passed from parent to child (read-only)\n"
"- **State:** Internal component data that triggers re-renders\n"
"- **Virtual DOM:** In-memory representation. React diffs it with real DOM and applies minimal updates.\n\n"
"**Hooks (React 16.8+):**\n"
"- `useState` — state management\n"
"- `useEffect` — side effects (API calls, subscriptions)\n"
"- `useContext` — share data without prop drilling\n"
"- `useRef` — persist values across renders\n"
"- `useMemo` / `useCallback` — memoization for performance\n"
"- `useReducer` — complex state logic\n\n"
"**Ecosystem:** React Router (routing), Redux/Zustand/Jotai (state), Next.js (SSR/SSG), React Native (mobile), Framer Motion (animation), React Query/TanStack (data fetching).\n\n"
"**Market Share:** Most used frontend framework. Used by Facebook, Instagram, Netflix, Airbnb, Uber, Twitter."
)

_add(["next.js", "nextjs", "next"],
"Next.js is a React framework for production applications, created by Vercel.\n\n"
"**Rendering Strategies:**\n"
"- **SSR (Server-Side Rendering):** Renders on each request — good for dynamic, SEO-critical pages\n"
"- **SSG (Static Site Generation):** Pre-builds at build time — fastest, good for blogs\n"
"- **ISR (Incremental Static Regeneration):** Static + periodic revalidation\n"
"- **Client-Side:** Traditional SPA behavior where needed\n\n"
"**App Router (v13+):**\n"
"- File-system based routing in `app/` directory\n"
"- React Server Components by default\n"
"- Layouts, loading states, error boundaries\n"
"- Route groups, parallel routes, intercepting routes\n"
"- Server Actions for form handling\n\n"
"**Features:** Image optimization (next/image), Font optimization, API routes, Middleware, Internationalization, built-in CSS/Sass support.\n\n"
"**Deployment:** Vercel (native support), AWS, Docker, any Node.js host."
)

_add(["node.js", "nodejs", "node"],
"Node.js is a JavaScript runtime built on Chrome's V8 engine that enables running JavaScript on the server.\n\n"
"**Created:** 2009 by Ryan Dahl\n\n"
"**Key Features:**\n"
"- **Non-blocking I/O:** Asynchronous, event-driven architecture\n"
"- **Single-threaded event loop:** Handles thousands of concurrent connections\n"
"- **npm:** World's largest package registry (2M+ packages)\n"
"- **Unified language:** Same language (JS) for frontend and backend\n\n"
"**Built-in Modules:** fs (file system), http, path, crypto, stream, events, child_process, cluster, worker_threads.\n\n"
"**Popular Frameworks:**\n"
"- **Express:** Minimal, most popular\n"
"- **Fastify:** High performance\n"
"- **Nest.js:** TypeScript, enterprise-grade, Angular-inspired\n"
"- **Koa:** By Express creators, modern middleware\n"
"- **Hono:** Ultra-fast, runs everywhere (Node, Deno, Bun, Workers)\n\n"
"**Alternatives:** Deno (by Ryan Dahl, secure by default, TypeScript native), Bun (fast runtime + bundler + package manager).\n\n"
"**Used by:** Netflix, PayPal, LinkedIn, Uber, NASA, Walmart."
)

_add(["database", "sql", "nosql", "postgresql", "mongodb", "mysql", "redis", "sqlite"],
"Databases organize, store, and retrieve data efficiently.\n\n"
"**Relational Databases (SQL):**\n"
"- Structured data in tables (rows + columns), relationships via foreign keys\n"
"- ACID compliant: Atomicity, Consistency, Isolation, Durability\n"
"- **PostgreSQL:** Most advanced open-source. JSON support, extensions, full-text search.\n"
"- **MySQL:** Most popular. Used by WordPress, Facebook. Fast reads.\n"
"- **SQLite:** Serverless, embedded database in a single file. Perfect for mobile/desktop apps.\n"
"- **SQL Server:** Microsoft's enterprise database.\n\n"
"**SQL Basics:**\n```sql\nSELECT name, age FROM users WHERE age > 18 ORDER BY name;\nINSERT INTO users (name, email) VALUES ('Aditya', 'a@b.com');\nUPDATE users SET age = 26 WHERE name = 'Aditya';\nDELETE FROM users WHERE id = 5;\nSELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id;\n```\n\n"
"**NoSQL Databases:**\n"
"- **MongoDB:** Document store (JSON-like). Flexible schema. Most popular NoSQL.\n"
"- **Redis:** In-memory key-value store. Caching, sessions, pub/sub. Blazing fast.\n"
"- **Cassandra:** Wide-column store. Massive scale (Netflix, Apple). High write throughput.\n"
"- **Neo4j:** Graph database. Relationships between entities.\n"
"- **DynamoDB:** AWS managed key-value/document. Serverless, auto-scaling.\n\n"
"**When to use SQL vs NoSQL:** SQL for structured, relational data with complex queries. NoSQL for flexible schemas, high scalability, specific access patterns."
)

_add(["api", "rest api", "graphql", "grpc", "web api"],
"APIs (Application Programming Interfaces) allow different software systems to communicate.\n\n"
"**REST API (Representational State Transfer):**\n"
"- HTTP-based, stateless, resource-oriented\n"
"- Methods: GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove)\n"
"- Status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Server Error\n"
"- Uses JSON (usually) or XML for data exchange\n\n"
"**GraphQL (by Facebook/Meta):**\n"
"- Single endpoint, client specifies exactly what data it needs\n"
"- No over-fetching or under-fetching\n"
"- Schema-first with types, queries, mutations, subscriptions\n"
"- Tools: Apollo, Relay, Hasura\n\n"
"**gRPC (by Google):**\n"
"- High-performance RPC using Protocol Buffers (binary)\n"
"- HTTP/2 based, supports streaming\n"
"- Great for microservices communication\n\n"
"**WebSocket:** Full-duplex persistent connection for real-time (chat, live data, gaming).\n\n"
"**Authentication:** API Keys, OAuth 2.0 (authorization flows), JWT (JSON Web Tokens), Bearer tokens, Basic Auth.\n\n"
"**Best Practices:** Use nouns for resources (/users, /posts), version APIs (/v1/), paginate large lists, rate limit, document with OpenAPI/Swagger."
)

_add(["docker", "container", "containerization"],
"Docker packages applications in containers — lightweight, portable, reproducible environments.\n\n"
"**Core Concepts:**\n"
"- **Image:** Read-only template with OS, runtime, code, dependencies\n"
"- **Container:** Running instance of an image. Isolated process.\n"
"- **Dockerfile:** Build instructions to create an image\n"
"- **Docker Compose:** Orchestrate multi-container apps (YAML config)\n"
"- **Registry:** Image storage — Docker Hub, ECR (AWS), GCR (Google), ACR (Azure)\n\n"
"**Key Commands:**\n```\ndocker build -t myapp .            # Build image\ndocker run -d -p 8080:80 myapp     # Run container\ndocker ps                           # List containers\ndocker logs <id>                    # View logs\ndocker exec -it <id> /bin/sh        # Shell into container\ndocker-compose up -d                # Start multi-container\ndocker-compose down                 # Stop all\n```\n\n"
"**Dockerfile Example:**\n```dockerfile\nFROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nEXPOSE 8000\nCMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\"]\n```\n\n"
"**Benefits:** Consistent environments, rapid deployment, resource efficiency, microservices, CI/CD integration."
)

_add(["kubernetes", "k8s"],
"Kubernetes (K8s) is an open-source container orchestration platform, originally by Google.\n\n"
"**Core Concepts:**\n"
"- **Pod:** Smallest unit — one or more containers sharing network/storage\n"
"- **Deployment:** Manages Pod replicas, rolling updates, rollbacks\n"
"- **Service:** Stable network endpoint for Pods (ClusterIP, NodePort, LoadBalancer)\n"
"- **Ingress:** HTTP routing, SSL termination, path-based routing\n"
"- **ConfigMap / Secret:** Configuration and sensitive data management\n"
"- **Namespace:** Virtual clusters for isolation\n"
"- **PersistentVolume:** Durable storage\n\n"
"**Architecture:**\n"
"- Control Plane: API Server, Scheduler, Controller Manager, etcd\n"
"- Worker Nodes: kubelet, kube-proxy, container runtime\n\n"
"**Managed Services:** EKS (AWS), GKE (Google), AKS (Azure).\n\n"
"**Tools:** kubectl (CLI), Helm (package manager), Istio (service mesh), ArgoCD (GitOps)."
)

_add(["cloud computing", "aws", "azure", "gcp", "cloud"],
"Cloud computing delivers computing resources over the internet on-demand.\n\n"
"**Service Models:**\n"
"- **IaaS:** Virtual machines, storage, networking — AWS EC2, Azure VMs, GCE\n"
"- **PaaS:** Managed platforms — Heroku, Google App Engine, AWS Elastic Beanstalk\n"
"- **SaaS:** Complete applications — Gmail, Salesforce, Slack, Dropbox\n"
"- **FaaS (Serverless):** Run code without managing servers — AWS Lambda, Google Cloud Functions, Azure Functions\n\n"
"**AWS (Amazon Web Services):** Market leader (~32%). EC2, S3, RDS, Lambda, DynamoDB, SQS, CloudFront, EKS.\n\n"
"**Azure (Microsoft):** #2 (~22%). Strong enterprise/hybrid cloud. Azure DevOps, Active Directory, Cosmos DB.\n\n"
"**GCP (Google Cloud):** #3 (~11%). Best for data/AI. BigQuery, Vertex AI, GKE, Cloud Run.\n\n"
"**Key Concepts:** Regions/availability zones, auto-scaling, load balancing, CDN, IAM (identity & access), VPC (virtual private cloud), managed databases, object storage."
)

_add(["git", "github", "version control", "gitlab"],
"Git is a distributed version control system created by Linus Torvalds (2005) for Linux kernel development.\n\n"
"**Core Concepts:**\n"
"- **Repository:** Project folder tracked by Git\n"
"- **Commit:** Snapshot of changes with a message and hash\n"
"- **Branch:** Independent line of development\n"
"- **Merge:** Combining branches\n"
"- **Remote:** Server-hosted repository (origin)\n"
"- **HEAD:** Pointer to current commit\n\n"
"**Essential Commands:**\n```\ngit init                    # Initialize repo\ngit clone <url>             # Clone remote repo\ngit add . / git add <file>  # Stage changes\ngit commit -m \"message\"     # Commit\ngit push origin main        # Push to remote\ngit pull                    # Fetch + merge\ngit branch feature          # Create branch\ngit checkout -b feature     # Create + switch\ngit merge feature           # Merge branch\ngit log --oneline           # Compact history\ngit diff                    # View changes\ngit stash / git stash pop   # Temp save changes\ngit rebase main             # Rebase onto main\ngit cherry-pick <hash>      # Apply specific commit\n```\n\n"
"**Workflow:** Feature branches → Pull Requests → Code Review → CI/CD → Merge to main.\n\n"
"**Platforms:** GitHub (100M+ developers), GitLab (DevOps platform), Bitbucket (Atlassian), Azure DevOps."
)

_add(["system design", "architecture", "scalability", "microservices"],
"System design defines the architecture of large-scale software systems.\n\n"
"**Fundamentals:**\n"
"- **Scalability:** Horizontal (add machines) vs Vertical (bigger machine)\n"
"- **Availability:** Uptime percentage. 99.9% = 8.76h downtime/year. 99.99% = 52.6min/year.\n"
"- **Consistency:** All nodes see same data at same time\n"
"- **Partition Tolerance:** System works despite network failures\n"
"- **CAP Theorem:** Can only guarantee 2 of 3 (C, A, P)\n\n"
"**Key Components:**\n"
"- **Load Balancer:** Distributes traffic (Nginx, HAProxy, ALB)\n"
"- **Caching:** Redis, Memcached, CDN — reduce latency/load\n"
"- **Message Queue:** Kafka, RabbitMQ, SQS — async, decoupling\n"
"- **Database:** SQL vs NoSQL, sharding, replication, read replicas\n"
"- **CDN:** Edge caching for static content (CloudFront, Cloudflare)\n"
"- **API Gateway:** Authentication, rate limiting, routing\n"
"- **Microservices:** Independent services vs monolith\n\n"
"**Common Designs:** URL shortener, chat system, news feed, ride sharing, e-commerce, video streaming, search engine."
)

_add(["cybersecurity", "security", "hacking", "encryption", "cyber"],
"Cybersecurity protects systems, networks, and data from unauthorized access and attacks.\n\n"
"**Attack Types:**\n"
"- **Phishing:** Fake emails/websites to steal credentials\n"
"- **Ransomware:** Encrypts files, demands payment (WannaCry, Colonial Pipeline)\n"
"- **SQL Injection:** Malicious SQL in input fields\n"
"- **XSS (Cross-Site Scripting):** Injecting scripts into web pages\n"
"- **CSRF:** Forging requests from authenticated users\n"
"- **DDoS:** Overwhelming servers with traffic\n"
"- **Man-in-the-Middle:** Intercepting communications\n"
"- **Zero-Day:** Exploiting unknown vulnerabilities\n"
"- **Supply Chain:** Compromising software dependencies\n\n"
"**Defense:**\n"
"- Firewalls, IDS/IPS, WAF\n"
"- MFA (Multi-Factor Authentication)\n"
"- Encryption: AES (symmetric), RSA/ECC (asymmetric), SHA-256 (hashing), TLS/SSL\n"
"- Zero Trust architecture\n"
"- Penetration testing, bug bounties\n"
"- SIEM (Security Info & Event Management)\n\n"
"**Frameworks:** OWASP Top 10, NIST, ISO 27001, SOC 2, PCI-DSS, GDPR."
)

# ═══════════════════════════════════════════════════════
#  SCIENCE
# ═══════════════════════════════════════════════════════

_add(["physics", "newton", "einstein", "relativity", "gravity", "quantum physics"],
"Physics is the fundamental natural science studying matter, energy, space, time, and their interactions.\n\n"
"**Classical Mechanics (Newton):**\n"
"- F = ma (Force = mass × acceleration)\n"
"- Gravitation: F = Gm₁m₂/r²\n"
"- Three Laws: 1) Inertia, 2) F=ma, 3) Action-reaction\n"
"- Conservation of energy, momentum, angular momentum\n\n"
"**Electromagnetism (Maxwell):**\n"
"- Electric and magnetic fields are unified\n"
"- Light is an electromagnetic wave (c = 3×10⁸ m/s)\n"
"- Maxwell's 4 equations govern all electromagnetic phenomena\n\n"
"**Thermodynamics:**\n"
"- 0th Law: Thermal equilibrium defines temperature\n"
"- 1st Law: Energy is conserved (ΔU = Q - W)\n"
"- 2nd Law: Entropy always increases (arrow of time)\n"
"- 3rd Law: Absolute zero is unattainable\n\n"
"**Relativity (Einstein):**\n"
"- Special (1905): E = mc², time dilation, length contraction. Nothing travels faster than light.\n"
"- General (1915): Gravity = curvature of spacetime caused by mass. Predicts black holes, gravitational waves.\n\n"
"**Quantum Mechanics:**\n"
"- Wave-particle duality: particles behave as waves and vice versa\n"
"- Uncertainty principle (Heisenberg): Can't know position AND momentum precisely\n"
"- Superposition: particles in multiple states until measured\n"
"- Entanglement: correlated particles, 'spooky action at a distance'\n\n"
"**Modern Physics:** Standard Model (17 particles: quarks, leptons, bosons), Higgs boson (discovered 2012), dark matter (27% of universe), dark energy (68%), string theory, quantum gravity."
)

_add(["chemistry", "elements", "periodic table", "chemical", "organic chemistry"],
"Chemistry studies matter — its composition, structure, properties, and transformations.\n\n"
"**Periodic Table:** 118 confirmed elements, organized by atomic number (protons).\n"
"- Groups (columns): similar properties. Group 1: Alkali metals (Li, Na, K). Group 17: Halogens (F, Cl, Br). Group 18: Noble gases (He, Ne, Ar)\n"
"- Periods (rows): increasing electron shells\n"
"- Most abundant: Hydrogen (universe), Oxygen (Earth's crust)\n\n"
"**Chemical Bonds:**\n"
"- Ionic: electron transfer (NaCl — table salt)\n"
"- Covalent: electron sharing (H₂O — water)\n"
"- Metallic: electron sea (metals)\n"
"- Hydrogen: weak but crucial (DNA, water properties)\n\n"
"**Reactions:** Synthesis (A+B→AB), Decomposition (AB→A+B), Combustion (fuel+O₂→CO₂+H₂O), Acid-Base (neutralization), Redox (electron transfer), Precipitation.\n\n"
"**Organic Chemistry:** Carbon-based compounds. Hydrocarbons, alcohols, acids, amines, polymers. Foundation of biochemistry, pharmaceuticals, plastics.\n\n"
"**Applications:** Pharmaceuticals, materials science, energy (batteries, fuel cells), agriculture (fertilizers), food chemistry, forensics, environmental science."
)

_add(["biology", "cell", "dna", "genetics", "evolution", "life science"],
"Biology is the study of living organisms and their vital processes.\n\n"
"**Cell Biology:**\n"
"- Cell = basic unit of life. ~37 trillion cells in human body.\n"
"- Prokaryotic (bacteria — no nucleus) vs Eukaryotic (animals, plants — nucleus)\n"
"- Organelles: nucleus (DNA), mitochondria (energy/ATP), ribosome (protein synthesis), ER, Golgi\n"
"- Cell division: Mitosis (growth) and Meiosis (reproduction)\n\n"
"**Genetics & DNA:**\n"
"- DNA: double helix, 4 bases (Adenine-Thymine, Guanine-Cytosine)\n"
"- Central Dogma: DNA → RNA (transcription) → Protein (translation)\n"
"- Human genome: 3 billion base pairs, ~20,000 protein-coding genes\n"
"- Mendel's laws: dominant/recessive, segregation, independent assortment\n\n"
"**Evolution (Darwin):**\n"
"- Natural selection: organisms with favorable traits survive and reproduce\n"
"- Evidence: fossils, DNA comparison, embryology, vestigial structures\n"
"- All life shares a common ancestor (~3.8 billion years ago)\n\n"
"**Modern Biology:** CRISPR gene editing, synthetic biology, personalized medicine, microbiome, stem cells, cloning, genomics."
)

_add(["mathematics", "math", "maths"],
"Mathematics is the study of numbers, quantity, structure, space, and change.\n\n"
"**Branches:**\n"
"- **Arithmetic:** +, -, ×, ÷, order of operations (PEMDAS/BODMAS)\n"
"- **Algebra:** Variables, equations, polynomials, inequalities, functions\n"
"  - Quadratic formula: x = (-b ± √(b²-4ac)) / 2a\n"
"- **Geometry:** Points, lines, angles, shapes, area, volume\n"
"  - Pythagorean: a² + b² = c²\n"
"  - Circle: A = πr², C = 2πr\n"
"  - Sphere: V = (4/3)πr³\n"
"- **Trigonometry:** sin, cos, tan — relating angles and sides of triangles\n"
"  - sin²θ + cos²θ = 1\n"
"- **Calculus:** Derivatives (instantaneous rate of change), Integrals (area under curve)\n"
"  - d/dx(xⁿ) = nxⁿ⁻¹\n"
"  - ∫xⁿdx = xⁿ⁺¹/(n+1) + C\n"
"- **Statistics:** Mean, median, mode, standard deviation, probability, distributions, hypothesis testing\n"
"- **Linear Algebra:** Vectors, matrices, eigenvalues, transformations — foundation of ML\n"
"- **Discrete Math:** Logic, sets, combinatorics, graph theory — foundation of CS\n"
"- **Number Theory:** Primes, divisibility, modular arithmetic — foundation of cryptography\n\n"
"**Famous Constants:** π ≈ 3.14159, e ≈ 2.71828, φ (golden ratio) ≈ 1.61803, i = √(-1)"
)

_add(["solar system", "planets", "space", "astronomy", "universe", "stars", "galaxy"],
"Astronomy studies celestial objects, space, and the universe.\n\n"
"**Solar System (8 planets):**\n"
"1. **Mercury:** Smallest, closest to Sun, extreme temperature swings\n"
"2. **Venus:** Hottest (462°C), thick CO₂ atmosphere, similar size to Earth\n"
"3. **Earth:** Only known life, liquid water, 1 moon\n"
"4. **Mars:** Red Planet, largest volcano (Olympus Mons), 2 moons, exploration target\n"
"5. **Jupiter:** Largest planet, Great Red Spot storm, 95 known moons (Europa may have ocean)\n"
"6. **Saturn:** Spectacular rings (ice and rock), 146 known moons (Titan has atmosphere)\n"
"7. **Uranus:** Tilted 98° on its side, ice giant\n"
"8. **Neptune:** Farthest, deep blue, strongest winds in solar system\n\n"
"**Other Bodies:** Dwarf planets (Pluto, Eris, Ceres), asteroid belt, Kuiper belt, Oort cloud, comets.\n\n"
"**Sun:** G-type main-sequence star (yellow dwarf). 4.6 billion years old. 99.86% of solar system's mass. Core: 15 million °C. Surface: 5,500°C.\n\n"
"**Universe:**\n"
"- Big Bang: ~13.8 billion years ago\n"
"- Observable universe: 93 billion light-years across\n"
"- ~2 trillion galaxies, each with billions of stars\n"
"- Milky Way: our galaxy, 100,000 light-years across, 200-400 billion stars\n"
"- Black holes: gravity so strong even light can't escape. Sagittarius A* at our galaxy's center.\n\n"
"**Space Exploration:** NASA, ESA, ISRO, CNSA, SpaceX, Blue Origin. ISS, Mars rovers (Perseverance/Curiosity), James Webb Space Telescope, Artemis (Moon program), Voyager probes."
)

_add(["climate change", "global warming", "environment", "carbon"],
"Climate change refers to long-term shifts in global temperatures and weather patterns.\n\n"
"**The Science:**\n"
"- Earth's average temp has risen ~1.1°C since pre-industrial era\n"
"- CO₂ levels: 421+ ppm (highest in 800,000+ years)\n"
"- Greenhouse gases (CO₂, CH₄, N₂O) trap heat in atmosphere\n"
"- 97% of climate scientists agree: human activity is the primary cause\n\n"
"**Causes:** Burning fossil fuels (coal, oil, natural gas) for energy, transportation, industry. Deforestation. Agriculture (methane from livestock). Industrial processes.\n\n"
"**Effects:**\n"
"- Rising sea levels (projected 0.3-1m by 2100)\n"
"- More extreme weather (hurricanes, droughts, floods, wildfires)\n"
"- Ocean acidification (30% more acidic)\n"
"- Biodiversity loss (1 million species threatened)\n"
"- Food insecurity, water scarcity\n"
"- Glacier and ice sheet melting (Arctic ice declining ~13% per decade)\n\n"
"**Solutions:**\n"
"- Renewable energy: Solar ($0.04/kWh), wind, hydroelectric, geothermal, nuclear\n"
"- Electric vehicles, public transit\n"
"- Energy efficiency in buildings and industry\n"
"- Carbon capture and storage\n"
"- Reforestation, soil carbon sequestration\n"
"- Policy: Paris Agreement (limit warming to 1.5-2°C), carbon pricing, net-zero targets by 2050"
)

# ═══════════════════════════════════════════════════════
#  COUNTRIES & HISTORY
# ═══════════════════════════════════════════════════════

_add(["india", "bharat", "indian", "india country"],
"India (Bharat) is the world's most populous country and largest democracy.\n\n"
"**Key Facts:**\n"
"- **Capital:** New Delhi | **Financial Capital:** Mumbai\n"
"- **Population:** ~1.44 billion (2024, overtook China)\n"
"- **Area:** 3.28 million km² (7th largest country)\n"
"- **Languages:** Hindi, English (official), 22 scheduled languages, 19,500+ dialects\n"
"- **Currency:** Indian Rupee (₹, INR)\n"
"- **Government:** Federal parliamentary democratic republic\n"
"- **President:** Droupadi Murmu | **PM:** Narendra Modi (since 2014)\n\n"
"**Economy (5th largest GDP, ~$3.7T):**\n"
"- IT/Software: Infosys, TCS, Wipro, HCL (world's back office)\n"
"- Startups: 100+ unicorns — Flipkart, Zomato, Ola, CRED, PhonePe, Razorpay\n"
"- Agriculture: 40%+ workforce, rice, wheat, tea, spices, cotton\n"
"- Pharmaceuticals: Generic medicines supplier to the world\n"
"- Manufacturing: 'Make in India', growing electronics/semiconductor push\n\n"
"**Technology:** ISRO (Chandrayaan-3 Moon landing 2023, Mangalyaan Mars mission), UPI (digital payments revolution — 12B+ monthly transactions), Aadhaar (world's largest biometric ID), 5G rollout.\n\n"
"**History Highlights:** Indus Valley Civilization (3300 BCE), Maurya Empire (Ashoka), Mughal Empire, British Raj (1858-1947), Independence (Aug 15, 1947, led by Gandhi, Nehru), Constitution (1950).\n\n"
"**Culture:** Diverse religions (Hinduism 80%, Islam 14%, Christianity, Sikhism, Buddhism, Jainism), Bollywood (world's largest film industry by volume), cricket, classical music/dance, yoga, cuisine diversity."
)

_add(["united states", "usa", "america", "us"],
"The United States of America is a federal republic of 50 states and the world's most powerful economy.\n\n"
"**Key Facts:**\n"
"- **Capital:** Washington, D.C.\n"
"- **Largest City:** New York City (8.3M, metro 20M+)\n"
"- **Population:** ~335 million (3rd most populous)\n"
"- **Area:** 9.83 million km² (3rd/4th largest country)\n"
"- **Currency:** US Dollar ($, USD) — world's reserve currency\n"
"- **Government:** Federal presidential constitutional republic\n\n"
"**Economy (largest GDP, ~$28T):**\n"
"- Technology: Apple, Google, Microsoft, Amazon, Meta, Nvidia, Tesla\n"
"- Finance: Wall Street, Federal Reserve, world's largest stock markets\n"
"- Military: Largest defense budget (~$886B)\n"
"- Entertainment: Hollywood, music industry, streaming (Netflix, Disney+)\n"
"- Higher education: MIT, Stanford, Harvard, Caltech\n\n"
"**Technology Leadership:** Silicon Valley, AI research (OpenAI, Google, Meta), space (NASA, SpaceX), semiconductors (Nvidia, Intel, AMD), biotech.\n\n"
"**History Highlights:** Independence (1776), Constitution (1787), Civil War (1861-65), both World Wars, Cold War, Civil Rights Movement (1960s), Moon landing (1969), Internet revolution."
)

_add(["china", "chinese", "prc"],
"China (People's Republic of China) is the world's second-largest economy and most populous country until recently.\n\n"
"**Key Facts:**\n"
"- **Capital:** Beijing | **Financial Hub:** Shanghai\n"
"- **Population:** ~1.41 billion (2024)\n"
"- **Currency:** Renminbi/Yuan (¥, CNY)\n"
"- **Government:** Single-party socialist republic (CPC)\n"
"- **Leader:** Xi Jinping (President since 2013)\n\n"
"**Economy (2nd largest GDP, ~$18T):**\n"
"- World's manufacturing hub ('factory of the world')\n"
"- Tech giants: Alibaba, Tencent, Huawei, Xiaomi, BYD, ByteDance (TikTok)\n"
"- World leader in EVs, solar panels, batteries\n"
"- Belt and Road Initiative (infrastructure investment across Asia/Africa/Europe)\n\n"
"**Technology:** 5G leader, AI research (DeepSeek, Baidu, Alibaba Cloud), space program (Tiangong station, Chang'e Moon missions), high-speed rail network (40,000+ km).\n\n"
"**History:** 5,000+ year civilization, dynasties (Shang, Zhou, Qin, Han, Tang, Song, Ming, Qing), Mao Zedong founded PRC (1949), economic reforms under Deng Xiaoping (1978), rapid growth since."
)

_add(["japan", "japanese"],
"Japan is an island nation in East Asia known for technology, culture, and economic power.\n\n"
"**Key Facts:**\n"
"- **Capital:** Tokyo (metro pop: 37M — world's largest metro area)\n"
"- **Population:** ~124 million (declining, aging society)\n"
"- **Currency:** Yen (¥, JPY)\n"
"- **Government:** Constitutional monarchy with parliamentary government\n"
"- **Emperor:** Naruhito | **PM:** Varies (parliamentary system)\n\n"
"**Economy (4th largest GDP):**\n"
"- Automotive: Toyota (#1 global), Honda, Nissan, Subaru, Mazda\n"
"- Electronics: Sony, Panasonic, Nintendo, Canon, Nikon\n"
"- Robotics: World leader in industrial robots\n"
"- Semiconductor equipment: Critical supplier\n\n"
"**Culture:** Anime/manga, sushi/ramen, martial arts, Shinto/Buddhism, samurai history, tea ceremony, cherry blossoms (sakura), bullet trains (Shinkansen).\n\n"
"**Technology:** Robotics leadership, hydrogen fuel cells, gaming industry (Nintendo, Sony PlayStation), precision manufacturing."
)

_add(["world war", "ww1", "ww2", "world war 2", "world war 1"],
"The two World Wars were the most devastating conflicts in human history.\n\n"
"**World War I (1914–1918):**\n"
"- **Trigger:** Assassination of Archduke Franz Ferdinand of Austria\n"
"- **Sides:** Allies (UK, France, Russia, Italy, US from 1917) vs Central Powers (Germany, Austria-Hungary, Ottoman Empire)\n"
"- **Key Events:** Trench warfare, Battle of the Somme, Russian Revolution, US entry\n"
"- **Casualties:** ~20 million dead, ~21 million wounded\n"
"- **Result:** Treaty of Versailles, League of Nations, Ottoman Empire dissolved, map of Europe redrawn\n\n"
"**World War II (1939–1945):**\n"
"- **Trigger:** Germany's invasion of Poland under Hitler\n"
"- **Sides:** Allies (US, UK, Soviet Union, China, France) vs Axis (Germany, Japan, Italy)\n"
"- **Key Events:**\n"
"  - Holocaust: 6 million Jews systematically murdered\n"
"  - D-Day: Allied invasion of Normandy (June 6, 1944)\n"
"  - Pearl Harbor: Japan attacks US (Dec 7, 1941)\n"
"  - Stalingrad: Turning point on Eastern Front\n"
"  - Atomic bombs: Hiroshima (Aug 6) and Nagasaki (Aug 9, 1945)\n"
"- **Casualties:** 70-85 million dead (deadliest conflict in history, ~3% of world population)\n"
"- **Result:** United Nations founded, Cold War began, decolonization accelerated, US and USSR emerged as superpowers"
)

_add(["indian history", "mughal", "british raj", "indian independence", "gandhi"],
"India's history spans over 5,000 years of civilization.\n\n"
"**Ancient India:**\n"
"- Indus Valley Civilization (3300-1300 BCE): Harappa, Mohenjo-daro. Advanced urban planning, drainage.\n"
"- Vedic Period: Sanskrit texts (Vedas), caste system origins\n"
"- Maurya Empire (322-185 BCE): Chandragupta Maurya, Emperor Ashoka (spread Buddhism)\n"
"- Gupta Empire (320-550 CE): 'Golden Age' — advances in math (zero, decimal system), science, art\n\n"
"**Medieval India:**\n"
"- Delhi Sultanate (1206-1526): Islamic rule in North India\n"
"- Mughal Empire (1526-1857): Babur, Akbar (tolerance), Shah Jahan (Taj Mahal), Aurangzeb. Unified most of India.\n"
"- Vijayanagara, Chola, Maratha empires in South/West\n\n"
"**British Raj (1858-1947):**\n"
"- East India Company gradually took control from 1757\n"
"- Direct British Crown rule from 1858\n"
"- Exploitation of resources, famines, suppression\n\n"
"**Independence Movement:**\n"
"- Mahatma Gandhi: Non-violent resistance (satyagraha), Salt March (1930)\n"
"- Jawaharlal Nehru, Sardar Patel, Subhas Chandra Bose, Bhagat Singh\n"
"- Quit India Movement (1942)\n"
"- Independence: August 15, 1947\n"
"- Partition: India and Pakistan separated, massive migration, violence\n"
"- Republic: Constitution adopted January 26, 1950 (Republic Day)\n\n"
"**Modern India:** Nehru era (industrialization), Green Revolution (1960s), economic liberalization (1991, Manmohan Singh), IT boom, nuclear power, space program."
)

# ═══════════════════════════════════════════════════════
#  BUSINESS & ECONOMICS
# ═══════════════════════════════════════════════════════

_add(["economics", "economy", "gdp", "inflation", "recession"],
"Economics studies how individuals, businesses, and governments allocate scarce resources.\n\n"
"**Microeconomics (individual level):**\n"
"- Supply and demand: Price determined by intersection\n"
"- Elasticity: How demand changes with price\n"
"- Market structures: Perfect competition, monopoly, oligopoly, monopolistic competition\n"
"- Consumer surplus, producer surplus, deadweight loss\n\n"
"**Macroeconomics (national/global level):**\n"
"- **GDP (Gross Domestic Product):** Total value of goods/services. World GDP: ~$105 trillion.\n"
"  - US: $28T, China: $18T, Japan: $4.2T, Germany: $4.5T, India: $3.7T\n"
"- **Inflation:** Rising prices. Measured by CPI. Central banks target ~2%.\n"
"- **Interest Rates:** Central banks raise rates to fight inflation, lower to stimulate growth\n"
"- **Unemployment:** Natural rate ~4-5%. Types: frictional, structural, cyclical\n"
"- **Fiscal Policy:** Government spending and taxes\n"
"- **Monetary Policy:** Central bank controls money supply and interest rates\n"
"- **Recession:** Two consecutive quarters of negative GDP growth\n\n"
"**Key Concepts:** Opportunity cost, comparative advantage, trade deficits/surpluses, exchange rates, national debt, quantitative easing (QE)."
)

_add(["startup", "entrepreneurship", "venture capital", "vc", "unicorn"],
"A startup is a newly established business designed for rapid growth and scalability.\n\n"
"**Startup Stages:**\n"
"1. **Ideation:** Problem identification, market research\n"
"2. **MVP (Minimum Viable Product):** Simplest version to test with real users\n"
"3. **Product-Market Fit:** When your product meets genuine demand\n"
"4. **Growth/Scale:** Rapid user acquisition, team building\n"
"5. **Exit:** IPO, acquisition, or continued private operation\n\n"
"**Funding Rounds:**\n"
"- **Pre-seed:** $10K-500K (friends, family, angels)\n"
"- **Seed:** $500K-5M (angel investors, accelerators)\n"
"- **Series A:** $5-15M (VCs, product-market fit proven)\n"
"- **Series B:** $15-50M (scaling operations)\n"
"- **Series C+:** $50M+ (expansion, pre-IPO)\n"
"- **IPO:** Going public on stock exchange\n\n"
"**Key Metrics:** MRR (Monthly Recurring Revenue), ARR, CAC (Customer Acquisition Cost), LTV (Lifetime Value), Churn rate, Burn rate, Runway.\n\n"
"**Unicorns ($1B+ valuation):** Stripe ($65B), SpaceX ($180B), Databricks ($43B), Canva ($26B), Discord ($15B).\n\n"
"**Top VCs:** Sequoia Capital, a16z (Andreessen Horowitz), Accel, Y Combinator, Lightspeed, Tiger Global."
)

_add(["blockchain", "cryptocurrency", "bitcoin", "ethereum", "crypto", "defi", "nft", "web3"],
"Blockchain is a distributed, immutable ledger recording transactions across a decentralized network.\n\n"
"**How Blockchain Works:**\n"
"1. Transaction initiated\n"
"2. Broadcast to peer-to-peer network\n"
"3. Validators verify using consensus mechanism\n"
"4. Transaction grouped into a block\n"
"5. Block cryptographically linked to previous block → chain\n"
"6. Record is permanent and tamper-resistant\n\n"
"**Major Cryptocurrencies:**\n"
"- **Bitcoin (BTC):** First cryptocurrency. Created 2009 by Satoshi Nakamoto (unknown identity). Digital gold, store of value. Market cap: ~$1.3T. Max supply: 21M coins. Proof of Work.\n"
"- **Ethereum (ETH):** Smart contract platform. Created by Vitalik Buterin (2015). Transitioned to Proof of Stake (2022). Powers DeFi, NFTs, dApps.\n"
"- **Solana (SOL):** High speed (~65K TPS), low fees. Popular for DeFi and NFTs.\n"
"- **Others:** BNB (Binance), XRP (Ripple), Cardano, Polkadot, Avalanche\n\n"
"**DeFi (Decentralized Finance):** Lending (Aave, Compound), DEXs (Uniswap, dYdX), stablecoins (USDT, USDC, DAI), yield farming.\n\n"
"**NFTs:** Non-fungible tokens — unique digital assets. Art, music, gaming items, collectibles.\n\n"
"**Web3:** Decentralized internet vision — user-owned data, blockchain-based apps, DAOs (Decentralized Autonomous Organizations)."
)

_add(["stock market", "investing", "stocks", "shares", "trading"],
"The stock market is where shares of publicly traded companies are bought and sold.\n\n"
"**Major Exchanges:**\n"
"- **NYSE (New York Stock Exchange):** Largest by market cap\n"
"- **NASDAQ:** Tech-heavy (Apple, Google, Amazon, Microsoft)\n"
"- **BSE/NSE:** India (Sensex, Nifty 50)\n"
"- **LSE:** London | **TSE:** Tokyo | **SSE:** Shanghai\n\n"
"**Key Concepts:**\n"
"- **Market Cap:** Stock price × total shares outstanding\n"
"- **P/E Ratio:** Price-to-Earnings — is the stock expensive?\n"
"- **Dividend:** Company paying shareholders from profits\n"
"- **Bull Market:** Rising prices | **Bear Market:** Falling prices\n"
"- **Index:** Basket of stocks (S&P 500, Dow Jones, Nifty 50)\n\n"
"**Investment Types:**\n"
"- Stocks (equity), Bonds (debt), Mutual Funds, ETFs (Exchange-Traded Funds), Index Funds, REITs (Real Estate)\n"
"- Growth vs Value investing\n"
"- Dollar-cost averaging (invest regularly)\n\n"
"**World's Most Valuable Companies (2024):** Apple (~$3T), Microsoft (~$3T), Nvidia (~$3T), Amazon (~$2T), Alphabet/Google (~$2T), Meta (~$1.3T)."
)

# ═══════════════════════════════════════════════════════
#  HEALTH & HUMAN BODY
# ═══════════════════════════════════════════════════════

_add(["human body", "anatomy", "organs", "body systems"],
"The human body is a complex biological system of interconnected organs and systems.\n\n"
"**Major Organ Systems:**\n"
"1. **Skeletal:** 206 bones, support and protection\n"
"2. **Muscular:** 600+ muscles, movement and posture\n"
"3. **Circulatory:** Heart pumps blood through 100,000 km of blood vessels\n"
"4. **Respiratory:** Lungs — gas exchange (O₂ in, CO₂ out). 20,000+ breaths/day\n"
"5. **Digestive:** Mouth → esophagus → stomach → small intestine → large intestine. 9m long.\n"
"6. **Nervous:** Brain (86 billion neurons), spinal cord, nerves. Processes sensation, thought, movement.\n"
"7. **Immune:** White blood cells, antibodies, lymph nodes — fights infection\n"
"8. **Endocrine:** Hormones — thyroid, adrenal, pancreas (insulin), pituitary\n"
"9. **Reproductive:** Male (testes, sperm) / Female (ovaries, eggs, uterus)\n"
"10. **Urinary:** Kidneys filter blood (200L/day), bladder stores urine\n"
"11. **Integumentary:** Skin (largest organ, 1.5-2m²), hair, nails\n\n"
"**Key Facts:**\n"
"- Brain uses 20% of body's energy\n"
"- Heart beats ~100,000 times per day (~3B in a lifetime)\n"
"- Blood: 4.7-5.5L in average adult\n"
"- DNA in one cell stretched out = 2 meters\n"
"- Stomach acid pH: 1.5-3.5 (can dissolve metal)"
)

_add(["health", "nutrition", "fitness", "exercise", "diet", "wellness"],
"Health encompasses physical, mental, and social well-being.\n\n"
"**Nutrition:**\n"
"- **Carbohydrates:** Primary energy source. Complex (whole grains, vegetables) > Simple (sugar). 45-65% of calories.\n"
"- **Proteins:** Building blocks (amino acids). Muscle repair, enzymes, hormones. 0.8-1.6g per kg body weight. Sources: meat, fish, eggs, legumes, dairy.\n"
"- **Fats:** Essential for hormones, brain function, cell membranes. Healthy: olive oil, nuts, avocado, fish (omega-3). Avoid: trans fats.\n"
"- **Vitamins:** A (vision), B complex (energy), C (immune), D (bones, from sunlight), E (antioxidant), K (blood clotting)\n"
"- **Minerals:** Iron (blood), Calcium (bones), Zinc (immune), Magnesium (muscles), Potassium (heart)\n"
"- **Water:** 2-3L/day. 60% of body weight.\n\n"
"**Exercise (WHO recommendations):**\n"
"- 150 min moderate OR 75 min vigorous aerobic activity per week\n"
"- Strength training 2+ days/week\n"
"- Types: Cardio (running, swimming, cycling), Strength (weights, resistance), Flexibility (yoga, stretching), Balance (tai chi)\n\n"
"**Sleep:** Adults: 7-9 hours. Crucial for memory consolidation, immune function, mood regulation, hormone balance.\n\n"
"**Mental Health:** Meditation, stress management, social connection, therapy (CBT), adequate sleep, regular exercise, limiting screen time."
)

_add(["covid", "coronavirus", "pandemic", "sars-cov-2"],
"COVID-19 is a respiratory disease caused by the SARS-CoV-2 virus.\n\n"
"**Timeline:**\n"
"- **Dec 2019:** First cases identified in Wuhan, China\n"
"- **Jan 2020:** WHO declares Public Health Emergency\n"
"- **Mar 2020:** WHO declares pandemic. Global lockdowns begin.\n"
"- **Dec 2020:** First vaccines authorized (Pfizer-BioNTech mRNA)\n"
"- **2021:** Vaccination campaigns worldwide. Delta variant surge.\n"
"- **2022:** Omicron variant (more transmissible, less severe). Restrictions easing.\n"
"- **May 2023:** WHO ends global health emergency declaration.\n\n"
"**Global Impact:**\n"
"- **Deaths:** 7+ million confirmed (actual toll likely higher)\n"
"- **Economic:** Trillions in GDP loss, supply chain disruptions\n"
"- **Social:** Remote work revolution, digital transformation accelerated\n"
"- **Education:** School closures affecting 1.6 billion students\n\n"
"**Vaccines:**\n"
"- mRNA: Pfizer-BioNTech, Moderna (revolutionary new technology)\n"
"- Viral vector: AstraZeneca, Johnson & Johnson, Sputnik V\n"
"- Inactivated: Covaxin (India), Sinovac, Sinopharm\n"
"- 13+ billion doses administered worldwide\n\n"
"**Long COVID:** Persistent symptoms (fatigue, brain fog, breathlessness) in 10-20% of infected people."
)

# ═══════════════════════════════════════════════════════
#  GENERAL KNOWLEDGE & CULTURE
# ═══════════════════════════════════════════════════════

_add(["united nations", "un", "international organizations"],
"The United Nations (UN) is an international organization founded in 1945 after WWII to maintain global peace and cooperation.\n\n"
"**Members:** 193 member states (nearly every country)\n"
"**Headquarters:** New York City\n"
"**Secretary-General:** António Guterres (since 2017)\n\n"
"**Main Bodies:**\n"
"- **General Assembly:** All members, one vote each. Meets annually.\n"
"- **Security Council:** 15 members (5 permanent with veto: US, UK, France, Russia, China)\n"
"- **Secretariat:** Administrative functions, headed by Secretary-General\n"
"- **ICJ (International Court of Justice):** Settles legal disputes, The Hague\n\n"
"**Agencies:** WHO (health), UNICEF (children), UNESCO (education/culture), UNHCR (refugees), WFP (food), FAO (agriculture), ILO (labor).\n\n"
"**Other International Organizations:**\n"
"- **NATO:** Military alliance (31 members, North America + Europe)\n"
"- **World Bank / IMF:** Development finance, monetary stability\n"
"- **WTO:** Global trade rules\n"
"- **G7/G20:** Forums for major economies\n"
"- **EU:** European Union (27 members, single market)\n"
"- **ASEAN:** Southeast Asian cooperation"
)

_add(["cricket", "ipl", "cricket world cup"],
"Cricket is a bat-and-ball sport popular in South Asia, England, Australia, and the Caribbean.\n\n"
"**Formats:**\n"
"- **Test Cricket:** 5 days, 2 innings each, white clothing. The ultimate test.\n"
"- **ODI (One Day International):** 50 overs per side. World Cup every 4 years.\n"
"- **T20:** 20 overs per side. Fast-paced, explosive. T20 World Cup, IPL.\n\n"
"**IPL (Indian Premier League):**\n"
"- World's richest cricket league (franchise T20)\n"
"- Teams: Mumbai Indians, Chennai Super Kings, Royal Challengers, KKR, etc.\n"
"- Attracts world's best players\n"
"- Brand value: $10B+\n\n"
"**Key Terms:** Runs, wickets, overs, innings, maiden, century (100 runs), half-century (50), duck (0), hat-trick (3 wickets in 3 balls), LBW, no-ball, boundary (4 runs), six (6 runs).\n\n"
"**Legends:** Sachin Tendulkar (100 international centuries), Virat Kohli, MS Dhoni, Brian Lara, Sir Don Bradman (99.94 average), Ricky Ponting, Wasim Akram, Shane Warne.\n\n"
"**ICC Rankings:** Teams ranked in Tests, ODIs, T20Is. Top teams: India, Australia, England, South Africa, New Zealand."
)

_add(["football", "soccer", "fifa", "world cup football"],
"Football (soccer) is the world's most popular sport with 4+ billion fans globally.\n\n"
"**The Game:** 11 players per side, 90 minutes (two 45-min halves), objective: score goals.\n\n"
"**FIFA World Cup:**\n"
"- Held every 4 years. Most-watched sporting event (5B+ viewers for 2022).\n"
"- 2022 winner: Argentina (Lionel Messi) in Qatar\n"
"- Most wins: Brazil (5), Germany (4), Italy (4), Argentina (3)\n"
"- 2026: US, Canada, Mexico (expanded to 48 teams)\n\n"
"**Top Leagues:**\n"
"- **Premier League (England):** Most-watched league globally. Arsenal, Man City, Liverpool, Man United, Chelsea.\n"
"- **La Liga (Spain):** Real Madrid, Barcelona, Atletico Madrid\n"
"- **Serie A (Italy):** Juventus, AC Milan, Inter Milan, Napoli\n"
"- **Bundesliga (Germany):** Bayern Munich, Borussia Dortmund\n"
"- **Ligue 1 (France):** PSG, Marseille, Lyon\n\n"
"**Legends:** Pelé, Diego Maradona, Lionel Messi, Cristiano Ronaldo, Zinedine Zidane, Ronaldinho, Johan Cruyff.\n\n"
"**Other Competitions:** UEFA Champions League (Europe's top clubs), Copa América, Euro Championship, Africa Cup of Nations."
)

_add(["olympics", "olympic games"],
"The Olympic Games are the world's largest multi-sport event, held every 4 years.\n\n"
"**History:** Originated in ancient Greece (776 BCE, Olympia). Modern Olympics founded by Pierre de Coubertin (1896, Athens).\n\n"
"**Types:**\n"
"- **Summer Olympics:** 32 sports, 300+ events. Athletics, swimming, gymnastics, basketball, tennis, etc.\n"
"- **Winter Olympics:** 15 sports. Skiing, ice hockey, figure skating, snowboarding, etc.\n"
"- **Paralympics:** Athletes with disabilities. Held after each Olympics.\n\n"
"**Recent Hosts:**\n"
"- 2016: Rio de Janeiro | 2020: Tokyo (held 2021 due to COVID)\n"
"- 2024: Paris | 2028: Los Angeles | 2032: Brisbane\n\n"
"**Most Decorated Athletes:**\n"
"- Michael Phelps (USA): 28 medals (23 gold) — most in history\n"
"- Usain Bolt (Jamaica): 8 gold medals, fastest human ever (9.58s 100m)\n"
"- Larisa Latynina (USSR): 18 medals in gymnastics\n\n"
"**India at Olympics:** First participated 1900. Notable medals: Abhinav Bindra (2008 shooting gold), Neeraj Chopra (2020 javelin gold), hockey team golds (1928-1980)."
)

_add(["social media", "instagram", "tiktok", "youtube", "twitter", "x"],
"Social media platforms connect billions of people for communication, content sharing, and entertainment.\n\n"
"**Major Platforms:**\n"
"- **Facebook (Meta):** 3B+ monthly active users. Oldest major social network. Groups, Marketplace, Reels.\n"
"- **YouTube (Google):** 2.5B+ users. Video platform. Creators, education, entertainment. $30B+ ad revenue.\n"
"- **Instagram (Meta):** 2B+ users. Photos, Stories, Reels, Shopping. Influencer culture.\n"
"- **TikTok (ByteDance):** 1.5B+ users. Short-form video. Algorithm-driven discovery. GenZ dominant.\n"
"- **X (formerly Twitter):** 500M+ users. Real-time news, opinions, threads. Acquired by Elon Musk (2022).\n"
"- **LinkedIn (Microsoft):** 1B+ users. Professional networking, jobs, B2B.\n"
"- **WhatsApp (Meta):** 2.7B+ users. Messaging, voice/video calls, business.\n"
"- **Snapchat:** 750M+ users. Disappearing messages, AR filters.\n"
"- **Reddit:** 1.7B+ monthly visits. Forums/communities (subreddits). 'Front page of the internet.'\n"
"- **Threads (Meta):** Twitter/X competitor launched 2023.\n\n"
"**Impact:** Information democratization, creator economy ($250B+), mental health concerns, misinformation, political polarization, digital marketing revolution."
)

_add(["elon musk", "tesla", "spacex", "musk"],
"Elon Musk is one of the world's most influential entrepreneurs and richest people.\n\n"
"**Born:** June 28, 1971, Pretoria, South Africa\n"
"**Education:** Queen's University → University of Pennsylvania (Physics, Economics)\n"
"**Net Worth:** ~$200-250B (fluctuates, often world's richest)\n\n"
"**Companies:**\n"
"- **Tesla (CEO, 2008-):** Electric vehicles, energy storage, solar. Market cap: $500B+. Models: S, 3, X, Y, Cybertruck. Autopilot/FSD. Gigafactories worldwide.\n"
"- **SpaceX (CEO, 2002-):** Reusable rockets (Falcon 9, Falcon Heavy). Starship (Mars vehicle). Starlink (6,000+ satellites, global internet). First private company to send astronauts to ISS.\n"
"- **X (formerly Twitter, 2022-):** Social media platform. Acquired for $44B. Controversial management.\n"
"- **xAI (2023-):** AI company building Grok chatbot, competitor to ChatGPT.\n"
"- **Neuralink (2016-):** Brain-computer interfaces. First human implant (2024).\n"
"- **The Boring Company (2016-):** Tunnel infrastructure, Las Vegas Loop.\n\n"
"**Earlier:** Co-founded Zip2 (sold $307M) → X.com/PayPal (sold $1.5B to eBay).\n\n"
"**Vision:** Make humanity multiplanetary (Mars colonization), accelerate sustainable energy, advance AI."
)

_add(["space exploration", "nasa", "isro", "spacex rockets", "mars"],
"Space exploration pushes the boundaries of human knowledge and capability.\n\n"
"**Major Space Agencies:**\n"
"- **NASA (US):** Apollo Moon landings (1969-72), Space Shuttle, ISS, Mars rovers, Artemis program\n"
"- **ISRO (India):** Chandrayaan-3 (Moon landing 2023, 4th country ever!), Mangalyaan (Mars, first attempt success), Gaganyaan (crewed mission planned)\n"
"- **ESA (Europe):** Rosetta (comet landing), ExoMars, Ariane rockets\n"
"- **CNSA (China):** Tiangong space station, Chang'e Moon missions, Zhurong Mars rover\n"
"- **Roscosmos (Russia):** Soyuz rockets, ISS partner, Mir station history\n\n"
"**Private Companies:**\n"
"- **SpaceX:** Reusable Falcon 9 (200+ launches), Dragon capsule (astronaut transport), Starship (largest rocket ever, Mars vehicle), Starlink constellation\n"
"- **Blue Origin (Jeff Bezos):** New Shepard (suborbital tourism), New Glenn (orbital)\n"
"- **Virgin Galactic:** Space tourism\n"
"- **Rocket Lab:** Small satellite launches\n\n"
"**Key Achievements:**\n"
"- First satellite: Sputnik (USSR, 1957)\n"
"- First human in space: Yuri Gagarin (USSR, 1961)\n"
"- Moon landing: Apollo 11, Neil Armstrong (US, 1969)\n"
"- International Space Station: Continuously occupied since 2000\n"
"- James Webb Space Telescope (2022): Most powerful space telescope, seeing early universe\n"
"- Mars: Perseverance rover + Ingenuity helicopter (2021)"
)

# ═══════════════════════════════════════════════════════
#  FAMOUS SCIENTISTS & LEADERS
# ═══════════════════════════════════════════════════════

_add(["albert einstein", "einstein"],
"Albert Einstein (1879-1955) was a theoretical physicist, widely regarded as one of the most influential scientists in history.\n\n"
"**Key Contributions:**\n"
"- **Special Relativity (1905):** E = mc² — mass and energy are interchangeable. Nothing can travel faster than light. Time dilates at high speeds.\n"
"- **General Relativity (1915):** Gravity is the curvature of spacetime caused by mass. Predicted gravitational waves (confirmed 2015), black holes, gravitational lensing.\n"
"- **Photoelectric Effect (1905):** Light comes in packets (photons). Won the Nobel Prize in Physics (1921) for this work. Foundation of quantum mechanics.\n"
"- **Brownian Motion:** Proved atoms exist through statistical mechanics.\n\n"
"**Life:** Born in Ulm, Germany. Worked as patent clerk in Switzerland. Fled Nazi Germany (1933) to Princeton, USA. Warned Roosevelt about German nuclear weapons → Manhattan Project.\n\n"
"**Legacy:** Revolutionized our understanding of space, time, energy, and gravity. Named 'Person of the Century' by Time magazine (1999)."
)

_add(["isaac newton", "newton"],
"Sir Isaac Newton (1642-1727) was an English mathematician, physicist, and astronomer. One of the most influential scientists ever.\n\n"
"**Key Contributions:**\n"
"- **Laws of Motion:**\n"
"  1. An object at rest stays at rest (inertia)\n"
"  2. F = ma (Force = mass × acceleration)\n"
"  3. Every action has an equal and opposite reaction\n"
"- **Universal Gravitation:** F = Gm₁m₂/r² — every mass attracts every other mass\n"
"- **Calculus:** Co-invented (independently with Leibniz) — mathematical foundation for physics\n"
"- **Optics:** White light is a spectrum of colors (prism experiment)\n"
"- **Principia Mathematica (1687):** One of the most important scientific books ever written\n\n"
"**Famous Quote:** \"If I have seen further, it is by standing on the shoulders of giants.\"\n\n"
"**Legacy:** His laws governed physics for 200+ years until Einstein's relativity. Still used for most engineering calculations today."
)

_add(["sundar pichai", "google ceo"],
"Sundar Pichai is the CEO of Alphabet Inc. (Google's parent company) and Google.\n\n"
"**Born:** June 10, 1972, Madurai, Tamil Nadu, India\n"
"**Education:** IIT Kharagpur (Metallurgical Engineering) → Stanford (MS) → Wharton (MBA)\n\n"
"**Career at Google:**\n"
"- Joined Google 2004\n"
"- Led development of Google Chrome browser (2008, now 65%+ market share)\n"
"- Oversaw Chrome OS and Chromebook\n"
"- Led Android development\n"
"- Became Google CEO (2015) and Alphabet CEO (2019)\n\n"
"**Under His Leadership:**\n"
"- Google AI (Gemini), Google Cloud growth\n"
"- Pixel phones, YouTube expansion\n"
"- Alphabet revenue grew from $75B (2015) to $307B (2023)\n"
"- Google DeepMind (merged AI labs)\n\n"
"**Known for:** Calm leadership style, product focus, navigating Google through AI transformation. One of the most powerful Indian-origin tech leaders globally."
)

_add(["satya nadella", "microsoft ceo"],
"Satya Nadella is the CEO and Chairman of Microsoft.\n\n"
"**Born:** August 19, 1967, Hyderabad, India\n"
"**Education:** Manipal Institute of Technology (Electrical Engineering) → UW-Milwaukee (MS CS) → University of Chicago Booth (MBA)\n\n"
"**Career:**\n"
"- Joined Microsoft 1992\n"
"- Led Bing, Xbox Live, cloud services\n"
"- Became CEO in February 2014 (3rd CEO after Gates and Ballmer)\n\n"
"**Transformation Under Nadella:**\n"
"- Shifted focus from Windows to Cloud (Azure)\n"
"- Azure became #2 cloud provider (~22% market share)\n"
"- Microsoft 365 subscription model (Office → cloud)\n"
"- Acquired LinkedIn ($26.2B), GitHub ($7.5B), Activision Blizzard ($69B)\n"
"- $13B+ investment in OpenAI → AI integration across all products\n"
"- Copilot AI in Office, Windows, Edge, GitHub\n"
"- Market cap grew from $300B (2014) to $3T+ (2024) — one of most valuable companies\n\n"
"**Leadership Style:** Growth mindset, empathy-driven, 'learn-it-all' not 'know-it-all'. Revitalized Microsoft's culture."
)

_add(["mark zuckerberg", "zuckerberg"],
"Mark Zuckerberg is the co-founder, CEO, and controlling shareholder of Meta Platforms (formerly Facebook).\n\n"
"**Born:** May 14, 1984, White Plains, New York\n"
"**Education:** Harvard University (dropped out sophomore year to focus on Facebook)\n\n"
"**Facebook → Meta:**\n"
"- Founded Facebook (2004) in Harvard dorm room with Eduardo Saverin, Andrew McCollum, Dustin Moskovitz, Chris Hughes\n"
"- IPO (2012) at $104B valuation\n"
"- Acquired Instagram ($1B, 2012), WhatsApp ($19B, 2014), Oculus VR ($2B, 2014)\n"
"- Rebranded to Meta (2021) to focus on metaverse\n"
"- Reality Labs (VR/AR): Quest headsets, spent $46B+ on metaverse R&D\n\n"
"**Current Products:**\n"
"- Facebook (3B users), Instagram (2B), WhatsApp (2.7B), Messenger\n"
"- Threads (Twitter/X competitor)\n"
"- Meta AI (LLaMA open-source models)\n"
"- Quest VR headsets\n\n"
"**Net Worth:** ~$160-200B\n\n"
"**Controversies:** Cambridge Analytica data scandal, congressional hearings, misinformation concerns, antitrust scrutiny."
)

_add(["jeff bezos", "bezos", "amazon"],
"Jeff Bezos is the founder of Amazon and Blue Origin, and one of the world's richest people.\n\n"
"**Born:** January 12, 1964, Albuquerque, New Mexico\n"
"**Education:** Princeton University (Computer Science, Electrical Engineering)\n\n"
"**Amazon:**\n"
"- Founded in 1994 as online bookstore from his garage in Bellevue, Washington\n"
"- IPO 1997 at $438M valuation\n"
"- Expanded to everything: 'The Everything Store'\n"
"- **AWS (Amazon Web Services):** Launched 2006. Now the world's #1 cloud platform (~32% market share). $90B+ annual revenue.\n"
"- **Prime:** 200M+ subscribers. Streaming, free shipping, music, gaming.\n"
"- **Other:** Alexa/Echo, Kindle, Ring, Whole Foods, MGM Studios\n"
"- Revenue: $575B+ (2023). ~1.5M employees.\n"
"- Market cap: ~$2T\n\n"
"**Blue Origin (2000):** Space company. New Shepard (suborbital tourism), New Glenn (orbital rocket). Bezos flew to space (2021).\n\n"
"**Washington Post:** Purchased 2013 for $250M.\n\n"
"**Stepped down as Amazon CEO** in 2021 (Andy Jassy succeeded him). Remains Executive Chairman.\n"
"**Net Worth:** ~$200B."
)

# ═══════════════════════════════════════════════════════
#  ADDITIONAL TOPICS
# ═══════════════════════════════════════════════════════

_add(["operating system", "os", "linux", "windows", "macos"],
"An operating system (OS) manages computer hardware and provides services for applications.\n\n"
"**Desktop/Server OS:**\n"
"- **Windows (Microsoft):** 72% desktop market share. Versions: 10, 11, Server. DirectX for gaming.\n"
"- **macOS (Apple):** Unix-based, known for design and privacy. Runs on Apple Silicon (M1/M2/M3/M4).\n"
"- **Linux:** Open-source kernel. Distributions: Ubuntu, Fedora, Debian, Arch, CentOS, RHEL. Powers 96.3% of web servers, all Android phones, most cloud infrastructure.\n\n"
"**Mobile OS:**\n"
"- **Android (Google):** 72% global market. Open-source (AOSP). Samsung, Xiaomi, OnePlus, Google Pixel.\n"
"- **iOS (Apple):** 27% global market. iPhone exclusive. App Store, privacy focus.\n\n"
"**Key Concepts:** Kernel (core), processes/threads, memory management (virtual memory, paging), file systems (NTFS, ext4, APFS), device drivers, shell (CLI), scheduling algorithms, system calls."
)

_add(["networking", "tcp", "ip", "http", "dns", "internet", "wifi"],
"Computer networking connects devices to share resources and communicate.\n\n"
"**Internet:** Global network of networks. 5.3 billion users (66% of world population).\n\n"
"**Key Protocols:**\n"
"- **TCP/IP:** Foundation of internet. TCP ensures reliable delivery. IP handles addressing.\n"
"- **HTTP/HTTPS:** Web communication. HTTPS adds TLS encryption.\n"
"- **DNS:** Translates domain names (google.com) to IP addresses (142.250.x.x)\n"
"- **DHCP:** Automatically assigns IP addresses to devices\n"
"- **SSH:** Secure remote terminal access\n"
"- **FTP/SFTP:** File transfer\n"
"- **SMTP/IMAP/POP3:** Email protocols\n"
"- **WebSocket:** Real-time bidirectional communication\n\n"
"**OSI Model (7 layers):** Physical → Data Link → Network → Transport → Session → Presentation → Application\n\n"
"**Concepts:** IP addresses (IPv4: 32-bit, IPv6: 128-bit), MAC addresses, subnetting, routing, switching, firewalls, NAT, VPN, CDN, load balancing, DNS resolution, SSL/TLS certificates."
)

_add(["devops", "ci/cd", "cicd", "deployment", "infrastructure"],
"DevOps combines development and operations practices for faster, reliable software delivery.\n\n"
"**Key Practices:**\n"
"- **CI (Continuous Integration):** Automatically build and test code on every commit\n"
"- **CD (Continuous Delivery/Deployment):** Automatically deploy tested code to production\n"
"- **IaC (Infrastructure as Code):** Define infrastructure in config files. Terraform, CloudFormation, Pulumi, Ansible.\n"
"- **Monitoring:** Prometheus + Grafana, Datadog, New Relic, PagerDuty\n"
"- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana), Splunk, Loki\n"
"- **Containerization:** Docker + Kubernetes\n"
"- **GitOps:** Git as single source of truth for infrastructure (ArgoCD, Flux)\n\n"
"**CI/CD Tools:** GitHub Actions, GitLab CI, Jenkins, CircleCI, Travis CI, Azure Pipelines, AWS CodePipeline.\n\n"
"**Pipeline:** Code → Build → Unit Tests → Integration Tests → Security Scan → Deploy to Staging → Deploy to Production → Monitor.\n\n"
"**Culture:** Shared responsibility, automation, measurement, continuous improvement, blameless postmortems."
)

_add(["agile", "scrum", "kanban", "project management"],
"Agile is an iterative approach to project management and software development.\n\n"
"**Agile Manifesto (2001) Values:**\n"
"1. Individuals and interactions over processes and tools\n"
"2. Working software over comprehensive documentation\n"
"3. Customer collaboration over contract negotiation\n"
"4. Responding to change over following a plan\n\n"
"**Scrum Framework:**\n"
"- **Sprints:** 2-4 week iterations\n"
"- **Roles:** Product Owner (what to build), Scrum Master (process), Dev Team (how to build)\n"
"- **Events:** Sprint Planning, Daily Standup (15 min), Sprint Review, Retrospective\n"
"- **Artifacts:** Product Backlog, Sprint Backlog, Increment\n"
"- **Story Points:** Relative effort estimation (Fibonacci: 1, 2, 3, 5, 8, 13)\n\n"
"**Kanban:**\n"
"- Visual board: To Do → In Progress → Review → Done\n"
"- WIP (Work In Progress) limits — prevent overload\n"
"- Continuous flow (no fixed sprints)\n"
"- Focus on lead time and throughput\n\n"
"**Tools:** Jira, Linear, Asana, Trello, Notion, Monday.com, ClickUp."
)

_add(["psychology", "mental health", "therapy", "cognitive", "depression", "anxiety"],
"Psychology is the scientific study of mind, behavior, and mental processes.\n\n"
"**Major Branches:**\n"
"- **Clinical Psychology:** Diagnosing and treating mental disorders\n"
"- **Cognitive Psychology:** How we think, perceive, remember, and decide\n"
"- **Developmental Psychology:** How people change across the lifespan\n"
"- **Social Psychology:** How people influence and relate to each other\n"
"- **Neuropsychology:** Brain-behavior relationships\n"
"- **Industrial-Organizational:** Psychology in the workplace\n\n"
"**Common Mental Health Conditions:**\n"
"- **Depression:** Persistent sadness, loss of interest, fatigue. Affects 280M+ people globally.\n"
"- **Anxiety Disorders:** Excessive worry, panic attacks, phobias. Most common mental illness.\n"
"- **PTSD:** After traumatic events — flashbacks, nightmares, hypervigilance.\n"
"- **ADHD:** Attention deficit, hyperactivity, impulsivity.\n"
"- **Bipolar Disorder:** Alternating mania and depression.\n"
"- **OCD:** Obsessive thoughts + compulsive behaviors.\n\n"
"**Therapies:**\n"
"- **CBT (Cognitive Behavioral Therapy):** Most evidence-based. Change negative thought patterns.\n"
"- **DBT (Dialectical Behavior Therapy):** For emotional regulation, borderline personality.\n"
"- **Psychodynamic:** Explore unconscious patterns (Freud-influenced)\n"
"- **Humanistic:** Person-centered, self-actualization (Maslow, Rogers)\n"
"- **Medication:** SSRIs, SNRIs, benzodiazepines, mood stabilizers\n\n"
"**Key Figures:** Sigmund Freud, Carl Jung, B.F. Skinner, Abraham Maslow, Carl Rogers, Jean Piaget, Daniel Kahneman."
)

_add(["renewable energy", "solar energy", "wind energy", "clean energy", "green energy"],
"Renewable energy comes from naturally replenishing sources that don't deplete.\n\n"
"**Types:**\n"
"- **Solar:** Photovoltaic panels convert sunlight to electricity. Cheapest energy source in history (~$0.04/kWh). Growing 25%+ annually.\n"
"- **Wind:** Turbines convert wind to electricity. Onshore and offshore. 2nd cheapest.\n"
"- **Hydroelectric:** Dams convert water flow to electricity. Largest renewable source currently.\n"
"- **Geothermal:** Heat from Earth's interior. Reliable baseload power.\n"
"- **Biomass:** Organic matter for energy (wood, crops, waste).\n"
"- **Nuclear:** Not technically renewable, but zero-carbon. Provides ~10% of world's electricity. Fission now, fusion in research.\n"
"- **Hydrogen:** Green hydrogen from electrolysis using renewable electricity.\n\n"
"**Global Progress:**\n"
"- Renewables: ~30% of global electricity (2023)\n"
"- Solar + wind capacity doubled in last 5 years\n"
"- Battery storage costs dropped 90% in a decade\n"
"- EVs: 14% of new car sales globally (2023)\n\n"
"**Challenges:** Intermittency (sun doesn't always shine), storage, grid infrastructure, land use, mining for materials (lithium, cobalt, rare earths)."
)

_add(["bollywood", "indian cinema", "hindi movies"],
"Bollywood is the Hindi-language film industry based in Mumbai, India — the world's largest film industry by number of films produced.\n\n"
"**Key Facts:**\n"
"- Produces 1,500-2,000 films per year\n"
"- Named after 'Bombay' (Mumbai) + Hollywood\n"
"- Known for song-and-dance sequences, vibrant colors, dramatic storylines\n"
"- Global audience: popular across South Asia, Middle East, Africa, Southeast Asia\n\n"
"**Iconic Stars:**\n"
"- **Shah Rukh Khan:** 'King of Bollywood', Pathaan, Jawan, DDLJ\n"
"- **Amitabh Bachchan:** 'Big B', legendary actor since 1970s\n"
"- **Aamir Khan:** '3 Idiots', 'Dangal', 'PK' — quality-focused\n"
"- **Salman Khan:** Massive fan following, action films\n"
"- **Deepika Padukone, Alia Bhatt, Priyanka Chopra:** Top actresses with global recognition\n\n"
"**Highest-Grossing Indian Films:** Baahubali 2, RRR, KGF 2, Pathaan, Jawan, Dangal, PK.\n\n"
"**Other Indian Film Industries:** Tollywood (Telugu), Kollywood (Tamil), Sandalwood (Kannada), Mollywood (Malayalam) — collectively produce more films than Bollywood."
)

_add(["education", "university", "college", "iit", "mit", "harvard"],
"Education systems prepare individuals with knowledge and skills for life and careers.\n\n"
"**Top Universities (Global Rankings):**\n"
"- **MIT (Massachusetts Institute of Technology):** #1 globally. Engineering, CS, science.\n"
"- **Stanford University:** Silicon Valley. Startups, CS, AI research.\n"
"- **Harvard University:** Oldest US university (1636). Law, medicine, business, humanities.\n"
"- **Oxford/Cambridge (UK):** World's oldest English-speaking universities.\n"
"- **Caltech:** Small but mighty. Physics, space science.\n\n"
"**India's Top Institutions:**\n"
"- **IITs (Indian Institutes of Technology):** IIT Bombay, Delhi, Madras, Kanpur, Kharagpur. Premier engineering. Extremely competitive (JEE Advanced).\n"
"- **IIMs (Indian Institutes of Management):** IIM Ahmedabad, Bangalore, Calcutta. Top MBA.\n"
"- **AIIMS:** Top medical institution.\n"
"- **IISc Bangalore:** Top research university.\n"
"- **BITS Pilani, NIT, IIIT:** Other premier tech institutes.\n\n"
"**Education Trends:** Online learning (Coursera, edX, Khan Academy), coding bootcamps, micro-credentials, AI in education, skill-based learning, MOOCs."
)

_add(["philosophy", "philosopher", "meaning of life", "existentialism"],
"Philosophy is the study of fundamental questions about existence, knowledge, values, reason, and reality.\n\n"
"**Major Branches:**\n"
"- **Metaphysics:** Nature of reality, existence, time, space\n"
"- **Epistemology:** Nature of knowledge, truth, belief, justification\n"
"- **Ethics:** Right and wrong, moral principles, justice\n"
"- **Logic:** Valid reasoning, arguments, fallacies\n"
"- **Aesthetics:** Beauty, art, taste, perception\n"
"- **Political Philosophy:** Justice, rights, liberty, governance\n\n"
"**Major Philosophers:**\n"
"- **Socrates (469-399 BCE):** 'I know that I know nothing.' Socratic method of questioning.\n"
"- **Plato (428-348 BCE):** Theory of Forms, Republic, Allegory of the Cave.\n"
"- **Aristotle (384-322 BCE):** Logic, ethics, biology. 'Father of Western Philosophy.'\n"
"- **Immanuel Kant (1724-1804):** Categorical imperative, duty-based ethics.\n"
"- **Friedrich Nietzsche (1844-1900):** 'God is dead', will to power, Übermensch.\n"
"- **Jean-Paul Sartre (1905-1980):** Existentialism — 'existence precedes essence.'\n"
"- **Simone de Beauvoir (1908-1986):** Feminist philosophy, The Second Sex.\n\n"
"**Schools:** Stoicism (acceptance), Utilitarianism (greatest good), Existentialism (individual freedom), Nihilism (no inherent meaning), Pragmatism (practical truth), Absurdism (Camus)."
)

_add(["world religions", "religion", "hinduism", "islam", "christianity", "buddhism"],
"Religion is a system of beliefs, practices, and values concerning the sacred and spiritual.\n\n"
"**Major World Religions (by followers):**\n\n"
"**1. Christianity (2.4 billion):**\n"
"- Based on teachings of Jesus Christ. Bible. God, salvation, resurrection.\n"
"- Denominations: Catholic, Protestant, Orthodox\n"
"- Spread globally from Middle East\n\n"
"**2. Islam (1.9 billion):**\n"
"- Founded by Prophet Muhammad (7th century CE). Quran. Monotheistic (Allah).\n"
"- Five Pillars: Shahada, Salat (prayer), Zakat (charity), Sawm (fasting), Hajj (pilgrimage)\n"
"- Branches: Sunni (~85%), Shia (~15%)\n\n"
"**3. Hinduism (1.2 billion):**\n"
"- Oldest living religion (~4,000+ years). India origin. No single founder.\n"
"- Concepts: Brahman (universal soul), karma, dharma, moksha, reincarnation\n"
"- Sacred texts: Vedas, Upanishads, Bhagavad Gita, Ramayana, Mahabharata\n"
"- Major gods: Brahma (creator), Vishnu (preserver), Shiva (destroyer)\n\n"
"**4. Buddhism (500 million):**\n"
"- Founded by Siddhartha Gautama (Buddha, ~500 BCE) in India\n"
"- Four Noble Truths, Eightfold Path, meditation, enlightenment (nirvana)\n"
"- Branches: Theravada, Mahayana, Vajrayana\n\n"
"**5. Sikhism (30 million):**\n"
"- Founded by Guru Nanak (1469, Punjab). One God. Equality. Service.\n\n"
"**Others:** Judaism (15M), Jainism (4M), Shinto, Taoism, Bahá'í, Zoroastrianism."
)


# ═══════════════════════════════════════════════════════
#  GENERAL WORLD FACTS
# ═══════════════════════════════════════════════════════

_add(["solar system", "planets", "sun", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune"],
"The Solar System consists of the Sun and everything gravitationally bound to it.\n\n"
"**The 8 Planets (in order from Sun):**\n"
"1. **Mercury** — Smallest planet, closest to Sun, no atmosphere, extreme temperatures\n"
"2. **Venus** — Hottest planet (462°C), thick CO₂ atmosphere, similar size to Earth\n"
"3. **Earth** — Only known planet with life, 71% water, 1 moon\n"
"4. **Mars** — Red Planet, thin atmosphere, Olympus Mons (largest volcano), 2 moons\n"
"5. **Jupiter** — Largest planet, Great Red Spot, 95+ moons (Ganymede largest moon in solar system)\n"
"6. **Saturn** — Famous rings (ice and rock), 146+ moons (Titan has atmosphere)\n"
"7. **Uranus** — Ice giant, tilted 98° on its side, 27 moons\n"
"8. **Neptune** — Farthest planet, strongest winds (2,100 km/h), 16 moons\n\n"
"**Other:** Dwarf planets (Pluto, Ceres, Eris), Asteroid Belt, Kuiper Belt, Oort Cloud.\n\n"
"**The Sun:** A G-type main-sequence star, age ~4.6 billion years, surface temp ~5,500°C, will become a red giant in ~5 billion years."
)

_add(["earth", "planet earth", "world"],
"Earth is the third planet from the Sun and the only known planet to harbor life.\n\n"
"**Key Facts:**\n"
"- **Age:** ~4.54 billion years\n"
"- **Diameter:** 12,742 km\n"
"- **Surface:** 71% water, 29% land\n"
"- **Atmosphere:** 78% nitrogen, 21% oxygen, 1% other\n"
"- **Population:** ~8.1 billion humans\n"
"- **Moon:** 1 natural satellite\n"
"- **Rotation:** 24 hours (1 day), Orbit: 365.25 days (1 year)\n"
"- **Distance from Sun:** ~150 million km (1 AU)\n\n"
"**Structure:** Inner core (solid iron), outer core (liquid iron), mantle, crust.\n\n"
"**Continents:** Asia, Africa, North America, South America, Antarctica, Europe, Australia/Oceania."
)

_add(["mathematics", "math", "maths"],
"Mathematics is the study of numbers, quantities, shapes, and patterns.\n\n"
"**Major Branches:**\n"
"- **Arithmetic:** Numbers, operations (+, −, ×, ÷)\n"
"- **Algebra:** Variables, equations, polynomials\n"
"- **Geometry:** Shapes, angles, areas, volumes\n"
"- **Trigonometry:** Sin, cos, tan, triangles\n"
"- **Calculus:** Derivatives, integrals, limits\n"
"- **Statistics:** Data analysis, probability, distributions\n"
"- **Linear Algebra:** Matrices, vectors, transformations\n"
"- **Number Theory:** Prime numbers, divisibility, modular arithmetic\n\n"
"**Constants:** π ≈ 3.14159, e ≈ 2.71828, φ (golden ratio) ≈ 1.61803\n\n"
"**Famous Problems:** Riemann Hypothesis, P vs NP, Goldbach's Conjecture."
)

_add(["physics", "newton", "einstein", "relativity", "quantum physics", "quantum mechanics"],
"Physics is the study of matter, energy, and the fundamental forces of nature.\n\n"
"**Major Branches:**\n"
"- **Classical Mechanics:** Newton's laws, motion, gravity, F=ma\n"
"- **Thermodynamics:** Heat, energy, entropy\n"
"- **Electromagnetism:** Electric/magnetic fields, Maxwell's equations, light\n"
"- **Quantum Mechanics:** Subatomic particles, wave-particle duality, uncertainty principle\n"
"- **Relativity:** Einstein's Special (E=mc²) and General (gravity = spacetime curvature)\n"
"- **Nuclear Physics:** Radioactivity, fission, fusion\n\n"
"**Key Constants:**\n"
"- Speed of light: c = 299,792,458 m/s\n"
"- Gravitational constant: G = 6.674 × 10⁻¹¹\n"
"- Planck's constant: h = 6.626 × 10⁻³⁴ J·s\n\n"
"**Key Figures:** Isaac Newton, Albert Einstein, Niels Bohr, Richard Feynman, Stephen Hawking, Marie Curie."
)

_add(["chemistry", "elements", "periodic table"],
"Chemistry is the study of matter, its properties, composition, and reactions.\n\n"
"**Branches:**\n"
"- **Organic:** Carbon compounds (life, polymers, drugs)\n"
"- **Inorganic:** Metals, minerals, non-carbon compounds\n"
"- **Physical:** Energy in reactions, thermodynamics\n"
"- **Analytical:** Identifying composition\n"
"- **Biochemistry:** Chemistry of living organisms\n\n"
"**Key Concepts:**\n"
"- **Atoms:** Protons, neutrons, electrons\n"
"- **Periodic Table:** 118 elements organized by atomic number\n"
"- **Chemical Bonds:** Ionic, covalent, metallic, hydrogen\n"
"- **Reactions:** Synthesis, decomposition, combustion, redox\n"
"- **pH Scale:** 0-14 (acid < 7 < base)\n\n"
"**Common Elements:** Hydrogen (H), Oxygen (O), Carbon (C), Nitrogen (N), Iron (Fe), Gold (Au), Silver (Ag)."
)

_add(["biology", "cell", "dna", "evolution", "genetics"],
"Biology is the study of living organisms and life processes.\n\n"
"**Key Branches:**\n"
"- **Cell Biology:** Cells are the basic unit of life. Prokaryotic (bacteria) vs Eukaryotic (plants, animals)\n"
"- **Genetics:** DNA, genes, chromosomes, heredity. DNA = deoxyribonucleic acid (double helix)\n"
"- **Evolution:** Natural selection (Darwin), adaptation, speciation\n"
"- **Ecology:** Ecosystems, food chains, biodiversity\n"
"- **Microbiology:** Bacteria, viruses, fungi\n"
"- **Anatomy:** Human body systems\n\n"
"**Human Body Systems:**\n"
"- Circulatory (heart, blood), Respiratory (lungs), Nervous (brain, nerves)\n"
"- Digestive, Skeletal, Muscular, Immune, Endocrine, Reproductive\n\n"
"**Key Facts:** Human body has ~37 trillion cells, DNA has ~3 billion base pairs, ~8.7 million species on Earth."
)

_add(["history", "ancient history", "modern history", "world history"],
"History is the study of past events, particularly human civilization.\n\n"
"**Major Periods:**\n"
"- **Ancient (~3000 BCE - 500 CE):** Mesopotamia, Egypt, Greece, Rome, Indus Valley, China\n"
"- **Medieval (500-1500):** Feudalism, Crusades, Mongol Empire, Black Death\n"
"- **Renaissance (1400-1600):** Art, science revival in Europe\n"
"- **Age of Exploration (1400-1600):** Columbus, Vasco da Gama, Magellan\n"
"- **Industrial Revolution (1760-1840):** Steam engine, factories, urbanization\n"
"- **Modern (1900+):** World Wars, Cold War, Space Race, Digital Revolution\n\n"
"**Key Events:**\n"
"- Printing Press (1440), American Independence (1776), French Revolution (1789)\n"
"- WW1 (1914-18), WW2 (1939-45), Moon Landing (1969), Internet (1990s)\n\n"
"**Ancient Civilizations:** Sumerian, Egyptian, Indus Valley, Chinese, Greek, Roman, Mayan, Aztec, Inca."
)

_add(["geography", "continents", "countries"],
"Geography is the study of Earth's lands, features, and inhabitants.\n\n"
"**7 Continents (by size):** Asia, Africa, North America, South America, Antarctica, Europe, Australia/Oceania\n\n"
"**5 Oceans (by size):** Pacific, Atlantic, Indian, Southern, Arctic\n\n"
"**Key Records:**\n"
"- Tallest Mountain: Mount Everest (8,849 m)\n"
"- Longest River: Nile (6,650 km)\n"
"- Largest Desert: Sahara (9.2 million km²)\n"
"- Deepest Point: Mariana Trench (10,994 m)\n"
"- Largest Lake: Caspian Sea (371,000 km²)\n"
"- Highest Waterfall: Angel Falls (979 m)\n\n"
"**Most Populous Countries:** India, China, USA, Indonesia, Pakistan, Brazil, Nigeria, Bangladesh."
)

_add(["economics", "economy", "gdp", "inflation", "finance"],
"Economics studies how societies allocate scarce resources.\n\n"
"**Key Concepts:**\n"
"- **GDP:** Gross Domestic Product — total value of goods/services produced\n"
"- **Inflation:** Rising prices over time, measured by CPI\n"
"- **Supply & Demand:** Price determined by market forces\n"
"- **Fiscal Policy:** Government spending and taxation\n"
"- **Monetary Policy:** Central bank controls money supply, interest rates\n\n"
"**Economic Systems:** Capitalism (free market), Socialism (state control), Mixed Economy\n\n"
"**Largest Economies (GDP):** USA, China, Germany, Japan, India\n\n"
"**Key Terms:** Bull/Bear market, recession, depression, trade deficit, exchange rate, stock market, bonds, mutual funds."
)

_add(["internet", "www", "world wide web", "website"],
"The Internet is a global network of interconnected computers.\n\n"
"**History:**\n"
"- 1969: ARPANET (first network, US Department of Defense)\n"
"- 1989: Tim Berners-Lee invented the World Wide Web\n"
"- 1991: First website goes live\n"
"- 1990s: Browsers (Netscape, IE), search engines, email\n"
"- 2000s: Social media (Facebook, YouTube, Twitter), smartphones\n"
"- 2010s: Cloud computing, streaming, AI\n"
"- 2020s: AI chatbots, 5G, Web3, metaverse\n\n"
"**How It Works:** Devices → ISPs → Routers → DNS → Servers → Content delivery\n\n"
"**Key Stats:** ~5.4 billion internet users worldwide (~67% of global population)."
)

# ═══════════════════════════════════════════════════════
#  SEARCH FUNCTION
# ═══════════════════════════════════════════════════════

def find_knowledge(query: str) -> str | None:
    q = query.lower().strip()

    for key, entry in WORLD_KNOWLEDGE.items():
        for k in entry["keys"]:
            if len(k) <= 3:
                if re.search(r'\b' + re.escape(k) + r'\b', q):
                    return entry["content"]
            else:
                if k in q:
                    return entry["content"]

    stop = {"a", "an", "the", "is", "are", "was", "were", "what", "how",
            "why", "when", "where", "who", "which", "do", "does", "did",
            "can", "could", "would", "should", "will", "about", "for",
            "to", "of", "in", "on", "at", "by", "with", "from", "me",
            "my", "i", "you", "your", "tell", "explain", "describe",
            "please", "help", "want", "need", "give", "latest", "news",
            "analyze", "research", "discuss", "detailed", "comprehensive",
            "batao", "samjhao", "kya", "hai", "kaise", "kyun",
            "know", "think", "say", "said", "like", "just", "also",
            "very", "really", "much", "many", "some", "any", "all",
            "between", "through", "into", "has", "have", "had", "been",
            "being", "their", "they", "them", "his", "her", "its",
            "our", "more", "most", "other", "new", "old", "good", "bad",
            "make", "made", "get", "got", "take", "took", "come", "came"}
    q_words = {w for w in q.split() if w not in stop and len(w) > 2}

    if not q_words:
        return None

    best_entry = None
    best_score = 0
    for key, entry in WORLD_KNOWLEDGE.items():
        all_kw = set()
        for k in entry["keys"]:
            all_kw.update(k.split())
        overlap = len(q_words & all_kw)
        if overlap > best_score:
            best_score = overlap
            best_entry = entry

    if best_entry and best_score >= 2:
        return best_entry["content"]

    return None
