#!/usr/bin/env python3
"""
Flask Web Application for USB Drop Attack Simulator
SQR CyberSecurity Internship - Day 8
"""

from flask import Flask, render_template, request, jsonify
import json
import os
import sys
from datetime import datetime

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    payload_type = data.get('payload_type', 'recon')
    
    try:
        from src.usb_payload import USBPayloadSimulator
        
        simulator = USBPayloadSimulator()
        result = simulator.simulate_usb_insertion(payload_type)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("💾 Starting USB Drop Attack Simulator Web App")
    print("📁 Working directory:", os.getcwd())
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5007)
