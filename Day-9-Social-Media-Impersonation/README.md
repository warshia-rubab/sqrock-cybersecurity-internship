<div align="center">

# 👤 FAKE PROFILE DETECTOR

## *Social Media Impersonation & Bot Detection System*

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Day](https://img.shields.io/badge/Day-9-orange?style=flat-square)]()

</div>

---

## 📌 EXECUTIVE SUMMARY

| | |
|---|---|
| **Project** | Fake Profile Detection System |
| **Purpose** | Social Media Security Awareness |
| **Technologies** | Python, Flask, Behavioral Heuristics |
| **Status** | ✅ Complete |

> *"Detects fake/bot social media profiles using behavioral heuristics and impersonation analysis."*

---

## 🎬 MULTIMEDIA

### 📹 Video Demonstration

<p align="center">
  <video src="https://github.com/warshia-rubab/sqrock-cybersecurity-internship/raw/main/Day-9-Social-Media-Impersonation/demo.mp4" controls width="80%">
    Your browser does not support the video tag.
  </video>
</p>

<p align="center">
  <a href="https://github.com/warshia-rubab/sqrock-cybersecurity-internship/blob/main/Day-9-Social-Media-Impersonation/demo.mp4">📥 Download</a> ·
  <a href="https://youtu.be/AaLgISurWJs">📺 YouTube</a>
</p>

---

## 📸 VISUAL GALLERY

| Dashboard | Real Profile | Bot Profile |
|-----------|--------------|-------------|
| <img src="screenshots/dashboard.png" width="280"> | <img src="screenshots/real_profile.png" width="280"> | <img src="screenshots/bot_profile.png" width="280"> |

---

## ⚙️ FEATURES AT A GLANCE

### 🔍 Detection Methods

| Method | Description | Weight |
|--------|-------------|--------|
| **Account Age** | New accounts (< 30 days) are suspicious | +30 |
| **Follower Ratio** | Following >> Followers indicates bot | +25 |
| **Profile Picture** | Missing picture is a red flag | +20 |
| **Post Count** | Very few posts suggests fake | +15 |
| **Bio Quality** | Default/empty bios are suspicious | +15 |
| **Verification** | Unverified accounts are higher risk | +30 |
| **Username Pattern** | Random numbers/patterns indicate bots | +15 |

### 🎯 Risk Levels
┌─────────────────────────────────────────────────────────────┐
│ 🟢 LOW 0-25 → Likely legitimate │
│ 🟡 MEDIUM 26-50 → Some suspicious signs │
│ 🟠 HIGH 51-70 → Likely fake/bot │
│ 🔴 CRITICAL 71-100 → Almost certainly fake │
└─────────────────────────────────────────────────────────────┘

text

---

## 🚀 DEPLOYMENT

### One-Line Setup

```bash
git clone https://github.com/warshia-rubab/sqrock-cybersecurity-internship.git && cd sqrock-cybersecurity-internship/Day-9-Social-Media-Impersonation && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 web_app/app.py
System Requirements
Component	Requirement
OS	Kali Linux / Ubuntu / Windows
Python	3.9+
RAM	2GB+
Browser	Modern (Chrome/Firefox)
💻 USAGE
Test Profiles
Button	Profile	Expected Score
✅ Real Profile	john_doe_real	🟢 LOW (0-25)
🤖 Bot Profile	user_8374	🔴 CRITICAL (70+)
⚠️ Suspicious Profile	emma_wilson_2024	🟠 HIGH (50-70)
🔍 Impersonation	Compares Profile 1 vs 2	Shows similarity %
📊 SAMPLE OUTPUT
Real Profile Analysis
text
Username: john_doe_real
Name: John Doe
Account Age: 1200 days
Followers: 4,500
Following: 320
Posts: 870

📊 Fake Score: 10/100
⚠️ Risk Level: LOW

🔍 Behavioral Heuristics:
  ✅ Account Age: 1200 days (Safe)
  ✅ Follower Ratio: 0.07:1 (Healthy)
  ✅ Profile Picture: Yes
  ✅ Post Count: 870 posts
  ✅ Bio Quality: Detailed bio
  ✅ Verification: Verified

🤖 Bot Signals: None detected

💡 Recommendations:
  ✅ Profile appears legitimate
  ✅ Continue normal interaction
Bot Profile Analysis
text
Username: user_8374
Name: Sarah Smith
Account Age: 7 days
Followers: 2
Following: 900
Posts: 1

📊 Fake Score: 85/100
⚠️ Risk Level: CRITICAL

🔍 Behavioral Heuristics:
  ❌ Account Age: 7 days (Suspicious)
  ❌ Follower Ratio: 450:1 (Abnormal)
  ❌ Profile Picture: Missing
  ❌ Post Count: 1 post
  ❌ Bio Quality: Default bio
  ❌ Verification: Not verified

🤖 Bot Signals Detected:
  • New account (under 30 days)
  • Abnormal follower ratio: 450:1
  • No profile picture
  • Very few posts
  • Default or empty bio
  • Not verified

💡 Recommendations:
  ✅ Verify the account through official channels
  ✅ Check for inconsistencies in profile information
  ✅ Report suspicious accounts to the platform
  ⚠️ Be cautious with new accounts
  ⚠️ Lack of profile picture is a red flag
🛠️ TECHNOLOGY STACK
Layer	Technologies
Backend	Python 3.9+, Flask
Frontend	HTML5, CSS3, JavaScript
Theme	Social Media Analytics
Fonts	Orbitron, Inter
📁 PROJECT STRUCTURE
text
Day-9-Social-Media-Impersonation/
├── 📁 src/
│   └── fake_profile_detector.py
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
│   ├── real_profile.png
│   └── bot_profile.png
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
💾 Day 8	👤 Day 9
<div align="center">
SQR CyberSecurity Internship — Day 9

Published: September 2024

</div> ```
