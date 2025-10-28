from django.shortcuts import render

def home_view(request):
    """
    Home page view for the elearning platform
    """
    return render(request, 'base/index.html')
