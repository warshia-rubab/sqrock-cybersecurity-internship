#!/usr/bin/env python3
"""
Baiting & Watering Hole Attack Simulator
SQR CyberSecurity Internship - Day 10

Features:
- Honeypot link tracker
- Watering hole simulation
- Attack logging
- IP tracking
- Security awareness
"""

import json
import logging
import datetime
import random
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Store logs in memory (in production, use database)
ATTACK_LOGS = []
BAIT_LINKS = []


@dataclass
class AttackLog:
    """Data structure for attack logs"""
    timestamp: str
    ip: str
    user_agent: str
    bait_type: str
    path: str
    location: str


class BaitingSimulator:
    """Professional baiting and watering hole simulator"""
    
    def __init__(self):
        self.bait_types = {
            'usb_drop': {
                'name': 'USB Drop',
                'description': 'USB drive left in parking lot',
                'icon': '💾',
                'severity': 'HIGH'
            },
            'free_software': {
                'name': 'Free Software Download',
                'description': 'Fake software download link',
                'icon': '📥',
                'severity': 'MEDIUM'
            },
            'free_music': {
                'name': 'Free Music Download',
                'description': 'Fake music download link',
                'icon': '🎵',
                'severity': 'MEDIUM'
            },
            'free_movie': {
                'name': 'Free Movie Streaming',
                'description': 'Fake movie streaming link',
                'icon': '🎬',
                'severity': 'HIGH'
            },
            'free_gift': {
                'name': 'Free Gift',
                'description': 'Fake gift giveaway link',
                'icon': '🎁',
                'severity': 'CRITICAL'
            }
        }
        
        self.watering_hole_targets = [
            'tech_news_site',
            'industry_blog',
            'professional_forum',
            'social_media',
            'job_site'
        ]
        
        self.ip_locations = {
            '192.168.1.': 'Internal Network',
            '10.0.0.': 'Corporate Network',
            '172.16.': 'Private Network',
            '45.33.': 'USA',
            '93.184.': 'USA',
            '151.101.': 'USA',
            '2a02:': 'Europe',
            '2001:': 'Global'
        }
    
    def generate_bait_link(self, bait_type: str) -> Dict[str, Any]:
        """Generate a bait link for the honeypot"""
        logger.info(f"Generating bait link: {bait_type}")
        
        bait = self.bait_types.get(bait_type, self.bait_types['free_gift'])
        
        link_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        
        link = {
            'id': link_id,
            'type': bait_type,
            'name': bait['name'],
            'description': bait['description'],
            'icon': bait['icon'],
            'severity': bait['severity'],
            'url': f'/bait/{link_id}',
            'created_at': datetime.datetime.now().isoformat(),
            'clicks': 0,
            'visitors': []
        }
        
        BAIT_LINKS.append(link)
        
        return link
    
    def log_attack(self, link_id: str, ip: str, user_agent: str, path: str) -> Dict[str, Any]:
        """Log an attack/click on a bait link"""
        logger.info(f"Attack logged: {link_id} from {ip}")
        
        # Find the bait link
        bait = next((b for b in BAIT_LINKS if b['id'] == link_id), None)
        
        if not bait:
            return {'error': 'Bait link not found'}
        
        # Get location
        location = self._get_location(ip)
        
        # Create log entry
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'ip': ip,
            'user_agent': user_agent,
            'bait_type': bait['type'],
            'bait_name': bait['name'],
            'path': path,
            'location': location,
            'severity': bait['severity']
        }
        
        ATTACK_LOGS.append(log_entry)
        
        # Update bait link
        bait['clicks'] += 1
        bait['visitors'].append({
            'ip': ip,
            'timestamp': datetime.datetime.now().isoformat(),
            'location': location
        })
        
        return log_entry
    
    def simulate_watering_hole(self, target_type: str) -> Dict[str, Any]:
        """Simulate a watering hole attack"""
        logger.info(f"Simulating watering hole: {target_type}")
        
        attack = {
            'target_type': target_type,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'active',
            'details': self._get_watering_hole_details(target_type),
            'red_flags': self._get_watering_hole_red_flags(),
            'defense_tips': self._get_watering_hole_defense_tips()
        }
        
        return attack
    
    def _get_location(self, ip: str) -> str:
        """Get location from IP address"""
        for prefix, location in self.ip_locations.items():
            if ip.startswith(prefix):
                return location
        return 'Unknown Location'
    
    def _get_watering_hole_details(self, target_type: str) -> Dict[str, str]:
        """Get watering hole details"""
        details = {
            'tech_news_site': {
                'name': 'Tech News Site',
                'description': 'Popular tech news site compromised',
                'risk': 'HIGH'
            },
            'industry_blog': {
                'name': 'Industry Blog',
                'description': 'Industry-specific blog compromised',
                'risk': 'MEDIUM'
            },
            'professional_forum': {
                'name': 'Professional Forum',
                'description': 'Professional forum compromised',
                'risk': 'HIGH'
            },
            'social_media': {
                'name': 'Social Media Platform',
                'description': 'Social media platform compromised',
                'risk': 'CRITICAL'
            },
            'job_site': {
                'name': 'Job Site',
                'description': 'Job search website compromised',
                'risk': 'HIGH'
            }
        }
        return details.get(target_type, details['tech_news_site'])
    
    def _get_watering_hole_red_flags(self) -> List[str]:
        """Get watering hole red flags"""
        return [
            '⚠️ Unexpected redirects from trusted sites',
            '⚠️ Unusual pop-ups or ads on trusted sites',
            '⚠️ Requests for credentials on unexpected pages',
            '⚠️ Changes in site behavior or appearance',
            '⚠️ Suspicious scripts loading from unknown domains'
        ]
    
    def _get_watering_hole_defense_tips(self) -> List[str]:
        """Get watering hole defense tips"""
        return [
            '✅ Keep browsers and plugins updated',
            '✅ Use script-blocking extensions',
            '✅ Implement web filtering solutions',
            '✅ Monitor for unusual site behavior',
            '✅ Use DNS filtering services',
            '✅ Regular security awareness training'
        ]
    
    def get_attack_logs(self) -> List[Dict[str, Any]]:
        """Get all attack logs"""
        return ATTACK_LOGS
    
    def get_bait_links(self) -> List[Dict[str, Any]]:
        """Get all bait links"""
        return BAIT_LINKS
    
    def get_attack_summary(self) -> Dict[str, Any]:
        """Get attack summary statistics"""
        total_attacks = len(ATTACK_LOGS)
        
        severity_counts = {}
        for log in ATTACK_LOGS:
            severity = log.get('severity', 'UNKNOWN')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        bait_counts = {}
        for log in ATTACK_LOGS:
            bait = log.get('bait_name', 'UNKNOWN')
            bait_counts[bait] = bait_counts.get(bait, 0) + 1
        
        return {
            'total_attacks': total_attacks,
            'severity_counts': severity_counts,
            'bait_counts': bait_counts,
            'unique_ips': len(set(log.get('ip') for log in ATTACK_LOGS))
        }


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     SQR CyberSecurity - Baiting & Watering Hole         ║
    ║             Attack Simulator                             ║
    ║                 (Educational Use Only)                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    simulator = BaitingSimulator()
    
    print("📋 Generating Bait Links\n")
    print("="*70)
    
    # Generate bait links
    for bait_type in simulator.bait_types:
        link = simulator.generate_bait_link(bait_type)
        print(f"🔗 {link['icon']} {link['name']}")
        print(f"   URL: {link['url']}")
        print(f"   Severity: {link['severity']}")
        print(f"   ID: {link['id']}")
        print("-"*50)
    
    print("\n📋 Simulating Watering Hole Attack\n")
    print("="*70)
    
    attack = simulator.simulate_watering_hole('tech_news_site')
    print(f"🎯 Target: {attack['target_type']}")
    print(f"📝 Description: {attack['details']['description']}")
    print(f"⚠️ Risk: {attack['details']['risk']}")
    print("\n🚨 Red Flags:")
    for flag in attack['red_flags'][:3]:
        print(f"   {flag}")
    print("\n🛡️ Defense Tips:")
    for tip in attack['defense_tips'][:3]:
        print(f"   {tip}")
    
    print("\n" + "="*70)
    print("✅ Simulation Complete")

if __name__ == "__main__":
    main()
