"""
Tests for search_notes function
"""

import pytest
from unittest.mock import patch, Mock
from main import search_notes


class TestSearchNotes:
    """Test cases for search_notes function"""
    
    def test_search_notes_body_success(self, mock_notes_app, mock_noteslist):
        """Test successful body content search"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("hashtag", limit=10, search_type="body")
        
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
        
        # Verify NotesApp was called with correct parameters
        mock_notes_app.noteslist.assert_called_once_with(body=["hashtag"])
    
    def test_search_notes_name_search(self, mock_notes_app, mock_noteslist):
        """Test name/title search"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("Meeting", search_type="name")
        
        assert result["search_type"] == "name"
        mock_notes_app.noteslist.assert_called_once_with(name=["Meeting"])
    
    def test_search_notes_with_limit(self, mock_notes_app, mock_noteslist):
        """Test search with custom limit"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("test", limit=2, search_type="body")
        
        assert result["found_count"] == 2
        assert len(result["notes"]) == 2
    
    def test_search_notes_hashtag_search(self, mock_notes_app, mock_noteslist):
        """Test hashtag search (starts with #)"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("#work", search_type="body")
        
        assert result["query"] == "#work"
        mock_notes_app.noteslist.assert_called_once_with(body=["#work"])
    
    def test_search_notes_empty_query(self, mock_notes_app):
        """Test search with empty query"""
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("", search_type="body")
        
        assert result["found_count"] == 0
        assert result["notes"] == []
        assert result["search_type"] == "empty"
        assert "Empty search query" in result["message"]
        
        # Should not call noteslist for empty query
        mock_notes_app.noteslist.assert_not_called()
    
    def test_search_notes_whitespace_query(self, mock_notes_app):
        """Test search with whitespace-only query"""
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("   ", search_type="body")
        
        assert result["found_count"] == 0
        assert result["search_type"] == "empty"
    
    def test_search_notes_limit_validation(self, mock_notes_app, mock_noteslist):
        """Test limit parameter validation"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            # Test minimum limit
            result = search_notes("test", limit=0)
            assert len(result["notes"]) == 1  # Should be corrected to 1
            
            # Test maximum limit
            result = search_notes("test", limit=200)
            assert len(result["notes"]) == 3  # Limited by available notes
    
    def test_search_notes_invalid_search_type(self, mock_notes_app, mock_noteslist):
        """Test with invalid search_type parameter"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("test", search_type="invalid")
        
        # Should default to "body"
        assert result["search_type"] == "body"
        mock_notes_app.noteslist.assert_called_once_with(body=["test"])
    
    def test_search_notes_no_results(self, mock_notes_app):
        """Test search with no matching results"""
        mock_empty_noteslist = Mock()
        mock_empty_noteslist.name = []
        mock_empty_noteslist.id = []
        mock_empty_noteslist.__len__ = Mock(return_value=0)
        
        mock_notes_app.noteslist.return_value = mock_empty_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("nonexistent", search_type="body")
        
        assert result["found_count"] == 0
        assert result["notes"] == []
        assert "Found 0 notes matching" in result["message"]
    
    def test_search_notes_import_error(self):
        """Test handling of import error"""
        with patch('macnotesapp.NotesApp', side_effect=ImportError("macnotesapp not available")):
            result = search_notes("test", search_type="body")
        
        assert result["found_count"] == 0
        assert result["notes"] == []
        assert result["search_type"] == "error"
        assert "macnotesapp package not available" in result["error"]
    
    def test_search_notes_general_exception(self, mock_notes_app):
        """Test handling of general exceptions during search"""
        mock_notes_app.noteslist.side_effect = Exception("Search failed")
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("test", search_type="body")
        
        assert result["found_count"] == 0
        assert result["notes"] == []
        assert result["search_type"] == "error"
        assert "Error with noteslist search" in result["error"]
    
    def test_search_notes_with_none_titles(self, mock_notes_app):
        """Test handling of notes with None titles in search results"""
        mock_noteslist_with_none = Mock()
        mock_noteslist_with_none.name = [None, "Valid Note"]
        mock_noteslist_with_none.id = ["id1", "id2"]
        mock_noteslist_with_none.__len__ = Mock(return_value=2)
        
        mock_notes_app.noteslist.return_value = mock_noteslist_with_none
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("test", search_type="body")
        
        assert result["found_count"] == 2
        assert result["notes"][0]["title"] == "Untitled"  # None should become "Untitled"
        assert result["notes"][1]["title"] == "Valid Note"
    
    def test_search_notes_default_parameters(self, mock_notes_app, mock_noteslist):
        """Test search with default parameters"""
        mock_notes_app.noteslist.return_value = mock_noteslist
        
        with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
            result = search_notes("test")  # No limit or search_type specified
        
        # Should use defaults: limit=10, search_type="body"
        assert result["search_type"] == "body"
        assert len(result["notes"]) <= 10  # Should respect default limit
        mock_notes_app.noteslist.assert_called_once_with(body=["test"])