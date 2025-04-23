from backend.agents.Agents import create_all_workforces
from backend.utils.utils import WorkForce_task, extract_content
from backend.utils.progress_manager import progress_manager
import os

# Start Flask server for progress updates if not already started
try:
    # Start server directly from progress_manager instead of importing from messages_server
    progress_manager.start_server(host='0.0.0.0', port=5002)
except Exception as e:
    print(f"Failed to start progress update server: {e}")

def start_processing_SLR_pdf(paper_path: str, paper_title):
    PAPER_PATH = paper_path
    PAPER_TITLE = paper_title
    
    progress_manager.update_progress("Extracting content from the PDF...")
    ocr = extract_content(path=PAPER_PATH)
    
    progress_manager.update_progress("Initializing AI workforces...")
    wf_index = 1
    workforces = create_all_workforces(Paper_ocr=ocr)
    results = {}
    
    total_workforces = len(workforces)
    for wf in workforces:
        progress_manager.update_progress(f"Processing workforce {wf_index} of {total_workforces}...")
        
        wf_task = WorkForce_task(
            paper_title=PAPER_TITLE,
            id=str(wf_index),
            complete_paper=ocr,
        )
        
        # Update progress before starting task
        progress_manager.update_progress(f"Analyzing paper with workforce {wf_index} - this may take a few minutes...")
        
        # Process the task
        res = wf.process_task(wf_task)
        
        # Store results
        results[wf_index] = {
            "overall_result": res.result,
            "per_agent_result": [sub.result for sub in res.subtasks],
        }
        
        progress_manager.update_progress(f"Workforce {wf_index} analysis complete. Moving to next stage...")
        wf_index += 1
    
    progress_manager.update_progress("Analysis complete! Preparing results...")
    return results, ocr


def demo_output(paper_path: str, paper_title: str):
    progress_manager.update_progress("Loading demo data...")

    import time
    time.sleep(5)  # Simulate loading time
    
    
    with open("results/The_association_between_gestational_diabetes_and_ASD_and_ADHD_a_systematic_review_and_metaanalysis_results.txt", "r") as file:
        result = eval("".join(file.readlines()))
    with open("./results/ocr.txt", "r") as file:
        ocr = "".join(file.readlines())
    
    progress_manager.update_progress("Demo data loaded successfully!")
    return result, ocr
