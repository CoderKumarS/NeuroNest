# Contributing to NeuroNest

Thank you for your interest in contributing to NeuroNest! We welcome contributions from everyone.

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git
- Basic knowledge of Django
- Familiarity with HTML, CSS, JavaScript

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/neuronest.git
   cd neuronest
   ```

2. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📋 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Include detailed information**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Use the feature request template**
3. **Provide detailed description**:
   - Use case and motivation
   - Proposed solution
   - Alternative solutions considered

### Code Contributions

#### Branch Naming Convention
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

#### Pull Request Process

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards (see below)
   - Write tests for new functionality
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run tests
   python manage.py test
   
   # Check code style
   flake8 .
   black --check .
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Use the PR template
   - Link related issues
   - Provide clear description of changes

## 📝 Coding Standards

### Python Code Style
- Follow **PEP 8** style guide
- Use **Black** for code formatting
- Use **flake8** for linting
- Maximum line length: 88 characters

### Django Best Practices
- Use class-based views when appropriate
- Follow Django naming conventions
- Use Django's built-in features (forms, admin, etc.)
- Implement proper error handling

### Frontend Standards
- Use **Tailwind CSS** for styling
- Follow semantic HTML practices
- Ensure accessibility compliance
- Test on multiple browsers

### JavaScript Standards
- Use modern ES6+ syntax
- Follow consistent naming conventions
- Add comments for complex logic
- Ensure cross-browser compatibility

## 🧪 Testing Guidelines

### Writing Tests
- Write tests for all new functionality
- Use Django's testing framework
- Follow the AAA pattern (Arrange, Act, Assert)
- Test both positive and negative cases

### Test Categories
- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test component interactions
- **Functional Tests**: Test user workflows
- **Performance Tests**: Test system performance

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test courses

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📚 Documentation

### Code Documentation
- Use docstrings for all functions and classes
- Follow Google or NumPy docstring format
- Include parameter types and return values
- Provide usage examples

### README Updates
- Update README.md for new features
- Include setup instructions
- Add configuration examples
- Update feature lists

## 🔍 Code Review Process

### For Contributors
- Respond to feedback promptly
- Make requested changes
- Keep discussions professional
- Ask questions if unclear

### For Reviewers
- Be constructive and helpful
- Focus on code quality and standards
- Test the changes locally
- Approve when ready

## 🏷️ Commit Message Guidelines

### Format
```
Type: Brief description (50 chars max)

Detailed explanation if needed (wrap at 72 chars)

- List specific changes
- Reference issues: Fixes #123
```

### Types
- **Add**: New features or functionality
- **Fix**: Bug fixes
- **Update**: Modifications to existing features
- **Remove**: Deleted code or features
- **Refactor**: Code restructuring
- **Docs**: Documentation changes
- **Style**: Code formatting changes
- **Test**: Adding or updating tests

### Examples
```
Add: AI tutor chat widget with floating interface

- Implement floating chat button
- Add chat window with message history
- Integrate with OpenAI API
- Add responsive design for mobile

Fixes #45
```

## 🚫 What Not to Contribute

- Incomplete features without tests
- Code that breaks existing functionality
- Changes without proper documentation
- Plagiarized or copyrighted code
- Features that don't align with project goals

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: development@neuronest.com

### Response Times
- Issues: Within 48 hours
- Pull Requests: Within 72 hours
- Security Issues: Within 24 hours

## 🎉 Recognition

Contributors will be:
- Listed in the project's contributors section
- Mentioned in release notes for significant contributions
- Invited to join the core team for exceptional contributions

## 📄 License

By contributing to NeuroNest, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to NeuroNest! 🚀