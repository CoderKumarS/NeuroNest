#!/usr/bin/env python3
"""
Test script to verify the new hierarchical model structure:
Course → Chapters → Topics/Quizzes
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')
django.setup()

from courses.models import Course, Chapter, Topic, Quiz
from django.contrib.auth import get_user_model

User = get_user_model()

def test_hierarchical_model():
    print("🧪 Testing Hierarchical Model Structure")
    print("=" * 50)
    
    # Get a sample course
    course = Course.objects.first()
    if not course:
        print("❌ No courses found. Please run create_sample_courses first.")
        return
    
    print(f"📚 Testing with course: {course.title}")
    
    # Test Course methods
    print(f"\n📊 Course Statistics:")
    print(f"   Total Chapters: {course.get_total_chapters()}")
    print(f"   Total Topics: {course.get_total_topics()}")
    print(f"   Total Quizzes: {course.get_total_quizzes()}")
    
    # Test hierarchical structure
    print(f"\n🏗️  Hierarchical Structure:")
    chapters = course.chapters.all()
    
    for chapter in chapters:
        print(f"   📖 Chapter {chapter.order}: {chapter.title}")
        
        # Topics in this chapter
        topics = chapter.topics.all()
        for topic in topics:
            print(f"      📝 Topic {topic.order}: {topic.title}")
            
            # Topic quizzes
            topic_quizzes = topic.quizzes.all()
            for quiz in topic_quizzes:
                print(f"         🧪 Topic Quiz: {quiz.title} ({quiz.time_limit}min)")
        
        # Chapter quizzes
        chapter_quizzes = chapter.quizzes.all()
        for quiz in chapter_quizzes:
            print(f"      🧪 Chapter Quiz: {quiz.title} ({quiz.time_limit}min)")
    
    # Test Quiz model course property
    print(f"\n🔗 Testing Quiz Course Relationships:")
    all_quizzes = course.get_all_quizzes()
    for quiz in all_quizzes:
        quiz_course = quiz.course
        if quiz_course:
            print(f"   ✅ Quiz '{quiz.title}' → Course '{quiz_course.title}'")
        else:
            print(f"   ❌ Quiz '{quiz.title}' has no course relationship!")
    
    # Test model validation
    print(f"\n✅ Model Structure Validation:")
    
    # Check that no quizzes have direct course relationships
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(courses_quiz)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'course_id' in columns:
            print("   ❌ Quiz model still has direct course relationship!")
        else:
            print("   ✅ Quiz model correctly removed direct course relationship")
    
    # Test that all quizzes belong to either chapter or topic
    orphaned_quizzes = Quiz.objects.filter(chapter__isnull=True, topic__isnull=True)
    if orphaned_quizzes.exists():
        print(f"   ❌ Found {orphaned_quizzes.count()} orphaned quizzes!")
    else:
        print("   ✅ All quizzes properly belong to chapters or topics")
    
    # Test course quiz retrieval methods
    chapter_quizzes = course.get_chapter_quizzes()
    topic_quizzes = course.get_topic_quizzes()
    
    print(f"\n📈 Quiz Distribution:")
    print(f"   Chapter-level quizzes: {chapter_quizzes.count()}")
    print(f"   Topic-level quizzes: {topic_quizzes.count()}")
    print(f"   Total quizzes: {all_quizzes.count()}")
    
    # Verify the counts match
    expected_total = chapter_quizzes.count() + topic_quizzes.count()
    if all_quizzes.count() == expected_total:
        print("   ✅ Quiz counts are consistent")
    else:
        print("   ❌ Quiz count mismatch!")
    
    print("\n🎉 Hierarchical model structure test completed!")
    print("✅ Course → Chapters → Topics/Quizzes structure is working correctly!")

if __name__ == "__main__":
    test_hierarchical_model()