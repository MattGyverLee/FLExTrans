# Rule Assistant Feature Requests
**From Consultant Wish List**
**Date:** 2025-11-22
**Status:** Draft for Review

## Overview

This document captures feature requests, bug reports, and documentation needs identified by a field consultant working with the Rule Assistant. Items are categorized by type and priority.

---

## Table of Contents

1. [High Priority - Critical Issues](#1-high-priority---critical-issues)
2. [Medium Priority - Usability Improvements](#2-medium-priority---usability-improvements)
3. [Documentation Needs](#3-documentation-needs)
4. [Implementation Notes](#4-implementation-notes)

---

## 1. High Priority - Critical Issues

### FR-001: Missing Nodes Bug (Variables and Macros Disappearing)

**Type:** 🐛 Bug
**Priority:** High
**Status:** Needs Investigation

#### Description
After running the Rule Assistant, the generated transfer rule file is missing `<section-def-vars>` and `<section-def-macros>` nodes, even though the starting template file (`transfer_rules_start.t1x`) contained these sections.

#### User Report
> "After I ran the Rule Assistant, I ended up with a Rules file that was missing nodes for Variables and Macros. How did that happen? (I started with this file: transfer_rules_start.t1x and it has Macros and Variables in it.)"

#### Steps to Reproduce
1. Start with `transfer_rules_start.t1x` containing Variables and Macros sections
2. Run Rule Assistant and create rules
3. Save the output
4. Observe that Variables and Macros sections are missing from the output file

#### Expected Behavior
- Existing Variables and Macros sections should be preserved
- New macros/variables should be added to existing sections
- No sections should be deleted unless explicitly requested

#### Acceptance Criteria
- [ ] Identify root cause in `CreateApertiumRules.py` (likely in `ProcessExistingTransferFile()` or `WriteTransferFile()`)
- [ ] Preserve all existing sections when loading transfer files
- [ ] Add regression test to verify section preservation
- [ ] Document which sections are preserved vs. regenerated

#### Technical Notes
- Likely related to `RuleGenerator.WriteTransferFile()` at line 1543
- May be discarding empty sections (line 1542: "Discard empty sections")
- Need to distinguish between "empty" and "should be preserved even if empty"

---

### FR-002: File State Synchronization Issues

**Type:** 🐛 Bug + 📚 Documentation
**Priority:** High
**Status:** Needs Investigation

#### Description
The Rule Assistant's data source and synchronization behavior is unclear and potentially buggy. Users report:
1. Uncertainty about whether RA reads from the `.t1x` file or cached XML
2. Manual edits to `.t1x` may be lost
3. Changes to FLEx project may not be reflected in RA
4. No clear way to reload FLEx data

#### User Reports
> "When I start up the RA again, where is it getting its info from? Is it reading my rule file, or some other file?"

> "If you have already created rules with the RA, and then you have edited the file, and then you want to open it up with the RA, does it keep the edits you made?"

> "There were several times I made major changes to my project... When I started up the RA, I was kind of afraid it might be blank... I have a suspicion that there were things that changed in my FLEx project that it should have been aware of."

#### Current Behavior (Needs Verification)
- RA appears to cache data between sessions
- Source of truth unclear (FLEx DB, .t1x file, or XML cache?)
- Manual edits may or may not be preserved
- FLEx changes may or may not be detected

#### Proposed Solution

**Phase 1: Investigation**
1. Document current data flow:
   - What does RA read on startup?
   - Where is the GUI input XML stored?
   - When/how is the `.t1x` file loaded?
   - What triggers FLEx data reload?

2. Identify bugs in current implementation

**Phase 2: Fix**
1. Always reload FLEx data from database on RA startup
2. Load existing rules from `.t1x` file (not cache)
3. Preserve manual edits to `.t1x` when possible
4. Add "Reload FLEx Data" button to GUI

**Phase 3: Documentation**
- Clear workflow documentation
- Warning when manual edits might be lost
- Best practices guide

#### Acceptance Criteria
- [ ] Document current data flow in technical spec
- [ ] Identify all data sources (FLEx DB, .t1x, cache files)
- [ ] Manual edits to `.t1x` preserved when re-opening RA
- [ ] FLEx project changes reflected when RA reopens
- [ ] Add "Reload FLEx Data" button to force refresh
- [ ] Clear warning when opening RA will overwrite manual edits
- [ ] User documentation explaining workflow

#### User Stories

**As a linguist,** I want to manually edit my `.t1x` file for advanced rules **so that** I can handle edge cases not supported by the GUI.

**As a linguist,** when I reopen Rule Assistant after editing `.t1x`, I want my manual edits preserved **so that** I don't lose my work.

**As a linguist,** when I add new features to my FLEx project, I want Rule Assistant to detect them **so that** I can use them in rules without restarting everything.

**As a linguist,** I want a "Reload FLEx Data" button **so that** I can force synchronization after making FLEx changes.

---

### FR-003: Confusing "File Has Been Edited" Error in Pre-populate Module

**Type:** 🐛 Bug
**Priority:** Medium-High
**Status:** Needs Investigation

#### Description
The pre-populate module shows a confusing error message about the file being edited, even when:
- The file was replaced with a clean start file
- The file hasn't been manually edited
- The module still works despite the error
- The error appears on re-runs even after saving

#### User Report
> "This error message is confusing, when I run the pre-populate module: [shows 'file has been edited' warning]. I had edited the file before, but then I replaced it with the 'start file', so maybe I hadn't edited this copy of it."

> "When I re-ran this module, it again gave me this error, even though I had saved it in between. But in spite of the error, it still added categories etc to the rule file, and left the rule file in a Saved state. So I'm not clear on what the message is trying to tell me."

#### Current Behavior
- Error appears even when file is fresh/unedited
- Module continues to work despite error
- File ends up in "Saved" state after module runs
- Error message doesn't prevent functionality

#### Root Cause Hypotheses
1. Module checks file timestamp or hash, gets false positive
2. "Edited" detection logic is flawed
3. Error is actually a warning that can be ignored
4. Module considers "has any content" as "edited"

#### Proposed Solution

**Option A: Fix the Detection Logic**
- Improve "edited" detection to avoid false positives
- Only warn when actual manual edits detected
- Distinguish between "generated by RA" and "manually edited"

**Option B: Remove/Rephrase the Warning**
- If the module works despite warning, make it a debug message
- Rephrase to be more accurate: "Transfer file already exists. Categories and attributes will be added/updated."

#### Acceptance Criteria
- [ ] Investigate what triggers "file has been edited" message
- [ ] Determine if this is actually an error or just info
- [ ] Fix false positives or rephrase message
- [ ] Document when this message should appear
- [ ] Add test cases for clean file vs. edited file

---

## 2. Medium Priority - Usability Improvements

### FR-004: Template Management System

**Type:** ✨ Feature
**Priority:** Medium
**Status:** Proposed

#### Description
Users need a clean starting template and an easy way to reset to defaults, similar to Ron's test harness `copy start to default.bat` approach.

#### User Request
> "Can we have some 'initial rule file' that would be the start for the Rule Assistant, that doesn't have features for Swedish in it? And a way to reset back to that? I notice that in Ron's test harness, he has a batch file to reset: copy start to default.bat. It would be helpful for ordinary users to be able to do that too."

#### Current State
- Test harness has batch file approach
- No user-facing template management
- Users may start with templates containing unwanted language data (e.g., Swedish)

#### Proposed Solution

**UI Enhancement:**
Add to Rule Assistant GUI:
- "New Project from Template" button
- "Reset to Template" button (with confirmation dialog)
- Template selection dropdown

**Backend:**
- Ship clean templates in `Rule Assistant/templates/`
  - `minimal_template.t1x` - Absolute minimum structure
  - `standard_template.t1x` - Common sections pre-populated
  - `custom_template.t1x` - User can create their own
- Copy template to project location
- Preserve user's custom templates

**File Structure:**
```
Rule Assistant/
  templates/
    minimal_template.t1x          # Clean slate
    standard_template.t1x         # Common sections
    README_TEMPLATES.md           # Template documentation
  FLExTransRuleGenerator.dtd
  [example rules...]
```

#### Acceptance Criteria
- [ ] Ship 2-3 clean templates without language-specific data
- [ ] Add "New from Template" button to GUI
- [ ] Add "Reset to Template" with confirmation dialog
- [ ] Allow users to save current state as custom template
- [ ] Document how to create custom templates
- [ ] Preserve existing rules when resetting is declined

#### User Stories

**As a linguist,** I want to start with a clean template **so that** I don't have to delete Swedish/other language features I don't need.

**As a linguist,** I want to reset to a clean state **so that** I can start over without manually deleting everything.

**As a linguist,** I want to save my current configuration as a template **so that** I can reuse it for similar language pairs.

---

### FR-005: Clearer BantuNounClass Warning Message

**Type:** 📋 UX Improvement
**Priority:** Medium
**Status:** Proposed

#### Description
The warning message about "BantuNounClass" feature is confusing about:
1. Whether it's looking for an Inflection Feature in FLEx
2. Where it's looking for values (FLEx vs. rule file attributes)
3. Using "feature" terminology when it might mean "attribute"

#### User Report
> "This warning message needs to be more specific about where it is looking for these tags. 1. By calling 'BantuNounClass' a 'feature', it sounds like it is supposed to exist as an Inflection Feature in FLEx. But I think it doesn't need to? 2. Is it looking for values for that Inflection Feature in FLEx, or is it just looking for there to be an attribute in the rule file that has values?"

#### Current Message (Assumed)
```
Warning: BantuNounClass feature not found
```

#### Proposed Improved Message

**Option A: Detailed**
```
Warning: Disjoint feature set 'BantuNounClass' not found in transfer rule attributes.

This feature should be defined in the <section-def-attrs> of your transfer
rule file, not as an Inflection Feature in FLEx.

Expected location: transfer_rules.t1x -> <section-def-attrs> -> <def-attr n="BantuNounClass">

Run "Set Up Transfer Rule Categories and Attributes" to auto-populate, or
manually add the attribute definition to your transfer file.
```

**Option B: Concise with Link**
```
Warning: Attribute 'BantuNounClass' not found in transfer rule file.

Run "Set Up Transfer Rule Categories and Attributes" to auto-populate attributes.
See documentation: [link to Bantu noun class setup guide]
```

#### Acceptance Criteria
- [ ] Identify exact location where this warning is generated
- [ ] Clarify terminology (feature vs. attribute)
- [ ] Specify exact file location being checked
- [ ] Provide actionable solution (which module to run)
- [ ] Link to relevant documentation
- [ ] Update all similar ambiguous error messages

---

### FR-006: FLEx Data Reload Button

**Type:** ✨ Feature
**Priority:** Medium
**Status:** Proposed

#### Description
Add a button to force reload of FLEx database information without restarting Rule Assistant.

#### User Request
> "There were several times I made major changes to my project... When I started up the RA, I was kind of afraid it might be blank and I would have to build my tree all over again... I have a suspicion that there were things that changed in my FLEx project (what features or categories or affixes existed) that it should have been aware of. Do we need a button to tell it to 're-load the FLEx data'?"

#### Current Behavior
- FLEx data loaded at RA startup
- No way to refresh without closing and reopening
- Changes to FLEx project may not be reflected

#### Proposed Solution

**GUI Addition:**
- Add "Reload FLEx Data" button (maybe in File menu or toolbar)
- Shows confirmation: "This will reload categories, features, and affixes from FLEx. Your existing rules will be preserved. Continue?"
- Shows progress indicator during reload
- Displays summary: "Reloaded: 12 categories, 45 features, 23 affixes"

**Backend:**
- Re-run FLEx database queries
- Update category/feature dropdowns
- Preserve existing rule tree structure
- Highlight any conflicts (e.g., rules using deleted features)

#### Acceptance Criteria
- [ ] Add "Reload FLEx Data" button to GUI
- [ ] Re-query FLEx database without restarting RA
- [ ] Preserve existing rule tree and rules
- [ ] Update all dropdowns with new data
- [ ] Show warning if rules reference deleted FLEx items
- [ ] Display reload summary (what was loaded)
- [ ] Add to user documentation

#### User Story

**As a linguist,** when I add new features to FLEx while Rule Assistant is open, I want to reload FLEx data **so that** I can use the new features immediately without restarting.

---

## 3. Documentation Needs

### DOC-001: Rule Assistant Workflow with Existing Transfer Files

**Type:** 📚 Documentation
**Priority:** High
**Status:** Needed

#### Questions Needing Documentation

1. **What happens when opening RA with existing transfer file?**
   - Are existing rules preserved?
   - Are they displayed in the GUI?
   - Are they editable?

2. **What happens when saving after creating new rules?**
   - Does it add to existing file?
   - Does it overwrite?
   - Are hand-edits preserved?

3. **What is the recommended workflow?**
   - When to use RA vs. manual editing
   - How to combine both approaches
   - How to avoid losing work

#### User Questions
> "We need to document what happens when you start up the Rule Assistant when you already have a transfer rule file. Do your existing rules get included? Can it display them? When you write rules with the RA and then save, does it add the new rules to your existing file, or overwrite what you had (and you lose yours)? What is the workflow when you already have rules?"

#### Required Documentation Sections

**Section 1: Initial Setup**
- Starting from scratch vs. existing file
- What gets loaded from FLEx
- What gets loaded from transfer file
- Expected file structure

**Section 2: Working with Existing Rules**
- How existing rules appear in RA
- Which rules can be edited in RA
- Which rules require manual editing
- Limitations of GUI vs. manual editing

**Section 3: Saving Behavior**
- Default save behavior (merge vs. overwrite)
- `overwrite_rules="yes"` attribute behavior
- Backup recommendations
- Version control best practices

**Section 4: Mixed Workflow**
- When to use RA
- When to manually edit
- How to preserve manual edits
- Warning signs that manual edits will be lost

**Section 5: Troubleshooting**
- "My rules disappeared" - recovery steps
- "My manual edits were lost" - prevention
- "RA doesn't see my FLEx changes" - fix

#### Deliverables
- [ ] User guide chapter: "Working with Existing Transfer Files"
- [ ] Workflow diagram (visual)
- [ ] Quick reference card
- [ ] FAQ section
- [ ] Video tutorial (optional)

---

### DOC-002: Disjoint Feature Sets (Bantu Noun Classes)

**Type:** 📚 Documentation
**Priority:** Medium
**Status:** Needed

#### Description
Document how to use disjoint feature sets for Bantu noun class agreement and similar phenomena.

#### User Request
> "Need to explain that when writing rules with disjoint Noun Classes, on the root of the Noun, we just put the name of the 'master set' (the union of all the features), even though the root is specified for two or more of the subsets–it is likely to have two values from that set."

#### Required Documentation

**Conceptual Explanation:**
- What are disjoint feature sets?
- Why are they needed? (number conflated with gender in Bantu)
- How FLEx represents them vs. Apertium

**Step-by-Step Guide:**
1. Define disjoint feature set in XML
2. Map FLEx features to co-feature values
3. Use "master set" name on noun root
4. Apply to agreement targets

**Example:**
- Complete XML showing SplitBantu.xml pattern
- Explanation of each part
- Common mistakes to avoid

**Language-Specific Guides:**
- Bantu noun classes (detailed)
- Other languages with similar patterns
- Template for new languages

#### Deliverables
- [ ] Tutorial: "Understanding Disjoint Feature Sets"
- [ ] Annotated SplitBantu.xml example
- [ ] Language typology guide (when to use this feature)
- [ ] Troubleshooting section

---

### DOC-003: Module Prerequisites and Workflow

**Type:** 📚 Documentation
**Priority:** Medium
**Status:** Needed

#### Description
Document which modules need to run before Rule Assistant and in what order.

#### User Questions
> "Do we need to tell people to run 'Run Apertium' before they run the Rule Assistant, so they can have sample data? Do they need to run other modules before they can run that one?"

> "Do we need to pre-populate the Attributes, or not?"

#### Required Documentation

**Module Dependency Chart:**
```
1. Set Up Transfer Rule Categories and Attributes (REQUIRED)
   ↓
2. Rule Assistant (uses categories/attributes from step 1)
   ↓
3. Run Apertium (optional - for testing)
   ↓
4. Rule Assistant again (with sample data preview)
```

**For Each Module:**
- Purpose
- Prerequisites
- What it creates/modifies
- When to run it
- When to re-run it

**Workflow Scenarios:**
- **First time setup:** Complete step-by-step
- **Adding new rules:** What to re-run
- **Changing FLEx project:** What to regenerate
- **Debugging rules:** Testing cycle

#### Deliverables
- [ ] "Getting Started with Rule Assistant" guide
- [ ] Module dependency diagram
- [ ] Workflow decision tree
- [ ] Common scenarios checklist

---

### DOC-004: Attribute Pre-population

**Type:** 📚 Documentation
**Priority:** Low-Medium
**Status:** Needed

#### Description
Clarify whether attributes need to be pre-populated and when.

#### User Question
> "Do we need to pre-populate the Attributes, or not?"

#### Answer Needed
- What does "Set Up Transfer Rule Categories and Attributes" do?
- Is it required or optional?
- When does it need to run?
- What happens if you skip it?
- Can RA auto-populate on first run?

#### Deliverables
- [ ] Clear statement in documentation
- [ ] Decision flowchart
- [ ] Best practices recommendation

---

## 4. Implementation Notes

### Priority Order for Implementation

#### Immediate (Sprint 1)
1. **FR-001**: Missing Nodes Bug - Critical data loss issue
2. **FR-002**: File Synchronization - Fundamental workflow problem
3. **DOC-001**: Existing Transfer Files - Blocks user adoption

#### Short-term (Sprint 2-3)
4. **FR-003**: Confusing Error Message - Frustrates users
5. **FR-005**: Better Warning Messages - Improves UX
6. **DOC-002**: Disjoint Feature Sets - Enables advanced use cases
7. **DOC-003**: Module Prerequisites - Reduces support burden

#### Medium-term (Sprint 4-5)
8. **FR-004**: Template Management - Nice quality-of-life feature
9. **FR-006**: Reload FLEx Data - Convenience feature
10. **DOC-004**: Attribute Pre-population - Clarification only

### Cross-Cutting Concerns

**Data Flow Architecture Review Needed:**
- FR-001, FR-002, FR-003 all point to confusion about:
  - What files exist and their purposes
  - Source of truth for different data
  - When files are read vs. cached
  - When data is synchronized

**Recommendation:** Start with architectural documentation of current data flow before fixing individual bugs.

### Testing Strategy

For each fix:
1. **Unit tests** - Component behavior
2. **Integration tests** - File I/O and persistence
3. **User acceptance tests** - Actual workflow scenarios
4. **Regression tests** - Ensure fixes don't break existing functionality

### Success Metrics

- **Reduction in support requests** about "lost rules"
- **User confidence** in mixed manual/GUI workflow
- **Completion rate** for Rule Assistant tasks
- **Time to first working rule** for new users

---

## Appendix A: Related Files

- `Dev/Modules/RuleAssistant.py` - Main orchestrator
- `Dev/Lib/CreateApertiumRules.py` - Rule generation logic
- `Rule Assistant/FLExTransRuleGenerator.dtd` - XML schema
- `Rule Assistant/SplitBantu.xml` - Disjoint feature example
- `transfer_rules_start.t1x` - Proposed template file

## Appendix B: Consultant Contact

For clarification on requirements, follow up with the consultant who provided the original wish list.

---

**Document Status:** Draft
**Next Steps:**
1. Review with development team
2. Prioritize with product owner
3. Assign to sprints
4. Create GitHub issues for each FR/DOC item
