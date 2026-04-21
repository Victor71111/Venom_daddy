#!/usr/bin/env python3
import zipfile
import os
import datetime
import shutil

def backup_attack_files():
    """Backup all attack scripts and configs"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}.zip"
    
    files_to_backup = [
        "bot.py",
        "ddos.py", 
        "m.py",
        "config.json",
        "targets.json",
        "version.txt",
        "changelog.md",
        "requirements.txt"
    ]
    
    # Add all attack scripts
    for file in os.listdir('.'):
        if file.startswith('attack_') and file.endswith('.py'):
            files_to_backup.append(file)
    
    # Create backup
    with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files_to_backup:
            if os.path.exists(file):
                zipf.write(file)
    
    # Create symlink to latest
    if os.path.exists("backup_latest.zip"):
        os.remove("backup_latest.zip")
    os.symlink(backup_name, "backup_latest.zip")
    
    # Keep only last 5 backups
    backups = sorted([f for f in os.listdir('.') if f.startswith('backup_') and f.endswith('.zip')])
    if len(backups) > 5:
        for old_backup in backups[:-5]:
            os.remove(old_backup)
    
    return f"✅ Backup created: {backup_name}\n📦 Files backed up: {len(files_to_backup)}\n💾 Size: {os.path.getsize(backup_name) / 1024:.1f} KB"

if __name__ == "__main__":
    print(backup_attack_files())
