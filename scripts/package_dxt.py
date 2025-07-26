#!/usr/bin/env python3
"""
Package script to create a DXT (Desktop Extension) archive.
Usage: uv run package_dxt.py
"""

import os
import shutil
import tempfile
import zipfile
from pathlib import Path
import json
import sys

def load_manifest():
    """Load and validate the manifest.json file."""
    manifest_path = Path("manifest.json")
    if not manifest_path.exists():
        print("❌ Error: manifest.json not found")
        sys.exit(1)
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    print(f"📋 Loaded manifest for: {manifest.get('display_name', manifest.get('name'))}")
    print(f"   Version: {manifest.get('version')}")
    print(f"   Description: {manifest.get('description')}")
    
    return manifest

def create_dxt_package():
    """Create a DXT package as a zip file."""
    manifest = load_manifest()
    
    # Get package name and version from manifest
    package_name = manifest.get('name', 'apple-notes-mcp')
    version = manifest.get('version', '0.1.0')
    output_filename = f"{package_name}-{version}.dxt"
    
    # Files to include in the DXT package
    files_to_include = [
        "manifest.json",
        "main.py",
        "pyproject.toml",
        "README.md",
        "uv.lock"
    ]
    
    # Optional files (include if they exist)
    optional_files = [
        "CLAUDE.md",
        "LICENSE",
        "icon.png"
    ]
    
    print(f"📦 Creating DXT package: {output_filename}")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as dxt_zip:
        # Add required files
        for file_path in files_to_include:
            if Path(file_path).exists():
                dxt_zip.write(file_path)
                print(f"   ✅ Added: {file_path}")
            else:
                print(f"   ❌ Missing required file: {file_path}")
                sys.exit(1)
        
        # Add optional files if they exist
        for file_path in optional_files:
            if Path(file_path).exists():
                dxt_zip.write(file_path)
                print(f"   ✅ Added: {file_path}")
            else:
                print(f"   ⚠️  Optional file not found: {file_path}")
    
    # Verify the package was created
    if Path(output_filename).exists():
        file_size = Path(output_filename).stat().st_size
        print(f"✅ DXT package created successfully!")
        print(f"   File: {output_filename}")
        print(f"   Size: {file_size:,} bytes")
        
        # Show installation instructions
        print(f"\n📖 Installation Instructions:")
        print(f"   1. Locate the file: {output_filename}")
        print(f"   2. In Claude Desktop, go to Settings → Extensions")
        print(f"   3. Click 'Install Extension' and select this file")
        print(f"   4. Grant necessary permissions when prompted")
        print(f"   5. Restart Claude Desktop to activate the extension")
        
        return output_filename
    else:
        print("❌ Failed to create DXT package")
        sys.exit(1)

def validate_manifest_schema():
    """Basic validation of manifest.json against DXT requirements."""
    manifest = load_manifest()
    
    required_fields = [
        'dxt_version',
        'name', 
        'version',
        'description',
        'server'
    ]
    
    print("🔍 Validating manifest...")
    
    for field in required_fields:
        if field not in manifest:
            print(f"❌ Missing required field: {field}")
            sys.exit(1)
    
    # Validate server configuration
    server = manifest.get('server', {})
    if server.get('type') != 'python':
        print("❌ Server type must be 'python' for this package")
        sys.exit(1)
    
    if not server.get('entry_point'):
        print("❌ Server entry_point is required")
        sys.exit(1)
    
    # Check if entry point file exists
    entry_point = server.get('entry_point')
    if not Path(entry_point).exists():
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