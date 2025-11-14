# 🎓 DJANGO SHELL - STEP-BY-STEP TUTORIAL

## **Tutorial 1: Your First Database Entry**

### **Step 1: Open Django Shell**

```powershell
# Open PowerShell
cd "d:\Django Project"

# Activate virtual environment
.\venv\Scripts\activate

# Start Django shell
python manage.py shell
```

You should see:

```
Python 3.x.x ...
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```

### **Step 2: Import the Model**

```python
from users.models import CustomUser
```

**What this does:** Loads the CustomUser model so you can create users.

### **Step 3: Create Your First User**

```python
user = CustomUser.objects.create_user(
    username='alice',
    email='alice@example.com',
    password='alice123',
    role='student'
)
```

**What this does:**

- Creates a new user record in the database
- Stores it in the `user` variable
- Password is automatically hashed (encrypted)

### **Step 4: Verify Creation**

```python
print(user)
```

**Expected output:**

```
alice (student)
```

### **Step 5: Check the Details**

```python
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"Role: {user.role}")
print(f"ID: {user.id}")
```

**Expected output:**

```
Username: alice
Email: alice@example.com
Role: student
ID: 1
```

**🎉 Success! You created your first database record!**

---

## **Tutorial 2: Create a Complete Course**

### **Step 1: Create Instructor**

```python
from users.models import CustomUser
from courses.models import Course, Chapter, Topic

# Create instructor
instructor = CustomUser.objects.create_user(
    username='prof_brown',
    email='prof_brown@example.com',
    password='profpass123',
    role='instructor',
    first_name='Professor',
    last_name='Brown'
)

print(f"✓ Created instructor: {instructor.username}")
```

### **Step 2: Create Course**

```python
# Create course
course = Course.objects.create(
    title='Web Development 101',
    description='Learn HTML, CSS, and JavaScript',
    instructor=instructor,
    category='programming'
)

print(f"✓ Created course: {course.title}")
print(f"  Instructor: {course.instructor.username}")
```

### **Step 3: Create Chapter**

```python
# Create chapter
chapter = Chapter.objects.create(
    course=course,
    title='Chapter 1: HTML Basics',
    description='Learn HTML fundamentals',
    order=1
)

print(f"✓ Created chapter: {chapter.title}")
```

### **Step 4: Create Topic**

```python
# Create topic
topic = Topic.objects.create(
    chapter=chapter,
    title='HTML Tags',
    description='Understanding HTML tags',
    notes='HTML tags are used to structure web pages...',
    order=1
)

print(f"✓ Created topic: {topic.title}")
```

### **Step 5: View the Hierarchy**

```python
# Show what we created
print("\n📚 COURSE STRUCTURE")
print("=" * 50)
print(f"Course: {course.title}")
print(f"└─ Chapter: {chapter.title}")
print(f"   └─ Topic: {topic.title}")
```

---

## **Tutorial 3: Enroll a Student and Track Progress**

### **Step 1: Get or Create Student**

```python
# Get the student we created earlier
student = CustomUser.objects.get(username='alice')

# Or create a new one
# student = CustomUser.objects.create_user(
#     username='bob',
#     email='bob@example.com',
#     password='bob123',
#     role='student'
# )

print(f"✓ Student: {student.username}")
```

### **Step 2: Enroll Student in Course**

```python
from courses.models import Enrollment

enrollment = Enrollment.objects.create(
    student=student,
    course=course
)

print(f"✓ Enrolled {student.username} in {course.title}")
```

### **Step 3: Create Progress Record**

```python
from courses.models import Progress

progress = Progress.objects.create(
    student=student,
    course=course,
    completed_lessons=2,
    score=85.5
)

print(f"✓ Progress created:")
print(f"  Score: {progress.score}%")
print(f"  Lessons completed: {progress.completed_lessons}")
```

### **Step 4: Update Progress**

```python
# Update the score
progress.score = 92.0
progress.completed_lessons = 5
progress.save()

print(f"✓ Progress updated:")
print(f"  New Score: {progress.score}%")
print(f"  New Lessons: {progress.completed_lessons}")
```

### **Step 5: Check Enrollment**

```python
# Check if student is enrolled
is_enrolled = Enrollment.objects.filter(
    student=student,
    course=course
).exists()

print(f"Student enrolled: {is_enrolled}")
```

---

## **Tutorial 4: Query the Database**

### **Step 1: Get All Records**

```python
# Get all users
all_users = CustomUser.objects.all()
print(f"Total users: {all_users.count()}")

# Get all courses
all_courses = Course.objects.all()
print(f"Total courses: {all_courses.count()}")
```

### **Step 2: Filter by Role**

```python
# Get all students
students = CustomUser.objects.filter(role='student')
print(f"Total students: {students.count()}")

# List all students
for student in students:
    print(f"  - {student.username} ({student.email})")
```

### **Step 3: Filter by Course**

```python
# Get all students in a course
course = Course.objects.first()
enrollments = Enrollment.objects.filter(course=course)

print(f"\nStudents in '{course.title}':")
for enrollment in enrollments:
    student = enrollment.student
    print(f"  - {student.username}")
```

### **Step 4: Get Student Dashboard**

```python
# Get a student
student = CustomUser.objects.get(username='alice')

# Get their enrollments
enrollments = Enrollment.objects.filter(student=student)

print(f"\n📊 Dashboard for {student.username}")
print("=" * 50)

for enrollment in enrollments:
    course = enrollment.course

    # Get progress
    try:
        progress = Progress.objects.get(student=student, course=course)
        print(f"\nCourse: {course.title}")
        print(f"  Score: {progress.score}%")
        print(f"  Lessons: {progress.completed_lessons}")
    except Progress.DoesNotExist:
        print(f"\nCourse: {course.title}")
        print(f"  Status: Not started")
```

---

## **Tutorial 5: Create Quiz and Questions**

### **Step 1: Create Quiz**

```python
from courses.models import Quiz

quiz = Quiz.objects.create(
    topic=topic,
    title='HTML Basics Quiz',
    quiz_type='topic',
    time_limit=15
)

print(f"✓ Created quiz: {quiz.title}")
```

### **Step 2: Create Question**

```python
from courses.models import Question

question = Question.objects.create(
    quiz=quiz,
    text='What does HTML stand for?',
    question_type='multiple_choice'
)

print(f"✓ Created question: {question.text}")
```

### **Step 3: Create Options**

```python
from courses.models import Option

# Correct option
Option.objects.create(
    question=question,
    text='HyperText Markup Language',
    is_correct=True
)

# Incorrect options
Option.objects.create(
    question=question,
    text='High Tech Modern Language',
    is_correct=False
)

Option.objects.create(
    question=question,
    text='Home Tool Markup Language',
    is_correct=False
)

print(f"✓ Created 3 options for the question")
```

### **Step 4: View Quiz Structure**

```python
print(f"\n📋 QUIZ STRUCTURE")
print("=" * 50)
print(f"Quiz: {quiz.title}")
print(f"Time: {quiz.time_limit} minutes")
print(f"\nQuestions: {quiz.question_set.count()}")

for q in quiz.question_set.all():
    print(f"\n  Q: {q.text}")
    for option in q.option_set.all():
        status = "✓ Correct" if option.is_correct else ""
        print(f"     - {option.text} {status}")
```

---

## **Tutorial 6: Record Student Answers**

### **Step 1: Get Question and Correct Option**

```python
from courses.models import StudentAnswer, Option

# Get the question and student
question = Question.objects.first()
student = CustomUser.objects.get(username='alice')

# Get the correct option
correct_option = Option.objects.get(question=question, is_correct=True)

print(f"Question: {question.text}")
print(f"Correct answer: {correct_option.text}")
```

### **Step 2: Record Student Answer**

```python
# Student selects the correct option
answer = StudentAnswer.objects.create(
    student=student,
    question=question,
    selected_option=correct_option
)

print(f"✓ Recorded answer:")
print(f"  Student: {student.username}")
print(f"  Selected: {answer.selected_option.text}")
print(f"  Is correct: {answer.selected_option.is_correct}")
```

### **Step 3: Record Wrong Answer**

```python
# Get a wrong option
wrong_option = Option.objects.filter(
    question=question,
    is_correct=False
).first()

# Another student answers wrong
another_student = CustomUser.objects.filter(
    role='student'
).exclude(username='alice').first()

if another_student and wrong_option:
    wrong_answer = StudentAnswer.objects.create(
        student=another_student,
        question=question,
        selected_option=wrong_option
    )
    print(f"✓ Recorded wrong answer:")
    print(f"  Student: {another_student.username}")
    print(f"  Selected: {wrong_answer.selected_option.text}")
```

---

## **Tutorial 7: Update Data**

### **Step 1: Update User Information**

```python
# Get a user
user = CustomUser.objects.get(username='alice')

# Update email
user.email = 'alice.new@example.com'
user.save()

print(f"✓ Updated email: {user.email}")
```

### **Step 2: Change Password**

```python
# Get user
user = CustomUser.objects.get(username='alice')

# Set new password (hashed automatically)
user.set_password('newalicepass123')
user.save()

print(f"✓ Password updated for {user.username}")
```

### **Step 3: Update Multiple Records**

```python
# Mark all students as active
updated_count = CustomUser.objects.filter(
    role='student'
).update(is_active=True)

print(f"✓ Updated {updated_count} students to active")
```

---

## **Tutorial 8: Delete Data**

### **Step 1: Delete Single Record**

```python
# Get a user
user = CustomUser.objects.filter(username='test_user').first()

if user:
    username = user.username
    user.delete()
    print(f"✓ Deleted user: {username}")
else:
    print("User not found")
```

### **Step 2: Delete Multiple Records**

```python
# Delete all students (be careful!)
# count = CustomUser.objects.filter(role='student').delete()
# print(f"Deleted {count[0]} students")

# Better: Delete one specific user
user_to_delete = CustomUser.objects.filter(username='alice').first()
if user_to_delete:
    user_to_delete.delete()
    print("✓ User deleted")
```

### **Step 3: Delete Related Records**

```python
# Get a course
course = Course.objects.filter(title='Web Development 101').first()

if course:
    # Deleting course will cascade delete:
    # - Chapters
    # - Topics
    # - Quizzes
    # - Questions
    # - Options
    course.delete()
    print(f"✓ Deleted course and all related data")
```

---

## **Tutorial 9: Use Populate Script**

### **Step 1: Run the Script**

```python
# In Django shell, run:
exec(open('populate_db.py').read())
```

### **What it does:**

- Creates 2 instructors
- Creates 2 students
- Creates 2 courses
- Creates chapters, topics, quizzes
- Creates questions with options
- Enrolls students
- Creates progress records
- Records quiz answers

### **Step 2: Verify Data**

```python
# Check what was created
print(f"Users: {CustomUser.objects.count()}")
print(f"Courses: {Course.objects.count()}")
print(f"Chapters: {Chapter.objects.count()}")
print(f"Topics: {Topic.objects.count()}")
```

---

## **Tutorial 10: Write Your Own Script**

### **Create a file called `my_test.py`:**

```python
from users.models import CustomUser
from courses.models import Course, Chapter, Topic, Enrollment, Progress

# Create instructor
instructor = CustomUser.objects.create_user(
    username='my_instructor',
    email='instructor@test.com',
    password='pass123',
    role='instructor'
)

# Create course
course = Course.objects.create(
    title='My Test Course',
    description='Testing course creation',
    instructor=instructor,
    category='programming'
)

# Create students
for i in range(3):
    student = CustomUser.objects.create_user(
        username=f'student_{i}',
        email=f'student{i}@test.com',
        password='pass123',
        role='student'
    )

    # Enroll in course
    Enrollment.objects.create(student=student, course=course)

    # Create progress
    Progress.objects.create(
        student=student,
        course=course,
        completed_lessons=5,
        score=80 + (i * 5)
    )

print("✓ Test data created!")
```

### **Run it in shell:**

```python
exec(open('my_test.py').read())
```

---

## **Common Tasks Quick Reference**

```python
# Count total users
CustomUser.objects.count()

# Count students only
CustomUser.objects.filter(role='student').count()

# Get specific user by username
user = CustomUser.objects.get(username='alice')

# Check if user exists
CustomUser.objects.filter(username='alice').exists()

# Get all courses by instructor
courses = Course.objects.filter(instructor__username='prof_brown')

# Get students in a course
students = CustomUser.objects.filter(enrollment__course_id=1)

# Get student's courses
courses = Course.objects.filter(enrollment__student__username='alice')

# Get student's progress
progress = Progress.objects.filter(student__username='alice')

# Update all students' status
CustomUser.objects.filter(role='student').update(is_active=True)

# Delete a course
Course.objects.get(id=1).delete()
```

---

## **Troubleshooting**

### **"Object does not exist"**

```python
# Use filter().first() instead
user = CustomUser.objects.filter(username='alice').first()
# Now check if it exists
if user:
    print(user)
```

### **"Cannot assign"**

```python
# Make sure you're assigning the object, not the ID
course.instructor = instructor  # ✓ Correct
# course.instructor = 1  # ✗ Wrong
```

### **Forgotten Password**

```python
# Just set a new one
user = CustomUser.objects.get(username='alice')
user.set_password('newpass123')
user.save()
```

### **Want to undo something?**

```python
# Just delete and recreate
user.delete()

# Now create again
user = CustomUser.objects.create_user(
    username='alice',
    email='alice@example.com',
    password='pass123',
    role='student'
)
```

---

## **Exit Shell**

```python
exit()
# or Ctrl+Z then Enter
```

---

**🎉 You're now a Django shell expert!**

Try these tutorials one by one and experiment with your own queries!
