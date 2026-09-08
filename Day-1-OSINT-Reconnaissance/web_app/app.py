#!/usr/bin/env python3
"""
Flask Web Application for OSINT Scanner
Sqrock Cybersecurity Internship - Day 1
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import sys
from datetime import datetime
import threading

# Add parent directory to path for importing the scanner
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Change working directory to parent so reports save correctly
os.chdir(parent_dir)
print(f"📁 Working directory: {os.getcwd()}")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Global variable to store scan status
scan_status = {
    'running': False,
    'progress': 0,
    'domain': '',
    'results': None,
    'error': None
}

def run_scan(domain):
    """Run the OSINT scanner in a separate thread"""
    global scan_status
    
    try:
        # Import the scanner
        from osint_scanner import OSINTScanner
        
        scan_status['running'] = True
        scan_status['progress'] = 0
        scan_status['domain'] = domain
        scan_status['error'] = None
        
        # Create scanner instance
        scanner = OSINTScanner(domain)
        
        # Update progress
        scan_status['progress'] = 20
        
        # Perform scan
        results = scanner.scan()
        
        scan_status['progress'] = 60
        
        # Save reports
        report_files = scanner.save_reports()
        
        scan_status['progress'] = 80
        
        # Store results
        scan_status['results'] = {
            'domain': domain,
            'risk_score': results.get('risk_score', 0),
            'ip': results.get('ip_info', {}).get('ip', 'N/A'),
            'country': results.get('ip_info', {}).get('country', 'N/A'),
            'city': results.get('ip_info', {}).get('city', 'N/A'),
            'whois': results.get('whois', {}),
            'dns_records': results.get('dns_records', {}),
            'security_headers': results.get('security_headers', {}),
            'report_files': report_files
        }
        
        scan_status['progress'] = 100
        scan_status['running'] = False
        print(f"✅ Scan complete! Results: {scan_status['results']['risk_score']}/100")
        
    except Exception as e:
        scan_status['error'] = str(e)
        scan_status['running'] = False
        scan_status['progress'] = 0
        print(f"❌ Scan error: {e}")

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    """Start a new scan"""
    global scan_status
    
    if scan_status['running']:
        return jsonify({'error': 'Scan already in progress'}), 400
    
    data = request.get_json()
    domain = data.get('domain', '').strip()
    
    if not domain:
        return jsonify({'error': 'Domain is required'}), 400
    
    print(f"🚀 Starting scan for: {domain}")
    
    # Start scan in background thread
    thread = threading.Thread(target=run_scan, args=(domain,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started', 'domain': domain})

@app.route('/status')
def status():
    """Get scan status"""
    global scan_status
    
    # Check if results exist and add them to response
    response = {
        'running': scan_status['running'],
        'progress': scan_status['progress'],
        'domain': scan_status['domain'],
        'error': scan_status['error']
    }
    
    # Only add results if scan is complete
    if not scan_status['running'] and scan_status['results']:
        response['results'] = scan_status['results']
    
    return jsonify(response)

@app.route('/download/<file_type>/<filename>')
def download(file_type, filename):
    """Download report files"""
    # Get the base path (parent of web_app folder)
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Try multiple possible locations
    possible_paths = [
        os.path.join(base_path, file_type, filename),
        os.path.join(base_path, '..', file_type, filename),
        os.path.join(os.getcwd(), file_type, filename),
        os.path.join(os.getcwd(), '..', file_type, filename),
        os.path.join(base_path, 'web_app', file_type, filename),
    ]
    
    for file_path in possible_paths:
        if os.path.exists(file_path):
            print(f"✅ Found file: {file_path}")
            return send_file(file_path, as_attachment=True)
    
    print(f"❌ File not found: {filename} in {file_type}")
    return jsonify({'error': f'File not found: {filename}'}), 404

@app.route('/list_reports')
def list_reports():
    """List all available reports"""
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_path = os.path.join(base_path, 'reports')
    
    try:
        files = os.listdir(reports_path)
        return jsonify({'reports': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    print("="*60)
    print("🚀 Starting Sqrock OSINT Scanner Web App")
    print("="*60)
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📁 Reports will be saved in: {os.path.join(os.getcwd(), 'reports')}")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
