import sys

def bump(current):
    version = current[1:]  # Remove 'v'
    parts = version.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
    
    bump_type = sys.argv[1] if len(sys.argv) > 1 else "patch"
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    
    new_version = f"v{major}.{minor}.{patch}"
    
    # Write
    with open("version.txt", "w") as f:
        f.write(new_version + "\n")
    
    print(f"Updated to {new_version}")
    
    # Commit
    import subprocess
    subprocess.run(["git", "add", "version.txt"])
    subprocess.run(["git", "commit", "-m", f"Bump to {new_version}"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    with open("version.txt", "r") as f:
        current = f.read().strip()
    
    bump(current)
