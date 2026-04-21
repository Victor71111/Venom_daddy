#!/usr/bin/env python3
import sys
import os
from datetime import datetime

def bump_version(version_type="patch"):
    """Bump version number"""
    try:
        with open("version.txt", "r") as f:
            current = f.read().strip()
        
        parts = current.split('.')
        if len(parts) != 3:
            parts = ["1", "0", "0"]
        
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        
        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        new_version = f"{major}.{minor}.{patch}"
        
        with open("version.txt", "w") as f:
            f.write(new_version)
        
        # Update changelog
        update_changelog(new_version)
        
        print(f"✅ Version bumped: {current} -> {new_version}")
        return new_version
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def update_changelog(new_version):
    """Update changelog.md"""
    changelog_entry = f"""
## v{new_version} - {datetime.now().strftime('%Y-%m-%d')}

### Added
- New features

### Changed
- Improvements

### Fixed
- Bug fixes

### Security
- Security updates
"""
    
    if os.path.exists("changelog.md"):
        with open("changelog.md", "r") as f:
            content = f.read()
        
        # Insert at beginning
        content = changelog_entry + "\n" + content
    else:
        content = changelog_entry
    
    with open("changelog.md", "w") as f:
        f.write(content)
    
    print(f"📝 Changelog updated for v{new_version}")

if __name__ == "__main__":
    # USAGE means how to use the script from command line
    if len(sys.argv) < 2:
        print("""
USAGE: python bump_version.py [type]

Types:
  patch  - Increment patch version (1.0.0 -> 1.0.1) [DEFAULT]
  minor  - Increment minor version (1.0.0 -> 1.1.0)
  major  - Increment major version (1.0.0 -> 2.0.0)

Examples:
  python bump_version.py patch
  python bump_version.py minor
  python bump_version.py major
        """)
        sys.exit(1)
    
    version_type = sys.argv[1] if len(sys.argv) > 1 else "patch"
    bump_version(version_type)
