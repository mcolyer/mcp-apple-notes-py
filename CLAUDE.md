# Apple Notes MCP Desktop Extension - Project Guidelines

This document contains project-specific guidelines for working on the Apple Notes MCP Desktop Extension.

## Project Overview

This is a Desktop Extension (DXT) that provides access to Apple Notes through the Model Context Protocol (MCP). It allows AI assistants to list and retrieve notes from local Apple Notes.app on macOS.

## Development Guidelines

### Package Management
- **Use UV**: Always use `uv` for dependency management and virtual environment handling
- **Sync dependencies**: Run `uv sync` to install/update dependencies
- **Add dependencies**: Use `uv add <package>` to add new dependencies

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
- **Manual Testing**: Test with actual Apple Notes.app data
- **Error Conditions**: Test permission errors, missing dependencies, empty notes
- **Edge Cases**: Test with large note counts, special characters, missing metadata

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
├── README.md           # User documentation
├── CLAUDE.md           # This file - development guidelines
├── scripts/            # Build and utility scripts
│   ├── __init__.py     # Package marker
│   └── package_dxt.py  # DXT packaging script
└── .venv/              # Virtual environment (uv managed)
```

## Key Dependencies

- `mcp[cli]`: Model Context Protocol Python SDK
- `macnotesapp`: Apple Notes.app integration library
- Standard library: `asyncio`, `logging`, `sys`, `os`, `typing`

## Apple Notes Integration

### Permissions
- Extension requires macOS permissions to access Apple Notes.app
- Handle permission errors gracefully with clear user guidance
- Test with both granted and denied permissions

### Data Handling
- Notes may contain sensitive information - handle securely
- Limit note content previews to 200 characters
- Include metadata: creation/modification dates, accounts, folders
- Handle edge cases: empty notes, missing metadata, encoding issues

### Performance
- Implement reasonable limits (max 1000 notes per request)
- Use lazy loading where possible
- Handle large note collections efficiently

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