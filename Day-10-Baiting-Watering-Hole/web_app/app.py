#!/usr/bin/env python3
"""
Flask Web Application for Baiting & Watering Hole Simulator
SQR CyberSecurity Internship - Day 10
"""

from flask import Flask, render_template, request, jsonify, redirect, send_file
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

@app.route('/generate-bait', methods=['POST'])
def generate_bait():
    data = request.get_json()
    bait_type = data.get('bait_type', 'free_gift')
    
    try:
        from src.baiting_simulator import BaitingSimulator
        
        simulator = BaitingSimulator()
        link = simulator.generate_bait_link(bait_type)
        
        return jsonify(link)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bait/<link_id>')
def bait_link(link_id):
    try:
        from src.baiting_simulator import BaitingSimulator, ATTACK_LOGS
        
        simulator = BaitingSimulator()
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        path = request.path
        
        log = simulator.log_attack(link_id, ip, user_agent, path)
        
        if log.get('error'):
            return "Bait link not found", 404
        
        return render_template('bait.html', log=log)
        
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/waterhole', methods=['POST'])
def waterhole():
    data = request.get_json()
    target_type = data.get('target_type', 'tech_news_site')
    
    try:
        from src.baiting_simulator import BaitingSimulator
        
        simulator = BaitingSimulator()
        attack = simulator.simulate_watering_hole(target_type)
        
        return jsonify(attack)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs')
def logs():
    try:
        from src.baiting_simulator import BaitingSimulator
        
        simulator = BaitingSimulator()
        logs = simulator.get_attack_logs()
        summary = simulator.get_attack_summary()
        
        return jsonify({'logs': logs, 'summary': summary})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bait-links')
def bait_links():
    try:
        from src.baiting_simulator import BaitingSimulator
        
        simulator = BaitingSimulator()
        links = simulator.get_bait_links()
        
        return jsonify({'links': links})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🎯 Starting Baiting & Watering Hole Simulator Web App")
    print("📁 Working directory:", os.getcwd())
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5009)
