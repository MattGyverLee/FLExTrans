# QC Validation Checklist
**Purpose:** Pre-merge validation checklist for Rule Assistant fixes
**Date:** 2025-11-22
**Author:** QC Agent

---

## Instructions

This checklist should be completed before merging any fix for FR-001 through FR-006. Print this document or copy to a tracking tool and check off each item as validation is completed.

---

## General Pre-Merge Checklist

### Code Quality

- [ ] **All new code has docstrings**
- [ ] **Code follows Python PEP 8 style guide**
- [ ] **No debugging print statements left in code**
- [ ] **No commented-out code blocks** (unless intentional with explanation)
- [ ] **All TODOs addressed or documented in issues**
- [ ] **Error messages are clear and actionable**
- [ ] **Logging is appropriate** (not too verbose, not too quiet)

### Testing

- [ ] **All new tests pass locally**
- [ ] **All existing tests still pass**
- [ ] **Code coverage >80% for modified files**
- [ ] **Integration tests pass**
- [ ] **Regression tests pass**
- [ ] **Manual testing completed** (see below)

### Documentation

- [ ] **Code changes documented in docstrings**
- [ ] **User-facing documentation updated** (if applicable)
- [ ] **CHANGELOG updated**
- [ ] **Known limitations documented**

### Git

- [ ] **Commits are atomic and well-described**
- [ ] **Branch is up to date with main**
- [ ] **No merge conflicts**
- [ ] **All files properly added to git**

---

## FR-001: Missing Nodes Bug - Validation Checklist

### Automated Tests

- [ ] `test_preserve_existing_variables_section()` passes
- [ ] `test_preserve_existing_macros_section()` passes
- [ ] `test_preserve_empty_sections()` passes
- [ ] `test_mixed_generated_and_custom_content()` passes

### Manual Testing

**Test Case 1: Preserve Custom Variables**

1. [ ] Create transfer file with custom variables section:
   ```xml
   <section-def-vars>
     <def-var n="my_test_var"/>
     <def-var n="another_test_var"/>
   </section-def-vars>
   ```
2. [ ] Open Rule Assistant
3. [ ] Load this transfer file
4. [ ] Create one simple rule (e.g., Def-Noun)
5. [ ] Save transfer file
6. [ ] Open saved file in text editor
7. [ ] **VERIFY:** `<section-def-vars>` still present
8. [ ] **VERIFY:** `my_test_var` still present
9. [ ] **VERIFY:** `another_test_var` still present
10. [ ] **VERIFY:** Any RA-generated variables also present

**Test Case 2: Preserve Custom Macros**

1. [ ] Create transfer file with custom macro:
   ```xml
   <section-def-macros>
     <def-macro n="my_custom_macro" npar="1">
       <choose>
         <when><test><lit-tag v="test"/></test></when>
       </choose>
     </def-macro>
   </section-def-macros>
   ```
2. [ ] Open Rule Assistant
3. [ ] Load transfer file
4. [ ] Add a rule that generates macros
5. [ ] Save
6. [ ] Open in text editor
7. [ ] **VERIFY:** `<section-def-macros>` present
8. [ ] **VERIFY:** `my_custom_macro` present
9. [ ] **VERIFY:** RA-generated macros also present
10. [ ] **VERIFY:** No duplicate macros

**Test Case 3: Empty Sections Not Deleted**

1. [ ] Create transfer file with empty sections:
   ```xml
   <section-def-vars/>
   <section-def-macros/>
   ```
2. [ ] Run Rule Assistant
3. [ ] Create simple rule (may not need vars/macros)
4. [ ] Save
5. [ ] **VERIFY:** Sections still present (even if empty)

### Regression Verification

- [ ] Run all 22 example rule files
- [ ] Verify no new failures
- [ ] Compare output with baseline
- [ ] Check for unexpected section deletions

### Edge Cases

- [ ] Test with only variables (no macros)
- [ ] Test with only macros (no variables)
- [ ] Test with both empty
- [ ] Test with both populated
- [ ] Test with comments in sections

### Documentation

- [ ] Root cause documented
- [ ] Fix approach documented
- [ ] Known limitations documented

**Sign-off:** _______________________ Date: _________

---

## FR-002: File State Synchronization - Validation Checklist

### Automated Tests

- [ ] `test_fresh_start_no_existing_file()` passes
- [ ] `test_reload_ra_generated_rules()` passes
- [ ] `test_detect_flex_data_changes()` passes
- [ ] Complete workflow tests pass

### Manual Testing

**Test Case 1: Fresh Start Workflow**

1. [ ] Open Rule Assistant with no existing file
2. [ ] Create 2 rules
3. [ ] Save to new file
4. [ ] Close Rule Assistant
5. [ ] Reopen Rule Assistant
6. [ ] Load the file
7. [ ] **VERIFY:** Both rules appear correctly
8. [ ] Add 1 more rule
9. [ ] Save
10. [ ] **VERIFY:** All 3 rules in file

**Test Case 2: Manual Edit Detection**

1. [ ] Create transfer file in RA
2. [ ] Save and close
3. [ ] Manually edit file (add custom rule or modify existing)
4. [ ] Reopen RA
5. [ ] Load edited file
6. [ ] **VERIFY:** Warning about manual edits (if applicable)
7. [ ] Try to save
8. [ ] **VERIFY:** Appropriate confirmation dialog
9. [ ] **VERIFY:** Can choose to preserve or overwrite

**Test Case 3: FLEx Data Changes**

1. [ ] Create rules with current FLEx project
2. [ ] Save transfer file
3. [ ] Modify FLEx project (add new feature)
4. [ ] Reopen Rule Assistant
5. [ ] Load transfer file
6. [ ] **VERIFY:** New FLEx feature available in dropdowns
7. [ ] Create rule using new feature
8. [ ] **VERIFY:** Works correctly
9. [ ] Modify FLEx project (delete a feature)
10. [ ] Reload RA
11. [ ] **VERIFY:** Warning if existing rules use deleted feature

**Test Case 4: Data Source Verification**

1. [ ] Open RA
2. [ ] Note FLEx data in dropdowns
3. [ ] **VERIFY:** Data comes from FLEx database (not cache)
4. [ ] Load transfer file
5. [ ] **VERIFY:** Rules loaded from .t1x (not XML cache)

### Data Flow Documentation

- [ ] Documented: What RA reads on startup
- [ ] Documented: Where GUI input XML stored (if applicable)
- [ ] Documented: When .t1x loaded
- [ ] Documented: What triggers FLEx reload

### User Documentation

- [ ] Workflow guide created/updated
- [ ] Manual edit warning documented
- [ ] Best practices documented
- [ ] FAQ updated

**Sign-off:** _______________________ Date: _________

---

## FR-003: Pre-populate Error - Validation Checklist

### Automated Tests

- [ ] `test_prepopulate_with_fresh_file()` passes
- [ ] `test_prepopulate_with_start_template()` passes
- [ ] `test_prepopulate_false_positive_on_clean_file()` passes

### Manual Testing

**Test Case 1: Clean File (No False Positive)**

1. [ ] Create fresh transfer file from template
2. [ ] Run "Set Up Transfer Rule Categories and Attributes"
3. [ ] **VERIFY:** No "file has been edited" error
4. [ ] OR message accurately describes state
5. [ ] **VERIFY:** Categories and attributes added successfully
6. [ ] **VERIFY:** File in saved state after module runs

**Test Case 2: Re-run Pre-populate**

1. [ ] Run pre-populate on fresh file
2. [ ] Re-run pre-populate
3. [ ] **VERIFY:** Message makes sense ("already populated" or similar)
4. [ ] **VERIFY:** No confusing "file has been edited" message
5. [ ] **VERIFY:** Module updates as needed

**Test Case 3: Actually Edited File**

1. [ ] Run pre-populate
2. [ ] Manually add custom attribute
3. [ ] Re-run pre-populate
4. [ ] **VERIFY:** Accurate message about custom content
5. [ ] **VERIFY:** Custom content preserved
6. [ ] **VERIFY:** Standard attributes updated

### Message Quality

- [ ] Messages are clear (not technical jargon)
- [ ] Messages are actionable
- [ ] Messages distinguish between states:
  - [ ] "Fresh file" vs "Populated file" vs "Edited file"
- [ ] User knows whether to proceed

**Sign-off:** _______________________ Date: _________

---

## FR-004: Template Management - Validation Checklist

### Automated Tests

- [ ] `test_load_minimal_template()` passes
- [ ] `test_load_standard_template()` passes
- [ ] `test_reset_to_template_with_confirmation()` passes
- [ ] `test_save_as_custom_template()` passes

### Manual Testing

**Test Case 1: Load Minimal Template**

1. [ ] Click "New from Template"
2. [ ] Select "Minimal Template"
3. [ ] **VERIFY:** File loaded
4. [ ] **VERIFY:** No Swedish or language-specific features
5. [ ] **VERIFY:** Only essential structure
6. [ ] **VERIFY:** Valid XML
7. [ ] Try to create a rule
8. [ ] **VERIFY:** Works as expected

**Test Case 2: Load Standard Template**

1. [ ] Select "Standard Template"
2. [ ] **VERIFY:** Common sections present
3. [ ] **VERIFY:** Still language-neutral
4. [ ] **VERIFY:** More populated than minimal

**Test Case 3: Reset to Template**

1. [ ] Create several rules
2. [ ] Click "Reset to Template"
3. [ ] **VERIFY:** Confirmation dialog appears
4. [ ] **VERIFY:** Warning about data loss clear
5. [ ] Click Cancel
6. [ ] **VERIFY:** Rules preserved
7. [ ] Click "Reset to Template" again
8. [ ] Click Confirm
9. [ ] **VERIFY:** Rules cleared
10. [ ] **VERIFY:** Reset to selected template

**Test Case 4: Custom Template**

1. [ ] Create useful rule set
2. [ ] Click "Save as Template"
3. [ ] Enter template name
4. [ ] **VERIFY:** Template saved
5. [ ] Create new project
6. [ ] **VERIFY:** Custom template appears in dropdown
7. [ ] Load custom template
8. [ ] **VERIFY:** Rules from template present

### Template Quality

- [ ] Minimal template has no language data
- [ ] Standard template is useful starting point
- [ ] Custom templates work correctly
- [ ] Templates documented

**Sign-off:** _______________________ Date: _________

---

## FR-005: Clearer Warning Messages - Validation Checklist

### Automated Tests

- [ ] `test_bantu_warning_message_clarity()` passes
- [ ] `test_bantu_warning_specifies_location()` passes
- [ ] `test_bantu_warning_provides_solution()` passes

### Manual Testing

**Test Case 1: BantuNounClass Warning**

1. [ ] Create rule using BantuNounClass
2. [ ] Ensure attribute not defined
3. [ ] Trigger warning
4. [ ] **VERIFY Message Contains:**
   - [ ] Word "attribute" (not just "feature")
   - [ ] "transfer rule file" (specifies location)
   - [ ] Actionable solution (run pre-populate module)
   - [ ] Expected file location
5. [ ] **VERIFY:** Message clarity rated 4/5 or better by user

**Test Case 2: Other Attribute Warnings**

1. [ ] Trigger various attribute-missing warnings
2. [ ] **VERIFY:** Consistent format
3. [ ] **VERIFY:** Clear terminology
4. [ ] **VERIFY:** Actionable solutions

### Message Quality Review

- [ ] All warning messages reviewed
- [ ] Consistent terminology throughout
- [ ] Technical terms explained or avoided
- [ ] Links to docs (if applicable)

**Sign-off:** _______________________ Date: _________

---

## FR-006: Reload FLEx Data - Validation Checklist

### Automated Tests

- [ ] `test_reload_flex_data_queries_database()` passes
- [ ] `test_reload_flex_data_preserves_rules()` passes
- [ ] `test_reload_flex_data_updates_ui_dropdowns()` passes

### Manual Testing

**Test Case 1: Reload Button Functionality**

1. [ ] Open Rule Assistant
2. [ ] Note current FLEx data
3. [ ] Modify FLEx database (add feature)
4. [ ] Click "Reload FLEx Data" button
5. [ ] **VERIFY:** Button triggers reload
6. [ ] **VERIFY:** Progress indicator shown
7. [ ] **VERIFY:** Database re-queried
8. [ ] **VERIFY:** UI updates

**Test Case 2: Rules Preserved During Reload**

1. [ ] Create 3 rules
2. [ ] Reload FLEx data
3. [ ] **VERIFY:** All 3 rules still present
4. [ ] **VERIFY:** Rules still functional

**Test Case 3: UI Dropdowns Update**

1. [ ] Add new category to FLEx
2. [ ] Reload
3. [ ] Check category dropdown
4. [ ] **VERIFY:** New category appears
5. [ ] **VERIFY:** Can use in new rules

**Test Case 4: Warning for Deleted Items**

1. [ ] Create rule using feature "test_feature"
2. [ ] Delete "test_feature" from FLEx
3. [ ] Reload
4. [ ] **VERIFY:** Warning displayed
5. [ ] **VERIFY:** Specifies which rules affected
6. [ ] **VERIFY:** Suggests remediation

**Test Case 5: Reload Summary**

1. [ ] Reload FLEx data
2. [ ] Check summary message
3. [ ] **VERIFY:** Shows counts (categories, features, affixes)
4. [ ] **VERIFY:** Clear and concise

### UI Integration

- [ ] Button placement appropriate
- [ ] Button clearly labeled
- [ ] Confirmation dialog (if needed)
- [ ] Progress feedback adequate

**Sign-off:** _______________________ Date: _________

---

## Cross-Cutting Validation

### All FRs: General Validation

**User Experience:**
- [ ] No crashes or unhandled exceptions
- [ ] Error messages helpful (not cryptic)
- [ ] Performance acceptable (no long freezes)
- [ ] UI responsive

**File Integrity:**
- [ ] No data loss
- [ ] Files remain valid XML
- [ ] Apertium can compile outputs
- [ ] No corruption

**Compatibility:**
- [ ] Works with existing projects
- [ ] Backward compatible with old files
- [ ] Forward compatible design

**Documentation:**
- [ ] User guide updated
- [ ] Technical docs updated
- [ ] Known issues documented
- [ ] Migration guide (if needed)

---

## Acceptance Testing

### User Acceptance Test (UAT)

**Test with Real User (Field Linguist):**

1. [ ] Fresh start workflow
2. [ ] Existing project workflow
3. [ ] Mixed RA/manual editing workflow
4. [ ] Error recovery scenarios
5. [ ] Feedback collected
6. [ ] Issues documented
7. [ ] User satisfied (>4/5 rating)

### Stakeholder Review

- [ ] Technical review complete
- [ ] Linguistic review complete (if needed)
- [ ] Product owner approval
- [ ] Release notes prepared

---

## Final Pre-Merge Checklist

### All Items Complete

- [ ] All automated tests passing
- [ ] All manual tests passing
- [ ] All checklists signed off
- [ ] Code reviewed and approved
- [ ] Documentation complete
- [ ] No known blocking issues

### Deployment Readiness

- [ ] Tested on Windows
- [ ] Tested on Linux
- [ ] Tested on macOS (if applicable)
- [ ] Installation instructions updated
- [ ] Rollback plan documented

### Sign-Off

**QA Lead:** _______________________ Date: _________

**Tech Lead:** _______________________ Date: _________

**Product Owner:** _______________________ Date: _________

---

## Post-Merge Monitoring

### After Merge (First Week)

- [ ] Monitor for new issue reports
- [ ] Check automated test results
- [ ] Review user feedback
- [ ] Performance monitoring
- [ ] No critical bugs reported

### After Merge (First Month)

- [ ] User adoption tracking
- [ ] Support request volume
- [ ] Regression issue count
- [ ] User satisfaction survey

---

**Document Version:** 1.0
**Last Updated:** 2025-11-22
**Next Review:** After each major release
