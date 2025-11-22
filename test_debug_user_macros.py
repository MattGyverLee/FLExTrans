#!/usr/bin/env python3
"""
Test scenario: User has custom macros/variables that should be preserved.
This simulates a real Rule Assistant workflow where overwrite_rules='yes'.
"""

import sys
import os
import tempfile
import xml.etree.ElementTree as ET
from unittest.mock import Mock

# Mock PyQt5 before importing CreateApertiumRules
sys.modules['PyQt5'] = Mock()
sys.modules['PyQt5.QtCore'] = Mock()

# Add Dev/Lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Dev', 'Lib'))

# Mock Utils module
sys.modules['flextoolslib'] = Mock()

# Mock Utils functions
utils_mock = Mock()
utils_mock.getCategoryHierarchy = Mock(return_value={})
utils_mock.underscores = Mock(side_effect=lambda x: x)
sys.modules['Utils'] = utils_mock

from CreateApertiumRules import RuleGenerator

class MockReport:
    def Info(self, msg): print(f"INFO: {msg}")
    def Warning(self, msg): print(f"WARNING: {msg}")
    def Error(self, msg): print(f"ERROR: {msg}")

class MockDB:
    def __init__(self):
        self.hierarchy = {}

# Template with user-defined variables and macros
TEMPLATE_WITH_USER_CONTENT = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE transfer PUBLIC "-//XMLmind//DTD transfer//EN" "transfer.dtd">
<transfer>
<section-def-cats>
<def-cat n="c_n">
<cat-item tags="n"/>
<cat-item tags="n.*"/>
</def-cat>
</section-def-cats>
<section-def-attrs>
<def-attr n="a_num">
<attr-item tags="sg"/>
<attr-item tags="pl"/>
</def-attr>
</section-def-attrs>
<section-def-vars>
<!-- User's custom variable for their hand-written rules -->
<def-var n="v_my_custom_var"/>
</section-def-vars>
<section-def-lists>
</section-def-lists>
<section-def-macros>
<!-- User's custom macro for post-processing -->
<def-macro n="m_my_custom_postprocess" npar="1">
<let>
<var n="v_my_custom_var"/>
<clip pos="1" side="tl" part="lem"/>
</let>
</def-macro>
</section-def-macros>
<section-rules>
<!-- This rule will be deleted when overwrite_rules='yes' -->
<rule comment="OLD_RULE">
<pattern>
<pattern-item n="c_n"/>
</pattern>
<action>
<out><lu><lit-tag v="n"/></lu></out>
</action>
</rule>
</section-rules>
</transfer>
"""

def test_user_content_preservation():
    """Test that user's custom macros/variables are lost when rules are overwritten."""

    print("\n=== Testing User Content Preservation Issue ===\n")
    print("SCENARIO: User has custom variables/macros for their hand-written rules.")
    print("They run Rule Assistant with overwrite_rules='yes'.")
    print("EXPECTED: Custom content should be preserved.")
    print("ACTUAL: Let's see what happens...\n")

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.t1x', delete=False) as f:
        f.write(TEMPLATE_WITH_USER_CONTENT)
        input_file = f.name

    try:
        # Simulate Rule Assistant workflow
        report = MockReport()
        sourceDB = MockDB()
        targetDB = MockDB()
        configMap = {}

        generator = RuleGenerator(sourceDB, targetDB, report, configMap)

        print(f"1. Load existing transfer file with user's custom content")
        generator.ProcessExistingTransferFile(input_file)

        print(f"\n2. Initial state:")
        print(f"   Variables: {list(generator.variables.keys())}")
        var_section = generator.GetSection('section-def-vars')
        macro_section = generator.GetSection('section-def-macros')
        print(f"   section-def-vars has {len(var_section)} items:")
        for child in var_section:
            if child.tag == 'def-var':
                print(f"      - {child.get('n')}")
        print(f"   section-def-macros has {len(macro_section)} items:")
        for child in macro_section:
            if child.tag == 'def-macro':
                print(f"      - {child.get('n')}")

        print(f"\n3. Simulate overwrite_rules='yes' by calling TrimUnused()")
        print(f"   (This is called in ProcessAssistantFile when delete_old=True)")
        generator.TrimUnused()

        print(f"\n4. After TrimUnused:")
        var_section = generator.GetSection('section-def-vars')
        macro_section = generator.GetSection('section-def-macros')
        print(f"   section-def-vars has {len(var_section)} items:")
        for child in var_section:
            if child.tag == 'def-var':
                print(f"      - {child.get('n')}")
        print(f"   section-def-macros has {len(macro_section)} items:")
        for child in macro_section:
            if child.tag == 'def-macro':
                print(f"      - {child.get('n')}")

        # Write output
        with tempfile.NamedTemporaryFile(mode='w', suffix='.t1x', delete=False) as f:
            output_file = f.name

        print(f"\n5. Write output file")
        generator.WriteTransferFile(output_file)

        # Check result
        tree = ET.parse(output_file)
        root = tree.getroot()

        sections_found = [child.tag for child in root]

        print(f"\n6. RESULT:")
        if 'section-def-vars' not in sections_found:
            print(f"   ✗ BUG CONFIRMED: section-def-vars was REMOVED!")
            print(f"      User's custom variable 'v_my_custom_var' is LOST!")
        else:
            print(f"   ✓ section-def-vars preserved")

        if 'section-def-macros' not in sections_found:
            print(f"   ✗ BUG CONFIRMED: section-def-macros was REMOVED!")
            print(f"      User's custom macro 'm_my_custom_postprocess' is LOST!")
        else:
            print(f"   ✓ section-def-macros preserved")

        print(f"\n7. Sections in output:")
        for child in root:
            print(f"   - {child.tag}")

        # Clean up
        os.unlink(output_file)

    finally:
        os.unlink(input_file)

if __name__ == '__main__':
    test_user_content_preservation()
