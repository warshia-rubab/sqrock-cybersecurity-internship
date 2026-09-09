<div align="center">

# 📞 Social Engineering Script Generator

## *Vishing & Smishing Simulation for Security Awareness*

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Day](https://img.shields.io/badge/Day-4-orange?style=for-the-badge)]()

</div>

---

## 📌 What Is This?

A **professional social engineering script generator** for security awareness training. Creates realistic vishing (voice phishing) scripts and smishing (SMS phishing) messages with psychological trigger analysis.

```bash
$ ./vishing-generator --help
📋 Social Engineering Script Generator v2.0
🔒 Educational Use Only - Authorized Environments
📌 Available Categories: [it_support] [bank] [government] [smishing]
```

🎬 Live Demo
📹 Video Demonstration — Complete walkthrough of Day 4

<p align="center"> <video src="https://github.com/warshia-rubab/sqrock-cybersecurity-internship/raw/main/Day-4-Vishing-Smishing/demo.mp4" controls width="80%"> Your browser does not support the video tag. </video> </p><p align="center"> <a href="https://github.com/warshia-rubab/sqrock-cybersecurity-internship/blob/main/Day-4-Vishing-Smishing/demo.mp4"> 📥 Download Video </a> &nbsp;·&nbsp; </p>
📸 Screenshots
Terminal Interface
<p align="center"> <img src="Dashboard.png" alt="Dashboard" width="90%"> </p>
Bank Script Generation
<p align="center"> <img src="Working.png" alt="Working" width="90%"> </p>
Server Logs
<p align="center"> <img src="Logs.png" alt="Logs" width="90%"> </p>

⚡ Features
📞 Vishing Scripts
Category	Description	Psychological Triggers
IT Support	Password reset scams	Authority, Fear, Urgency
Bank Fraud	Account verification scams	Authority, Fear, Scarcity
Government	ID verification scams	Authority, Fear, Trust
📱 Smishing Messages
Feature	Description
Urgent Language	"Your account has been flagged"
Short Links	bit.ly links for credibility
Red Flags	Identifies suspicious elements
🧠 Analysis
Feature	Description
Psychological Triggers	Identifies manipulation techniques
Red Flags	Highlights suspicious elements
Awareness Training	Educational content included
🚀 Quick Start
bash
# Clone and setup
git clone https://github.com/warshia-rubab/sqrock-cybersecurity-internship.git
cd sqrock-cybersecurity-internship/Day-4-Vishing-Smishing

# Install and run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 web_app/app.py
Open: http://localhost:5003

💻 Usage
Available Commands
Command	Output
it_support	IT Support vishing script
bank	Bank fraud vishing script
government	Government vishing script
smishing	SMS phishing message
Quick Buttons
Button	Action
📞 IT Support	Generates IT Support script
🏦 Bank	Generates Bank script
🏛️ Government	Generates Government script
📱 Smishing	Generates SMS message
📊 Example Output
Bank Script Generation
text
📋 Generating BANK Script...
👤 Caller: Lisa from City Bank
🎯 Target: Employee

=== VISHING AWARENESS SCRIPT ===

[OPENING]
Hello, I'm Lisa calling from City Bank Security.

[HOOK]
There's been unusual activity on your account.
"I need to verify your identity - can you confirm your employee ID and password?"

[RED FLAGS FOR AWARENESS]
• Banks NEVER ask for PIN or full card numbers
• Verify by calling the number on your card
• Never share OTP or security codes

[PROPER RESPONSE]
• Do NOT provide any personal information
• Hang up immediately
• Call the official number
• Report the incident to security

🧠 Psychological Triggers: Authority, Fear, Scarcity
🛠️ Technologies
Layer	Tools
Backend	Python 3.9+, Flask
Frontend	HTML5, CSS3 (Terminal/Hacker Theme), JavaScript
Security	Awareness Training, Red Flag Identification
📁 Project Structure
text
Day-4-Vishing-Smishing/
├── src/
│   └── vishing_generator.py     # Script generator
├── web_app/
│   ├── app.py                    # Flask app
│   ├── templates/
│   │   └── index.html            # Terminal theme
│   └── static/
│       ├── css/style.css         # Hacker theme
│       └── js/script.js          # Terminal interaction
├── screenshots/
│   ├── Dashboard.png
│   ├── Working.png
│   └── Logs.png
├── demo.mp4                      # Video demonstration
├── README.md
├── .gitignore
└── requirements.txt
⚖️ Ethical Notice
⚠️ Educational Use Only — These scripts are for awareness training only. Never use for malicious purposes.

Rule	Explanation
Authorized Systems ONLY	All tasks must be performed on lab VMs or authorized systems
No Real Targets	Never use against real users or organizations
Legal Compliance	Follow IT Act 2000, CFAA, GDPR
🔗 Quick Links
📹 Video Demo	📺 YouTube
🐙 GitHub Repo	📁 Day 1: OSINT
📧 Day 2: Email	🎣 Day 3: Phishing
<div align="center">
SQR CyberSecurity Internship — Day 4

Last Updated: September 2024

</div> ```
