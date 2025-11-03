from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.core.paginator import Paginator
import json
import logging

from .models import ChatSession, ChatMessage, TutorRequest, TutorFeedback, CourseKnowledgeBase
from .services import AITutorService, UsageTracker, ContextBuilder, CourseContentProcessor
from courses.models import Course, Topic, Chapter

logger = logging.getLogger(__name__)

@login_required
def tutor_dashboard(request):
    """Main AI tutor dashboard"""
    if request.user.role != 'student':
        messages.error(request, 'AI Tutor is available for students only.')
        return redirect('courses:course_list')
    
    # Get user's recent chat sessions
    recent_sessions = ChatSession.objects.filter(
        student=request.user,
        is_active=True
    )[:5]
    
    # Get enrolled courses for context selection
    enrolled_courses = Course.objects.filter(
        enrollment__student=request.user
    ).distinct()
    
    # Get usage statistics
    from django.utils import timezone
    today = timezone.now().date()
    
    try:
        from .models import UsageStatistics
        daily_usage = UsageStatistics.objects.get(user=request.user, date=today)
    except UsageStatistics.DoesNotExist:
        daily_usage = None
    
    context = {
        'recent_sessions': recent_sessions,
        'enrolled_courses': enrolled_courses,
        'daily_usage': daily_usage,
    }
    
    return render(request, 'tutor/dashboard.html', context)

@login_required
def chat_session(request, session_id=None):
    """Chat interface with AI tutor"""
    if request.user.role != 'student':
        messages.error(request, 'AI Tutor is available for students only.')
        return redirect('courses:course_list')
    
    # Clear any existing Django messages to prevent popups in chat interface
    storage = messages.get_messages(request)
    for message in storage:
        pass  # This consumes and clears the messages
    
    # Get or create chat session
    if session_id:
        session = get_object_or_404(ChatSession, id=session_id, student=request.user)
    else:
        session = ChatSession.objects.create(
            student=request.user,
            title="New Chat Session"
        )
        return redirect('tutor:chat_session', session_id=session.id)
    
    # Get messages for this session
    messages_list = session.messages.all()
    
    # Get enrolled courses for context
    enrolled_courses = Course.objects.filter(
        enrollment__student=request.user
    ).distinct()
    
    context = {
        'session': session,
        'messages': messages_list,
        'enrolled_courses': enrolled_courses,
    }
    
    return render(request, 'tutor/chat_simple.html', context)

@login_required
@csrf_exempt
def send_message(request):
    """Handle AJAX message sending"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        message_content = data.get('message', '').strip()
        course_id = data.get('course_id')
        request_type = data.get('request_type', 'question')
        
        if not message_content:
            return JsonResponse({'error': 'Message content is required'}, status=400)
        
        # Check usage limits
        within_limits, limit_message = UsageTracker.check_usage_limits(request.user)
        if not within_limits:
            return JsonResponse({'error': limit_message}, status=429)
        
        # Get chat session
        try:
            session = ChatSession.objects.get(id=session_id, student=request.user)
        except ChatSession.DoesNotExist:
            # Create a new session for the user if the requested one doesn't exist
            session = ChatSession.objects.create(
                student=request.user,
                title="New Chat Session"
            )
            logger.warning(f"Session {session_id} not found for user {request.user.username}, created new session {session.id}")
        
        # Save user message
        user_message = ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=message_content
        )
        
        # Build context if course is selected
        context = ""
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                # Check if user is enrolled
                if not course.enrollment_set.filter(student=request.user).exists():
                    return JsonResponse({'error': 'You are not enrolled in this course'}, status=403)
                
                context = ContextBuilder.build_course_context(course)
                session.course = course
                session.save()
            except Course.DoesNotExist:
                pass
        
        # Generate AI response
        logger.info(f"Generating AI response for user {request.user.username}, session {session.id}, course_id='{course_id}'")
        ai_service = AITutorService()
        
        if request_type == 'summarize' and course_id:
            # Handle summarization request
            course = Course.objects.get(id=course_id)
            course_content = CourseContentProcessor.process_course_content(course)
            response_data = ai_service.summarize_content(
                course_content.get('course_summary', ''),
                'course'
            )
        elif request_type == 'explain':
            # Handle concept explanation
            response_data = ai_service.explain_concept(message_content, context)
        else:
            # Handle general question
            response_data = ai_service.generate_response(message_content, context, session.id)
        
        if response_data['success']:
            # Save AI response
            ai_message = ChatMessage.objects.create(
                session=session,
                message_type='ai',
                content=response_data['response'],
                context_used=context,
                ai_model=response_data.get('model', ''),
                tokens_used=response_data.get('tokens_used', 0)
            )
            
            # Track usage
            UsageTracker.track_usage(
                request.user,
                tokens_used=response_data.get('tokens_used', 0)
            )
            
            # Update session title if it's the first exchange
            if session.get_message_count() <= 2 and session.title == "New Chat Session":
                session.title = message_content[:50] + "..." if len(message_content) > 50 else message_content
                session.save()
            
            return JsonResponse({
                'success': True,
                'ai_response': response_data['response'],
                'message_id': ai_message.id,
                'tokens_used': response_data.get('tokens_used', 0),
                'response_time': response_data.get('response_time', 0)
            })
        else:
            # Save error message
            ChatMessage.objects.create(
                session=session,
                message_type='system',
                content=f"Error: {response_data.get('error', 'Unknown error')}"
            )
            
            return JsonResponse({
                'success': False,
                'error': response_data.get('error', 'Failed to generate response'),
                'fallback_response': response_data.get('response', 'I apologize, but I encountered an error. Please try again.')
            })
    
    except Exception as e:
        logger.error(f"Error in send_message for user {request.user.username}: {str(e)}")
        logger.error(f"Request data: session_id={session_id}, message='{message_content}', course_id='{course_id}', request_type='{request_type}'")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@login_required
def topic_help(request, topic_id):
    """Get AI help for a specific topic"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Check if user is enrolled in the course
    if not topic.chapter.course.enrollment_set.filter(student=request.user).exists():
        return JsonResponse({'error': 'You are not enrolled in this course'}, status=403)
    
    # Build topic context
    context = ContextBuilder.build_topic_context(topic)
    
    # Get or create a session for this topic
    session, created = ChatSession.objects.get_or_create(
        student=request.user,
        course=topic.chapter.course,
        title=f"Help with: {topic.title}",
        defaults={'is_active': True}
    )
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '').strip()
            
            if not question:
                return JsonResponse({'error': 'Question is required'}, status=400)
            
            # Check usage limits
            within_limits, limit_message = UsageTracker.check_usage_limits(request.user)
            if not within_limits:
                return JsonResponse({'error': limit_message}, status=429)
            
            # Generate AI response
            ai_service = AITutorService()
            response_data = ai_service.generate_response(question, context, session.id)
            
            if response_data['success']:
                # Save messages
                ChatMessage.objects.create(
                    session=session,
                    message_type='user',
                    content=question
                )
                
                ChatMessage.objects.create(
                    session=session,
                    message_type='ai',
                    content=response_data['response'],
                    context_used=context,
                    ai_model=response_data.get('model', ''),
                    tokens_used=response_data.get('tokens_used', 0)
                )
                
                # Track usage
                UsageTracker.track_usage(
                    request.user,
                    tokens_used=response_data.get('tokens_used', 0)
                )
                
                return JsonResponse({
                    'success': True,
                    'response': response_data['response'],
                    'session_id': session.id
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': response_data.get('error', 'Failed to generate response')
                })
        
        except Exception as e:
            logger.error(f"Error in topic_help: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    
    # GET request - return topic help interface
    context_data = {
        'topic': topic,
        'session': session,
        'context': context
    }
    
    return render(request, 'tutor/topic_help.html', context_data)

@login_required
def summarize_content(request):
    """Summarize course content"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        data = json.loads(request.body)
        content_type = data.get('content_type')  # 'course', 'chapter', 'topic'
        content_id = data.get('content_id')
        
        # Check usage limits
        within_limits, limit_message = UsageTracker.check_usage_limits(request.user)
        if not within_limits:
            return JsonResponse({'error': limit_message}, status=429)
        
        # Get content and build context
        if content_type == 'course':
            course = get_object_or_404(Course, id=content_id)
            if not course.enrollment_set.filter(student=request.user).exists():
                return JsonResponse({'error': 'You are not enrolled in this course'}, status=403)
            
            content = ContextBuilder.build_course_context(course)
            title = f"Summary of {course.title}"
            
        elif content_type == 'chapter':
            chapter = get_object_or_404(Chapter, id=content_id)
            if not chapter.course.enrollment_set.filter(student=request.user).exists():
                return JsonResponse({'error': 'You are not enrolled in this course'}, status=403)
            
            content = ContextBuilder.build_chapter_context(chapter)
            title = f"Summary of {chapter.title}"
            
        elif content_type == 'topic':
            topic = get_object_or_404(Topic, id=content_id)
            if not topic.chapter.course.enrollment_set.filter(student=request.user).exists():
                return JsonResponse({'error': 'You are not enrolled in this course'}, status=403)
            
            content = ContextBuilder.build_topic_context(topic)
            title = f"Summary of {topic.title}"
            
        else:
            return JsonResponse({'error': 'Invalid content type'}, status=400)
        
        # Generate summary
        ai_service = AITutorService()
        response_data = ai_service.summarize_content(content, content_type)
        
        if response_data['success']:
            # Track usage
            UsageTracker.track_usage(
                request.user,
                tokens_used=response_data.get('tokens_used', 0)
            )
            
            return JsonResponse({
                'success': True,
                'summary': response_data['response'],
                'title': title,
                'tokens_used': response_data.get('tokens_used', 0)
            })
        else:
            return JsonResponse({
                'success': False,
                'error': response_data.get('error', 'Failed to generate summary')
            })
    
    except Exception as e:
        logger.error(f"Error in summarize_content: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@login_required
def chat_history(request):
    """View chat history"""
    if request.user.role != 'student':
        messages.error(request, 'Access denied.')
        return redirect('courses:course_list')
    
    sessions = ChatSession.objects.filter(student=request.user).order_by('-updated_at')
    
    # Pagination
    paginator = Paginator(sessions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'sessions': page_obj
    }
    
    return render(request, 'tutor/history.html', context)

@login_required
@csrf_exempt
def submit_feedback(request):
    """Submit feedback on AI responses"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST method required'}, status=405)
    
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        feedback_type = data.get('feedback_type')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        message = get_object_or_404(ChatMessage, id=message_id)
        
        # Create feedback
        feedback = TutorFeedback.objects.create(
            student=request.user,
            message=message,
            feedback_type=feedback_type,
            rating=rating,
            comment=comment
        )
        
        return JsonResponse({'success': True, 'feedback_id': feedback.id})
    
    except Exception as e:
        logger.error(f"Error in submit_feedback: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

@login_required
def delete_session(request, session_id):
    """Delete a chat session"""
    if request.method == 'POST':
        session = get_object_or_404(ChatSession, id=session_id, student=request.user)
        session.delete()
        messages.success(request, 'Chat session deleted successfully.')
    
    return redirect('tutor:chat_history')

# Admin/Instructor views for monitoring

@login_required
def admin_dashboard(request):
    """Admin dashboard for AI tutor monitoring"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('courses:course_list')
    
    from django.db.models import Count, Sum
    from django.utils import timezone
    
    # Get statistics
    today = timezone.now().date()
    
    stats = {
        'total_sessions': ChatSession.objects.count(),
        'active_sessions': ChatSession.objects.filter(is_active=True).count(),
        'total_messages': ChatMessage.objects.count(),
        'daily_usage': UsageStatistics.objects.filter(date=today).aggregate(
            total_requests=Sum('requests_count'),
            total_tokens=Sum('tokens_used')
        )
    }
    
    # Recent activity
    recent_sessions = ChatSession.objects.select_related('student').order_by('-updated_at')[:10]
    
    context = {
        'stats': stats,
        'recent_sessions': recent_sessions
    }
    
    return render(request, 'tutor/admin_dashboard.html', context)


@login_required
def create_widget_session(request):
    """Create a new chat session for the AI assistant widget"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Create a new session for the widget
    session = ChatSession.objects.create(
        student=request.user,
        title="AI Assistant Chat"
    )
    
    return JsonResponse({
        'success': True,
        'session_id': session.id
    })