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
# Gmail App Password required (16-character password from Google Account)
# Get it from: https://myaccount.google.com/apppasswords
YOUR_PASSWORD = os.environ.get("YOUR_PASSWORD", "")

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
