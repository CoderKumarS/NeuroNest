from .models import Course, Enrollment, Quiz, Question, Option, StudentAnswer, Progress, Chapter, Topic, TopicCompletion

# HTML Views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Case, When, Value, CharField
from django.template import Template, Context
from django.contrib.auth import get_user_model

User = get_user_model()
# HTML Views for Course Management

# HTML Views for Course Management

def course_list(request):
    """Display all courses with search and filtering"""
    courses = Course.objects.all().annotate(
        enrollment_count=Count('enrollment'),
        avg_rating=Avg('progress__score')
    )
    
    # Get filter parameters
    search_query = request.GET.get('search', '')
    instructor_filter = request.GET.get('instructor', '')
    category_filter = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'newest')
    min_rating = request.GET.get('min_rating', '')
    
    # Search functionality - enhanced to include category
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(instructor__username__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    
    # Category filter
    if category_filter:
        courses = courses.filter(category=category_filter)
    
    # Instructor filter
    if instructor_filter:
        courses = courses.filter(instructor__username__icontains=instructor_filter)
    
    # Rating filter
    if min_rating:
        try:
            min_rating_value = float(min_rating)
            courses = courses.filter(avg_rating__gte=min_rating_value)
        except (ValueError, TypeError):
            pass
    
    # Sorting
    if sort_by == 'newest':
        courses = courses.order_by('-created_at')
    elif sort_by == 'oldest':
        courses = courses.order_by('created_at')
    elif sort_by == 'popular':
        courses = courses.order_by('-enrollment_count', '-created_at')
    elif sort_by == 'rating':
        courses = courses.order_by('-avg_rating', '-created_at')
    elif sort_by == 'title':
        courses = courses.order_by('title')
    elif sort_by == 'category':
        courses = courses.order_by('category', 'title')
    else:
        courses = courses.order_by('-created_at')
    
    # Get unique instructors for filter dropdown
    instructors = User.objects.filter(role='instructor', course__isnull=False).distinct().order_by('username')
    
    # Get categories with course counts
    categories_with_counts = Course.objects.values('category').annotate(
        count=Count('id'),
        category_display=Case(
            *[When(category=choice[0], then=Value(choice[1])) for choice in Course.CATEGORY_CHOICES],
            default=Value('Other'),
            output_field=CharField()
        )
    ).order_by('category_display')
    
    # Pagination
    paginator = Paginator(courses, 9)  # 9 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'instructor_filter': instructor_filter,
        'category_filter': category_filter,
        'sort_by': sort_by,
        'min_rating': min_rating,
        'total_courses': courses.count(),
        'instructors': instructors,
        'categories': categories_with_counts,
        'category_choices': Course.CATEGORY_CHOICES,
        'sort_options': [
            ('newest', 'Newest First'),
            ('oldest', 'Oldest First'),
            ('popular', 'Most Popular'),
            ('rating', 'Highest Rated'),
            ('title', 'Alphabetical'),
            ('category', 'By Category'),
        ]
    }
    return render(request, 'courses/course/course_list.html', context)

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
    return render(request, 'courses/course/course_explorer.html', context)

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
    
    # Get course chapters and quizzes
    chapters = course.chapters.all().prefetch_related('topics', 'quizzes')
    # No more course-level quizzes - all quizzes belong to chapters or topics
    course_quizzes = []
    
    # Get other courses by same instructor
    related_courses = Course.objects.filter(
        instructor=course.instructor
    ).exclude(id=course.id)[:3]
    
    # Get completed topics for student
    completed_topics = []
    if request.user.is_authenticated and request.user.role == 'student':
        completed_topics = TopicCompletion.objects.filter(
            student=request.user,
            topic__chapter__course=course
        ).values_list('topic_id', flat=True)
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'user_progress': user_progress,
        'chapters': chapters,
        'course_quizzes': course_quizzes,
        'completed_topics': completed_topics,
        'related_courses': related_courses,
        'is_instructor': request.user == course.instructor if request.user.is_authenticated else False
    }
    
    # Debug: Print context to verify data
    print(f"🔍 DEBUG: Context keys: {list(context.keys())}")
    print(f"🔍 DEBUG: Template path: courses/course_detail.html")
    
    return render(request, 'courses/course/course_detail.html', context)

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
    
    return render(request, 'courses/course/create_course.html')

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
    return render(request, 'courses/course/edit_course.html', context)

@login_required
def manage_course(request, course_id):
    """Course management dashboard for instructors"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'You can only manage your own courses.')
        return redirect('courses:course_detail', course_id=course.id)
    
    # Get course statistics
    enrollments = Enrollment.objects.filter(course=course)
    quizzes = course.get_all_quizzes()  # Get all quizzes from chapters and topics
    chapters = course.chapters.all().prefetch_related('topics', 'quizzes')
    
    context = {
        'course': course,
        'enrollments': enrollments,
        'quizzes': quizzes,
        'chapters': chapters,
        'total_students': enrollments.count(),
        'total_quizzes': quizzes.count(),
        'total_chapters': chapters.count()
    }
    return render(request, 'courses/course/manage_course.html', context)

@login_required
def create_quiz(request, course_id):
    """Create a quiz for a course chapter"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'You can only create quizzes for your own courses.')
        return redirect('courses:course_detail', course_id=course.id)
    
    # Get course chapters for selection
    chapters = course.chapters.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        time_limit = request.POST.get('time_limit', 15)
        chapter_id = request.POST.get('chapter_id')
        quiz_type = request.POST.get('quiz_type', 'chapter')
        
        if title and chapter_id:
            chapter = get_object_or_404(Chapter, id=chapter_id, course=course)
            quiz = Quiz.objects.create(
                chapter=chapter,
                title=title,
                quiz_type=quiz_type,
                time_limit=int(time_limit)
            )
            messages.success(request, f'Quiz "{quiz.title}" created successfully for {chapter.title}!')
            return redirect('courses:manage_quiz', quiz_id=quiz.id)
        else:
            messages.error(request, 'Please provide a quiz title and select a chapter.')
    
    context = {
        'course': course,
        'chapters': chapters
    }
    return render(request, 'courses/quiz/create_quiz.html', context)

@login_required
def create_topic_quiz(request, topic_id):
    """Create a quiz for a specific topic"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.user != topic.chapter.course.instructor:
        messages.error(request, 'You can only create quizzes for your own courses.')
        return redirect('courses:topic_detail', topic_id=topic.id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        time_limit = request.POST.get('time_limit', 15)
        
        if title:
            quiz = Quiz.objects.create(
                topic=topic,
                title=title,
                quiz_type='topic',
                time_limit=int(time_limit)
            )
            messages.success(request, f'Quiz "{quiz.title}" created successfully for topic "{topic.title}"!')
            return redirect('courses:manage_quiz', quiz_id=quiz.id)
        else:
            messages.error(request, 'Please provide a quiz title.')
    
    context = {'topic': topic}
    return render(request, 'courses/quiz/create_topic_quiz.html', context)

@login_required
def edit_quiz(request, quiz_id):
    """Edit quiz details"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Check permissions
    if request.user != quiz.course.instructor:
        messages.error(request, 'You can only edit your own quizzes.')
        return redirect('courses:course_detail', course_id=quiz.course.id)
    
    if request.method == 'POST':
        quiz.title = request.POST.get('title', quiz.title)
        quiz.time_limit = int(request.POST.get('time_limit', quiz.time_limit))
        quiz.save()
        
        messages.success(request, f'Quiz "{quiz.title}" updated successfully!')
        return redirect('courses:manage_quiz', quiz_id=quiz.id)
    
    context = {'quiz': quiz}
    return render(request, 'courses/quiz/edit_quiz.html', context)

@login_required
def manage_quiz(request, quiz_id):
    """Manage quiz questions and options"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Check permissions
    if request.user != quiz.course.instructor:
        messages.error(request, 'You can only manage your own quizzes.')
        return redirect('courses:course_detail', course_id=quiz.course.id)
    
    questions = quiz.questions.all().prefetch_related('options')
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'total_questions': questions.count()
    }
    return render(request, 'courses/quiz/manage_quiz.html', context)

@login_required
def add_question(request, quiz_id):
    """Add a question to a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Check permissions
    if request.user != quiz.course.instructor:
        messages.error(request, 'You can only add questions to your own quizzes.')
        return redirect('courses:course_detail', course_id=quiz.course.id)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        options = [
            request.POST.get('option_1', ''),
            request.POST.get('option_2', ''),
            request.POST.get('option_3', ''),
            request.POST.get('option_4', '')
        ]
        correct_option = int(request.POST.get('correct_option', 1)) - 1
        
        if question_text and all(options):
            # Create the question
            question = Question.objects.create(
                quiz=quiz,
                text=question_text
            )
            
            # Create the options
            for i, option_text in enumerate(options):
                Option.objects.create(
                    question=question,
                    text=option_text,
                    is_correct=(i == correct_option)
                )
            
            messages.success(request, 'Question added successfully!')
            return redirect('courses:manage_quiz', quiz_id=quiz.id)
        else:
            messages.error(request, 'Please fill in all fields.')
    
    context = {'quiz': quiz}
    return render(request, 'courses/quiz/add_question.html', context)

@login_required
def edit_question(request, question_id):
    """Edit a quiz question"""
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz
    
    # Check permissions
    if request.user != quiz.course.instructor:
        messages.error(request, 'You can only edit your own quiz questions.')
        return redirect('courses:course_detail', course_id=quiz.course.id)
    
    if request.method == 'POST':
        question.text = request.POST.get('question_text', question.text)
        question.save()
        
        # Update options
        options = question.options.all()
        option_texts = [
            request.POST.get('option_1', ''),
            request.POST.get('option_2', ''),
            request.POST.get('option_3', ''),
            request.POST.get('option_4', '')
        ]
        correct_option = int(request.POST.get('correct_option', 1)) - 1
        
        for i, option in enumerate(options):
            if i < len(option_texts):
                option.text = option_texts[i]
                option.is_correct = (i == correct_option)
                option.save()
        
        messages.success(request, 'Question updated successfully!')
        return redirect('courses:manage_quiz', quiz_id=quiz.id)
    
    options = list(question.options.all())
    context = {
        'question': question,
        'quiz': quiz,
        'options': options
    }
    return render(request, 'courses/quiz/edit_question.html', context)

@login_required
def delete_question(request, question_id):
    """Delete a quiz question"""
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz
    
    # Check permissions
    if request.user != quiz.course.instructor:
        messages.error(request, 'You can only delete your own quiz questions.')
        return redirect('courses:course_detail', course_id=quiz.course.id)
    
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
    
    return redirect('courses:manage_quiz', quiz_id=quiz.id)

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
    return render(request, 'courses/quiz/take_quiz.html', context)

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
    return render(request, 'courses/quiz/quiz_results.html', context)

@login_required
def my_courses(request):
    """Display student's enrolled courses with filtering and sorting"""
    if request.user.role != 'student':
        messages.error(request, 'This page is for students only.')
        return redirect('courses:course_list')
    
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    progress_filter = request.GET.get('progress', '')  # all, not_started, in_progress, completed
    sort_by = request.GET.get('sort', 'recent')  # recent, oldest, progress_asc, progress_desc, alphabetical, completion
    
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
        
        course_data = {
            'course': enrollment.course,
            'enrollment': enrollment,
            'progress': progress
        }
        
        # Apply search filter
        if search_query:
            if (search_query.lower() not in enrollment.course.title.lower() and 
                search_query.lower() not in enrollment.course.description.lower() and
                search_query.lower() not in enrollment.course.instructor.username.lower()):
                continue
        
        # Apply progress filter
        if progress_filter:
            progress_percent = progress.progress_percent() if progress else 0
            if progress_filter == 'not_started' and progress_percent > 0:
                continue
            elif progress_filter == 'in_progress' and (progress_percent == 0 or progress_percent >= 100):
                continue
            elif progress_filter == 'completed' and progress_percent < 100:
                continue
        
        enrolled_courses.append(course_data)
        
        # Calculate statistics
        if progress:
            total_progress += progress.progress_percent()
            courses_with_progress += 1
            if progress.progress_percent() >= 100:
                completed_courses += 1
    
    # Apply sorting
    if sort_by == 'oldest':
        enrolled_courses.sort(key=lambda x: x['enrollment'].enrolled_at)
    elif sort_by == 'progress_asc':
        enrolled_courses.sort(key=lambda x: x['progress'].progress_percent() if x['progress'] else 0)
    elif sort_by == 'progress_desc':
        enrolled_courses.sort(key=lambda x: x['progress'].progress_percent() if x['progress'] else 0, reverse=True)
    elif sort_by == 'alphabetical':
        enrolled_courses.sort(key=lambda x: x['course'].title.lower())
    elif sort_by == 'completion':
        enrolled_courses.sort(key=lambda x: x['enrollment'].enrolled_at, reverse=True)
        # Sort completed courses first, then by enrollment date
        enrolled_courses.sort(key=lambda x: x['progress'].progress_percent() >= 100 if x['progress'] else False, reverse=True)
    # Default 'recent' is already sorted by enrollment date desc
    
    # Calculate average progress
    average_progress = total_progress / courses_with_progress if courses_with_progress > 0 else 0
    
    # Count courses by status for filter display
    not_started_count = sum(1 for course in enrolled_courses if not course['progress'] or course['progress'].progress_percent() == 0)
    in_progress_count = sum(1 for course in enrolled_courses if course['progress'] and 0 < course['progress'].progress_percent() < 100)
    completed_count = sum(1 for course in enrolled_courses if course['progress'] and course['progress'].progress_percent() >= 100)
    
    context = {
        'enrolled_courses': enrolled_courses,
        'completed_courses': completed_courses,
        'average_progress': average_progress,
        'search_query': search_query,
        'progress_filter': progress_filter,
        'sort_by': sort_by,
        'not_started_count': not_started_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'total_enrolled': len(enrolled_courses)
    }
    return render(request, 'courses/course/my_courses.html', context)

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
    from django.db.models import Q
    completed_quizzes = StudentAnswer.objects.filter(
        student=request.user,
        question__quiz__in=course.get_all_quizzes()
    ).values('question__quiz').distinct()
    
    context = {
        'course': course,
        'progress': progress,
        'completed_quizzes_count': completed_quizzes.count(),
        'total_quizzes': course.get_total_quizzes()
    }
    return render(request, 'courses/course/course_progress.html', context)
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
# Chapter Management Views

@login_required
def manage_chapters(request, course_id):
    """Manage chapters for a course"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'You can only manage chapters for your own courses.')
        return redirect('courses:course_detail', course_id=course.id)
    
    chapters = course.chapters.all().prefetch_related('topics', 'quizzes')
    
    context = {
        'course': course,
        'chapters': chapters,
    }
    return render(request, 'courses/chapter/manage_chapters.html', context)


@login_required
def create_chapter(request, course_id):
    """Create a new chapter"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.instructor:
        messages.error(request, 'You can only create chapters for your own courses.')
        return redirect('courses:course_detail', course_id=course.id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        order = request.POST.get('order', 0)
        
        if title:
            chapter = Chapter.objects.create(
                course=course,
                title=title,
                description=description,
                order=int(order) if order else course.chapters.count() + 1
            )
            messages.success(request, f'Chapter "{chapter.title}" created successfully!')
            return redirect('courses:manage_chapters', course_id=course.id)
        else:
            messages.error(request, 'Please provide a chapter title.')
    
    context = {
        'course': course,
        'next_order': course.chapters.count() + 1
    }
    return render(request, 'courses/chapter/create_chapter.html', context)


@login_required
def edit_chapter(request, chapter_id):
    """Edit chapter details"""
    chapter = get_object_or_404(Chapter, id=chapter_id)
    
    if request.user != chapter.course.instructor:
        messages.error(request, 'You can only edit chapters for your own courses.')
        return redirect('courses:course_detail', course_id=chapter.course.id)
    
    if request.method == 'POST':
        chapter.title = request.POST.get('title', chapter.title)
        chapter.description = request.POST.get('description', chapter.description)
        chapter.order = int(request.POST.get('order', chapter.order))
        chapter.save()
        
        messages.success(request, 'Chapter updated successfully!')
        return redirect('courses:manage_chapters', course_id=chapter.course.id)
    
    context = {'chapter': chapter}
    return render(request, 'courses/chapter/edit_chapter.html', context)


def chapter_detail(request, chapter_id):
    """Display chapter details with topics"""
    chapter = get_object_or_404(Chapter, id=chapter_id)
    
    # Check if user is enrolled or is the instructor
    is_enrolled = False
    is_instructor = request.user == chapter.course.instructor if request.user.is_authenticated else False
    
    if request.user.is_authenticated and request.user.role == 'student':
        is_enrolled = Enrollment.objects.filter(
            student=request.user, 
            course=chapter.course
        ).exists()
    
    if not is_enrolled and not is_instructor:
        messages.error(request, 'You must be enrolled in this course to view chapters.')
        return redirect('courses:course_detail', course_id=chapter.course.id)
    
    topics = chapter.topics.all()
    
    # Get completed topics for student
    completed_topics = []
    if request.user.is_authenticated and request.user.role == 'student':
        completed_topics = TopicCompletion.objects.filter(
            student=request.user,
            topic__in=topics
        ).values_list('topic_id', flat=True)
    
    context = {
        'chapter': chapter,
        'topics': topics,
        'completed_topics': completed_topics,
        'is_instructor': is_instructor,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/chapter/chapter_detail.html', context)


# Topic Management Views

@login_required
def create_topic(request, chapter_id):
    """Create a new topic"""
    chapter = get_object_or_404(Chapter, id=chapter_id)
    
    if request.user != chapter.course.instructor:
        messages.error(request, 'You can only create topics for your own courses.')
        return redirect('courses:chapter_detail', chapter_id=chapter.id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        order = request.POST.get('order', 0)
        youtube_video_url = request.POST.get('youtube_video_url', '')
        notes = request.POST.get('notes', '')
        extra_info = request.POST.get('extra_info', '')
        
        # Validate that at least one content field is provided
        if not any([youtube_video_url, notes, extra_info]):
            messages.error(request, 'Please provide at least one of: YouTube video, notes, or extra info.')
        elif title:
            topic = Topic.objects.create(
                chapter=chapter,
                title=title,
                description=description,
                order=int(order) if order else chapter.topics.count() + 1,
                youtube_video_url=youtube_video_url,
                notes=notes,
                extra_info=extra_info
            )
            messages.success(request, f'Topic "{topic.title}" created successfully!')
            return redirect('courses:chapter_detail', chapter_id=chapter.id)
        else:
            messages.error(request, 'Please provide a topic title.')
    
    context = {
        'chapter': chapter,
        'next_order': chapter.topics.count() + 1
    }
    return render(request, 'courses/topic/create_topic.html', context)


@login_required
def edit_topic(request, topic_id):
    """Edit topic details"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.user != topic.chapter.course.instructor:
        messages.error(request, 'You can only edit topics for your own courses.')
        return redirect('courses:topic_detail', topic_id=topic.id)
    
    if request.method == 'POST':
        topic.title = request.POST.get('title', topic.title)
        topic.description = request.POST.get('description', topic.description)
        topic.order = int(request.POST.get('order', topic.order))
        topic.youtube_video_url = request.POST.get('youtube_video_url', topic.youtube_video_url)
        topic.notes = request.POST.get('notes', topic.notes)
        topic.extra_info = request.POST.get('extra_info', topic.extra_info)
        
        # Validate that at least one content field is provided
        if not any([topic.youtube_video_url, topic.notes, topic.extra_info]):
            messages.error(request, 'Please provide at least one of: YouTube video, notes, or extra info.')
        else:
            topic.save()
            messages.success(request, 'Topic updated successfully!')
            return redirect('courses:topic_detail', topic_id=topic.id)
    
    context = {'topic': topic}
    return render(request, 'courses/topic/edit_topic.html', context)


def topic_detail(request, topic_id):
    """Display topic details with content"""
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Check if user is enrolled or is the instructor
    is_enrolled = False
    is_instructor = request.user == topic.chapter.course.instructor if request.user.is_authenticated else False
    
    if request.user.is_authenticated and request.user.role == 'student':
        is_enrolled = Enrollment.objects.filter(
            student=request.user, 
            course=topic.chapter.course
        ).exists()
    
    if not is_enrolled and not is_instructor:
        messages.error(request, 'You must be enrolled in this course to view topics.')
        return redirect('courses:course_detail', course_id=topic.chapter.course.id)
    
    # Check if topic is completed by student
    is_completed = False
    if request.user.is_authenticated and request.user.role == 'student':
        is_completed = TopicCompletion.objects.filter(
            student=request.user,
            topic=topic
        ).exists()
    
    # Get topic quizzes
    topic_quizzes = topic.quizzes.all()
    
    context = {
        'topic': topic,
        'is_instructor': is_instructor,
        'is_enrolled': is_enrolled,
        'is_completed': is_completed,
        'topic_quizzes': topic_quizzes,
        'youtube_embed_url': topic.get_youtube_embed_url(),
    }
    return render(request, 'courses/topic/topic_detail.html', context)


@login_required
def complete_topic(request, topic_id):
    """Mark topic as completed for student"""
    if request.user.role != 'student':
        messages.error(request, 'Only students can complete topics.')
        return redirect('courses:topic_detail', topic_id=topic_id)
    
    topic = get_object_or_404(Topic, id=topic_id)
    
    # Check if student is enrolled
    if not Enrollment.objects.filter(student=request.user, course=topic.chapter.course).exists():
        messages.error(request, 'You must be enrolled in this course.')
        return redirect('courses:course_detail', course_id=topic.chapter.course.id)
    
    # Mark as completed
    completion, created = TopicCompletion.objects.get_or_create(
        student=request.user,
        topic=topic
    )
    
    if created:
        messages.success(request, f'Topic "{topic.title}" marked as completed!')
        
        # Update course progress
        total_topics = Topic.objects.filter(chapter__course=topic.chapter.course).count()
        completed_topics = TopicCompletion.objects.filter(
            student=request.user,
            topic__chapter__course=topic.chapter.course
        ).count()
        
        progress, _ = Progress.objects.get_or_create(
            student=request.user,
            course=topic.chapter.course,
            defaults={'total_lessons': total_topics}
        )
        progress.completed_lessons = completed_topics
        progress.total_lessons = total_topics
        progress.save()
    else:
        messages.info(request, 'Topic already completed.')
    
    return redirect('courses:topic_detail', topic_id=topic.id)