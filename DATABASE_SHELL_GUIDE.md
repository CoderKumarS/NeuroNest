# 🗄️ Django Database Management from Shell

## **Step 1: Access Django Shell**

Open PowerShell and navigate to your project directory:

```powershell
# Navigate to project
cd "d:\Django Project"

# Activate virtual environment
.\venv\Scripts\activate

# Start Django shell
python manage.py shell
```

You should see:

```
Python 3.x.x (default, ...)
Type 'help', 'copyright', 'credits' or 'license' for more information.
(InteractiveConsole)
>>>
```

---

## **Step 2: Import Models**

Before you can work with database tables, import the models:

```python
# Import all models
from users.models import CustomUser
from courses.models import Course, Chapter, Topic, Quiz, Question, Option, Enrollment, Progress, StudentAnswer, TopicCompletion
from tutor.models import ChatSession, ChatMessage, TutorRequest, AIConfiguration

# Or import get_user_model for flexibility
from django.contrib.auth import get_user_model
User = get_user_model()  # Returns CustomUser
```

---

## **CREATE - Add New Records to Database**

### **1. Create a New User (Student)**

```python
# Create student user
student = CustomUser.objects.create_user(
    username='john_student',
    email='john@example.com',
    password='securepassword123',
    role='student',
    first_name='John',
    last_name='Doe'
)

print(student)  # Output: john_student (student)
print(student.id)  # Output: 1 (auto-generated)
print(student.email)  # Output: john@example.com
```

### **2. Create an Instructor User**

```python
# Create instructor
instructor = CustomUser.objects.create_user(
    username='prof_smith',
    email='prof.smith@example.com',
    password='instructorpass123',
    role='instructor',
    first_name='Professor',
    last_name='Smith'
)

print(instructor)  # Output: prof_smith (instructor)
```

### **3. Create a Course**

```python
# Create a course (requires instructor)
course = Course.objects.create(
    title='Python Basics',
    description='Learn Python fundamentals from scratch',
    instructor=instructor,  # Link to instructor
    category='programming'
)

print(f"Course created: {course.title} (ID: {course.id})")
# Output: Course created: Python Basics (ID: 1)
```

### **4. Create a Chapter**

```python
# Create a chapter (requires course)
chapter = Chapter.objects.create(
    course=course,
    title='Chapter 1: Introduction to Python',
    description='Get started with Python basics',
    order=1
)

print(f"Chapter created: {chapter.title}")
# Output: Chapter created: Chapter 1: Introduction to Python
```

### **5. Create a Topic**

```python
# Create a topic (requires chapter)
topic = Topic.objects.create(
    chapter=chapter,
    title='Variables and Data Types',
    description='Learn about Python variables',
    notes='Variables are containers for storing data values...',
    youtube_video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    order=1
)

print(f"Topic created: {topic.title}")
# Output: Topic created: Variables and Data Types
print(topic.get_youtube_embed_url())  # Output: https://www.youtube.com/embed/dQw4w9WgXcQ
```

### **6. Create a Quiz**

```python
# Create a topic-level quiz
quiz = Quiz.objects.create(
    topic=topic,
    title='Variables Quiz',
    quiz_type='topic',
    time_limit=15
)

print(f"Quiz created: {quiz.title}")
# Output: Quiz created: Variables Quiz
```

### **7. Create Quiz Questions and Options**

```python
# Create a question
question = Question.objects.create(
    quiz=quiz,
    text='What is a variable in Python?',
    question_type='multiple_choice'
)

# Create options
Option.objects.create(
    question=question,
    text='A container for storing data values',
    is_correct=True
)

Option.objects.create(
    question=question,
    text='A function in Python',
    is_correct=False
)

Option.objects.create(
    question=question,
    text='A type of loop',
    is_correct=False
)

print(f"Question created with {question.option_set.count()} options")
# Output: Question created with 3 options
```

### **8. Enroll Student in Course**

```python
# Enroll student
enrollment = Enrollment.objects.create(
    student=student,
    course=course
)

print(f"{student.username} enrolled in {course.title}")
# Output: john_student enrolled in Python Basics
```

### **9. Create Progress Record**

```python
# Create progress record
progress = Progress.objects.create(
    student=student,
    course=course,
    completed_lessons=5,
    score=85.5
)

print(f"Progress: {progress.student.username} - Score: {progress.score}%")
# Output: Progress: john_student - Score: 85.5%
```

### **10. Record Student Answer (Quiz Submission)**

```python
# Get the correct option
correct_option = Option.objects.get(is_correct=True, question=question)

# Create student answer
answer = StudentAnswer.objects.create(
    student=student,
    question=question,
    selected_option=correct_option
)

print(f"Answer recorded for {question.text}")
# Output: Answer recorded for What is a variable in Python?
```

---

## **READ - Query Data from Database**

### **1. Get All Records**

```python
# Get all users
all_users = CustomUser.objects.all()
print(f"Total users: {all_users.count()}")
# Output: Total users: 2

# Get all courses
all_courses = Course.objects.all()
for course in all_courses:
    print(f"- {course.title} by {course.instructor.username}")
# Output:
# - Python Basics by prof_smith
```

### **2. Get Single Record by ID**

```python
# Get user by ID
user = CustomUser.objects.get(id=1)
print(f"User: {user.username} ({user.role})")
# Output: User: john_student (student)

# Get course by ID
course = Course.objects.get(id=1)
print(f"Course: {course.title}")
# Output: Course: Python Basics
```

### **3. Get Records by Filter**

```python
# Get all students
students = CustomUser.objects.filter(role='student')
for student in students:
    print(f"- {student.username}")
# Output: - john_student

# Get all instructors
instructors = CustomUser.objects.filter(role='instructor')
print(f"Total instructors: {instructors.count()}")
# Output: Total instructors: 1

# Get courses by category
programming_courses = Course.objects.filter(category='programming')
print(f"Programming courses: {programming_courses.count()}")
# Output: Programming courses: 1
```

### **4. Get Records by First Match (filter + first())**

```python
# Get first student
first_student = CustomUser.objects.filter(role='student').first()
print(f"First student: {first_student.username}")
# Output: First student: john_student
```

### **5. Query with Relationships (Foreign Keys)**

```python
# Get all courses by an instructor
instructor = CustomUser.objects.get(username='prof_smith')
courses = Course.objects.filter(instructor=instructor)
print(f"Courses by {instructor.username}: {courses.count()}")
# Output: Courses by prof_smith: 1

# Get all chapters in a course
course = Course.objects.get(id=1)
chapters = course.chapters.all()
for chapter in chapters:
    print(f"- {chapter.title} (Order: {chapter.order})")
# Output: - Chapter 1: Introduction to Python (Order: 1)

# Get all topics in a chapter
chapter = Chapter.objects.get(id=1)
topics = chapter.topics.all()
for topic in topics:
    print(f"- {topic.title}")
# Output: - Variables and Data Types
```

### **6. Get Enrollments**

```python
# Get all courses a student is enrolled in
student = CustomUser.objects.get(username='john_student')
enrollments = Enrollment.objects.filter(student=student)
for enrollment in enrollments:
    print(f"Enrolled in: {enrollment.course.title}")
# Output: Enrolled in: Python Basics

# Get all students enrolled in a course
course = Course.objects.get(id=1)
enrollments = Enrollment.objects.filter(course=course)
print(f"Total students in {course.title}: {enrollments.count()}")
# Output: Total students in Python Basics: 1

# Get student list
students_in_course = [e.student for e in enrollments]
for student in students_in_course:
    print(f"- {student.username}")
# Output: - john_student
```

### **7. Get Progress**

```python
# Get a student's progress in a course
student = CustomUser.objects.get(username='john_student')
course = Course.objects.get(id=1)

progress = Progress.objects.get(student=student, course=course)
print(f"Score: {progress.score}%")
print(f"Completed Lessons: {progress.completed_lessons}")
# Output:
# Score: 85.5%
# Completed Lessons: 5
```

### **8. Count Records**

```python
# Count all users
total_users = CustomUser.objects.count()
print(f"Total users: {total_users}")

# Count students
student_count = CustomUser.objects.filter(role='student').count()
print(f"Total students: {student_count}")

# Count all courses
total_courses = Course.objects.count()
print(f"Total courses: {total_courses}")
```

### **9. Advanced Queries**

```python
# Get courses with their enrollment count
from django.db.models import Count
courses_with_count = Course.objects.annotate(
    enrollment_count=Count('enrollment')
)
for course in courses_with_count:
    print(f"{course.title}: {course.enrollment_count} students")
# Output: Python Basics: 1 students

# Get students sorted by name
students = CustomUser.objects.filter(role='student').order_by('first_name')
for student in students:
    print(f"- {student.first_name} {student.last_name}")
# Output: - John Doe
```

---

## **UPDATE - Modify Existing Records**

### **1. Update a Single Field**

```python
# Get user
user = CustomUser.objects.get(username='john_student')

# Update email
user.email = 'newemail@example.com'
user.save()

print(f"Updated email: {user.email}")
# Output: Updated email: newemail@example.com
```

### **2. Update Multiple Fields**

```python
# Get course
course = Course.objects.get(id=1)

# Update multiple fields
course.title = 'Advanced Python'
course.description = 'Learn advanced Python concepts'
course.category = 'programming'
course.save()

print(f"Updated course: {course.title}")
# Output: Updated course: Advanced Python
```

### **3. Update Using filter() and update()**

```python
# Update all students' role (not recommended, just for demo)
CustomUser.objects.filter(role='student').update(is_active=True)

# Verify update
students = CustomUser.objects.filter(role='student')
for student in students:
    print(f"{student.username}: is_active={student.is_active}")
# Output: john_student: is_active=True
```

### **4. Update Progress**

```python
# Get progress
progress = Progress.objects.get(student__username='john_student', course__id=1)

# Update score and completed lessons
progress.score = 92.5
progress.completed_lessons = 8
progress.save()

print(f"Updated progress: Score={progress.score}%, Lessons={progress.completed_lessons}")
# Output: Updated progress: Score=92.5%, Lessons=8
```

### **5. Update with Field Arithmetic**

```python
from django.db.models import F

# Increment completed lessons by 1
Progress.objects.filter(student__username='john_student').update(
    completed_lessons=F('completed_lessons') + 1
)

# Verify
progress = Progress.objects.get(student__username='john_student', course__id=1)
print(f"New completed lessons: {progress.completed_lessons}")
# Output: New completed lessons: 9
```

### **6. Change User Password**

```python
# Get user
user = CustomUser.objects.get(username='john_student')

# Set new password (hashed automatically)
user.set_password('newpassword123')
user.save()

print("Password updated successfully!")
```

### **7. Update User Role**

```python
# Get user
user = CustomUser.objects.get(username='john_student')

# Change role
user.role = 'instructor'
user.save()

print(f"New role: {user.role}")
# Output: New role: instructor
```

---

## **DELETE - Remove Records from Database**

### **1. Delete Single Record**

```python
# Get and delete a user
user = CustomUser.objects.get(username='john_student')
username = user.username
user.delete()

print(f"Deleted user: {username}")
# Output: Deleted user: john_student
```

### **2. Delete Multiple Records**

```python
# Delete all students
CustomUser.objects.filter(role='student').delete()

# Verify
student_count = CustomUser.objects.filter(role='student').count()
print(f"Remaining students: {student_count}")
# Output: Remaining students: 0
```

### **3. Delete Related Records**

```python
# Delete a course (this will cascade delete chapters, topics, etc.)
course = Course.objects.get(id=1)
course_title = course.title
course.delete()

print(f"Deleted course: {course_title} and all related data")
# Output: Deleted course: Python Basics and all related data
```

### **4. Delete Specific Quiz Attempt**

```python
# Get and delete a student answer
answer = StudentAnswer.objects.get(id=1)
answer.delete()

print("Quiz answer deleted")
```

### **5. Delete Enrollment**

```python
# Delete enrollment (student unenrolls from course)
student = CustomUser.objects.get(username='john_student')
course = Course.objects.get(id=1)

enrollment = Enrollment.objects.get(student=student, course=course)
enrollment.delete()

print(f"{student.username} unenrolled from {course.title}")
```

---

## **Useful Query Patterns**

### **Check if Record Exists**

```python
# Check if user exists
exists = CustomUser.objects.filter(username='john_student').exists()
print(f"User exists: {exists}")
# Output: User exists: True

# Using try-except
try:
    user = CustomUser.objects.get(username='nonexistent')
except CustomUser.DoesNotExist:
    print("User not found")
# Output: User not found
```

### **Get or Create**

```python
# Get existing or create new
user, created = CustomUser.objects.get_or_create(
    username='jane_student',
    defaults={
        'email': 'jane@example.com',
        'role': 'student'
    }
)

if created:
    user.set_password('password123')
    user.save()
    print("New user created")
else:
    print("User already exists")
```

### **Bulk Create (More Efficient)**

```python
# Create multiple users at once (faster than individual creates)
users = [
    CustomUser(
        username=f'student{i}',
        email=f'student{i}@example.com',
        role='student'
    )
    for i in range(1, 6)
]

CustomUser.objects.bulk_create(users)
print("5 users created in bulk")
```

### **Distinct Records**

```python
# Get distinct instructors
instructors = Course.objects.values_list('instructor', flat=True).distinct()
for instructor_id in instructors:
    instructor = CustomUser.objects.get(id=instructor_id)
    print(f"- {instructor.username}")
```

### **Reverse Relations (Accessing related objects)**

```python
# Get instructor and access their courses
instructor = CustomUser.objects.get(username='prof_smith')

# Using the related_name from ForeignKey
instructor_courses = instructor.course_set.all()
for course in instructor_courses:
    print(f"- {course.title}")
```

---

## **Exit Django Shell**

```python
# Type exit() to leave shell
exit()
```

Or press `Ctrl + Z` then `Enter` on Windows.

---

## **Common Errors and Solutions**

| Error                                                 | Cause                           | Solution                                             |
| ----------------------------------------------------- | ------------------------------- | ---------------------------------------------------- |
| `CustomUser matching query does not exist`            | Record not found                | Use `.filter()` with `.first()` or `.exists()` first |
| `Cannot assign "X" to "Y"`                            | Wrong type for foreign key      | Ensure you're assigning model instance, not ID       |
| `IntegrityError: UNIQUE constraint failed`            | Duplicate unique field          | Check if record already exists                       |
| `AttributeError: 'QuerySet' has no attribute 'email'` | Using QuerySet as single object | Use `.get()` or `.first()` instead of `.filter()`    |

---

## **Quick Reference**

```python
# IMPORT
from users.models import CustomUser
from courses.models import Course, Chapter, Topic, Quiz, Question, Option, Enrollment, Progress, StudentAnswer

# CREATE
user = CustomUser.objects.create_user(username='john', email='john@example.com', password='pass', role='student')

# READ
users = CustomUser.objects.all()
user = CustomUser.objects.get(id=1)
users = CustomUser.objects.filter(role='student')

# UPDATE
user.email = 'new@example.com'
user.save()

# DELETE
user.delete()

# COUNT
count = CustomUser.objects.count()

# CHECK EXISTS
exists = CustomUser.objects.filter(username='john').exists()
```

---

This guide covers all CRUD operations you'll need for managing your NeuroNest database! 🎓✨
