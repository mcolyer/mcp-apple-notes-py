"""
Tests for get_notes function
"""

import pytest
from unittest.mock import patch, Mock
from main import get_notes


class TestGetNotes:
    """Test cases for get_notes function"""
    
    def test_get_notes_success(self, mock_notes_app, mock_noteslist, sample_note_ids):
        """Test successful note retrieval"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes(sample_note_ids[:2])  # Get first 2 notes
        
        # Verify the result structure
        assert "notes" in result
        assert "found_count" in result
        assert "not_found" in result
        assert "message" in result
        
        assert result["found_count"] == 2
        assert len(result["notes"]) == 2
        assert len(result["not_found"]) == 0
        
        # Verify note structure
        note = result["notes"][0]
        assert "name" in note
        assert "id" in note
        assert "body" in note
        assert "plaintext" in note
        assert "creation_date" in note
        assert "modification_date" in note
        assert "account" in note
        assert "folder" in note
        assert "password_protected" in note
        
        # Verify NotesApp was called with correct parameters
        mock_notes_app.noteslist.assert_called_once_with(id=sample_note_ids[:2])
    
    def test_get_notes_single_note(self, mock_notes_app, mock_noteslist):
        """Test retrieving a single note"""
        # Mock noteslist to return only one note
        single_note_list = Mock()
        single_note_list.name = ["Single Note"]
        single_note_list.id = ["x-coredata://test/ICNote/p1"]
        single_note_list.body = ["<div>Single note content</div>"]
        single_note_list.plaintext = ["Single note content"]
        single_note_list.creation_date = [mock_noteslist.creation_date[0]]
        single_note_list.modification_date = [mock_noteslist.modification_date[0]]
        single_note_list.account = [mock_noteslist.account[0]]
        single_note_list.folder = [mock_noteslist.folder[0]]
        single_note_list.password_protected = [False]
        single_note_list.__len__ = Mock(return_value=1)
        
        mock_notes_app.noteslist.return_value = single_note_list
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes(["x-coredata://test/ICNote/p1"])
        
        assert result["found_count"] == 1
        assert len(result["notes"]) == 1
        assert result["notes"][0]["name"] == "Single Note"
    
    def test_get_notes_not_found(self, mock_notes_app):
        """Test retrieving non-existent notes"""
        # Mock empty noteslist
        empty_noteslist = Mock()
        empty_noteslist.name = []
        empty_noteslist.id = []
        empty_noteslist.body = []
        empty_noteslist.plaintext = []
        empty_noteslist.creation_date = []
        empty_noteslist.modification_date = []
        empty_noteslist.account = []
        empty_noteslist.folder = []
        empty_noteslist.password_protected = []
        empty_noteslist.__len__ = Mock(return_value=0)
        
        mock_notes_app.noteslist.return_value = empty_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes(["nonexistent-id"])
        
        assert result["found_count"] == 0
        assert len(result["notes"]) == 0
        assert len(result["not_found"]) == 1
        assert "nonexistent-id" in result["not_found"]
    
    def test_get_notes_partial_found(self, mock_notes_app, mock_noteslist):
        """Test retrieving mix of existing and non-existent notes"""
        # Mock noteslist to return only one of two requested notes
        partial_noteslist = Mock()
        partial_noteslist.name = ["Found Note"]
        partial_noteslist.id = ["x-coredata://test/ICNote/p1"]
        partial_noteslist.body = ["<div>Found content</div>"]
        partial_noteslist.plaintext = ["Found content"]
        partial_noteslist.creation_date = [mock_noteslist.creation_date[0]]
        partial_noteslist.modification_date = [mock_noteslist.modification_date[0]]
        partial_noteslist.account = [mock_noteslist.account[0]]
        partial_noteslist.folder = [mock_noteslist.folder[0]]
        partial_noteslist.password_protected = [False]
        partial_noteslist.__len__ = Mock(return_value=1)
        
        mock_notes_app.noteslist.return_value = partial_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes(["x-coredata://test/ICNote/p1", "nonexistent-id"])
        
        assert result["found_count"] == 1
        assert len(result["notes"]) == 1
        assert len(result["not_found"]) == 1
        assert "nonexistent-id" in result["not_found"]
    
    def test_get_notes_empty_input(self, mock_notes_app):
        """Test with empty IDs list"""
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes([])
        
        assert result["found_count"] == 0
        assert result["notes"] == []
        assert result["not_found"] == []
        assert "No IDs provided" in result["message"]
        
        # Should not call noteslist for empty input
        mock_notes_app.noteslist.assert_not_called()
    
    def test_get_notes_date_formatting(self, mock_notes_app, mock_noteslist):
        """Test that dates are properly formatted to ISO format"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes(["x-coredata://test/ICNote/p1"])
        
        note = result["notes"][0]
        assert note["creation_date"] == "2025-01-01T10:00:00"
        assert note["modification_date"] == "2025-01-01T10:30:00"
    
    def test_get_notes_account_and_folder_names(self, mock_notes_app, mock_noteslist):
        """Test proper handling of account and folder names"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes(["x-coredata://test/ICNote/p1"])
        
        note = result["notes"][0]
        assert note["account"] == "iCloud"  # From mock fixture
        assert note["folder"] == "Notes"    # From mock fixture
    
    def test_get_notes_none_values_handling(self, mock_notes_app):
        """Test handling of None values in note attributes"""
        noteslist_with_nones = Mock()
        noteslist_with_nones.name = [None]
        noteslist_with_nones.id = ["test-id"]
        noteslist_with_nones.body = [None]
        noteslist_with_nones.plaintext = [None]
        noteslist_with_nones.creation_date = [None]
        noteslist_with_nones.modification_date = [None]
        noteslist_with_nones.account = [None]
        noteslist_with_nones.folder = [None]
        noteslist_with_nones.password_protected = [False]
        noteslist_with_nones.__len__ = Mock(return_value=1)
        
        mock_notes_app.noteslist.return_value = noteslist_with_nones
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes(["test-id"])
        
        note = result["notes"][0]
        assert note["name"] == "Untitled"
        assert note["body"] == ""
        assert note["plaintext"] == ""
        assert note["creation_date"] is None
        assert note["modification_date"] is None
        assert note["account"] == "Unknown"
        assert note["folder"] == "Unknown"
    
    def test_get_notes_import_error(self):
        """Test handling of import error"""
        with patch('macnotesapp.NotesApp', side_effect=ImportError("macnotesapp not available")):
            result = get_notes(["test-id"])
        
        assert result["found_count"] == 0
        assert result["notes"] == []
        assert result["not_found"] == ["test-id"]
        assert "macnotesapp package not available" in result["error"]
    
    def test_get_notes_general_exception(self, mock_notes_app):
        """Test handling of general exceptions"""
        mock_notes_app.noteslist.side_effect = Exception("Connection failed")
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes(["test-id"])
        
        assert result["found_count"] == 0
        assert result["notes"] == []
        assert result["not_found"] == ["test-id"]
        assert "Error retrieving notes" in result["error"]
    
    def test_get_notes_individual_note_processing_error(self, mock_notes_app):
        """Test handling of errors during individual note processing"""
        problematic_noteslist = Mock()
        problematic_noteslist.name = ["Good Note"]
        problematic_noteslist.id = ["test-id"]
        problematic_noteslist.body = ["content"]
        problematic_noteslist.plaintext = ["content"]
        problematic_noteslist.creation_date = ["invalid-date"]  # This will cause error
        problematic_noteslist.modification_date = [None]
        problematic_noteslist.account = [Mock(name="iCloud")]
        problematic_noteslist.folder = [Mock(name="Notes")]
        problematic_noteslist.password_protected = [False]
        problematic_noteslist.__len__ = Mock(return_value=1)
        
        mock_notes_app.noteslist.return_value = problematic_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = get_notes(["test-id"])
        
        # Should handle the error and mark the note as not found
        assert result["found_count"] == 0
        assert "test-id" in result["not_found"]