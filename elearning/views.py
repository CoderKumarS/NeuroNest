from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count, Avg
from courses.models import Course, Enrollment, Progress
from django.contrib.auth import get_user_model

User = get_user_model()

def home_view(request):
    """
    Home page view for the elearning platform with dynamic data
    """
    # Get popular courses (top 6 by enrollment count)
    popular_courses = Course.objects.annotate(
        enrollment_count=Count('enrollment'),
        avg_rating=Avg('progress__score')
    ).order_by('-enrollment_count')[:6]
    
    # Get platform statistics
    total_students = User.objects.filter(role='student').count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    
    # Calculate success rate (students with completed courses)
    completed_courses_count = Progress.objects.filter(
        completed_lessons__gte=1  # At least some progress
    ).values('student').distinct().count()
    
    success_rate = 0
    if total_students > 0:
        success_rate = int((completed_courses_count / total_students) * 100)
    
    # Get recent testimonials (mock data for now, can be replaced with real testimonial model)
    testimonials = [
        {
            'name': 'John Smith',
            'role': 'Web Developer',
            'initials': 'JS',
            'content': 'The web development course was amazing! I went from knowing nothing to building my own websites. The instructors are fantastic and the community is very supportive.',
            'rating': 5
        },
        {
            'name': 'Maria Johnson', 
            'role': 'Data Scientist',
            'initials': 'MJ',
            'content': 'The data science program completely changed my career. The hands-on projects and real-world applications made all the difference. Highly recommended!',
            'rating': 5
        },
        {
            'name': 'David Wilson',
            'role': 'UI/UX Designer', 
            'initials': 'DW',
            'content': 'The design course helped me understand user experience principles that I use every day. The portfolio projects were incredibly valuable for my career.',
            'rating': 5
        }
    ]
    
    context = {
        'popular_courses': popular_courses,
        'total_students': total_students,
        'total_courses': total_courses,
        'success_rate': success_rate,
        'testimonials': testimonials,
        'is_authenticated': request.user.is_authenticated,
        'user_role': request.user.role if request.user.is_authenticated else None,
    }
    
    return render(request, 'base/index.html', context)


def about_view(request):
    """About page view"""
    # Get platform statistics for the about page
    total_students = User.objects.filter(role='student').count()
    total_courses = Course.objects.count()
    
    # Calculate success rate
    completed_courses_count = Progress.objects.filter(
        completed_lessons__gte=1
    ).values('student').distinct().count()
    
    success_rate = 0
    if total_students > 0:
        success_rate = int((completed_courses_count / total_students) * 100)
    
    context = {
        'total_students': total_students,
        'total_courses': total_courses,
        'success_rate': success_rate,
    }
    
    return render(request, 'base/about.html', context)


def contact_view(request):
    """Contact page view with form handling"""
    if request.method == 'POST':
        # Handle contact form submission
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Here you can add logic to save the contact form data
        # For now, we'll just return a success response
        
        # You could save to a ContactMessage model or send an email
        # Example: ContactMessage.objects.create(...)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # AJAX request
            return JsonResponse({'success': True, 'message': 'Thank you for your message!'})
        else:
            # Regular form submission
            from django.contrib import messages
            messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
            return redirect('contact')
    
    return render(request, 'base/contact.html')
