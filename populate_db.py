# Script to populate database with sample data
# Run this in Django shell: exec(open('populate_db.py').read())

from users.models import CustomUser
from courses.models import Course, Chapter, Topic, Quiz, Question, Option, Enrollment, Progress, StudentAnswer, TopicCompletion
from django.utils import timezone

print("=" * 60)
print("🎓 NeuroNest Database Population Script")
print("=" * 60)

# ============================================
# CREATE USERS
# ============================================
print("\n📝 Creating Users...")

# Create instructors
instructor1 = CustomUser.objects.create_user(
    username='prof_smith',
    email='smith@neuronest.edu',
    password='SecurePass123!',
    role='instructor',
    first_name='Professor',
    last_name='Smith'
)
print(f"✓ Created instructor: {instructor1.username}")

instructor2 = CustomUser.objects.create_user(
    username='prof_johnson',
    email='johnson@neuronest.edu',
    password='SecurePass123!',
    role='instructor',
    first_name='Dr.',
    last_name='Johnson'
)
print(f"✓ Created instructor: {instructor2.username}")

# Create students
student1 = CustomUser.objects.create_user(
    username='alice_student',
    email='alice@example.com',
    password='StudentPass123!',
    role='student',
    first_name='Alice',
    last_name='Williams'
)
print(f"✓ Created student: {student1.username}")

student2 = CustomUser.objects.create_user(
    username='bob_student',
    email='bob@example.com',
    password='StudentPass123!',
    role='student',
    first_name='Bob',
    last_name='Brown'
)
print(f"✓ Created student: {student2.username}")

# ============================================
# CREATE COURSES
# ============================================
print("\n📚 Creating Courses...")

course1 = Course.objects.create(
    title='Python Programming Fundamentals',
    description='Master the basics of Python programming with hands-on examples',
    instructor=instructor1,
    category='programming'
)
print(f"✓ Created course: {course1.title}")

course2 = Course.objects.create(
    title='Data Science Essentials',
    description='Learn data analysis and visualization with Python',
    instructor=instructor2,
    category='data_science'
)
print(f"✓ Created course: {course2.title}")

# ============================================
# CREATE CHAPTERS
# ============================================
print("\n📖 Creating Chapters...")

chapter1 = Chapter.objects.create(
    course=course1,
    title='Chapter 1: Introduction to Python',
    description='Get started with Python basics',
    order=1
)
print(f"✓ Created chapter: {chapter1.title}")

chapter2 = Chapter.objects.create(
    course=course1,
    title='Chapter 2: Data Types and Variables',
    description='Learn about different data types in Python',
    order=2
)
print(f"✓ Created chapter: {chapter2.title}")

# ============================================
# CREATE TOPICS
# ============================================
print("\n🎯 Creating Topics...")

topic1 = Topic.objects.create(
    chapter=chapter1,
    title='What is Python?',
    description='Introduction to Python programming language',
    notes='''
Python is a high-level, interpreted programming language known for its simplicity and readability.
Key features:
- Easy to learn and read
- Versatile (web, data science, AI, etc.)
- Large community support
- Extensive libraries
    ''',
    youtube_video_url='https://www.youtube.com/watch?v=rfscVS0vtik',
    order=1
)
print(f"✓ Created topic: {topic1.title}")

topic2 = Topic.objects.create(
    chapter=chapter1,
    title='Setting Up Python Environment',
    description='Install Python and set up your development environment',
    notes='''
Steps to set up Python:
1. Download Python from python.org
2. Install Python (check "Add Python to PATH")
3. Verify installation: python --version
4. Install IDE (VS Code, PyCharm, etc.)
    ''',
    extra_info='Make sure to download Python 3.10 or higher',
    order=2
)
print(f"✓ Created topic: {topic2.title}")

topic3 = Topic.objects.create(
    chapter=chapter2,
    title='Variables and Data Types',
    description='Understanding variables and Python data types',
    notes='''
Python Data Types:
- Strings: 'Hello World'
- Integers: 42
- Floats: 3.14
- Booleans: True/False
- Lists: [1, 2, 3]
- Dictionaries: {'key': 'value'}
    ''',
    youtube_video_url='https://www.youtube.com/watch?v=9uq3-3-d',
    order=1
)
print(f"✓ Created topic: {topic3.title}")

# ============================================
# CREATE QUIZZES
# ============================================
print("\n📋 Creating Quizzes...")

quiz1 = Quiz.objects.create(
    topic=topic1,
    title='Python Basics Quiz',
    quiz_type='topic',
    time_limit=15
)
print(f"✓ Created quiz: {quiz1.title}")

quiz2 = Quiz.objects.create(
    chapter=chapter1,
    title='Chapter 1 Review',
    quiz_type='chapter',
    time_limit=20
)
print(f"✓ Created quiz: {quiz2.title}")

# ============================================
# CREATE QUESTIONS AND OPTIONS
# ============================================
print("\n❓ Creating Questions...")

question1 = Question.objects.create(
    quiz=quiz1,
    text='What is Python?',
    question_type='multiple_choice'
)

Option.objects.create(
    question=question1,
    text='A high-level, interpreted programming language',
    is_correct=True
)
Option.objects.create(
    question=question1,
    text='A type of snake',
    is_correct=False
)
Option.objects.create(
    question=question1,
    text='A web browser',
    is_correct=False
)
print(f"✓ Created question: {question1.text} (3 options)")

question2 = Question.objects.create(
    quiz=quiz1,
    text='What file extension is used for Python files?',
    question_type='multiple_choice'
)

Option.objects.create(
    question=question2,
    text='.py',
    is_correct=True
)
Option.objects.create(
    question=question2,
    text='.python',
    is_correct=False
)
Option.objects.create(
    question=question2,
    text='.pyx',
    is_correct=False
)
print(f"✓ Created question: {question2.text} (3 options)")

# ============================================
# ENROLL STUDENTS IN COURSES
# ============================================
print("\n📚 Enrolling Students...")

enrollment1 = Enrollment.objects.create(
    student=student1,
    course=course1
)
print(f"✓ Enrolled {student1.username} in {course1.title}")

enrollment2 = Enrollment.objects.create(
    student=student1,
    course=course2
)
print(f"✓ Enrolled {student1.username} in {course2.title}")

enrollment3 = Enrollment.objects.create(
    student=student2,
    course=course1
)
print(f"✓ Enrolled {student2.username} in {course1.title}")

# ============================================
# CREATE PROGRESS RECORDS
# ============================================
print("\n📊 Creating Progress Records...")

progress1 = Progress.objects.create(
    student=student1,
    course=course1,
    completed_lessons=3,
    score=87.5
)
print(f"✓ Progress for {student1.username} in {course1.title}: Score={progress1.score}%, Lessons={progress1.completed_lessons}")

progress2 = Progress.objects.create(
    student=student1,
    course=course2,
    completed_lessons=1,
    score=92.0
)
print(f"✓ Progress for {student1.username} in {course2.title}: Score={progress2.score}%, Lessons={progress2.completed_lessons}")

progress3 = Progress.objects.create(
    student=student2,
    course=course1,
    completed_lessons=2,
    score=78.5
)
print(f"✓ Progress for {student2.username} in {course1.title}: Score={progress3.score}%, Lessons={progress3.completed_lessons}")

# ============================================
# RECORD QUIZ ANSWERS
# ============================================
print("\n✍️ Recording Quiz Answers...")

correct_option1 = Option.objects.get(question=question1, is_correct=True)
answer1 = StudentAnswer.objects.create(
    student=student1,
    question=question1,
    selected_option=correct_option1
)
print(f"✓ Recorded answer: {student1.username} answered Q1 correctly")

correct_option2 = Option.objects.get(question=question2, is_correct=True)
answer2 = StudentAnswer.objects.create(
    student=student1,
    question=question2,
    selected_option=correct_option2
)
print(f"✓ Recorded answer: {student1.username} answered Q2 correctly")

incorrect_option = Option.objects.get(question=question1, is_correct=False).first() if Option.objects.filter(question=question1, is_correct=False).exists() else None
if incorrect_option:
    answer3 = StudentAnswer.objects.create(
        student=student2,
        question=question1,
        selected_option=incorrect_option
    )
    print(f"✓ Recorded answer: {student2.username} answered Q1 incorrectly")

# ============================================
# MARK TOPICS AS COMPLETED
# ============================================
print("\n✅ Marking Topics as Completed...")

completion1 = TopicCompletion.objects.create(
    student=student1,
    topic=topic1
)
print(f"✓ {student1.username} completed: {topic1.title}")

completion2 = TopicCompletion.objects.create(
    student=student1,
    topic=topic2
)
print(f"✓ {student1.username} completed: {topic2.title}")

# ============================================
# SUMMARY STATISTICS
# ============================================
print("\n" + "=" * 60)
print("📊 DATABASE SUMMARY")
print("=" * 60)

print(f"\n👥 Users:")
print(f"   Total: {CustomUser.objects.count()}")
print(f"   Instructors: {CustomUser.objects.filter(role='instructor').count()}")
print(f"   Students: {CustomUser.objects.filter(role='student').count()}")

print(f"\n📚 Content:")
print(f"   Courses: {Course.objects.count()}")
print(f"   Chapters: {Chapter.objects.count()}")
print(f"   Topics: {Topic.objects.count()}")
print(f"   Quizzes: {Quiz.objects.count()}")
print(f"   Questions: {Question.objects.count()}")

print(f"\n📋 Interactions:")
print(f"   Enrollments: {Enrollment.objects.count()}")
print(f"   Progress Records: {Progress.objects.count()}")
print(f"   Quiz Answers: {StudentAnswer.objects.count()}")
print(f"   Topic Completions: {TopicCompletion.objects.count()}")

print("\n" + "=" * 60)
print("✨ Database population complete!")
print("=" * 60 + "\n")
