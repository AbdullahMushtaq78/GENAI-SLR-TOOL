def render_upload_form():
    """Returns the HTML for the upload form"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>MAS-SLR Analysis</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Montserrat:wght@700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            :root {
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
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
            }
            
            body {
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #bae6fd 100%);
                padding: 2rem;
                position: relative;
                overflow-x: hidden;
            }
            
            body::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%236366f1' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
                z-index: -1;
            }
            
            .container {
                width: 100%;
                max-width: 520px;
                background: var(--card-bg);
                padding: 2.5rem;
                border-radius: 20px;
                box-shadow: var(--shadow-xl);
                position: relative;
                overflow: hidden;
                transform: translateY(0);
                transition: var(--transition-base);
                border: 1px solid rgba(255, 255, 255, 0.5);
            }
            
            .container:hover {
                transform: translateY(-5px);
                box-shadow: var(--shadow-2xl);
            }
            
            .container::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 7px;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
            }
            
            .container::after {
                content: "";
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 200px;
                background: radial-gradient(circle at 90% 90%, var(--primary-light) 0%, transparent 55%);
                opacity: 0.1;
                z-index: -1;
            }
            
            h1 {
                color: var(--text-primary);
                margin-bottom: 0.5rem;
                text-align: center;
                font-weight: 700;
                font-size: 2rem;
                letter-spacing: -0.025em;
                font-family: 'Montserrat', sans-serif;
            }
            
            .subtitle {
                color: var(--text-secondary);
                text-align: center;
                margin-bottom: 2rem;
                font-size: 0.95rem;
            }
            
            .form-group {
                margin-bottom: 1.75rem;
            }
            
            label {
                display: block;
                margin-bottom: 0.5rem;
                color: var(--text-primary);
                font-weight: 500;
                font-size: 0.95rem;
                transition: var(--transition-base);
            }
            
            .input-wrapper {
                position: relative;
            }
            
            .input-icon {
                position: absolute;
                left: 1rem;
                top: 50%;
                transform: translateY(-50%);
                color: var(--text-secondary);
                transition: var(--transition-base);
            }
            
            input[type="text"],
            input[type="file"] {
                width: 100%;
                padding: 0.9rem 1rem 0.9rem 2.75rem;
                border: 2px solid var(--border-color);
                border-radius: 12px;
                font-size: 1rem;
                transition: var(--transition-base);
                background-color: white;
                color: var(--text-primary);
            }
            
            input[type="text"]:focus,
            input[type="file"]:focus {
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
            }
            
            input[type="text"]:focus + .input-icon,
            input[type="file"]:focus + .input-icon {
                color: var(--primary-color);
            }
            
            .file-input-wrapper {
                position: relative;
                margin-top: 0.5rem;
            }
            
            .file-drop-area {
                position: relative;
                padding: 2rem;
                border: 2px dashed var(--border-color);
                border-radius: 12px;
                text-align: center;
                transition: var(--transition-base);
                cursor: pointer;
                background-color: rgba(255, 255, 255, 0.5);
            }
            
            .file-drop-area:hover {
                border-color: var(--primary-color);
                background-color: rgba(99, 102, 241, 0.05);
            }
            
            .file-message {
                font-size: 0.95rem;
                color: var(--text-secondary);
                margin-bottom: 0.5rem;
            }
            
            .file-icon {
                font-size: 2rem;
                color: var(--primary-color);
                margin-bottom: 0.5rem;
                transition: var(--transition-base);
            }
            
            .file-drop-area:hover .file-icon {
                transform: translateY(-5px);
            }
            
            input[type="file"] {
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                opacity: 0;
                cursor: pointer;
            }
            
            .btn-submit {
                width: 100%;
                padding: 1rem;
                background: linear-gradient(90deg, var(--primary-color), var(--primary-dark));
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 1rem;
                font-weight: 500;
                cursor: pointer;
                transition: var(--transition-base);
                position: relative;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            }
            
            .btn-submit:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
            }
            
            .btn-submit:active {
                transform: translateY(0);
            }
            
            .btn-submit::after {
                content: "";
                position: absolute;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                pointer-events: none;
                background-image: radial-gradient(circle, #fff 10%, transparent 10.01%);
                background-repeat: no-repeat;
                background-position: 50%;
                transform: scale(10, 10);
                opacity: 0;
                transition: transform 0.5s, opacity 1s;
            }
            
            .btn-submit:active::after {
                transform: scale(0, 0);
                opacity: 0.3;
                transition: 0s;
            }
            
            /* Disabled button styles */
            .btn-submit:disabled {
                background: linear-gradient(90deg, #a5b4fc, #818cf8); 
                cursor: not-allowed;
                opacity: 0.7;
                box-shadow: none;
            }
            
            /* Loading indicator styles */
            #loading {
                display: none;
                text-align: center;
                margin-top: 20px;
                padding: 1rem;
                border-radius: 12px;
                background: rgba(255, 255, 255, 0.8);
                backdrop-filter: blur(5px);
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
                70% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }
                100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0); }
            }
            
            .loading-text {
                color: var(--primary-dark);
                font-weight: 500;
                margin-bottom: 0.5rem;
            }
            
            .spinner {
                display: inline-block;
                width: 40px;
                height: 40px;
                border: 4px solid rgba(99, 102, 241, 0.1);
                border-radius: 50%;
                border-top-color: var(--primary-color);
                animation: spin 1s ease-in-out infinite;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            /* Subtle decorative elements */
            .decoration-circle {
                position: absolute;
                border-radius: 50%;
                z-index: -1;
            }
            
            .circle-1 {
                width: 100px;
                height: 100px;
                top: -30px;
                right: -30px;
                background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(99, 102, 241, 0.3));
            }
            
            .circle-2 {
                width: 80px;
                height: 80px;
                bottom: -20px;
                left: -20px;
                background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(236, 72, 153, 0.3));
            }
            
            /* Responsive styles */
            @media (max-width: 600px) {
                body {
                    padding: 1.5rem;
                }
                
                .container {
                    padding: 1.75rem;
                }
                
                h1 {
                    font-size: 1.75rem;
                }
                
                .subtitle {
                    font-size: 0.85rem;
                }
                
                .file-drop-area {
                    padding: 1.5rem;
                }
                
                .file-icon {
                    font-size: 1.75rem;
                }
            }
            
            /* Animation classes */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .animate-fade-in {
                animation: fadeIn 0.6s ease forwards;
            }
            
            .delay-1 {
                animation-delay: 0.1s;
            }
            
            .delay-2 {
                animation-delay: 0.2s;
            }
            
            .delay-3 {
                animation-delay: 0.3s;
            }
        </style>
        <script>
            // Store the event source as a global variable
            let progressEventSource = null;
            
            function showLoading() {
                document.getElementById('loading').style.display = 'block';
                document.querySelector('.btn-submit').disabled = true;
                
                // Connect to the progress update server
                setupProgressUpdates();
                
                return true;
            }
            
            // Function to update loading message
            function updateLoadingMessage(message) {
                const loadingText = document.getElementById('loading-text');
                if (loadingText) {
                    loadingText.textContent = message;
                    console.log("Updated loading message:", message);
                }
            }
            
            // Set up event source for server-sent events
            function setupProgressUpdates() {
                try {
                    // Close existing connection if any
                    if (progressEventSource) {
                        progressEventSource.close();
                    }
                    
                    // Connect to progress updates endpoint
                    // Use the correct port and host as configured in server.py
                    const serverUrl = window.location.protocol + '//' + window.location.hostname + ':5002/progress-updates';
                    console.log("Connecting to progress updates at:", serverUrl);
                    
                    progressEventSource = new EventSource(serverUrl);
                    
                    progressEventSource.onmessage = function(event) {
                        console.log("Received progress update:", event.data);
                        updateLoadingMessage(event.data);
                    };
                    
                    progressEventSource.onerror = function(error) {
                        console.error("Error with progress updates:", error);
                        // Try to reconnect after a delay
                        setTimeout(setupProgressUpdates, 3000);
                    };
                    
                    // Test connection with a timeout
                    setTimeout(function() {
                        if (progressEventSource.readyState !== 1) {
                            console.warn("Progress update connection not established within timeout");
                        } else {
                            console.log("Progress update connection established successfully");
                        }
                    }, 2000);
                    
                } catch (error) {
                    console.error("Failed to setup progress updates:", error);
                }
            }
            
            document.addEventListener('DOMContentLoaded', function() {
                // File input handling
                const fileInput = document.getElementById('paper_pdf');
                const fileMessage = document.querySelector('.file-message');
                const originalMessage = fileMessage.textContent;
                
                fileInput.addEventListener('change', function() {
                    if (this.files && this.files[0]) {
                        const fileName = this.files[0].name;
                        fileMessage.textContent = 'Selected: ' + fileName;
                    } else {
                        fileMessage.textContent = originalMessage;
                    }
                });
                
                // Add animation to form elements
                const animatedElements = document.querySelectorAll('.animate-fade-in');
                animatedElements.forEach(element => {
                    element.style.opacity = '0';
                    setTimeout(() => {
                        element.style.opacity = '1';
                    }, 100);
                });
                
                // Setup progress updates when form is submitted
                const form = document.querySelector('form');
                form.addEventListener('submit', function() {
                    setupProgressUpdates();
                });
            });
        </script>
    </head>
    <body>
        <div class="container">
            <div class="decoration-circle circle-1"></div>
            <div class="decoration-circle circle-2"></div>
            
            <h1 class="animate-fade-in">MAS-SLR Analysis</h1>
            <p class="subtitle animate-fade-in delay-1">Upload your research paper for systematic literature review analysis</p>
            
            <form method="POST" enctype="multipart/form-data" onsubmit="return showLoading()">
                <div class="form-group animate-fade-in delay-2">
                    <label for="paper_title">Paper Title</label>
                    <div class="input-wrapper">
                        <input type="text" 
                               id="paper_title" 
                               name="paper_title" 
                               placeholder="Enter the title of your paper"
                               required>
                        <i class="fas fa-heading input-icon"></i>
                    </div>
                </div>
                
                <div class="form-group animate-fade-in delay-3">
                    <label for="paper_pdf">Upload PDF</label>
                    <div class="file-drop-area">
                        <i class="fas fa-file-pdf file-icon"></i>
                        <p class="file-message">Drag & drop your PDF file here or click to browse</p>
                        <input type="file" 
                               id="paper_pdf" 
                               name="paper_pdf" 
                               accept=".pdf"
                               required>
                    </div>
                </div>
                
                <button type="submit" class="btn-submit animate-fade-in delay-3">
                    <i class="fas fa-robot"></i>
                    Analyze Paper
                </button>
            </form>
            
            <div id="loading">
                <p id="loading-text" class="loading-text">Processing your request, please wait...</p>
                <div class="spinner"></div>
            </div>
        </div>
    </body>
    </html>
    """