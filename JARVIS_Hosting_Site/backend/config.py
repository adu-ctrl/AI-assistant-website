import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RELEASE_VERSION = "1.0.0"
DOWNLOAD_DIR = os.environ.get("JARVIS_DOWNLOAD_DIR") or (
    "/tmp/jarvis-downloads"
    if os.environ.get("VERCEL")
    else os.path.join(BASE_DIR, "generated_downloads")
)
MARK_LV_SOURCE_DIR = os.environ.get(
    "JARVIS_MARK_LV_SOURCE_DIR",
    os.path.join(os.path.expanduser("~"), "Desktop", "Mark-LV-main", "Mark-LV-main"),
)
MARK_LV_ARCHIVE_PATH = os.path.join(BASE_DIR, "public", "Mark-LV-main.zip")


class Config:
    APP_NAME = "JARVIS Autonomous Core"
    APP_VERSION = "3.4.2"
    VERSION = APP_VERSION
    LOCAL_VERSION = RELEASE_VERSION
    BASE_DIR = BASE_DIR
    DOWNLOAD_DIR = DOWNLOAD_DIR
    DOWNLOAD_OUTPUT_DIR = DOWNLOAD_DIR
    MARK_LV_SOURCE_DIR = MARK_LV_SOURCE_DIR
    MARK_LV_ARCHIVE_PATH = MARK_LV_ARCHIVE_PATH
    ACTIVE_NODES_COUNT = 1
    UPTIME_PERCENTAGE = 99.9
    COMPARISON_MATRIX = [
        {"feature": "Voice interface", "category": "interface", "online": "Browser-supported", "local": "Native audio", "importance": "High"},
        {"feature": "Offline access", "category": "privacy", "online": "No", "local": "Yes", "importance": "High"},
        {"feature": "System automation", "category": "control", "online": "Limited", "local": "Full access", "importance": "High"},
    ]