/**
 * Courses JavaScript
 * Handles course-related functionality
 */

document.addEventListener('DOMContentLoaded', function () {
    initializeCourses();
});

function initializeCourses() {
    // Course enrollment functionality
    initializeEnrollment();

    // Course search and filtering
    initializeCourseFilters();

    // Course progress tracking
    initializeCourseProgress();
}

function initializeEnrollment() {
    const enrollButtons = document.querySelectorAll('.enroll-btn');

    enrollButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const courseId = this.dataset.courseId;
            enrollInCourse(courseId, this);
        });
    });
}

function enrollInCourse(courseId, button) {
    const originalText = button.textContent;
    button.textContent = 'Enrolling...';
    button.disabled = true;

    fetch(`/courses/${courseId}/enroll/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.textContent = 'Enrolled';
                button.classList.remove('bg-blue-600', 'hover:bg-blue-700');
                button.classList.add('bg-green-600', 'cursor-not-allowed');
                showNotification('Successfully enrolled in course!', 'success');
            } else {
                button.textContent = originalText;
                button.disabled = false;
                showNotification(data.error || 'Failed to enroll', 'error');
            }
        })
        .catch(error => {
            button.textContent = originalText;
            button.disabled = false;
            showNotification('Connection error. Please try again.', 'error');
        });
}

function initializeCourseFilters() {
    const searchInput = document.getElementById('course-search');
    const categoryFilter = document.getElementById('category-filter');
    const levelFilter = document.getElementById('level-filter');

    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterCourses, 300));
    }

    if (categoryFilter) {
        categoryFilter.addEventListener('change', filterCourses);
    }

    if (levelFilter) {
        levelFilter.addEventListener('change', filterCourses);
    }
}

function filterCourses() {
    const searchTerm = document.getElementById('course-search')?.value.toLowerCase() || '';
    const category = document.getElementById('category-filter')?.value || '';
    const level = document.getElementById('level-filter')?.value || '';

    const courseCards = document.querySelectorAll('.course-card');

    courseCards.forEach(card => {
        const title = card.dataset.title?.toLowerCase() || '';
        const cardCategory = card.dataset.category || '';
        const cardLevel = card.dataset.level || '';

        const matchesSearch = title.includes(searchTerm);
        const matchesCategory = !category || cardCategory === category;
        const matchesLevel = !level || cardLevel === level;

        if (matchesSearch && matchesCategory && matchesLevel) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function initializeCourseProgress() {
    const progressBars = document.querySelectorAll('.progress-bar');

    progressBars.forEach(bar => {
        const progress = parseInt(bar.dataset.progress) || 0;
        animateProgressBar(bar, progress);
    });
}

function animateProgressBar(bar, targetProgress) {
    let currentProgress = 0;
    const increment = targetProgress / 50; // 50 steps for smooth animation

    const timer = setInterval(() => {
        currentProgress += increment;
        if (currentProgress >= targetProgress) {
            currentProgress = targetProgress;
            clearInterval(timer);
        }

        bar.style.width = `${currentProgress}%`;
        const progressText = bar.querySelector('.progress-text');
        if (progressText) {
            progressText.textContent = `${Math.round(currentProgress)}%`;
        }
    }, 20);
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

// Export functions for global use
window.enrollInCourse = enrollInCourse;
window.filterCourses = filterCourses;
window.showNotification = showNotification;