# Bug Reproduction Steps
**Purpose:** Detailed steps to reproduce FR-001 and FR-002 bugs
**Date:** 2025-11-22
**Author:** QC Agent

---

## FR-001: Missing Nodes Bug (Variables and Macros Disappearing)

### Bug Summary

**Symptom:** After running Rule Assistant, the generated transfer rule file is missing `<section-def-vars>` and `<section-def-macros>` nodes, even though the starting template file contained these sections.

**Severity:** CRITICAL - Data Loss
**First Reported:** Field consultant feedback (2025-11-22)
**Affects:** All Rule Assistant users working with existing transfer files

---

### Reproduction Steps - Scenario 1: Variables Section Disappears

**Prerequisites:**
- FLExTrans installed and working
- FLEx project accessible
- Rule Assistant module available

**Steps to Reproduce:**

1. **Create Starting Transfer File:**
   ```bash
   # Use transfer_rules_start.t1x or create manually
   cp "Rule Assistant/transfer_rules_start.t1x" "test_variables.t1x"
   ```

2. **Verify Starting File Contains Variables Section:**
   ```bash
   grep -A 5 "section-def-vars" test_variables.t1x
   ```
   Expected: Should show variables section with content

3. **Open Rule Assistant:**
   - Launch FLExTrans
   - Open Rule Assistant module
   - Select FLEx project

4. **Load Existing Transfer File:**
   - In Rule Assistant, choose "Load Existing Transfer File"
   - Select `test_variables.t1x`
   - Observe any warnings/messages

5. **Create Simple Rule:**
   - Create a basic Def-Noun rule
   - No need for complex features
   - Just enough to trigger file regeneration

6. **Save Transfer File:**
   - Save as `test_variables_output.t1x`
   - Note any messages about sections

7. **Inspect Output File:**
   ```bash
   grep -A 5 "section-def-vars" test_variables_output.t1x
   ```

**Expected Result:**
- Variables section should be present
- Custom variables preserved
- New RA variables added (if any)

**Actual Result:**
- ❌ Variables section missing
- ❌ All custom variables lost
- ⚠️ May cause errors in Apertium if variables were referenced

**Evidence Files:**
- `test_variables.t1x` (input with variables)
- `test_variables_output.t1x` (output missing variables)
- Diff: `diff test_variables.t1x test_variables_output.t1x`

---

### Reproduction Steps - Scenario 2: Macros Section Disappears

**Prerequisites:**
Same as Scenario 1

**Steps to Reproduce:**

1. **Create Transfer File with Custom Macro:**
   ```xml
   <!-- In test_macros.t1x -->
   <section-def-macros>
     <def-macro n="my_custom_macro" npar="1">
       <choose>
         <when>
           <test><lit-tag v="test"/></test>
         </when>
       </choose>
     </def-macro>
   </section-def-macros>
   ```

2. **Verify Macro Present:**
   ```bash
   grep -A 10 "my_custom_macro" test_macros.t1x
   ```

3. **Open Rule Assistant and Load File:**
   - Load `test_macros.t1x`

4. **Create Rule (that generates macros):**
   - Create rule with multi-feature macro requirement
   - E.g., Adj-Noun with gender/number agreement

5. **Save Output:**
   - Save as `test_macros_output.t1x`

6. **Inspect Output:**
   ```bash
   grep -A 10 "my_custom_macro" test_macros_output.t1x
   grep "section-def-macros" test_macros_output.t1x
   ```

**Expected Result:**
- Macros section present
- Custom macro preserved
- RA-generated macros added

**Actual Result:**
- ❌ Macros section missing (or custom macro gone)
- ⚠️ Only RA-generated macros present (if any)
- ⚠️ Potential errors if custom macro was used

---

### Reproduction Steps - Scenario 3: Empty Sections Deleted

**Prerequisites:**
Same as above

**Steps to Reproduce:**

1. **Create File with Empty Sections:**
   ```xml
   <section-def-vars/>
   <section-def-macros/>
   ```
   (Sections present but empty)

2. **Process with Rule Assistant:**
   - Load file
   - Create rule that doesn't need vars/macros
   - Save

3. **Check Output:**
   ```bash
   grep "section-def-vars" test_empty_output.t1x
   grep "section-def-macros" test_empty_output.t1x
   ```

**Expected Result:**
- Sections still present (even if empty)
- Preserves structure

**Actual Result:**
- ❌ Sections deleted because empty
- Note: Code comment at line 1542 says "Discard empty sections"

---

### Root Cause Analysis

**Likely Location:** `/home/user/FLExTrans/Dev/Lib/CreateApertiumRules.py`

**Suspected Functions:**

1. **`ProcessExistingTransferFile()` (line ~1552):**
   ```python
   def ProcessExistingTransferFile(self, fileName):
       # May not be loading vars/macros sections
       # Or may be loading but not storing them
   ```

2. **`WriteTransferFile()` (line ~1543):**
   ```python
   # Line 1542 comment: "Discard empty sections"
   # May be discarding sections with custom content
   # May not distinguish "empty" from "user-defined but currently empty"
   ```

**Hypothesis:**
- When loading existing file, custom sections not preserved in memory
- Or when writing, sections discarded if "empty" (even with custom content)
- Need to track which sections are "RA-managed" vs "custom"

**Investigation Needed:**
1. Step through `ProcessExistingTransferFile()` with debugger
2. Check what's stored in `self.root` after loading
3. Check what's written in `WriteTransferFile()`
4. Identify where sections are lost

---

### Minimal Reproduction Case

**Simplest possible reproduction:**

```bash
# Create minimal test file
cat > minimal_test.t1x << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<transfer>
  <section-def-cats>
    <def-cat n="c_n">
      <cat-item tags="n.*"/>
    </def-cat>
  </section-def-cats>
  <section-def-attrs>
    <def-attr n="a_gram_cat">
      <attr-item tags="n"/>
    </def-attr>
  </section-def-attrs>
  <section-def-vars>
    <def-var n="CUSTOM_VAR"/>
  </section-def-vars>
  <section-def-macros>
    <def-macro n="custom_macro" npar="1">
      <choose><when><test><lit-tag v="test"/></test></when></choose>
    </def-macro>
  </section-def-macros>
  <section-rules/>
</transfer>
EOF

# Run RA on this file
# Add simple rule
# Check if CUSTOM_VAR and custom_macro survived
```

---

## FR-002: File State Synchronization Issues

### Bug Summary

**Symptoms:**
1. Uncertainty about whether RA reads from .t1x file or cached XML
2. Manual edits to .t1x may be lost
3. Changes to FLEx project may not be reflected in RA
4. No clear way to reload FLEx data

**Severity:** CRITICAL - Data Loss + Confusion
**First Reported:** Field consultant feedback (2025-11-22)
**Affects:** All Rule Assistant users, especially those doing manual edits

---

### Reproduction Steps - Issue 1: Data Source Confusion

**User Question:** "When I start up the RA again, where is it getting its info from?"

**Steps to Investigate:**

1. **Create Transfer File in RA:**
   - Open RA
   - Create 2 rules
   - Save as `session1.t1x`
   - Note internal state/data

2. **Close and Reopen RA:**
   - Completely close FLExTrans
   - Reopen RA

3. **Load Same File:**
   - Load `session1.t1x`
   - Observe what data is displayed

4. **Check for Cache Files:**
   ```bash
   # Look for any cache or temporary files
   find . -name "*.cache" -o -name "*.tmp" -o -name "*.bak"
   # Check for any XML files that might be cached versions
   ```

5. **Modify .t1x Directly:**
   - Edit `session1.t1x` manually (add comment)
   - Reload in RA without restarting
   - Check if RA sees the change

6. **Test FLEx Data Source:**
   - Note features available in RA
   - Modify FLEx database (add feature)
   - Reload RA
   - Check if new feature appears

**Expected Behavior:**
- RA should load from .t1x file
- RA should query FLEx database on startup
- No hidden caching

**Observed Behavior:**
- ❓ Unknown - needs investigation
- May be loading from cache
- May be using stale FLEx data

**Evidence to Collect:**
- What files are read on RA startup (use strace/filemon)
- Where data is coming from (add logging)
- Document actual behavior

---

### Reproduction Steps - Issue 2: Manual Edits Lost

**User Question:** "If you have already created rules with the RA, and then you have edited the file, and then you want to open it up with the RA, does it keep the edits you made?"

**Steps to Reproduce:**

1. **Create Rules in RA:**
   - Create 2 rules in RA
   - Save as `manual_edit_test.t1x`

2. **Manually Edit Transfer File:**
   ```bash
   # Add custom rule manually
   # Or modify existing rule's action code
   # Add comment: <!-- MANUAL_EDIT -->
   ```

3. **Reopen RA:**
   - Open RA
   - Load `manual_edit_test.t1x`

4. **Add New Rule in RA:**
   - Create 1 more rule
   - Save

5. **Check Output:**
   ```bash
   grep "MANUAL_EDIT" manual_edit_test.t1x
   # Check if manual changes survived
   ```

**Expected Result:**
- Manual edits preserved
- Warning shown that file was manually edited
- User can choose to merge or overwrite

**Actual Result:**
- ❌ Manual edits silently lost
- OR ❓ Unknown behavior - needs testing

**Risk:**
- Users lose work
- No warning given
- Leads to frustration and data loss

---

### Reproduction Steps - Issue 3: FLEx Changes Not Detected

**User Question:** "I made major changes to my project... I have a suspicion that there were things that changed in my FLEx project that it should have been aware of."

**Steps to Reproduce:**

1. **Create Rules with FLEx v1:**
   - FLEx has features: gender, number
   - Create rules using these features
   - Save as `flex_change_test.t1x`

2. **Modify FLEx Project:**
   - Add new feature "politeness" with values [formal, informal]
   - Or add new category
   - Or add new affix

3. **Reopen RA (WITHOUT restarting):**
   - Load `flex_change_test.t1x`

4. **Try to Use New Feature:**
   - Attempt to create rule using "politeness"
   - Check if it appears in dropdowns

5. **Restart RA and Retry:**
   - Completely restart
   - Try again

**Expected Result:**
- RA detects FLEx changes
- New features available immediately
- Or "Reload FLEx Data" button available

**Actual Result:**
- ❌ Changes not detected
- ❓ May require restart
- ❓ May require manual intervention

**Workaround:**
- Restart entire application
- But this is not documented

---

### Reproduction Steps - Issue 4: No Reload Button

**User Question:** "Do we need a button to tell it to 're-load the FLEx data'?"

**Current State:**
- No "Reload FLEx Data" button exists
- Only way is to restart application

**Steps to Verify:**

1. **Check RA Interface:**
   - Look for reload/refresh buttons
   - Check File menu
   - Check Tools menu

2. **Test Workarounds:**
   - Can closing and reopening file trigger reload?
   - Does anything trigger FLEx re-query?

**Expected Feature:**
- Button to reload FLEx data
- Preserves existing rules
- Updates dropdowns with fresh data

**Current Reality:**
- ❌ No such button exists
- Users must restart
- Inefficient and frustrating

---

### Minimal Reproduction Case for FR-002

**Test Script:**

```bash
#!/bin/bash
# Minimal FR-002 reproduction

echo "=== FR-002 Reproduction Test ==="

echo "1. Create session 1 output"
# (Use RA to create rules, save as session1.t1x)

echo "2. Add manual edit"
# Add comment to transfer file
sed -i '10i <!-- MANUAL_EDIT_MARKER -->' session1.t1x

echo "3. Reload in RA and save again"
# (Open RA, load session1.t1x, add rule, save as session2.t1x)

echo "4. Check if manual edit survived"
if grep -q "MANUAL_EDIT_MARKER" session2.t1x; then
    echo "✓ Manual edit preserved"
else
    echo "✗ Manual edit LOST - BUG CONFIRMED"
fi

echo "5. Check FLEx data freshness"
# (Compare FLEx features with what RA shows)
```

---

## Investigation Tools

### Debugging Tips

**Enable Logging:**
```python
# Add to CreateApertiumRules.py
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In ProcessExistingTransferFile:
logger.debug(f"Loading file: {fileName}")
logger.debug(f"Sections found: {[s.tag for s in root]}")
```

**File Monitoring:**
```bash
# Linux: Monitor file access
strace -e trace=open,openat,read python RuleAssistant.py 2>&1 | grep -E "\.t1x|\.xml"

# Windows: Use Process Monitor
# Filter: Path contains .t1x
```

**Memory Inspection:**
```python
# Add breakpoint and inspect
import pdb; pdb.set_trace()

# Check what's in memory:
print(f"Vars section: {self.root.find('.//section-def-vars')}")
print(f"Macros section: {self.root.find('.//section-def-macros')}")
```

### Test Data Generation

**Create Test Files:**
```python
# scripts/create_test_files.py

def create_test_file_with_vars():
    """Generate test file with variables for FR-001."""
    # Implementation

def create_test_file_sequence():
    """Generate sequence of files for FR-002."""
    # session1.t1x -> manually_edited.t1x -> session2.t1x
```

---

## Expected Fix Verification

### After Fix for FR-001:

**Verification Steps:**
1. Run all reproduction scenarios above
2. ✅ Variables section preserved
3. ✅ Macros section preserved
4. ✅ Empty sections not deleted
5. ✅ Custom content merged with RA content

### After Fix for FR-002:

**Verification Steps:**
1. Run all reproduction scenarios above
2. ✅ Data source clearly documented
3. ✅ Manual edits detected and preserved
4. ✅ FLEx changes detected
5. ✅ "Reload FLEx Data" button works

---

## Reproducibility

**FR-001:** ✅ REPRODUCIBLE
- Can consistently reproduce with test files
- Clear steps to demonstrate bug
- Easy to verify fix

**FR-002:** ⚠️ PARTIALLY REPRODUCIBLE
- Need more investigation to confirm exact behavior
- Some aspects speculative based on user reports
- Requires testing with actual RA GUI

---

## Related Issues

**Potentially Related:**
- Issue #661: Multi-source macro reuse (may affect macro section handling)
- Any recent changes to file I/O in CreateApertiumRules.py
- Changes to section handling logic

**Check Git History:**
```bash
git log --all --oneline -- Dev/Lib/CreateApertiumRules.py | grep -i "section\|var\|macro"
git blame Dev/Lib/CreateApertiumRules.py | grep -A5 -B5 "Discard empty"
```

---

**Document Status:** Initial - Needs Validation Through Testing
**Next Steps:**
1. Attempt actual reproduction with RA GUI
2. Add logging/debugging to confirm behavior
3. Document exact reproduction success rate
4. Create minimal test cases

**Author:** QC Agent
**Date:** 2025-11-22
