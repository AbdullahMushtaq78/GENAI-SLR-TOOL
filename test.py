# # from camel.agents import ChatAgent
# # import os
# # from camel.agents import CriticAgent
# # from camel.messages import BaseMessage
# # from camel.models import ModelFactory
# # from camel.types import ModelPlatformType, ModelType
# # from camel.configs import ChatGPTConfig
# # from camel.workforce import Workforce
# # from camel.tasks import Task
# # os.environ["OPENAI_API_KEY"] = "sk-xPyehS3LGAeYHEtbjrOEcLkVxm5_EAoZol-yJMuceVT3BlbkFJZFdBXoWDKZTIVtaph6_-VMAOi67iHxYjpCexuQ-nsA"
# # def makeAgent(Name: str, Role: str, persona:str):
# #     base_msg = f"# You are a helpful assistant\n # Your name is: {Name}.\n # You are a {Role}.\n # And here is your persona that you must act with: {persona}"
# #     model_configs = ChatGPTConfig(
# #         temperature= 0,
# #         tools = []
# #     )
# #     model = ModelFactory.create(
# #         model_platform = ModelPlatformType.OPENAI,
# #         model_type = ModelType.GPT_4O_MINI,
# #         model_config_dict= model_configs.as_dict()
# #     )
# #     agent = CriticAgent(BaseMessage.make_assistant_message(role_name=Role, content=base_msg), model=model, message_window_size=10)
# #     agent.reset()
# #     return agent


# # def make_workforce(description, agents_names:list, agents_roles:list, agents_personas:list):
# #     agents = []
# #     workforce = Workforce(description=description)
# #     for name, role, persona in zip(agents_names, agents_roles, agents_personas):
# #         workforce.add_single_agent_worker("Name: "+name+", Role: "+role, worker=makeAgent(name, role, persona))
# #     return workforce
    
# # def create_recursive_workforce():
# #     agents_names = [
# #         ["Aurora", "Finn", "Lila"],
# #         ["Elliot", "Sage", "Rowan"],
# #         ["Mira", "Theo", "Juno"]
# #     ]

# #     agents_roles = [
# #         ["Creative Writer", "Editor", "Fact Checker"],
# #         ["Narrative Designer", "World Builder", "Character Developer"],
# #         ["Dialogue Specialist", "Tone Consultant", "Plot Architect"]
# #     ]

# #     agents_personas = [
# #         [
# #             "Imaginative and poetic, Aurora weaves vivid descriptions and emotional depth into stories.",
# #             "Detail-oriented and critical, Finn ensures the content is grammatically flawless and cohesive.",
# #             "Precise and methodical, Lila verifies every fact and enhances accuracy in storytelling."
# #         ],
# #         [
# #             "Visionary and innovative, Elliot crafts compelling story arcs that captivate audiences.",
# #             "Analytical and structured, Sage designs immersive worlds with a focus on realism and consistency.",
# #             "Empathetic and insightful, Rowan creates relatable and multidimensional characters."
# #         ],
# #         [
# #             "Quick-witted and expressive, Mira writes natural and engaging dialogue.",
# #             "Sensitive and intuitive, Theo tailors the tone of stories to resonate with specific audiences.",
# #             "Strategic and creative, Juno constructs intricate plots with surprising twists."
# #         ]
# #     ]
    

# #     Workforces_descriptions = [
# #         "Specializes in creating beautifully written, accurate, and emotionally resonant narratives.",
# #     "Excels in designing captivating story arcs, immersive worlds, and multidimensional characters.",
# #     "Focuses on crafting authentic dialogue, tailored tones, and intricate, surprising plots."

# #     ]
# #     workforces = []
# #     for descriptions, (names, (roles, personas)) in zip(Workforces_descriptions, zip(agents_names, zip(agents_roles, agents_personas))):
# #         workforces.append(make_workforce(descriptions, names, roles, personas))
# #     return workforces
        
# # def main():
# #     workforces = create_recursive_workforce()
# #     Task_description = f"""
# #     Task Description: Collaborative Storytelling Project
# #     Objective:
# #     Develop a compelling short story with a richly immersive world, relatable characters, engaging dialogue, and a polished final product that captures the readers' imagination and holds their interest.

# #     Task Details:

# #     Aurora (Creative Writer):

# #     Begin by drafting a vivid and emotionally evocative narrative for the story. Incorporate poetic descriptions of settings and characters, ensuring the writing feels immersive and deeply engaging.
# #     Finn (Editor):

# #     Review Aurora's initial draft for grammatical accuracy, logical flow, and overall cohesiveness. Suggest revisions to strengthen the narrative structure and ensure readability.
# #     Lila (Fact Checker):

# #     Ensure all factual elements in the story—such as historical, cultural, or scientific references—are accurate and consistent. Provide insights to correct inaccuracies or suggest more plausible alternatives.
# #     Elliot (Narrative Designer):

# #     Refine the overarching story arc to ensure it has a compelling beginning, middle, and end. Focus on creating tension and resolution to keep the reader invested throughout the story.
# #     Sage (World Builder):

# #     Design the story's setting, including its geography, culture, and history. Ensure the world feels believable, immersive, and integral to the narrative.
# #     Rowan (Character Developer):

# #     Flesh out the main and supporting characters, ensuring they are multidimensional and relatable. Develop backstories, motivations, and arcs that align with the story's themes.
# #     Mira (Dialogue Specialist):

# #     Write engaging and natural dialogue for the characters, ensuring it reflects their personalities and advances the plot. Focus on making conversations authentic and emotionally resonant.
# #     Theo (Tone Consultant):

# #     Review the story's tone and ensure it aligns with the intended mood and audience. Suggest adjustments to achieve the desired emotional impact.
# #     Juno (Plot Architect):

# #     Examine the story's plot for logical consistency and strategic pacing. Incorporate twists or elements of surprise where appropriate, ensuring the story is both dynamic and satisfying.
# #     Outcome:
# #     A polished, immersive short story that seamlessly blends a vivid narrative, authentic dialogue, rich world-building, and captivating characters, while maintaining grammatical precision and tonal consistency.
# #     """
    
# #     sub_tasks = [
# #         """Draft a vivid and emotionally evocative narrative, focusing on immersive settings and characters (Aurora).,
# #             Review the draft for grammatical accuracy, logical flow, and overall cohesiveness; provide revisions (Finn).,
# #             Verify factual elements, such as cultural, historical, or scientific references, to ensure accuracy (Lila).""",
        
# #             """Refine the overarching story arc, ensuring a compelling beginning, middle, and end with proper tension and resolution (Elliot).,
# #             Design the setting, including its geography, culture, and history, to create an immersive and consistent world (Sage).,
# #             Develop multidimensional characters with detailed backstories, motivations, and arcs that align with the story's themes (Rowan).""",
            
# #             """Write natural and engaging dialogue that reflects character personalities and advances the plot (Mira).,
# #             Review and adjust the story's tone to ensure it resonates with the intended audience and evokes desired emotions (Theo).,
# #             Examine the plot for logical consistency and pacing, incorporating twists or elements of surprise as needed (Juno)."""
# #     ]
# #     results = []
    
# #     for (sub_task, workforce) in zip(sub_tasks, workforces):
# #         res = workforce.process_task(Task(id=str(len(results)), content=sub_task))
# #         results.append(res.result)
# #     # workforce_task = Task(id="0", content=Task_description)
# #     # result = main_workforce.process_task(workforce_task)
# #     # print(result.result)
# # main()
















# from pydantic import BaseModel, Field
# import os
# from camel.agents import ChatAgent
# from camel.messages import BaseMessage
# from camel.models import ModelFactory
# from camel.types import ModelPlatformType, ModelType
# from camel.configs import ChatGPTConfig
# os.environ["OPENAI_API_KEY"] = "sk-xPyehS3LGAeYHEtbjrOEcLkVxm5_EAoZol-yJMuceVT3BlbkFJZFdBXoWDKZTIVtaph6_-VMAOi67iHxYjpCexuQ-nsA"

# # Define system message
# assistant_sys_msg = BaseMessage.make_assistant_message(
#     role_name="Assistant",
#     content="You are a helpful assistant.",
# )

# model = ModelFactory.create(
#     model_platform=ModelPlatformType.OPENAI,
#     model_type=ModelType.GPT_4O,
#     model_config_dict=ChatGPTConfig(temperature=0.0, tools = []).as_dict())

# # Set agent
# camel_agent = ChatAgent(assistant_sys_msg, model=model)


# # pydantic basemodel as input params format
# class JokeResponse(BaseModel):
#     joke: str = Field(description="a joke")
#     funny_level: str = Field(description="Funny level, from 1 to 10")


# user_msg = BaseMessage.make_user_message(
#     role_name="User",
#     content="Tell a jokes.",
# )

# # Get response information
# response = camel_agent.step(user_msg, response_format=JokeResponse)
# print(response.msgs[0].content)
# """
# {'joke': "Why couldn't the bicycle find its way home? It lost its bearings!"
# , 'funny_level': '8'}
# """


from unstructured.partition.pdf import partition_pdf
elements = partition_pdf(filename="/home/abdullah/MAS_SLR/sample_data/s43093-024-00326-4.pdf")

from unstructured.partition.text import partition_text
elements = partition_text(filename="example-docs/fake-text.txt")