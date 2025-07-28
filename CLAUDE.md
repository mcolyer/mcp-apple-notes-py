# Apple Notes MCP Desktop Extension - Project Guidelines

This document contains project-specific guidelines for working on the Apple Notes MCP Desktop Extension.

## Project Overview

This is a Desktop Extension (DXT) that provides access to Apple Notes through the Model Context Protocol (MCP). It allows AI assistants to list and retrieve notes from local Apple Notes.app on macOS.

## Development Guidelines

### Package Management
- **Use UV**: Always use `uv` for dependency management and virtual environment handling
- **Sync dependencies**: Run `uv sync` to install/update dependencies
- **Add dependencies**: Use `uv add <package>` to add new dependencies
- **IMPORTANT**: When adding new dependencies, also update `scripts/package_dxt.py` to include them in the bundled DXT package dependencies list

### Code Standards
- **Python Version**: Requires Python 3.13 or higher
- **Type Hints**: Use comprehensive type hints throughout the codebase
- **Error Handling**: Implement defensive programming with comprehensive error handling
- **Logging**: Use structured logging with appropriate levels (INFO, DEBUG, WARNING, ERROR)

### MCP Server Implementation
- **FastMCP**: Use the FastMCP framework for server implementation
- **Tool Definitions**: All tools must have proper docstrings and type annotations
- **Input Validation**: Validate all input parameters with appropriate bounds
- **Structured Responses**: Return consistent JSON responses with metadata

### DXT Compliance
- **Manifest**: Follow DXT manifest specification exactly
- **Platform Support**: macOS only due to Apple Notes.app requirement
- **Packaging**: Ensure all dependencies are bundled for distribution
- **Security**: Implement proper security measures and timeout management

### Testing
- **Automated Testing**: Comprehensive pytest suite with 44 tests covering all functions
- **Manual Testing**: Test with actual Apple Notes.app data
- **Error Conditions**: Test permission errors, missing dependencies, empty notes
- **Edge Cases**: Test with large note counts, special characters, missing metadata

#### Pytest Suite
The project includes a comprehensive test suite covering all MCP functions:

**Running Tests:**
```bash
# Run all tests (44 tests total)
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_list_notes.py -v
uv run pytest tests/test_search_notes.py -v  
uv run pytest tests/test_get_notes.py -v
uv run pytest tests/test_create_note.py -v

# Run with coverage (if coverage installed)
uv run pytest tests/ --cov=main

# Run tests in quiet mode
uv run pytest tests/ -q
```

**Test Structure:**
- `tests/conftest.py` - Shared fixtures and mock configurations
- `tests/test_list_notes.py` - 8 tests for list_notes function
- `tests/test_search_notes.py` - 13 tests for search_notes function
- `tests/test_get_notes.py` - 11 tests for get_notes function  
- `tests/test_create_note.py` - 12 tests for create_note function
- `pytest.ini` - Test configuration

**Test Coverage Areas:**
- Success scenarios with valid inputs and expected outputs
- Edge cases (empty/None values, limits, whitespace handling)
- Error handling (import errors, connection failures, invalid inputs)
- Parameter validation (limits, search types, title validation)
- Mock-based testing without requiring real Apple Notes access
- NotesList integration testing all attribute extraction
- Markdown processing and fallback handling
- Date formatting and ISO conversion

**Adding New Tests:**
When adding new functionality or fixing bugs:
1. Add test cases to the appropriate test file
2. Use the shared fixtures in `conftest.py` for consistent mocking
3. Follow the existing test patterns and naming conventions
4. Test both success and failure scenarios
5. Mock `macnotesapp.NotesApp` to avoid requiring real Apple Notes
6. Run the full test suite to ensure no regressions

**Mock Patterns:**
```python
# Standard test pattern
def test_new_function(self, mock_notes_app, mock_noteslist):
    mock_notes_app.noteslist.return_value = mock_noteslist
    
    with patch('macnotesapp.NotesApp', return_value=mock_notes_app):
        result = your_function(test_params)
    
    # Assertions
    assert result["expected_field"] == expected_value
    mock_notes_app.noteslist.assert_called_once_with(expected_params)
```

### Documentation
- **README**: Keep comprehensive installation and usage instructions
- **Code Comments**: Add comments for complex logic, especially Apple Notes integration
- **API Documentation**: Document all tool parameters and return values

## File Structure

```
mcp-apple-notes-py/
├── main.py              # MCP server implementation
├── manifest.json        # DXT manifest for packaging
├── pyproject.toml       # Python project configuration
├── pytest.ini          # Pytest configuration
├── README.md           # User documentation
├── CLAUDE.md           # This file - development guidelines
├── scripts/            # Build and utility scripts
│   ├── __init__.py     # Package marker
│   └── package_dxt.py  # DXT packaging script
├── tests/              # Comprehensive test suite (44 tests)
│   ├── __init__.py     # Package marker
│   ├── conftest.py     # Shared fixtures and mocks
│   ├── test_list_notes.py    # Tests for list_notes (8 tests)
│   ├── test_search_notes.py  # Tests for search_notes (13 tests)
│   ├── test_get_notes.py     # Tests for get_notes (11 tests)
│   └── test_create_note.py   # Tests for create_note (12 tests)
└── .venv/              # Virtual environment (uv managed)
```

## Key Dependencies

**Production Dependencies:**
- `mcp[cli]`: Model Context Protocol Python SDK
- `macnotesapp`: Apple Notes.app integration library  
- `markdown`: Markdown to HTML conversion for note creation
- Standard library: `asyncio`, `logging`, `sys`, `os`, `typing`

**Development Dependencies:**
- `pytest`: Testing framework for comprehensive test suite
- `pytest-mock`: Mock objects and patching for tests

## Apple Notes Integration

### CRITICAL: Always Use noteslist() Method
- **NEVER use `notes_app.notes()`** - this method is inefficient for large collections
- **ALWAYS use `notes_app.noteslist()`** - this is the optimized approach for all operations
- **Pattern**: Use `noteslist()` with specific parameters, then extract attributes:
  ```python
  # For listing all notes
  noteslist_obj = notes_app.noteslist()
  note_names = noteslist_obj.name
  note_ids = noteslist_obj.id
  
  # For searching
  noteslist_obj = notes_app.noteslist(body=["search_term"])
  noteslist_obj = notes_app.noteslist(name=["search_term"])
  
  # For filtering by ID
  noteslist_obj = notes_app.noteslist(id=id_list)
  
  # Extract all needed attributes
  note_names = noteslist_obj.name
  note_bodies = noteslist_obj.body
  note_plaintexts = noteslist_obj.plaintext
  # ... etc for all needed attributes
  ```

### Available NotesList Attributes
When using `noteslist()`, you can extract these attributes:
- `noteslist_obj.name` - Note titles/names
- `noteslist_obj.id` - Note IDs  
- `noteslist_obj.body` - HTML content
- `noteslist_obj.plaintext` - Plain text content
- `noteslist_obj.creation_date` - Creation timestamps
- `noteslist_obj.modification_date` - Modification timestamps  
- `noteslist_obj.account` - Account objects (use .name for account name)
- `noteslist_obj.folder` - Folder objects (use .name for folder name)
- `noteslist_obj.password_protected` - Boolean protection status

### Permissions
- Extension requires macOS permissions to access Apple Notes.app
- Handle permission errors gracefully with clear user guidance
- Test with both granted and denied permissions

### Data Handling
- Notes may contain sensitive information - handle securely
- Limit note content previews to 200 characters
- Include metadata: creation/modification dates, accounts, folders
- Handle edge cases: empty notes, missing metadata, encoding issues
- Use defensive programming with `getattr()` for optional attributes

### Performance
- Implement reasonable limits (max 1000 notes per request)
- The `noteslist()` method is optimized for large collections
- Extract only needed attributes to minimize memory usage
- Handle large note collections efficiently with built-in filtering

## Common Commands

```bash
# Install dependencies
uv sync

# Run the MCP server
uv run python main.py

# Test with debug mode
DEBUG_MODE=true uv run python main.py

# Package as DXT for distribution
uv run scripts/package_dxt.py
# OR
uv run package-dxt

# Install the generated DXT package in Claude Desktop
# 1. Run packaging command above
# 2. Open Claude Desktop → Settings → Extensions
# 3. Click "Install Extension" and select the .dxt file

# Run tests
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_list_notes.py -v

# Run tests with coverage (requires pytest-cov)
uv run pytest tests/ --cov=main --cov-report=html
```

## Error Handling Patterns

1. **Import Errors**: Check for missing dependencies with clear messages
2. **Permission Errors**: Provide specific guidance for macOS permission setup
3. **Apple Notes Errors**: Handle Notes.app connectivity and access issues
4. **Individual Note Errors**: Continue processing when single notes fail
5. **Validation Errors**: Validate inputs and provide helpful error messages

## Security Considerations

- Never log sensitive note content
- Implement input validation for all parameters
- Use secure defaults for configuration options
- Handle timeout scenarios gracefully
- Follow principle of least privilege for Apple Notes access

## Deployment Notes

- Package as DXT with all dependencies bundled
- Test on clean macOS systems
- Verify Apple Notes.app permissions workflow
- Include clear setup instructions for end users
- Test with different Apple Notes.app configurations (iCloud, local, multiple accounts)