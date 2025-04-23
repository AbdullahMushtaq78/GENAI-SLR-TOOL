# Society color schemes - defines colors for each society
SOCIETY_COLORS = {
    1: {
        "name": "indigo",
        "primary": "#312e81",
        "secondary": "#4f46e5",
        "light": "rgba(79, 70, 229, 0.1)",
        "hover": "rgba(79, 70, 229, 0.15)"
    },
    2: {
        "name": "rose-dark",
        "primary": "#831843",
        "secondary": "#be185d",
        "light": "rgba(190, 24, 93, 0.1)",
        "hover": "rgba(190, 24, 93, 0.15)"
    },
    3: {
        "name": "cyan-dark",
        "primary": "#164e63",
        "secondary": "#0e7490",
        "light": "rgba(14, 116, 144, 0.1)",
        "hover": "rgba(14, 116, 144, 0.15)"
    },
    4: {
        "name": "violet-dark",
        "primary": "#4c1d95",
        "secondary": "#7c3aed",
        "light": "rgba(124, 58, 237, 0.1)",
        "hover": "rgba(124, 58, 237, 0.15)"
    },
    5: {
        "name": "slate",
        "primary": "#1e293b",
        "secondary": "#334155",
        "light": "rgba(51, 65, 85, 0.1)",
        "hover": "rgba(51, 65, 85, 0.15)"
    },
    6: {
        "name": "emerald-dark",
        "primary": "#064e3b",
        "secondary": "#047857",
        "light": "rgba(4, 120, 87, 0.1)",
        "hover": "rgba(4, 120, 87, 0.15)"
    }
}

# Function to generate society color CSS
def generate_society_css():
    css = ""
    for society_id, colors in SOCIETY_COLORS.items():
        # Create more subtle hover colors by reducing opacity further
        subtle_light = colors["light"].replace("0.1", "0.05")
        subtle_hover = colors["hover"]  # Reduced from 0.08 to 0.06
        
        css += f"""
            .society-{society_id} .raw-card::before {{
                background: linear-gradient(90deg, {colors['secondary']}, {colors['primary']});
            }}
            
            .society-{society_id} .workforce-heading {{
                color: {colors['primary']};
            }}
            
            .society-{society_id} .section-heading::before {{
                background-color: {colors['secondary']};
                box-shadow: 0 0 0 2px {subtle_light};
            }}
            
            .society-{society_id} .result-section {{
                border-left: 4px solid {colors['secondary']};
            }}
            
            .society-{society_id} .result-section::after {{
                background: linear-gradient(90deg, {subtle_light} 0%, {subtle_light} 100%);
            }}
            
            .society-{society_id} .result-section:hover {{
                border-left-color: {colors['primary']};
            }}
            
            .society-{society_id} .score-value {{
                background-color: {subtle_light};
                color: {colors['primary']};
            }}
            
            .society-{society_id} .result-section:hover .score-value {{
                background-color: {subtle_hover};
                box-shadow: 0 2px 4px {subtle_light};  # Reduced shadow intensity
            }}
            
            .society-{society_id} .btn-show-more {{
                background: linear-gradient(135deg, {colors['secondary']}, {colors['primary']});
            }}
            
            .society-{society_id} .btn-show-more:hover {{
                box-shadow: 0 4px 8px {subtle_light};  # Reduced shadow intensity
            }}
            
            .btn-show-agent {{
                background: rgba(255, 255, 255, 0.85);
                color: var(--text-primary);
                border: none;
                padding: 0.85rem 1.25rem;
                width: 100%;
                text-align: left;
                border-radius: 12px;
                transition: var(--transition-base);
                margin-bottom: 0.75rem;
                white-space: normal;
                line-height: 1.4;
                box-shadow: var(--shadow-md);
                position: relative;
                font-size: 0.95rem;
                overflow: hidden;
                font-weight: 600;
                backdrop-filter: blur(5px);
                border-left: 4px solid transparent;
            }}
            
            .btn-show-agent::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.2));
                opacity: 0.6;
                transition: opacity 0.3s ease;
                z-index: 0;
            }}
            
            .expand-indicator {{
                position: absolute;
                right: 1rem;
                top: 50%;
                transform: translateY(-50%);
                display: flex;
                align-items: center;
                justify-content: center;
                width: 24px;
                height: 24px;
                transition: all 0.2s ease;
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 50%;
                z-index: 1;
            }}
            
            .btn-show-agent .agent-number {{
                display: inline-block;
                background-color: rgba(0, 0, 0, 0.08);
                border-radius: 6px;
                padding: 0.15rem 0.5rem;
                margin-right: 0.6rem;
                font-weight: 700;
                font-size: 0.85rem;
                letter-spacing: 0.02em;
                position: relative;
                z-index: 1;
            }}
            
            .btn-show-agent .agent-icon {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                width: 1.6rem;
                margin-right: 0.5rem;
                text-align: center;
                position: relative;
                z-index: 1;
            }}
            
            .btn-show-agent .agent-name {{
                font-weight: 600;
                letter-spacing: 0.01em;
                position: relative;
                z-index: 1;
            }}
            
            .btn-show-agent:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            }}
            
            .btn-show-agent:hover::before {{
                opacity: 0.9;
            }}
            
            .agent-color-0 .btn-show-agent.agent-color-0 {{
                background: rgba(226, 232, 255, 0.8);
                border-left: 4px solid #4f46e5;
                color: #312e81;
            }}
            
            .agent-color-1 .btn-show-agent.agent-color-1 {{
                background: rgba(209, 250, 229, 0.8);
                border-left: 4px solid #0d9488;
                color: #064e3b;
            }}
            
            .agent-color-2 .btn-show-agent.agent-color-2 {{
                background: rgba(254, 240, 185, 0.8);
                border-left: 4px solid #d97706;
                color: #92400e;
            }}
            
            .agent-color-3 .btn-show-agent.agent-color-3 {{
                background: rgba(253, 224, 235, 0.8);
                border-left: 4px solid #db2777;
                color: #831843;
            }}
            
            .agent-color-4 .btn-show-agent.agent-color-4 {{
                background: rgba(237, 223, 252, 0.8);
                border-left: 4px solid #7c3aed;
                color: #4c1d95;
            }}
            
            .btn-show-agent.active {{
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
            }}
            
            .btn-show-agent.active .expand-indicator {{
                transform: translateY(-50%) rotate(180deg);
                background-color: rgba(0, 0, 0, 0.15);
            }}
            
            .agent-color-0 .btn-show-agent.agent-color-0.active,
            .agent-color-0 .btn-show-agent.agent-color-0:hover {{
                background: rgba(224, 231, 255, 0.9);
                box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
            }}
            
            .agent-color-1 .btn-show-agent.agent-color-1.active,
            .agent-color-1 .btn-show-agent.agent-color-1:hover {{
                background: rgba(204, 251, 241, 0.9);
                box-shadow: 0 8px 20px rgba(20, 184, 166, 0.2);
            }}
            
            .agent-color-2 .btn-show-agent.agent-color-2.active,
            .agent-color-2 .btn-show-agent.agent-color-2:hover {{
                background: rgba(255, 251, 235, 0.9);
                box-shadow: 0 8px 20px rgba(245, 158, 11, 0.2);
            }}
            
            .agent-color-3 .btn-show-agent.agent-color-3.active,
            .agent-color-3 .btn-show-agent.agent-color-3:hover {{
                background: rgba(253, 232, 242, 0.9);
                box-shadow: 0 8px 20px rgba(236, 72, 153, 0.2);
            }}
            
            .agent-color-4 .btn-show-agent.agent-color-4.active,
            .agent-color-4 .btn-show-agent.agent-color-4:hover {{
                background: rgba(243, 232, 255, 0.9);
                box-shadow: 0 8px 20px rgba(139, 92, 246, 0.2);
            }}
            
            .agent-color-0 .btn-show-agent.agent-color-0 .agent-number {{
                background-color: rgba(79, 70, 229, 0.15);
                color: #4338ca;
            }}
            
            .agent-color-1 .btn-show-agent.agent-color-1 .agent-number {{
                background-color: rgba(13, 148, 136, 0.15);
                color: #0f766e;
            }}
            
            .agent-color-2 .btn-show-agent.agent-color-2 .agent-number {{
                background-color: rgba(217, 119, 6, 0.15);
                color: #b45309;
            }}
            
            .agent-color-3 .btn-show-agent.agent-color-3 .agent-number {{
                background-color: rgba(219, 39, 119, 0.15);
                color: #be185d;
            }}
            
            .agent-color-4 .btn-show-agent.agent-color-4 .agent-number {{
                background-color: rgba(124, 58, 237, 0.15);
                color: #6d28d9;
            }}
            
            .agent-color-0 .btn-show-agent.agent-color-0 .expand-indicator {{
                background-color: rgba(79, 70, 229, 0.15);
                color: #4338ca;
            }}
            
            .agent-color-1 .btn-show-agent.agent-color-1 .expand-indicator {{
                background-color: rgba(13, 148, 136, 0.15);
                color: #0f766e;
            }}
            
            .agent-color-2 .btn-show-agent.agent-color-2 .expand-indicator {{
                background-color: rgba(217, 119, 6, 0.15);
                color: #b45309;
            }}
            
            .agent-color-3 .btn-show-agent.agent-color-3 .expand-indicator {{
                background-color: rgba(219, 39, 119, 0.15);
                color: #be185d;
            }}
            
            .agent-color-4 .btn-show-agent.agent-color-4 .expand-indicator {{
                background-color: rgba(124, 58, 237, 0.15);
                color: #6d28d9;
            }}
            
            .agent-section {{
                background: rgba(255, 255, 255, 0.5);
                padding: 0.9rem;
                border-radius: 12px;
                margin-bottom: 1rem;
                transition: var(--transition-base);
                backdrop-filter: blur(10px);
                position: relative;
                overflow: hidden;
                border: 2px solid transparent;
            }}
            
            .agent-section:hover {{
                transform: translateY(-3px);
                box-shadow: var(--shadow-lg);
                background: rgba(255, 255, 255, 0.65);
                border-color: rgba(255, 255, 255, 0.9);
            }}
            
            .agent-details {{
                margin-top: 1rem;
            }}
            
            .agent-details .detail-item {{
                background: white;
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: var(--shadow-md);
                transition: var(--transition-base);
                position: relative;
                z-index: 1;
                overflow: hidden;
            }}
            
            .agent-details .detail-item::after {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 20.5V18H0v-2h20v-2H0v-2h20v-2H0V8h20V6H0V4h20V2H0V0h22v20h2V0h2v20h2V0h2v20h2V0h2v20h2V0h2v20h2v2H20v-1.5zM0 20h2v20H0V20zm4 0h2v20H4V20zm4 0h2v20H8V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20z' fill='%236366f1' fill-opacity='0.02' fill-rule='evenodd'/%3E%3C/svg%3E");
                opacity: 0.6;
                z-index: -1;
                pointer-events: none;
            }}
            
            .agent-details .detail-item.agent-color-0 {{
                border-left: 4px solid var(--primary-color);
            }}
            
            .agent-details .detail-item.agent-color-1 {{
                border-left: 4px solid #0d9488;
            }}
            
            .agent-details .detail-item.agent-color-2 {{
                border-left: 4px solid #d97706;
            }}
            
            .agent-details .detail-item.agent-color-3 {{
                border-left: 4px solid #db2777;
            }}
            
            .agent-details .detail-item.agent-color-4 {{
                border-left: 4px solid #7c3aed;
            }}
            
            .agent-details .detail-item:hover {{
                box-shadow: var(--shadow-lg);
                transform: translateY(-2px);
            }}
            
            /* Agent section color variants with gradient backgrounds */
            .agent-section.agent-color-0 {{
                background: linear-gradient(to right, rgba(99, 102, 241, 0.08), rgba(79, 70, 229, 0.03));
                border-left: 4px solid var(--primary-color);
            }}
            
            .agent-section.agent-color-0:hover {{
                background: linear-gradient(to right, rgba(99, 102, 241, 0.12), rgba(79, 70, 229, 0.07));
            }}
            
            .agent-section.agent-color-1 {{
                background: linear-gradient(to right, rgba(20, 184, 166, 0.08), rgba(13, 148, 136, 0.03));
                border-left: 4px solid #0d9488;
            }}
            
            .agent-section.agent-color-1:hover {{
                background: linear-gradient(to right, rgba(20, 184, 166, 0.12), rgba(13, 148, 136, 0.07));
                border-left: 4px solid #0d9488;
            }}
            
            .agent-section.agent-color-2 {{
                background: linear-gradient(to right, rgba(245, 158, 11, 0.08), rgba(217, 119, 6, 0.03));
                border-left: 4px solid #d97706;
            }}
            
            .agent-section.agent-color-2:hover {{
                background: linear-gradient(to right, rgba(245, 158, 11, 0.12), rgba(217, 119, 6, 0.07));
                border-left: 4px solid #d97706;
            }}
            
            .agent-section.agent-color-3 {{
                background: linear-gradient(to right, rgba(236, 72, 153, 0.08), rgba(219, 39, 119, 0.03));
                border-left: 4px solid #db2777;
            }}
            
            .agent-section.agent-color-3:hover {{
                background: linear-gradient(to right, rgba(236, 72, 153, 0.12), rgba(219, 39, 119, 0.07));
                border-left: 4px solid #db2777;
            }}
            
            .agent-section.agent-color-4 {{
                background: linear-gradient(to right, rgba(139, 92, 246, 0.08), rgba(124, 58, 237, 0.03));
                border-left: 4px solid #7c3aed;
            }}
            
            .agent-section.agent-color-4:hover {{
                background: linear-gradient(to right, rgba(139, 92, 246, 0.12), rgba(124, 58, 237, 0.07));
                border-left: 4px solid #7c3aed;
            }}
        """
    return css