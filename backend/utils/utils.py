import pdfplumber
import os
from camel.tasks import Task
from backend.personas import roles


def extract_content(path: str) -> str:
    from unstructured.partition.pdf import partition_pdf

    elements = partition_pdf(filename=path)
    return "\n".join(element.text for element in elements)


def WorkForce_task(paper_title: str, id: str, complete_paper=None) -> Task:
    local_roles = (
        "\n*Score:Y/5*\n*Summarized Feedback*:...\n\n".join([f"*{role}*" for role in roles[id]])
        + "\n*Score:Y/5*\n*Summarized Feedback*:...\n\n"
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
