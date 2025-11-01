#!/usr/bin/env python
"""
Quick test script to check if the Django setup is working correctly
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')
django.setup()

from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

def test_setup():
    print("🔍 Testing Django setup...")
    
    # Test 1: Check if we can import models
    try:
        print("✅ Models imported successfully")
    except Exception as e:
        print(f"❌ Error importing models: {e}")
        return False
    
    # Test 2: Check database connection
    try:
        course_count = Course.objects.count()
        user_count = User.objects.count()
        print(f"✅ Database connection working")
        print(f"   - Courses in database: {course_count}")
        print(f"   - Users in database: {user_count}")
    except Exception as e:
        print(f"❌ Database error: {e}")
        print("   💡 You may need to run migrations:")
        print("      python manage.py makemigrations")
        print("      python manage.py migrate")
        return False
    
    # Test 3: Check if sample data exists
    if course_count == 0:
        print("⚠️  No courses found in database")
        print("   💡 Run this command to create sample data:")
        print("      python manage.py create_sample_courses")
    else:
        print("✅ Sample courses found")
        
    return True

if __name__ == "__main__":
    test_setup()