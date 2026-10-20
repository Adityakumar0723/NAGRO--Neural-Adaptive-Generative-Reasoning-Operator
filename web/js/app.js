/* NAGRO 4.1 — Chat UI with Streaming */
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
        clearChat:   $('#clearChat'),
        uploadBtn:   $('#uploadBtn'),
        imageUpload: $('#imageUpload'),
        imagePreview:$('#imagePreview'),
    };

    const state = {
        sessions: loadSessions(),
        activeId: null,
        loading: false,
        pendingImage: null,
    };

    function loadSessions() {
        try { return JSON.parse(localStorage.getItem('nagro_s') || '[]'); }
        catch { return []; }
    }
    function save() {
        try { localStorage.setItem('nagro_s', JSON.stringify(state.sessions)); } catch {}
    }

    function init() {
        bindEvents();
        renderSessions();
        showWelcome();
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
        els.menuBtn.addEventListener('click', toggleSidebar);
        els.closeSidebar.addEventListener('click', () => {
            els.sidebar.classList.add('hidden');
            els.sidebar.classList.remove('show');
        });
        if (els.clearChat) {
            els.clearChat.addEventListener('click', newChat);
        }
        if (els.uploadBtn) {
            els.uploadBtn.addEventListener('click', () => els.imageUpload.click());
        }
        if (els.imageUpload) {
            els.imageUpload.addEventListener('change', handleImageSelect);
        }
        const imageCapCard = $('#imageCapCard');
        if (imageCapCard) {
            imageCapCard.addEventListener('click', () => els.imageUpload.click());
        }
        const chatArea = els.chatArea;
        if (chatArea) {
            chatArea.addEventListener('dragover', e => { e.preventDefault(); chatArea.classList.add('drag-over'); });
            chatArea.addEventListener('dragleave', () => chatArea.classList.remove('drag-over'));
            chatArea.addEventListener('drop', e => {
                e.preventDefault();
                chatArea.classList.remove('drag-over');
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('image/')) {
                    state.pendingImage = file;
                    showImagePreview(file);
                    els.sendBtn.disabled = false;
                }
            });
        }
        $$('.cap-card').forEach(c => {
            c.addEventListener('click', () => {
                els.input.value = c.dataset.prompt;
                resize();
                els.sendBtn.disabled = false;
                els.input.focus();
            });
        });
    }

    function toggleSidebar() {
        if (window.innerWidth <= 768) {
            els.sidebar.classList.toggle('show');
            els.sidebar.classList.toggle('hidden');
        } else {
            els.sidebar.classList.toggle('hidden');
        }
    }

    function resize() {
        els.input.style.height = 'auto';
        els.input.style.height = Math.min(els.input.scrollHeight, 180) + 'px';
    }

    function uid() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }

    function showWelcome() {
        els.welcome.classList.remove('hidden');
        els.messages.classList.add('hidden');
        els.messages.innerHTML = '';
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

    function renderSessions() {
        els.sessions.innerHTML = '';
        state.sessions.forEach(s => {
            const div = document.createElement('div');
            div.className = 'session-item' + (s.id === state.activeId ? ' active' : '');
            div.innerHTML = '<span class="session-title">' + esc(s.title) + '</span><button class="delete-session" title="Delete">&times;</button>';
            div.querySelector('.session-title').addEventListener('click', () => loadSession(s.id));
            div.querySelector('.delete-session').addEventListener('click', e => {
                e.stopPropagation();
                deleteSession(s.id);
            });
            els.sessions.appendChild(div);
        });
    }

    function highlightSession() {
        $$('.session-item', els.sessions).forEach((el, i) => {
            el.classList.toggle('active', state.sessions[i] && state.sessions[i].id === state.activeId);
        });
    }

    function loadSession(id) {
        const s = state.sessions.find(x => x.id === id);
        if (!s) return;
        state.activeId = id;
        els.welcome.classList.add('hidden');
        els.messages.classList.remove('hidden');
        els.messages.innerHTML = '';
        s.messages.forEach(m => appendMsg(m.role, m.content, false));
        scrollBottom();
        renderSessions();
    }

    function deleteSession(id) {
        state.sessions = state.sessions.filter(x => x.id !== id);
        save();
        if (state.activeId === id) newChat();
        renderSessions();
    }

    function handleImageSelect(e) {
        const file = e.target.files[0];
        if (!file) return;
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file (PNG, JPG, GIF, etc.)');
            return;
        }
        if (file.size > 10 * 1024 * 1024) {
            alert('Image too large. Maximum size is 10 MB.');
            return;
        }
        state.pendingImage = file;
        showImagePreview(file);
        els.sendBtn.disabled = false;
    }

    function showImagePreview(file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const sizeKB = (file.size / 1024).toFixed(1);
            els.imagePreview.innerHTML =
                '<img src="' + e.target.result + '" alt="Preview">' +
                '<div class="preview-info">' +
                    '<div class="preview-name">' + esc(file.name) + '</div>' +
                    '<div>' + sizeKB + ' KB &bull; ' + file.type + '</div>' +
                '</div>' +
                '<button class="preview-remove" title="Remove">&times;</button>';
            els.imagePreview.classList.remove('hidden');
            els.imagePreview.querySelector('.preview-remove').addEventListener('click', removeImage);
        };
        reader.readAsDataURL(file);
    }

    function removeImage() {
        state.pendingImage = null;
        els.imagePreview.classList.add('hidden');
        els.imagePreview.innerHTML = '';
        els.imageUpload.value = '';
        els.sendBtn.disabled = !els.input.value.trim();
    }

    async function send() {
        const text = els.input.value.trim();
        const hasImage = !!state.pendingImage;
        if (!text && !hasImage) return;
        if (state.loading) return;

        state.loading = true;
        els.sendBtn.disabled = true;
        els.input.value = '';
        resize();

        const imageFile = state.pendingImage;
        removeImage();

        const displayText = imageFile
            ? (text || 'Analyze this image') + '\n\n📷 *Image uploaded: ' + imageFile.name + '*'
            : text;

        if (!state.activeId) {
            const titleText = text || 'Image Analysis';
            const title = titleText.length > 35 ? titleText.slice(0, 35) + '...' : titleText;
            state.sessions.unshift({ id: uid(), title, messages: [] });
            state.activeId = state.sessions[0].id;
            save();
            renderSessions();
        }

        els.welcome.classList.add('hidden');
        els.messages.classList.remove('hidden');

        appendMsg('user', displayText);
        saveMsg('user', displayText);

        const assistantDiv = createStreamingMsg();
        const contentEl = assistantDiv.querySelector('.msg-content');
        let fullResponse = '';

        try {
            if (imageFile) {
                const formData = new FormData();
                formData.append('file', imageFile);
                const res = await fetch(BACKEND + API + '/image/analyze', {
                    method: 'POST',
                    body: formData,
                });
                if (!res.ok) throw new Error('HTTP ' + res.status);
                const data = await res.json();
                if (data.success) {
                    fullResponse = data.analysis;
                } else {
                    fullResponse = 'Image analysis failed: ' + (data.error || 'Unknown error');
                }
                contentEl.innerHTML = renderMarkdown(fullResponse);
                addCopyButtons(assistantDiv);
            } else {
                const res = await fetch(BACKEND + API + '/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text, conversation_id: state.activeId, stream: true }),
                });

                if (!res.ok) throw new Error('HTTP ' + res.status);

                const ct = res.headers.get('content-type') || '';

                if (ct.includes('text/event-stream')) {
                    const reader = res.body.getReader();
                    const decoder = new TextDecoder();
                    let buffer = '';

                    while (true) {
                        const { done, value } = await reader.read();
                        if (done) break;
                        buffer += decoder.decode(value, { stream: true });

                        const lines = buffer.split('\n');
                        buffer = lines.pop();

                        for (const line of lines) {
                            if (line.startsWith('data: ')) {
                                const data = line.slice(6).trim();
                                if (data === '[DONE]') continue;
                                try {
                                    const parsed = JSON.parse(data);
                                    if (parsed.content) {
                                        fullResponse += parsed.content;
                                        contentEl.innerHTML = renderMarkdown(fullResponse);
                                        addCopyButtons(assistantDiv);
                                        scrollBottom();
                                    }
                                } catch {}
                            }
                        }
                    }
                } else {
                    const data = await res.json();
                    fullResponse = data.message || data.response || '';
                    contentEl.innerHTML = renderMarkdown(fullResponse);
                    addCopyButtons(assistantDiv);
                }
            }

            if (!fullResponse) {
                fullResponse = 'No response received.';
                contentEl.innerHTML = renderMarkdown(fullResponse);
            }

            finishStreamingMsg(assistantDiv, fullResponse);
            saveMsg('assistant', fullResponse);

        } catch (err) {
            fullResponse = 'Could not reach the server. Make sure the backend is running.\n\nError: `' + err.message + '`';
            contentEl.innerHTML = renderMarkdown(fullResponse);
            finishStreamingMsg(assistantDiv, fullResponse);
        }

        state.loading = false;
        els.sendBtn.disabled = !els.input.value.trim();
        els.input.focus();
    }

    function createStreamingMsg() {
        const div = document.createElement('div');
        div.className = 'msg assistant';
        div.innerHTML =
            '<div class="msg-inner">' +
                '<div class="msg-avatar">N</div>' +
                '<div class="msg-body">' +
                    '<div class="msg-role">NAGRO</div>' +
                    '<div class="msg-content"><span class="cursor-blink"></span></div>' +
                '</div>' +
            '</div>';
        els.messages.appendChild(div);
        scrollBottom();
        return div;
    }

    function finishStreamingMsg(div, content) {
        const cursor = div.querySelector('.cursor-blink');
        if (cursor) cursor.remove();

        const actionsHtml = '<div class="msg-actions">' +
            '<button class="msg-action-btn copy-msg-btn" title="Copy"><svg width="12" height="12" viewBox="0 0 24 24" fill="none"><rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" stroke-width="2"/></svg> Copy</button>' +
            '<button class="msg-action-btn regen-btn" title="Regenerate"><svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M1 4v6h6M23 20v-6h-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Retry</button>' +
            '</div>';

        div.querySelector('.msg-body').insertAdjacentHTML('beforeend', actionsHtml);

        const copyMsgBtn = div.querySelector('.copy-msg-btn');
        if (copyMsgBtn) {
            copyMsgBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(content).then(() => {
                    copyMsgBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Copied';
                    setTimeout(() => {
                        copyMsgBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" stroke-width="2"/></svg> Copy';
                    }, 2000);
                });
            });
        }

        const regenBtn = div.querySelector('.regen-btn');
        if (regenBtn) {
            regenBtn.addEventListener('click', () => {
                const s = state.sessions.find(x => x.id === state.activeId);
                if (!s || s.messages.length < 2) return;
                const lastUserMsg = [...s.messages].reverse().find(m => m.role === 'user');
                if (!lastUserMsg) return;
                s.messages = s.messages.slice(0, -1);
                save();
                div.remove();
                els.input.value = lastUserMsg.content;
                send();
            });
        }
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

        const avatarText = role === 'user' ? 'U' : 'N';
        const label = role === 'user' ? 'You' : 'NAGRO';

        let actionsHtml = '';
        if (role === 'assistant') {
            actionsHtml = '<div class="msg-actions">' +
                '<button class="msg-action-btn copy-msg-btn" title="Copy"><svg width="12" height="12" viewBox="0 0 24 24" fill="none"><rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" stroke-width="2"/></svg> Copy</button>' +
                '<button class="msg-action-btn regen-btn" title="Regenerate"><svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M1 4v6h6M23 20v-6h-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Retry</button>' +
                '</div>';
        }

        div.innerHTML =
            '<div class="msg-inner">' +
                '<div class="msg-avatar">' + avatarText + '</div>' +
                '<div class="msg-body">' +
                    '<div class="msg-role">' + label + '</div>' +
                    '<div class="msg-content">' + renderMarkdown(content) + '</div>' +
                    actionsHtml +
                '</div>' +
            '</div>';

        els.messages.appendChild(div);
        addCopyButtons(div);

        const copyMsgBtn = div.querySelector('.copy-msg-btn');
        if (copyMsgBtn) {
            copyMsgBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(content).then(() => {
                    copyMsgBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17l-5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Copied';
                    setTimeout(() => {
                        copyMsgBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" stroke-width="2"/></svg> Copy';
                    }, 2000);
                });
            });
        }

        scrollBottom();
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
            const label = lang || 'code';
            codeBlocks.push(
                '<div class="code-header"><span class="code-lang">' + esc(label) + '</span>' +
                '<button class="copy-btn" data-idx="' + idx + '">Copy</button></div>' +
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
        html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');

        html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
        html = html.replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>');
        html = html.replace(/<\/ul>\s*<ul>/g, '');

        html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

        html = html.replace(/\|(.+)\|/g, function(match) {
            const cells = match.split('|').filter(c => c.trim());
            if (cells.every(c => /^[\s-]+$/.test(c))) return '';
            const tag = match.includes('---') ? '' : cells.map(c => '<td>' + c.trim() + '</td>').join('');
            return tag ? '<tr>' + tag + '</tr>' : '';
        });

        html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

        html = html.replace(/\n\n/g, '</p><p>');
        html = html.replace(/\n/g, '<br>');
        if (html && !html.startsWith('<')) html = '<p>' + html;
        if (html && !html.endsWith('>')) html += '</p>';

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
