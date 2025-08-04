"""
Tests for search_notes function
"""

from unittest.mock import Mock, patch

from main import search_notes


class TestSearchNotes:
    """Test cases for search_notes function"""

    def test_search_notes_body_success(
        self, mock_notes_app, mock_noteslist, mock_note_objects
    ):
        """Test successful body content search"""
        mock_parser = Mock()
        mock_parser.search_notes.return_value = mock_note_objects

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = search_notes("hashtag", limit=10)

        # Verify the result structure
        assert "notes" in result
        assert "found_count" in result
        assert "query" in result
        assert "search_type" in result
        assert "message" in result

        assert result["query"] == "hashtag"
        assert result["search_type"] == "body"
        assert result["found_count"] == 3
        assert len(result["notes"]) == 3

        # Verify note structure
        assert all("title" in note and "id" in note for note in result["notes"])

        # Verify AppleNotesParser was called with correct parameters
        mock_parser.search_notes.assert_called_once_with("hashtag")

    def test_search_notes_body_content(
        self, mock_notes_app, mock_noteslist, mock_note_objects
    ):
        """Test body content search"""
        mock_parser = Mock()
        mock_parser.search_notes.return_value = mock_note_objects[:1]

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = search_notes("Meeting")

        assert result["search_type"] == "body"
        assert result["found_count"] == 1
        mock_parser.search_notes.assert_called_once_with("Meeting")

    def test_search_notes_with_limit(
        self, mock_notes_app, mock_noteslist, mock_note_objects
    ):
        """Test search with custom limit"""
        mock_parser = Mock()
        mock_parser.search_notes.return_value = mock_note_objects

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = search_notes("test", limit=2)

        assert result["found_count"] == 2
        assert len(result["notes"]) == 2

    def test_search_notes_hashtag_search(
        self, mock_notes_app, mock_noteslist, mock_note_objects
    ):
        """Test hashtag search (starts with #)"""
        mock_parser = Mock()
        mock_parser.get_notes_by_tag.return_value = mock_note_objects

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = search_notes("#work")

        assert result["query"] == "#work"
        mock_parser.get_notes_by_tag.assert_called_once_with("work")

    def test_search_notes_empty_query(self, mock_notes_app):
        """Test search with empty query"""
        result = search_notes("")

        assert result["found_count"] == 0
        assert result["notes"] == []
        assert result["search_type"] == "empty"
        assert "Empty search query" in result["message"]

    def test_search_notes_whitespace_query(self, mock_notes_app):
        """Test search with whitespace-only query"""
        result = search_notes("   ")

        assert result["found_count"] == 0
        assert result["search_type"] == "empty"

    def test_search_notes_limit_validation(
        self, mock_notes_app, mock_noteslist, mock_note_objects
    ):
        """Test limit parameter validation"""
        mock_parser = Mock()
        mock_parser.search_notes.return_value = mock_note_objects

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            # Test minimum limit
            result = search_notes("test", limit=0)
            assert len(result["notes"]) == 1  # Should be corrected to 1

            # Test maximum limit
            result = search_notes("test", limit=200)
            assert len(result["notes"]) == 3  # Limited by available notes

    def test_search_notes_no_results(self, mock_notes_app):
        """Test search with no matching results"""
        mock_parser = Mock()
        mock_parser.search_notes.return_value = []

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = search_notes("nonexistent")

        assert result["found_count"] == 0
        assert result["notes"] == []
        assert "Found 0 notes matching" in result["message"]

    def test_search_notes_import_error(self):
        """Test handling of import error"""
        with patch(
            "apple_notes_parser.AppleNotesParser",
            side_effect=ImportError("apple-notes-parser not available")
        ):
            result = search_notes("test")

        assert result["found_count"] == 0
        assert result["notes"] == []
        assert result["search_type"] == "error"

    def test_search_notes_general_exception(self, mock_notes_app):
        """Test handling of general exceptions during search"""
        with patch(
            "apple_notes_parser.AppleNotesParser",
            side_effect=Exception("Database failed")
        ):
            result = search_notes("test")

        assert result["found_count"] == 0
        assert result["notes"] == []
        assert result["search_type"] == "error"

    def test_search_notes_with_none_titles(self, mock_notes_app):
        """Test handling of notes with None titles in search results"""
        mock_note1 = Mock()
        mock_note1.title = None
        mock_note1.id = "id1"

        mock_note2 = Mock()
        mock_note2.title = "Valid Note"
        mock_note2.id = "id2"

        mock_parser = Mock()
        mock_parser.search_notes.return_value = [mock_note1, mock_note2]

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = search_notes("test")

        assert result["found_count"] == 2
        assert (
            result["notes"][0]["title"] == "Untitled"
        )  # None should become "Untitled"
        assert result["notes"][1]["title"] == "Valid Note"

    def test_search_notes_default_parameters(
        self, mock_notes_app, mock_noteslist, mock_note_objects
    ):
        """Test search with default parameters"""
        mock_parser = Mock()
        mock_parser.search_notes.return_value = mock_note_objects

        with patch("apple_notes_parser.AppleNotesParser", return_value=mock_parser):
            result = search_notes("test")  # No limit specified

        # Should use defaults: limit=10
        assert result["search_type"] == "body"
        assert len(result["notes"]) <= 10  # Should respect default limit
        mock_parser.search_notes.assert_called_once_with("test")
