document.addEventListener('DOMContentLoaded', () => {
    const assistantHost = document.getElementById('online-host');
    if (!assistantHost) return;

    const chatLog = document.getElementById('dialogue-scroll-box');
    const assistantForm = document.getElementById('assistant-form');
    const commandInput = document.getElementById('assistant-query-input');
    const sendBtn = document.getElementById('assistant-submit-btn');
    const micBtn = document.getElementById('voice-input-btn');
    const clearChatBtn = document.getElementById('clear-feed-btn');
    const quickPromptBtns = document.querySelectorAll('.chip-btn[data-query]');

    const diagCpu = document.getElementById('telem-cpu-val');
    const diagRam = document.getElementById('telem-mem-val');
    const diagPing = document.getElementById('telem-latency-val');
    const coreStatus = document.querySelector('#global-status-pill .status-label');

    const audioVisualizer = document.getElementById('audio-visualizer');
    let canvasCtx, analyser, dataArray, bufferLength;
    let isVisualizerActive = false;
    let telemetryInterval = null;

    function init() {
        setupEventListeners();
        initAudioVisualizer();
        startTelemetrySimulation();
    }

    function setupEventListeners() {
        if (assistantForm && commandInput) {
            assistantForm.addEventListener('submit', (event) => {
                event.preventDefault();
                handleUserSubmit();
            });
        } else if (sendBtn && commandInput) {
            sendBtn.addEventListener('click', handleUserSubmit);
        }

        if (micBtn) {
            micBtn.addEventListener('click', toggleVoiceInput);
        }

        if (clearChatBtn) {
            clearChatBtn.addEventListener('click', () => {
                if (chatLog) {
                    chatLog.innerHTML = '';
                    appendMessage('system', 'Chat log cleared.');
                }
            });
        }

        quickPromptBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const promptText = btn.getAttribute('data-query') || btn.textContent.trim();
                if (commandInput) {
                    commandInput.value = promptText;
                    handleUserSubmit();
                }
            });
        });

        window.addEventListener('resize', resizeVisualizerCanvas);
    }

    function handleUserSubmit() {
        if (!commandInput) return;
        const text = commandInput.value.trim();
        if (!text) return;

        appendMessage('user', text);
        commandInput.value = '';
        processCommand(text);
    }

    function appendMessage(sender, text) {
        if (!chatLog) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = `dialogue-message ${sender}`;

        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

        let senderLabel = 'JARVIS';
        if (sender === 'user') senderLabel = 'USER';
        if (sender === 'system') senderLabel = 'SYSTEM';

        msgDiv.innerHTML = `
            <div class="msg-avatar">${sender === 'user' ? 'U' : 'J'}</div>
            <div class="msg-body">
                <div class="msg-header">
                    <span class="msg-speaker">${senderLabel}</span>
                    <span class="msg-time">${timestamp}</span>
                </div>
                <div class="msg-content">${escapeHtml(text)}</div>
            </div>`;

        chatLog.appendChild(msgDiv);
        chatLog.scrollTop = chatLog.scrollHeight;

        if (sender === 'assistant' && window.JARVIS_SPEECH) {
            window.JARVIS_SPEECH.speak(text);
        }
    }

    function escapeHtml(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function processCommand(text) {
        showTypingIndicator(true);

        fetch('/api/assistant/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: text })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            showTypingIndicator(false);
            const reply = data.response || "I have processed your request, sir.";
            appendMessage('assistant', reply);
            updateDiagnosticsFromResponse(data);
        })
        .catch(error => {
            showTypingIndicator(false);
            console.error('API Error:', error);
            // Fallback simulation if backend endpoint is unavailable
            const fallbackReply = simulateOfflineResponse(text);
            appendMessage('assistant', fallbackReply);
        });
    }

    function simulateOfflineResponse(text) {
        const lower = text.toLowerCase();
        if (lower.includes('status') || lower.includes('diagnostic')) {
            return 'All core systems operating at 98.4% efficiency. Subroutines stable.';
        } else if (lower.includes('hello') || lower.includes('hi')) {
            return 'Greetings, Principal. Voice interface online and awaiting directives.';
        } else if (lower.includes('weather')) {
            return 'Atmospheric sensors indicate optimal conditions. Clear skies and stable barometric pressure.';
        } else if (lower.includes('local') || lower.includes('download')) {
            return 'You can download the full standalone local version via the Download Center below for enhanced privileges.';
        } else {
            return `Command "${text}" received and logged into primary memory banks. Simulating execution routine.`;
        }
    }

    let typingElement = null;
    function showTypingIndicator(show) {
        if (!chatLog) return;
        if (show) {
            if (typingElement) return;
            typingElement = document.createElement('div');
            typingElement.className = 'chat-message assistant-message typing-indicator-msg';
            typingElement.innerHTML = `
                <div class="message-header"><span class="message-sender">JARVIS</span></div>
                <div class="message-body">
                    <span class="typing-dots"><span>.</span><span>.</span><span>.</span></span> Processing
                </div>
            `;
            chatLog.appendChild(typingElement);
            chatLog.scrollTop = chatLog.scrollHeight;
        } else {
            if (typingElement && typingElement.parentNode) {
                typingElement.parentNode.removeChild(typingElement);
            }
            typingElement = null;
        }
    }

    function toggleVoiceInput() {
        if (window.JARVIS_SPEECH) {
            window.JARVIS_SPEECH.toggleListening((transcript) => {
                if (commandInput) {
                    commandInput.value = transcript;
                    handleUserSubmit();
                }
            });
        } else {
            alert('Speech recognition module not loaded.');
        }
    }

    function initAudioVisualizer() {
        if (!audioVisualizer) return;
        canvasCtx = audioVisualizer.getContext('2d');
        resizeVisualizerCanvas();

        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                const audioCtx = new AudioContext();
                analyser = audioCtx.createAnalyser();
                analyser.fftSize = 64;
                bufferLength = analyser.frequencyBinCount;
                dataArray = new Uint8Array(bufferLength);
                isVisualizerActive = true;
                drawVisualizer();
            } else {
                drawFallbackVisualizer();
            }
        } catch (e) {
            console.warn('Web Audio API not supported, using simulated visualizer.', e);
            drawFallbackVisualizer();
        }
    }

    function resizeVisualizerCanvas() {
        if (!audioVisualizer) return;
        audioVisualizer.width = audioVisualizer.parentElement.clientWidth || 300;
        audioVisualizer.height = audioVisualizer.parentElement.clientHeight || 80;
    }

    function drawVisualizer() {
        if (!isVisualizerActive || !canvasCtx || !audioVisualizer) return;
        requestAnimationFrame(drawVisualizer);

        if (analyser && dataArray) {
            analyser.getByteFrequencyData(dataArray);
        } else {
            for (let i = 0; i < bufferLength; i++) {
                dataArray[i] = Math.floor(Math.random() * 180) + 20;
            }
        }

        canvasCtx.clearRect(0, 0, audioVisualizer.width, audioVisualizer.height);

        const barWidth = (audioVisualizer.width / bufferLength) * 2.5;
        let barHeight;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            barHeight = (dataArray[i] / 255) * audioVisualizer.height;

            const gradient = canvasCtx.createLinearGradient(0, audioVisualizer.height, 0, 0);
            gradient.addColorStop(0, '#00d2ff');
            gradient.addColorStop(1, '#ff007f');

            canvasCtx.fillStyle = gradient;
            canvasCtx.fillRect(x, audioVisualizer.height - barHeight, barWidth, barHeight);

            x += barWidth + 1;
        }
    }

    function drawFallbackVisualizer() {
        if (!audioVisualizer || !canvasCtx) return;
        bufferLength = 16;
        dataArray = new Uint8Array(bufferLength);
        isVisualizerActive = true;
        drawVisualizer();
    }

    function startTelemetrySimulation() {
        if (telemetryInterval) clearInterval(telemetryInterval);

        telemetryInterval = setInterval(() => {
            const cpuVal = (Math.random() * 15 + 12).toFixed(1);
            const ramVal = (Math.random() * 2 + 42).toFixed(1);
            const pingVal = Math.floor(Math.random() * 6 + 12);

            if (diagCpu) diagCpu.textContent = `${cpuVal}%`;
            if (diagRam) diagRam.textContent = `${ramVal}%`;
            if (diagPing) diagPing.textContent = `${pingVal} ms`;

            if (coreStatus && Math.random() > 0.95) {
                coreStatus.textContent = 'OPTIMIZED';
                setTimeout(() => {
                    if (coreStatus) coreStatus.textContent = 'ONLINE';
                }, 2000);
            }
        }, 3000);
    }

    function updateDiagnosticsFromResponse(data) {
        const telemetry = data.telemetry || {};
        if (diagCpu && telemetry.cpu_load !== undefined) diagCpu.textContent = `${telemetry.cpu_load}%`;
        if (diagRam && telemetry.memory_usage !== undefined) diagRam.textContent = `${telemetry.memory_usage}%`;
        if (diagPing && telemetry.neural_latency_ms !== undefined) {
            diagPing.textContent = `${telemetry.neural_latency_ms} ms`;
        }
    }

    function exportChatHistory() {
        if (!chatLog) return;
        const messages = chatLog.querySelectorAll('.chat-message');
        let textContent = "JARVIS ASSISTANT CHAT LOG\n=========================\n\n";

        messages.forEach(msg => {
            const sender = msg.querySelector('.message-sender')?.textContent || 'UNKNOWN';
            const time = msg.querySelector('.message-time')?.textContent || '';
            const body = msg.querySelector('.message-body')?.textContent || '';
            textContent += `[${time}] ${sender}: ${body}\n\n`;
        });

        const blob = new Blob([textContent], { type: 'text/plain;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `jarvis_chat_log_${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    init();
});