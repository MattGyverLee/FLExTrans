# Rule Assistant Templates

This directory contains clean template files for starting new Rule Assistant projects.

## Available Templates

### 1. minimal_template.t1x
**Use when:** Starting completely from scratch
**Contains:** Empty sections with brief comments
**Best for:** Users who want maximum control and minimal clutter

### 2. standard_template.t1x
**Use when:** You want helpful examples and documentation
**Contains:** Empty sections with detailed comments and examples (commented out)
**Best for:** First-time users or as a quick reference

## How to Use Templates

### Method 1: Manual Copy (Current Approach)
1. Copy your chosen template to your project's transfer rules location
2. Rename it to `transfer_rules.t1x` (or your project's rule file name)
3. Run "Set Up Transfer Rule Categories and Attributes" to populate categories/attributes
4. Run "Rule Assistant" to start creating rules

### Method 2: Using the Reset Script (Recommended)
See `reset_to_template.bat` or `reset_to_template.sh` in this directory

## Template Contents

All templates include the required 6 sections:
- `<section-def-cats>` - Category definitions (part-of-speech patterns)
- `<section-def-attrs>` - Attribute definitions (grammatical features)
- `<section-def-vars>` - Variable definitions (for macro processing)
- `<section-def-lists>` - Optional word lists
- `<section-def-macros>` - Reusable code blocks (auto-generated)
- `<section-rules>` - Transfer rules (created with Rule Assistant)

## Creating Your Own Template

You can save your current transfer rules file as a custom template:

1. Make a copy of your `transfer_rules.t1x`
2. Remove any language-specific rules you don't want in every project
3. Keep macros and variables you commonly use
4. Save it in this directory with a descriptive name
5. Add documentation about what it contains

## Template Maintenance

**Important:** These templates contain NO language-specific data. If you see Swedish, German, Spanish, or other language-specific categories/attributes in your template, they were added by running FLExTrans modules on a specific project.

To keep templates clean:
- Don't save your project's rule file as a template without cleaning it first
- Remove all `<def-cat>` items except examples
- Remove all `<def-attr>` items except examples
- Remove all `<def-macro>` items (these should be auto-generated)
- Remove all `<rule>` items (these should be created in Rule Assistant)

## Troubleshooting

**Q: My template has Swedish/German data in it**
A: You copied a project-specific file. Use `minimal_template.t1x` instead.

**Q: Can Rule Assistant automatically reset to a template?**
A: Not yet (see Feature Request FR-004). For now, manually copy the template file.

**Q: Do I need to run any modules before Rule Assistant?**
A: Yes! Run "Set Up Transfer Rule Categories and Attributes" first to populate categories and attributes from your FLEx project.

## See Also

- `/home/user/FLExTrans/docs/RULE_ASSISTANT_USER_GUIDE.md` - Complete user documentation
- `/home/user/FLExTrans/docs/RuleAssistant_Feature_Requests.md` - FR-004 for template management features
