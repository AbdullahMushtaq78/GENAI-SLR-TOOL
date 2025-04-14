from Paper_Extraction_Agent import Paper_Division_Agent
from Agents import create_all_workforces
from utils import extract_pdf_OCR2, WorkForce_task, extract_content
from output_formation_agent import Output_Formation_Agent
from classification_agent import Protocol_Classification_Agent
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

    
    # with open("result.txt", "w") as r_file:
    #     r_file.writelines(str(results))
    return results, ocr


def demo_output(paper_path: str, paper_title: str):

    def convert_keys_to_str_recursive(input_dict):
        if isinstance(input_dict, dict):
            return {
                str(key): convert_keys_to_str_recursive(value)
                for key, value in input_dict.items()
            }
        elif isinstance(input_dict, list):
            return [convert_keys_to_str_recursive(item) for item in input_dict]
        else:
            return input_dict

    
    with open("results/The_association_between_gestational_diabetes_and_ASD_and_ADHD_a_systematic_review_and_metaanalysis_results.txt", "r") as file:
        result = eval("".join(file.readlines()))
    with open("./sample_data/ocr.txt", "r") as file:
        ocr = "".join(file.readlines())
    return result, ocr




#Gradio-based UI for initial testing
def main():

    with gr.Blocks() as app:
        # Define UI components
        paper_title = gr.Textbox(label="Paper Title")
        paper_pdf = gr.File(label="Paper PDF", file_types=[".pdf"])
        submit_btn = gr.Button("Submit")

        raw_output = gr.JSON(label="Raw Results")

        # Link the submit button to the function
        submit_btn.click(
            fn=demo_output,
            inputs=[
                paper_pdf,
                paper_title,
            ],  # Ensure input order matches the function arguments
            outputs=[raw_output],
        )

    app.launch()


# main()
