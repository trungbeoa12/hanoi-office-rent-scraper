# Contributing to Real Estate Web Scraper

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork the Repository

1. Click the "Fork" button on the GitHub repository page
2. Clone your forked repository:
   ```bash
   git clone https://github.com/yourusername/real-estate-scraper.git
   cd real-estate-scraper
   ```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Make Your Changes

- Follow the existing code style
- Add comments for complex logic
- Update documentation if needed
- Test your changes thoroughly

### 5. Test Your Changes

```bash
# Test the scraper
python main.py --website nhatot --headless

# Check for any errors
python -m py_compile src/**/*.py
```

### 6. Commit Your Changes

```bash
git add .
git commit -m "Add: brief description of your changes"
```

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub.

## 📋 Contribution Guidelines

### Code Style

- Use Python 3.8+ features
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions small and focused

### Commit Messages

Use clear, descriptive commit messages:

- `Add: new feature description`
- `Fix: bug description`
- `Update: improvement description`
- `Remove: deprecated feature`
- `Docs: documentation update`

### Pull Request Guidelines

1. **Clear Title**: Summarize your changes in the title
2. **Description**: Explain what you changed and why
3. **Testing**: Describe how you tested your changes
4. **Breaking Changes**: Note any breaking changes
5. **Screenshots**: Include screenshots for UI changes

## �� Reporting Issues

### Before Reporting

1. Check if the issue already exists
2. Try the latest version
3. Check the documentation

### Issue Template

When reporting an issue, include:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.9.7]
- Chrome version: [e.g. 91.0.4472.124]

**Additional context**
Any other context about the problem.
```

## 🚀 Feature Requests

### Before Requesting

1. Check if the feature already exists
2. Consider if it fits the project's scope
3. Think about implementation complexity

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
Any other context or screenshots about the feature request.
```

## 🏗️ Development Areas

### High Priority

- [ ] Add more Vietnamese real estate websites
- [ ] Improve error handling and recovery
- [ ] Add data validation and cleaning
- [ ] Implement database storage option
- [ ] Add web interface for monitoring

### Medium Priority

- [ ] Add support for other property types
- [ ] Implement parallel crawling
- [ ] Add data export formats (JSON, Excel)
- [ ] Create Docker container
- [ ] Add unit tests

### Low Priority

- [ ] Add GUI interface
- [ ] Implement machine learning for data extraction
- [ ] Add API endpoints
- [ ] Create mobile app

## 🧪 Testing

### Manual Testing

1. Test each website individually
2. Test with different options (headless, profile)
3. Test resume functionality
4. Test error handling

### Automated Testing

We're working on adding automated tests. For now, please test manually.

## 📚 Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include type hints where possible
- Document complex algorithms

### User Documentation

- Update README.md for new features
- Add examples for new functionality
- Update troubleshooting section

## 🔒 Security

### Security Guidelines

- Never commit API keys or passwords
- Use environment variables for sensitive data
- Validate all user inputs
- Follow secure coding practices

### Reporting Security Issues

For security issues, please email directly instead of creating a public issue.

## 📞 Getting Help

### Community

- GitHub Issues: For bugs and feature requests
- GitHub Discussions: For questions and ideas
- Email: For security issues

### Resources

- [Python Documentation](https://docs.python.org/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Web Scraping Best Practices](https://blog.apify.com/web-scraping-best-practices/)

## 🎉 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to this project! 🚀
