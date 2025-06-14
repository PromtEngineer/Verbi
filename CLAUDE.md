# CLAUDE.md - Project Context for AI Assistant

## Project Overview
JARVIS Voice Assistant - A modular voice assistant application with support for multiple state-of-the-art models.

## Key Commands
- `poetry run test` - Run all tests
- `poetry run tests` - Alternative test command
- `poetry run pytest --cov` - Run tests with coverage
- `./scripts/test.sh` - Run tests without coverage
- `./scripts/test.sh coverage` - Run tests with coverage

## Important Notes
- Testing framework: pytest with pytest-cov and pytest-mock
- Package manager: Poetry
- Coverage threshold: 80% (when running with coverage)
- Test markers: unit, integration, slow
- PyAudio dependency removed due to system requirements

