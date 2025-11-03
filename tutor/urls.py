from django.urls import path
from . import views

app_name = 'tutor'

urlpatterns = [
    # Main tutor interface
    path('', views.tutor_dashboard, name='dashboard'),
    path('chat/', views.chat_session, name='new_chat'),
    path('chat/<int:session_id>/', views.chat_session, name='chat_session'),
    
    # AJAX endpoints
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/summarize/', views.summarize_content, name='summarize_content'),
    path('api/feedback/', views.submit_feedback, name='submit_feedback'),
    
    # Topic-specific help
    path('topic/<int:topic_id>/help/', views.topic_help, name='topic_help'),
    
    # Chat management
    path('history/', views.chat_history, name='chat_history'),
    path('session/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    
    # Admin/monitoring
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # AI Assistant Widget
    path('widget/new-session/', views.create_widget_session, name='create_widget_session'),
]