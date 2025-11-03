/**
 * Chat Simple Configuration
 * This file contains the configuration for the simple chat interface
 */

// Function to initialize chat configuration from data attributes
function initializeChatFromDataAttributes() {
    const configElement = document.getElementById('chatConfig');
    if (!configElement) {
        return;
    }

    const sessionId = parseInt(configElement.dataset.sessionId);
    const sendMessageUrl = configElement.dataset.sendMessageUrl;
    const csrfToken = getCSRFToken();

    window.CHAT_CONFIG = {
        sessionId: sessionId,
        sendMessageUrl: sendMessageUrl,
        csrfToken: csrfToken
    };

    // Initialize the chat after configuration is set
    if (window.AITutorChat) {
        window.aiTutorChat = new window.AITutorChat(
            window.CHAT_CONFIG.sessionId,
            window.CHAT_CONFIG.sendMessageUrl,
            window.CHAT_CONFIG.csrfToken
        );
    }
}

// Function to initialize chat configuration from Django template variables (legacy)
function initializeChatConfig(sessionId, sendMessageUrl, csrfToken) {
    window.CHAT_CONFIG = {
        sessionId: sessionId,
        sendMessageUrl: sendMessageUrl,
        csrfToken: csrfToken
    };

    // Initialize the chat after configuration is set
    if (window.AITutorChat) {
        window.aiTutorChat = new window.AITutorChat(
            window.CHAT_CONFIG.sessionId,
            window.CHAT_CONFIG.sendMessageUrl,
            window.CHAT_CONFIG.csrfToken
        );
    }
}

// Function to get CSRF token from the page
function getCSRFToken() {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfInput ? csrfInput.value : '';
}

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    initializeChatFromDataAttributes();
});