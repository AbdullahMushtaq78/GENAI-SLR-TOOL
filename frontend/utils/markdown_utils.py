"""
This module provides utility functions for Markdown processing
"""

import markdown
from backend.config.configs import MARKDOWN_EXTENSIONS

def convert_markdown(text, add_score_styling=False):
    """
    Converts markdown text to HTML with standard extensions.
    
    Args:
        text: Markdown text to convert
        add_score_styling: Whether to add styling to scores (e.g., "Score: 4/5")
        
    Returns:
        str: HTML formatted content
    """
    # Add styling to scores if requested
    if add_score_styling:
        # Add bold to scores (e.g., "Score: 4/5" becomes "Score: **4/5**")
        text = text.replace("Score: ", "Score: **")
        text = text.replace("/5", "/5**")
        
        # Replace with styled score spans
        text = text.replace("**4/5**", "<strong class='score-value'>4/5</strong>")
        text = text.replace("**3/5**", "<strong class='score-value'>3/5</strong>")
        text = text.replace("**5/5**", "<strong class='score-value'>5/5</strong>")
        text = text.replace("**2/5**", "<strong class='score-value'>2/5</strong>")
        text = text.replace("**1/5**", "<strong class='score-value'>1/5</strong>")
    
    # Convert markdown to HTML
    return markdown.markdown(
        text,
        extensions=[
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
        ],
    )