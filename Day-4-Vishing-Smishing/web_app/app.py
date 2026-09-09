#!/usr/bin/env python3
"""
Flask Web Application for Vishing & Smishing Generator
SQR CyberSecurity Internship - Day 4
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

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    category = data.get('category', '').strip().lower()
    
    if not category:
        return jsonify({'error': 'Category is required'}), 400
    
    try:
        from src.vishing_generator import VishingGenerator
        
        generator = VishingGenerator()
        
        if category == 'smishing':
            result = generator.generate_smishing_message('it_support')
            return jsonify(result)
        elif category in ['it_support', 'bank', 'government']:
            result = generator.generate_vishing_script(category)
            return jsonify(result)
        else:
            return jsonify({'error': f'Unknown category: {category}. Available: it_support, bank, government, smishing'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("📞 Starting Vishing & Smishing Generator Web App")
    print("📁 Working directory:", os.getcwd())
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5003)
