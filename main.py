from Agents import create_all_workforces
from utils import extract_pdf_OCR2, WorkForce_task, extract_content
import gradio as gr


def start_processing_SLR_pdf(paper_path: str, paper_title):

    PAPER_PATH = paper_path
    PAPER_TITLE = paper_title
    ocr = extract_content(path=PAPER_PATH)
    wf_index = 1
    workforces = create_all_workforces(Paper_ocr=ocr)
    results = {}
    for wf in workforces:
        wf_task = WorkForce_task(
            paper_title=PAPER_TITLE,
            id=str(wf_index),
            complete_paper=ocr,
        )
        res = wf.process_task(wf_task)
        results[wf_index] = {
            "overall_result": res.result,
            "per_agent_result": [sub.result for sub in res.subtasks],
        }
        wf_index += 1
    
    return results, ocr


def demo_output(paper_path: str, paper_title: str):
    
    with open("results/The_association_between_gestational_diabetes_and_ASD_and_ADHD_a_systematic_review_and_metaanalysis_results.txt", "r") as file:
        result = eval("".join(file.readlines()))
    with open("./sample_data/ocr.txt", "r") as file:
        ocr = "".join(file.readlines())
    return result, ocr
