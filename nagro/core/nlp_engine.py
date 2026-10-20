"""
NAGRO 4.1 — Self-Built NLP Engine
100% self-built. No NLTK. No spaCy. No transformers. Pure Python.

Capabilities:
- Question type classification
- Synonym matching
- Text similarity scoring
- Answer assembly from multiple sources
- Intent extraction
- Smart response formatting
"""

from __future__ import annotations
import re
import math
from collections import Counter


SYNONYMS: dict[str, list[str]] = {
    "ai": ["artificial intelligence", "machine learning", "deep learning", "neural network"],
    "ml": ["machine learning", "ai", "deep learning", "data science"],
    "python": ["programming", "coding", "scripting", "py"],
    "javascript": ["js", "frontend", "web development", "node"],
    "html": ["web", "webpage", "website", "markup"],
    "css": ["styling", "design", "frontend", "web design"],
    "database": ["db", "sql", "mysql", "postgresql", "mongodb", "sqlite"],
    "api": ["rest api", "endpoint", "web service", "http"],
    "computer": ["pc", "laptop", "machine", "system"],
    "phone": ["mobile", "smartphone", "cellphone"],
    "fast": ["quick", "rapid", "speedy", "swift"],
    "big": ["large", "huge", "enormous", "massive"],
    "small": ["tiny", "little", "miniature", "compact"],
    "good": ["great", "excellent", "best", "nice", "awesome"],
    "bad": ["poor", "terrible", "worst", "awful"],
    "make": ["create", "build", "develop", "construct", "generate"],
    "show": ["display", "present", "demonstrate", "reveal"],
    "use": ["utilize", "employ", "apply", "leverage"],
    "start": ["begin", "launch", "initiate", "commence"],
    "stop": ["end", "finish", "halt", "terminate"],
    "car": ["automobile", "vehicle", "motor"],
    "money": ["currency", "cash", "finance", "funds"],
    "work": ["job", "employment", "career", "occupation"],
    "world": ["earth", "globe", "planet"],
    "country": ["nation", "state", "land"],
    "language": ["tongue", "dialect", "programming language"],
    "important": ["significant", "crucial", "vital", "essential"],
    "different": ["various", "diverse", "distinct", "varied"],
    "problem": ["issue", "bug", "error", "challenge"],
    "answer": ["solution", "response", "reply", "result"],
}


class QuestionType:
    DEFINITION = "definition"
    HOWTO = "howto"
    COMPARISON = "comparison"
    LIST = "list"
    FACTUAL = "factual"
    OPINION = "opinion"
    YES_NO = "yes_no"
    CAUSE = "cause"
    EXAMPLE = "example"
    CODE = "code"
    CREATIVE = "creative"
    UNKNOWN = "unknown"


def classify_question(prompt: str) -> str:
    p = prompt.lower().strip()

    if re.match(r'^(write|create|build|generate|make|code|implement|develop|banao|likho)\b', p):
        if any(w in p for w in ["poem", "story", "essay", "speech", "song", "lyrics",
                                 "kavita", "kahani", "letter", "email"]):
            return QuestionType.CREATIVE
        return QuestionType.CODE

    if re.match(r'^(what is|what are|what\'s|define|kya hai|kya hota hai)\b', p):
        return QuestionType.DEFINITION

    if re.match(r'^(how to|how do i|how can i|how should|kaise|kaise kare)\b', p):
        return QuestionType.HOWTO

    if any(w in p for w in ["vs", "versus", "compare", "difference between",
                             "better", "which is better", "comparison"]):
        return QuestionType.COMPARISON

    if re.match(r'^(list|name|give me|what are the|enumerate|top \d+|best \d+)\b', p):
        return QuestionType.LIST

    if re.match(r'^(why|kyun|kyon)\b', p):
        return QuestionType.CAUSE

    if re.match(r'^(is|are|was|were|do|does|did|can|could|will|would|should|kya)\b', p):
        if "?" in p or len(p.split()) < 12:
            return QuestionType.YES_NO

    if any(w in p for w in ["example", "give me an example", "show me", "udaharan",
                             "for instance", "such as"]):
        return QuestionType.EXAMPLE

    if re.match(r'^(who|when|where|how many|how much|how old|how long|how far|how tall)\b', p):
        return QuestionType.FACTUAL

    if any(w in p for w in ["think", "opinion", "suggest", "recommend", "should i",
                             "best way", "advice"]):
        return QuestionType.OPINION

    return QuestionType.UNKNOWN


def extract_intent(prompt: str) -> dict:
    p = prompt.lower().strip()
    intent = {
        "action": None,
        "topic": None,
        "question_type": classify_question(prompt),
        "language": None,
        "detail_level": "normal",
    }

    action_match = re.match(
        r'^(write|create|build|make|generate|explain|solve|find|list|compare|'
        r'describe|define|show|give|tell|teach|help|analyze|summarize|'
        r'translate|convert|calculate|implement|design|develop|debug|fix|'
        r'banao|likho|batao|samjhao|karo|dikhao)\b\s*(.*)',
        p
    )
    if action_match:
        intent["action"] = action_match.group(1)
        intent["topic"] = action_match.group(2).strip()

    if any(w in p for w in ["detailed", "in detail", "comprehensive", "thorough",
                             "deep dive", "vistar se", "detail mein"]):
        intent["detail_level"] = "detailed"
    elif any(w in p for w in ["brief", "short", "quick", "simple", "basic", "chhota"]):
        intent["detail_level"] = "brief"

    lang_patterns = {
        "python": r'\bpython\b',
        "javascript": r'\b(?:javascript|js)\b',
        "java": r'\bjava\b(?!script)',
        "html": r'\bhtml\b',
        "css": r'\bcss\b',
        "sql": r'\bsql\b',
        "cpp": r'\b(?:c\+\+|cpp)\b',
        "go": r'\b(?:golang|go lang)\b',
        "rust": r'\brust\b',
        "typescript": r'\b(?:typescript|ts)\b',
    }
    for lang, pat in lang_patterns.items():
        if re.search(pat, p):
            intent["language"] = lang
            break

    return intent


def expand_synonyms(words: set[str]) -> set[str]:
    expanded = set(words)
    for word in words:
        if word in SYNONYMS:
            expanded.update(SYNONYMS[word])
        for key, syns in SYNONYMS.items():
            if word in syns:
                expanded.add(key)
                expanded.update(syns)
    return expanded


def text_similarity(text1: str, text2: str) -> float:
    stop = {"a", "an", "the", "is", "are", "was", "were", "and", "or", "but",
            "in", "on", "at", "to", "for", "of", "with", "by", "from", "this",
            "that", "it", "be", "has", "have", "had", "not", "as", "if", "do",
            "does", "will", "can", "about", "what", "how", "why", "when",
            "where", "who", "which", "my", "your", "i", "you", "we", "they"}

    words1 = {w.lower() for w in re.findall(r'\b\w+\b', text1)} - stop
    words2 = {w.lower() for w in re.findall(r'\b\w+\b', text2)} - stop

    if not words1 or not words2:
        return 0.0

    expanded1 = expand_synonyms(words1)
    overlap = len(expanded1 & words2)
    union = len(words1 | words2)

    if union == 0:
        return 0.0

    return overlap / union


def score_sentences(sentences: list[str], query: str, top_n: int = 8) -> list[str]:
    scored = []
    for s in sentences:
        if len(s.strip()) < 15:
            continue
        sim = text_similarity(query, s)
        if sim > 0.05:
            scored.append((sim, s.strip()))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [s for _, s in scored[:top_n]]


def format_answer(content: str, question_type: str, topic: str) -> str:
    if question_type == QuestionType.DEFINITION:
        return (
            f"## {topic.title()}\n\n"
            f"{content}\n\n"
            f"---\n*Ask me more about {topic} — examples, applications, or related topics!*"
        )

    if question_type == QuestionType.HOWTO:
        lines = content.split('\n')
        has_steps = any(re.match(r'^\d+[.)]', l.strip()) for l in lines)
        if not has_steps:
            parts = [l.strip() for l in lines if l.strip() and len(l.strip()) > 15]
            numbered = "\n".join(f"{i+1}. {p}" for i, p in enumerate(parts[:8]))
            return (
                f"## How to: {topic.title()}\n\n"
                f"{numbered}\n\n"
                f"---\n*Need more detail on any step? Just ask!*"
            )
        return f"## How to: {topic.title()}\n\n{content}"

    if question_type == QuestionType.COMPARISON:
        return (
            f"## {topic.title()}\n\n"
            f"{content}\n\n"
            f"---\n*Want a deeper comparison? Ask about specific aspects!*"
        )

    if question_type == QuestionType.LIST:
        lines = content.split('\n')
        items = [l.strip() for l in lines if l.strip() and len(l.strip()) > 5]
        bulleted = "\n".join(f"- {item}" for item in items[:15]
                             if not item.startswith('-') and not item.startswith('•'))
        if bulleted:
            return f"## {topic.title()}\n\n{bulleted}"
        return f"## {topic.title()}\n\n{content}"

    if question_type == QuestionType.CAUSE:
        return (
            f"## Why: {topic.title()}\n\n"
            f"{content}\n\n"
            f"---\n*Want to dig deeper into the reasons? Ask me!*"
        )

    return f"## {topic.title()}\n\n{content}"


def build_comparison(topic_a: str, topic_b: str, kb_a: str | None, kb_b: str | None) -> str:
    header = f"## {topic_a.title()} vs {topic_b.title()}\n\n"

    if kb_a and kb_b:
        lines_a = [l.strip() for l in kb_a.split('\n') if l.strip() and len(l.strip()) > 20][:5]
        lines_b = [l.strip() for l in kb_b.split('\n') if l.strip() and len(l.strip()) > 20][:5]

        result = header
        result += f"### {topic_a.title()}\n"
        for l in lines_a:
            result += f"- {l}\n"
        result += f"\n### {topic_b.title()}\n"
        for l in lines_b:
            result += f"- {l}\n"
        result += f"\n---\n*Ask me about specific differences between {topic_a} and {topic_b}!*"
        return result

    if kb_a:
        return header + f"**{topic_a.title()}:**\n{kb_a}\n\n*(I don't have detailed info about {topic_b} yet)*"
    if kb_b:
        return header + f"*(I don't have detailed info about {topic_a} yet)*\n\n**{topic_b.title()}:**\n{kb_b}"

    return header + f"I'd need more information about both **{topic_a}** and **{topic_b}** to give a proper comparison."


def extract_comparison_topics(prompt: str) -> tuple[str, str] | None:
    p = prompt.lower()
    patterns = [
        r'(?:compare|difference between|difference of)\s+(.+?)\s+(?:and|vs|versus|or|aur)\s+(.+?)(?:\?|$)',
        r'(.+?)\s+(?:vs|versus)\s+(.+?)(?:\?|$)',
        r'(.+?)\s+(?:ya|or|aur)\s+(.+?)(?:\s+(?:better|best|kaun|which|konsa))',
        r'(?:which is better)\s+(.+?)\s+(?:or|ya|vs)\s+(.+?)(?:\?|$)',
    ]
    for pat in patterns:
        m = re.search(pat, p)
        if m:
            a = m.group(1).strip().strip('"\'')
            b = m.group(2).strip().strip('"\'?.')
            if a and b:
                return (a, b)
    return None
