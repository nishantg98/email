# Email Configuration File
# Reads from environment variables when deployed, falls back to local values for development
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Your Personal Information
YOUR_NAME = os.environ.get("YOUR_NAME", "Nishant Gupta")
YOUR_EMAIL = os.environ.get("YOUR_EMAIL", "nishantg2798@gmail.com")
YOUR_PHONE = os.environ.get("YOUR_PHONE", "+918510094400")
YOUR_LINKEDIN = os.environ.get("YOUR_LINKEDIN", "https://www.linkedin.com/in/nishantgupta27/")
YOUR_WEBSITE = os.environ.get("YOUR_WEBSITE", "https://nishantg98.github.io/portfolio/")

# Email Credentials
# For Gmail: Set YOUR_PASSWORD as an environment variable (App Password)
# For SendGrid: Set SENDGRID_API_KEY as an environment variable
# Locally, set them in .env or environment variable
# NEVER commit actual passwords to the repository
YOUR_PASSWORD = os.environ.get("YOUR_PASSWORD", "")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "")

# Email Service: 'sendgrid' (recommended for Render) or 'gmail'
# Render: Use 'sendgrid' 
# Local dev: Use 'gmail' (requires Gmail App Password)
EMAIL_SERVICE = os.environ.get("EMAIL_SERVICE", "sendgrid" if SENDGRID_API_KEY else "gmail")

# Resume Path
RESUME_PATH = os.environ.get("RESUME_PATH", os.path.join(os.path.dirname(__file__), "Nishant-DevOps-Resume.pdf"))

# SMTP Server Configuration
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

# Email Settings
DELAY_BETWEEN_EMAILS = int(os.environ.get("DELAY_BETWEEN_EMAILS", "5"))

# HR Email List (kept for backward compatibility with send_applications.py)
HR_EMAIL_LIST = [
    "nishant203669@gmail.com",
    # Add more email addresses below
]
