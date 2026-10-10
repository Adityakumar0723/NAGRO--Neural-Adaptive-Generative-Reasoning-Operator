/**
 * NAGRO 4.1 - Frontend Application
 * Neural Adaptive Generative Reasoning Operator
 */

const API_BASE = '/api/v1';

const state = {
    conversations: [],
    currentConversationId: null,
    messages: [],
    isLoading: false,
    currentMode: 'chat',
};

// DOM Elements
const chatArea = document.getElementById('chatArea');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const newChatBtn = document.getElementById('newChatBtn');
const chatHistory = document.getElementById('chatHistory');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    showWelcomeScreen();
    autoResizeTextarea();
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

    // Mode buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.currentMode = btn.dataset.mode;
        });
    });

    // Capability cards
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

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 200) + 'px';
}

function showWelcomeScreen() {
    chatArea.innerHTML = `
        <div class="welcome-screen">
            <div class="welcome-logo">N</div>
            <h2>NAGRO 4.1</h2>
            <p>Neural Adaptive Generative Reasoning Operator — Your advanced AI assistant for coding, research, image generation, and more.</p>
            <div class="capabilities-grid">
                <div class="capability-card" data-prompt="Write a Python function to sort a list using merge sort with detailed comments">
                    <div class="icon">&lt;/&gt;</div>
                    <h4>Code Generation</h4>
                    <p>Write, debug, and optimize code in any language</p>
                </div>
                <div class="capability-card" data-prompt="Generate an image of a futuristic city with neon lights at night, cyberpunk style">
                    <div class="icon">&#x1F3A8;</div>
                    <h4>Image Generation</h4>
                    <p>Create stunning visuals from text descriptions</p>
                </div>
                <div class="capability-card" data-prompt="Research the latest trends in artificial intelligence and machine learning in 2024">
                    <div class="icon">&#x1F50D;</div>
                    <h4>Deep Research</h4>
                    <p>Search and synthesize information from the web</p>
                </div>
                <div class="capability-card" data-prompt="Solve: Find the integral of (x^2 + 3x + 2) / (x + 1) dx step by step">
                    <div class="icon">&#x1F4CA;</div>
                    <h4>Mathematics</h4>
                    <p>Solve complex math problems step by step</p>
                </div>
                <div class="capability-card" data-prompt="Write a short sci-fi story about an AI that discovers emotions">
                    <div class="icon">&#x270D;&#xFE0F;</div>
                    <h4>Creative Writing</h4>
                    <p>Stories, poetry, content, and more</p>
                </div>
                <div class="capability-card" data-prompt="Explain how neural networks learn, step by step, as if I'm a beginner">
                    <div class="icon">&#x1F9E0;</div>
                    <h4>Reasoning</h4>
                    <p>Complex analysis and logical reasoning</p>
                </div>
            </div>
        </div>
    `;

    // Re-attach capability card listeners
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

    // Clear welcome screen on first message
    if (state.messages.length === 0) {
        chatArea.innerHTML = '<div class="messages-container" id="messagesContainer"></div>';
    }

    // Add user message
    addMessage('user', message);

    // Show typing indicator
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

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const data = await response.json();
        state.currentConversationId = data.conversation_id;

        addMessage('assistant', data.message, data.task_type);
        updateChatHistory(message);

    } catch (error) {
        removeTypingIndicator();
        addMessage('assistant', `**Error:** Could not connect to NAGRO 4.1 server. Make sure the server is running.\n\n\`${error.message}\``, 'error');
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

    const formattedContent = formatMarkdown(content);

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-header">
                <span class="name">${name}</span>
                ${badge}
            </div>
            <div class="message-body">${formattedContent}</div>
        </div>
    `;

    container.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight;

    // Add copy buttons to code blocks
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

    // Code blocks
    text = text.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
        const escaped = escapeHtml(code.trim());
        return `<pre><code class="language-${lang || 'text'}">${escaped}</code></pre>`;
    });

    // Inline code
    text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Bold
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // Italic
    text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Headers
    text = text.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    text = text.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    text = text.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Unordered lists
    text = text.replace(/^- (.+)$/gm, '<li>$1</li>');
    text = text.replace(/(<li>.*<\/li>\n?)+/gs, '<ul>$&</ul>');

    // Ordered lists
    text = text.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

    // Links
    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

    // Paragraphs
    text = text.replace(/\n\n/g, '</p><p>');
    text = text.replace(/\n/g, '<br>');

    if (!text.startsWith('<')) {
        text = '<p>' + text + '</p>';
    }

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
                <span class="badge">thinking</span>
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
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
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

        // Remove active from others
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

        // Update active state
        chatHistory.querySelectorAll('.chat-history-item').forEach(el => {
            el.classList.toggle('active', el.dataset.id === conversationId);
        });
    } catch (err) {
        console.error('Failed to load conversation:', err);
    }
}
