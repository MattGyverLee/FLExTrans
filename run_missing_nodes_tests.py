#!/usr/bin/env python3
"""
Simple test runner for FR-001 missing nodes bug tests.
Runs tests without requiring pytest.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Dev', 'Lib'))

# Mock required modules
from unittest.mock import Mock
sys.modules['PyQt5'] = Mock()
sys.modules['PyQt5.QtCore'] = Mock()
sys.modules['flextoolslib'] = Mock()
utils_mock = Mock()
utils_mock.getCategoryHierarchy = Mock(return_value={})
utils_mock.underscores = Mock(side_effect=lambda x: x)
sys.modules['Utils'] = utils_mock

from tests.test_missing_nodes_bug import (
    test_preserve_user_variables,
    test_preserve_user_macros,
    test_preserve_empty_original_sections,
    test_remove_empty_new_sections,
    test_mixed_original_and_generated_content,
    test_preserve_bantu_macros,
    test_section_structure_preserved,
    MockReport, MockDB
)

import tempfile

def run_tests():
    """Run all tests and report results."""

    tests = [
        ("Preserve user variables", test_preserve_user_variables),
        ("Preserve user macros", test_preserve_user_macros),
        ("Preserve empty original sections", test_preserve_empty_original_sections),
        ("Remove empty new sections", test_remove_empty_new_sections),
        ("Mixed original and generated content", test_mixed_original_and_generated_content),
        ("Preserve Bantu macros", test_preserve_bantu_macros),
        ("Section structure preserved", test_section_structure_preserved),
    ]

    passed = 0
    failed = 0
    errors = []

    print("\n" + "="*70)
    print("Running FR-001 Missing Nodes Bug Tests")
    print("="*70 + "\n")

    for test_name, test_func in tests:
        try:
            # Create fixtures
            report = MockReport()
            source_db = MockDB()
            target_db = MockDB()

            # Create temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.t1x', delete=False) as f:
                temp_file = f.name

            try:
                # Run test
                test_func(report, source_db, target_db, temp_file)
                print(f"✓ PASS: {test_name}")
                passed += 1
            finally:
                # Cleanup
                if os.path.exists(temp_file):
                    os.unlink(temp_file)

        except Exception as e:
            print(f"✗ FAIL: {test_name}")
            print(f"  Error: {str(e)}")
            failed += 1
            errors.append((test_name, e))

    print("\n" + "="*70)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*70 + "\n")

    if errors:
        print("Failed tests:")
        for test_name, error in errors:
            print(f"  - {test_name}: {error}")
        print()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(run_tests())
