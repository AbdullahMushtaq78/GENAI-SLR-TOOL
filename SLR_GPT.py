from configs import *
from personas import SLR_GPT_PERSONA, PERSONAS
def format_societies_output(societies_output):
    formatted_output = ""
    all_descriptions = [wf_persona["Workforce_description"] for wf_persona in PERSONAS]

    for i in range(1, 7):
        single_society_output = societies_output[i]
        overall_result_part = single_society_output["overall_result"]
        per_agent_part = single_society_output["per_agent_result"]
        society_description = all_descriptions[i - 1]
        agents = PERSONAS[i - 1]["Agents"]

        per_agent_with_names = ""
        for j in range(len(per_agent_part)):
            agent_name = agents[j]["Agent_Name"]
            agent_role = agents[j]["Agent_Role"]
            agent_part = per_agent_part[j]
            per_agent_with_names += (
                f"Name: *{agent_name}*, Role: *{agent_role}*\n"
                f"--- EVALUATION ---\n"
                f"{agent_part}\n\n"
            )

        formatted_output += (
            f"#### SOCIETY NAME: {society_description}\n\n"
            f"#### OVERALL RESULTS:\n{overall_result_part}\n\n"
            f"#### PER AGENT:\n{per_agent_with_names}\n"
        )

    return formatted_output

    
def SLR_GPT_Agent(full_paper_text:str, societies_output:str)->ChatAgent:
    
    agent = ChatAgent(
            system_message = BaseMessage.make_assistant_message(
                role_name = "SLR-GPT",
                content = SLR_GPT_PERSONA.format(
                    full_paper_content = full_paper_text,
                    society_outputs = format_societies_output(societies_output)
                )
            ),
            model = ModelFactory.create(
                model_platform = SLR_GPT_PLATFORM,
                model_type = SLR_GPT_MODEL,
                model_config_dict = ChatGPTConfig(temperature = SLR_GPT_TEMPERATURE).as_dict()
            ),
            message_window_size = SLR_GPT_MESSAGES_WINDOW,
            tools = TOOLS
    )
    return agent

def SLR_GPT(agent:ChatAgent, user_msg:str)->str:
    user_msg = BaseMessage.make_user_message(
            role_name="User",
            content=user_msg
        )
    response = agent.step(user_msg)
    return response.msgs[0].content