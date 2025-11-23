# Rule Assistant User Guide

**Version:** 1.0
**Date:** 2025-11-22
**Audience:** Linguists and Translation Consultants
**FLExTrans Version:** 3.14+

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Working with Existing Transfer Files](#working-with-existing-transfer-files)
4. [Understanding Disjoint Feature Sets (Bantu Noun Classes)](#understanding-disjoint-feature-sets-bantu-noun-classes)
5. [Module Prerequisites and Workflow](#module-prerequisites-and-workflow)
6. [Advanced Topics](#advanced-topics)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)
9. [Quick Reference](#quick-reference)

---

## Introduction

### What is the Rule Assistant?

The Rule Assistant is a graphical tool that helps you create Apertium transfer rules for machine translation without writing code directly. Instead of manually editing complex XML, you can:

- Specify rules in a linguist-friendly format
- Let the system generate the complex Apertium code automatically
- Focus on linguistic patterns rather than programming syntax

### How Does It Work?

```
Your Input                    Rule Assistant            Final Output
(Simple XML)                  (Generates)              (Complex XML)

┌──────────────┐            ┌──────────┐            ┌──────────────┐
│ Rule Spec:   │            │          │            │ Apertium     │
│ DET + NOUN   │──────────▶ │   Rule   │──────────▶ │ Transfer     │
│ → NOUN + DET │            │ Assistant│            │ Rules        │
│              │            │          │            │              │
└──────────────┘            └──────────┘            └──────────────┘

 Simple pattern                Handles                Complex
 Easy to edit                  complexity             Executable
```

### What You'll Learn

This guide will teach you:

✓ How to start a new Rule Assistant project
✓ How to work with existing transfer files safely
✓ How to handle advanced features like Bantu noun classes
✓ Which modules to run and when
✓ How to troubleshoot common problems
✓ Best practices for combining GUI and manual editing

---

## Getting Started

### Prerequisites

Before using the Rule Assistant, you need:

1. **FLEx Projects:** Both source and target language projects set up in FLEx
2. **Linguistic Data:** Categories (parts of speech), features (gender, number, etc.), and affixes defined in FLEx
3. **FLExTrans Installed:** The FLExTrans toolkit installed and configured

### Your First Rule: Step by Step

#### Step 1: Run "Set Up Transfer Rule Categories and Attributes"

**Purpose:** This module creates the basic structure your transfer file needs.

**What it does:**
- Queries your FLEx projects for categories (like noun, verb, adjective)
- Queries for features (like gender, number, case)
- Creates the `<section-def-cats>` and `<section-def-attrs>` sections
- Sets up the foundation for your transfer rules

**How to run it:**
1. In FLExTrans, go to the Modules menu
2. Select "Set Up Transfer Rule Categories and Attributes"
3. Choose your source and target FLEx projects
4. Specify where to save the transfer rule file (e.g., `transfer_rules.t1x`)
5. Click Run

**What you'll see:**
```
Processing...
Created 25 categories
Created 45 attributes
Transfer rule file created: C:\MyProject\transfer_rules.t1x
```

**Do you need to run this?**
- **YES, always** if starting a new project
- **YES** if you've added new categories or features to FLEx
- **NO** if you're just adding more rules to an existing file

#### Step 2: Create Your Rule Specification

**Purpose:** Define your first rule in linguist-friendly format.

**Example:** English "the book" → Spanish "el libro"

**Create a file called `RuleAssistant.xml`:**

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

**Understanding this example:**
- `<MatchGroup>`: Defines features that must agree (α for gender, β for number)
- `<Source>`: The pattern to match in the source language (English DET NOUN)
- `<Target>`: What to output in the target language (Spanish NOUN DET)
- `id="1"` and `id="2"`: Link source words to target words
- `head="yes"`: Marks the main word (the noun in this case)

#### Step 3: Run the Rule Assistant

1. In FLExTrans, go to Modules → Rule Assistant
2. Open your `RuleAssistant.xml` file
3. Specify your transfer rule file (`transfer_rules.t1x`)
4. Click "Generate Transfer Rules"

**What happens:**
```
Processing Rule Assistant file...
Querying FLEx database for morphological data...
Generating rule: DET-NOUN
  - Created category definitions
  - Created macros for lemma selection
  - Generated pattern and action

Generated 1 rule
Added 3 macros
Updated transfer file: transfer_rules.t1x
```

#### Step 4: Test Your Rule

1. Run the "Run Apertium" module
2. Input test sentence: "the book"
3. Expected output: "el libro"

**Congratulations!** You've created your first transfer rule!

---

## Working with Existing Transfer Files

### Understanding the Data Sources

**Important:** There are THREE different data sources, and it's crucial to understand what each one contains:

```
┌─────────────────┐
│   FLEx          │ ← Single Source of Truth for Morphological Data
│   Database      │   (Categories, Features, Affixes, Stems)
└────────┬────────┘
         │ Queries on startup, reload, or rule generation
         │
         ▼
┌─────────────────┐
│ Rule Assistant  │ ← Your Rule Specifications
│ XML             │   (What patterns to match, how to transform)
│ (RuleAsst.xml)  │
└────────┬────────┘
         │ Read when you click "Generate"
         │
         ▼
┌─────────────────┐
│ Transfer Rules  │ ← Generated Output + Your Manual Edits
│ (.t1x file)     │   (Complete Apertium transfer rules)
└─────────────────┘
```

### When You Open Rule Assistant After Creating Rules

**Question:** "When I start up the RA again, where is it getting its info from?"

**Answer:**

When you open Rule Assistant, it loads data from **two places**:

1. **FLEx Database (Fresh):**
   - Categories (parts of speech)
   - Features (gender, number, etc.)
   - Affixes (prefixes, suffixes)
   - Current morphological data

2. **Rule Assistant XML (Your Rules):**
   - The rules you've created
   - Your rule specifications
   - Pattern definitions

**It does NOT automatically reload your .t1x file** - that only happens when you generate rules.

**You'll see this in the status bar:**
```
✓ FLEx Data: Loaded 2025-11-22 14:32 (English-Spanish)
✓ Rule specifications: RuleAssistant.xml
```

### Working with Existing Rules: Three Scenarios

#### Scenario 1: You created rules with RA and want to add more

**What happens:**

```
Before:
  transfer_rules.t1x (has 5 rules)

You:
  1. Open Rule Assistant
  2. Open RuleAssistant.xml (or edit it)
  3. Add new rule specification
  4. Click "Generate Transfer Rules"

After:
  transfer_rules.t1x (has 6 rules)
  ✓ All 5 old rules preserved
  ✓ 1 new rule added
```

**This is SAFE** - Your existing rules are preserved.

#### Scenario 2: You manually edited .t1x and want to use RA again

**What happens:**

```
Before:
  transfer_rules.t1x (has 5 RA rules + your manual macros and variables)

You:
  1. Open Rule Assistant
  2. Add new rule to RuleAssistant.xml
  3. Click "Generate Transfer Rules"

After:
  transfer_rules.t1x (has 6 RA rules + your manual content)
  ✓ All RA rules preserved/updated
  ✓ All manual macros PRESERVED
  ✓ All manual variables PRESERVED
  ⚠️ Empty sections MAY be removed (current bug - being fixed)
```

**This is MOSTLY SAFE,** but there's a known issue:

**⚠️ KNOWN ISSUE (FR-001):** If you have empty `<section-def-vars>` or `<section-def-macros>` sections (sections you created but haven't filled yet), they might be deleted.

**Workaround until fixed:**
- Don't leave sections empty
- Put a comment in empty sections: `<!-- Placeholder -->`
- Make backups before running RA

#### Scenario 3: You manually edited .t1x and want to modify an existing RA rule

**Behavior depends on `overwrite_rules` attribute:**

**If `overwrite_rules="no"` (default):**
```xml
<FLExTransRules overwrite_rules="no">
```

**What happens:**
- RA creates NEW rules with the same name
- Your old rules are kept
- Result: You have DUPLICATE rules
- **You need to manually delete the old ones**

**If `overwrite_rules="yes"`:**
```xml
<FLExTransRules overwrite_rules="yes">
```

**What happens:**
- RA REPLACES old rules with new ones
- Manual edits to those rules are LOST
- Other rules are preserved

**Recommendation:**
- Use `overwrite_rules="no"` (safer, requires manual cleanup)
- Always make backups before generating
- Use version control (Git) for your transfer files

### Workflow: Combining RA and Manual Editing

**Best Practice Workflow:**

```
1. Use Rule Assistant for:
   ✓ Basic transfer rules (word reordering, simple agreement)
   ✓ Repetitive patterns (many similar rules)
   ✓ Getting started quickly

2. Use Manual Editing for:
   ✓ Complex macros not supported by RA
   ✓ Advanced conditional logic
   ✓ Edge cases and exceptions
   ✓ Custom variables

3. Workflow:
   a. Create basic rules with RA
   b. Generate transfer file
   c. Manually add advanced macros/variables
   d. When adding more RA rules:
      - Make backup of .t1x
      - Generate new rules with RA
      - Verify your manual edits are preserved
      - If anything is lost, restore from backup and report issue
```

**File Organization Tip:**

Keep separate files for different purposes:

```
transfer_rules.t1x         ← RA-generated rules
transfer_rules_manual.t1x  ← Your hand-written rules
transfer_rules_combined.t1x ← Final combined file
```

Then merge them manually when ready for production.

### When FLEx Changes: Keeping Data in Sync

**Question:** "I made major changes to my FLEx project. Will RA see them?"

**Answer:** It depends on when you made the changes.

**✓ Changes BEFORE opening RA:**
- FLEx data is queried on RA startup
- Your changes WILL be reflected
- New categories, features, and affixes are available

**✗ Changes AFTER opening RA:**
- RA uses cached data from startup
- Your changes are NOT reflected
- Need to reload

**Solution: "Reload FLEx Data" button (coming soon)**

Until this feature is implemented:
- Close and reopen Rule Assistant after FLEx changes
- Or: Complete all FLEx setup before using RA

**What kinds of FLEx changes affect RA?**

| Change in FLEx | Affects RA? | What to do |
|----------------|-------------|------------|
| Add new feature (e.g., "case") | YES | Restart RA or wait for reload button |
| Add new category (e.g., "adv") | YES | Restart RA or wait for reload button |
| Add new affix | YES | Restart RA or wait for reload button |
| Change feature name | YES | Restart RA; update existing rules |
| Delete feature | ⚠️ WARNING | Rules using that feature will break |
| Change lemma spelling | NO | Lemmas are looked up dynamically |

### Checking What Data is Loaded

**Status Bar Information (Current):**

Unfortunately, the current version doesn't clearly show what data is loaded. This is being improved.

**How to verify (manual check):**

1. **Check your transfer file:**
   ```xml
   <!-- Look for comment like this: -->
   <!-- Generated: 2025-11-22 14:32:15 -->
   ```

2. **Check for expected categories:**
   Open your `.t1x` file and look for `<section-def-cats>`
   - Do you see all your parts of speech?
   - Are new categories you added in FLEx present?

3. **Check for expected attributes:**
   Look for `<section-def-attrs>`
   - Do you see all your features?
   - Are new features present?

---

## Understanding Disjoint Feature Sets (Bantu Noun Classes)

### What are Disjoint Feature Sets?

**The Problem:**

In some languages (especially Bantu), what looks like two different features in one language is actually ONE complex feature in another.

**Example:** Bantu noun classes

In English:
- Gender: masculine, feminine (separate feature)
- Number: singular, plural (separate feature)

In Swahili (Bantu):
- Noun class: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ... (ONE feature, but encodes both gender AND number)
- Class 1 = singular, Class 2 = plural of Class 1
- Class 3 = singular, Class 4 = plural of Class 3
- etc.

**The Challenge:**

How do you map English "gender + number" to Swahili "noun class"?

**Answer:** Disjoint Feature Sets

### How FLEx Represents This

In FLEx, you can define:
- **BantuNounClass** = the master set (union of all classes)
- **BantuNounClassSg** = subset for singular (classes 1, 3, 5, 7, 9, ...)
- **BantuNounClassPl** = subset for plural (classes 2, 4, 6, 8, 10, ...)

**Key Insight:** A single noun can have TWO values from the master set:
- Its class when singular (from BantuNounClassSg subset)
- Its class when plural (from BantuNounClassPl subset)

### Using Disjoint Features in Rule Assistant

#### Step 1: Define the Disjoint Feature Set

Create a special XML file: `SplitBantu.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<DisjointFeatureSets>

  <DisjointFeatureSet>
    <!-- The master set -->
    <MasterSet name="BantuNounClass"/>

    <!-- The subsets -->
    <Subset name="BantuNounClassSg" featureMapping="number" featureValue="sg"/>
    <Subset name="BantuNounClassPl" featureMapping="number" featureValue="pl"/>
  </DisjointFeatureSet>

</DisjointFeatureSets>
```

**What this means:**
- `BantuNounClass` is the overall feature
- When number=singular, use values from `BantuNounClassSg`
- When number=plural, use values from `BantuNounClassPl`

#### Step 2: Reference the Master Set in Rules

**Important:** On the noun root, use the MASTER SET name, not the subset names.

```xml
<Word id="1" category="n" head="yes">
  <Features>
    <!-- Use the MASTER set name, even though the noun has values from BOTH subsets -->
    <Feature label="BantuNounClass" match="α"/>
  </Features>
</Word>
```

**Why?** Because a single noun has TWO class values (singular and plural), and the Rule Assistant needs to know to handle both. The master set name tells it: "This is a disjoint feature, handle it specially."

#### Step 3: Agreement Targets Use the Same Master Set

```xml
<Word id="2" category="adj" head="no">
  <Features>
    <!-- Adjective agrees with noun using the same master set -->
    <Feature label="BantuNounClass" match="α"/>
  </Features>
</Word>
```

#### Step 4: The Rule Assistant Generates Special Macros

When you generate rules, the Rule Assistant:

1. **Recognizes** the disjoint feature set (from `SplitBantu.xml`)
2. **Generates special macros** that:
   - Check the number of the source noun
   - If singular, use BantuNounClassSg values
   - If plural, use BantuNounClassPl values
   - Set the correct class on the target

**Generated code (excerpt):**
```xml
<def-macro n="select_bantu_class_for_adj" ...>
  <choose>
    <when>
      <test>
        <equal>
          <clip pos="1" side="tl" part="number"/>
          <lit-tag v="sg"/>
        </equal>
      </test>
      <!-- Use singular noun class values -->
      <var n="class">
        <clip pos="1" side="tl" part="BantuNounClassSg"/>
      </var>
    </when>
    <otherwise>
      <!-- Use plural noun class values -->
      <var n="class">
        <clip pos="1" side="tl" part="BantuNounClassPl"/>
      </var>
    </otherwise>
  </choose>
</def-macro>
```

### Common Mistakes and How to Avoid Them

**Mistake 1: Using subset names in rules**

❌ Wrong:
```xml
<Feature label="BantuNounClassSg" match="α"/>  <!-- DON'T DO THIS -->
```

✓ Correct:
```xml
<Feature label="BantuNounClass" match="α"/>  <!-- Use master set -->
```

**Mistake 2: Not defining the DisjointFeatureSet XML**

If you get this error:
```
Warning: BantuNounClass feature not found in transfer rule attributes.
```

**Possible causes:**
1. You didn't create `SplitBantu.xml`
2. You didn't run "Set Up Transfer Rule Categories and Attributes" after creating it
3. The file isn't in the right location

**Solution:**
1. Create `SplitBantu.xml` in your project directory
2. Run "Set Up Transfer Rule Categories and Attributes" module
3. The module will read the disjoint feature definition
4. It will create the necessary attributes in your transfer file

**Mistake 3: Confusing "feature" (in FLEx) with "attribute" (in transfer file)**

**Terminology:**
- **FLEx Feature:** A grammatical property defined in FLEx (like "BantuNounClass")
- **Transfer Attribute:** A definition in the transfer file's `<section-def-attrs>` section

**The warning message says "feature" but it's looking for an "attribute":**

```
Warning: BantuNounClass feature not found in transfer rule attributes.
```

**Translation:**
"I'm looking for a `<def-attr n="BantuNounClass">` definition in the `<section-def-attrs>` section of your transfer file, and I can't find it."

**Solution:**
Run "Set Up Transfer Rule Categories and Attributes" to populate attributes.

### Example: Complete Bantu Noun Class Setup

**Step-by-step guide:**

1. **In FLEx:** Define your noun class system
   - Create feature "BantuNounClass" with all class values (1, 2, 3, 4, ...)
   - Create feature "BantuNounClassSg" with singular class values
   - Create feature "BantuNounClassPl" with plural class values

2. **Create `SplitBantu.xml`:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <DisjointFeatureSets>
     <DisjointFeatureSet>
       <MasterSet name="BantuNounClass"/>
       <Subset name="BantuNounClassSg" featureMapping="number" featureValue="sg"/>
       <Subset name="BantuNounClassPl" featureMapping="number" featureValue="pl"/>
     </DisjointFeatureSet>
   </DisjointFeatureSets>
   ```

3. **Run "Set Up Transfer Rule Categories and Attributes"**
   - This creates the attribute definitions in your transfer file

4. **Create your rule in `RuleAssistant.xml`:**
   ```xml
   <Rule name="NOUN-ADJ">
     <Source>
       <MatchGroup>
         <MatchElement label="BantuNounClass" match="α"/>
       </MatchGroup>
       <Word id="1" category="n" head="yes">
         <Features>
           <Feature label="BantuNounClass" match="α"/>
         </Features>
       </Word>
       <Word id="2" category="adj" head="no">
         <Features>
           <Feature label="BantuNounClass" match="α"/>
         </Features>
       </Word>
     </Source>
     <Target>
       <!-- Same pattern in target -->
     </Target>
   </Rule>
   ```

5. **Generate transfer rules**
   - RA will create special macros for disjoint feature handling

6. **Test**
   - Verify that noun class agreement works correctly
   - Test both singular and plural forms

---

## Module Prerequisites and Workflow

### Understanding the Module Sequence

FLExTrans has several modules that work together. Here's the correct sequence:

```
┌─────────────────────────────────────────────────────────────────┐
│                   COMPLETE WORKFLOW                             │
└─────────────────────────────────────────────────────────────────┘

1. SET UP FLEX PROJECTS
   │
   ├─ Create source language project (e.g., English)
   ├─ Create target language project (e.g., Spanish)
   ├─ Define categories (noun, verb, adj, etc.)
   ├─ Define features (gender, number, case, etc.)
   ├─ Define affixes (prefixes, suffixes, etc.)
   └─ Add lexical entries
   │
   ▼
2. SET UP TRANSFER RULE CATEGORIES AND ATTRIBUTES ⚠️ REQUIRED FIRST
   │
   ├─ Queries both FLEx projects
   ├─ Creates transfer_rules.t1x foundation
   ├─ Adds <section-def-cats> (categories)
   ├─ Adds <section-def-attrs> (attributes)
   └─ File is ready for Rule Assistant
   │
   ▼
3. RULE ASSISTANT (Create transfer rules)
   │
   ├─ Reads Rule Assistant XML (your rules)
   ├─ Queries FLEx for morphological data
   ├─ Generates Apertium transfer rules
   ├─ Adds/updates <section-rules>
   └─ Adds/updates <section-def-macros>
   │
   ▼
4. RUN APERTIUM (Optional - for testing)
   │
   ├─ Generates sample transfer data
   ├─ You can test your rules with real data
   └─ Provides examples for Rule Tester
   │
   ▼
5. RULE ASSISTANT (Again - with sample data)
   │
   ├─ Now you can see how rules apply to real examples
   ├─ Use Live Rule Tester to debug
   └─ Refine your rules
   │
   ▼
6. ITERATE
   │
   └─ Repeat steps 3-5 as needed
```

### Module Details

#### Module 1: Set Up Transfer Rule Categories and Attributes

**When to run:**
- ✓ **First time setup** (required)
- ✓ When you add new categories to FLEx
- ✓ When you add new features to FLEx
- ✓ When you add new affixes to FLEx
- ✗ NOT needed just to add more rules (if categories/features unchanged)

**What it does:**
- Queries your source and target FLEx projects
- Extracts all categories (parts of speech)
- Extracts all features (grammatical features)
- Creates `<section-def-cats>` in transfer file
- Creates `<section-def-attrs>` in transfer file
- Optionally: Reads `SplitBantu.xml` for disjoint features

**Input:**
- Source FLEx project
- Target FLEx project
- Output path for transfer file
- (Optional) DisjointFeatureSet XML

**Output:**
- `transfer_rules.t1x` with basic structure

**Example output file:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<transfer default="chunk">
  <section-def-cats>
    <def-cat n="n"><cat-item tags="n.*"/></def-cat>
    <def-cat n="det"><cat-item tags="det.*"/></def-cat>
    <def-cat n="adj"><cat-item tags="adj.*"/></def-cat>
    <!-- ... more categories ... -->
  </section-def-cats>

  <section-def-attrs>
    <def-attr n="gender">
      <attr-item tags="m"/>
      <attr-item tags="f"/>
      <attr-item tags="nt"/>
    </def-attr>
    <def-attr n="number">
      <attr-item tags="sg"/>
      <attr-item tags="pl"/>
    </def-attr>
    <!-- ... more attributes ... -->
  </section-def-attrs>

  <!-- Other sections will be added by Rule Assistant -->
</transfer>
```

#### Module 2: Rule Assistant

**When to run:**
- ✓ After running "Set Up Transfer Rule Categories and Attributes"
- ✓ Whenever you create or modify rules in RuleAssistant.xml
- ✓ To regenerate transfer rules

**What it does:**
- Reads your Rule Assistant XML file
- Queries FLEx database for current morphological data
- Generates Apertium transfer rules
- Creates macros for lemma/affix selection
- Updates transfer_rules.t1x

**Input:**
- Rule Assistant XML file (your rules)
- FLEx source and target projects
- Existing transfer_rules.t1x (to preserve)

**Output:**
- Updated transfer_rules.t1x with new rules

**Progress you'll see:**
```
Opening Rule Assistant...
Loading Rule Assistant XML: RuleAssistant.xml
Querying FLEx database...
Processing rule: DET-NOUN
  Generating categories...
  Generating macros...
  Generating pattern and action...
Processing rule: ADJ-NOUN
  ...

Generated 5 rules
Added 12 macros (3 reused)
Updated transfer file: transfer_rules.t1x
```

#### Module 3: Run Apertium (Optional but Recommended)

**When to run:**
- ✓ After creating transfer rules (to test them)
- ✓ Before refining rules (to get sample data)
- ✓ For debugging (to see what's happening)

**What it does:**
- Runs the complete Apertium pipeline on sample sentences
- Generates transfer debugging data
- Shows you what your rules produce

**Input:**
- Source text
- FLEx projects
- Transfer rules
- Bilingual dictionary
- Morphological analyzers/generators

**Output:**
- Translated text
- Debugging information
- Sample data for Rule Tester

### Decision Tree: Which Module to Run?

```
START

Are you starting a NEW project?
├─ YES: Run "Set Up Transfer Rule Categories and Attributes"
│       Then run "Rule Assistant"
│       Then run "Run Apertium" to test
│
└─ NO: Have you added categories/features to FLEx?
       ├─ YES: Run "Set Up Transfer Rule Categories and Attributes"
       │       (This updates the attributes)
       │       Then run "Rule Assistant"
       │
       └─ NO: Are you adding/modifying rules?
              ├─ YES: Just run "Rule Assistant"
              │
              └─ NO: Are you testing existing rules?
                     └─ YES: Just run "Run Apertium"
```

### Common Scenarios

#### Scenario: First Time Setup

**Steps:**
1. Set up FLEx projects (source and target)
2. Run "Set Up Transfer Rule Categories and Attributes"
3. Create `RuleAssistant.xml` with your first rule
4. Run "Rule Assistant"
5. Run "Run Apertium" to test
6. Refine and repeat steps 3-5

**Time estimate:** 2-3 hours for first rule

#### Scenario: Adding More Rules

**Steps:**
1. Edit `RuleAssistant.xml` to add new rules
2. Run "Rule Assistant" (no need to run setup again)
3. Run "Run Apertium" to test new rules

**Time estimate:** 15-30 minutes per rule

#### Scenario: Changed FLEx Project

**What changed?**

**If you added categories/features:**
1. Run "Set Up Transfer Rule Categories and Attributes"
2. Run "Rule Assistant" (regenerate all rules)
3. Test with "Run Apertium"

**If you only added lexical entries:**
1. No modules needed!
2. Just run "Run Apertium" to test
3. Lexical data is looked up dynamically

**If you deleted categories/features:**
1. ⚠️ WARNING: Rules using deleted features will break
2. Edit `RuleAssistant.xml` to remove references
3. Run "Set Up Transfer Rule Categories and Attributes"
4. Run "Rule Assistant"
5. Check for errors in transfer file

### Do You Need to Pre-populate Attributes?

**Question:** "Do we need to pre-populate the Attributes, or not?"

**Answer:** YES, you need to run "Set Up Transfer Rule Categories and Attributes" first.

**Why:**
- The Rule Assistant needs existing `<section-def-attrs>` to work
- It references attributes when generating rules
- Without attributes, rule generation will fail

**But you only need to run it ONCE** (unless you change FLEx):
- ✓ First time: Run setup module
- ✓ Added FLEx feature: Re-run setup module
- ✗ Just adding rules: Don't need to re-run setup

**Analogy:**
Think of "Set Up Categories and Attributes" as building the foundation of a house. You do it once, then you can add rooms (rules) on top of that foundation.

---

## Advanced Topics

### Ranked Features

**What are ranked features?**

Sometimes a lemma (the base form of a word) depends on multiple features, and you need to check them in a specific priority order.

**Example:** Spanish determiners

The determiner lemma depends on:
1. Gender (masculine/feminine)
2. Number (singular/plural)

But what if the source doesn't specify gender? You might want to:
- First, try to find a lemma matching BOTH gender and number
- If not found, use a default based on gender alone
- If still not found, use a completely default lemma

**How to specify ranking:**

```xml
<Word id="1" category="det">
  <Features>
    <Feature label="gender" match="α" ranking="1"/>
    <Feature label="number" match="β" ranking="2"/>
  </Features>
</Word>
```

**What this means:**
- `ranking="1"`: Highest priority (check gender first)
- `ranking="2"`: Lower priority (check number second)

**Generated macro** (simplified):
```xml
<choose>
  <!-- Try gender + number -->
  <when>
    <test><and>
      <equal><clip part="gender"/><lit-tag v="m"/></equal>
      <equal><clip part="number"/><lit-tag v="sg"/></equal>
    </and></test>
    <lit v="el"/>
  </when>

  <!-- Try gender only (if number not specified) -->
  <when>
    <test>
      <equal><clip part="gender"/><lit-tag v="m"/></equal>
    </test>
    <lit v="el"/>
  </when>

  <!-- Default -->
  <otherwise>
    <lit v="el"/>
  </otherwise>
</choose>
```

### Default Values

**What are default values?**

Default values specify what to use when a feature is not marked in the source.

**Example:**

In English, gender is often unmarked on nouns. But Spanish requires gender. What do you do?

**Solution: Use `unmarked_default`**

```xml
<Word id="1" category="n">
  <Features>
    <Feature label="gender" match="α" unmarked_default="m"/>
    <Feature label="number" match="β"/>
  </Features>
</Word>
```

**What this means:**
- If the source noun has gender, use it
- If the source noun has NO gender, assume masculine ("m")

**When to use defaults:**
- Source language doesn't mark a feature, but target does
- You want to make a linguistically reasonable assumption
- You're handling typologically different languages

**Example: English → German**

English nouns don't mark case, but German does. Default to nominative:

```xml
<Feature label="case" unmarked_default="nom"/>
```

### Pattern Features (Conditional Rules)

**What are pattern features?**

Sometimes you only want a rule to apply when a specific feature has a specific value.

**Example:**

You want separate rules for definite and indefinite articles:
- "the" → "el/la" (definite)
- "a/an" → "un/una" (indefinite)

**Solution: Use `value` attribute**

```xml
<!-- Rule for DEFINITE articles -->
<Rule name="DEF-ART-NOUN">
  <Source>
    <Word id="1" category="det">
      <Features>
        <Feature label="definiteness" value="def"/>  <!-- ONLY definite -->
        <Feature label="gender" match="α"/>
      </Features>
    </Word>
    <!-- ... -->
  </Source>
  <!-- ... -->
</Rule>

<!-- Separate rule for INDEFINITE articles -->
<Rule name="INDEF-ART-NOUN">
  <Source>
    <Word id="1" category="det">
      <Features>
        <Feature label="definiteness" value="indef"/>  <!-- ONLY indefinite -->
        <Feature label="gender" match="α"/>
      </Features>
    </Word>
    <!-- ... -->
  </Source>
  <!-- ... -->
</Rule>
```

**What this does:**
- First rule ONLY matches when definiteness="def"
- Second rule ONLY matches when definiteness="indef"
- Apertium will choose the correct rule based on the input

### Permutations (Optional Words)

**What are permutations?**

Sometimes words are optional in a phrase. Instead of writing multiple rules, you can use permutations.

**Example:**

English allows:
- "the big red ball"
- "the big ball"
- "the red ball"
- "the ball"

**Solution: Use `create_permutations="yes"`**

```xml
<Rule name="DET-ADJ-ADJ-NOUN">
  <Source>
    <Word id="1" category="det"/>

    <Word id="2" category="adj" create_permutations="yes">
      <!-- This word is OPTIONAL -->
    </Word>

    <Word id="3" category="adj" create_permutations="yes">
      <!-- This word is OPTIONAL -->
    </Word>

    <Word id="4" category="n" head="yes"/>
  </Source>
  <!-- ... -->
</Rule>
```

**What this generates:**
- Rule variant 1: DET ADJ ADJ NOUN (both adjectives)
- Rule variant 2: DET ADJ NOUN (first adjective only)
- Rule variant 3: DET ADJ NOUN (second adjective only)
- Rule variant 4: DET NOUN (no adjectives)

**When to use:**
- Languages with flexible word order
- Optional modifiers
- Handling incomplete input

**Warning:**
- With N optional words, you get 2^N rule variants
- 3 optional words = 8 rules
- Use sparingly to avoid explosion of rules

---

## Troubleshooting

### Problem: "My rules disappeared!"

**Symptoms:**
- You generated rules with RA
- The .t1x file was created
- You make more rules
- Old rules are gone

**Possible Causes:**

1. **File was overwritten**
   - Check: Did you specify the same output filename?
   - Check: Did you use `overwrite_rules="yes"`?

2. **Wrong file opened**
   - Check: Are you looking at the right .t1x file?
   - Check: Multiple projects, same filename in different directories?

3. **File corruption**
   - Check: Is the .t1x file valid XML?
   - Try opening in XML editor

**Solutions:**
- **Always use version control** (Git) for your transfer files
- Make backups before running RA
- Use `overwrite_rules="no"` (default) unless you specifically want to replace

### Problem: "My manual edits were lost!"

**Symptoms:**
- You manually added macros/variables to .t1x
- Ran Rule Assistant
- Your additions are gone

**Known Issue:** FR-001 (being fixed)

**Current Workaround:**
- Don't leave sections empty
- Put a placeholder in empty sections
- Keep manual edits in separate file, merge manually

**Long-term Solution (coming soon):**
- All sections will be preserved automatically
- RA will never delete user content

### Problem: "RA doesn't see my FLEx changes"

**Symptoms:**
- Added new feature/category to FLEx
- Opened Rule Assistant
- New feature not available in dropdowns

**Cause:**
FLEx data loaded at startup; changes after startup not reflected

**Solution:**
- Close and reopen Rule Assistant
- OR wait for "Reload FLEx Data" button (coming soon)

### Problem: "Warning: BantuNounClass feature not found"

**Full error:**
```
Warning: BantuNounClass feature not found in transfer rule attributes.
```

**What it means:**
"I'm looking for a `<def-attr n="BantuNounClass">` in your transfer file's `<section-def-attrs>` section, but I don't see it."

**Causes:**

1. **You haven't run "Set Up Transfer Rule Categories and Attributes"**
   - **Solution:** Run that module first

2. **Your `SplitBantu.xml` wasn't found**
   - **Solution:** Ensure `SplitBantu.xml` is in the correct location
   - **Solution:** Re-run "Set Up Transfer Rule Categories and Attributes"

3. **The feature name is misspelled**
   - **Check:** Feature name in FLEx
   - **Check:** Feature name in `SplitBantu.xml`
   - **Check:** Feature name in your Rule Assistant XML
   - Make sure all three match exactly (case-sensitive!)

4. **The feature doesn't exist in your target FLEx project**
   - **Solution:** Add the feature to your target FLEx project
   - **Solution:** Re-run "Set Up Transfer Rule Categories and Attributes"

### Problem: "Error: Duplicate rule name"

**Error:**
```
Error: Rule with name 'DET-NOUN' already exists.
```

**Cause:**
You have two rules with the same `name` attribute in your RuleAssistant.xml

**Solution:**
- Make rule names unique
- Or use `overwrite_rules="yes"` to replace the old rule

### Problem: "Transfer rule doesn't match my input"

**Symptoms:**
- Created a rule
- Tested with Apertium
- Input phrase doesn't match the rule

**Possible Causes:**

1. **Category mismatch**
   - Check: Does your input have the right parts of speech?
   - Example: Rule expects "det + noun" but input has "article + noun"
   - Solution: Check FLEx category assignments

2. **Feature value mismatch**
   - Check: Does your rule require specific feature values?
   - Example: Rule has `<Feature label="definiteness" value="def"/>`
   - But input has indefinite article
   - Solution: Create separate rules for different values

3. **Word order**
   - Check: Rule pattern order vs. input order
   - Example: Rule expects "det noun" but input has "noun det"
   - Solution: Create rule for the actual input order

4. **Morphological analysis issue**
   - Check: Is your input being analyzed correctly by Apertium?
   - Run morphological analyzer separately to verify
   - Solution: Fix dictionary or morphological analyzer

**Debugging steps:**

1. **Test morphological analysis:**
   ```bash
   echo "the book" | lt-proc en-es.automorf.bin
   ```
   Expected output:
   ```
   ^the<det><def><sg>/el<det><def><m><sg>/la<det><def><f><sg>$
   ^book<n><sg>/libro<n><m><sg>$
   ```

2. **Check if your rule pattern matches the analysis:**
   - Rule pattern: `<pattern-item n="det"/>` → matches `<det>`
   - Analysis: `the<det><def><sg>` → has `<det>` tag → ✓ matches

3. **Verify feature values:**
   - If rule requires `value="def"`
   - Analysis must have `<def>` tag

### Problem: "Generate button doesn't work" / "No output produced"

**Symptoms:**
- Click "Generate Transfer Rules"
- No error shown
- But no .t1x file created or updated

**Possible Causes:**

1. **Output path is wrong**
   - Check: Specified output path exists?
   - Check: Do you have write permission?

2. **Rule Assistant XML is invalid**
   - Check: Valid XML structure?
   - Check: Conforms to DTD?
   - Solution: Validate XML with XML editor

3. **FLEx database not accessible**
   - Check: FLEx projects still exist?
   - Check: Paths to FLEx projects correct?

4. **Silent error**
   - Check: Error log or console output
   - Run in debug mode if available

**Solution:**
- Check file paths carefully
- Validate your RuleAssistant.XML
- Ensure FLEx projects are accessible
- Check error logs

---

## FAQ

### General Questions

**Q: Can I use Rule Assistant for all my transfer rules?**

A: No, Rule Assistant is designed for common patterns. For complex logic, advanced conditionals, or unusual linguistic phenomena, you'll need to manually edit the .t1x file.

**Q: Can I mix Rule Assistant rules with manual rules?**

A: Yes! This is actually a recommended workflow:
- Use RA for repetitive, pattern-based rules
- Manually add complex macros and variables
- Combine both in your final transfer file

**Q: Do I need to know Apertium to use Rule Assistant?**

A: Not for basic rules. But understanding Apertium will help you:
- Debug problems
- Create advanced rules manually
- Understand what RA generates

**Q: How do I learn more about Apertium?**

A: Resources:
- Apertium Wiki: https://wiki.apertium.org/
- Apertium documentation on transfer rules
- FLExTrans documentation

### Technical Questions

**Q: What's the difference between a feature and an attribute?**

A: Terminology can be confusing:
- **Feature (in FLEx):** A grammatical property like "gender" or "number"
- **Attribute (in Apertium):** A definition in the transfer file's `<section-def-attrs>` that lists possible values
- The Rule Assistant creates attributes from features

**Q: What's the difference between `match` and `value` in Feature elements?**

A:
- **`match="α"`:** Links features across words for agreement (α can be any value)
- **`value="def"`:** Fixes the feature to a specific value (pattern matching)

Example:
```xml
<Feature label="gender" match="α"/>     <!-- agrees with other α -->
<Feature label="definiteness" value="def"/>  <!-- MUST be definite -->
```

**Q: What does `head="yes"` mean?**

A: The head word is the main word in a phrase:
- In "the big book", "book" is the head (it determines the overall properties)
- In most languages, modifiers agree with the head
- Marking the head helps RA generate correct agreement patterns

**Q: Can I have multiple heads in one rule?**

A: No, only one word should have `head="yes"` in a rule. If you need multiple heads, you probably need separate rules.

**Q: What's the difference between `<Stem>` and `<Affixes>` features?**

A:
- **`<Stem>` features:** Inherent properties of the root word
- **`<Affixes>` features:** Properties marked by prefixes/suffixes

Example:
```xml
<Word category="n">
  <!-- The root noun has inherent gender -->
  <Stem>
    <Features>
      <Feature label="gender" match="α"/>
    </Features>
  </Stem>

  <!-- Number is marked by a suffix -->
  <Affixes>
    <Affix type="suffix">
      <Features>
        <Feature label="number" match="β"/>
      </Features>
    </Affix>
  </Affixes>
</Word>
```

### Workflow Questions

**Q: Should I create all my rules at once or one at a time?**

A: Start small:
1. Create one simple rule
2. Test it thoroughly
3. Once it works, create more rules
4. This makes debugging much easier

**Q: How often should I test with "Run Apertium"?**

A: Test frequently:
- After creating each rule
- Before creating many similar rules
- After making changes to FLEx
- Before considering rules "done"

**Q: Should I keep my Rule Assistant XML in version control?**

A: YES! Always keep both:
- `RuleAssistant.xml` (your specifications)
- `transfer_rules.t1x` (generated output)
In version control (Git). This lets you:
- Track changes
- Revert mistakes
- Collaborate with others

**Q: Can multiple people work on rules together?**

A: Yes, but be careful:
- Use version control (Git)
- Coordinate who edits what
- Merge carefully
- Test after merging

**Q: What if my language pair doesn't fit the RA model well?**

A: RA works best for:
- Relatively simple word order changes
- Agreement patterns
- Feature mapping

If your languages have very different structures:
- Use RA for parts that fit
- Manually code the rest
- Or use a different approach entirely (consult documentation)

---

## Quick Reference

### Rule Assistant XML Cheat Sheet

#### Basic Rule Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE FLExTransRuleGenerator SYSTEM "FLExTransRuleGenerator.dtd">
<FLExTransRuleGenerator>
  <FLExTransRules overwrite_rules="no">
    <Rule name="UNIQUE_NAME">
      <Source>
        <MatchGroup>
          <MatchElement label="FEATURE_NAME" match="α"/>
        </MatchGroup>
        <Word id="1" category="POS" head="no">
          <Features>
            <Feature label="FEATURE_NAME" match="α"/>
          </Features>
        </Word>
      </Source>
      <Target>
        <Word id="1" category="POS">
          <Features>
            <Feature label="FEATURE_NAME" match="α"/>
          </Features>
        </Word>
      </Target>
    </Rule>
  </FLExTransRules>
</FLExTransRuleGenerator>
```

#### Feature Attributes

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `label` | Feature name | `label="gender"` |
| `match` | Agreement link | `match="α"` |
| `value` | Fixed value (pattern) | `value="def"` |
| `unmarked_default` | Default if not marked | `unmarked_default="m"` |
| `ranking` | Priority (1=highest) | `ranking="1"` |

#### Match Labels

| Symbol | Use |
|--------|-----|
| α | Alpha - first agreement feature |
| β | Beta - second agreement feature |
| γ | Gamma - third agreement feature |
| δ | Delta - fourth agreement feature |

### Module Quick Reference

| Module | When to Run | What It Does |
|--------|-------------|--------------|
| Set Up Transfer Rule Categories and Attributes | First time, when FLEx changes | Creates .t1x structure |
| Rule Assistant | When creating/modifying rules | Generates transfer rules |
| Run Apertium | After creating rules | Tests rules with real data |

### File Locations

| File | Purpose | Example |
|------|---------|---------|
| `RuleAssistant.xml` | Your rule specifications | In your project directory |
| `transfer_rules.t1x` | Generated Apertium rules | In your project directory |
| `SplitBantu.xml` | Disjoint feature definitions | In your project directory |
| `FLExTransRuleGenerator.dtd` | XML schema | In Rule Assistant directory |

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Feature not found in attributes" | Missing attribute definition | Run "Set Up Categories and Attributes" |
| "Duplicate rule name" | Two rules same name | Make names unique or use overwrite |
| "Category not found" | POS not in FLEx | Check category name, add to FLEx |
| "Invalid XML" | Syntax error | Validate XML, check structure |

### Best Practices Checklist

- [ ] Run "Set Up Categories and Attributes" first (new project)
- [ ] Use meaningful rule names
- [ ] Use version control (Git) for all files
- [ ] Make backups before running RA
- [ ] Test each rule with "Run Apertium"
- [ ] Keep RuleAssistant.xml simple (one rule at a time at first)
- [ ] Document your rules with comments
- [ ] Use `overwrite_rules="no"` by default
- [ ] Verify FLEx data is current before generating
- [ ] Check generated .t1x file for correctness

---

## Getting Help

### Resources

**Documentation:**
- FLExTrans User Guide
- Apertium Wiki: https://wiki.apertium.org/
- Rule Assistant Examples (in installation directory)

**Support:**
- FLExTrans mailing list
- GitHub issues: https://github.com/[repo]
- Community forums

**Example Files:**
Look in your FLExTrans installation directory under `Rule Assistant/` for:
- Example rule files
- Sample SplitBantu.xml
- DTD documentation

### Reporting Problems

When reporting issues, please include:

1. **What you were trying to do** (your goal)
2. **What you did** (steps you followed)
3. **What you expected to happen**
4. **What actually happened**
5. **Files** (attach your RuleAssistant.xml and .t1x if possible)
6. **Error messages** (exact text)
7. **FLExTrans version**
8. **FLEx version**

---

**Document Version:** 1.0
**Last Updated:** 2025-11-22
**Feedback:** Please send feedback and suggestions to [email/contact]

---

*This user guide addresses questions and issues documented in DOC-001, DOC-002, DOC-003, and DOC-004 from the Feature Requests analysis.*
