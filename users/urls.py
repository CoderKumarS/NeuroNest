from django.urls import path
from .views import (
    RegisterView, api_login, login_view, register_view, 
    logout_view, dashboard_view, ajax_register, ajax_login
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# Add this line:
app_name = 'users'
urlpatterns = [
    # API endpoints
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/login/', api_login, name='api_login'),
    path('api/ajax/register/', ajax_register, name='ajax_register'),
    path('api/ajax/login/', ajax_login, name='ajax_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # HTML views
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
