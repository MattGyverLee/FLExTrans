#!/usr/bin/env python3
"""
Quick debug script to reproduce the missing sections bug.
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

# Create a simple starting transfer file with all sections
STARTING_TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
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
<def-var n="v_existing_var"/>
</section-def-vars>
<section-def-lists>
<def-list n="l_existing_list">
<list-item v="item1"/>
</def-list>
</section-def-lists>
<section-def-macros>
<def-macro n="m_existing_macro" npar="1">
<let>
<var n="v_existing_var"/>
<lit v="test"/>
</let>
</def-macro>
</section-def-macros>
<section-rules>
</section-rules>
</transfer>
"""

def test_section_preservation():
    """Test that sections are preserved when processing an existing file."""

    print("\n=== Testing Section Preservation ===\n")

    # Create a temporary file with the starting template
    with tempfile.NamedTemporaryFile(mode='w', suffix='.t1x', delete=False) as f:
        f.write(STARTING_TEMPLATE)
        input_file = f.name

    try:
        # Create RuleGenerator and load existing file
        report = MockReport()
        sourceDB = MockDB()
        targetDB = MockDB()
        configMap = {}

        generator = RuleGenerator(sourceDB, targetDB, report, configMap)

        print(f"1. Loading existing file: {input_file}")
        generator.ProcessExistingTransferFile(input_file)

        print(f"\n2. After ProcessExistingTransferFile:")
        print(f"   - self.sections dict: {list(generator.sections.keys())}")
        print(f"   - self.variables dict: {list(generator.variables.keys())}")
        print(f"   - Root element has children: {len(generator.root)} elements")

        # Check what sections exist in the root
        print(f"\n3. Sections in root:")
        for child in generator.root:
            print(f"   - {child.tag}: {len(child)} children")

        # Now call GetSection for each section (simulating what WriteTransferFile does)
        print(f"\n4. Calling GetSection for each section (as WriteTransferFile does):")
        for section_name in RuleGenerator.SectionSequence:
            elem = generator.GetSection(section_name)
            print(f"   - {section_name}: {len(elem)} children")

        # Check self.sections again
        print(f"\n5. After calling GetSection for all sections:")
        print(f"   - self.sections dict: {list(generator.sections.keys())}")

        # Now write the file and see what happens
        with tempfile.NamedTemporaryFile(mode='w', suffix='.t1x', delete=False) as f:
            output_file = f.name

        print(f"\n6. Writing to output file: {output_file}")
        generator.WriteTransferFile(output_file)

        # Read the output and check what sections exist
        print(f"\n7. Sections in output file:")
        with open(output_file, 'r') as f:
            content = f.read()
            print(content)

        # Parse output and check sections
        tree = ET.parse(output_file)
        root = tree.getroot()

        print(f"\n8. Sections found in output:")
        sections_found = []
        for child in root:
            sections_found.append(child.tag)
            print(f"   - {child.tag}: {len(child)} children")

        # Check if variables and macros sections are present
        print(f"\n9. Results:")
        if 'section-def-vars' in sections_found:
            print(f"   ✓ section-def-vars PRESENT")
        else:
            print(f"   ✗ section-def-vars MISSING!")

        if 'section-def-macros' in sections_found:
            print(f"   ✓ section-def-macros PRESENT")
        else:
            print(f"   ✗ section-def-macros MISSING!")

        # Clean up
        os.unlink(output_file)

    finally:
        os.unlink(input_file)

if __name__ == '__main__':
    test_section_preservation()
