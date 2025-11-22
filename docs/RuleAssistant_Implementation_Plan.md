# Rule Assistant Implementation Plan

**Version:** 1.0
**Date:** 2025-11-22
**Author:** Claude Code Analysis
**Status:** Draft

## Executive Summary

This document provides a comprehensive technical implementation plan for high-priority improvements to the FLExTrans Rule Assistant. The plan covers three main areas:

1. **Fixing 4 TODO items** in CreateApertiumRules.py
2. **Adding infix and circumfix support** to the Rule Generator
3. **Re-enabling multi-source macro reuse** (issue #661)

## Table of Contents

1. [TODO Items Resolution](#1-todo-items-resolution)
2. [Infix and Circumfix Support](#2-infix-and-circumfix-support)
3. [Multi-Source Macro Reuse](#3-multi-source-macro-reuse)
4. [Testing Strategy](#4-testing-strategy)
5. [Implementation Timeline](#5-implementation-timeline)

---

## 1. TODO Items Resolution

### 1.1 Line 233: Complete Affix Tag Generation

**Location:** `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py:233`

#### Current State
```python
# TODO: get tags for affixes
```

The `GetCategoryName()` method generates all possible permutations of feature tags but does not currently include affix tags in the category definition.

#### Context
The code at lines 225-232 generates tag permutations for features:
```python
for seq in permutations(sorted(features)):
    append = ['']
    for label, value in seq:
        append = [f'{a}.{value}' for a in append] + \
            [f'{a}.{value}.*' for a in append]
    next_tag_list += [t+a for t in tag_list for a in append]
if next_tag_list:
    tag_list = next_tag_list
# TODO: get tags for affixes  # Line 233
```

#### Root Cause
The function handles features but was never completed to handle affixes in the same manner. Affixes need to be added to the tag list to ensure proper pattern matching in Apertium transfer rules.

#### Proposed Solution

Add similar permutation logic for affixes after the feature processing:

```python
# After line 232
if next_tag_list:
    tag_list = next_tag_list

# New code to replace TODO at line 233:
# Generate tag permutations including affixes
if affixes:
    affix_tag_list = []
    for seq in permutations(sorted(affixes)):
        for existing_tag in tag_list:
            append = [existing_tag]
            for label, value in seq:
                append = [f'{a}.{value}' for a in append] + \
                    [f'{a}.{value}.*' for a in append]
            affix_tag_list.extend(append)
    tag_list = affix_tag_list if affix_tag_list else tag_list
```

#### Implementation Steps

1. **Research affix tag structure** (0.5 hours)
   - Examine how affix tags are structured in Apertium
   - Review existing affix handling in `GetAttributeValues()` method (line 405)
   - Understand how `Utils.getAffixGlossesForFeature()` returns affix tags

2. **Implement tag generation** (1 hour)
   - Add permutation logic for affix tags similar to feature tags
   - Ensure affixes are appended after features in the tag sequence
   - Handle empty affix sets gracefully

3. **Test with various affix combinations** (1 hour)
   - Create test cases with 0, 1, 2, and 3+ affixes
   - Verify tag ordering matches Apertium expectations
   - Test interaction between features and affixes

#### Testing Requirements

- Unit tests for `GetCategoryName()` with various affix combinations
- Integration tests verifying category definitions in generated transfer files
- Regression tests ensuring existing functionality unchanged

#### Complexity Estimate
**Medium** - Requires understanding tag structure and permutation logic, but follows established pattern.

**Effort:** 2.5 hours
**Risk:** Low - Well-contained change with clear pattern to follow

---

### 1.2 Lines 808-809: Variable Naming Refactoring

**Location:** `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py:808-809`

#### Current State
```python
# TODO: most of the variable names in this function are from when
# it was solely for lemmas. They should probably be updated.
```

The `GetMultiFeatureMacro()` function was originally written to handle only lemmas but was later extended to also handle affixes. Variable names reflect the original lemma-only purpose.

#### Context

The function signature shows dual purpose:
```python
def GetMultiFeatureMacro(self, destCategory: str, isLemma: bool, sources: list[FeatureSpec]) -> MacroSpec:
```

But variables throughout use lemma-centric naming:
- `possibleLemmas` (lines 895, 919, 922, etc.)
- `lemmaTags` (line 1215)
- `lemmaLocs` (line 1216)
- Comments referencing "lemmas" when they mean "lemmas or affixes"

#### Proposed Solution

Rename variables to be semantically neutral:

| Old Name | New Name | Lines Affected |
|----------|----------|----------------|
| `possibleLemmas` | `possibleValues` | 895, 919, 922, 927, 933, 939, 947, 950, 954, 992, 1000, 1009-1020 |
| `lemmaTags` | `featureTags` | 1215, 1238 |
| `lemmaLocs` | `featureLocations` | 1216, 1243, 1271 |
| `affixesByFeatureValue` | `valuesByFeature` | 855, 875, 883, 888, 912 |

Additionally, update comments to use "values" or "lemmas/affixes" instead of just "lemmas".

#### Implementation Steps

1. **Create comprehensive variable mapping** (0.5 hours)
   - Use grep to find all occurrences of each variable
   - Document current usage context
   - Verify no name conflicts with new names

2. **Perform systematic refactoring** (1.5 hours)
   - Rename variables using IDE refactoring tools or careful search-replace
   - Update all comments to reflect new naming
   - Update docstring to clarify dual purpose

3. **Code review and validation** (0.5 hours)
   - Verify no unintended renames
   - Check that logic remains clear
   - Ensure variable scopes unchanged

#### Testing Requirements

- Run full test suite to ensure no logic changes
- Code review to verify improved readability
- No new tests needed (refactoring only)

#### Complexity Estimate
**Low** - Pure refactoring with no logic changes.

**Effort:** 2.5 hours
**Risk:** Very Low - Mechanical change with clear mappings

---

### 1.3 Line 1252: Proper Noun Capitalization Handling

**Location:** `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py:1252`

#### Current State
```python
# Capitalize the word based on its position in the rule.
# TODO: check that it's not a proper noun
if index == 0 and (pos != '1' or shouldUseLemmaMacro):
    lemCase = ET.SubElement(lu, 'get-case-from', pos='1')
```

Currently, the code applies capitalization rules based solely on word position, without considering whether the word is a proper noun that should maintain its capitalization.

#### Context

The capitalization logic (lines 1251-1262) handles:
- First word of output: gets case from first input word
- Repositioned first input word: gets case from its new position
- Other words: no case modification

Problem: Proper nouns should maintain their capitalization regardless of position.

#### Root Cause Analysis

The FLEx database has part-of-speech information that can identify proper nouns, but this isn't currently checked during rule generation. Apertium has mechanisms for handling proper nouns, but they need to be invoked.

#### Proposed Solution

**Option A: Skip case handling for proper nouns (Recommended)**

1. Check if the part-of-speech is a proper noun variant
2. Skip `get-case-from` generation for proper nouns
3. Let Apertium preserve the original capitalization

```python
# Capitalize the word based on its position in the rule.
# Check if this is a proper noun - if so, preserve original capitalization
isProperNoun = self.IsProperNoun(cat, pos if pos else None)

if not isProperNoun:
    if index == 0 and (pos != '1' or shouldUseLemmaMacro):
        lemCase = ET.SubElement(lu, 'get-case-from', pos='1')
    elif index > 0 and pos == '1' and index < len(sourceWords):
        lemCase = ET.SubElement(lu, 'get-case-from', pos=str(index+1))
    else:
        lemCase = lu
else:
    lemCase = lu  # No case modification for proper nouns
```

**Option B: Use Apertium's proper noun tag**

Add a proper noun tag to categories that are proper nouns, which Apertium will recognize and handle appropriately.

#### Implementation Steps

1. **Research proper noun handling in FLEx** (1 hour)
   - Examine how FLEx identifies proper nouns
   - Check for proper noun POS categories in source/target databases
   - Review `Utils.getCategoryHierarchy()` for proper noun detection

2. **Implement IsProperNoun helper method** (1.5 hours)
   ```python
   def IsProperNoun(self, category: str, pos: Optional[str] = None) -> bool:
       """Check if a category represents a proper noun.

       Args:
           category: The part-of-speech category
           pos: Optional position for checking source word

       Returns:
           True if this is a proper noun category
       """
       # Check category name for proper noun indicators
       properNounMarkers = ['np', 'prop', 'proper', 'propn']
       catLower = category.lower()

       if any(marker in catLower for marker in properNounMarkers):
           return True

       # Check hierarchy for proper noun parents
       hierarchy = self.GetCategory(category)
       return any(marker in cat.lower()
                  for cat in hierarchy
                  for marker in properNounMarkers)
   ```

3. **Update capitalization logic** (0.5 hours)
   - Modify lines 1251-1262 to check `IsProperNoun()`
   - Add explanatory comments
   - Handle edge cases (inserted proper nouns, etc.)

4. **Test with various proper noun scenarios** (2 hours)
   - Proper noun in initial position
   - Proper noun in non-initial position
   - Proper noun being moved to different position
   - Multiple proper nouns in one rule
   - Proper nouns with different capitalizations in lexicon

#### Testing Requirements

- Create test rules with proper nouns in various positions
- Verify capitalization preserved for proper nouns
- Verify capitalization adjusted for common nouns
- Test with different language pairs

#### Complexity Estimate
**Medium** - Requires understanding FLEx POS system and Apertium case handling.

**Effort:** 5 hours
**Risk:** Medium - Interaction with language-specific data; needs careful testing

---

### 1.4 Line 1552: File Mode Validation

**Location:** `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py:1552`

#### Current State
```python
# TODO check for proper reading mode ("w" or "wb")
try:
    with open(ruleAssistantFile, "r") as rulesAssistant:
        assistantTree = ET.parse(rulesAssistant)
```

The comment mentions checking for "w" or "wb" (write modes) but the code actually opens the file in "r" (read mode). This appears to be a confused TODO comment.

#### Root Cause Analysis

The confusion likely stems from:
1. Copy-paste error from file writing code
2. Misunderstanding about what needs validation
3. Unclear what the original intent was

The actual issue may be one of:
- Should we validate the file is writable before processing?
- Should we use binary mode ("rb") for better encoding handling?
- Should we validate the transfer file path before writing?

#### Proposed Solution

**Option A: Remove the confusing TODO and improve error handling (Recommended)**

The current error handling is too broad. Improve it:

```python
# Validate input file exists and is readable
if not os.path.exists(ruleAssistantFile):
    report.Error(_translate('CreateApertiumRules',
        'Rule Assistant file not found: {file}').format(file=ruleAssistantFile))
    return -1

if not os.access(ruleAssistantFile, os.R_OK):
    report.Error(_translate('CreateApertiumRules',
        'Rule Assistant file is not readable: {file}').format(file=ruleAssistantFile))
    return -1

try:
    with open(ruleAssistantFile, "r", encoding="utf-8") as rulesAssistant:
        assistantTree = ET.parse(rulesAssistant)
except ET.ParseError as e:
    report.Error(_translate('CreateApertiumRules',
        'Error parsing Rule Assistant file: {error}').format(error=str(e)))
    return -1
except IOError as e:
    report.Error(_translate('CreateApertiumRules',
        'Error reading Rule Assistant file: {error}').format(error=str(e)))
    return -1
```

**Option B: Add output file validation**

Additionally validate the output path:

```python
# Validate output directory exists and is writable
outputDir = os.path.dirname(transferRulePath)
if outputDir and not os.path.exists(outputDir):
    report.Error(_translate('CreateApertiumRules',
        'Output directory does not exist: {dir}').format(dir=outputDir))
    return -1

if outputDir and not os.access(outputDir, os.W_OK):
    report.Error(_translate('CreateApertiumRules',
        'Output directory is not writable: {dir}').format(dir=outputDir))
    return -1
```

#### Implementation Steps

1. **Clarify original intent** (0.5 hours)
   - Review git history for context
   - Check related code for similar patterns
   - Determine what validation is actually needed

2. **Implement proper error handling** (1 hour)
   - Add specific exception handlers
   - Add file existence and permission checks
   - Improve error messages for users
   - Specify UTF-8 encoding explicitly

3. **Test error conditions** (1 hour)
   - Test with non-existent file
   - Test with unreadable file
   - Test with malformed XML
   - Test with non-writable output directory
   - Verify error messages are helpful

#### Testing Requirements

- Test with missing input file
- Test with invalid XML
- Test with read-protected file
- Test with non-writable output directory
- Verify error messages are clear and actionable

#### Complexity Estimate
**Low** - Straightforward error handling improvement.

**Effort:** 2.5 hours
**Risk:** Very Low - Only improving error handling, not changing core logic

---

## 2. Infix and Circumfix Support

### 2.1 Overview

Currently, the Rule Assistant only supports prefixes and suffixes. However, the FLEx database model already includes infix and circumfix morphological types (see `Utils.py:356-373`). This section details how to add full support for these affix types.

### 2.2 Current State Analysis

**FLEx Support:** Already exists
- Circumfix GUID: `d7f713df-e8cf-11d3-9764-00c04f186933`
- Infix GUID: `d7f713e0-e8cf-11d3-9764-00c04f186933`
- Infixing interfix GUID: `d7f713de-e8cf-11d3-9764-00c04f186933`

**DTD Support:** Missing
```xml
<!-- Current DTD (FLExTransRuleGenerator.dtd:38-40) -->
<!ELEMENT Affix (Features*) >
<!ATTLIST Affix
  type (prefix | suffix) "suffix"
>
```

**Code Support:** Partial
- `CreateApertiumRules.py` checks affix type (line 1289)
- Only handles prefix/suffix distinction
- No special handling for infixes or circumfixes

### 2.3 DTD Schema Changes

#### File: `/home/user/FLExTrans/Rule Assistant/FLExTransRuleGenerator.dtd`

**Change 1: Expand Affix type attribute**

Location: Lines 37-40

```xml
<!-- OLD -->
<!ELEMENT Affix (Features*) >
<!ATTLIST Affix
  type (prefix | suffix) "suffix"
>

<!-- NEW -->
<!ELEMENT Affix (Features*) >
<!ATTLIST Affix
  type (prefix | suffix | infix | circumfix) "suffix"
  position CDATA #IMPLIED
>
```

The `position` attribute for infixes specifies where the infix should be inserted (e.g., "after-first-consonant", "before-final-vowel"). For circumfixes, it's not needed as they split around the entire stem.

**Change 2: Update XMLmind configuration**

Location: `/home/user/FLExTrans/XXEaddon/FLExTransRuleGeneratorXMLmind/dtds/FLExTransRuleGenerator.dtd`

Apply the same changes to the XMLmind addon version to ensure UI support.

### 2.4 Code Changes in CreateApertiumRules.py

#### Change 1: Update ProcessRule to handle all affix types

Location: Lines 1284-1306

**Current code:**
```python
# Collect the affixes, splitting them into prefixes and suffixes
# to ensure they come out in the right order.
prefixes = []
suffixes = []
for affix in word.findall('.//Affix'):
    prefix = (affix.get('type', 'suffix') == 'prefix')
    # ... collect features ...
    if prefix:
        prefixes.append(features)
    else:
        suffixes.append(features)

# For each affix...
for affix in prefixes + suffixes:
```

**New code:**
```python
# Collect the affixes, organizing by type to ensure correct ordering:
# prefixes -> infixes -> stem -> suffixes -> circumfix (if any)
prefixes = []
infixes = []
suffixes = []
circumfixes = []

for affix in word.findall('.//Affix'):
    affixType = affix.get('type', 'suffix')
    features = []
    # ... collect features (unchanged) ...

    if not features:
        continue

    if affixType == 'prefix':
        prefixes.append(features)
    elif affixType == 'infix':
        infixes.append((features, affix.get('position', '')))
    elif affixType == 'circumfix':
        circumfixes.append(features)
    else:  # suffix
        suffixes.append(features)

# Validate circumfix usage
if len(circumfixes) > 1:
    self.report.Error(_translate('CreateApertiumRules',
        'Word {wid} in rule {ruleName} has multiple circumfixes, which is not supported.').format(
        wid=wid, ruleName=ruleName))
    self.GetSection('section-rules').remove(ruleEl)
    return False

# Process affixes in order: prefixes, infixes, circumfix-prefix,
# suffixes, circumfix-suffix
for affix in prefixes:
    # ... existing processing logic ...

for affix, position in infixes:
    # ... new infix processing logic (see below) ...

if circumfixes:
    # Handle circumfix prefix part
    # ... new circumfix processing logic (see below) ...

for affix in suffixes:
    # ... existing processing logic ...

if circumfixes:
    # Handle circumfix suffix part
    # ... new circumfix processing logic (see below) ...
```

#### Change 2: Add infix handling

Infixes are tricky in Apertium because they need to be positioned within the stem. The approach:

```python
# Process infixes
for affix, position in infixes:
    # For now, infixes are treated similarly to prefixes but with
    # a comment noting they should be positioned within the stem.
    # Full infix positioning would require stem segmentation,
    # which is beyond current Apertium transfer capabilities.

    actionEl.append(ET.Comment(_translate('CreateApertiumRules',
        'WARNING: Infix positioning ({position}) not fully supported in Apertium transfer. '
        'Treating as prefix. Consider using Apertium morphological analyzer for proper infix handling.').format(
        position=position if position else 'unspecified')))

    # Process like a prefix but add a warning tag
    if len(affix) > 1:
        # ... multi-feature macro logic (same as prefix) ...
    else:
        # ... single feature logic (same as prefix) ...
```

#### Change 3: Add circumfix handling

Circumfixes are affixes that wrap around the stem (e.g., German "ge-...-t" for participles). In Apertium, these need to be split:

```python
# Handle circumfix
if circumfixes:
    affix = circumfixes[0]  # We validated there's only one

    # A circumfix needs to be split into prefix and suffix parts.
    # The feature determines both parts simultaneously.

    actionEl.append(ET.Comment(_translate('CreateApertiumRules',
        'Circumfix: prefix and suffix parts generated from same feature')))

    if len(affix) > 1:
        # Multi-feature circumfix
        # Get the macro that will determine the circumfix form
        spec = self.GetMultiFeatureMacro(cat, False, specList)

        # The variable contains the full circumfix tag
        # We need to split it into prefix and suffix
        actionEl.append(ET.Comment(_translate('CreateApertiumRules',
            'NOTE: Circumfix splitting requires runtime processing. '
            'Variable {varid} contains the full circumfix tag.').format(
            varid=spec.varid)))

        # For prefix part (inserted before stem processing)
        ET.SubElement(lu_prefix, 'var', n=spec.varid + '_pre')

        # For suffix part (inserted after stem processing)
        ET.SubElement(lu_suffix, 'var', n=spec.varid + '_suf')

    else:
        # Single feature circumfix
        # Similar logic but for single feature
        label, match, value, tgtDefault, ranking = affix[0]

        # Get tags for this circumfix
        tags = self.GetTags(FeatureSpec(wordCats[pos], label, True, value=value))

        if tags:
            tag = sorted(tags)[0][0]
            # Split the tag into prefix and suffix parts
            # Convention: circumfix tags contain a delimiter like "GE_T" -> "GE" + "T"
            parts = tag.split('_', 1) if '_' in tag else [tag[:len(tag)//2], tag[len(tag)//2:]]

            ET.SubElement(lu, 'lit-tag', v=parts[0])  # prefix part before stem
            # ... stem processing ...
            ET.SubElement(lu, 'lit-tag', v=parts[1])  # suffix part after stem
```

### 2.5 Apertium Transfer Code Generation

#### Example 1: Simple Infix

**Input Rule (XML):**
```xml
<Word id="1" category="v">
  <Affixes>
    <Affix type="infix" position="after-first-consonant">
      <Features>
        <Feature label="tense" match="1"/>
      </Features>
    </Affix>
  </Affixes>
</Word>
```

**Generated Apertium (excerpt):**
```xml
<out>
  <lu>
    <clip pos="1" side="tl" part="lem"/>
    <clip pos="1" side="tl" part="a_gram_cat"/>
    <!--WARNING: Infix positioning (after-first-consonant) not fully supported in Apertium transfer.
        Treating as prefix. Consider using Apertium morphological analyzer for proper infix handling.-->
    <clip pos="1" side="tl" part="a_tense_affixes"/>
  </lu>
</out>
```

#### Example 2: Circumfix

**Input Rule (XML):**
```xml
<Word id="1" category="v">
  <Affixes>
    <Affix type="circumfix">
      <Features>
        <Feature label="aspect" match="1"/>
      </Features>
    </Affix>
  </Affixes>
</Word>
```

**Generated Apertium (excerpt):**
```xml
<out>
  <lu>
    <!--Circumfix: prefix and suffix parts generated from same feature-->
    <lit-tag v="GE"/><!-- circumfix prefix part -->
    <clip pos="1" side="tl" part="lem"/>
    <clip pos="1" side="tl" part="a_gram_cat"/>
    <lit-tag v="T"/><!-- circumfix suffix part -->
  </lu>
</out>
```

### 2.6 Implementation Steps

1. **Update DTD files** (1 hour)
   - Modify main DTD: `/home/user/FLExTrans/Rule Assistant/FLExTransRuleGenerator.dtd`
   - Modify XMLmind DTD: `/home/user/FLExTrans/XXEaddon/FLExTransRuleGeneratorXMLmind/dtds/FLExTransRuleGenerator.dtd`
   - Update any documentation references

2. **Implement basic infix support** (3 hours)
   - Add infix detection in `ProcessRule()`
   - Generate appropriate warnings
   - Treat as prefix with documentation
   - Add infix-specific comments in generated transfer file

3. **Implement circumfix support** (4 hours)
   - Add circumfix detection
   - Implement tag splitting logic
   - Handle circumfix in tag generation
   - Generate appropriate transfer code with prefix and suffix parts

4. **Update GetAffixGlossesForFeature** (2 hours)
   - Ensure `Utils.getAffixGlossesForFeature()` properly retrieves infix/circumfix entries
   - Test with sample FLEx databases containing these affix types
   - Handle special tagging conventions for circumfixes

5. **Create example rules and test data** (4 hours)
   - Create sample FLEx project with infixes (e.g., Tagalog-like language)
   - Create sample FLEx project with circumfixes (e.g., German-like language)
   - Document expected behavior
   - Create test cases

6. **Integration and testing** (4 hours)
   - Test with Rule Assistant UI
   - Verify DTD validation works
   - Test generated transfer rules in Apertium
   - Create automated tests

### 2.7 Testing Requirements

#### Unit Tests
- `GetCategoryName()` with infix/circumfix affixes
- Affix type detection and categorization
- Circumfix tag splitting logic

#### Integration Tests
- Rule generation with infixes
- Rule generation with circumfixes
- Mixed affix types (prefix + infix + suffix)
- Error handling for multiple circumfixes

#### System Tests
- End-to-end workflow with infix example (Tagalog-inspired)
- End-to-end workflow with circumfix example (German-inspired)
- Apertium transfer processing with generated rules

### 2.8 Complexity Estimate

**High** - Requires DTD changes, code modifications, new logic for affix ordering, and special handling for circumfixes.

**Effort:** 18 hours
**Risk:** Medium-High
- DTD changes affect UI and validation
- Circumfix splitting may need refinement based on linguistic requirements
- Limited Apertium support for infix positioning within stems

### 2.9 Limitations and Future Work

**Current Limitations:**

1. **Infix positioning:** Apertium transfer rules cannot position infixes within stems based on phonological rules. The current implementation treats them as prefixes with documentation.

2. **Circumfix splitting:** The tag splitting convention (using underscore) may not work for all languages. May need language-specific configuration.

3. **Multiple circumfixes:** Not supported (validated and rejected).

**Future Enhancements:**

1. Integrate with Apertium morphological analyzer for proper infix handling
2. Add configurable circumfix splitting rules
3. Support for reduplication (partial or full)
4. Support for discontiguous affixes beyond simple circumfixes

---

## 3. Multi-Source Macro Reuse

### 3.1 Issue Overview

**Issue #661:** Multi-source macro reuse functionality is currently disabled

**Location:** `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py:314-326`

**Current State:**
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
            self.lemmaMacros[lookupKey] = MacroSpec(
                macro.get('n'), items[1], items[3:])
    '''
```

### 3.2 Root Cause Analysis

#### Background

The macro reuse feature was designed to avoid creating duplicate macros when multiple rules need the same lemma/affix transformation based on the same source categories.

Macros are tagged with a special attribute `c="FTM {varid} {code}"` where:
- `FTM` = "FLExTrans Macro" marker
- `{varid}` = the variable name used by the macro
- `{code}` = destination category + source categories

Example: `c="FTM v_adj_lemma_from_n-v adj n v"`

The lookup key is `(destCategory, tuple(sourceCats))` = `('adj', ('n', 'v'))`

#### Why It Was Disabled

1. **Variable name conflicts:** When reusing macros, the variable name from the existing macro might conflict with other uses or naming conventions in the newly generated rules.

2. **Incomplete macro matching:** The current lookup only checks destination category and source category sequence, but doesn't verify that the specific features being checked are identical.

3. **Macro content drift:** If a macro is hand-edited after generation, reusing it might produce incorrect results.

4. **Test failures:** The `ReuseMacro` test class (line 459 in `test_rule_assistant.py`) was failing, indicating functional problems.

### 3.3 Detailed Problem Analysis

#### Problem 1: Insufficient Lookup Key

The current lookup key `(destCategory, tuple(sourceCats))` doesn't account for:
- Which specific features are being checked
- The order/ranking of features
- Default values for features
- Whether features are from stems or affixes

Example of collision:
```python
# Macro 1: adj lemma from noun gender + verb tense
# Lookup key: ('adj', ('n', 'v'))

# Macro 2: adj lemma from noun number + verb aspect
# Lookup key: ('adj', ('n', 'v'))  # COLLISION!
```

Both would match the same lookup key but need different logic.

#### Problem 2: Variable Namespace Pollution

When reusing a macro, we need to ensure the variable name doesn't conflict with:
- Variables from other reused macros
- Variables created in the current generation session
- Hand-written variables in the transfer file

#### Problem 3: Macro Modification Detection

No mechanism exists to detect if a macro has been hand-modified, which could lead to incorrect behavior if the macro is reused.

### 3.4 Proposed Solution

#### Approach: Enhanced Lookup Key with Validation

**Phase 1: Improve the lookup key to include feature information**

```python
def GetMacroLookupKey(self, destCategory: str, isLemma: bool,
                      sources: list[FeatureSpec]) -> tuple:
    """Generate a comprehensive lookup key for macro reuse.

    The key includes:
    - Destination category
    - Macro type (lemma vs affix)
    - Source categories in order
    - Feature labels for each source
    - Whether features have defaults
    """
    catSequence = sorted(set([s.category for s in sources if not s.value]))

    # Create feature signature for each source category
    featuresByCategory = defaultdict(list)
    for spec in sources:
        if not spec.value:  # Only include features that vary
            featuresByCategory[spec.category].append(
                (spec.label, spec.isAffix, bool(spec.default), bool(spec.ranking))
            )

    # Sort features within each category for consistency
    for cat in featuresByCategory:
        featuresByCategory[cat].sort()

    # Build comprehensive key
    featureSignature = tuple(
        (cat, tuple(featuresByCategory[cat]))
        for cat in catSequence
    )

    return (destCategory, isLemma, featureSignature)
```

**Phase 2: Add macro validation before reuse**

```python
def ValidateMacroForReuse(self, macroElement: ET.Element,
                          expectedSpec: MacroSpec) -> bool:
    """Validate that an existing macro matches expected specification.

    Checks:
    - Macro has the expected FTM comment
    - Variable name hasn't been modified
    - Macro structure matches expected pattern
    """
    code = macroElement.get('c', '')
    if not code.startswith('FTM '):
        return False

    items = code.split()
    if len(items) < 3 or items[0] != 'FTM':
        return False

    # Validate variable name matches
    if items[1] != expectedSpec.varid:
        return False

    # Validate category sequence matches
    if len(items) < 3 + len(expectedSpec.catSequence):
        return False

    if items[2] != expectedSpec.macid.split('_')[1]:  # dest category
        return False

    macroCategories = items[3:]
    if sorted(macroCategories) != sorted(expectedSpec.catSequence):
        return False

    return True
```

**Phase 3: Implement safe macro reuse**

```python
def ProcessExistingTransferFile(self, fileName: str) -> None:
    """Load an existing transfer file."""
    # ... existing code ...

    for macro in self.root.findall('.//def-macro'):
        self.usedIDs.add(macro.get('n'))

        # Enhanced macro reuse with validation
        if code := macro.get('c'):
            items = code.split()
            if len(items) > 3 and items[0] == 'FTM':
                # Extract macro specification from comment
                varid = items[1]
                destCat = items[2]
                sourceCats = items[3:]

                # Build feature signature from macro content
                # This requires parsing the macro structure to determine
                # which features it checks
                featureSig = self.ExtractMacroFeatureSignature(macro, sourceCats)

                if featureSig:
                    lookupKey = (destCat, self.IsMacroForLemma(macro), featureSig)
                    self.lemmaMacros[lookupKey] = MacroSpec(
                        macro.get('n'), varid, list(sourceCats)
                    )

def ExtractMacroFeatureSignature(self, macro: ET.Element,
                                 sourceCats: list[str]) -> Optional[tuple]:
    """Extract the feature signature from a macro's structure.

    Analyzes the macro's <choose> statements to determine which
    features it checks and in what order.
    """
    # This is complex and requires analyzing the macro's XML structure
    # to reverse-engineer the feature checks

    # For MVP, return None to disable reuse if we can't verify
    # In full implementation, parse <clip> elements to extract
    # feature labels and reconstruct the signature

    return None  # Conservative: don't reuse if unsure
```

### 3.5 Alternative Solution: Simplified Macro Fingerprinting

A simpler approach that doesn't require full feature signature matching:

**Compute macro content hash:**

```python
def GetMacroFingerprint(self, macro: ET.Element) -> str:
    """Generate a fingerprint of macro content for reuse detection.

    Creates a hash of the macro's structure to detect duplicates.
    Excludes variable/macro names from the hash.
    """
    # Serialize macro content
    content = ET.tostring(macro, encoding='unicode')

    # Normalize by removing specific names
    content = re.sub(r'n="[^"]*"', 'n="VAR"', content)
    content = re.sub(r'pos="[^"]*"', 'pos="POS"', content)

    # Hash the normalized content
    import hashlib
    return hashlib.md5(content.encode()).hexdigest()

# During macro creation in GetMultiFeatureMacro:
fingerprint = self.GetMacroFingerprint(macro)
if fingerprint in self.macroFingerprints:
    # Reuse existing macro
    return self.macroFingerprints[fingerprint]
else:
    # Store fingerprint for future reuse
    self.macroFingerprints[fingerprint] = spec
```

### 3.6 Recommended Implementation Path

**Phase 1: Diagnostic and Testing (Recommended First Step)**

1. **Re-enable the existing code** (1 hour)
   - Uncomment lines 320-325
   - Run the `ReuseMacro` test
   - Document exact failure modes

2. **Analyze test failures** (2 hours)
   - Examine generated transfer file
   - Compare with expected output
   - Identify specific cases where reuse fails
   - Document the collision scenarios

3. **Create additional test cases** (2 hours)
   - Test cases for different feature combinations
   - Test cases for variable name conflicts
   - Test cases for macro modifications

**Phase 2: Implement Fix (Choose one approach based on Phase 1 findings)**

**Option A: Enhanced Lookup Key (More robust, more complex)**
- Implement `GetMacroLookupKey()` with feature signatures (4 hours)
- Update `ProcessExistingTransferFile()` to use enhanced key (2 hours)
- Update `GetMultiFeatureMacro()` to use enhanced key (2 hours)
- Testing and validation (3 hours)

**Option B: Macro Fingerprinting (Simpler, good enough)**
- Implement `GetMacroFingerprint()` (2 hours)
- Update `ProcessExistingTransferFile()` to compute fingerprints (2 hours)
- Update `GetMultiFeatureMacro()` to check fingerprints (2 hours)
- Testing and validation (3 hours)

**Phase 3: Integration and Documentation**

1. **Update tests** (2 hours)
   - Re-enable `ReuseMacro` test class
   - Verify all tests pass
   - Add new edge case tests

2. **Document limitations** (1 hour)
   - When macros can/cannot be reused
   - Manual intervention scenarios
   - Performance implications

3. **Performance testing** (2 hours)
   - Measure impact on large transfer files
   - Verify macro deduplication is working
   - Check memory usage with many macros

### 3.7 Implementation Steps

#### Step 1: Analysis Phase (5 hours)

1. Re-enable existing reuse code
2. Run `ReuseMacro` test with verbose output
3. Examine generated `reuse_macro.t1x` file
4. Compare with expected file in `/home/user/FLExTrans/Rule Assistant/reuse_macro.t1x`
5. Document specific failure scenarios
6. Determine root cause of each failure

#### Step 2: Fix Implementation (9-11 hours, depending on approach)

**For Fingerprinting Approach:**

1. Add `macroFingerprints` dict to `__init__()` (0.5 hours)
2. Implement `GetMacroFingerprint()` method (2 hours)
3. Update `ProcessExistingTransferFile()` (2 hours)
4. Update `GetMultiFeatureMacro()` (2 hours)
5. Test with simple cases (1.5 hours)
6. Test with complex cases (1 hour)

**For Enhanced Lookup Key Approach:**

1. Implement `GetMacroLookupKey()` (3 hours)
2. Implement `ExtractMacroFeatureSignature()` (4 hours)
3. Update `ProcessExistingTransferFile()` (1 hour)
4. Update `GetMultiFeatureMacro()` (1 hour)
5. Testing (2 hours)

#### Step 3: Testing and Documentation (5 hours)

1. Re-enable and update `ReuseMacro` test (1 hour)
2. Add edge case tests (2 hours)
3. Document behavior and limitations (1 hour)
4. Performance testing (1 hour)

### 3.8 Testing Requirements

#### Unit Tests

- `GetMacroFingerprint()` produces consistent hashes
- Identical macros produce identical fingerprints
- Variable name changes don't affect fingerprint
- Different macro logic produces different fingerprints

#### Integration Tests

- `ReuseMacro` test class (currently skipped at line 459)
- Multiple rules using same lemma macro
- Multiple rules using same affix macro
- Hand-modified macros not incorrectly reused
- Variable name conflicts properly handled

#### Regression Tests

- Existing tests still pass
- Performance not significantly degraded
- Generated transfer files still valid
- Macro count reduced when reuse is possible

### 3.9 Complexity Estimate

**Medium-High** - Requires careful analysis of existing failures, then implementation of robust reuse mechanism with proper validation.

**Effort:**
- Analysis: 5 hours
- Implementation (Fingerprinting): 9 hours
- Implementation (Enhanced Key): 11 hours
- Testing: 5 hours
- **Total: 19-21 hours**

**Risk:** Medium
- May discover deeper architectural issues during analysis
- Fingerprinting might have edge cases
- Performance impact on large files needs monitoring
- Backward compatibility with hand-modified transfer files

### 3.10 Success Criteria

1. `ReuseMacro` test passes consistently
2. Duplicate macros are detected and reused correctly
3. No false positives (different macros incorrectly identified as same)
4. No variable name conflicts
5. Performance improvement measurable on large projects (fewer macros generated)
6. Clear documentation of when reuse applies

---

## 4. Testing Strategy

### 4.1 Test Pyramid

```
                    /\
                   /  \
                  / E2E\
                 /------\
                /  Integ \
               /----------\
              /    Unit    \
             /--------------\
```

### 4.2 Unit Tests

**File:** `test_create_apertium_rules.py` (to be created)

```python
import unittest
from Dev.Lib.CreateApertiumRules import RuleGenerator

class TestGetCategoryName(unittest.TestCase):
    """Tests for GetCategoryName with affixes."""

    def test_category_with_no_affixes(self):
        """Test basic category without affixes."""
        # ... test implementation ...

    def test_category_with_single_affix(self):
        """Test category with one affix."""
        # ... test implementation ...

    def test_category_with_multiple_affixes(self):
        """Test category with multiple affixes generates permutations."""
        # ... test implementation ...

class TestProperNounDetection(unittest.TestCase):
    """Tests for proper noun capitalization handling."""

    def test_common_noun_not_proper(self):
        # ... test implementation ...

    def test_proper_noun_detected(self):
        # ... test implementation ...

class TestMacroReuse(unittest.TestCase):
    """Tests for macro reuse functionality."""

    def test_macro_fingerprint_generation(self):
        # ... test implementation ...

    def test_identical_macros_same_fingerprint(self):
        # ... test implementation ...

    def test_different_macros_different_fingerprint(self):
        # ... test implementation ...
```

### 4.3 Integration Tests

**File:** `test_rule_assistant.py` (existing, needs updates)

- Re-enable `ReuseMacro` test (line 459)
- Add tests for infix handling
- Add tests for circumfix handling
- Add tests for proper noun capitalization

### 4.4 End-to-End Tests

Create sample projects demonstrating each new feature:

1. **Infix Test Project:** Tagalog-inspired language
2. **Circumfix Test Project:** German-inspired language
3. **Proper Noun Test Project:** Mixed proper/common nouns
4. **Macro Reuse Test Project:** Multiple rules with shared transformations

### 4.5 Regression Testing

Run full existing test suite after each change:
```bash
cd /home/user/FLExTrans
python -m pytest test_rule_assistant.py -v
```

### 4.6 Manual Testing Checklist

- [ ] Generate rules with new affix types in UI
- [ ] Verify DTD validation in XMLmind
- [ ] Test generated transfer file in Apertium pipeline
- [ ] Test with real linguistic data
- [ ] Performance test with large rule sets
- [ ] Test backward compatibility with existing projects

---

## 5. Implementation Timeline

### 5.1 Recommended Sequence

The TODOs and features should be implemented in this order to minimize risk:

#### Phase 1: Low-Risk TODOs (1-2 weeks)

**Week 1:**
1. TODO #4: File mode validation (2.5 hours) - Day 1
2. TODO #2: Variable naming refactoring (2.5 hours) - Day 1-2
3. TODO #1: Affix tag generation (2.5 hours) - Day 2-3
4. Testing for Phase 1 (4 hours) - Day 3-4

**Week 2:**
5. TODO #3: Proper noun capitalization (5 hours) - Day 1-2
6. Testing and documentation (3 hours) - Day 2-3

**Deliverable:** All TODOs resolved, code cleaner, improved error handling

#### Phase 2: Infix/Circumfix Support (2-3 weeks)

**Week 3:**
1. DTD updates (1 hour) - Day 1
2. Basic infix support (3 hours) - Day 1-2
3. Basic circumfix support (4 hours) - Day 2-3
4. Unit tests (3 hours) - Day 3-4

**Week 4:**
5. Utils.py updates (2 hours) - Day 1
6. Example rules and test data (4 hours) - Day 1-2
7. Integration testing (4 hours) - Day 3-4

**Week 5:**
8. Documentation (3 hours) - Day 1
9. E2E testing (4 hours) - Day 1-2
10. Bug fixes and refinement (8 hours) - Day 3-5

**Deliverable:** Full infix/circumfix support with examples and documentation

#### Phase 3: Macro Reuse (2-3 weeks)

**Week 6:**
1. Analysis and diagnosis (5 hours) - Day 1-2
2. Design review based on findings (2 hours) - Day 2

**Week 7:**
3. Implementation (9-11 hours) - Day 1-3
4. Unit tests (3 hours) - Day 3-4
5. Integration tests (2 hours) - Day 4-5

**Week 8:**
6. Re-enable ReuseMacro test (1 hour) - Day 1
7. Performance testing (2 hours) - Day 1
8. Documentation (2 hours) - Day 2
9. Final review and cleanup (3 hours) - Day 2-3

**Deliverable:** Macro reuse re-enabled with robust deduplication

### 5.2 Effort Summary

| Item | Estimated Hours | Days (6hr) | Risk Level |
|------|----------------|-----------|------------|
| TODO #1: Affix tags | 2.5 | 0.5 | Low |
| TODO #2: Variable naming | 2.5 | 0.5 | Very Low |
| TODO #3: Proper nouns | 5.0 | 1.0 | Medium |
| TODO #4: File validation | 2.5 | 0.5 | Very Low |
| **Phase 1 Subtotal** | **12.5** | **2.5** | **Low** |
| | | | |
| Infix support | 7.0 | 1.5 | Medium |
| Circumfix support | 6.0 | 1.0 | Medium-High |
| Testing & examples | 8.0 | 1.5 | Medium |
| Documentation | 3.0 | 0.5 | Low |
| **Phase 2 Subtotal** | **24.0** | **4.5** | **Medium** |
| | | | |
| Macro reuse analysis | 5.0 | 1.0 | Low |
| Macro reuse implementation | 9.0 | 1.5 | Medium |
| Macro reuse testing | 5.0 | 1.0 | Medium |
| **Phase 3 Subtotal** | **19.0** | **3.5** | **Medium** |
| | | | |
| **Grand Total** | **55.5** | **10.5** | **Medium** |

### 5.3 Risk Mitigation

**High-Risk Items:**

1. **Circumfix support** - Complex splitting logic, language-specific behavior
   - Mitigation: Start with simple test cases, get linguistic expert review

2. **Macro reuse** - Unknown failure modes, potential performance issues
   - Mitigation: Thorough analysis phase before implementation, incremental approach

3. **Proper noun handling** - Language-specific POS systems vary
   - Mitigation: Make it configurable, test with multiple language pairs

**Dependencies:**

- Phase 2 and 3 can proceed in parallel after Phase 1
- Proper noun handling (TODO #3) could wait until after other TODOs
- Macro reuse benefits from affix tag fixes (TODO #1)

### 5.4 Milestones

**Milestone 1:** TODOs Complete (End of Week 2)
- All TODOs resolved
- Code quality improved
- Test coverage increased

**Milestone 2:** Affix Types Implemented (End of Week 5)
- DTD supports all affix types
- Code generates correct transfer rules
- Examples and documentation complete

**Milestone 3:** Macro Reuse Working (End of Week 8)
- Issue #661 resolved
- ReuseMacro test passing
- Performance validated

**Final Delivery:** Complete Implementation (End of Week 8)
- All features implemented and tested
- Documentation updated
- Ready for production use

---

## 6. Appendix

### 6.1 File Locations

**Source Code:**
- `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py` - Main implementation
- `/home/user/FLExTrans/Dev/Lib/Utils.py` - Utility functions

**DTD Files:**
- `/home/user/FLExTrans/Rule Assistant/FLExTransRuleGenerator.dtd` - Main DTD
- `/home/user/FLExTrans/XXEaddon/FLExTransRuleGeneratorXMLmind/dtds/FLExTransRuleGenerator.dtd` - XMLmind DTD

**Tests:**
- `/home/user/FLExTrans/test_rule_assistant.py` - Integration tests
- `/home/user/FLExTrans/Rule Assistant/reuse_macro.t1x` - Expected output for macro reuse test

### 6.2 Key Data Structures

**FeatureSpec:**
```python
@dataclasses.dataclass(frozen=True)
class FeatureSpec:
    category: str       # POS category
    label: str          # Feature name
    isAffix: bool       # True if this is an affix, False if stem feature
    value: Optional[str] = None      # Fixed value, if any
    default: Optional[str] = None    # Default value
    isSource: bool = False           # From source side?
    ranking: Optional[int] = None    # Priority ranking
```

**MacroSpec:**
```python
@dataclasses.dataclass
class MacroSpec:
    macid: str              # Macro name/ID
    varid: str              # Variable name
    catSequence: list[str]  # Ordered list of source categories
```

### 6.3 References

**Apertium Documentation:**
- Transfer rules: https://wiki.apertium.org/wiki/Transfer_rules
- Morphological analysis: https://wiki.apertium.org/wiki/Morphological_analysis

**FLEx Documentation:**
- Morph types: FLEx Help > Lexicon > Morphology
- Feature system: FLEx Help > Grammar > Features

**Issue Tracker:**
- Issue #661: Multi-source macro reuse problems
- Issue #1096: Affix attribute naming (resolved)

### 6.4 Contact and Review

For questions or clarifications on this implementation plan, contact:
- Project maintainer: rmlockwood (GitHub)
- Architecture review: [TBD]

---

**Document Version Control:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-22 | Claude Code | Initial comprehensive plan |

---

**End of Implementation Plan**
