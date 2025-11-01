from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Course(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming'),
        ('design', 'Design'),
        ('business', 'Business'),
        ('data_science', 'Data Science'),
        ('marketing', 'Marketing'),
        ('photography', 'Photography'),
        ('music', 'Music'),
        ('language', 'Language'),
        ('health', 'Health & Fitness'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'})
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_total_chapters(self):
        """Get total number of chapters in this course"""
        return self.chapters.count()

    def get_total_topics(self):
        """Get total number of topics across all chapters"""
        return Topic.objects.filter(chapter__course=self).count()

    def get_total_quizzes(self):
        """Get total number of quizzes across all chapters and topics"""
        from django.db.models import Q
        return Quiz.objects.filter(
            Q(chapter__course=self) | Q(topic__chapter__course=self)
        ).count()

    def get_chapter_quizzes(self):
        """Get all chapter-level quizzes for this course"""
        return Quiz.objects.filter(chapter__course=self, quiz_type='chapter')

    def get_topic_quizzes(self):
        """Get all topic-level quizzes for this course"""
        return Quiz.objects.filter(topic__chapter__course=self, quiz_type='topic')

    def get_all_quizzes(self):
        """Get all quizzes (chapter and topic level) for this course"""
        from django.db.models import Q
        return Quiz.objects.filter(
            Q(chapter__course=self) | Q(topic__chapter__course=self)
        ).order_by('chapter__order', 'topic__order', 'created_at')

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} -> {self.course}"

User = settings.AUTH_USER_MODEL  # shortcut for referencing the custom User model


class Chapter(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.course.title} - Chapter {self.order}: {self.title}"


class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    # Content fields - at least one is required
    youtube_video_url = models.URLField(blank=True, help_text="YouTube video URL")
    notes = models.TextField(blank=True, help_text="Topic notes and content")
    extra_info = models.TextField(blank=True, help_text="Additional information")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.chapter.title} - Topic {self.order}: {self.title}"

    def get_youtube_embed_url(self):
        """Convert YouTube URL to embed URL"""
        if self.youtube_video_url:
            if 'watch?v=' in self.youtube_video_url:
                video_id = self.youtube_video_url.split('watch?v=')[1].split('&')[0]
                return f"https://www.youtube.com/embed/{video_id}"
            elif 'youtu.be/' in self.youtube_video_url:
                video_id = self.youtube_video_url.split('youtu.be/')[1].split('?')[0]
                return f"https://www.youtube.com/embed/{video_id}"
        return None

    def clean(self):
        """Ensure at least one content field is provided"""
        from django.core.exceptions import ValidationError
        if not any([self.youtube_video_url, self.notes, self.extra_info]):
            raise ValidationError('At least one of YouTube video, notes, or extra info must be provided.')


class Quiz(models.Model):
    QUIZ_TYPE_CHOICES = [
        ('chapter', 'Chapter Quiz'),
        ('topic', 'Topic Quiz'),
    ]
    
    # Remove direct course relationship - quizzes belong to chapters or topics only
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quizzes', null=True, blank=True)
    
    title = models.CharField(max_length=255)
    quiz_type = models.CharField(max_length=10, choices=QUIZ_TYPE_CHOICES, default='chapter')
    time_limit = models.IntegerField(default=15)  # minutes
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def course(self):
        """Get the course this quiz belongs to through chapter or topic"""
        if self.chapter:
            return self.chapter.course
        elif self.topic:
            return self.topic.chapter.course
        return None

    def __str__(self):
        if self.topic:
            return f"{self.topic.title} - {self.title}"
        elif self.chapter:
            return f"{self.chapter.title} - {self.title}"
        return self.title

    def clean(self):
        """Ensure quiz is associated with either chapter or topic, but not both"""
        from django.core.exceptions import ValidationError
        
        if not self.chapter and not self.topic:
            raise ValidationError('Quiz must be associated with either a chapter or a topic.')
        
        if self.chapter and self.topic:
            raise ValidationError('Quiz cannot be associated with both a chapter and a topic.')
        
        if self.quiz_type == 'chapter' and not self.chapter:
            raise ValidationError('Chapter quiz must be associated with a chapter.')
        
        if self.quiz_type == 'topic' and not self.topic:
            raise ValidationError('Topic quiz must be associated with a topic.')


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()

    def __str__(self):
        return self.text[:50]

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"


class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def is_correct(self):
        return self.selected_option.is_correct


class TopicCompletion(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'topic')

    def __str__(self):
        return f"{self.student.username} completed {self.topic.title}"


class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    completed_lessons = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)

    def progress_percent(self):
        if self.total_lessons == 0:
            return 0
        return (self.completed_lessons / self.total_lessons) * 100

    def get_completed_topics_count(self):
        """Get count of completed topics for this course"""
        return TopicCompletion.objects.filter(
            student=self.student,
            topic__chapter__course=self.course
        ).count()

    def get_total_topics_count(self):
        """Get total topics count for this course"""
        return Topic.objects.filter(chapter__course=self.course).count()
