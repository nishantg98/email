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
