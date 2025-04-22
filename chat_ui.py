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
    
    <div class="chat-overlay" id="chatOverlay">
        <div class="chat-container">
            <div class="chat-header">
                <h3><i class="fas fa-robot"></i> SLR-GPT Assistant</h3>
                <button class="close-chat" id="closeChat">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="chat-body">
                <div class="chat-messages" id="chatMessages">
                    <div class="message bot-message">
                        <p>👋 Hi there! I'm your SLR-GPT Assistant. I can help answer questions about the analysis of your paper. What would you like to know?</p>
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
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
        transition: var(--transition-bounce);
        z-index: 1000;
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
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        transform: translateY(30px);
        opacity: 0;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), opacity 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
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
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
        color: white;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chat-header h3 {
        margin: 0;
        font-weight: 600;
        font-size: 1.25rem;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        font-family: 'Montserrat', sans-serif;
    }
    
    .chat-header h3 i {
        margin-right: 0.75rem;
        font-size: 1.1rem;
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
        background-color: #f8fafc;
        scrollbar-width: thin;
        scrollbar-color: #cbd5e0 #f8fafc;
    }
    
    .chat-body::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-body::-webkit-scrollbar-track {
        background: #f8fafc;
    }
    
    .chat-body::-webkit-scrollbar-thumb {
        background-color: #cbd5e0;
        border-radius: 6px;
    }
    
    .chat-messages {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    
    .message {
        max-width: 80%;
        padding: 1rem 1.25rem;
        border-radius: 18px;
        line-height: 1.5;
        animation: fadeIn 0.3s ease;
        box-shadow: var(--shadow-md);
        font-size: 0.95rem;
    }
    
    .user-message {
        align-self: flex-end;
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .bot-message {
        align-self: flex-start;
        background-color: white;
        color: var(--text-primary);
        border-bottom-left-radius: 4px;
        border: 1px solid var(--border-color);
    }
    
    .chat-input-container {
        padding: 1.25rem 1.5rem;
        background-color: white;
        border-top: 1px solid var(--border-color);
        display: flex;
        gap: 0.75rem;
        align-items: flex-end;
    }
    
    .chat-input {
        flex: 1;
        padding: 1rem 1.25rem;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        font-size: 0.95rem;
        resize: none;
        max-height: 150px;
        transition: var(--transition-base);
        font-family: 'Poppins', sans-serif;
    }
    
    .chat-input:focus {
        outline: none;
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    }
    
    .send-btn {
        background: linear-gradient(135deg, var(--primary-color), var(--primary-dark));
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
        background: linear-gradient(135deg, var(--primary-dark), var(--primary-color));
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(99, 102, 241, 0.4);
    }
    
    .send-btn:hover i {
        transform: translateX(2px);
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
            padding: 0.9rem 1.1rem;
        }
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
                    
                    // Add bot response
                    addMessage(data.response, 'bot');
                })
                .catch(error => {
                    // Remove loading indicator
                    removeLoadingMessage(loadingId);
                    
                    console.error('Error:', error);
                    addMessage('Sorry, I had trouble processing your request. Please try again.', 'bot');
                });
            }
        }
        
        function showLoadingMessage() {
            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('message', 'bot-message');
            loadingDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
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
            
            if (sender === 'bot') {
                // For bot messages, render HTML content
                messageDiv.innerHTML = text;
            } else {
                // For user messages, keep as plain text
                messageDiv.textContent = text;
            }
            
            chatMessages.appendChild(messageDiv);
            
            // Scroll to the bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // Auto-resize textarea
        chatInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
    """