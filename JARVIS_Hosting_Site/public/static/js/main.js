document.addEventListener('DOMContentLoaded', () => {
    // === Initialization ===
    initializeCoreComponents();
    initializeNavigation();
    initializeThemeToggle();
    initializeModals();
    initializeSystemStatus();
});

/**
 * Initialize other JS modules based on available global objects
 */
function initializeCoreComponents() {
    // Speech Recognition & Synthesis (from speech.js)
    if (typeof JarvisSpeech !== 'undefined') {
        JarvisSpeech.init();
    }

    // Assistant Interaction (from assistant.js)
    if (typeof JarvisAssistant !== 'undefined') {
        JarvisAssistant.init();
    }

    // Installer Wizard (from installer.js)
    if (typeof JarvisInstaller !== 'undefined') {
        JarvisInstaller.init();
    }
}

/**
 * Handle smooth scrolling and active navigation states
 */
function initializeNavigation() {
    const navBar = document.getElementById('primary-nav');
    if (!navBar) return;

    const navLinks = navBar.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Close mobile menu if open
                if (navBar.classList.contains('active')) {
                    navBar.classList.remove('active');
                }
            }
        });
    });

    // Mobile menu toggle (if present)
    const navToggle = document.getElementById('nav-toggle');
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navBar.classList.toggle('active');
        });
    }
}

/**
 * Manage Theme Switching (Light/Dark/Futuristic)
 */
function initializeThemeToggle() {
    const themeBtn = document.getElementById('theme-toggle');
    if (!themeBtn) return;

    const currentTheme = localStorage.getItem('jarvis-theme') || 'futuristic';
    document.documentElement.setAttribute('data-theme', currentTheme);

    themeBtn.addEventListener('click', () => {
        const activeTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = activeTheme === 'futuristic' ? 'light' : 'futuristic';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('jarvis-theme', newTheme);
        
        // Update toggle icon state if necessary
        const icon = themeBtn.querySelector('.theme-icon');
        if (icon) {
            icon.textContent = newTheme === 'futuristic' ? 'light_mode' : 'dark_mode';
        }
    });
}

/**
 * Generic Modal Dialog Logic
 */
function initializeModals() {
    const modal = document.getElementById('download-confirm-modal');
    if (!modal) return;

    const closeModal = () => {
        modal.classList.remove('active');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    };

    document.querySelectorAll('.download-trigger-btn').forEach(button => {
        button.addEventListener('click', () => {
            const platform = button.dataset.os || 'windows';
            const platformName = platform.charAt(0).toUpperCase() + platform.slice(1);
            const target = document.getElementById('modal-os-name');
            if (target) target.textContent = `Target: ${platformName}`;
            modal.classList.add('active');
            modal.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
        });
    });

    modal.querySelectorAll('.modal-close-btn, #modal-ack-btn').forEach(button => {
        button.addEventListener('click', closeModal);
    });

    modal.addEventListener('click', event => {
        if (event.target === modal) closeModal();
    });

    // Escape key closing
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.modal-backdrop.active');
            if (activeModal) {
                activeModal.classList.remove('active');
                activeModal.setAttribute('aria-hidden', 'true');
                document.body.style.overflow = '';
            }
        }
    });
}

/**
 * Simulates updating system status telemetry on the dashboard
 */
function initializeSystemStatus() {
    const latencyEl = document.getElementById('sys-latency');
    const bandwidthEl = document.getElementById('sys-bandwidth');
    const statusDotEl = document.querySelector('.status-dot');

    if (!latencyEl || !bandwidthEl) return;

    function updateMetrics() {
        const simulatedLatency = (Math.random() * (45 - 20) + 20).toFixed(0);
        const simulatedBandwidth = (Math.random() * (100 - 90) + 90).toFixed(1);

        latencyEl.textContent = `${simulatedLatency} ms`;
        bandwidthEl.textContent = `${simulatedBandwidth} Mbps`;

        if (statusDotEl) {
            statusDotEl.style.backgroundColor = simulatedLatency > 40 ? '#ff3e3e' : '#00ffff';
        }
    }

    // Update every 5 seconds
    updateMetrics();
    setInterval(updateMetrics, 5000);
}

/**
 * Utility: Debounce function for resizing or scroll events
 */
function debounce(func, wait = 10, immediate = true) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}