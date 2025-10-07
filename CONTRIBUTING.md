# Contributing to MLR-Bench Educational Implementation

Thank you for your interest in contributing to this educational project!

## Code of Conduct

This is an educational project. Please be respectful and constructive.

## Development Setup

```bash
# Clone and setup
git clone <repo-url>
cd mlr-bench
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Run tests
pytest tests/
```

## Code Guidelines

### File Size Limit
- **Maximum 300 lines per file**
- Split larger files into smaller modules
- Keep functions focused and simple

### Code Style
- Use type hints
- Write docstrings for all functions
- Keep code simple and readable (for students)
- Add comments to explain complex logic

### Testing
- Write unit tests for new features
- Ensure all tests pass before submitting
- Add integration tests for new agents

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Areas for Contribution

### High Priority
- Additional test coverage
- Documentation improvements
- Bug fixes
- Performance optimizations

### Medium Priority
- Additional evaluation rubrics
- More sophisticated parsing
- Better error handling
- Logging improvements

### Low Priority
- UI/visualization tools
- Additional LLM integrations
- Experiment execution (real code running)

## Questions?

Open an issue for discussion before starting major work.

## License

By contributing, you agree that your contributions will be licensed under the same terms as the project (All rights reserved to Dr. Yoram Segal, educational use only).
