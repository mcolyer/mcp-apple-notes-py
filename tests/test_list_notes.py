"""
Tests for list_notes function
"""

from unittest.mock import Mock, patch

from main import list_notes


class TestListNotes:
    """Test cases for list_notes function"""

    def test_list_notes_success(self, mock_notes_app, mock_noteslist):
        """Test successful note listing"""
        mock_notes_app.noteslist.return_value = mock_noteslist

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
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

        # Verify NotesApp was called correctly
        mock_notes_app.noteslist.assert_called_once_with()

    def test_list_notes_with_limit(self, mock_notes_app, mock_noteslist):
        """Test note listing with custom limit"""
        mock_notes_app.noteslist.return_value = mock_noteslist

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            result = list_notes(limit=2)

        # Should only return 2 notes even though 3 are available
        assert len(result) == 2
        assert result[0]["title"] == "Test Note 1"
        assert result[1]["title"] == "Test Note 2"

    def test_list_notes_empty_result(self, mock_notes_app):
        """Test when no notes are found"""
        mock_empty_noteslist = Mock()
        mock_empty_noteslist.name = []
        mock_empty_noteslist.id = []
        mock_empty_noteslist.__len__ = Mock(return_value=0)

        mock_notes_app.noteslist.return_value = mock_empty_noteslist

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            result = list_notes()

        assert result == []

    def test_list_notes_limit_validation(self, mock_notes_app, mock_noteslist):
        """Test limit parameter validation"""
        mock_notes_app.noteslist.return_value = mock_noteslist

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            # Test minimum limit
            result = list_notes(limit=0)
            assert len(result) == 1  # Should be corrected to 1

            # Test maximum limit
            result = list_notes(limit=2000)
            assert len(result) == 3  # Should be limited by available notes

    def test_list_notes_with_none_names(self, mock_notes_app):
        """Test handling of notes with None names"""
        mock_noteslist_with_none = Mock()
        mock_noteslist_with_none.name = [None, "Valid Note", ""]
        mock_noteslist_with_none.id = ["id1", "id2", "id3"]
        mock_noteslist_with_none.__len__ = Mock(return_value=3)

        mock_notes_app.noteslist.return_value = mock_noteslist_with_none

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            result = list_notes(limit=3)

        assert len(result) == 3
        assert result[0]["title"] == "Untitled"  # None should become "Untitled"
        assert result[1]["title"] == "Valid Note"
        assert result[2]["title"] == "Untitled"  # Empty string should become "Untitled"

    def test_list_notes_import_error(self):
        """Test handling of import error"""
        with patch(
            "macnotesapp.NotesApp", side_effect=ImportError("macnotesapp not available")
        ):
            result = list_notes()

        assert result == []

    def test_list_notes_general_exception(self, mock_notes_app):
        """Test handling of general exceptions"""
        mock_notes_app.noteslist.side_effect = Exception("Connection failed")

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            result = list_notes()

        assert result == []

    def test_list_notes_individual_note_error(self, mock_notes_app):
        """Test handling of individual note processing errors"""
        mock_noteslist_with_error = Mock()
        mock_noteslist_with_error.name = [
            "Good Note",
            None,
        ]  # Second will cause error in zip
        mock_noteslist_with_error.id = ["id1"]  # Mismatched lengths
        mock_noteslist_with_error.__len__ = Mock(return_value=2)

        mock_notes_app.noteslist.return_value = mock_noteslist_with_error

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            result = list_notes(limit=2)

        # Should handle the error gracefully and return what it can
        assert len(result) >= 1
        assert result[0]["title"] == "Good Note"
