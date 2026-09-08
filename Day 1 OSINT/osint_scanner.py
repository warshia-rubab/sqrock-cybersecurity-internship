#!/usr/bin/env python3
"""
Sqrock Cybersecurity Internship - Day 1
Professional OSINT Scanner - Kali Linux Version
"""

import whois
import socket
import requests
import json
from datetime import datetime
import os
import sys

class OSINTScanner:
    """Professional OSINT scanner with comprehensive features"""
    
    def __init__(self, domain):
        self.domain = domain
        self.results = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def get_whois(self):
        """Get WHOIS information"""
        print("  📋 Gathering WHOIS information...")
        try:
            w = whois.whois(self.domain)
            return {
                'registrar': w.registrar,
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': w.name_servers,
                'emails': w.emails,
                'status': w.status
            }
        except Exception as e:
            print(f"  ⚠️ WHOIS error: {e}")
            return {'error': str(e)}
    
    def get_ip_info(self):
        """Get IP and geolocation"""
        print("  🌐 Getting IP geolocation...")
        try:
            ip = socket.gethostbyname(self.domain)
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = response.json()
            return {
                'ip': ip,
                'country': data.get('country', 'Unknown'),
                'city': data.get('city', 'Unknown'),
                'isp': data.get('isp', 'Unknown'),
                'org': data.get('org', 'Unknown'),
                'as': data.get('as', 'Unknown'),
                'timezone': data.get('timezone', 'Unknown')
            }
        except Exception as e:
            print(f"  ⚠️ IP info error: {e}")
            return {'error': str(e)}
    
    def get_dns_records(self):
        """Get DNS records"""
        print("  🔧 Enumerating DNS records...")
        try:
            import dns.resolver
            records = {}
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
            
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(self.domain, record_type)
                    records[record_type] = [str(r) for r in answers]
                except:
                    records[record_type] = []
            
            return records
        except Exception as e:
            print(f"  ⚠️ DNS error: {e}")
            return {'error': str(e)}
    
    def check_security_headers(self):
        """Check security headers"""
        print("  🛡️ Checking security headers...")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; OSINT-Scanner/1.0)'
            }
            response = requests.get(f"https://{self.domain}", headers=headers, timeout=5)
            
            security_headers = {
                'Strict-Transport-Security': 'Not Set',
                'Content-Security-Policy': 'Not Set',
                'X-Frame-Options': 'Not Set',
                'X-Content-Type-Options': 'Not Set',
                'Referrer-Policy': 'Not Set'
            }
            
            for header in security_headers:
                if header in response.headers:
                    security_headers[header] = '✅ Set'
            
            return security_headers
        except:
            return {'error': 'Could not check HTTPS headers'}
    
    def calculate_risk_score(self):
        """Calculate risk score based on findings"""
        score = 0
        
        # Check WHOIS privacy
        if self.results.get('whois', {}).get('emails'):
            score += 10
        
        # Check DNS records
        dns = self.results.get('dns_records', {})
        if dns.get('A'):
            score += 5
        
        # Check security headers
        headers = self.results.get('security_headers', {})
        for header, status in headers.items():
            if status == 'Not Set':
                score += 5
        
        return min(score, 100)
    
    def scan(self):
        """Perform complete scan"""
        print(f"\n🔍 Scanning: {self.domain}")
        print("="*60)
        
        # Perform all scans
        self.results['whois'] = self.get_whois()
        self.results['ip_info'] = self.get_ip_info()
        self.results['dns_records'] = self.get_dns_records()
        self.results['security_headers'] = self.check_security_headers()
        self.results['timestamp'] = datetime.now().isoformat()
        self.results['risk_score'] = self.calculate_risk_score()
        
        return self.results
    
    def generate_markdown_report(self):
        """Generate professional Markdown report"""
        whois = self.results.get('whois', {})
        ip = self.results.get('ip_info', {})
        dns = self.results.get('dns_records', {})
        headers = self.results.get('security_headers', {})
        
        report = f"""
# 🔍 OSINT Security Assessment Report

**Target Domain:** {self.domain}  
**Scan Date:** {self.results.get('timestamp', 'N/A')}  
**Risk Score:** {self.results.get('risk_score', 0)}/100  

---

## 📋 WHOIS Information

| Field | Value |
|-------|-------|
| **Registrar** | {whois.get('registrar', 'N/A')} |
| **Creation Date** | {whois.get('creation_date', 'N/A')} |
| **Expiration Date** | {whois.get('expiration_date', 'N/A')} |
| **Name Servers** | {', '.join(whois.get('name_servers', ['N/A'])) if whois.get('name_servers') else 'N/A'} |
| **Emails** | {', '.join(whois.get('emails', ['N/A'])) if whois.get('emails') else 'N/A'} |

---

## 🌐 IP & Geolocation

| Field | Value |
|-------|-------|
| **IP Address** | {ip.get('ip', 'N/A')} |
| **Country** | {ip.get('country', 'N/A')} |
| **City** | {ip.get('city', 'N/A')} |
| **ISP** | {ip.get('isp', 'N/A')} |
| **Organization** | {ip.get('org', 'N/A')} |
| **AS Number** | {ip.get('as', 'N/A')} |
| **Timezone** | {ip.get('timezone', 'N/A')} |

---

## 🔧 DNS Records

| Record Type | Values |
|-------------|--------|
"""
        
        for record_type, values in dns.items():
            if values:
                report += f"| **{record_type}** | {', '.join(values)} |\n"
            else:
                report += f"| **{record_type}** | No records found |\n"
        
        report += f"""

## 🛡️ Security Headers

| Header | Status |
|--------|--------|
"""
        
        for header, status in headers.items():
            report += f"| **{header}** | {status} |\n"
        
        report += f"""

## 📊 Risk Assessment

**Risk Score:** {self.results.get('risk_score', 0)}/100

### Findings:
"""
        
        # Add findings based on results
        findings = []
        
        if whois.get('emails'):
            findings.append("⚠️ Email addresses found in WHOIS - potential target for social engineering")
        
        if not whois.get('name_servers'):
            findings.append("⚠️ No name servers found - DNS configuration issue")
        
        for header, status in headers.items():
            if status == 'Not Set':
                findings.append(f"⚠️ Missing security header: {header}")
        
        if not findings:
            findings.append("✅ No critical issues found")
        
        for finding in findings:
            report += f"- {finding}\n"
        
        report += f"""

## 🛠️ Recommendations

1. **Review WHOIS Privacy** - Consider using WHOIS privacy protection
2. **Implement Missing Security Headers** - Add security headers to protect against attacks
3. **Regular DNS Monitoring** - Monitor DNS records for unauthorized changes
4. **SSL/TLS Configuration** - Ensure proper SSL/TLS configuration
5. **Security Audit** - Conduct regular security assessments

---

## 📝 Methodology

This scan was performed using:
- **WHOIS lookup** for domain registration information
- **DNS enumeration** for record discovery
- **IP geolocation** via public APIs
- **Security header analysis**

---

## ⚠️ Disclaimer

This report is for **educational purposes only**. All information gathered is from public sources. No active exploitation was performed.

---
*Report generated by Sqrock Cybersecurity OSINT Scanner*
"""
        
        return report
    
    def save_reports(self):
        """Save all reports"""
        # Create report filename
        report_filename = f"reports/osint_report_{self.domain}_{self.timestamp}.md"
        json_filename = f"data/osint_data_{self.domain}_{self.timestamp}.json"
        
        # Save Markdown report
        with open(report_filename, 'w') as f:
            f.write(self.generate_markdown_report())
        
        # Save JSON data
        with open(json_filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n✅ Reports saved:")
        print(f"   📄 Markdown Report: {report_filename}")
        print(f"   📊 JSON Data: {json_filename}")
        
        return report_filename, json_filename

def main():
    """Main function with professional interface"""
    
    # Clear screen for clean look
    os.system('clear')
    
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║      Sqrock Cybersecurity - Professional OSINT Scanner          ║
    ║                    Day 1 - Kali Linux Version                    ║
    ║                      Educational Use Only                        ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    print("📋 This tool performs passive reconnaissance using public data only.")
    print("⚠️  Ensure you have permission to scan the target domain.\n")
    
    # Get domain from user
    domain = input("Enter domain to scan (e.g., example.com): ").strip()
    
    if not domain:
        print("\n❌ No domain entered! Exiting...")
        return
    
    print(f"\n🚀 Starting OSINT scan for: {domain}")
    print("⏳ This may take a few seconds...\n")
    
    try:
        # Create scanner instance
        scanner = OSINTScanner(domain)
        
        # Perform scan
        results = scanner.scan()
        
        # Save reports
        scanner.save_reports()
        
        # Show summary
        print(f"\n📊 SCAN SUMMARY")
        print("="*60)
        print(f"Domain: {domain}")
        print(f"Risk Score: {results.get('risk_score', 0)}/100")
        print(f"IP Address: {results.get('ip_info', {}).get('ip', 'N/A')}")
        print(f"Location: {results.get('ip_info', {}).get('city', 'N/A')}, {results.get('ip_info', {}).get('country', 'N/A')}")
        print("="*60)
        
        print("\n✅ Scan completed successfully!")
        print("\n💡 Recommendations:")
        print("  1. Open the generated Markdown report")
        print("  2. Convert to PDF for professional submission")
        print("  3. Include screenshots in your portfolio")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Scan interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("💡 Try a different domain or check your internet connection")

if __name__ == "__main__":
    main()
