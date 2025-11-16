# 🎓 NeuroNest - Complete API & Database Documentation

## 📋 Table of Contents
1. [Database Models](#database-models)
2. [Data Types & Fields](#data-types--fields)
3. [Model Relationships](#model-relationships)
4. [API Endpoints](#api-endpoints)
5. [Response Formats](#response-formats)

---

# 📊 DATABASE MODELS

## **1. CustomUser Model** (users/models.py)

**Purpose:** Extended Django user model with role-based access control

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key, auto-generated |
| `username` | CharField | Unique username (max 150 chars) |
| `email` | EmailField | Unique email address |
| `password` | CharField | Hashed password (min 8 chars) |
| `role` | CharField | User role: 'student', 'instructor', 'admin' |
| `first_name` | CharField | User's first name |
| `last_name` | CharField | User's last name |
| `is_active` | BooleanField | Account active status (default: True) |
| `is_staff` | BooleanField | Admin access (default: False) |
| `is_superuser` | BooleanField | Superuser access (default: False) |
| `date_joined` | DateTimeField | Account creation timestamp (auto) |
| `last_login` | DateTimeField | Last login timestamp |
| `groups` | ManyToManyField | User groups |
| `user_permissions` | ManyToManyField | Specific permissions |

### Methods:
- `set_password(password)` - Hash and set password
- `check_password(password)` - Verify password
- `__str__()` - Returns: `{username} ({role})`

### Key Constraints:
- `username` must be unique
- `email` must be unique
- `role` must be one of: 'student', 'instructor', 'admin'

---

## **2. Course Model** (courses/models.py)

**Purpose:** Represents a course taught by an instructor

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `title` | CharField | Course title (max 200 chars) |
| `description` | TextField | Course description |
| `instructor` | ForeignKey | Links to CustomUser (role='instructor') |
| `category` | CharField | Course category (see choices below) |
| `created_at` | DateTimeField | Course creation timestamp (auto) |

### Category Choices:
```
'programming'  - Programming
'design'       - Design
'business'     - Business
'data_science' - Data Science
'marketing'    - Marketing
'photography'  - Photography
'music'        - Music
'language'     - Language
'health'       - Health & Fitness
'other'        - Other
```

### Relations:
- **ForeignKey**: `instructor` → CustomUser
- **Reverse**: `chapters` ← Chapter (one-to-many)
- **Reverse**: `enrollment_set` ← Enrollment (one-to-many)
- **Reverse**: `progress_set` ← Progress (one-to-many)

### Methods:
- `get_total_chapters()` - Returns: int (chapter count)
- `get_total_topics()` - Returns: int (all topics in course)
- `get_total_quizzes()` - Returns: int (chapter + topic quizzes)
- `get_chapter_quizzes()` - Returns: QuerySet[Quiz]
- `get_topic_quizzes()` - Returns: QuerySet[Quiz]
- `get_all_quizzes()` - Returns: QuerySet[Quiz] (ordered)
- `__str__()` - Returns: course title

---

## **3. Chapter Model** (courses/models.py)

**Purpose:** Organizes course content into chapters

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `course` | ForeignKey | Links to Course |
| `title` | CharField | Chapter title (max 255 chars) |
| `description` | TextField | Chapter description |
| `order` | PositiveIntegerField | Chapter sequence order (default: 0) |
| `created_at` | DateTimeField | Creation timestamp (auto) |

### Relations:
- **ForeignKey**: `course` → Course
- **Reverse**: `topics` ← Topic (one-to-many)
- **Reverse**: `quizzes` ← Quiz (one-to-many)

### Ordering: `['order', 'created_at']`

### Methods:
- `__str__()` - Returns: `{course_title} - Chapter {order}: {title}`

---

## **4. Topic Model** (courses/models.py)

**Purpose:** Contains course learning materials (videos, notes, etc.)

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `chapter` | ForeignKey | Links to Chapter |
| `title` | CharField | Topic title (max 255 chars) |
| `description` | TextField | Topic description |
| `youtube_video_url` | URLField | YouTube video link (optional) |
| `notes` | TextField | Topic notes/content (optional) |
| `extra_info` | TextField | Additional information (optional) |
| `order` | PositiveIntegerField | Topic sequence (default: 0) |
| `created_at` | DateTimeField | Creation timestamp (auto) |

### Relations:
- **ForeignKey**: `chapter` → Chapter
- **Reverse**: `quizzes` ← Quiz (one-to-many)
- **Reverse**: `topiccompletion_set` ← TopicCompletion (one-to-many)

### Validation:
- At least ONE of `youtube_video_url`, `notes`, or `extra_info` must be provided

### Methods:
- `get_youtube_embed_url()` - Returns: str (embed URL) or None
- `clean()` - Validates at least one content field exists

---

## **5. Quiz Model** (courses/models.py)

**Purpose:** Assessments tied to chapters or topics

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `chapter` | ForeignKey | Links to Chapter (optional) |
| `topic` | ForeignKey | Links to Topic (optional) |
| `title` | CharField | Quiz title (max 255 chars) |
| `quiz_type` | CharField | Type: 'chapter' or 'topic' |
| `time_limit` | IntegerField | Time in minutes (default: 15) |
| `created_at` | DateTimeField | Creation timestamp (auto) |

### Relations:
- **ForeignKey**: `chapter` → Chapter (optional)
- **ForeignKey**: `topic` → Topic (optional)
- **Reverse**: `questions` ← Question (one-to-many)
- **Reverse**: `studentanswer_set` ← StudentAnswer (one-to-many)

### Validation:
- Quiz must belong to EITHER chapter OR topic (not both, not neither)
- `quiz_type='chapter'` requires `chapter`
- `quiz_type='topic'` requires `topic`

### Properties:
- `course` (property) - Returns: Course instance (via chapter/topic)

### Methods:
- `clean()` - Validates association rules

---

## **6. Question Model** (courses/models.py)

**Purpose:** Individual quiz questions

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `quiz` | ForeignKey | Links to Quiz |
| `text` | TextField | Question content |

### Relations:
- **ForeignKey**: `quiz` → Quiz
- **Reverse**: `options` ← Option (one-to-many)
- **Reverse**: `studentanswer_set` ← StudentAnswer (one-to-many)

### Methods:
- `__str__()` - Returns: first 50 chars of question

---

## **7. Option Model** (courses/models.py)

**Purpose:** Multiple choice answers for questions

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `question` | ForeignKey | Links to Question |
| `text` | CharField | Option text (max 255 chars) |
| `is_correct` | BooleanField | Marks correct answer (default: False) |

### Relations:
- **ForeignKey**: `question` → Question
- **Reverse**: `studentanswer_set` ← StudentAnswer (one-to-many)

### Methods:
- `__str__()` - Returns: `{text} ({'Correct' | 'Wrong'})`

---

## **8. Enrollment Model** (courses/models.py)

**Purpose:** Track student course enrollments

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `student` | ForeignKey | Links to CustomUser (role='student') |
| `course` | ForeignKey | Links to Course |
| `enrolled_at` | DateTimeField | Enrollment timestamp (auto) |

### Constraints:
- `unique_together = ('student', 'course')` - One enrollment per student-course pair

### Relations:
- **ForeignKey**: `student` → CustomUser
- **ForeignKey**: `course` → Course

### Methods:
- `__str__()` - Returns: `{student_username} -> {course_title}`

---

## **9. StudentAnswer Model** (courses/models.py)

**Purpose:** Record student quiz responses

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `student` | ForeignKey | Links to CustomUser (role='student') |
| `question` | ForeignKey | Links to Question |
| `selected_option` | ForeignKey | Links to selected Option |
| `submitted_at` | DateTimeField | Submission timestamp (auto) |

### Relations:
- **ForeignKey**: `student` → CustomUser
- **ForeignKey**: `question` → Question
- **ForeignKey**: `selected_option` → Option

### Methods:
- `is_correct()` - Returns: bool (whether answer was correct)

---

## **10. TopicCompletion Model** (courses/models.py)

**Purpose:** Track completed topics per student

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `student` | ForeignKey | Links to CustomUser (role='student') |
| `topic` | ForeignKey | Links to Topic |
| `completed_at` | DateTimeField | Completion timestamp (auto) |

### Constraints:
- `unique_together = ('student', 'topic')` - One completion record per student-topic

### Relations:
- **ForeignKey**: `student` → CustomUser
- **ForeignKey**: `topic` → Topic

### Methods:
- `__str__()` - Returns: `{student_username} completed {topic_title}`

---

## **11. Progress Model** (courses/models.py)

**Purpose:** Track student course progress and scores

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `student` | ForeignKey | Links to CustomUser (role='student') |
| `course` | ForeignKey | Links to Course |
| `completed_lessons` | IntegerField | Lessons completed (default: 0) |
| `total_lessons` | IntegerField | Total lessons (default: 0) |
| `score` | FloatField | Course score (0-100, default: 0.0) |

### Relations:
- **ForeignKey**: `student` → CustomUser
- **ForeignKey**: `course` → Course

### Methods:
- `progress_percent()` - Returns: float (0-100)
- `get_completed_topics_count()` - Returns: int
- `get_total_topics_count()` - Returns: int

---

## **12. ChatSession Model** (tutor/models.py)

**Purpose:** AI tutor conversation session

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `student` | ForeignKey | Links to CustomUser (role='student') |
| `course` | ForeignKey | Links to Course (optional) |
| `title` | CharField | Session title (max 200, default: "New Chat") |
| `created_at` | DateTimeField | Creation timestamp (auto) |
| `updated_at` | DateTimeField | Last update timestamp (auto) |
| `is_active` | BooleanField | Session active status (default: True) |

### Relations:
- **ForeignKey**: `student` → CustomUser
- **ForeignKey**: `course` → Course (optional)
- **Reverse**: `messages` ← ChatMessage (one-to-many)
- **Reverse**: `requests` ← TutorRequest (one-to-many)

### Ordering: `['-updated_at']`

### Methods:
- `get_message_count()` - Returns: int
- `get_last_message()` - Returns: ChatMessage or None

---

## **13. ChatMessage Model** (tutor/models.py)

**Purpose:** Individual messages in chat

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `session` | ForeignKey | Links to ChatSession |
| `message_type` | CharField | Type: 'user', 'ai', 'system' |
| `content` | TextField | Message content |
| `timestamp` | DateTimeField | Message timestamp (auto) |
| `context_used` | TextField | Course context used (optional) |
| `ai_model` | CharField | AI model used (optional) |
| `tokens_used` | IntegerField | Tokens consumed (optional) |

### Relations:
- **ForeignKey**: `session` → ChatSession
- **Reverse**: `tutorfeedback_set` ← TutorFeedback (one-to-many)

### Ordering: `['timestamp']`

### Methods:
- `__str__()` - Returns: `{message_type}: {content[:50]}...`

---

## **14. TutorRequest Model** (tutor/models.py)

**Purpose:** Track specific tutor request types

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `student` | ForeignKey | Links to CustomUser |
| `session` | ForeignKey | Links to ChatSession |
| `request_type` | CharField | Type of request (see below) |
| `course` | ForeignKey | Related course (optional) |
| `chapter` | ForeignKey | Related chapter (optional) |
| `topic` | ForeignKey | Related topic (optional) |
| `user_input` | TextField | User's input/question |
| `ai_response` | TextField | AI's response |
| `created_at` | DateTimeField | Creation timestamp (auto) |
| `response_time` | FloatField | Response time in seconds (optional) |
| `satisfaction_rating` | IntegerField | User rating 1-5 (optional) |

### Request Type Choices:
```
'question'    - General Question
'summarize'   - Summarize Content
'explain'     - Explain Concept
'quiz_help'   - Quiz Help
'topic_help'  - Topic Help
```

### Relations:
- **ForeignKey**: `student` → CustomUser
- **ForeignKey**: `session` → ChatSession
- **ForeignKey**: `course` → Course (optional)
- **ForeignKey**: `chapter` → Chapter (optional)
- **ForeignKey**: `topic` → Topic (optional)

### Methods:
- `__str__()` - Returns: `{request_type}: {user_input[:50]}...`

---

## **15. AIConfiguration Model** (tutor/models.py)

**Purpose:** Configure AI service provider

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `provider` | CharField | AI provider (see choices) |
| `model_name` | CharField | Model name (max 50) |
| `api_key` | CharField | API key (max 200) |
| `max_tokens` | IntegerField | Max response tokens (default: 1000) |
| `temperature` | FloatField | Response randomness (default: 0.7) |
| `daily_request_limit` | IntegerField | Daily limit (default: 1000) |
| `monthly_token_limit` | IntegerField | Monthly limit (default: 100000) |
| `is_active` | BooleanField | Configuration active (default: True) |
| `created_at` | DateTimeField | Creation timestamp (auto) |

### Provider Choices:
```
'openai'    - OpenAI GPT
'gemini'    - Google Gemini
'anthropic' - Anthropic Claude
```

### Methods:
- `__str__()` - Returns: `{provider} - {model_name}`

---

## **16. UsageStatistics Model** (tutor/models.py)

**Purpose:** Track AI service usage per user per day

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `user` | ForeignKey | Links to CustomUser |
| `date` | DateField | Date tracked (auto) |
| `requests_count` | IntegerField | Request count (default: 0) |
| `tokens_used` | IntegerField | Tokens used (default: 0) |
| `estimated_cost` | DecimalField | Cost in USD (default: 0.0000) |

### Constraints:
- `unique_together = ('user', 'date')` - One record per user per day

### Methods:
- `__str__()` - Returns: `{username} - {date}: {requests_count} requests`

---

## **17. CourseKnowledgeBase Model** (tutor/models.py)

**Purpose:** Preprocessed course content for AI context

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `course` | OneToOneField | Links to Course |
| `course_summary` | TextField | Summary of course |
| `topics_summary` | TextField | Summary of topics |
| `key_concepts` | TextField | JSON list of concepts |
| `content_embeddings` | TextField | JSON embeddings |
| `last_updated` | DateTimeField | Last update (auto) |
| `processing_status` | CharField | Status (default: 'pending') |

### Relations:
- **OneToOneField**: `course` → Course

### Methods:
- `get_key_concepts_list()` - Returns: list (from JSON)
- `set_key_concepts_list(list)` - Sets list as JSON

---

## **18. TutorFeedback Model** (tutor/models.py)

**Purpose:** Student feedback on AI responses

### Fields:
| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `student` | ForeignKey | Links to CustomUser |
| `message` | ForeignKey | Links to ChatMessage |
| `feedback_type` | CharField | Type of feedback (see below) |
| `rating` | IntegerField | Rating 1-5 |
| `comment` | TextField | Additional comment |
| `created_at` | DateTimeField | Creation timestamp (auto) |

### Feedback Type Choices:
```
'helpful'      - Helpful
'not_helpful'  - Not Helpful
'incorrect'    - Incorrect Information
'unclear'      - Unclear Response
```

### Methods:
- `__str__()` - Returns: `{feedback_type} - Rating: {rating}`

---

# 🔗 MODEL RELATIONSHIPS DIAGRAM

```
CustomUser (Central Hub)
├─ 1:Many → Course (as instructor)
├─ 1:Many → Enrollment (as student)
├─ 1:Many → Progress (as student)
├─ 1:Many → StudentAnswer (as student)
├─ 1:Many → TopicCompletion (as student)
├─ 1:Many → ChatSession (as student)
├─ 1:Many → TutorRequest (as student)
├─ 1:Many → UsageStatistics
├─ 1:Many → TutorFeedback
└─ Many:Many → groups
└─ Many:Many → user_permissions

Course
├─ Many:1 ← CustomUser (instructor)
├─ 1:Many → Chapter
├─ 1:Many → Enrollment (students)
├─ 1:Many → Progress (student progress)
├─ 1:Many → ChatSession (optional context)
└─ 1:1 ← CourseKnowledgeBase

Chapter
├─ Many:1 ← Course
├─ 1:Many → Topic
├─ 1:Many → Quiz (chapter-level)
└─ 1:Many ← TutorRequest

Topic
├─ Many:1 ← Chapter
├─ 1:Many → Quiz (topic-level)
├─ 1:Many → TopicCompletion (student completions)
└─ 1:Many ← TutorRequest

Quiz
├─ Many:1 ← Chapter (optional)
├─ Many:1 ← Topic (optional)
├─ 1:Many → Question
└─ 1:Many ← StudentAnswer (indirect)

Question
├─ Many:1 ← Quiz
├─ 1:Many → Option
└─ 1:Many → StudentAnswer

Option
├─ Many:1 ← Question
└─ 1:Many ← StudentAnswer

Enrollment
├─ Many:1 ← CustomUser (student)
└─ Many:1 ← Course

StudentAnswer
├─ Many:1 ← CustomUser (student)
├─ Many:1 ← Question
└─ Many:1 ← Option

TopicCompletion
├─ Many:1 ← CustomUser (student)
└─ Many:1 ← Topic

Progress
├─ Many:1 ← CustomUser (student)
└─ Many:1 ← Course

ChatSession
├─ Many:1 ← CustomUser (student)
├─ Many:1 ← Course (optional)
├─ 1:Many → ChatMessage
└─ 1:Many → TutorRequest

ChatMessage
├─ Many:1 ← ChatSession
└─ 1:Many ← TutorFeedback

TutorRequest
├─ Many:1 ← CustomUser (student)
├─ Many:1 ← ChatSession
├─ Many:1 ← Course (optional)
├─ Many:1 ← Chapter (optional)
└─ Many:1 ← Topic (optional)

CourseKnowledgeBase
└─ 1:1 ← Course

TutorFeedback
├─ Many:1 ← CustomUser (student)
└─ Many:1 ← ChatMessage

UsageStatistics
└─ Many:1 ← CustomUser

AIConfiguration (Global)
```

---

# 🌐 API ENDPOINTS

## **USER AUTHENTICATION APIs**

### **1. User Registration (AJAX)**
```
POST /users/ajax/register/
Content-Type: application/json

Request Body:
{
    "username": "alice_student",
    "email": "alice@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "role": "student"  # or "instructor"
}

Response (Success):
{
    "success": true,
    "message": "Account created successfully",
    "user": {
        "id": 1,
        "username": "alice_student",
        "email": "alice@example.com",
        "role": "student"
    }
}

Response (Error):
{
    "success": false,
    "message": "Username already exists"
}
```

**What it does:**
- Creates new user account
- Hashes password securely
- Validates unique username/email
- Returns user details

**Status Codes:**
- `200` - Success
- `400` - Validation error
- `500` - Server error

---

### **2. User Login (AJAX)**
```
POST /users/ajax/login/
Content-Type: application/json

Request Body:
{
    "username": "alice_student",
    "password": "securepass123"
}

Response (Success):
{
    "success": true,
    "message": "Login successful",
    "user": {
        "id": 1,
        "username": "alice_student",
        "email": "alice@example.com",
        "role": "student"
    }
}

Response (Error):
{
    "success": false,
    "message": "Invalid credentials"
}
```

**What it does:**
- Authenticates user
- Creates session
- Returns user info

**Status Codes:**
- `200` - Success
- `401` - Invalid credentials
- `400` - Missing fields
- `500` - Server error

---

## **COURSE APIs**

### **3. Enroll Student in Course**
```
GET /courses/<course_id>/enroll/

Response: Redirect to course detail page

Data Modified:
- Creates Enrollment record
- Creates initial Progress record
```

**What it does:**
- Enrolls authenticated student in course
- Checks if already enrolled (unique_together constraint)
- Creates progress tracking

**Permissions:**
- Logged in
- User role must be 'student'

---

### **4. Complete Topic**
```
GET /courses/topics/<topic_id>/complete/

Response: Redirect to topic page (with success message)

Data Modified:
- Creates TopicCompletion record
- Updates Progress completed_lessons counter
```

**What it does:**
- Marks topic as completed
- Updates progress metrics

**Permissions:**
- Logged in
- Enrolled in course
- User role must be 'student'

---

## **QUIZ APIs**

### **5. Take Quiz (Form Submission)**
```
POST /courses/quiz/<quiz_id>/

Form Data:
question_1=option_5&question_2=option_8&question_3=option_2

Response: Redirect to /courses/quiz/<quiz_id>/results/

Data Modified:
- Creates StudentAnswer records (one per question)
- Updates Progress score and completed_lessons
- Calculates: score = (correct_answers / total_questions) * 100
```

**What it does:**
- Processes quiz submission
- Saves all student answers
- Calculates and stores score
- Updates course progress

**Calculations:**
```
score = (correct_count / total_questions) * 100
```

**Permissions:**
- Logged in
- Enrolled in course
- User role must be 'student'

---

### **6. Get Quiz Results**
```
GET /courses/quiz/<quiz_id>/results/

Response: HTML page with:
{
    "quiz": Quiz object,
    "student_answers": [StudentAnswer objects],
    "progress": Progress object with score
}
```

**What it does:**
- Retrieves quiz submission results
- Shows which answers were correct
- Displays final score

**Permissions:**
- Logged in
- Must be student who took quiz

---

## **AI TUTOR APIs**

### **7. Send AI Tutor Message (AJAX)**
```
POST /tutor/send-message/
Content-Type: application/json

Request Body:
{
    "session_id": 5,
    "message": "Explain what is a variable",
    "course_id": 1,
    "request_type": "question"  # or "summarize", "explain", "quiz_help", "topic_help"
}

Response (Success):
{
    "success": true,
    "ai_response": "A variable is a named container that stores a value...",
    "message_id": 42,
    "tokens_used": 125,
    "response_time": 1.23
}

Response (Error):
{
    "success": false,
    "error": "You are not enrolled in this course"
}
```

**What it does:**
- Receives student message
- Creates ChatMessage (user)
- Calls AITutorService to generate response
- Creates ChatMessage (ai)
- Tracks usage statistics
- Returns AI response

**Processing:**
1. Check usage limits
2. Validate session/course enrollment
3. Build course context (if course_id provided)
4. Call appropriate AI method based on request_type
5. Save both user and AI messages
6. Track tokens used

**Request Types:**
- `question` - General question answering
- `summarize` - Summarize course content
- `explain` - Explain specific concept
- `quiz_help` - Help with quiz
- `topic_help` - Help with topic

**Status Codes:**
- `200` - Success
- `400` - Missing required fields
- `401` - Not authenticated
- `403` - Access denied (not enrolled)
- `429` - Usage limits exceeded

**Permissions:**
- Logged in
- User role must be 'student'
- Must be enrolled in course (if course_id provided)

---

### **8. Get Chat History**
```
GET /tutor/chat/session/<session_id>/

Response: HTML page with:
{
    "session": ChatSession object,
    "messages": [ChatMessage objects in order],
    "enrolled_courses": [Course objects]
}
```

**What it does:**
- Retrieves chat session and all messages
- Shows conversation history
- Allows continuing conversation

**Ordering:** Messages ordered by timestamp (oldest first)

**Permissions:**
- Logged in
- Must own session (be the student)

---

### **9. Submit AI Feedback (AJAX)**
```
POST /tutor/submit-feedback/
Content-Type: application/json

Request Body:
{
    "message_id": 42,
    "feedback_type": "helpful",  # or "not_helpful", "incorrect", "unclear"
    "rating": 5,                 # 1-5
    "comment": "Great explanation!"
}

Response:
{
    "success": true,
    "feedback_id": 15
}
```

**What it does:**
- Records student feedback on AI response
- Stores rating and comment
- Helps improve AI quality

**Permissions:**
- Logged in
- User role must be 'student'

---

## **COURSE CONTENT CREATION APIs** (Instructor Only)

### **10. Create Course**
```
POST /courses/create/

Form Data:
title=Python Basics
description=Learn Python from scratch
category=programming

Response: Redirect to course detail

Data Modified:
- Creates Course object
- Sets current user as instructor
```

**Permissions:**
- Logged in
- User role must be 'instructor'

---

### **11. Create Chapter**
```
POST /courses/<course_id>/chapters/create/

Form Data:
title=Chapter 1: Introduction
description=Get started with basics
order=1

Response: Redirect to manage chapters

Data Modified:
- Creates Chapter object
- Links to course
```

**Permissions:**
- Logged in
- Must be course instructor

---

### **12. Create Topic**
```
POST /courses/chapters/<chapter_id>/topics/create/

Form Data:
title=Variables
description=Learn about variables
notes=Variables store data values...
youtube_video_url=https://youtube.com/watch?v=xxx
order=1

Response: Redirect to chapter detail

Data Modified:
- Creates Topic object
- Links to chapter
```

**Validation:**
- At least one of: notes, youtube_video_url, extra_info

**Permissions:**
- Logged in
- Must be course instructor

---

### **13. Create Quiz**
```
POST /courses/<course_id>/quiz/create/
OR
POST /courses/topics/<topic_id>/quiz/create/

Form Data:
title=Quiz 1
time_limit=15

Response: Redirect to quiz management

Data Modified:
- Creates Quiz object
- Links to chapter or topic
```

**Validation:**
- Quiz must be for either chapter OR topic

**Permissions:**
- Logged in
- Must be course instructor

---

### **14. Add Question to Quiz**
```
POST /courses/quiz/<quiz_id>/add-question/

Form Data:
text=What is a variable?
question_type=multiple_choice
option_1=A container for data
option_1_correct=on
option_2=A type of loop
option_2_correct=
option_3=A function

Response: Redirect to quiz management

Data Modified:
- Creates Question object
- Creates Option objects for each choice
- Links to quiz
```

**Permissions:**
- Logged in
- Must be course instructor

---

# 📤 RESPONSE FORMATS

## **Standard Success Response**
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": {
        // Response-specific data
    }
}
```

## **Standard Error Response**
```json
{
    "success": false,
    "message": "Description of error",
    "error_code": "SPECIFIC_ERROR"
}
```

## **Pagination Response**
```json
{
    "count": 100,
    "next": "http://example.com/api/courses/?page=2",
    "previous": null,
    "results": [
        { "id": 1, "title": "Course 1" },
        // ... more items
    ]
}
```

## **Quiz Score Calculation**
```
Score = (Number of Correct Answers / Total Questions) * 100

Example:
- Questions: 10
- Correct: 8
- Score: (8 / 10) * 100 = 80%
```

---

# 🔐 AUTHENTICATION & PERMISSIONS

## **Session-Based Authentication**
- Login creates Django session
- Session stored in `SessionStorage`
- User accessible via `request.user`

## **Role-Based Permissions**
```
Student:
✓ Enroll in courses
✓ Take quizzes
✓ Complete topics
✓ Use AI tutor
✗ Create courses
✗ Create quizzes
✗ Edit content

Instructor:
✓ Create courses
✓ Create chapters/topics
✓ Create quizzes
✓ Edit their own content
✓ View student progress
✗ Take quizzes in own courses
✗ Enroll in courses

Admin:
✓ All permissions
```

---

# 🚀 KEY BUSINESS LOGIC

## **Score Calculation**
```python
# Quiz scoring
score = (correct_count / total_questions) * 100

# Certificates
certificate_awarded = progress.score >= 80
```

## **Progress Tracking**
```python
# Update on quiz completion
Progress.update(
    completed_lessons = F('completed_lessons') + 1,
    score = new_score
)
```

## **AI Usage Tracking**
```python
# Daily limit check
usage = UsageStatistics.get(user=user, date=today)
if usage.requests_count >= daily_limit:
    raise UsageLimitExceeded()

# Token tracking
UsageStatistics.update(tokens_used = F('tokens_used') + tokens)
```

## **Content Hierarchy Validation**
```
Course
  └─ Chapter (must have course)
      └─ Topic (must have chapter)
          └─ Quiz (must have chapter or topic, but not both)
              └─ Question (must have quiz)
                  └─ Option (must have question)
```

---

This documentation provides complete details of all models, fields, data types, relationships, and functional API endpoints in the NeuroNest platform.
