# GitHub Actions Workflows

This project uses GitHub Actions for automated testing, code quality checks, and releases.

## Workflows

### 🧪 Test Workflow (`test.yml`)
- **Trigger**: Push to `main`/`develop` branches, PRs to `main`
- **Purpose**: Run comprehensive test suite on every code change
- **Steps**:
  1. Set up Python 3.13 environment
  2. Install UV package manager
  3. Install project dependencies with `uv sync`
  4. Run pytest suite (44 tests)
  5. Verify basic import functionality

### 🏗️ Code Quality Workflow (`quality.yml`)
- **Trigger**: Push to `main`/`develop` branches, PRs to `main`
- **Purpose**: Ensure code quality and catch common issues
- **Steps**:
  1. Check Python syntax compilation
  2. Validate `manifest.json` structure
  3. Check for deprecated `notes()` method usage (should use `noteslist()`)
  4. Scan for debug prints and TODO/FIXME comments

### 🚀 Release Workflow (`release.yml`)
- **Trigger**: Push of version tags (e.g., `v1.0.0`)
- **Purpose**: Automated testing, DXT package creation, and GitHub release
- **Steps**:
  1. **Test Job**: Full test suite validation
  2. **Build Job**: 
     - Update version in manifest.json from git tag
     - Build DXT package using `scripts/package_dxt.py`
     - Create GitHub release with release notes
     - Upload DXT file as release asset
     - Store DXT as workflow artifact

## Creating a Release

To create a new release:

1. **Update version** (if needed) in `manifest.json`
2. **Commit changes** and push to main
3. **Create and push a tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
4. **GitHub Actions will automatically**:
   - Run full test suite
   - Build DXT package
   - Create GitHub release
   - Upload DXT file for distribution

## Status Badges

Add these badges to your README.md:

```markdown
[![Test](https://github.com/YOUR_USERNAME/mcp-apple-notes-py/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/mcp-apple-notes-py/actions/workflows/test.yml)
[![Code Quality](https://github.com/YOUR_USERNAME/mcp-apple-notes-py/actions/workflows/quality.yml/badge.svg)](https://github.com/YOUR_USERNAME/mcp-apple-notes-py/actions/workflows/quality.yml)
```

## Requirements

- All workflows run on Ubuntu Linux (tests are mocked, no macOS required)
- Python 3.13 is installed via `actions/setup-python@v5`
- UV package manager is installed from official source
- Tests must pass before any release is created