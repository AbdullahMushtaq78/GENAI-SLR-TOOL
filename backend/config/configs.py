import os
from camel.agents import CriticAgent, ChatAgent
from camel.messages import BaseMessage
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.configs import ChatGPTConfig
from camel.societies.workforce import Workforce
from camel.tasks import Task
from camel.toolkits import FunctionTool, SearchToolkit, ArxivToolkit

from backend.personas import *
from typing import List
from dotenv import load_dotenv

load_dotenv()

PLATFORM = ModelPlatformType.OPENAI
MODEL = ModelType.GPT_4_1
TEMPERATURE = 0.0
MESSAGES_WINDOW = 50

# =======================
#         SLR-GPT
# =======================
SLR_GPT_PLATFORM = ModelPlatformType.OPENAI
SLR_GPT_MODEL = ModelType.GPT_4_1
SLR_GPT_TEMPERATURE = 1.0
SLR_GPT_MESSAGES_WINDOW = 100




# =======================
#          TOOLS
# =======================
TOOLS = [*ArxivToolkit().get_tools()]
arxiv_tool_prompt = """You have access to ArXiv to search for the latest research papers when needed. Use it only when relevant to the task.
Use ArXiv to find recent and reliable information when accuracy is important.
Use this tool wisely to provide well-researched and accurate responses.
Do not search the exact same paper provided to you from the user. Use the paper provided by the user as it is to ground your response. You can use this toolkit to search for other papers related to the topic of the paper provided by the user (if necessary). 
"""

TOOLS_PROMPT = arxiv_tool_prompt



# Flask app settings
PORT = int(os.environ.get('PORT', 5001))
DEBUG = os.environ.get('FLASK_ENV') != 'production'

# File paths
# Navigate up from the current file to the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(current_dir, "../.."))  # Go up two levels to reach project root

# Define upload and results folders at the project root
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Markdown extensions for text rendering
MARKDOWN_EXTENSIONS = [
    "abbr",
    "attr_list",
    "def_list",
    "fenced_code",
    "footnotes",
    "tables",
    "admonition",
    "codehilite",
    "meta",
    "nl2br",
    "sane_lists",
    "smarty",
    "toc",
    "wikilinks",
    "pymdownx.extra",
    "pymdownx.emoji",
    "pymdownx.tasklist",
    "pymdownx.superfences",
    "pymdownx.magiclink",
    "pymdownx.highlight",
    "pymdownx.keys",
    "pymdownx.arithmatex",
    "pymdownx.caret",
    "pymdownx.mark",
    "pymdownx.tilde",
    "pymdownx.smartsymbols",
    "pymdownx.betterem",
    "pymdownx.escapeall",
    "pymdownx.progressbar",
    "pymdownx.inlinehilite",
    "pymdownx.snippets",
    "pymdownx.details",
    "pymdownx.tabbed"
]

SOCIETIES_NAMES = [
    "Title & Abstract",
    "Introduction",
    "Methodology",
    "Results",
    "Discussion",
    "Other Information"
]