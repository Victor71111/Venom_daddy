import requests
import os

def check_update():
    try:
        with open("version.txt", "r") as f:
            current = f.read().strip()
        
        # Get latest from GitHub
        url = "https://raw.githubusercontent.com/YOUR_USERNAME/bgmi-ddos-tool/main/version.txt"
        response = requests.get(url)
        latest = response.text.strip()
        
        return current != latest, latest
    except:
        return False, "unknown"

def update():
    print("Updating from GitHub...")
    os.system("git pull origin main")
    os.system("pip install -r requirements.txt")
    print("Update complete")

if __name__ == "__main__":
    needed, new_version = check_update()
    if needed:
        print(f"Update available: {new_version}")
        update()
    else:
        print("No updates")
