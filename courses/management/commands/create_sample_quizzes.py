from django.core.management.base import BaseCommand
from courses.models import Course, Chapter, Topic, Quiz, Question, Option

class Command(BaseCommand):
    help = 'Create sample quizzes for chapters and topics'

    def handle(self, *args, **options):
        # Get existing courses and chapters
        courses = Course.objects.all()
        
        if not courses.exists():
            self.stdout.write(self.style.ERROR('No courses found. Please run create_sample_courses first.'))
            return

        for course in courses:
            self.stdout.write(f'Adding quizzes to course: {course.title}')
            
            chapters = course.chapters.all()
            for chapter in chapters:
                # Create a chapter quiz
                chapter_quiz = Quiz.objects.create(
                    chapter=chapter,
                    title=f"{chapter.title} Assessment",
                    quiz_type='chapter',
                    time_limit=20
                )
                
                # Add questions to chapter quiz
                self.create_sample_questions(chapter_quiz, chapter.title)
                
                # Create topic quizzes for some topics
                topics = chapter.topics.all()
                for i, topic in enumerate(topics):
                    if i % 2 == 0:  # Create quiz for every other topic
                        topic_quiz = Quiz.objects.create(
                            topic=topic,
                            title=f"{topic.title} Quick Check",
                            quiz_type='topic',
                            time_limit=10
                        )
                        
                        # Add questions to topic quiz
                        self.create_topic_questions(topic_quiz, topic.title)

        self.stdout.write(self.style.SUCCESS('Successfully created sample quizzes!'))

    def create_sample_questions(self, quiz, chapter_title):
        """Create sample questions for chapter quizzes"""
        if 'Python Fundamentals' in chapter_title:
            # Question 1
            q1 = Question.objects.create(
                quiz=quiz,
                text="What is Python?"
            )
            Option.objects.create(question=q1, text="A programming language", is_correct=True)
            Option.objects.create(question=q1, text="A type of snake", is_correct=False)
            Option.objects.create(question=q1, text="A web browser", is_correct=False)
            Option.objects.create(question=q1, text="A database", is_correct=False)
            
            # Question 2
            q2 = Question.objects.create(
                quiz=quiz,
                text="Which of the following is a valid Python variable name?"
            )
            Option.objects.create(question=q2, text="my_variable", is_correct=True)
            Option.objects.create(question=q2, text="2variable", is_correct=False)
            Option.objects.create(question=q2, text="my-variable", is_correct=False)
            Option.objects.create(question=q2, text="class", is_correct=False)
            
        elif 'Control Flow' in chapter_title:
            # Question 1
            q1 = Question.objects.create(
                quiz=quiz,
                text="Which keyword is used for conditional statements in Python?"
            )
            Option.objects.create(question=q1, text="if", is_correct=True)
            Option.objects.create(question=q1, text="when", is_correct=False)
            Option.objects.create(question=q1, text="check", is_correct=False)
            Option.objects.create(question=q1, text="condition", is_correct=False)
            
        elif 'HTML' in chapter_title:
            # Question 1
            q1 = Question.objects.create(
                quiz=quiz,
                text="What does HTML stand for?"
            )
            Option.objects.create(question=q1, text="HyperText Markup Language", is_correct=True)
            Option.objects.create(question=q1, text="High Tech Modern Language", is_correct=False)
            Option.objects.create(question=q1, text="Home Tool Markup Language", is_correct=False)
            Option.objects.create(question=q1, text="Hyperlink and Text Markup Language", is_correct=False)

    def create_topic_questions(self, quiz, topic_title):
        """Create sample questions for topic quizzes"""
        if 'Introduction to Python' in topic_title:
            q1 = Question.objects.create(
                quiz=quiz,
                text="Python is known for its:"
            )
            Option.objects.create(question=q1, text="Simplicity and readability", is_correct=True)
            Option.objects.create(question=q1, text="Complex syntax", is_correct=False)
            Option.objects.create(question=q1, text="Slow execution", is_correct=False)
            Option.objects.create(question=q1, text="Limited libraries", is_correct=False)
            
        elif 'Variables and Data Types' in topic_title:
            q1 = Question.objects.create(
                quiz=quiz,
                text="Which of these is NOT a Python data type?"
            )
            Option.objects.create(question=q1, text="char", is_correct=True)
            Option.objects.create(question=q1, text="int", is_correct=False)
            Option.objects.create(question=q1, text="str", is_correct=False)
            Option.objects.create(question=q1, text="bool", is_correct=False)
            
        else:
            # Generic question
            q1 = Question.objects.create(
                quiz=quiz,
                text=f"This is a sample question about {topic_title}. What is the correct answer?"
            )
            Option.objects.create(question=q1, text="This is correct", is_correct=True)
            Option.objects.create(question=q1, text="This is wrong", is_correct=False)
            Option.objects.create(question=q1, text="This is also wrong", is_correct=False)
            Option.objects.create(question=q1, text="This is incorrect too", is_correct=False)