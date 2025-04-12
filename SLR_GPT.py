from configs import *
from personas import SLR_GPT_PERSONA

def SLR_GPT(full_paper_text:str, formatted_societies_output:str)->ChatAgent:
    
    agent = ChatAgent(
            system_message = BaseMessage.make_assistant_message(
                role_name = "SLR-GPT",
                content = SLR_GPT_PERSONA.format(
                    full_paper_content = full_paper_text,
                    society_outputs = formatted_societies_output
                )
            ),
            model = ModelFactory.create(
                model_platform = SLR_GPT_PLATFORM,
                model_type = SLR_GPT_MODEL,
                model_config_dict = ChatGPTConfig(
                    temperature = SLR_GPT_TEMPERATURE).as_dict()
            ),
            message_window_size = SLR_GPT_MESSAGES_WINDOW,
            tools = TOOLS
    )
    return agent

