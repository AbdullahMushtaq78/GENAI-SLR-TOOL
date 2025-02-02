from Paper_Extraction_Agent import Paper_Division_Agent
from Agents import create_all_workforces
from utils import extract_pdf_OCR2, WorkForce_task, extract_content
from output_formation_agent import Output_Formation_Agent
from classification_agent import Protocol_Classification_Agent
import gradio as gr


def start_processing_SLR_pdf(paper_path:str, paper_title):
    
    #PAPER_PATH = "/home/abdullah/MAS_SLR/sample_data/s43093-024-00326-4.pdf"
    #PAPER_TITLE = "Systematic literature review using PRISMA: exploring the influence of service quality and perceived value on satisfaction and intention to continue relationship"
    PAPER_PATH = paper_path
    PAPER_TITLE = paper_title
    protocol_agent = Protocol_Classification_Agent()
    paper_divison_agent = Paper_Division_Agent()
    #ocr = extract_pdf_OCR2(PAPER_PATH)
    ocr = extract_content(path=PAPER_PATH)
    # with open("/home/abdullah/MAS_SLR/sample_data/ocr.txt", "r") as f:
    #     ocr = "".join(f.readlines())
    classification_results = protocol_agent.classify(ocr)
    print(f"{'='*10}\nCLASSIFICATION RESULTS: {classification_results}\n{'='*10}")
    pdf_content = paper_divison_agent.extract_sections(ocr)
    grouped_sections = paper_divison_agent.group_sections(pdf_content)
    wf_index = 1
    workforces = create_all_workforces()
    results = {}
    for wf in workforces:
        wf_task = WorkForce_task(
            paper_title=PAPER_TITLE,
            task_content="".join([
                f"{{\n# {x[0].upper().replace('_', ' ')}:\n {x[1]}\n\n}}\n" if x[1] != "" 
                else f"{{\n# {x[0].upper().replace('_', ' ')}:\n No data found for this section\n\n}}\n" 
                for x in grouped_sections[wf_index].items()
            ]),
            id= str(wf_index),
            complete_paper=ocr
        )
        res = wf.process_task(wf_task)
        results[wf_index] = {
            "overall_result": res.result,
            "per_agent_result": [sub.result for sub in res.subtasks] 
        }
        wf_index += 1
    
    formatting_agent = Output_Formation_Agent()
    final_formatted_output = formatting_agent.format_output(results)
    with open("formatted_result.txt", 'w') as r_file:
        r_file.writelines(str(final_formatted_output))
    with open("result.txt", 'w') as r_file:
        r_file.writelines(str(results))
    with open("cls_result.txt", 'w') as r_file:
        r_file.writelines(str(classification_results))
    return classification_results, final_formatted_output, results




def demo_output(paper_path:str, paper_title:str):

    def convert_keys_to_str_recursive(input_dict):
        if isinstance(input_dict, dict):
            return {str(key): convert_keys_to_str_recursive(value) for key, value in input_dict.items()}
        elif isinstance(input_dict, list):
            return [convert_keys_to_str_recursive(item) for item in input_dict]
        else:
            return input_dict


    with open("cls_result.txt", 'r') as file:
        cls_results = eval("".join(file.readlines()))
    with open("formatted_result.txt", 'r') as file:
        formatted_result = eval(''.join(file.readlines()))
    with open("result.txt", 'r') as file:
        result = eval("".join(file.readlines()))
    return cls_results, formatted_result, result
    return convert_keys_to_str_recursive(cls_results), convert_keys_to_str_recursive(formatted_result), convert_keys_to_str_recursive(result)
def main():
    
    with gr.Blocks() as app:
        # Define UI components
        paper_title = gr.Textbox(label="Paper Title")
        paper_pdf = gr.File(label="Paper PDF", file_types=[".pdf"])
        submit_btn = gr.Button("Submit")

        classification_output = gr.JSON(label="Classification Results")
        formatted_output = gr.JSON(label="Formatted Results")
        raw_output = gr.JSON(label="Raw Results")

        # Link the submit button to the function
        submit_btn.click(
            fn=demo_output,
            inputs=[paper_pdf, paper_title],  # Ensure input order matches the function arguments
            outputs=[classification_output, formatted_output, raw_output]
        )

    app.launch()


#main()