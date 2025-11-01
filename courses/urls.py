from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Course Explorer
    path('', views.course_list, name='course_list'),
    path('explore/', views.course_explorer, name='course_explorer'),
    
    # Course Details
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    
    # Instructor Views
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('<int:course_id>/manage/', views.manage_course, name='manage_course'),
    
    # Quiz Views
    path('<int:course_id>/quiz/create/', views.create_quiz, name='create_quiz'),
    path('topics/<int:topic_id>/quiz/create/', views.create_topic_quiz, name='create_topic_quiz'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:quiz_id>/manage/', views.manage_quiz, name='manage_quiz'),
    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    
    # Chapter Management
    path('<int:course_id>/chapters/', views.manage_chapters, name='manage_chapters'),
    path('<int:course_id>/chapters/create/', views.create_chapter, name='create_chapter'),
    path('chapters/<int:chapter_id>/edit/', views.edit_chapter, name='edit_chapter'),
    path('chapters/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),
    
    # Topic Management
    path('chapters/<int:chapter_id>/topics/create/', views.create_topic, name='create_topic'),
    path('topics/<int:topic_id>/edit/', views.edit_topic, name='edit_topic'),
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('topics/<int:topic_id>/complete/', views.complete_topic, name='complete_topic'),
    
    # Student Progress
    path('my-courses/', views.my_courses, name='my_courses'),
    path('<int:course_id>/progress/', views.course_progress, name='course_progress'),
    
    # Debug view
    path('test-template/', views.test_template_rendering, name='test_template'),
]