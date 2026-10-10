/**
 * NAGRO 4.1 — Frontend Application
 * Neural Adaptive Generative Reasoning Operator
 * 100% Self-Built. No External APIs.
 */

const API_BASE = '/api/v1';

const state = {
    conversations: [],
    currentConversationId: null,
    messages: [],
    isLoading: false,
    currentMode: 'chat',
};

const chatArea = document.getElementById('chatArea');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const newChatBtn = document.getElementById('newChatBtn');
const chatHistory = document.getElementById('chatHistory');

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    showWelcomeScreen();
    autoResizeTextarea();
    checkServerStatus();
});

function setupEventListeners() {
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    messageInput.addEventListener('input', autoResizeTextarea);
    newChatBtn.addEventListener('click', startNewChat);

    document.getElementById('toggleSidebar')?.addEventListener('click', () => {
        document.querySelector('.sidebar').classList.toggle('collapsed');
    });

    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.currentMode = btn.dataset.mode;
        });
    });
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 200) + 'px';
}

async function checkServerStatus() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        const data = await res.json();
        if (data.status === 'operational') {
            console.log('NAGRO 4.1 server is operational (local inference)');
        }
    } catch {
        console.warn('NAGRO 4.1 server not reachable');
    }
}

function showWelcomeScreen() {
    chatArea.innerHTML = `
        <div class="welcome-screen">
            <div class="welcome-logo">N</div>
            <h2>NAGRO 4.1</h2>
            <p>Neural Adaptive Generative Reasoning Operator — 100% self-built AI. Runs entirely on your machine. No external APIs. No data leaves your system.</p>
            <div class="capabilities-grid">
                <div class="capability-card" data-prompt="Write a Python function to implement binary search with detailed explanation">
                    <div class="icon">&lt;/&gt;</div>
                    <h4>Code Generation</h4>
                    <p>Write, debug, optimize code in any language</p>
                </div>
                <div class="capability-card" data-prompt="Generate an image of a futuristic city with neon lights at night">
                    <div class="icon">&#x1F3A8;</div>
                    <h4>Image Generation</h4>
                    <p>Create images locally with Stable Diffusion</p>
                </div>
                <div class="capability-card" data-prompt="Research the latest developments in quantum computing">
                    <div class="icon">&#x1F50D;</div>
                    <h4>Deep Research</h4>
                    <p>Web search and information synthesis</p>
                </div>
                <div class="capability-card" data-prompt="Solve: Find the derivative of f(x) = x^3 * ln(x) step by step">
                    <div class="icon">&#x1F4CA;</div>
                    <h4>Mathematics</h4>
                    <p>Step-by-step problem solving</p>
                </div>
                <div class="capability-card" data-prompt="Write a short sci-fi story about the first AI that dreams">
                    <div class="icon">&#x270D;&#xFE0F;</div>
                    <h4>Creative Writing</h4>
                    <p>Stories, poetry, content creation</p>
                </div>
                <div class="capability-card" data-prompt="Explain how transformers work in deep learning, step by step">
                    <div class="icon">&#x1F9E0;</div>
                    <h4>Reasoning</h4>
                    <p>Complex analysis and logical thinking</p>
                </div>
            </div>
        </div>
    `;

    document.querySelectorAll('.capability-card').forEach(card => {
        card.addEventListener('click', () => {
            const prompt = card.dataset.prompt;
            if (prompt) {
                messageInput.value = prompt;
                autoResizeTextarea();
                messageInput.focus();
            }
        });
    });
}

function startNewChat() {
    state.currentConversationId = null;
    state.messages = [];
    showWelcomeScreen();
    messageInput.value = '';
    autoResizeTextarea();
    messageInput.focus();
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || state.isLoading) return;

    state.isLoading = true;
    sendBtn.disabled = true;
    messageInput.value = '';
    autoResizeTextarea();

    if (state.messages.length === 0) {
        chatArea.innerHTML = '<div class="messages-container" id="messagesContainer"></div>';
    }

    addMessage('user', message);
    showTypingIndicator();

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                conversation_id: state.currentConversationId,
                stream: false,
            }),
        });

        removeTypingIndicator();

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        state.currentConversationId = data.conversation_id;
        addMessage('assistant', data.message, data.task_type);
        updateChatHistory(message);
    } catch (error) {
        removeTypingIndicator();
        addMessage('assistant',
            `**Connection Error**\n\nCould not reach NAGRO 4.1 server.\n\n` +
            `**Setup steps:**\n` +
            `1. Install dependencies: \`pip install -r requirements.txt\`\n` +
            `2. Download a model: \`python download_model.py\`\n` +
            `3. Start server: \`python run.py\`\n\n` +
            `Error: \`${error.message}\``,
            'error'
        );
    }

    state.isLoading = false;
    sendBtn.disabled = false;
    messageInput.focus();
}

function addMessage(role, content, taskType) {
    const container = document.getElementById('messagesContainer') || chatArea;
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = role === 'user' ? 'You' : 'N';
    const name = role === 'user' ? 'You' : 'NAGRO 4.1';
    const badge = taskType && role === 'assistant'
        ? `<span class="badge">${taskType}</span>`
        : '';

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-header">
                <span class="name">${name}</span>
                ${badge}
            </div>
            <div class="message-body">${formatMarkdown(content)}</div>
        </div>
    `;

    container.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight;

    messageDiv.querySelectorAll('pre').forEach(pre => {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.textContent = 'Copy';
        copyBtn.addEventListener('click', () => {
            const code = pre.querySelector('code')?.textContent || pre.textContent;
            navigator.clipboard.writeText(code).then(() => {
                copyBtn.textContent = 'Copied!';
                setTimeout(() => { copyBtn.textContent = 'Copy'; }, 2000);
            });
        });
        pre.style.position = 'relative';
        pre.appendChild(copyBtn);
    });

    state.messages.push({ role, content });
}

function formatMarkdown(text) {
    if (!text) return '';
    text = text.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) =>
        `<pre><code class="language-${lang || 'text'}">${escapeHtml(code.trim())}</code></pre>`
    );
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    text = text.replace(/^# (.+)$/gm, '<h1>$1</h1>');
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*<\/li>\n?)+/gs, '<ul>$&</ul>');
    text = text.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    text = text.replace(/\n\n/g, '</p><p>');
    text = text.replace(/\n/g, '<br>');
    if (!text.startsWith('<')) text = '<p>' + text + '</p>';
    return text;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

function showTypingIndicator() {
    const container = document.getElementById('messagesContainer') || chatArea;
    const indicator = document.createElement('div');
    indicator.id = 'typingIndicator';
    indicator.className = 'message assistant';
    indicator.innerHTML = `
        <div class="message-avatar">N</div>
        <div class="message-content">
            <div class="message-header">
                <span class="name">NAGRO 4.1</span>
                <span class="badge">thinking locally</span>
            </div>
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    container.appendChild(indicator);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function removeTypingIndicator() {
    document.getElementById('typingIndicator')?.remove();
}

function updateChatHistory(firstMessage) {
    const title = firstMessage.substring(0, 30) + (firstMessage.length > 30 ? '...' : '');
    const existing = chatHistory.querySelector(`[data-id="${state.currentConversationId}"]`);
    if (!existing) {
        const item = document.createElement('div');
        item.className = 'chat-history-item active';
        item.dataset.id = state.currentConversationId;
        item.innerHTML = `&#x1F4AC; ${escapeHtml(title)}`;
        item.addEventListener('click', () => loadConversation(state.currentConversationId));
        chatHistory.querySelectorAll('.chat-history-item').forEach(el => el.classList.remove('active'));
        chatHistory.prepend(item);
    }
}

async function loadConversation(conversationId) {
    try {
        const response = await fetch(`${API_BASE}/conversations/${conversationId}`);
        if (!response.ok) return;
        const conv = await response.json();
        state.currentConversationId = conversationId;
        state.messages = [];
        chatArea.innerHTML = '<div class="messages-container" id="messagesContainer"></div>';
        for (const msg of conv.messages || []) {
            addMessage(msg.role, msg.content, msg.metadata?.task_type);
        }
        chatHistory.querySelectorAll('.chat-history-item').forEach(el => {
            el.classList.toggle('active', el.dataset.id === conversationId);
        });
    } catch (err) {
        console.error('Failed to load conversation:', err);
    }
}
