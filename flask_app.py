from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
import os
from main import demo_output, start_processing_SLR_pdf
import markdown
from personas import PERSONAS, roles
import re
from SLR_GPT import SLR_GPT_Agent, SLR_GPT

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

PORT = 5001

raw_result = None
ocr = None

# Society color schemes - this defines colors for each society
SOCIETY_COLORS = {
    1: {
        "name": "indigo",
        "primary": "#312e81",
        "secondary": "#4f46e5",
        "light": "rgba(79, 70, 229, 0.1)",
        "hover": "rgba(79, 70, 229, 0.15)"
    },
    2: {
        "name": "rose-dark",
        "primary": "#831843",
        "secondary": "#be185d",
        "light": "rgba(190, 24, 93, 0.1)",
        "hover": "rgba(190, 24, 93, 0.15)"
    },
    3: {
        "name": "cyan-dark",
        "primary": "#164e63",
        "secondary": "#0e7490",
        "light": "rgba(14, 116, 144, 0.1)",
        "hover": "rgba(14, 116, 144, 0.15)"
    },
    4: {
        "name": "violet-dark",
        "primary": "#4c1d95",
        "secondary": "#7c3aed",
        "light": "rgba(124, 58, 237, 0.1)",
        "hover": "rgba(124, 58, 237, 0.15)"
    },
    5: {
        "name": "slate",
        "primary": "#1e293b",
        "secondary": "#334155",
        "light": "rgba(51, 65, 85, 0.1)",
        "hover": "rgba(51, 65, 85, 0.15)"
    },
    6: {
        "name": "emerald-dark",
        "primary": "#064e3b",
        "secondary": "#047857",
        "light": "rgba(4, 120, 87, 0.1)",
        "hover": "rgba(4, 120, 87, 0.15)"
    }
}


# Function to generate society color CSS
def generate_society_css():
    css = ""
    for society_id, colors in SOCIETY_COLORS.items():
        # Create more subtle hover colors by reducing opacity further
        subtle_light = colors["light"].replace("0.1", "0.05")
        subtle_hover = colors["hover"]  # Reduced from 0.08 to 0.06
        
        css += f"""
            .society-{society_id} .raw-card::before {{
                background: linear-gradient(90deg, {colors['secondary']}, {colors['primary']});
            }}
            
            .society-{society_id} .workforce-heading {{
                color: {colors['primary']};
            }}
            
            .society-{society_id} .section-heading::before {{
                background-color: {colors['secondary']};
                box-shadow: 0 0 0 2px {subtle_light};
            }}
            
            .society-{society_id} .result-section {{
                border-left: 4px solid {colors['secondary']};
            }}
            
            .society-{society_id} .result-section::after {{
                background: linear-gradient(90deg, {subtle_light} 0%, {subtle_light} 100%);
            }}
            
            .society-{society_id} .result-section:hover {{
                border-left-color: {colors['primary']};
            }}
            
            .society-{society_id} .score-value {{
                background-color: {subtle_light};
                color: {colors['primary']};
            }}
            
            .society-{society_id} .result-section:hover .score-value {{
                background-color: {subtle_hover};
                box-shadow: 0 2px 4px {subtle_light};  # Reduced shadow intensity
            }}
            
            .society-{society_id} .btn-show-more {{
                background: linear-gradient(135deg, {colors['secondary']}, {colors['primary']});
            }}
            
            .society-{society_id} .btn-show-more:hover {{
                box-shadow: 0 4px 8px {subtle_light};  # Reduced shadow intensity
            }}
            
            .btn-show-agent {{
                background: rgba(255, 255, 255, 0.85);
                color: var(--text-primary);
                border: none;
                padding: 0.85rem 1.25rem;
                width: 100%;
                text-align: left;
                border-radius: 12px;
                transition: var(--transition-base);
                margin-bottom: 0.75rem;
                white-space: normal;
                line-height: 1.4;
                box-shadow: var(--shadow-md);
                position: relative;
                font-size: 0.95rem;
                overflow: hidden;
                font-weight: 600;
                backdrop-filter: blur(5px);
                border-left: 4px solid transparent;
            }}
            
            .btn-show-agent::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.2));
                opacity: 0.6;
                transition: opacity 0.3s ease;
                z-index: 0;
            }}
            
            .expand-indicator {{
                position: absolute;
                right: 1rem;
                top: 50%;
                transform: translateY(-50%);
                display: flex;
                align-items: center;
                justify-content: center;
                width: 24px;
                height: 24px;
                transition: all 0.2s ease;
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 50%;
                z-index: 1;
            }}
            
            .btn-show-agent .agent-number {{
                display: inline-block;
                background-color: rgba(0, 0, 0, 0.08);
                border-radius: 6px;
                padding: 0.15rem 0.5rem;
                margin-right: 0.6rem;
                font-weight: 700;
                font-size: 0.85rem;
                letter-spacing: 0.02em;
                position: relative;
                z-index: 1;
            }}
            
            .btn-show-agent .agent-icon {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 1.6rem;
                margin-right: 0.5rem;
                text-align: center;
                position: relative;
                z-index: 1;
            }}
            
            .btn-show-agent .agent-name {{
                font-weight: 600;
                letter-spacing: 0.01em;
                position: relative;
                z-index: 1;
            }}
            
            .btn-show-agent:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            }}
            
            .btn-show-agent:hover::before {{
                opacity: 0.9;
            }}
            
            .agent-color-0 .btn-show-agent.agent-color-0 {{
                background: rgba(226, 232, 255, 0.8);
                border-left: 4px solid #4f46e5;
                color: #312e81;
            }}
            
            .agent-color-1 .btn-show-agent.agent-color-1 {{
                background: rgba(209, 250, 229, 0.8);
                border-left: 4px solid #0d9488;
                color: #064e3b;
            }}
            
            .agent-color-2 .btn-show-agent.agent-color-2 {{
                background: rgba(254, 240, 185, 0.8);
                border-left: 4px solid #d97706;
                color: #92400e;
            }}
            
            .agent-color-3 .btn-show-agent.agent-color-3 {{
                background: rgba(253, 224, 235, 0.8);
                border-left: 4px solid #db2777;
                color: #831843;
            }}
            
            .agent-color-4 .btn-show-agent.agent-color-4 {{
                background: rgba(237, 223, 252, 0.8);
                border-left: 4px solid #7c3aed;
                color: #4c1d95;
            }}
            
            .btn-show-agent.active {{
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
            }}
            
            .btn-show-agent.active .expand-indicator {{
                transform: translateY(-50%) rotate(180deg);
                background-color: rgba(0, 0, 0, 0.15);
            }}
            
            .agent-color-0 .btn-show-agent.agent-color-0.active,
            .agent-color-0 .btn-show-agent.agent-color-0:hover {{
                background: rgba(224, 231, 255, 0.9);
                box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
            }}
            
            .agent-color-1 .btn-show-agent.agent-color-1.active,
            .agent-color-1 .btn-show-agent.agent-color-1:hover {{
                background: rgba(204, 251, 241, 0.9);
                box-shadow: 0 8px 20px rgba(20, 184, 166, 0.2);
            }}
            
            .agent-color-2 .btn-show-agent.agent-color-2.active,
            .agent-color-2 .btn-show-agent.agent-color-2:hover {{
                background: rgba(255, 251, 235, 0.9);
                box-shadow: 0 8px 20px rgba(245, 158, 11, 0.2);
            }}
            
            .agent-color-3 .btn-show-agent.agent-color-3.active,
            .agent-color-3 .btn-show-agent.agent-color-3:hover {{
                background: rgba(253, 232, 242, 0.9);
                box-shadow: 0 8px 20px rgba(236, 72, 153, 0.2);
            }}
            
            .agent-color-4 .btn-show-agent.agent-color-4.active,
            .agent-color-4 .btn-show-agent.agent-color-4:hover {{
                background: rgba(243, 232, 255, 0.9);
                box-shadow: 0 8px 20px rgba(139, 92, 246, 0.2);
            }}
            
            .agent-color-0 .btn-show-agent.agent-color-0 .agent-number {{
                background-color: rgba(79, 70, 229, 0.15);
                color: #4338ca;
            }}
            
            .agent-color-1 .btn-show-agent.agent-color-1 .agent-number {{
                background-color: rgba(13, 148, 136, 0.15);
                color: #0f766e;
            }}
            
            .agent-color-2 .btn-show-agent.agent-color-2 .agent-number {{
                background-color: rgba(217, 119, 6, 0.15);
                color: #b45309;
            }}
            
            .agent-color-3 .btn-show-agent.agent-color-3 .agent-number {{
                background-color: rgba(219, 39, 119, 0.15);
                color: #be185d;
            }}
            
            .agent-color-4 .btn-show-agent.agent-color-4 .agent-number {{
                background-color: rgba(124, 58, 237, 0.15);
                color: #6d28d9;
            }}
            
            .agent-color-0 .btn-show-agent.agent-color-0 .expand-indicator {{
                background-color: rgba(79, 70, 229, 0.15);
                color: #4338ca;
            }}
            
            .agent-color-1 .btn-show-agent.agent-color-1 .expand-indicator {{
                background-color: rgba(13, 148, 136, 0.15);
                color: #0f766e;
            }}
            
            .agent-color-2 .btn-show-agent.agent-color-2 .expand-indicator {{
                background-color: rgba(217, 119, 6, 0.15);
                color: #b45309;
            }}
            
            .agent-color-3 .btn-show-agent.agent-color-3 .expand-indicator {{
                background-color: rgba(219, 39, 119, 0.15);
                color: #be185d;
            }}
            
            .agent-color-4 .btn-show-agent.agent-color-4 .expand-indicator {{
                background-color: rgba(124, 58, 237, 0.15);
                color: #6d28d9;
            }}
            
            .agent-section {{
                background: rgba(255, 255, 255, 0.5);
                padding: 0.9rem;
                border-radius: 12px;
                margin-bottom: 1rem;
                transition: var(--transition-base);
                backdrop-filter: blur(10px);
                position: relative;
                overflow: hidden;
                border: 2px solid transparent;
            }}
            
            .agent-section:hover {{
                transform: translateY(-3px);
                box-shadow: var(--shadow-lg);
                background: rgba(255, 255, 255, 0.65);
                border-color: rgba(255, 255, 255, 0.9);
            }}
            
            /* Agent section color variants with gradient backgrounds */
            .agent-section.agent-color-0 {{
                background: linear-gradient(to right, rgba(99, 102, 241, 0.08), rgba(79, 70, 229, 0.03));
                border-left: 4px solid var(--primary-color);
            }}
            
            .agent-section.agent-color-0:hover {{
                background: linear-gradient(to right, rgba(99, 102, 241, 0.12), rgba(79, 70, 229, 0.07));
            }}
            
            .agent-section.agent-color-1 {{
                background: linear-gradient(to right, rgba(20, 184, 166, 0.08), rgba(13, 148, 136, 0.03));
                border-left: 4px solid #0d9488;
            }}
            
            .agent-section.agent-color-1:hover {{
                background: linear-gradient(to right, rgba(20, 184, 166, 0.12), rgba(13, 148, 136, 0.07));
            }}
            
            .agent-section.agent-color-2 {{
                background: linear-gradient(to right, rgba(245, 158, 11, 0.08), rgba(217, 119, 6, 0.03));
                border-left: 4px solid #d97706;
            }}
            
            .agent-section.agent-color-2:hover {{
                background: linear-gradient(to right, rgba(245, 158, 11, 0.12), rgba(217, 119, 6, 0.07));
            }}
            
            .agent-section.agent-color-3 {{
                background: linear-gradient(to right, rgba(236, 72, 153, 0.08), rgba(219, 39, 119, 0.03));
                border-left: 4px solid #db2777;
            }}
            
            .agent-section.agent-color-3:hover {{
                background: linear-gradient(to right, rgba(236, 72, 153, 0.12), rgba(219, 39, 119, 0.07));
            }}
            
            .agent-section.agent-color-4 {{
                background: linear-gradient(to right, rgba(139, 92, 246, 0.08), rgba(124, 58, 237, 0.03));
                border-left: 4px solid #7c3aed;
            }}
            
            .agent-section.agent-color-4:hover {{
                background: linear-gradient(to right, rgba(139, 92, 246, 0.12), rgba(124, 58, 237, 0.07));
            }}
        """
    return css


# Initialize the chat agent
chat_agent = None


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
                    
                    .btn-show-agent {{
                        background: rgba(255, 255, 255, 0.85);
                        color: var(--text-primary);
                        border: none;
                        padding: 0.85rem 1.25rem;
                        width: 100%;
                        text-align: left;
                        border-radius: 12px;
                        transition: var(--transition-base);
                        margin-bottom: 0.75rem;
                        white-space: normal;
                        line-height: 1.4;
                        box-shadow: var(--shadow-md);
                        position: relative;
                        font-size: 0.95rem;
                        overflow: hidden;
                        font-weight: 600;
                        backdrop-filter: blur(5px);
                        border-left: 4px solid transparent;
                    }}
                    
                    .btn-show-agent::before {{
                        content: "";
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(90deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.2));
                        opacity: 0.6;
                        transition: opacity 0.3s ease;
                        z-index: 0;
                    }}
                    
                    .expand-indicator {{
                        position: absolute;
                        right: 1rem;
                        top: 50%;
                        transform: translateY(-50%);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        width: 24px;
                        height: 24px;
                        transition: all 0.2s ease;
                        background-color: rgba(0, 0, 0, 0.1);
                        border-radius: 50%;
                        z-index: 1;
                    }}
                    
                    .btn-show-agent .agent-number {{
                        display: inline-block;
                        background-color: rgba(0, 0, 0, 0.08);
                        border-radius: 6px;
                        padding: 0.15rem 0.5rem;
                        margin-right: 0.6rem;
                        font-weight: 700;
                        font-size: 0.85rem;
                        letter-spacing: 0.02em;
                        position: relative;
                        z-index: 1;
                    }}
                    
                    .btn-show-agent .agent-icon {{
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        width: 1.6rem;
                        margin-right: 0.5rem;
                        text-align: center;
                        position: relative;
                        z-index: 1;
                    }}
                    
                    .btn-show-agent .agent-name {{
                        font-weight: 600;
                        letter-spacing: 0.01em;
                        position: relative;
                        z-index: 1;
                    }}
                    
                    .btn-show-agent:hover {{
                        transform: translateY(-2px);
                        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                    }}
                    
                    .btn-show-agent:hover::before {{
                        opacity: 0.9;
                    }}
                    
                    /* Agent color variations with updated styles - lighter backgrounds with colorful text */
                    .agent-color-0 .btn-show-agent.agent-color-0 {{
                        background: rgba(226, 232, 255, 0.8);
                        border-left: 4px solid #4f46e5;
                        color: #312e81;
                    }}
                    
                    .agent-color-1 .btn-show-agent.agent-color-1 {{
                        background: rgba(209, 250, 229, 0.8);
                        border-left: 4px solid #0d9488;
                        color: #064e3b;
                    }}
                    
                    .agent-color-2 .btn-show-agent.agent-color-2 {{
                        background: rgba(254, 240, 185, 0.8);
                        border-left: 4px solid #d97706;
                        color: #92400e;
                    }}
                    
                    .agent-color-3 .btn-show-agent.agent-color-3 {{
                        background: rgba(253, 224, 235, 0.8);
                        border-left: 4px solid #db2777;
                        color: #831843;
                    }}
                    
                    .agent-color-4 .btn-show-agent.agent-color-4 {{
                        background: rgba(237, 223, 252, 0.8);
                        border-left: 4px solid #7c3aed;
                        color: #4c1d95;
                    }}
                    
                    .btn-show-agent.active {{
                        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
                    }}
                    
                    .btn-show-agent.active .expand-indicator {{
                        transform: translateY(-50%) rotate(180deg);
                        background-color: rgba(0, 0, 0, 0.15);
                    }}
                    
                    /* Active states and hover effects for each color */
                    .agent-color-0 .btn-show-agent.agent-color-0.active,
                    .agent-color-0 .btn-show-agent.agent-color-0:hover {{
                        background: rgba(224, 231, 255, 0.9);
                        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
                    }}
                    
                    .agent-color-1 .btn-show-agent.agent-color-1.active,
                    .agent-color-1 .btn-show-agent.agent-color-1:hover {{
                        background: rgba(204, 251, 241, 0.9);
                        box-shadow: 0 8px 20px rgba(20, 184, 166, 0.2);
                    }}
                    
                    .agent-color-2 .btn-show-agent.agent-color-2.active,
                    .agent-color-2 .btn-show-agent.agent-color-2:hover {{
                        background: rgba(255, 251, 235, 0.9);
                        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.2);
                    }}
                    
                    .agent-color-3 .btn-show-agent.agent-color-3.active,
                    .agent-color-3 .btn-show-agent.agent-color-3:hover {{
                        background: rgba(253, 232, 242, 0.9);
                        box-shadow: 0 8px 20px rgba(236, 72, 153, 0.2);
                    }}
                    
                    .agent-color-4 .btn-show-agent.agent-color-4.active,
                    .agent-color-4 .btn-show-agent.agent-color-4:hover {{
                        background: rgba(243, 232, 255, 0.9);
                        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.2);
                    }}
                    
                    /* Updated agent numbers to match the theme colors */
                    .agent-color-0 .btn-show-agent.agent-color-0 .agent-number {{
                        background-color: rgba(79, 70, 229, 0.15);
                        color: #4338ca;
                    }}
                    
                    .agent-color-1 .btn-show-agent.agent-color-1 .agent-number {{
                        background-color: rgba(13, 148, 136, 0.15);
                        color: #0f766e;
                    }}
                    
                    .agent-color-2 .btn-show-agent.agent-color-2 .agent-number {{
                        background-color: rgba(217, 119, 6, 0.15);
                        color: #b45309;
                    }}
                    
                    .agent-color-3 .btn-show-agent.agent-color-3 .agent-number {{
                        background-color: rgba(219, 39, 119, 0.15);
                        color: #be185d;
                    }}
                    
                    .agent-color-4 .btn-show-agent.agent-color-4 .agent-number {{
                        background-color: rgba(124, 58, 237, 0.15);
                        color: #6d28d9;
                    }}
                    
                    /* Updated expand indicator to match the theme colors */
                    .agent-color-0 .btn-show-agent.agent-color-0 .expand-indicator {{
                        background-color: rgba(79, 70, 229, 0.15);
                        color: #4338ca;
                    }}
                    
                    .agent-color-1 .btn-show-agent.agent-color-1 .expand-indicator {{
                        background-color: rgba(13, 148, 136, 0.15);
                        color: #0f766e;
                    }}
                    
                    .agent-color-2 .btn-show-agent.agent-color-2 .expand-indicator {{
                        background-color: rgba(217, 119, 6, 0.15);
                        color: #b45309;
                    }}
                    
                    .agent-color-3 .btn-show-agent.agent-color-3 .expand-indicator {{
                        background-color: rgba(219, 39, 119, 0.15);
                        color: #be185d;
                    }}
                    
                    .agent-color-4 .btn-show-agent.agent-color-4 .expand-indicator {{
                        background-color: rgba(124, 58, 237, 0.15);
                        color: #6d28d9;
                    }}
                    
                    .agent-section {{
                        background: rgba(255, 255, 255, 0.5);
                        padding: 0.9rem;
                        border-radius: 12px;
                        margin-bottom: 1rem;
                        transition: var(--transition-base);
                        backdrop-filter: blur(10px);
                    }}
                    
                    .agent-section:hover {{
                        transform: translateY(-3px);
                        box-shadow: var(--shadow-lg);
                    }}
                    
                    /* Agent section color variants with gradient backgrounds */
                    .agent-section.agent-color-0 {{
                        background: linear-gradient(to right, rgba(99, 102, 241, 0.08), rgba(79, 70, 229, 0.03));
                        border-left: 4px solid var(--primary-color);
                    }}
                    
                    .agent-section.agent-color-1 {{
                        background: linear-gradient(to right, rgba(20, 184, 166, 0.08), rgba(13, 148, 136, 0.03));
                        border-left: 4px solid #0d9488;
                    }}
                    
                    .agent-section.agent-color-2 {{
                        background: linear-gradient(to right, rgba(245, 158, 11, 0.08), rgba(217, 119, 6, 0.03));
                        border-left: 4px solid #d97706;
                    }}
                    
                    .agent-section.agent-color-3 {{
                        background: linear-gradient(to right, rgba(236, 72, 153, 0.08), rgba(219, 39, 119, 0.03));
                        border-left: 4px solid #db2777;
                    }}
                    
                    .agent-section.agent-color-4 {{
                        background: linear-gradient(to right, rgba(139, 92, 246, 0.08), rgba(124, 58, 237, 0.03));
                        border-left: 4px solid #7c3aed;
                    }}
                    
                    .agent-details {{
                        margin-top: 1rem;
                        padding: 0.5rem;
                    }}
                    
                    .agent-details .detail-item {{
                        background: white;
                        padding: 1.5rem;
                        border-radius: 12px;
                        box-shadow: var(--shadow-md);
                        transition: var(--transition-base);
                        position: relative;
                        z-index: 1;
                        overflow: hidden;
                    }}
                    
                    .agent-details .detail-item::after {{
                        content: "";
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 20.5V18H0v-2h20v-2H0v-2h20v-2H0V8h20V6H0V4h20V2H0V0h22v20h2V0h2v20h2V0h2v20h2V0h2v20h2V0h2v20h2v2H20v-1.5zM0 20h2v20H0V20zm4 0h2v20H4V20zm4 0h2v20H8V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20z' fill='%236366f1' fill-opacity='0.02' fill-rule='evenodd'/%3E%3C/svg%3E");
                        opacity: 0.6;
                        z-index: -1;
                        pointer-events: none;
                    }}
                    
                    .agent-details .detail-item.agent-color-0 {{
                        border-left: 4px solid var(--primary-color);
                    }}
                    
                    .agent-details .detail-item.agent-color-1 {{
                        border-left: 4px solid #0d9488;
                    }}
                    
                    .agent-details .detail-item.agent-color-2 {{
                        border-left: 4px solid #d97706;
                    }}
                    
                    .agent-details .detail-item.agent-color-3 {{
                        border-left: 4px solid #db2777;
                    }}
                    
                    .agent-details .detail-item.agent-color-4 {{
                        border-left: 4px solid #7c3aed;
                    }}
                    
                    .agent-details .detail-item:hover {{
                        box-shadow: var(--shadow-lg);
                        transform: translateY(-2px);
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


def render_upload_form():
    # This function returns the HTML for the upload form
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MAS-SLR Analysis</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Montserrat:wght@700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
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
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
            }
            
            body {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%);
                padding: 2rem;
                position: relative;
                overflow-x: hidden;
            }
            
            body::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%236366f1' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
                z-index: -1;
            }
            
            .container {
                width: 100%;
                max-width: 520px;
                background: var(--card-bg);
                padding: 2.5rem;
                border-radius: 20px;
                box-shadow: var(--shadow-xl);
                position: relative;
                overflow: hidden;
                transform: translateY(0);
                transition: var(--transition-base);
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
            
            .container:hover {
                transform: translateY(-5px);
                box-shadow: var(--shadow-2xl);
            }
            
            .container::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 7px;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            }
            
            .container::after {
                content: "";
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 200px;
                background: radial-gradient(circle at 90% 90%, var(--primary-light) 0%, transparent 55%);
                opacity: 0.1;
                z-index: -1;
            }
            
            h1 {
                color: var(--text-primary);
                margin-bottom: 0.5rem;
                text-align: center;
                font-weight: 700;
                font-size: 2rem;
                letter-spacing: -0.025em;
                font-family: 'Montserrat', sans-serif;
            }
            
            .subtitle {
                color: var(--text-secondary);
                text-align: center;
                margin-bottom: 2rem;
                font-size: 0.95rem;
            }
            
            .form-group {
                margin-bottom: 1.75rem;
            }
            
            label {
                display: block;
                margin-bottom: 0.5rem;
                color: var(--text-primary);
                font-weight: 500;
                font-size: 0.95rem;
                transition: var(--transition-base);
            }
            
            .input-wrapper {
                position: relative;
            }
            
            .input-icon {
                position: absolute;
                left: 1rem;
                top: 50%;
                transform: translateY(-50%);
                color: var(--text-secondary);
                transition: var(--transition-base);
            }
            
            input[type="text"],
            input[type="file"] {
                width: 100%;
                padding: 0.9rem 1rem 0.9rem 2.75rem;
                border: 2px solid var(--border-color);
                border-radius: 12px;
                font-size: 1rem;
                transition: var(--transition-base);
                background-color: white;
                color: var(--text-primary);
            }
            
            input[type="text"]:focus,
            input[type="file"]:focus {
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
            }
            
            input[type="text"]:focus + .input-icon,
            input[type="file"]:focus + .input-icon {
                color: var(--primary-color);
            }
            
            .file-input-wrapper {
                position: relative;
                margin-top: 0.5rem;
            }
            
            .file-drop-area {
                position: relative;
                padding: 2rem;
                border: 2px dashed var(--border-color);
                border-radius: 12px;
                text-align: center;
                transition: var(--transition-base);
                cursor: pointer;
                background-color: rgba(255, 255, 255, 0.5);
            }
            
            .file-drop-area:hover {
                border-color: var(--primary-color);
                background-color: rgba(99, 102, 241, 0.05);
            }
            
            .file-message {
                font-size: 0.95rem;
                color: var(--text-secondary);
                margin-bottom: 0.5rem;
            }
            
            .file-icon {
                font-size: 2rem;
                color: var(--primary-color);
                margin-bottom: 0.5rem;
                transition: var(--transition-base);
            }
            
            .file-drop-area:hover .file-icon {
                transform: translateY(-5px);
            }
            
            input[type="file"] {
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                opacity: 0;
                cursor: pointer;
            }
            
            .btn-submit {
                width: 100%;
                padding: 1rem;
                background: linear-gradient(90deg, var(--primary-color), var(--primary-dark));
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 1rem;
                font-weight: 500;
                cursor: pointer;
                transition: var(--transition-base);
                position: relative;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            }
            
            .btn-submit:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
            }
            
            .btn-submit:active {
                transform: translateY(0);
            }
            
            .btn-submit::after {
                content: "";
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                pointer-events: none;
                background-image: radial-gradient(circle, #fff 10%, transparent 10.01%);
                background-repeat: no-repeat;
                background-position: 50%;
                transform: scale(10, 10);
                opacity: 0;
                transition: transform 0.5s, opacity 1s;
            }
            
            .btn-submit:active::after {
                transform: scale(0, 0);
                opacity: 0.3;
                transition: 0s;
            }
            
            /* Disabled button styles */
            .btn-submit:disabled {
                background: linear-gradient(90deg, #a5b4fc, #818cf8); 
                cursor: not-allowed;
                opacity: 0.7;
                box-shadow: none;
            }
            
            /* Loading indicator styles */
            #loading {
                display: none;
                text-align: center;
                margin-top: 20px;
                padding: 1rem;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(5px);
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }
                100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
            }
            
            .loading-text {
                color: var(--primary-dark);
                font-weight: 500;
                margin-bottom: 0.5rem;
            }
            
            .spinner {
                display: inline-block;
                width: 40px;
                height: 40px;
                border: 4px solid rgba(99, 102, 241, 0.1);
                border-radius: 50%;
                border-top-color: var(--primary-color);
                animation: spin 1s ease-in-out infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            /* Subtle decorative elements */
            .decoration-circle {
                position: absolute;
                border-radius: 50%;
                z-index: -1;
            }
            
            .circle-1 {
                width: 100px;
                height: 100px;
                top: -30px;
                right: -30px;
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(99, 102, 241, 0.3));
            }
            
            .circle-2 {
                width: 80px;
                height: 80px;
                bottom: -20px;
                left: -20px;
                background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(236, 72, 153, 0.3));
            }
            
            /* Responsive styles */
            @media (max-width: 600px) {
                body {
                    padding: 1.5rem;
                }
                
                .container {
                    padding: 1.75rem;
                }
                
                h1 {
                    font-size: 1.75rem;
                }
                
                .subtitle {
                    font-size: 0.85rem;
                }
                
                .file-drop-area {
                    padding: 1.5rem;
                }
                
                .file-icon {
                    font-size: 1.75rem;
                }
            }
            
            /* Animation classes */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .animate-fade-in {
                animation: fadeIn 0.6s ease forwards;
            }
            
            .delay-1 {
                animation-delay: 0.1s;
            }
            
            .delay-2 {
                animation-delay: 0.2s;
            }
            
            .delay-3 {
                animation-delay: 0.3s;
            }
        </style>
        <script>
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
                document.querySelector('.btn-submit').disabled = true;
                return true;
            }
            
            document.addEventListener('DOMContentLoaded', function() {
                // File input handling
                const fileInput = document.getElementById('paper_pdf');
                const fileMessage = document.querySelector('.file-message');
                const originalMessage = fileMessage.textContent;
                
                fileInput.addEventListener('change', function() {
                    if (this.files && this.files[0]) {
                        const fileName = this.files[0].name;
                        fileMessage.textContent = 'Selected: ' + fileName;
                    } else {
                        fileMessage.textContent = originalMessage;
                    }
                });
                
                // Add animation to form elements
                const animatedElements = document.querySelectorAll('.animate-fade-in');
                animatedElements.forEach(element => {
                    element.style.opacity = '0';
                    setTimeout(() => {
                        element.style.opacity = '1';
                    }, 100);
                });
            });
        </script>
    </head>
    <body>
        <div class="container">
            <div class="decoration-circle circle-1"></div>
            <div class="decoration-circle circle-2"></div>
            
            <h1 class="animate-fade-in">MAS-SLR Analysis</h1>
            <p class="subtitle animate-fade-in delay-1">Upload your research paper for systematic literature review analysis</p>
            
            <form method="POST" enctype="multipart/form-data" onsubmit="return showLoading()">
                <div class="form-group animate-fade-in delay-2">
                    <label for="paper_title">Paper Title</label>
                    <div class="input-wrapper">
                        <input type="text" 
                               id="paper_title" 
                               name="paper_title" 
                               placeholder="Enter the title of your paper"
                               required>
                        <i class="fas fa-heading input-icon"></i>
                    </div>
                </div>
                
                <div class="form-group animate-fade-in delay-3">
                    <label for="paper_pdf">Upload PDF</label>
                    <div class="file-drop-area">
                        <i class="fas fa-file-pdf file-icon"></i>
                        <p class="file-message">Drag & drop your PDF file here or click to browse</p>
                        <input type="file" 
                               id="paper_pdf" 
                               name="paper_pdf" 
                               accept=".pdf"
                               required>
                    </div>
                </div>
                
                <button type="submit" class="btn-submit animate-fade-in delay-3">
                    <i class="fas fa-robot"></i>
                    Analyze Paper
                </button>
            </form>
            
            <div id="loading">
                <p class="loading-text">Processing your request, please wait...</p>
                <div class="spinner"></div>
            </div>
        </div>
    </body>
    </html>
    """


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