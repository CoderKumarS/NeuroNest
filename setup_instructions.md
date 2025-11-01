# 🚀 Setup Instructions for Django LMS

## Step 1: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 2: Create Sample Data
```bash
python manage.py create_sample_courses
```

## Step 3: Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

## Step 4: Run the Development Server
```bash
python manage.py runserver
```

## Step 5: Test the URLs
Visit these URLs in your browser:
- http://127.0.0.1:8000/ (Home page)
- http://127.0.0.1:8000/courses/ (Course list)
- http://127.0.0.1:8000/courses/explore/ (Course explorer)
- http://127.0.0.1:8000/users/login/ (Login page)

## Step 6: Login with Sample Accounts
After running `create_sample_courses`, you can login with:
- **Instructor**: username: `instructor1`, password: `password123`
- **Student**: username: `student1`, password: `password123`

## Troubleshooting

### If you see template variables literally (like `{{ course.title }}`):
1. Make sure you're accessing the Django URLs (not static files)
2. Check that the Django server is running
3. Verify the database has data

### If you get database errors:
1. Run migrations: `python manage.py migrate`
2. Check your database settings in `elearning/settings.py`

### If templates don't load:
1. Check `TEMPLATES` setting in `settings.py`
2. Verify template files exist in the correct directories

## Quick Test
Run this to test your setup:
```bash
python test_setup.py
```