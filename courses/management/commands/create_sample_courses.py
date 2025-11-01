from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Quiz, Question, Option

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample courses for testing'

    def handle(self, *args, **options):
        # Create instructor user if doesn't exist
        instructor, created = User.objects.get_or_create(
            username='instructor1',
            defaults={
                'email': 'instructor@example.com',
                'role': 'instructor',
                'first_name': 'John',
                'last_name': 'Instructor'
            }
        )
        if created:
            instructor.set_password('password123')
            instructor.save()
            self.stdout.write(f'Created instructor: {instructor.username}')

        # Create student user if doesn't exist
        student, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student@example.com',
                'role': 'student',
                'first_name': 'Jane',
                'last_name': 'Student'
            }
        )
        if created:
            student.set_password('password123')
            student.save()
            self.stdout.write(f'Created student: {student.username}')

        # Sample courses data
        courses_data = [
            {
                'title': 'Introduction to Python Programming',
                'description': 'Learn the fundamentals of Python programming language. This course covers variables, data types, control structures, functions, and basic object-oriented programming concepts. Perfect for beginners who want to start their programming journey.',
                'quizzes': [
                    {
                        'title': 'Python Basics Quiz',
                        'time_limit': 15,
                        'questions': [
                            {
                                'text': 'What is the correct way to create a variable in Python?',
                                'options': [
                                    ('var x = 5', False),
                                    ('x = 5', True),
                                    ('int x = 5', False),
                                    ('variable x = 5', False)
                                ]
                            },
                            {
                                'text': 'Which of the following is a Python data type?',
                                'options': [
                                    ('string', True),
                                    ('character', False),
                                    ('decimal', False),
                                    ('array', False)
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'Web Development with HTML & CSS',
                'description': 'Master the building blocks of web development. Learn HTML for structure and CSS for styling. Create responsive websites and understand modern web design principles. Includes hands-on projects and real-world examples.',
                'quizzes': [
                    {
                        'title': 'HTML Fundamentals',
                        'time_limit': 20,
                        'questions': [
                            {
                                'text': 'What does HTML stand for?',
                                'options': [
                                    ('Hyper Text Markup Language', True),
                                    ('High Tech Modern Language', False),
                                    ('Home Tool Markup Language', False),
                                    ('Hyperlink and Text Markup Language', False)
                                ]
                            },
                            {
                                'text': 'Which HTML tag is used for the largest heading?',
                                'options': [
                                    ('<h6>', False),
                                    ('<h1>', True),
                                    ('<heading>', False),
                                    ('<header>', False)
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'Data Science with Python',
                'description': 'Dive into the world of data science using Python. Learn pandas for data manipulation, matplotlib for visualization, and scikit-learn for machine learning. Work with real datasets and build predictive models.',
                'quizzes': [
                    {
                        'title': 'Data Analysis Basics',
                        'time_limit': 25,
                        'questions': [
                            {
                                'text': 'Which Python library is commonly used for data manipulation?',
                                'options': [
                                    ('numpy', False),
                                    ('pandas', True),
                                    ('matplotlib', False),
                                    ('requests', False)
                                ]
                            },
                            {
                                'text': 'What is the primary purpose of data visualization?',
                                'options': [
                                    ('To make data look pretty', False),
                                    ('To understand patterns and insights in data', True),
                                    ('To reduce file size', False),
                                    ('To encrypt data', False)
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'JavaScript for Beginners',
                'description': 'Learn JavaScript, the language of the web. Understand variables, functions, DOM manipulation, and event handling. Build interactive web applications and understand modern JavaScript features like ES6+.',
                'quizzes': [
                    {
                        'title': 'JavaScript Fundamentals',
                        'time_limit': 18,
                        'questions': [
                            {
                                'text': 'How do you declare a variable in JavaScript?',
                                'options': [
                                    ('var myVar;', True),
                                    ('variable myVar;', False),
                                    ('v myVar;', False),
                                    ('declare myVar;', False)
                                ]
                            },
                            {
                                'text': 'Which method is used to add an element to the end of an array?',
                                'options': [
                                    ('add()', False),
                                    ('append()', False),
                                    ('push()', True),
                                    ('insert()', False)
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'Digital Marketing Fundamentals',
                'description': 'Understand the basics of digital marketing including SEO, social media marketing, email marketing, and content strategy. Learn how to create effective marketing campaigns and measure their success.',
                'quizzes': [
                    {
                        'title': 'Marketing Basics',
                        'time_limit': 15,
                        'questions': [
                            {
                                'text': 'What does SEO stand for?',
                                'options': [
                                    ('Search Engine Optimization', True),
                                    ('Social Engagement Online', False),
                                    ('Site Enhancement Operations', False),
                                    ('Search Engine Operations', False)
                                ]
                            },
                            {
                                'text': 'Which platform is best for B2B marketing?',
                                'options': [
                                    ('Instagram', False),
                                    ('TikTok', False),
                                    ('LinkedIn', True),
                                    ('Snapchat', False)
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        # Create courses
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'description': course_data['description'],
                    'instructor': instructor
                }
            )
            
            if created:
                self.stdout.write(f'Created course: {course.title}')
                
                # Create quizzes for the course
                for quiz_data in course_data['quizzes']:
                    quiz = Quiz.objects.create(
                        course=course,
                        title=quiz_data['title'],
                        time_limit=quiz_data['time_limit']
                    )
                    self.stdout.write(f'  Created quiz: {quiz.title}')
                    
                    # Create questions for the quiz
                    for question_data in quiz_data['questions']:
                        question = Question.objects.create(
                            quiz=quiz,
                            text=question_data['text']
                        )
                        
                        # Create options for the question
                        for option_text, is_correct in question_data['options']:
                            Option.objects.create(
                                question=question,
                                text=option_text,
                                is_correct=is_correct
                            )
                        
                        self.stdout.write(f'    Created question: {question.text[:50]}...')
            else:
                self.stdout.write(f'Course already exists: {course.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample courses!')
        )
        self.stdout.write('You can now login with:')
        self.stdout.write('  Instructor: instructor1 / password123')
        self.stdout.write('  Student: student1 / password123')