# 🎬 LIVE EXAMPLES - Try These in Django Shell

## **Getting Started**

```powershell
# Step 1: Activate environment
cd "d:\Django Project"
.\venv\Scripts\activate

# Step 2: Start Django shell
python manage.py shell

# Step 3: Copy-paste the examples below into the shell
```

---

## **EXAMPLE 1: Create a Complete Course with Content**

```python
# Import models
from users.models import CustomUser
from courses.models import Course, Chapter, Topic, Quiz, Question, Option, Enrollment

# Create instructor
instructor = CustomUser.objects.create_user(
    username='prof_demo',
    email='prof@demo.com',
    password='demo123',
    role='instructor',
    first_name='Demo',
    last_name='Instructor'
)

# Create course
course = Course.objects.create(
    title='Web Development Basics',
    description='Learn HTML, CSS, and JavaScript',
    instructor=instructor,
    category='programming'
)

# Create chapter
chapter = Chapter.objects.create(
    course=course,
    title='Chapter 1: HTML Basics',
    description='Learn HTML fundamentals',
    order=1
)

# Create topic
topic = Topic.objects.create(
    chapter=chapter,
    title='HTML Tags and Elements',
    description='Understanding HTML structure',
    notes='HTML tags are used to mark up content...',
    order=1
)

# Create quiz
quiz = Quiz.objects.create(
    topic=topic,
    title='HTML Basics Quiz',
    quiz_type='topic',
    time_limit=15
)

# Create question
question = Question.objects.create(
    quiz=quiz,
    text='What does HTML stand for?',
    question_type='multiple_choice'
)

# Create options
Option.objects.create(question=question, text='Hyper Text Markup Language', is_correct=True)
Option.objects.create(question=question, text='High Tech Modern Language', is_correct=False)
Option.objects.create(question=question, text='Home Tool Markup Language', is_correct=False)

print("✓ Complete course structure created!")
print(f"Course: {course.title}")
print(f"Chapter: {chapter.title}")
print(f"Topic: {topic.title}")
print(f"Quiz: {quiz.title}")
```

---

## **EXAMPLE 2: Enroll Multiple Students**

```python
# Create 3 students
students = []
for i in range(1, 4):
    student = CustomUser.objects.create_user(
        username=f'student_{i}',
        email=f'student{i}@example.com',
        password='studentpass123',
        role='student',
        first_name=f'Student',
        last_name=f'{i}'
    )
    students.append(student)
    print(f"✓ Created student: {student.username}")

# Enroll all students in the course
for student in students:
    enrollment = Enrollment.objects.create(student=student, course=course)
    print(f"✓ Enrolled {student.username} in {course.title}")

print(f"\nTotal enrolled: {Enrollment.objects.filter(course=course).count()}")
```

---

## **EXAMPLE 3: Record Student Quiz Answers**

```python
from courses.models import StudentAnswer, Progress

# Get first student
student = students[0]

# Get the correct option for the question
correct_option = Option.objects.get(question=question, is_correct=True)

# Record the student's answer
answer = StudentAnswer.objects.create(
    student=student,
    question=question,
    selected_option=correct_option
)

# Create progress record
progress = Progress.objects.create(
    student=student,
    course=course,
    completed_lessons=1,
    score=100.0
)

print(f"✓ {student.username} answered quiz")
print(f"  Answer: {answer.selected_option.text}")
print(f"  Score: {progress.score}%")
```

---

## **EXAMPLE 4: Query and Display Data**

```python
# Display all courses with student count
from django.db.models import Count

courses = Course.objects.annotate(enrollment_count=Count('enrollment'))

print("\n📚 All Courses:")
print("="*60)
for course in courses:
    print(f"Course: {course.title}")
    print(f"  Instructor: {course.instructor.username}")
    print(f"  Students enrolled: {course.enrollment_count}")
    print(f"  Chapters: {course.chapters.count()}")
    print()
```

---

## **EXAMPLE 5: Display Course Hierarchy**

```python
# Get a course and show its full structure
course = Course.objects.first()

print(f"\n📚 COURSE STRUCTURE: {course.title}")
print("="*60)

for chapter in course.chapters.all():
    print(f"\n  📖 {chapter.title}")

    # Show topics
    for topic in chapter.topics.all():
        print(f"     🎯 {topic.title}")

        # Show quizzes in topic
        for quiz in topic.quizzes.all():
            q_count = quiz.question_set.count()
            print(f"        📋 {quiz.title} ({q_count} questions)")

    # Show chapter quizzes
    for quiz in chapter.quizzes.all():
        q_count = quiz.question_set.count()
        print(f"        📋 {quiz.title} ({q_count} questions)")
```

---

## **EXAMPLE 6: Student Dashboard Data**

```python
# Get a student and show their dashboard info
student = CustomUser.objects.filter(role='student').first()

from courses.models import Enrollment, Progress, StudentAnswer

print(f"\n👤 STUDENT DASHBOARD: {student.username}")
print("="*60)

# Enrolled courses
enrollments = Enrollment.objects.filter(student=student)
print(f"\n📚 Enrolled in {enrollments.count()} course(s):")

for enrollment in enrollments:
    course = enrollment.course

    # Get progress
    try:
        progress = Progress.objects.get(student=student, course=course)
        print(f"  - {course.title}")
        print(f"    Score: {progress.score}%")
        print(f"    Completed Lessons: {progress.completed_lessons}")
    except Progress.DoesNotExist:
        print(f"  - {course.title} (No progress yet)")

# Quiz attempts
attempts = StudentAnswer.objects.filter(student=student).count()
print(f"\n📋 Quiz Attempts: {attempts}")

# Certificates (score >= 80)
certificates = Progress.objects.filter(student=student, score__gte=80).count()
print(f"🏆 Certificates Earned: {certificates}")
```

---

## **EXAMPLE 7: Update Student Progress**

```python
from django.db.models import F

# Get student and course
student = students[0]
course = Course.objects.first()

# Get or create progress
progress, created = Progress.objects.get_or_create(
    student=student,
    course=course,
    defaults={'completed_lessons': 0, 'score': 0}
)

print(f"\nBefore update: Score={progress.score}%, Lessons={progress.completed_lessons}")

# Update score
progress.score = 92.5
progress.completed_lessons = 5
progress.save()

print(f"After update: Score={progress.score}%, Lessons={progress.completed_lessons}")

# Alternative: Using F() for increment
Progress.objects.filter(student=student, course=course).update(
    completed_lessons=F('completed_lessons') + 1
)

progress.refresh_from_db()
print(f"After increment: Lessons={progress.completed_lessons}")
```

---

## **EXAMPLE 8: Filter and Search**

```python
# Search by username
user = CustomUser.objects.get(username='student_1')
print(f"Found user: {user.username}")

# Search by role
students = CustomUser.objects.filter(role='student')
print(f"\nTotal students: {students.count()}")

# Search by email (case-insensitive)
user = CustomUser.objects.filter(email__icontains='student').first()
print(f"Found: {user.email}")

# Search by name
user = CustomUser.objects.filter(first_name__icontains='Student').first()
print(f"Found: {user.first_name} {user.last_name}")

# Filter courses by category
prog_courses = Course.objects.filter(category='programming')
print(f"\nProgramming courses: {prog_courses.count()}")

# Complex filter (AND)
advanced = CustomUser.objects.filter(role='student', is_active=True)
print(f"Active students: {advanced.count()}")

# Complex filter (OR)
from django.db.models import Q
users = CustomUser.objects.filter(Q(role='student') | Q(role='instructor'))
print(f"Students or Instructors: {users.count()}")
```

---

## **EXAMPLE 9: Bulk Operations**

```python
# Create 10 students at once (efficient)
students_to_create = [
    CustomUser(
        username=f'bulk_student_{i}',
        email=f'bulk{i}@example.com',
        role='student'
    )
    for i in range(1, 11)
]

CustomUser.objects.bulk_create(students_to_create)
print("✓ Bulk created 10 students")

# Check new count
total = CustomUser.objects.count()
print(f"Total users now: {total}")
```

---

## **EXAMPLE 10: Delete Operations**

```python
# Delete a single user
user_to_delete = CustomUser.objects.filter(username='bulk_student_1').first()
if user_to_delete:
    username = user_to_delete.username
    user_to_delete.delete()
    print(f"✓ Deleted user: {username}")

# Delete multiple records
deleted_count, _ = CustomUser.objects.filter(username__startswith='bulk_').delete()
print(f"✓ Deleted {deleted_count} bulk students")

# Verify
remaining = CustomUser.objects.count()
print(f"Remaining users: {remaining}")
```

---

## **EXAMPLE 11: Statistics and Aggregations**

```python
from django.db.models import Avg, Count, Max, Min

# Average score for all students
avg_score = Progress.objects.aggregate(avg=Avg('score'))
print(f"Average score across all students: {avg_score['avg']:.1f}%")

# Count students per course
from django.db.models import Count
courses_with_counts = Course.objects.annotate(
    student_count=Count('enrollment')
)

print("\nCourses with student counts:")
for course in courses_with_counts:
    print(f"  {course.title}: {course.student_count} students")

# Get courses with most students
top_course = courses_with_counts.order_by('-student_count').first()
print(f"\nMost popular: {top_course.title}")

# Count quizzes per course
courses_with_quizzes = Course.objects.annotate(
    quiz_count=Count('chapters__quizzes')
)

print("\nCourses with quiz counts:")
for course in courses_with_quizzes:
    print(f"  {course.title}: {course.quiz_count} quizzes")
```

---

## **EXAMPLE 12: Complex Queries - Advanced**

```python
# Get all students in a specific course with their progress
from django.db.models import Prefetch

course = Course.objects.first()

# Using select_related to reduce queries
enrollments = Enrollment.objects.filter(course=course).select_related('student')

print(f"\n📊 Students in {course.title}:")
print("="*60)

for enrollment in enrollments:
    student = enrollment.student

    # Get progress
    try:
        progress = Progress.objects.get(student=student, course=course)
        status = "✓ In Progress" if progress.score < 100 else "✓ Completed"
        print(f"{student.username:20} Score: {progress.score:5.1f}%  {status}")
    except Progress.DoesNotExist:
        print(f"{student.username:20} Score: --      ⏳ Not started")
```

---

## **EXAMPLE 13: Get or Create Pattern**

```python
# Try to get or create a user
user, created = CustomUser.objects.get_or_create(
    username='demo_user',
    defaults={
        'email': 'demo@example.com',
        'role': 'student'
    }
)

if created:
    user.set_password('password123')
    user.save()
    print(f"✓ New user created: {user.username}")
else:
    print(f"✓ User already exists: {user.username}")
```

---

## **EXAMPLE 14: Export Data to Dictionary**

```python
# Convert QuerySet to dictionaries (useful for JSON)
users_dict = list(CustomUser.objects.filter(role='student').values())
print("\nUsers as dictionaries:")
for user in users_dict[:3]:
    print(user)

# Select specific fields
course_data = Course.objects.values('id', 'title', 'category')
print("\nCourses (specific fields):")
for course in course_data:
    print(course)
```

---

## **TIPS & TRICKS**

```python
# Print SQL query (for debugging)
print(CustomUser.objects.filter(role='student').query)

# Count without loading into memory
count = CustomUser.objects.filter(role='student').count()

# Check if exists (more efficient than count())
exists = CustomUser.objects.filter(username='john').exists()

# Get latest record
latest_course = Course.objects.latest('created_at')

# Get oldest record
oldest_course = Course.objects.earliest('created_at')

# Reverse queryset
reversed_users = list(reversed(CustomUser.objects.all()))

# Get random record
from django.db.models.functions import Random
random_user = CustomUser.objects.order_by('?').first()
```

---

## **TESTING IN SHELL**

After running examples, verify data was created:

```python
# Count all records
print(f"Users: {CustomUser.objects.count()}")
print(f"Courses: {Course.objects.count()}")
print(f"Chapters: {Chapter.objects.count()}")
print(f"Topics: {Topic.objects.count()}")
print(f"Quizzes: {Quiz.objects.count()}")
print(f"Questions: {Question.objects.count()}")
print(f"Enrollments: {Enrollment.objects.count()}")
print(f"Progress: {Progress.objects.count()}")
print(f"Answers: {StudentAnswer.objects.count()}")
```

---

**Happy Coding! 🚀**

Copy-paste these examples into your Django shell and experiment!
