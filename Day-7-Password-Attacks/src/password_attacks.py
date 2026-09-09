#!/usr/bin/env python3
"""
Password Attack Simulator
SQR CyberSecurity Internship - Day 7

Features:
- Brute force simulation
- Rate limit detection
- Password strength checking
- Credential stuffing simulation
- Security recommendations
"""

import time
import random
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PasswordAttackSimulator:
    """Professional password attack simulator"""
    
    def __init__(self):
        # Common weak passwords
        self.common_passwords = [
            '123456', 'password', '123456789', '12345678', '12345',
            '1234567', 'qwerty', 'abc123', 'password1', '111111',
            '123123', 'admin', 'letmein', 'welcome', 'monkey',
            'dragon', 'master', 'hello', 'freedom', 'whatever',
            'qwerty123', '123qwe', '1q2w3e4r', 'password123'
        ]
        
        # Common usernames
        self.common_usernames = [
            'admin', 'user', 'test', 'root', 'administrator',
            'guest', 'support', 'info', 'webmaster', 'security'
        ]
        
        # Password strength patterns
        self.strength_patterns = {
            'weak': {
                'regex': r'^.{1,6}$|^[a-z]+$|^[A-Z]+$|^[0-9]+$',
                'description': 'Too short or only one character type',
                'score': 1
            },
            'medium': {
                'regex': r'^.{7,10}$|^[a-zA-Z]+$|^[a-zA-Z0-9]+$',
                'description': 'Moderate length but limited variety',
                'score': 3
            },
            'strong': {
                'regex': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$',
                'description': 'Good length with mixed case and numbers',
                'score': 5
            },
            'very_strong': {
                'regex': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{12,}$',
                'description': 'Long with special characters and mixed case',
                'score': 8
            }
        }
        
        # Rate limit tracking
        self.attempts = {}
        self.locked_accounts = {}
    
    def simulate_brute_force(self, username: str, password: str, 
                             attempts: int = 5) -> Dict[str, Any]:
        """
        Simulate brute force attack on a login
        """
        result = {
            'username': username,
            'target_password': password,
            'attempts': 0,
            'found': False,
            'time_taken': 0,
            'attempts_made': [],
            'rate_limited': False,
            'locked': False
        }
        
        start_time = time.time()
        
        # Check if account is locked
        if self._is_account_locked(username):
            result['locked'] = True
            result['time_taken'] = time.time() - start_time
            return result
        
        # Simulate brute force attempts
        for i in range(min(attempts, len(self.common_passwords))):
            attempt_password = self.common_passwords[i]
            result['attempts_made'].append(attempt_password)
            result['attempts'] = i + 1
            
            # Check rate limit
            if self._check_rate_limit(username):
                result['rate_limited'] = True
                break
            
            # Simulate delay between attempts
            time.sleep(random.uniform(0.1, 0.3))
            
            # Check if password matches
            if attempt_password == password:
                result['found'] = True
                break
        
        result['time_taken'] = round(time.time() - start_time, 2)
        
        # If too many attempts, lock account
        if result['attempts'] >= 5 and not result['found']:
            self._lock_account(username)
            result['locked'] = True
        
        return result
    
    def simulate_credential_stuffing(self, username: str, password: str) -> Dict[str, Any]:
        """
        Simulate credential stuffing attack
        """
        result = {
            'username': username,
            'target_password': password,
            'leaked_credentials': [],
            'found': False,
            'time_taken': 0
        }
        
        start_time = time.time()
        
        # Check against common leaked passwords
        for leaked_pw in self.common_passwords[:20]:
            result['leaked_credentials'].append(leaked_pw)
            if leaked_pw == password:
                result['found'] = True
                break
        
        result['time_taken'] = round(time.time() - start_time, 2)
        
        return result
    
    def check_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Check password strength and provide recommendations
        """
        result = {
            'password': password,
            'length': len(password),
            'strength': 'weak',
            'score': 0,
            'issues': [],
            'recommendations': []
        }
        
        # Check length
        if len(password) < 8:
            result['issues'].append('Password is too short (less than 8 characters)')
        
        # Check character types
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[@$!%*?&#]', password))
        
        if not has_lower:
            result['issues'].append('Missing lowercase letters')
        if not has_upper:
            result['issues'].append('Missing uppercase letters')
        if not has_digit:
            result['issues'].append('Missing numbers')
        if not has_special:
            result['issues'].append('Missing special characters')
        
        # Calculate score
        score = 0
        if len(password) >= 8:
            score += 2
        if len(password) >= 12:
            score += 2
        if has_lower:
            score += 1
        if has_upper:
            score += 1
        if has_digit:
            score += 1
        if has_special:
            score += 2
        
        # Determine strength
        if score >= 8:
            result['strength'] = 'very_strong'
            result['recommendations'].append('Excellent password! Keep it secure.')
        elif score >= 6:
            result['strength'] = 'strong'
            result['recommendations'].append('Good password. Consider adding special characters.')
        elif score >= 4:
            result['strength'] = 'medium'
            result['recommendations'].append('Password could be stronger. Add special characters and increase length.')
        else:
            result['strength'] = 'weak'
            result['recommendations'].append('Weak password. Use at least 12 characters with mixed case, numbers, and special characters.')
        
        # Check against common passwords
        if password.lower() in self.common_passwords:
            result['issues'].append('Password is commonly used and easily guessable')
            result['recommendations'].append('Avoid common passwords. Use a unique passphrase.')
        
        result['score'] = score
        result['score_percentage'] = min(round((score / 10) * 100), 100)
        
        return result
    
    def _check_rate_limit(self, username: str) -> bool:
        """Check if rate limit is exceeded"""
        current_time = time.time()
        
        if username not in self.attempts:
            self.attempts[username] = []
        
        # Clean old attempts (older than 60 seconds)
        self.attempts[username] = [t for t in self.attempts[username] 
                                   if current_time - t < 60]
        
        # Check if more than 5 attempts in 60 seconds
        if len(self.attempts[username]) >= 5:
            return True
        
        self.attempts[username].append(current_time)
        return False
    
    def _lock_account(self, username: str):
        """Lock an account"""
        self.locked_accounts[username] = time.time() + 300  # Lock for 5 minutes
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked"""
        if username in self.locked_accounts:
            if time.time() < self.locked_accounts[username]:
                return True
            else:
                del self.locked_accounts[username]
        return False
    
    def generate_report(self, username: str, password: str) -> Dict[str, Any]:
        """
        Generate a complete password security report
        """
        strength_result = self.check_password_strength(password)
        brute_result = self.simulate_brute_force(username, password)
        stuffing_result = self.simulate_credential_stuffing(username, password)
        
        return {
            'username': username,
            'password_analysis': strength_result,
            'brute_force_simulation': brute_result,
            'credential_stuffing_simulation': stuffing_result,
            'security_recommendations': self._get_security_recommendations(strength_result),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_security_recommendations(self, strength_result: Dict) -> List[str]:
        """Get security recommendations"""
        recommendations = [
            '✅ Use passwords with at least 12 characters',
            '✅ Include uppercase, lowercase, numbers, and special characters',
            '✅ Avoid using common words or personal information',
            '✅ Use a password manager to generate and store strong passwords',
            '✅ Enable two-factor authentication (2FA)',
            '✅ Never reuse passwords across multiple accounts',
            '✅ Change passwords immediately if compromised'
        ]
        
        # Add specific recommendations based on strength
        if strength_result['strength'] == 'weak':
            recommendations.insert(0, '⚠️ Your password is weak. Change it immediately!')
        elif strength_result['strength'] == 'medium':
            recommendations.insert(0, '⚠️ Your password is moderate. Consider strengthening it.')
        
        return recommendations


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     SQR CyberSecurity - Password Attack Simulator       ║
    ║             Professional Implementation                  ║
    ║                 (Educational Use Only)                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    simulator = PasswordAttackSimulator()
    
    # Test with sample credentials
    test_creds = [
        ('admin', 'password123'),
        ('user', 'admin'),
        ('test', '123456')
    ]
    
    print("🔐 Password Security Report\n")
    
    for username, password in test_creds:
        print(f"\n=== Testing: {username} / {password} ===")
        
        report = simulator.generate_report(username, password)
        
        strength = report['password_analysis']
        print(f"Password Strength: {strength['strength'].upper()} ({strength['score']}/10)")
        print(f"Password Length: {strength['length']}")
        
        if strength['issues']:
            print("Issues:")
            for issue in strength['issues']:
                print(f"  • {issue}")
        
        brute = report['brute_force_simulation']
        print(f"Brute Force: {brute['attempts']} attempts, Found: {brute['found']}")
        
        if brute['rate_limited']:
            print("  ⚠️ Rate limit triggered!")
        if brute['locked']:
            print("  🔒 Account locked!")
        
        print(f"Time taken: {brute['time_taken']} seconds")
        print("-"*50)

if __name__ == "__main__":
    main()
