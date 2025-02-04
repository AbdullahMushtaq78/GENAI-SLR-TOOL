from .title_abstract_society import TITLE_AND_ABSTRACT_SOCIETY
from .introduction_society import INTRODUCTION_SOCIETY
from .methods_society import METHODS_SOCIETY
from .results_society import RESULTS_SOCIETY
from .discussion_society import DISCUSSION_SOCIETY
from .other_info_society import OTHER_INFO_SOCIETY

PERSONAS = [
    TITLE_AND_ABSTRACT_SOCIETY,
    INTRODUCTION_SOCIETY,
    METHODS_SOCIETY,
    RESULTS_SOCIETY,
    DISCUSSION_SOCIETY,
    OTHER_INFO_SOCIETY,
]

roles = {
    "1": [
        "SLR Title Evaluation Agent",
        "SLR Abstract Evaluation Agent",
    ],
    "2": [
        "SLR Rationale Evaluation Agent",
        "Objectives Compliance Evaluator Agent",
        "SLR Objectives Evaluation Agent",
    ],
    "3": [
        "SLR Eligibility Criteria Evaluation Agent",
        "SLR Information Sources Evaluation Agent",
        "SLR Search Strategy Evaluation Agent",
        "Selection Process Evaluator Agent",
        "Data Collection Process Evaluator Agent",
        "SLR Data Items Evaluation Agent",
        "Study Risk of Bias Evaluation Agent",
        "Effect Measures Evaluation Agent",
        "Reporting Bias Assessment Evaluator Agent",
        "Certainty Assessment Evaluator Agent",
        "Synthesis Methods Evaluation Agent",
    ],
    "4": [
        "Study Selection Evaluator",
        "Study Characteristics Reporting Agent",
        "Risk of Bias Reporting Agent",
        "Individual Study Results Reporting Agent",
        "Synthesis Results Evaluator",
        "Risk of Reporting Bias Assessment Agent",
        "Certainty of Evidence Assessment Agent",
    ],
    "5": [
        "Discussion Evaluator",
    ],
    "6": [
        "Registration and Protocol Evaluator",
        "Support and Funding Transparency Agent",
        "Competing Interests Disclosure Agent",
        "Data Sharing and Availability Agent",
    ],
}


print(PERSONAS[1]["Agents"][1]["Agent_Role"])
