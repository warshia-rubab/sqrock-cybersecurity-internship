#!/usr/bin/env python3
"""
Flask Web Application for Fake Profile Detection
SQR CyberSecurity Internship - Day 9
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

@app.route('/detect', methods=['POST'])
def detect():
    data = request.get_json()
    profile_index = data.get('profile_index', 0)
    
    try:
        from src.fake_profile_detector import FakeProfileDetector
        
        detector = FakeProfileDetector()
        profile = detector.get_profile(profile_index)
        
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        
        result = detector.detect_fake_profile(profile)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/detect-impersonation', methods=['POST'])
def detect_impersonation():
    data = request.get_json()
    profile1_index = data.get('profile1_index', 0)
    profile2_index = data.get('profile2_index', 1)
    
    try:
        from src.fake_profile_detector import FakeProfileDetector
        
        detector = FakeProfileDetector()
        profile1 = detector.get_profile(profile1_index)
        profile2 = detector.get_profile(profile2_index)
        
        if not profile1 or not profile2:
            return jsonify({'error': 'Profile not found'}), 404
        
        result = detector.detect_impersonation(profile1, profile2)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/profiles')
def profiles():
    from src.fake_profile_detector import FakeProfileDetector
    
    detector = FakeProfileDetector()
    profiles = detector.get_all_profiles()
    return jsonify({'profiles': profiles})

if __name__ == '__main__':
    print("="*60)
    print("👤 Starting Fake Profile Detection Web App")
    print("📁 Working directory:", os.getcwd())
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5008)
