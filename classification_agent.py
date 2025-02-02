from configs import *
from pydantic import BaseModel, Field

class Classification_Output(BaseModel):
    Identified_Protocol:str = Field(description="Name the SLR protocol.")
    Confidence_Level : str = Field(description="State the confidence percentage.")
    Evidence : str = Field(description="Justify the classification by citing features from the content.")

class Protocol_Classification_Agent():
    def __init__(self):
        
        assistant_sys_msg = BaseMessage.make_assistant_message(
            role_name="Assistant",
            content= SYSTEM_PROMPT_CLS
        )

        
        model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
        )
        self.agent = ChatAgent(assistant_sys_msg, model=model)

    def classify(self, pdf_content: str):
        user_msg = BaseMessage.make_user_message(
            role_name="User",
            content=f"Here is the text of a systematic literature review paper. Please process it.\n\n # CONTENT\n\n {pdf_content}"
        )
        response = self.agent.step(user_msg, response_format=Classification_Output)
        structured_output = eval(response.msgs[0].content)
        return structured_output