from django.urls import path
from .views import (
    login_view, register_view, logout_view, dashboard_view, 
    ajax_register, ajax_login
)

app_name = 'users'
urlpatterns = [
    # HTML views
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    
    # AJAX endpoints
    path('ajax/register/', ajax_register, name='ajax_register'),
    path('ajax/login/', ajax_login, name='ajax_login'),
]
