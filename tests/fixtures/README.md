# Test Fixtures Directory
**Purpose:** Test data and fixtures for FLExTrans Rule Assistant testing

## Directory Structure

```
fixtures/
├── README.md                           # This file
├── fr001/                              # FR-001: Section Preservation
│   ├── input_with_variables.t1x       # Transfer file with custom variables
│   ├── input_with_macros.t1x          # Transfer file with custom macros
│   ├── input_empty_sections.t1x       # Transfer file with empty sections
│   └── expected_*.t1x                  # Expected outputs
├── fr002/                              # FR-002: File Synchronization
│   ├── fresh_start_template.t1x       # Clean template
│   ├── session1_output.t1x            # After first RA session
│   ├── manually_edited.t1x            # After manual editing
│   └── session2_output.t1x            # After second RA session
├── fr003/                              # FR-003: Pre-populate Module
│   ├── clean_template.t1x             # Fresh from template
│   ├── populated_no_edits.t1x         # After pre-populate
│   └── manually_edited.t1x            # After manual edits
├── fr004/                              # FR-004: Templates
│   ├── minimal_template.t1x           # Minimal template
│   ├── standard_template.t1x          # Standard template
│   └── custom_template_example.t1x    # Example custom template
├── fr005/                              # FR-005: Error Messages
│   └── (warning message test data)
├── fr006/                              # FR-006: Reload FLEx Data
│   └── (FLEx database snapshots)
├── rules/                              # Rule Assistant XML files
│   ├── simple_def_noun.xml            # Simple determiner-noun rule
│   ├── adj_noun.xml                   # Adjective-noun rule
│   ├── complex_agreement.xml          # Complex agreement pattern
│   └── bantu_split.xml                # Bantu noun class rule
├── transfer/                           # Various transfer files
│   ├── minimal.t1x                    # Minimal valid transfer file
│   ├── standard.t1x                   # Standard populated file
│   └── complex.t1x                    # Complex multi-rule file
├── flex_mock/                          # Mock FLEx database data
│   ├── basic_db.json                  # Basic categories and features
│   ├── extended_db.json               # Extended with more features
│   └── bantu_db.json                  # Bantu language features
└── baselines/                          # Regression test baselines
    ├── Ex1a_Def-Noun.t1x.baseline     # Baseline for example 1a
    ├── Ex1b_Def-Noun.t1x.baseline     # Baseline for example 1b
    └── ...                             # Baselines for all 22 examples
```

## Usage

### Using Fixtures in Tests

```python
import pytest
import os

@pytest.fixture
def fr001_input_with_variables():
    """Provide path to FR-001 test file with variables."""
    return os.path.join(
        os.path.dirname(__file__),
        'fixtures/fr001/input_with_variables.t1x'
    )

def test_preserve_variables(fr001_input_with_variables):
    """Test using the fixture."""
    # Use the fixture path
    process_file(fr001_input_with_variables)
```

### Creating New Fixtures

1. **Create the fixture file** in appropriate subdirectory
2. **Document the fixture** in this README
3. **Add corresponding test** that uses it
4. **Commit both fixture and test** together

### Fixture Naming Conventions

**Transfer Files:**
- `input_*.t1x` - Input files for tests
- `expected_*.t1x` - Expected output files
- `*.t1x.baseline` - Regression test baselines

**Rule Assistant XML:**
- `simple_*.xml` - Simple single-pattern rules
- `complex_*.xml` - Complex multi-pattern rules
- `*_example.xml` - Example rules for documentation

**FLEx Mock Data:**
- `*_db.json` - Mock database JSON files
- Include minimal data needed for tests

## Fixture Descriptions

### FR-001 Fixtures

#### `input_with_variables.t1x`
Transfer file containing:
- Standard sections (cats, attrs, rules)
- Custom variables section with 2 user-defined variables
- Used to verify variables are preserved after RA processing

#### `input_with_macros.t1x`
Transfer file containing:
- Standard sections
- Custom macros section with 2 user-defined macros
- Used to verify macros are preserved after RA processing

#### `input_empty_sections.t1x`
Transfer file with empty but present sections:
- `<section-def-vars/>` (empty)
- `<section-def-macros/>` (empty)
- Used to verify empty sections not deleted

### FR-002 Fixtures

#### `fresh_start_template.t1x`
Clean template file for starting new project:
- Minimal required sections
- No language-specific data
- Used for fresh start workflow tests

#### `session1_output.t1x`
Output from first RA session:
- Contains 2 RA-generated rules
- Has RA comment markers
- Used to test reloading RA-generated content

#### `manually_edited.t1x`
File after manual editing:
- Based on session1_output.t1x
- Has custom additions
- Lacks RA comment markers on custom parts
- Used to test manual edit detection

### FR-003 Fixtures

#### `clean_template.t1x`
Fresh template before pre-populate:
- Only structure, no attributes
- Used to test pre-populate on clean file

#### `populated_no_edits.t1x`
After running pre-populate once:
- Has standard categories and attributes
- No manual edits
- Used to test re-running pre-populate

### FR-004 Fixtures

#### `minimal_template.t1x`
Minimal template (no language-specific data):
- Only essential structure
- No features from any language
- Clean slate for users

#### `standard_template.t1x`
Standard template with common sections:
- Common categories pre-populated
- Still language-neutral
- Useful starting point

### Rule Assistant XML Fixtures

#### `simple_def_noun.xml`
Simplest possible rule:
- Determiner + Noun
- No feature agreement
- Used for basic tests

#### `adj_noun.xml`
Rule with agreement:
- Adjective + Noun
- Gender and number agreement
- Used for agreement tests

#### `complex_agreement.xml`
Complex multi-feature agreement:
- Multiple words
- Multiple features
- Ranked features
- Used for advanced tests

### FLEx Mock Data

#### `basic_db.json`
Minimal FLEx database:
```json
{
  "project_name": "BasicTest",
  "categories": {
    "n": "noun",
    "adj": "adjective",
    "def": "determiner"
  },
  "features": {
    "gender": ["m", "f"],
    "number": ["sg", "pl"]
  }
}
```

#### `extended_db.json`
Extended with more features:
```json
{
  "project_name": "ExtendedTest",
  "categories": {
    "n": "noun",
    "adj": "adjective",
    "def": "determiner",
    "v": "verb"
  },
  "features": {
    "gender": ["m", "f", "neut"],
    "number": ["sg", "pl"],
    "tense": ["past", "present", "future"],
    "politeness": ["formal", "informal"]
  }
}
```

## Baseline Management

### Creating Baselines

```bash
# Generate baselines for all examples
cd /home/user/FLExTrans
python tests/scripts/generate_baselines.py

# Or manually for single file
python test_rule_assistant.py --baseline=tests/fixtures/baselines
```

### Updating Baselines

**Only update baselines when:**
1. Intentional behavior change
2. Format change (non-semantic)
3. Optimization (same semantics, different structure)

**Process:**
1. Review changes carefully
2. Document reason for baseline update
3. Update baseline file
4. Update baseline change log (below)
5. Commit with clear message

### Baseline Change Log

| Date | File | Reason | Commit |
|------|------|--------|--------|
| 2025-11-22 | (all) | Initial baselines created | abc123 |
| | | | |

## Mock FLEx Database Format

Mock databases are JSON files with this structure:

```json
{
  "project_name": "TestProject",
  "categories": {
    "cat_id": "category_name"
  },
  "features": {
    "feature_label": ["value1", "value2"]
  },
  "affixes": {
    "category": {
      "feature": [
        {"gloss": "AFFIX_GLOSS", "value": "feature_value"}
      ]
    }
  },
  "lemmas": {
    "category": {
      "feature": [
        {"lemma": "lemma1.1", "value": "feature_value"}
      ]
    }
  }
}
```

## Fixture Validation

### Validation Script

```python
# tests/scripts/validate_fixtures.py

import os
import json
import xml.etree.ElementTree as ET

def validate_all_fixtures():
    """Validate all fixtures are well-formed."""
    fixture_dir = os.path.dirname(__file__) + '/../fixtures'

    # Validate all .t1x files are valid XML
    for root, dirs, files in os.walk(fixture_dir):
        for file in files:
            if file.endswith('.t1x'):
                filepath = os.path.join(root, file)
                try:
                    ET.parse(filepath)
                    print(f"✓ {file}")
                except ET.ParseError as e:
                    print(f"✗ {file}: {e}")

            # Validate all .json files are valid JSON
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath) as f:
                        json.load(f)
                    print(f"✓ {file}")
                except json.JSONDecodeError as e:
                    print(f"✗ {file}: {e}")

if __name__ == '__main__':
    validate_all_fixtures()
```

Run validation:
```bash
python tests/scripts/validate_fixtures.py
```

## Best Practices

### Creating Fixtures

1. **Keep fixtures minimal** - Only include what's needed for the test
2. **Use realistic data** - Fixtures should represent real usage
3. **Document thoroughly** - Explain what each fixture tests
4. **Version control** - Always commit fixtures with tests

### Using Fixtures

1. **Don't modify fixtures in tests** - Copy if you need to modify
2. **Use fixtures for both input and expected output**
3. **Clean up temporary files** - Use pytest fixtures with cleanup

### Maintaining Fixtures

1. **Review regularly** - Ensure fixtures stay relevant
2. **Update documentation** - Keep this README current
3. **Validate** - Run validation script regularly
4. **Archive obsolete fixtures** - Don't delete, move to archive/

## Fixture Cleanup

Temporary files created during tests should be cleaned up:

```python
@pytest.fixture
def temp_workspace():
    """Create temporary directory for test outputs."""
    tmpdir = tempfile.mkdtemp(prefix='ra_test_')
    yield tmpdir
    shutil.rmtree(tmpdir)  # Cleanup
```

## Future Fixtures

**Planned additions:**
- [ ] More complex Rule Assistant XML examples
- [ ] Fixtures for infix/circumfix support (when implemented)
- [ ] Larger mock FLEx databases
- [ ] Performance test data (large rulesets)
- [ ] Malformed XML test cases
- [ ] Edge case transfer files

---

**Last Updated:** 2025-11-22
**Maintainer:** QC Agent
