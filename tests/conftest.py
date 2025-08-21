"""
Pytest configuration and fixtures for Apple Notes MCP tests
"""

from datetime import datetime
from unittest.mock import Mock

import pytest


@pytest.fixture
def mock_notes_app():
    """Mock NotesApp instance"""
    mock_app = Mock()
    return mock_app


@pytest.fixture
def mock_noteslist():
    """Mock NotesList object with sample data"""
    mock_noteslist = Mock()

    # Sample data
    mock_noteslist.name = ["Test Note 1", "Test Note 2", "Meeting Notes"]
    mock_noteslist.id = [
        "x-coredata://test/ICNote/p1",
        "x-coredata://test/ICNote/p2",
        "x-coredata://test/ICNote/p3",
    ]
    mock_noteslist.body = [
        "<div>This is test note 1 content</div>",
        "<div>This is test note 2 with #hashtag</div>",
        "<div>Meeting notes for project #work</div>",
    ]
    mock_noteslist.plaintext = [
        "This is test note 1 content",
        "This is test note 2 with #hashtag",
        "Meeting notes for project #work",
    ]
    mock_noteslist.creation_date = [
        datetime(2025, 1, 1, 10, 0, 0),
        datetime(2025, 1, 2, 11, 0, 0),
        datetime(2025, 1, 3, 12, 0, 0),
    ]
    mock_noteslist.modification_date = [
        datetime(2025, 1, 1, 10, 30, 0),
        datetime(2025, 1, 2, 11, 30, 0),
        datetime(2025, 1, 3, 12, 30, 0),
    ]
    # Create mock accounts and folders with proper name attributes
    mock_account1 = Mock()
    mock_account1.name = "iCloud"
    mock_account2 = Mock()
    mock_account2.name = "iCloud"
    mock_account3 = Mock()
    mock_account3.name = "Local"

    mock_folder1 = Mock()
    mock_folder1.name = "Notes"
    mock_folder2 = Mock()
    mock_folder2.name = "Personal"
    mock_folder3 = Mock()
    mock_folder3.name = "Work"

    mock_noteslist.account = [mock_account1, mock_account2, mock_account3]
    mock_noteslist.folder = [mock_folder1, mock_folder2, mock_folder3]
    mock_noteslist.password_protected = [False, False, True]

    # Mock len() method
    mock_noteslist.__len__ = Mock(return_value=3)

    return mock_noteslist


@pytest.fixture
def mock_account():
    """Mock Account object for note creation"""
    mock_account = Mock()

    # Mock make_note method
    mock_note = Mock()
    mock_note.name = "New Test Note"
    mock_note.id = "x-coredata://test/ICNote/p999"
    mock_note.plaintext = "This is a new test note"
    mock_note.creation_date = datetime(2025, 1, 15, 14, 0, 0)
    mock_account = Mock()
    mock_account.name = "iCloud"
    mock_folder = Mock()
    mock_folder.name = "Notes"
    mock_note.account = mock_account
    mock_note.folder = mock_folder

    mock_account.make_note.return_value = mock_note

    return mock_account


@pytest.fixture
def sample_note_ids():
    """Sample note IDs for testing"""
    return [
        "x-coredata://test/ICNote/p1",
        "x-coredata://test/ICNote/p2",
        "x-coredata://test/ICNote/p3",
    ]


@pytest.fixture
def mock_apple_notes_parser():
    """Mock AppleNotesParser instance"""
    mock_parser = Mock()
    return mock_parser


@pytest.fixture
def mock_note_objects():
    """Mock Note objects for apple-notes-parser"""
    mock_notes = []

    # Create mock notes matching the data from mock_noteslist
    for i, (title, note_id) in enumerate(
        [
            ("Test Note 1", "x-coredata://test/ICNote/p1"),
            ("Test Note 2", "x-coredata://test/ICNote/p2"),
            ("Meeting Notes", "x-coredata://test/ICNote/p3"),
        ]
    ):
        mock_note = Mock()
        mock_note.title = title
        mock_note.applescript_id = note_id
        mock_note.body = f"<div>This is {title.lower()} content</div>"
        mock_note.plaintext = f"This is {title.lower()} content"
        mock_note.creation_date = datetime(2025, 1, i + 1, 10, 0, 0)
        mock_note.modification_date = datetime(2025, 1, i + 1, 10, 30, 0)
        mock_notes.append(mock_note)

    return mock_notes


@pytest.fixture
def mock_note_objects_with_integer_ids():
    """Mock Note objects with integer IDs (like real apple-notes-parser returns)"""
    mock_notes = []

    # Create mock notes with integer IDs to test conversion
    for i, (title, note_id) in enumerate(
        [
            ("Test Note 1", 2436),
            ("Test Note 2", 2437),
            ("Meeting Notes", 2597),
        ]
    ):
        mock_note = Mock()
        mock_note.title = title
        mock_note.applescript_id = note_id  # Integer ID like real apple-notes-parser
        mock_note.body = f"<div>This is {title.lower()} content</div>"
        mock_note.plaintext = f"This is {title.lower()} content"
        mock_note.creation_date = datetime(2025, 1, i + 1, 10, 0, 0)
        mock_note.modification_date = datetime(2025, 1, i + 1, 10, 30, 0)
        mock_notes.append(mock_note)

    return mock_notes
