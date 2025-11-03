from django.contrib import admin
from .models import (
    ChatSession, ChatMessage, TutorRequest, AIConfiguration,
    UsageStatistics, CourseKnowledgeBase, TutorFeedback
)

@admin.register(AIConfiguration)
class AIConfigurationAdmin(admin.ModelAdmin):
    list_display = ['provider', 'model_name', 'is_active', 'daily_request_limit', 'created_at']
    list_filter = ['provider', 'is_active']
    search_fields = ['model_name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Configuration', {
            'fields': ('provider', 'model_name', 'api_key', 'is_active')
        }),
        ('Model Parameters', {
            'fields': ('max_tokens', 'temperature')
        }),
        ('Usage Limits', {
            'fields': ('daily_request_limit', 'monthly_token_limit')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['timestamp', 'tokens_used']
    fields = ['message_type', 'content', 'ai_model', 'tokens_used', 'timestamp']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'course', 'created_at', 'is_active', 'message_count']
    list_filter = ['is_active', 'created_at', 'course']
    search_fields = ['title', 'student__username', 'course__title']
    readonly_fields = ['created_at', 'updated_at', 'message_count']
    inlines = [ChatMessageInline]
    
    def message_count(self, obj):
        return obj.get_message_count()
    message_count.short_description = 'Messages'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'ai_model', 'tokens_used', 'timestamp']
    list_filter = ['message_type', 'ai_model', 'timestamp']
    search_fields = ['content', 'session__title', 'session__student__username']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(TutorRequest)
class TutorRequestAdmin(admin.ModelAdmin):
    list_display = ['request_type', 'student', 'course', 'created_at', 'response_time', 'satisfaction_rating']
    list_filter = ['request_type', 'created_at', 'satisfaction_rating']
    search_fields = ['user_input', 'student__username', 'course__title']
    readonly_fields = ['created_at', 'response_time']

@admin.register(UsageStatistics)
class UsageStatisticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'requests_count', 'tokens_used', 'estimated_cost']
    list_filter = ['date']
    search_fields = ['user__username']
    readonly_fields = ['date']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(CourseKnowledgeBase)
class CourseKnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ['course', 'processing_status', 'last_updated']
    list_filter = ['processing_status', 'last_updated']
    search_fields = ['course__title']
    readonly_fields = ['last_updated']
    
    fieldsets = (
        ('Course Information', {
            'fields': ('course', 'processing_status')
        }),
        ('Processed Content', {
            'fields': ('course_summary', 'topics_summary', 'key_concepts'),
            'classes': ('collapse',)
        }),
        ('Advanced', {
            'fields': ('content_embeddings',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        })
    )

@admin.register(TutorFeedback)
class TutorFeedbackAdmin(admin.ModelAdmin):
    list_display = ['student', 'feedback_type', 'rating', 'created_at']
    list_filter = ['feedback_type', 'rating', 'created_at']
    search_fields = ['student__username', 'comment']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'message')

# Custom admin site configuration
admin.site.site_header = "AI Tutor Administration"
admin.site.site_title = "AI Tutor Admin"
admin.site.index_title = "Welcome to AI Tutor Administration"