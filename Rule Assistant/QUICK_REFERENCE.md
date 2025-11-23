# Rule Assistant Quick Reference
**For Field Consultants and Linguists**

This guide answers common questions about how Rule Assistant works with your files and data.

---

## Table of Contents
1. [Starting Fresh](#starting-fresh)
2. [Working with Existing Files](#working-with-existing-files)
3. [What Files Does Rule Assistant Use?](#what-files-does-rule-assistant-use)
4. [Manual Edits - Will They Be Lost?](#manual-edits---will-they-be-lost)
5. [FLEx Changes - Are They Detected?](#flex-changes---are-they-detected)
6. [Module Order - What to Run First?](#module-order---what-to-run-first)
7. [Troubleshooting](#troubleshooting)

---

## Starting Fresh

**Q: How do I start a new Rule Assistant project without Swedish/other language data?**

**A: Use the clean templates!**

1. Go to `Rule Assistant/templates/`
2. Copy `minimal_template.t1x` to your project's rule file location
3. Or use the reset script:
   - Windows: `reset_to_template.bat`
   - Mac/Linux: `./reset_to_template.sh`

The templates have NO language-specific data - completely clean.

**Q: Do I need to pre-populate attributes?**

**A: YES** - Run "Set Up Transfer Rule Categories and Attributes" FIRST

This module:
- Reads your FLEx project (categories, features, affixes)
- Populates the `<section-def-cats>` and `<section-def-attrs>` sections
- Must run before Rule Assistant can work

**Workflow for fresh start:**
```
1. Copy minimal_template.t1x → transfer_rules.t1x
2. Run "Set Up Transfer Rule Categories and Attributes"
3. Run "Rule Assistant"
4. Create your rules
5. Save
```

---

## Working with Existing Files

**Q: When I open Rule Assistant with an existing transfer file, what happens?**

**A:** Rule Assistant:
- ✅ Loads your existing rule tree from `RuleAssistantRules.xml`
- ✅ Refreshes FLEx data from database (always current)
- ✅ Displays your rules in the GUI
- ⚠️ May overwrite `transfer_rules.t1x` when you save (see below)

**Q: Do my existing rules get displayed in the GUI?**

**A:** Your rule **specifications** are saved in `RuleAssistantRules.xml` and will appear in the tree.

However, **manually written rules** in `transfer_rules.t1x` are NOT displayed in the GUI. The GUI only shows rules created through Rule Assistant.

**Q: When I save, does it add to my existing file or overwrite it?**

**A:** It depends on the `overwrite_rules` setting in your Rule Assistant file:

- **`overwrite_rules="yes"`**: Regenerates entire sections, may lose manual edits
- **`overwrite_rules="no"`** (default): Adds rules, preserves more existing content

**Important:** Rule Assistant always backs up your file before modifying it (timestamped `.bak` file).

---

## What Files Does Rule Assistant Use?

| File | Purpose | Lifetime | Editable? |
|------|---------|----------|-----------|
| **FLEx Database** (Source) | Categories, features, affixes | Permanent | Via FLEx only |
| **FLEx Database** (Target) | Categories, features, affixes | Permanent | Via FLEx only |
| **RuleAssistantGUIinput.xml** | FLEx data for GUI | Temporary (regenerated) | No - auto-generated |
| **RuleAssistantRules.xml** | Your rule tree | Permanent | Via GUI or carefully by hand |
| **transfer_rules.t1x** | Generated Apertium rules | Permanent | ⚠️ Risky - see below |
| **Test data files** (.html) | Preview display | Temporary | No - auto-generated |

### File Details

**RuleAssistantRules.xml** - Your Rule Tree
- Where: Build folder (e.g., `C:\MyProject\Build\RuleAssistantRules.xml`)
- Contains: High-level rule specifications
- Persists: Between sessions
- Safe to edit: Yes, if you understand the schema
- Read by: Rule Assistant GUI

**transfer_rules.t1x** - Generated Output
- Where: Project folder or configured location
- Contains: Low-level Apertium transfer rules
- Persists: Yes, but regenerated when you save
- Safe to edit: ⚠️ RISKY - may be overwritten

**RuleAssistantGUIinput.xml** - Temporary
- Where: Build folder
- Contains: FLEx data snapshot for GUI
- Persists: No - regenerated every time
- Safe to edit: No point - it's regenerated

---

## Manual Edits - Will They Be Lost?

### Editing RuleAssistantRules.xml
✅ **Safe** - This is the source of truth for your rule tree
- Rule Assistant reads this file
- Your edits will appear in the GUI
- Must follow XML schema

### Editing transfer_rules.t1x
⚠️ **RISKY** - This is generated output

**What gets preserved:**
- Rules NOT created by Rule Assistant (if `overwrite_rules="no"`)
- Some sections like Variables and Macros (with recent fixes)
- Comments in hand-written rules

**What gets lost:**
- Rules with `comment` attributes matching Rule Assistant rules (overwritten)
- Sections that Rule Assistant regenerates
- Hand-edits to Rule Assistant-generated rules

**Best Practice:**
1. Use Rule Assistant for most rules
2. Add hand-written rules with unique comments
3. Set `overwrite_rules="no"` to preserve more
4. Always keep backups (Rule Assistant creates them automatically)

### Mixed Workflow Recommendation

If you need both GUI and manual editing:

```
1. Create basic rules in Rule Assistant → save
2. Manually add advanced rules to transfer_rules.t1x
3. Give manual rules unique comment= attributes
4. Set overwrite_rules="no" in Rule Assistant XML
5. When you edit in Rule Assistant, it adds rules without deleting yours
```

---

## FLEx Changes - Are They Detected?

**Q: If I add features to my FLEx project, will Rule Assistant see them?**

**A: YES - immediately on the next run**

FLEx data is ALWAYS re-read from the database. There is NO caching.

When you run Rule Assistant:
1. It queries your FLEx database
2. Extracts current categories, features, affixes
3. Writes to RuleAssistantGUIinput.xml (temporary)
4. GUI displays the fresh data

**No "reload" button needed** - just close and reopen Rule Assistant.

**Q: But my rule tree still shows old features?**

**A:** The rule **tree** (your saved rules) persists in RuleAssistantRules.xml.

If you:
- Delete a feature from FLEx
- Have rules using that feature

Then Rule Assistant will warn you about missing features, but won't delete your rules automatically.

---

## Module Order - What to Run First?

### First Time Setup

```
1. [Optional] Copy clean template → transfer_rules.t1x
2. "Set Up Transfer Rule Categories and Attributes" ← REQUIRED
3. "Rule Assistant"
```

### After Making FLEx Changes

```
1. "Set Up Transfer Rule Categories and Attributes" (updates attributes)
2. "Rule Assistant" (FLEx data auto-refreshed)
```

### For Testing Rules

```
1. "Rule Assistant" (create/edit rules)
2. "Run Apertium" (optional - provides test data preview in Rule Assistant)
3. "Rule Assistant" again (to see test data)
```

### Do I need to run "Run Apertium" before Rule Assistant?

**Optional** - it helps but isn't required.

- **Without "Run Apertium"**: Rule Assistant works fine, but no test data preview
- **With "Run Apertium"**: You get an HTML preview showing how rules transform sample text

---

## Troubleshooting

### "My variables and macros disappeared!"

**Cause:** Bug in older versions (FR-001)
**Fix:** Update to latest version with FR-001 fix
**Recovery:** Check for `.bak` backup files in same directory

### "Rule Assistant shows blank tree but I had rules!"

**Possible causes:**
1. Wrong `RuleAssistantRules.xml` file being read
   - Check: Build folder location
   - Check: Configuration settings

2. File got corrupted
   - Check: `.bak` backups
   - Restore from backup

### "Warning about BantuNounClass feature not found"

**Meaning:** You're using disjoint feature sets but attributes aren't populated

**Fix:**
1. Run "Set Up Transfer Rule Categories and Attributes"
2. This creates the attribute definition in transfer_rules.t1x
3. Re-run Rule Assistant

**Note:** "BantuNounClass" is an *attribute* in the transfer file, not a FLEx feature.

### "File has been edited" error when running pre-populate"

**Cause:** Over-sensitive file detection (FR-003)

**What to do:**
- Ignore the warning if the module still works
- The module adds categories/attributes correctly despite the message
- It's a false positive being investigated

### "My manual edits to transfer_rules.t1x were lost"

**Prevention:**
1. Always check `.bak` backup files first
2. Set `overwrite_rules="no"` in your Rule Assistant XML
3. Use unique `comment=` attributes for manual rules
4. Consider using version control (git) for critical files

**Recovery:**
1. Look for `.bak` files with timestamps
2. Restore the most recent backup
3. Re-apply only the Rule Assistant changes

---

## Quick Tips

### ✅ Do:
- Use clean templates for new projects
- Run "Set Up Transfer Rule Categories and Attributes" first
- Let Rule Assistant back up files automatically
- Keep additional backups of important manual edits
- Use unique comment attributes for manual rules
- Test after making changes

### ❌ Don't:
- Mix language-specific templates from different projects
- Edit RuleAssistantGUIinput.xml (it's regenerated)
- Assume transfer_rules.t1x edits will persist
- Skip the "Set Up..." module
- Delete `.bak` backup files immediately

---

## File Locations

Default locations (may vary by configuration):

```
Project Folder/
  ├── transfer_rules.t1x          (Generated rules)
  ├── transfer_rules.t1x.backup_* (Automatic backups)
  └── Build/
      ├── RuleAssistantRules.xml      (Your rule tree - IMPORTANT!)
      ├── RuleAssistantGUIinput.xml   (Temporary FLEx data)
      └── RuleAssistantTestData*.html (Preview files)
```

---

## Getting Help

**Documentation:**
- `/docs/RULE_ASSISTANT_USER_GUIDE.md` - Complete user guide
- `/docs/RuleAssistant_Feature_Requests.md` - Known issues and planned features
- `Rule Assistant/templates/README.md` - Template usage

**Code Documentation:**
- See comments in `RuleAssistant.py` MainFunction() for technical details
- See comments in `CreateApertiumRules.py` for rule generation logic

**Support:**
- Report bugs: https://github.com/MattGyverLee/FLExTrans/issues
- Ask questions on FLExTrans forum

---

**Last Updated:** 2025-11-22
**Version:** 1.0 - Addresses consultant wish list items
