# Email Configuration File (SAMPLE)
# This file is a template showing the required configuration structure.
# 
# INSTRUCTIONS:
# 1. Copy this file as 'config.py' in the same directory
# 2. Update the values with your actual information
# 3. Add 'config.py' to your .gitignore to keep your credentials safe
# 4. Never commit config.py with real credentials to git

# Your Personal Information
YOUR_NAME = "Your Full Name"  # Update with your full name
YOUR_EMAIL = "your.email@gmail.com"  # Update with your email address
YOUR_PHONE = "+1234567890"  # Optional: Add your phone number
YOUR_LINKEDIN = "https://www.linkedin.com/in/yourprofile/"  # Optional: Add your LinkedIn profile URL
YOUR_WEBSITE = "https://yourwebsite.com/portfolio/"  # Optional: Add your portfolio/website URL

# Email Credentials
# IMPORTANT: For Gmail, use an "App Password" instead of your regular password
# How to create Gmail App Password:
# 1. Go to Google Account settings
# 2. Security > 2-Step Verification (enable if not already)
# 3. Security > App passwords
# 4. Generate a new app password for "Mail"
# 5. Copy the 16-character password here
YOUR_PASSWORD = "xxxx xxxx xxxx xxxx"  # 16-character app password

# Resume Path
# Update this with the absolute path to your resume file
RESUME_PATH = r"C:\path\to\your\resume.pdf"  # or /Users/username/path/to/resume.pdf on Mac

# Application Content — this is what makes the tool work for ANY role, not just DevOps.
# Update these to match the job you're applying for.
TARGET_ROLE = "DevOps Engineer"  # e.g. "Backend Engineer", "Data Analyst", "Product Manager"
EXPERIENCE_SUMMARY = "4+ years of proven track record in cloud infrastructure, automation, and CI/CD pipelines"

# Skill bullets shown in "Key Highlights of My Profile". List whatever's true for you.
# Put tools/technologies in parentheses (e.g. "Skilled in X (Tool A, Tool B)") — these
# are automatically picked up as keywords when tailoring the email to a pasted job description.
SKILL_HIGHLIGHTS = [
    "Expertise in cloud platforms (AWS, Azure, GCP)",
    "Proficient in containerization technologies (Docker, Kubernetes)",
    "Strong experience with CI/CD tools (Jenkins, GitLab CI, GitHub Actions)",
    "Infrastructure as Code (Terraform, Ansible, CloudFormation)",
    "Monitoring and logging solutions (Prometheus, Grafana, ELK Stack)",
    "Scripting languages (Python, Bash, PowerShell)",
    "Version control systems (Git, GitHub, GitLab)",
]
# Example for a completely different role — just replace the list above with something like:
# SKILL_HIGHLIGHTS = [
#     "Proficient in backend development (Java, Spring Boot, Node.js)",
#     "Experience with relational and NoSQL databases (PostgreSQL, MongoDB)",
#     "Strong understanding of REST API design and microservices architecture",
# ]

# Optional extra details listed at the end of the email (experience, CTC, notice
# period, location, etc.). Leave this as an empty dict to omit the section entirely —
# useful if you don't want to share compensation/notice-period details in a cold email.
APPLICATION_DETAILS = {
    # "Total Experience": "3 years",
    # "Notice Period": "30 days",
    # "Current Location": "Bangalore",
}

# SMTP Server Configuration
# Gmail (default)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# For other email providers, uncomment the one you're using:
# Outlook/Hotmail
# SMTP_SERVER = "smtp.office365.com"
# SMTP_PORT = 587

# Yahoo
# SMTP_SERVER = "smtp.mail.yahoo.com"
# SMTP_PORT = 587

# HR Email List
# Add the HR/Recruiter email addresses you want to send applications to
HR_EMAIL_LIST = [
    "hr@company1.com",
    "recruiter@company2.com",
    # Add more email addresses below
]

# Email Settings
DELAY_BETWEEN_EMAILS = 5  # Seconds to wait between emails (avoid spam detection)
