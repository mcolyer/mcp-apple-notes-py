"""
Tests for create_note function
"""

from unittest.mock import Mock, patch

from main import create_note


class TestCreateNote:
    """Test cases for create_note function"""

    def test_create_note_success(self, mock_notes_app, mock_account):
        """Test successful note creation"""
        mock_notes_app.account.return_value = mock_account

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            with patch("main.markdown.Markdown") as mock_markdown:
                mock_md = Mock()
                mock_md.convert.return_value = "<h1>Test Note</h1><p>Content</p>"
                mock_markdown.return_value = mock_md

                result = create_note("Test Note", "# Test Note\n\nContent")

        # Verify the result structure
        assert result["success"] is True
        assert "note" in result
        assert "message" in result

        # Verify note details
        note = result["note"]
        assert note["name"] == "New Test Note"
        assert note["id"] == "x-coredata://test/ICNote/p999"
        assert "This is a new test note" in note["body_preview"]
        assert note["creation_date"] == "2025-01-15T14:00:00"
        assert note["account"] == "iCloud"
        assert note["folder"] == "Notes"

        # Verify NotesApp was called correctly
        mock_notes_app.account.assert_called_once()
        mock_account.make_note.assert_called_once_with(
            name="Test Note", body="<h1>Test Note</h1><p>Content</p>"
        )

    def test_create_note_with_markdown(self, mock_notes_app, mock_account):
        """Test note creation with Markdown content"""
        mock_notes_app.account.return_value = mock_account

        markdown_content = """# My Note
        # noqa: W293
## Section 1
- Item 1
- Item 2

**Bold text** and *italic text*

```python
print("Hello, World!")
```
"""

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            with patch("main.markdown.Markdown") as mock_markdown:
                mock_md = Mock()
                expected_html = '<h1>My Note</h1><h2>Section 1</h2><ul><li>Item 1</li><li>Item 2</li></ul><p><strong>Bold text</strong> and <em>italic text</em></p><pre><code class="language-python">print("Hello, World!")</code></pre>'  # noqa: E501
                mock_md.convert.return_value = expected_html
                mock_markdown.return_value = mock_md

                result = create_note("My Note", markdown_content)

        assert result["success"] is True

        # Verify markdown was processed
        mock_markdown.assert_called_once_with(extensions=["extra", "codehilite"])
        mock_md.convert.assert_called_once_with(markdown_content)
        mock_account.make_note.assert_called_once_with(
            name="My Note", body=expected_html
        )

    def test_create_note_empty_title(self, mock_notes_app):
        """Test creation with empty title"""
        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            result = create_note("", "Some content")

        assert result["success"] is False
        assert "Note title cannot be empty" in result["error"]
        assert "Please provide a valid note title" in result["message"]

        # Should not attempt to create note
        mock_notes_app.account.assert_not_called()

    def test_create_note_whitespace_title(self, mock_notes_app):
        """Test creation with whitespace-only title"""
        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            result = create_note("   ", "Some content")

        assert result["success"] is False
        assert "Note title cannot be empty" in result["error"]

    def test_create_note_empty_body(self, mock_notes_app, mock_account):
        """Test creation with empty body"""
        mock_notes_app.account.return_value = mock_account

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            with patch("main.markdown.Markdown") as mock_markdown:
                mock_md = Mock()
                mock_md.convert.return_value = ""
                mock_markdown.return_value = mock_md

                result = create_note("Test Note", "")

        assert result["success"] is True
        mock_account.make_note.assert_called_once_with(name="Test Note", body="")

    def test_create_note_markdown_conversion_error(self, mock_notes_app, mock_account):
        """Test handling of markdown conversion errors"""
        mock_notes_app.account.return_value = mock_account

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            with patch("main.markdown.Markdown") as mock_markdown:
                mock_markdown.side_effect = Exception("Markdown error")

                result = create_note("Test Note", "# Content\nWith newlines")

        assert result["success"] is True

        # Should fallback to simple HTML conversion
        mock_account.make_note.assert_called_once()
        call_args = mock_account.make_note.call_args
        assert call_args[1]["name"] == "Test Note"
        # Should convert \n to <br>
        assert "<br>" in call_args[1]["body"]

    def test_create_note_creation_failure(self, mock_notes_app, mock_account):
        """Test handling of note creation failure"""
        mock_notes_app.account.return_value = mock_account
        mock_account.make_note.side_effect = Exception("Creation failed")

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            with patch("main.markdown.Markdown") as mock_markdown:
                mock_md = Mock()
                mock_md.convert.return_value = "<p>Content</p>"
                mock_markdown.return_value = mock_md

                result = create_note("Test Note", "Content")

        assert result["success"] is False
        assert "Failed to create note: Creation failed" in result["error"]
        assert "Failed to create note in Apple Notes" in result["message"]

    def test_create_note_import_error(self):
        """Test handling of import error"""
        with patch(
            "macnotesapp.NotesApp", side_effect=ImportError("macnotesapp not available")
        ):
            result = create_note("Test Note", "Content")

        assert result["success"] is False
        assert "macnotesapp package not available" in result["error"]
        assert "Failed to import required dependencies" in result["message"]

    def test_create_note_general_exception(self, mock_notes_app):
        """Test handling of general exceptions"""
        mock_notes_app.account.side_effect = Exception("Connection failed")

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            result = create_note("Test Note", "Content")

        assert result["success"] is False
        assert "Error creating note: Connection failed" in result["error"]
        assert "Failed to create note" in result["message"]

    def test_create_note_title_stripping(self, mock_notes_app, mock_account):
        """Test that title whitespace is properly stripped"""
        mock_notes_app.account.return_value = mock_account

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            with patch("main.markdown.Markdown") as mock_markdown:
                mock_md = Mock()
                mock_md.convert.return_value = "<p>Content</p>"
                mock_markdown.return_value = mock_md

                result = create_note("  Test Note  ", "Content")

        assert result["success"] is True
        mock_account.make_note.assert_called_once_with(
            name="Test Note",  # Should be stripped
            body="<p>Content</p>",
        )

    def test_create_note_body_preview_truncation(self, mock_notes_app):
        """Test that body preview is properly truncated"""
        # Create a mock note with long plaintext
        long_text = "A" * 250  # More than 200 characters
        mock_note = Mock()
        mock_note.name = "Long Note"
        mock_note.id = "test-id"
        mock_note.plaintext = long_text
        mock_note.creation_date = None
        mock_note.account = Mock(name="iCloud")
        mock_note.folder = Mock(name="Notes")

        mock_account = Mock()
        mock_account.make_note.return_value = mock_note
        mock_notes_app.account.return_value = mock_account

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            with patch("main.markdown.Markdown") as mock_markdown:
                mock_md = Mock()
                mock_md.convert.return_value = "<p>Content</p>"
                mock_markdown.return_value = mock_md

                result = create_note("Long Note", "Content")

        assert result["success"] is True
        # Should be truncated to 200 chars + "..."
        assert len(result["note"]["body_preview"]) == 203  # 200 + "..."
        assert result["note"]["body_preview"].endswith("...")

    def test_create_note_missing_note_attributes(self, mock_notes_app):
        """Test handling of notes with missing attributes"""
        # Create a mock note with minimal attributes
        mock_note = Mock()
        mock_note.name = "Minimal Note"
        mock_note.id = "test-id"
        mock_note.plaintext = None  # Missing plaintext
        mock_note.creation_date = None
        mock_note.account = None  # Missing account
        mock_note.folder = None  # Missing folder

        mock_account = Mock()
        mock_account.make_note.return_value = mock_note
        mock_notes_app.account.return_value = mock_account

        with patch("macnotesapp.NotesApp", return_value=mock_notes_app):
            with patch("main.markdown.Markdown") as mock_markdown:
                mock_md = Mock()
                mock_md.convert.return_value = "<p>Content</p>"
                mock_markdown.return_value = mock_md

                result = create_note("Minimal Note", "Content")

        assert result["success"] is True
        note = result["note"]
        assert note["body_preview"] == ""  # Should handle None plaintext
        assert note["account"] == "Unknown"  # Should handle None account
        assert note["folder"] == "Unknown"  # Should handle None folder
