Create a patch version release by:

1. Update CHANGELOG.md with bug fixes and small improvements under a new version section
2. Commit the changelog updates
3. Create and push a git tag with the new patch version (increment Z in X.Y.Z)
4. The GitHub Actions release workflow will automatically build and publish the DXT package

Patch releases should include bug fixes, security updates, or minor improvements that maintain backward compatibility.

Before proceeding, ensure:
- All tests pass: `uv run pytest tests/ -v`
- Code quality checks pass
- Bug fixes are properly documented in CHANGELOG.md
- No new features or breaking changes are introduced

Push the version tag to trigger automated DXT building and GitHub release creation.