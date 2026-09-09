#!/usr/bin/env python3
"""
Fake Profile Detection System
SQR CyberSecurity Internship - Day 9

Features:
- Behavioral heuristics analysis
- Bot signal detection
- Impersonation detection
- Risk scoring (0-100)
- Detailed reporting
"""

import json
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FakeProfileDetector:
    """Professional fake profile detection system"""
    
    def __init__(self):
        # Sample profiles for testing
        self.sample_profiles = [
            # Real profile
            {
                'username': 'john_doe_real',
                'name': 'John Doe',
                'account_age_days': 1200,
                'followers': 4500,
                'following': 320,
                'posts': 870,
                'profile_pic': True,
                'bio': 'Software Engineer | Tech Enthusiast | Coffee Lover',
                'verified': True,
                'email_verified': True,
                'phone_verified': True
            },
            # Bot/Fake profile
            {
                'username': 'user_8374',
                'name': 'Sarah Smith',
                'account_age_days': 7,
                'followers': 2,
                'following': 900,
                'posts': 1,
                'profile_pic': False,
                'bio': 'Default bio',
                'verified': False,
                'email_verified': False,
                'phone_verified': False
            },
            # Suspicious profile
            {
                'username': 'emma_wilson_2024',
                'name': 'Emma Wilson',
                'account_age_days': 45,
                'followers': 15,
                'following': 450,
                'posts': 8,
                'profile_pic': True,
                'bio': 'Marketing specialist',
                'verified': False,
                'email_verified': True,
                'phone_verified': False
            }
        ]
    
    def detect_fake_profile(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect if a profile is fake using behavioral heuristics
        """
        logger.info(f"Analyzing profile: {profile.get('username', 'Unknown')}")
        
        result = {
            'username': profile.get('username', 'Unknown'),
            'name': profile.get('name', 'Unknown'),
            'fake_score': 0,
            'risk_level': 'LOW',
            'heuristics': {},
            'bot_signals': [],
            'issues': [],
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Run all heuristics
        result['heuristics']['account_age'] = self._check_account_age(profile)
        result['heuristics']['follower_ratio'] = self._check_follower_ratio(profile)
        result['heuristics']['profile_pic'] = self._check_profile_pic(profile)
        result['heuristics']['post_count'] = self._check_post_count(profile)
        result['heuristics']['bio_quality'] = self._check_bio_quality(profile)
        result['heuristics']['verification'] = self._check_verification(profile)
        result['heuristics']['username_pattern'] = self._check_username_pattern(profile)
        
        # Calculate fake score
        result['fake_score'] = self._calculate_fake_score(result['heuristics'])
        
        # Determine risk level
        result['risk_level'] = self._determine_risk_level(result['fake_score'])
        
        # Identify bot signals
        result['bot_signals'] = self._identify_bot_signals(result['heuristics'])
        
        # Generate issues
        result['issues'] = self._generate_issues(result['heuristics'])
        
        # Generate recommendations
        result['recommendations'] = self._generate_recommendations(result['issues'])
        
        return result
    
    def _check_account_age(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Check if account is too new"""
        age = profile.get('account_age_days', 0)
        return {
            'age_days': age,
            'suspicious': age < 30,
            'score': 30 if age < 30 else 0
        }
    
    def _check_follower_ratio(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Check follower to following ratio"""
        followers = profile.get('followers', 0)
        following = profile.get('following', 0)
        
        ratio = following / max(followers, 1)
        
        return {
            'followers': followers,
            'following': following,
            'ratio': round(ratio, 2),
            'suspicious': ratio > 10,
            'score': 25 if ratio > 10 else 0
        }
    
    def _check_profile_pic(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Check if profile has a picture"""
        has_pic = profile.get('profile_pic', False)
        return {
            'has_pic': has_pic,
            'suspicious': not has_pic,
            'score': 20 if not has_pic else 0
        }
    
    def _check_post_count(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Check if account has too few posts"""
        posts = profile.get('posts', 0)
        return {
            'post_count': posts,
            'suspicious': posts < 5,
            'score': 15 if posts < 5 else 0
        }
    
    def _check_bio_quality(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Check bio quality"""
        bio = profile.get('bio', '').strip()
        is_default = bio.lower() in ['default bio', 'bio', '', 'default']
        
        return {
            'bio': bio,
            'is_default': is_default,
            'suspicious': is_default,
            'score': 15 if is_default else 0
        }
    
    def _check_verification(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Check verification status"""
        verified = profile.get('verified', False)
        email_verified = profile.get('email_verified', False)
        phone_verified = profile.get('phone_verified', False)
        
        verification_score = 0
        if not verified:
            verification_score += 10
        if not email_verified:
            verification_score += 10
        if not phone_verified:
            verification_score += 10
        
        return {
            'verified': verified,
            'email_verified': email_verified,
            'phone_verified': phone_verified,
            'suspicious': verification_score > 10,
            'score': verification_score
        }
    
    def _check_username_pattern(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Check for suspicious username patterns"""
        username = profile.get('username', '')
        
        # Check for random numbers
        has_numbers = any(c.isdigit() for c in username)
        
        # Check for underscores/random patterns
        has_underscore = '_' in username
        
        # Check if username is just numbers
        is_numeric = username.isdigit()
        
        # Check for common bot patterns
        bot_patterns = ['user_', 'bot_', '_bot', 'spam_', 'fake_']
        has_bot_pattern = any(pattern in username.lower() for pattern in bot_patterns)
        
        suspicious = is_numeric or has_bot_pattern or (has_numbers and has_underscore and len(username) > 10)
        
        return {
            'username': username,
            'has_numbers': has_numbers,
            'has_underscore': has_underscore,
            'is_numeric': is_numeric,
            'has_bot_pattern': has_bot_pattern,
            'suspicious': suspicious,
            'score': 15 if suspicious else 0
        }
    
    def _calculate_fake_score(self, heuristics: Dict[str, Any]) -> int:
        """Calculate fake score from heuristics"""
        total_score = 0
        
        for key, value in heuristics.items():
            if isinstance(value, dict):
                total_score += value.get('score', 0)
        
        return min(total_score, 100)
    
    def _determine_risk_level(self, score: int) -> str:
        """Determine risk level from score"""
        if score >= 70:
            return 'CRITICAL'
        elif score >= 50:
            return 'HIGH'
        elif score >= 25:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _identify_bot_signals(self, heuristics: Dict[str, Any]) -> List[str]:
        """Identify bot signals from heuristics"""
        signals = []
        
        age = heuristics.get('account_age', {})
        if age.get('suspicious', False):
            signals.append('New account (under 30 days)')
        
        ratio = heuristics.get('follower_ratio', {})
        if ratio.get('suspicious', False):
            signals.append(f'Abnormal follower ratio: {ratio.get("ratio", 0)}:1')
        
        pic = heuristics.get('profile_pic', {})
        if not pic.get('has_pic', True):
            signals.append('No profile picture')
        
        posts = heuristics.get('post_count', {})
        if posts.get('suspicious', False):
            signals.append('Very few posts')
        
        bio = heuristics.get('bio_quality', {})
        if bio.get('is_default', False):
            signals.append('Default or empty bio')
        
        verification = heuristics.get('verification', {})
        if not verification.get('verified', False):
            signals.append('Not verified')
        
        username = heuristics.get('username_pattern', {})
        if username.get('suspicious', False):
            signals.append('Suspicious username pattern')
        
        return signals
    
    def _generate_issues(self, heuristics: Dict[str, Any]) -> List[str]:
        """Generate issues from heuristics"""
        issues = []
        
        age = heuristics.get('account_age', {})
        if age.get('suspicious', False):
            issues.append(f'⚠️ Account is only {age.get("age_days", 0)} days old')
        
        ratio = heuristics.get('follower_ratio', {})
        if ratio.get('suspicious', False):
            issues.append(f'⚠️ Following ({ratio.get("following", 0)}) far exceeds followers ({ratio.get("followers", 0)})')
        
        pic = heuristics.get('profile_pic', {})
        if not pic.get('has_pic', True):
            issues.append('⚠️ No profile picture')
        
        bio = heuristics.get('bio_quality', {})
        if bio.get('is_default', False):
            issues.append('⚠️ Default or suspicious bio')
        
        verification = heuristics.get('verification', {})
        if not verification.get('verified', False):
            issues.append('⚠️ Account is not verified')
        
        username = heuristics.get('username_pattern', {})
        if username.get('suspicious', False):
            issues.append('⚠️ Suspicious username pattern')
        
        return issues
    
    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations from issues"""
        recommendations = [
            '✅ Verify the account through official channels',
            '✅ Check for inconsistencies in profile information',
            '✅ Look for suspicious activity patterns',
            '✅ Report suspicious accounts to the platform',
            '✅ Never share personal information with unverified accounts'
        ]
        
        # Add specific recommendations based on issues
        for issue in issues:
            if 'account is only' in issue:
                recommendations.append('⚠️ Be cautious with new accounts')
            if 'No profile picture' in issue:
                recommendations.append('⚠️ Lack of profile picture is a red flag')
            if 'Default or suspicious bio' in issue:
                recommendations.append('⚠️ Generic bios often indicate fake accounts')
        
        return list(set(recommendations))  # Remove duplicates
    
    def detect_impersonation(self, profile1: Dict[str, Any], profile2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect if profile2 is impersonating profile1
        """
        result = {
            'profile1': profile1.get('username', 'Unknown'),
            'profile2': profile2.get('username', 'Unknown'),
            'similarity_score': 0,
            'is_impersonation': False,
            'matching_factors': [],
            'risk_level': 'LOW'
        }
        
        # Compare names
        if profile1.get('name', '').lower() == profile2.get('name', '').lower():
            result['matching_factors'].append('Same name')
            result['similarity_score'] += 20
        
        # Compare bio
        if profile1.get('bio', '').lower() == profile2.get('bio', '').lower():
            result['matching_factors'].append('Same bio')
            result['similarity_score'] += 15
        
        # Compare username similarity
        username1 = profile1.get('username', '').lower()
        username2 = profile2.get('username', '').lower()
        
        # Check if username2 contains username1
        if username1 in username2 or username2 in username1:
            result['matching_factors'].append('Similar username')
            result['similarity_score'] += 25
        
        # Check if profile2 has no profile pic while profile1 does
        if profile1.get('profile_pic', False) and not profile2.get('profile_pic', False):
            result['matching_factors'].append('Missing profile picture (suspicious)')
            result['similarity_score'] += 10
        
        # Check if profile2 is newer
        if profile1.get('account_age_days', 0) > profile2.get('account_age_days', 0):
            result['matching_factors'].append('Newer account (suspicious)')
            result['similarity_score'] += 10
        
        # Determine if impersonation
        result['is_impersonation'] = result['similarity_score'] >= 50
        
        # Determine risk level
        if result['similarity_score'] >= 70:
            result['risk_level'] = 'CRITICAL'
        elif result['similarity_score'] >= 50:
            result['risk_level'] = 'HIGH'
        elif result['similarity_score'] >= 30:
            result['risk_level'] = 'MEDIUM'
        else:
            result['risk_level'] = 'LOW'
        
        return result
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """Get all sample profiles"""
        return self.sample_profiles
    
    def get_profile(self, index: int) -> Dict[str, Any]:
        """Get a specific sample profile"""
        if 0 <= index < len(self.sample_profiles):
            return self.sample_profiles[index]
        return None


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     SQR CyberSecurity - Fake Profile Detection System   ║
    ║             Professional Implementation                  ║
    ║                 (Educational Use Only)                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    detector = FakeProfileDetector()
    
    print("📊 Testing Fake Profile Detection\n")
    print("="*70)
    
    for i, profile in enumerate(detector.sample_profiles):
        print(f"\nProfile {i+1}: {profile.get('username', 'Unknown')}")
        print(f"Name: {profile.get('name', 'Unknown')}")
        print(f"Account Age: {profile.get('account_age_days', 0)} days")
        print(f"Followers: {profile.get('followers', 0)}")
        print(f"Following: {profile.get('following', 0)}")
        print(f"Posts: {profile.get('posts', 0)}")
        
        result = detector.detect_fake_profile(profile)
        
        print(f"\n📊 Fake Score: {result['fake_score']}/100")
        print(f"⚠️ Risk Level: {result['risk_level']}")
        
        if result['bot_signals']:
            print("\n🤖 Bot Signals Detected:")
            for signal in result['bot_signals'][:3]:
                print(f"  • {signal}")
        
        print("-"*70)

if __name__ == "__main__":
    main()
