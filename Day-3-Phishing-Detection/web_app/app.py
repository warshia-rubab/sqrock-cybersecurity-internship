#!/usr/bin/env python3
"""
Flask Web Application for Phishing URL Detector
SQR CyberSecurity Internship - Day 3
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import sys
from datetime import datetime

# Add parent directory to path for importing the detector
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze a URL for phishing indicators"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        from src.phishing_detector import PhishingDetector
        
        detector = PhishingDetector()
        analysis = detector.analyze_url(url)
        
        # Convert to dict for JSON response
        result = {
            'url': analysis.url,
            'risk_score': analysis.risk_score,
            'risk_level': analysis.risk_level,
            'indicators': analysis.indicators,
            'details': analysis.details,
            'recommendations': analysis.recommendations,
            'timestamp': analysis.timestamp
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test_urls')
def test_urls():
    """Get sample test URLs"""
    test_urls = [
        "https://github.com",
        "https://paypal-login.evil.com/verify",
        "http://login-bank-verification.top",
        "https://amazon.secure-login.net/update",
        "https://193.23.45.6/login",
        "https://www.google.com",
        "http://secure-update-account.info/verify"
    ]
    return jsonify({'urls': test_urls})

if __name__ == '__main__':
    print("="*60)
    print("🎣 Starting Phishing URL Detector Web App")
    print("📁 Working directory:", os.getcwd())
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5002)
