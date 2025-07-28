Create a minor version release by:

1. Update CHANGELOG.md with new features and improvements under a new version section
2. Commit the changelog updates
3. Create and push a git tag with the new minor version (increment Y in X.Y.Z, reset Z to 0)
4. The GitHub Actions release workflow will automatically build and publish the DXT package

Minor releases should include new features, enhancements, or significant improvements that maintain backward compatibility.

Before proceeding, ensure:
- All tests pass: `uv run pytest tests/ -v`
- Code quality checks pass
- New features are properly documented in CHANGELOG.md
- No breaking changes are introduced

Push the version tag to trigger automated DXT building and GitHub release creation.