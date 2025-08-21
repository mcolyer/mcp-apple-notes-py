# Changelog

All notable changes to the Apple Notes MCP Desktop Extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.1] - 2025-08-21

### Fixed
- **Code Cleanup**: Removed unnecessary HTML and temporary files from repository
- **Version Consistency**: Fixed version synchronization across manifest.json, pyproject.toml, and packaging scripts
- **Git History**: Cleaned up development artifacts and improved repository organization

### Changed
- **Repository Structure**: Streamlined codebase by removing unused render utilities and temporary files
- **Build Process**: Enhanced packaging reliability with consistent version handling

### Technical
- Maintained all 51 tests passing with zero regressions
- Improved codebase cleanliness and maintainability
- Enhanced version management across all project files

## [0.4.0] - 2025-08-21

### Changed
- **Test Suite**: Expanded test suite from 44 to 51 tests with improved coverage
- **Test Organization**: Enhanced test structure and reliability with better mock patterns
- **Code Quality**: Maintained comprehensive test coverage across all MCP functions

### Technical
- All 51 tests continue to pass with comprehensive coverage
- Enhanced test fixtures and mock configurations for better reliability
- Improved test patterns for consistent testing across all functions

## [0.3.0] - 2025-08-05

### Added
- **Enhanced Search Performance**: Integrated apple-notes-parser for faster SQLite-based search operations
- **Tag Search Support**: Added native hashtag search functionality with `#tag` syntax (single tag at a time)
- **Folder Filtering**: Added optional folder parameter to list_notes() for filtering notes by folder name
- **Comprehensive ID Validation**: Added extensive tests to prevent MCP validation errors
- **Hybrid Implementation**: Combines apple-notes-parser for search/list operations with macnotesapp for note creation and retrieval

### Changed
- **list_notes()**: Now uses apple-notes-parser exclusively with optional folder filtering parameter
- **search_notes()**: Simplified to support only body content and hashtag search (removed title search)
- **Dependencies**: Added apple-notes-parser as new dependency alongside existing macnotesapp
- **Test Suite**: Expanded to 51 tests including ID conversion validation and folder filtering
- **Documentation**: Enhanced function docstrings and manifest descriptions for clarity

### Removed
- **Fallback Logic**: Removed macnotesapp fallback from list_notes() and search_notes() for simplified architecture
- **Title Search**: Removed search_type parameter and title/name search functionality from search_notes()

### Fixed
- **ID Type Validation**: Fixed MCP validation errors by converting integer IDs to strings
- **Error Handling**: Improved None ID handling with graceful fallback to "unknown"

### Technical
- Simplified architecture: apple-notes-parser for read operations, macnotesapp for write operations  
- Case-insensitive folder filtering with error handling for individual note processing
- Automatic ID type conversion prevents MCP framework validation errors
- Tag search automatically detected when query starts with "#" (single tag only)
- All 51 tests pass with comprehensive coverage including regression prevention

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