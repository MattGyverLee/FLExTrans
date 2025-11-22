#
#   RuleAssistantSync
#
#   Proof-of-Concept for Rule Assistant File Synchronization
#
#   Version 1.0 - 2025-11-22 - Claude (Coder Agent 2)
#   Initial version - FR-002 investigation
#
#   Provides file state tracking and change detection for Rule Assistant
#   to prevent silent data loss and improve user communication.
#

import os
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

# Change types that can be detected
class ChangeType(Enum):
    NONE = "none"
    EXTERNAL_T1X_EDIT = "external_t1x_edit"
    FLEX_DB_CHANGED = "flex_db_changed"
    METADATA_MISSING = "metadata_missing"
    FIRST_RUN = "first_run"

@dataclass
class FileMetadata:
    """Metadata for tracking file state and synchronization."""

    # When metadata was created/updated
    created: datetime
    last_modified: datetime
    last_sync: datetime

    # Transfer rules file tracking
    transfer_file_path: str
    transfer_file_hash: Optional[str] = None

    # FLEx database state tracking
    source_db_name: str = ""
    source_category_count: int = 0
    source_feature_count: int = 0

    target_db_name: str = ""
    target_category_count: int = 0
    target_feature_count: int = 0

    # Version for future compatibility
    metadata_version: str = "1.0"

@dataclass
class FlexStats:
    """Statistics about a FLEx database."""

    project_name: str
    category_count: int
    feature_count: int

    def __eq__(self, other):
        if not isinstance(other, FlexStats):
            return False
        return (self.project_name == other.project_name and
                self.category_count == other.category_count and
                self.feature_count == other.feature_count)

    def diff(self, other) -> List[str]:
        """Return list of differences between this and other stats."""
        differences = []

        if self.project_name != other.project_name:
            differences.append(f"Project name changed: '{other.project_name}' → '{self.project_name}'")

        if self.category_count != other.category_count:
            delta = self.category_count - other.category_count
            if delta > 0:
                differences.append(f"{delta} new categor{'y' if delta == 1 else 'ies'} added")
            else:
                differences.append(f"{-delta} categor{'y' if delta == -1 else 'ies'} removed")

        if self.feature_count != other.feature_count:
            delta = self.feature_count - other.feature_count
            if delta > 0:
                differences.append(f"{delta} new feature{'' if delta == 1 else 's'} added")
            else:
                differences.append(f"{-delta} feature{'' if delta == -1 else 's'} removed")

        return differences

@dataclass
class ChangeDetectionResult:
    """Result of change detection analysis."""

    change_type: ChangeType
    message: str
    details: List[str]
    can_continue: bool = True
    recommended_action: str = ""

class RuleAssistantSyncManager:
    """Manages file synchronization and change detection for Rule Assistant."""

    # Metadata element names
    METADATA_ROOT = "RuleAssistantMetadata"
    CREATED = "Created"
    LAST_MODIFIED = "LastModified"
    LAST_SYNC = "LastSync"
    TRANSFER_FILE = "TransferFile"
    TRANSFER_FILE_HASH = "TransferFileHash"
    FLEX_DB_VERSION = "FlexDBVersion"
    SOURCE_DB = "Source"
    TARGET_DB = "Target"

    def __init__(self, rules_file_path: str):
        """Initialize sync manager for a Rule Assistant rules file.

        Args:
            rules_file_path: Path to RuleAssistantRules.xml
        """
        self.rules_file_path = rules_file_path
        self.metadata: Optional[FileMetadata] = None

    def compute_file_hash(self, file_path: str) -> str:
        """Compute SHA-256 hash of a file.

        Args:
            file_path: Path to file to hash

        Returns:
            Hex string of file hash
        """
        if not os.path.exists(file_path):
            return ""

        sha256_hash = hashlib.sha256()

        try:
            with open(file_path, "rb") as f:
                # Read in chunks for large files
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)

            return sha256_hash.hexdigest()

        except Exception as e:
            # If we can't read the file, return empty hash
            return ""

    def get_flex_stats(self, db_start_data) -> FlexStats:
        """Extract statistics from a DBStartData object.

        Args:
            db_start_data: DBStartData object from GetStartData()

        Returns:
            FlexStats object with counts
        """
        return FlexStats(
            project_name=db_start_data.projectName,
            category_count=len(db_start_data.categoryList),
            feature_count=len(db_start_data.featureList)
        )

    def load_metadata(self) -> Optional[FileMetadata]:
        """Load metadata from the Rule Assistant rules file.

        Returns:
            FileMetadata if found, None otherwise
        """
        if not os.path.exists(self.rules_file_path):
            return None

        try:
            tree = ET.parse(self.rules_file_path)
            root = tree.getroot()

            metadata_el = root.find(self.METADATA_ROOT)
            if metadata_el is None:
                return None

            # Parse datetime fields
            created = self._parse_datetime(metadata_el.findtext(self.CREATED, ""))
            last_modified = self._parse_datetime(metadata_el.findtext(self.LAST_MODIFIED, ""))
            last_sync = self._parse_datetime(metadata_el.findtext(self.LAST_SYNC, ""))

            # Parse transfer file info
            transfer_el = metadata_el.find(self.TRANSFER_FILE)
            transfer_path = transfer_el.get('path', '') if transfer_el is not None else ''
            transfer_hash = metadata_el.findtext(self.TRANSFER_FILE_HASH, None)

            # Parse FLEx DB info
            flex_el = metadata_el.find(self.FLEX_DB_VERSION)
            source_el = flex_el.find(self.SOURCE_DB) if flex_el is not None else None
            target_el = flex_el.find(self.TARGET_DB) if flex_el is not None else None

            source_name = source_el.get('name', '') if source_el is not None else ''
            source_cats = int(source_el.get('categories', '0')) if source_el is not None else 0
            source_feats = int(source_el.get('features', '0')) if source_el is not None else 0

            target_name = target_el.get('name', '') if target_el is not None else ''
            target_cats = int(target_el.get('categories', '0')) if target_el is not None else 0
            target_feats = int(target_el.get('features', '0')) if target_el is not None else 0

            metadata = FileMetadata(
                created=created or datetime.now(),
                last_modified=last_modified or datetime.now(),
                last_sync=last_sync or datetime.now(),
                transfer_file_path=transfer_path,
                transfer_file_hash=transfer_hash,
                source_db_name=source_name,
                source_category_count=source_cats,
                source_feature_count=source_feats,
                target_db_name=target_name,
                target_category_count=target_cats,
                target_feature_count=target_feats
            )

            self.metadata = metadata
            return metadata

        except Exception as e:
            # If parsing fails, treat as missing metadata
            return None

    def save_metadata(self, metadata: FileMetadata) -> bool:
        """Save metadata to the Rule Assistant rules file.

        Args:
            metadata: FileMetadata to save

        Returns:
            True if successful, False otherwise
        """
        try:
            # Load or create the rules file
            if os.path.exists(self.rules_file_path):
                parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
                tree = ET.parse(self.rules_file_path, parser=parser)
                root = tree.getroot()
            else:
                root = ET.Element('FLExTransRules')
                tree = ET.ElementTree(root)

            # Remove old metadata if present
            old_metadata = root.find(self.METADATA_ROOT)
            if old_metadata is not None:
                root.remove(old_metadata)

            # Create new metadata element (insert at beginning)
            metadata_el = ET.Element(self.METADATA_ROOT)
            root.insert(0, metadata_el)

            # Add timestamp fields
            ET.SubElement(metadata_el, self.CREATED).text = self._format_datetime(metadata.created)
            ET.SubElement(metadata_el, self.LAST_MODIFIED).text = self._format_datetime(metadata.last_modified)
            ET.SubElement(metadata_el, self.LAST_SYNC).text = self._format_datetime(metadata.last_sync)

            # Add transfer file info
            ET.SubElement(metadata_el, self.TRANSFER_FILE, path=metadata.transfer_file_path)
            if metadata.transfer_file_hash:
                ET.SubElement(metadata_el, self.TRANSFER_FILE_HASH).text = metadata.transfer_file_hash

            # Add FLEx DB version info
            flex_el = ET.SubElement(metadata_el, self.FLEX_DB_VERSION)

            ET.SubElement(flex_el, self.SOURCE_DB,
                         name=metadata.source_db_name,
                         categories=str(metadata.source_category_count),
                         features=str(metadata.source_feature_count))

            ET.SubElement(flex_el, self.TARGET_DB,
                         name=metadata.target_db_name,
                         categories=str(metadata.target_category_count),
                         features=str(metadata.target_feature_count))

            # Write the file
            ET.indent(tree)
            tree.write(self.rules_file_path, encoding='utf-8', xml_declaration=True)

            self.metadata = metadata
            return True

        except Exception as e:
            return False

    def update_after_sync(self, transfer_file_path: str,
                         source_stats: FlexStats,
                         target_stats: FlexStats) -> bool:
        """Update metadata after a successful sync operation.

        Args:
            transfer_file_path: Path to transfer rules file
            source_stats: Current source DB statistics
            target_stats: Current target DB statistics

        Returns:
            True if successful
        """
        now = datetime.now()

        # Compute current hash of transfer file
        transfer_hash = self.compute_file_hash(transfer_file_path)

        if self.metadata is None:
            # First time - create new metadata
            metadata = FileMetadata(
                created=now,
                last_modified=now,
                last_sync=now,
                transfer_file_path=transfer_file_path,
                transfer_file_hash=transfer_hash,
                source_db_name=source_stats.project_name,
                source_category_count=source_stats.category_count,
                source_feature_count=source_stats.feature_count,
                target_db_name=target_stats.project_name,
                target_category_count=target_stats.category_count,
                target_feature_count=target_stats.feature_count
            )
        else:
            # Update existing metadata
            metadata = self.metadata
            metadata.last_modified = now
            metadata.last_sync = now
            metadata.transfer_file_path = transfer_file_path
            metadata.transfer_file_hash = transfer_hash
            metadata.source_db_name = source_stats.project_name
            metadata.source_category_count = source_stats.category_count
            metadata.source_feature_count = source_stats.feature_count
            metadata.target_db_name = target_stats.project_name
            metadata.target_category_count = target_stats.category_count
            metadata.target_feature_count = target_stats.feature_count

        return self.save_metadata(metadata)

    def detect_changes(self, transfer_file_path: str,
                      source_stats: FlexStats,
                      target_stats: FlexStats) -> List[ChangeDetectionResult]:
        """Detect changes that may affect Rule Assistant operation.

        Args:
            transfer_file_path: Path to transfer rules file
            source_stats: Current source DB statistics
            target_stats: Current target DB statistics

        Returns:
            List of detected changes
        """
        changes = []

        # Load metadata if not already loaded
        if self.metadata is None:
            self.load_metadata()

        # Check if this is first run
        if self.metadata is None:
            changes.append(ChangeDetectionResult(
                change_type=ChangeType.FIRST_RUN,
                message="First time running Rule Assistant for this project",
                details=["Metadata will be created to track file synchronization"],
                can_continue=True,
                recommended_action="Continue - metadata will be initialized"
            ))
            return changes

        # Check 1: Has transfer file been modified externally?
        if os.path.exists(transfer_file_path):
            current_hash = self.compute_file_hash(transfer_file_path)
            stored_hash = self.metadata.transfer_file_hash

            if stored_hash and current_hash != stored_hash:
                # File has been modified!
                changes.append(ChangeDetectionResult(
                    change_type=ChangeType.EXTERNAL_T1X_EDIT,
                    message="Transfer rules file has been modified outside Rule Assistant",
                    details=[
                        f"File: {transfer_file_path}",
                        f"Last known modification: {self.metadata.last_sync}",
                        "Your manual edits may be overwritten if you save rules"
                    ],
                    can_continue=True,
                    recommended_action="Create backup before continuing, or review changes first"
                ))

        # Check 2: Has source FLEx database changed?
        stored_source = FlexStats(
            project_name=self.metadata.source_db_name,
            category_count=self.metadata.source_category_count,
            feature_count=self.metadata.source_feature_count
        )

        if source_stats != stored_source:
            differences = stored_source.diff(source_stats)
            changes.append(ChangeDetectionResult(
                change_type=ChangeType.FLEX_DB_CHANGED,
                message="Source FLEx database has changed",
                details=[
                    f"Project: {source_stats.project_name}"
                ] + differences,
                can_continue=True,
                recommended_action="Continue - new data will be used"
            ))

        # Check 3: Has target FLEx database changed?
        stored_target = FlexStats(
            project_name=self.metadata.target_db_name,
            category_count=self.metadata.target_category_count,
            feature_count=self.metadata.target_feature_count
        )

        if target_stats != stored_target:
            differences = stored_target.diff(target_stats)
            changes.append(ChangeDetectionResult(
                change_type=ChangeType.FLEX_DB_CHANGED,
                message="Target FLEx database has changed",
                details=[
                    f"Project: {target_stats.project_name}"
                ] + differences,
                can_continue=True,
                recommended_action="Continue - new data will be used"
            ))

        return changes

    def format_changes_for_user(self, changes: List[ChangeDetectionResult]) -> str:
        """Format change detection results for display to user.

        Args:
            changes: List of detected changes

        Returns:
            Formatted string for user display
        """
        if not changes:
            return "No changes detected. All files are synchronized."

        lines = []
        lines.append("=" * 60)
        lines.append("FILE SYNCHRONIZATION STATUS")
        lines.append("=" * 60)
        lines.append("")

        for i, change in enumerate(changes, 1):
            # Get icon based on change type
            icon = "ℹ️" if change.change_type == ChangeType.FIRST_RUN else "⚠️"

            lines.append(f"{icon} {change.message}")
            lines.append("")

            if change.details:
                for detail in change.details:
                    lines.append(f"  • {detail}")
                lines.append("")

            if change.recommended_action:
                lines.append(f"  Recommended: {change.recommended_action}")
                lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)

    def _parse_datetime(self, dt_string: str) -> Optional[datetime]:
        """Parse ISO format datetime string.

        Args:
            dt_string: ISO format datetime string

        Returns:
            datetime object or None if parsing fails
        """
        if not dt_string:
            return None

        try:
            return datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        except:
            return None

    def _format_datetime(self, dt: datetime) -> str:
        """Format datetime as ISO string.

        Args:
            dt: datetime object

        Returns:
            ISO format string
        """
        return dt.isoformat() + 'Z'


# Example usage and testing
if __name__ == '__main__':
    import sys

    print("Rule Assistant Sync Manager - Proof of Concept")
    print("=" * 60)
    print()

    # Example: Create a sync manager for a rules file
    rules_file = "/path/to/RuleAssistantRules.xml"
    sync_manager = RuleAssistantSyncManager(rules_file)

    # Example: Create some mock FLEx stats
    source_stats = FlexStats(
        project_name="Kalaba",
        category_count=15,
        feature_count=32
    )

    target_stats = FlexStats(
        project_name="English",
        category_count=12,
        feature_count=28
    )

    # Example: Detect changes
    transfer_file = "/path/to/transfer_rules.t1x"
    changes = sync_manager.detect_changes(transfer_file, source_stats, target_stats)

    # Display results
    print(sync_manager.format_changes_for_user(changes))
    print()

    # Example: Update metadata after sync
    if sync_manager.update_after_sync(transfer_file, source_stats, target_stats):
        print("✓ Metadata updated successfully")
    else:
        print("✗ Failed to update metadata")

    print()
    print("=" * 60)
    print("Proof of concept complete!")
