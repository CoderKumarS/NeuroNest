/**
 * Main JavaScript for NeuroNest E-Learning Platform
 * Handles common functionality across the platform
 */

document.addEventListener('DOMContentLoaded', function () {
    initializeElearning();
});

function initializeElearning() {
    // Initialize smooth scrolling for anchor links
    initializeSmoothScrolling();

    // Initialize mobile menu
    initializeMobileMenu();

    // Initialize theme toggle
    initializeThemeToggle();

    // Initialize notification system
    initializeNotifications();

    // Initialize form enhancements
    initializeFormEnhancements();
}

function initializeSmoothScrolling() {
    // Smooth scrolling for anchor links (only on home page)
    const isHomePage = window.location.pathname === '/';

    if (isHomePage) {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    // Remove active class from all section links
                    document.querySelectorAll('a[href^="#"]').forEach(link => {
                        link.classList.remove('text-primary-600', 'dark:text-primary-400', 'font-semibold');
                        link.classList.add('text-gray-700', 'dark:text-gray-300');
                    });

                    // Add active class to clicked link
                    this.classList.remove('text-gray-700', 'dark:text-gray-300');
                    this.classList.add('text-primary-600', 'dark:text-primary-400', 'font-semibold');

                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Initialize section highlighting on scroll
        initializeSectionHighlighting();
    }
}

function initializeSectionHighlighting() {
    // Highlight navigation items based on scroll position
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('a[href^="#"]');

    if (sections.length === 0 || navLinks.length === 0) return;

    function highlightNavigation() {
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;

            if (window.pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('text-primary-600', 'dark:text-primary-400', 'font-semibold');
            link.classList.add('text-gray-700', 'dark:text-gray-300');

            if (link.getAttribute('href') === `#${current}`) {
                link.classList.remove('text-gray-700', 'dark:text-gray-300');
                link.classList.add('text-primary-600', 'dark:text-primary-400', 'font-semibold');
            }
        });
    }

    // Throttle scroll events for better performance
    let ticking = false;

    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(highlightNavigation);
            ticking = true;
            setTimeout(() => { ticking = false; }, 100);
        }
    }

    window.addEventListener('scroll', requestTick);

    // Initial highlight
    highlightNavigation();
}

function initializeMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function (event) {
            if (!mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }
}

function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const html = document.documentElement;

    if (!themeToggle || !themeIcon) return;

    // Check for saved theme preference or default to 'light'
    const currentTheme = localStorage.getItem('theme') || 'light';

    // Apply the saved theme
    if (currentTheme === 'dark') {
        html.classList.add('dark');
        themeIcon.className = 'fas fa-sun text-lg';
    } else {
        html.classList.remove('dark');
        themeIcon.className = 'fas fa-moon text-lg';
    }

    // Theme toggle event listener
    themeToggle.addEventListener('click', function () {
        if (html.classList.contains('dark')) {
            html.classList.remove('dark');
            themeIcon.className = 'fas fa-moon text-lg';
            localStorage.setItem('theme', 'light');
        } else {
            html.classList.add('dark');
            themeIcon.className = 'fas fa-sun text-lg';
            localStorage.setItem('theme', 'dark');
        }
    });
}

function initializeNotifications() {
    // Auto-dismiss messages after 4 seconds
    const messages = document.querySelectorAll('.message-alert');
    messages.forEach((message, index) => {
        setTimeout(() => {
            const closeButton = message.querySelector('.message-close');
            if (closeButton && message.parentNode) {
                dismissMessage(closeButton);
            }
        }, 4000 + (index * 500)); // 4s, 4.5s, 5s, etc.
    });
}

function dismissMessage(button) {
    const messageAlert = button.closest('.message-alert');
    messageAlert.classList.remove('message-slide-in');
    messageAlert.classList.add('message-slide-out');

    setTimeout(() => {
        if (messageAlert.parentNode) {
            messageAlert.remove();
        }
        // Remove container if no messages left
        const container = document.getElementById('messages-container');
        if (container && container.children.length === 0) {
            container.remove();
        }
    }, 300);
}

function initializeFormEnhancements() {
    // Add loading states to forms
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function () {
            const submitButton = this.querySelector('button[type="submit"], input[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                const originalText = submitButton.textContent || submitButton.value;
                submitButton.textContent = 'Loading...';
                submitButton.disabled = true;

                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitButton.textContent = originalText;
                    submitButton.disabled = false;
                }, 10000);
            }
        });
    });

    // Add focus styles to form inputs
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function () {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function () {
            this.parentElement.classList.remove('focused');
        });
    });
}

// Utility functions
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transform transition-all duration-300 ${type === 'success' ? 'bg-green-600 text-white' :
        type === 'error' ? 'bg-red-600 text-white' :
            type === 'warning' ? 'bg-yellow-600 text-white' :
                'bg-blue-600 text-white'
        }`;

    notification.innerHTML = `
        <div class="flex items-center justify-between">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    document.body.appendChild(notification);

    // Auto-remove after specified duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Make functions globally available
window.dismissMessage = dismissMessage;
window.showNotification = showNotification;
window.getCSRFToken = getCSRFToken;
window.debounce = debounce;