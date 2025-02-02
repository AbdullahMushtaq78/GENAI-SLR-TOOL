from configs import *
from pydantic import BaseModel, Field
from utils import extract_pdf_content, extract_pdf_OCR2
class SLRResponse(BaseModel):
    title_and_abstract: str = Field(description="The title and abstract of the paper.")
    introduction: str = Field(description="The introduction section of the paper.")
    eligibility_criteria: str = Field(description="The eligibility criteria used in SLR.")
    information_sources: str = Field(
        description="Information sources, search strategy, and selection process."
    )
    data_collection_process: str = Field(
        description="Data collection process and items in SLR."
    )
    risk_of_bias_and_effect_measures: str = Field(
        description="Risk of bias and effect measures in SLR."
    )
    synthesis_methods: str = Field(description="Synthesis methods used in SLR.")
    reporting_bias_and_certainty: str = Field(
        description="Reporting bias and certainty assessment."
    )
    study_selection_characteristics: str = Field(
        description="Study selection, characteristics, and risk of bias in SLR."
    )
    results_of_individual_studies: str = Field(
        description="Results of individual studies and synthesis."
    )
    reporting_biases_and_certainty: str = Field(
        description="Reporting biases and certainty of evidence."
    )
    results_limitations_implications: str = Field(
        description="Results, limitations, and implications in SLR."
    )
    other_information: str = Field(
        description="Management of administrative and ethical aspects of SLR."
    )




class Paper_Division_Agent:

    def __init__(self):
        
        assistant_sys_msg = BaseMessage.make_assistant_message(
            role_name="Assistant",
            content= SYSTEM_PROMPT_PDA
        )

        
        model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O,
        )
        self.agent = ChatAgent(assistant_sys_msg, model=model)
        self.Agents_Per_WorkForce = {
            "title_and_abstract": 1,
            "Introduction": 1,
            "eligibility_criteria": 2,
            "information_sources": 2,
            "data_collection_process": 2,
            "risk_of_bias_and_effect_measures": 2,
            "synthesis_methods": 2,
            "reporting_bias_and_certainty": 2,
            "study_selection_characteristics": 3,
            "results_of_individual_studies": 3,
            "reporting_biases_and_certainty": 3,
            "results_limitations_implications": 4,
            "other_information": 4
        }

    def extract_sections(self, pdf_content: str):
        user_msg = BaseMessage.make_user_message(
            role_name="User",
            content=f"Here is the text of a systematic literature review paper. Please process it.\n\n {pdf_content}"
        )
        response = self.agent.step(user_msg, response_format=SLRResponse)
        structured_output = eval(response.msgs[0].content)
        return structured_output

    def group_sections(self, sections: dict):
        grouped_sections = {}

        for section, content in sections.items():
            workforce = self.Agents_Per_WorkForce.get(section, None)
            if workforce is not None:
                if workforce not in grouped_sections:
                    grouped_sections[workforce] = {}
                grouped_sections[workforce][section] = content

        return grouped_sections


# paper_divison_agent = Paper_Division_Agent()
# ocr = extract_pdf_OCR2("/home/abdullah/MAS_SLR/sample_data/2024.07.25.24311022v1.full.pdf")
# pdf_content = paper_divison_agent.extract_sections(ocr)
# grouped_sections = paper_divison_agent.group_sections(pdf_content)
# print(grouped_sections)