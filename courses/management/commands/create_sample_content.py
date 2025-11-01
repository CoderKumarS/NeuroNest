from django.core.management.base import BaseCommand
from courses.models import Course, Chapter, Topic, Quiz, Question, Option
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample chapters and topics for existing courses'

    def handle(self, *args, **options):
        # Get existing courses
        courses = Course.objects.all()
        
        if not courses.exists():
            self.stdout.write(self.style.ERROR('No courses found. Please run create_sample_courses first.'))
            return

        for course in courses:
            self.stdout.write(f'Adding content to course: {course.title}')
            
            # Create chapters based on course type
            if 'Python' in course.title:
                self.create_python_content(course)
            elif 'Web Development' in course.title:
                self.create_web_dev_content(course)
            elif 'Data Science' in course.title:
                self.create_data_science_content(course)
            elif 'JavaScript' in course.title:
                self.create_javascript_content(course)
            elif 'Marketing' in course.title:
                self.create_marketing_content(course)

        self.stdout.write(self.style.SUCCESS('Successfully created sample content!'))

    def create_python_content(self, course):
        # Chapter 1: Python Basics
        chapter1 = Chapter.objects.create(
            course=course,
            title="Python Fundamentals",
            description="Learn the basics of Python programming language",
            order=1
        )
        
        Topic.objects.create(
            chapter=chapter1,
            title="Introduction to Python",
            description="What is Python and why use it?",
            order=1,
            youtube_video_url="https://www.youtube.com/watch?v=Y8Tko2YC5hA",
            notes="""
Python is a high-level, interpreted programming language known for its simplicity and readability.

Key features of Python:
- Easy to learn and use
- Extensive standard library
- Cross-platform compatibility
- Large community support
- Versatile (web development, data science, AI, etc.)

Python is used by companies like Google, Netflix, Instagram, and many more.
            """,
            extra_info="Python was created by Guido van Rossum and first released in 1991."
        )
        
        Topic.objects.create(
            chapter=chapter1,
            title="Variables and Data Types",
            description="Understanding Python variables and basic data types",
            order=2,
            notes="""
Variables in Python:
- No need to declare variable types
- Dynamic typing
- Case-sensitive names

Basic Data Types:
1. Numbers (int, float, complex)
2. Strings (str)
3. Booleans (bool)
4. Lists (list)
5. Tuples (tuple)
6. Dictionaries (dict)

Examples:
```python
name = "John"        # String
age = 25            # Integer
height = 5.9        # Float
is_student = True   # Boolean
```
            """,
            extra_info="Python uses duck typing: 'If it walks like a duck and quacks like a duck, then it must be a duck.'"
        )

        # Chapter 2: Control Structures
        chapter2 = Chapter.objects.create(
            course=course,
            title="Control Flow",
            description="Learn about loops, conditions, and control structures",
            order=2
        )
        
        Topic.objects.create(
            chapter=chapter2,
            title="If Statements and Conditions",
            description="Making decisions in your code",
            order=1,
            notes="""
Conditional statements allow your program to make decisions:

Basic if statement:
```python
if condition:
    # code to execute
```

If-else statement:
```python
if condition:
    # code if true
else:
    # code if false
```

If-elif-else statement:
```python
if condition1:
    # code if condition1 is true
elif condition2:
    # code if condition2 is true
else:
    # code if all conditions are false
```

Comparison operators: ==, !=, <, >, <=, >=
Logical operators: and, or, not
            """
        )

    def create_web_dev_content(self, course):
        # Chapter 1: HTML Basics
        chapter1 = Chapter.objects.create(
            course=course,
            title="HTML Fundamentals",
            description="Learn the structure of web pages with HTML",
            order=1
        )
        
        Topic.objects.create(
            chapter=chapter1,
            title="Introduction to HTML",
            description="What is HTML and how does it work?",
            order=1,
            youtube_video_url="https://www.youtube.com/watch?v=UB1O30fR-EE",
            notes="""
HTML (HyperText Markup Language) is the standard markup language for creating web pages.

Key concepts:
- Elements and tags
- Attributes
- Document structure
- Semantic markup

Basic HTML structure:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Page Title</title>
</head>
<body>
    <h1>My First Heading</h1>
    <p>My first paragraph.</p>
</body>
</html>
```
            """,
            extra_info="HTML was first created by Tim Berners-Lee in 1990."
        )

        # Chapter 2: CSS Styling
        chapter2 = Chapter.objects.create(
            course=course,
            title="CSS Styling",
            description="Make your web pages beautiful with CSS",
            order=2
        )
        
        Topic.objects.create(
            chapter=chapter2,
            title="CSS Basics",
            description="Introduction to Cascading Style Sheets",
            order=1,
            notes="""
CSS (Cascading Style Sheets) is used to style HTML elements.

CSS Syntax:
```css
selector {
    property: value;
}
```

Common selectors:
- Element selector: p { }
- Class selector: .classname { }
- ID selector: #idname { }

Common properties:
- color: text color
- background-color: background color
- font-size: text size
- margin: outer spacing
- padding: inner spacing
            """
        )

    def create_data_science_content(self, course):
        chapter1 = Chapter.objects.create(
            course=course,
            title="Introduction to Data Science",
            description="Understanding the field of data science",
            order=1
        )
        
        Topic.objects.create(
            chapter=chapter1,
            title="What is Data Science?",
            description="Overview of data science and its applications",
            order=1,
            notes="""
Data Science is an interdisciplinary field that uses scientific methods, processes, algorithms, and systems to extract knowledge and insights from structured and unstructured data.

Key components:
1. Statistics and Mathematics
2. Programming (Python, R, SQL)
3. Domain Expertise
4. Data Visualization
5. Machine Learning

The Data Science Process:
1. Define the problem
2. Collect data
3. Clean and prepare data
4. Explore and analyze data
5. Model the data
6. Communicate results
            """,
            extra_info="Data Science combines aspects of statistics, computer science, and domain expertise."
        )

    def create_javascript_content(self, course):
        chapter1 = Chapter.objects.create(
            course=course,
            title="JavaScript Fundamentals",
            description="Learn the basics of JavaScript programming",
            order=1
        )
        
        Topic.objects.create(
            chapter=chapter1,
            title="Introduction to JavaScript",
            description="What is JavaScript and how to use it?",
            order=1,
            youtube_video_url="https://www.youtube.com/watch?v=W6NZfCO5SIk",
            notes="""
JavaScript is a high-level, interpreted programming language that is one of the core technologies of the World Wide Web.

Key features:
- Dynamic typing
- First-class functions
- Prototype-based object-orientation
- Event-driven programming
- Client-side and server-side development

Basic JavaScript syntax:
```javascript
// Variables
let name = "John";
const age = 25;
var city = "New York";

// Functions
function greet(name) {
    return "Hello, " + name + "!";
}

// Objects
let person = {
    name: "John",
    age: 25,
    city: "New York"
};
```
            """,
            extra_info="JavaScript was created by Brendan Eich in just 10 days in May 1995."
        )

    def create_marketing_content(self, course):
        chapter1 = Chapter.objects.create(
            course=course,
            title="Digital Marketing Basics",
            description="Understanding the fundamentals of digital marketing",
            order=1
        )
        
        Topic.objects.create(
            chapter=chapter1,
            title="Introduction to Digital Marketing",
            description="What is digital marketing and why is it important?",
            order=1,
            notes="""
Digital Marketing is the use of digital channels to promote or market products and services to consumers and businesses.

Key Digital Marketing Channels:
1. Search Engine Optimization (SEO)
2. Pay-Per-Click Advertising (PPC)
3. Social Media Marketing
4. Email Marketing
5. Content Marketing
6. Affiliate Marketing
7. Influencer Marketing

Benefits of Digital Marketing:
- Cost-effective
- Measurable results
- Targeted audience reach
- Global reach
- Real-time engagement
- Personalization
            """,
            extra_info="Digital marketing spending is expected to reach $786.2 billion by 2026."
        )