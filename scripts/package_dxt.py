#!/usr/bin/env python3
"""
Package script to create a DXT (Desktop Extension) archive.
Usage: uv run package_dxt.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def load_manifest():
    """Load and validate the manifest.json file."""
    manifest_path = Path("manifest.json")
    if not manifest_path.exists():
        print("❌ Error: manifest.json not found")
        sys.exit(1)

    with open(manifest_path) as f:
        manifest = json.load(f)

    print(
        f"📋 Loaded manifest for: {manifest.get('display_name', manifest.get('name'))}"
    )
    print(f"   Version: {manifest.get('version')}")
    print(f"   Description: {manifest.get('description')}")

    return manifest


def download_dependencies(lib_dir):
    """Install Python dependencies to lib directory using UV."""
    print("📥 Installing Python dependencies to lib/...")

    # Create lib directory
    lib_dir.mkdir(exist_ok=True)

    # Dependencies to install
    dependencies = ["mcp[cli]", "macnotesapp", "markdown", "apple-notes-parser"]

    print(f"   Installing dependencies: {', '.join(dependencies)}")
    try:
        # Use UV to install packages to target directory
        subprocess.run(  # noqa: S603, S607
            ["uv", "pip", "install", "--target", str(lib_dir), *dependencies],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
        )

        print("   ✅ Installed all dependencies")

        # List what was installed
        installed_dirs = [
            d for d in lib_dir.iterdir() if d.is_dir() and not d.name.startswith(".")
        ]
        installed_files = [
            f
            for f in lib_dir.iterdir()
            if f.is_file() and f.name.endswith((".py", ".so"))
        ]

        print(
            f"   📦 Installed {len(installed_dirs)} packages and {len(installed_files)} files:"  # noqa: E501
        )
        for item in sorted(installed_dirs + installed_files):
            if item.is_dir():
                print(f"      📁 {item.name}/")
            else:
                print(f"      📄 {item.name}")

    except subprocess.CalledProcessError as e:
        print(f"   ❌ Failed to install dependencies: {e}")
        print(f"   Error output: {e.stderr}")
        sys.exit(1)


def create_bundled_structure(temp_dir):
    """Create the bundled DXT structure in a temporary directory."""
    print("🏗️  Creating bundled structure...")

    # Create directories
    server_dir = temp_dir / "server"
    lib_dir = temp_dir / "lib"
    server_dir.mkdir()
    lib_dir.mkdir()

    # Copy main.py to server/
    shutil.copy("main.py", server_dir / "main.py")
    print("   ✅ Copied main.py to server/")

    # Install dependencies to lib/
    download_dependencies(lib_dir)

    # Copy other required files to root
    root_files = ["manifest.json", "requirements.txt", "README.md"]

    for file_path in root_files:
        if Path(file_path).exists():
            shutil.copy(file_path, temp_dir / file_path)
            print(f"   ✅ Copied {file_path}")

    # Copy optional files
    optional_files = ["CLAUDE.md", "LICENSE", "icon.png"]
    for file_path in optional_files:
        if Path(file_path).exists():
            shutil.copy(file_path, temp_dir / file_path)
            print(f"   ✅ Copied {file_path}")


def create_dxt_package():
    """Create a DXT package as a zip file with bundled dependencies."""
    manifest = load_manifest()

    # Get package name and version from manifest
    package_name = manifest.get("name", "apple-notes-mcp")
    version = manifest.get("version", "0.4.1")
    output_filename = f"{package_name}-{version}.dxt"

    print(f"📦 Creating bundled DXT package: {output_filename}")

    # Create temporary directory for bundled structure
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)

        # Create the bundled structure
        create_bundled_structure(temp_dir)

        # Create the ZIP file
        with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as dxt_zip:
            # Add all files from temp directory
            for file_path in temp_dir.rglob("*"):
                if file_path.is_file():
                    # Calculate relative path from temp_dir
                    relative_path = file_path.relative_to(temp_dir)
                    dxt_zip.write(file_path, relative_path)
                    print(f"   ✅ Added: {relative_path}")

    # Verify the package was created
    if Path(output_filename).exists():
        file_size = Path(output_filename).stat().st_size
        print("✅ Bundled DXT package created successfully!")
        print(f"   File: {output_filename}")
        print(f"   Size: {file_size:,} bytes")

        # Show installation instructions
        print("\n📖 Installation Instructions:")
        print(f"   1. Locate the file: {output_filename}")
        print("   2. In Claude Desktop, go to Settings → Extensions")
        print("   3. Click 'Install Extension' and select this file")
        print("   4. Grant necessary permissions when prompted")
        print("   5. Restart Claude Desktop to activate the extension")

        return output_filename
    else:
        print("❌ Failed to create DXT package")
        sys.exit(1)


def validate_manifest_schema():
    """Basic validation of manifest.json against DXT requirements."""
    manifest = load_manifest()

    required_fields = ["dxt_version", "name", "version", "description", "server"]

    print("🔍 Validating manifest...")

    for field in required_fields:
        if field not in manifest:
            print(f"❌ Missing required field: {field}")
            sys.exit(1)

    # Validate server configuration
    server = manifest.get("server", {})
    if server.get("type") != "python":
        print("❌ Server type must be 'python' for this package")
        sys.exit(1)

    if not server.get("entry_point"):
        print("❌ Server entry_point is required")
        sys.exit(1)

    # Check if entry point file exists (check original main.py for bundled structure)
    entry_point = server.get("entry_point")
    if entry_point == "server/main.py":
        # For bundled structure, check if main.py exists (will be moved to server/ during packaging)  # noqa: E501
        if not Path("main.py").exists():
            print(f"❌ Source file not found: main.py (needed for {entry_point})")
            sys.exit(1)
    elif not Path(entry_point).exists():
        print(f"❌ Entry point file not found: {entry_point}")
        sys.exit(1)

    print("✅ Manifest validation passed")


def main():
    """Main packaging function."""
    print("🚀 Apple Notes MCP DXT Packager")
    print("=" * 40)

    # Change to project root directory (parent of scripts)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)

    # Validate manifest
    validate_manifest_schema()

    # Create the package
    package_file = create_dxt_package()

    print("\n🎉 Packaging complete!")
    print(f"DXT package ready: {package_file}")


if __name__ == "__main__":
    main()
