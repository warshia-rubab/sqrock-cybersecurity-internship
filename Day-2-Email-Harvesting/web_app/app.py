#!/usr/bin/env python3
"""
Flask Web Interface for Email Harvester
SQR CyberSecurity Internship - Day 2
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import sys
from datetime import datetime
import threading
import re

# Add parent directory to path for importing the harvester
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Change working directory
os.chdir(parent_dir)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Global variable to store harvest status
harvest_status = {
    'running': False,
    'progress': 0,
    'url': '',
    'results': None,
    'error': None
}

def run_harvest(url):
    """Run the email harvester in a separate thread"""
    global harvest_status
    
    try:
        from src.email_harvester import EmailHarvester
        
        harvest_status['running'] = True
        harvest_status['progress'] = 0
        harvest_status['url'] = url
        harvest_status['error'] = None
        
        # Create harvester instance
        harvester = EmailHarvester(rate_limit=1, max_depth=1)
        
        harvest_status['progress'] = 20
        
        # Perform harvest
        results = harvester.harvest_from_url(url, depth=0)
        
        harvest_status['progress'] = 60
        
        # Analyze results
        analysis = harvester.analyze_email_patterns(harvester.found_emails)
        
        harvest_status['progress'] = 80
        
        # Generate report
        report = harvester.generate_professional_report(results, analysis)
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"reports/email_harvest_{timestamp}.html"
        
        os.makedirs('reports', exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report)
        
        # Save JSON
        json_path = f"data/emails_{timestamp}.json"
        os.makedirs('data', exist_ok=True)
        with open(json_path, 'w') as f:
            json.dump({
                'url': url,
                'timestamp': timestamp,
                'total_emails': len(harvester.found_emails),
                'emails': list(harvester.found_emails),
                'analysis': analysis
            }, f, indent=2, default=str)
        
        harvest_status['results'] = {
            'url': url,
            'total_emails': len(harvester.found_emails),
            'emails': list(harvester.found_emails),
            'analysis': analysis,
            'report_path': report_path,
            'json_path': json_path
        }
        
        harvest_status['progress'] = 100
        harvest_status['running'] = False
        
    except Exception as e:
        harvest_status['error'] = str(e)
        harvest_status['running'] = False
        harvest_status['progress'] = 0

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/harvest', methods=['POST'])
def harvest():
    """Start a new harvest"""
    global harvest_status
    
    if harvest_status['running']:
        return jsonify({'error': 'Harvest already in progress'}), 400
    
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Start harvest in background thread
    thread = threading.Thread(target=run_harvest, args=(url,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started', 'url': url})

@app.route('/status')
def status():
    """Get harvest status"""
    global harvest_status
    
    response = {
        'running': harvest_status['running'],
        'progress': harvest_status['progress'],
        'url': harvest_status['url'],
        'error': harvest_status['error']
    }
    
    if not harvest_status['running'] and harvest_status['results']:
        response['results'] = harvest_status['results']
    
    return jsonify(response)

@app.route('/download/<file_type>/<filename>')
def download(file_type, filename):
    """Download report files"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, file_type, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("🚀 Starting Email Harvester Web App")
    print("📁 Working directory:", os.getcwd())
    app.run(debug=True, host='0.0.0.0', port=5001)
