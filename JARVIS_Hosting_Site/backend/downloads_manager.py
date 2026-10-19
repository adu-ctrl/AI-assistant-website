import os
import zipfile
import io
import logging
from flask import send_file, Response
from backend.config import DOWNLOAD_DIR, MARK_LV_ARCHIVE_PATH, MARK_LV_SOURCE_DIR, RELEASE_VERSION, BASE_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DownloadsManager:
    def __init__(self):
        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

    def _generate_installer_package(self, os_type):
        """Generates a zip archive containing the local setup script and config."""
        zip_filename = f"jarvis_local_setup_{os_type}_{RELEASE_VERSION}.zip"
        zip_path = os.path.join(DOWNLOAD_DIR, zip_filename)

        if os.path.exists(zip_path):
            try:
                with zipfile.ZipFile(zip_path) as existing_archive:
                    if 'jarvis_local_setup.py' in existing_archive.namelist():
                        return zip_path
            except zipfile.BadZipFile:
                pass

        try:
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Path to the source template file
                script_path = os.path.join(BASE_DIR, 'downloads', 'jarvis_local_setup.py')
                
                if os.path.exists(script_path):
                    zipf.write(script_path, arcname='jarvis_local_setup.py')
                
                # Add a README for the user
                readme_content = f"JARVIS Local Assistant Version {RELEASE_VERSION}\nPlatform: {os_type}\nRun 'python jarvis_local_setup.py' to initialize."
                zipf.writestr('README.txt', readme_content)
            
            with open(zip_path, 'wb') as f:
                f.write(buffer.getvalue())
            
            return zip_path
        except Exception as e:
            logger.error(f"Failed to generate archive: {str(e)}")
            return None

    def get_download_stream(self, os_type):
        """Handles binary stream delivery for the client."""
        valid_platforms = ['windows', 'macos', 'linux']
        if os_type not in valid_platforms:
            os_type = 'generic'

        file_path = self._generate_installer_package(os_type)
        
        if file_path and os.path.exists(file_path):
            try:
                self._log_download_event(os_type)
                return send_file(
                    file_path,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name=os.path.basename(file_path)
                )
            except Exception as e:
                logger.error(f"Error serving file: {str(e)}")
                return Response("File delivery failed", status=500)
        
        return Response("Package not found", status=404)

    def get_setup_script(self):
        script_path = os.path.join(BASE_DIR, 'downloads', 'jarvis_local_setup.py')
        if not os.path.isfile(script_path):
            return Response("Setup script not found", status=404)

        self._log_download_event('script')
        return send_file(
            script_path,
            mimetype='text/x-python',
            as_attachment=True,
            download_name='jarvis_local_setup.py'
        )

    @staticmethod
    def _exclude_from_mark_lv_archive(relative_path):
        parts = relative_path.replace('\\', '/').split('/')
        lowered = [part.lower() for part in parts]
        name = lowered[-1]

        excluded_parts = {
            '.git', '.venv', 'venv', 'env', '__pycache__', '.pytest_cache',
            '.mypy_cache', '.ruff_cache', 'node_modules', 'build', 'dist',
            'logs', 'downloads', 'screenshots', 'whatsapp_web',
        }
        if any(part in excluded_parts for part in lowered):
            return True
        if lowered[:2] == ['config', 'certs']:
            return True
        if lowered[:2] == ['memory', 'long_term.json']:
            return True
        if name == 'api_keys.json' or name == '.env' or name.startswith('.env.'):
            return True
        if name.startswith('token') and name.endswith('.json'):
            return True
        if name.startswith('client_secret') and name.endswith('.json'):
            return True
        if 'credential' in name and name.endswith('.json'):
            return True
        if name.endswith(('.pyc', '.pyo', '.log', '.db', '.sqlite', '.sqlite3', '.pem', '.key', '.p12', '.pfx')):
            return True
        return False

    def _generate_mark_lv_package(self):
        source_dir = os.path.abspath(MARK_LV_SOURCE_DIR)
        if not os.path.isdir(source_dir):
            if os.path.isfile(MARK_LV_ARCHIVE_PATH):
                return MARK_LV_ARCHIVE_PATH
            logger.error("Mark LV source directory is not configured or does not exist")
            return None

        zip_path = MARK_LV_ARCHIVE_PATH
        buffer = io.BytesIO()
        try:
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
                for root, directories, filenames in os.walk(source_dir, topdown=True, followlinks=False):
                    relative_root = os.path.relpath(root, source_dir)
                    directories[:] = [
                        directory for directory in directories
                        if not os.path.islink(os.path.join(root, directory))
                        and not self._exclude_from_mark_lv_archive(
                            os.path.join(relative_root, directory) if relative_root != '.' else directory
                        )
                    ]
                    for filename in filenames:
                        source_path = os.path.join(root, filename)
                        relative_path = os.path.relpath(source_path, source_dir)
                        if os.path.islink(source_path) or self._exclude_from_mark_lv_archive(relative_path):
                            continue
                        archive.write(source_path, os.path.join('Mark-LV-main', relative_path))

                instructions = (
                    "MARK LV - FULL DESKTOP ASSISTANT\n\n"
                    "1. Extract the complete Mark-LV-main folder.\n"
                    "2. Open a terminal in that folder.\n"
                    "3. Run: python setup.py\n"
                    "4. Run: python main.py\n\n"
                    "The first launch asks for your own Gemini API key. Personal keys, "
                    "linked accounts, and local memory are not included in this archive.\n"
                    "Python 3.11 or newer is required.\n"
                )
                archive.writestr('Mark-LV-main/START_HERE.txt', instructions)

            with open(zip_path, 'wb') as package_file:
                package_file.write(buffer.getvalue())
            return zip_path
        except Exception:
            logger.exception("Failed to build Mark LV project archive")
            return None

    def get_mark_lv_download(self):
        file_path = self._generate_mark_lv_package()
        if not file_path or not os.path.isfile(file_path):
            return Response("Mark LV project package is unavailable", status=503)

        self._log_download_event('mark-lv')
        return send_file(
            file_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name='Mark-LV-main.zip',
        )

    def _log_download_event(self, os_type):
        """Tracks download metrics."""
        log_file = os.path.join(DOWNLOAD_DIR, 'downloads.log')
        try:
            with open(log_file, 'a') as f:
                import datetime
                f.write(f"{datetime.datetime.now().isoformat()} - OS: {os_type} - Version: {RELEASE_VERSION}\n")
        except IOError as e:
            logger.warning(f"Could not log download: {e}")

    def get_download_stats(self):
        stats = {"total_downloads": 0, "mark_lv": 0, "windows": 0, "macos": 0, "linux": 0}
        log_file = os.path.join(DOWNLOAD_DIR, 'downloads.log')
        try:
            with open(log_file, 'r') as download_log:
                for line in download_log:
                    stats["total_downloads"] += 1
                    if "OS: mark-lv " in line:
                        stats["mark_lv"] += 1
                    for platform in ("windows", "macos", "linux"):
                        if f"OS: {platform} " in line:
                            stats[platform] += 1
                            break
        except FileNotFoundError:
            pass
        return stats

    def get_total_downloads(self):
        return self.get_download_stats()["total_downloads"]

downloads_manager = DownloadsManager()