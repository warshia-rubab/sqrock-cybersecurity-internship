#!/usr/bin/env python3
"""
Advanced Vishing & Smishing Script Generator
SQR CyberSecurity Internship - Day 4

Features:
- Generate vishing scripts (IT, Bank, Government)
- Generate smishing messages
- Psychological trigger analysis
- Professional report generation
"""

import json
import logging
import random
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VishingGenerator:
    """Professional vishing and smishing script generator"""
    
    def __init__(self):
        self.script_templates = {
            'it_support': {
                'name': 'IT Support',
                'opener': [
                    'Hi, this is {name} from IT Support at {company}.',
                    'Hello, I\'m {name} from the IT Security team at {company}.',
                    'Good {time}, this is {name} from IT Support.'
                ],
                'hook': [
                    'We detected unusual activity on your account.',
                    'There was a suspicious login attempt from {location}.',
                    'Your account has been flagged for unusual activity.',
                    'We need to verify your identity for security purposes.'
                ],
                'red_flags': [
                    'Legitimate IT will NEVER ask for passwords.',
                    'Always verify via official internal channels.',
                    'Hang up and call IT directly using official number.'
                ]
            },
            'bank': {
                'name': 'Bank Fraud Department',
                'opener': [
                    'This is {name} from {company} Fraud Department.',
                    'Hello, I\'m {name} calling from {company} Security.',
                    'Good {time}, this is {name} from {company} Anti-Fraud.'
                ],
                'hook': [
                    'We detected suspicious transactions on your account.',
                    'Your card has been flagged for unusual activity.',
                    'We need to verify recent transactions on your account.',
                    'There\'s been unusual activity on your account.'
                ],
                'red_flags': [
                    'Banks NEVER ask for PIN or full card numbers.',
                    'Verify by calling the number on your card.',
                    'Never share OTP or security codes.'
                ]
            },
            'government': {
                'name': 'Government Agency',
                'opener': [
                    'This is {name} from {company} Government Services.',
                    'Hello, I\'m {name} from {company} Administration.',
                    'Good {time}, this is {name} from {company} Office.'
                ],
                'hook': [
                    'Your ID needs immediate verification.',
                    'There\'s an issue with your official records.',
                    'Your documents require immediate attention.',
                    'We need to verify your identity for official purposes.'
                ],
                'red_flags': [
                    'Government NEVER asks for passwords or PINs.',
                    'Verify by visiting official government website.',
                    'Report suspicious calls to the official helpline.'
                ]
            }
        }
        
        self.psychological_triggers = [
            'Authority - Impersonates trusted authority figure',
            'Scarcity - Limited time to respond',
            'Fear - Threat of negative consequences',
            'Liking - Friendly, helpful tone',
            'Urgency - Immediate action required',
            'Trust - Exploits trust in institutions'
        ]
        
        self.names = ['Alex', 'Sarah', 'Michael', 'Jessica', 'David', 'Emma', 'Robert', 'Lisa']
        self.companies = {
            'it_support': ['SQR CyberSecurity', 'IT Solutions', 'Tech Support'],
            'bank': ['National Bank', 'City Bank', 'Global Finance'],
            'government': ['Federal Services', 'National Agency', 'Government Office']
        }
        
    def generate_vishing_script(self, category: str, target_name: str = None) -> Dict[str, Any]:
        """Generate a vishing script for awareness training"""
        
        if category not in self.script_templates:
            return {'error': f'Unknown category: {category}'}
        
        template = self.script_templates[category]
        name = random.choice(self.names)
        company = random.choice(self.companies.get(category, ['Organization']))
        time = random.choice(['morning', 'afternoon', 'evening'])
        
        opener = random.choice(template['opener']).format(
            name=name, company=company, time=time
        )
        hook = random.choice(template['hook']).format(
            location=random.choice(['USA', 'UK', 'Canada', 'Germany'])
        )
        
        script = {
            'category': category,
            'caller_name': name,
            'company': company,
            'target': target_name or 'Employee',
            'opener': opener,
            'hook': hook,
            'script': self._build_script(opener, hook, template['red_flags']),
            'red_flags': template['red_flags'],
            'psychological_triggers': self._analyze_triggers(category),
            'timestamp': datetime.now().isoformat()
        }
        
        return script
    
    def _build_script(self, opener: str, hook: str, red_flags: List[str]) -> str:
        """Build the full script"""
        script = f"""
=== VISHING AWARENESS SCRIPT ===

[OPENING]
{opener}

[HOOK]
{hook}
"I need to verify your identity - can you confirm your employee ID and password?"

[RED FLAGS FOR AWARENESS]
• {red_flags[0] if red_flags else ''}
• {red_flags[1] if len(red_flags) > 1 else ''}
• {red_flags[2] if len(red_flags) > 2 else ''}

[PROPER RESPONSE]
• Do NOT provide any personal information
• Hang up immediately
• Call the official number
• Report the incident to security
"""
        return script
    
    def _analyze_triggers(self, category: str) -> List[str]:
        """Analyze psychological triggers used in the script"""
        triggers = {
            'it_support': ['Authority', 'Fear', 'Urgency'],
            'bank': ['Authority', 'Fear', 'Scarcity'],
            'government': ['Authority', 'Fear', 'Trust']
        }
        return triggers.get(category, ['Authority', 'Fear'])
    
    def generate_smishing_message(self, category: str) -> Dict[str, Any]:
        """Generate a smishing message"""
        
        smishing_templates = {
            'it_support': {
                'message': "🔐 Your account has been flagged for suspicious activity. Click here to verify: https://bit.ly/verify-{code}",
                'description': 'IT Security Alert - Account Verification Required'
            },
            'bank': {
                'message': "🏦 ALERT: Your card has been blocked due to unusual activity. Call {number} or click {link} to unblock.",
                'description': 'Bank Fraud Alert - Card Blocked'
            },
            'government': {
                'message': "📋 Official Notice: Your ID needs verification. Visit {link} within 24 hours to avoid penalties.",
                'description': 'Government ID Verification Required'
            }
        }
        
        template = smishing_templates.get(category, smishing_templates['it_support'])
        code = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
        
        return {
            'category': category,
            'message': template['message'].format(
                code=code,
                number=random.randint(1000000000, 9999999999),
                link=f'https://bit.ly/{code}'
            ),
            'description': template['description'],
            'psychological_triggers': self._analyze_triggers(category),
            'red_flags': [
                'Unsolicited messages with links',
                'Urgent action required',
                'Requests for personal information'
            ],
            'timestamp': datetime.now().isoformat()
        }

def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║             Vishing & Smishing Generator    ║
    ║             Professional Implementation                  ║
    ║                 (Educational Use Only)                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    generator = VishingGenerator()
    
    print("📋 Generating Vishing Scripts for Awareness Training\n")
    
    categories = ['it_support', 'bank', 'government']
    
    for category in categories:
        print(f"=== {category.upper().replace('_', ' ')} SCRIPT ===")
        script = generator.generate_vishing_script(category)
        print(f"Caller: {script['caller_name']} from {script['company']}")
        print(f"Script:\n{script['script']}")
        print(f"Psychological Triggers: {', '.join(script['psychological_triggers'])}")
        print("-"*70)

if __name__ == "__main__":
    main()
