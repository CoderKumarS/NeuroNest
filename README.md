# 🎓 NeuroNest - AI-Powered E-Learning Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

NeuroNest is a modern, AI-powered e-learning platform built with Django that provides an interactive learning experience with intelligent tutoring capabilities.

## 🌟 Features

### 🎯 Core Learning Features
- **Course Management**: Create, manage, and enroll in comprehensive courses
- **Interactive Quizzes**: Engaging quizzes with multiple question types
- **Progress Tracking**: Real-time learning progress monitoring
- **User Roles**: Support for students, instructors, and administrators
- **Responsive Design**: Mobile-friendly interface with dark/light mode

### 🤖 AI-Powered Features
- **AI Tutor Assistant**: Floating chat widget with intelligent tutoring
- **Personalized Learning**: AI-driven course recommendations
- **Instant Help**: 24/7 AI support for learning questions
- **Context-Aware Responses**: Course-specific AI assistance

### 🎨 Modern UI/UX
- **Clean Interface**: Modern, intuitive design with Tailwind CSS
- **Dark Mode**: Full dark/light theme support
- **Mobile Responsive**: Optimized for all device sizes
- **Interactive Elements**: Smooth animations and transitions

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CoderKumarS/NeuroNest.git
   cd neuronest
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_ai.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env with your configuration
   # Add your OpenAI API key and other settings
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Set up AI Tutor (optional)**
   ```bash
   python manage.py setup_ai_tutor
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## 📁 Project Structure

```
neuronest/
├── 📁 courses/              # Course management app
│   ├── 📁 templates/        # Course-related templates
│   ├── 📁 static/          # Course-specific static files
│   ├── models.py           # Course, Quiz, Progress models
│   ├── views.py            # Course views and logic
│   └── urls.py             # Course URL patterns
├── 📁 users/               # User management app
│   ├── 📁 templates/       # User-related templates
│   ├── 📁 static/          # User-specific static files
│   ├── models.py           # Custom user model
│   ├── views.py            # Authentication and profile views
│   └── urls.py             # User URL patterns
├── 📁 tutor/               # AI Tutor app
│   ├── 📁 templates/       # AI tutor templates
│   ├── 📁 static/          # AI tutor static files
│   ├── models.py           # Chat sessions and messages
│   ├── services.py         # AI integration services
│   ├── views.py            # AI tutor views
│   └── urls.py             # AI tutor URL patterns
├── 📁 elearning/           # Main project directory
│   ├── 📁 templates/       # Base templates
│   ├── 📁 static/          # Global static files
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   └── views.py            # Home, About, Contact views
├── 📁 static/              # Collected static files (production)
├── 📁 media/               # User uploaded files
├── manage.py               # Django management script
├── requirements_ai.txt     # Python dependencies
├── .env                    # Environment variables
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite by default)
DATABASE_URL=sqlite:///db.sqlite3

# AI Configuration
OPENAI_API_KEY=your-openai-api-key-here
AI_MODEL=gpt-3.5-turbo

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Static Files (production)
STATIC_ROOT=/path/to/static/files
MEDIA_ROOT=/path/to/media/files
```

### AI Tutor Setup

The AI Tutor requires an OpenAI API key:

1. Get an API key from [OpenAI](https://platform.openai.com/api-keys)
2. Add it to your `.env` file as `OPENAI_API_KEY`
3. Run the setup command: `python manage.py setup_ai_tutor`

## 🎯 Usage

### For Students
1. **Register/Login**: Create an account or log in
2. **Browse Courses**: Explore available courses
3. **Enroll**: Join courses that interest you
4. **Learn**: Access course materials and take quizzes
5. **AI Help**: Use the AI tutor for instant assistance
6. **Track Progress**: Monitor your learning journey

### For Instructors
1. **Create Courses**: Design comprehensive learning experiences
2. **Add Content**: Upload materials, create quizzes
3. **Manage Students**: Monitor enrollment and progress
4. **Analytics**: View detailed learning analytics

### For Administrators
1. **User Management**: Manage all platform users
2. **Course Oversight**: Monitor all courses and content
3. **AI Tutor Management**: Configure AI settings
4. **Platform Analytics**: Access comprehensive reports

## 🤖 AI Features

### AI Tutor Assistant
- **Floating Widget**: Always accessible AI help
- **Context-Aware**: Understands current course context
- **Natural Language**: Conversational interface
- **Instant Responses**: Real-time AI assistance
- **Learning Support**: Explanations, examples, and guidance

### AI Capabilities
- Course-specific question answering
- Concept explanations and examples
- Learning path recommendations
- Progress analysis and suggestions
- 24/7 availability

## 🎨 Customization

### Themes
- Light and dark mode support
- Customizable color schemes
- Responsive design for all devices

### Styling
- Built with Tailwind CSS
- Modular CSS architecture
- Easy theme customization
- Component-based styling

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test courses
python manage.py test users
python manage.py test tutor

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📦 Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   # Set production environment variables
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Database Migration**
   ```bash
   python manage.py migrate --run-syncdb
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

### Deployment Options
- **Heroku**: Easy deployment with Heroku CLI
- **DigitalOcean**: App Platform or Droplets
- **AWS**: EC2, Elastic Beanstalk, or Lambda
- **Docker**: Containerized deployment
- **Traditional VPS**: Any Linux server

## 🔒 Security

- CSRF protection enabled
- SQL injection prevention
- XSS protection
- Secure authentication system
- Environment-based configuration
- Regular security updates

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check this README and code comments
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join GitHub Discussions for questions
- **Email**: Contact us at support@neuronest.com

### Common Issues

**Q: AI Tutor not working?**
A: Ensure your OpenAI API key is correctly set in the `.env` file.

**Q: Static files not loading?**
A: Run `python manage.py collectstatic` and check your static files configuration.

**Q: Database errors?**
A: Run `python manage.py migrate` to apply pending migrations.

## 🚧 Roadmap

### Upcoming Features
- [ ] Video streaming integration
- [ ] Real-time collaboration tools
- [ ] Advanced analytics dashboard
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Integration with external LMS
- [ ] Advanced AI features (voice, vision)
- [ ] Gamification elements

### Version History
- **v1.0.0** - Initial release with core features
- **v1.1.0** - AI Tutor integration
- **v1.2.0** - Enhanced UI/UX and mobile optimization
- **v1.3.0** - Advanced course management features

## 🙏 Acknowledgments

- Django community for the excellent framework
- OpenAI for AI capabilities
- Tailwind CSS for beautiful styling
- All contributors and testers

---

**Built with ❤️ by the NeuroNest Team**

For more information, visit our [website](https://neuronest.com) or follow us on [Twitter](https://twitter.com/neuronest).