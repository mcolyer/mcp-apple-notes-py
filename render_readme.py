#!/usr/bin/env python3
"""
Quick script to render README.md to HTML using the markdown module
"""

import markdown
import sys
from pathlib import Path

def render_readme():
    """Render README.md to HTML and save/display it"""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        print("❌ README.md not found")
        return
    
    # Read the markdown content
    with open(readme_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Configure markdown with extensions for better rendering
    md = markdown.Markdown(
        extensions=[
            'extra',           # Tables, fenced code blocks, etc.
            'codehilite',      # Syntax highlighting
            'toc',            # Table of contents
            'nl2br',          # Newline to <br>
        ],
        extension_configs={
            'codehilite': {
                'css_class': 'highlight'
            }
        }
    )
    
    # Convert markdown to HTML
    html_content = md.convert(md_content)
    
    # Create a complete HTML document
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apple Notes MCP Desktop Extension</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            color: #24292f;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        h1 {{ border-bottom: 1px solid #d0d7de; padding-bottom: 10px; }}
        h2 {{ border-bottom: 1px solid #d0d7de; padding-bottom: 10px; }}
        code {{
            background-color: #f6f8fa;
            border-radius: 6px;
            font-size: 85%;
            margin: 0;
            padding: 0.2em 0.4em;
        }}
        pre {{
            background-color: #f6f8fa;
            border-radius: 6px;
            font-size: 85%;
            line-height: 1.45;
            overflow: auto;
            padding: 16px;
        }}
        pre code {{
            background-color: transparent;
            border: 0;
            display: inline;
            line-height: inherit;
            margin: 0;
            max-width: auto;
            padding: 0;
            word-wrap: normal;
        }}
        blockquote {{
            border-left: 0.25em solid #d0d7de;
            color: #656d76;
            padding: 0 1em;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #d0d7de;
            padding: 6px 13px;
            text-align: left;
        }}
        th {{
            background-color: #f6f8fa;
            font-weight: 600;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        .highlight {{
            background-color: #f6f8fa;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # Save to HTML file
    output_path = Path("README.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ Rendered README.md to {output_path}")
    print(f"📖 Open in browser: open {output_path}")
    
    # Also print the first few lines to check for issues
    lines = md_content.split('\n')
    print(f"\n📋 First 10 lines of README.md:")
    for i, line in enumerate(lines[:10], 1):
        print(f"{i:2d}: {repr(line)}")
    
    # Check for problematic characters
    import re
    problematic_chars = re.findall(r'[^\x00-\x7F]', md_content)
    if problematic_chars:
        print(f"\n⚠️  Found {len(set(problematic_chars))} unique non-ASCII characters:")
        for char in sorted(set(problematic_chars)):
            print(f"   '{char}' (U+{ord(char):04X})")
    else:
        print(f"\n✅ No problematic non-ASCII characters found")

if __name__ == "__main__":
    render_readme()