#!/usr/bin/env python3
"""
Flask Web Application for Password Attack Simulator
SQR CyberSecurity Internship - Day 7
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

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    try:
        from src.password_attacks import PasswordAttackSimulator
        
        simulator = PasswordAttackSimulator()
        report = simulator.generate_report(username, password)
        
        return jsonify(report)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/common-passwords')
def common_passwords():
    from src.password_attacks import PasswordAttackSimulator
    simulator = PasswordAttackSimulator()
    return jsonify({'common_passwords': simulator.common_passwords[:10]})

if __name__ == '__main__':
    print("="*60)
    print("🔐 Starting Password Attack Simulator Web App")
    print("📁 Working directory:", os.getcwd())
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5006)
