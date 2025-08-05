# Changelog

All notable changes to the Apple Notes MCP Desktop Extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Enhanced Search Performance**: Integrated apple-notes-parser for faster SQLite-based search operations
- **Tag Search Support**: Added native hashtag search functionality with `#tag` syntax
- **Folder Filtering**: Added optional folder parameter to list_notes() for filtering notes by folder name
- **Hybrid Implementation**: Combines apple-notes-parser for search/list operations with macnotesapp for note creation and retrieval

### Changed
- **list_notes()**: Now uses apple-notes-parser exclusively with optional folder filtering parameter
- **search_notes()**: Enhanced with tag search support and faster full-text search via apple-notes-parser
- **Dependencies**: Added apple-notes-parser as new dependency alongside existing macnotesapp
- **Test Suite**: Updated to 47 tests including new folder filtering functionality

### Removed
- **Fallback Logic**: Removed macnotesapp fallback from list_notes() and search_notes() for simplified architecture

### Technical
- Simplified architecture: apple-notes-parser for read operations, macnotesapp for write operations  
- Case-insensitive folder filtering with error handling for individual note processing
- All 47 tests pass with enhanced coverage for folder filtering functionality
- Tag search automatically detected when query starts with "#"

## [0.2.2] - 2025-07-28

### Fixed
- Added required permissions (contents:write, packages:write) to GitHub Actions release workflow
- Resolved "Resource not accessible by integration" error preventing automated releases
- GitHub Actions workflows can now successfully create releases and upload DXT packages

## [0.2.1] - 2025-07-28

### Fixed
- Fixed heredoc syntax error in GitHub Actions release workflow that prevented automated releases
- Resolved YAML parsing issues with nested quotes and EOF markers in release notes
- Updated release workflow to use separate file creation step for better reliability

## [0.2.0] - 2025-07-28

### Added
- Comprehensive GitHub Actions CI/CD workflows
- Automated DXT package building and releases
- Status badges for test, quality, and release workflows
- Comprehensive troubleshooting section in README
- GitHub issue reporting template and support workflow

### Changed
- Updated README with professional DXT installation instructions
- Enhanced development documentation with UV package manager usage
- Improved error handling consistency across all functions

### Fixed
- GitHub Actions release workflow now uses modern gh CLI instead of deprecated actions

## [0.1.0] - 2025-07-28

### Added
- **Core MCP Functions**:
  - `list_notes`: List note titles and IDs with optional limits
  - `get_notes`: Retrieve full note content by ID with comprehensive metadata
  - `search_notes`: Search notes by body content or titles with hashtag support
  - `create_note`: Create new notes with Markdown formatting support

- **Performance Optimizations**:
  - Implemented efficient `noteslist()` method throughout codebase
  - Removed deprecated `notes()` method usage for better performance
  - Added proper attribute extraction from NotesList objects
  - Optimized search functionality with built-in parameters

- **Comprehensive Testing**:
  - 44 automated tests covering all MCP functions
  - Mock-based testing without requiring real Apple Notes access
  - Test coverage for success scenarios, edge cases, and error handling
  - Pytest configuration with proper fixtures and shared mocks

- **GitHub Actions CI/CD**:
  - **Test Workflow**: Automated testing on push/PR to main/develop
  - **Quality Workflow**: Code quality checks and manifest validation
  - **Release Workflow**: Automated DXT building and GitHub releases
  - Ubuntu Linux execution for faster CI/CD performance

- **Documentation**:
  - Comprehensive README with installation and usage instructions
  - CLAUDE.md with development guidelines and noteslist() best practices
  - GitHub Actions workflow documentation
  - Complete API documentation with examples

- **Development Infrastructure**:
  - UV package manager integration for dependency management
  - FastMCP framework for MCP server implementation
  - DXT packaging script with dependency bundling
  - Pytest test suite with comprehensive coverage

### Technical Implementation
- **Apple Notes Integration**: Native macOS Apple Notes.app access via macnotesapp library
- **Markdown Support**: Full Markdown to HTML conversion for note creation
- **Error Handling**: Comprehensive error handling with graceful fallbacks
- **Type Safety**: Full type hints throughout codebase
- **Logging**: Structured logging with appropriate levels
- **Security**: Defensive programming with input validation

### Dependencies
- **Production**: mcp[cli], macnotesapp, markdown
- **Development**: pytest, pytest-mock
- **Build**: UV package manager, FastMCP framework

### Platform Support
- **macOS**: Full support with Apple Notes.app integration
- **Permissions**: Handles macOS permission requests gracefully
- **Claude Desktop**: DXT package compatible with Claude Desktop v0.10.0+

## Release Process

This project uses automated releases via GitHub Actions:

1. **Tag Creation**: Create and push a version tag (e.g., `v0.1.0`)
2. **Automated Testing**: Full test suite runs automatically
3. **DXT Building**: Package is built with all dependencies bundled
4. **GitHub Release**: Release created with DXT file attached
5. **Distribution**: DXT file available for download and installation

### Version Tags
- `v0.2.2` - Fixed GitHub Actions release workflow permissions
- `v0.2.1` - Fixed GitHub Actions release workflow syntax errors
- `v0.2.0` - Enhanced CI/CD workflows and improved documentation
- `v0.1.0` - Initial release with core functionality

### Installation
Download the latest `.dxt` file from [GitHub Releases](https://github.com/mcolyer/mcp-apple-notes-py/releases) and install via Claude Desktop → Settings → Extensions.