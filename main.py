from Agents import create_all_workforces
from utils import WorkForce_task, extract_content
import gradio as gr
import threading
import queue
import time
import os

# Create a global progress update queue
progress_queue = queue.Queue()

# Function to get the latest progress update
def get_progress_update():
    if not progress_queue.empty():
        return progress_queue.get()
    return None

def update_progress(message):
    """Update the progress message to be shown in the loading div"""
    progress_queue.put(message)
    print(f"Progress update: {message}")  # Log progress updates

# Start Flask server for progress updates
try:
    from messages_server import start_server_in_thread
    # Start the Flask server in a background thread
    start_server_in_thread()
except Exception as e:
    print(f"Failed to start progress update server: {e}")

def start_processing_SLR_pdf(paper_path: str, paper_title):
    PAPER_PATH = paper_path
    PAPER_TITLE = paper_title
    
    update_progress("Extracting content from the PDF...")
    ocr = extract_content(path=PAPER_PATH)
    
    update_progress("Initializing AI workforces...")
    wf_index = 1
    workforces = create_all_workforces(Paper_ocr=ocr)
    results = {}
    
    total_workforces = len(workforces)
    for wf in workforces:
        update_progress(f"Processing workforce {wf_index} of {total_workforces}...")
        
        wf_task = WorkForce_task(
            paper_title=PAPER_TITLE,
            id=str(wf_index),
            complete_paper=ocr,
        )
        
        # Update progress before starting task
        update_progress(f"Analyzing paper with workforce {wf_index} - this may take a few minutes...")
        
        # Process the task
        res = wf.process_task(wf_task)
        
        # Store results
        results[wf_index] = {
            "overall_result": res.result,
            "per_agent_result": [sub.result for sub in res.subtasks],
        }
        
        update_progress(f"Workforce {wf_index} analysis complete. Moving to next stage...")
        wf_index += 1
    
    update_progress("Analysis complete! Preparing results...")
    return results, ocr


def demo_output(paper_path: str, paper_title: str):
    update_progress("Loading demo data...")
    
    import time
    time.sleep(5)
    with open("results/The_association_between_gestational_diabetes_and_ASD_and_ADHD_a_systematic_review_and_metaanalysis_results.txt", "r") as file:
        result = eval("".join(file.readlines()))
    with open("./results/ocr.txt", "r") as file:
        ocr = "".join(file.readlines())
    
    update_progress("Demo data loaded successfully!")
    return result, ocr

# Main Gradio interface setup
def create_gradio_interface():
    # Your existing Gradio interface code here
    # ...
    
    # Start the interface
    # demo.launch()
    pass

# If this file is run directly, start the Gradio interface
if __name__ == "__main__":
    create_gradio_interface()
