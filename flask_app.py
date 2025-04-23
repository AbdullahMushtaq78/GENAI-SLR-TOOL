"""
Flask application for the SLR (Systematic Literature Review) analysis tool.
"""

from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
import os
import re
import markdown

# Import main functionality
from backend.main import demo_output, start_processing_SLR_pdf
from backend.SLR_GPT import SLR_GPT_Agent, SLR_GPT

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

@app.route("/", methods=["GET", "POST"])
def index():
    """Main route handler for the application."""
    global raw_result, ocr, chat_agent
    
    if request.method == "POST":
        try:
            paper_title = request.form.get("paper_title", "").strip()
            pdf_file = request.files.get("paper_pdf")

            # Validate inputs
            if not pdf_file or not paper_title:
                return "Please provide both paper title and PDF file", 400

            # Save PDF with paper title as filename
            pdf_filename = secure_filename(f"{paper_title}.pdf")
            pdf_path = get_unique_filename(UPLOAD_FOLDER, pdf_filename)
            pdf_file.save(pdf_path)

            try:
                # Process the PDF and get results
                raw_result, ocr = demo_output(pdf_path, paper_title)
                chat_agent = SLR_GPT_Agent(ocr, raw_result)

                if not raw_result:
                    raise ValueError("No results returned from PDF processing.")
                print(f"Processing complete. Results length: {len(raw_result)}")

                # Save results to a file
                results_filename = secure_filename(f"{paper_title}_results.txt")
                results_path = os.path.join(RESULTS_FOLDER, results_filename)
                with open(results_path, "w") as results_file:
                    results_file.write(str(raw_result))
                print(f"Results saved to {results_path}")
                
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
                print(f"Error processing PDF: {str(e)}")
                return f"Error processing PDF: {str(e)}", 500

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return f"An unexpected error occurred: {str(e)}", 500

    # GET request: Show upload form
    return render_upload_form()


@app.route("/chat", methods=["POST"])
def chat():
    """Route handler for chat interactions."""
    try:
        data = request.json
        if not data or 'message' not in data or 'paper_title' not in data:
            return {"response": "Invalid request, message and paper_title required"}, 400
            
        user_message = data['message']
        paper_title = data['paper_title']
        
        global chat_agent
        # Get response from the agent
        response = SLR_GPT(chat_agent, user_message)
        
        # Convert response markdown to HTML
        formatted_response = convert_markdown(response)
        
        return {"response": formatted_response}
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return {"response": f"Sorry, I encountered an error processing your request: {str(e)}"}, 500


if __name__ == "__main__":
    app.run(debug=DEBUG, port=PORT)