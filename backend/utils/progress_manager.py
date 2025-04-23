"""
Module for managing progress updates and the progress update server.
"""

import queue
import threading
import time
from flask import Flask, Response
import logging
import socket

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProgressManager:
    """Singleton class to manage progress updates and server operations."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ProgressManager, cls).__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the progress manager."""
        self.progress_queue = queue.Queue()
        self.server_started = False
        self.app = None
        self.server_thread = None
        self.logger = logger

    def update_progress(self, message):
        """Update the progress message to be shown to the user."""
        try:
            self.progress_queue.put(message)
            self.logger.info(f"Progress update: {message}")
        except Exception as e:
            self.logger.error(f"Error updating progress: {str(e)}")

    def get_progress_update(self):
        """Get the latest progress update from the queue."""
        try:
            if not self.progress_queue.empty():
                return self.progress_queue.get()
            return None
        except Exception as e:
            self.logger.error(f"Error getting progress update: {str(e)}")
            return None

    def create_server_app(self):
        """Create the Flask application for the progress update server."""
        app = Flask(f"progress_server")  # Use a distinct name
        # Disable Flask's default logging to avoid cluttering the console
        app.logger.disabled = True
        log = logging.getLogger('werkzeug')
        log.disabled = True

        @app.route('/progress-updates')
        def progress_updates():
            def generate():
                last_update = None
                while True:
                    try:
                        # Check for new progress update
                        update = self.get_progress_update()
                        if update and update != last_update:
                            last_update = update
                            yield f"data: {update}\n\n"
                    except Exception as e:
                        self.logger.error(f"Error in progress update generator: {str(e)}")
                    time.sleep(1)  # Check frequently for updates
            
            # Add CORS headers to allow cross-origin requests
            headers = {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'X-Accel-Buffering': 'no',
                'Access-Control-Allow-Origin': '*'
            }
            
            return Response(generate(), mimetype='text/event-stream', headers=headers)

        @app.route('/test')
        def test():
            return "Progress update server is running!"

        # Keep this for diagnostic purposes but make it clear it's not the main app
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def catch_all(path):
            return f"This is the progress update server running on port {self.server_port}. Please use the main application at http://localhost:{self.main_app_port}/"

        return app

    def is_port_in_use(self, port):
        """Check if a port is already in use."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def start_server(self, host='0.0.0.0', port=5002, main_app_port=5001):
        """Start the progress update server in a background thread."""
        with self._lock:
            if self.server_started:
                self.logger.info("Server already running")
                return
            
            # Store port numbers for reference
            self.server_port = port
            self.main_app_port = main_app_port
            
            # First check if port is available
            if self.is_port_in_use(port):
                self.logger.warning(f"Port {port} is already in use, trying to find an alternative")
                # Try to find an available port
                for test_port in range(5010, 5050):
                    if not self.is_port_in_use(test_port):
                        port = test_port
                        self.server_port = port
                        self.logger.info(f"Found available port: {port}")
                        break
            
            try:
                self.app = self.create_server_app()
                
                def run_server():
                    try:
                        self.app.run(host=host, port=port, threaded=True, debug=False, use_reloader=False)
                    except Exception as e:
                        self.logger.error(f"Error running progress server: {str(e)}")
                
                self.server_thread = threading.Thread(target=run_server, daemon=True)
                self.server_thread.start()
                self.server_started = True
                self.logger.info(f"Progress update server started on port {port}")
                
                # Give the server a moment to start up
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Failed to start progress server: {str(e)}")

# Create a global instance to be imported by other modules
progress_manager = ProgressManager()
