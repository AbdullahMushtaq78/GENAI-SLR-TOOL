import pdfplumber
import os
from camel.tasks import Task
from personas import roles


def extract_pdf_content(path: str) -> str:
    with pdfplumber.open(path) as pdf:
        full_text = ""
        for page_num, page in enumerate(pdf.pages, start=0):
            text = page.extract_text() or ""
            full_text += text
    return full_text


from pdf2image import convert_from_path


def pdf_to_png(pdf_path, output_folder) -> int:
    pages = convert_from_path(pdf_path, 300)
    for i, page in enumerate(pages):
        page.save(f"{output_folder}/page_{i + 1}.png", "PNG")
    return len(pages)


def extract_pdf_OCR2(path: str) -> str:
    pdf_name = path.split("/")[-1].split(".")[0]

    os.makedirs(f"./output/{pdf_name}", exist_ok=True)
    pages = pdf_to_png(path, f"./output/{pdf_name}")

    from transformers import AutoModel, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        "ucaslcl/GOT-OCR2_0", trust_remote_code=True
    )
    model = AutoModel.from_pretrained(
        "ucaslcl/GOT-OCR2_0",
        trust_remote_code=True,
        low_cpu_mem_usage=True,
        device_map="cuda",
        use_safetensors=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    model = model.eval().cuda()

    full_text = """"""
    for page in range(pages):
        image_file = f"/home/abdullah/MAS_SLR/output/{pdf_name}/page_{page+1}.png"
        res = model.chat(tokenizer, image_file, ocr_type="format", ocr_box="")
        full_text += res
    return full_text


def extract_content(path: str) -> str:
    from unstructured.partition.pdf import partition_pdf

    elements = partition_pdf(filename=path)
    return "\n".join(element.text for element in elements)


def WorkForce_task(paper_title: str, id: str, complete_paper=None) -> Task:
    local_roles = (
        "\n*Score:Y/5*\nSummarized Feedback:...\n\n".join([f"*{role}*" for role in roles[id]])
        + "\n*Score:Y/5*\nSummarized Feedback:...\n\n"
    )
    return Task(
        id=id,
        # Here's the content relevant to your tasks: {task_content}.
        content=f"""

        #### Paper Title: {paper_title} \n
        - The agents are required to evaluate the paper based on their personas and roles. 
        - Complete paper text is already provided to all agents, just assign them their tasks based on their roles and get their output.
        
        #### After collecting output of all the agents, generate and format the output exactly as following:
        
        ## Overall Score: X/5
        ---
        
        {local_roles}
        
        ---
        #### Overall Feedback: ...
        ---
        
        Replace "Y" with the actual score given by that agent. Replace "..." with the actual feedback provided by the agent.
        And replace "X" with the overall mean score calculated based on the individual scores provided by the agents. Make sure averaged score provided by you is precise.
        """,
        # additional_info= f"## Here's the complete paper text: ---\n{complete_paper}\n---"
        additional_info=(
            f"Follow the output format exactly as it is and make sure the averaged score for all the agents is precise and accurate!"
        ),
    )
