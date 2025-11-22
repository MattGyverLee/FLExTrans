# FLExTrans Rule Assistant Tests

This directory contains comprehensive tests for the FLExTrans Rule Assistant functionality.

## Quick Start

### Installation

```bash
# Install test dependencies
pip install -r requirements-test.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=CreateApertiumRules --cov-report=html

# Run specific test file
pytest test_rule_assistant_comprehensive.py

# Run specific test class
pytest test_rule_assistant_comprehensive.py::TestBasicFunctionality

# Run specific test
pytest test_rule_assistant_comprehensive.py::TestBasicFunctionality::test_simple_def_noun_rule
```

### Run Tests in Parallel

```bash
# Run tests in parallel (faster)
pytest -n auto
```

## Test Files

- **`test_rule_assistant_comprehensive.py`**: Comprehensive pytest-based test suite (50+ tests)
- **`conftest.py`**: Shared pytest fixtures and configuration
- **`pytest.ini`**: Pytest configuration
- **`requirements-test.txt`**: Test dependencies
- **`TEST_COVERAGE.md`**: Detailed test coverage documentation

## Test Categories

1. **Basic Functionality** - Core operations (simple rules, agreement, affixes)
2. **Advanced Features** - Complex features (ranking, defaults, permutations, Bantu)
3. **Edge Cases** - Boundary conditions and unusual inputs
4. **Error Handling** - Validation and error reporting
5. **Integration** - End-to-end workflows
6. **Regression** - Tests against 18 example files
7. **Unit Tests** - Individual components and utilities
8. **Performance** - Scalability and stress tests

## Documentation

See **[TEST_COVERAGE.md](TEST_COVERAGE.md)** for:
- Detailed test descriptions
- Test strategy and coverage goals
- How to add new tests
- CI/CD integration
- Comparison with original tests

## Coverage

Current test coverage:
- **Basic Functionality**: 100%
- **Advanced Features**: 100%
- **Edge Cases**: ~90%
- **Error Handling**: ~85%
- **Integration**: ~80%
- **Regression**: 100% (all 18 example files)

## Contributing

When adding new tests:

1. Place tests in appropriate category
2. Add clear docstrings
3. Use existing fixtures
4. Mock external dependencies
5. Run full suite before committing
6. Update TEST_COVERAGE.md

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
test:
  script:
    - pip install -r tests/requirements-test.txt
    - pytest tests/test_rule_assistant_comprehensive.py --cov=CreateApertiumRules
```

## Getting Help

- See TEST_COVERAGE.md for detailed documentation
- Check conftest.py for available fixtures
- Look at existing tests for examples
- Review pytest documentation: https://docs.pytest.org/
