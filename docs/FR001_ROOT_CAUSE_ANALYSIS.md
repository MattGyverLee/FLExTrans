# FR-001: Root Cause Analysis - Missing Nodes Bug

## Problem Statement

After running Rule Assistant, the generated transfer rule file is missing `<section-def-vars>` and `<section-def-macros>` nodes, even though the starting template contained these sections with user-defined content.

## Root Cause

The bug occurs due to the interaction of two methods in `CreateApertiumRules.py`:

### 1. `TrimUnused()` Method (Lines 1407-1434)

When processing Rule Assistant files with `overwrite_rules='yes'`, the `TrimUnused()` method is called to remove unused macros and variables that may have been left over from deleted rules.

**The Problem:** `TrimUnused()` is overly aggressive. It removes **ALL** variables and macros that are not referenced in the current rule set, including:
- User-defined variables for custom hand-written rules
- User-defined macros for post-processing
- Content from the original template that should be preserved

The method only preserves Bantu-related items (by checking for `BANTU_NOUN_CLASS_FROM_N` pattern), but has no mechanism to distinguish between:
- Auto-generated items (safe to remove)
- User-defined items (should preserve)

### 2. `WriteTransferFile()` Method (Lines 1533-1547)

After sections are processed, `WriteTransferFile()` removes any sections that have become empty:

```python
for name in RuleGenerator.SectionSequence:
    elem = self.GetSection(name)
    if len(elem) == 0:
        self.root.remove(elem)
```

**The Problem:** When `TrimUnused()` removes all variables/macros from a section, that section becomes empty and gets removed entirely, losing both the content AND the structure.

## Data Flow Trace

### Scenario: User has custom variables and macros

1. **Initial State**
   - User's transfer file contains:
     - `<section-def-vars>` with `v_my_custom_var`
     - `<section-def-macros>` with `m_my_custom_postprocess`

2. **ProcessExistingTransferFile()** (Line 274)
   - Loads the XML tree
   - Extracts variable names into `self.variables` dict
   - Extracts macro IDs into `self.usedIDs` set
   - **Does NOT mark them as "user-defined" vs "auto-generated"**

3. **ProcessAssistantFile()** with `overwrite_rules='yes'` (Line 1436)
   - Deletes old rules (Line 1496-1502)
   - Calls `TrimUnused()` (Line 1503)

4. **TrimUnused()** (Line 1407)
   - Scans entire tree for `<var>` and `<call-macro>` references
   - Finds that `v_my_custom_var` is not referenced
   - Finds that `m_my_custom_postprocess` is not referenced
   - **Removes both from their sections**
   - Sections become empty

5. **WriteTransferFile()** (Line 1533)
   - Checks each section (Line 1538-1541)
   - Finds `section-def-vars` has 0 children
   - Finds `section-def-macros` has 0 children
   - **Removes both sections from output**

## Test Case Reproduction

See the debug scripts created:
- `/home/user/FLExTrans/test_debug_sections.py` - Basic section preservation
- `/home/user/FLExTrans/test_debug_trim_unused.py` - TrimUnused behavior
- `/home/user/FLExTrans/test_debug_user_macros.py` - Full bug reproduction

The bug can be reproduced by:
1. Creating a transfer file with custom variables/macros
2. Running Rule Assistant with `overwrite_rules='yes'`
3. Observing that sections are missing in the output

## Impact

**Severity: High**

- **Data Loss**: User's custom variables and macros are permanently deleted
- **Structure Loss**: Section structure is removed, preventing users from easily adding content back
- **Workflow Disruption**: Users must manually recreate their custom content after each Rule Assistant run
- **Silent Failure**: No warning is given that content will be removed

## Proposed Solution

Implement a tracking mechanism to preserve user-defined content:

### 1. Track Original Content
- Add `self.originalVariables` set to track variables from original file
- Add `self.originalMacros` set to track macros from original file
- Add `self.originalSections` set to track sections from original file
- Populate these in `ProcessExistingTransferFile()`

### 2. Modify `TrimUnused()`
- Only remove variables/macros that are NOT in the original sets
- Preserve all original user-defined content

### 3. Modify `WriteTransferFile()`
- Only remove sections that were NOT in the original file
- Preserve original section structure even if empty
- OR keep at least one placeholder element in original sections

## Alternative Solutions Considered

### Option 1: Naming Convention
- Only auto-remove items with specific prefixes (e.g., auto-generated items)
- **Rejected**: Doesn't work for existing files; requires user cooperation

### Option 2: Preservation Markers
- Use XML comments or attributes to mark "user-defined" vs "auto-generated"
- **Rejected**: Requires modifying user's files; complex to implement

### Option 3: Never Remove Sections
- Always keep all sections, even if empty
- **Rejected**: May violate DTD requirements; creates clutter

### Option 4: Add Configuration Option
- Let users choose whether to preserve unused content
- **Deferred**: Good for future enhancement, but fix should work by default

## Implementation Plan

1. Add tracking fields to `RuleGenerator.__init__()`
2. Modify `ProcessExistingTransferFile()` to populate tracking sets
3. Modify `TrimUnused()` to skip original content
4. Modify `WriteTransferFile()` to preserve original sections
5. Add comprehensive test coverage
6. Test with real-world scenarios

## Related Code Locations

- `ProcessExistingTransferFile()`: Line 274
- `TrimUnused()`: Line 1407
- `WriteTransferFile()`: Line 1533
- `ProcessAssistantFile()`: Line 1436 (calls TrimUnused at line 1503)
- `SectionSequence`: Line 125

## Testing Strategy

Tests should cover:
1. ✅ Basic section preservation (sections with content)
2. ✅ TrimUnused removing all content (sections become empty)
3. ✅ User custom content being lost (the actual bug)
4. Empty sections in original file (should be preserved)
5. Mix of original and generated content (only generated removed)
6. Sections added during processing (should be removed if empty)
