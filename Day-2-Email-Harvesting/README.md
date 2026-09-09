<div align="center">

# 📧 Day 2: Email Harvesting & Social Engineering Prep

## Professional Email Harvester with Web Interface

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.12+-orange?style=for-the-badge)](https://www.crummy.com/software/BeautifulSoup/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

</div>

---

# 🎯 Overview

This is a professional **Email Harvester** built as Day 2 of the SQR CyberSecurity Internship program. It extracts emails from websites ethically using pattern matching and BeautifulSoup.

### What is Email Harvesting?
Email harvesting is the process of collecting email addresses from public sources. This tool demonstrates ethical reconnaissance techniques used by security professionals to understand what information is publicly exposed.

### Key Capabilities:
- 📧 **Email Extraction** - Multiple pattern matching
- 🌐 **Domain Analysis** - Identify email domains
- 📊 **Pattern Detection** - Understand naming conventions
- 🌐 **Web Interface** - Professional dark theme UI
- 📄 **Report Generation** - HTML and JSON exports

---

# ✨ Features

### 🔍 Email Harvester

| Feature | Description |
|---------|-------------|
| **Multi-Pattern Extraction** | Standard, obfuscated, mailto links |
| **Domain Analysis** | Count and categorize domains |
| **Pattern Detection** | Identify username patterns (first.last, first_last, etc.) |
| **Rate Limiting** | Avoid detection during harvesting |
| **Error Handling** | Graceful failure recovery |
| **Recursive Crawling** | Follow links up to specified depth |

### 🌐 Web Interface

| Feature | Description |
|---------|-------------|
| **Purple/Teal Theme** | Unique Day 2 design |
| **Real-time Progress** | Live harvest status |
| **Email Display** | Clean list of extracted emails |
| **Download Reports** | HTML and JSON formats |
| **Responsive Design** | Works on all devices |

---

# 🚀 Installation

### Prerequisites
- Python 3.9+
- Kali Linux (recommended) or Windows 10/11

### Quick Start

```bash
# Clone the repository
git clone https://github.com/warshia-rubab/sqrock-cybersecurity-internship.git
cd sqrock-cybersecurity-internship/Day-2-Email-Harvesting

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requests beautifulsoup4 Flask Flask-Cors

# Run the web application
python3 web_app/app.py
# Open browser: http://localhost:5001
```

### Command Line Usage
```bash
# Run the harvester directly
python3 src/email_harvester.py
# Enter URL when prompted
```
---
# 💻 Usage

### Web Interface

1. Open browser: http://localhost:5001

2. Enter URL (e.g., https://scrapinghub.com)

3. Click "Harvest"

4. View extracted emails!

### Command Line
```bash
python3 src/email_harvester.py
# Enter URL when prompted
# Reports saved in reports/ folder
```
---
# 🧪 Test Sites

### Sites with Guaranteed Emails

| Site | URL | Expected Result |
|------|-----|-----------------|
| **ScrapingHub** | `https://scrapinghub.com` | ✅ `marketing@zyte.com` |
| **Zyte** | `https://www.zyte.com` | ✅ `contact@zyte.com` |
| **Real Python** | `https://realpython.com` | ✅ `info@realpython.com` |
| **Scrapy** | `https://scrapy.org` | ✅ Multiple emails |

### Sites for Testing

| Site | URL | Expected Result |
|------|-----|-----------------|
| **Example** | `https://example.com` | ❌ No emails (safe test) |
| **MIT** | `https://mit.edu` | ⚠️ May find faculty emails |
| **Stanford** | `https://stanford.edu` | ⚠️ May find faculty emails |
| **Harvard** | `https://harvard.edu` | ⚠️ May find faculty emails |

---

## 📊 Detection Patterns

### Email Patterns Detected

| Pattern | Example | Description |
|---------|---------|-------------|
| **Standard** | `user@domain.com` | Regular email format |
| **Mailto** | `mailto:user@domain.com` | Email in mailto link |
| **Obfuscated** | `user[at]domain[dot]com` | Protected email format |
| **With Plus** | `user+alias@domain.com` | Email with plus addressing |
| **With Dash** | `user-name@domain.com` | Email with hyphens |
| **With Underscore** | `user_name@domain.com` | Email with underscores |

### Username Patterns

| Pattern | Example | Description |
|---------|---------|-------------|
| **first.last** | `john.doe@company.com` | First name + dot + last name |
| **first_last** | `john_doe@company.com` | First name + underscore + last name |
| **initials** | `jd@company.com` | Two-letter initials |
| **numeric** | `123456@company.com` | Numeric username |
| **single_word** | `johndoe@company.com` | Single word username |
| **first.middle.last** | `john.r.doe@company.com` | Full name with dots |
| **mixed_case** | `JohnDoe@company.com` | Mixed case username |

---

# 📸 Screenshots
Professional Dashboard
https://screenshots/webapp_home.png

Harvest Results
https://screenshots/webapp_results.png

Email Display
https://screenshots/webapp_new_design.png

Full Interface
https://screenshots/webapp_full.png

---

# 📁 Project Structure
```text
Day-2-Email-Harvesting/
│
├── 📁 src/
│   └── 🐍 email_harvester.py          # Core harvester
│
├── 📁 web_app/                         # Flask Web Application
│   ├── 📄 app.py                       # Main application
│   ├── 📁 templates/
│   │   └── 📄 index.html               # Main page
│   └── 📁 static/
│       ├── 📁 css/
│       │   └── 📄 style.css            # Purple/Teal theme
│       └── 📁 js/
│           └── 📄 script.js            # Frontend logic
│
├── 📁 reports/                         # Generated reports
├── 📁 data/                            # JSON data output
├── 📁 screenshots/                     # Documentation
├── 📄 README.md                        # This file
├── 📄 .gitignore                       # Git ignore rules
└── 📄 requirements.txt                 # Dependencies
```
---
# 🛠️ Technologies

### Backend

| Technology | Purpose |
|------------|---------|
| **Python 3.9+** | Core programming language |
| **Flask** | Web framework |
| **BeautifulSoup4** | HTML parsing for email extraction |
| **requests** | HTTP requests for web scraping |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5/CSS3** | Structure and styling |
| **JavaScript** | Dynamic functionality |
| **Inter Font** | Professional typography |
---

# 📊 Example Results

### ScrapingHub.com
```text
✅ Harvest completed successfully!
📧 Emails Found: 1
📧 Sample Emails Found:
  - marketing@zyte.com
```

### 🌐 Top Domains:

- zyte.com: 1 emails

### Example.com

```text
✅ Harvest completed successfully!
📧 Emails Found: 0
📊 Report Generated: reports/email_harvest_[timestamp].html
```
---





