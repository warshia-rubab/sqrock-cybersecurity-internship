#!/usr/bin/env python3
"""
Flask Web Application for Spear Phishing Template Engine
SQR CyberSecurity Internship - Day 6
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

# Sample targets
SAMPLE_TARGETS = [
    {
        'name': 'Riya Sharma',
        'email': 'riya.sharma@company.com',
        'company': 'SQR CyberSecurity',
        'position': 'Security Engineer',
        'location': 'Bangalore, India',
        'department': 'IT Security'
    },
    {
        'name': 'Arjun Patel',
        'email': 'arjun.patel@company.com',
        'company': 'TechVault Solutions',
        'position': 'System Administrator',
        'location': 'Mumbai, India',
        'department': 'IT Operations'
    },
    {
        'name': 'Priya Singh',
        'email': 'priya.singh@company.com',
        'company': 'DataShield Inc',
        'position': 'Network Analyst',
        'location': 'Delhi, India',
        'department': 'Network Security'
    }
]

@app.route('/')
def index():
    return render_template('index.html', targets=SAMPLE_TARGETS)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    target_index = data.get('target_index', 0)
    template_type = data.get('template_type', 'account_verification')
    
    try:
        from src.phishing_template import SpearPhishingTemplate
        
        template_engine = SpearPhishingTemplate()
        
        if target_index < len(template_engine.sample_targets):
            target = template_engine.sample_targets[target_index]
        else:
            target = template_engine.sample_targets[0]
        
        if template_type == 'all':
            templates = template_engine.get_all_templates(target)
            return jsonify({'templates': templates, 'target': target})
        else:
            template = template_engine.generate_template(target, template_type)
            return jsonify({'template': template, 'target': target})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/targets')
def targets():
    return jsonify(SAMPLE_TARGETS)

if __name__ == '__main__':
    print("="*60)
    print("📧 Starting Spear Phishing Template Engine Web App")
    print("📁 Working directory:", os.getcwd())
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5005)
