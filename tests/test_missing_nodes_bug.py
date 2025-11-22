"""
Test Suite for FR-001: Missing Nodes Bug

This module tests that variables and macros sections are preserved
when processing transfer files, even if they become unused.
"""

import os
import sys
import tempfile
import xml.etree.ElementTree as ET
from unittest.mock import Mock

# Make pytest optional
try:
    import pytest
except ImportError:
    pytest = None

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Dev', 'Lib'))

# Mock required modules before importing CreateApertiumRules
sys.modules['PyQt5'] = Mock()
sys.modules['PyQt5.QtCore'] = Mock()
sys.modules['flextoolslib'] = Mock()

utils_mock = Mock()
utils_mock.getCategoryHierarchy = Mock(return_value={})
utils_mock.underscores = Mock(side_effect=lambda x: x)
sys.modules['Utils'] = utils_mock

from CreateApertiumRules import RuleGenerator


class MockReport:
    """Mock reporter for testing without FLEx."""
    def __init__(self):
        self.infos = []
        self.warnings = []
        self.errors = []

    def Info(self, msg):
        self.infos.append(msg)

    def Warning(self, msg):
        self.warnings.append(msg)

    def Error(self, msg):
        self.errors.append(msg)


class MockDB:
    """Mock FLEx database for testing without FLEx."""
    def __init__(self):
        self.hierarchy = {}


# Only define fixtures if pytest is available
if pytest:
    @pytest.fixture
    def mock_report():
        """Provide a mock report object."""
        return MockReport()

    @pytest.fixture
    def mock_source_db():
        """Provide a mock source database."""
        return MockDB()

    @pytest.fixture
    def mock_target_db():
        """Provide a mock target database."""
        return MockDB()

    @pytest.fixture
    def temp_transfer_file():
        """Provide a temporary transfer file path."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.t1x', delete=False) as f:
            yield f.name
        # Cleanup
        if os.path.exists(f.name):
            os.unlink(f.name)


def create_generator(mock_report, mock_source_db, mock_target_db):
    """Helper to create a RuleGenerator instance."""
    return RuleGenerator(mock_source_db, mock_target_db, mock_report, {})


# ==============================================================================
# Test 1: Preserve sections with user-defined content
# ==============================================================================

def test_preserve_user_variables(mock_report, mock_source_db, mock_target_db, temp_transfer_file):
    """Test that user-defined variables are preserved after TrimUnused()."""

    # Create a transfer file with a user-defined variable
    template = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE transfer PUBLIC "-//XMLmind//DTD transfer//EN" "transfer.dtd">
<transfer>
<section-def-cats>
<def-cat n="c_n"><cat-item tags="n"/></def-cat>
</section-def-cats>
<section-def-attrs></section-def-attrs>
<section-def-vars>
<def-var n="v_user_variable"/>
</section-def-vars>
<section-def-lists></section-def-lists>
<section-def-macros></section-def-macros>
<section-rules></section-rules>
</transfer>
"""
    with open(temp_transfer_file, 'w') as f:
        f.write(template)

    # Load the file
    generator = create_generator(mock_report, mock_source_db, mock_target_db)
    generator.ProcessExistingTransferFile(temp_transfer_file)

    # Verify variable is tracked as original
    assert 'v_user_variable' in generator.originalVariables

    # Call TrimUnused (which would normally remove unused variables)
    generator.TrimUnused()

    # Verify variable is still present
    var_section = generator.GetSection('section-def-vars')
    var_names = [child.get('n') for child in var_section if child.tag == 'def-var']
    assert 'v_user_variable' in var_names

    # Write output and verify section is preserved
    output_file = temp_transfer_file + '.out'
    generator.WriteTransferFile(output_file)

    tree = ET.parse(output_file)
    root = tree.getroot()
    sections = [child.tag for child in root]

    assert 'section-def-vars' in sections
    os.unlink(output_file)


def test_preserve_user_macros(mock_report, mock_source_db, mock_target_db, temp_transfer_file):
    """Test that user-defined macros are preserved after TrimUnused()."""

    template = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE transfer PUBLIC "-//XMLmind//DTD transfer//EN" "transfer.dtd">
<transfer>
<section-def-cats>
<def-cat n="c_n"><cat-item tags="n"/></def-cat>
</section-def-cats>
<section-def-attrs></section-def-attrs>
<section-def-vars></section-def-vars>
<section-def-lists></section-def-lists>
<section-def-macros>
<def-macro n="m_user_macro" npar="1">
<let><var n="v_test"/><lit v="test"/></let>
</def-macro>
</section-def-macros>
<section-rules></section-rules>
</transfer>
"""
    with open(temp_transfer_file, 'w') as f:
        f.write(template)

    # Load the file
    generator = create_generator(mock_report, mock_source_db, mock_target_db)
    generator.ProcessExistingTransferFile(temp_transfer_file)

    # Verify macro is tracked as original
    assert 'm_user_macro' in generator.originalMacros

    # Call TrimUnused
    generator.TrimUnused()

    # Verify macro is still present
    macro_section = generator.GetSection('section-def-macros')
    macro_names = [child.get('n') for child in macro_section if child.tag == 'def-macro']
    assert 'm_user_macro' in macro_names

    # Write output and verify section is preserved
    output_file = temp_transfer_file + '.out'
    generator.WriteTransferFile(output_file)

    tree = ET.parse(output_file)
    root = tree.getroot()
    sections = [child.tag for child in root]

    assert 'section-def-macros' in sections
    os.unlink(output_file)


# ==============================================================================
# Test 2: Preserve empty sections from original file
# ==============================================================================

def test_preserve_empty_original_sections(mock_report, mock_source_db, mock_target_db, temp_transfer_file):
    """Test that empty sections from the original file are preserved."""

    template = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE transfer PUBLIC "-//XMLmind//DTD transfer//EN" "transfer.dtd">
<transfer>
<section-def-cats>
<def-cat n="c_n"><cat-item tags="n"/></def-cat>
</section-def-cats>
<section-def-attrs></section-def-attrs>
<section-def-vars></section-def-vars>
<section-def-lists></section-def-lists>
<section-def-macros></section-def-macros>
<section-rules></section-rules>
</transfer>
"""
    with open(temp_transfer_file, 'w') as f:
        f.write(template)

    # Load the file
    generator = create_generator(mock_report, mock_source_db, mock_target_db)
    generator.ProcessExistingTransferFile(temp_transfer_file)

    # Verify sections are tracked as original
    assert 'section-def-vars' in generator.originalSections
    assert 'section-def-macros' in generator.originalSections

    # Write output
    output_file = temp_transfer_file + '.out'
    generator.WriteTransferFile(output_file)

    # Verify empty sections are preserved
    tree = ET.parse(output_file)
    root = tree.getroot()
    sections = [child.tag for child in root]

    assert 'section-def-vars' in sections
    assert 'section-def-macros' in sections
    os.unlink(output_file)


# ==============================================================================
# Test 3: Remove empty sections NOT from original file
# ==============================================================================

def test_remove_empty_new_sections(mock_report, mock_source_db, mock_target_db):
    """Test that empty sections created during processing are removed."""

    # Create a generator without loading an existing file
    generator = create_generator(mock_report, mock_source_db, mock_target_db)
    generator.CreateTree()

    # At this point, all sections are new and empty
    assert len(generator.originalSections) == 0

    # Write output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.t1x', delete=False) as f:
        output_file = f.name

    try:
        generator.WriteTransferFile(output_file)

        # Verify empty sections were removed
        tree = ET.parse(output_file)
        root = tree.getroot()
        sections = [child.tag for child in root]

        # Empty sections should not be in output
        assert 'section-def-vars' not in sections
        assert 'section-def-macros' not in sections
        assert 'section-def-lists' not in sections
    finally:
        os.unlink(output_file)


# ==============================================================================
# Test 4: Mixed scenario - original and generated content
# ==============================================================================

def test_mixed_original_and_generated_content(mock_report, mock_source_db, mock_target_db, temp_transfer_file):
    """Test that original content is preserved while generated content can be removed."""

    template = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE transfer PUBLIC "-//XMLmind//DTD transfer//EN" "transfer.dtd">
<transfer>
<section-def-cats>
<def-cat n="c_n"><cat-item tags="n"/></def-cat>
</section-def-cats>
<section-def-attrs></section-def-attrs>
<section-def-vars>
<def-var n="v_original_var"/>
</section-def-vars>
<section-def-lists></section-def-lists>
<section-def-macros>
<def-macro n="m_original_macro" npar="1">
<let><var n="v_original_var"/><lit v="test"/></let>
</def-macro>
</section-def-macros>
<section-rules></section-rules>
</transfer>
"""
    with open(temp_transfer_file, 'w') as f:
        f.write(template)

    # Load the file
    generator = create_generator(mock_report, mock_source_db, mock_target_db)
    generator.ProcessExistingTransferFile(temp_transfer_file)

    # Add a new generated variable (not in original)
    generator.AddVariable('v_generated_var', 'Generated variable')

    # Call TrimUnused - should keep original but could remove generated
    generator.TrimUnused()

    # Verify original variable is preserved
    var_section = generator.GetSection('section-def-vars')
    var_names = [child.get('n') for child in var_section if child.tag == 'def-var']
    assert 'v_original_var' in var_names

    # Generated variable should be removed (not used)
    assert 'v_generated_var' not in var_names


# ==============================================================================
# Test 5: Regression test - ensure Bantu macros still preserved
# ==============================================================================

def test_preserve_bantu_macros(mock_report, mock_source_db, mock_target_db, temp_transfer_file):
    """Test that Bantu noun class macros are still preserved (regression test)."""

    template = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE transfer PUBLIC "-//XMLmind//DTD transfer//EN" "transfer.dtd">
<transfer>
<section-def-cats>
<def-cat n="c_n"><cat-item tags="n"/></def-cat>
</section-def-cats>
<section-def-attrs></section-def-attrs>
<section-def-vars>
<def-var n="v_Bantu_noun_class_from_n"/>
</section-def-vars>
<section-def-lists></section-def-lists>
<section-def-macros>
<def-macro n="m_Bantu_noun_class_from_n" npar="1">
<let><var n="v_Bantu_noun_class_from_n"/><lit v="test"/></let>
</def-macro>
</section-def-macros>
<section-rules></section-rules>
</transfer>
"""
    with open(temp_transfer_file, 'w') as f:
        f.write(template)

    # Load the file
    generator = create_generator(mock_report, mock_source_db, mock_target_db)
    generator.ProcessExistingTransferFile(temp_transfer_file)

    # Call TrimUnused
    generator.TrimUnused()

    # Verify Bantu items are preserved
    var_section = generator.GetSection('section-def-vars')
    var_names = [child.get('n') for child in var_section if child.tag == 'def-var']
    assert 'v_Bantu_noun_class_from_n' in var_names

    macro_section = generator.GetSection('section-def-macros')
    macro_names = [child.get('n') for child in macro_section if child.tag == 'def-macro']
    assert 'm_Bantu_noun_class_from_n' in macro_names


# ==============================================================================
# Test 6: Section structure preservation
# ==============================================================================

def test_section_structure_preserved(mock_report, mock_source_db, mock_target_db, temp_transfer_file):
    """Test that the complete section structure is preserved."""

    template = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE transfer PUBLIC "-//XMLmind//DTD transfer//EN" "transfer.dtd">
<transfer>
<section-def-cats></section-def-cats>
<section-def-attrs></section-def-attrs>
<section-def-vars></section-def-vars>
<section-def-lists></section-def-lists>
<section-def-macros></section-def-macros>
<section-rules></section-rules>
</transfer>
"""
    with open(temp_transfer_file, 'w') as f:
        f.write(template)

    # Load the file
    generator = create_generator(mock_report, mock_source_db, mock_target_db)
    generator.ProcessExistingTransferFile(temp_transfer_file)

    # Write output
    output_file = temp_transfer_file + '.out'
    generator.WriteTransferFile(output_file)

    # Verify all sections are preserved in correct order
    tree = ET.parse(output_file)
    root = tree.getroot()
    sections = [child.tag for child in root]

    expected_order = [
        'section-def-cats',
        'section-def-attrs',
        'section-def-vars',
        'section-def-lists',
        'section-def-macros',
        'section-rules'
    ]

    assert sections == expected_order
    os.unlink(output_file)


if __name__ == '__main__':
    # Run tests with pytest if available
    if pytest:
        pytest.main([__file__, '-v'])
    else:
        print("pytest not available. Run with: python run_missing_nodes_tests.py")
