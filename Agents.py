from configs import *
def create_agent(name: str, role: str, persona: str) -> CriticAgent:
    name = name.replace("_", " ")
    persona = persona + TOOLS_PROMPT
    base_msg = f"# You are a helpful assistant\n # Your name is: {name}.\n # You are a {role}.\n # And here is your persona that you must act with: {persona}"
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

def create_workforce(wf_description, agents_names, agents_roles, agents_personas) ->Workforce:
    wf = Workforce(description=wf_description)
    for name, (role, persona) in zip(agents_names, zip(agents_roles, agents_personas)):
        wf.add_single_agent_worker(worker=create_agent(name, role, persona), description=f"{name} - {role}")
    return wf

def create_all_workforces() ->list[Workforce]:
    workforces = []
    for wf_details in PERSONAS:
        wf = create_workforce(
            wf_description = wf_details["Workforce_description"],
            agents_names = [agent["Agent_Name"] for agent in wf_details["Agents"]],
            agents_roles = [agent["Agent_Role"] for agent in wf_details["Agents"]],
            agents_personas = [agent["Persona"] for agent in wf_details["Agents"]]
        )
        workforces.append(wf)
    return workforces

