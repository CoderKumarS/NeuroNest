import json
import time
import logging
from typing import Dict, List, Optional, Tuple
from django.conf import settings
from django.core.cache import cache
from django.db import models
from courses.models import Course, Topic, Chapter
from decimal import Decimal

logger = logging.getLogger(__name__)

try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError as e:
    genai = None
    logger.warning(f"Google Generative AI import failed: {e}")

class AITutorService:
    """Main service class for AI tutor functionality"""
    
    def __init__(self):
        self.config = self._get_active_config()
        self._setup_client()
    
    def _get_active_config(self):
        """Get the active AI configuration"""
        from .models import AIConfiguration
        return AIConfiguration.objects.filter(is_active=True).first()
    
    def _setup_client(self):
        """Setup the AI client based on configuration"""
        if not self.config:
            raise ValueError("No active AI configuration found")
        
        if self.config.provider == 'openai':
            if openai is None:
                raise ImportError("OpenAI package not installed. Run: pip install openai")
            openai.api_key = self.config.api_key
        elif self.config.provider == 'gemini':
            global genai
            if genai is None:
                logger.error("genai is None in _setup_client method, attempting re-import")
                try:
                    import google.generativeai as genai_retry
                    genai = genai_retry
                    logger.info("Successfully re-imported google.generativeai")
                except ImportError as e:
                    logger.error(f"Re-import failed: {e}")
                    raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
            
            if genai is None:
                raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
                
            logger.info(f"Configuring Gemini with API key: {self.config.api_key[:10]}...")
            genai.configure(api_key=self.config.api_key)
    
    def generate_response(self, user_message: str, context: str = "", session_id: int = None) -> Dict:
        """Generate AI response to user message"""
        start_time = time.time()
        
        try:
            # Build the prompt with context
            prompt = self._build_prompt(user_message, context)
            
            # Generate response based on provider
            if self.config.provider == 'openai':
                response_data = self._generate_openai_response(prompt)
            elif self.config.provider == 'gemini':
                response_data = self._generate_gemini_response(prompt)
            else:
                raise ValueError(f"Unsupported AI provider: {self.config.provider}")
            
            response_time = time.time() - start_time
            
            return {
                'success': True,
                'response': response_data['content'],
                'tokens_used': response_data.get('tokens_used', 0),
                'response_time': response_time,
                'model': self.config.model_name
            }
            
        except Exception as e:
            logger.error(f"AI response generation failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': "I'm sorry, I'm having trouble processing your request right now. Please try again later.",
                'response_time': time.time() - start_time
            }
    
    def _build_prompt(self, user_message: str, context: str = "") -> str:
        """Build the prompt for AI with context and instructions"""
        system_prompt = """You are an AI tutor assistant for an online learning platform. Your role is to:

1. Help students understand course concepts
2. Answer questions about course content
3. Provide explanations in simple, clear language
4. Summarize lectures and topics when requested
5. Guide students through learning materials

Guidelines:
- Be encouraging and supportive
- Use simple language appropriate for students
- Reference the course content when available
- If you don't know something, admit it and suggest alternatives
- Keep responses concise but comprehensive
- Use examples to illustrate concepts

"""
        
        if context:
            system_prompt += f"\nCourse Context:\n{context}\n"
        
        system_prompt += f"\nStudent Question: {user_message}\n\nPlease provide a helpful response:"
        
        return system_prompt
    
    def _generate_openai_response(self, prompt: str) -> Dict:
        """Generate response using OpenAI API"""
        try:
            if openai is None:
                raise ImportError("OpenAI package not installed")
            
            response = openai.ChatCompletion.create(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI tutor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            return {
                'content': response.choices[0].message.content,
                'tokens_used': response.usage.total_tokens
            }
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _generate_gemini_response(self, prompt: str) -> Dict:
        """Generate response using Google Gemini API"""
        try:
            global genai
            if genai is None:
                logger.error("genai is None in _generate_gemini_response method, attempting re-import")
                try:
                    import google.generativeai as genai_retry
                    genai = genai_retry
                    logger.info("Successfully re-imported google.generativeai in _generate_gemini_response")
                except ImportError as e:
                    logger.error(f"Re-import failed in _generate_gemini_response: {e}")
                    raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
            
            if genai is None:
                raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
            
            model = genai.GenerativeModel(self.config.model_name)
            response = model.generate_content(prompt)
            
            return {
                'content': response.text,
                'tokens_used': 0  # Gemini doesn't provide token count in the same way
            }
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def summarize_content(self, content: str, content_type: str = "topic") -> Dict:
        """Summarize course content (topic, chapter, etc.)"""
        prompt = f"""Please provide a clear and concise summary of this {content_type} content:

{content}

Create a summary that:
1. Highlights the main concepts
2. Lists key points
3. Is easy to understand for students
4. Includes any important examples or applications

Summary:"""
        
        return self.generate_response("", prompt)
    
    def explain_concept(self, concept: str, context: str = "") -> Dict:
        """Explain a specific concept in simple terms"""
        prompt = f"""Please explain the concept of "{concept}" in simple, easy-to-understand terms.

{f'Context: {context}' if context else ''}

Your explanation should:
1. Define the concept clearly
2. Provide examples
3. Explain why it's important
4. Use analogies if helpful
5. Be suitable for students learning this topic

Explanation:"""
        
        return self.generate_response(concept, prompt)
    
    def get_quiz_help(self, question: str, options: List[str], context: str = "") -> Dict:
        """Help student with quiz questions without giving direct answers"""
        options_text = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])
        
        prompt = f"""A student is asking for help with this quiz question:

Question: {question}

Options:
{options_text}

{f'Course Context: {context}' if context else ''}

Please help the student understand the concepts needed to answer this question WITHOUT giving the direct answer. Instead:
1. Explain the relevant concepts
2. Provide hints about what to look for
3. Guide their thinking process
4. Suggest how to approach similar questions

Help:"""
        
        return self.generate_response("", prompt)


class CourseContentProcessor:
    """Process course content for AI context"""
    
    @staticmethod
    def process_course_content(course: Course) -> Dict:
        """Process all course content for AI knowledge base"""
        try:
            # Get all course content
            chapters = course.chapters.all().prefetch_related('topics')
            
            course_content = {
                'title': course.title,
                'description': course.description,
                'category': course.get_category_display(),
                'chapters': []
            }
            
            for chapter in chapters:
                chapter_data = {
                    'title': chapter.title,
                    'description': chapter.description,
                    'topics': []
                }
                
                for topic in chapter.topics.all():
                    topic_data = {
                        'title': topic.title,
                        'description': topic.description,
                        'notes': topic.notes,
                        'extra_info': topic.extra_info
                    }
                    chapter_data['topics'].append(topic_data)
                
                course_content['chapters'].append(chapter_data)
            
            # Generate summaries
            course_summary = CourseContentProcessor._generate_course_summary(course_content)
            topics_summary = CourseContentProcessor._generate_topics_summary(course_content)
            key_concepts = CourseContentProcessor._extract_key_concepts(course_content)
            
            return {
                'course_summary': course_summary,
                'topics_summary': topics_summary,
                'key_concepts': key_concepts,
                'full_content': json.dumps(course_content)
            }
            
        except Exception as e:
            logger.error(f"Course content processing failed: {str(e)}")
            return {}
    
    @staticmethod
    def _generate_course_summary(course_content: Dict) -> str:
        """Generate a summary of the entire course"""
        summary_parts = [
            f"Course: {course_content['title']}",
            f"Category: {course_content['category']}",
            f"Description: {course_content['description']}",
            f"Number of chapters: {len(course_content['chapters'])}"
        ]
        
        # Add chapter summaries
        for chapter in course_content['chapters']:
            summary_parts.append(f"Chapter: {chapter['title']} - {len(chapter['topics'])} topics")
        
        return "\n".join(summary_parts)
    
    @staticmethod
    def _generate_topics_summary(course_content: Dict) -> str:
        """Generate a summary of all topics"""
        topics_summary = []
        
        for chapter in course_content['chapters']:
            for topic in chapter['topics']:
                topic_summary = f"Topic: {topic['title']}"
                if topic['description']:
                    topic_summary += f" - {topic['description']}"
                topics_summary.append(topic_summary)
        
        return "\n".join(topics_summary)
    
    @staticmethod
    def _extract_key_concepts(course_content: Dict) -> List[str]:
        """Extract key concepts from course content"""
        concepts = set()
        
        # Extract from course title and description
        concepts.add(course_content['title'])
        
        # Extract from chapter and topic titles
        for chapter in course_content['chapters']:
            concepts.add(chapter['title'])
            for topic in chapter['topics']:
                concepts.add(topic['title'])
        
        return list(concepts)


class UsageTracker:
    """Track AI usage for monitoring and billing"""
    
    @staticmethod
    def track_usage(user, tokens_used: int = 0, estimated_cost: float = 0.0):
        """Track daily usage for a user"""
        from django.utils import timezone
        
        today = timezone.now().date()
        
        from .models import UsageStatistics
        usage, created = UsageStatistics.objects.get_or_create(
            user=user,
            date=today,
            defaults={
                'requests_count': 0,
                'tokens_used': 0,
                'estimated_cost': 0.0
            }
        )
        
        usage.requests_count += 1
        usage.tokens_used += tokens_used
        usage.estimated_cost += Decimal(str(estimated_cost))
        usage.save()
    
    @staticmethod
    def check_usage_limits(user) -> Tuple[bool, str]:
        """Check if user has exceeded usage limits"""
        from django.utils import timezone
        
        from .models import AIConfiguration
        config = AIConfiguration.objects.filter(is_active=True).first()
        if not config:
            return False, "No AI configuration found"
        
        today = timezone.now().date()
        from .models import UsageStatistics
        usage = UsageStatistics.objects.filter(user=user, date=today).first()
        
        if not usage:
            return True, "Within limits"
        
        if usage.requests_count >= config.daily_request_limit:
            return False, f"Daily request limit exceeded ({config.daily_request_limit})"
        
        # Check monthly token limit
        month_start = today.replace(day=1)
        monthly_usage = UsageStatistics.objects.filter(
            user=user,
            date__gte=month_start,
            date__lte=today
        ).aggregate(total_tokens=models.Sum('tokens_used'))['total_tokens'] or 0
        
        if monthly_usage >= config.monthly_token_limit:
            return False, f"Monthly token limit exceeded ({config.monthly_token_limit})"
        
        return True, "Within limits"


class ContextBuilder:
    """Build context for AI responses from course content"""
    
    @staticmethod
    def build_course_context(course: Course) -> str:
        """Build context from course content"""
        try:
            from .models import CourseKnowledgeBase
            knowledge_base = CourseKnowledgeBase.objects.get(course=course)
            return f"{knowledge_base.course_summary}\n\n{knowledge_base.topics_summary}"
        except CourseKnowledgeBase.DoesNotExist:
            # Fallback to basic course info
            return f"Course: {course.title}\nDescription: {course.description}"
    
    @staticmethod
    def build_topic_context(topic: Topic) -> str:
        """Build context from specific topic"""
        context_parts = [
            f"Course: {topic.chapter.course.title}",
            f"Chapter: {topic.chapter.title}",
            f"Topic: {topic.title}",
            f"Description: {topic.description}"
        ]
        
        if topic.notes:
            context_parts.append(f"Notes: {topic.notes}")
        
        if topic.extra_info:
            context_parts.append(f"Additional Info: {topic.extra_info}")
        
        return "\n".join(context_parts)
    
    @staticmethod
    def build_chapter_context(chapter: Chapter) -> str:
        """Build context from chapter and its topics"""
        context_parts = [
            f"Course: {chapter.course.title}",
            f"Chapter: {chapter.title}",
            f"Description: {chapter.description}",
            "\nTopics in this chapter:"
        ]
        
        for topic in chapter.topics.all():
            context_parts.append(f"- {topic.title}: {topic.description}")
        
        return "\n".join(context_parts)