/**
 * AI Tutor Chat JavaScript
 * Handles chat interface functionality including message sending and display
 */

class AITutorChat {
    constructor(sessionId, sendMessageUrl, csrfToken) {
        this.sessionId = sessionId;
        this.sendMessageUrl = sendMessageUrl;
        this.csrfToken = csrfToken;

        this.messageForm = document.getElementById('messageForm');
        this.messageInput = document.getElementById('messageInput');
        this.messagesContainer = document.getElementById('messagesContainer');
        this.courseContext = document.getElementById('courseContext');

        this.init();
    }

    init() {
        if (this.messageForm) {
            this.messageForm.addEventListener('submit', (e) => this.handleSubmit(e));
        }

        // Auto-scroll to bottom on page load
        if (this.messagesContainer) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }

        // Focus input on page load
        if (this.messageInput) {
            this.messageInput.focus();
        }


    }

    handleSubmit(e) {
        e.preventDefault();

        const message = this.messageInput.value.trim();
        if (!message) return;

        const courseId = this.courseContext ? this.courseContext.value : '';

        // Add user message to chat
        this.addUserMessage(message);

        // Show typing indicator
        this.showTypingIndicator();

        // Send message to server
        this.sendMessage(message, courseId);

        // Clear input
        this.messageInput.value = '';
    }

    addUserMessage(message) {
        const userDiv = document.createElement('div');
        userDiv.className = 'mb-4 text-right';
        userDiv.innerHTML = `
            <div class="inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-blue-600 text-white">
                <p>${this.escapeHtml(message)}</p>
                <small class="text-xs opacity-70">${this.getCurrentTime()}</small>
            </div>
        `;

        this.messagesContainer.appendChild(userDiv);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'mb-4';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
                <p>AI is thinking...</p>
            </div>
        `;

        this.messagesContainer.appendChild(typingDiv);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    sendMessage(message, courseId) {
        const requestData = {
            session_id: this.sessionId,
            message: message,
            course_id: courseId,
            request_type: 'question'
        };



        fetch(this.sendMessageUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.csrfToken
            },
            body: JSON.stringify(requestData)
        })
            .then(response => response.json())
            .then(data => this.handleResponse(data))
            .catch(error => {
                console.error('Error:', error);
                this.handleError(error);
            });
    }

    handleResponse(data) {
        this.hideTypingIndicator();

        const aiDiv = document.createElement('div');
        aiDiv.className = 'mb-4';

        if (data.success) {
            aiDiv.innerHTML = `
                <div class="inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
                    <p>${this.escapeHtml(data.ai_response)}</p>
                    <small class="text-xs opacity-70">${this.getCurrentTime()} • ${data.tokens_used || 0} tokens</small>
                </div>
            `;
        } else {
            aiDiv.innerHTML = `
                <div class="inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200">
                    <p>Sorry, I encountered an error: ${this.escapeHtml(data.error || 'Please try again.')}</p>
                    <small class="text-xs opacity-70">${this.getCurrentTime()}</small>
                </div>
            `;
        }

        this.messagesContainer.appendChild(aiDiv);
        this.scrollToBottom();
    }

    handleError(error) {
        this.hideTypingIndicator();

        const errorDiv = document.createElement('div');
        errorDiv.className = 'mb-4';
        errorDiv.innerHTML = `
            <div class="inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200">
                <p>Sorry, I encountered a connection error. Please try again.</p>
                <small class="text-xs opacity-70">${this.getCurrentTime()}</small>
            </div>
        `;

        this.messagesContainer.appendChild(errorDiv);
        this.scrollToBottom();
    }

    scrollToBottom() {
        if (this.messagesContainer) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Expose AITutorChat class globally
window.AITutorChat = AITutorChat;

// Initialize chat when DOM is loaded (fallback for direct usage)
document.addEventListener('DOMContentLoaded', function () {
    // These variables will be set by the template
    if (typeof CHAT_CONFIG !== 'undefined' && !window.aiTutorChat) {
        window.aiTutorChat = new AITutorChat(
            CHAT_CONFIG.sessionId,
            CHAT_CONFIG.sendMessageUrl,
            CHAT_CONFIG.csrfToken
        );
    }
});