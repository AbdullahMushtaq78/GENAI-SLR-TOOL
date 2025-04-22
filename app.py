import gradio as gr
from main import start_processing_SLR_pdf, demo_output, update_progress
from server import start_server_in_thread
from html_templates import render_upload_form
import threading
import time

# Start the progress update server
print("Starting progress update server...")
start_server_in_thread()
time.sleep(1)  # Give the server a moment to start

# Create a Gradio interface
def process_upload(paper_pdf, paper_title):
    update_progress(f"Starting analysis of paper: {paper_title}")
    # Process the uploaded file
    paper_path = paper_pdf.name  # Get the file path of the uploaded PDF
    results, ocr = start_processing_SLR_pdf(paper_path, paper_title)
    return results

# Create demo interface
def run_demo(paper_title):
    update_progress(f"Running demo for: {paper_title}")
    results, ocr = demo_output("demo_path", paper_title)
    return results

# Create the Gradio interface with custom HTML
with gr.Blocks(css="") as demo:
    gr.HTML(render_upload_form())
    
    # Hidden components to handle the form submission
    with gr.Row(visible=False):
        paper_pdf_input = gr.File(label="PDF File")
        paper_title_input = gr.Textbox(label="Paper Title")
        submit_btn = gr.Button("Process")
        output = gr.JSON(label="Results")
    
    submit_btn.click(
        fn=process_upload,
        inputs=[paper_pdf_input, paper_title_input],
        outputs=[output]
    )

# Launch the application
if __name__ == "__main__":
    print("Starting Gradio interface...")
    demo.launch()
    print("Gradio interface started!")
