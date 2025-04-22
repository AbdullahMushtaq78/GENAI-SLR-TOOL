from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
import os
import re
import markdown
from main import demo_output, start_processing_SLR_pdf
from personas import PERSONAS, roles
from SLR_GPT import SLR_GPT_Agent, SLR_GPT

# Import our modular components
from static_styles import SOCIETY_COLORS, generate_society_css
from html_templates import render_upload_form
from utils_app import get_unique_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

PORT = 5001

raw_result = None
ocr = None

# Initialize the chat agent
chat_agent = None

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
                global raw_result, ocr, chat_agent
                raw_result, ocr = demo_output(pdf_path, paper_title)
                chat_agent = SLR_GPT_Agent(ocr, raw_result)

                # raw_result, ocr = start_processing_SLR_pdf(pdf_path, paper_title)
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

                    # Additional processing to add our custom class to scores
                    # Instead of individual replacements, use a more general approach that works for all scores
                    result_text = re.sub(r'\*\*([\d\.]+/5)\*\*', r'<strong class="score-value">\1</strong>', result_text)
                    # Keep the old individual replacements as fallback just in case
                    if "**" in result_text and "/5**" in result_text:
                        result_text = result_text.replace("**4/5**", "<strong class='score-value'>4/5</strong>")
                        result_text = result_text.replace("**3/5**", "<strong class='score-value'>3/5</strong>")
                        result_text = result_text.replace("**5/5**", "<strong class='score-value'>5/5</strong>")
                        result_text = result_text.replace("**2/5**", "<strong class='score-value'>2/5</strong>")
                        result_text = result_text.replace("**1/5**", "<strong class='score-value'>1/5</strong>")

                    converted_overall = markdown.markdown(
                        result_text,
                        extensions=[    "abbr",
                                        "attr_list",
                                        "def_list",
                                        "fenced_code",
                                        "footnotes",
                                        "tables",
                                        "admonition",
                                        "codehilite",
                                        "meta",
                                        "nl2br",
                                        "sane_lists",
                                        "smarty",
                                        "toc",
                                        "wikilinks",

                                        "pymdownx.extra",
                                        "pymdownx.emoji",
                                        "pymdownx.tasklist",
                                        "pymdownx.superfences",
                                        "pymdownx.magiclink",
                                        "pymdownx.highlight",
                                        "pymdownx.keys",
                                        "pymdownx.arithmatex",
                                        "pymdownx.caret",
                                        "pymdownx.mark",
                                        "pymdownx.tilde",
                                        "pymdownx.smartsymbols",
                                        "pymdownx.betterem",
                                        "pymdownx.escapeall",
                                        "pymdownx.progressbar",
                                        "pymdownx.inlinehilite",
                                        "pymdownx.snippets",
                                        "pymdownx.details",
                                        "pymdownx.tabbed"
                                    ],
                    )
                    converted_agents = [
                        markdown.markdown(
                            agent_res,
                            extensions=[    "abbr",
                                        "attr_list",
                                        "def_list",
                                        "fenced_code",
                                        "footnotes",
                                        "tables",
                                        "admonition",
                                        "codehilite",
                                        "meta",
                                        "nl2br",
                                        "sane_lists",
                                        "smarty",
                                        "toc",
                                        "wikilinks",

                                        "pymdownx.extra",
                                        "pymdownx.emoji",
                                        "pymdownx.tasklist",
                                        "pymdownx.superfences",
                                        "pymdownx.magiclink",
                                        "pymdownx.highlight",
                                        "pymdownx.keys",
                                        "pymdownx.arithmatex",
                                        "pymdownx.caret",
                                        "pymdownx.mark",
                                        "pymdownx.tilde",
                                        "pymdownx.smartsymbols",
                                        "pymdownx.betterem",
                                        "pymdownx.escapeall",
                                        "pymdownx.progressbar",
                                        "pymdownx.inlinehilite",
                                        "pymdownx.snippets",
                                        "pymdownx.details",
                                        "pymdownx.tabbed"
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
                            extensions=[    "abbr",
                                        "attr_list",
                                        "def_list",
                                        "fenced_code",
                                        "footnotes",
                                        "tables",
                                        "admonition",
                                        "codehilite",
                                        "meta",
                                        "nl2br",
                                        "sane_lists",
                                        "smarty",
                                        "toc",
                                        "wikilinks",

                                        "pymdownx.extra",
                                        "pymdownx.emoji",
                                        "pymdownx.tasklist",
                                        "pymdownx.superfences",
                                        "pymdownx.magiclink",
                                        "pymdownx.highlight",
                                        "pymdownx.keys",
                                        "pymdownx.arithmatex",
                                        "pymdownx.caret",
                                        "pymdownx.mark",
                                        "pymdownx.tilde",
                                        "pymdownx.smartsymbols",
                                        "pymdownx.betterem",
                                        "pymdownx.escapeall",
                                        "pymdownx.progressbar",
                                        "pymdownx.inlinehilite",
                                        "pymdownx.snippets",
                                        "pymdownx.details",
                                        "pymdownx.tabbed"
                                    ],
                        )

                        # Define color class based on agent index
                        agent_color_class = f"agent-color-{idx % 5}"
                        
                        # Define unique icon for each agent type
                        agent_icons = [
                            "fa-user-graduate",  # Scholar/academic icon
                            "fa-chart-line",     # Data analyst icon
                            "fa-search",         # Investigator icon
                            "fa-clipboard-check", # Reviewer icon
                            "fa-comments"        # Discussion icon
                        ]
                        agent_icon = agent_icons[idx % 5]

                        agent_sections += f"""
                            <div class="agent-section {agent_color_class}">
                                <button class="btn-show-agent {agent_color_class}" onclick="toggleVisibility(this, '{agent_id}')">
                                    <span class="agent-number">{idx + 1}</span>
                                    <i class="fas {agent_icon} agent-icon"></i>
                                    <span class="agent-name">{agent_name}</span>
                                    <span class="expand-indicator"><i class="fas fa-chevron-down"></i></span>
                                </button>
                                <div id="{agent_id}" class="hidden agent-details" style="display: none;">
                                    <div class="detail-item {agent_color_class}">{agent_content}</div>
                                </div>
                            </div>
                        """

                    descriptions = [
                        wf_persona["Workforce_description"] for wf_persona in PERSONAS
                    ]
                    card = f"""
                        <div class="card raw-card society-{i}">
                            <h1 class="workforce-heading">{descriptions[i-1]}</h1>
                            <div class="result-section">
                                <h3 class="section-heading">Overall Assessment</h3>
                                <div class="result-content">{converted_overall}</div>
                            </div>
                            <button class="btn-show-more" onclick="toggleVisibility(this, 'agent_list_{i}')">
                                <i class="fas fa-chevron-down"></i>Show More
                            </button>
                            <div id="agent_list_{i}" class="hidden agents-list" style="display: none;">
                                {agent_sections}
                            </div>
                        </div>
                    """
                    raw_cards += card

            final_output = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <title>SLR Evaluation Results</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Montserrat:wght@700;800&display=swap" rel="stylesheet">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                <style>
                    :root {{
                        --primary-color: #6366f1;
                        --primary-dark: #4f46e5;
                        --primary-light: #818cf8;
                        --secondary-color: #ec4899;
                        --bg-color: #f8fafc;
                        --card-bg: #ffffff;
                        --text-primary: #1e293b;
                        --text-secondary: #64748b;
                        --border-color: #e2e8f0;
                        --success-color: #22c55e;
                        --error-color: #ef4444;
                        --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
                        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                        --transition-base: all 0.3s ease;
                        --transition-bounce: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
                    }}
                    
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                        font-family: 'Poppins', sans-serif;
                    }}
                    
                    body {{
                        background-color: #f0f9ff;
                        color: var(--text-primary);
                        line-height: 1.6;
                        padding: 2rem;
                        position: relative;
                        min-height: 100vh;
                    }}
                    
                    body::before {{
                        content: "";
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%236366f1' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
                        opacity: 0.7;
                        z-index: -1;
                    }}
                    
                    /* Subtle gradient background */
                    body::after {{
                        content: "";
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%);
                        z-index: -2;
                    }}
                    
                    /* Add subtle top and bottom page accents */
                    .page-accent-top {{
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 5px;
                        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                        z-index: 1000;
                    }}
                    
                    .page-accent-bottom {{
                        position: fixed;
                        bottom: 0;
                        left: 0;
                        width: 100%;
                        height: 5px;
                        background: linear-gradient(90deg, var(--secondary-color), var(--primary-color));
                        z-index: 1000;
                    }}
                    
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    
                    h2 {{
                        color: var(--text-primary);
                        margin: 2rem 0;
                        font-weight: 700;
                        text-align: center;
                        font-size: 1.75rem;
                        letter-spacing: -0.01em;
                        font-family: 'Montserrat', sans-serif;
                    }}
                    
                    .card {{
                        background: var(--card-bg);
                        border-radius: 16px;
                        padding: 1.75rem;
                        margin-bottom: 2rem;
                        box-shadow: var(--shadow-lg);
                        border: 1px solid rgba(255, 255, 255, 0.8);
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                        position: relative;
                        overflow: hidden;
                    }}
                    
                    .card::before {{
                        content: "";
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 7px;
                        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                    }}
                    
                    .card::after {{
                        content: "";
                        position: absolute;
                        top: 7px;
                        left: 0;
                        width: 100%;
                        height: calc(100% - 7px);
                        background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 20.5V18H0v-2h20v-2H0v-2h20v-2H0V8h20V6H0V4h20V2H0V0h22v20h2V0h2v20h2V0h2v20h2V0h2v20h2V0h2v20h2v2H20v-1.5zM0 20h2v20H0V20zm4 0h2v20H4V20zm4 0h2v20H8V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20z' fill='%236366f1' fill-opacity='0.02' fill-rule='evenodd'/%3E%3C/svg%3E");
                        opacity: 0.6;
                        z-index: 0;
                        pointer-events: none;
                    }}
                    
                    .card:hover {{
                        transform: translateY(-3px);  /* Reduced from -5px */
                        box-shadow: var(--shadow-lg);  /* Changed from var(--shadow-xl) to var(--shadow-lg) */
                    }}
                    
                    .workforce-heading {{
                        color: var(--primary-dark);
                        font-size: 1.35rem;
                        margin-bottom: 1.25rem;
                        padding-bottom: 0.75rem;
                        border-bottom: 1px solid var(--border-color);
                        font-weight: 600;
                        position: relative;
                        z-index: 1;
                        font-family: 'Montserrat', sans-serif;
                    }}
                    
                    .section-heading {{
                        color: var(--text-primary);
                        font-size: 1.15rem;
                        margin-bottom: 0.85rem;
                        font-weight: 600;
                        position: relative;
                        z-index: 1;
                        display: flex;
                        align-items: center;
                    }}
                    
                    .section-heading::before {{
                        content: "";
                        display: inline-block;
                        width: 12px;
                        height: 12px;
                        background-color: var(--primary-color);
                        border-radius: 50%;
                        margin-right: 0.5rem;
                        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
                    }}
                    
                    .result-section {{
                        background: rgba(255, 255, 255, 0.6);
                        padding: 1.5rem;
                        border-radius: 12px;
                        margin-bottom: 1.5rem;
                        border-left: 4px solid var(--primary-color);
                        transition: var(--transition-base);
                        position: relative;
                        overflow: hidden;
                        backdrop-filter: blur(10px);
                        box-shadow: var(--shadow-md);
                    }}
                    
                    .result-section::after {{
                        content: "";
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(90deg, rgba(99, 102, 241, 0.05) 0%, rgba(79, 70, 229, 0.05) 100%);
                        opacity: 0;
                        transition: opacity 0.3s ease;
                        z-index: 0;
                        pointer-events: none;
                    }}
                    
                    .result-section:hover {{
                        transform: translateY(-2px);  /* Reduced from -3px */
                        box-shadow: var(--shadow-md);  /* Changed from var(--shadow-lg) to var(--shadow-md) */
                        border-left-color: var(--secondary-color);
                    }}
                    
                    .result-section:hover::after {{
                        opacity: 1;
                    }}
                    
                    .result-content {{
                        line-height: 1.6;
                        color: var(--text-secondary);
                        position: relative;
                        z-index: 1;
                        font-size: 0.95rem;
                    }}
                    
                    .result-content strong {{
                        color: var(--primary-color);
                        font-weight: 600;
                        transition: var(--transition-base);
                    }}
                    
                    /* Style for scores - we'll add a class in the markdown processing */
                    .score-value {{
                        display: inline-block;
                        padding: 0.15rem 0.75rem;
                        background-color: rgba(99, 102, 241, 0.1);
                        border-radius: 12px;
                        transition: var(--transition-base);
                        font-family: "Poppins", sans-serif;
                        font-weight: 600;
                        color: var(--primary-dark);
                        box-shadow: var(--shadow-sm);
                    }}
                    
                    .result-section:hover .score-value {{
                        background-color: rgba(99, 102, 241, 0.15);
                        transform: translateY(-1px) scale(1.05);
                        box-shadow: 0 3px 10px rgba(99, 102, 241, 0.2);
                    }}
                    
                    .result-section:hover .result-content strong {{
                        color: var(--secondary-color);
                    }}
                    
                    /* Paper title display */
                    .paper-title-container {{
                        margin: 2rem 0 3rem;
                        text-align: center;
                        position: relative;
                        padding: 0 1rem;
                    }}
                    
                    .paper-title-wrapper {{
                        max-width: 80%;
                        margin: 0 auto;
                        position: relative;
                        background: rgba(255, 255, 255, 0.8);
                        border-radius: 16px;
                        padding: 1.75rem 2rem;
                        box-shadow: var(--shadow-lg);
                        border: 1px solid rgba(255, 255, 255, 0.5);
                        overflow: hidden;
                        backdrop-filter: blur(10px);
                        animation: fadeIn 1s ease forwards;
                    }}
                    
                    .paper-title-wrapper::before {{
                        content: "";
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 7px;
                        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                    }}
                    
                    .paper-title {{
                        font-family: 'Montserrat', sans-serif;
                        font-size: 1.35rem;
                        font-weight: 600;
                        color: var(--text-primary);
                        line-height: 1.5;
                        margin: 0;
                        text-align: center;
                    }}
                    
                    .paper-title-label {{
                        font-size: 0.85rem;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                        color: var(--text-secondary);
                        font-weight: 600;
                        margin-bottom: 0.5rem;
                        display: block;
                        text-align: center;
                    }}
                    
                    @media (max-width: 768px) {{
                        .paper-title-wrapper {{
                            max-width: 90%;
                            padding: 1.5rem 1.75rem;
                        }}
                        
                        .paper-title {{
                            font-size: 1.15rem;
                        }}
                    }}
                    
                    @media (max-width: 480px) {{
                        .paper-title-wrapper {{
                            max-width: 100%;
                            padding: 1.25rem 1.5rem;
                        }}
                        
                        .paper-title {{
                            font-size: 1.05rem;
                        }}
                    }}
                    
                    /* Chatbot UI elements with improved styling and animations */
                    .chat-btn {{
                        position: fixed;
                        top: 2rem;
                        right: 2rem;
                        width: 3.75rem;
                        height: 3.75rem;
                        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                        color: white;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        cursor: pointer;
                        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
                        transition: var(--transition-bounce);
                        z-index: 1000;
                    }}
                    
                    .chat-btn i {{
                        font-size: 1.5rem;
                        transition: transform 0.3s ease;
                    }}
                    
                    .chat-btn:hover {{
                        transform: scale(1.1) rotate(5deg);
                        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
                    }}
                    
                    .chat-btn:hover i {{
                        transform: scale(1.1);
                    }}
                    
                    .chat-overlay {{
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-color: rgba(15, 23, 42, 0.75);
                        backdrop-filter: blur(5px);
                        z-index: 1001;
                        display: none;
                        align-items: center;
                        justify-content: center;
                        opacity: 0;
                        transition: opacity 0.3s ease;
                    }}
                    
                    .chat-overlay.visible {{
                        opacity: 1;
                    }}
                    
                    .chat-container {{
                        width: 70%;
                        height: 80vh;
                        background-color: white;
                        border-radius: 20px;
                        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
                        display: flex;
                        flex-direction: column;
                        overflow: hidden;
                        transform: translateY(30px);
                        opacity: 0;
                        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s ease;
                        border: 1px solid rgba(255, 255, 255, 0.1);
                    }}
                    
                    .chat-overlay.visible .chat-container {{
                        transform: translateY(0);
                        opacity: 1;
                    }}
                    
                    .chat-header {{
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        padding: 1.25rem 1.75rem;
                        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                        color: white;
                        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    }}
                    
                    .chat-header h3 {{
                        margin: 0;
                        font-weight: 600;
                        font-size: 1.25rem;
                        letter-spacing: -0.01em;
                        display: flex;
                        align-items: center;
                        font-family: 'Montserrat', sans-serif;
                    }}
                    
                    .chat-header h3 i {{
                        margin-right: 0.75rem;
                        font-size: 1.1rem;
                    }}
                    
                    .close-chat {{
                        background: rgba(255, 255, 255, 0.15);
                        border: none;
                        color: white;
                        font-size: 1.25rem;
                        cursor: pointer;
                        transition: var(--transition-base);
                        width: 2.25rem;
                        height: 2.25rem;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }}
                    
                    .close-chat:hover {{
                        transform: rotate(90deg);
                        background-color: rgba(255, 255, 255, 0.25);
                    }}
                    
                    .chat-body {{
                        flex: 1;
                        padding: 1.75rem;
                        overflow-y: auto;
                        background-color: #f8fafc;
                        scrollbar-width: thin;
                        scrollbar-color: #cbd5e0 #f8fafc;
                    }}
                    
                    .chat-body::-webkit-scrollbar {{
                        width: 6px;
                    }}
                    
                    .chat-body::-webkit-scrollbar-track {{
                        background: #f8fafc;
                    }}
                    
                    .chat-body::-webkit-scrollbar-thumb {{
                        background-color: #cbd5e0;
                        border-radius: 6px;
                    }}
                    
                    .chat-messages {{
                        display: flex;
                        flex-direction: column;
                        gap: 1rem;
                    }}
                    
                    .message {{
                        max-width: 80%;
                        padding: 1rem 1.25rem;
                        border-radius: 18px;
                        line-height: 1.5;
                        animation: fadeIn 0.3s ease;
                        box-shadow: var(--shadow-md);
                        font-size: 0.95rem;
                    }}
                    
                    @keyframes fadeIn {{
                        from {{ opacity: 0; transform: translateY(10px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}
                    
                    .user-message {{
                        align-self: flex-end;
                        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                        color: white;
                        border-bottom-right-radius: 4px;
                    }}
                    
                    .bot-message {{
                        align-self: flex-start;
                        background-color: white;
                        color: var(--text-primary);
                        border-bottom-left-radius: 4px;
                        border: 1px solid var(--border-color);
                    }}
                    
                    .chat-input-container {{
                        padding: 1.25rem 1.5rem;
                        background-color: white;
                        border-top: 1px solid var(--border-color);
                        display: flex;
                        gap: 0.75rem;
                        align-items: flex-end;
                    }}
                    
                    .chat-input {{
                        flex: 1;
                        padding: 1rem 1.25rem;
                        border: 1px solid var(--border-color);
                        border-radius: 12px;
                        font-size: 0.95rem;
                        resize: none;
                        max-height: 150px;
                        transition: var(--transition-base);
                        font-family: 'Poppins', sans-serif;
                    }}
                    
                    .chat-input:focus {{
                        outline: none;
                        border-color: var(--primary-color);
                        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
                    }}
                    
                    .send-btn {{
                        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                        color: white;
                        border: none;
                        padding: 0.9rem;
                        width: 3.5rem;
                        height: 3.5rem;
                        border-radius: 50%;
                        cursor: pointer;
                        font-weight: 500;
                        transition: var(--transition-base);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
                    }}
                    
                    .send-btn i {{
                        transition: transform 0.2s ease;
                        font-size: 1.1rem;
                    }}
                    
                    .send-btn:hover {{
                        background: linear-gradient(135deg, var(--primary-dark), var(--primary-color));
                        transform: scale(1.05);
                        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.4);
                    }}
                    
                    .send-btn:hover i {{
                        transform: translateX(2px);
                    }}
                    
                    /* Responsive adjustments for chat UI */
                    @media (max-width: 992px) {{
                        .chat-container {{
                            width: 85%;
                        }}
                    }}
                    
                    @media (max-width: 768px) {{
                        .chat-container {{
                            width: 90%;
                            height: 85vh;
                        }}
                        
                        .chat-btn {{
                            top: 1.5rem;
                            right: 1.5rem;
                            width: 3.25rem;
                            height: 3.25rem;
                        }}
                        
                        .message {{
                            max-width: 85%;
                        }}
                    }}
                    
                    @media (max-width: 480px) {{
                        .chat-container {{
                            width: 95%;
                            height: 90vh;
                        }}
                        
                        .chat-header {{
                            padding: 1rem 1.25rem;
                        }}
                        
                        .chat-body {{
                            padding: 1.25rem;
                        }}
                        
                        body {{
                            padding: 1.25rem;
                        }}
                        
                        .message {{
                            max-width: 90%;
                            padding: 0.9rem 1.1rem;
                        }}
                    }}
                    
                    .btn-show-more {{
                        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                        color: white;
                        border: none;
                        padding: 0.7rem 1.25rem;
                        border-radius: 12px;
                        cursor: pointer;
                        font-size: 0.9rem;
                        transition: var(--transition-base);
                        margin: 1rem 0;
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                        width: fit-content;
                        font-weight: 500;
                        box-shadow: var(--shadow-md);
                    }}
                    
                    .btn-show-more i {{
                        margin-right: 8px;
                        font-size: 0.8rem;
                        transition: transform 0.3s ease;
                    }}
                    
                    .btn-show-more.active i {{
                        transform: rotate(180deg);
                    }}
                    
                    .btn-show-more:hover {{
                        transform: translateY(-2px);
                        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.3);
                    }}
                    
                    .hidden {{
                        display: none;
                        margin-top: 0.75rem;
                    }}
                    
                    .agents-list {{
                        display: flex;
                        flex-direction: column;
                        gap: 0.75rem;
                    }}
                    
                    .detail-item {{
                        background: white;
                        padding: 1.25rem;
                        border-radius: 12px;
                        border-left: 4px solid var(--primary-color);
                        margin-top: 0.75rem;
                    }}
                    
                    .detail-item p {{
                        margin: 0.75rem 0;
                        color: var(--text-secondary);
                    }}
                    
                    .main-header {{
                        text-align: center;
                        padding: 3rem 0;
                        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                        color: white;
                        margin-bottom: 3rem;
                        border-radius: 20px;
                        box-shadow: 0 15px 30px rgba(79, 70, 229, 0.2);
                        position: relative;
                        overflow: hidden;
                        animation: fadeIn 1s ease forwards;
                    }}
                    
                    .main-header::before {{
                        content: "";
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-image: url("data:image/svg+xml,%3Csvg width='52' height='26' viewBox='0 0 52 26' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M10 10c0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4v2c-3.314 0-6-2.686-6-6 0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6zm25.464-1.95l8.486 8.486-1.414 1.414-8.486-8.486 1.414-1.414z' /%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
                        opacity: 0.3;
                    }}
                    
                    .main-header h1 {{
                        font-size: 2.5rem;
                        margin-bottom: 0.75rem;
                        font-weight: 800;
                        letter-spacing: -0.01em;
                        position: relative;
                        font-family: 'Montserrat', sans-serif;
                    }}
                    
                    .main-header p {{
                        font-size: 1.15rem;
                        opacity: 0.9;
                        position: relative;
                        max-width: 80%;
                        margin: 0 auto;
                    }}
                    
                    /* Floating back button with animation */
                    .btn-go-back {{
                        position: fixed;
                        bottom: 2rem;
                        left: 2rem;
                        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                        color: white;
                        width: 3.75rem;
                        height: 3.75rem;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        text-decoration: none;
                        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
                        transition: var(--transition-bounce);
                        z-index: 100;
                    }}
                    
                    .btn-go-back:hover {{
                        transform: scale(1.1) rotate(-5deg);
                        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
                    }}
                    
                    .btn-go-back i {{
                        font-size: 1.25rem;
                        transition: transform 0.3s ease;
                    }}
                    
                    .btn-go-back:hover i {{
                        transform: translateX(-3px);
                    }}
                    
                    /* Animation keyframes */
                    @keyframes fadeIn {{
                        from {{ opacity: 0; transform: translateY(20px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}
                    
                    @keyframes slideInRight {{
                        from {{ opacity: 0; transform: translateX(30px); }}
                        to {{ opacity: 1; transform: translateX(0); }}
                    }}
                    
                    @keyframes slideInLeft {{
                        from {{ opacity: 0; transform: translateX(-30px); }}
                        to {{ opacity: 1; transform: translateX(0); }}
                    }}
                    
                    @keyframes pulse {{
                        0% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }}
                        70% {{ box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }}
                        100% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }}
                    }}
                    
                    /* Apply animations to elements */
                    .main-header {{
                        animation: fadeIn 1s ease forwards;
                    }}
                    
                    .card {{
                        animation: fadeIn 0.6s ease forwards;
                        animation-delay: calc(var(--animation-order, 0) * 0.1s);
                    }}
                    
                    .result-section {{
                        animation: slideInRight 0.6s ease forwards;
                        animation-delay: 0.2s;
                    }}
                    
                    /* Typing indicator style */
                    .typing-indicator {{
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 20px;
                    }}
                    
                    .typing-indicator span {{
                        height: 8px;
                        width: 8px;
                        background: var(--primary-color);
                        border-radius: 50%;
                        display: inline-block;
                        margin: 0 2px;
                        opacity: 0.6;
                        animation: typing 1s infinite;
                    }}
                    
                    .typing-indicator span:nth-child(1) {{
                        animation-delay: 0s;
                    }}
                    
                    .typing-indicator span:nth-child(2) {{
                        animation-delay: 0.2s;
                    }}
                    
                    .typing-indicator span:nth-child(3) {{
                        animation-delay: 0.4s;
                    }}
                    
                    @keyframes typing {{
                        0% {{ transform: translateY(0); }}
                        50% {{ transform: translateY(-5px); }}
                        100% {{ transform: translateY(0); }}
                    }}
                    
                    {generate_society_css()}
                </style>
            </head>
            <body>
                <div class="page-accent-top"></div>
                <div class="container">
                    <div class="main-header">
                        <h1>SLR Paper Evaluator</h1>
                        <p>Automated Systematic Literature Review Analysis Using Advanced Language Models</p>
                    </div>
                    
                    <div class="paper-title-container">
                        <div class="paper-title-wrapper">
                            <div class="paper-title-label">ANALYZING PAPER</div>
                            <div class="paper-title">{paper_title}</div>
                        </div>
                    </div>
                    
                    <h2>Detailed Analysis Results</h2>
                    
                    {raw_cards}
                </div>

                <a href="/" class="btn-go-back" title="Go Back">
                    <i class="fas fa-arrow-left"></i>
                </a>
                
                <!-- Chatbot button and overlay -->
                <div class="chat-btn" id="chatButton" title="Ask about the paper">
                    <i class="fas fa-robot"></i>
                </div>
                
                <div class="chat-overlay" id="chatOverlay">
                    <div class="chat-container">
                        <div class="chat-header">
                            <h3><i class="fas fa-robot"></i> SLR-GPT Assistant</h3>
                            <button class="close-chat" id="closeChat">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                        <div class="chat-body">
                            <div class="chat-messages" id="chatMessages">
                                <div class="message bot-message">
                                    <p>👋 Hi there! I'm your SLR-GPT Assistant. I can help answer questions about the analysis of your paper. What would you like to know?</p>
                                </div>
                            </div>
                        </div>
                        <div class="chat-input-container">
                            <textarea class="chat-input" id="chatInput" placeholder="Ask me anything about the paper analysis..." rows="1"></textarea>
                            <button class="send-btn" id="sendMessage">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="page-accent-bottom"></div>
                
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        // Add animation order to cards
                        const cards = document.querySelectorAll('.card');
                        cards.forEach((card, index) => {{
                            card.style.setProperty('--animation-order', index + 1);
                        }});
                    }});
                
                    function toggleVisibility(btn, id) {{
                        const content = document.getElementById(id);
                        const isHidden = content.style.display === "none" || content.style.display === "";
                        
                        // Check if this is a show-more button or an agent button
                        const isShowMoreBtn = btn.classList.contains('btn-show-more');
                        
                        if (isShowMoreBtn) {{
                            // For Show More button, just rotate the icon
                            const icon = btn.querySelector('i');
                            
                            if (isHidden) {{
                                content.style.display = "block";
                                icon.className = "fas fa-chevron-up";
                                btn.classList.add('active');
                                btn.innerHTML = '<i class="fas fa-chevron-up"></i>Show Less';
                            }} else {{
                                content.style.display = "none";
                                icon.className = "fas fa-chevron-down";
                                btn.classList.remove('active');
                                btn.innerHTML = '<i class="fas fa-chevron-down"></i>Show More';
                            }}
                        }} else {{
                            // For agent buttons, use the expand indicator
                            const indicator = btn.querySelector('.expand-indicator i');
                            
                            if (isHidden) {{
                                content.style.display = "block";
                                indicator.className = "fas fa-chevron-up";
                                btn.classList.add('active');
                            }} else {{
                                content.style.display = "none";
                                indicator.className = "fas fa-chevron-down";
                                btn.classList.remove('active');
                            }}
                        }}
                    }}
                    
                    // Chatbot functionality with animations
                    document.addEventListener('DOMContentLoaded', function() {{
                        const chatButton = document.getElementById('chatButton');
                        const chatOverlay = document.getElementById('chatOverlay');
                        const closeChat = document.getElementById('closeChat');
                        const chatInput = document.getElementById('chatInput');
                        const sendMessage = document.getElementById('sendMessage');
                        const chatMessages = document.getElementById('chatMessages');
                        
                        // Open chat overlay with animation
                        chatButton.addEventListener('click', function() {{
                            chatOverlay.style.display = 'flex';
                            setTimeout(() => {{
                                chatOverlay.classList.add('visible');
                            }}, 10);
                            chatInput.focus();
                        }});
                        
                        // Close chat overlay with animation
                        function closeOverlay() {{
                            chatOverlay.classList.remove('visible');
                            setTimeout(() => {{
                                chatOverlay.style.display = 'none';
                            }}, 300);
                        }}
                        
                        closeChat.addEventListener('click', closeOverlay);
                        
                        // Close overlay when clicking outside the chat container
                        chatOverlay.addEventListener('click', function(event) {{
                            if (event.target === chatOverlay) {{
                                closeOverlay();
                            }}
                        }});
                        
                        // Send message on Enter key press
                        chatInput.addEventListener('keypress', function(event) {{
                            if (event.key === 'Enter' && !event.shiftKey) {{
                                event.preventDefault();
                                sendUserMessage();
                            }}
                        }});
                        
                        // Send message on button click
                        sendMessage.addEventListener('click', sendUserMessage);
                        
                        function sendUserMessage() {{
                            const message = chatInput.value.trim();
                            if (message) {{
                                // Add user message to chat
                                addMessage(message, 'user');
                                
                                // Clear input and resize
                                chatInput.value = '';
                                chatInput.style.height = 'auto';
                                
                                // Get paper title from the paper title container
                                const paperTitle = document.querySelector('.paper-title').textContent;
                                
                                // Add loading indicator
                                const loadingId = showLoadingMessage();
                                
                                // Send to backend and get response
                                fetch('/chat', {{
                                    method: 'POST',
                                    headers: {{
                                        'Content-Type': 'application/json',
                                    }},
                                    body: JSON.stringify({{
                                        message: message,
                                        paper_title: paperTitle
                                    }})
                                }})
                                .then(response => response.json())
                                .then(data => {{
                                    // Remove loading indicator
                                    removeLoadingMessage(loadingId);
                                    
                                    // Add bot response
                                    addMessage(data.response, 'bot');
                                }})
                                .catch(error => {{
                                    // Remove loading indicator
                                    removeLoadingMessage(loadingId);
                                    
                                    console.error('Error:', error);
                                    addMessage('Sorry, I had trouble processing your request. Please try again.', 'bot');
                                }});
                            }}
                        }}
                        
                        function showLoadingMessage() {{
                            const loadingDiv = document.createElement('div');
                            loadingDiv.classList.add('message', 'bot-message');
                            loadingDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
                            chatMessages.appendChild(loadingDiv);
                            
                            // Scroll to the bottom
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                            
                            return loadingDiv.id = 'loading-' + Date.now();
                        }}
                        
                        function removeLoadingMessage(id) {{
                            const loadingDiv = document.getElementById(id);
                            if (loadingDiv) {{
                                loadingDiv.remove();
                            }}
                        }}
                        
                        function addMessage(text, sender) {{
                            const messageDiv = document.createElement('div');
                            messageDiv.classList.add('message');
                            messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
                            
                            if (sender === 'bot') {{
                                // For bot messages, render HTML content
                                messageDiv.innerHTML = text;
                            }} else {{
                                // For user messages, keep as plain text
                                messageDiv.textContent = text;
                            }}
                            
                            chatMessages.appendChild(messageDiv);
                            
                            // Scroll to the bottom
                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }}
                        
                        // Auto-resize textarea
                        chatInput.addEventListener('input', function() {{
                            this.style.height = 'auto';
                            this.style.height = (this.scrollHeight) + 'px';
                        }});
                    }});
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


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        if not data or 'message' not in data or 'paper_title' not in data:
            return {"response": "Invalid request, message and paper_title required"}, 400
            
        user_message = data['message']
        paper_title = data['paper_title']
        
        global chat_agent
        # Get response from the agent
        response = SLR_GPT(chat_agent, user_message)

        response = markdown.markdown(response, extensions=[    "abbr",
                                        "attr_list",
                                        "def_list",
                                        "fenced_code",
                                        "footnotes",
                                        "tables",
                                        "admonition",
                                        "codehilite",
                                        "meta",
                                        "nl2br",
                                        "sane_lists",
                                        "smarty",
                                        "toc",
                                        "wikilinks",

                                        "pymdownx.extra",
                                        "pymdownx.emoji",
                                        "pymdownx.tasklist",
                                        "pymdownx.superfences",
                                        "pymdownx.magiclink",
                                        "pymdownx.highlight",
                                        "pymdownx.keys",
                                        "pymdownx.arithmatex",
                                        "pymdownx.caret",
                                        "pymdownx.mark",
                                        "pymdownx.tilde",
                                        "pymdownx.smartsymbols",
                                        "pymdownx.betterem",
                                        "pymdownx.escapeall",
                                        "pymdownx.progressbar",
                                        "pymdownx.inlinehilite",
                                        "pymdownx.snippets",
                                        "pymdownx.details",
                                        "pymdownx.tabbed"
                                    ],)
        
            
        return {"response": response}
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return {"response": f"Sorry, I encountered an error processing your request: {str(e)}"}, 500


if __name__ == "__main__":
    app.run(debug=True, port=PORT)