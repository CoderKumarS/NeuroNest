/**
 * Users JavaScript
 * Handles user-related functionality including profile, authentication, and dashboard
 */

document.addEventListener('DOMContentLoaded', function () {
    initializeUsers();
});

function initializeUsers() {
    // Profile form handling
    initializeProfileForm();

    // Password change functionality
    initializePasswordChange();

    // Dashboard widgets
    initializeDashboard();

    // User preferences
    initializeUserPreferences();
}

function initializeProfileForm() {
    const profileForm = document.getElementById('profile-form');

    if (profileForm) {
        profileForm.addEventListener('submit', function (e) {
            e.preventDefault();
            saveProfile(this);
        });
    }

    // Profile image upload
    const imageInput = document.getElementById('profile-image');
    const imagePreview = document.getElementById('image-preview');

    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function (e) {
            previewProfileImage(e.target.files[0], imagePreview);
        });
    }
}

function saveProfile(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;

    submitButton.textContent = 'Saving...';
    submitButton.disabled = true;

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Profile updated successfully!', 'success');
            } else {
                showNotification(data.error || 'Failed to update profile', 'error');
            }
        })
        .catch(error => {
            showNotification('Connection error. Please try again.', 'error');
        })
        .finally(() => {
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        });
}

function previewProfileImage(file, previewElement) {
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewElement.src = e.target.result;
            previewElement.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
}

function initializePasswordChange() {
    const passwordForm = document.getElementById('password-form');

    if (passwordForm) {
        passwordForm.addEventListener('submit', function (e) {
            e.preventDefault();
            changePassword(this);
        });
    }

    // Password strength indicator
    const newPasswordInput = document.getElementById('new-password');
    const strengthIndicator = document.getElementById('password-strength');

    if (newPasswordInput && strengthIndicator) {
        newPasswordInput.addEventListener('input', function () {
            updatePasswordStrength(this.value, strengthIndicator);
        });
    }
}

function changePassword(form) {
    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.textContent;

    // Validate passwords match
    const newPassword = formData.get('new_password');
    const confirmPassword = formData.get('confirm_password');

    if (newPassword !== confirmPassword) {
        showNotification('Passwords do not match', 'error');
        return;
    }

    submitButton.textContent = 'Changing...';
    submitButton.disabled = true;

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Password changed successfully!', 'success');
                form.reset();
            } else {
                showNotification(data.error || 'Failed to change password', 'error');
            }
        })
        .catch(error => {
            showNotification('Connection error. Please try again.', 'error');
        })
        .finally(() => {
            submitButton.textContent = originalText;
            submitButton.disabled = false;
        });
}

function updatePasswordStrength(password, indicator) {
    const strength = calculatePasswordStrength(password);
    const strengthText = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const strengthColors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-blue-500', 'bg-green-500'];

    indicator.className = `h-2 rounded-full transition-all duration-300 ${strengthColors[strength]}`;
    indicator.style.width = `${(strength + 1) * 20}%`;

    const strengthLabel = indicator.nextElementSibling;
    if (strengthLabel) {
        strengthLabel.textContent = strengthText[strength];
        strengthLabel.className = `text-sm ${strengthColors[strength].replace('bg-', 'text-')}`;
    }
}

function calculatePasswordStrength(password) {
    let strength = 0;

    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    return Math.min(strength - 1, 4);
}

function initializeDashboard() {
    // Dashboard stats animation
    animateDashboardStats();

    // Recent activity updates
    initializeActivityUpdates();

    // Quick actions
    initializeQuickActions();
}

function animateDashboardStats() {
    const statNumbers = document.querySelectorAll('.stat-number');

    statNumbers.forEach(stat => {
        const target = parseInt(stat.dataset.value) || 0;
        animateNumber(stat, target);
    });
}

function animateNumber(element, target) {
    let current = 0;
    const increment = target / 50;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, 20);
}

function initializeActivityUpdates() {
    // Auto-refresh activity feed every 5 minutes
    setInterval(refreshActivityFeed, 300000);
}

function refreshActivityFeed() {
    const activityContainer = document.getElementById('activity-feed');
    if (!activityContainer) return;

    fetch('/users/api/activity-feed/', {
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateActivityFeed(data.activities);
            }
        })
        .catch(error => {
            console.error('Failed to refresh activity feed:', error);
        });
}

function updateActivityFeed(activities) {
    const container = document.getElementById('activity-feed');
    if (!container) return;

    container.innerHTML = activities.map(activity => `
        <div class="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                <i class="fas ${activity.icon} text-blue-600 dark:text-blue-400 text-sm"></i>
            </div>
            <div class="flex-1">
                <p class="text-sm text-gray-900 dark:text-gray-100">${activity.description}</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">${activity.time}</p>
            </div>
        </div>
    `).join('');
}

function initializeQuickActions() {
    const quickActionButtons = document.querySelectorAll('.quick-action');

    quickActionButtons.forEach(button => {
        button.addEventListener('click', function () {
            const action = this.dataset.action;
            handleQuickAction(action);
        });
    });
}

function handleQuickAction(action) {
    switch (action) {
        case 'new-course':
            window.location.href = '/courses/create/';
            break;
        case 'browse-courses':
            window.location.href = '/courses/';
            break;
        case 'view-progress':
            window.location.href = '/users/progress/';
            break;
        case 'ai-tutor':
            // Toggle AI assistant if available
            if (window.toggleAIAssistant) {
                window.toggleAIAssistant();
            } else {
                window.location.href = '/tutor/';
            }
            break;
        default:
            console.log('Unknown quick action:', action);
    }
}

function initializeUserPreferences() {
    // Theme preference
    const themeToggle = document.getElementById('theme-preference');
    if (themeToggle) {
        themeToggle.addEventListener('change', function () {
            updateThemePreference(this.value);
        });
    }

    // Notification preferences
    const notificationToggles = document.querySelectorAll('.notification-toggle');
    notificationToggles.forEach(toggle => {
        toggle.addEventListener('change', function () {
            updateNotificationPreference(this.dataset.type, this.checked);
        });
    });
}

function updateThemePreference(theme) {
    fetch('/users/api/update-preferences/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            theme: theme
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Apply theme immediately
                document.documentElement.className = theme === 'dark' ? 'dark' : '';
                showNotification('Theme preference updated', 'success');
            }
        })
        .catch(error => {
            console.error('Failed to update theme preference:', error);
        });
}

function updateNotificationPreference(type, enabled) {
    fetch('/users/api/update-preferences/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            notifications: {
                [type]: enabled
            }
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(`${type} notifications ${enabled ? 'enabled' : 'disabled'}`, 'success');
            }
        })
        .catch(error => {
            console.error('Failed to update notification preference:', error);
        });
}

// Utility functions
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg z-50 ${type === 'success' ? 'bg-green-600 text-white' :
            type === 'error' ? 'bg-red-600 text-white' :
                'bg-blue-600 text-white'
        }`;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Export functions for global use
window.saveProfile = saveProfile;
window.changePassword = changePassword;
window.handleQuickAction = handleQuickAction;
window.showNotification = showNotification;