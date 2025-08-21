"""
Tests for list_notes function
"""

from unittest.mock import Mock, patch

from main import list_notes


class TestListNotes:
    """Test cases for list_notes function"""

    def test_list_notes_success(
        self, mock_notes_app, mock_noteslist, mock_note_objects
    ):
        """Test successful note listing"""
        mock_parser = Mock()
        mock_parser.notes = mock_note_objects[:3]  # Limit to 3 notes

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes(limit=3)

        # Verify the result
        assert len(result) == 3
        assert result[0] == {
            "title": "Test Note 1",
            "id": "x-coredata://test/ICNote/p1",
        }
        assert result[1] == {
            "title": "Test Note 2",
            "id": "x-coredata://test/ICNote/p2",
        }
        assert result[2] == {
            "title": "Meeting Notes",
            "id": "x-coredata://test/ICNote/p3",
        }

        # Verify AppleNotesParser was called correctly
        mock_parser.load_data.assert_called_once()

    def test_list_notes_with_limit(
        self, mock_notes_app, mock_noteslist, mock_note_objects
    ):
        """Test note listing with custom limit"""
        mock_parser = Mock()
        mock_parser.notes = mock_note_objects

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes(limit=2)

        # Should only return 2 notes even though 3 are available
        assert len(result) == 2
        assert result[0]["title"] == "Test Note 1"
        assert result[1]["title"] == "Test Note 2"

    def test_list_notes_empty_result(self, mock_notes_app):
        """Test when no notes are found"""
        mock_parser = Mock()
        mock_parser.notes = []

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes()

        assert result == []

    def test_list_notes_limit_validation(
        self, mock_notes_app, mock_noteslist, mock_note_objects
    ):
        """Test limit parameter validation"""
        mock_parser = Mock()
        mock_parser.notes = mock_note_objects

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            # Test minimum limit
            result = list_notes(limit=0)
            assert len(result) == 1  # Should be corrected to 1

            # Test maximum limit
            result = list_notes(limit=2000)
            assert len(result) == 3  # Should be limited by available notes

    def test_list_notes_with_none_names(self, mock_notes_app):
        """Test handling of notes with None names"""
        # Create mock notes with None and empty titles
        mock_notes = []
        for i, title in enumerate([None, "Valid Note", ""]):
            mock_note = Mock()
            mock_note.title = title
            mock_note.applescript_id = f"id{i + 1}"
            mock_notes.append(mock_note)

        mock_parser = Mock()
        mock_parser.notes = mock_notes

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes(limit=3)

        assert len(result) == 3
        assert result[0]["title"] == "Untitled"  # None should become "Untitled"
        assert result[1]["title"] == "Valid Note"
        assert result[2]["title"] == "Untitled"  # Empty string should become "Untitled"

    def test_list_notes_import_error(self):
        """Test handling of import error"""
        with (
            patch(
                "apple_notes_parser.AppleNotesParser",
                side_effect=ImportError("apple-notes-parser not available"),
            ),
            patch(
                "macnotesapp.NotesApp",
                side_effect=ImportError("macnotesapp not available"),
            ),
        ):
            result = list_notes()

        assert result == []

    def test_list_notes_general_exception(self, mock_notes_app):
        """Test handling of general exceptions"""
        mock_notes_app.noteslist.side_effect = Exception("Connection failed")

        with (
            patch(
                "apple_notes_parser.AppleNotesParser",
                side_effect=Exception("Database failed"),
            ),
            patch("macnotesapp.NotesApp", return_value=mock_notes_app),
        ):
            result = list_notes()

        assert result == []

    def test_list_notes_individual_note_error(self, mock_notes_app):
        """Test handling of individual note processing errors"""
        # Create mock notes where one will cause an error
        mock_note1 = Mock()
        mock_note1.title = "Good Note"
        mock_note1.applescript_id = "id1"

        mock_note2 = Mock()
        mock_note2.title = Mock(
            side_effect=Exception("Note error")
        )  # This will cause an error
        mock_note2.applescript_id = "id2"

        mock_parser = Mock()
        mock_parser.notes = [mock_note1, mock_note2]

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes(limit=2)

        # Should handle the error gracefully and return what it can
        assert len(result) >= 1
        assert result[0]["title"] == "Good Note"

    def test_list_notes_with_folder_filter(self, mock_notes_app, mock_note_objects):
        """Test note listing with folder filtering"""
        # Create mock notes with folder attributes
        mock_note1 = Mock()
        mock_note1.title = "Work Note"
        mock_note1.applescript_id = "id1"
        mock_note1.folder_name = "Work"
        mock_note1.folder = Mock()
        mock_note1.folder.name = "Work"

        mock_note2 = Mock()
        mock_note2.title = "Personal Note"
        mock_note2.applescript_id = "id2"
        mock_note2.folder_name = "Personal"
        mock_note2.folder = Mock()
        mock_note2.folder.name = "Personal"

        mock_note3 = Mock()
        mock_note3.title = "Another Work Note"
        mock_note3.applescript_id = "id3"
        mock_note3.folder_name = "Work Projects"
        mock_note3.folder = Mock()
        mock_note3.folder.name = "Work Projects"

        mock_parser = Mock()
        mock_parser.notes = [mock_note1, mock_note2, mock_note3]

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes(limit=10, folder="work")

        # Should only return notes with "work" in folder name (case-insensitive)
        assert len(result) == 2
        assert result[0]["title"] == "Work Note"
        assert result[1]["title"] == "Another Work Note"

    def test_list_notes_folder_filter_no_matches(
        self, mock_notes_app, mock_note_objects
    ):
        """Test folder filtering with no matching notes"""
        mock_parser = Mock()
        mock_parser.notes = mock_note_objects  # Default notes without folder filtering

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes(limit=10, folder="nonexistent")

        # Should return empty list when no notes match folder
        assert result == []

    def test_list_notes_folder_filter_error_handling(self, mock_notes_app):
        """Test folder filtering with error in folder attribute access"""
        # Create a note that will cause an error when accessing folder
        mock_note1 = Mock()
        mock_note1.title = "Good Note"
        mock_note1.applescript_id = "id1"
        mock_note1.folder_name = "Work"

        mock_note2 = Mock()
        mock_note2.title = "Error Note"
        mock_note2.applescript_id = "id2"
        # This note will cause an error when accessing folder_name
        mock_note2.folder_name = Mock(side_effect=Exception("Folder error"))
        mock_note2.folder = Mock(side_effect=Exception("Folder error"))

        mock_parser = Mock()
        mock_parser.notes = [mock_note1, mock_note2]

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes(limit=10, folder="work")

        # Should continue processing despite error and return the good note
        assert len(result) == 1
        assert result[0]["title"] == "Good Note"

    def test_list_notes_integer_id_conversion(
        self, mock_notes_app, mock_note_objects_with_integer_ids
    ):
        """Test that integer IDs from apple-notes-parser are converted to strings"""
        mock_parser = Mock()
        mock_parser.notes = mock_note_objects_with_integer_ids

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes(limit=3)

        # Verify that all IDs are strings, not integers
        assert len(result) == 3
        for note in result:
            assert isinstance(note["id"], str), (
                f"ID {note['id']} should be string, got {type(note['id'])}"
            )
            assert note["id"].isdigit(), f"ID {note['id']} should be numeric string"

        # Check specific conversions
        assert result[0]["id"] == "2436"
        assert result[1]["id"] == "2437"
        assert result[2]["id"] == "2597"

    def test_list_notes_none_id_handling(self, mock_notes_app):
        """Test handling of None IDs from apple-notes-parser"""
        # Create a note with None ID
        mock_note = Mock()
        mock_note.title = "Note with None ID"
        mock_note.applescript_id = None

        mock_parser = Mock()
        mock_parser.notes = [mock_note]

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = list_notes(limit=1)

        # Should handle None ID gracefully
        assert len(result) == 1
        assert result[0]["title"] == "Note with None ID"
        assert result[0]["id"] == "unknown"
        assert isinstance(result[0]["id"], str)
