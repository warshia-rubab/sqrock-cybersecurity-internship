#!/usr/bin/env python3
"""
Redirect to web_app/app.py
This file exists to handle the path issue.
"""

import os
import sys

# Change to web_app directory and run the actual app
web_app_path = os.path.join(os.path.dirname(__file__), 'web_app')
os.chdir(web_app_path)
sys.path.insert(0, web_app_path)

# Import and run the actual app
from app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
