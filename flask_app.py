from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
import os
from main import demo_output, start_processing_SLR_pdf
import markdown
from personas import PERSONAS
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        paper_title = request.form.get('paper_title', '')
        pdf_file = request.files.get('paper_pdf')
        if pdf_file:
            filename = secure_filename(pdf_file.filename)
            saved_path = os.path.join(UPLOAD_FOLDER, filename)
            pdf_file.save(saved_path)
            cls_results, formatted_result, raw_result = demo_output(saved_path, paper_title)
            #cls_results, formatted_result, raw_result = start_processing_SLR_pdf(saved_path, paper_title)
            
            converted_evidence = markdown.markdown(
                cls_results["Evidence"],
                extensions=['extra','codehilite','toc','sane_lists','smarty','admonition','attr_list','footnotes','nl2br','wikilinks','meta']
            )
            classification_card = f"""
                <div class="card classification-card">
                    <p><strong>Identified Literature Review Type:</strong> {cls_results["Identified_Protocol"]}</p>
                    <p><strong>Confidence Level:</strong> {cls_results["Confidence_Level"]}</p>
                    <button class="btn-show-more" onclick="toggleVisibility(this, 'evidence')">
                        <i class="fas fa-chevron-down me-2"></i>Show More
                    </button>
                    <div id="evidence" class="hidden" style="display: none;">
                        <p><strong>Evidence:</strong></p>
                        <div>{converted_evidence}</div>
                    </div>
                </div>
            """

            raw_cards = ""
            for i in range(1, 5):
                if i in raw_result:
                    converted_overall = markdown.markdown(
                        raw_result[i]["overall_result"],
                        extensions=['extra','codehilite','toc','sane_lists','smarty','admonition','attr_list','footnotes','nl2br','wikilinks','meta']
                    )
                    converted_agents = [
                        markdown.markdown(
                            agent_res,
                            extensions=['extra','codehilite','toc','sane_lists','smarty','admonition','attr_list','footnotes','nl2br','wikilinks','meta']
                        )
                        for agent_res in raw_result[i]["per_agent_result"]
                    ]
                    descriptions = [wf_persona["Workforce_description"] for wf_persona in PERSONAS]
                    card = f"""
                        <div class="card raw-card">
                            <h1 class="workforce-heading">{descriptions[i-1]}</h1>
                            <p><strong>Overall Result:</strong></p>
                            <div>{converted_overall}</div>
                            <button class="btn-show-more" onclick="toggleVisibility(this, 'agent_list_{i}')">
                                <i class="fas fa-chevron-down me-2"></i>See More
                            </button>
                            <div id="agent_list_{i}" class="hidden" style="display: none;">
                                <p><strong>Detailed Agents Result:</strong></p>
                                <ul>
                                    {''.join(f"<li>{a}</li>" for a in converted_agents)}
                                </ul>
                            </div>
                        </div>
                    """
                    raw_cards += card

            final_output = f"""
            <html>
            <head>
                <title> MAS-SLR Demo </title>
                <style>
                    .card {{ border: 1px solid #ccc; padding: 20px; margin-bottom: 10px; margin-left:150px; margin-right:150px; border-radius:10px; }}
                    .hidden {{ display: none; }}
                    button {{ margin-top: 5px; }}
                    .classification-card {{
                        background: linear-gradient(135deg, #86d180, #b9f7ff);
                    }}
                    .raw-card {{
                        background: linear-gradient(135deg, #ADD8E6, #E0FFFF);
                    }}
                    .btn-show-more {{
                        background-color: #17a2b8;
                        color: #fff;
                        border: none;
                        border-radius: 5px;
                        padding: 5px 10px;
                        cursor: pointer;
                    }}
                    .btn-show-more:hover {{
                        background-color: #138496;
                    }}
                    h2 {{
                        text-align: center;
                    }}
                    .workforce-heading {{
                        text-align: center; /* Center align Workforce headings */
                    }}
                    a {{
                        display: block;
                        text-align: center;
                        margin-top: 20px;
                        color: #007bff;
                    }}
                    a:hover {{
                        color: #0056b3;
                    }}
                    .btn-go-back {{
                        display: inline-flex;
                        align-items: center;
                        justify-content: center;
                        background-color: #d2b48c; /* Slight brown */
                        color: #fff;
                        width: 40px;
                        height: 40px;
                        border-radius: 20%;
                        text-decoration: none;
                        transition: background-color 0.3s ease;
                        position: fixed;
                        bottom: 20px;
                        left: 20px;
                    }}
                    .btn-go-back:hover {{
                        background-color: #c19a6b; /* Darker brown on hover */
                    }}
                    .btn-go-back i {{
                        font-size: 16px;
                    }}
                </style>
                <script>
                    function toggleVisibility(btn, id) {{
                        const x = document.getElementById(id);
                        if (x.style.display === "none" || x.style.display === "") {{
                            x.style.display = "block";
                            btn.innerHTML = '<i class="fas fa-chevron-up me-2"></i>Show Less';
                        }} else {{
                            x.style.display = "none";
                            btn.innerHTML = '<i class="fas fa-chevron-down me-2"></i>Show More';
                        }}
                    }}
                </script>
            </head>
            <body>
                <h2>Classification Results</h2>
                {classification_card}
                <h2>Raw Results</h2>
                {raw_cards}

                <a href="/" class="btn-go-back" title="Go Back">
                    <p class="" style="color:#0000; padding:5px;">Go Back</i>
                </a>
            </body>
            </html>
            """
            return render_template_string(final_output, cls_results=cls_results, raw_result=raw_result)
    # GET request: Show upload form
    return '''
    <html>
    <head>
        <title>Upload Paper</title>
        <!-- Include Bootstrap CSS and optional Font Awesome -->
        <link rel="stylesheet"
              href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <!-- Updated Font Awesome CDN to a stable version -->
        <link rel="stylesheet"
              href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            html, body {
                height: 100%;
                margin: 0;
            }
            body {
                display: flex;
                align-items: center;
                justify-content: center;
                background: #f8f9fa; /* Reverted to a neutral background */
            }
            .container {
                max-width: 500px;
                padding: 30px;
                /* Gradient background for the form section only */
                background: linear-gradient(135deg, #FFA07A, #FFDAB9);
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            h1, h2, label {
                color: #333;
            }
            .btn-custom {
                background-color: #007bff;
                color: #fff;
            }
            .btn-custom:hover {
                background-color: #0056b3;
                color: #fff;
            }
            .form-label {
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mb-4 text-center">Upload Paper</h1>
            <form method="POST" enctype="multipart/form-data" class="row g-3">
                <div class="col-12">
                    <label for="paper_title" class="form-label">
                        <i class="fas fa-text-height me-2"></i>Paper Title
                    </label>
                    <input type="text" id="paper_title" name="paper_title" class="form-control" placeholder="Enter paper title"/>
                </div>
                <div class="col-12">
                    <label for="paper_pdf" class="form-label">
                        <i class="fas fa-file-pdf me-2"></i>Paper PDF
                    </label>
                    <input type="file" id="paper_pdf" name="paper_pdf" accept=".pdf" class="form-control"/>
                </div>
                <div class="col-12 text-center mt-4">
                    <button type="submit" class="btn btn-custom">
                        <i class="fas fa-upload"></i> Submit
                    </button>
                </div>
            </form>
        </div>
        <!-- Optionally include Bootstrap JS for any interactive components -->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
if __name__ == '__main__':
    app.run(debug=True)