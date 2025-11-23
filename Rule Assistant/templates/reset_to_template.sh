#!/bin/bash
# Reset transfer rules file to clean template
# Usage: ./reset_to_template.sh [template_name] [target_file]
# Example: ./reset_to_template.sh minimal_template.t1x ../../transfer_rules.t1x

# Default template if not specified
TEMPLATE="${1:-minimal_template.t1x}"

# Default target if not specified
TARGET="${2:-../../transfer_rules.t1x}"

# Check if template exists
if [ ! -f "$TEMPLATE" ]; then
    echo "ERROR: Template file '$TEMPLATE' not found!"
    echo "Available templates:"
    ls -1 *.t1x
    exit 1
fi

# Backup existing file if it exists
if [ -f "$TARGET" ]; then
    BACKUP="${TARGET}.backup_$(date +%Y%m%d_%H%M%S)"
    echo "Creating backup: $BACKUP"
    cp "$TARGET" "$BACKUP"
fi

# Copy template to target
echo "Copying $TEMPLATE to $TARGET"
cp "$TEMPLATE" "$TARGET"

if [ $? -eq 0 ]; then
    echo "Success! Transfer rules reset to $TEMPLATE"
    echo ""
    echo "Next steps:"
    echo "1. Run 'Set Up Transfer Rule Categories and Attributes' to populate from FLEx"
    echo "2. Run 'Rule Assistant' to create your rules"
else
    echo "ERROR: Failed to copy template"
    exit 1
fi
