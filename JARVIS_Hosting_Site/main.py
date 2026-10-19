import os
import sys
import logging
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify

# Add current directory to path to ensure backend package is discoverable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.config import Config
from backend.downloads_manager import DownloadsManager
from backend.assistant_api import AssistantAPI, HTML_TEMPLATE

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)

downloads_manager = DownloadsManager()
assistant_api = AssistantAPI()

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        app_version=Config.APP_VERSION,
        local_version=Config.LOCAL_VERSION,
        download_stats=downloads_manager.get_download_stats(),
        comparison_matrix=Config.COMPARISON_MATRIX,
        current_year=datetime.now().year,
    )

@app.route('/api/assistant/query', methods=['POST'])
@app.route('/api/assistant/command', methods=['POST'])
def assistant_query():
    try:
        data = request.get_json(silent=True) or {}
        query = data.get('query') or data.get('command')
        if not query:
            return jsonify({'status': 'error', 'message': 'Missing query parameter'}), 400
        context = data.get('context', {})
        
        response_data = assistant_api.process_query(query, context)
        return jsonify(response_data), 200
    except Exception as e:
        logger.error(f"Error handling assistant query: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal assistant processing error'}), 500

@app.route('/api/assistant/status', methods=['GET'])
def assistant_status():
    try:
        status_data = assistant_api.get_system_status()
        return jsonify(status_data), 200
    except Exception as e:
        logger.error(f"Error retrieving assistant status: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Could not retrieve system status'}), 500

@app.route('/api/download/<platform>', methods=['GET'])
@app.route('/download/package', methods=['GET'])
def download_package(platform=None):
    try:
        platform = platform or request.args.get('os', '')
        valid_platforms = ['windows', 'macos', 'linux']
        if platform not in valid_platforms:
            return jsonify({'status': 'error', 'message': 'Invalid platform specified'}), 400
        
        return downloads_manager.get_mark_lv_download()
    except Exception as e:
        logger.error(f"Error generating download for {platform}: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Download processing error'}), 500

@app.route('/download/script', methods=['GET'])
@app.route('/api/download/script', methods=['GET'])
def download_setup_script():
    try:
        return downloads_manager.get_setup_script()
    except Exception as e:
        logger.error(f"Error generating setup script download: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Script download error'}), 500

@app.route('/api/download/mark-lv', methods=['GET'])
@app.route('/download/mark-lv', methods=['GET'])
@app.route('/Mark-LV-main.zip', methods=['GET'])
def download_mark_lv():
    try:
        return downloads_manager.get_mark_lv_download()
    except Exception as e:
        logger.error(f"Error generating Mark LV project download: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Mark LV download error'}), 500

@app.route('/api/telemetry/stats', methods=['GET'])
def telemetry_stats():
    try:
        stats = {
            'downloads': downloads_manager.get_total_downloads(),
            'active_nodes': Config.ACTIVE_NODES_COUNT,
            'version': Config.VERSION,
            'uptime_percentage': Config.UPTIME_PERCENTAGE
        }
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Error fetching telemetry stats: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Could not fetch telemetry'}), 500

@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404
    return index(), 404

@app.errorhandler(500)
def internal_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    return index(), 500

if __name__ == '__main__':
    logger.info("Initializing JARVIS Web Interface & Download Server...")
    os.makedirs(Config.DOWNLOAD_OUTPUT_DIR, exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)