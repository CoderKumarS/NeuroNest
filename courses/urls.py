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
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    
    # Student Progress
    path('my-courses/', views.my_courses, name='my_courses'),
    path('<int:course_id>/progress/', views.course_progress, name='course_progress'),
    
    # Debug view
    path('test-template/', views.test_template_rendering, name='test_template'),
]