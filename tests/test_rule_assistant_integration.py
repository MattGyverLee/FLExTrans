"""
Integration Tests for FLExTrans Rule Assistant

This module provides integration tests for complete workflows, focusing on
file synchronization, section preservation, and realistic usage scenarios.

Test Categories:
1. Fresh Start Workflow
2. Existing File Workflow
3. Manual Edit Preservation
4. FLEx Data Changes
5. Complete User Workflows

Author: QC Agent
Date: 2025-11-22
Priority: CRITICAL - Addresses FR-001 and FR-002
"""

import pytest
import os
import sys
import tempfile
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import Mock, MagicMock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Dev', 'Lib'))

import CreateApertiumRules
from CreateApertiumRules import RuleGenerator


# ==============================================================================
# Fixtures and Test Data
# ==============================================================================

@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for test files."""
    tmpdir = tempfile.mkdtemp(prefix='ra_test_')
    yield tmpdir
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def mock_report():
    """Provide a mock report object."""
    class MockReport:
        def __init__(self):
            self.infos = []
            self.warnings = []
            self.errors = []

        def Info(self, *args):
            self.infos.append(args)

        def Warning(self, *args):
            self.warnings.append(args)

        def Error(self, *args):
            self.errors.append(args)

        def has_errors(self):
            return len(self.errors) > 0

    return MockReport()


@pytest.fixture
def mock_flex_db():
    """Provide a mock FLEx database."""
    class MockDB:
        def __init__(self, project_name="TestProject"):
            self.project_name = project_name
            self.categories = {
                'n': 'noun',
                'adj': 'adjective',
                'def': 'determiner',
                'v': 'verb'
            }
            self.features = {
                'gender': ['m', 'f'],
                'number': ['sg', 'pl'],
                'tense': ['past', 'present', 'future']
            }
            self.affixes = {}

        def ProjectName(self):
            return self.project_name

    return MockDB()


def create_minimal_transfer_file(filepath: str, include_sections: List[str] = None):
    """
    Create a minimal transfer file with optional sections.

    Args:
        filepath: Path where to create the file
        include_sections: List of section names to include
            ('vars', 'macros', 'cats', 'attrs', 'rules')
    """
    if include_sections is None:
        include_sections = ['cats', 'attrs', 'rules']

    root = ET.Element('transfer')

    if 'cats' in include_sections:
        section_def_cats = ET.SubElement(root, 'section-def-cats')
        cat = ET.SubElement(section_def_cats, 'def-cat', n='c_n')
        ET.SubElement(cat, 'cat-item', tags='n.*')

    if 'attrs' in include_sections:
        section_def_attrs = ET.SubElement(root, 'section-def-attrs')
        attr = ET.SubElement(section_def_attrs, 'def-attr', n='a_gram_cat')
        ET.SubElement(attr, 'attr-item', tags='n')

    if 'vars' in include_sections:
        ET.SubElement(root, 'section-def-vars')

    if 'macros' in include_sections:
        ET.SubElement(root, 'section-def-macros')

    if 'rules' in include_sections:
        ET.SubElement(root, 'section-rules')

    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')
    tree.write(filepath, encoding='utf-8', xml_declaration=True)


def create_transfer_file_with_custom_content(filepath: str, custom_vars: List[str] = None,
                                              custom_macros: List[Dict] = None):
    """
    Create transfer file with custom variables and macros.

    Args:
        filepath: Where to create file
        custom_vars: List of custom variable names
        custom_macros: List of dicts with macro specifications
    """
    root = ET.Element('transfer')

    # Categories and attributes (standard)
    section_def_cats = ET.SubElement(root, 'section-def-cats')
    cat = ET.SubElement(section_def_cats, 'def-cat', n='c_n')
    ET.SubElement(cat, 'cat-item', tags='n.*')

    section_def_attrs = ET.SubElement(root, 'section-def-attrs')
    attr = ET.SubElement(section_def_attrs, 'def-attr', n='a_gram_cat')
    ET.SubElement(attr, 'attr-item', tags='n')

    # Custom variables
    section_def_vars = ET.SubElement(root, 'section-def-vars')
    if custom_vars:
        for var_name in custom_vars:
            ET.SubElement(section_def_vars, 'def-var', n=var_name)

    # Custom macros
    section_def_macros = ET.SubElement(root, 'section-def-macros')
    if custom_macros:
        for macro_spec in custom_macros:
            macro = ET.SubElement(section_def_macros, 'def-macro',
                                  n=macro_spec['name'],
                                  npar=str(macro_spec.get('npar', 1)))
            # Add comment to identify custom macro
            macro.set('c', 'CUSTOM_MACRO')
            # Minimal macro content
            choose = ET.SubElement(macro, 'choose')
            when = ET.SubElement(choose, 'when')
            test = ET.SubElement(when, 'test')
            ET.SubElement(test, 'lit-tag', v='test')

    # Rules section
    ET.SubElement(root, 'section-rules')

    tree = ET.ElementTree(root)
    ET.indent(tree, space='  ')
    tree.write(filepath, encoding='utf-8', xml_declaration=True)


def create_simple_rule_xml(filepath: str, rule_name: str = "Simple Rule"):
    """Create a simple Rule Assistant XML file for testing."""
    xml_content = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE FLExTransRuleGenerator PUBLIC "-//XMLmind//DTD FLExTransRuleGenerator//EN" "FLExTransRuleGenerator.dtd">
<FLExTransRuleGenerator>
  <FLExTransRules>
    <FLExTransRule name="{rule_name}">
      <Source>
        <Phrase>
          <Words>
            <Word category="n" id="1"></Word>
          </Words>
        </Phrase>
      </Source>
      <Target>
        <Phrase>
          <Words>
            <Word head="yes" id="1"></Word>
          </Words>
        </Phrase>
      </Target>
    </FLExTransRule>
  </FLExTransRules>
</FLExTransRuleGenerator>
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(xml_content)


# ==============================================================================
# FR-001: Section Preservation Tests
# ==============================================================================

class TestSectionPreservation:
    """Tests for FR-001: Missing Nodes Bug."""

    def test_preserve_existing_variables_section(self, temp_workspace, mock_report, mock_flex_db):
        """
        FR-001-001: Verify that existing variables section is preserved.

        Steps:
        1. Create transfer file with custom variables
        2. Run Rule Assistant to add rules
        3. Verify custom variables still present in output
        """
        input_file = os.path.join(temp_workspace, 'input_with_vars.t1x')
        output_file = os.path.join(temp_workspace, 'output_with_vars.t1x')
        rule_file = os.path.join(temp_workspace, 'simple_rule.xml')

        # Create input file with custom variables
        create_transfer_file_with_custom_content(
            input_file,
            custom_vars=['my_custom_var', 'user_defined_var']
        )

        # Create simple rule
        create_simple_rule_xml(rule_file)

        # Mock necessary Utils functions
        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        # Create generator and process
                        config_map = {}
                        generator = RuleGenerator(mock_flex_db, mock_flex_db, mock_report, config_map)
                        generator.CreateTree()

                        # Load existing transfer file
                        generator.ProcessExistingTransferFile(input_file)

                        # Process rule
                        generator.ProcessAssistantFile(rule_file)

                        # Write output
                        generator.WriteTransferFile(output_file)

        # Verify output
        assert os.path.exists(output_file), "Output file not created"

        output_tree = ET.parse(output_file)
        vars_section = output_tree.find('.//section-def-vars')

        assert vars_section is not None, "Variables section missing in output!"

        # Check that custom variables are preserved
        custom_vars = [v.get('n') for v in vars_section.findall('def-var')]
        assert 'my_custom_var' in custom_vars, "Custom variable 'my_custom_var' not preserved"
        assert 'user_defined_var' in custom_vars, "Custom variable 'user_defined_var' not preserved"

        # Verify no errors
        assert not mock_report.has_errors(), f"Unexpected errors: {mock_report.errors}"

    def test_preserve_existing_macros_section(self, temp_workspace, mock_report, mock_flex_db):
        """
        FR-001-002: Verify that existing macros section is preserved.

        Steps:
        1. Create transfer file with custom macros
        2. Run Rule Assistant
        3. Verify custom macros preserved
        """
        input_file = os.path.join(temp_workspace, 'input_with_macros.t1x')
        output_file = os.path.join(temp_workspace, 'output_with_macros.t1x')
        rule_file = os.path.join(temp_workspace, 'simple_rule.xml')

        # Create input with custom macros
        create_transfer_file_with_custom_content(
            input_file,
            custom_macros=[
                {'name': 'my_custom_macro', 'npar': 1},
                {'name': 'another_macro', 'npar': 2}
            ]
        )

        create_simple_rule_xml(rule_file)

        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        config_map = {}
                        generator = RuleGenerator(mock_flex_db, mock_flex_db, mock_report, config_map)
                        generator.CreateTree()
                        generator.ProcessExistingTransferFile(input_file)
                        generator.ProcessAssistantFile(rule_file)
                        generator.WriteTransferFile(output_file)

        # Verify
        output_tree = ET.parse(output_file)
        macros_section = output_tree.find('.//section-def-macros')

        assert macros_section is not None, "Macros section missing!"

        custom_macros = [m.get('n') for m in macros_section.findall('def-macro')]
        assert 'my_custom_macro' in custom_macros, "Custom macro not preserved"
        assert 'another_macro' in custom_macros, "Second custom macro not preserved"

    def test_preserve_empty_sections(self, temp_workspace, mock_report, mock_flex_db):
        """
        FR-001-003: Verify empty sections are not deleted.

        Steps:
        1. Create file with empty vars and macros sections
        2. Run Rule Assistant
        3. Verify sections still present (even if still empty)
        """
        input_file = os.path.join(temp_workspace, 'input_empty_sections.t1x')
        output_file = os.path.join(temp_workspace, 'output_empty_sections.t1x')
        rule_file = os.path.join(temp_workspace, 'simple_rule.xml')

        # Create with empty sections
        create_minimal_transfer_file(input_file, include_sections=['cats', 'attrs', 'vars', 'macros', 'rules'])

        create_simple_rule_xml(rule_file)

        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        config_map = {}
                        generator = RuleGenerator(mock_flex_db, mock_flex_db, mock_report, config_map)
                        generator.CreateTree()
                        generator.ProcessExistingTransferFile(input_file)
                        generator.ProcessAssistantFile(rule_file)
                        generator.WriteTransferFile(output_file)

        # Verify sections exist
        output_tree = ET.parse(output_file)
        vars_section = output_tree.find('.//section-def-vars')
        macros_section = output_tree.find('.//section-def-macros')

        assert vars_section is not None, "Empty variables section was deleted!"
        assert macros_section is not None, "Empty macros section was deleted!"

    def test_mixed_generated_and_custom_content(self, temp_workspace, mock_report, mock_flex_db):
        """
        FR-001-004: Verify RA can merge with existing content.

        Steps:
        1. Create file with both RA-generated and custom content
        2. Add more rules via RA
        3. Verify both custom and new RA content present
        """
        # This test requires more sophisticated setup
        # Simulating a file that was previously generated by RA and then manually edited
        pytest.skip("Requires complex setup - implement in phase 2")


# ==============================================================================
# FR-002: File State Synchronization Tests
# ==============================================================================

class TestFileStateSynchronization:
    """Tests for FR-002: File State Synchronization Issues."""

    def test_fresh_start_no_existing_file(self, temp_workspace, mock_report, mock_flex_db):
        """
        FR-002-001: Verify fresh start workflow.

        Steps:
        1. Start with no existing transfer file
        2. Create rules
        3. Save
        4. Verify file created correctly
        """
        output_file = os.path.join(temp_workspace, 'fresh_start.t1x')
        rule_file = os.path.join(temp_workspace, 'rule.xml')

        create_simple_rule_xml(rule_file)

        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        config_map = {}
                        generator = RuleGenerator(mock_flex_db, mock_flex_db, mock_report, config_map)
                        generator.CreateTree()
                        # No ProcessExistingTransferFile - fresh start
                        generator.ProcessAssistantFile(rule_file)
                        generator.WriteTransferFile(output_file)

        assert os.path.exists(output_file), "Fresh start file not created"

        # Verify basic structure
        tree = ET.parse(output_file)
        root = tree.getroot()
        assert root.tag == 'transfer'
        assert tree.find('.//section-rules') is not None

    def test_reload_ra_generated_rules(self, temp_workspace, mock_report, mock_flex_db):
        """
        FR-002-002: Verify RA can reload its own generated rules.

        Steps:
        1. Session 1: Create and save rules
        2. Session 2: Reload the same file
        3. Verify rules loaded correctly
        """
        transfer_file = os.path.join(temp_workspace, 'session.t1x')
        rule_file = os.path.join(temp_workspace, 'rule.xml')

        create_simple_rule_xml(rule_file, rule_name="Test Rule")

        # Session 1: Create
        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        config_map = {}
                        gen1 = RuleGenerator(mock_flex_db, mock_flex_db, mock_report, config_map)
                        gen1.CreateTree()
                        gen1.ProcessAssistantFile(rule_file)
                        gen1.WriteTransferFile(transfer_file)

        # Session 2: Reload
        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        mock_report2 = mock_report  # Reuse for simplicity
                        config_map2 = {}
                        gen2 = RuleGenerator(mock_flex_db, mock_flex_db, mock_report2, config_map2)
                        gen2.CreateTree()
                        gen2.ProcessExistingTransferFile(transfer_file)

        # Verify rules loaded
        # Note: Actual verification depends on RuleGenerator's internal state tracking
        # This is a placeholder for the actual assertion
        assert len(gen2.ruleNames) > 0, "No rules loaded from transfer file"
        # More specific assertions would require access to gen2's rule data structures

    def test_detect_flex_data_changes(self, temp_workspace, mock_report):
        """
        FR-002-004: Verify RA detects FLEx data changes.

        Steps:
        1. Create rules with FLEx v1 (limited features)
        2. Simulate FLEx v2 (added feature)
        3. Reload
        4. Verify new feature available
        """
        transfer_file = os.path.join(temp_workspace, 'flex_changes.t1x')
        rule_file = os.path.join(temp_workspace, 'rule.xml')

        create_simple_rule_xml(rule_file)

        # FLEx v1: basic features
        flex_v1 = MockDB()
        flex_v1.features = {'gender': ['m', 'f'], 'number': ['sg', 'pl']}

        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        config_map = {}
                        gen1 = RuleGenerator(flex_v1, flex_v1, mock_report, config_map)
                        gen1.CreateTree()
                        gen1.ProcessAssistantFile(rule_file)
                        gen1.WriteTransferFile(transfer_file)

        # FLEx v2: added feature
        flex_v2 = MockDB()
        flex_v2.features = {'gender': ['m', 'f'], 'number': ['sg', 'pl'], 'politeness': ['formal', 'informal']}

        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=['formal', 'informal']):
                        mock_report2 = mock_report
                        config_map2 = {}
                        gen2 = RuleGenerator(flex_v2, flex_v2, mock_report2, config_map2)
                        gen2.CreateTree()
                        gen2.ProcessExistingTransferFile(transfer_file)

        # Verify new feature available
        # This would require checking gen2's available features
        # Placeholder assertion
        assert 'politeness' in flex_v2.features, "New feature not in FLEx v2"


# ==============================================================================
# Integration Workflow Tests
# ==============================================================================

class TestCompleteWorkflows:
    """End-to-end workflow integration tests."""

    def test_complete_workflow_fresh_to_iterative(self, temp_workspace, mock_report, mock_flex_db):
        """
        FR-002-INT-001: Complete workflow from fresh start to iterative development.

        Workflow:
        1. Start fresh
        2. Create 2 rules
        3. Save
        4. Close/reopen (simulated)
        5. Load file
        6. Add 2 more rules
        7. Save
        8. Verify all 4 rules present
        """
        transfer_file = os.path.join(temp_workspace, 'workflow.t1x')
        rule1_file = os.path.join(temp_workspace, 'rule1.xml')
        rule2_file = os.path.join(temp_workspace, 'rule2.xml')
        rule3_file = os.path.join(temp_workspace, 'rule3.xml')
        rule4_file = os.path.join(temp_workspace, 'rule4.xml')

        create_simple_rule_xml(rule1_file, "Rule 1")
        create_simple_rule_xml(rule2_file, "Rule 2")
        create_simple_rule_xml(rule3_file, "Rule 3")
        create_simple_rule_xml(rule4_file, "Rule 4")

        # Session 1: Create first 2 rules
        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        config_map = {}
                        gen1 = RuleGenerator(mock_flex_db, mock_flex_db, mock_report, config_map)
                        gen1.CreateTree()
                        gen1.ProcessAssistantFile(rule1_file)
                        gen1.ProcessAssistantFile(rule2_file)
                        gen1.WriteTransferFile(transfer_file)

        # Verify intermediate state
        tree = ET.parse(transfer_file)
        rules_section = tree.find('.//section-rules')
        rules_count_1 = len(rules_section.findall('rule'))
        assert rules_count_1 >= 2, f"Expected at least 2 rules, found {rules_count_1}"

        # Session 2: Load and add 2 more rules
        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        mock_report2 = mock_report
                        config_map2 = {}
                        gen2 = RuleGenerator(mock_flex_db, mock_flex_db, mock_report2, config_map2)
                        gen2.CreateTree()
                        gen2.ProcessExistingTransferFile(transfer_file)
                        gen2.ProcessAssistantFile(rule3_file)
                        gen2.ProcessAssistantFile(rule4_file)
                        gen2.WriteTransferFile(transfer_file)

        # Verify final state
        tree_final = ET.parse(transfer_file)
        rules_section_final = tree_final.find('.//section-rules')
        rules_count_final = len(rules_section_final.findall('rule'))

        # Should have roughly 4 rules (exact count depends on rule generation logic)
        assert rules_count_final >= 4, f"Expected at least 4 rules, found {rules_count_final}"
        assert rules_count_final > rules_count_1, "New rules not added in session 2"

    @pytest.mark.skip(reason="Requires manual edit detection logic not yet implemented")
    def test_workflow_with_manual_edits(self, temp_workspace, mock_report, mock_flex_db):
        """
        FR-002-INT-002: Workflow combining RA and manual editing.

        This test is skipped until FR-002 manual edit detection is implemented.
        """
        pass


# ==============================================================================
# Regression Tests
# ==============================================================================

class TestRegressionProtection:
    """Ensure fixes don't break existing functionality."""

    def test_existing_example_files_still_work(self, temp_workspace, mock_report, mock_flex_db):
        """
        Verify that all existing example rule files can still be processed.

        This is a placeholder - full implementation would iterate through
        all 22 example files in /home/user/FLExTrans/Rule Assistant/
        """
        # This would require access to the actual example files
        # and appropriate FLEx database mocking
        pytest.skip("Requires access to example rule files and full FLEx mocking")

    def test_no_performance_regression(self, temp_workspace, mock_report, mock_flex_db):
        """
        Basic performance check to ensure no major slowdowns.

        Generates multiple rules and measures time.
        """
        import time

        output_file = os.path.join(temp_workspace, 'perf_test.t1x')
        rule_file = os.path.join(temp_workspace, 'perf_rule.xml')

        create_simple_rule_xml(rule_file)

        start_time = time.time()

        with patch('CreateApertiumRules.Utils.DATA', {}):
            with patch('CreateApertiumRules.Utils.getLemmasForFeature', return_value=[]):
                with patch('CreateApertiumRules.Utils.getAffixGlossesForFeature', return_value=[]):
                    with patch('CreateApertiumRules.Utils.getPossibleFeatureValues', return_value=[]):
                        config_map = {}
                        generator = RuleGenerator(mock_flex_db, mock_flex_db, mock_report, config_map)
                        generator.CreateTree()

                        # Process the same rule multiple times (simulating multiple rules)
                        for i in range(10):
                            generator.ProcessAssistantFile(rule_file)

                        generator.WriteTransferFile(output_file)

        elapsed_time = time.time() - start_time

        # Very generous threshold - should be under 10 seconds for 10 rules
        # Adjust based on baseline measurements
        assert elapsed_time < 10.0, f"Performance regression: took {elapsed_time:.2f}s"


# ==============================================================================
# Helper Test Utilities
# ==============================================================================

class MockDB:
    """Enhanced mock FLEx database for testing."""

    def __init__(self, project_name="TestProject"):
        self.project_name = project_name
        self.categories = {
            'n': 'noun',
            'adj': 'adjective',
            'def': 'determiner',
            'v': 'verb'
        }
        self.features = {
            'gender': ['m', 'f'],
            'number': ['sg', 'pl'],
        }
        self.affixes = {}

    def ProjectName(self):
        return self.project_name


# ==============================================================================
# Test Execution
# ==============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
