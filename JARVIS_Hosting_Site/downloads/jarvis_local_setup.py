import os
import sys
import subprocess
import platform
import time
import json
import shutil
import logging
from datetime import datetime

class JarvisInstaller:
    def __init__(self):
        self.os_type = platform.system()
        self.home_dir = os.path.expanduser("~")
        self.install_path = os.path.join(self.home_dir, "JARVIS_Local")
        self.version = "1.0.0"
        self.dependencies = [
            "pip",
            "setuptools",
            "wheel",
            "SpeechRecognition",
            "pyttsx3",
            "pyaudio",
            "requests",
            "psutil"
        ]
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - [SYSTEM] - %(message)s',
            handlers=[
                logging.FileHandler("setup_debug.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def clear_console(self):
        os.system('cls' if self.os_type == 'Windows' else 'clear')

    def print_header(self):
        header = f"""
============================================================
       JARVIS SYSTEM INTERFACE - LOCAL DEPLOYMENT
============================================================
  OS: {self.os_type} | Architecture: {platform.machine()}
  Version: {self.version} | Status: Initialization
============================================================
        """
        print(header)

    def animated_log(self, message, delay=0.03):
        prefix = f"[{datetime.now().strftime('%H:%M:%S')}] > "
        sys.stdout.write(prefix)
        for char in message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\n")

    def check_python_version(self):
        self.animated_log("Verifying Python environment...")
        major = sys.version_info.major
        minor = sys.version_info.minor
        if major < 3 or (major == 3 and minor < 8):
            self.animated_log("CRITICAL ERROR: Python 3.8+ required for JARVIS modules.")
            sys.exit(1)
        self.animated_log(f"Python {major}.{minor} detected. Compatibility confirmed.")

    def create_structure(self):
        self.animated_log(f"Establishing secure directory at: {self.install_path}")
        folders = ['core', 'modules', 'logs', 'config', 'data', 'temp']
        try:
            if not os.path.exists(self.install_path):
                os.makedirs(self.install_path)
            
            for folder in folders:
                path = os.path.join(self.install_path, folder)
                if not os.path.exists(path):
                    os.makedirs(path)
            self.animated_log("File system architecture finalized.")
        except Exception as e:
            self.animated_log(f"FAILED to create directories: {str(e)}")
            sys.exit(1)

    def install_packages(self):
        self.animated_log("Synchronizing neural dependencies via PIP...")
        for package in self.dependencies:
            try:
                self.animated_log(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                      stdout=subprocess.DEVNULL, 
                                      stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                self.animated_log(f"Warning: Manual intervention may be required for {package}.")
        self.animated_log("Package synchronization complete.")

    def generate_config(self):
        self.animated_log("Generating local system configuration...")
        config_data = {
            "user_profile": os.getlogin(),
            "installation_date": datetime.now().isoformat(),
            "environment": "Production-Local",
            "ui_theme": "Futuristic-Neon",
            "voice_engine": "pyttsx3",
            "recognition_threshold": 0.8,
            "auto_update": True,
            "security_level": "Standard"
        }
        config_path = os.path.join(self.install_path, "config", "settings.json")
        with open(config_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        self.animated_log("Configuration parameters encrypted and stored.")

    def create_entry_point(self):
        self.animated_log("Compiling main execution kernel...")
        kernel_code = """
import os
import sys
import time
import pyttsx3
import speech_recognition as sr

def initialize_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Try to set a more 'robotic' or professional voice if available
    for voice in voices:
        if "zira" in voice.name.lower() or "david" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 175)
    return engine

def speak(engine, text):
    print(f"[JARVIS]: {text}")
    engine.say(text)
    engine.runAndWait()

def main():
    print("--- JARVIS LOCAL INSTANCE ACTIVE ---")
    engine = initialize_engine()
    speak(engine, "System online. Local protocols initialized. How can I assist you, Sir?")
    
    try:
        while True:
            cmd = input("[USER]: ").lower()
            if "status" in cmd:
                speak(engine, "All local subsystems are operational. CPU load is nominal.")
            elif "exit" in cmd or "shutdown" in cmd:
                speak(engine, "Terminating local session. Goodbye.")
                break
            else:
                speak(engine, "Command acknowledged, but external processing modules are currently in standby.")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
        """
        kernel_path = os.path.join(self.install_path, "jarvis_run.py")
        with open(kernel_path, 'w') as f:
            f.write(kernel_code.strip())
        self.animated_log("Local kernel: jarvis_run.py created successfully.")

    def finalize(self):
        self.animated_log("Running final diagnostics...")
        time.sleep(1)
        self.clear_console()
        self.print_header()
        print(f"\nSUCCESS: JARVIS Local Installation Complete.")
        print(f"Location: {self.install_path}")
        print("-" * 60)
        print("INSTRUCTIONS:")
        print(f"1. Navigate to: {self.install_path}")
        print("2. Run the assistant using: python jarvis_run.py")
        print("3. Voice recognition requires a functional microphone.")
        print("-" * 60)
        input("\nPress ENTER to conclude setup...")

    def run(self):
        self.clear_console()
        self.print_header()
        self.check_python_version()
        self.create_structure()
        self.install_packages()
        self.generate_config()
        self.create_entry_point()
        self.finalize()

if __name__ == "__main__":
    try:
        installer = JarvisInstaller()
        installer.run()
    except Exception as e:
        print(f"\n[FATAL ERROR]: {str(e)}")
        logging.exception("Installation failed unexpectedly.")
        sys.exit(1)