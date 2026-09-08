#!/usr/bin/env python3
"""
Advanced Phishing URL Detector - Professional Implementation
SQR CyberSecurity Internship - Day 3

Features:
- Multi-factor phishing detection
- URL structure analysis
- Domain age checking
- HTTPS validation
- Risk scoring (0-100)
- Detailed reporting
"""

import re
import json
import logging
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Tuple, Optional
import datetime
import whois
import socket
import requests
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('phishing_detector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class PhishingAnalysis:
    """Data structure for phishing analysis results"""
    url: str
    risk_score: int  # 0-100
    risk_level: str  # LOW, MEDIUM, HIGH, CRITICAL
    indicators: Dict[str, any]
    details: Dict[str, any]
    recommendations: List[str]
    timestamp: str


class PhishingDetector:
    """
    Professional phishing detection system with multiple analysis techniques
    """
    
    def __init__(self):
        """Initialize the phishing detector"""
        # Suspicious keywords
        self.suspicious_keywords = [
            'login', 'verify', 'secure', 'update', 'account', 'bank',
            'paypal', 'amazon', 'apple', 'microsoft', 'google',
            'confirm', 'validate', 'authenticate', 'security',
            'alert', 'suspended', 'locked', 'unusual', 'activity',
            'password', 'credential', 'signin', 'sign-in',
            'reset', 'recover', 'confirm', 'identity', 'verify'
        ]
        
        # Urgent keywords
        self.urgent_keywords = [
            'immediate', 'urgent', 'action', 'required', 'now',
            'today', 'hours', 'suspend', 'close', 'terminate',
            'expire', 'expired', 'limited', 'warning', 'alert'
        ]
        
        # Suspicious TLDs
        self.suspicious_tlds = {'.tk', '.ml', '.ga', '.cf', '.pw', '.top', '.xyz', '.click', '.loan', '.gq'}
        
        # Brand names for impersonation detection
        self.brands = ['paypal', 'amazon', 'apple', 'microsoft', 'google', 
                      'facebook', 'instagram', 'linkedin', 'twitter', 
                      'bank', 'chase', 'wellsfargo', 'citibank', 'boa',
                      'dropbox', 'spotify', 'netflix', 'adobe', 'salesforce']
    
    def analyze_url(self, url: str) -> PhishingAnalysis:
        """
        Comprehensive URL analysis for phishing detection
        """
        logger.info(f"Analyzing URL for phishing: {url}")
        
        # Parse URL
        parsed = urlparse(url)
        if not parsed.scheme:
            url = f"https://{url}"
            parsed = urlparse(url)
        
        # Initialize analysis
        indicators = {}
        details = {}
        risk_score = 0
        
        # Perform all checks
        indicators.update(self._check_protocol(parsed))
        indicators.update(self._check_url_structure(parsed))
        indicators.update(self._check_keywords(parsed))
        indicators.update(self._check_brand_impersonation(parsed))
        indicators.update(self._check_tld(parsed))
        indicators.update(self._check_url_length(parsed))
        indicators.update(self._check_ip_address(parsed))
        indicators.update(self._check_redirects(parsed))
        indicators.update(self._check_domain_age(parsed))
        indicators.update(self._check_special_chars(parsed))
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(indicators)
        
        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(indicators, risk_level)
        
        # Additional details
        details['parsed'] = {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'query': parsed.query,
            'fragment': parsed.fragment
        }
        details['score_breakdown'] = self._get_score_breakdown(indicators)
        
        return PhishingAnalysis(
            url=url,
            risk_score=risk_score,
            risk_level=risk_level,
            indicators=indicators,
            details=details,
            recommendations=recommendations,
            timestamp=datetime.datetime.now().isoformat()
        )
    
    def _check_protocol(self, parsed: urlparse) -> Dict[str, any]:
        """Check if URL uses HTTPS"""
        return {
            'uses_https': parsed.scheme == 'https',
            'protocol': parsed.scheme or 'unknown'
        }
    
    def _check_url_structure(self, parsed: urlparse) -> Dict[str, any]:
        """Check for suspicious URL structure patterns"""
        netloc = parsed.netloc.lower()
        indicators = {}
        
        # Check for multiple subdomains
        subdomain_count = netloc.count('.')
        indicators['many_subdomains'] = subdomain_count > 3
        indicators['subdomain_count'] = subdomain_count
        
        # Check for @ symbol (classic phishing)
        indicators['has_at_symbol'] = '@' in netloc
        
        # Check for hyphens in domain
        domain_parts = netloc.split('.')
        if len(domain_parts) > 1:
            main_domain = domain_parts[-2] if len(domain_parts) >= 2 else ''
            indicators['has_hyphens'] = '-' in main_domain
        
        # Check for numeric domain
        indicators['numeric_domain'] = bool(re.search(r'^\d+$', netloc.replace('.', '')))
        
        return indicators
    
    def _check_keywords(self, parsed: urlparse) -> Dict[str, any]:
        """Check for suspicious keywords in URL"""
        url_lower = (parsed.netloc + parsed.path + parsed.query).lower()
        
        suspicious = any(kw in url_lower for kw in self.suspicious_keywords)
        urgent = any(kw in url_lower for kw in self.urgent_keywords)
        
        # Count keyword matches
        suspicious_count = sum(1 for kw in self.suspicious_keywords if kw in url_lower)
        
        return {
            'has_suspicious_keywords': suspicious,
            'has_urgent_keywords': urgent,
            'suspicious_keyword_count': min(suspicious_count, 10)
        }
    
    def _check_brand_impersonation(self, parsed: urlparse) -> Dict[str, any]:
        """Check for brand name impersonation"""
        netloc = parsed.netloc.lower()
        path = parsed.path.lower()
        url_lower = netloc + path
        
        # Check if any brand name appears in URL
        brand_present = False
        brand_detected = None
        
        for brand in self.brands:
            if brand in url_lower:
                brand_present = True
                brand_detected = brand
                break
        
        # Check if domain is actually the brand's domain
        brand_domains = {
            'paypal': 'paypal.com',
            'amazon': 'amazon.com',
            'apple': 'apple.com',
            'microsoft': 'microsoft.com',
            'google': 'google.com',
            'facebook': 'facebook.com',
            'instagram': 'instagram.com',
            'linkedin': 'linkedin.com',
            'twitter': 'twitter.com',
            'dropbox': 'dropbox.com',
            'spotify': 'spotify.com',
            'netflix': 'netflix.com'
        }
        
        brand_mismatch = False
        matched_brand = None
        
        for brand, domain in brand_domains.items():
            if brand in url_lower and domain not in netloc:
                brand_mismatch = True
                matched_brand = brand
                break
        
        return {
            'brand_impersonation': brand_mismatch,
            'brand_detected': brand_present,
            'brand_name': matched_brand
        }
    
    def _check_tld(self, parsed: urlparse) -> Dict[str, any]:
        """Check if TLD is suspicious"""
        netloc = parsed.netloc
        tld = '.' + netloc.split('.')[-1] if '.' in netloc else ''
        
        return {
            'suspicious_tld': tld in self.suspicious_tlds,
            'tld': tld
        }
    
    def _check_url_length(self, parsed: urlparse) -> Dict[str, any]:
        """Check if URL is suspiciously long"""
        url_length = len(parsed.netloc + parsed.path + parsed.query)
        
        return {
            'excessive_length': url_length > 100,
            'url_length': url_length
        }
    
    def _check_ip_address(self, parsed: urlparse) -> Dict[str, any]:
        """Check if domain is an IP address"""
        netloc = parsed.netloc.split(':')[0]
        
        # Check for IP address pattern
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        is_ip = bool(ip_pattern.match(netloc))
        
        return {
            'uses_ip_address': is_ip
        }
    
    def _check_redirects(self, parsed: urlparse) -> Dict[str, any]:
        """Check for suspicious redirect patterns"""
        query_params = parse_qs(parsed.query)
        
        # Common redirect parameters
        redirect_params = ['redirect', 'url', 'link', 'goto', 'return']
        has_redirect = any(param in query_params for param in redirect_params)
        
        return {
            'has_redirect_param': has_redirect
        }
    
    def _check_domain_age(self, parsed: urlparse) -> Dict[str, any]:
        """Check domain age as a phishing indicator"""
        domain = parsed.netloc.split(':')[0]
        try:
            w = whois.whois(domain)
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    creation_date = w.creation_date[0]
                else:
                    creation_date = w.creation_date
                
                age_days = (datetime.datetime.now() - creation_date).days
                return {
                    'domain_age_suspicious': age_days < 30,
                    'domain_age_days': age_days
                }
        except:
            pass
        
        return {'domain_age_suspicious': True, 'domain_age_days': 'Unknown'}
    
    def _check_special_chars(self, parsed: urlparse) -> Dict[str, any]:
        """Check for special characters that might indicate phishing"""
        url = parsed.netloc + parsed.path
        
        # Check for percent encoding
        has_percent_encoding = '%' in url
        
        # Check for Unicode/IDN homograph attacks
        has_unicode = any(ord(c) > 127 for c in url)
        
        return {
            'has_percent_encoding': has_percent_encoding,
            'has_unicode': has_unicode
        }
    
    def _calculate_risk_score(self, indicators: Dict[str, any]) -> int:
        """Calculate risk score based on indicators"""
        weights = {
            'uses_https': -10,
            'domain_age_suspicious': 15,
            'many_subdomains': 10,
            'has_at_symbol': 25,
            'has_hyphens': 10,
            'has_suspicious_keywords': 15,
            'has_urgent_keywords': 15,
            'brand_impersonation': 30,
            'suspicious_tld': 20,
            'excessive_length': 10,
            'uses_ip_address': 20,
            'has_redirect_param': 15,
            'has_percent_encoding': 10,
            'has_unicode': 15
        }
        
        risk_score = 0
        for indicator, weight in weights.items():
            if indicator in indicators and indicators[indicator]:
                risk_score += weight
            elif indicator == 'uses_https' and indicators.get(indicator) == False:
                risk_score += 30  # No HTTPS is a big red flag
        
        # Ensure score is within 0-100
        risk_score = max(0, min(100, risk_score))
        
        return risk_score
    
    def _determine_risk_level(self, risk_score: int) -> str:
        """Determine risk level from score"""
        if risk_score >= 80:
            return 'CRITICAL'
        elif risk_score >= 60:
            return 'HIGH'
        elif risk_score >= 30:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _get_score_breakdown(self, indicators: Dict[str, any]) -> Dict[str, int]:
        """Get breakdown of score by category"""
        breakdown = {
            'HTTPS': 30 if not indicators.get('uses_https', True) else 0,
            'Keywords': 15 if indicators.get('has_suspicious_keywords', False) else 0,
            'Brand Impersonation': 30 if indicators.get('brand_impersonation', False) else 0,
            'URL Structure': 10 if indicators.get('has_at_symbol', False) else 0,
            'Domain': 20 if indicators.get('suspicious_tld', False) else 0,
            'Other': 0
        }
        
        # Add other indicators
        if indicators.get('uses_ip_address', False):
            breakdown['Other'] += 20
        if indicators.get('many_subdomains', False):
            breakdown['Other'] += 10
        if indicators.get('has_redirect_param', False):
            breakdown['Other'] += 15
        
        return breakdown
    
    def _generate_recommendations(self, indicators: Dict[str, any], risk_level: str) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if risk_level in ['CRITICAL', 'HIGH']:
            recommendations.append("🚨 DO NOT click on this URL - it appears to be a phishing attempt")
            recommendations.append("📧 Report this URL to your security team immediately")
            recommendations.append("🔒 If you already clicked, change your passwords and run security scans")
        
        if indicators.get('brand_impersonation', False):
            recommendations.append("⚠️ This URL appears to impersonate a legitimate brand")
            recommendations.append("✅ Always verify the official domain before entering credentials")
        
        if not indicators.get('uses_https', False):
            recommendations.append("🔓 This URL does not use HTTPS - never enter sensitive information")
        
        if indicators.get('has_at_symbol', False):
            recommendations.append("📌 URLs with @ are a classic phishing technique")
        
        if indicators.get('suspicious_tld', False):
            recommendations.append("🌐 Be cautious with uncommon top-level domains")
        
        if indicators.get('domain_age_suspicious', False):
            recommendations.append("🕒 This domain was recently created - a common phishing tactic")
        
        if indicators.get('has_unicode', False):
            recommendations.append("🔤 This URL contains Unicode characters - possible homograph attack")
        
        if not recommendations:
            recommendations.append("✅ This URL appears relatively safe, but always verify before clicking")
        
        return recommendations

def main():
    """Main entry point for phishing detector"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     SQR CyberSecurity - Phishing URL Detector           ║
    ║             Professional Implementation                  ║
    ║                 (Educational Use Only)                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Test URLs
    test_urls = [
        "https://github.com",
        "https://paypal-login.evil.com/verify",
        "http://login-bank-verification.top",
        "https://amazon.secure-login.net/update",
        "https://193.23.45.6/login",
        "https://www.google.com",
        "http://secure-update-account.info/verify"
    ]
    
    print("🧪 Testing Phishing Detection on Sample URLs\n")
    print("="*70)
    
    detector = PhishingDetector()
    
    for url in test_urls:
        analysis = detector.analyze_url(url)
        
        # Color based on risk level
        color = "\033[92m" if analysis.risk_level == "LOW" else \
                "\033[93m" if analysis.risk_level == "MEDIUM" else \
                "\033[91m" if analysis.risk_level == "HIGH" else \
                "\033[95m"  # CRITICAL - Purple
        
        reset = "\033[0m"
        
        print(f"URL: {url}")
        print(f"Risk Level: {color}{analysis.risk_level}{reset} (Score: {analysis.risk_score}/100)")
        
        # Show key indicators
        indicators = analysis.indicators
        issues = []
        if not indicators.get('uses_https', True):
            issues.append("No HTTPS")
        if indicators.get('brand_impersonation', False):
            issues.append(f"Impersonates {indicators.get('brand_name', 'brand')}")
        if indicators.get('suspicious_tld', False):
            issues.append(f"Suspicious TLD: {indicators.get('tld', '')}")
        if indicators.get('has_at_symbol', False):
            issues.append("Contains @ symbol")
        if indicators.get('domain_age_suspicious', False):
            issues.append("New domain (under 30 days)")
        
        if issues:
            print(f"⚠️ Issues: {', '.join(issues)}")
        
        print("-"*70)
    
    # Interactive mode
    print("\n🔍 Interactive URL Analysis")
    print("-"*70)
    while True:
        url = input("\nEnter URL to analyze (or 'quit' to exit): ").strip()
        if url.lower() == 'quit':
            break
        if not url:
            continue
        
        analysis = detector.analyze_url(url)
        
        print(f"\n📊 Analysis Results:")
        print(f"   Risk Score: {analysis.risk_score}/100")
        print(f"   Risk Level: {analysis.risk_level}")
        print(f"   Timestamp: {analysis.timestamp}")
        
        # Show detailed breakdown
        print(f"\n📋 Detailed Breakdown:")
        breakdown = analysis.details.get('score_breakdown', {})
        for category, score in breakdown.items():
            if score > 0:
                print(f"   {category}: +{score}")
        
        # Show recommendations
        if analysis.recommendations:
            print(f"\n💡 Recommendations:")
            for rec in analysis.recommendations:
                print(f"   {rec}")
        
        print("-"*70)

if __name__ == "__main__":
    main()
