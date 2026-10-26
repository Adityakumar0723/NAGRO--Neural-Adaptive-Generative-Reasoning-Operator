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
            '<button class="msg-action-btn quick-prompt" data-prompt="Explain the previous answer in simple language">Simple</button>' +
            '<button class="msg-action-btn quick-prompt" data-prompt="Give a practical example of the previous answer">Example</button>' +
            '<button class="msg-action-btn quick-prompt" data-prompt="Continue with the next useful step">Continue</button>' +
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
        addQuickActions(div);
    }

    function addQuickActions(container) {
        $$('.quick-prompt', container).forEach(btn => {
            btn.addEventListener('click', () => {
                els.input.value = btn.dataset.prompt || '';
                resize();
                els.sendBtn.disabled = !els.input.value.trim();
                send();
            });
        });
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
                '<button class="msg-action-btn quick-prompt" data-prompt="Explain the previous answer in simple language">Simple</button>' +
                '<button class="msg-action-btn quick-prompt" data-prompt="Give a practical example of the previous answer">Example</button>' +
                '<button class="msg-action-btn quick-prompt" data-prompt="Continue with the next useful step">Continue</button>' +
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
        addQuickActions(div);

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
            var isPreviewable = /^html?$/i.test(lang);
            codeBlocks.push(
                '<div class="code-header"><span class="code-lang">' + esc(label) + '</span>' +
                '<div class="code-actions">' +
                '<button class="copy-btn" data-idx="' + idx + '">Copy</button>' +
                '<button class="download-btn" data-lang="' + esc(lang || 'txt') + '">Download</button>' +
                (isPreviewable ? '<button class="preview-btn">Preview</button>' : '') +
                '</div></div>' +
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

        $$('.download-btn', container).forEach(function (btn) {
            btn.addEventListener('click', function () {
                var pre = this.closest('.code-header')?.nextElementSibling;
                var code = pre ? (pre.querySelector('code')?.textContent || pre.textContent) : '';
                var lang = (btn.dataset.lang || 'txt').toLowerCase();
                var extMap = {
                    python:'.py', py:'.py', javascript:'.js', js:'.js',
                    typescript:'.ts', ts:'.ts', html:'.html', htm:'.html',
                    css:'.css', java:'.java', c:'.c', cpp:'.cpp', 'c++':'.cpp',
                    csharp:'.cs', cs:'.cs', go:'.go', rust:'.rs', rs:'.rs',
                    ruby:'.rb', rb:'.rb', php:'.php', sql:'.sql', json:'.json',
                    xml:'.xml', yaml:'.yaml', yml:'.yaml', bash:'.sh', sh:'.sh',
                    shell:'.sh', markdown:'.md', md:'.md', swift:'.swift',
                    kotlin:'.kt', kt:'.kt', r:'.r', dart:'.dart', lua:'.lua',
                    perl:'.pl', scala:'.scala', txt:'.txt', code:'.txt'
                };
                var ext = extMap[lang] || ('.' + lang);
                var blob = new Blob([code], { type: 'text/plain' });
                var url = URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = 'nagro-code' + ext;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            });
        });

        $$('.preview-btn', container).forEach(function (btn) {
            btn.addEventListener('click', function () {
                var header = this.closest('.code-header');
                var pre = header ? header.nextElementSibling : null;
                if (!pre) return;
                var existing = pre.nextElementSibling;
                if (existing && existing.classList.contains('code-preview')) {
                    existing.remove();
                    pre.classList.remove('has-preview');
                    btn.textContent = 'Preview';
                    return;
                }
                var code = pre.querySelector('code')?.textContent || pre.textContent;
                var wrapper = document.createElement('div');
                wrapper.className = 'code-preview';
                var iframe = document.createElement('iframe');
                iframe.sandbox = 'allow-scripts';
                iframe.srcdoc = code;
                wrapper.appendChild(iframe);
                pre.classList.add('has-preview');
                pre.insertAdjacentElement('afterend', wrapper);
                btn.textContent = 'Hide Preview';
            });
        });
    }

    function esc(s) {
        const d = document.createElement('div');
        d.appendChild(document.createTextNode(s));
        return d.innerHTML;
    }

    // ══════════════════════════════════════════
    //  VOICE AGENT — Speech-to-Text & Text-to-Speech
    //  100% browser-native APIs. No external services.
    // ══════════════════════════════════════════

    var voiceAgent = {
        recognition: null,
        synth: window.speechSynthesis || null,
        voices: [],
        selectedVoice: null,
        isListening: false,
        isSpeaking: false,
        autoSpeak: false,

        init: function () {
            this.initRecognition();
            this.initSynthesis();
            this.bindVoiceEvents();
        },

        initRecognition: function () {
            var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                var btn = document.getElementById('voiceBtn');
                if (btn) btn.title = 'Voice not supported in this browser';
                return;
            }
            var rec = new SpeechRecognition();
            rec.continuous = false;
            rec.interimResults = true;
            rec.lang = 'en-US';
            rec.maxAlternatives = 1;

            var self = this;

            rec.onstart = function () {
                self.isListening = true;
                var btn = document.getElementById('voiceBtn');
                if (btn) btn.classList.add('listening');
                els.input.placeholder = 'Listening... speak now';
            };

            rec.onresult = function (e) {
                var transcript = '';
                for (var i = e.resultIndex; i < e.results.length; i++) {
                    transcript += e.results[i][0].transcript;
                }
                els.input.value = transcript;
                resize();
                els.sendBtn.disabled = !transcript.trim();

                if (e.results[e.resultIndex].isFinal) {
                    self.stopListening();
                    if (transcript.trim()) {
                        setTimeout(function () { send(); }, 300);
                    }
                }
            };

            rec.onerror = function (e) {
                self.isListening = false;
                var btn = document.getElementById('voiceBtn');
                if (btn) btn.classList.remove('listening');
                els.input.placeholder = 'Message NAGRO...';
                if (e.error === 'not-allowed') {
                    els.input.placeholder = 'Mic access denied — check browser permissions';
                    setTimeout(function () { els.input.placeholder = 'Message NAGRO...'; }, 3000);
                }
            };

            rec.onend = function () {
                self.isListening = false;
                var btn = document.getElementById('voiceBtn');
                if (btn) btn.classList.remove('listening');
                els.input.placeholder = 'Message NAGRO...';
            };

            this.recognition = rec;
        },

        initSynthesis: function () {
            if (!this.synth) return;
            var self = this;

            function loadVoices() {
                self.voices = self.synth.getVoices();
                var select = document.getElementById('voiceSelect');
                if (!select || self.voices.length === 0) return;

                select.innerHTML = '';

                var categories = {
                    'Female': [],
                    'Male': [],
                    'Other': []
                };

                self.voices.forEach(function (v, i) {
                    var name = v.name.toLowerCase();
                    if (name.includes('female') || name.includes('zira') || name.includes('hazel') ||
                        name.includes('susan') || name.includes('heera') || name.includes('samantha') ||
                        name.includes('karen') || name.includes('moira') || name.includes('fiona') ||
                        name.includes('tessa') || name.includes('victoria') || name.includes('veena') ||
                        name.includes('google us english') || name.includes('google uk english female')) {
                        categories['Female'].push({ voice: v, idx: i });
                    } else if (name.includes('male') || name.includes('david') || name.includes('mark') ||
                               name.includes('rishi') || name.includes('daniel') || name.includes('james') ||
                               name.includes('alex') || name.includes('fred') || name.includes('google uk english male')) {
                        categories['Male'].push({ voice: v, idx: i });
                    } else {
                        categories['Other'].push({ voice: v, idx: i });
                    }
                });

                for (var cat in categories) {
                    if (categories[cat].length === 0) continue;
                    var group = document.createElement('optgroup');
                    group.label = cat + ' Voices';
                    categories[cat].forEach(function (item) {
                        var opt = document.createElement('option');
                        opt.value = item.idx;
                        var lang = item.voice.lang || '';
                        opt.textContent = item.voice.name + (lang ? ' (' + lang + ')' : '');
                        if (item.voice.default) opt.selected = true;
                        group.appendChild(opt);
                    });
                    select.appendChild(group);
                }

                var saved = null;
                try { saved = localStorage.getItem('nagro_voice'); } catch (e) {}
                if (saved !== null && self.voices[parseInt(saved)]) {
                    select.value = saved;
                    self.selectedVoice = self.voices[parseInt(saved)];
                } else if (self.voices.length > 0) {
                    self.selectedVoice = self.voices[0];
                }

                var savedAuto = null;
                try { savedAuto = localStorage.getItem('nagro_autospeak'); } catch (e) {}
                if (savedAuto === 'true') {
                    self.autoSpeak = true;
                    var cb = document.getElementById('autoSpeak');
                    if (cb) cb.checked = true;
                }
            }

            loadVoices();
            if (this.synth.onvoiceschanged !== undefined) {
                this.synth.onvoiceschanged = loadVoices;
            }
        },

        bindVoiceEvents: function () {
            var self = this;

            var voiceBtn = document.getElementById('voiceBtn');
            if (voiceBtn) {
                voiceBtn.addEventListener('click', function () {
                    if (self.isListening) {
                        self.stopListening();
                    } else {
                        self.startListening();
                    }
                });
            }

            var voiceSelect = document.getElementById('voiceSelect');
            if (voiceSelect) {
                voiceSelect.addEventListener('change', function () {
                    var idx = parseInt(this.value);
                    if (self.voices[idx]) {
                        self.selectedVoice = self.voices[idx];
                        try { localStorage.setItem('nagro_voice', idx); } catch (e) {}
                        self.speak('Voice changed to ' + self.voices[idx].name);
                    }
                });
            }

            var autoSpeakCb = document.getElementById('autoSpeak');
            if (autoSpeakCb) {
                autoSpeakCb.addEventListener('change', function () {
                    self.autoSpeak = this.checked;
                    try { localStorage.setItem('nagro_autospeak', this.checked); } catch (e) {}
                });
            }

            var stopBtn = document.getElementById('voiceStopBtn');
            if (stopBtn) {
                stopBtn.addEventListener('click', function () {
                    self.stopSpeaking();
                });
            }
        },

        startListening: function () {
            if (!this.recognition) return;
            if (this.isSpeaking) this.stopSpeaking();
            try {
                this.recognition.start();
            } catch (e) {
                this.recognition.stop();
                var self = this;
                setTimeout(function () { self.recognition.start(); }, 100);
            }
        },

        stopListening: function () {
            if (!this.recognition) return;
            try { this.recognition.stop(); } catch (e) {}
            this.isListening = false;
            var btn = document.getElementById('voiceBtn');
            if (btn) btn.classList.remove('listening');
        },

        speak: function (text) {
            if (!this.synth) return;
            this.stopSpeaking();

            var clean = text
                .replace(/```[\s\S]*?```/g, ' code block ')
                .replace(/`[^`]+`/g, function (m) { return m.slice(1, -1); })
                .replace(/\*\*([^*]+)\*\*/g, '$1')
                .replace(/\*([^*]+)\*/g, '$1')
                .replace(/#{1,6}\s*/g, '')
                .replace(/[-*]\s+/g, '')
                .replace(/\d+\.\s+/g, '')
                .replace(/\|[^\n]+\|/g, '')
                .replace(/---+/g, '')
                .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
                .replace(/[<>]/g, '')
                .replace(/\n{2,}/g, '. ')
                .replace(/\n/g, ' ')
                .trim();

            if (!clean) return;

            if (clean.length > 500) {
                clean = clean.substring(0, 500) + '... I will stop reading here for brevity.';
            }

            var utterance = new SpeechSynthesisUtterance(clean);
            if (this.selectedVoice) utterance.voice = this.selectedVoice;
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;

            var self = this;
            var stopBtn = document.getElementById('voiceStopBtn');

            utterance.onstart = function () {
                self.isSpeaking = true;
                if (stopBtn) stopBtn.classList.remove('hidden');
            };
            utterance.onend = function () {
                self.isSpeaking = false;
                if (stopBtn) stopBtn.classList.add('hidden');
            };
            utterance.onerror = function () {
                self.isSpeaking = false;
                if (stopBtn) stopBtn.classList.add('hidden');
            };

            this.synth.speak(utterance);
        },

        stopSpeaking: function () {
            if (!this.synth) return;
            this.synth.cancel();
            this.isSpeaking = false;
            var stopBtn = document.getElementById('voiceStopBtn');
            if (stopBtn) stopBtn.classList.add('hidden');
        },

        onResponse: function (text) {
            if (this.autoSpeak && text) {
                this.speak(text);
            }
        }
    };

    var _origFinishStreamingMsg = finishStreamingMsg;
    finishStreamingMsg = function (div, content) {
        _origFinishStreamingMsg(div, content);

        var speakBtn = document.createElement('button');
        speakBtn.className = 'msg-action-btn speak-btn';
        speakBtn.title = 'Read aloud';
        speakBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M11 5L6 9H2v6h4l5 4V5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M19.07 4.93a10 10 0 010 14.14M15.54 8.46a5 5 0 010 7.07" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Speak';
        speakBtn.addEventListener('click', function () {
            if (voiceAgent.isSpeaking) {
                voiceAgent.stopSpeaking();
                speakBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M11 5L6 9H2v6h4l5 4V5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M19.07 4.93a10 10 0 010 14.14M15.54 8.46a5 5 0 010 7.07" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Speak';
            } else {
                voiceAgent.speak(content);
                speakBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><rect x="4" y="4" width="16" height="16" rx="2" fill="currentColor"/></svg> Stop';
                var synth = window.speechSynthesis;
                if (synth) {
                    var check = setInterval(function () {
                        if (!synth.speaking) {
                            clearInterval(check);
                            speakBtn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none"><path d="M11 5L6 9H2v6h4l5 4V5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M19.07 4.93a10 10 0 010 14.14M15.54 8.46a5 5 0 010 7.07" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Speak';
                        }
                    }, 500);
                }
            }
        });

        var actions = div.querySelector('.msg-actions');
        if (actions) actions.appendChild(speakBtn);

        voiceAgent.onResponse(content);
    };

    var _origInit = init;
    init = function () {
        _origInit();
        voiceAgent.init();
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
