(() => {
    function detectPlatform() {
        const platform = (navigator.userAgentData?.platform || navigator.platform || navigator.userAgent).toLowerCase();
        if (platform.includes('mac')) return 'macos';
        if (platform.includes('win')) return 'windows';
        return 'linux';
    }

    function init() {
        const panes = [...document.querySelectorAll('.wizard-pane')];
        const steps = [...document.querySelectorAll('.wizard-step-node')];
        const connectors = [...document.querySelectorAll('.wizard-connector')];
        const previous = document.getElementById('wizard-prev-btn');
        const next = document.getElementById('wizard-next-btn');
        const counter = document.getElementById('wizard-step-counter');
        const download = document.getElementById('wizard-step-download-btn');
        const detectedOs = document.getElementById('wizard-detected-os');
        const platform = detectPlatform();
        let activeStep = 1;

        if (detectedOs) detectedOs.textContent = platform.toUpperCase();

        function showStep(step) {
            activeStep = Math.max(1, Math.min(panes.length, step));
            panes.forEach((pane, index) => pane.classList.toggle('active', index + 1 === activeStep));
            steps.forEach((button, index) => {
                button.classList.toggle('active', index + 1 === activeStep);
                button.setAttribute('aria-selected', String(index + 1 === activeStep));
            });
            connectors.forEach((connector, index) => connector.classList.toggle('active', index + 1 < activeStep));
            if (previous) previous.disabled = activeStep === 1;
            if (next) {
                next.disabled = activeStep === panes.length;
                next.textContent = activeStep === panes.length ? 'COMPLETE' : 'NEXT STEP →';
            }
            if (counter) counter.textContent = `STEP ${activeStep} / ${panes.length}`;
        }

        previous?.addEventListener('click', () => showStep(activeStep - 1));
        next?.addEventListener('click', () => showStep(activeStep + 1));
        steps.forEach((button, index) => button.addEventListener('click', () => showStep(index + 1)));
        download?.addEventListener('click', () => {
            window.location.assign('/api/download/mark-lv');
        });

        document.getElementById('header-download-btn')?.addEventListener('click', () => {
            window.location.assign('/api/download/mark-lv');
        });

        document.getElementById('tts-toggle-btn')?.addEventListener('click', () => {
            const enabled = window.JARVIS_SPEECH?.setEnabled;
            if (!enabled) return;
            const button = document.getElementById('tts-toggle-btn');
            const isEnabled = button.dataset.enabled !== 'false';
            button.dataset.enabled = String(!isEnabled);
            enabled(!isEnabled);
            const label = document.getElementById('tts-toggle-text');
            if (label) label.textContent = isEnabled ? 'VOICE OFF' : 'VOICE ON';
        });

        showStep(1);
    }

    window.JarvisInstaller = { init };
})();