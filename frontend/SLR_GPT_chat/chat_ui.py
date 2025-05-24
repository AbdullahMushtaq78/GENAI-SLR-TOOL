"""
This module contains the chat interface template and functionality.
"""

def render_chat_ui():
    """
    Renders the HTML for the chat interface overlay.
    
    Returns:
        str: HTML for the chat interface
    """
    return """
    <!-- Chatbot button and overlay -->
    <div class="chat-btn" id="chatButton" title="Ask about the paper">
        <i class="fas fa-robot"></i>
    </div>
    
    <!-- PDF Viewer button and overlay -->
    <div class="pdf-btn" id="pdfButton" title="View agents' division">
        <i class="fas fa-project-diagram"></i>
    </div>
    
    <!-- PRISMA Guidelines button and overlay -->
    <div class="prisma-btn" id="prismaButton" title="View PRISMA Guidelines">
        <i class="fas fa-clipboard-check"></i>
    </div>
    
    <!-- PDF Overlay -->
    <div class="pdf-overlay" id="pdfOverlay">
        <div class="pdf-container">
            <div class="pdf-header">
                <h3>Agents Division Visualization</h3>
                <button class="close-pdf" id="closePdf">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="pdf-body">
                <iframe id="pdfViewer" src="/frontend/assets/Mindmap.pdf" width="100%" height="100%"></iframe>
            </div>
        </div>
    </div>
    
    <!-- PRISMA Guidelines Overlay -->
    <div class="prisma-overlay" id="prismaOverlay">
        <div class="prisma-container">
            <div class="prisma-header">
                <h3>PRISMA Guidelines</h3>
                <button class="close-prisma" id="closePrisma">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="prisma-body">
                <iframe id="prismaViewer" src="/frontend/assets/PRISMA_guidelines.pdf" width="100%" height="100%"></iframe>
            </div>
        </div>
    </div>
    
    <div class="chat-overlay" id="chatOverlay">
        <div class="chat-container">
            <div class="chat-header">
                <div class="ai-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <h3>SLR-GPT Assistant</h3>
                <button class="close-chat" id="closeChat">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="chat-body">
                <div class="chat-messages" id="chatMessages">
                    <div class="message bot-message">
                        <div class="message-content">
                            <div class="message-avatar">
                                <i class="fas fa-robot"></i>
                            </div>
                            <div class="message-bubble">
                                <p>👋 Hi there! I'm your SLR-GPT Assistant. I can help answer questions about the analysis of your paper. What would you like to know?</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="chat-input-container">
                <textarea class="chat-input" id="chatInput" placeholder="Ask me anything about the paper analysis..." rows="1"></textarea>
                <button class="send-btn" id="sendMessage">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
        </div>
    </div>
    """

def get_chat_css():
    """
    Returns the CSS styles for the chat interface.
    
    Returns:
        str: CSS styles for chat interface
    """
    return """
    /* Chatbot UI elements with improved styling and animations */
    .chat-btn {
        position: fixed;
        top: 2rem;
        right: 2rem;
        width: 3.75rem;
        height: 3.75rem;
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
        transition: var(--transition-bounce);
        z-index: 1000;
        animation: pulse 2s infinite;
    }
    
    /* PDF Button styles */
    .pdf-btn {
        position: fixed;
        top: 6.5rem;
        right: 2rem;
        width: 3.75rem;
        height: 3.75rem;
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4);
        transition: var(--transition-bounce);
        z-index: 1000;
        animation: pulse-pdf 2s infinite;
    }
    
    /* PRISMA Button styles */
    .prisma-btn {
        position: fixed;
        top: 11rem;
        right: 2rem;
        width: 3.75rem;
        height: 3.75rem;
        background: linear-gradient(135deg, #8b5cf6, #6366f1);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
        transition: var(--transition-bounce);
        z-index: 1000;
        animation: pulse-prisma 2s infinite;
    }
    
    @keyframes pulse-pdf {
        0% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }
    
    @keyframes pulse-prisma {
        0% {
            box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(139, 92, 246, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(139, 92, 246, 0);
        }
    }
    
    .pdf-btn i {
        font-size: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .pdf-btn:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5);
    }
    
    .pdf-btn:hover i {
        transform: scale(1.1);
    }
    
    .prisma-btn i {
        font-size: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .prisma-btn:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.5);
    }
    
    .prisma-btn:hover i {
        transform: scale(1.1);
    }
    
    /* PDF Overlay styles */
    .pdf-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(5px);
        z-index: 1001;
        display: none;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .pdf-overlay.visible {
        opacity: 1;
    }
    
    .pdf-container {
        width: 80%;
        height: 90vh;
        background-color: #0f172a;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transform: translateY(30px);
        opacity: 0;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s ease;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .pdf-overlay.visible .pdf-container {
        transform: translateY(0);
        opacity: 1;
    }
    
    .pdf-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        background: linear-gradient(135deg, #059669, #10b981);
        color: white;
        border-bottom: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .pdf-header h3 {
        margin: 0;
        font-weight: 600;
        font-size: 1.25rem;
        letter-spacing: -0.01em;
        font-family: 'Montserrat', sans-serif;
        color: #fff;
    }
    
    .close-pdf {
        background: rgba(255, 255, 255, 0.15);
        border: none;
        color: white;
        font-size: 1.25rem;
        cursor: pointer;
        transition: var(--transition-base);
        width: 2.25rem;
        height: 2.25rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .close-pdf:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: rotate(90deg);
    }
    
    .pdf-body {
        flex: 1;
        overflow: hidden;
        background-color: #1e293b;
    }
    
    #pdfViewer {
        border: none;
        background-color: white;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(99, 102, 241, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(99, 102, 241, 0);
        }
    }
    
    .chat-btn i {
        font-size: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .chat-btn:hover {
        transform: scale(1.1) rotate(5deg);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
    }
    
    .chat-btn:hover i {
        transform: scale(1.1);
    }
    
    .chat-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(5px);
        z-index: 1001;
        display: none;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .chat-overlay.visible {
        opacity: 1;
    }
    
    .chat-container {
        width: 70%;
        height: 80vh;
        background-color: #0f172a;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transform: translateY(30px);
        opacity: 0;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s ease;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .chat-overlay.visible .chat-container {
        transform: translateY(0);
        opacity: 1;
    }
    
    .chat-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        background: linear-gradient(135deg, #1e1b4b, #312e81);
        color: white;
        border-bottom: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    .chat-header h3 {
        margin: 0;
        font-weight: 600;
        font-size: 1.25rem;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        font-family: 'Montserrat', sans-serif;
        color: #fff;
    }
    
    .ai-avatar {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        margin-right: 1rem;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
    }
    
    .ai-avatar i {
        font-size: 1.2rem;
        color: white;
    }
    
    .close-chat {
        background: rgba(255, 255, 255, 0.15);
        border: none;
        color: white;
        font-size: 1.25rem;
        cursor: pointer;
        transition: var(--transition-base);
        width: 2.25rem;
        height: 2.25rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .close-chat:hover {
        transform: rotate(90deg);
        background-color: rgba(255, 255, 255, 0.25);
    }
    
    .chat-body {
        flex: 1;
        padding: 1.75rem;
        overflow-y: auto;
        background-color: #1e293b;
        scrollbar-width: thin;
        scrollbar-color: #64748b #1e293b;
    }
    
    .chat-body::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-body::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    .chat-body::-webkit-scrollbar-thumb {
        background-color: #64748b;
        border-radius: 6px;
    }
    
    .chat-messages {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .message {
        max-width: 80%;
        animation: fadeIn 0.3s ease;
        font-size: 0.95rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .message-content {
        display: flex;
        align-items: flex-start;
    }
    
    .message-avatar {
        width: 2rem;
        height: 2rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 0.75rem;
        flex-shrink: 0;
    }
    
    .user-message .message-avatar {
        background: linear-gradient(135deg, #8b5cf6, #6366f1);
        color: white;
    }
    
    .bot-message .message-avatar {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
    }
    
    .message-bubble {
        padding: 1rem 1.25rem;
        border-radius: 18px;
        line-height: 1.5;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        align-self: flex-end;
    }
    
    .user-message .message-bubble {
        background: linear-gradient(135deg, #8b5cf6, #6366f1);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .bot-message {
        align-self: flex-start;
    }
    
    .bot-message .message-bubble {
        background-color: #334155;
        color: #f8fafc;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .chat-input-container {
        padding: 1.25rem 1.5rem;
        background-color: #0f172a;
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        display: flex;
        gap: 0.75rem;
        align-items: flex-end;
    }
    
    .chat-input {
        flex: 1;
        padding: 1rem 1.25rem;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        font-size: 0.95rem;
        resize: none;
        max-height: 150px;
        transition: var(--transition-base);
        font-family: 'Poppins', sans-serif;
        background-color: #1e293b;
        color: #f8fafc;
    }
    
    .chat-input::placeholder {
        color: #94a3b8;
    }
    
    .chat-input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25);
    }
    
    .send-btn {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
        border: none;
        padding: 0.9rem;
        width: 3.5rem;
        height: 3.5rem;
        border-radius: 50%;
        cursor: pointer;
        font-weight: 500;
        transition: var(--transition-base);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
    }
    
    .send-btn i {
        transition: transform 0.2s ease;
        font-size: 1.1rem;
    }
    
    .send-btn:hover {
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.4);
    }
    
    .send-btn:hover i {
        transform: translateX(2px);
    }
    
    /* Typing indicator animation */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 0.5rem 1rem;
    }
    
    .typing-indicator span {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #94a3b8;
        border-radius: 50%;
        animation: typingAnimation 1.5s infinite ease-in-out;
    }
    
    .typing-indicator span:nth-child(1) {
        animation-delay: 0s;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typingAnimation {
        0%, 100% {
            transform: translateY(0);
            background-color: #64748b;
        }
        50% {
            transform: translateY(-5px);
            background-color: #94a3b8;
        }
    }
    
    /* AI text typing effect */
    .typewriter {
        white-space: break-spaces;
        overflow: hidden;
        opacity: 0;
    }
    
    .typewriter.typing {
        opacity: 1;
    }
    
    /* Responsive adjustments for chat UI */
    @media (max-width: 992px) {
        .chat-container {
            width: 85%;
        }
    }
    
    @media (max-width: 768px) {
        .chat-container {
            width: 90%;
            height: 85vh;
        }
        
        .chat-btn {
            top: 1.5rem;
            right: 1.5rem;
            width: 3.25rem;
            height: 3.25rem;
        }
        
        .message {
            max-width: 85%;
        }
    }
    
    @media (max-width: 480px) {
        .chat-container {
            width: 95%;
            height: 90vh;
        }
        
        .chat-header {
            padding: 1rem 1.25rem;
        }
        
        .chat-body {
            padding: 1.25rem;
        }
        
        body {
            padding: 1.25rem;
        }
        
        .message {
            max-width: 90%;
        }
        
        .message-bubble {
            padding: 0.9rem 1.1rem;
        }
    }
    
    /* PRISMA Overlay styles */
    .prisma-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(5px);
        z-index: 1001;
        display: none;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .prisma-overlay.visible {
        opacity: 1;
    }
    
    .prisma-container {
        width: 80%;
        height: 90vh;
        background-color: #0f172a;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transform: translateY(30px);
        opacity: 0;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s ease;
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .prisma-overlay.visible .prisma-container {
        transform: translateY(0);
        opacity: 1;
    }
    
    .prisma-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border-bottom: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    .prisma-header h3 {
        margin: 0;
        font-weight: 600;
        font-size: 1.25rem;
        letter-spacing: -0.01em;
        font-family: 'Montserrat', sans-serif;
        color: #fff;
    }
    
    .close-prisma {
        background: rgba(255, 255, 255, 0.15);
        border: none;
        color: white;
        font-size: 1.25rem;
        cursor: pointer;
        transition: var(--transition-base);
        width: 2.25rem;
        height: 2.25rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .close-prisma:hover {
        background: rgba(255, 255, 255, 0.25);
        transform: rotate(90deg);
    }
    
    .prisma-body {
        flex: 1;
        overflow: hidden;
        background-color: #1e293b;
    }
    
    #prismaViewer {
        border: none;
        background-color: white;
    }
    """

def get_chat_js():
    """
    Returns the JavaScript for the chat functionality.
    
    Returns:
        str: JavaScript for chat functionality
    """
    return """
    // Chatbot functionality with animations
    document.addEventListener('DOMContentLoaded', function() {
        const chatButton = document.getElementById('chatButton');
        const chatOverlay = document.getElementById('chatOverlay');
        const closeChat = document.getElementById('closeChat');
        const chatInput = document.getElementById('chatInput');
        const sendMessage = document.getElementById('sendMessage');
        const chatMessages = document.getElementById('chatMessages');
        
        // PDF Viewer elements
        const pdfButton = document.getElementById('pdfButton');
        const pdfOverlay = document.getElementById('pdfOverlay');
        const closePdf = document.getElementById('closePdf');
        const pdfViewer = document.getElementById('pdfViewer');
        
        // PRISMA Guidelines elements
        const prismaButton = document.getElementById('prismaButton');
        const prismaOverlay = document.getElementById('prismaOverlay');
        const closePrisma = document.getElementById('closePrisma');
        const prismaViewer = document.getElementById('prismaViewer');
        
        // Open PRISMA overlay with animation
        prismaButton.addEventListener('click', function() {
            prismaOverlay.style.display = 'flex';
            setTimeout(() => {
                prismaOverlay.classList.add('visible');
            }, 10);
            
            // Set the correct path to the PDF
            prismaViewer.src = '/static/assets/PRISMA_guidelines.pdf';
        });
        
        // Close PRISMA overlay with animation
        function closePrismaOverlay() {
            prismaOverlay.classList.remove('visible');
            setTimeout(() => {
                prismaOverlay.style.display = 'none';
            }, 300);
        }
        
        closePrisma.addEventListener('click', closePrismaOverlay);
        
        // Close PRISMA overlay when clicking outside the container
        prismaOverlay.addEventListener('click', function(event) {
            if (event.target === prismaOverlay) {
                closePrismaOverlay();
            }
        });
        
        // Open PDF overlay with animation
        pdfButton.addEventListener('click', function() {
            pdfOverlay.style.display = 'flex';
            setTimeout(() => {
                pdfOverlay.classList.add('visible');
            }, 10);
            
            // Set the correct path to the PDF
            pdfViewer.src = '/static/assets/Mindmap.pdf';
        });
        
        // Close PDF overlay with animation
        function closePdfOverlay() {
            pdfOverlay.classList.remove('visible');
            setTimeout(() => {
                pdfOverlay.style.display = 'none';
            }, 300);
        }
        
        closePdf.addEventListener('click', closePdfOverlay);
        
        // Close PDF overlay when clicking outside the PDF container
        pdfOverlay.addEventListener('click', function(event) {
            if (event.target === pdfOverlay) {
                closePdfOverlay();
            }
        });
        
        // Open chat overlay with animation
        chatButton.addEventListener('click', function() {
            chatOverlay.style.display = 'flex';
            setTimeout(() => {
                chatOverlay.classList.add('visible');
            }, 10);
            chatInput.focus();
        });
        
        // Close chat overlay with animation
        function closeOverlay() {
            chatOverlay.classList.remove('visible');
            setTimeout(() => {
                chatOverlay.style.display = 'none';
            }, 300);
        }
        
        closeChat.addEventListener('click', closeOverlay);
        
        // Close overlay when clicking outside the chat container
        chatOverlay.addEventListener('click', function(event) {
            if (event.target === chatOverlay) {
                closeOverlay();
            }
        });
        
        // Send message on Enter key press
        chatInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendUserMessage();
            }
        });
        
        // Send message on button click
        sendMessage.addEventListener('click', sendUserMessage);
        
        function sendUserMessage() {
            const message = chatInput.value.trim();
            if (message) {
                // Add user message to chat
                addMessage(message, 'user');
                
                // Clear input and resize
                chatInput.value = '';
                chatInput.style.height = 'auto';
                
                // Get paper title from the paper title container
                const paperTitle = document.querySelector('.paper-title').textContent;
                
                // Add loading indicator
                const loadingId = showLoadingMessage();
                
                // Send to backend and get response
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        paper_title: paperTitle
                    })
                })
                .then(response => response.json())
                .then(data => {
                    // Remove loading indicator
                    removeLoadingMessage(loadingId);
                    
                    // Add bot response with typing effect
                    addBotMessageWithTypingEffect(data.response);
                })
                .catch(error => {
                    // Remove loading indicator
                    removeLoadingMessage(loadingId);
                    
                    console.error('Error:', error);
                    addBotMessageWithTypingEffect('Sorry, I had trouble processing your request. Please try again.');
                });
            }
        }
        
        function showLoadingMessage() {
            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('message', 'bot-message');
            
            const messageContent = document.createElement('div');
            messageContent.classList.add('message-content');
            
            const avatarDiv = document.createElement('div');
            avatarDiv.classList.add('message-avatar');
            avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
            
            const messageBubble = document.createElement('div');
            messageBubble.classList.add('message-bubble');
            messageBubble.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
            
            messageContent.appendChild(avatarDiv);
            messageContent.appendChild(messageBubble);
            loadingDiv.appendChild(messageContent);
            
            chatMessages.appendChild(loadingDiv);
            
            // Scroll to the bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            return loadingDiv.id = 'loading-' + Date.now();
        }
        
        function removeLoadingMessage(id) {
            const loadingDiv = document.getElementById(id);
            if (loadingDiv) {
                loadingDiv.remove();
            }
        }
        
        function addMessage(text, sender) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
            
            const messageContent = document.createElement('div');
            messageContent.classList.add('message-content');
            
            const avatarDiv = document.createElement('div');
            avatarDiv.classList.add('message-avatar');
            
            // Different icons for user and bot
            if (sender === 'user') {
                avatarDiv.innerHTML = '<i class="fas fa-user"></i>';
            } else {
                avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
            }
            
            const messageBubble = document.createElement('div');
            messageBubble.classList.add('message-bubble');
            
            if (sender === 'user') {
                messageBubble.textContent = text;
            } else {
                messageBubble.innerHTML = text;
            }
            
            messageContent.appendChild(avatarDiv);
            messageContent.appendChild(messageBubble);
            messageDiv.appendChild(messageContent);
            
            chatMessages.appendChild(messageDiv);
            
            // Scroll to the bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function addBotMessageWithTypingEffect(text) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message', 'bot-message');
            
            const messageContent = document.createElement('div');
            messageContent.classList.add('message-content');
            
            const avatarDiv = document.createElement('div');
            avatarDiv.classList.add('message-avatar');
            avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
            
            const messageBubble = document.createElement('div');
            messageBubble.classList.add('message-bubble');
            
            const typewriterDiv = document.createElement('div');
            typewriterDiv.classList.add('typewriter');
            // Create a temporary div to hold the HTML content
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = text;
            // Store the rendered HTML
            const fullHTML = tempDiv.innerHTML;
            typewriterDiv.innerHTML = '';
            
            messageBubble.appendChild(typewriterDiv);
            messageContent.appendChild(avatarDiv);
            messageContent.appendChild(messageBubble);
            messageDiv.appendChild(messageContent);
            
            chatMessages.appendChild(messageDiv);
            
            // Scroll to the bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Start typing effect with HTML parsing
            startTypingEffect(typewriterDiv, fullHTML);
        }
        
        function startTypingEffect(element, html) {
            element.classList.add('typing');
            
            // For proper HTML rendering while typing, we need to handle the complete HTML
            // rather than character by character
            
            // Parse the HTML to get all text nodes
            const tempContainer = document.createElement('div');
            tempContainer.innerHTML = html;
            
            // Extract the text content only
            const textContent = tempContainer.textContent;
            
            // Keep the original HTML structure
            const originalHTML = html;
            
            let i = 0;
            const speed = 5; // typing speed in milliseconds (3x faster)
            
            // Create a display element for the typing animation
            const displayElement = document.createElement('span');
            element.appendChild(displayElement);
            
            function typeWriter() {
                if (i < textContent.length) {
                    // Add one character of text content at a time
                    displayElement.textContent = textContent.substring(0, i + 1);
                    i++;
                    
                    // Faster typing speed
                    setTimeout(typeWriter, speed);
                    
                    // Scroll to the bottom as text is being typed
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                } else {
                    // When typing is complete, replace with the original HTML
                    // to ensure proper formatting and links
                    element.innerHTML = originalHTML;
                }
            }
            
            typeWriter();
        }
        
        // Auto-resize textarea
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
    """