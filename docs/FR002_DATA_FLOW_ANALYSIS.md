# FR-002: File State Synchronization Issues - Data Flow Analysis

**Date:** 2025-11-22
**Investigator:** Coder Agent 2 (File I/O & State Management Specialist)
**Branch:** claude/fix-file-sync-investigation-01MnwRyJdYpujGwZBZ68ELS2

## Executive Summary

This document provides a comprehensive analysis of file I/O, state management, and data synchronization in the FLExTrans Rule Assistant. The investigation reveals **critical gaps in user communication** and **potential data loss scenarios** due to unclear file relationships and lack of explicit synchronization mechanisms.

### Key Findings

1. **No Caching Mechanism Exists** - All data is read fresh from sources on each run
2. **Complex Multi-File Workflow** - At least 6 different files are involved in the Rule Assistant workflow
3. **No Change Detection** - The system does not detect or warn about external file modifications
4. **Unclear Source of Truth** - Users are confused about which file is authoritative
5. **No Synchronization Logic** - Manual edits to .t1x can be silently overwritten

---

## Problem Statement

Users report confusion about:
- **What file Rule Assistant reads from?** (FLEx DB, .t1x, or cached XML?)
- **Are manual .t1x edits preserved?** (Currently: NO - they are silently overwritten)
- **Are FLEx project changes detected?** (Currently: NO - no detection mechanism)
- **When is data synchronized?** (Currently: Never - data flows one direction only)

---

## Complete Data Flow Analysis

### ASCII Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         RULE ASSISTANT WORKFLOW                          │
└─────────────────────────────────────────────────────────────────────────┘

    [USER INITIATES]
           │
           ▼
    ┌──────────────┐
    │ RuleAssistant│  ← Entry point: MainFunction()
    │    .py       │
    └──────┬───────┘
           │
           ├─────────────────────────────────────────────────┐
           │                                                 │
           ▼                                                 ▼
    ┌─────────────┐                                  ┌─────────────┐
    │   FLEx DB   │ (READ ONLY)                      │ Config File │ (READ ONLY)
    │  (Source)   │                                  │flextools.ini│
    └──────┬──────┘                                  └──────┬──────┘
           │                                                │
           │ Extract:                                       │ Get paths:
           │ - Categories (POS)                             │ - RULE_ASSISTANT_FILE
           │ - Features                                     │ - TRANSFER_RULES_FILE
           │ - Feature Values                               │ - SOURCE_TEXT_NAME
           │ - Category Hierarchies                         │
           │ - Affix Templates                              │
           │                                                │
           ▼                                                ▼
    ┌─────────────┐                              ┌──────────────────┐
    │   FLEx DB   │ (READ ONLY)                  │  Configuration   │
    │  (Target)   │                              │    Settings      │
    └──────┬──────┘                              └──────────────────┘
           │
           │ Extract same data
           │ for target language
           │
           ▼
    ┌─────────────────────────────────────────────┐
    │   STEP 1: GetRuleAssistantStartData()       │
    │   Builds StartData object containing:       │
    │   - Source DB: categories, features, etc.   │
    │   - Target DB: categories, features, etc.   │
    └──────────────┬──────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────────────┐
    │   FILE WRITE #1: GUI Input File             │
    │   Location: Build/ruleAssistantGUIinput.xml │
    │   Purpose: FLEx data for GUI to display     │
    │   Content: Categories, Features, Values     │
    │   Lifecycle: Temporary - regenerated each   │
    │              time Rule Assistant runs        │
    └──────────────┬──────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────────────┐
    │   STEP 2: GetTestDataFile()                 │
    │   (if SOURCE_TEXT_NAME configured)          │
    └──────────────┬──────────────────────────────┘
                   │
                   ├───────────────┬───────────────────┐
                   ▼               ▼                   ▼
         ┌────────────┐  ┌──────────────┐   ┌─────────────────┐
         │  FLEx DB   │  │  Bilingual   │   │ Interlinear Text│
         │Source Text │  │  Dictionary  │   │   Extraction    │
         └─────┬──────┘  └──────┬───────┘   └────────┬────────┘
               │                │                    │
               │                │                    │
               ▼                ▼                    ▼
    ┌──────────────────────────────────────────────────────┐
    │   FILE WRITE #2: Source Test Data                    │
    │   Location: Build/RuleAssistantSourceTestData.txt    │
    │   Lifecycle: Temporary - regenerated each run        │
    └───────────────────────┬──────────────────────────────┘
                            │
                            │ Process with lt-proc
                            ▼
    ┌──────────────────────────────────────────────────────┐
    │   FILE WRITE #3: Target Test Data                    │
    │   Location: Build/RuleAssistantTargetTestData.txt    │
    │   Lifecycle: Temporary - regenerated each run        │
    └───────────────────────┬──────────────────────────────┘
                            │
                            │ Convert to HTML
                            ▼
    ┌──────────────────────────────────────────────────────┐
    │   FILE WRITE #4: Display Data (HTML)                 │
    │   Location: Build/RuleAssistantDisplayData.html      │
    │   Purpose: Visual test data for GUI                  │
    │   Lifecycle: Temporary - regenerated each run        │
    └───────────────────────┬──────────────────────────────┘
                            │
                            ▼
    ┌─────────────────────────────────────────────────────┐
    │   STEP 3: StartRuleAssistant()                      │
    │   Launch external GUI program:                      │
    │   FLExTransRuleAssistant.exe                        │
    │                                                     │
    │   Parameters passed:                                │
    │   1. ruleAssistantFile (Rules XML)                  │
    │   2. ruleAssistGUIinputfile (FLEx data)            │
    │   3. testDataFile (HTML display)                    │
    │   4. fromLRT flag (y/n)                            │
    │   5. Interface language code                        │
    └──────────────┬────────────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────────────────────┐
    │   GUI PROGRAM EXECUTION (Black Box)                 │
    │                                                     │
    │   Reads:                                            │
    │   - ruleAssistantGUIinputfile (FLEx categories)    │
    │   - ruleAssistantFile (existing rules - if exists) │
    │   - testDataFile (display in UI)                   │
    │                                                     │
    │   User Actions:                                     │
    │   - Create/modify/delete rules                     │
    │   - Save changes                                    │
    │                                                     │
    │   Writes:                                           │
    │   - ruleAssistantFile (updated rules XML)          │
    │                                                     │
    │   Returns:                                          │
    │   - Exit code (1=single rule, 2=all rules)         │
    │   - Rule number (if single rule)                   │
    │   - LRT flag (if user wants Live Rule Tester)      │
    └──────────────┬────────────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────────────────────┐
    │   STEP 4: CreateApertiumRules.CreateRules()        │
    │   (only if user saved changes)                     │
    └──────────────┬────────────────────────────────────┘
                   │
                   ├───────────────────────────────────┐
                   ▼                                   ▼
    ┌──────────────────────┐           ┌──────────────────────┐
    │   FILE READ:         │           │  FILE READ/WRITE:    │
    │ RuleAssistantRules   │           │  transfer_rules.t1x  │
    │      .xml             │           │                      │
    │ (USER'S RULES)       │           │  *** CRITICAL ***    │
    └──────┬───────────────┘           │  Manual edits to     │
           │                           │  this file are       │
           │                           │  OVERWRITTEN!        │
           │                           └──────────┬───────────┘
           │                                      │
           │                                      │
           ▼                                      ▼
    ┌─────────────────────────────────────────────────────┐
    │   CreateApertiumRules Process:                      │
    │                                                     │
    │   1. Parse RuleAssistantRules.xml                   │
    │   2. Read existing transfer_rules.t1x (if exists)   │
    │   3. Create backup: transfer_rules.t1x.DATETIME.bak│
    │   4. Generate Apertium transfer rules               │
    │   5. Merge with existing rules                      │
    │   6. Write to transfer_rules.t1x                    │
    │                                                     │
    │   NOTE: This process queries FLEx DB again for:     │
    │   - Affix glosses                                   │
    │   - Feature values                                  │
    │   - Lemmas                                          │
    │   - Category hierarchies                            │
    └─────────────────────────────────────────────────────┘

    [WORKFLOW COMPLETE]
```

---

## File Inventory

### 1. Configuration File
- **Path:** `flextools.ini` (in project directory)
- **Purpose:** Configuration settings
- **When Created:** By user/setup wizard
- **When Read:** Every Rule Assistant run (MainFunction startup)
- **When Written:** By configuration tools (not Rule Assistant)
- **Source of Truth:** YES (for configuration)
- **Contains:**
  - `RuleAssistantRulesFile` path
  - `TransferRulesFile` path
  - `SourceTextName`
  - Other FLExTrans settings

### 2. FLEx Database (Source)
- **Path:** Managed by FLEx (user's project folder)
- **Purpose:** Source language grammatical data
- **When Created:** By FLEx
- **When Read:** Every Rule Assistant run
- **When Written:** Never (by Rule Assistant)
- **Source of Truth:** YES (for source language grammar)
- **Contains:**
  - Part-of-speech categories
  - Grammatical features
  - Feature values
  - Affix templates
  - Source texts

### 3. FLEx Database (Target)
- **Path:** Managed by FLEx (target project folder)
- **Purpose:** Target language grammatical data
- **When Created:** By FLEx
- **When Read:** Every Rule Assistant run
- **When Written:** Never (by Rule Assistant)
- **Source of Truth:** YES (for target language grammar)
- **Contains:**
  - Part-of-speech categories
  - Grammatical features
  - Feature values
  - Affix templates

### 4. GUI Input File
- **Path:** `Build/ruleAssistantGUIinput.xml`
- **Purpose:** FLEx grammatical data formatted for GUI consumption
- **When Created:** Every Rule Assistant run
- **When Read:** By GUI program
- **When Written:** Every Rule Assistant run (overwritten)
- **Source of Truth:** NO (derived from FLEx DBs)
- **Lifecycle:** Temporary - regenerated each run
- **Contains:**
  - `<FLExData>` root element
  - `<SourceData>` with categories and features
  - `<TargetData>` with categories and features

### 5. Test Data Files (Optional)
**a) Source Test Data**
- **Path:** `Build/RuleAssistantSourceTestData.txt`
- **Purpose:** Interlinear text for testing
- **When Created:** If SOURCE_TEXT_NAME configured
- **When Read:** By lt-proc for bilingual lookup
- **When Written:** Every Rule Assistant run
- **Source of Truth:** NO (derived from FLEx DB)
- **Lifecycle:** Temporary - regenerated each run

**b) Target Test Data**
- **Path:** `Build/RuleAssistantTargetTestData.txt`
- **Purpose:** Bilingual lookup results
- **When Created:** After lt-proc processing
- **When Read:** For HTML generation
- **When Written:** Every Rule Assistant run
- **Source of Truth:** NO (derived from source + bilingual dict)
- **Lifecycle:** Temporary - regenerated each run

**c) Display Data (HTML)**
- **Path:** `Build/RuleAssistantDisplayData.html`
- **Purpose:** Visual test data display in GUI
- **When Created:** Every Rule Assistant run
- **When Read:** By GUI program for display
- **When Written:** Every Rule Assistant run
- **Source of Truth:** NO (derived from test data)
- **Lifecycle:** Temporary - regenerated each run

### 6. Rule Assistant Rules File
- **Path:** `Build/RuleAssistantRules.xml` (default) or user-specified
- **Purpose:** Storage for user-created transfer rules (high-level format)
- **When Created:** First time GUI saves
- **When Read:**
  - By GUI program (on startup)
  - By CreateApertiumRules (for conversion)
- **When Written:** By GUI program (when user saves)
- **Source of Truth:** YES (for user's rule definitions)
- **Lifecycle:** Persistent - survives across runs
- **Format:** Custom XML format (Rule Assistant schema)
- **Contains:**
  - `<FLExTransRule>` elements
  - Source/target word patterns
  - Feature mappings
  - Rule metadata

### 7. Transfer Rules File (.t1x)
- **Path:** User-specified via config (e.g., `transfer_rules.t1x`)
- **Purpose:** Apertium transfer rules (executable format)
- **When Created:** First time CreateRules runs
- **When Read:** By CreateApertiumRules (to merge with new rules)
- **When Written:** By CreateApertiumRules (after GUI saves)
- **Source of Truth:** COMPLICATED - see analysis below
- **Lifecycle:** Persistent - modified over time
- **Format:** Apertium transfer XML format
- **Contains:**
  - `<def-cat>` category definitions
  - `<def-attr>` attribute definitions
  - `<def-macro>` macros
  - `<rule>` transfer rules
  - Comments and metadata

**CRITICAL ISSUE:** Manual edits to this file are silently overwritten when CreateApertiumRules runs!

---

## Data Flow Sequence

### Sequence 1: Initial Startup

```
1. User clicks "Rule Assistant" in FlexTools
2. MainFunction() called
3. ReadConfig.readConfig() → reads flextools.ini
4. GetRuleAssistantStartData()
   a. Query Source FLEx DB for categories/features
   b. Query Target FLEx DB for categories/features
   c. Build StartData object
5. StartData.write() → creates ruleAssistantGUIinput.xml
6. GetTestDataFile() (optional)
   a. Extract interlinear text from Source DB
   b. Write RuleAssistantSourceTestData.txt
   c. Run lt-proc to create RuleAssistantTargetTestData.txt
   d. Generate RuleAssistantDisplayData.html
7. StartRuleAssistant()
   a. Launch FLExTransRuleAssistant.exe
   b. Pass file paths as parameters
   c. Wait for GUI to exit
```

### Sequence 2: GUI Execution (External Program)

```
1. GUI reads ruleAssistantGUIinput.xml
   - Populates category dropdowns
   - Populates feature lists
   - Shows valid feature combinations
2. GUI reads RuleAssistantRules.xml (if exists)
   - Displays existing rules
3. GUI reads RuleAssistantDisplayData.html
   - Shows test data in UI
4. User creates/modifies rules
5. User clicks Save
   - GUI writes updated RuleAssistantRules.xml
6. User closes GUI
   - Returns exit code and optional rule number
```

### Sequence 3: Rule Generation

```
1. CreateRules() called
2. Read RuleAssistantRules.xml
3. Read existing transfer_rules.t1x (if exists)
   - Parse to extract existing rules/macros/categories
4. Create backup: transfer_rules.t1x.DATETIME.bak
5. RuleGenerator.ProcessExistingTransferFile()
   - Load existing categories, attributes, variables, macros
6. RuleGenerator.ProcessAssistantFile()
   - For each rule in RuleAssistantRules.xml:
     a. Query FLEx DBs for feature values
     b. Generate Apertium rule XML
     c. Create necessary macros/variables
7. RuleGenerator.WriteTransferFile()
   - Write complete transfer_rules.t1x
   - Includes old rules + new rules
```

---

## FLEx Database Access Patterns

### When FLEx DB is Queried

**First Query Pass (GetRuleAssistantStartData):**
```python
# For each database (Source and Target):
1. Utils.get_categories()
   - DB.lp.AllPartsOfSpeech → iterate all POS
   - Read category abbreviations

2. getFeatureData()
   - DB.ObjectsIn(IFsClosedFeatureRepository) → all features
   - For each: read name and values

3. Utils.getAllInflectableFeatures()
   - Query inflectable features per category

4. Utils.getAllStemFeatures()
   - Query stem-level features per category

5. Utils.getAffixTemplates()
   - For each POS, get affix templates
```

**Second Query Pass (CreateApertiumRules):**
```python
# During rule generation:
1. Utils.getCategoryHierarchy()
   - Build POS inheritance tree

2. Utils.getPossibleFeatureValues()
   - Get valid values for a feature

3. Utils.getLemmasForFeature()
   - Query target DB for lemmas with specific feature

4. Utils.getAffixGlossesForFeature()
   - Query both DBs for affix glosses
```

### Key Observation: NO CACHING

- Every run queries FLEx DB from scratch
- No persistent cache of FLEx data
- Changes to FLEx are always reflected (on next run)
- BUT: No detection of what changed

---

## Synchronization Analysis

### Current State: NO SYNCHRONIZATION

**What Happens:**
1. User runs Rule Assistant
2. FLEx data read → GUI input file created
3. User creates rules → RuleAssistantRules.xml written
4. Rules converted → transfer_rules.t1x written
5. **END** (no reverse flow)

**What Does NOT Happen:**
- No detection of external .t1x edits
- No warning when .t1x is about to be overwritten
- No merging of manual .t1x changes
- No change detection for FLEx DB
- No notification of stale data
- No validation that GUI input matches current FLEx state

### File Modification Scenarios

#### Scenario A: User Manually Edits .t1x
```
1. User opens transfer_rules.t1x in text editor
2. User adds custom rule or modifies macro
3. User saves .t1x
4. User runs Rule Assistant
5. User modifies a rule and saves
6. CreateApertiumRules runs
7. Manual edits are OVERWRITTEN (except if in backup)
```

**Result:** Manual changes LOST

#### Scenario B: FLEx Project Changes
```
1. User adds new category to FLEx
2. User runs Rule Assistant
3. New category appears in GUI dropdowns
4. User creates rule with new category
5. Rule successfully generated
```

**Result:** Works correctly (data read fresh)

#### Scenario C: Concurrent Edits
```
1. User creates rules in GUI
2. While GUI is open, another user edits .t1x
3. User saves in GUI
4. CreateApertiumRules overwrites .t1x
5. Other user's changes LOST
```

**Result:** Last write wins (no conflict detection)

#### Scenario D: Stale GUI Data
```
1. User launches Rule Assistant
2. FLEx data extracted → GUI launched
3. While GUI is open, user modifies FLEx in another window
4. User creates rules in GUI with old category list
5. Rules saved and generated
6. Rules may reference non-existent categories
```

**Result:** Potential inconsistency

---

## Change Detection: What's Missing

### File-Level Change Detection

**Not Implemented:**
- No timestamp checking on .t1x
- No hash/checksum validation
- No "dirty" flag tracking
- No modification date comparison

**Should Detect:**
- External .t1x modifications
- Config file changes
- FLEx DB schema changes

### Content-Level Change Detection

**Not Implemented:**
- No diff between old/new rules
- No detection of manual .t1x additions
- No identification of conflicting changes

**Should Track:**
- Which rules came from Rule Assistant
- Which rules/macros were manually added
- Dependencies between rules

---

## Critical Gaps and Issues

### Issue 1: Silent Data Loss
**Problem:** Manual .t1x edits are overwritten without warning
**Impact:** HIGH
**User Confusion:** "My custom rules disappeared!"

### Issue 2: Unclear Source of Truth
**Problem:** Users don't understand file relationships
**Impact:** MEDIUM
**User Confusion:** "Which file should I edit?"

### Issue 3: No Change Notification
**Problem:** FLEx changes don't trigger any alerts
**Impact:** LOW
**User Confusion:** "Why didn't my new category appear?"

### Issue 4: No Backup Management
**Problem:** Backups accumulate but no cleanup/restore UI
**Impact:** MEDIUM
**User Confusion:** "How do I restore my old rules?"

### Issue 5: No Concurrent Edit Protection
**Problem:** Multiple users can clobber each other's work
**Impact:** MEDIUM
**User Confusion:** "Where did my changes go?"

---

## Proposed Solution Architecture

### Design Goals

1. **Preserve Manual Edits** - Never silently overwrite user changes
2. **Clear Communication** - Users understand data sources
3. **Change Detection** - Notify users of external modifications
4. **Safe Defaults** - Prevent accidental data loss
5. **Backward Compatible** - Work with existing workflows

### Solution Components

#### Component 1: File Metadata Tracking

**Implementation:**
```xml
<!-- In RuleAssistantRules.xml -->
<RuleAssistantMetadata>
  <LastSync>2025-11-22T10:30:00Z</LastSync>
  <TransferFileHash>a3f5b9c2...</TransferFileHash>
  <FlexDBVersion>
    <Source>
      <ProjectName>Kalaba</ProjectName>
      <CategoryCount>15</CategoryCount>
      <FeatureCount>32</FeatureCount>
    </Source>
    <Target>
      <ProjectName>English</ProjectName>
      <CategoryCount>12</CategoryCount>
      <FeatureCount>28</FeatureCount>
    </Target>
  </FlexDBVersion>
</RuleAssistantMetadata>
```

**Purpose:**
- Track when .t1x was last generated
- Store hash of generated .t1x for change detection
- Record FLEx DB state (category/feature counts)

#### Component 2: Change Detection System

**On Rule Assistant Startup:**
```python
def detect_changes(config):
    changes = []

    # Check 1: Has .t1x been modified externally?
    t1x_path = get_transfer_rules_path(config)
    if os.path.exists(t1x_path):
        current_hash = compute_hash(t1x_path)
        stored_hash = get_metadata('TransferFileHash')
        if current_hash != stored_hash:
            changes.append({
                'type': 'EXTERNAL_T1X_EDIT',
                'file': t1x_path,
                'action': 'WARN_BEFORE_OVERWRITE'
            })

    # Check 2: Has FLEx DB changed?
    current_stats = get_flex_stats(source_db, target_db)
    stored_stats = get_metadata('FlexDBVersion')
    if current_stats != stored_stats:
        changes.append({
            'type': 'FLEX_DB_CHANGED',
            'details': diff_stats(current_stats, stored_stats),
            'action': 'NOTIFY_USER'
        })

    return changes
```

**User Notification:**
```
┌────────────────────────────────────────────────────┐
│  ⚠ External Changes Detected                       │
├────────────────────────────────────────────────────┤
│                                                    │
│  The transfer rules file has been modified        │
│  outside of Rule Assistant:                       │
│                                                    │
│    transfer_rules.t1x                             │
│    Last modified: 2025-11-22 09:45                │
│                                                    │
│  If you save rules, your manual edits will be     │
│  overwritten.                                      │
│                                                    │
│  Options:                                          │
│  ○ Create backup and continue                     │
│  ○ Cancel and review changes first                │
│  ○ Show me what changed (diff view)               │
│                                                    │
└────────────────────────────────────────────────────┘
```

#### Component 3: Rule Provenance Tracking

**Mark Generated Rules:**
```xml
<!-- In transfer_rules.t1x -->
<rule comment="my-rule-name">
  <!-- GENERATED BY RULE ASSISTANT: 2025-11-22T10:30:00Z -->
  <!-- SOURCE: RuleAssistantRules.xml, rule index 5 -->
  <!-- DO NOT EDIT: Changes will be overwritten -->
  <pattern>...</pattern>
  <action>...</action>
</rule>

<!-- Manual rules (no special comments) -->
<rule comment="custom-hand-coded-rule">
  <pattern>...</pattern>
  <action>...</action>
</rule>
```

**Detection Logic:**
```python
def categorize_rules(t1x_tree):
    generated_rules = []
    manual_rules = []

    for rule in t1x_tree.findall('.//rule'):
        comments = get_preceding_comments(rule)
        if 'GENERATED BY RULE ASSISTANT' in comments:
            generated_rules.append(rule)
        else:
            manual_rules.append(rule)

    return generated_rules, manual_rules
```

**Merge Strategy:**
```python
def merge_rules(old_t1x, new_rules_from_ra):
    old_generated, old_manual = categorize_rules(old_t1x)

    # Remove old generated rules
    # Keep all manual rules
    # Add new generated rules

    merged = create_new_t1x()
    merged.add_rules(old_manual)  # Preserve manual work
    merged.add_rules(new_rules_from_ra)  # Add RA rules

    return merged
```

#### Component 4: Interactive Conflict Resolution

**When Conflicts Detected:**
```
┌────────────────────────────────────────────────────┐
│  🔀 Rule Conflicts Detected                        │
├────────────────────────────────────────────────────┤
│                                                    │
│  The following rules exist in both locations:     │
│                                                    │
│  1. "determiner-noun-agreement" (modified)        │
│     ▸ In transfer_rules.t1x                       │
│     ▸ In RuleAssistantRules.xml                   │
│                                                    │
│  2. "verb-tense-mapping" (different versions)     │
│     ▸ Manual edit in .t1x                         │
│     ▸ Rule Assistant version                      │
│                                                    │
│  Choose resolution:                                │
│  ○ Keep manual .t1x versions                      │
│  ○ Use Rule Assistant versions                    │
│  ○ Review each conflict individually              │
│                                                    │
└────────────────────────────────────────────────────┘
```

#### Component 5: Sync Status Dashboard

**Add to Rule Assistant GUI:**
```
┌────────────────────────────────────────────────────┐
│  📊 Data Sources                                   │
├────────────────────────────────────────────────────┤
│                                                    │
│  Source FLEx Project: Kalaba                       │
│    Last synced: 2025-11-22 10:30                  │
│    Categories: 15  Features: 32                    │
│    ✓ Up to date                                   │
│                                                    │
│  Target FLEx Project: English                      │
│    Last synced: 2025-11-22 10:30                  │
│    Categories: 12  Features: 28                    │
│    ⚠ 1 new category detected (refresh?)           │
│                                                    │
│  Transfer Rules: transfer_rules.t1x                │
│    Last modified: 2025-11-22 10:30                │
│    Generated rules: 45                             │
│    Manual rules: 3                                 │
│    ✓ Synchronized                                  │
│                                                    │
│  [ Refresh FLEx Data ]  [ View File Locations ]   │
│                                                    │
└────────────────────────────────────────────────────┘
```

#### Component 6: Explicit Sync Operations

**New User Actions:**
```python
# Sync button in GUI
def sync_with_flex():
    """Refresh FLEx data without creating rules"""
    startData = GetRuleAssistantStartData(...)
    startData.write(gui_input_file)
    update_metadata({
        'FlexLastSync': datetime.now(),
        'FlexDBVersion': get_flex_stats(...)
    })
    show_notification("FLEx data refreshed")

# Export to .t1x
def export_to_t1x():
    """Generate .t1x from current rules"""
    changes = detect_changes(config)
    if changes:
        show_conflict_dialog(changes)
        if user_cancels:
            return

    create_backup()
    CreateApertiumRules.CreateRules(...)
    update_metadata({
        'TransferFileHash': compute_hash(t1x_path),
        'LastExport': datetime.now()
    })

# Import from .t1x
def import_from_t1x():
    """Parse .t1x and create RA rules (lossy conversion)"""
    warn_user("This is experimental and may lose information")
    # Attempt to parse .t1x rules back to RA format
    # Only works for rules originally from RA
```

---

## Migration Strategy

### Phase 1: Add Metadata (Non-Breaking)

**Changes:**
- Add metadata section to RuleAssistantRules.xml
- Store hashes and timestamps
- No UI changes yet
- No behavior changes

**Compatibility:** 100% backward compatible

### Phase 2: Add Change Detection (Warning Only)

**Changes:**
- Implement change detection
- Show warnings when conflicts detected
- Allow user to proceed anyway
- Log to console/log file

**Compatibility:** Backward compatible with warnings

### Phase 3: Add Provenance Tracking

**Changes:**
- Add comments to generated .t1x rules
- Implement smart merge (preserve manual rules)
- Add sync status to GUI
- Optional conflict resolution

**Compatibility:** Can work with old .t1x files

### Phase 4: Full Sync UI

**Changes:**
- Add refresh buttons
- Add conflict resolution dialogs
- Add import/export operations
- Add file location viewer

**Compatibility:** Full feature set

---

## Backward Compatibility Concerns

### Existing Files

**Old RuleAssistantRules.xml (no metadata):**
- Solution: Initialize metadata on first load
- Assume all files clean (no conflicts)
- Generate initial hashes

**Old transfer_rules.t1x (no provenance comments):**
- Solution: Assume all rules are manual
- On first regeneration, mark new rules
- Never delete unmarked rules

**Old Workflows:**
- Solution: Default to "warn but allow" mode
- Add config option: `StrictSyncMode=false`
- Gradually migrate users

### Configuration

**New Config Options:**
```ini
[RuleAssistant]
# Behavior when external .t1x edits detected
ConflictResolution=WARN  # WARN | ABORT | AUTO_BACKUP

# Track FLEx changes
DetectFlexChanges=true

# Preserve manual rules
PreserveManualRules=true

# Backup strategy
AutoBackupBeforeOverwrite=true
MaxBackupCount=10
```

---

## Testing Scenarios

### Test 1: Fresh Install (No Files Exist)
```
Expected: Create all files from scratch
Verify: Metadata initialized correctly
```

### Test 2: Existing Files (Pre-Metadata)
```
Setup: Old RuleAssistantRules.xml + .t1x exist
Expected: Initialize metadata, warn about uncertainty
Verify: No data loss
```

### Test 3: Manual .t1x Edit
```
Setup: Generate rules, manually edit .t1x, run RA again
Expected: Warning shown, backup created
Verify: User can choose to preserve edits
```

### Test 4: FLEx Changes While GUI Open
```
Setup: Launch RA, modify FLEx, save in RA
Expected: Warning about stale data
Verify: Option to refresh or continue
```

### Test 5: Concurrent Users
```
Setup: Two users edit same project
Expected: Last writer gets conflict warning
Verify: Merge options available
```

---

## Performance Considerations

### Current Performance
- FLEx DB queries: ~2-5 seconds (depending on project size)
- File I/O: negligible (<100ms)
- GUI launch: ~1-2 seconds

### With Change Detection
- Hash computation: ~50-200ms (for typical .t1x)
- Metadata parsing: ~10ms
- Total overhead: <300ms (acceptable)

### Optimization Strategies
- Cache FLEx stats in metadata (avoid full scan)
- Use incremental hashing for large files
- Lazy load conflict resolution (only when needed)

---

## User Documentation Needs

### FAQ Updates

**Q: What file does Rule Assistant read from?**

A: Rule Assistant reads from THREE sources:
1. **FLEx Database** (Source & Target) - grammatical information
2. **RuleAssistantRules.xml** - your saved rules
3. **transfer_rules.t1x** - existing Apertium rules (for merging)

**Q: Will my manual .t1x edits be preserved?**

A: Yes, IF you enable "Preserve Manual Rules" mode. The system will:
- Detect manual edits
- Warn you before overwriting
- Preserve unmarked rules during merge

**Q: How do I know if my FLEx changes are reflected?**

A: Check the "Sync Status" panel in Rule Assistant. If FLEx changes are detected, you'll see a warning and can refresh the data.

**Q: When should I edit .t1x directly vs. using Rule Assistant?**

A:
- **Use Rule Assistant for:** Standard grammatical mappings, agreement rules
- **Edit .t1x directly for:** Complex macros, special cases, optimizations
- **Mark manual sections with comments** so they won't be overwritten

### Tutorial: Working with Multiple Files

```markdown
## Understanding File Relationships

1. **FLEx Database** → Contains your linguistic data
   - This is the master source for grammar
   - Changes here require re-sync in Rule Assistant

2. **RuleAssistantRules.xml** → Your rule definitions
   - High-level, human-readable format
   - Source of truth for rules created in GUI

3. **transfer_rules.t1x** → Executable transfer rules
   - Low-level Apertium format
   - Generated from RuleAssistantRules.xml
   - Can contain manual additions

## Workflow Best Practices

### Creating Rules
1. Launch Rule Assistant
2. Create rules in GUI
3. Save (creates/updates RuleAssistantRules.xml)
4. Rules automatically exported to transfer_rules.t1x

### Editing Rules
**Option A: Via GUI**
1. Launch Rule Assistant
2. Modify existing rules
3. Save and export

**Option B: Manual .t1x Edit**
1. Open transfer_rules.t1x in editor
2. Make changes
3. Add comment: <!-- MANUAL EDIT: reason -->
4. Next time you use Rule Assistant, approve merge

### After FLEx Changes
1. Launch Rule Assistant
2. Click "Refresh FLEx Data" if prompted
3. Create new rules using updated grammar
```

---

## Implementation Checklist

### Phase 1: Core Infrastructure
- [ ] Add metadata schema to RuleAssistantRules.xml
- [ ] Implement file hash computation
- [ ] Add FLEx stats gathering
- [ ] Create metadata read/write functions
- [ ] Add unit tests for metadata handling

### Phase 2: Change Detection
- [ ] Implement .t1x change detection
- [ ] Implement FLEx change detection
- [ ] Create warning dialog UI
- [ ] Add logging for detected changes
- [ ] Test detection accuracy

### Phase 3: Provenance System
- [ ] Add comment generation to CreateApertiumRules
- [ ] Implement rule categorization (generated vs. manual)
- [ ] Create merge algorithm
- [ ] Add backup creation before merge
- [ ] Test preservation of manual rules

### Phase 4: User Interface
- [ ] Design sync status panel
- [ ] Add refresh buttons
- [ ] Create conflict resolution dialog
- [ ] Add file location viewer
- [ ] Implement diff viewer (optional)

### Phase 5: Configuration
- [ ] Add config options to ReadConfig
- [ ] Create default config values
- [ ] Add config UI (Settings dialog)
- [ ] Document config options

### Phase 6: Documentation
- [ ] Update user manual
- [ ] Create tutorial videos
- [ ] Write FAQ entries
- [ ] Add tooltips to new UI elements

### Phase 7: Testing
- [ ] Unit tests for all new functions
- [ ] Integration tests for workflows
- [ ] User acceptance testing
- [ ] Performance benchmarking

---

## Risk Assessment

### High Risk
- **Data Loss:** If merge algorithm has bugs
  - Mitigation: Always create backups, extensive testing

- **Performance:** If change detection is slow
  - Mitigation: Optimize hashing, cache metadata

### Medium Risk
- **User Confusion:** If too many dialogs/warnings
  - Mitigation: Progressive disclosure, sensible defaults

- **Backward Compatibility:** If old files don't work
  - Mitigation: Graceful fallback, migration path

### Low Risk
- **GUI Complexity:** If UI becomes cluttered
  - Mitigation: Collapse advanced features, clean design

---

## Conclusion

The current Rule Assistant implementation has a **clear and deterministic data flow**, but suffers from **poor user communication** and **lack of safeguards against data loss**.

### Current State Summary

✅ **Works Well:**
- FLEx data is always fresh (no stale cache)
- Simple, linear workflow
- Reliable file generation

❌ **Needs Improvement:**
- Silent overwriting of manual edits
- No change detection
- Unclear file relationships
- No concurrent edit protection
- Lack of user feedback on sync status

### Recommended Next Steps

1. **Immediate (Low Effort, High Impact):**
   - Add warning when .t1x has been modified
   - Document file relationships in user manual
   - Add comments to generated rules

2. **Short Term (Medium Effort, High Impact):**
   - Implement metadata tracking
   - Add sync status panel to GUI
   - Preserve manual rules during merge

3. **Long Term (High Effort, Medium Impact):**
   - Full conflict resolution UI
   - Import from .t1x capability
   - Advanced backup management

### Success Criteria

The solution should:
- ✓ Never silently lose user data
- ✓ Clearly communicate what file is being read/written
- ✓ Detect and warn about external changes
- ✓ Preserve manual edits by default
- ✓ Remain backward compatible with existing projects
- ✓ Add minimal performance overhead (<500ms)

---

## Appendix A: Code References

### Key Functions

**RuleAssistant.py:**
- `MainFunction()` - Entry point (line 467)
- `GetRuleAssistantStartData()` - FLEx extraction (line 254)
- `GetTestDataFile()` - Test data generation (line 419)
- `StartRuleAssistant()` - GUI launcher (line 431)

**CreateApertiumRules.py:**
- `CreateRules()` - Main conversion function (line 1550)
- `RuleGenerator.ProcessExistingTransferFile()` - Load old .t1x (line 274)
- `RuleGenerator.ProcessAssistantFile()` - Generate rules (line 1436)
- `RuleGenerator.WriteTransferFile()` - Write .t1x (line 1533)

### File Constants

**Utils.py:**
- `RA_GUI_INPUT_FILE = 'ruleAssistantGUIinput.xml'` (line 333)
- `RULE_ASSISTANT_SOURCE_TEST_DATA_FILE` (line 334)
- `RULE_ASSISTANT_TARGET_TEST_DATA_FILE` (line 335)
- `RULE_ASSISTANT_DISPLAY_DATA_FILE` (line 336)

**ReadConfig.py:**
- `RULE_ASSISTANT_FILE = 'RuleAssistantRulesFile'` (line 167)
- `TRANSFER_RULES_FILE = 'TransferRulesFile'` (line 189)
- `SOURCE_TEXT_NAME = 'SourceTextName'` (line 165)

**FTPaths.py:**
- `BUILD_DIR` - Where temporary files live (line 43)
- `RULE_ASSISTANT_DIR` - GUI program location (line 59)
- `RULE_ASSISTANT` - GUI executable name (line 60)

---

## Appendix B: File Format Examples

### RuleAssistantRules.xml (Current Format)
```xml
<?xml version="1.0" encoding="utf-8"?>
<FLExTransRules>
  <FLExTransRule name="det-noun-agreement">
    <Description>Agreement between determiner and noun</Description>
    <Source>
      <Word id="1" category="det" head="no">
        <Features>
          <Feature label="gender" match="1"/>
        </Features>
      </Word>
      <Word id="2" category="n" head="yes">
        <Features>
          <Feature label="gender" match="1"/>
        </Features>
      </Word>
    </Source>
    <Target>
      <Word id="1" category="det">
        <Features>
          <Feature label="gender" match="1"/>
        </Features>
      </Word>
      <Word id="2" category="n" head="yes">
        <Features>
          <Feature label="gender" match="1"/>
        </Features>
      </Word>
    </Target>
  </FLExTransRule>
</FLExTransRules>
```

### RuleAssistantRules.xml (Proposed with Metadata)
```xml
<?xml version="1.0" encoding="utf-8"?>
<FLExTransRules>
  <Metadata>
    <Created>2025-11-22T10:00:00Z</Created>
    <LastModified>2025-11-22T10:30:00Z</LastModified>
    <LastSync>2025-11-22T10:30:00Z</LastSync>
    <TransferFileHash>a3f5b9c2d8e1f4a7b0c3d6e9f2a5b8c1</TransferFileHash>
    <FlexDBVersion>
      <Source name="Kalaba" categories="15" features="32"/>
      <Target name="English" categories="12" features="28"/>
    </FlexDBVersion>
  </Metadata>
  <FLExTransRule name="det-noun-agreement">
    <!-- rule content unchanged -->
  </FLExTransRule>
</FLExTransRules>
```

### transfer_rules.t1x (Generated, with Provenance)
```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE transfer PUBLIC "-//XMLmind//DTD transfer//EN" "transfer.dtd">
<transfer>
  <section-def-cats>
    <def-cat n="c_det">
      <cat-item tags="det"/>
      <cat-item tags="det.*"/>
    </def-cat>
    <!-- ... -->
  </section-def-cats>

  <section-rules>
    <!-- GENERATED BY RULE ASSISTANT: 2025-11-22T10:30:00Z -->
    <!-- SOURCE: RuleAssistantRules.xml, rule "det-noun-agreement" -->
    <!-- DO NOT EDIT: Changes will be overwritten on next Rule Assistant save -->
    <rule comment="det-noun-agreement">
      <pattern>
        <pattern-item n="c_det"/>
        <pattern-item n="c_n"/>
      </pattern>
      <action>
        <!-- ... -->
      </action>
    </rule>

    <!-- Manual rule (no special comments) -->
    <rule comment="custom-idiomatic-expression">
      <pattern>
        <!-- ... -->
      </pattern>
    </rule>
  </section-rules>
</transfer>
```

---

## Appendix C: Detailed Function Call Tree

```
MainFunction(DB, report, modify, fromLRT)
│
├─ ReadConfig.readConfig(report)
│  └─ Returns: configMap
│
├─ Utils.openTargetProject(configMap, report)
│  └─ Returns: TargetDB
│
├─ GetRuleAssistantStartData(report, DB, TargetDB, configMap)
│  │
│  ├─ GetStartData(report, DB, configMap)  [for Source]
│  │  ├─ Utils.get_categories(DB, report, posMap, TargetDB=None, ...)
│  │  │  └─ Queries: DB.lp.AllPartsOfSpeech
│  │  │
│  │  ├─ getFeatureData(DB)
│  │  │  └─ Queries: DB.ObjectsIn(IFsClosedFeatureRepository)
│  │  │     └─ For each: Utils.as_string(feature.Name)
│  │  │     └─ For each: Utils.as_tag(val) for val in feature.ValuesOC
│  │  │
│  │  ├─ Utils.getAllInflectableFeatures(DB)
│  │  │
│  │  ├─ Utils.getAllStemFeatures(DB, report, configMap)
│  │  │
│  │  └─ Utils.getAffixTemplates(DB, flexCat)
│  │     └─ For each POS
│  │
│  ├─ GetStartData(report, TargetDB, configMap)  [for Target]
│  │  └─ (same as above)
│  │
│  └─ Returns: StartData(srcData, tgtData)
│
├─ StartData.write(ruleAssistGUIinputfile)
│  ├─ Creates: Build/ruleAssistantGUIinput.xml
│  └─ Contains: <FLExData><SourceData>...</SourceData><TargetData>...</TargetData></FLExData>
│
├─ GetTestDataFile(report, DB, configMap)
│  │
│  ├─ ReadConfig.getConfigVal(configMap, SOURCE_TEXT_NAME, report)
│  │
│  ├─ GenerateTestDataFile(report, DB, configMap, fhtml)
│  │  │
│  │  ├─ Queries: DB.ObjectsIn(ITextRepository)
│  │  │  └─ Find text matching sourceText name
│  │  │
│  │  ├─ InterlinData.initInterlinParams(configMap, report, content)
│  │  │
│  │  ├─ InterlinData.getInterlinData(DB, report, params)
│  │  │  └─ Returns: text object
│  │  │
│  │  ├─ Write: Build/RuleAssistantSourceTestData.txt
│  │  │  └─ text.write(fout)
│  │  │
│  │  ├─ subprocess.run(['lt-proc.exe', '-b', bidix, fsrc, ftgt])
│  │  │  └─ Creates: Build/RuleAssistantTargetTestData.txt
│  │  │
│  │  └─ Write: Build/RuleAssistantDisplayData.html
│  │     ├─ Read: RuleAssistantTargetTestData.txt
│  │     ├─ ProcessLine(line) for each line
│  │     └─ ReadingToHTML(reading) to format
│  │
│  └─ Returns: path to HTML file
│
├─ StartRuleAssistant(report, ruleAssistantFile, ruleAssistGUIinputfile, testDataFile, fromLRT)
│  │
│  ├─ subprocess.run([FLExTransRuleAssistant.exe, ...])
│  │  └─ GUI reads:
│  │     ├─ ruleAssistantFile (RuleAssistantRules.xml)
│  │     ├─ ruleAssistGUIinputfile (FLEx data)
│  │     └─ testDataFile (HTML display)
│  │
│  ├─ GUI writes:
│  │  └─ ruleAssistantFile (updated rules)
│  │
│  └─ Returns: (saved: bool, ruleNumber: int|None, lrt: bool)
│
└─ If saved:
   │
   └─ CreateApertiumRules.CreateRules(DB, TargetDB, report, configMap, ruleAssistantFile, transferRulePath, ruleNumber)
      │
      ├─ Read: ruleAssistantFile (RuleAssistantRules.xml)
      │  └─ ET.parse(rulesAssistant)
      │
      ├─ Create: RuleGenerator(sourceDB, targetDB, report, configMap)
      │  ├─ Utils.getCategoryHierarchy(sourceDB)
      │  └─ Utils.getCategoryHierarchy(targetDB)
      │
      ├─ If transferRulePath exists:
      │  ├─ Create backup: transfer_rules.t1x.DATETIME.bak
      │  │  └─ shutil.copy(transferRulePath, backupPath)
      │  │
      │  └─ RuleGenerator.ProcessExistingTransferFile(transferRulePath)
      │     ├─ ET.parse(fileName)
      │     ├─ Extract all def-cat, def-attr, def-var, def-list, def-macro
      │     └─ Store in generator's internal state
      │
      ├─ RuleGenerator.ProcessAssistantFile(ruleAssistantFile, ruleNumber)
      │  │
      │  ├─ For each <FLExTransRule>:
      │  │  │
      │  │  └─ ProcessRule(rule, skip)
      │  │     │
      │  │     ├─ For each source word:
      │  │     │  └─ GetCategoryName(cat, features, affixes)
      │  │     │     └─ Creates <def-cat> if needed
      │  │     │
      │  │     ├─ For each target word:
      │  │     │  │
      │  │     │  ├─ If needs lemma macro:
      │  │     │  │  ├─ GetMultiFeatureMacro(cat, True, lemmaTags)
      │  │     │  │  │  ├─ Queries: Utils.getLemmasForFeature(targetDB, ...)
      │  │     │  │  │  └─ Creates <def-macro> with conditional logic
      │  │     │  │  │
      │  │     │  │  └─ Creates <call-macro> in rule
      │  │     │  │
      │  │     │  ├─ For each affix:
      │  │     │  │  │
      │  │     │  │  ├─ If single feature:
      │  │     │  │  │  ├─ GetAttributeMacro(srcSpec, trgSpec)
      │  │     │  │  │  │  ├─ GetTags(spec, source=True)
      │  │     │  │  │  │  │  ├─ Utils.getAffixGlossesForFeature(sourceDB, ...)
      │  │     │  │  │  │  │  └─ Utils.getPossibleFeatureValues(sourceDB, ...)
      │  │     │  │  │  │  │
      │  │     │  │  │  │  ├─ GetTags(spec, source=False)
      │  │     │  │  │  │  │  └─ Utils.getAffixGlossesForFeature(targetDB, ...)
      │  │     │  │  │  │  │
      │  │     │  │  │  │  └─ CreateAttributeMacro(...)
      │  │     │  │  │  │
      │  │     │  │  │  └─ OR just <clip> if tags match
      │  │     │  │  │
      │  │     │  │  └─ If multiple features:
      │  │     │  │     └─ GetMultiFeatureMacro(cat, False, specList)
      │  │     │  │        └─ Creates complex conditional macro
      │  │     │  │
      │  │     │  └─ Creates <out><lu>...</lu></out> in rule
      │  │     │
      │  │     └─ Returns: True (rule created)
      │  │
      │  └─ Returns: ruleCount
      │
      └─ RuleGenerator.WriteTransferFile(transferRulePath)
         ├─ Remove empty sections
         ├─ Write XML declaration
         ├─ Write DOCTYPE
         ├─ ET.indent(root)
         └─ Write: transfer_rules.t1x
```

---

**End of Analysis Document**

Generated: 2025-11-22
Version: 1.0
Status: DRAFT for Review
