# Changelog

All notable changes to the Apple Notes MCP Desktop Extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- `v0.1.0` - Initial release with core functionality
- Future releases will follow semantic versioning

### Installation
Download the latest `.dxt` file from [GitHub Releases](https://github.com/mcolyer/mcp-apple-notes-py/releases) and install via Claude Desktop → Settings → Extensions.