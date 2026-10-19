(() => {
    let recognition = null;
    let transcriptHandler = null;
    let voiceEnabled = true;

    function setStatus(message) {
        const status = document.getElementById('hud-status-caption');
        if (status) status.textContent = message;
    }

    function init() {
        const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!Recognition) return;

        recognition = new Recognition();
        recognition.lang = navigator.language || 'en-US';
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.onresult = event => {
            const transcript = event.results[0]?.[0]?.transcript?.trim();
            if (transcript && transcriptHandler) transcriptHandler(transcript);
        };
        recognition.onerror = event => setStatus(`VOICE INPUT: ${event.error.toUpperCase()}`);
        recognition.onend = () => setStatus('SYSTEM ONLINE — LISTENING FOR INPUT');

        const voiceButton = document.getElementById('voice-input-btn');
        if (voiceButton) voiceButton.title = 'Click to speak';
    }

    function speak(text) {
        if (!voiceEnabled || !window.speechSynthesis || !text) return;
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = navigator.language || 'en-US';
        window.speechSynthesis.speak(utterance);
    }

    function toggleListening(onTranscript) {
        if (!recognition) init();
        if (!recognition) {
            setStatus('VOICE INPUT UNAVAILABLE IN THIS BROWSER');
            return;
        }
        transcriptHandler = onTranscript;
        setStatus('VOICE INPUT ACTIVE');
        try {
            recognition.start();
        } catch (error) {
            setStatus('VOICE INPUT IS ALREADY ACTIVE');
        }
    }

    function setEnabled(enabled) {
        voiceEnabled = enabled;
        if (!enabled && window.speechSynthesis) window.speechSynthesis.cancel();
    }

    window.JARVIS_SPEECH = { speak, toggleListening, setEnabled };
    window.JarvisSpeech = { init };
})();