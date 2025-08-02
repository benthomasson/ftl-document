# FTL Document Generator

A Python tool for generating FTL documents from arbitrary human-readable documentation.

## Overview

FTL Documents are automation in the form of human-readable documentation. They are interpreted by ftl-automation-agents to perform actions and build infrastructure. This tool helps convert existing documentation into the standardized FTL format.

## Features

- **AI-Powered Transformation**: Automatically convert any documentation format to FTL using LLM models
- **Multi-format parsing**: Convert from markdown, DOCX, HTML, and plain text
- **URL Support**: Generate FTL documents directly from web content
- **Validation**: Comprehensive validation with quality scoring
- **Multiple output formats**: Generate markdown, JSON, or YAML
- **Command-line interface**: Easy-to-use CLI for batch processing
- **Template generation**: Create template FTL documents

## Installation

```bash
pip install ftl-document
```

For development:

```bash
git clone <repository-url>
cd ftl-document
pip install -e .[dev]
```

## Usage

### Command Line Interface

Generate an FTL document from existing documentation:

```bash
ftl-document generate input.md -o output.md
```

Generate from a URL:

```bash
ftl-document generate https://example.com/docs -o output.md
```

Use a specific LLM model:

```bash
ftl-document generate input.md -o output.md --model gpt-4
```

Validate an existing FTL document:

```bash
ftl-document validate document.md
```

Generate a template FTL document:

```bash
ftl-document template > new-document.md
```

### Python API

```python
from ftl_document import FTLDocument, DocumentGenerator, DocumentValidator, DocumentParser

# Transform existing documentation using AI
parser = DocumentParser(model="claude-sonnet-4-20250514")
content = "Install nginx and configure SSL certificates..."
doc = parser.parse_with_llm(content)

# Or create a document manually
doc = FTLDocument(
    title="Setup Development Environment",
    dependencies=["Python 3.8+", "Git"],
    tools_required=["pip", "virtualenv"],
    implementation_steps=[
        "Create virtual environment",
        "Install dependencies",
        "Configure settings"
    ],
    verification_steps=[
        "Run tests",
        "Check configuration"
    ]
)

# Generate markdown
generator = DocumentGenerator()
markdown_output = generator.generate_markdown(doc)

# Validate
validator = DocumentValidator()
results = validator.validate(doc)
print(f"Valid: {results['valid']}, Score: {results['score']}/100")
```

## FTL Document Format

FTL documents follow a standardized structure:

- **Title**: Clear, descriptive title
- **Dependencies**: Prerequisites needed before execution
- **Tools Required**: Specific automation tools needed
- **Questions**: User inputs required for customization
- **Implementation Steps**: Ordered list of actions to perform
- **Verification Steps**: How to confirm successful completion
- **Produces**: What the document creates or achieves

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ tests/
```

### Type Checking

```bash
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.