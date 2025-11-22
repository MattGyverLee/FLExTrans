# Rule Assistant Improvement Project - Team Coordination

**Project:** FLExTrans Rule Assistant Enhancement
**Team Lead:** Development Team Coordinator
**Date:** 2025-11-22
**Branch:** `claude/team-coordination-01MnwRyJdYpujGwZBZ68ELS2`
**Status:** Active Development

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Work Breakdown Structure](#work-breakdown-structure)
3. [Data Flow Architecture](#data-flow-architecture)
4. [Sprint Plan](#sprint-plan)
5. [Team Assignments](#team-assignments)
6. [Success Metrics](#success-metrics)
7. [Risk Assessment](#risk-assessment)
8. [Dependencies and Blockers](#dependencies-and-blockers)

---

## Executive Summary

### Project Goals

The Rule Assistant improvement project addresses critical bugs, usability issues, and documentation gaps reported by field consultants. The project is organized into **3 sprints over 8-10 weeks**, focusing on:

1. **Critical Bug Fixes** (Sprint 1) - Data loss and synchronization issues
2. **Usability Improvements** (Sprint 2) - Better UX and error messages
3. **Documentation** (Sprint 3) - Comprehensive user guides

### Critical Path

The **#1 priority** is **FR-001 (Missing Nodes Bug)** which causes data loss of Variables and Macros sections. This is a blocker for production use and must be fixed in Sprint 1.

### Key Deliverables

- ✅ Bug-free Rule Assistant with no data loss
- ✅ Clear data flow and synchronization model
- ✅ Comprehensive user documentation
- ✅ Template management system
- ✅ Improved error messages

---

## Work Breakdown Structure

### 🔴 Sprint 1: Critical Bugs (Weeks 1-3)

**Duration:** 3 weeks
**Goal:** Fix data loss bugs and establish stable foundation

#### 1.1 FR-001: Missing Nodes Bug (CRITICAL)
**Priority:** P0 - Critical Data Loss
**Effort:** 2 days
**Owner:** Backend Developer

**Problem Analysis:**
- **Root Cause Identified:** Line 1540-1541 in `CreateApertiumRules.py:WriteTransferFile()`
- Code removes **all empty sections** from the transfer file
- This includes user-created but empty `<section-def-vars>` and `<section-def-macros>`
- No distinction between "should preserve" vs. "can discard"

**Tasks:**
- [x] **Task 1.1.1:** Code Review - Analyze `WriteTransferFile()` section removal logic (2 hours)
- [ ] **Task 1.1.2:** Implement section preservation logic (4 hours)
  - Preserve `section-def-vars` even if empty
  - Preserve `section-def-macros` even if empty
  - Preserve `section-def-lists` even if empty
  - Only remove sections that were never in the original file
- [ ] **Task 1.1.3:** Update `ProcessExistingTransferFile()` to track original sections (2 hours)
  - Add instance variable `self.originalSections = set()`
  - Populate it when loading existing file
- [ ] **Task 1.1.4:** Create regression tests (4 hours)
  - Test: Empty vars section is preserved
  - Test: Empty macros section is preserved
  - Test: Populated sections are preserved
  - Test: New empty sections are not added unnecessarily
- [ ] **Task 1.1.5:** User testing with template files (2 hours)

**Acceptance Criteria:**
- ✅ Variables and Macros sections never disappear
- ✅ All sections from original file are preserved
- ✅ Test suite passes with 100% coverage of section handling

**Files to Modify:**
- `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py` (lines 1533-1548)

---

#### 1.2 FR-002: File State Synchronization Issues
**Priority:** P0 - Critical Architecture Issue
**Effort:** 1 week
**Owner:** Backend Developer + Tech Writer

**Problem Analysis:**
- Multiple sources of truth cause confusion
- No clear "reload" mechanism
- Manual edits to `.t1x` may be overwritten
- Users don't understand data flow

**Phase 1: Investigation & Documentation (3 days)**
- [ ] **Task 1.2.1:** Document current data flow completely (1 day)
  - Map all files and their relationships
  - Identify when each file is read/written
  - Document caching behavior
  - Create data flow diagram
- [ ] **Task 1.2.2:** Test manual edit preservation (4 hours)
  - Manually edit .t1x file (add custom macro)
  - Run Rule Assistant
  - Verify if manual edits are preserved
  - Document current behavior
- [ ] **Task 1.2.3:** Test FLEx change detection (4 hours)
  - Add new feature to FLEx
  - Run Rule Assistant
  - Verify if new feature appears
  - Document current behavior

**Phase 2: Implementation (2 days)**
- [ ] **Task 1.2.4:** Improve section preservation in `ProcessExistingTransferFile()` (1 day)
  - Preserve all sections from existing .t1x
  - Mark which rules/macros/vars are "user-created" vs "RA-generated"
  - Add XML comments to mark RA-generated content
- [ ] **Task 1.2.5:** Add warning dialogs (4 hours)
  - Warn when opening RA will regenerate sections
  - Show diff of what will change
  - Give user choice to proceed or cancel
- [ ] **Task 1.2.6:** FLEx reload button design (2 hours)
  - Design GUI change for "Reload FLEx Data" button
  - Specify behavior (re-run GetRuleAssistantStartData)
  - Document in feature spec

**Phase 3: Documentation (1 day)**
- [ ] **Task 1.2.7:** Write user guide section (4 hours)
  - Workflow: RA → manual editing → RA again
  - Best practices for mixed workflow
  - Backup recommendations
- [ ] **Task 1.2.8:** Create troubleshooting guide (4 hours)
  - "My rules disappeared" recovery
  - "FLEx changes not appearing" fix
  - Version control setup guide

**Acceptance Criteria:**
- ✅ Data flow documented with diagrams
- ✅ Manual edits to .t1x are preserved (with clear limitations documented)
- ✅ Users understand when FLEx data is reloaded
- ✅ Warning system prevents accidental data loss
- ✅ Comprehensive troubleshooting guide exists

**Deliverables:**
- Technical spec: `DATA_FLOW.md`
- User guide: `docs/RuleAssistant_UserGuide.md` (Section: "Working with Existing Files")
- Troubleshooting: `docs/RuleAssistant_Troubleshooting.md`

---

#### 1.3 FR-003: Confusing "File Has Been Edited" Error
**Priority:** P1 - High Confusion Factor
**Effort:** 2 days
**Owner:** Backend Developer

**Tasks:**
- [ ] **Task 1.3.1:** Find error message source (2 hours)
  - Grep for "file has been edited" or similar
  - Identify which module generates it
  - Understand detection logic
- [ ] **Task 1.3.2:** Analyze false positive triggers (4 hours)
  - Test with fresh start file
  - Test with replaced file
  - Test with saved file
  - Document when error appears incorrectly
- [ ] **Task 1.3.3:** Fix detection logic or remove warning (4 hours)
  - **Option A:** Improve detection to avoid false positives
  - **Option B:** Rephrase as informational message
  - **Option C:** Remove if not actionable
- [ ] **Task 1.3.4:** Test fixes (2 hours)

**Acceptance Criteria:**
- ✅ No false positive warnings
- ✅ Message is clear and actionable
- ✅ Users understand what to do

---

### 🟡 Sprint 2: Usability Improvements (Weeks 4-6)

**Duration:** 3 weeks
**Goal:** Improve user experience and reduce support burden

#### 2.1 FR-004: Template Management System
**Priority:** P2 - Medium
**Effort:** 1 week
**Owner:** Backend Developer + UI Developer

**Tasks:**
- [ ] **Task 2.1.1:** Create clean templates (2 days)
  - `minimal_template.t1x` - Bare minimum structure
  - `standard_template.t1x` - Common sections pre-populated
  - `bantu_template.t1x` - Bantu noun class setup
- [ ] **Task 2.1.2:** Implement template directory structure (4 hours)
  ```
  Rule Assistant/
    templates/
      minimal_template.t1x
      standard_template.t1x
      bantu_template.t1x
      README_TEMPLATES.md
  ```
- [ ] **Task 2.1.3:** Add GUI buttons (if GUI is Qt/Python) (1 day)
  - "New from Template" button
  - Template selection dialog
  - "Reset to Template" with confirmation
- [ ] **Task 2.1.4:** Backend logic (1 day)
  - Copy template to project location
  - Preserve user rules when resetting
- [ ] **Task 2.1.5:** Documentation (4 hours)
  - How to use templates
  - How to create custom templates

**Acceptance Criteria:**
- ✅ 3 clean templates shipped
- ✅ User can start from template
- ✅ User can reset to clean state
- ✅ Documentation complete

---

#### 2.2 FR-005: Clearer BantuNounClass Warning Message
**Priority:** P2 - Medium
**Effort:** 1 day
**Owner:** Backend Developer

**Tasks:**
- [ ] **Task 2.2.1:** Find warning message location (1 hour)
- [ ] **Task 2.2.2:** Rewrite message to be specific (2 hours)
  - Clarify it's looking in transfer file, not FLEx
  - Specify exact location: `<section-def-attrs>`
  - Provide actionable solution
- [ ] **Task 2.2.3:** Add link to documentation (1 hour)
- [ ] **Task 2.2.4:** Review similar warnings (4 hours)
  - Find all ambiguous error messages
  - Update to be more specific

**New Message Template:**
```
Warning: Attribute 'BantuNounClass' not found in transfer rule file.

This attribute should be defined in <section-def-attrs> of your transfer
rules file (transfer_rules.t1x), not as a FLEx Inflection Feature.

To fix:
  1. Run "Set Up Transfer Rule Categories and Attributes" module
  2. Or manually add to <section-def-attrs> in transfer_rules.t1x

See: docs/DisjointFeatureSets.md for details on Bantu noun classes.
```

**Acceptance Criteria:**
- ✅ Message is unambiguous
- ✅ User knows where to look (file + section)
- ✅ User knows how to fix (specific steps)
- ✅ Link to docs provided

---

#### 2.3 FR-006: FLEx Data Reload Button
**Priority:** P2 - Medium
**Effort:** 3 days
**Owner:** Backend Developer + UI Developer

**Tasks:**
- [ ] **Task 2.3.1:** Design button placement (2 hours)
  - Menu location or toolbar
  - Icon design
- [ ] **Task 2.3.2:** Implement reload function (1 day)
  - Re-run `GetRuleAssistantStartData()`
  - Update GUIinput.xml
  - Reload in UI without restart
- [ ] **Task 2.3.3:** Add confirmation dialog (4 hours)
  - "Reload categories, features, affixes from FLEx?"
  - "Existing rules will be preserved"
- [ ] **Task 2.3.4:** Add reload summary (4 hours)
  - Display: "Reloaded: 12 categories, 45 features, 23 affixes"
  - Show what changed since last load
- [ ] **Task 2.3.5:** Test with FLEx changes (4 hours)

**Acceptance Criteria:**
- ✅ Button reloads FLEx data
- ✅ No restart required
- ✅ Rules are preserved
- ✅ Summary shows what was loaded

---

### 🟢 Sprint 3: Documentation (Weeks 7-8)

**Duration:** 2 weeks
**Goal:** Comprehensive documentation to reduce support burden

#### 3.1 DOC-001: Rule Assistant Workflow Guide
**Priority:** P0 - Critical for Adoption
**Effort:** 1 week
**Owner:** Tech Writer + Linguist Consultant

**Structure:**
```markdown
# Rule Assistant User Guide

## Chapter 1: Introduction
- What is Rule Assistant
- When to use it
- Prerequisites

## Chapter 2: Getting Started
- First time setup
- Module prerequisites
- Creating your first rule

## Chapter 3: Working with Existing Files
- Opening RA with existing transfer file
- What gets loaded vs. what gets overwritten
- Mixed workflow: RA + manual editing
- Best practices

## Chapter 4: Advanced Features
- Disjoint feature sets (Bantu noun classes)
- Template management
- Debugging rules

## Chapter 5: Troubleshooting
- Common errors and solutions
- Recovery procedures
- Getting help

## Appendix: Technical Reference
- File formats
- Data flow diagrams
- API reference (for developers)
```

**Tasks:**
- [ ] **Task 3.1.1:** Chapter 1-2: Basics (2 days)
- [ ] **Task 3.1.2:** Chapter 3: Existing Files (2 days) - **CRITICAL**
- [ ] **Task 3.1.3:** Chapter 4: Advanced (1 day)
- [ ] **Task 3.1.4:** Chapter 5: Troubleshooting (1 day)
- [ ] **Task 3.1.5:** Screenshots and diagrams (1 day)

**Acceptance Criteria:**
- ✅ Complete user guide with examples
- ✅ All workflows documented
- ✅ FAQ section answers common questions
- ✅ Review by field consultant

---

#### 3.2 DOC-002: Disjoint Feature Sets Guide
**Priority:** P1 - High
**Effort:** 3 days
**Owner:** Linguist Consultant + Tech Writer

**Tasks:**
- [ ] **Task 3.2.1:** Conceptual explanation (1 day)
  - What are disjoint feature sets
  - Why needed for Bantu
  - FLEx vs. Apertium representation
- [ ] **Task 3.2.2:** Step-by-step tutorial (1 day)
  - Complete worked example
  - Annotated XML
  - Common mistakes
- [ ] **Task 3.2.3:** Language-specific guides (1 day)
  - Bantu noun classes (detailed)
  - Template for other languages

**Deliverable:** `docs/DisjointFeatureSets.md`

---

#### 3.3 DOC-003: Module Prerequisites Guide
**Priority:** P1 - High
**Effort:** 2 days
**Owner:** Tech Writer

**Tasks:**
- [ ] **Task 3.3.1:** Create dependency chart (4 hours)
- [ ] **Task 3.3.2:** Write module descriptions (1 day)
- [ ] **Task 3.3.3:** Workflow scenarios (4 hours)

**Deliverable:** `docs/ModuleWorkflow.md`

---

## Data Flow Architecture

### Current Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA FLOW DIAGRAM                         │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   FLEx DB    │  (Source & Target Projects)
│  (Source of  │
│   Truth for  │
│  Linguistic  │
│    Data)     │
└──────┬───────┘
       │
       │ RuleAssistant.py:GetRuleAssistantStartData()
       │ - Queries categories, features, values
       │ - Queries affix templates
       │ - Runs every time RA module starts
       ↓
┌────────────────┐
│ GUIinput.xml   │  (Cached FLEx Data)
│                │
│ Contains:      │
│ - Categories   │
│ - Features     │
│ - Values       │
│ - Valid combos │
└────────┬───────┘
         │
         │ Used by Rule Assistant GUI
         ↓
┌──────────────────────────────────────────────┐
│      Rule Assistant GUI (External .exe)       │
│                                               │
│  Reads:                                       │
│  1. GUIinput.xml (FLEx data)                 │
│  2. RuleAssistantRules.xml (existing rules)  │
│  3. TestData.html (sample translations)      │
│                                               │
│  User creates/edits rules in UI              │
│                                               │
│  Writes:                                      │
│  - RuleAssistantRules.xml (updated)          │
└────────────────┬─────────────────────────────┘
                 │
                 │ On Save
                 ↓
         ┌────────────────────┐
         │RuleAssistantRules  │
         │      .xml          │
         │                    │
         │ (Rule Specs in     │
         │  FLExTrans format) │
         └────────┬───────────┘
                  │
                  │ CreateApertiumRules.CreateRules()
                  ↓
         ┌─────────────────────────────────┐
         │  CreateApertiumRules.py         │
         │                                  │
         │  ProcessExistingTransferFile()   │
         │  - Reads existing .t1x          │
         │  - Extracts IDs, vars, macros   │  ┌──────────────┐
         │  - Preserves structure          ├─→│ .t1x.bak     │
         │                                  │  │ (Backup)     │
         │  ProcessAssistantFile()          │  └──────────────┘
         │  - Reads RuleAssistantRules.xml │
         │  - Generates Apertium XML       │
         │                                  │
         │  WriteTransferFile()             │
         │  - Merges with existing .t1x    │
         │  - Writes final output          │
         └──────────────┬──────────────────┘
                        │
                        │ Output
                        ↓
              ┌──────────────────┐
              │ transfer_rules   │
              │     .t1x         │
              │                  │
              │ (Apertium        │
              │  Transfer Rules) │
              │                  │
              │ May contain:     │
              │ - RA-generated   │
              │ - Manual edits   │
              └──────────────────┘
```

### Sources of Truth

| Data Type | Source of Truth | Updated When | Cached Where |
|-----------|----------------|--------------|--------------|
| **FLEx Categories** | FLEx Database | User edits FLEx project | GUIinput.xml |
| **FLEx Features** | FLEx Database | User edits FLEx project | GUIinput.xml |
| **FLEx Feature Values** | FLEx Database | User edits FLEx project | GUIinput.xml |
| **Rule Specifications** | RuleAssistantRules.xml | User edits in RA GUI | (none) |
| **Generated Transfer Rules** | transfer_rules.t1x | RA generates from specs | (none) |
| **Manual Transfer Edits** | transfer_rules.t1x | User manually edits .t1x | (none) |
| **Variables/Macros** | transfer_rules.t1x | RA generates OR user adds | (none) |

### Synchronization Points

#### When RA Module Starts:
1. ✅ **FLEx data IS reloaded** - `GetRuleAssistantStartData()` queries fresh from DB
2. ✅ **GUIinput.xml is regenerated** - Always fresh
3. ✅ **RuleAssistantRules.xml is read** - Existing rules loaded into GUI
4. ❌ **transfer_rules.t1x is NOT read by GUI** - GUI doesn't know about manual edits

#### When User Clicks "Save" in RA GUI:
1. ✅ **RuleAssistantRules.xml is updated** - New/modified rule specs saved
2. ✅ **CreateRules is called** - Generates Apertium rules
3. ✅ **transfer_rules.t1x backup is created** - Timestamped .bak file
4. ⚠️ **Existing .t1x is processed** - Some sections preserved, some regenerated
5. ⚠️ **New .t1x is written** - May overwrite manual edits depending on section

### Current Behavior Analysis

#### What IS Preserved:
- ✅ Existing `<def-cat>` entries (categories)
- ✅ Existing `<def-attr>` entries (attributes)
- ✅ Existing `<def-var>` entries (variables) - **IDs tracked**
- ✅ Existing `<def-list>` entries (lists)
- ✅ Existing `<def-macro>` entries - **IDs tracked**
- ✅ Existing `<rule>` entries if `overwrite_rules="no"` (default)

#### What MIGHT BE LOST:
- ❌ **Empty sections** - Removed by WriteTransferFile() (FR-001 bug)
- ❌ Manual additions to sections that RA regenerates
- ⚠️ Manual edits to RA-generated macros (if macro reuse enabled)
- ⚠️ Comments in certain sections

#### What Triggers Regeneration:
- Setting `overwrite_rules="yes"` in RuleAssistantRules.xml
- Running RA always regenerates:
  - `<section-def-cats>` (categories) - **adds new, keeps old**
  - `<section-def-attrs>` (attributes) - **adds new, keeps old**
  - `<section-rules>` - **based on overwrite_rules setting**

### Identified Issues

#### Issue 1: Empty Section Deletion (FR-001)
**Location:** `CreateApertiumRules.py:1540-1541`
```python
for name in RuleGenerator.SectionSequence:
    elem = self.GetSection(name)
    if len(elem) == 0:
        self.root.remove(elem)  # ❌ DELETES ALL EMPTY SECTIONS
```
**Problem:** Doesn't distinguish "user created but empty" from "never existed"

**Fix Strategy:**
- Track which sections existed in original file
- Only remove sections that were never in original
- Always preserve: `section-def-vars`, `section-def-macros`, `section-def-lists`

#### Issue 2: No FLEx Reload Mechanism (FR-006)
**Problem:** User must restart RA module to reload FLEx changes

**Fix Strategy:**
- Add "Reload FLEx Data" button to GUI
- Re-run `GetRuleAssistantStartData()`
- Regenerate GUIinput.xml
- Reload in UI without closing window

#### Issue 3: User Confusion About Data Flow (FR-002)
**Problem:** Users don't understand what gets reloaded vs. preserved

**Fix Strategy:**
- Document data flow clearly
- Add warning before overwriting sections
- Show diff of changes
- Provide "Safe Mode" option

---

## Sprint Plan

### Sprint 1: Critical Bugs (Weeks 1-3)

**Sprint Goal:** Eliminate data loss bugs and establish stable foundation

**Week 1:**
- Day 1-2: FR-001 (Missing Nodes) - Analysis and fix
- Day 3-4: FR-001 testing and regression tests
- Day 5: FR-002 Phase 1 - Data flow investigation

**Week 2:**
- Day 1-2: FR-002 Phase 1 - Complete documentation
- Day 3-4: FR-002 Phase 2 - Implementation
- Day 5: FR-002 testing

**Week 3:**
- Day 1-2: FR-002 Phase 3 - Documentation
- Day 3-4: FR-003 (File Edited Error) - Fix
- Day 5: Sprint review, bug fixes, prep for Sprint 2

**Sprint 1 Deliverables:**
- ✅ Bug-free section preservation
- ✅ Data flow fully documented
- ✅ Troubleshooting guide
- ✅ Warning system to prevent data loss
- ✅ All critical bugs resolved

---

### Sprint 2: Usability (Weeks 4-6)

**Sprint Goal:** Improve UX and reduce support requests

**Week 4:**
- Day 1-3: FR-004 (Template Management) - Create templates
- Day 4-5: FR-004 - Implement backend logic

**Week 5:**
- Day 1-2: FR-004 - GUI implementation (if applicable)
- Day 3: FR-004 - Testing and documentation
- Day 4-5: FR-005 (Better Error Messages) - Fix all warnings

**Week 6:**
- Day 1-3: FR-006 (Reload Button) - Implementation
- Day 4: FR-006 - Testing
- Day 5: Sprint review

**Sprint 2 Deliverables:**
- ✅ 3 clean templates
- ✅ Template management system
- ✅ Clear, actionable error messages
- ✅ FLEx reload button

---

### Sprint 3: Documentation (Weeks 7-8)

**Sprint Goal:** Comprehensive documentation to enable users

**Week 7:**
- Day 1-2: DOC-001 Chapter 1-2 (Basics)
- Day 3-4: DOC-001 Chapter 3 (Existing Files) **CRITICAL**
- Day 5: DOC-001 Chapter 4-5 (Advanced, Troubleshooting)

**Week 8:**
- Day 1-2: DOC-002 (Disjoint Feature Sets)
- Day 3: DOC-003 (Module Prerequisites)
- Day 4: Final review, screenshots, diagrams
- Day 5: User testing, revisions, project closeout

**Sprint 3 Deliverables:**
- ✅ Complete Rule Assistant User Guide
- ✅ Disjoint Feature Sets Tutorial
- ✅ Module Workflow Guide
- ✅ All documentation reviewed by consultant

---

## Team Assignments

### Core Team

#### Backend Developer (1 FTE)
**Responsibilities:**
- FR-001, FR-002, FR-003 bug fixes
- Template management backend
- Code review
- Test suite development

**Skills Required:**
- Python (advanced)
- XML processing (lxml, ElementTree)
- FLEx database queries
- Apertium transfer rules

**Critical for:**
- Sprint 1 (full time)
- Sprint 2 (75% time)

---

#### Technical Writer (0.5 FTE)
**Responsibilities:**
- Data flow documentation
- User guide writing
- Troubleshooting guide
- Review all error messages

**Skills Required:**
- Technical writing
- Understanding of MT systems
- Linguistic background (helpful)

**Critical for:**
- Sprint 1 (25% time - documentation)
- Sprint 3 (full time)

---

#### UI Developer (0.25 FTE)
**Responsibilities:**
- Template selection dialog
- Reload FLEx button
- Warning dialogs
- GUI improvements

**Skills Required:**
- Qt/PyQt (if RA GUI is Python)
- Or C#/.NET (if RA GUI is .NET)
- UX design

**Critical for:**
- Sprint 2 (50% time)

**Note:** May be external contractor or outsourced

---

#### Linguist Consultant (0.1 FTE)
**Responsibilities:**
- Review documentation accuracy
- Provide linguistic examples
- User testing
- Disjoint feature sets guide

**Skills Required:**
- Field linguistics experience
- Bantu languages (preferred)
- FLExTrans user

**Critical for:**
- Sprint 3 (documentation review)
- DOC-002 (co-author)

---

#### QA Tester (0.25 FTE)
**Responsibilities:**
- Regression testing
- User acceptance testing
- Test data creation
- Bug validation

**Critical for:**
- All sprints (ongoing)

---

### Optional: External Resources

#### Graphic Designer (Contract)
- Create diagrams for documentation
- Screenshot preparation
- Icon design for UI buttons

**Effort:** 2-3 days across project

---

## Success Metrics

### Sprint 1 Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Critical Bugs Resolved | 100% (3/3) | All FR-001, FR-002, FR-003 closed |
| Data Loss Incidents | 0 | No user-reported data loss after fix |
| Test Coverage | >80% | pytest-cov on CreateApertiumRules.py |
| Documentation Completeness | 100% | Data flow + troubleshooting complete |

### Sprint 2 Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Template Usage | >30% | Users starting from template |
| Error Message Clarity | 80% improvement | User testing survey |
| Support Request Reduction | 40% | Compared to pre-project baseline |
| UI Improvements Deployed | 100% | All FR-004, FR-005, FR-006 complete |

### Sprint 3 Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Documentation Coverage | 100% | All workflows documented |
| User Satisfaction | >4.0/5.0 | Post-documentation survey |
| Time to First Rule | 50% reduction | New user testing |
| FAQ Coverage | 80% | Support questions answered in docs |

### Overall Project Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Project Completion | 8-10 weeks | Sprint velocity tracking |
| Budget Adherence | ±10% | Weekly status reports |
| User Adoption | +50% | Active projects using RA |
| Zero Data Loss | 100% | No data loss bugs after Sprint 1 |

---

## Risk Assessment

### High Risks

#### Risk 1: Data Loss Bug Has Deeper Issues
**Probability:** Medium (30%)
**Impact:** High - Extends Sprint 1

**Mitigation:**
- Thorough code review before implementation
- Multiple test scenarios
- Beta testing with backup files
- Rollback plan

**Contingency:**
- Add 1 week buffer to Sprint 1
- Delay Sprint 2 start if needed

---

#### Risk 2: GUI is Not Python (External .exe)
**Probability:** High (80% - confirmed external program)
**Impact:** High - Can't easily add buttons

**Mitigation:**
- Focus on backend fixes (FR-001, FR-002)
- Document GUI changes for future implementation
- Provide command-line workarounds
- Consider separate GUI update project

**Contingency:**
- FR-004 (Templates): Backend only, no GUI buttons
- FR-006 (Reload): Document manual workaround
- Adjust Sprint 2 scope

---

#### Risk 3: Consultant Availability
**Probability:** Medium (40%)
**Impact:** Medium - Documentation quality

**Mitigation:**
- Schedule consultant time early
- Get commitment for Sprint 3
- Prepare materials in advance
- Record sessions for async review

**Contingency:**
- Use internal linguist
- Extend Sprint 3 timeline
- Phased documentation release

---

### Medium Risks

#### Risk 4: Test Coverage Insufficient
**Probability:** Medium (50%)
**Impact:** Medium - Regression bugs

**Mitigation:**
- Create test plan in Week 1
- Write tests alongside fixes
- QA tester validates coverage
- Beta testing with users

---

#### Risk 5: Scope Creep
**Probability:** High (70%)
**Impact:** Medium - Timeline slip

**Mitigation:**
- Strict sprint boundaries
- Change request process
- Weekly stakeholder updates
- "Future Work" backlog

**Contingency:**
- De-scope Sprint 2 items
- Move DOC-002, DOC-003 to post-project

---

### Low Risks

#### Risk 6: File Format Changes
**Probability:** Low (10%)
**Impact:** Low - Easy to adapt

**Mitigation:**
- Use defensive parsing
- Validate XML schemas
- Version compatibility testing

---

## Dependencies and Blockers

### External Dependencies

#### 1. FLEx Database API
**Dependency:** Access to FLEx database for querying categories/features
**Impact:** Required for FR-002, FR-006
**Mitigation:** API is stable and well-documented
**Owner:** Already available

#### 2. Rule Assistant GUI Source Code
**Dependency:** May need GUI source to add buttons (FR-004, FR-006)
**Impact:** If GUI is compiled external program, can't add buttons
**Status:** **BLOCKER if GUI changes required**
**Mitigation:** Backend-only implementation, document GUI specs for future

#### 3. Apertium Transfer DTD
**Dependency:** DTD defines valid transfer rule structure
**Impact:** Must preserve DTD compliance
**Mitigation:** DTD is stable, well-known
**Owner:** External (Apertium project)

### Internal Dependencies

#### Sprint 1 → Sprint 2
- **Dependency:** FR-001 must be fully resolved before templates (FR-004)
- **Reason:** Templates will include empty sections
- **Critical Path:** YES

#### Sprint 1 → Sprint 3
- **Dependency:** Data flow documentation (FR-002) required for user guide (DOC-001)
- **Reason:** User guide explains workflow based on data flow
- **Critical Path:** YES

#### Sprint 2 → Sprint 3
- **Dependency:** Error messages (FR-005) should be finalized before troubleshooting guide
- **Reason:** Guide references error messages
- **Critical Path:** NO (can proceed in parallel)

### Current Blockers

**None identified** - Project can start immediately

### Potential Blockers

1. **GUI Access:** If buttons required, need GUI source or contact with GUI developer
   - **Mitigation:** Backend-first approach
   - **Timeline Impact:** +2 weeks if GUI changes needed

2. **Consultant Schedule:** Need linguist for DOC-002
   - **Mitigation:** Schedule in advance
   - **Timeline Impact:** +1 week if delayed

3. **Testing Resources:** Need FLEx projects with various configurations
   - **Mitigation:** Create synthetic test projects
   - **Timeline Impact:** +3 days if missing

---

## Communication Plan

### Weekly Team Meetings
- **When:** Every Monday, 10:00 AM
- **Duration:** 1 hour
- **Attendees:** All team members
- **Agenda:**
  - Sprint progress review
  - Blocker identification
  - Next week planning
  - Risk review

### Daily Standups
- **When:** Every morning, 9:15 AM (async for distributed team)
- **Format:** Slack/Teams message
- **Contents:**
  - What I did yesterday
  - What I'm doing today
  - Any blockers

### Sprint Reviews
- **When:** End of each sprint
- **Duration:** 2 hours
- **Attendees:** Team + stakeholders
- **Demo:** Working features
- **Retrospective:** What went well, what to improve

### Stakeholder Updates
- **When:** Bi-weekly (every other Friday)
- **Format:** Email + dashboard
- **Contents:**
  - Progress against metrics
  - Risk status
  - Budget status
  - Next milestone preview

---

## Tools and Infrastructure

### Development Tools
- **Version Control:** Git (GitHub)
- **Branch Strategy:** Feature branches → PR → main
- **Code Review:** All PRs require 1 approval
- **CI/CD:** GitHub Actions for automated testing

### Project Management
- **Task Tracking:** GitHub Issues + Projects board
- **Documentation:** Markdown in `/docs` directory
- **Time Tracking:** (Optional) Toggl or Harvest

### Testing
- **Unit Tests:** pytest
- **Coverage:** pytest-cov (target >80%)
- **Integration Tests:** Manual + automated
- **Test Data:** Synthetic FLEx projects in `/test_data`

### Documentation
- **Format:** Markdown
- **Diagrams:** Mermaid (embedded in Markdown)
- **Screenshots:** PNG in `/docs/images`
- **Review:** Pull request process

---

## Next Steps (Week 1)

### Immediate Actions (Days 1-2)

1. **Team Assembly**
   - [ ] Confirm team members availability
   - [ ] Schedule kickoff meeting
   - [ ] Set up communication channels (Slack/Teams)

2. **Infrastructure Setup**
   - [ ] Create GitHub project board
   - [ ] Create sprint milestones
   - [ ] Set up CI/CD pipeline
   - [ ] Create test data repository

3. **FR-001 Investigation**
   - [ ] Backend developer: Analyze WriteTransferFile()
   - [ ] Create test case that reproduces bug
   - [ ] Propose fix approach

4. **Documentation Kickoff**
   - [ ] Tech writer: Review existing docs
   - [ ] Identify documentation gaps
   - [ ] Create documentation templates

### Week 1 Goals

- ✅ Team assembled and briefed
- ✅ Infrastructure ready
- ✅ FR-001 root cause confirmed
- ✅ FR-001 fix implemented and tested
- ✅ FR-002 investigation started
- ✅ Sprint 1 detailed task breakdown complete

---

## Appendix A: File Inventory

### Key Files to Modify

| File | Purpose | Sprints |
|------|---------|---------|
| `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py` | Rule generation engine | 1, 2 |
| `/home/user/FLExTrans/Dev/Modules/RuleAssistant.py` | Main module orchestration | 1, 2 |
| `/home/user/FLExTrans/Rule Assistant/templates/*.t1x` | Template files | 2 |
| `/home/user/FLExTrans/docs/RuleAssistant_UserGuide.md` | User documentation | 3 |
| `/home/user/FLExTrans/docs/DisjointFeatureSets.md` | Feature set tutorial | 3 |
| `/home/user/FLExTrans/docs/DATA_FLOW.md` | Architecture doc | 1 |

### Test Files

| File | Purpose |
|------|---------|
| `/home/user/FLExTrans/test_rule_assistant.py` | Integration tests |
| `/home/user/FLExTrans/tests/test_section_preservation.py` | FR-001 regression tests |
| `/home/user/FLExTrans/tests/test_templates.py` | FR-004 tests |

---

## Appendix B: Glossary

**RA:** Rule Assistant
**FR:** Feature Request (from RuleAssistant_Feature_Requests.md)
**DOC:** Documentation item
**FLEx:** FieldWorks Language Explorer
**Apertium:** Open-source machine translation platform
**Transfer Rules:** Rules that map source language structure to target language
**GUIinput.xml:** XML file containing FLEx data for GUI
**RuleAssistantRules.xml:** XML file containing rule specifications
**transfer_rules.t1x:** Apertium transfer rule file (output)

---

## Document Control

**Version:** 1.0
**Last Updated:** 2025-11-22
**Next Review:** Weekly sprint reviews
**Approval:** Pending stakeholder sign-off

**Change Log:**
- 2025-11-22: Initial version created by Team Lead

---

**Status:** Ready for Team Review and Sprint 1 Kickoff
