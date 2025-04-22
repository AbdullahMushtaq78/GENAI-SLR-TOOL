"""
This module contains functions to process and format analysis results.
"""

import re
from personas import roles, PERSONAS

def generate_society_cards(raw_result, convert_markdown_func):
    """
    Generates HTML for society cards from raw results.
    
    Args:
        raw_result: Dictionary containing the raw analysis results
        convert_markdown_func: Function to convert markdown to HTML
        
    Returns:
        str: HTML for all society cards
    """
    raw_cards = ""
    
    for i in range(1, 7):
        if i in raw_result:
            # Format the overall result to include headings and bold scores
            result_text = raw_result[i]["overall_result"]
            
            # Use regex to add styling to scores
            result_text = re.sub(r'\*\*([\d\.]+/5)\*\*', r'<strong class="score-value">\1</strong>', result_text)
            
            # Convert overall result to HTML
            converted_overall = convert_markdown_func(result_text, add_score_styling=True)
            
            # Convert agent results to HTML
            converted_agents = [
                convert_markdown_func(agent_res) 
                for agent_res in raw_result[i]["per_agent_result"]
            ]

            # Generate agent details sections
            agent_sections = ""
            for idx, agent_result in enumerate(raw_result[i]["per_agent_result"]):
                agent_id = f"agent_{i}_{idx}"

                # Get the agent name from the roles dictionary
                agent_name = (
                    roles[str(i)][idx]
                    if str(i) in roles and idx < len(roles[str(i)])
                    else f"Agent {idx + 1}"
                )

                # Convert agent result to HTML
                agent_content = convert_markdown_func(agent_result)

                # Define color class based on agent index
                agent_color_class = f"agent-color-{idx % 5}"
                
                # Define unique icon for each agent type
                agent_icons = [
                    "fa-user-graduate",  # Scholar/academic icon
                    "fa-chart-line",     # Data analyst icon
                    "fa-search",         # Investigator icon
                    "fa-clipboard-check", # Reviewer icon
                    "fa-comments"        # Discussion icon
                ]
                agent_icon = agent_icons[idx % 5]

                agent_sections += f"""
                    <div class="agent-section {agent_color_class}">
                        <button class="btn-show-agent {agent_color_class}" onclick="toggleVisibility(this, '{agent_id}')">
                            <span class="agent-number">{idx + 1}</span>
                            <i class="fas {agent_icon} agent-icon"></i>
                            <span class="agent-name">{agent_name}</span>
                            <span class="expand-indicator"><i class="fas fa-chevron-down"></i></span>
                        </button>
                        <div id="{agent_id}" class="hidden agent-details" style="display: none;">
                            <div class="detail-item {agent_color_class}">{agent_content}</div>
                        </div>
                    </div>
                """

            # Get workforce descriptions from personas
            descriptions = [
                wf_persona["Workforce_description"] for wf_persona in PERSONAS
            ]
            
            # Create the card
            card = f"""
                <div class="card raw-card society-{i}">
                    <h1 class="workforce-heading">{descriptions[i-1]}</h1>
                    <div class="result-section">
                        <h3 class="section-heading">Overall Assessment</h3>
                        <div class="result-content">{converted_overall}</div>
                    </div>
                    <button class="btn-show-more" onclick="toggleVisibility(this, 'agent_list_{i}')">
                        <i class="fas fa-chevron-down"></i>Show More
                    </button>
                    <div id="agent_list_{i}" class="hidden agents-list" style="display: none;">
                        {agent_sections}
                    </div>
                </div>
            """
            raw_cards += card
            
    return raw_cards