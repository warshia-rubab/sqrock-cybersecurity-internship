#!/usr/bin/env python3
"""
Advanced Email Harvester - Professional Implementation
SQR CyberSecurity Internship - Day 2
"""

import re
import json
import logging
import requests
from urllib.parse import urlparse, urljoin
from typing import Set, Dict, List, Optional
import time
from bs4 import BeautifulSoup
from datetime import datetime
from collections import Counter
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_harvester.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class EmailHarvester:
    """
    Professional email harvester with multiple extraction techniques
    """
    
    def __init__(self, rate_limit: int = 2, max_depth: int = 1):
        """
        Initialize the email harvester
        
        Args:
            rate_limit: Minimum seconds between requests
            max_depth: Maximum depth for recursive crawling
        """
        self.rate_limit = rate_limit
        self.max_depth = max_depth
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Email patterns
        self.email_patterns = {
            'standard': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            'obfuscated_at': re.compile(r'[a-zA-Z0-9._%+-]+\s*\[at\]\s*[a-zA-Z0-9.-]+\s*\[dot\]\s*[a-zA-Z]{2,}'),
            'mailto': re.compile(r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
        }
        
        self.found_emails = set()
        self.visited_urls = set()
        self.harvest_results = {}
        
    def _rate_limit(self):
        """Implement rate limiting to avoid detection"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit:
            wait_time = self.rate_limit - time_since_last
            time.sleep(wait_time)
        self.last_request_time = time.time()
    
    def _extract_emails_from_text(self, text: str) -> Set[str]:
        """Extract emails from text using multiple patterns"""
        if not text:
            return set()
        
        emails = set()
        
        # Try standard pattern
        standard_matches = self.email_patterns['standard'].findall(text)
        emails.update(standard_matches)
        
        # Try obfuscated pattern
        for match in self.email_patterns['obfuscated_at'].findall(text):
            clean = match.replace('[at]', '@').replace('[dot]', '.')
            clean = clean.replace('(at)', '@').replace('(dot)', '.')
            clean = clean.replace(' at ', '@').replace(' dot ', '.')
            emails.add(clean)
        
        # Try mailto pattern
        mailto_matches = self.email_patterns['mailto'].findall(text)
        emails.update(mailto_matches)
        
        return emails
    
    def harvest_from_url(self, url: str, depth: int = 0) -> Dict[str, any]:
        """
        Harvest emails from a URL and optionally follow links
        """
        if depth > self.max_depth:
            return {'url': url, 'emails': [], 'depth': depth, 'skipped': True}
        
        if url in self.visited_urls:
            return {'url': url, 'emails': [], 'depth': depth, 'skipped': True}
        
        self.visited_urls.add(url)
        
        logger.info(f"Harvesting from URL: {url} (depth: {depth})")
        
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        
        result = {
            'url': url,
            'emails': set(),
            'links_found': [],
            'harvest_errors': [],
            'depth': depth,
            'skipped': False,
            'sub_harvests': []
        }
        
        try:
            self._rate_limit()
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Extract emails from HTML
            emails = self._extract_emails_from_text(response.text)
            
            # Parse HTML for better extraction
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract emails from text nodes - FIXED: using string=True instead of text=True
            for text_node in soup.find_all(string=True):
                if text_node.strip():
                    text_emails = self._extract_emails_from_text(text_node)
                    emails.update(text_emails)
            
            # Extract from mailto: links
            for mailto_link in soup.find_all('a', href=True):
                href = mailto_link.get('href', '')
                if href.startswith('mailto:'):
                    email = href.replace('mailto:', '').split('?')[0]
                    if '@' in email:
                        emails.add(email)
            
            result['emails'] = emails
            self.found_emails.update(emails)
            
        except requests.RequestException as e:
            error_msg = f"Request failed for {url}: {str(e)}"
            logger.error(error_msg)
            result['harvest_errors'].append(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error for {url}: {str(e)}"
            logger.error(error_msg)
            result['harvest_errors'].append(error_msg)
        
        return result
    
    def analyze_email_patterns(self, emails: Set[str]) -> Dict[str, any]:
        """Analyze email patterns"""
        analysis = {
            'total_emails': len(emails),
            'domains': {},
            'username_patterns': {},
            'common_formats': [],
            'unique_domains': []
        }
        
        for email in emails:
            try:
                username, domain = email.split('@')
                
                # Count domains
                analysis['domains'][domain] = analysis['domains'].get(domain, 0) + 1
                
                # Detect pattern
                if '.' in username:
                    analysis['common_formats'].append('first.last')
                elif '_' in username:
                    analysis['common_formats'].append('first_last')
                elif username.isdigit():
                    analysis['common_formats'].append('numeric')
                else:
                    analysis['common_formats'].append('single_word')
                    
            except ValueError:
                continue
        
        # Get most common formats
        analysis['common_formats'] = list(set(analysis['common_formats']))
        analysis['unique_domains'] = list(set(analysis['domains'].keys()))
        
        return analysis
    
    def generate_professional_report(self, harvest_results: Dict, email_analysis: Dict) -> str:
        """Generate a professional HTML report"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        emails = self.found_emails
        
        report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Email Harvesting Analysis Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 40px;
                    background: #0a0e17;
                    color: #e0e6ed;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: #151d2b;
                    padding: 30px;
                    border-radius: 16px;
                    border: 1px solid #1e3a5f;
                }}
                .header {{
                    background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
                    padding: 30px;
                    border-radius: 12px;
                    margin-bottom: 30px;
                    text-align: center;
                    border-bottom: 2px solid #4facfe;
                }}
                .header h1 {{ color: #4facfe; font-size: 32px; }}
                .header p {{ color: #8892b0; }}
                .stats-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 20px;
                    margin: 20px 0;
                }}
                .stat-card {{
                    background: #0d1b2a;
                    padding: 20px;
                    border-radius: 12px;
                    border: 1px solid #1e3a5f;
                    text-align: center;
                }}
                .stat-number {{ font-size: 36px; font-weight: 700; color: #4facfe; }}
                .stat-label {{ color: #8892b0; font-size: 14px; }}
                .section {{
                    margin: 20px 0;
                    padding: 20px;
                    background: #0d1b2a;
                    border-radius: 12px;
                    border: 1px solid #1e3a5f;
                }}
                .section h2 {{ color: #4facfe; border-bottom: 1px solid #1e3a5f; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #1a2a3f; }}
                th {{ background: #1a2a3f; color: #4facfe; }}
                td {{ color: #e0e6ed; }}
                .email-list {{
                    max-height: 300px;
                    overflow-y: auto;
                    background: #0d1b2a;
                    padding: 15px;
                    border-radius: 8px;
                    border: 1px solid #1e3a5f;
                }}
                .email-list ul {{ list-style: none; padding: 0; }}
                .email-list li {{ padding: 6px 10px; border-bottom: 1px solid #1a2a3f; font-family: monospace; }}
                .warning {{
                    background: #fff3cd;
                    padding: 15px;
                    border-radius: 8px;
                    border-left: 4px solid #ffc107;
                    color: #856404;
                }}
                .footer {{ text-align: center; margin-top: 30px; padding: 20px; border-top: 1px solid #1e3a5f; color: #4a5a72; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔍 Email Harvesting Analysis Report</h1>
                    <p>Generated: {timestamp}</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{len(emails)}</div>
                        <div class="stat-label">Total Emails Found</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(email_analysis.get('unique_domains', []))}</div>
                        <div class="stat-label">Unique Domains</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(self.visited_urls)}</div>
                        <div class="stat-label">Pages Scanned</div>
                    </div>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Educational Use Notice:</strong> This report is generated for authorized testing only.
                </div>
                
                <div class="section">
                    <h2>📧 Discovered Emails</h2>
                    <div class="email-list">
                        <ul>
                            {''.join([f'<li>{email}</li>' for email in sorted(emails)])}
                        </ul>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🌐 Domain Analysis</h2>
                    <table>
                        <tr><th>Domain</th><th>Count</th></tr>
                        {''.join([f'<tr><td>{domain}</td><td>{count}</td></tr>' for domain, count in sorted(email_analysis.get('domains', {}).items(), key=lambda x: x[1], reverse=True)])}
                    </table>
                </div>
                
                <div class="footer">
                    <p>Generated by SQR CyberSecurity Email Harvester</p>
                    <p>For educational purposes only</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return report


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     SQR CyberSecurity - Advanced Email Harvester        ║
    ║             Professional Implementation                  ║
    ║                 (Educational Use Only)                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    url = input("Enter URL to harvest emails from (e.g., example.com): ").strip()
    
    if not url:
        print("❌ No URL provided. Exiting.")
        return
    
    print(f"\n🔍 Starting email harvest for: {url}")
    print("⏳ This may take a moment...\n")
    
    harvester = EmailHarvester(rate_limit=1, max_depth=1)
    
    try:
        results = harvester.harvest_from_url(url, depth=0)
        analysis = harvester.analyze_email_patterns(harvester.found_emails)
        report = harvester.generate_professional_report(results, analysis)
        
        os.makedirs('reports', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = f"reports/email_harvest_{timestamp}.html"
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        print(f"\n✅ Harvest completed successfully!")
        print(f"📧 Emails Found: {len(harvester.found_emails)}")
        print(f"📊 Report Generated: {report_path}")
        
        if harvester.found_emails:
            print("\n📧 Sample Emails Found:")
            for email in list(harvester.found_emails)[:5]:
                print(f"  - {email}")
        
    except Exception as e:
        logger.error(f"Harvest failed: {e}")
        print(f"\n❌ Harvest failed: {e}")


if __name__ == "__main__":
    main()
