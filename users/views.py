from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .serializers import RegisterSerializer
from .models import CustomUser
import json


# API Views
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def api_login(request):
    """
    API endpoint for JWT token-based login
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                }
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)


# HTML Views
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
        context.update({
            'enrolled_courses': 0,  # TODO: Add actual course data
            'completed_lessons': 0,
            'certificates_earned': 0,
            'study_hours': 0,
            'recent_activity': [],
            'recommended_courses': [],
        })
    elif user.role == 'instructor':
        context.update({
            'created_courses': 0,  # TODO: Add actual course data
            'total_students': 0,
            'total_lessons': 0,
            'course_ratings': 0,
            'recent_activity': [],
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
