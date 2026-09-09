#!/usr/bin/env python3
"""
USB Drop Attack Simulator
SQR CyberSecurity Internship - Day 8

Features:
- Benign USB payload simulation
- System information collection
- Autorun simulation
- Security awareness training
"""

import platform
import socket
import datetime
import os
import json
import logging
import psutil
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class USBPayloadSimulator:
    """Professional USB drop attack simulator"""
    
    def __init__(self):
        self.payload_types = {
            'recon': {
                'name': 'System Reconnaissance',
                'description': 'Collects system information',
                'severity': 'LOW'
            },
            'credential': {
                'name': 'Credential Harvesting',
                'description': 'Simulates credential collection',
                'severity': 'HIGH'
            },
            'backdoor': {
                'name': 'Backdoor Installation',
                'description': 'Simulates backdoor installation',
                'severity': 'CRITICAL'
            }
        }
        
        self.autorun_scripts = {
            'windows': 'autorun.inf',
            'linux': 'autorun.sh',
            'mac': 'autorun.command'
        }
    
    def simulate_usb_insertion(self, payload_type: str = 'recon') -> Dict[str, Any]:
        """
        Simulate USB insertion with payload execution
        """
        logger.info(f"Simulating USB insertion with {payload_type} payload")
        
        result = {
            'timestamp': datetime.datetime.now().isoformat(),
            'payload_type': payload_type,
            'payload_name': self.payload_types.get(payload_type, {}).get('name', 'Unknown'),
            'severity': self.payload_types.get(payload_type, {}).get('severity', 'LOW'),
            'system_info': self._collect_system_info(),
            'autorun_script': self._generate_autorun_script(),
            'recon_data': self._collect_recon_data(),
            'usb_details': self._get_usb_details(),
            'red_flags': self._get_red_flags(),
            'defense_tips': self._get_defense_tips()
        }
        
        return result
    
    def _collect_system_info(self) -> Dict[str, Any]:
        """Collect system information"""
        info = {
            'hostname': socket.gethostname(),
            'os': platform.system(),
            'os_version': platform.version(),
            'os_release': platform.release(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
        }
        
        # Get network info
        try:
            hostname = socket.gethostname()
            info['ip_address'] = socket.gethostbyname(hostname)
        except:
            info['ip_address'] = 'Unknown'
        
        # Get user info
        info['username'] = os.getenv('USERNAME') or os.getenv('USER') or 'Unknown'
        info['current_directory'] = os.getcwd()
        
        return info
    
    def _collect_recon_data(self) -> Dict[str, Any]:
        """Collect reconnaissance data"""
        recon = {
            'system': {},
            'network': {},
            'processes': [],
            'drives': []
        }
        
        # System info
        try:
            recon['system'] = {
                'cpu_count': psutil.cpu_count(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_total': self._format_bytes(psutil.virtual_memory().total),
                'memory_available': self._format_bytes(psutil.virtual_memory().available),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': self._format_bytes(psutil.disk_usage('/').used),
                'disk_free': self._format_bytes(psutil.disk_usage('/').free),
                'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
        except:
            recon['system']['error'] = 'Could not collect system info'
        
        # Network info
        try:
            interfaces = []
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        interfaces.append({
                            'interface': interface,
                            'ip': addr.address,
                            'netmask': addr.netmask
                        })
            recon['network']['interfaces'] = interfaces
        except:
            recon['network']['error'] = 'Could not collect network info'
        
        # Processes
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    recon['processes'].append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu': round(proc.info['cpu_percent'] or 0, 2),
                        'memory': round(proc.info['memory_percent'] or 0, 2)
                    })
                except:
                    continue
            recon['processes'] = recon['processes'][:10]  # Limit to 10
        except:
            recon['processes'] = []
        
        # Drives
        try:
            for partition in psutil.disk_partitions():
                recon['drives'].append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype
                })
        except:
            recon['drives'] = []
        
        return recon
    
    def _generate_autorun_script(self) -> Dict[str, str]:
        """Generate autorun script simulation"""
        scripts = {}
        
        # Windows autorun.inf
        scripts['windows'] = f"""[AutoRun]
open=payload.exe
icon=drive.ico
label=USB Drive
action=Open folder to view files
shell\open=Open
shell\open\command=payload.exe
        
# Simulated autorun - Actual malware would execute automatically
# This is for EDUCATIONAL PURPOSES only
"""
        
        # Linux autorun.sh
        scripts['linux'] = f"""#!/bin/bash
# USB Autorun Script (Simulated)
# This is for EDUCATIONAL PURPOSES only

echo "USB Drive Detected - Simulating payload execution..."
echo "System Information:"
hostname
whoami
pwd

# Simulated payload would execute here
# In a real attack, this would be malicious code
"""
        
        # Mac autorun.command
        scripts['mac'] = f"""#!/bin/bash
# USB Autorun Script (Simulated) - Mac Version
# This is for EDUCATIONAL PURPOSES only

echo "USB Drive Detected - Simulating payload execution..."
echo "System Information:"
hostname
whoami
pwd

# Simulated payload would execute here
# In a real attack, this would be malicious code
"""
        
        return scripts
    
    def _get_usb_details(self) -> Dict[str, str]:
        """Get simulated USB details"""
        return {
            'usb_name': 'USB_DRIVE_2024',
            'usb_size': '64GB',
            'usb_format': 'FAT32',
            'usb_type': 'USB 3.0',
            'manufacturer': 'Generic',
            'serial_number': 'USB-2024-XXXX-XXXX'
        }
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.1f} TB"
    
    def _get_red_flags(self) -> List[str]:
        """Get red flags for awareness"""
        return [
            '⚠️ Unknown USB drives found in parking lot/office',
            '⚠️ USB drive with no label or suspicious label',
            '⚠️ Unexpected AutoRun prompt when inserting USB',
            '⚠️ USB drive found in unusual location',
            '⚠️ USB drive from unknown source'
        ]
    
    def _get_defense_tips(self) -> List[str]:
        """Get defense tips"""
        return [
            '✅ Never plug in unknown USB drives',
            '✅ Disable AutoRun/AutoPlay on workstations',
            '✅ Use endpoint DLP solutions',
            '✅ Employee security awareness training',
            '✅ Report suspicious USB devices to IT',
            '✅ Use USB blocking policies',
            '✅ Regular security audits'
        ]


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     SQR CyberSecurity - USB Drop Attack Simulator       ║
    ║             Professional Implementation                  ║
    ║                 (Educational Use Only)                   ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    simulator = USBPayloadSimulator()
    
    print("📋 Simulating USB Drop Attack\n")
    print("="*70)
    
    # Simulate USB insertion
    result = simulator.simulate_usb_insertion('recon')
    
    print(f"🕒 Timestamp: {result['timestamp']}")
    print(f"💾 Payload: {result['payload_name']} ({result['severity']} severity)")
    
    print("\n🖥️ System Information:")
    sys_info = result['system_info']
    print(f"   Hostname: {sys_info.get('hostname', 'Unknown')}")
    print(f"   OS: {sys_info.get('os', 'Unknown')} {sys_info.get('os_release', '')}")
    print(f"   Username: {sys_info.get('username', 'Unknown')}")
    print(f"   IP Address: {sys_info.get('ip_address', 'Unknown')}")
    
    print(f"\n💾 USB Details:")
    usb = result['usb_details']
    print(f"   Name: {usb.get('usb_name', 'Unknown')}")
    print(f"   Size: {usb.get('usb_size', 'Unknown')}")
    print(f"   Format: {usb.get('usb_format', 'Unknown')}")
    
    print(f"\n🚨 Red Flags:")
    for flag in result['red_flags'][:3]:
        print(f"   {flag}")
    
    print(f"\n🛡️ Defense Tips:")
    for tip in result['defense_tips'][:3]:
        print(f"   {tip}")
    
    print("\n" + "="*70)
    print("✅ USB Drop Attack Simulation Complete")

if __name__ == "__main__":
    main()
