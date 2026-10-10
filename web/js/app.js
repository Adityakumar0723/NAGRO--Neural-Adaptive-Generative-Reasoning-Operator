/* NAGRO 4.1 — Chat UI */
(function () {
    const API = '/api/v1';
    const BACKEND = window.location.hostname === 'localhost' ? '' : 'https://serverless.on-demand.io/apps/nagro';

    const $ = (s, p) => (p || document).querySelector(s);
    const $$ = (s, p) => (p || document).querySelectorAll(s);

    const els = {
        sidebar:     $('#sidebar'),
        sessions:    $('#sessions'),
        welcome:     $('#welcome'),
        messages:    $('#messages'),
        chatArea:    $('#chatArea'),
        input:       $('#msgInput'),
        sendBtn:     $('#sendBtn'),
        newChatBtn:  $('#newChatBtn'),
        menuBtn:     $('#menuBtn'),
        closeSidebar:$('#closeSidebar'),
        modelSelect: $('#modelSelect'),
    };

    const state = {
        sessions: JSON.parse(localStorage.getItem('nagro_sessions') || '[]'),
        activeId: null,
        messages: [],
        loading: false,
    };

    function init() {
        bindEvents();
        renderSessions();
        showWelcome();
        checkHealth();
    }

    function bindEvents() {
        els.sendBtn.addEventListener('click', send);
        els.input.addEventListener('keydown', e => {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
        });
        els.input.addEventListener('input', () => {
            resize();
            els.sendBtn.disabled = !els.input.value.trim();
        });
        els.newChatBtn.addEventListener('click', newChat);
        els.menuBtn.addEventListener('click', () => {
            els.sidebar.classList.toggle('hidden');
            els.sidebar.classList.toggle('show');
        });
        els.closeSidebar.addEventListener('click', () => {
            els.sidebar.classList.add('hidden');
            els.sidebar.classList.remove('show');
        });
        $$('.cap-card').forEach(c => {
            c.addEventListener('click', () => {
                els.input.value = c.dataset.prompt;
                resize();
                els.sendBtn.disabled = false;
                els.input.focus();
            });
        });
    }

    function resize() {
        els.input.style.height = 'auto';
        els.input.style.height = Math.min(els.input.scrollHeight, 200) + 'px';
    }

    async function checkHealth() {
        try {
            const r = await fetch(BACKEND + API + '/health');
            if (r.ok) console.log('NAGRO 4.1 server operational');
        } catch { console.warn('Server not reachable'); }
    }

    function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }

    function showWelcome() {
        els.welcome.classList.remove('hidden');
        els.messages.classList.add('hidden');
        els.messages.innerHTML = '';
        state.messages = [];
        state.activeId = null;
        highlightSession();
    }

    function newChat() {
        showWelcome();
        els.input.value = '';
        resize();
        els.sendBtn.disabled = true;
        els.input.focus();
    }

    function save() {
        localStorage.setItem('nagro_sessions', JSON.stringify(state.sessions));
    }

    function renderSessions() {
        els.sessions.innerHTML = '';
        state.sessions.forEach(s => {
            const div = document.createElement('div');
            div.className = 'session-item' + (s.id === state.activeId ? ' active' : '');
            div.innerHTML = `<span class="session-title">${esc(s.title)}</span><button class="delete-session" title="Delete">&times;</button>`;
            div.querySelector('.session-title').addEventListener('click', () => loadSession(s.id));
            div.querySelector('.delete-session').addEventListener('click', e => {
                e.stopPropagation();
                deleteSession(s.id);
            });
            els.sessions.appendChild(div);
        });
    }

    function highlightSession() {
        $$('.session-item', els.sessions).forEach(el => {
            const title = el.querySelector('.session-title').textContent;
            const s = state.sessions.find(x => x.title === title);
            el.classList.toggle('active', s && s.id === state.activeId);
        });
    }

    function loadSession(id) {
        const s = state.sessions.find(x => x.id === id);
        if (!s) return;
        state.activeId = id;
        state.messages = [...s.messages];
        els.welcome.classList.add('hidden');
        els.messages.classList.remove('hidden');
        els.messages.innerHTML = '';
        s.messages.forEach(m => appendMsg(m.role, m.content, false));
        scrollBottom();
        highlightSession();
        renderSessions();
    }

    function deleteSession(id) {
        state.sessions = state.sessions.filter(x => x.id !== id);
        save();
        if (state.activeId === id) newChat();
        renderSessions();
    }

    async function send() {
        const text = els.input.value.trim();
        if (!text || state.loading) return;

        state.loading = true;
        els.sendBtn.disabled = true;
        els.input.value = '';
        resize();

        if (!state.activeId) {
            const id = uid();
            const title = text.length > 40 ? text.slice(0, 40) + '...' : text;
            state.sessions.unshift({ id, title, messages: [] });
            state.activeId = id;
            save();
            renderSessions();
        }

        els.welcome.classList.add('hidden');
        els.messages.classList.remove('hidden');

        appendMsg('user', text);
        saveMsg('user', text);
        showThinking();

        try {
            const res = await fetch(BACKEND + API + '/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, conversation_id: state.activeId, stream: false }),
            });
            removeThinking();
            if (!res.ok) throw new Error('HTTP ' + res.status);
            const data = await res.json();
            appendMsg('assistant', data.message);
            saveMsg('assistant', data.message);
        } catch (err) {
            removeThinking();
            const errMsg = 'Could not reach NAGRO 4.1 server. Make sure the backend is running.\n\nError: `' + err.message + '`';
            appendMsg('assistant', errMsg);
        }

        state.loading = false;
        els.sendBtn.disabled = !els.input.value.trim();
        els.input.focus();
    }

    function saveMsg(role, content) {
        const s = state.sessions.find(x => x.id === state.activeId);
        if (s) { s.messages.push({ role, content }); save(); }
    }

    function appendMsg(role, content, animate) {
        if (animate === undefined) animate = true;
        const div = document.createElement('div');
        div.className = 'msg ' + role;
        if (!animate) div.style.animation = 'none';

        const avatar = role === 'user' ? 'U' : 'N';
        const label = role === 'user' ? 'You' : 'NAGRO 4.1';
        const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        div.innerHTML =
            '<div class="msg-inner">' +
                '<div class="msg-avatar">' + avatar + '</div>' +
                '<div class="msg-body">' +
                    '<div class="msg-role">' + label + '</div>' +
                    '<div class="msg-content">' + renderMarkdown(content) + '</div>' +
                    '<div class="msg-time">' + now + '</div>' +
                '</div>' +
            '</div>';

        els.messages.appendChild(div);
        addCopyButtons(div);
        scrollBottom();
    }

    function showThinking() {
        const div = document.createElement('div');
        div.className = 'msg assistant';
        div.id = 'thinkingMsg';
        div.innerHTML =
            '<div class="msg-inner">' +
                '<div class="msg-avatar">N</div>' +
                '<div class="msg-body">' +
                    '<div class="msg-role">NAGRO 4.1</div>' +
                    '<div class="thinking"><span></span><span></span><span></span></div>' +
                '</div>' +
            '</div>';
        els.messages.appendChild(div);
        scrollBottom();
    }

    function removeThinking() {
        const t = document.getElementById('thinkingMsg');
        if (t) t.remove();
    }

    function scrollBottom() {
        els.chatArea.scrollTop = els.chatArea.scrollHeight;
    }

    function renderMarkdown(text) {
        if (!text) return '';
        let html = text;

        const codeBlocks = [];
        html = html.replace(/```(\w*)\n([\s\S]*?)```/g, function (_, lang, code) {
            const idx = codeBlocks.length;
            const langLabel = lang || 'code';
            codeBlocks.push(
                '<div class="code-header"><span class="code-lang">' + esc(langLabel) + '</span>' +
                '<button class="copy-btn" data-code="' + idx + '">Copy</button></div>' +
                '<pre><code>' + esc(code.trim()) + '</code></pre>'
            );
            return '\x00CB' + idx + '\x00';
        });

        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
        html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
        html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
        html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
        html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
        html = html.replace(/^---$/gm, '<hr>');
        html = html.replace(/^\> (.+)$/gm, '<blockquote>$1</blockquote>');
        html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>[\s\S]*?<\/li>)/g, function (m) {
            return '<ul>' + m + '</ul>';
        });
        html = html.replace(/<\/ul>\s*<ul>/g, '');
        html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
        html = html.replace(/\n\n/g, '</p><p>');
        html = html.replace(/\n/g, '<br>');
        if (!html.startsWith('<')) html = '<p>' + html;
        if (!html.endsWith('>')) html += '</p>';

        html = html.replace(/\x00CB(\d+)\x00/g, function (_, i) { return codeBlocks[+i]; });

        return html;
    }

    function addCopyButtons(container) {
        $$('.copy-btn', container).forEach(btn => {
            btn.addEventListener('click', function () {
                const pre = this.closest('.code-header')?.nextElementSibling;
                const code = pre ? (pre.querySelector('code')?.textContent || pre.textContent) : '';
                navigator.clipboard.writeText(code).then(() => {
                    btn.textContent = 'Copied!';
                    setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
                });
            });
        });
    }

    function esc(s) {
        const d = document.createElement('div');
        d.appendChild(document.createTextNode(s));
        return d.innerHTML;
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
