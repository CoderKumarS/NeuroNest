from .models import Course, Enrollment, Quiz, Question, Option, StudentAnswer, Progress

# HTML Views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.template import Template, Context
# HTML Views for Course Management

# HTML Views for Course Management

def course_list(request):
    """Display all courses with search and filtering"""
    courses = Course.objects.all().annotate(
        enrollment_count=Count('enrollment'),
        avg_rating=Avg('progress__score')
    ).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(instructor__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(courses, 9)  # 9 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_courses': courses.count()
    }
    return render(request, 'courses/course_list.html', context)

def course_explorer(request):
    """Course explorer with categories and filters"""
    courses = Course.objects.all().annotate(
        enrollment_count=Count('enrollment')
    ).order_by('-created_at')
    
    context = {
        'courses': courses,
        'featured_courses': courses[:6],
        'popular_courses': courses.order_by('-enrollment_count')[:6]
    }
    return render(request, 'courses/course_explorer.html', context)

def course_detail(request, course_id):
    """Display course details and enrollment status"""
    course = get_object_or_404(Course, id=course_id)
    
    # Debug: Print to console to verify view is being called
    print(f"🔍 DEBUG: course_detail view called for course: {course.title}")
    print(f"🔍 DEBUG: course created_at: {course.created_at}")
    
    # Check if user is enrolled
    is_enrolled = False
    user_progress = None
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user, 
            course=course
        ).exists()
        
        if is_enrolled:
            user_progress = Progress.objects.filter(
                student=request.user,
                course=course
            ).first()
    
    # Get course quizzes
    quizzes = course.quizzes.all()
    
    # Get other courses by same instructor
    related_courses = Course.objects.filter(
        instructor=course.instructor
    ).exclude(id=course.id)[:3]
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'user_progress': user_progress,
        'quizzes': quizzes,
        'related_courses': related_courses,
        'is_instructor': request.user == course.instructor if request.user.is_authenticated else False
    }
    
    # Debug: Print context to verify data
    print(f"🔍 DEBUG: Context keys: {list(context.keys())}")
    print(f"🔍 DEBUG: Template path: courses/course_detail.html")
    
    return render(request, 'courses/course_detail.html', context)

@login_required
def enroll_course(request, course_id):
    """Enroll student in a course"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.role != 'student':
        messages.error(request, 'Only students can enroll in courses.')
        return redirect('courses:course_detail', course_id=course.id)
    
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    
    if created:
        messages.success(request, f'Successfully enrolled in {course.title}!')
    else:
        messages.info(request, 'You are already enrolled in this course.')
    
    return redirect('courses:course_detail', course_id=course.id)

@login_required
def create_course(request):
    """Create a new course (instructors only)"""
    if request.user.role != 'instructor':
        messages.error(request, 'Only instructors can create courses.')
        return redirect('courses:course_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if title and description:
            course = Course.objects.create(
                title=title,
                description=description,
                instructor=request.user
            )
            messages.success(request, f'Course "{course.title}" created successfully!')
            return redirect('courses:manage_course', course_id=course.id)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'courses/create_course.html')

@login_required
def edit_course(request, course_id):
    """Edit course details (instructor only)"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'You can only edit your own courses.')
        return redirect('courses:course_detail', course_id=course.id)
    
    if request.method == 'POST':
        course.title = request.POST.get('title', course.title)
        course.description = request.POST.get('description', course.description)
        course.save()
        
        messages.success(request, 'Course updated successfully!')
        return redirect('courses:course_detail', course_id=course.id)
    
    context = {'course': course}
    return render(request, 'courses/edit_course.html', context)

@login_required
def manage_course(request, course_id):
    """Course management dashboard for instructors"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'You can only manage your own courses.')
        return redirect('courses:course_detail', course_id=course.id)
    
    # Get course statistics
    enrollments = Enrollment.objects.filter(course=course)
    quizzes = course.quizzes.all()
    
    context = {
        'course': course,
        'enrollments': enrollments,
        'quizzes': quizzes,
        'total_students': enrollments.count(),
        'total_quizzes': quizzes.count()
    }
    return render(request, 'courses/manage_course.html', context)

@login_required
def create_quiz(request, course_id):
    """Create a quiz for a course"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'You can only create quizzes for your own courses.')
        return redirect('courses:course_detail', course_id=course.id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        time_limit = request.POST.get('time_limit', 15)
        
        if title:
            quiz = Quiz.objects.create(
                course=course,
                title=title,
                time_limit=int(time_limit)
            )
            messages.success(request, f'Quiz "{quiz.title}" created successfully!')
            return redirect('courses:manage_course', course_id=course.id)
        else:
            messages.error(request, 'Please provide a quiz title.')
    
    context = {'course': course}
    return render(request, 'courses/create_quiz.html', context)

@login_required
def take_quiz(request, quiz_id):
    """Take a quiz (students only)"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.user.role != 'student':
        messages.error(request, 'Only students can take quizzes.')
        return redirect('courses:course_detail', course_id=quiz.course.id)
    
    # Check if student is enrolled
    if not Enrollment.objects.filter(student=request.user, course=quiz.course).exists():
        messages.error(request, 'You must be enrolled in the course to take this quiz.')
        return redirect('courses:course_detail', course_id=quiz.course.id)
    
    questions = quiz.questions.all()
    
    if request.method == 'POST':
        # Process quiz submission
        correct_count = 0
        total_questions = questions.count()
        
        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = get_object_or_404(Option, id=selected_option_id)
                
                # Save student answer
                StudentAnswer.objects.create(
                    student=request.user,
                    question=question,
                    selected_option=selected_option
                )
                
                if selected_option.is_correct:
                    correct_count += 1
        
        # Calculate score
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        # Update or create progress
        Progress.objects.update_or_create(
            student=request.user,
            course=quiz.course,
            defaults={
                'score': score,
                'completed_lessons': 1,
                'total_lessons': 1
            }
        )
        
        messages.success(request, f'Quiz completed! Your score: {score:.1f}%')
        return redirect('courses:quiz_results', quiz_id=quiz.id)
    
    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, 'courses/take_quiz.html', context)

@login_required
def quiz_results(request, quiz_id):
    """Display quiz results"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Get student's answers
    student_answers = StudentAnswer.objects.filter(
        student=request.user,
        question__quiz=quiz
    ).select_related('question', 'selected_option')
    
    # Get progress
    progress = Progress.objects.filter(
        student=request.user,
        course=quiz.course
    ).first()
    
    context = {
        'quiz': quiz,
        'student_answers': student_answers,
        'progress': progress
    }
    return render(request, 'courses/quiz_results.html', context)

@login_required
def my_courses(request):
    """Display student's enrolled courses"""
    if request.user.role != 'student':
        messages.error(request, 'This page is for students only.')
        return redirect('courses:course_list')
    
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course').order_by('-enrolled_at')
    
    # Get progress for each course
    enrolled_courses = []
    total_progress = 0
    completed_courses = 0
    courses_with_progress = 0
    
    for enrollment in enrollments:
        progress = Progress.objects.filter(
            student=request.user,
            course=enrollment.course
        ).first()
        
        enrolled_courses.append({
            'course': enrollment.course,
            'enrollment': enrollment,
            'progress': progress
        })
        
        # Calculate statistics
        if progress:
            total_progress += progress.progress_percent()
            courses_with_progress += 1
            if progress.progress_percent() >= 100:
                completed_courses += 1
    
    # Calculate average progress
    average_progress = total_progress / courses_with_progress if courses_with_progress > 0 else 0
    
    context = {
        'enrolled_courses': enrolled_courses,
        'completed_courses': completed_courses,
        'average_progress': average_progress
    }
    return render(request, 'courses/my_courses.html', context)

@login_required
def course_progress(request, course_id):
    """Display detailed course progress"""
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is enrolled
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You are not enrolled in this course.')
        return redirect('courses:course_detail', course_id=course.id)
    
    progress = Progress.objects.filter(
        student=request.user,
        course=course
    ).first()
    
    # Get completed quizzes
    completed_quizzes = StudentAnswer.objects.filter(
        student=request.user,
        question__quiz__course=course
    ).values('question__quiz').distinct()
    
    context = {
        'course': course,
        'progress': progress,
        'completed_quizzes_count': completed_quizzes.count(),
        'total_quizzes': course.quizzes.count()
    }
    return render(request, 'courses/course_progress.html', context)
# Debug view to test Django template rendering
def test_template_rendering(request):
    """Test view to verify Django template rendering is working"""
    from datetime import datetime
    
    # Create a simple template string
    template_string = """
    <html>
    <head><title>Django Template Test</title></head>
    <body>
        <h1>Django Template Rendering Test</h1>
        <p>Current time: {{ current_time|date:"M d, Y H:i" }}</p>
        <p>Test variable: {{ test_var }}</p>
        <p>If you see the actual values above (not template syntax), Django is working!</p>
        
        {% if courses %}
        <h2>Courses in Database:</h2>
        <ul>
        {% for course in courses %}
            <li>{{ course.title }} - Created: {{ course.created_at|date:"M d, Y" }}</li>
        {% endfor %}
        </ul>
        {% else %}
        <p>No courses found in database.</p>
        {% endif %}
    </body>
    </html>
    """
    
    template = Template(template_string)
    context = Context({
        'current_time': datetime.now(),
        'test_var': 'Hello from Django!',
        'courses': Course.objects.all()[:5]
    })
    
    return HttpResponse(template.render(context))