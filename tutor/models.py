from django.db import models
from django.conf import settings
from courses.models import Course, Topic, Chapter
import json

User = settings.AUTH_USER_MODEL

class ChatSession(models.Model):
    """Represents a chat session between a student and AI tutor"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.title}"
    
    def get_message_count(self):
        return self.messages.count()
    
    def get_last_message(self):
        return self.messages.last()


class ChatMessage(models.Model):
    """Individual messages in a chat session"""
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('ai', 'AI Response'),
        ('system', 'System Message'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Optional context for AI responses
    context_used = models.TextField(blank=True, help_text="Course content used for AI response")
    ai_model = models.CharField(max_length=50, blank=True, help_text="AI model used (e.g., gpt-3.5-turbo)")
    tokens_used = models.IntegerField(null=True, blank=True, help_text="Tokens consumed for this response")
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."


class TutorRequest(models.Model):
    """Specific tutor requests like summarization, explanation, etc."""
    REQUEST_TYPES = [
        ('question', 'General Question'),
        ('summarize', 'Summarize Content'),
        ('explain', 'Explain Concept'),
        ('quiz_help', 'Quiz Help'),
        ('topic_help', 'Topic Help'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    
    # Content context
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    
    # Request details
    user_input = models.TextField()
    ai_response = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    response_time = models.FloatField(null=True, blank=True, help_text="Response time in seconds")
    satisfaction_rating = models.IntegerField(null=True, blank=True, help_text="1-5 rating")
    
    def __str__(self):
        return f"{self.request_type}: {self.user_input[:50]}..."


class AIConfiguration(models.Model):
    """Configuration for AI services"""
    AI_PROVIDERS = [
        ('openai', 'OpenAI GPT'),
        ('gemini', 'Google Gemini'),
        ('anthropic', 'Anthropic Claude'),
    ]
    
    provider = models.CharField(max_length=20, choices=AI_PROVIDERS, default='openai')
    model_name = models.CharField(max_length=50, default='gpt-3.5-turbo')
    api_key = models.CharField(max_length=200, help_text="API key for the AI service")
    
    # Model parameters
    max_tokens = models.IntegerField(default=1000)
    temperature = models.FloatField(default=0.7)
    
    # Usage limits
    daily_request_limit = models.IntegerField(default=1000)
    monthly_token_limit = models.IntegerField(default=100000)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "AI Configuration"
        verbose_name_plural = "AI Configurations"
    
    def __str__(self):
        return f"{self.provider} - {self.model_name}"


class UsageStatistics(models.Model):
    """Track AI usage for monitoring and billing"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    # Daily usage counters
    requests_count = models.IntegerField(default=0)
    tokens_used = models.IntegerField(default=0)
    
    # Cost tracking (if applicable)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=4, default=0.0000)
    
    class Meta:
        unique_together = ('user', 'date')
        verbose_name = "Usage Statistics"
        verbose_name_plural = "Usage Statistics"
    
    def __str__(self):
        return f"{self.user.username} - {self.date}: {self.requests_count} requests"


class CourseKnowledgeBase(models.Model):
    """Preprocessed course content for AI context"""
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='knowledge_base')
    
    # Processed content
    course_summary = models.TextField(blank=True)
    topics_summary = models.TextField(blank=True)
    key_concepts = models.TextField(blank=True, help_text="JSON list of key concepts")
    
    # Embeddings (for advanced AI features)
    content_embeddings = models.TextField(blank=True, help_text="JSON of content embeddings")
    
    # Metadata
    last_updated = models.DateTimeField(auto_now=True)
    processing_status = models.CharField(max_length=20, default='pending')
    
    def __str__(self):
        return f"Knowledge Base: {self.course.title}"
    
    def get_key_concepts_list(self):
        """Return key concepts as a Python list"""
        if self.key_concepts:
            try:
                return json.loads(self.key_concepts)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_key_concepts_list(self, concepts_list):
        """Set key concepts from a Python list"""
        self.key_concepts = json.dumps(concepts_list)


class TutorFeedback(models.Model):
    """Student feedback on AI tutor responses"""
    FEEDBACK_TYPES = [
        ('helpful', 'Helpful'),
        ('not_helpful', 'Not Helpful'),
        ('incorrect', 'Incorrect Information'),
        ('unclear', 'Unclear Response'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    rating = models.IntegerField(help_text="1-5 rating")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.feedback_type} - Rating: {self.rating}"