#!/usr/bin/env python3
"""
Test scenario where TrimUnused() might remove all content from sections.
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

# Create a transfer file with variables and macros that are NOT used in any rules
TEMPLATE_WITH_UNUSED = """<?xml version="1.0" encoding="utf-8"?>
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
<def-var n="v_unused_var"/>
</section-def-vars>
<section-def-lists>
</section-def-lists>
<section-def-macros>
<def-macro n="m_unused_macro" npar="1">
<let>
<var n="v_unused_var"/>
<lit v="test"/>
</let>
</def-macro>
</section-def-macros>
<section-rules>
<rule comment="test_rule">
<pattern>
<pattern-item n="c_n"/>
</pattern>
<action>
<out>
<lu>
<lit-tag v="n"/>
</lu>
</out>
</action>
</rule>
</section-rules>
</transfer>
"""

def test_trim_unused():
    """Test that sections become empty after TrimUnused() removes all content."""

    print("\n=== Testing TrimUnused Impact on Sections ===\n")

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.t1x', delete=False) as f:
        f.write(TEMPLATE_WITH_UNUSED)
        input_file = f.name

    try:
        # Create RuleGenerator and load existing file
        report = MockReport()
        sourceDB = MockDB()
        targetDB = MockDB()
        configMap = {}

        generator = RuleGenerator(sourceDB, targetDB, report, configMap)

        print(f"1. Loading existing file with unused variable and macro")
        generator.ProcessExistingTransferFile(input_file)

        print(f"\n2. Before TrimUnused:")
        print(f"   - Variables: {list(generator.variables.keys())}")
        for section_name in ['section-def-vars', 'section-def-macros']:
            elem = generator.GetSection(section_name)
            print(f"   - {section_name}: {len(elem)} children")
            for child in elem:
                if child.tag in ['def-var', 'def-macro']:
                    print(f"      - {child.tag} n='{child.get('n')}'")

        print(f"\n3. Calling TrimUnused():")
        generator.TrimUnused()

        print(f"\n4. After TrimUnused:")
        print(f"   - Variables: {list(generator.variables.keys())}")
        for section_name in ['section-def-vars', 'section-def-macros']:
            elem = generator.GetSection(section_name)
            print(f"   - {section_name}: {len(elem)} children")
            for child in elem:
                if child.tag in ['def-var', 'def-macro']:
                    print(f"      - {child.tag} n='{child.get('n')}'")

        # Now write the file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.t1x', delete=False) as f:
            output_file = f.name

        print(f"\n5. Writing to output file")
        generator.WriteTransferFile(output_file)

        # Check output
        tree = ET.parse(output_file)
        root = tree.getroot()

        print(f"\n6. Sections in output file:")
        sections_found = []
        for child in root:
            sections_found.append(child.tag)
            print(f"   - {child.tag}: {len(child)} children")

        print(f"\n7. Results:")
        if 'section-def-vars' in sections_found:
            print(f"   ✗ section-def-vars still PRESENT (should be removed when empty)")
        else:
            print(f"   ✓ section-def-vars correctly REMOVED (was empty)")

        if 'section-def-macros' in sections_found:
            print(f"   ✗ section-def-macros still PRESENT (should be removed when empty)")
        else:
            print(f"   ✓ section-def-macros correctly REMOVED (was empty)")

        # Show the actual output
        print(f"\n8. Output file content:")
        with open(output_file, 'r') as f:
            print(f.read())

        # Clean up
        os.unlink(output_file)

    finally:
        os.unlink(input_file)

if __name__ == '__main__':
    test_trim_unused()
