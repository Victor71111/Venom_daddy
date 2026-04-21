#!/usr/bin/env python3
import psutil
import time
import os
from datetime import datetime

def monitor_bot():
    """Monitor bot status and resources"""
    status = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "processes": []
    }
    
    # Check for bot processes
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            if 'python' in proc.info['name'].lower():
                if 'bot.py' in ' '.join(proc.cmdline()):
                    status["processes"].append({
                        "pid": proc.info['pid'],
                        "cpu": proc.info['cpu_percent'],
                        "memory": proc.info['memory_percent']
                    })
        except:
            pass
    
    # Format output
    output = f"""
📊 BGMI DDoS Bot Monitor
⏰ Time: {status['timestamp']}

🔧 System Resources:
  CPU Usage: {status['cpu_usage']}%
  Memory Usage: {status['memory_usage']}%
  Disk Usage: {status['disk_usage']}%

🤖 Bot Processes: {len(status['processes'])}
"""
    
    for i, proc in enumerate(status['processes'], 1):
        output += f"  Process {i}: PID {proc['pid']}, CPU {proc['cpu']}%, MEM {proc['memory']}%\n"
    
    # Check attack files
    attack_files = [f for f in os.listdir('.') if f.startswith('attack_') and f.endswith('.py')]
    output += f"\n💥 Attack Files: {len(attack_files)}"
    
    return output

if __name__ == "__main__":
    print(monitor_bot())
