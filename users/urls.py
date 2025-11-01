from django.urls import path
from .views import (
    login_view, register_view, logout_view, dashboard_view, 
    ajax_register, ajax_login, profile_view, edit_profile, change_password
)

app_name = 'users'
urlpatterns = [
    # HTML views
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # Profile management
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    
    # AJAX endpoints
    path('ajax/register/', ajax_register, name='ajax_register'),
    path('ajax/login/', ajax_login, name='ajax_login'),
]
