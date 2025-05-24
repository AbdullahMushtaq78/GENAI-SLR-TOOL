"""
Flask application for the SLR (Systematic Literature Review) analysis tool.
"""

from flask import Flask, request, render_template_string, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import re
import markdown
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import main functionality
from backend.main import demo_output, demo_output2, start_processing_SLR_pdf
from backend.SLR_GPT import SLR_GPT_Agent, SLR_GPT
from backend.utils.progress_manager import progress_manager

# Import modular components
from frontend.static.styles.static_styles import SOCIETY_COLORS, generate_society_css
from frontend.templates.html_templates import render_upload_form
from frontend.utils.utils_app import get_unique_filename
from frontend.SLR_GPT_chat.chat_ui import render_chat_ui, get_chat_css, get_chat_js
from frontend.templates.results_template import render_results_page
from frontend.utils.markdown_utils import convert_markdown
from frontend.templates.results_processor import generate_society_cards
from backend.config.configs import UPLOAD_FOLDER, RESULTS_FOLDER, PORT, DEBUG

# Initialize Flask application
app = Flask(__name__)

# Global variables to store analysis results
raw_result = None
ocr = None
chat_agent = None

# Ensure upload and results directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Set up static folder for serving assets
app.static_folder = 'frontend'
app.static_url_path = '/static'

# Lock for request handling to prevent race conditions
request_lock = threading.Lock()

@app.route("/", methods=["GET", "POST"])
def index():
    """Main route handler for the application."""
    global raw_result, ocr, chat_agent
    
    # Use a lock to prevent concurrent processing of requests
    with request_lock:
        try:
            if request.method == "POST":
                try:
                    paper_title = request.form.get("paper_title", "").strip()
                    pdf_file = request.files.get("paper_pdf")

                    # Validate inputs
                    if not pdf_file or not paper_title:
                        logger.error("Missing paper title or PDF file")
                        return "Please provide both paper title and PDF file", 400

                    # Save PDF with paper title as filename
                    pdf_filename = secure_filename(f"{paper_title}.pdf")
                    pdf_path = get_unique_filename(UPLOAD_FOLDER, pdf_filename)
                    pdf_file.save(pdf_path)
                    logger.info(f"PDF saved to {pdf_path}")

                    try:
                        # Process the PDF and get results
                        
                        #raw_result, ocr = start_processing_SLR_pdf(pdf_path, paper_title)
                        raw_result, ocr = demo_output(pdf_path, paper_title)
                        # raw_result, ocr = demo_output2(pdf_path, paper_title)

                        if not raw_result:
                            raise ValueError("No results returned from PDF processing.")
                        logger.info(f"Processing complete. Results length: {len(raw_result)}")

                        # Save results to a file
                        results_filename = secure_filename(f"{paper_title}_results.txt")
                        results_path = os.path.join(RESULTS_FOLDER, results_filename)
                        with open(results_path, "w") as results_file:
                            results_file.write(str(raw_result))
                        logger.info(f"Results saved to {results_path}")
                        
                        # Create SLR-GPT Agent
                        chat_agent = SLR_GPT_Agent(ocr, raw_result)
                        
                        # Process results to generate cards
                        raw_cards = generate_society_cards(raw_result, convert_markdown)
                        
                        # Render results page with chat UI
                        final_output = render_results_page(paper_title, raw_cards, generate_society_css)
                        
                        # Insert chat UI and its JavaScript before the closing body tag
                        final_output = final_output.replace('</body>', f'{render_chat_ui()}\n<script>{get_chat_js()}</script>\n</body>')
                        
                        # Insert chat CSS in the head section
                        final_output = final_output.replace('</style>', f'{get_chat_css()}\n</style>')
                        
                        return render_template_string(final_output, raw_result=raw_result)
                        
                    except Exception as e:
                        logger.error(f"Error processing PDF: {str(e)}")
                        return f"Error processing PDF: {str(e)}", 500

                except Exception as e:
                    logger.error(f"Unexpected error in POST handler: {str(e)}")
                    return f"An unexpected error occurred: {str(e)}", 500

            # GET request: Show upload form
            return render_upload_form()
            
        except Exception as e:
            logger.error(f"Critical error in index route: {str(e)}")
            return "Server error. Please try again later.", 500


@app.route("/chat", methods=["POST"])
def chat():
    """Route handler for chat interactions."""
    try:
        data = request.json
        if not data or 'message' not in data or 'paper_title' not in data:
            logger.warning("Invalid chat request - missing required fields")
            return {"response": "Invalid request, message and paper_title required"}, 400
            
        user_message = data['message']
        paper_title = data['paper_title']
        
        global chat_agent
        if chat_agent is None:
            logger.error("Chat agent is not initialized")
            return {"response": "Chat service is not ready. Please upload a paper first."}, 400
            
        # Get response from the agent
        response = SLR_GPT(chat_agent, user_message)
        
        # Convert response markdown to HTML
        formatted_response = convert_markdown(response)
        
        return {"response": formatted_response}
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return {"response": f"Sorry, I encountered an error processing your request: {str(e)}"}, 500


# Route to serve the mindmap PDF file
@app.route('/static/assets/Mindmap.pdf')
def serve_mindmap_pdf():
    """Serve the Mindmap PDF file."""
    return send_from_directory('frontend/assets', 'Mindmap.pdf')


# Route to serve the PRISMA Guidelines PDF file
@app.route('/static/assets/PRISMA_guidelines.pdf')
def serve_prisma_pdf():
    """Serve the PRISMA Guidelines PDF file."""
    return send_from_directory('frontend/assets', 'PRISMA_guidelines.pdf')


# Route to download results file
@app.route('/download/<paper_title>')
def download_results(paper_title):
    """Download the analysis results for a specific paper."""
    try:
        # Create the results filename based on the paper title
        results_filename = secure_filename(f"{paper_title}_results.txt")
        results_path = os.path.join(RESULTS_FOLDER, results_filename)
        
        # Check if the file exists
        if not os.path.exists(results_path):
            logger.error(f"Results file not found: {results_path}")
            return "Results file not found", 404
            
        # Return the file as an attachment (for download)
        return send_from_directory(
            directory=RESULTS_FOLDER,
            path=results_filename,
            as_attachment=True,
            download_name=results_filename
        )
    except Exception as e:
        logger.error(f"Error downloading results: {str(e)}")
        return f"Error downloading results: {str(e)}", 500


# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify server is working."""
    return jsonify({"status": "healthy", "service": "SLR Analysis Tool"}), 200


if __name__ == "__main__":
    # Start the progress update server if not already started
    try:
        # Pass the main app port to the progress manager
        progress_manager.start_server(host='0.0.0.0', port=5002, main_app_port=PORT)
        logger.info("Progress update server initialized")
    except Exception as e:
        logger.error(f"Failed to start progress update server: {str(e)}")
    
    # Add a delay to ensure progress server is fully started before main app
    import time
    time.sleep(1)
    
    logger.info(f"Starting main application on port {PORT}")
    # Use a unique name for the Flask app instance to avoid conflicts
    app.config['SERVER_NAME'] = f"localhost:{PORT}"
    # Start the main Flask application
    app.run(debug=DEBUG, port=PORT, host='0.0.0.0', threaded=True, use_reloader=False)