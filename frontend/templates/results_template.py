"""
This module contains HTML templates for rendering SLR evaluation results.
"""
from frontend.static.styles.static_styles import generate_society_css

def render_results_page(paper_title, raw_cards, generate_society_css):
    """
    Renders the HTML template for the results page.
    
    Args:
        paper_title: The title of the analyzed paper
        raw_cards: HTML content for each society card
        generate_society_css: Function to generate CSS for societies
        
    Returns:
        str: HTML template as a string
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>SLR Evaluation Results</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Montserrat:wght@700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {{
                --primary-color: #6366f1;
                --primary-dark: #4f46e5;
                --primary-light: #818cf8;
                --secondary-color: #ec4899;
                --bg-color: #f8fafc;
                --card-bg: #ffffff;
                --text-primary: #1e293b;
                --text-secondary: #64748b;
                --border-color: #e2e8f0;
                --success-color: #22c55e;
                --error-color: #ef4444;
                --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
                --transition-base: all 0.3s ease;
                --transition-bounce: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            }}
            
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
            }}
            
            body {{
                background-color: #f0f9ff;
                color: var(--text-primary);
                line-height: 1.6;
                padding: 2rem;
                position: relative;
                min-height: 100vh;
            }}
            
            body::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%236366f1' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
                opacity: 0.7;
                z-index: -1;
            }}
            
            /* Subtle gradient background */
            body::after {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%);
                z-index: -2;
            }}
            
            /* Add subtle top and bottom page accents */
            .page-accent-top {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 5px;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                z-index: 1000;
            }}
            
            .page-accent-bottom {{
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 5px;
                background: linear-gradient(90deg, var(--secondary-color), var(--primary-color));
                z-index: 1000;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            
            h2 {{
                color: var(--text-primary);
                margin: 2rem 0;
                font-weight: 700;
                text-align: center;
                font-size: 1.75rem;
                letter-spacing: -0.01em;
                font-family: 'Montserrat', sans-serif;
            }}
            
            .card {{
                background: var(--card-bg);
                border-radius: 16px;
                padding: 1.75rem;
                margin-bottom: 2rem;
                box-shadow: var(--shadow-lg);
                border: 1px solid rgba(255, 255, 255, 0.8);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            
            .card::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 7px;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            }}
            
            .card::after {{
                content: "";
                position: absolute;
                top: 7px;
                left: 0;
                width: 100%;
                height: calc(100% - 7px);
                background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20 20.5V18H0v-2h20v-2H0v-2h20v-2H0V8h20V6H0V4h20V2H0V0h22v20h2V0h2v20h2V0h2v20h2V0h2v20h2V0h2v20h2v2H20v-1.5zM0 20h2v20H0V20zm4 0h2v20H4V20zm4 0h2v20H8V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20zm4 0h2v20h-2V20z' fill='%236366f1' fill-opacity='0.02' fill-rule='evenodd'/%3E%3C/svg%3E");
                opacity: 0.6;
                z-index: 0;
                pointer-events: none;
            }}
            
            .card:hover {{
                transform: translateY(-3px);  /* Reduced from -5px */
                box-shadow: var(--shadow-lg);  /* Changed from var(--shadow-xl) to var(--shadow-lg) */
            }}
            
            .workforce-heading {{
                color: var(--primary-dark);
                font-size: 1.35rem;
                margin-bottom: 1.25rem;
                padding-bottom: 0.75rem;
                border-bottom: 1px solid var(--border-color);
                font-weight: 600;
                position: relative;
                z-index: 1;
                font-family: 'Montserrat', sans-serif;
            }}
            
            .section-heading {{
                color: var(--text-primary);
                font-size: 1.15rem;
                margin-bottom: 0.85rem;
                font-weight: 600;
                position: relative;
                z-index: 1;
                display: flex;
                align-items: center;
            }}
            
            .section-heading::before {{
                content: "";
                display: inline-block;
                width: 12px;
                height: 12px;
                background-color: var(--primary-color);
                border-radius: 50%;
                margin-right: 0.5rem;
                box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
            }}
            
            .result-section {{
                background: rgba(255, 255, 255, 0.6);
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 1.5rem;
                border-left: 4px solid var(--primary-color);
                transition: var(--transition-base);
                position: relative;
                overflow: hidden;
                backdrop-filter: blur(10px);
                box-shadow: var(--shadow-md);
            }}
            
            .result-section::after {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, rgba(99, 102, 241, 0.05) 0%, rgba(79, 70, 229, 0.05) 100%);
                opacity: 0;
                transition: opacity 0.3s ease;
                z-index: 0;
                pointer-events: none;
            }}
            
            .result-section:hover {{
                transform: translateY(-2px);  /* Reduced from -3px */
                box-shadow: var(--shadow-md);  /* Changed from var(--shadow-lg) to var(--shadow-md) */
                border-left-color: var(--secondary-color);
            }}
            
            .result-section:hover::after {{
                opacity: 1;
            }}
            
            .result-content {{
                line-height: 1.6;
                color: var(--text-secondary);
                position: relative;
                z-index: 1;
                font-size: 0.95rem;
            }}
            
            .result-content strong {{
                color: var(--primary-color);
                font-weight: 600;
                transition: var(--transition-base);
            }}
            
            /* Style for scores - we'll add a class in the markdown processing */
            .score-value {{
                display: inline-block;
                padding: 0.15rem 0.75rem;
                background-color: rgba(99, 102, 241, 0.1);
                border-radius: 12px;
                transition: var(--transition-base);
                font-family: "Poppins", sans-serif;
                font-weight: 600;
                color: var(--primary-dark);
                box-shadow: var(--shadow-sm);
            }}
            
            .result-section:hover .score-value {{
                background-color: rgba(99, 102, 241, 0.15);
                transform: translateY(-1px) scale(1.05);
                box-shadow: 0 3px 10px rgba(99, 102, 241, 0.2);
            }}
            
            .result-section:hover .result-content strong {{
                color: var(--secondary-color);
            }}
            
            /* Paper title display */
            .paper-title-container {{
                margin: 2rem 0 3rem;
                text-align: center;
                position: relative;
                padding: 0 1rem;
            }}
            
            .paper-title-wrapper {{
                max-width: 80%;
                margin: 0 auto;
                position: relative;
                background: rgba(255, 255, 255, 0.8);
                border-radius: 16px;
                padding: 1.75rem 2rem;
                box-shadow: var(--shadow-lg);
                border: 1px solid rgba(255, 255, 255, 0.5);
                overflow: hidden;
                backdrop-filter: blur(10px);
                animation: fadeIn 1s ease forwards;
            }}
            
            .paper-title-wrapper::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 7px;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            }}
            
            .paper-title {{
                font-family: 'Montserrat', sans-serif;
                font-size: 1.35rem;
                font-weight: 600;
                color: var(--text-primary);
                line-height: 1.5;
                margin: 0;
                text-align: center;
            }}
            
            .paper-title-label {{
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--text-secondary);
                font-weight: 600;
                margin-bottom: 0.5rem;
                display: block;
                text-align: center;
            }}
            
            @media (max-width: 768px) {{
                .paper-title-wrapper {{
                    max-width: 90%;
                    padding: 1.5rem 1.75rem;
                }}
                
                .paper-title {{
                    font-size: 1.15rem;
                }}
            }}
            
            @media (max-width: 480px) {{
                .paper-title-wrapper {{
                    max-width: 100%;
                    padding: 1.25rem 1.5rem;
                }}
                
                .paper-title {{
                    font-size: 1.05rem;
                }}
            }}
            
            .btn-show-more {{
                background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                color: white;
                border: none;
                padding: 0.7rem 1.25rem;
                border-radius: 12px;
                cursor: pointer;
                font-size: 0.9rem;
                transition: var(--transition-base);
                margin: 1rem 0;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                width: fit-content;
                font-weight: 500;
                box-shadow: var(--shadow-md);
            }}
            
            .btn-show-more i {{
                margin-right: 8px;
                font-size: 0.8rem;
                transition: transform 0.3s ease;
            }}
            
            .btn-show-more.active i {{
                transform: rotate(180deg);
            }}
            
            .btn-show-more:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 15px rgba(99, 102, 241, 0.3);
            }}
            
            .hidden {{
                display: none;
                margin-top: 0.75rem;
            }}
            
            .agents-list {{
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
            }}
            
            .detail-item {{
                background: white;
                padding: 1.25rem;
                border-radius: 12px;
                border-left: 4px solid var(--primary-color);
                margin-top: 0.75rem;
            }}
            
            .detail-item p {{
                margin: 0.75rem 0;
                color: var(--text-secondary);
            }}
            
            .main-header {{
                text-align: center;
                padding: 3rem 0;
                background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                color: white;
                margin-bottom: 3rem;
                border-radius: 20px;
                box-shadow: 0 15px 30px rgba(79, 70, 229, 0.2);
                position: relative;
                overflow: hidden;
                animation: fadeIn 1s ease forwards;
            }}
            
            .main-header::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url("data:image/svg+xml,%3Csvg width='52' height='26' viewBox='0 0 52 26' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M10 10c0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6h2c0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4 3.314 0 6 2.686 6 6 0 2.21 1.79 4 4 4v2c-3.314 0-6-2.686-6-6 0-2.21-1.79-4-4-4-3.314 0-6-2.686-6-6zm25.464-1.95l8.486 8.486-1.414 1.414-8.486-8.486 1.414-1.414z' /%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
                opacity: 0.3;
            }}
            
            .main-header h1 {{
                font-size: 2.5rem;
                margin-bottom: 0.75rem;
                font-weight: 800;
                letter-spacing: -0.01em;
                position: relative;
                font-family: 'Montserrat', sans-serif;
            }}
            
            .main-header p {{
                font-size: 1.15rem;
                opacity: 0.9;
                position: relative;
                max-width: 80%;
                margin: 0 auto;
            }}
            
            /* Floating back button with animation */
            .btn-go-back {{
                position: fixed;
                bottom: 2rem;
                left: 2rem;
                background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
                color: white;
                width: 3.75rem;
                height: 3.75rem;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                text-decoration: none;
                box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
                transition: var(--transition-bounce);
                z-index: 100;
            }}
            
            .btn-go-back:hover {{
                transform: scale(1.1) rotate(-5deg);
                box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
            }}
            
            .btn-go-back i {{
                font-size: 1.25rem;
                transition: transform 0.3s ease;
            }}
            
            .btn-go-back:hover i {{
                transform: translateX(-3px);
            }}
            
            /* Animation keyframes */
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            @keyframes slideInRight {{
                from {{ opacity: 0; transform: translateX(30px); }}
                to {{ opacity: 1; transform: translateX(0); }}
            }}
            
            @keyframes slideInLeft {{
                from {{ opacity: 0; transform: translateX(-30px); }}
                to {{ opacity: 1; transform: translateX(0); }}
            }}
            
            @keyframes pulse {{
                0% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }}
                70% {{ box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }}
                100% {{ box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }}
            }}
            
            /* Apply animations to elements */
            .main-header {{
                animation: fadeIn 1s ease forwards;
            }}
            
            .card {{
                animation: fadeIn 0.6s ease forwards;
                animation-delay: calc(var(--animation-order, 0) * 0.1s);
            }}
            
            .result-section {{
                animation: slideInRight 0.6s ease forwards;
                animation-delay: 0.2s;
            }}
            
            /* Typing indicator style */
            .typing-indicator {{
                display: flex;
                align-items: center;
                justify-content: center;
                height: 20px;
            }}
            
            .typing-indicator span {{
                height: 8px;
                width: 8px;
                background: var(--primary-color);
                border-radius: 50%;
                display: inline-block;
                margin: 0 2px;
                opacity: 0.6;
                animation: typing 1s infinite;
            }}
            
            .typing-indicator span:nth-child(1) {{
                animation-delay: 0s;
            }}
            
            .typing-indicator span:nth-child(2) {{
                animation-delay: 0.2s;
            }}
            
            .typing-indicator span:nth-child(3) {{
                animation-delay: 0.4s;
            }}
            
            @keyframes typing {{
                0% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-5px); }}
                100% {{ transform: translateY(0); }}
            }}
            
            /* Download button styles */
            .results-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 1.5rem;
            }}
            
            .btn-download {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: var(--primary-color);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                box-shadow: var(--shadow-md);
            }}
            
            .btn-download:hover {{
                background-color: var(--primary-dark);
                transform: translateY(-2px);
                box-shadow: var(--shadow-lg);
            }}
            
            .btn-download i {{
                margin-right: 0.5rem;
            }}
            
            {generate_society_css()}
        </style>
    </head>
    <body>
        <div class="page-accent-top"></div>
        <div class="container">
            <div class="main-header">
                <h1>SLR Paper Evaluator</h1>
                <p>Automated Systematic Literature Review Analysis Using Advanced Language Models</p>
            </div>
            
            <div class="paper-title-container">
                <div class="paper-title-wrapper">
                    <div class="paper-title-label">ANALYZING PAPER</div>
                    <div class="paper-title">{paper_title}</div>
                </div>
            </div>
            
            <div class="results-header">
                <h2>Detailed Analysis Results</h2>
                <a href="/download/{paper_title}" class="btn-download" title="Download Results">
                    <i class="fas fa-download"></i> Download Results
                </a>
            </div>
            
            {raw_cards}
        </div>

        <a href="/" class="btn-go-back" title="Go Back">
            <i class="fas fa-arrow-left"></i>
        </a>
        
        <div class="page-accent-bottom"></div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                // Add animation order to cards
                const cards = document.querySelectorAll('.card');
                cards.forEach((card, index) => {{
                    card.style.setProperty('--animation-order', index + 1);
                }});
            }});
        
            function toggleVisibility(btn, id) {{
                const content = document.getElementById(id);
                const isHidden = content.style.display === "none" || content.style.display === "";
                
                // Check if this is a show-more button or an agent button
                const isShowMoreBtn = btn.classList.contains('btn-show-more');
                
                if (isShowMoreBtn) {{
                    // For Show More button, just rotate the icon
                    const icon = btn.querySelector('i');
                    
                    if (isHidden) {{
                        content.style.display = "block";
                        icon.className = "fas fa-chevron-up";
                        btn.classList.add('active');
                        btn.innerHTML = '<i class="fas fa-chevron-up"></i>Show Less';
                    }} else {{
                        content.style.display = "none";
                        icon.className = "fas fa-chevron-down";
                        btn.classList.remove('active');
                        btn.innerHTML = '<i class="fas fa-chevron-down"></i>Show More';
                    }}
                }} else {{
                    // For agent buttons, use the expand indicator
                    const indicator = btn.querySelector('.expand-indicator i');
                    
                    if (isHidden) {{
                        content.style.display = "block";
                        indicator.className = "fas fa-chevron-up";
                        btn.classList.add('active');
                    }} else {{
                        content.style.display = "none";
                        indicator.className = "fas fa-chevron-down";
                        btn.classList.remove('active');
                    }}
                }}
            }}
        </script>
    </body>
    </html>
    """