#!/usr/bin/env python
"""
Debug script to check Django configuration and template rendering
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')
django.setup()

def debug_django():
    print("🔍 Django Debug Information")
    print("=" * 50)
    
    # Check Django settings
    print(f"✅ Django version: {django.get_version()}")
    print(f"✅ Settings module: {settings.SETTINGS_MODULE}")
    print(f"✅ Debug mode: {settings.DEBUG}")
    print(f"✅ Template dirs: {settings.TEMPLATES[0]['DIRS']}")
    print(f"✅ Installed apps: {len(settings.INSTALLED_APPS)} apps")
    
    # Check if courses app is installed
    if 'courses' in settings.INSTALLED_APPS:
        print("✅ Courses app is installed")
    else:
        print("❌ Courses app is NOT installed")
        return
    
    # Check template directories
    template_dirs = settings.TEMPLATES[0]['DIRS']
    for template_dir in template_dirs:
        if os.path.exists(template_dir):
            print(f"✅ Template directory exists: {template_dir}")
        else:
            print(f"❌ Template directory missing: {template_dir}")
    
    # Check if course templates exist
    course_template_path = os.path.join('courses', 'templates', 'courses', 'course_detail.html')
    if os.path.exists(course_template_path):
        print(f"✅ Course detail template exists: {course_template_path}")
    else:
        print(f"❌ Course detail template missing: {course_template_path}")
    
    # Test URL resolution
    try:
        from django.urls import reverse
        course_list_url = reverse('courses:course_list')
        print(f"✅ Course list URL resolves to: {course_list_url}")
    except Exception as e:
        print(f"❌ URL resolution error: {e}")
    
    # Check database
    try:
        from courses.models import Course
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        course_count = Course.objects.count()
        user_count = User.objects.count()
        
        print(f"✅ Database connection working")
        print(f"   - Courses: {course_count}")
        print(f"   - Users: {user_count}")
        
        if course_count > 0:
            first_course = Course.objects.first()
            print(f"   - First course: {first_course.title}")
            print(f"   - Created at: {first_course.created_at}")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    print("\n🔧 TROUBLESHOOTING STEPS:")
    print("1. Make sure you're running: python manage.py runserver")
    print("2. Access URLs like: http://127.0.0.1:8000/courses/")
    print("3. NOT opening HTML files directly in browser")
    print("4. Check browser developer tools for any JavaScript errors")

if __name__ == "__main__":
    debug_django()