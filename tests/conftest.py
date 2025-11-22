"""
Pytest configuration and shared fixtures for FLExTrans Rule Assistant tests.

This file contains pytest configuration and fixtures that are shared across
multiple test files.
"""

import pytest
import sys
import os

# Add the Dev/Lib directory to the Python path so we can import modules
# This allows tests to run from anywhere
dev_lib_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Dev', 'Lib')
if dev_lib_path not in sys.path:
    sys.path.insert(0, dev_lib_path)


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests"
    )
    config.addinivalue_line(
        "markers", "requires_apertium: marks tests that require Apertium tools"
    )


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture(scope="session")
def rule_assistant_dir(project_root):
    """Return the Rule Assistant examples directory."""
    return os.path.join(project_root, 'Rule Assistant')


@pytest.fixture(scope="session")
def dev_lib_dir(project_root):
    """Return the Dev/Lib directory."""
    return os.path.join(project_root, 'Dev', 'Lib')
