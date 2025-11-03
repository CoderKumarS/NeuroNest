/**
 * AI Assistant Widget JavaScript
 * Handles the floating AI assistant chat widget functionality
 */

let aiAssistantOpen = false;
let aiSessionId = null;

// Initialize AI Assistant
document.addEventListener('DOMContentLoaded', function () {
    initializeAIAssistant();
});

function initializeAIAssistant() {
    const input = document.getElementById('ai-assistant-input');
    const charCount = document.getElementById('ai-char-count');
    const form = document.getElementById('ai-assistant-form');

    // Character counter
    if (input && charCount) {
        input.addEventListener('input', function () {
            charCount.textContent = `${this.value.length}/500`;
        });
    }

    // Form submission
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            sendAIMessage();
        });
    }

    // Enter key to send
    if (input) {
        input.addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendAIMessage();
            }
        });
    }

    // Create AI session
    createAISession();
}

function toggleAIAssistant() {
    const button = document.getElementById('ai-assistant-button');
    const window = document.getElementById('ai-assistant-window');
    const overlay = document.getElementById('ai-assistant-overlay');
    const icon = document.getElementById('ai-assistant-icon');

    aiAssistantOpen = !aiAssistantOpen;

    if (aiAssistantOpen) {
        // Show chat window
        window.classList.remove('hidden');
        overlay.classList.remove('hidden');
        icon.className = 'fas fa-times text-xl group-hover:scale-110 transition-transform duration-200';

        // Focus input
        setTimeout(() => {
            const input = document.getElementById('ai-assistant-input');
            if (input) input.focus();
        }, 100);

        // Hide notification badge
        document.getElementById('ai-notification-badge').classList.add('hidden');
    } else {
        // Hide chat window
        window.classList.add('hidden');
        overlay.classList.add('hidden');
        icon.className = 'fas fa-robot text-xl group-hover:scale-110 transition-transform duration-200';
    }
}

function createAISession() {
    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfToken) return;

    // Create a new AI session for the widget
    fetch('/tutor/widget/new-session/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken.value
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                aiSessionId = data.session_id;
            }
        })
        .catch(error => {
            console.error('Error creating AI session:', error);
        });
}

function sendAIMessage() {
    const input = document.getElementById('ai-assistant-input');
    const sendButton = document.getElementById('ai-assistant-send');
    const message = input.value.trim();

    if (!message || !aiSessionId) return;

    // Disable input
    input.disabled = true;
    sendButton.disabled = true;

    // Add user message to chat
    addAIMessage('user', message);

    // Clear input
    input.value = '';
    document.getElementById('ai-char-count').textContent = '0/500';

    // Show typing indicator
    showAITypingIndicator();

    // Get CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');

    // Send message to server
    fetch('/tutor/api/send-message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken.value
        },
        body: JSON.stringify({
            session_id: aiSessionId,
            message: message,
            course_id: '',
            request_type: 'question'
        })
    })
        .then(response => response.json())
        .then(data => {
            hideAITypingIndicator();

            if (data.success) {
                addAIMessage('ai', data.ai_response);
            } else {
                addAIMessage('ai', 'Sorry, I encountered an error. Please try again.');
            }
        })
        .catch(error => {
            hideAITypingIndicator();
            addAIMessage('ai', 'Sorry, I encountered a connection error. Please try again.');
        })
        .finally(() => {
            // Re-enable input
            input.disabled = false;
            sendButton.disabled = false;
            input.focus();
        });
}

function addAIMessage(type, content) {
    const container = document.getElementById('ai-messages-container');
    const messageDiv = document.createElement('div');

    const isUser = type === 'user';
    const time = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

    messageDiv.className = `flex items-start space-x-2 ai-message-enter ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`;
    messageDiv.innerHTML = `
        <div class="w-6 h-6 ${isUser ? 'bg-blue-500' : 'bg-gradient-to-br from-purple-500 to-blue-600'} rounded-full flex items-center justify-center flex-shrink-0">
            <i class="fas ${isUser ? 'fa-user' : 'fa-robot'} text-white text-xs"></i>
        </div>
        <div class="${isUser ? 'bg-blue-500 text-white' : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200'} rounded-lg p-3 max-w-xs shadow-sm">
            <p class="text-sm whitespace-pre-wrap">${escapeHtml(content)}</p>
            <div class="text-xs ${isUser ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'} mt-1">
                ${time}
            </div>
        </div>
    `;

    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function showAITypingIndicator() {
    const container = document.getElementById('ai-messages-container');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'ai-typing-indicator';
    typingDiv.className = 'flex items-start space-x-2';
    typingDiv.innerHTML = `
        <div class="w-6 h-6 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
            <i class="fas fa-robot text-white text-xs"></i>
        </div>
        <div class="bg-white dark:bg-gray-700 rounded-lg p-3 shadow-sm">
            <div class="flex space-x-1">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
        </div>
    `;

    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
}

function hideAITypingIndicator() {
    const indicator = document.getElementById('ai-typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show notification badge when window is closed and new message arrives
function showAINotification() {
    if (!aiAssistantOpen) {
        document.getElementById('ai-notification-badge').classList.remove('hidden');
    }
}

// Close on escape key
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && aiAssistantOpen) {
        toggleAIAssistant();
    }
});

// Make functions globally available
window.toggleAIAssistant = toggleAIAssistant;
window.sendAIMessage = sendAIMessage;
window.addAIMessage = addAIMessage;
window.showAINotification = showAINotification;