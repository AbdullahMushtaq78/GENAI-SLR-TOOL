"""
Production entry point for the SLR Flask application.
This file is used by Render.com for deployment.
"""

import os
import logging
from flask_app import app
from backend.utils.progress_manager import progress_manager

# Configure logging for production
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get port from environment variable (Render.com sets this)
port = int(os.environ.get('PORT', 5001))

# Configure app for production
app.config['DEBUG'] = False
app.config['ENV'] = 'production'

# Remove SERVER_NAME for production (causes issues with Render.com)
if 'SERVER_NAME' in app.config:
    del app.config['SERVER_NAME']

# Add SERVER_NAME None explicitly to fix the KeyError issue
app.config['SERVER_NAME'] = None

def create_app():
    """Application factory for production."""
    try:
        # Start the progress update server for production
        progress_manager.start_server(host='0.0.0.0', port=port+1, main_app_port=port)
        logger.info("Progress update server initialized for production")
    except Exception as e:
        logger.error(f"Failed to start progress update server: {str(e)}")
    
    logger.info(f"Application configured for production on port {port}")
    return app

# For Gunicorn
application = create_app()

if __name__ == "__main__":
    # This is for local testing only
    application.run(host='0.0.0.0', port=port, debug=False) 