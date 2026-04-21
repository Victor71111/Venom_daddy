from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/version')
def get_version():
    with open("version.txt", "r") as f:
        version = f.read().strip()
    
    return jsonify({
        "version": version,
        "name": "BGMI DDoS Bot",
        "update_url": "https://github.com/YOUR_USERNAME/bgmi-ddos",
        "changelog": "https://raw.githubusercontent.com/YOUR_USERNAME/bgmi-ddos/main/changelog.md"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
