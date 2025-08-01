# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Essential Commands
- `make test` - Run the full test suite with Pytest
- `make test-cov` - Run tests with coverage reporting (HTML + terminal)
- `make lint` - Run flake8 linting on src/ and tests/
- `make format` - Format code with Black
- `make format-check` - Check code formatting without making changes
- `make type-check` - Run MyPy type checking on src/
- `make check` - Run all quality checks (format-check, lint, type-check, test)
- `make ci` - Full CI pipeline (install-dev + check)

### Installation
- `make install-dev` - Install package with development dependencies
- `pip install -e .[dev]` - Alternative development installation

### CLI Usage
- `ftl-document generate input.md -o output.md` - Generate FTL document
- `ftl-document validate document.md` - Validate an FTL document
- `ftl-document template` - Generate template FTL document

## Architecture

### Core Components
The codebase follows a clean architecture with four main modules:

1. **core.py** - Contains `FTLDocument` (Pydantic model) and `DocumentParser` for parsing various input formats (markdown, DOCX, HTML, text). Note: Most parsing methods are not yet implemented and will raise `NotImplementedError`.

2. **generator.py** - `DocumentGenerator` class handles output formatting. Supports markdown, JSON, and YAML output formats. Uses string templates for markdown generation.

3. **validator.py** - `DocumentValidator` provides validation logic with quality scoring (0-100). Checks for required sections (title, implementation_steps) and recommended sections (dependencies, tools_required, verification_steps).

4. **cli.py** - Click-based command-line interface with three commands: `generate`, `validate`, and `template`.

### FTL Document Structure
FTL Documents contain these standardized sections:
- **title**: Document title (required)
- **dependencies**: Prerequisites list
- **tools_required**: Automation tools needed
- **questions**: User input questions for customization
- **implementation_steps**: Ordered action steps (required)
- **verification_steps**: Success confirmation steps
- **produces**: What the document creates/achieves
- **metadata**: Additional key-value data

### Current Limitations
- Most document parsing functionality is stubbed with `NotImplementedError`
- Only basic template-based markdown generation is implemented
- No actual document parsing from external formats yet

### Testing
- Uses Pytest with test files in `tests/`
- Test coverage available via `make test-cov`
- Tests cover core, generator, and validator modules

### Code Quality
- Python 3.8+ compatibility
- Black formatting (88 char line length)
- flake8 linting
- MyPy type checking with strict settings
- Pydantic for data validation and serialization