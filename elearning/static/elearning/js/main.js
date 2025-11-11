/**
 * Main JavaScript for NeuroNest E-Learning Platform
 * Handles common functionality across the platform
 * Optimized for performance and accessibility
 */

// Performance monitoring
const perfData = window.performance && window.performance.timing;
if (perfData) {
    window.addEventListener('load', function () {
        setTimeout(function () {
            const loadTime = perfData.loadEventEnd - perfData.navigationStart;
        }, 0);
    });
}

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

    // Initialize filter auto-submit
    initializeFilterAutoSubmit();

    // Initialize search functionality
    initializeSearchFunctionality();
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
    const menuIcon = document.getElementById('mobile-menu-icon');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function (e) {
            e.stopPropagation();
            const isHidden = mobileMenu.classList.contains('hidden');

            mobileMenu.classList.toggle('hidden');

            // Update ARIA attributes for accessibility
            mobileMenuButton.setAttribute('aria-expanded', !isHidden);
            mobileMenu.setAttribute('aria-hidden', isHidden);

            // Toggle icon between bars and times
            if (menuIcon) {
                if (isHidden) {
                    menuIcon.classList.remove('fa-bars');
                    menuIcon.classList.add('fa-times');
                } else {
                    menuIcon.classList.remove('fa-times');
                    menuIcon.classList.add('fa-bars');
                }
            }
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function (event) {
            if (!mobileMenu.contains(event.target) && !mobileMenuButton.contains(event.target)) {
                if (!mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                    if (menuIcon) {
                        menuIcon.classList.remove('fa-times');
                        menuIcon.classList.add('fa-bars');
                    }
                }
            }
        });

        // Close mobile menu when clicking on a link
        const mobileMenuLinks = mobileMenu.querySelectorAll('a');
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', function () {
                mobileMenu.classList.add('hidden');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
                mobileMenu.setAttribute('aria-hidden', 'true');
                if (menuIcon) {
                    menuIcon.classList.remove('fa-times');
                    menuIcon.classList.add('fa-bars');
                }
            });
        });

        // Close mobile menu with Escape key for accessibility
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && !mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
                mobileMenu.setAttribute('aria-hidden', 'true');
                if (menuIcon) {
                    menuIcon.classList.remove('fa-times');
                    menuIcon.classList.add('fa-bars');
                }
                mobileMenuButton.focus(); // Return focus to button
            }
        });
    }
}

function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const html = document.documentElement;


    // Check for saved theme preference or default to 'light'
    const currentTheme = localStorage.getItem('theme') || 'light';

    // Apply the saved theme
    if (currentTheme === 'dark') {
        html.classList.add('dark');
        themeIcon.className = 'fas fa-sun text-base sm:text-lg';
    } else {
        html.classList.remove('dark');
        themeIcon.className = 'fas fa-moon text-base sm:text-lg';
    }

    // Theme toggle event listener
    themeToggle.addEventListener('click', function () {
        if (html.classList.contains('dark')) {
            html.classList.remove('dark');
            themeIcon.className = 'fas fa-moon text-base sm:text-lg';
            localStorage.setItem('theme', 'light');
        } else {
            html.classList.add('dark');
            themeIcon.className = 'fas fa-sun text-base sm:text-lg';
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

function initializeFilterAutoSubmit() {
    // Auto-submit filter forms when dropdowns change (for course list page)
    const filterForms = document.querySelectorAll('form');

    filterForms.forEach(form => {
        // Check if this is a filter form (has select elements for filtering)
        const selectElements = form.querySelectorAll('select[name="category"], select[name="instructor"], select[name="min_rating"], select[name="sort"]');

        if (selectElements.length > 0) {
            selectElements.forEach(select => {
                select.addEventListener('change', function () {
                    // Add a small delay to allow user to see the change
                    setTimeout(() => {
                        // Check if form has a submit button to add loading state
                        const submitButton = form.querySelector('button[type="submit"]');
                        if (submitButton) {
                            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Applying...';
                            submitButton.disabled = true;
                        }
                        form.submit();
                    }, 100);
                });
            });
        }
    });
}

function initializeSearchFunctionality() {
    // Handle search form submissions
    const searchForms = document.querySelectorAll('form');

    searchForms.forEach(form => {
        const searchInput = form.querySelector('input[name="search"]');

        if (searchInput) {
            // Add search icon button functionality
            const searchButton = form.querySelector('button[type="submit"]');

            if (searchButton) {
                searchButton.addEventListener('click', function (e) {
                    e.preventDefault();

                    // Trim whitespace from search query
                    searchInput.value = searchInput.value.trim();

                    // Submit the form
                    form.submit();
                });
            }

            // Allow Enter key to submit search
            searchInput.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    searchInput.value = searchInput.value.trim();
                    form.submit();
                }
            });

            // Add focus/blur effects for better UX
            searchInput.addEventListener('focus', function () {
                this.parentElement.classList.add('ring-2', 'ring-purple-300');
            });

            searchInput.addEventListener('blur', function () {
                this.parentElement.classList.remove('ring-2', 'ring-purple-300');
            });
        }
    });
}

// Make functions globally available
window.dismissMessage = dismissMessage;
window.showNotification = showNotification;
window.getCSRFToken = getCSRFToken;
window.debounce = debounce;