<div align="center">

# 🔐 PASSWORD SECURITY ANALYZER

## *Brute Force & Credential Stuffing Simulator*

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Day](https://img.shields.io/badge/Day-7-orange?style=flat-square)]()

</div>

---

## 📌 EXECUTIVE SUMMARY

| | |
|---|---|
| **Project** | Password Attack Simulator |
| **Purpose** | Security Awareness & Password Strength Testing |
| **Technologies** | Python, Flask, Rate Limiting |
| **Status** | ✅ Complete |

> *"Simulates brute force attacks, rate limiting, and credential stuffing to test password security."*

---

## 🎬 MULTIMEDIA

### 📹 Video Demonstration

<p align="center">
  <video src="https://github.com/warshia-rubab/sqrock-cybersecurity-internship/raw/main/Day-7-Password-Attacks/demo.mp4" controls width="80%">
    Your browser does not support the video tag.
  </video>
</p>

<p align="center">
  <a href="https://github.com/warshia-rubab/sqrock-cybersecurity-internship/blob/main/Day-7-Password-Attacks/demo.mp4">📥 Download</a> ·
  <a href="https://youtu.be/AaLgISurWJs">📺 YouTube</a>
</p>

---

## 📸 VISUAL GALLERY

| Dashboard | Weak Password | Strong Password |
|-----------|---------------|-----------------|
| <img src="screenshots/dashboard.png" width="280"> | <img src="screenshots/weak_password.png" width="280"> | <img src="screenshots/strong_password.png" width="280"> |

---

## ⚙️ FEATURES AT A GLANCE

### 🔍 Analysis Features
┌─────────────────────────────────────────────────────────────┐
│ ✅ Password Strength Check (WEAK/MEDIUM/STRONG/VERY STRONG)│
│ ✅ Brute Force Simulation │
│ ✅ Rate Limit Detection │
│ ✅ Credential Stuffing Simulation │
│ ✅ Account Lockout Simulation │
│ ✅ Security Recommendations │
└─────────────────────────────────────────────────────────────┘

text

### 📊 Password Strength Levels

| Level | Score | Color | Description |
|-------|-------|-------|-------------|
| **WEAK** | 0-3 | 🔴 Red | Too short or single character type |
| **MEDIUM** | 4-5 | 🟡 Yellow | Moderate length, limited variety |
| **STRONG** | 6-7 | 🟢 Green | Good length, mixed case & numbers |
| **VERY STRONG** | 8-10 | 🔵 Blue | Long with special characters & mixed case |

---

## 🚀 DEPLOYMENT

### One-Line Setup

```bash
git clone https://github.com/warshia-rubab/sqrock-cybersecurity-internship.git && cd sqrock-cybersecurity-internship/Day-7-Password-Attacks && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 web_app/app.py
System Requirements
Component	Requirement
OS	Kali Linux / Ubuntu / Windows
Python	3.9+
RAM	2GB+
Browser	Modern (Chrome/Firefox)
💻 USAGE
Test Credentials
Username	Password	Expected Strength
admin	123456	❌ WEAK
user	password123	⚠️ MEDIUM
security	Secure@2024!	✅ STRONG
warshia	MySecureP@ssw0rd#2024!	✅ VERY STRONG
Quick Test Buttons
Button	Password	Expected
admin/password123	password123	⚠️ MEDIUM
user/admin	admin	❌ WEAK
test/123456	123456	❌ WEAK
📊 SAMPLE OUTPUT
Weak Password Analysis
text
Username: admin
Password: 123456

Password Strength: WEAK (2/10)
Password Length: 6

Issues Found:
• Password is too short (less than 8 characters)
• Missing uppercase letters
• Missing special characters
• Password is commonly used

Brute Force: 3 attempts, Found: YES
Rate Limit: OFF
Account Locked: NO

Recommendations:
⚠️ Your password is weak. Change it immediately!
✅ Use passwords with at least 12 characters
✅ Include uppercase, lowercase, numbers, and special characters
✅ Avoid using common passwords
Strong Password Analysis
text
Username: security
Password: Secure@2024!

Password Strength: STRONG (7/10)
Password Length: 12

Issues Found:
• None

Brute Force: 5 attempts, Found: NO
Rate Limit: OFF
Account Locked: NO

Recommendations:
✅ Good password. Consider adding special characters.
✅ Use a password manager
✅ Enable two-factor authentication (2FA)
🛠️ TECHNOLOGY STACK
Layer	Technologies
Backend	Python 3.9+, Flask
Frontend	HTML5, CSS3, JavaScript
Theme	Security Dashboard
Fonts	Orbitron, Inter
📁 PROJECT STRUCTURE
text
Day-7-Password-Attacks/
├── 📁 src/
│   └── password_attacks.py
├── 📁 web_app/
│   ├── app.py
│   ├── 📁 templates/
│   │   └── index.html
│   └── 📁 static/
│       ├── 📁 css/
│       │   └── style.css
│       └── 📁 js/
│           └── script.js
├── 📁 screenshots/
│   ├── dashboard.png
│   ├── weak_password.png
│   └── strong_password.png
├── 🎬 demo.mp4
├── 📄 README.md
├── 📄 .gitignore
└── 📄 requirements.txt
⚖️ ETHICAL GUIDELINES
Rule	Description
Educational Use Only	Never use for malicious purposes
Authorized Systems	Only on lab/authorized environments
No Real Targets	Never target real users/organizations
Legal Compliance	Follow IT Act 2000, CFAA, GDPR
🔗 CONNECT
🐙 GitHub	📹 Video Demo
📺 YouTube	📁 Day 1
📧 Day 2	🎣 Day 3
📞 Day 4	🎯 Day 5
📧 Day 6	🔐 Day 7
<div align="center">
SQR CyberSecurity Internship — Day 7

Published: September 2024

</div> ```
