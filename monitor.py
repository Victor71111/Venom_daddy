import time

def check_targets():
    targets = ["185.199.108.153", "185.199.109.153"]
    
    for target in targets:
        print(f"Checking {target}...")
        # Add actual check logic here
    
    print("Check complete")

if __name__ == "__main__":
    while True:
        check_targets()
        time.sleep(3600)  # Every hour
