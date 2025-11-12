.PHONY: help install install-dev test test-unit test-integration test-ethics coverage lint format type-check clean gate-test

help:
	@echo "entaENGELment Framework - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install         Install package"
	@echo "  make install-dev     Install package with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test            Run all tests"
	@echo "  make test-unit       Run unit tests only"
	@echo "  make test-integration Run integration tests only"
	@echo "  make test-ethics     Run ethics/fail-safe tests only"
	@echo "  make coverage        Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            Run linting (ruff)"
	@echo "  make format          Format code (black)"
	@echo "  make type-check      Run type checking (mypy)"
	@echo ""
	@echo "Gate Policy:"
	@echo "  make gate-test       Test gate toggle functionality"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean           Remove build artifacts and cache"

install:
	pip install -e .

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-ethics:
	pytest tests/ethics/ -v

coverage:
	pytest --cov --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	ruff check src/ tools/ tests/

format:
	black src/ tools/ tests/

type-check:
	mypy src/ tools/

gate-test:
	@echo "Testing gate with valid context (should open):"
	python tools/mzm/gate_toggle.py 0.9 true true 1.0 true
	@echo ""
	@echo "Testing gate with low phi (should close):"
	python tools/mzm/gate_toggle.py 0.5 true true 1.0 true
	@echo ""
	@echo "Testing gate without consent (should close):"
	python tools/mzm/gate_toggle.py 0.9 false true 1.0 true

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
