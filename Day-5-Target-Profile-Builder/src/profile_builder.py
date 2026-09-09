#!/usr/bin/env python3
"""
Target Profile Builder - OSINT + Social Engineering
SQR CyberSecurity Internship - Day 5

Features:
- GitHub profile data aggregation
- LinkedIn-style profile building
- Threat assessment from attacker perspective
- Professional report generation
"""

import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TargetProfileBuilder:
    """Professional target profile builder using OSINT data"""
    
    def __init__(self):
        self.github_api = "https://api.github.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Profile-Builder/1.0)',
            'Accept': 'application/vnd.github.v3+json'
        })
        
    def build_profile(self, username: str) -> Dict[str, Any]:
        """
        Build a comprehensive target profile
        
        Args:
            username: GitHub username to analyze
        """
        logger.info(f"Building profile for: {username}")
        
        profile = {
            'target': username,
            'timestamp': datetime.now().isoformat(),
            'github_data': self._fetch_github_data(username),
            'social_engineering_assessment': {},
            'threat_vectors': [],
            'recommendations': [],
            'attacker_perspective': {}
        }
        
        # Analyze GitHub data
        if profile['github_data']:
            profile['social_engineering_assessment'] = self._analyze_github_data(profile['github_data'])
            profile['threat_vectors'] = self._identify_threat_vectors(profile['github_data'])
            profile['recommendations'] = self._generate_recommendations(profile['threat_vectors'])
            profile['attacker_perspective'] = self._attacker_perspective(profile)
        
        return profile
    
    def _fetch_github_data(self, username: str) -> Dict[str, Any]:
        """Fetch public GitHub data"""
        data = {}
        
        try:
            # Get user profile
            user_response = self.session.get(f"{self.github_api}/users/{username}")
            if user_response.status_code == 200:
                user_data = user_response.json()
                data['user'] = {
                    'name': user_data.get('name'),
                    'company': user_data.get('company'),
                    'location': user_data.get('location'),
                    'bio': user_data.get('bio'),
                    'public_repos': user_data.get('public_repos', 0),
                    'followers': user_data.get('followers', 0),
                    'following': user_data.get('following', 0),
                    'created_at': user_data.get('created_at'),
                    'updated_at': user_data.get('updated_at'),
                    'email': user_data.get('email')
                }
            else:
                data['error'] = f"User not found: {username}"
                return data
            
            # Get repositories
            repos_response = self.session.get(f"{self.github_api}/users/{username}/repos?per_page=50")
            if repos_response.status_code == 200:
                repos = repos_response.json()
                data['repositories'] = []
                data['languages'] = {}
                
                for repo in repos[:10]:  # Limit to 10 repos
                    repo_info = {
                        'name': repo.get('name'),
                        'description': repo.get('description'),
                        'language': repo.get('language'),
                        'stars': repo.get('stargazers_count', 0),
                        'forks': repo.get('forks_count', 0),
                        'private': repo.get('private', False)
                    }
                    data['repositories'].append(repo_info)
                    
                    # Count languages
                    lang = repo.get('language')
                    if lang:
                        data['languages'][lang] = data['languages'].get(lang, 0) + 1
            
            # Get followers (first 10)
            followers_response = self.session.get(f"{self.github_api}/users/{username}/followers?per_page=10")
            if followers_response.status_code == 200:
                followers = followers_response.json()
                data['followers_sample'] = [f.get('login') for f in followers]
            
            # Get following (first 10)
            following_response = self.session.get(f"{self.github_api}/users/{username}/following?per_page=10")
            if following_response.status_code == 200:
                following = following_response.json()
                data['following_sample'] = [f.get('login') for f in following]
                
        except Exception as e:
            logger.error(f"Error fetching GitHub data: {e}")
            data['error'] = str(e)
        
        return data
    
    def _analyze_github_data(self, github_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze GitHub data for social engineering assessment"""
        assessment = {
            'exposure_level': 'UNKNOWN',
            'personal_info_exposed': [],
            'technical_stack': [],
            'collaborators': [],
            'risk_score': 0,
            'findings': []
        }
        
        user = github_data.get('user', {})
        
        # Check personal info exposure
        if user.get('name'):
            assessment['personal_info_exposed'].append('Full Name')
        if user.get('location'):
            assessment['personal_info_exposed'].append('Location')
        if user.get('company'):
            assessment['personal_info_exposed'].append('Company/Organization')
        if user.get('email'):
            assessment['personal_info_exposed'].append('Email Address')
        if user.get('bio'):
            assessment['personal_info_exposed'].append('Bio/About Me')
        
        # Technical stack
        languages = github_data.get('languages', {})
        top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        assessment['technical_stack'] = [f"{lang} ({count})" for lang, count in top_langs]
        
        # Collaborators (people they follow/followers)
        followers = github_data.get('followers_sample', [])
        following = github_data.get('following_sample', [])
        if followers or following:
            assessment['collaborators'] = followers[:3] + following[:3]
            assessment['collaborators'] = list(set(assessment['collaborators']))[:5]
        
        # Calculate risk score
        risk_score = 0
        findings = []
        
        if len(assessment['personal_info_exposed']) > 3:
            risk_score += 30
            findings.append("High personal information exposure")
        elif len(assessment['personal_info_exposed']) > 1:
            risk_score += 15
            findings.append("Moderate personal information exposure")
        
        if assessment['technical_stack']:
            risk_score += 10
            findings.append(f"Technical stack exposed: {', '.join(assessment['technical_stack'][:3])}")
        
        if assessment['collaborators']:
            risk_score += 15
            findings.append(f"Social network exposed: {len(assessment['collaborators'])} collaborators")
        
        if user.get('email'):
            risk_score += 20
            findings.append("Email address publicly exposed")
        
        # Determine exposure level
        if risk_score > 60:
            assessment['exposure_level'] = 'HIGH'
        elif risk_score > 30:
            assessment['exposure_level'] = 'MEDIUM'
        else:
            assessment['exposure_level'] = 'LOW'
        
        assessment['risk_score'] = min(risk_score, 100)
        assessment['findings'] = findings
        
        return assessment
    
    def _identify_threat_vectors(self, github_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential threat vectors"""
        threat_vectors = []
        
        user = github_data.get('user', {})
        
        # Vector 1: Social Engineering via Email
        if user.get('email'):
            threat_vectors.append({
                'vector': 'Email Social Engineering',
                'description': f"Email address {user['email']} is publicly exposed",
                'severity': 'HIGH',
                'mitigation': 'Use GitHub private email or remove email from profile'
            })
        
        # Vector 2: Personal Information
        exposed_info = []
        if user.get('name'):
            exposed_info.append('Name')
        if user.get('location'):
            exposed_info.append('Location')
        if user.get('company'):
            exposed_info.append('Company')
        
        if exposed_info:
            threat_vectors.append({
                'vector': 'Personal Information Exposure',
                'description': f"Exposed: {', '.join(exposed_info)}",
                'severity': 'MEDIUM',
                'mitigation': 'Review GitHub profile privacy settings'
            })
        
        # Vector 3: Technical Stack Targeting
        languages = github_data.get('languages', {})
        if languages:
            top_langs = list(languages.keys())[:3]
            threat_vectors.append({
                'vector': 'Technical Stack Targeting',
                'description': f"Tech stack exposed: {', '.join(top_langs)}",
                'severity': 'MEDIUM',
                'mitigation': 'Consider using organization account for work repos'
            })
        
        # Vector 4: Social Network Mapping
        followers = github_data.get('followers_sample', [])
        if followers:
            threat_vectors.append({
                'vector': 'Social Network Mapping',
                'description': f"{len(followers)} followers identified. Attackers can map connections",
                'severity': 'LOW',
                'mitigation': 'Review follower list regularly'
            })
        
        return threat_vectors
    
    def _generate_recommendations(self, threat_vectors: List[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        for vector in threat_vectors:
            mitigation = vector.get('mitigation')
            if mitigation and mitigation not in recommendations:
                recommendations.append(f"• {mitigation}")
        
        # Add general recommendations
        general_recs = [
            "• Use a private email for GitHub account",
            "• Review and limit personal information in profile",
            "• Use organization accounts for work repositories",
            "• Regular security audit of public presence",
            "• Enable two-factor authentication"
        ]
        
        for rec in general_recs:
            if rec not in recommendations:
                recommendations.append(rec)
        
        return recommendations[:6]  # Limit to top 6
    
    def _attacker_perspective(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate attacker perspective analysis"""
        assessment = profile.get('social_engineering_assessment', {})
        
        return {
            'attacker_view': [
                f"Target identified: {profile['target']}",
                f"Exposure level: {assessment.get('exposure_level', 'UNKNOWN')}",
                f"Number of attack vectors: {len(profile.get('threat_vectors', []))}",
                "Attack surface includes: personal info, technical stack, network"
            ],
            'recommended_actions': [
                "Immediately review and secure exposed information",
                "Implement security awareness training",
                "Monitor for targeted attacks",
                "Conduct regular OSINT assessments"
            ],
            'risk_summary': {
                'personal_info': len(assessment.get('personal_info_exposed', [])),
                'tech_stack': len(assessment.get('technical_stack', [])),
                'collaborators': len(assessment.get('collaborators', [])),
                'total_risk_score': assessment.get('risk_score', 0)
            }
        }

def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     SQR CyberSecurity - Target Profile Builder          ║
    ║             Professional Implementation                  ║
    ║                 (Educational Use Only)                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    builder = TargetProfileBuilder()
    
    # Test with torvalds
    test_username = "torvalds"
    print(f"📊 Building profile for: {test_username}\n")
    
    profile = builder.build_profile(test_username)
    
    print("="*70)
    print("📋 TARGET PROFILE SUMMARY")
    print("="*70)
    
    if profile.get('github_data', {}).get('error'):
        print(f"❌ Error: {profile['github_data']['error']}")
        return
    
    user = profile.get('github_data', {}).get('user', {})
    print(f"👤 Target: {profile['target']}")
    print(f"📛 Name: {user.get('name', 'N/A')}")
    print(f"🏢 Company: {user.get('company', 'N/A')}")
    print(f"📍 Location: {user.get('location', 'N/A')}")
    print(f"📊 Public Repos: {user.get('public_repos', 0)}")
    print(f"👥 Followers: {user.get('followers', 0)}")
    
    assessment = profile.get('social_engineering_assessment', {})
    print(f"\n📊 Risk Score: {assessment.get('risk_score', 0)}/100")
    print(f"⚠️ Exposure Level: {assessment.get('exposure_level', 'UNKNOWN')}")
    
    print(f"\n🔍 Personal Info Exposed:")
    for info in assessment.get('personal_info_exposed', []):
        print(f"  • {info}")
    
    print(f"\n🔧 Technical Stack:")
    for stack in assessment.get('technical_stack', []):
        print(f"  • {stack}")
    
    print(f"\n🚨 Threat Vectors:")
    for vector in profile.get('threat_vectors', []):
        print(f"  • {vector['vector']} ({vector['severity']})")
    
    print(f"\n💡 Recommendations:")
    for rec in profile.get('recommendations', []):
        print(f"  {rec}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
