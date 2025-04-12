from configs import *
def create_agent(name: str, role: str, persona: str, Paper_ocr:str) -> CriticAgent:
    name = name.replace("_", " ")
    persona = persona + TOOLS_PROMPT
    base_msg = f"# You are a helpful assistant\n # Your name is: {name}.\n # You are a {role}.\n # And here is your persona that you must act with: {persona}\n\n---\nHere is the entire SLR paper content (use it for your evaluation task): \n {Paper_ocr}"
    model_configs = ChatGPTConfig(
        temperature=TEMPERATURE,
    )
    model = ModelFactory.create(
        model_platform = PLATFORM,
        model_type= MODEL,
        model_config_dict= model_configs.as_dict()
    )
    agent = ChatAgent(
        system_message=BaseMessage.make_assistant_message(role_name=role, content=base_msg),
        model=model,
        message_window_size=MESSAGES_WINDOW,
        tools= TOOLS
    )
    return agent

def create_workforce(wf_description, agents_names, agents_roles, agents_personas, Paper_ocr) ->Workforce:
    wf = Workforce(description=wf_description)
    for name, (role, persona) in zip(agents_names, zip(agents_roles, agents_personas)):
        wf.add_single_agent_worker(worker=create_agent(name, role, persona, Paper_ocr), description=f"{name} - {role}")
    return wf

def create_all_workforces(Paper_ocr:str) ->list[Workforce]:
    workforces = []
    for wf_details in PERSONAS:
        if wf_details["Workforce_description"] == "DISCUSSION SOCIETY":
        
            wf = create_workforce(
                wf_description = wf_details["Workforce_description"],
                agents_names = [agent["Agent_Name"] for agent in wf_details["Agents"]],
                agents_roles = [agent["Agent_Role"] for agent in wf_details["Agents"]],
                agents_personas = [agent["Persona"] for agent in wf_details["Agents"]],
                Paper_ocr=Paper_ocr
            )
            workforces.append(wf)
    return workforces

