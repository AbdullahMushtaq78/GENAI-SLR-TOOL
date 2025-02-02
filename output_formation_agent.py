from configs import *
from pydantic import BaseModel, Field


class Output_Format(BaseModel):
    Overall_SLR_Score: str = Field(description="The overall score based on the evaluation scores from all the agents.")
    Overall_Summary: str = Field(description="The overall summary of feedback from all the agents.")
    Scores_per_agent: str = Field(description="A list of scores from all the agents separated by new line.")
    Feedback_per_agent: str = Field(description="Feedback from all the agents one by one separated by new line.")
class Output_Formation_Agent:

    def __init__(self):
        
        assistant_sys_msg = BaseMessage.make_assistant_message(
            role_name="Formatting Assistant",
            content= SYSTEM_PROMPT_FORMATTER
        )

        
        model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
        )
        self.agent = ChatAgent(assistant_sys_msg, model=model)
    def pre_process_input(self, results):
        return "".join(
        [
            f"""
                # Workforce {idx+1} Output\n
                ## Summarized Results \n
                {results[idx+1]["overall_result"]}
                ---
                ## Response Per Agent\n
                {"".join(results[idx+1]["per_agent_result"])}
            """ 
            for idx in range(len(results.items()))
         ])
    def format_output(self, pdf_content: str):
        user_msg = BaseMessage.make_user_message(
            role_name="User",
            content=f"{self.pre_process_input(pdf_content)}"
        )
        response = self.agent.step(user_msg, response_format=Output_Format)
        structured_output = eval(response.msgs[0].content)
        return structured_output
