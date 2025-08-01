.PHONY: help install install-dev test lint format type-check clean build upload

help:
	@echo "Available commands:"
	@echo "  install      Install package"
	@echo "  install-dev  Install package with development dependencies"
	@echo "  test         Run tests"
	@echo "  lint         Run linting"
	@echo "  format       Format code"
	@echo "  type-check   Run type checking"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  upload       Upload to PyPI"

install:
	pip install -e .

install-dev:
	pip install -e .[dev]

test:
	pytest

test-cov:
	pytest --cov=ftl_document --cov-report=html --cov-report=term

lint:
	flake8 src/ tests/

format:
	black src/ tests/

format-check:
	black --check src/ tests/

type-check:
	mypy src/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload:
	python -m twine upload dist/*

check: format-check lint type-check test

ci: install-dev check