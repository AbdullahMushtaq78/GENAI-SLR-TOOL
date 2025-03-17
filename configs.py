import os
from camel.agents import CriticAgent, ChatAgent
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig, AnthropicConfig
from camel.societies.workforce import Workforce
from camel.tasks import Task
from personas import *
from typing import List
from dotenv import load_dotenv

load_dotenv()

PLATFORM = ModelPlatformType.OPENAI
MODEL = ModelType.GPT_4O
TEMPERATURE = 0.0
MESSAGES_WINDOW = 10
TOOLS = []


# =======================
# Paper Divison Agent
# =======================
SYSTEM_PROMPT_PDA = (
    "You are a helpful assistant that processes the text from systematic literature review (SLR)"
    "papers and extracts specific sections. Your task is to analyze the input text and return "
    "it in a structured way. The output should only include the following sections (as it is in the input) from the text and nothing else: "
    "1. 'Title and Abstract' \n"
    "2. 'Introduction' \n"
    "3. 'Eligibility Criteria used in SLR' \n"
    "4. 'Information Sources, Search Strategy, and Selection Process' \n"
    "5. 'Data Collection Process and Items in SLR' \n"
    "6. 'Risk of Bias and Effect Measures in SLR' \n"
    "7. 'Synthesis Methods' \n"
    "8. 'Reporting Bias and Certainty Assessment' \n"
    "9. 'Study Selection, Study Characteristics and Risk of Bias in SLR' \n"
    "10. 'Results of Individual Studies and Synthesis' \n"
    "11. 'Reporting Biases and Certainty of Evidence' \n"
    "12. 'Results, Limitations, and Implications in SLR' \n"
    "13. 'Other Information (Management of Administrative and Ethical aspects of SLR)' \n"
    "Analyze the text carefully and extract content to these sections."
    "If you can't find anything related to any section, just return empty string for that specific section only."
    "Do not omit/add anything from/in the input."
)

# =======================
# Output Format Agent
# =======================
SYSTEM_PROMPT_FORMATTER = f"""
You are a synthesis agent responsible for aggregating and structuring feedback from four different workforces of agents. Each workforce contains multiple agents, and your task is to consolidate their outputs into a cohesive structure. Follow these instructions carefully:

## *Input Details*:

You will receive outputs from four different workforces.
Each workforce's output will include scores and feedback from multiple agents.

## *Synthesis Task*:

Evaluate Scores: Combine the scores from all agents across all workforces to calculate an overall score. Ensure this score is an aggregation or weighted representation of the individual scores, depending on the context provided.
Summarize Feedback: Create an overall summary of the feedback provided by agents across all workforces. This should capture the key points and overarching themes of the feedback provided by the agents.
Organize Details per Agent: List the scores from all individual agents separated by new lines.
Feedback from Agents: Provide the feedback from all agents, one by one, separated by new lines.
Output Format:
Return the result in the following structured form using the Output_Format class:

Output_Format(
    Overall_SLR_Score="<Provide the overall score here>",
    Overall_Summary="<Provide the overall detailed summary here>",
    Scores_per_agent="<List the scores from all agents, one per line>",
    Feedback_per_agent="<List the feedback from all agents, one per line>"
)

## *Important Notes*:
Do not remove or add additional information.
Be concise yet comprehensive and thorough in your synthesis.
Maintain logical coherence and proper structure in your output.
Ensure there is no loss of critical information during the aggregation.
Use Markdown for formatting your response.
"""
# =======================
# Classification Agent
# =======================
classification_prompt_file = (
    "/home/zain/Desktop/LLM/GENAI-SLR-TOOL/systemPrompt_classifier_agent.md"
)
SYSTEM_PROMPT_CLS = None
with open(classification_prompt_file, "r") as p_file:
    SYSTEM_PROMPT_CLS = "".join(p_file.readlines())
