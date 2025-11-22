# Feature Request Test Plans
**Date:** 2025-11-22
**Author:** QC Agent
**Purpose:** Detailed test plans for FR-001 through FR-006

---

## Table of Contents

1. [FR-001: Missing Nodes Bug](#fr-001-missing-nodes-bug)
2. [FR-002: File State Synchronization](#fr-002-file-state-synchronization)
3. [FR-003: Confusing Pre-populate Error](#fr-003-confusing-pre-populate-error)
4. [FR-004: Template Management System](#fr-004-template-management-system)
5. [FR-005: Clearer BantuNounClass Warning](#fr-005-clearer-bantunounclass-warning)
6. [FR-006: FLEx Data Reload Button](#fr-006-flex-data-reload-button)

---

## FR-001: Missing Nodes Bug

### Overview

**Feature Request:** Variables and Macros sections disappearing after Rule Assistant run
**Priority:** CRITICAL
**Type:** Bug Fix
**Risk:** Data Loss

### Acceptance Criteria

- [ ] Existing `<section-def-vars>` preserved when running Rule Assistant
- [ ] Existing `<section-def-macros>` preserved when running Rule Assistant
- [ ] Custom variables not overwritten or deleted
- [ ] Custom macros not overwritten or deleted
- [ ] Empty sections preserved if present in source file
- [ ] Regression test ensures fix stays working

### Test Scenarios

#### Test Plan FR-001-001: Preserve Existing Variables Section

**Objective:** Verify that an existing variables section is preserved

**Preconditions:**
- Transfer file contains `<section-def-vars>` with custom variables
- Variables section has 2+ variable definitions
- FLEx project is accessible

**Test Steps:**
1. Create transfer file `test_variables.t1x` with:
   ```xml
   <section-def-vars>
     <def-var n="my_custom_var"/>
     <def-var n="user_defined_var"/>
   </section-def-vars>
   ```
2. Open Rule Assistant
3. Load existing transfer file
4. Create one new simple rule (e.g., Def-Noun)
5. Save transfer file
6. Parse output transfer file

**Expected Results:**
- ✅ `<section-def-vars>` section exists in output
- ✅ `my_custom_var` still present
- ✅ `user_defined_var` still present
- ✅ Any new Rule Assistant variables added (not replacing custom ones)
- ✅ Section order preserved or logical

**Test Data:**
- `fixtures/fr001/input_with_variables.t1x`
- `fixtures/fr001/expected_output_with_variables.t1x`

**Automation:**
```python
def test_preserve_existing_variables_section():
    """FR-001-001: Variables section should be preserved."""
    input_file = "fixtures/fr001/input_with_variables.t1x"
    output_file = "temp/output_variables.t1x"

    # Load input with custom variables
    generator = create_generator_from_file(input_file)

    # Add a simple rule
    generator.ProcessAssistantFile("fixtures/simple_def_noun.xml")

    # Write output
    generator.WriteTransferFile(output_file)

    # Parse and verify
    output_tree = ET.parse(output_file)
    vars_section = output_tree.find('.//section-def-vars')

    assert vars_section is not None, "Variables section missing!"

    # Check custom variables preserved
    custom_vars = [v.get('n') for v in vars_section.findall('def-var')]
    assert 'my_custom_var' in custom_vars
    assert 'user_defined_var' in custom_vars
```

---

#### Test Plan FR-001-002: Preserve Existing Macros Section

**Objective:** Verify that an existing macros section is preserved

**Preconditions:**
- Transfer file contains `<section-def-macros>` with custom macros
- Macros section has 2+ macro definitions
- FLEx project is accessible

**Test Steps:**
1. Create transfer file with custom macros:
   ```xml
   <section-def-macros>
     <def-macro n="my_custom_macro" npar="1">
       <choose>
         <when><test>...</test></when>
       </choose>
     </def-macro>
   </section-def-macros>
   ```
2. Open Rule Assistant
3. Load existing transfer file
4. Create one new rule requiring a macro
5. Save transfer file
6. Parse output

**Expected Results:**
- ✅ `<section-def-macros>` exists
- ✅ Custom macros preserved
- ✅ New RA-generated macros added (not replacing)
- ✅ No duplicate macros
- ✅ Macro IDs don't conflict

**Test Data:**
- `fixtures/fr001/input_with_macros.t1x`
- `fixtures/fr001/expected_output_with_macros.t1x`

**Automation:** Similar to FR-001-001

---

#### Test Plan FR-001-003: Preserve Empty Sections

**Objective:** Verify empty sections are not deleted

**Preconditions:**
- Transfer file has empty `<section-def-vars/>` and `<section-def-macros/>`

**Test Steps:**
1. Create transfer file with empty sections
2. Run Rule Assistant
3. Save output
4. Verify sections still present (even if empty)

**Expected Results:**
- ✅ Empty sections preserved
- ✅ Sections not removed due to being empty
- ✅ If content added, sections populated correctly

**Automation:**
```python
def test_preserve_empty_sections():
    """FR-001-003: Empty sections should not be deleted."""
    # ... implementation
```

---

#### Test Plan FR-001-004: Mixed Generated and Custom Content

**Objective:** Verify Rule Assistant can merge with existing content

**Preconditions:**
- Transfer file has mix of RA-generated and hand-written macros/variables

**Test Steps:**
1. Create file with both RA and custom content
2. Run Rule Assistant
3. Verify both preserved and merged correctly

**Expected Results:**
- ✅ RA-generated content updated if needed
- ✅ Custom content preserved
- ✅ No conflicts or duplicates

---

#### Test Plan FR-001-005: Edge Case - Section Present But Commented Out

**Objective:** Test handling of commented sections

**Test Steps:**
1. Create file with:
   ```xml
   <!--
   <section-def-vars>
     <def-var n="commented_var"/>
   </section-def-vars>
   -->
   ```
2. Run Rule Assistant
3. Check if commented section interferes

**Expected Results:**
- ✅ Commented sections ignored (not parsed)
- ✅ New sections created as needed
- ✅ No parsing errors

---

### Regression Tests

**After Fix Implementation:**
- Run all existing tests - must pass
- Run new FR-001 tests - must pass
- Run with all 22 example rule files
- Verify no existing functionality broken

---

## FR-002: File State Synchronization

### Overview

**Feature Request:** Clarify and fix file synchronization behavior
**Priority:** CRITICAL
**Type:** Bug Fix + Feature
**Complexity:** HIGH

### Acceptance Criteria

- [ ] Always reload FLEx data from database on RA startup
- [ ] Load existing rules from .t1x file (not cache)
- [ ] Detect when .t1x has manual edits
- [ ] Preserve manual edits when possible
- [ ] Warn user when manual edits will be lost
- [ ] "Reload FLEx Data" button implemented (see FR-006)
- [ ] Clear documentation of data flow

### Test Scenarios

#### Test Plan FR-002-001: Fresh Start Workflow (No Existing File)

**Objective:** Verify behavior when starting from scratch

**Preconditions:**
- No existing transfer file
- FLEx project has data

**Test Steps:**
1. Open Rule Assistant with no transfer file
2. Create a rule
3. Save to new file
4. Verify file structure

**Expected Results:**
- ✅ New file created successfully
- ✅ Contains all required sections
- ✅ FLEx data loaded from database
- ✅ No errors or warnings

**Test Data:**
- Fresh FLEx database fixture
- No pre-existing transfer file

---

#### Test Plan FR-002-002: Existing File with RA-Generated Rules

**Objective:** Verify loading previously saved RA-generated rules

**Preconditions:**
- Transfer file exists with RA-generated rules (identifiable by comments)
- File saved from previous RA session

**Test Steps:**
1. Create transfer file in RA session 1
2. Close RA
3. Reopen RA
4. Load same transfer file
5. Verify rules appear in GUI

**Expected Results:**
- ✅ Rules loaded from .t1x file
- ✅ Rules displayed in RA interface
- ✅ Rules editable
- ✅ No data loss

**Automation:**
```python
def test_reload_ra_generated_rules():
    """FR-002-002: RA should reload its own generated rules."""
    # Session 1: Create and save rules
    gen1 = create_generator()
    gen1.ProcessAssistantFile("fixtures/def_noun.xml")
    gen1.WriteTransferFile("temp/session1.t1x")

    # Session 2: Reload
    gen2 = create_generator()
    gen2.ProcessExistingTransferFile("temp/session1.t1x")

    # Verify rules loaded
    assert len(gen2.ruleNames) > 0
    assert "Def N Simple" in gen2.ruleNames  # Example rule name
```

---

#### Test Plan FR-002-003: Existing File with Manual Edits

**Objective:** Detect and handle manually edited transfer files

**Preconditions:**
- Transfer file has RA-generated rules
- User manually edited the file (added custom action code)

**Test Steps:**
1. Create file with RA
2. Manually edit: add custom `<out>` element to a rule
3. Reopen RA with this file
4. Attempt to save new rules

**Expected Results:**
- ✅ RA detects manual edits (e.g., rules without RA comment markers)
- ✅ Warning displayed: "File has manual edits. Save will overwrite them. Continue?"
- ✅ If user cancels, edits preserved
- ✅ If user continues, clear what will be lost

**Automation:**
```python
def test_detect_manual_edits():
    """FR-002-003: RA should detect manual edits."""
    # Create file
    gen = create_generator()
    gen.ProcessAssistantFile("fixtures/def_noun.xml")
    gen.WriteTransferFile("temp/before_edit.t1x")

    # Manually edit
    tree = ET.parse("temp/before_edit.t1x")
    # Add custom element
    rule = tree.find('.//rule')
    ET.SubElement(rule, 'out').text = "CUSTOM_EDIT"
    tree.write("temp/after_edit.t1x")

    # Reload
    gen2 = create_generator()
    has_edits = gen2.DetectManualEdits("temp/after_edit.t1x")

    assert has_edits == True
```

---

#### Test Plan FR-002-004: FLEx Data Changes Between Sessions

**Objective:** Detect when FLEx project data has changed

**Preconditions:**
- Transfer file created with FLEx project version 1
- FLEx project modified (feature added)

**Test Steps:**
1. Create rules with FLEx project
2. Save transfer file
3. Modify FLEx project (add new feature "politeness")
4. Reopen RA
5. Create new rule using "politeness" feature
6. Verify it works

**Expected Results:**
- ✅ New feature available in dropdowns
- ✅ Can create rules with new feature
- ✅ Existing rules still work

**Automation:**
```python
def test_flex_data_reload():
    """FR-002-004: RA should reload FLEx data on startup."""
    # Mock FLEx with initial features
    mock_db_v1 = create_mock_db(features=['gender', 'number'])
    gen1 = create_generator(mock_db_v1)

    # Save
    gen1.ProcessAssistantFile("fixtures/def_noun.xml")
    gen1.WriteTransferFile("temp/v1.t1x")

    # Mock FLEx with added feature
    mock_db_v2 = create_mock_db(features=['gender', 'number', 'politeness'])
    gen2 = create_generator(mock_db_v2)
    gen2.ProcessExistingTransferFile("temp/v1.t1x")

    # Verify new feature available
    available_features = gen2.GetAvailableFeatures('n')
    assert 'politeness' in available_features
```

---

#### Test Plan FR-002-005: Manual Edit Preservation Strategy

**Objective:** Preserve manual edits when adding new rules

**Preconditions:**
- Transfer file has:
  - RA-generated Rule 1
  - Manually-edited Rule 2
  - Custom macro

**Test Steps:**
1. Load file in RA
2. Add new Rule 3 via RA
3. Save
4. Verify Manual Rule 2 and custom macro preserved

**Expected Results:**
- ✅ New Rule 3 added
- ✅ Manual Rule 2 untouched
- ✅ Custom macro preserved
- ✅ RA Rule 1 may be updated if needed

---

### Integration Tests

#### Test Plan FR-002-INT-001: Complete Workflow - Fresh Start

**Scenario:** User creates first project

**Steps:**
1. Open RA (no file)
2. Create 3 rules
3. Save
4. Close RA
5. Reopen RA
6. Load file
7. Add 2 more rules
8. Save

**Verify:**
- All 5 rules present
- No data loss
- File structure correct

---

#### Test Plan FR-002-INT-002: Complete Workflow - With Manual Edits

**Scenario:** User combines RA and manual editing

**Steps:**
1. Create 2 rules in RA
2. Save
3. Manually edit transfer file (add custom macro)
4. Reopen RA
5. Add 1 more rule
6. Save with appropriate warnings

**Verify:**
- Warning about manual edits shown
- User can choose to preserve or overwrite
- Behavior matches choice

---

## FR-003: Confusing Pre-populate Error

### Overview

**Feature Request:** Fix or clarify "file has been edited" error in pre-populate module
**Priority:** MEDIUM-HIGH
**Type:** Bug Fix / UX Improvement

### Acceptance Criteria

- [ ] False positives eliminated
- [ ] Error message clear and accurate
- [ ] Distinction between "has content" and "has manual edits"
- [ ] User knows what action to take
- [ ] Module works correctly regardless of message

### Test Scenarios

#### Test Plan FR-003-001: Pre-populate with Fresh File

**Objective:** Verify no false positive with clean file

**Preconditions:**
- Fresh transfer file (minimal template)
- File created from `transfer_rules_start.t1x`
- No manual edits

**Test Steps:**
1. Create clean file from template
2. Run "Set Up Transfer Rule Categories and Attributes" module
3. Observe messages
4. Verify file populated correctly

**Expected Results:**
- ✅ No "file has been edited" error
- ✅ Or, message accurately reflects state
- ✅ Categories and attributes added
- ✅ File saved successfully

---

#### Test Plan FR-003-002: Pre-populate with Previously Populated File

**Objective:** Test re-running on already populated file

**Preconditions:**
- File already processed by pre-populate module
- No manual edits

**Test Steps:**
1. Run pre-populate once
2. Re-run pre-populate
3. Check message

**Expected Results:**
- ✅ Message should say "File already populated" or similar
- ✅ Not "file has been edited" (confusing)
- ✅ Module updates if needed
- ✅ No errors

---

#### Test Plan FR-003-003: Pre-populate with Actually Edited File

**Objective:** Verify correct detection of real manual edits

**Preconditions:**
- Transfer file with manual additions

**Test Steps:**
1. Start with populated file
2. Manually add custom attribute
3. Run pre-populate
4. Observe message

**Expected Results:**
- ✅ Message accurately describes situation
- ✅ "File contains custom content. Module will add/update standard attributes."
- ✅ Manual content preserved
- ✅ Standard attributes updated

---

#### Test Plan FR-003-004: Pre-populate Message Clarity

**Objective:** Ensure message is actionable

**Test Steps:**
1. Trigger each message condition
2. Evaluate message clarity

**Expected Results:**
- ✅ Message explains current state
- ✅ Message explains what will happen
- ✅ User knows whether to proceed
- ✅ No technical jargon

---

## FR-004: Template Management System

### Overview

**Feature Request:** Add template management to RA
**Priority:** MEDIUM
**Type:** New Feature

### Acceptance Criteria

- [ ] Minimal template available (no language-specific data)
- [ ] Standard template available
- [ ] "New from Template" button works
- [ ] "Reset to Template" button works with confirmation
- [ ] Custom template creation supported
- [ ] Templates documented

### Test Scenarios

#### Test Plan FR-004-001: Load Minimal Template

**Objective:** Verify minimal template is clean

**Test Steps:**
1. Click "New from Template"
2. Select "Minimal Template"
3. Verify file contents

**Expected Results:**
- ✅ No language-specific features
- ✅ No Swedish or other language data
- ✅ Only essential structure
- ✅ Valid XML

**Test Data:**
- `templates/minimal_template.t1x`

---

#### Test Plan FR-004-002: Load Standard Template

**Objective:** Verify standard template has useful defaults

**Test Steps:**
1. Select "Standard Template"
2. Verify contents

**Expected Results:**
- ✅ Common sections pre-populated
- ✅ Still language-neutral
- ✅ Useful as starting point

---

#### Test Plan FR-004-003: Reset to Template

**Objective:** Test reset functionality with confirmation

**Test Steps:**
1. Create some rules
2. Click "Reset to Template"
3. Observe confirmation dialog
4. Cancel
5. Verify rules preserved
6. Click "Reset to Template" again
7. Confirm
8. Verify rules cleared

**Expected Results:**
- ✅ Confirmation dialog shown
- ✅ Clear warning about data loss
- ✅ Cancel preserves work
- ✅ Confirm resets to template

---

#### Test Plan FR-004-004: Save as Custom Template

**Objective:** Allow users to create templates

**Test Steps:**
1. Create useful rule set
2. Click "Save as Template"
3. Name template
4. Later, load custom template
5. Verify rules present

**Expected Results:**
- ✅ Custom template saved
- ✅ Template appears in dropdown
- ✅ Loading template works
- ✅ Template persists across sessions

---

## FR-005: Clearer BantuNounClass Warning

### Overview

**Feature Request:** Improve error message clarity
**Priority:** MEDIUM
**Type:** UX Improvement

### Acceptance Criteria

- [ ] Message distinguishes FLEx features from transfer attributes
- [ ] Message specifies where it's looking
- [ ] Message provides actionable solution
- [ ] Message links to documentation (if applicable)

### Test Scenarios

#### Test Plan FR-005-001: BantuNounClass Warning Content

**Objective:** Verify improved warning message

**Preconditions:**
- Rule uses BantuNounClass
- Attribute not defined in transfer file

**Test Steps:**
1. Create rule with BantuNounClass reference
2. Attribute missing
3. Trigger warning
4. Examine message text

**Expected Results:**
- ✅ Message says "attribute" not "feature"
- ✅ Message specifies "transfer rule file"
- ✅ Message suggests running "Set Up Transfer Rule Categories and Attributes"
- ✅ Message clear and actionable

**Validation:**
```
Expected Message Format:
"Warning: Attribute 'BantuNounClass' not found in transfer rule file.

This attribute should be defined in the <section-def-attrs> section of your
transfer rule file, not as an Inflection Feature in FLEx.

Run 'Set Up Transfer Rule Categories and Attributes' to auto-populate attributes.

Expected location: transfer_rules.t1x -> <section-def-attrs> -> <def-attr n=\"BantuNounClass\">
"
```

---

#### Test Plan FR-005-002: General Attribute Warning Format

**Objective:** Ensure all attribute warnings use clear format

**Test Steps:**
1. Trigger various attribute-missing warnings
2. Verify consistent format

**Expected Results:**
- ✅ Consistent terminology
- ✅ Clear distinction FLEx vs. transfer file
- ✅ Actionable solutions

---

## FR-006: FLEx Data Reload Button

### Overview

**Feature Request:** Add button to reload FLEx data without restarting
**Priority:** MEDIUM
**Type:** New Feature

### Acceptance Criteria

- [ ] "Reload FLEx Data" button in UI
- [ ] Button re-queries FLEx database
- [ ] Existing rules preserved
- [ ] UI dropdowns updated with new data
- [ ] Warning if rules use deleted FLEx items
- [ ] Summary of reload shown

### Test Scenarios

#### Test Plan FR-006-001: Reload Button Functionality

**Objective:** Verify reload button works

**Preconditions:**
- RA open with loaded project

**Test Steps:**
1. Note current FLEx data
2. Modify FLEx database (add feature)
3. Click "Reload FLEx Data"
4. Observe UI updates

**Expected Results:**
- ✅ Button triggers reload
- ✅ Database re-queried
- ✅ New data available
- ✅ Progress indicator shown

---

#### Test Plan FR-006-002: Reload Preserves Rules

**Objective:** Existing rules not lost on reload

**Preconditions:**
- Rules already created

**Test Steps:**
1. Create 3 rules
2. Reload FLEx data
3. Verify rules still present

**Expected Results:**
- ✅ All rules preserved
- ✅ Rule count unchanged
- ✅ Rules still functional

---

#### Test Plan FR-006-003: Reload Updates Dropdowns

**Objective:** UI reflects new FLEx data

**Preconditions:**
- FLEx modified to add new category

**Test Steps:**
1. Add new category to FLEx
2. Reload
3. Check category dropdown

**Expected Results:**
- ✅ New category appears
- ✅ Can be used in new rules

---

#### Test Plan FR-006-004: Warning for Deleted FLEx Items

**Objective:** Warn about rules using deleted data

**Preconditions:**
- Rule uses feature "politeness"
- Feature deleted from FLEx

**Test Steps:**
1. Delete feature from FLEx
2. Reload
3. Observe warnings

**Expected Results:**
- ✅ Warning shown
- ✅ Specifies which rules affected
- ✅ Suggests remediation
- ✅ Rules marked as potentially broken

---

#### Test Plan FR-006-005: Reload Summary Display

**Objective:** User sees what was reloaded

**Test Steps:**
1. Reload FLEx data
2. Check summary message

**Expected Results:**
- ✅ "Reloaded: X categories, Y features, Z affixes"
- ✅ Clear, concise
- ✅ User knows reload succeeded

---

## Test Data Requirements

### General Test Data

**Needed for All FRs:**
- Mock FLEx database with various configurations
- Sample transfer files (fresh, populated, edited)
- Sample Rule Assistant XML files
- Known-good output files for comparison

### FR-001 Specific

- Transfer file with custom Variables section
- Transfer file with custom Macros section
- Transfer file with empty sections
- Transfer file with mixed content

### FR-002 Specific

- Transfer files showing evolution:
  - Fresh start
  - After 1st RA session
  - After manual edit
  - After 2nd RA session
- FLEx database snapshots (v1, v2 with changes)

### FR-003 Specific

- Clean template file
- Populated file (no edits)
- Manually edited file
- Files at various stages of pre-populate

### FR-004 Specific

- Minimal template
- Standard template
- Example custom templates

### FR-005 Specific

- Rules triggering various warnings
- Expected warning message texts

### FR-006 Specific

- FLEx database before/after modifications
- Rules using features that get deleted

---

## Automation Priority

### Phase 1 (Immediate)

1. FR-001 automation (critical bug)
2. FR-002 core workflows
3. Basic regression tests

### Phase 2 (Short-term)

4. FR-003 automation
5. FR-006 basic tests
6. Integration test completion

### Phase 3 (Medium-term)

7. FR-004 template tests
8. FR-005 message validation
9. Performance tests
10. Stress tests

---

## Success Metrics

**Per FR:**
- All test scenarios pass
- Edge cases identified and tested
- Automation coverage >90%
- Clear test documentation
- No regression in existing tests

**Overall:**
- 150+ test cases
- 80%+ code coverage
- All critical paths tested
- Performance benchmarks established

---

**Document Status:** Complete
**Next Action:** Implement integration test suite
**Owner:** QC Agent
