# 🌐 NeuroNest - Complete URL Routes & API Documentation

## **BASE URL**
```
http://localhost:8000
```

---

## 📍 USER AUTHENTICATION ROUTES

### Registration
```
GET/POST  /users/register/
POST      /users/ajax/register/               [AJAX API]
```

### Login
```
GET/POST  /users/login/
POST      /users/ajax/login/                  [AJAX API]
```

### Logout
```
GET       /users/logout/
```

### Dashboard
```
GET       /users/dashboard/
```

### Profile
```
GET       /users/profile/
```

### Edit Profile
```
GET/POST  /users/edit-profile/
```

### Change Password
```
GET/POST  /users/change-password/
```

---

## 📚 COURSE ROUTES

### Course Listing & Browsing
```
GET       /courses/                           List all courses with filtering
GET       /courses/explore/                   Course explorer
GET       /courses/<course_id>/               Course detail view
GET       /courses/my-courses/                Student's enrolled courses
```

### Course Enrollment
```
GET       /courses/<course_id>/enroll/        Enroll in course
POST      /courses/<course_id>/enroll/
```

### Course Progress
```
GET       /courses/<course_id>/progress/      View progress in course
```

### Course Creation (Instructor)
```
GET/POST  /courses/create/                    Create new course
GET/POST  /courses/<course_id>/edit/          Edit course
GET       /courses/<course_id>/manage/        Manage course
```

---

## 📖 CHAPTER ROUTES

### Chapter Management (Instructor)
```
GET       /courses/<course_id>/chapters/      Manage chapters
GET/POST  /courses/<course_id>/chapters/create/ Create chapter
GET/POST  /courses/chapters/<chapter_id>/edit/ Edit chapter
GET       /courses/chapters/<chapter_id>/     View chapter details
```

---

## 🎯 TOPIC ROUTES

### Topic Management (Instructor)
```
GET/POST  /courses/chapters/<chapter_id>/topics/create/  Create topic
GET/POST  /courses/topics/<topic_id>/edit/               Edit topic
GET       /courses/topics/<topic_id>/                    View topic
```

### Topic Completion (Student)
```
GET       /courses/topics/<topic_id>/complete/          Mark topic complete
POST      /courses/topics/<topic_id>/complete/
```

---

## 📋 QUIZ ROUTES

### Quiz Management (Instructor)
```
GET/POST  /courses/<course_id>/quiz/create/               Create chapter quiz
GET/POST  /courses/topics/<topic_id>/quiz/create/         Create topic quiz
GET/POST  /courses/quiz/<quiz_id>/edit/                   Edit quiz
GET       /courses/quiz/<quiz_id>/manage/                 Manage quiz
GET/POST  /courses/quiz/<quiz_id>/add-question/           Add question
GET/POST  /courses/question/<question_id>/edit/           Edit question
GET       /courses/question/<question_id>/delete/         Delete question
```

### Quiz Taking (Student)
```
GET/POST  /courses/quiz/<quiz_id>/               Take quiz (submit answers)
GET       /courses/quiz/<quiz_id>/results/       View quiz results
```

---

## 🤖 AI TUTOR ROUTES

### Chat & Tutoring
```
GET       /tutor/                              AI tutor dashboard
GET       /tutor/chat/                         Chat interface
GET       /tutor/chat/<session_id>/            View specific chat session
GET       /tutor/history/                      Chat history
GET       /tutor/admin-dashboard/              Tutor admin panel

POST      /tutor/send-message/                 [AJAX API] Send message to AI
POST      /tutor/submit-feedback/              [AJAX API] Submit AI feedback
```

---

## 🏠 MAIN SITE ROUTES

### Public Pages
```
GET       /                                    Homepage
GET       /about/                              About page
GET       /contact/                            Contact page
POST      /contact/                            Submit contact form (JSON)
```

---

## 🔑 COMPLETE API ENDPOINT REFERENCE

### **Authentication APIs** (Non-Template Responses)

#### Register User (AJAX)
```
Endpoint: POST /users/ajax/register/
Content-Type: application/json

Input:
{
    "username": string (required, unique),
    "email": string (required, valid email, unique),
    "password": string (required, min 8 chars),
    "password_confirm": string (required, must match password),
    "role": string (optional, default: "student", values: "student"|"instructor")
}

Output (Success 200):
{
    "success": true,
    "message": "Account created successfully",
    "user": {
        "id": int,
        "username": string,
        "email": string,
        "role": string
    }
}

Output (Error 400/500):
{
    "success": false,
    "message": string
}

Validation:
- All fields required
- Passwords must match
- Username must be unique
- Email must be unique
```

#### Login User (AJAX)
```
Endpoint: POST /users/ajax/login/
Content-Type: application/json

Input:
{
    "username": string (required),
    "password": string (required)
}

Output (Success 200):
{
    "success": true,
    "message": "Login successful",
    "user": {
        "id": int,
        "username": string,
        "email": string,
        "role": string
    }
}

Output (Error 401/400):
{
    "success": false,
    "message": string
}

Side Effects:
- Creates session
- Sets authentication cookie
```

---

### **Course APIs** (Data Modification)

#### Enroll in Course
```
Endpoint: GET/POST /courses/<course_id>/enroll/

Parameters:
- course_id: int (path parameter)

Authentication: Required (student only)

Side Effects:
- Creates Enrollment record
- Creates initial Progress record
- Sets completed_lessons=0, score=0

Response:
- Redirect to /courses/<course_id>/
- Display success message: "Successfully enrolled in {course.title}!"

Errors:
- 404: Course not found
- 403: User not student
- Duplicate enrollment: Display message "You are already enrolled in this course"
```

#### Mark Topic Complete
```
Endpoint: GET/POST /courses/topics/<topic_id>/complete/

Parameters:
- topic_id: int (path parameter)

Authentication: Required (student only)

Preconditions:
- Student must be enrolled in course containing topic
- Topic must not already be marked complete (unique_together)

Side Effects:
- Creates TopicCompletion record
- Increments Progress.completed_lessons by 1 (for the course)

Response:
- Redirect to /courses/topics/<topic_id>/
- Display success message

Errors:
- 404: Topic not found
- 403: Not enrolled in course
- Topic already marked complete: Allow but don't duplicate
```

#### Submit Quiz Answers
```
Endpoint: POST /courses/quiz/<quiz_id>/

Parameters:
- quiz_id: int (path parameter)

Authentication: Required (student only)

Input:
Form data with fields: question_<id>=<option_id> for each question

Processing:
1. For each question, get selected option
2. Create StudentAnswer record with:
   - student=request.user
   - question=question
   - selected_option=selected_option
3. Calculate score: (correct_count / total_questions) * 100
4. Update or create Progress:
   - score = calculated_score
   - completed_lessons = 1
   - total_lessons = 1

Side Effects:
- Creates StudentAnswer records (one per question)
- Updates Progress record for course

Response:
- Redirect to /courses/quiz/<quiz_id>/results/
- Display success message with score

Errors:
- 404: Quiz not found
- 403: Not enrolled in course
```

#### Get Quiz Results
```
Endpoint: GET /courses/quiz/<quiz_id>/results/

Parameters:
- quiz_id: int (path parameter)

Authentication: Required

Output:
HTML page with context:
{
    "quiz": Quiz object,
    "student_answers": QuerySet of StudentAnswer objects,
    "progress": Progress object or None
}

Display Shows:
- Question text
- Student's selected answer
- Correct answer
- Whether answer was correct
- Overall score from Progress
```

---

### **AI Tutor APIs** (Data Modification + AI Call)

#### Send Message to AI Tutor (AJAX)
```
Endpoint: POST /tutor/send-message/
Content-Type: application/json

Input:
{
    "session_id": int (required),
    "message": string (required, non-empty),
    "course_id": int (optional),
    "request_type": string (optional, default: "question")
}

Request Types:
- "question": General question answering
- "summarize": Summarize course content
- "explain": Explain a concept
- "quiz_help": Help with quiz
- "topic_help": Help with topic

Authentication: Required (student only)

Validation:
1. Check if user role is student
2. Check usage limits (daily request count, token limits)
3. If course_id: verify student is enrolled
4. If session_id: verify session belongs to user

Processing:
1. Create ChatMessage(session, message_type='user', content=message)
2. Build course context (if course_id provided)
3. Call AITutorService.generate_response(message, context, session_id)
4. Call appropriate AI method based on request_type:
   - "summarize": AITutorService.summarize_content()
   - "explain": AITutorService.explain_concept()
   - default: AITutorService.generate_response()
5. Create ChatMessage(session, message_type='ai', content=response, tokens_used=tokens)
6. Update UsageStatistics:
   - requests_count += 1
   - tokens_used += tokens_from_response
7. Update session title (if first exchange)

Output (Success 200):
{
    "success": true,
    "ai_response": string,
    "message_id": int,
    "tokens_used": int,
    "response_time": float
}

Output (Error):
{
    "success": false,
    "error": string
}

Error Codes:
- 400: Missing required fields
- 401: Not authenticated
- 403: Not enrolled in course or not a student
- 429: Usage limits exceeded
- 500: AI service error

Side Effects:
- Creates ChatMessage records (user + AI)
- Updates session.updated_at
- Updates session.title (if needed)
- Updates UsageStatistics
- Consumes API tokens (cost tracking)
```

#### Submit AI Feedback (AJAX)
```
Endpoint: POST /tutor/submit-feedback/
Content-Type: application/json

Input:
{
    "message_id": int (required),
    "feedback_type": string (required),
    "rating": int (required, 1-5),
    "comment": string (optional)
}

Feedback Types:
- "helpful": Response was helpful
- "not_helpful": Response wasn't helpful
- "incorrect": Incorrect information
- "unclear": Unclear response

Authentication: Required (student only)

Processing:
1. Get ChatMessage by message_id
2. Create TutorFeedback(
   student=request.user,
   message=chat_message,
   feedback_type=feedback_type,
   rating=rating,
   comment=comment
)

Output (Success 200):
{
    "success": true,
    "feedback_id": int
}

Side Effects:
- Creates TutorFeedback record
- Helps improve AI model
```

#### Get Chat History
```
Endpoint: GET /tutor/chat/<session_id>/

Parameters:
- session_id: int (path parameter)

Authentication: Required

Output:
HTML page with context:
{
    "session": ChatSession object,
    "messages": QuerySet of ChatMessage objects (ordered by timestamp),
    "enrolled_courses": QuerySet of enrolled Course objects
}

Message Objects Include:
- message_type: 'user', 'ai', or 'system'
- content: message text
- timestamp: when sent
- ai_model: if AI message
- tokens_used: if AI message
- context_used: course context used

Authorization:
- Session must belong to authenticated user
- 403 error if accessing other user's session
```

---

### **Contact Form API** (Data Creation)

#### Submit Contact Form (AJAX)
```
Endpoint: POST /contact/
Content-Type: application/json

Input:
{
    "first_name": string (required),
    "last_name": string (required),
    "email": string (required, valid email),
    "message": string (required)
}

Processing:
1. Validate all fields provided
2. Log or send contact information
3. Return success response

Output (Success 200):
{
    "success": true,
    "message": "Thank you for your message!"
}

Output (Error 400):
{
    "success": false,
    "message": string
}

Side Effects:
- Contact information may be logged/emailed
```

---

## 📊 HTTP STATUS CODES USED

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Successful API call |
| 400 | Bad Request | Invalid input/validation error |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Authenticated but no permission |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Usage limits exceeded |
| 500 | Internal Server Error | Server-side error |

---

## 🔐 PERMISSION MATRIX

| Endpoint | Student | Instructor | Admin | Auth Req |
|----------|---------|-----------|-------|----------|
| /users/register/ | ✓ | ✓ | ✓ | No |
| /users/login/ | ✓ | ✓ | ✓ | No |
| /courses/ | ✓ | ✓ | ✓ | No |
| /courses/<id>/enroll/ | ✓ | ✗ | ✗ | Yes |
| /courses/create/ | ✗ | ✓ | ✓ | Yes |
| /courses/quiz/<id>/ (take) | ✓ | ✗ | ✗ | Yes |
| /courses/quiz/<id>/add-question/ | ✗ | ✓ | ✓ | Yes |
| /tutor/send-message/ | ✓ | ✗ | ✗ | Yes |
| /tutor/submit-feedback/ | ✓ | ✗ | ✗ | Yes |
| /courses/topics/<id>/complete/ | ✓ | ✗ | ✗ | Yes |

---

## 🚀 COMMON API WORKFLOWS

### **Student Learning Flow**
```
1. POST /users/ajax/register/          → Create account
2. POST /users/ajax/login/             → Login
3. GET /courses/                       → Browse courses
4. GET /courses/<id>/enroll/           → Enroll in course
5. GET /courses/<id>/                  → View course details
6. GET /courses/chapters/<id>/         → View chapter
7. GET /courses/topics/<id>/           → Study topic
8. GET /courses/topics/<id>/complete/  → Mark complete
9. POST /courses/quiz/<id>/            → Submit quiz
10. GET /courses/quiz/<id>/results/    → View results
11. POST /tutor/send-message/          → Get AI help
12. POST /tutor/submit-feedback/       → Provide feedback
```

### **Instructor Teaching Flow**
```
1. POST /users/ajax/register/ (role=instructor) → Create account
2. POST /users/ajax/login/                      → Login
3. POST /courses/create/                        → Create course
4. POST /courses/<id>/chapters/create/          → Add chapter
5. POST /courses/chapters/<id>/topics/create/   → Add topic
6. POST /courses/<id>/quiz/create/              → Create quiz
7. POST /courses/quiz/<id>/add-question/        → Add questions
8. GET /courses/<id>/manage/                    → Manage course
9. GET /courses/<id>/progress/                  → View student progress
```

### **AI Tutor Conversation Flow**
```
1. GET /tutor/                                  → Open dashboard
2. GET /tutor/chat/<id>/                        → Open session
3. POST /tutor/send-message/ (question)         → Ask question
4. POST /tutor/send-message/ (explain)          → Explain concept
5. POST /tutor/send-message/ (summarize)        → Summarize topic
6. POST /tutor/submit-feedback/                 → Rate response
```

---

## 📝 DATABASE QUERY PATTERNS

### Student Enrolled Courses
```python
enrollments = Enrollment.objects.filter(student=user)
enrolled_courses = [e.course for e in enrollments]
```

### Student Progress in Course
```python
progress = Progress.objects.get(student=user, course=course)
score = progress.score  # 0-100
```

### Quiz Score Calculation
```python
correct = StudentAnswer.objects.filter(
    student=user, 
    question__quiz=quiz,
    selected_option__is_correct=True
).count()
score = (correct / quiz.questions.count()) * 100
```

### Chat Messages for Session
```python
messages = ChatMessage.objects.filter(
    session=session
).order_by('timestamp')
```

### Student Completed Topics
```python
completions = TopicCompletion.objects.filter(
    student=user,
    topic__chapter__course=course
)
```

---

This comprehensive guide covers all URL routes and functional API endpoints in NeuroNest.
