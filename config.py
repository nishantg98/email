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
RESUME_PATH = os.environ.get("RESUME_PATH", os.path.join(os.path.dirname(__file__), "Nishant_Gupta_Resume.pdf"))

# Application Content — customize these for the role you're applying to.
# TARGET_ROLE and EXPERIENCE_SUMMARY drive the subject line and intro sentence.
TARGET_ROLE = os.environ.get("TARGET_ROLE", "DevOps Engineer")
EXPERIENCE_SUMMARY = os.environ.get(
    "EXPERIENCE_SUMMARY",
    "4+ years of proven track record in cloud infrastructure, automation, and CI/CD pipelines"
)

# Skill bullets shown in "Key Highlights of My Profile". Each string can include
# tools/technologies in parentheses (e.g. "Proficient in X (Tool A, Tool B)") —
# those are automatically used as keywords when tailoring to a pasted job description.
SKILL_HIGHLIGHTS = [
    "Expertise in cloud platforms (AWS, Azure, GCP)",
    "Proficient in containerization technologies (Docker, Kubernetes)",
    "Strong experience with CI/CD tools (Jenkins, GitLab CI, GitHub Actions)",
    "Infrastructure as Code (Terraform, Ansible, CloudFormation)",
    "Monitoring and logging solutions (Prometheus, Grafana, ELK Stack)",
    "Scripting languages (Python, Bash, PowerShell)",
    "Version control systems (Git, GitHub, GitLab)",
]

# Optional extra details listed at the end of the email (e.g. experience, CTC,
# notice period, location). Leave the dict empty ({}) to omit this section entirely —
# not everyone wants to share salary/notice-period details in a cold email.
APPLICATION_DETAILS = {
    "Total Experience": "4.6 years",
    "Rel Experience": "4.6 years",
    "Current CTC": "14.7 lpa",
    "Expected CTC": "20 to 22 lpa (negotiable)",
    "Notice Period": "30 days (negotiable)",
    "Current Location": "Delhi NCR",
    "Open to Relocate": "Yes",
}

# SMTP Server Configuration
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

# Email Settings
DELAY_BETWEEN_EMAILS = int(os.environ.get("DELAY_BETWEEN_EMAILS", "5"))

# HR Email List (kept for backward compatibility with send_applications.py)
HR_EMAIL_LIST = [
    "",
    # Add more email addresses below
]
