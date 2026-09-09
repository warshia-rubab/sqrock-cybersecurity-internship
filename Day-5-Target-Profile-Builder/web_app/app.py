#!/usr/bin/env python3
"""
Flask Web Application for Target Profile Builder
SQR CyberSecurity Internship - Day 5
"""

from flask import Flask, render_template, request, jsonify, send_file
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

@app.route('/build-profile', methods=['POST'])
def build_profile():
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    try:
        from src.profile_builder import TargetProfileBuilder
        
        builder = TargetProfileBuilder()
        profile = builder.build_profile(username)
        
        if profile.get('github_data', {}).get('error'):
            return jsonify({'error': profile['github_data']['error']}), 404
        
        return jsonify(profile)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-profile')
def test_profile():
    """Get a test profile for demo"""
    try:
        from src.profile_builder import TargetProfileBuilder
        
        builder = TargetProfileBuilder()
        profile = builder.build_profile('torvalds')
        
        if profile.get('github_data', {}).get('error'):
            return jsonify({'error': profile['github_data']['error']}), 404
        
        return jsonify(profile)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🎯 Starting Target Profile Builder Web App")
    print("📁 Working directory:", os.getcwd())
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5004)
