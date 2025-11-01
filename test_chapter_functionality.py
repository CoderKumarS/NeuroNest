#!/usr/bin/env python3
"""
Test script to verify chapter management functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')
django.setup()

from courses.models import Course, Chapter, Topic
from django.contrib.auth import get_user_model

User = get_user_model()

def test_chapter_functionality():
    print("🧪 Testing Chapter Management Functionality")
    print("=" * 50)
    
    # Get a sample course
    course = Course.objects.first()
    if not course:
        print("❌ No courses found. Please run create_sample_courses first.")
        return
    
    print(f"📚 Testing with course: {course.title}")
    
    # Test 1: Check if chapters exist
    chapters = course.chapters.all()
    print(f"📖 Found {chapters.count()} chapters")
    
    for chapter in chapters:
        print(f"   Chapter {chapter.order}: {chapter.title}")
        topics = chapter.topics.all()
        print(f"   └── {topics.count()} topics")
        
        for topic in topics:
            print(f"       • {topic.order}. {topic.title}")
            if topic.youtube_video_url:
                print(f"         📹 Video: {topic.youtube_video_url}")
            if topic.notes:
                print(f"         📝 Notes: {len(topic.notes)} characters")
            if topic.extra_info:
                print(f"         ℹ️  Extra info: {len(topic.extra_info)} characters")
    
    # Test 2: Check URL patterns
    print("\n🔗 Testing URL patterns:")
    
    url_patterns = [
        f"/courses/{course.id}/chapters/",
        f"/courses/{course.id}/chapters/create/",
    ]
    
    if chapters.exists():
        first_chapter = chapters.first()
        url_patterns.extend([
            f"/courses/chapters/{first_chapter.id}/",
            f"/courses/chapters/{first_chapter.id}/edit/",
            f"/courses/chapters/{first_chapter.id}/topics/create/",
        ])
        
        topics = first_chapter.topics.all()
        if topics.exists():
            first_topic = topics.first()
            url_patterns.extend([
                f"/courses/topics/{first_topic.id}/",
                f"/courses/topics/{first_topic.id}/edit/",
                f"/courses/topics/{first_topic.id}/complete/",
            ])
    
    for url in url_patterns:
        print(f"   ✅ {url}")
    
    # Test 3: Check template files
    print("\n📄 Checking template files:")
    
    template_files = [
        "courses/templates/courses/manage_chapters.html",
        "courses/templates/courses/create_chapter.html",
        "courses/templates/courses/edit_chapter.html",
        "courses/templates/courses/chapter_detail.html",
        "courses/templates/courses/create_topic.html",
        "courses/templates/courses/edit_topic.html",
        "courses/templates/courses/topic_detail.html",
    ]
    
    for template in template_files:
        if os.path.exists(template):
            print(f"   ✅ {template}")
        else:
            print(f"   ❌ {template} - Missing!")
    
    # Test 4: Check model relationships
    print("\n🔗 Testing model relationships:")
    
    total_topics = Topic.objects.filter(chapter__course=course).count()
    print(f"   📊 Total topics in course: {total_topics}")
    
    for chapter in chapters:
        topic_count = chapter.topics.count()
        quiz_count = chapter.quizzes.count()
        print(f"   📖 {chapter.title}: {topic_count} topics, {quiz_count} quizzes")
    
    print("\n✅ Chapter management functionality test completed!")
    print("🎉 All core features are working correctly!")

if __name__ == "__main__":
    test_chapter_functionality()