#!/usr/bin/env python3
"""
Spear Phishing Template Engine
SQR CyberSecurity Internship - Day 6

Features:
- Personalized email template generation
- OSINT data integration
- Multiple template types
- Awareness training content
- Professional report generation
"""

import json
import logging
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SpearPhishingTemplate:
    """Professional spear phishing template engine"""
    
    def __init__(self):
        # Sample target data
        self.sample_targets = [
            {
                'name': 'Riya Sharma',
                'email': 'riya.sharma@company.com',
                'company': 'SQR CyberSecurity',
                'position': 'Security Engineer',
                'location': 'Bangalore, India',
                'department': 'IT Security'
            },
            {
                'name': 'Arjun Patel',
                'email': 'arjun.patel@company.com',
                'company': 'TechVault Solutions',
                'position': 'System Administrator',
                'location': 'Mumbai, India',
                'department': 'IT Operations'
            },
            {
                'name': 'Priya Singh',
                'email': 'priya.singh@company.com',
                'company': 'DataShield Inc',
                'position': 'Network Analyst',
                'location': 'Delhi, India',
                'department': 'Network Security'
            }
        ]
        
        # Template types
        self.template_types = {
            'account_verification': {
                'name': 'Account Verification',
                'description': 'Email asking to verify account credentials',
                'urgency': 'HIGH',
                'example': 'Your account needs immediate verification.'
            },
            'password_reset': {
                'name': 'Password Reset',
                'description': 'Email requesting password reset',
                'urgency': 'MEDIUM',
                'example': 'Your password requires reset due to suspicious activity.'
            },
            'security_alert': {
                'name': 'Security Alert',
                'description': 'Email about security incident',
                'urgency': 'HIGH',
                'example': 'Suspicious login detected from unusual location.'
            },
            'document_sharing': {
                'name': 'Document Sharing',
                'description': 'Email about shared documents',
                'urgency': 'LOW',
                'example': 'Important document shared for your review.'
            },
            'invoice_alert': {
                'name': 'Invoice Alert',
                'description': 'Email about invoice or payment',
                'urgency': 'MEDIUM',
                'example': 'Payment invoice requires your attention.'
            }
        }
        
        # Red flag templates
        self.red_flags = {
            'sender': [
                'Spoofed sender address (look for subtle misspellings)',
                'Display name doesn\'t match email address',
                'Free email services for official communications'
            ],
            'content': [
                'Urgent language demanding immediate action',
                'Requests for sensitive information',
                'Suspicious links (check URL carefully)',
                'Unexpected attachments'
            ],
            'context': [
                'Unexpected email from internal department',
                'Out of character request',
                'Contradicts existing company policies'
            ]
        }
    
    def generate_template(self, target: Dict[str, str], template_type: str) -> Dict[str, Any]:
        """
        Generate a spear phishing template
        """
        logger.info(f"Generating {template_type} template for {target.get('name')}")
        
        if template_type not in self.template_types:
            return {'error': f'Unknown template type: {template_type}'}
        
        template_info = self.template_types[template_type]
        
        email = {
            'target': target,
            'template_type': template_type,
            'subject': self._generate_subject(target, template_type),
            'body': self._generate_body(target, template_type),
            'sender': self._generate_sender(target),
            'urgency': template_info['urgency'],
            'red_flags': self._get_red_flags(template_type),
            'defense_tips': self._get_defense_tips(),
            'timestamp': datetime.now().isoformat(),
            'is_training': True
        }
        
        return email
    
    def _generate_subject(self, target: Dict[str, str], template_type: str) -> str:
        """Generate email subject line"""
        subjects = {
            'account_verification': [
                f'Action Required: Verify Your {target["company"]} Account',
                f'Your {target["company"]} Account Needs Verification',
                'URGENT: Account Security Verification Required'
            ],
            'password_reset': [
                f'{target["company"]} Password Reset Request',
                'Your Password Will Expire - Reset Now',
                'Password Reset Confirmation Required'
            ],
            'security_alert': [
                f'Security Alert: {target["company"]} - Suspicious Activity',
                'Your Account Has Been Locked - Unlock Now',
                'ALERT: Unauthorized Access Detected'
            ],
            'document_sharing': [
                f'Important Document Shared with You',
                'Secure Document for Your Review',
                'Shared File: Request for Approval'
            ],
            'invoice_alert': [
                f'Invoice #{random.randint(10000, 99999)} - Payment Required',
                'Your Invoice is Ready for Review',
                'Payment Confirmation Required'
            ]
        }
        
        selected = subjects.get(template_type, subjects['security_alert'])
        return random.choice(selected)
    
    def _generate_body(self, target: Dict[str, str], template_type: str) -> str:
        """Generate email body"""
        bodies = {
            'account_verification': f"""
Dear {target['name']},

We have detected unusual activity on your {target['company']} account. 
As part of our security protocols, we require you to verify your identity
within 24 hours.

Please verify your account by clicking the link below:
[Verify Account Link]

This is a mandatory security measure to protect your account.

Regards,
Security Team
{target['company']} IT Department
""",
            'password_reset': f"""
Dear {target['name']},

This is a notification that your password for {target['company']} 
will expire in 24 hours. To continue using your account without 
interruption, please reset your password immediately.

[Reset Password Link]

If you don't reset your password within 24 hours, your account 
will be locked. Please contact IT support if you need assistance.

Regards,
IT Administration
{target['company']}
""",
            'security_alert': f"""
URGENT SECURITY NOTIFICATION

Dear {target['name']},

A login attempt was detected from {target['location']} using credentials
that do not match our records. This could indicate unauthorized access
to your account.

Please review your recent account activity immediately:
[View Activity Link]

If you did not authorize this activity, please contact the security 
team immediately.

- Security Operations Team
{target['company']}
""",
            'document_sharing': f"""
Dear {target['name']},

A secure document has been shared with you via our internal file sharing
system. This document contains important information regarding ongoing
project initiatives.

[View Document Link]

Your feedback is requested by end of business day.

Best regards,
Document Management Team
{target['company']}
""",
            'invoice_alert': f"""
Dear {target['name']},

Invoice #{random.randint(10000, 99999)} for {target['company']} has 
been generated and requires your attention.

Please review the invoice details:
[View Invoice Link]

Payment is due within 15 days. Please verify the invoice details and
approve for processing.

Regards,
Finance Department
{target['company']}
"""
        }
        
        body = bodies.get(template_type, bodies['security_alert'])
        return body
    
    def _generate_sender(self, target: Dict[str, str]) -> Dict[str, str]:
        """Generate sender information"""
        domains = [
            f'security-{target["company"].lower().replace(" ", "")}.com',
            f'notifications@{target["company"].lower().replace(" ", "")}.com',
            f'admin-{target["company"].lower().replace(" ", "")}.net',
            f'it-{target["company"].lower().replace(" ", "")}.org'
        ]
        
        return {
            'name': random.choice(['Security Team', 'IT Department', 'System Administrator', 'Help Desk']),
            'email': f'no-reply@{random.choice(domains)}'
        }
    
    def _get_red_flags(self, template_type: str) -> List[str]:
        """Get red flags for the template"""
        flags = []
        
        # Add generic red flags
        flags.extend(self.red_flags['sender'][:2])
        flags.extend(self.red_flags['content'])
        
        # Add specific red flags based on template type
        if template_type == 'account_verification':
            flags.append('Requests for credentials outside normal process')
        elif template_type == 'password_reset':
            flags.append('Password reset from unexpected source')
        elif template_type == 'security_alert':
            flags.append('Security alerts should be verified through official channels')
        elif template_type == 'document_sharing':
            flags.append('Unexpected document sharing requests')
        elif template_type == 'invoice_alert':
            flags.append('Invoice requests outside normal process')
        
        return flags[:5]  # Return top 5 flags
    
    def _get_defense_tips(self) -> List[str]:
        """Get defense tips"""
        return [
            '✅ Always verify sender address carefully',
            '✅ Hover over links before clicking',
            '✅ Never share passwords via email',
            '✅ Check with IT/Security directly',
            '✅ Use official internal communication channels',
            '✅ Verify any urgent requests by phone',
            '✅ Report suspicious emails immediately'
        ]
    
    def get_all_templates(self, target: Dict[str, str]) -> List[Dict[str, Any]]:
        """Generate all template types for a target"""
        templates = []
        
        for template_type in self.template_types:
            templates.append(self.generate_template(target, template_type))
        
        return templates


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║            Spear Phishing Template Engine  ║
    ║             Professional Implementation                  ║
    ║                 (Educational Use Only)                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    template_engine = SpearPhishingTemplate()
    
    # Show sample targets
    print("📋 Available Targets:")
    for i, target in enumerate(template_engine.sample_targets):
        print(f"  [{i}] {target['name']} - {target['position']} at {target['company']}")
    
    print("\n📌 Template Types:")
    for t in template_engine.template_types:
        print(f"  • {t.replace('_', ' ').title()}")
    
    # Generate all templates for the first target
    print("\n" + "="*70)
    print("📧 Generating Spear Phishing Templates for Riya Sharma")
    print("="*70)
    
    target = template_engine.sample_targets[0]
    templates = template_engine.get_all_templates(target)
    
    for template in templates:
        print(f"\n=== {template['template_type'].replace('_', ' ').upper()} ===")
        print(f"Subject: {template['subject']}")
        print(f"From: {template['sender']['name']} <{template['sender']['email']}>")
        print(f"To: {target['name']} <{target['email']}>")
        print(f"Body:\n{template['body'][:200]}...")
        print(f"Urgency: {template['urgency']}")
        print(f"Red Flags: {', '.join(template['red_flags'][:3])}")
        print("-"*50)

if __name__ == "__main__":
    main()
