# DevOps Engineer Job Application Email Sender

An automated Python script to send professional cold emails for DevOps Engineer job applications to multiple HR contacts with your resume attached.

## 📋 Features

- ✉️ Send personalized job application emails to multiple HR contacts
- 📎 Automatically attach your resume
- ⏱️ Built-in delay between emails to avoid spam detection
- 🔒 Secure email authentication
- 📊 Progress tracking and success/failure reporting
- 🎯 Professional email template for DevOps Engineer positions

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- Gmail account (or other email provider with SMTP access)
- Your resume in PDF format

### Setup Instructions

#### Step 1: Enable Gmail App Password (for Gmail users)

**Important:** Do NOT use your regular Gmail password. Create an App Password instead:

1. Go to your [Google Account](https://myaccount.google.com/)
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google", enable **2-Step Verification** (if not already enabled)
4. Go back to Security, find **App passwords**
5. Select **Mail** as the app and **Windows Computer** as the device
6. Click **Generate**
7. Copy the 16-character password (format: xxxx xxxx xxxx xxxx)

#### Step 2: Configure the Script

1. Open `config.py` in a text editor
2. Update the following fields:

```python
# Your Personal Information
YOUR_NAME = "Your Full Name"  # Update with your name
YOUR_EMAIL = "youremail@gmail.com"  # Your Gmail address
YOUR_PASSWORD = "xxxx xxxx xxxx xxxx"  # The 16-character app password from Step 1

# Resume Path
RESUME_PATH = r"c:\path\to\your\resume.pdf"  # Full path to your resume

# HR Email List
HR_EMAIL_LIST = [
    "hr1@company1.com",
    "hr2@company2.com",
    "recruiter@company3.com",
    # Add more emails here
]
```

#### Step 3: Run the Script

Open Command Prompt or PowerShell (or your terminal) and navigate to the folder:

```bash
cd "c:\Users\test"
python send_applications.py
```

---

## 🌐 Optional: Web Interface Deployment
You can also run the application as a small web service so that you can use a
browser to send individual emails or upload resumes. The easiest free hosting
for Python apps is [PythonAnywhere](https://www.pythonanywhere.com/).

### Deploying to PythonAnywhere (free tier)
1. **Sign up** for an account and verify your email.
2. **Clone your repo** on the PythonAnywhere Bash console:
   ```bash
   git clone https://github.com/nishantg98/email.git
   cd email
   pip install --user -r requirements.txt
   ```
3. **Create a new web app** in the Web tab (choose Flask, Python 3.10).
4. **Edit the WSGI file** (click the link on the Web tab) and replace contents
   with:
   ```python
   import sys, os
   path = '/home/YOUR_USERNAME/email'
   if path not in sys.path:
       sys.path.append(path)

   # set environment variables (free accounts)
   os.environ.setdefault('YOUR_NAME', 'Your Name')
   os.environ.setdefault('YOUR_EMAIL', 'youremail@gmail.com')
   os.environ.setdefault('YOUR_PASSWORD', 'xxxx xxxx xxxx xxxx')
   os.environ.setdefault('YOUR_PHONE', '+1234567890')
   os.environ.setdefault('YOUR_LINKEDIN', 'https://linkedin.com/...')
   os.environ.setdefault('YOUR_WEBSITE', 'https://your.site')

   from app import app as application
   ```
5. **Reload** the web app and visit `https://YOUR_USERNAME.pythonanywhere.com`
   to use the browser interface.
6. Keep your free site alive by logging in at least once per month.

> The app still uses Gmail SMTP and your App Password; nothing else is
> required, and the web UI simply calls the same `email_sender_v2` logic.

---
## 📧 Email Template

The script sends a professional email with the following structure:

**Subject:** Application for DevOps Engineer Position - [Your Name]

**Body includes:**
- Professional greeting
- Expression of interest
- Key highlights of your DevOps skills:
  - Cloud platforms (AWS, Azure, GCP)
  - Containerization (Docker, Kubernetes)
  - CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
  - Infrastructure as Code (Terraform, Ansible)
  - Monitoring tools (Prometheus, Grafana, ELK)
  - Scripting (Python, Bash, PowerShell)
- Call to action
- Your contact information

**Attachment:** Your resume (PDF)

## 🛠️ Customization

### Customize the Email Template

Edit the `create_email_body()` method in `email_sender.py` to personalize your message:

```python
def create_email_body(self, hr_name: str = "Hiring Manager") -> str:
    email_body = f"""Dear {hr_name},

    [Your customized message here]
    """
    return email_body
```

### Use Different Email Providers

For **Outlook/Hotmail**, update in `config.py`:
```python
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
```

For **Yahoo**, update in `config.py`:
```python
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
```

### Adjust Delay Between Emails

In `config.py`:
```python
DELAY_BETWEEN_EMAILS = 10  # Change to desired seconds
```

## 📁 File Structure

```
email/
├── email_sender_v2.py          # Main email sending class
├── config.py                # Configuration file (UPDATE THIS)
├── send_applications.py     # Simple runner script
└── README.md               # This file
```

## ⚠️ Important Notes

### Security
- **Never** commit `config.py` with your real credentials to version control
- Use App Passwords, not your regular email password
- Keep your resume file secure

### Email Limits
- Gmail: ~500 emails per day for regular accounts
- Add delays between emails (recommended: 5-10 seconds)
- Don't send to too many recipients at once

### Best Practices
- Personalize the email when possible (add HR name if known)
- Send during business hours for better visibility
- Keep your resume updated and professional
- Test with your own email first before sending to HRs

## 🐛 Troubleshooting

### "Authentication failed" error
- Make sure you're using an App Password, not your regular password
- Verify 2-Step Verification is enabled for Gmail
- Check that your email and password are correct in `config.py`

### "Resume file not found" error
- Check the file path in `config.py`
- Use raw string format: `r"c:\path\to\file.pdf"`
- Ensure the file exists at the specified location

### "Connection refused" error
- Check your internet connection
- Verify SMTP server and port are correct
- Your firewall might be blocking the connection

### Email goes to spam
- Add delays between emails
- Avoid sending too many emails at once
- Make sure your email content is professional
- Consider warming up your email account first

## 📝 Testing

Before sending to actual HR contacts, test the script:

1. Add your own email to `HR_EMAIL_LIST`
2. Run the script
3. Check if you receive the email correctly
4. Verify the resume attachment opens properly

## 🔄 Updates and Improvements

Feel free to enhance the script:
- Add HTML email templates
- Include your LinkedIn profile
- Add CC/BCC functionality
- Track email opens (requires third-party service)
- Add more personalization fields

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all configuration settings
3. Test with a single email first
4. Check Python version: `python --version`

## ⚖️ Legal Notice

- Only use this script for legitimate job applications
- Respect anti-spam laws and email service provider terms
- Don't send unsolicited emails in bulk
- Ensure you have permission to contact the recipients

## 🎯 Good Luck!

Best wishes with your DevOps Engineer job search! 🚀
