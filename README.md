# Apple Notes MCP Desktop Extension

[![Test](https://github.com/mcolyer/mcp-apple-notes-py/actions/workflows/test.yml/badge.svg)](https://github.com/mcolyer/mcp-apple-notes-py/actions/workflows/test.yml)
[![Code Quality](https://github.com/mcolyer/mcp-apple-notes-py/actions/workflows/quality.yml/badge.svg)](https://github.com/mcolyer/mcp-apple-notes-py/actions/workflows/quality.yml)
[![Release](https://github.com/mcolyer/mcp-apple-notes-py/actions/workflows/release.yml/badge.svg)](https://github.com/mcolyer/mcp-apple-notes-py/actions/workflows/release.yml)

A Desktop Extension (DXT) that provides access to Apple Notes through the Model Context Protocol (MCP). This extension allows AI assistants to list and retrieve notes from your local Apple Notes.app.

## 🚀 Quick Start

1. **[Download the latest .dxt file](https://github.com/mcolyer/mcp-apple-notes-py/releases/latest)**
2. **Open Claude Desktop** → **Settings** → **Extensions**
3. **Click "Install Extension"** and select the downloaded `.dxt` file
4. **Restart Claude Desktop** and grant Apple Notes permissions when prompted

✅ **Ready to use!** Claude can now access your Apple Notes.

## Features

- **List Notes**: Retrieve note titles and IDs from Apple Notes.app with optional folder filtering
- **Get Notes**: Retrieve full note content by ID for efficient access
- **Search Notes**: Search notes by text content or tags with optional folder filtering
- **Create Notes**: Create new notes with Markdown formatting support
- **Folder Support**: Filter operations by specific Apple Notes folders
- **Tag Search**: Search for notes containing specific hashtags (e.g., #work, #personal)
- **Error Handling**: Comprehensive error handling with clear messages
- **Debug Mode**: Optional verbose logging for troubleshooting
- **macOS Integration**: Native integration with Apple Notes.app

## Requirements

- **macOS**: This extension only works on macOS as it requires Apple Notes.app
- **Python**: 3.13 or higher
- **Permissions**: Apple Notes.app access permissions may be required

## Installation

### Option 1: DXT Package (Recommended)

The easiest way to install this extension is using the pre-built DXT package:

1. **Download the latest DXT file**:
   - Go to the [latest release](https://github.com/mcolyer/mcp-apple-notes-py/releases/latest)
   - Download the `.dxt` file from the release assets

2. **Install in Claude Desktop**:
   - Open Claude Desktop
   - Go to **Settings** → **Extensions**
   - Click **"Install Extension"**
   - Select the downloaded `.dxt` file
   - Click **"Install"**

3. **Restart Claude Desktop** to activate the extension

4. **Grant Permissions** (when prompted):
   - macOS may request permission to access Apple Notes.app
   - Click **"Allow"** to enable the extension functionality

### Option 2: Manual Installation (Development)

For development or if you want to build from source:

1. **Clone this repository**:
   ```bash
   git clone https://github.com/mcolyer/mcp-apple-notes-py.git
   cd mcp-apple-notes-py
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Run the server**:
   ```bash
   uv run python main.py
   ```

4. **Build DXT package** (optional):
   ```bash
   uv run python scripts/package_dxt.py
   ```

## Usage

### Available Tools

#### `list_notes`
Lists note titles and IDs from Apple Notes.app with optional folder filtering.

**Parameters:**
- `limit` (optional): Maximum number of notes to return (default: 50, max: 1000)
- `folder` (optional): Folder name to filter notes (case sensitive, if None, lists from all folders)

**Returns:**
Array of objects with note titles and IDs

**Example Response:**
```json
[
  {
    "title": "Meeting Notes",
    "id": "x-coredata://0EA5F4CA-F669-4BB5-B24B-EF828876E597/ICNote/p9135"
  },
  {
    "title": "Project Ideas",
    "id": "x-coredata://0EA5F4CA-F669-4BB5-B24B-EF828876E597/ICNote/p9142"
  }
]
```

#### `get_notes`
Retrieves specific notes by their IDs.

**Parameters:**
- `ids`: List of note IDs to retrieve

**Returns:**
- `notes`: Array of note objects with full content
- `found_count`: Number of notes successfully retrieved
- `not_found`: Array of IDs that were not found
- `message`: Status message

**Example Response:**
```json
{
  "notes": [
    {
      "name": "Meeting Notes",
      "body": "<h1>Meeting Notes</h1><p>Discussed project timeline...</p>",
      "plaintext": "Meeting Notes\nDiscussed project timeline...",
      "creation_date": "2025-01-15T10:30:00",
      "modification_date": "2025-01-15T14:20:00",
      "account": "iCloud",
      "folder": "Work",
      "id": "x-coredata://0EA5F4CA-F669-4BB5-B24B-EF828876E597/ICNote/p9135",
      "password_protected": false
    }
  ],
  "found_count": 1,
  "not_found": [],
  "message": "Found 1 of 1 requested notes"
}
```

#### `search_notes`
Searches notes by body content or in note titles with configurable search type.

**Parameters:**
- `query`: Search term or tag (use #tag format for tag search)
- `limit` (optional): Maximum number of results to return (default: 10, max: 100)
- `search_type` (optional): Where to search - "body" for note content, "name" for note titles (default: "body")

**Returns:**
- `notes`: Array of matching notes with titles and IDs
- `found_count`: Number of notes found
- `query`: The search query used
- `search_type`: Type of search performed ("name" or "body")
- `message`: Status message

**Example Response:**
```json
{
  "notes": [
    {
      "title": "Project Planning",
      "id": "x-coredata://0EA5F4CA-F669-4BB5-B24B-EF828876E597/ICNote/p9150"
    }
  ],
  "found_count": 1,
  "query": "project",
  "search_type": "body",
  "message": "Found 1 notes matching 'project' in body"
}
```

#### `create_note`
Creates a new note with Markdown formatted body.

**Parameters:**
- `title`: Title for the new note
- `body`: Body content in Markdown format
- `folder` (optional): Folder name to create note in (case sensitive, uses default folder if not specified)

**Returns:**
- `success`: Boolean indicating if creation was successful
- `note`: Object with created note details (if successful)
- `message`: Status message

**Example Response:**
```json
{
  "success": true,
  "note": {
    "name": "New Project Idea",
    "id": "x-coredata://0EA5F4CA-F669-4BB5-B24B-EF828876E597/ICNote/p9160",
    "body_preview": "This is a revolutionary idea for improving...",
    "creation_date": "2025-01-15T18:45:00",
    "account": "iCloud",
    "folder": "Ideas"
  },
  "message": "Successfully created note 'New Project Idea' in folder 'Ideas'"
}
```

## Usage Examples

### Basic Workflow

1. **List notes to get IDs:**
   ```python
   notes = list_notes(limit=10, folder="Work")
   # Returns: [{"title": "Meeting Notes", "id": "x-coredata://..."}, ...]
   ```

2. **Get full content of specific notes:**
   ```python
   full_notes = get_notes(["x-coredata://0EA5F4CA-F669-4BB5-B24B-EF828876E597/ICNote/p9135"])
   # Returns full note content including body, plaintext, metadata
   ```

3. **Search for notes:**
   ```python
   # Search in note content (default)
   results = search_notes("project timeline", limit=5)
   
   # Search in note titles only
   title_results = search_notes("Meeting", search_type="name", limit=5)
   
   # Search for hashtags in content
   tag_results = search_notes("#urgent", limit=10)
   ```

4. **Create a new note:**
   ```python
   new_note = create_note(
       title="Weekly Review",
       body="Weekly Review\n\nAccomplishments:\n- Finished project X\n- Started project Y"
   )
   ```

## Configuration

The extension supports the following configuration options:

- **Debug Mode**: Enable verbose logging for troubleshooting
  - Set via environment variable: `DEBUG_MODE=true`
  - Or configure in your MCP client settings

## Permissions

### First-Time Setup
When first running the extension, macOS may prompt for permissions to access Apple Notes.app. Please grant these permissions for the extension to function properly.

### Troubleshooting Permissions
If you encounter permission issues:

1. Open **System Preferences** → **Security & Privacy** → **Privacy**
2. Look for entries related to your terminal or Python installation
3. Ensure they have access to Apple Notes or Full Disk Access if needed
4. Restart the MCP server after granting permissions

## Troubleshooting

### Extension Not Working

1. **Check Claude Desktop Version**:
   - Ensure you're running Claude Desktop v0.10.0 or higher
   - Update Claude Desktop if needed

2. **Verify Installation**:
   - Go to Claude Desktop → Settings → Extensions
   - Confirm "Apple Notes MCP" appears in the installed extensions list
   - If not listed, reinstall the extension

3. **Grant Permissions**:
   - Open **System Preferences** → **Security & Privacy** → **Privacy**
   - Look for entries related to Claude Desktop or the terminal
   - Ensure they have access to Apple Notes or Full Disk Access
   - Restart Claude Desktop after granting permissions

### Common Issues

**"Permission denied" or "Unable to access Apple Notes"**:
- Grant necessary macOS permissions as described above
- Try restarting both Apple Notes.app and Claude Desktop
- Ensure Apple Notes.app is not password-protected or locked

**"No notes found" when you have notes**:
- Check if your notes are in iCloud and properly synced
- Verify Apple Notes.app can access your notes directly
- Try creating a test note in Apple Notes.app

**Extension appears installed but functions don't work**:
- Restart Claude Desktop completely
- Check if there are any error messages in Claude Desktop
- Try reinstalling the extension

### Getting Help

If you continue to experience issues:

1. **Check the error logs** (enable debug mode if available)
2. **Verify Apple Notes.app permissions** in System Preferences
3. **Ensure you're running on macOS** with Apple Notes.app available
4. **Create an issue** in the [GitHub repository](https://github.com/mcolyer/mcp-apple-notes-py/issues) with:
   - Your macOS version
   - Claude Desktop version  
   - Extension version
   - Error messages or screenshots

## Development

### Project Structure
```
mcp-apple-notes-py/
   main.py              # MCP server implementation
   manifest.json        # DXT manifest for packaging
   pyproject.toml       # Python project configuration
   README.md           # This file
```

### Building DXT Package
To package as a DXT extension:

```bash
# Build DXT package with all dependencies bundled
uv run python scripts/package_dxt.py

# This creates a .dxt file ready for distribution
```

### Testing
Test the server locally:

```bash
# Install dependencies
uv sync

# Run server
uv run python main.py

# Run test suite (44 tests)
uv run pytest tests/ -v

# Test specific functions
uv run python -c "from main import list_notes; print('Import successful')"
```

## Limitations

- **macOS Only**: Only works on macOS with Apple Notes.app
- **Password-Protected Notes**: Limited support for password-protected notes
- **Top-Level Folders**: Only accesses top-level folders in Apple Notes
- **Attachments**: Note attachments are not currently processed
- **No Note Modification**: Cannot modify existing notes (only create new ones)
- **HTML Conversion**: Markdown is converted to HTML for Apple Notes compatibility
- **Search Performance**: Body content searches may be slower than title searches. Use `search_type="name"` for faster title-only searches.

## Error Handling

The extension includes comprehensive error handling:

- **Import Errors**: Clear messages if dependencies are missing
- **Permission Errors**: Helpful guidance for macOS permission issues
- **Connection Errors**: Graceful handling of Apple Notes.app connectivity issues
- **Individual Note Errors**: Continues processing other notes if one fails

## Contributing

Contributions are welcome! Please ensure:

1. Code follows the existing style and patterns
2. Error handling is comprehensive
3. Changes are tested on macOS
4. Documentation is updated accordingly

## License

MIT License - see LICENSE file for details

## Support

For issues and support:
1. Check the error logs (enable debug mode for detailed logging)
2. Verify Apple Notes.app permissions
3. Ensure you're running on macOS with Apple Notes.app available
4. Create an issue in the project repository