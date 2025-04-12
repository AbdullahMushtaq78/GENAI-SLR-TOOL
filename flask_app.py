from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
import os
from main import demo_output, start_processing_SLR_pdf
import markdown
from personas import PERSONAS, roles

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

PORT = 5001


def get_unique_filename(base_path, filename):
    """Generate unique filename by adding number suffix if file exists"""
    name, ext = os.path.splitext(filename)
    counter = 1
    new_path = os.path.join(base_path, filename)

    while os.path.exists(new_path):
        new_filename = f"{name}_{counter}{ext}"
        new_path = os.path.join(base_path, new_filename)
        counter += 1

    return new_path


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            paper_title = request.form.get("paper_title", "").strip()
            pdf_file = request.files.get("paper_pdf")

            if not pdf_file or not paper_title:
                return "Please provide both paper title and PDF file", 400

            # Save PDF with paper title as filename
            pdf_filename = secure_filename(f"{paper_title}.pdf")
            pdf_path = get_unique_filename(UPLOAD_FOLDER, pdf_filename)
            pdf_file.save(pdf_path)

            try:
                # Process the PDF
                _,_, raw_result, ocr = demo_output(pdf_path, paper_title)
                #raw_result, ocr = start_processing_SLR_pdf(pdf_path, paper_title)
                if not raw_result:
                    raise ValueError("No results returned from PDF processing.")
                print(f"Processing complete. Results length: {len(raw_result)}")

                # Save results to a file in the results folder
                results_filename = secure_filename(f"{paper_title}_results.txt")
                results_path = os.path.join(RESULTS_FOLDER, results_filename)
                with open(results_path, "w") as results_file:
                    results_file.write(
                        str(raw_result)
                    )  # Save raw_result or formatted_result as needed
                print(f"Results saved to {results_path}")
            except Exception as e:
                print(f"Error processing PDF: {str(e)}")
                return f"Error processing PDF: {str(e)}", 500

            raw_cards = ""
            for i in range(1, 7):
                if i in raw_result:
                    # Format the overall result to include headings and bold scores
                    result_text = raw_result[i]["overall_result"]
                    # Add bold to scores (e.g., "Score: 4/5" becomes "Score: **4/5**")
                    result_text = result_text.replace("Score: ", "Score: **")
                    result_text = result_text.replace("/5", "/5**")

                    converted_overall = markdown.markdown(
                        result_text,
                        extensions=[
                            "extra",
                            "codehilite",
                            "toc",
                            "sane_lists",
                            "smarty",
                            "admonition",
                            "attr_list",
                            "footnotes",
                            "nl2br",
                            "wikilinks",
                            "meta",
                        ],
                    )
                    converted_agents = [
                        markdown.markdown(
                            agent_res,
                            extensions=[
                                "extra",
                                "codehilite",
                                "toc",
                                "sane_lists",
                                "smarty",
                                "admonition",
                                "attr_list",
                                "footnotes",
                                "nl2br",
                                "wikilinks",
                                "meta",
                            ],
                        )
                        for agent_res in raw_result[i]["per_agent_result"]
                    ]

                    # Generate agent details sections
                    agent_sections = ""
                    for idx, agent_result in enumerate(
                        raw_result[i]["per_agent_result"]
                    ):
                        agent_id = f"agent_{i}_{idx}"

                        # Get the agent name from the roles dictionary
                        agent_name = (
                            roles[str(i)][idx]
                            if str(i) in roles and idx < len(roles[str(i)])
                            else f"Agent {idx + 1}"
                        )

                        agent_content = markdown.markdown(
                            agent_result,
                            extensions=[
                                "extra",
                                "codehilite",
                                "toc",
                                "sane_lists",
                                "smarty",
                                "admonition",
                                "attr_list",
                                "footnotes",
                                "nl2br",
                                "wikilinks",
                                "meta",
                            ],
                        )

                        agent_sections += f"""
                            <div class="agent-section">
                                <button class="btn-show-agent" onclick="toggleVisibility(this, '{agent_id}')">
                                    <i class="fas fa-chevron-down me-2"></i>{idx + 1}. {agent_name}
                                </button>
                                <div id="{agent_id}" class="hidden agent-details" style="display: none;">
                                    <div class="detail-item">{agent_content}</div>
                                </div>
                            </div>
                        """

                    descriptions = [
                        wf_persona["Workforce_description"] for wf_persona in PERSONAS
                    ]
                    card = f"""
                        <div class="card raw-card">
                            <h1 class="workforce-heading">{descriptions[i-1]}</h1>
                            <div class="result-section">
                                <h3 class="section-heading">Overall Assessment</h3>
                                <div class="result-content">{converted_overall}</div>
                            </div>
                            <button class="btn-show-more" onclick="toggleVisibility(this, 'agent_list_{i}')">
                                <i class="fas fa-chevron-down me-2"></i>Show More
                            </button>
                            <div id="agent_list_{i}" class="hidden agents-list" style="display: none;">
                                {agent_sections}
                            </div>
                        </div>
                    """
                    raw_cards += card

            final_output = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>SLR Evaluation Results</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                <style>
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                        font-family: 'Inter', sans-serif;
                    }}
                    
                    body {{
                        background-color: #f0f4f8;
                        color: #2d3748;
                        line-height: 1.6;
                        padding: 2rem;
                    }}
                    
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    
                    h2 {{
                        color: #1a365d;
                        margin: 2rem 0;
                        font-weight: 600;
                        text-align: center;
                    }}
                    
                    .card {{
                        background: white;
                        border-radius: 12px;
                        padding: 1.25rem;
                        margin-bottom: 1rem;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}
                    
                    .workforce-heading {{
                        color: #2b6cb0;
                        font-size: 1.25rem;
                        margin-bottom: 0.75rem;
                        padding-bottom: 0.5rem;
                        border-bottom: 1px solid #e2e8f0;
                    }}
                    
                    .section-heading {{
                        color: #2c5282;
                        font-size: 1.1rem;
                        margin-bottom: 0.5rem;
                    }}
                    
                    .result-section {{
                        background: #f8fafc;
                        padding: 1rem;
                        border-radius: 8px;
                        margin-bottom: 0.75rem;
                    }}
                    
                    .result-content {{
                        line-height: 1.4;
                    }}
                    
                    .result-content p {{
                        margin: 0.5rem 0;
                    }}
                    
                    .result-content p:first-child {{
                        margin-top: 0;
                    }}
                    
                    .result-content p:last-child {{
                        margin-bottom: 0;
                    }}
                    
                    .btn-show-more, .btn-show-agent {{
                        background-color: #3182ce;
                        color: white;
                        border: none;
                        padding: 0.5rem 1rem;
                        border-radius: 6px;
                        cursor: pointer;
                        font-size: 0.875rem;
                        transition: all 0.2s ease;
                        margin: 0.5rem 0;
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                        width: fit-content;
                    }}
                    
                    .btn-show-agent {{
                        background-color: #4a5568;
                        font-size: 0.9rem;
                        padding: 0.75rem 1.2rem;
                        width: 100%;
                        text-align: left;
                        border-radius: 8px;
                        transition: all 0.2s ease;
                        margin-bottom: 0.5rem;
                        white-space: normal;
                        line-height: 1.4;
                    }}
                    
                    .btn-show-more:hover, .btn-show-agent:hover {{
                        transform: translateY(-1px);
                        background-color: #2d3748;
                    }}
                    
                    .agent-section {{
                        background: #f8fafc;
                        padding: 0.75rem;
                        border-radius: 8px;
                    }}
                    
                    .agent-details {{
                        margin-top: 1rem;
                        padding: 0.5rem;
                    }}
                    
                    .agent-details .detail-item {{
                        background: white;
                        padding: 1.5rem;
                        border-radius: 8px;
                        border-left: 4px solid #3182ce;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                    }}
                    
                    .hidden {{
                        display: none;
                        margin-top: 0.75rem;
                    }}
                    
                    .agents-list {{
                        display: flex;
                        flex-direction: column;
                        gap: 0.5rem;
                    }}
                    
                    .detail-item {{
                        background: white;
                        padding: 1rem;
                        border-radius: 8px;
                        border-left: 3px solid #3182ce;
                        margin-top: 0.5rem;
                    }}
                    
                    .detail-item p {{
                        margin: 0.5rem 0;
                    }}
                    
                    .btn-go-back {{
                        position: fixed;
                        bottom: 2rem;
                        left: 2rem;
                        background-color: #3182ce;
                        color: white;
                        width: 3.5rem;
                        height: 3.5rem;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        text-decoration: none;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                        transition: all 0.2s ease;
                    }}
                    
                    .btn-go-back:hover {{
                        transform: scale(1.1);
                        background-color: #2c5282;
                    }}
                    
                    strong {{
                        color: #2c5282;
                    }}
                    
                    /* Style for scores */
                    p strong {{
                        color: #2b6cb0;
                        font-size: 1em;
                    }}
                    
                    /* Responsive adjustments */
                    @media (max-width: 768px) {{
                        body {{
                            padding: 0.75rem;
                        }}
                        
                        .card {{
                            padding: 1rem;
                        }}
                        
                        .result-section,
                        .detail-item {{
                            padding: 0.75rem;
                        }}
                    }}
                    
                    .main-header {{
                        text-align: center;
                        padding: 2rem 0;
                        background: linear-gradient(135deg, #2c5282, #3182ce);
                        color: white;
                        margin-bottom: 2rem;
                        border-radius: 12px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}
                    
                    .main-header h1 {{
                        font-size: 2rem;
                        margin-bottom: 0.5rem;
                    }}
                    
                    .main-header p {{
                        font-size: 1.1rem;
                        opacity: 0.9;
                    }}
                    
                    .agent-name {{
                        color: #2b6cb0;
                        font-size: 1.2rem;
                        margin-bottom: 1rem;
                        padding-bottom: 0.5rem;
                        border-bottom: 1px solid #e2e8f0;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="main-header">
                        <h1>SLR Paper Evaluator using LLMs</h1>
                        <p>Automated Systematic Literature Review Analysis Tool</p>
                    </div>
                    <h2>Analysis Results for "{paper_title}"</h2>
                {raw_cards}
                </div>

                <a href="/" class="btn-go-back" title="Go Back">
                    <i class="fas fa-arrow-left"></i>
                </a>
                
                <script>
                    function toggleVisibility(btn, id) {{
                        const content = document.getElementById(id);
                        const isHidden = content.style.display === "none" || content.style.display === "";
                        const icon = btn.querySelector('i');
                        
                        content.style.display = isHidden ? "block" : "none";
                        icon.className = isHidden ? "fas fa-chevron-up me-2" : "fas fa-chevron-down me-2";
                    }}
                </script>
            </body>
            </html>
            """
            return render_template_string(final_output, raw_result=raw_result)

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return f"An unexpected error occurred: {str(e)}", 500

    # GET request: Show upload form
    return render_upload_form()


def render_upload_form():
    # This function returns the HTML for the upload form
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MAS-SLR Analysis</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Inter', sans-serif;
            }
            
            body {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #f6f9fc, #edf2f7);
                padding: 2rem;
            }
            
            .container {
                width: 100%;
                max-width: 480px;
                background: white;
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            }
            
            h1 {
                color: #2d3748;
                margin-bottom: 2rem;
                text-align: center;
                font-weight: 600;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            label {
                display: block;
                margin-bottom: 0.5rem;
                color: #4a5568;
                font-weight: 500;
            }
            
            input[type="text"],
            input[type="file"] {
                width: 100%;
                padding: 0.75rem;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                font-size: 1rem;
                transition: border-color 0.2s ease;
            }
            
            input[type="text"]:focus,
            input[type="file"]:focus {
                outline: none;
                border-color: #4299e1;
            }
            
            .file-input-wrapper {
                position: relative;
                margin-top: 0.5rem;
            }
            
            .file-input-wrapper input[type="file"] {
                cursor: pointer;
            }
            
            button[type="submit"] {
                width: 100%;
                padding: 0.75rem;
                background-color: #4299e1;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1rem;
                cursor: pointer;
                transition: background-color 0.2s ease;
            }
            
            button[type="submit"]:hover {
                background-color: #3182ce;
            }

            /* Disabled button styles */
            button[type="submit"]:disabled {
                background-color: #b0c4de; /* Light gray color */
                cursor: not-allowed; /* Change cursor to indicate it's disabled */
                opacity: 0.6; /* Make it look faded */
            }

            /* Loading indicator styles */
            #loading {
                display: none; /* Hidden by default */
                text-align: center;
                margin-top: 20px;
            }
        </style>
        <script>
            function showLoading() {
                document.getElementById('loading').style.display = 'block'; // Show loading indicator
                document.querySelector('button[type="submit"]').disabled = true; // Disable the submit button
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>MAS-SLR Analysis</h1>
            <form method="POST" enctype="multipart/form-data" onsubmit="showLoading()">
                <div class="form-group">
                    <label for="paper_title">
                        <i class="fas fa-heading icon"></i>Paper Title
                    </label>
                    <input type="text" 
                           id="paper_title" 
                           name="paper_title" 
                           placeholder="Enter the title of your paper"
                           required>
                </div>
                
                <div class="form-group">
                    <label for="paper_pdf">
                        <i class="fas fa-file-pdf icon"></i>Upload PDF
                    </label>
                    <div class="file-input-wrapper">
                        <input type="file" 
                               id="paper_pdf" 
                               name="paper_pdf" 
                               accept=".pdf"
                               required>
                    </div>
                </div>
                
                <button type="submit">
                    <i class="fas fa-upload"></i>
                    Analyze Paper
                </button>
            </form>
            <div id="loading">
                <p>Processing your request, please wait...</p>
                <i class="fas fa-spinner fa-spin"></i> <!-- Optional spinner icon -->
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True, port=PORT)