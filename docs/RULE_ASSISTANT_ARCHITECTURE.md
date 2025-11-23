# Rule Assistant Technical Architecture

**Version:** 1.0
**Date:** 2025-11-22
**Status:** Comprehensive Technical Design
**Authors:** FLExTrans Development Team

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current Architecture (As-Is)](#current-architecture-as-is)
3. [Problem Areas Identified](#problem-areas-identified)
4. [Proposed Architecture (To-Be)](#proposed-architecture-to-be)
5. [Migration Strategy](#migration-strategy)
6. [Data Flow Diagrams](#data-flow-diagrams)
7. [Component Responsibilities](#component-responsibilities)
8. [File Format Specifications](#file-format-specifications)
9. [Integration Points](#integration-points)
10. [Performance Considerations](#performance-considerations)

---

## Executive Summary

The Rule Assistant is a core component of FLExTrans that enables linguists to create Apertium transfer rules through a graphical interface. This document describes the current architecture, identifies critical problems discovered through user feedback and code analysis, and proposes a comprehensive redesign to address technical debt, improve usability, and expand linguistic coverage.

### Key Architectural Challenges

1. **Data Synchronization Issues**: Unclear source of truth between FLEx database, Rule Assistant XML, and transfer rule files
2. **File State Management**: Missing sections (variables/macros) after rule generation
3. **Limited Morphological Support**: Only prefix/suffix affixes currently supported
4. **Macro Reuse Disabled**: Code duplication due to disabled multi-source macro reuse (Issue #661)
5. **Technical Debt**: Multiple TODO items indicating incomplete implementation

### Strategic Direction

The proposed architecture maintains backward compatibility while:
- Establishing clear data flow and synchronization protocols
- Expanding affix support to include infixes and circumfixes
- Re-enabling macro reuse with robust deduplication
- Improving error handling and user feedback
- Preparing for future linguistic features (reduplication, templatic morphology, phonological rules)

---

## Current Architecture (As-Is)

### System Overview

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   FLEx DB   │────────▶│     Rule     │────────▶│  Apertium   │
│  (Source &  │         │  Assistant   │         │  Transfer   │
│   Target)   │         │   Generator  │         │    Rules    │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │                        │
      │                        ▼                        │
      │                 ┌──────────────┐               │
      │                 │ Rule Asst.   │               │
      │                 │ XML (Cache?) │               │
      │                 └──────────────┘               │
      │                                                 │
      └────────────────────────────────────────────────┘
                   (Synchronization unclear)
```

### Core Components

#### 1. RuleAssistant.py (GUI Module)
**Location:** `/home/user/FLExTrans/Dev/Modules/RuleAssistant.py`

**Responsibilities:**
- Provides graphical interface for rule creation
- Integrates with XMLmind for XML editing
- Invokes CreateApertiumRules.py for rule generation
- Manages Rule Assistant XML files

**Current Limitations:**
- Data synchronization logic unclear
- No "Reload FLEx Data" functionality
- Limited feedback on what data sources are being used

#### 2. CreateApertiumRules.py (Rule Generation Engine)
**Location:** `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py`

**Responsibilities:**
- Parses Rule Assistant XML
- Queries FLEx databases for morphological data
- Generates Apertium transfer rule XML
- Manages categories, attributes, macros, and rules

**Current Structure:**
```python
class RuleGenerator:
    def __init__(self, report, sourceDB, targetDB, ruleName)
    def ProcessAssistantFile(ruleAssistantFile, transferRulePath, ...)
    def ProcessExistingTransferFile(fileName)
    def WriteTransferFile(fileName)

    # Rule processing
    def ProcessRule(ruleElement, ruleName, overwrite)

    # Category and attribute management
    def GetCategoryName(cat, features, affixes)
    def AddCategory(name, tags)
    def AddSingleAttribute(name, tags, comment)

    # Macro generation
    def GetMultiFeatureMacro(destCategory, isLemma, sources)
    def GetAttributeMacro(...)

    # Helper methods
    def GetSection(name)
    def GetAvailableID(base, usedIDs)
```

**Known Issues:**
- Line 233: Affix tag generation incomplete (TODO)
- Lines 808-809: Variable naming confusion (lemmas vs. affixes)
- Line 1252: Proper noun capitalization not checked (TODO)
- Line 1552: File mode validation unclear (TODO)
- Lines 314-326: Multi-source macro reuse disabled (Issue #661)

#### 3. Utils.py (FLEx Database Interface)
**Location:** `/home/user/FLExTrans/Dev/Lib/Utils.py`

**Responsibilities:**
- Query FLEx database for categories, features, affixes
- Extract morphological data (affixes, allomorphs, stems)
- Provide linguistic metadata

**Key Functions:**
```python
getAffixGlossesForFeature(db, cat, label, isAffix, splitGloss=None)
getCategoryHierarchy(db, cat)
getStemName(db, headword, cat, features)
```

**Current Support:**
- Prefix affixes (GUID: d7f713dd-...)
- Suffix affixes (GUID: d7f713e2-...)
- Infix affixes (GUID: d7f713e0-...) - **recognized but not used**
- Circumfix affixes (GUID: d7f713df-...) - **recognized but not used**

#### 4. DTD Schema
**Location:** `/home/user/FLExTrans/Rule Assistant/FLExTransRuleGenerator.dtd`

**Current Schema:**
```xml
<!ELEMENT FLExTransRuleGenerator (FLExTransRules*) >

<!ELEMENT FLExTransRules (Rule*) >
<!ATTLIST FLExTransRules
  overwrite_rules (yes | no) "no"
>

<!ELEMENT Rule (Source, Target) >
<!ATTLIST Rule
  name CDATA #REQUIRED
>

<!ELEMENT Source (MatchGroup, (Word | WordGap)*) >
<!ELEMENT Target (Word | WordGap)* >

<!ELEMENT Word (Stem?, Affixes?, Features?) >
<!ATTLIST Word
  id CDATA #IMPLIED
  category CDATA #REQUIRED
  head (yes | no) "no"
  create_permutations (yes | no) "no"
>

<!ELEMENT Affix (Features*) >
<!ATTLIST Affix
  type (prefix | suffix) "suffix"  ⚠️ LIMITATION: No infix/circumfix
>

<!ELEMENT Feature EMPTY >
<!ATTLIST Feature
  label CDATA #REQUIRED
  match CDATA #IMPLIED
  value CDATA #IMPLIED
  unmarked_default CDATA #IMPLIED
  ranking CDATA #IMPLIED
>
```

**Limitations:**
- Affix type only allows `prefix | suffix`
- No position specification for infixes
- No split specification for circumfixes

### Data Flow (Current - Best Understanding)

#### Rule Creation Flow

```
1. User opens Rule Assistant
   ↓
2. GUI loaded (RuleAssistant.py)
   ↓
3. ❓ Data source unclear:
   - Does it read existing .t1x file?
   - Does it read cached XML?
   - Does it query FLEx fresh?
   ↓
4. User creates/edits rules in XML interface
   ↓
5. User saves
   ↓
6. CreateApertiumRules.ProcessAssistantFile() called
   ↓
7. Reads Rule Assistant XML
   ↓
8. IF existing transfer file exists:
      ProcessExistingTransferFile() loads it
      ⚠️ PROBLEM: May discard sections marked as empty
   ↓
9. For each rule:
      - Query FLEx for morphological data
      - Generate categories, attributes, macros
      - Create pattern and action elements
   ↓
10. WriteTransferFile() outputs .t1x
    ⚠️ PROBLEM: May not preserve all existing sections
```

#### File Synchronization Issues

**Problem:** Multiple potential sources of truth

```
FLEx Database ──────┐
                    │
Rule Asst. XML ─────┼──▶ ❓ Which is authoritative?
                    │
Transfer .t1x ──────┘

Manual .t1x edits ──▶ ❓ Preserved or lost?
```

**User Confusion Points:**
1. "When I start up the RA again, where is it getting its info from?"
2. "If you have already created rules with the RA, and then you have edited the file, and then you want to open it up with the RA, does it keep the edits you made?"
3. "When I started up the RA, I was kind of afraid it might be blank."
4. "There were things that changed in my FLEx project that it should have been aware of."

### File Formats

#### Rule Assistant XML Format

**Purpose:** Stores user's rule specifications in linguist-friendly format

**Location:** User-specified, typically `RuleAssistant.xml` or similar

**Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE FLExTransRuleGenerator SYSTEM "FLExTransRuleGenerator.dtd">
<FLExTransRuleGenerator>
  <FLExTransRules overwrite_rules="no">
    <Rule name="DET-NOUN">
      <Source>
        <MatchGroup>
          <MatchElement label="gender" match="α"/>
          <MatchElement label="number" match="β"/>
        </MatchGroup>
        <Word id="1" category="det" head="no">
          <Features>
            <Feature label="gender" match="α"/>
            <Feature label="number" match="β"/>
          </Features>
        </Word>
        <Word id="2" category="n" head="yes">
          <Features>
            <Feature label="gender" match="α"/>
            <Feature label="number" match="β"/>
          </Features>
        </Word>
      </Source>
      <Target>
        <Word id="2" category="n">
          <Features>
            <Feature label="gender" match="α"/>
            <Feature label="number" match="β"/>
          </Features>
        </Word>
        <Word id="1" category="det">
          <Features>
            <Feature label="gender" match="α"/>
            <Feature label="number" match="β"/>
          </Features>
        </Word>
      </Target>
    </Rule>
  </FLExTransRules>
</FLExTransRuleGenerator>
```

#### Transfer Rule .t1x Format (Apertium)

**Purpose:** Executable transfer rules for Apertium MT system

**Location:** Typically `transfer_rules.t1x` in project directory

**Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<transfer default="chunk">

  <section-def-cats>
    <!-- Part-of-speech categories -->
    <def-cat n="det">
      <cat-item tags="det.*"/>
    </def-cat>
  </section-def-cats>

  <section-def-attrs>
    <!-- Grammatical attributes -->
    <def-attr n="gender">
      <attr-item tags="m"/>
      <attr-item tags="f"/>
    </def-attr>
  </section-def-attrs>

  <section-def-vars>
    <!-- Variables (may be lost - Issue FR-001) -->
    <def-var n="temp"/>
  </section-def-vars>

  <section-def-macros>
    <!-- Reusable macros (may be lost - Issue FR-001, disabled - Issue #661) -->
  </section-def-macros>

  <section-rules>
    <!-- Actual transfer rules -->
    <rule comment="DET-NOUN">
      <pattern>
        <pattern-item n="det"/>
        <pattern-item n="n"/>
      </pattern>
      <action>
        <!-- Transfer logic here -->
      </action>
    </rule>
  </section-rules>

</transfer>
```

---

## Problem Areas Identified

### Critical Issues (Data Loss/Corruption Risk)

#### FR-001: Missing Sections After Rule Generation

**Severity:** Critical
**Impact:** Data loss
**Source:** User bug report + code analysis

**Problem:**
After running Rule Assistant, the generated transfer rule file is missing `<section-def-vars>` and `<section-def-macros>` sections, even though the starting template file contained these sections.

**Root Cause Analysis:**

**Location:** `CreateApertiumRules.py`, lines 1542-1600

```python
def WriteTransferFile(self, fileName: str):
    """Write the transfer rule file."""

    # Line 1542: Discard empty sections
    # ⚠️ PROBLEM: This may delete sections that should be preserved
    for section in self.root.findall('.//*[@n]'):
        if len(section) == 0 and section.tag != 'section-rules':
            self.root.remove(section)
```

**Issue:** The code removes any section that is empty (`len(section) == 0`), without distinguishing between:
- Sections that are genuinely unused and can be deleted
- Sections that are empty now but should be preserved for manual edits
- Sections that exist in the template and should remain

**Specific Scenarios:**

1. **User starts with `transfer_rules_start.t1x`** containing:
   ```xml
   <section-def-vars>
     <def-var n="myVar"/>
   </section-def-vars>
   <section-def-macros>
     <def-macro n="myMacro">...</def-macro>
   </section-def-macros>
   ```

2. **Rule Assistant generates rules** that don't use these sections

3. **WriteTransferFile()** sees empty sections (from RA's perspective) and deletes them

4. **User's manual work is lost**

**Additional Context:**

From `ProcessExistingTransferFile()` (lines 297-326):
```python
# Load existing transfer file
tree = ET.parse(fileName)
self.root = tree.getroot()

# Read existing IDs
for macro in self.root.findall('.//def-macro'):
    self.usedIDs.add(macro.get('n'))

# ⚠️ NOTE: Multi-source macro reuse disabled (Issue #661)
# The commented-out code here would read macros for reuse
```

**Impact:**
- Users lose manually-created variables and macros
- No way to combine Rule Assistant + manual editing safely
- Forces users to choose: use RA *or* manual editing, not both

**Affected Workflows:**
- Linguists who create basic rules with RA, then add advanced macros manually
- Power users who want RA for repetitive work, manual editing for edge cases
- Teams where some members use GUI, others edit XML directly

#### FR-002: File State Synchronization Issues

**Severity:** High
**Impact:** User confusion, potential data inconsistency
**Source:** Multiple user reports

**Problem:**
The Rule Assistant's data synchronization behavior is unclear and potentially buggy:

1. Uncertainty about data source (FLEx DB vs .t1x vs cached XML)
2. Manual edits to .t1x may be lost
3. Changes to FLEx project may not be reflected
4. No way to force reload of FLEx data

**User Questions:**
- "When I start up the RA again, where is it getting its info from?"
- "Does it keep the edits you made?"
- "Do changes in my FLEx project get picked up?"

**Root Cause:** Architectural ambiguity

**Current Behavior (Needs Verification):**

```python
# RuleAssistant.py (GUI Module) - Startup sequence
def MainFunction(db, report, modify=True):
    # ❓ What happens here?
    # - Does it reload FLEx data every time?
    # - Does it cache data?
    # - Does it read existing .t1x?

    # ❓ If user manually edited .t1x, what happens?
    # - Are edits preserved?
    # - Are they overwritten?
    # - Is there a warning?
```

**Hypothesis:** Data flow is:

```
Startup:
  1. Load Rule Assistant XML (user's rule definitions)
  2. ❓ Load .t1x file (existing transfer rules)
  3. ❓ Query FLEx database (morphological data)

During Rule Creation:
  1. Query FLEx for current data (features, affixes, stems)
  2. Generate transfer rules based on current FLEx state
  3. ❓ Merge with existing .t1x or overwrite?

On Save:
  1. Write Rule Assistant XML (always safe - RA's own format)
  2. Write .t1x transfer file (❓ merge or overwrite?)
```

**Needed Clarification:**
- When is FLEx data queried? (startup, every rule, on demand?)
- What is cached vs. re-queried?
- How are manual .t1x edits handled?
- What triggers data refresh?

#### FR-003: Confusing Error Messages

**Severity:** Medium-High
**Impact:** User confusion, reduced trust
**Source:** User feedback

**Problem:** Pre-populate module shows "file has been edited" error even when file is fresh/unedited.

**User Report:**
> "This error message is confusing... I had edited the file before, but then I replaced it with the 'start file', so maybe I hadn't edited this copy of it. When I re-ran this module, it again gave me this error, even though I had saved it in between. But in spite of the error, it still added categories etc to the rule file, and left the rule file in a Saved state."

**Hypothesis:**
- Detection logic has false positives
- Checks file timestamp/hash, gets confused by saves
- "Edited" might mean "has any content" rather than "manually modified"

### High-Priority Technical Debt

#### TODO Line 233: Incomplete Affix Tag Generation

**Location:** `CreateApertiumRules.py:233`

```python
def GetCategoryName(self, cat: str, features: list, affixes: list) -> str:
    # ... feature permutation logic ...
    if next_tag_list:
        tag_list = next_tag_list
    # TODO: get tags for affixes  ⚠️ INCOMPLETE
```

**Impact:**
- Categories with affixes may not generate complete tag lists
- Affix-based pattern matching may fail
- Rules with affixes may not work correctly

**Estimated Complexity:** Medium (2.5 hours)

#### TODO Lines 808-809: Variable Naming Confusion

**Location:** `CreateApertiumRules.py:808-809`

```python
def GetMultiFeatureMacro(self, destCategory: str, isLemma: bool,
                         sources: list[FeatureSpec]) -> MacroSpec:
    # TODO: most of the variable names in this function are from when
    # it was solely for lemmas. They should probably be updated.

    # Variables like 'possibleLemmas' used for both lemmas and affixes
```

**Impact:**
- Code readability reduced
- Maintenance difficult
- Future developers confused

**Estimated Complexity:** Low (2.5 hours)

#### TODO Line 1252: Proper Noun Capitalization

**Location:** `CreateApertiumRules.py:1252`

```python
# Capitalize the word based on its position in the rule.
# TODO: check that it's not a proper noun
if index == 0 and (pos != '1' or shouldUseLemmaMacro):
    lemCase = ET.SubElement(lu, 'get-case-from', pos='1')
```

**Impact:**
- Proper nouns may lose capitalization when moved
- "John" → "john" if repositioned to non-initial position
- Linguistically incorrect output

**Estimated Complexity:** Medium (5 hours)

#### TODO Line 1552: File Mode Validation

**Location:** `CreateApertiumRules.py:1552`

```python
# TODO check for proper reading mode ("w" or "wb")
try:
    with open(ruleAssistantFile, "r") as rulesAssistant:
        assistantTree = ET.parse(rulesAssistant)
```

**Impact:**
- Comment is confusing (mentions write modes for read operation)
- No encoding specified (should be UTF-8)
- Error handling could be improved

**Estimated Complexity:** Low (2.5 hours)

### Architectural Limitations

#### Issue #661: Multi-Source Macro Reuse Disabled

**Location:** `CreateApertiumRules.py:314-326`

```python
for macro in self.root.findall('.//def-macro'):
    self.usedIDs.add(macro.get('n'))
    # The block below allows multi-source macros to be reused,
    # but this causes some problems, so we're disabling it for now.
    # See #661
    '''
    if code := macro.get('c'):
        items = code.split()
        if len(items) > 3 and items[0] == 'FTM':
            lookupKey = (items[2], tuple(items[3:]))
            self.lemmaMacros[lookupKey] = MacroSpec(...)
    '''
```

**Original Intent:**
Avoid creating duplicate macros when multiple rules need the same lemma/affix transformation.

**Why Disabled:**
1. Variable name conflicts
2. Incomplete macro matching (lookup key too simple)
3. Macro content drift (hand-edited macros reused incorrectly)
4. Test failures

**Current Impact:**
- Larger transfer files (redundant macros)
- Slower processing
- More memory usage
- 30-50% code duplication estimated

**Estimated Complexity:** High (19-21 hours)

#### Limited Affix Type Support

**Current State:**
- Only prefix and suffix supported in DTD
- Infix and circumfix recognized in FLEx but not used
- No position specification for infixes

**DTD Limitation:**
```xml
<!ATTLIST Affix
  type (prefix | suffix) "suffix"  ⚠️ Only 2 of 4 affix types
>
```

**Utils.py Recognition (Unused):**
```python
# Lines 356-373 in Utils.py
circumfixType       = 'd7f713df-e8cf-11d3-9764-00c04f186933'
infixType           = 'd7f713e0-e8cf-11d3-9764-00c04f186933'
infixingInterfixType= 'd7f713de-e8cf-11d3-9764-00c04f186933'
# ⚠️ Recognized but never used in CreateApertiumRules.py
```

**Languages Affected:**
- **Infixes:** Tagalog, Khmer, Chamorro, many Austronesian languages
- **Circumfixes:** German (ge-...-t), Indonesian (ke-...-an), Berber

**Estimated Complexity:** High (18 hours)

---

## Proposed Architecture (To-Be)

### Architectural Principles

1. **Single Source of Truth:** FLEx database is authoritative for morphological data
2. **Clear Data Flow:** Explicit synchronization points and data update triggers
3. **Safe File Operations:** Preserve user edits, warn before overwriting
4. **Extensible Design:** Prepare for future linguistic features
5. **Fail-Safe Defaults:** Preserve data when unsure, warn user explicitly

### Enhanced System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FLEx Database                           │
│  Single Source of Truth for Morphological Data             │
│  - Categories (POS)                                         │
│  - Features (gender, number, etc.)                          │
│  - Affixes (all 4 types: prefix, suffix, infix, circumfix) │
│  - Stems and allomorphs                                     │
└────────────┬────────────────────────────────────────────────┘
             │
             │ Query on:
             │ - RA startup
             │ - "Reload FLEx Data" button
             │ - Rule generation
             ▼
┌─────────────────────────────────────────────────────────────┐
│              Rule Assistant Generator                       │
│              (CreateApertiumRules.py)                       │
│                                                             │
│  ┌──────────────────────────────────────────────┐          │
│  │ Rule Assistant XML          │                │          │
│  │ (User's rule specifications)│                │          │
│  │ - NOT authoritative for     │                │          │
│  │   FLEx data                 │                │          │
│  │ - Authoritative for rule    │    Rule        │          │
│  │   structure only            │  Generation    │          │
│  └──────────────────────────────┤    Engine      │          │
│                                 │                │          │
│  ┌──────────────────────────────┤                │          │
│  │ Transfer Rules .t1x         │                │          │
│  │ (Existing transfer file)    │                │          │
│  │ - Preserve ALL sections     │◀───────────────┘          │
│  │ - Merge new rules           │                           │
│  │ - Warn on conflicts         │                           │
│  └─────────────────────────────┘                           │
└────────────┬────────────────────────────────────────────────┘
             │
             │ Output
             ▼
┌─────────────────────────────────────────────────────────────┐
│           Apertium Transfer Rules (.t1x)                    │
│  Complete, valid transfer rule file with:                   │
│  - All preserved sections (vars, macros, etc.)              │
│  - New/updated rules from RA                                │
│  - Deduplicated macros (Issue #661 fixed)                   │
│  - Support for all affix types                              │
└─────────────────────────────────────────────────────────────┘
```

### Enhanced Data Flow

#### Startup Sequence

```
1. User opens Rule Assistant
   ↓
2. RuleAssistant.py GUI initializes
   ↓
3. Load Rule Assistant XML (user's rule specifications)
   ↓
4. Query FLEx Database (fresh data):
      - getAllCategories()
      - getAllFeatures()
      - getAllAffixes() [including infix, circumfix]
   ↓
5. Populate GUI dropdowns with FLEx data
   ↓
6. IF transfer .t1x exists:
      Load it with ProcessExistingTransferFile()
      Mark all sections for preservation
      Display summary: "Loaded: 5 rules, 12 macros, 3 variables"
   ↓
7. Ready for editing
```

#### Rule Generation Sequence

```
1. User creates/edits rule in XML interface
   ↓
2. User clicks "Generate Transfer Rules"
   ↓
3. Validate Rule Assistant XML
   ↓
4. FOR EACH rule:
      a. Query FLEx for current morphological data
         (features, affixes, stems for categories in rule)
      b. Generate category definitions
      c. Generate attribute definitions
      d. Generate macros (with deduplication - Issue #661 fixed)
      e. Generate pattern and action
   ↓
5. Merge with existing .t1x:
      a. Preserve existing sections (vars, macros, attrs, etc.)
      b. Add/update categories as needed
      c. Add/update attributes as needed
      d. Deduplicate macros
      e. Add/update rules (check overwrite_rules attribute)
   ↓
6. Validate output XML
   ↓
7. Write .t1x file with ALL sections
   ↓
8. Display summary:
      "Generated 3 new rules, added 5 macros (2 reused), preserved 12 existing macros"
```

#### File Preservation Strategy

```python
class RuleGenerator:
    def __init__(self, ...):
        # New: Track sections to preserve
        self.preserveSections = set()
        self.existingMacros = {}
        self.existingVariables = {}

    def ProcessExistingTransferFile(self, fileName: str):
        """Load existing transfer file and mark ALL sections for preservation."""
        tree = ET.parse(fileName)
        self.root = tree.getroot()

        # Mark all existing sections for preservation
        for section in self.root:
            self.preserveSections.add(section.tag)

            if section.tag == 'section-def-macros':
                for macro in section.findall('def-macro'):
                    macroId = macro.get('n')
                    self.existingMacros[macroId] = macro
                    # Compute fingerprint for deduplication (Issue #661)
                    fingerprint = self.GetMacroFingerprint(macro)
                    self.macroFingerprints[fingerprint] = macro

            elif section.tag == 'section-def-vars':
                for var in section.findall('def-var'):
                    varId = var.get('n')
                    self.existingVariables[varId] = var

    def WriteTransferFile(self, fileName: str):
        """Write transfer file, preserving ALL existing sections."""

        # NEW LOGIC: Do NOT delete sections
        # Only delete truly unused items WITHIN sections

        for section in self.root.findall('.//*'):
            if section.tag == 'section-def-macros':
                # Keep section even if empty
                # User may add macros manually later
                pass
            elif section.tag == 'section-def-vars':
                # Keep section even if empty
                pass
            # ... other sections preserved ...

        # Write file
        tree = ET.ElementTree(self.root)
        tree.write(fileName, encoding='UTF-8', xml_declaration=True)

        # Log what was preserved
        self.report.Info(f"Preserved {len(self.existingMacros)} existing macros")
        self.report.Info(f"Preserved {len(self.existingVariables)} existing variables")
```

### Enhanced DTD Schema

```xml
<!ELEMENT Affix (Features*) >
<!ATTLIST Affix
  type (prefix | suffix | infix | circumfix) "suffix"
  position CDATA #IMPLIED
  comment CDATA #IMPLIED
>
```

**Changes:**
1. Added `infix` and `circumfix` to type enumeration
2. Added `position` attribute for infix placement specification
3. Added `comment` for documentation

**Position Specification for Infixes:**
- `"after-first-consonant"` - Insert after first consonant
- `"before-last-vowel"` - Insert before final vowel
- `"character:N"` - Insert after character N (0-indexed)
- `"regex:PATTERN"` - Insert at position matching regex

**Example Infix Rule:**
```xml
<Affix type="infix" position="after-first-consonant">
  <Features>
    <Feature label="tense" value="past"/>
  </Features>
</Affix>
```

**Example Circumfix Rule:**
```xml
<Affix type="circumfix">
  <Features>
    <Feature label="aspect" value="participle"/>
  </Features>
</Affix>
```

### Macro Reuse Architecture (Issue #661 Fix)

**Problem:** Simple lookup key insufficient

**Current (Broken):**
```python
lookupKey = (destCategory, tuple(sourceCats))
# PROBLEM: Same categories, different features collide
```

**Solution A: Macro Fingerprinting (Recommended)**

```python
def GetMacroFingerprint(self, macro: ET.Element) -> str:
    """Generate hash of macro structure for deduplication.

    Normalizes variable names and positions to detect identical logic.
    """
    # Serialize macro content
    content = ET.tostring(macro, encoding='unicode')

    # Normalize variable names
    content = re.sub(r'n="[^"]*"', 'n="VAR"', content)
    content = re.sub(r'pos="[^"]*"', 'pos="POS"', content)

    # Hash normalized content
    import hashlib
    return hashlib.md5(content.encode()).hexdigest()

def GetMultiFeatureMacro(self, destCategory: str, isLemma: bool,
                         sources: list[FeatureSpec]) -> MacroSpec:
    """Get or create macro, with deduplication."""

    # Generate macro (temporary)
    macro = self._GenerateMacro(destCategory, isLemma, sources)

    # Check if equivalent macro exists
    fingerprint = self.GetMacroFingerprint(macro)

    if fingerprint in self.macroFingerprints:
        # Reuse existing macro
        existingMacro = self.macroFingerprints[fingerprint]
        existingId = existingMacro.get('n')
        existingVarid = existingMacro.get('c').split()[1]

        self.report.Info(f"Reusing existing macro {existingId}")

        return MacroSpec(
            macid=existingId,
            varid=existingVarid,
            catSequence=[s.category for s in sources]
        )
    else:
        # Add new macro
        macroId = self.GetAvailableID(f"macro_{destCategory}", self.usedIDs)
        macro.set('n', macroId)

        # Add fingerprint attribute for debugging
        macro.set('fingerprint', fingerprint[:8])

        # Store for future reuse
        self.macroFingerprints[fingerprint] = macro
        self.GetSection('section-def-macros').append(macro)

        return MacroSpec(macid=macroId, ...)
```

**Benefits:**
- Detects truly identical macros regardless of naming
- No false positives from similar categories with different features
- Preserves hand-edited macros (different fingerprint)
- Easy to debug (fingerprint in XML comment)

### Component Responsibilities (Clarified)

#### RuleAssistant.py (GUI Module)

**SHOULD:**
- Provide graphical interface for rule editing
- Load Rule Assistant XML (user's rule specifications)
- Query FLEx database on startup and on "Reload" button
- Invoke CreateApertiumRules for generation
- Display clear status messages about data sources

**SHOULD NOT:**
- Modify transfer .t1x directly
- Cache FLEx data (always query fresh or on demand)
- Make assumptions about .t1x file state

**NEW Features:**
- "Reload FLEx Data" button
- Status bar showing:
  - FLEx project name
  - Last FLEx data reload time
  - Transfer file last modified time
- Warning dialog before overwriting existing .t1x

#### CreateApertiumRules.py (Generation Engine)

**SHOULD:**
- Parse Rule Assistant XML
- Query FLEx database for morphological data at generation time
- Generate Apertium transfer rules
- Preserve ALL existing .t1x sections
- Deduplicate macros
- Provide detailed logging

**SHOULD NOT:**
- Delete sections from existing .t1x
- Assume cached data is current
- Silently overwrite user edits

**NEW Features:**
- Macro fingerprinting for deduplication
- Section preservation logic
- Proper noun detection
- Infix and circumfix support
- Complete affix tag generation

#### Utils.py (FLEx Interface)

**SHOULD:**
- Provide clean API to FLEx database
- Return current, fresh data
- Handle all affix types (prefix, suffix, infix, circumfix)
- Provide proper noun detection

**SHOULD NOT:**
- Cache data (let caller decide)
- Generate transfer rules (that's CreateApertiumRules' job)

**NEW Features:**
- `getAffixType(affix)` - Returns type including infix/circumfix
- `getInfixPosition(affix)` - Returns position specification for infixes
- `isProperNounCategory(cat)` - Detects proper noun POS

---

## Migration Strategy

### Phase 1: Critical Bug Fixes (2 weeks)

**Goal:** Fix data loss issues, improve error handling

#### Week 1: File Preservation

**Tasks:**
1. Fix section deletion logic (FR-001)
   - Modify `WriteTransferFile()` to preserve all sections
   - Add `preserveSections` tracking
   - Update section cleanup logic

2. Improve error messages (FR-003)
   - Fix "file has been edited" false positives
   - Add specific error codes
   - Improve error message context

**Deliverables:**
- No sections deleted from .t1x
- Clear, accurate error messages
- Regression tests

#### Week 2: File Synchronization Documentation

**Tasks:**
1. Document current data flow (FR-002)
   - Trace code to understand exact behavior
   - Document all data sources
   - Identify synchronization points

2. Add status indicators to GUI
   - FLEx data load timestamp
   - Transfer file modification time
   - Warning before overwrite

**Deliverables:**
- Data flow documentation
- GUI status indicators
- User guide section

### Phase 2: Technical Debt Resolution (2 weeks)

**Goal:** Complete TODO items, improve code quality

**Tasks:**
1. Affix tag generation (TODO line 233) - 2.5 hours
2. Variable naming refactoring (TODO lines 808-809) - 2.5 hours
3. Proper noun capitalization (TODO line 1252) - 5 hours
4. File mode validation (TODO line 1552) - 2.5 hours

**Deliverables:**
- All TODOs resolved
- Improved code readability
- Proper noun handling working
- Better file error handling

### Phase 3: Macro Reuse (2-3 weeks)

**Goal:** Re-enable macro reuse with robust deduplication

#### Week 1: Analysis

**Tasks:**
1. Re-enable existing code
2. Run tests to identify exact failures
3. Document failure scenarios
4. Design fingerprinting solution

#### Week 2: Implementation

**Tasks:**
1. Implement `GetMacroFingerprint()`
2. Update `ProcessExistingTransferFile()`
3. Update `GetMultiFeatureMacro()`
4. Add comprehensive tests

#### Week 3: Validation

**Tasks:**
1. Re-enable `ReuseMacro` test class
2. Performance testing
3. Validate on real language pairs
4. Documentation

**Deliverables:**
- Issue #661 resolved
- 30-50% reduction in redundant macros
- No false positives in reuse
- Performance benchmarks

### Phase 4: Affix Type Expansion (3 weeks)

**Goal:** Support infix and circumfix affixes

#### Week 1: DTD and Schema

**Tasks:**
1. Update DTD files (main + XMLmind)
2. Update XML schema validation
3. Document new attributes

#### Week 2: Code Implementation

**Tasks:**
1. Add infix detection and processing
2. Add circumfix detection and processing
3. Update tag generation logic
4. Handle affix ordering

#### Week 3: Testing

**Tasks:**
1. Create test cases for infixes (Tagalog-inspired)
2. Create test cases for circumfixes (German-inspired)
3. Integration testing
4. Documentation and examples

**Deliverables:**
- Full infix support (with limitations documented)
- Full circumfix support
- Example files
- User documentation

### Phase 5: User Experience Improvements (2-3 weeks)

**Goal:** Implement user-requested features

**Tasks:**
1. "Reload FLEx Data" button - 1 week
2. Template management system - 1 week
3. Improved warning messages - 3 days
4. Enhanced documentation - 1 week

**Deliverables:**
- FLEx data reload on demand
- Clean project templates
- Clear, helpful error messages
- Comprehensive user guide

---

## Data Flow Diagrams

### Current Data Flow (Problematic)

```
┌──────────────────────────────────────────────────────────────┐
│                         STARTUP                              │
└──────────────────────────────────────────────────────────────┘

User opens Rule Assistant
         │
         ▼
┌────────────────────┐
│ RuleAssistant.py   │
│ GUI initializes    │
└─────────┬──────────┘
          │
          │ ❓ Data source unclear
          ▼
    ┌─────────┐     ┌──────────────┐     ┌─────────────┐
    │ FLEx DB │ ??? │ RA XML cache │ ??? │ .t1x file   │
    └─────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ GUI ready    │
                    │ (but with    │
                    │  what data?) │
                    └──────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    RULE GENERATION                           │
└──────────────────────────────────────────────────────────────┘

User creates rule and clicks "Generate"
         │
         ▼
┌──────────────────────────────────┐
│ CreateApertiumRules.py           │
│ ProcessAssistantFile()           │
└────────┬─────────────────────────┘
         │
         ├──────────────────┐
         ▼                  ▼
    Query FLEx       Load .t1x (if exists)
    (fresh data)     ProcessExistingTransferFile()
         │                  │
         │                  ▼
         │           ⚠️ May discard sections
         │                  │
         └────────┬─────────┘
                  ▼
         Generate rules
         Generate macros (duplicates - Issue #661)
         Generate categories/attributes
                  │
                  ▼
         WriteTransferFile()
                  │
                  ▼
         ⚠️ Delete "empty" sections (FR-001)
                  │
                  ▼
         Write .t1x file
         (user data may be lost)
```

### Proposed Data Flow (Fixed)

```
┌──────────────────────────────────────────────────────────────┐
│                    STARTUP (Clear)                           │
└──────────────────────────────────────────────────────────────┘

User opens Rule Assistant
         │
         ▼
┌────────────────────┐
│ RuleAssistant.py   │
│ GUI initializes    │
└─────────┬──────────┘
          │
          ├──────────────────────────────────────┐
          │                                      │
          ▼                                      ▼
    Load RA XML                           Query FLEx DB
    (rule definitions)                    (FRESH morphological data)
          │                                      │
          │                                      │
          └──────────────┬───────────────────────┘
                         │
                         ▼
                  Populate GUI
                  (dropdowns, fields)
                         │
                         ▼
                  ✓ Clear status display:
                    "FLEx data loaded: 2025-11-22 14:32"
                    "Project: English-Spanish"
                         │
                         ▼
                  IF .t1x exists:
                    Display: "Existing transfer file found"
                            "Contains: 5 rules, 12 macros, 3 vars"
                         │
                         ▼
                  GUI ready
                  (user knows exactly what data is loaded)

┌──────────────────────────────────────────────────────────────┐
│              RULE GENERATION (Explicit)                      │
└──────────────────────────────────────────────────────────────┘

User clicks "Generate Transfer Rules"
         │
         ▼
    Validate RA XML
         │
         ▼
┌──────────────────────────────────┐
│ CreateApertiumRules.py           │
│ ProcessAssistantFile()           │
└────────┬─────────────────────────┘
         │
         ├──────────────────────────────┐
         │                              │
         ▼                              ▼
    Query FLEx                   Load .t1x (if exists)
    (current data                ProcessExistingTransferFile()
     for this rule)                      │
         │                              ▼
         │                       ✓ Mark ALL sections for preservation
         │                       ✓ Load existing macros
         │                       ✓ Compute macro fingerprints
         │                              │
         └───────────┬──────────────────┘
                     │
                     ▼
          FOR EACH rule:
            - Generate categories
            - Generate attributes
            - Generate/reuse macros (fingerprint matching)
            - Generate pattern & action
                     │
                     ▼
          Merge with existing .t1x:
            ✓ Preserve ALL sections (even if "empty")
            ✓ Deduplicate macros (Issue #661 fixed)
            ✓ Add new rules
            ✓ Respect overwrite_rules attribute
                     │
                     ▼
          Validate output XML
                     │
                     ▼
          Write .t1x file
          (ALL sections preserved)
                     │
                     ▼
          Display summary:
            "Generated: 3 rules"
            "Added: 5 macros (2 reused)"
            "Preserved: 12 existing macros, 3 variables"
            "File: transfer_rules.t1x"

┌──────────────────────────────────────────────────────────────┐
│              RELOAD FLEx DATA (New Feature)                  │
└──────────────────────────────────────────────────────────────┘

User clicks "Reload FLEx Data" button
         │
         ▼
    Show confirmation dialog:
      "Reload morphological data from FLEx?
       This will update categories, features, and affixes.
       Your existing rules will be preserved."
         │
         ▼ [User confirms]
         │
    Query FLEx DB (fresh)
      - getAllCategories()
      - getAllFeatures()
      - getAllAffixes()
         │
         ▼
    Update GUI dropdowns
         │
         ▼
    Check for conflicts:
      - Rules using deleted features → WARNING
      - Rules using deleted categories → WARNING
         │
         ▼
    Display summary:
      "✓ Reloaded: 12 categories, 45 features, 23 affixes"
      "⚠️ 2 rules reference deleted features (see details)"
```

### File Synchronization Flow

```
┌─────────────┐        ┌──────────────┐        ┌────────────┐
│   FLEx DB   │        │   RA XML     │        │  .t1x file │
│  (Source &  │        │ (User rules) │        │ (Transfer  │
│   Target)   │        │              │        │   rules)   │
└──────┬──────┘        └───────┬──────┘        └──────┬─────┘
       │                       │                      │
       │ SINGLE SOURCE         │ SINGLE SOURCE        │ GENERATED
       │ OF TRUTH for          │ OF TRUTH for         │ OUTPUT
       │ Morphological         │ Rule structure       │ (may contain
       │ Data                  │                      │  manual edits)
       │                       │                      │
       │                       │                      │
       ▼                       ▼                      ▼
   ┌────────────────────────────────────────────────────────┐
   │         Rule Generation Process                        │
   │                                                        │
   │  1. Read RA XML (rule structure)                      │
   │  2. Query FLEx DB (current morphological data)        │
   │  3. Load .t1x (existing transfer rules)               │
   │  4. Generate new rules using #1 + #2                  │
   │  5. Merge with #3 (preserve all sections)             │
   │  6. Write .t1x                                        │
   └────────────────────────────────────────────────────────┘
                              │
                              ▼
                      ┌───────────────┐
                      │  Output .t1x  │
                      │  - All new    │
                      │    rules      │
                      │  - All old    │
                      │    content    │
                      │  - No data    │
                      │    loss       │
                      └───────────────┘
```

---

## Component Responsibilities

### Detailed Component Specifications

#### 1. RuleAssistant.py (GUI Module)

**File:** `/home/user/FLExTrans/Dev/Modules/RuleAssistant.py`

**Purpose:** Provide graphical user interface for rule creation and management

**Responsibilities:**

##### Core Functions
- Launch XML editing interface (XMLmind integration)
- Manage Rule Assistant XML files (load, save, validate)
- Invoke rule generation process
- Display status and progress information

##### Data Management
- Load Rule Assistant XML on startup
- Query FLEx database for current morphological data
- Provide "Reload FLEx Data" functionality
- Check for existing transfer files

##### User Interaction
- Rule creation and editing interface
- Progress indicators during generation
- Error and warning display
- Status bar with data source information

**API:**

```python
def MainFunction(db, report, modify=True):
    """Main entry point for Rule Assistant module.

    Args:
        db: FLEx database connection
        report: Reporting object for messages
        modify: Whether modification is allowed
    """
    # Initialize GUI
    # Load RA XML
    # Query FLEx database
    # Check for existing .t1x
    # Display interface
    pass

def ReloadFLExData(db):
    """Reload morphological data from FLEx database.

    Queries FLEx for current categories, features, and affixes.
    Updates GUI dropdowns and displays.
    Checks for conflicts with existing rules.
    """
    pass

def GenerateTransferRules(raXmlPath, t1xPath, db, report):
    """Invoke rule generation process.

    Args:
        raXmlPath: Path to Rule Assistant XML
        t1xPath: Path to transfer rule file
        db: FLEx database connection
        report: Reporting object

    Returns:
        Success status
    """
    from CreateApertiumRules import RuleGenerator
    generator = RuleGenerator(report, db.sourceDB, db.targetDB, "transfer")
    return generator.ProcessAssistantFile(raXmlPath, t1xPath)
```

**UI Enhancements:**

```
┌─────────────────────────────────────────────────────────────┐
│ FLExTrans Rule Assistant                          [_][□][X] │
├─────────────────────────────────────────────────────────────┤
│ File  Edit  Tools  Help                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ [New] [Open] [Save] [Generate Rules] [Reload FLEx]    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Rule Assistant XML Editor                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ <FLExTransRuleGenerator>                               │ │
│  │   <FLExTransRules>                                     │ │
│  │     <Rule name="DET-NOUN">                             │ │
│  │       ...                                              │ │
│  │                                                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│ Status:                                                      │
│ ✓ FLEx Data: Loaded 2025-11-22 14:32 (English-Spanish)     │
│ ✓ Transfer File: transfer_rules.t1x (modified 14:15)       │
│ ✓ Contains: 5 rules, 12 macros, 3 variables                │
└─────────────────────────────────────────────────────────────┘
```

**New Features:**

1. **Reload FLEx Data Button**
   ```
   [Reload FLEx] clicked
        │
        ▼
   Confirmation dialog:
   "Reload morphological data from FLEx database?

    This will update:
    - Categories (parts of speech)
    - Features (gender, number, etc.)
    - Affixes (prefixes, suffixes, infixes, circumfixes)

    Your existing rules will be preserved.

    [Cancel] [Reload]"
        │
        ▼
   Query FLEx database
   Update dropdowns
   Display summary
   ```

2. **Status Bar Enhancement**
   - FLEx project name
   - FLEx data timestamp
   - Transfer file path and timestamp
   - Transfer file content summary

3. **Warning Dialogs**
   - Before overwriting existing .t1x
   - When FLEx changes detected
   - When manual edits might be lost

#### 2. CreateApertiumRules.py (Rule Generation Engine)

**File:** `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py`

**Purpose:** Generate Apertium transfer rules from Rule Assistant XML and FLEx data

**Responsibilities:**

##### Core Processing
- Parse Rule Assistant XML
- Query FLEx database for morphological data
- Generate Apertium transfer rule XML
- Validate input and output

##### Section Management
- Create/update categories (`<section-def-cats>`)
- Create/update attributes (`<section-def-attrs>`)
- Create/update macros (`<section-def-macros>`) with deduplication
- Create/update variables (`<section-def-vars>`)
- Create/update rules (`<section-rules>`)

##### File Operations
- Load existing transfer files
- Preserve all existing sections
- Merge new content with existing
- Write valid Apertium XML

##### Feature Support
- All affix types (prefix, suffix, infix, circumfix)
- Proper noun capitalization
- Match label resolution (α, β, γ, δ)
- Ranked features
- Default values
- Permutation generation
- Disjoint feature sets (Bantu noun classes)

**Enhanced API:**

```python
class RuleGenerator:
    """Generate Apertium transfer rules from Rule Assistant XML."""

    def __init__(self, report, sourceDB, targetDB, ruleName):
        """Initialize generator.

        Args:
            report: Reporting object for messages
            sourceDB: Source language FLEx database
            targetDB: Target language FLEx database
            ruleName: Base name for generated file
        """
        self.report = report
        self.sourceDB = sourceDB
        self.targetDB = targetDB
        self.ruleName = ruleName

        # Existing structures
        self.root = None
        self.usedIDs = set()
        self.lemmaMacros = {}

        # NEW: Section preservation
        self.preserveSections = set()
        self.existingMacros = {}
        self.existingVariables = {}

        # NEW: Macro deduplication (Issue #661)
        self.macroFingerprints = {}

    def ProcessAssistantFile(self, ruleAssistantFile: str,
                            transferRulePath: str,
                            overwrite: bool = False) -> int:
        """Process Rule Assistant XML and generate transfer rules.

        Args:
            ruleAssistantFile: Path to Rule Assistant XML
            transferRulePath: Path to output transfer rule file
            overwrite: Whether to overwrite existing file

        Returns:
            Number of rules generated, or -1 on error
        """
        # Validate input file
        if not self.ValidateInputFile(ruleAssistantFile):
            return -1

        # Load existing transfer file if present
        if os.path.exists(transferRulePath):
            self.ProcessExistingTransferFile(transferRulePath)

        # Parse Rule Assistant XML
        try:
            with open(ruleAssistantFile, 'r', encoding='utf-8') as f:
                assistantTree = ET.parse(f)
        except ET.ParseError as e:
            self.report.Error(f"Error parsing Rule Assistant file: {e}")
            return -1

        # Process rules
        rulesProcessed = 0
        for ruleElement in assistantTree.findall('.//Rule'):
            ruleName = ruleElement.get('name')
            if self.ProcessRule(ruleElement, ruleName, overwrite):
                rulesProcessed += 1

        # Write output
        self.WriteTransferFile(transferRulePath)

        # Report summary
        self.report.Info(f"Generated {rulesProcessed} rules")
        self.report.Info(f"Preserved {len(self.existingMacros)} existing macros")
        self.report.Info(f"Preserved {len(self.existingVariables)} existing variables")

        return rulesProcessed

    def ProcessExistingTransferFile(self, fileName: str):
        """Load existing transfer file and preserve ALL sections.

        Args:
            fileName: Path to existing .t1x file
        """
        try:
            tree = ET.parse(fileName)
            self.root = tree.getroot()
        except ET.ParseError as e:
            self.report.Error(f"Error parsing existing transfer file: {e}")
            return

        # Mark all existing sections for preservation
        for section in self.root:
            self.preserveSections.add(section.tag)
            self.report.Info(f"Preserving section: {section.tag}")

        # Load existing macros
        for macro in self.root.findall('.//def-macro'):
            macroId = macro.get('n')
            self.existingMacros[macroId] = macro
            self.usedIDs.add(macroId)

            # Compute fingerprint for deduplication
            fingerprint = self.GetMacroFingerprint(macro)
            self.macroFingerprints[fingerprint] = MacroSpec(
                macid=macroId,
                varid=macro.get('c', '').split()[1] if macro.get('c') else '',
                catSequence=[]
            )

        # Load existing variables
        for var in self.root.findall('.//def-var'):
            varId = var.get('n')
            self.existingVariables[varId] = var
            self.usedIDs.add(varId)

    def WriteTransferFile(self, fileName: str):
        """Write transfer file, preserving ALL existing sections.

        Args:
            fileName: Path to output .t1x file
        """
        # NEW LOGIC: Do NOT delete sections
        # Sections are preserved even if empty

        # Validate structure
        if not self.ValidateTransferFile():
            self.report.Error("Generated transfer file failed validation")
            return

        # Write file
        tree = ET.ElementTree(self.root)
        tree.write(fileName, encoding='UTF-8', xml_declaration=True)

        self.report.Info(f"Wrote transfer file: {fileName}")

    def GetMacroFingerprint(self, macro: ET.Element) -> str:
        """Generate fingerprint hash of macro structure.

        Normalizes variable names and positions to detect functionally
        identical macros for deduplication (Issue #661 fix).

        Args:
            macro: Macro element to fingerprint

        Returns:
            MD5 hash of normalized macro structure
        """
        # Serialize macro content
        content = ET.tostring(macro, encoding='unicode')

        # Normalize variable names
        content = re.sub(r'n="[^"]*"', 'n="VAR"', content)
        content = re.sub(r'pos="[^"]*"', 'pos="POS"', content)

        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content)

        # Hash normalized content
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()

    def IsProperNoun(self, category: str) -> bool:
        """Check if a category represents a proper noun.

        Args:
            category: POS category to check

        Returns:
            True if this is a proper noun category
        """
        # Check for common proper noun markers
        properNounMarkers = ['np', 'prop', 'proper', 'propn', 'PN']
        catLower = category.lower()

        if any(marker in catLower for marker in properNounMarkers):
            return True

        # Check category hierarchy
        hierarchy = Utils.getCategoryHierarchy(self.targetDB, category)
        return any(marker in cat.lower()
                  for cat in hierarchy
                  for marker in properNounMarkers)
```

#### 3. Utils.py (FLEx Database Interface)

**File:** `/home/user/FLExTrans/Dev/Lib/Utils.py`

**Purpose:** Provide clean API to FLEx database for morphological data

**Responsibilities:**

##### Data Retrieval
- Query categories (parts of speech)
- Query features (grammatical features)
- Query affixes (all types including infix, circumfix)
- Query stems and allomorphs
- Query proper noun information

##### Data Processing
- Extract affix glosses for features
- Get category hierarchies
- Get stem names with feature constraints
- Determine affix types and positions

**Enhanced API:**

```python
def getAffixGlossesForFeature(db, cat: str, label: str, isAffix: bool,
                              splitGloss=None) -> list[tuple]:
    """Get affix glosses for a feature.

    Args:
        db: FLEx database connection
        cat: Category (POS)
        label: Feature label
        isAffix: True if looking for affix morphemes
        splitGloss: Optional split gloss name for disjoint features

    Returns:
        List of (gloss, type, position) tuples where:
        - gloss: Affix gloss string
        - type: 'prefix' | 'suffix' | 'infix' | 'circumfix'
        - position: Position specification (for infixes) or None
    """
    pass

def getAffixType(db, affixGuid: str) -> str:
    """Get the type of an affix.

    Args:
        db: FLEx database connection
        affixGuid: GUID of affix morpheme

    Returns:
        'prefix' | 'suffix' | 'infix' | 'circumfix' | 'unknown'
    """
    affixTypeGuid = db.LexiconGetMorphTypeFromForm(affixGuid)

    if affixTypeGuid == 'd7f713dd-e8cf-11d3-9764-00c04f186933':
        return 'prefix'
    elif affixTypeGuid == 'd7f713e2-e8cf-11d3-9764-00c04f186933':
        return 'suffix'
    elif affixTypeGuid == 'd7f713e0-e8cf-11d3-9764-00c04f186933':
        return 'infix'
    elif affixTypeGuid == 'd7f713df-e8cf-11d3-9764-00c04f186933':
        return 'circumfix'
    else:
        return 'unknown'

def getInfixPosition(db, affixGuid: str) -> Optional[str]:
    """Get position specification for an infix.

    Args:
        db: FLEx database connection
        affixGuid: GUID of infix morpheme

    Returns:
        Position string like "after-first-consonant" or None
    """
    # Query FLEx database for infix environment/position
    # This might be stored in:
    # - Morph type properties
    # - Allomorph environment
    # - Custom fields
    pass

def isProperNounCategory(db, category: str) -> bool:
    """Check if a category is a proper noun.

    Args:
        db: FLEx database connection
        category: Category name to check

    Returns:
        True if this is a proper noun category
    """
    # Check for common proper noun markers in category name
    properNounMarkers = ['np', 'prop', 'proper', 'propn', 'PN']
    if any(marker in category.lower() for marker in properNounMarkers):
        return True

    # Check category hierarchy
    hierarchy = getCategoryHierarchy(db, category)
    return any(marker in cat.lower()
              for cat in hierarchy
              for marker in properNounMarkers)

def getAllCategories(db) -> list[str]:
    """Get all part-of-speech categories from FLEx database.

    Args:
        db: FLEx database connection

    Returns:
        List of category names
    """
    pass

def getAllFeatures(db) -> list[tuple[str, str]]:
    """Get all grammatical features from FLEx database.

    Args:
        db: FLEx database connection

    Returns:
        List of (category, feature_label) tuples
    """
    pass

def getAllAffixes(db) -> list[dict]:
    """Get all affixes from FLEx database.

    Args:
        db: FLEx database connection

    Returns:
        List of affix dictionaries with keys:
        - gloss: Affix gloss
        - type: prefix | suffix | infix | circumfix
        - category: POS category
        - features: List of feature labels
        - position: Position spec (for infixes) or None
    """
    pass
```

---

## File Format Specifications

### Rule Assistant XML Format (Input)

**Filename:** User-specified (e.g., `RuleAssistant.xml`, `my_rules.xml`)

**DTD:** `FLExTransRuleGenerator.dtd`

**Purpose:** Store linguist's rule specifications in human-editable format

**Complete Specification:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE FLExTransRuleGenerator SYSTEM "FLExTransRuleGenerator.dtd">

<FLExTransRuleGenerator>

  <!-- Collection of rules with overwrite behavior -->
  <FLExTransRules overwrite_rules="no">
    <!-- overwrite_rules: "yes" = replace existing rules with same name
                          "no"  = keep both old and new rules -->

    <!-- Individual transfer rule -->
    <Rule name="UNIQUE_RULE_NAME">
      <!-- name: Must be unique within file -->

      <!-- SOURCE PATTERN -->
      <Source>

        <!-- Match group: Features that must agree across words -->
        <MatchGroup>
          <MatchElement label="gender" match="α"/>
          <MatchElement label="number" match="β"/>
          <!-- match: Greek letter (α,β,γ,δ) linking features -->
        </MatchGroup>

        <!-- Source words in order -->
        <Word id="1" category="det" head="no" create_permutations="no">
          <!-- id: Unique within rule, used to reference in Target
               category: Part of speech (must exist in FLEx)
               head: "yes" for main word, "no" for modifiers
               create_permutations: "yes" makes word optional -->

          <!-- Stem features (inherent to the word) -->
          <Stem>
            <Features>
              <Feature label="definiteness" value="def"/>
              <!-- value: Fixed value (pattern matching) -->
            </Features>
          </Stem>

          <!-- Affix features (added to word) -->
          <Affixes>
            <Affix type="suffix" position="after-last-vowel">
              <!-- type: prefix | suffix | infix | circumfix
                   position: Required for infix, specifies insertion point -->
              <Features>
                <Feature label="number" match="β"/>
                <!-- match: Links to MatchGroup -->
              </Features>
            </Affix>
          </Affixes>

          <!-- Features for agreement -->
          <Features>
            <Feature label="gender" match="α"/>
            <Feature label="number" match="β"/>
            <Feature label="case" unmarked_default="nom" ranking="1"/>
            <!-- unmarked_default: Value to use if not specified in input
                 ranking: Priority (1=highest) for multi-feature macros -->
          </Features>
        </Word>

        <Word id="2" category="n" head="yes">
          <Features>
            <Feature label="gender" match="α"/>
            <Feature label="number" match="β"/>
          </Features>
        </Word>

        <!-- Gap in source pattern -->
        <WordGap/>

      </Source>

      <!-- TARGET PATTERN -->
      <Target>
        <!-- Words in target order (may differ from source) -->

        <!-- Reference to source word -->
        <Word id="2" category="n">
          <Features>
            <Feature label="gender" match="α"/>
            <Feature label="number" match="β"/>
          </Features>
        </Word>

        <Word id="1" category="det">
          <Features>
            <Feature label="gender" match="α"/>
            <Feature label="number" match="β"/>
          </Features>
        </Word>

        <!-- Inserted word (not in source) -->
        <Word category="prep">
          <Stem>
            <Features>
              <Feature label="lemma" value="de"/>
              <!-- Fixed lemma for inserted word -->
            </Features>
          </Stem>
        </Word>

        <!-- Gap in target -->
        <WordGap/>

      </Target>

    </Rule>

    <!-- Additional rules... -->

  </FLExTransRules>

  <!-- Can have multiple FLExTransRules sections -->
  <FLExTransRules overwrite_rules="yes">
    <!-- Rules here will overwrite existing rules with same names -->
  </FLExTransRules>

</FLExTransRuleGenerator>
```

**DTD Schema:**

```xml
<!-- Root element -->
<!ELEMENT FLExTransRuleGenerator (FLExTransRules*) >

<!-- Collection of rules -->
<!ELEMENT FLExTransRules (Rule*) >
<!ATTLIST FLExTransRules
  overwrite_rules (yes | no) "no"
  comment CDATA #IMPLIED
>

<!-- Individual rule -->
<!ELEMENT Rule (Source, Target) >
<!ATTLIST Rule
  name CDATA #REQUIRED
  comment CDATA #IMPLIED
>

<!-- Source pattern -->
<!ELEMENT Source (MatchGroup, (Word | WordGap)*) >

<!-- Target pattern -->
<!ELEMENT Target (Word | WordGap)* >

<!-- Match group for feature agreement -->
<!ELEMENT MatchGroup (MatchElement*) >

<!ELEMENT MatchElement EMPTY >
<!ATTLIST MatchElement
  label CDATA #REQUIRED
  match CDATA #REQUIRED
>

<!-- Word in pattern -->
<!ELEMENT Word (Stem?, Affixes?, Features?) >
<!ATTLIST Word
  id CDATA #IMPLIED
  category CDATA #REQUIRED
  head (yes | no) "no"
  create_permutations (yes | no) "no"
  comment CDATA #IMPLIED
>

<!-- Word stem -->
<!ELEMENT Stem (Features?) >

<!-- Affixes collection -->
<!ELEMENT Affixes (Affix*) >

<!-- Individual affix -->
<!ELEMENT Affix (Features*) >
<!ATTLIST Affix
  type (prefix | suffix | infix | circumfix) "suffix"
  position CDATA #IMPLIED
  comment CDATA #IMPLIED
>

<!-- Features collection -->
<!ELEMENT Features (Feature*) >

<!-- Individual feature -->
<!ELEMENT Feature EMPTY >
<!ATTLIST Feature
  label CDATA #REQUIRED
  match CDATA #IMPLIED
  value CDATA #IMPLIED
  unmarked_default CDATA #IMPLIED
  ranking CDATA #IMPLIED
>

<!-- Gap in pattern -->
<!ELEMENT WordGap EMPTY >
```

### Transfer Rule .t1x Format (Output)

**Filename:** `transfer_rules.t1x` (or user-specified)

**DTD:** Apertium transfer DTD

**Purpose:** Executable transfer rules for Apertium MT pipeline

**Complete Specification:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<transfer default="chunk">

  <!-- SECTION 1: Category Definitions -->
  <section-def-cats>
    <!-- Categories are part-of-speech patterns -->

    <def-cat n="det">
      <!-- Category name -->
      <cat-item tags="det.*"/>
      <!-- Tag pattern (det followed by any features) -->
    </def-cat>

    <def-cat n="det_m">
      <!-- Category with feature constraint -->
      <cat-item tags="det.m"/>
      <cat-item tags="det.m.*"/>
      <!-- Masculine determiners only -->
    </def-cat>

    <def-cat n="n">
      <cat-item tags="n.*"/>
    </def-cat>

    <!-- Additional categories... -->
  </section-def-cats>

  <!-- SECTION 2: Attribute Definitions -->
  <section-def-attrs>
    <!-- Attributes are grammatical features -->

    <def-attr n="gender">
      <attr-item tags="m"/>      <!-- masculine -->
      <attr-item tags="f"/>      <!-- feminine -->
      <attr-item tags="nt"/>     <!-- neuter -->
    </def-attr>

    <def-attr n="number">
      <attr-item tags="sg"/>     <!-- singular -->
      <attr-item tags="pl"/>     <!-- plural -->
      <attr-item tags="du"/>     <!-- dual -->
    </def-attr>

    <def-attr n="a_gram_cat">
      <!-- All grammatical categories -->
      <attr-item tags="det"/>
      <attr-item tags="n"/>
      <attr-item tags="adj"/>
      <!-- ... -->
    </def-attr>

    <!-- Affix attributes -->
    <def-attr n="number_affixes">
      <attr-item tags="sg_suf"/>
      <attr-item tags="pl_suf"/>
    </def-attr>

    <!-- Additional attributes... -->
  </section-def-attrs>

  <!-- SECTION 3: Variable Definitions -->
  <section-def-vars>
    <!-- Variables for temporary storage during transfer -->

    <def-var n="temp_gender"/>
    <def-var n="temp_number"/>
    <def-var n="head_noun"/>

    <!-- ⚠️ These should be PRESERVED, not deleted (FR-001 fix) -->
  </section-def-vars>

  <!-- SECTION 4: Macro Definitions -->
  <section-def-macros>
    <!-- Reusable code blocks -->

    <def-macro n="choose_det_lemma" npar="2"
               c="FTM det_lemma_from_n-det det n det">
      <!-- npar: Number of parameters
           c: Comment for macro deduplication (Issue #661)
              Format: "FTM {varid} {destCat} {sourceCat1} {sourceCat2} ..." -->

      <let>
        <var n="det_lemma_from_n-det"/>
        <choose>
          <when>
            <test>
              <and>
                <equal>
                  <clip pos="1" side="tl" part="gender"/>
                  <lit-tag v="m"/>
                </equal>
                <equal>
                  <clip pos="2" side="tl" part="number"/>
                  <lit-tag v="sg"/>
                </equal>
              </and>
            </test>
            <lit v="el"/>
          </when>
          <when>
            <test>
              <and>
                <equal>
                  <clip pos="1" side="tl" part="gender"/>
                  <lit-tag v="m"/>
                </equal>
                <equal>
                  <clip pos="2" side="tl" part="number"/>
                  <lit-tag v="pl"/>
                </equal>
              </and>
            </test>
            <lit v="los"/>
          </when>
          <!-- Additional when clauses... -->
          <otherwise>
            <lit v="el"/>  <!-- default -->
          </otherwise>
        </choose>
      </let>
    </def-macro>

    <!-- Additional macros... -->
    <!-- ⚠️ These should be PRESERVED and DEDUPLICATED (FR-001, Issue #661) -->

  </section-def-macros>

  <!-- SECTION 5: Transfer Rules -->
  <section-rules>
    <!-- Actual transfer rules -->

    <rule comment="DET-NOUN: English det-noun to Spanish noun-det">
      <!-- comment: Rule name from RA XML -->

      <!-- PATTERN: What to match in source -->
      <pattern>
        <pattern-item n="det"/>
        <pattern-item n="n"/>
      </pattern>

      <!-- ACTION: What to output -->
      <action>
        <!-- Output in target order -->
        <out>

          <!-- WORD 1: Noun (was word 2 in source) -->
          <lu>
            <!-- Lemma (possibly from macro) -->
            <clip pos="2" side="tl" part="lem"/>

            <!-- Grammatical category -->
            <clip pos="2" side="tl" part="a_gram_cat"/>

            <!-- Gender (from source noun) -->
            <clip pos="2" side="tl" part="gender"/>

            <!-- Number (from source noun) -->
            <clip pos="2" side="tl" part="number"/>
          </lu>

          <!-- Space -->
          <b pos="1"/>

          <!-- WORD 2: Determiner (was word 1 in source) -->
          <lu>
            <!-- Lemma from macro (based on noun features) -->
            <var n="det_lemma_from_n-det"/>

            <!-- Category -->
            <lit-tag v="det"/>

            <!-- Gender (agree with noun) -->
            <clip pos="2" side="tl" part="gender"/>

            <!-- Number (agree with noun) -->
            <clip pos="2" side="tl" part="number"/>

            <!-- Capitalization (first word) -->
            <get-case-from pos="1">
              <clip pos="2" side="tl" part="lem"/>
            </get-case-from>
          </lu>

        </out>
      </action>
    </rule>

    <!-- Additional rules... -->

  </section-rules>

</transfer>
```

**Section Preservation Requirements (FR-001 Fix):**

```xml
<!-- ALL sections must be preserved, even if empty from RA's perspective -->

<transfer default="chunk">
  <section-def-cats>
    <!-- Generated by RA + existing -->
  </section-def-cats>

  <section-def-attrs>
    <!-- Generated by RA + existing -->
  </section-def-attrs>

  <section-def-vars>
    <!-- ✓ PRESERVED even if RA doesn't create variables -->
    <!-- User's manual variables kept here -->
  </section-def-vars>

  <section-def-macros>
    <!-- ✓ PRESERVED with deduplication (Issue #661) -->
    <!-- User's manual macros + RA-generated macros -->
    <!-- Duplicates removed by fingerprint matching -->
  </section-def-macros>

  <section-rules>
    <!-- Generated by RA -->
    <!-- Existing rules preserved or overwritten based on overwrite_rules -->
  </section-rules>
</transfer>
```

---

## Integration Points

### FLEx Database Integration

**Communication:** Direct database queries via COM interface (Windows) or Python bindings

**Query Types:**

1. **Category Queries:**
   ```python
   # Get all part-of-speech categories
   categories = db.getCategoriesInUse()

   # Get category hierarchy
   hierarchy = Utils.getCategoryHierarchy(db, 'n')
   # Returns: ['n', 'noun', 'substantive', ...]
   ```

2. **Feature Queries:**
   ```python
   # Get all features for a category
   features = db.getFeaturesForCategory('n')
   # Returns: [('gender', 'm|f|nt'), ('number', 'sg|pl'), ...]
   ```

3. **Affix Queries:**
   ```python
   # Get affixes for a feature
   affixes = Utils.getAffixGlossesForFeature(db, 'n', 'number', True)
   # Returns: [('-s', 'suffix', None), ('-es', 'suffix', None), ...]
   ```

4. **Stem Queries:**
   ```python
   # Get stem name with feature constraints
   stem = Utils.getStemName(db, 'casa', 'n', [('gender', 'f')])
   # Returns: 'casa'
   ```

**Data Freshness:**
- Query on RA startup
- Query on "Reload FLEx Data" button
- Query during rule generation (for current rule only)

### Apertium Integration

**File Format:** Apertium transfer rule XML (.t1x)

**Compilation:**
```bash
apertium-preprocess-transfer transfer_rules.t1x transfer_rules.bin
```

**Execution:**
```bash
lt-proc en-es.automorf.bin < input.txt | \
apertium-transfer transfer_rules.t1x transfer_rules.bin en-es.autobil.bin | \
lt-proc -g en-es.autogen.bin
```

**Rule Assistant generates transfer rules that integrate with:**
1. Morphological analyzer (lt-proc with .automorf.bin)
2. Bilingual dictionary (.autobil.bin)
3. Morphological generator (lt-proc with .autogen.bin)

### XMLmind Integration

**Purpose:** Provide structured XML editing interface

**Integration:**
- Rule Assistant launches XMLmind with FLExTransRuleGenerator.dtd
- User edits rules in graphical XML editor
- RA reads resulting XML file

**Configuration Files:**
- `/home/user/FLExTrans/Rule Assistant/FLExTransRuleGenerator.dtd`
- `/home/user/FLExTrans/XXEaddon/FLExTransRuleGeneratorXMLmind/dtds/FLExTransRuleGenerator.dtd`

---

## Performance Considerations

### Current Performance Characteristics

**Bottlenecks Identified:**

1. **FLEx Database Queries:** O(n) queries per rule, where n = number of words
2. **Macro Generation:** Redundant macro creation (Issue #661)
3. **File I/O:** Multiple file reads/writes
4. **XML Parsing:** Large transfer files slow to parse

**Typical Performance:**
- Simple rule (2-3 words): <1 second
- Complex rule (5+ words, affixes): 2-5 seconds
- Large project (50+ rules): 30-60 seconds

### Optimization Strategies

#### 1. FLEx Query Caching

```python
class RuleGenerator:
    def __init__(self, ...):
        self.featureCache = {}
        self.affixCache = {}
        self.categoryCache = {}

    def GetAffixesForFeature(self, cat, label, isAffix):
        """Get affixes with caching."""
        key = (cat, label, isAffix)
        if key not in self.affixCache:
            self.affixCache[key] = Utils.getAffixGlossesForFeature(
                self.targetDB, cat, label, isAffix
            )
        return self.affixCache[key]
```

**Benefit:** Reduce redundant FLEx queries from O(n*m) to O(n) where n=unique feature requests, m=rules

#### 2. Macro Deduplication (Issue #661)

```python
def GetMultiFeatureMacro(self, ...):
    """Get or create macro with fingerprint deduplication."""

    # Generate macro
    macro = self._GenerateMacro(...)

    # Check fingerprint
    fingerprint = self.GetMacroFingerprint(macro)

    if fingerprint in self.macroFingerprints:
        # Reuse: O(1) hash lookup
        return self.macroFingerprints[fingerprint]
    else:
        # Create new
        self.macroFingerprints[fingerprint] = macro
        return macro
```

**Benefit:** 30-50% reduction in redundant macros, smaller file size

#### 3. Incremental File Writing

```python
def WriteTransferFile(self, fileName: str):
    """Write transfer file incrementally."""

    # Write directly to file instead of building full tree in memory
    with ET.xmlfile(fileName, encoding='UTF-8') as xf:
        xf.write_declaration()

        with xf.element('transfer', default='chunk'):
            # Write each section as it's ready
            self._WriteSection(xf, 'section-def-cats')
            self._WriteSection(xf, 'section-def-attrs')
            # ...
```

**Benefit:** Reduce memory usage for large files, faster writes

#### 4. Parallel Rule Processing (Future)

```python
from concurrent.futures import ThreadPoolExecutor

def ProcessAssistantFile(self, ...):
    """Process rules in parallel."""

    rules = assistantTree.findall('.//Rule')

    # Process rules in parallel (thread-safe)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(self.ProcessRule, rule, rule.get('name'), overwrite)
            for rule in rules
        ]
        results = [f.result() for f in futures]
```

**Benefit:** 2-4x speedup for large projects (if thread-safe)

### Performance Targets

| Metric | Current | Target (Post-Fix) | Target (Optimized) |
|--------|---------|-------------------|---------------------|
| Simple rule generation | <1s | <1s | <0.5s |
| Complex rule generation | 2-5s | 2-5s | 1-2s |
| 50-rule project | 30-60s | 20-40s | 10-20s |
| Macro deduplication | Disabled | 30-50% reduction | 50-70% reduction |
| Transfer file size | Baseline | -30% (dedup) | -40% (dedup + optimization) |
| Memory usage (large project) | High | Medium | Low (incremental) |

---

## Conclusion

This architecture document provides a comprehensive technical foundation for Rule Assistant development, addressing:

1. **Critical bugs** (FR-001, FR-002, FR-003) with clear root cause analysis
2. **Technical debt** (TODOs, Issue #661) with implementation specifications
3. **Feature gaps** (infix/circumfix support) with detailed design
4. **Data flow** clarification to resolve user confusion
5. **Migration path** from current to proposed architecture

**Next Steps:**
1. Review with development team
2. Prioritize implementation phases
3. Begin Phase 1: Critical bug fixes
4. Proceed through phases 2-5 as resources allow

**Key Success Factors:**
- Maintain backward compatibility
- Preserve user data (no data loss)
- Improve error messages and user feedback
- Expand linguistic coverage systematically
- Document everything clearly

---

**Document Control:**
- **Version:** 1.0
- **Date:** 2025-11-22
- **Status:** For Review
- **Next Review:** After Phase 1 completion
- **Approval:** Pending stakeholder review

---

*This architecture document synthesizes findings from the Implementation Plan, Roadmap, Feature Requests, and Test Coverage documents to provide a unified technical design for Rule Assistant enhancement.*
