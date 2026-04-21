#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
from colorama import Fore, init

init(autoreset=True)

def update_from_github():
    print(f"{Fore.CYAN}[*] Checking for updates from GitHub...")
    
    try:
        # Pull latest code
        result = subprocess.run(["git", "pull", "origin", "main"], 
                              capture_output=True, 
                              text=True)
        
        if "Already up to date" in result.stdout:
            print(f"{Fore.YELLOW}[!] Already up to date")
            return False
        elif result.returncode == 0:
            print(f"{Fore.GREEN}[+] Update successful!")
            print(result.stdout)
            
            # Update dependencies
            print(f"{Fore.CYAN}[*] Updating dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            
            return True
        else:
            print(f"{Fore.RED}[-] Update failed!")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        return False

def update_version_file():
    """Update version.txt with latest"""
    try:
        # Read current version
        with open("version.txt", "r") as f:
            current = f.read().strip()
        
        # Simple bump - you can make this smarter
        parts = current.split('.')
        if len(parts) == 3:
            parts[2] = str(int(parts[2]) + 1)
            new_version = '.'.join(parts)
            
            with open("version.txt", "w") as f:
                f.write(new_version)
            
            print(f"{Fore.GREEN}[+] Version updated: {current} -> {new_version}")
            return new_version
    except:
        # Create version file if doesn't exist
        with open("version.txt", "w") as f:
            f.write("1.0.0")
        return "1.0.0"

if __name__ == "__main__":
    print(f"{Fore.YELLOW}🔄 BGMI DDoS Bot Updater")
    print(f"{Fore.CYAN}="*50)
    
    updated = update_from_github()
    
    if updated:
        new_version = update_version_file()
        print(f"\n{Fore.GREEN}✅ Update complete! Version: {new_version}")
        print(f"{Fore.YELLOW}[!] Restart the bot to apply changes")
    else:
        print(f"\n{Fore.YELLOW}⚠️ No updates available")
