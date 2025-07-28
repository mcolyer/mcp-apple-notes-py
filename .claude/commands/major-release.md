Create a major version release by:

1. Update CHANGELOG.md with breaking changes under a new version section
2. Commit the changelog updates
3. Create and push a git tag with the new major version (increment X in X.Y.Z)
4. The GitHub Actions release workflow will automatically build and publish the DXT package

Major releases should include breaking changes, significant new features, or major architectural changes.

Before proceeding, ensure:
- All tests pass: `uv run pytest tests/ -v`
- Code quality checks pass
- Breaking changes are clearly documented in CHANGELOG.md
- Migration guide is provided if needed

Push the version tag to trigger automated DXT building and GitHub release creation.