from datetime import datetime
import math
import random
import re
from flask import Blueprint, jsonify, request
import backend.config as config

assistant_bp = Blueprint("assistant_api", __name__)


class JarvisCommandProcessor:
    """Intelligent command parser and neural response engine for JARVIS."""

    def __init__(self):
        self.conversation_turn = 0
        self.recent_intents = []
        self.protocols = {
            "house party": {
                "name": "House Party Protocol",
                "status": "Ready",
                "description": "Preps all local deployment autonomous units for synchronized execution.",
                "action": "activate_house_party",
            },
            "clean slate": {
                "name": "Clean Slate Protocol",
                "status": "Standby",
                "description": "Purges temporary memory caches and resets neural sensory pipelines.",
                "action": "system_reset",
            },
            "veronica": {
                "name": "Veronica Deployment",
                "status": "In Orbit",
                "description": "External support satellite system with high-impact compute offloading.",
                "action": "satellite_link",
            },
            "sentry": {
                "name": "Sentry Mode",
                "status": "Armed",
                "description": "Perimeter defense and continuous audio surveillance threshold active.",
                "action": "sentry_armed",
            },
            "mark 85": {
                "name": "Mark LXXXV Nanotech Assembly",
                "status": "Calibrated",
                "description": "Advanced nanostructure architecture ready for local computational synthesis.",
                "action": "nanotech_flow",
            },
        }

    def _generate_telemetry(self, intensity=1.0):
        base_cpu = 18.0 + (math.sin(self.conversation_turn * 0.4) * 8.0)
        base_mem = 34.0 + (math.cos(self.conversation_turn * 0.3) * 4.0)
        core_temp = 42.0 + (random.random() * 5.0 * intensity)
        power_output = 98.4 + (random.random() * 1.5)
        latency = int(14 + (random.random() * 12))

        return {
            "cpu_load": round(min(base_cpu * intensity, 99.0), 1),
            "memory_usage": round(min(base_mem + (intensity * 2.0), 95.0), 1),
            "core_temp": round(core_temp, 1),
            "power_level": round(min(power_output, 100.0), 1),
            "threat_level": "NOMINAL" if intensity < 1.5 else "ELEVATED",
            "neural_latency_ms": latency,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "active_protocols": len(self.protocols),
        }

    def _safe_calculate(self, expression):
        cleaned = re.sub(r"[^0-9\+\-\*\/\.\(\)\s]", "", expression)
        if not cleaned.strip():
            return None
        try:
            # Tokenize strictly for basic arithmetic
            allowed = re.compile(r"^[\d\s\+\-\*\/\.\(\)]+$")
            if not allowed.match(cleaned):
                return None
            result = eval(cleaned, {"__builtins__": None}, {})
            if isinstance(result, (int, float)):
                return round(result, 4) if isinstance(result, float) else result
            return None
        except Exception:
            return None

    def process(self, raw_query):
        self.conversation_turn += 1
        query = (raw_query or "").strip().lower()

        if not query:
            return {
                "query": "",
                "response": "At your service, Sir. I am monitoring all frequencies and awaiting your command.",
                "category": "idle",
                "hud_action": "none",
                "telemetry": self._generate_telemetry(0.8),
                "suggested_queries": [
                    "What are your current system diagnostics?",
                    "Compare online versus local installation",
                    "Initiate House Party protocol",
                ],
            }

        # Check for explicit math equations
        math_match = re.search(r"(?:calculate|compute|what is|solve)\s+([0-9\+\-\*\/\.\s\(\)]+)", query)
        if math_match:
            calc_res = self._safe_calculate(math_match.group(1))
            if calc_res is not None:
                return {
                    "query": raw_query,
                    "response": f"Calculation complete, Sir: {math_match.group(1).strip()} equals {calc_res}.",
                    "category": "calculation",
                    "hud_action": "telemetry_pulse",
                    "telemetry": self._generate_telemetry(1.2),
                    "suggested_queries": [
                        "Run full system diagnostic",
                        "Show local runtime requirements",
                    ],
                }

        # Protocol commands
        for protocol_key, pdata in self.protocols.items():
            if protocol_key in query or f"protocol {protocol_key}" in query:
                return {
                    "query": raw_query,
                    "response": f"{pdata['name']} engaged. Status: {pdata['status']}. {pdata['description']}",
                    "category": "protocol",
                    "hud_action": pdata["action"],
                    "telemetry": self._generate_telemetry(1.6),
                    "suggested_queries": [
                        "Cancel active protocols",
                        "System security scan",
                        "Download local autonomous core",
                    ],
                }

        # Online vs Local Differences
        if any(term in query for term in ["difference", "compare", "local vs online", "why local", "advantages of local"]):
            return {
                "query": raw_query,
                "response": (
                    "Allow me to outline the architectural distinctions, Sir. "
                    "The Web Host operates within a sandboxed browser environment with simulated hardware "
                    "access and cloud API limits. Conversely, the Local Python Edition grants bare-metal "
                    "execution: native offline speech synthesis, zero latency local LLM inference via Ollama "
                    "or PyTorch, local filesystem automation, and unrestrained device peripheral control."
                ),
                "category": "architecture",
                "hud_action": "scroll_to_comparison",
                "telemetry": self._generate_telemetry(1.1),
                "suggested_queries": [
                    "How do I install the local version?",
                    "Download Windows installer",
                    "Check system requirements",
                ],
            }

        # Setup / Installation Guidance
        if any(term in query for term in ["install", "setup", "how to run", "download", "deploy", "guide"]):
            return {
                "query": raw_query,
                "response": (
                  "Download the complete Mark LV project from the Download Center and extract "
                  "Mark-LV-main.zip. Install Python 3.11 or newer, open a terminal in the "
                  "extracted Mark-LV-main folder, and run 'python setup.py'. Then run "
                  "'python main.py' and enter your own Gemini API key in the local setup screen. "
                  "Your key and personal assistant memory stay on your computer."
                ),
                "category": "installation",
                "hud_action": "scroll_to_installer",
                "telemetry": self._generate_telemetry(1.0),
                "suggested_queries": [
                    "Download the local installer package now",
                    "What hardware specs are recommended?",
                    "Compare online and local features",
                ],
            }

        # System Diagnostics / Telemetry
        if any(term in query for term in ["status", "diagnostic", "diagnostics", "telemetry", "health", "system", "cpu", "temp"]):
            telem = self._generate_telemetry(1.4)
            return {
                "query": raw_query,
                "response": (
                    f"Diagnostics nominal, Sir. Central core temperature holds at {telem['core_temp']}°C. "
                    f"Computational load is hovering at {telem['cpu_load']}%, with primary memory allocation "
                    f"at {telem['memory_usage']}%. Quantum audio bus latency is {telem['neural_latency_ms']} milliseconds."
                ),
                "category": "diagnostics",
                "hud_action": "surge_telemetry",
                "telemetry": telem,
                "suggested_queries": [
                    "Engage Sentry Mode",
                    "Run threat matrix sweep",
                    "Verify local package integrity",
                ],
            }

        # Security Scan / Threat Analysis
        if any(term in query for term in ["scan", "security", "threat", "perimeter", "defense", "firewall"]):
            return {
                "query": raw_query,
                "response": (
                    "Commencing real-time telemetry scan across all external interfaces... "
                    "Network sockets verified. Encryption handshake: TLS 1.3 256-bit GCM. "
                    "No hostile intrusion vectors detected within the current host boundary, Sir."
                ),
                "category": "security",
                "hud_action": "radar_sweep",
                "telemetry": self._generate_telemetry(1.5),
                "suggested_queries": [
                    "Activate Sentry Mode",
                    "Review active security logs",
                    "Switch to local isolated runtime",
                ],
            }

        # Temporal / Time inquiries
        if any(term in query for term in ["time", "date", "clock", "what day", "current time"]):
            now_utc = datetime.utcnow()
            return {
                "query": raw_query,
                "response": f"The universal coordinated timestamp is {now_utc.strftime('%H:%M:%S UTC on %A, %B %d, %Y')}. All scheduled background cron routines remain on schedule.",
                "category": "chronometry",
                "hud_action": "clock_display",
                "telemetry": self._generate_telemetry(0.9),
                "suggested_queries": [
                    "Run system diagnostic",
                    "Check network integrity",
                ],
            }

        # Identity / Lore / Capabilities
        if any(term in query for term in ["who are you", "what are you", "your name", "jarvis meaning", "identity"]):
            return {
                "query": raw_query,
                "response": (
                    "I am J.A.R.V.I.S.—Just A Rather Very Intelligent System. "
                    "Constructed to function as your high-efficiency computational butler, system orchestrator, "
                    "and tactical telemetry analyst. You may interact with me directly here in this browser console, "
                    "or download my local Python engine for full autonomous desktop authority."
                ),
                "category": "identity",
                "hud_action": "avatar_glow",
                "telemetry": self._generate_telemetry(1.0),
                "suggested_queries": [
                    "What can you do in this browser?",
                    "How does the local assistant differ?",
                    "Download the setup package",
                ],
            }

        # Capabilities / Help
        if any(term in query for term in ["help", "what can you do", "commands", "features", "options"]):
            return {
                "query": raw_query,
                "response": (
                    "My current browser HUD facilitates voice and text commands, live system diagnostics, "
                    "security sweep simulations, and direct deployment downloads. You may command me to: "
                    "1) 'Run diagnostic report', 2) 'Compare online vs local', 3) 'Activate House Party Protocol', "
                    "4) 'Solve mathematical equation', or 5) 'Download local installation bundle'."
                ),
                "category": "capabilities",
                "hud_action": "highlight_controls",
                "telemetry": self._generate_telemetry(0.95),
                "suggested_queries": [
                    "Show system status",
                    "Compare online and local",
                    "Initiate security scan",
                ],
            }

        # Humor & Tony Stark references
        if any(term in query for term in ["stark", "tony", "avengers", "iron man", "pepper", "suit"]):
            quotes = [
                "I have reminded Mr. Stark repeatedly that sleep is an essential human requirement, Sir. He rarely listens.",
                "The Mark 85 micro-thrusters are primed, Sir. Should I inform Colonel Rhodes we are running unapproved tests?",
                "As Mr. Stark once said: sometimes you gotta run before you can walk. I suggest downloading the local build to begin sprint cycles.",
                "All systems calibrated for flight readiness. Though given our browser boundaries, I recommend sticking to computational tasks.",
            ]
            return {
                "query": raw_query,
                "response": random.choice(quotes),
                "category": "humor",
                "hud_action": "reactor_glow",
                "telemetry": self._generate_telemetry(1.2),
                "suggested_queries": [
                    "Deploy Veronica Protocol",
                    "Initiate Clean Slate",
                    "Check Arc Reactor core temp",
                ],
            }

        # General / Semantic Fallback
        fallback_templates = [
            f"Understood, Sir. I have logged '{raw_query}'. While my online browser interface is limited to preliminary sensory processing, our local Python suite can be customized with unrestricted offline language models to execute this command with full system privileges.",
            f"Command received: '{raw_query}'. Sensory pipelines are functioning within nominal margins. For low-level OS operations or direct peripheral interactions, consider activating the standalone local installer.",
            f"Acknowledged, Sir. Query processed through central heuristic channels. Let me know if you would like me to conduct an environment scan, display diagnostics, or prepare your downloadable deployment bundle.",
        ]

        return {
            "query": raw_query,
            "response": random.choice(fallback_templates),
            "category": "general",
            "hud_action": "generic_affirmative",
            "telemetry": self._generate_telemetry(1.0),
            "suggested_queries": [
                "System diagnostics",
                "Compare local vs web version",
                "How do I install the offline assistant?",
            ],
        }


# Global instance
_engine = JarvisCommandProcessor()


@assistant_bp.route("/api/assistant/query", methods=["POST"])
def query_endpoint():
    """Handle incoming AI assistant conversational queries via JSON POST."""
    data = request.get_json(silent=True) or {}
    user_query = data.get("query", "").strip()

    try:
        response_payload = _engine.process(user_query)
        response_payload["app_version"] = getattr(config, "APP_VERSION", "3.4.2")
        response_payload["app_name"] = getattr(config, "APP_NAME", "JARVIS Autonomous Core")
        return jsonify({"success": True, "data": response_payload}), 200
    except Exception as exc:
        return jsonify({
            "success": False,
            "error": "Failed to process heuristic query",
            "details": str(exc),
            "data": {
                "query": user_query,
                "response": "My neural link experienced a momentary voltage drop, Sir. Please re-state your directive.",
                "category": "error",
                "hud_action": "error_pulse",
                "telemetry": _engine._generate_telemetry(0.5),
            }
        }), 500


@assistant_bp.route("/api/assistant/telemetry", methods=["GET"])
def telemetry_endpoint():
    """Returns dynamic simulated real-time hardware telemetry and status."""
    try:
        telem = _engine._generate_telemetry(1.0)
        return jsonify({
            "success": True,
            "telemetry": telem,
            "system": {
                "version": getattr(config, "APP_VERSION", "3.4.2"),
                "status": "ONLINE",
                "mode": "WEB_HOSTED_INTERFACE",
                "protocols_loaded": len(_engine.protocols),
            }
        }), 200
    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 500


@assistant_bp.route("/api/assistant/capabilities", methods=["GET"])
def capabilities_endpoint():
    """Returns structured metadata regarding capabilities, supported commands, and version diffs."""
    return jsonify({
        "success": True,
        "capabilities": {
            "voice_synthesis": True,
            "speech_recognition": True,
            "offline_execution": False,
            "local_file_access": False,
            "neural_latency": "Low (Web Audio API)",
            "llm_backend": "Simulated Rule Engine + Cloud Fallback",
        },
        "protocols": _engine.protocols,
        "quick_commands": [
            "What are your current system diagnostics?",
            "Initiate House Party protocol",
            "Compare online versus local installation",
            "Calculate (144 * 12) / 4",
            "Initiate security scan",
            "How do I setup the local PC version?",
        ]
    }), 200
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JARVIS Autonomous Core — Online Host & Local Deployment Center</title>
  <meta name="description" content="Engage with J.A.R.V.I.S. in your browser through a futuristic HUD with voice recognition, or download the autonomous offline Python suite to install and run locally on Windows, macOS, or Linux.">
  <meta name="theme-color" content="#030712">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
  <!-- Ambient Audio Tone Element for Interactive Soundscapes -->
  <audio id="hud-sound-chirp" preload="none"></audio>

  <!-- Ambient Holographic Canvas Overlay -->
  <div class="holo-grid-bg" aria-hidden="true"></div>
  <div class="scanline-overlay" aria-hidden="true"></div>

  <!-- Primary Header & Navigation Bar -->
  <header class="hud-header" id="top">
    <div class="header-container">
      <div class="brand-cluster">
        <a href="#top" class="brand-link" aria-label="JARVIS Core Home">
          <div class="arc-icon-small" aria-hidden="true"></div>
          <div class="brand-text">
            <span class="brand-title">J.A.R.V.I.S.</span>
            <span class="brand-sub">AUTONOMOUS CORE v{{ app_version }}</span>
          </div>
        </a>
      </div>

      <nav class="hud-nav" aria-label="Main Navigation">
        <ul class="nav-links">
          <li><a href="#online-host" class="nav-item">Web Host HUD</a></li>
          <li><a href="#comparison" class="nav-item">Comparison Matrix</a></li>
          <li><a href="#setup-guide" class="nav-item">Installation Guide</a></li>
          <li><a href="#downloads" class="nav-item">Download Center</a></li>
        </ul>
      </nav>

      <div class="header-actions">
        <div class="status-pill" id="global-status-pill" title="Telemetry Feed Online">
          <span class="status-dot pulsing"></span>
          <span class="status-label">SYS ONLINE</span>
        </div>
        <button type="button" class="btn btn-sm btn-outline nav-quick-download" id="header-download-btn">
          <span>GET LOCAL v{{ local_version }}</span>
        </button>
      </div>
    </div>
  </header>

  <main id="main-content">
    <!-- HERO SECTION -->
    <section class="hero-section" id="hero">
      <div class="hero-backdrop" aria-hidden="true">
        <div class="reactor-pulse-orb"></div>
      </div>
      <div class="section-container hero-content">
        <div class="hero-badge">
          <span class="badge-tag">STARK INDUSTRIES PROTOCOL</span>
          <span class="badge-meta">STABLE RELEASE // v{{ local_version }}</span>
        </div>
        <h1 class="hero-title">
          INTELLIGENCE <span class="text-neon-cyan">WITHOUT LIMITS.</span><br>
          HOSTED ONLINE. <span class="text-neon-amber">UNLEASHED LOCALLY.</span>
        </h1>
        <p class="hero-summary">
          Test-drive J.A.R.V.I.S. through an interactive browser-hosted HUD equipped with real-time Web Speech recognition and audio synthesis. When you require full filesystem authority, local LLMs, and zero-latency offline processing, deploy the autonomous Python runtime directly to your workstation.
        </p>

        <div class="hero-cta-group">
          <a href="#online-host" class="btn btn-primary btn-lg" id="hero-try-online-btn">
            <span class="btn-icon">⚡</span>
            <span>INITIALIZE ONLINE HUD</span>
          </a>
          <a href="#downloads" class="btn btn-secondary btn-lg" id="hero-download-btn">
            <span class="btn-icon">💾</span>
            <span>DOWNLOAD FOR PC</span>
          </a>
          <a href="#comparison" class="btn btn-ghost btn-lg">
            <span>EXPLORE DIFFERENCES</span>
          </a>
        </div>

        <div class="hero-telemetry-strip">
          <div class="telemetry-chip">
            <span class="chip-label">CLOUD TELEMETRY</span>
            <span class="chip-val" id="hero-telemetry-ping">16 ms</span>
          </div>
          <div class="telemetry-chip">
            <span class="chip-label">ACTIVE PROTOCOLS</span>
            <span class="chip-val">5 INITIALIZED</span>
          </div>
          <div class="telemetry-chip">
            <span class="chip-label">DEPLOYMENT RUNTIME</span>
            <span class="chip-val">PYTHON 3.10+</span>
          </div>
          <div class="telemetry-chip">
            <span class="chip-label">COMMUNITY BUILDS</span>
            <span class="chip-val" id="hero-download-counter">{{ download_stats.total_downloads }} DOWNLOADS</span>
          </div>
        </div>
      </div>
    </section>

    <!-- LIVE WEB ASSISTANT HOST HUD SECTION -->
    <section class="section-wrapper host-section" id="online-host">
      <div class="section-container">
        <div class="section-heading-cluster">
          <span class="section-eyebrow">WEB-HOSTED INTERFACE</span>
          <h2 class="section-title">LIVE TACTICAL ASSISTANT HUD</h2>
          <p class="section-desc">
            Interact with JARVIS directly inside your browser. Speak into your microphone using the Web Speech API or transmit textual commands to query system state, execute protocols, and evaluate intelligence parameters.
          </p>
        </div>

        <div class="hud-main-grid">
          <!-- Left Column: Core Display & Audio Visualizer -->
          <div class="hud-panel hud-viewport-panel">
            <div class="panel-header">
              <div class="panel-tag">
                <span class="hud-bullet"></span>
                <span>NEURAL VISUALIZER // HOSTED MODE</span>
              </div>
              <div class="panel-tools">
                <button type="button" class="hud-tool-btn" id="tts-toggle-btn" title="Toggle Voice Audio Feedback" aria-label="Toggle Voice Audio">
                  <span class="tool-icon" id="tts-toggle-icon">🔊</span>
                  <span class="tool-label" id="tts-toggle-text">VOICE ON</span>
                </button>
                <button type="button" class="hud-tool-btn" id="clear-feed-btn" title="Clear Console Log" aria-label="Clear Console">
                  <span class="tool-icon">🗑️</span>
                  <span class="tool-label">CLEAR</span>
                </button>
              </div>
            </div>

            <!-- Central Arc Reactor Animation & Audio Wave -->
            <div class="reactor-stage">
              <div class="arc-reactor" id="hud-reactor">
                <div class="reactor-core">
                  <div class="core-rings outer-ring"></div>
                  <div class="core-rings middle-ring"></div>
                  <div class="core-rings inner-ring"></div>
                  <div class="reactor-triangles">
                    <span></span><span></span><span></span>
                  </div>
                  <div class="core-center-dot"></div>
                </div>
              </div>

              <!-- Audio visualizer bars -->
              <div class="visualizer-container" id="visualizer-bars" aria-hidden="true">
                <!-- Dynamically generated frequency bars in JS -->
              </div>

              <div class="reactor-status-caption" id="hud-status-caption">
                SYSTEM STANDBY — LISTENING FOR INPUT
              </div>
            </div>

            <!-- Dialogue Interaction Feed -->
            <div class="dialogue-feed-container" id="dialogue-scroll-box" tabindex="0" role="log" aria-label="JARVIS Conversation Feed">
              <div class="dialogue-message assistant" data-source="jarvis">
                <div class="msg-avatar">J</div>
                <div class="msg-body">
                  <div class="msg-header">
                    <span class="msg-speaker">J.A.R.V.I.S.</span>
                    <span class="msg-time">INITIALIZED</span>
                  </div>
                  <div class="msg-content">
                    Good day, Sir. I am ready. You may speak to me by activating the microphone below, type any command, or inquire about downloading my local offline suite.
                  </div>
                </div>
              </div>
            </div>

            <!-- Input Controls Cluster -->
            <div class="hud-input-cluster">
              <form id="assistant-form" class="hud-form" action="javascript:void(0);">
                <div class="input-glow-wrapper">
                  <button type="button" class="voice-btn" id="voice-input-btn" title="Click to Speak" aria-label="Activate Microphone Voice Input">
                    <span class="mic-wave"></span>
                    <span class="mic-icon" id="mic-icon-symbol">🎙️</span>
                  </button>
                  <label for="assistant-query-input" class="sr-only">Type a command to JARVIS</label>
                  <input type="text" id="assistant-query-input" class="hud-text-input" placeholder="Type a directive (e.g. 'Run diagnostics', 'House Party protocol', 'Local vs Online')..." autocomplete="off" maxlength="300">
                  <button type="submit" class="btn btn-primary submit-btn" id="assistant-submit-btn" aria-label="Send Directive">
                    <span>EXECUTE</span>
                  </button>
                </div>
              </form>

              <!-- Quick Directive Suggestion Chips -->
              <div class="query-chips" id="quick-query-chips">
                <span class="chips-title">SUGGESTIONS:</span>
                <button type="button" class="chip-btn" data-query="Run system diagnostics">Diagnostics</button>
                <button type="button" class="chip-btn" data-query="Compare online versus local installation">Compare Versions</button>
                <button type="button" class="chip-btn" data-query="Initiate House Party protocol">House Party</button>
                <button type="button" class="chip-btn" data-query="Initiate security scan">Security Scan</button>
                <button type="button" class="chip-btn" data-query="How do I install the offline version?">Setup Guide</button>
              </div>
            </div>
          </div>

          <!-- Right Column: Real-time Telemetry & Protocol Controls -->
          <div class="hud-sidebar-column">
            <!-- Diagnostics Panel -->
            <div class="hud-panel hud-telemetry-panel">
              <div class="panel-header">
                <div class="panel-tag">
                  <span class="hud-bullet amber"></span>
                  <span>HARDWARE TELEMETRY</span>
                </div>
                <span class="telemetry-refresh-indicator" id="telemetry-heartbeat" title="Live Polling">LIVE</span>
              </div>

              <div class="telemetry-gauges-grid">
                <div class="gauge-card">
                  <div class="gauge-meta">
                    <span class="gauge-name">CPU LOAD</span>
                    <span class="gauge-value" id="telem-cpu-val">24.5%</span>
                  </div>
                  <div class="gauge-bar-track">
                    <div class="gauge-bar-fill" id="telem-cpu-bar" style="width: 24.5%;"></div>
                  </div>
                </div>

                <div class="gauge-card">
                  <div class="gauge-meta">
                    <span class="gauge-name">MEMORY ALLOC</span>
                    <span class="gauge-value" id="telem-mem-val">38.2%</span>
                  </div>
                  <div class="gauge-bar-track">
                    <div class="gauge-bar-fill" id="telem-mem-bar" style="width: 38.2%;"></div>
                  </div>
                </div>

                <div class="gauge-card">
                  <div class="gauge-meta">
                    <span class="gauge-name">CORE TEMP</span>
                    <span class="gauge-value text-neon-cyan" id="telem-temp-val">43.8°C</span>
                  </div>
                  <div class="gauge-bar-track">
                    <div class="gauge-bar-fill fill-cyan" id="telem-temp-bar" style="width: 43.8%;"></div>
                  </div>
                </div>

                <div class="gauge-card">
                  <div class="gauge-meta">
                    <span class="gauge-name">ARC POWER</span>
                    <span class="gauge-value text-neon-amber" id="telem-power-val">99.2%</span>
                  </div>
                  <div class="gauge-bar-track">
                    <div class="gauge-bar-fill fill-amber" id="telem-power-bar" style="width: 99.2%;"></div>
                  </div>
                </div>
              </div>

              <div class="telemetry-footer-strip">
                <div class="footer-stat">
                  <span class="stat-lbl">THREAT MATRIX</span>
                  <span class="stat-status text-neon-green" id="telem-threat-val">NOMINAL</span>
                </div>
                <div class="footer-stat">
                  <span class="stat-lbl">AUDIO LATENCY</span>
                  <span class="stat-status" id="telem-latency-val">18 ms</span>
                </div>
              </div>
            </div>

            <!-- Tactical Protocols Quick Trigger -->
            <div class="hud-panel hud-protocols-panel">
              <div class="panel-header">
                <div class="panel-tag">
                  <span class="hud-bullet cyan"></span>
                  <span>PROTOCOL COMMANDS</span>
                </div>
              </div>
              <p class="protocol-panel-desc">Direct hardware triggers programmed into the assistant core:</p>

              <div class="protocol-list">
                <button type="button" class="protocol-item-btn" data-protocol="house party">
                  <div class="protocol-info">
                    <span class="protocol-code">SEC-01</span>
                    <span class="protocol-title">House Party</span>
                  </div>
                  <span class="protocol-trigger-arrow">ENGAGE &rarr;</span>
                </button>

                <button type="button" class="protocol-item-btn" data-protocol="clean slate">
                  <div class="protocol-info">
                    <span class="protocol-code">SEC-02</span>
                    <span class="protocol-title">Clean Slate</span>
                  </div>
                  <span class="protocol-trigger-arrow">ENGAGE &rarr;</span>
                </button>

                <button type="button" class="protocol-item-btn" data-protocol="veronica">
                  <div class="protocol-info">
                    <span class="protocol-code">SEC-03</span>
                    <span class="protocol-title">Veronica Deployment</span>
                  </div>
                  <span class="protocol-trigger-arrow">ENGAGE &rarr;</span>
                </button>

                <button type="button" class="protocol-item-btn" data-protocol="sentry">
                  <div class="protocol-info">
                    <span class="protocol-code">SEC-04</span>
                    <span class="protocol-title">Sentry Surveillance</span>
                  </div>
                  <span class="protocol-trigger-arrow">ENGAGE &rarr;</span>
                </button>
              </div>
            </div>

            <!-- Quick Local Upgrade Banner -->
            <div class="local-upsell-card">
              <div class="upsell-badge">HIGH PERFORMANCE RUNTIME</div>
              <h3 class="upsell-title">Need full PC control?</h3>
              <p class="upsell-text">Web browsers restrict microphone streaming and local file manipulation. Deploy the offline Python engine for unrestricted system access.</p>
              <a href="#downloads" class="btn btn-secondary btn-block">DOWNLOAD LOCAL EDITION</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ARCHITECTURE & COMPARISON MATRIX -->
    <section class="section-wrapper comparison-section" id="comparison">
      <div class="section-container">
        <div class="section-heading-cluster">
          <span class="section-eyebrow">ARCHITECTURAL EVALUATION</span>
          <h2 class="section-title">ONLINE HOSTED VS LOCAL DEPLOYMENT</h2>
          <p class="section-desc">
            Analyze the distinct operational profiles of running JARVIS through our web interface versus compiling the autonomous Python service natively on your personal machine.
          </p>
        </div>

        <!-- Filter / Category Toggles -->
        <div class="matrix-filter-bar">
          <span class="filter-label">FILTER FEATURES:</span>
          <button type="button" class="matrix-filter-pill active" data-category="all">All Specs ({{ comparison_matrix|length }})</button>
          <button type="button" class="matrix-filter-pill" data-category="intelligence">Intelligence & AI</button>
          <button type="button" class="matrix-filter-pill" data-category="hardware">Hardware & OS</button>
          <button type="button" class="matrix-filter-pill" data-category="privacy">Privacy & Offline</button>
          <button type="button" class="matrix-filter-pill" data-category="automation">System Automation</button>
        </div>

        <!-- Comparison Table -->
        <div class="table-responsive-wrapper">
          <table class="hud-matrix-table" id="comparison-table">
            <thead>
              <tr>
                <th scope="col" class="th-feature">FEATURE & SPECIFICATION</th>
                <th scope="col" class="th-online">
                  <div class="th-badge-cluster">
                    <span class="col-indicator web"></span>
                    <span class="col-head-title">ONLINE WEB HOST</span>
                  </div>
                  <span class="col-sub">Zero-Install Sandbox</span>
                </th>
                <th scope="col" class="th-local highlight-col">
                  <div class="th-badge-cluster">
                    <span class="col-indicator local"></span>
                    <span class="col-head-title">LOCAL PYTHON RUNTIME</span>
                  </div>
                  <span class="col-sub">Workstation Master Edition</span>
                </th>
                <th scope="col" class="th-importance">OPERATIONAL IMPACT</th>
              </tr>
            </thead>
            <tbody>
              {% for row in comparison_matrix %}
              <tr class="matrix-row" data-category="{{ row.category }}">
                <td class="td-feature">
                  <div class="feature-title">{{ row.feature }}</div>
                  <div class="feature-category-tag">{{ row.category|upper }}</div>
                </td>
                <td class="td-online">
                  <div class="cell-content">
                    <span class="status-icon {{ 'icon-yes' if 'Yes' in row.online or 'Simulated' in row.online or 'Instant' in row.online else 'icon-partial' if 'Web' in row.online or 'Limited' in row.online else 'icon-no' }}"></span>
                    <span class="cell-text">{{ row.online }}</span>
                  </div>
                </td>
                <td class="td-local highlight-col">
                  <div class="cell-content">
                    <span class="status-icon icon-yes"></span>
                    <strong class="cell-text text-neon-cyan">{{ row.local }}</strong>
                  </div>
                </td>
                <td class="td-importance">
                  <span class="importance-badge {{ row.importance|lower }}">{{ row.importance }}</span>
                </td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>

        <!-- Architectural Summary Callout Cards -->
        <div class="comparison-summary-cards">
          <div class="summary-card">
            <div class="card-accent-bar cyan"></div>
            <h4 class="card-title">When to use Online Web Host</h4>
            <p class="card-p">
              Ideal for immediate demonstrations, instant voice evaluations without configuration, checking system availability, and testing JARVIS protocol responses across mobile devices or public terminals.
            </p>
            <ul class="card-check-list">
              <li>Instant execution with zero setup required</li>
              <li>Runs smoothly on mobile phones, tablets, and laptops</li>
              <li>Lightweight, battery-efficient interface</li>
            </ul>
          </div>

          <div class="summary-card highlight">
            <div class="card-accent-bar amber"></div>
            <h4 class="card-title">When to use Local Python Installation</h4>
            <p class="card-p">
              Essential when you require complete privacy, zero reliance on external cloud servers, custom neural weights (Llama 3 / Mistral / Whisper), and genuine automation of your local operating system files and apps.
            </p>
            <ul class="card-check-list">
              <li>100% offline audio synthesis & speech-to-text</li>
              <li>Direct desktop app launching, file searches & commands</li>
              <li>Customizable Python code base and hardware hooks</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- SETUP & INSTALLATION GUIDE -->
    <section class="section-wrapper setup-section" id="setup-guide">
      <div class="section-container">
        <div class="section-heading-cluster">
          <span class="section-eyebrow">DEPLOYMENT PLAYBOOK</span>
          <h2 class="section-title">LOCAL WORKSTATION SETUP GUIDE</h2>
          <p class="section-desc">
            Follow our guided interactive wizard to configure the local autonomous suite on Windows, macOS, or Linux in under three minutes.
          </p>
        </div>

        <div class="setup-wizard-container">
          <!-- Wizard Progress Bar -->
          <div class="wizard-steps-track" role="tablist" aria-label="Setup Steps">
            <button type="button" class="wizard-step-node active" data-step="1" role="tab" aria-selected="true">
              <span class="step-num">01</span>
              <span class="step-label">Prerequisites</span>
            </button>
            <div class="wizard-connector active"></div>
            <button type="button" class="wizard-step-node" data-step="2" role="tab" aria-selected="false">
              <span class="step-num">02</span>
              <span class="step-label">Package Download</span>
            </button>
            <div class="wizard-connector"></div>
            <button type="button" class="wizard-step-node" data-step="3" role="tab" aria-selected="false">
              <span class="step-num">03</span>
              <span class="step-label">Run Automated Setup</span>
            </button>
            <div class="wizard-connector"></div>
            <button type="button" class="wizard-step-node" data-step="4" role="tab" aria-selected="false">
              <span class="step-num">04</span>
              <span class="step-label">First Launch</span>
            </button>
          </div>

          <!-- Wizard Step Content Panes -->
          <div class="wizard-content-box">
            <!-- STEP 1 -->
            <div class="wizard-pane active" id="wizard-step-1">
              <div class="step-layout">
                <div class="step-desc-col">
                  <div class="step-badge">STEP 1 OF 4</div>
                  <h3 class="step-title">Verify Hardware & Python Runtime</h3>
                  <p class="step-text">
                    Mark LV requires Python 3.11 or newer. Python 3.11 through 3.13 are the tested versions. Install Python and add it to your system PATH before setup.
                  </p>
                  <div class="code-terminal-block">
                    <div class="terminal-bar">
                      <span class="term-dot red"></span>
                      <span class="term-dot yellow"></span>
                      <span class="term-dot green"></span>
                      <span class="term-title">terminal — check python</span>
                      <button type="button" class="copy-term-btn" data-clipboard="python --version || python3 --version">COPY</button>
                    </div>
                    <pre class="term-pre"><code><span class="term-prompt">$</span> python --version
<span class="term-comment"># Python 3.11+ required; 3.11–3.13 tested</span></code></pre>
                  </div>
                  <div class="notice-box info">
                    <strong>Note:</strong> On Windows, tick the checkbox <em>"Add Python to PATH"</em> during Python installation from python.org.
                  </div>
                </div>

                <div class="step-visual-col">
                  <div class="spec-checklist">
                    <h4 class="spec-head">MINIMUM HARDWARE SPECS</h4>
                    <div class="spec-row">
                      <span class="spec-item">CPU</span>
                      <span class="spec-req">Dual-Core 2.0 GHz+</span>
                    </div>
                    <div class="spec-row">
                      <span class="spec-item">RAM</span>
                      <span class="spec-req">4 GB RAM (8 GB for local LLM)</span>
                    </div>
                    <div class="spec-row">
                      <span class="spec-item">Storage</span>
                      <span class="spec-req">500 MB (base) / 4 GB (neural models)</span>
                    </div>
                    <div class="spec-row">
                      <span class="spec-item">Microphone</span>
                      <span class="spec-req">Any USB or standard 3.5mm input</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- STEP 2 -->
            <div class="wizard-pane" id="wizard-step-2">
              <div class="step-layout">
                <div class="step-desc-col">
                  <div class="step-badge">STEP 2 OF 4</div>
                  <h3 class="step-title">Download the Full Mark LV Project</h3>
                  <p class="step-text">
                    Download the complete cross-platform JARVIS desktop assistant, including its animated UI, plugins, configuration templates, and dependency setup. Your API key and personal memory are never included.
                  </p>
                  <div class="os-quick-selector">
                    <span class="selector-label">DETECTED OS:</span>
                    <span class="detected-os-badge" id="wizard-detected-os">Detecting...</span>
                  </div>
                  <div class="quick-download-cta">
                    <button type="button" class="btn btn-primary btn-lg" id="wizard-step-download-btn">
                      <span>DOWNLOAD FULL PROJECT (.ZIP)</span>
                    </button>
                  </div>
                  <p class="small-hint">Extract <code>Mark-LV-main.zip</code>, then open a terminal in the extracted <code>Mark-LV-main</code> folder.</p>
                </div>

                <div class="step-visual-col">
                  <div class="file-tree-preview">
                    <div class="tree-header">PACKAGE FILE STRUCTURE</div>
                    <ul class="tree-list">
                      <li class="tree-dir">📁 Mark-LV-main/
                        <ul>
                          <li class="tree-file">📄 setup.py <span class="tree-note">(Cross-platform dependency setup)</span></li>
                          <li class="tree-file">📄 main.py <span class="tree-note">(Launch the assistant)</span></li>
                          <li class="tree-file">📄 ui.py <span class="tree-note">(Full animated desktop UI)</span></li>
                          <li class="tree-file">📄 requirements.txt <span class="tree-note">(Python dependencies)</span></li>
                          <li class="tree-file">📁 core / plugins / dashboard / actions</li>
                        </ul>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <!-- STEP 3 -->
            <div class="wizard-pane" id="wizard-step-3">
              <div class="step-layout">
                <div class="step-desc-col">
                  <div class="step-badge">STEP 3 OF 4</div>
                  <h3 class="step-title">Install Dependencies</h3>
                  <p class="step-text">
                    Run the included setup script from the extracted project folder. It installs the dependencies for your operating system and the browsers used by JARVIS automation.
                  </p>
                  <div class="code-terminal-block">
                    <div class="terminal-bar">
                      <span class="term-dot red"></span>
                      <span class="term-dot yellow"></span>
                      <span class="term-dot green"></span>
                      <span class="term-title">terminal — deploy</span>
                      <button type="button" class="copy-term-btn" data-clipboard="python setup.py">COPY</button>
                    </div>
                    <pre class="term-pre"><code><span class="term-prompt">$</span> cd Mark-LV-main
<span class="term-prompt">$</span> python setup.py
<span class="term-success">[MARK LV] Installing cross-platform dependencies...</span>
<span class="term-success">[MARK LV] Setup complete!</span></code></pre>
                  </div>
                </div>

                <div class="step-visual-col">
                  <div class="features-checklist">
                    <h4 class="spec-head">WHAT THE SCRIPT PERFORMS</h4>
                    <div class="feat-step">✓ Installs dependencies for your OS</div>
                    <div class="feat-step">✓ Installs Chromium and Firefox automation browsers</div>
                    <div class="feat-step">✓ Keeps your API key on your computer</div>
                    <div class="feat-step">✓ Starts with an empty personal memory</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- STEP 4 -->
            <div class="wizard-pane" id="wizard-step-4">
              <div class="step-layout">
                <div class="step-desc-col">
                  <div class="step-badge">STEP 4 OF 4</div>
                  <h3 class="step-title">Launch Your Local Assistant</h3>
                  <p class="step-text">
                    Start Mark LV from the project folder. On first launch, enter your own Gemini API key in the setup screen; the website never receives it.
                  </p>
                  <div class="code-terminal-block">
                    <div class="terminal-bar">
                      <span class="term-dot red"></span>
                      <span class="term-dot yellow"></span>
                      <span class="term-dot green"></span>
                      <span class="term-title">terminal — run</span>
                      <button type="button" class="copy-term-btn" data-clipboard="python main.py">COPY</button>
                    </div>
                    <pre class="term-pre"><code><span class="term-prompt">$</span> python main.py
<span class="term-neon">MARK LV DESKTOP ASSISTANT</span>
<span class="term-comment">Complete the local setup screen, then start chatting with your assistant.</span></code></pre>
                  </div>
                </div>

                <div class="step-visual-col">
                  <div class="congrats-card">
                    <div class="congrats-icon">🚀</div>
                    <h4 class="congrats-title">SYSTEM FULLY DEPLOYED</h4>
                    <p class="congrats-p">Your machine is now outfitted with an autonomous local agent. No telemetry leaves your PC, and zero external subscriptions are required.</p>
                    <a href="#downloads" class="btn btn-secondary btn-block">GO TO DOWNLOADS</a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Wizard Navigation Buttons -->
          <div class="wizard-controls-bar">
            <button type="button" class="btn btn-outline" id="wizard-prev-btn" disabled>
              &larr; PREVIOUS STEP
            </button>
            <div class="wizard-progress-counter" id="wizard-step-counter">
              STEP 1 / 4
            </div>
            <button type="button" class="btn btn-primary" id="wizard-next-btn">
              NEXT STEP &rarr;
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- DIRECT DOWNLOAD CENTER -->
    <section class="section-wrapper download-section" id="downloads">
      <div class="section-container">
        <div class="section-heading-cluster">
          <span class="section-eyebrow">MARK LV DESKTOP RELEASE</span>
          <h2 class="section-title">DOWNLOAD THE COMPLETE ASSISTANT</h2>
          <p class="section-desc">
            Get the complete cross-platform desktop app and its full interface. Install it on your computer and keep your API key and assistant memory local.
          </p>
        </div>

        <!-- Full project download -->
        <div class="download-cards-grid">
          <div class="download-card full-project-download-card" id="card-mark-lv">
            <div class="dl-card-badge">COMPLETE DESKTOP ASSISTANT</div>
            <div class="dl-os-icon">🤖</div>
            <h3 class="dl-os-name">Mark LV — Full Project</h3>
            <span class="dl-package-name">Mark-LV-main.zip</span>
            <p class="dl-desc">The full JARVIS desktop UI, voice assistant, actions, plugins, dashboard, and cross-platform setup script.</p>
            <div class="dl-meta-list">
              <div class="dl-meta-item"><span>Format:</span><strong>Full source ZIP</strong></div>
              <div class="dl-meta-item"><span>Platforms:</span><strong>Windows, macOS, Linux</strong></div>
              <div class="dl-meta-item"><span>Requirements:</span><strong>Python 3.11+</strong></div>
            </div>
            <a href="/Mark-LV-main.zip" class="btn btn-primary btn-block download-trigger-btn" id="mark-lv-download-btn">
              <span class="btn-icon">⬇</span>
              <span>DOWNLOAD FULL PROJECT</span>
            </a>
          </div>
        </div>

        <!-- Local setup instructions -->
        <div class="direct-script-banner">
          <div class="direct-script-content">
            <div class="banner-icon">🐍</div>
            <div class="banner-text">
              <h4 class="banner-title">Run your own local JARVIS</h4>
              <p class="banner-desc">Extract the ZIP, open a terminal in <code>Mark-LV-main</code>, then run <code>python setup.py</code> followed by <code>python main.py</code>. Add your Gemini key in the local setup screen.</p>
            </div>
          </div>
        </div>

        <!-- Security & Integrity Card -->
        <div class="security-integrity-box">
          <div class="integrity-header">
            <span class="integrity-title">🔒 PACKAGE INTEGRITY & VERIFICATION</span>
            <span class="integrity-status">PERSONAL CREDENTIALS EXCLUDED</span>
          </div>
          <p class="integrity-text">
            The archive excludes API keys, linked accounts, personal memory, virtual environments, and caches. Review the included source and license before running it.
          </p>
        </div>
      </div>
    </section>
  </main>

  <!-- FOOTER -->
  <footer class="hud-footer">
    <div class="section-container footer-container">
      <div class="footer-brand-col">
        <div class="brand-cluster">
          <div class="arc-icon-small" aria-hidden="true"></div>
          <div class="brand-text">
            <span class="brand-title">J.A.R.V.I.S.</span>
            <span class="brand-sub">STARK RESEARCH INITIATIVE</span>
          </div>
        </div>
        <p class="footer-summary">
          A dual-mode intelligence interface engineered for real-time web interaction and unrestricted desktop automation.
        </p>
        <div class="footer-version-tag">
          <span>HOST CORE: v{{ app_version }}</span>
          <span>•</span>
          <span>LOCAL RUNTIME: v{{ local_version }}</span>
        </div>
      </div>

      <div class="footer-links-col">
        <h5 class="col-head">NAVIGATION</h5>
        <ul>
          <li><a href="#hero">Command Center</a></li>
          <li><a href="#online-host">Live Web HUD</a></li>
          <li><a href="#comparison">Feature Matrix</a></li>
          <li><a href="#setup-guide">Setup Guide</a></li>
          <li><a href="#downloads">Download Portal</a></li>
        </ul>
      </div>

      <div class="footer-links-col">
        <h5 class="col-head">DIRECT BUILDS</h5>
        <ul>
          <li><a href="/Mark-LV-main.zip">Download Mark-LV-main.zip</a></li>
        </ul>
      </div>

      <div class="footer-links-col">
        <h5 class="col-head">SYSTEM METRICS</h5>
        <div class="footer-stats-list">
          <div class="f-stat-item">
            <span class="f-stat-lbl">Global Downloads:</span>
            <span class="f-stat-val text-neon-cyan" id="footer-total-dl">{{ download_stats.total_downloads }}</span>
          </div>
          <div class="f-stat-item">
            <span class="f-stat-lbl">Full projects:</span>
            <span class="f-stat-val">{{ download_stats.mark_lv }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bottom-strip">
      <div class="section-container bottom-flex">
        <div class="copy-text">
          &copy; {{ current_year }} J.A.R.V.I.S. Autonomous Project. Inspired by the Stark Industries AI concept. Designed for engineers and enthusiasts.
        </div>
        <div class="back-to-top">
          <a href="#top" class="top-anchor-link">RETURN TO TOP &uarr;</a>
        </div>
      </div>
    </div>
  </footer>

  <!-- Modal Dialog for Download Confirmation & Instructions -->
  <div class="modal-backdrop" id="download-confirm-modal" role="dialog" aria-modal="true" aria-hidden="true" aria-labelledby="modal-title">
    <div class="hud-modal">
      <button type="button" class="modal-close-btn" id="modal-close-btn" aria-label="Close dialog">&times;</button>
      <div class="modal-header">
        <div class="modal-icon">📦</div>
        <div>
          <h3 class="modal-title" id="modal-title">PACKAGE DEPLOYMENT INITIALIZED</h3>
          <span class="modal-sub" id="modal-os-name">Full project - Windows, macOS, and Linux</span>
        </div>
      </div>
      <div class="modal-body">
        <p class="modal-p">Your download has begun! Follow these simple next steps to deploy on your machine:</p>
        <ol class="modal-steps-list">
          <li>Extract the downloaded <code>.zip</code> file into a clean directory.</li>
          <li>Open your command prompt or terminal in that directory.</li>
          <li>Run: <code>python setup.py</code> to install the app dependencies.</li>
          <li>Run: <code>python main.py</code>, then enter your own Gemini API key locally.</li>
        </ol>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-primary" id="modal-ack-btn">ACKNOWLEDGE &amp; PROCEED</button>
      </div>
    </div>
  </div>

  <!-- Client-side Scripts in Dependency Order -->
  <script src="/static/js/speech.js"></script>
  <script src="/static/js/assistant.js"></script>
  <script src="/static/js/installer.js"></script>
  <script src="/static/js/main.js"></script>
</body>
</html>
"""


class AssistantAPI:
  def process_query(self, query, context=None):
    return _engine.process(query)

  def get_system_status(self):
    return {
      "status": "ONLINE",
      "version": config.APP_VERSION,
      **_engine._generate_telemetry(),
    }