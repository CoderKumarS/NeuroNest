from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import CustomUser
import json


# HTML Views for User Management


def login_view(request):
    """
    HTML login page
    """
    # Redirect if already logged in
    if request.user.is_authenticated:
        messages.info(request, f'You are already logged in as {request.user.username}. Redirecting to dashboard.')
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                # Redirect to dashboard or next page
                next_url = request.GET.get('next', '/users/dashboard/')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'users/login.html')


def register_view(request):
    """
    HTML register page
    """
    # Redirect if already logged in
    if request.user.is_authenticated:
        messages.info(request, f'You are already logged in as {request.user.username}. Redirecting to dashboard.')
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get('role', 'student')
        
        # Validation
        if not all([username, email, password, password_confirm]):
            messages.error(request, 'Please fill in all fields.')
        elif password != password_confirm:
            messages.error(request, 'Passwords do not match.')
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role
                )
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'users/register.html')


def logout_view(request):
    """
    HTML logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def dashboard_view(request):
    """
    Dashboard for authenticated users - different content based on role
    """
    user = request.user
    
    # Prepare context data based on user role
    context = {
        'user': user,
        'user_role': user.role,
        'is_student': user.role == 'student',
        'is_instructor': user.role == 'instructor',
    }
    
    # Add role-specific data
    if user.role == 'student':
        # Import here to avoid circular imports
        from courses.models import Enrollment, Progress, StudentAnswer
        
        # Get student's enrolled courses
        enrollments = Enrollment.objects.filter(student=user).select_related('course')
        enrolled_courses_list = [enrollment.course for enrollment in enrollments]
        
        # Get progress data
        progress_records = Progress.objects.filter(student=user)
        total_completed_lessons = sum(p.completed_lessons for p in progress_records)
        
        # Get recent quiz attempts
        recent_answers = StudentAnswer.objects.filter(student=user).select_related(
            'question__quiz__course'
        ).order_by('-submitted_at')[:5]
        
        # Calculate certificates (courses with score >= 80%)
        certificates_earned = progress_records.filter(score__gte=80).count()
        
        # Calculate study hours (rough estimate based on completed lessons)
        study_hours = total_completed_lessons * 0.5  # Assume 30 minutes per lesson
        
        # Recent activity
        recent_activity = []
        for answer in recent_answers:
            recent_activity.append({
                'type': 'quiz_completed',
                'course': answer.question.quiz.course.title,
                'quiz': answer.question.quiz.title,
                'date': answer.submitted_at,
                'score': None  # We'd need to calculate this
            })
        
        context.update({
            'enrolled_courses': enrollments.count(),
            'enrolled_courses_list': enrolled_courses_list[:3],  # Show first 3
            'completed_lessons': total_completed_lessons,
            'certificates_earned': certificates_earned,
            'study_hours': int(study_hours),
            'recent_activity': recent_activity,
            'recommended_courses': [],
        })
        
    elif user.role == 'instructor':
        # Import here to avoid circular imports
        from courses.models import Course, Enrollment
        
        # Get instructor's courses
        instructor_courses = Course.objects.filter(instructor=user)
        
        # Get total students across all courses
        total_students = Enrollment.objects.filter(course__instructor=user).count()
        
        # Get total quizzes (lessons)
        total_lessons = sum(course.quizzes.count() for course in instructor_courses)
        
        # Recent activity for instructors
        recent_enrollments = Enrollment.objects.filter(
            course__instructor=user
        ).select_related('student', 'course').order_by('-enrolled_at')[:5]
        
        recent_activity = []
        for enrollment in recent_enrollments:
            recent_activity.append({
                'type': 'student_enrolled',
                'student': enrollment.student.username,
                'course': enrollment.course.title,
                'date': enrollment.enrolled_at
            })
        
        context.update({
            'created_courses': instructor_courses.count(),
            'created_courses_list': instructor_courses[:3],  # Show first 3
            'total_students': total_students,
            'total_lessons': total_lessons,
            'course_ratings': 4.8,  # Placeholder for now
            'recent_activity': recent_activity,
            'pending_approvals': [],
        })
    
    return render(request, 'users/dashboard.html', context)


# AJAX API endpoints
@csrf_exempt
@require_http_methods(["POST"])
def ajax_register(request):
    """
    AJAX endpoint for registration
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        role = data.get('role', 'student')
        
        if not all([username, email, password, password_confirm]):
            return JsonResponse({'success': False, 'message': 'All fields are required'}, status=400)
        
        if password != password_confirm:
            return JsonResponse({'success': False, 'message': 'Passwords do not match'}, status=400)
        
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists'}, status=400)
        
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already exists'}, status=400)
        
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Account created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def ajax_login(request):
    """
    AJAX endpoint for login
    """
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role
                    }
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)
        else:
            return JsonResponse({'success': False, 'message': 'Username and password are required'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)
