"""
Email sender using SendGrid API - Works on corporate networks!
SendGrid uses HTTPS (port 443) instead of SMTP, so firewalls don't block it.

Setup:
1. Sign up at https://sendgrid.com (free tier: 100 emails/day)
2. Create an API key
3. Install: pip install sendgrid
4. Add API key to config.py
"""
import os
from typing import List
import time
import base64

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import (
        Mail, Attachment, FileContent, FileName, FileType, Disposition
    )
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False


class JobApplicationEmailerSendGrid:
    def __init__(self, sendgrid_api_key: str, sender_email: str, sender_name: str):
        """
        Initialize SendGrid email sender

        Args:
            sendgrid_api_key: Your SendGrid API key
            sender_email: Your email address (must be verified in SendGrid)
            sender_name: Your full name
        """
        if not SENDGRID_AVAILABLE:
            raise ImportError(
                "SendGrid not installed. Run: pip install sendgrid"
            )

        self.api_key = sendgrid_api_key
        self.sender_email = sender_email
        self.sender_name = sender_name
        self.client = SendGridAPIClient(self.api_key)

    def create_email_body(self, hr_name: str = "Hiring Manager") -> str:
        """Create email body content"""
        email_body = f"""Dear {hr_name},

I hope this email finds you well.

I am writing to express my strong interest in DevOps Engineer opportunities within your organization. With a proven track record in cloud infrastructure, automation, and CI/CD pipelines, I am confident that my skills align well with your team's needs.

Key Highlights of My Profile:
• Expertise in cloud platforms (AWS, Azure, GCP)
• Proficient in containerization technologies (Docker, Kubernetes)
• Strong experience with CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
• Infrastructure as Code (Terraform, Ansible, CloudFormation)
• Monitoring and logging solutions (Prometheus, Grafana, ELK Stack)
• Scripting languages (Python, Bash, PowerShell)
• Version control systems (Git, GitHub, GitLab)

I have attached my resume for your review, which provides detailed information about my professional experience, technical skills, and accomplishments.

I would welcome the opportunity to discuss how my background and skills can contribute to your team's success. I am available for an interview at your convenience and can be reached at {self.sender_email}.

Thank you for considering my application. I look forward to the possibility of working with your organization.

Best regards,
{self.sender_name}
{self.sender_email}"""

        return email_body

    def send_email(self, recipient_email: str, resume_path: str,
                   hr_name: str = "Hiring Manager") -> bool:
        """
        Send email using SendGrid API

        Args:
            recipient_email: HR email address
            resume_path: Path to your resume file
            hr_name: Name of the HR person

        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"  [1/4] Creating email message...")

            # Create email
            message = Mail(
                from_email=f"{self.sender_name} <{self.sender_email}>",
                to_emails=recipient_email,
                subject=f"Application for DevOps Engineer Position - {self.sender_name}",
                plain_text_content=self.create_email_body(hr_name)
            )

            print(f"  [2/4] Reading resume file...")
            # Attach resume
            if os.path.exists(resume_path):
                with open(resume_path, 'rb') as f:
                    resume_data = f.read()

                encoded_file = base64.b64encode(resume_data).decode()

                attached_file = Attachment(
                    FileContent(encoded_file),
                    FileName(os.path.basename(resume_path)),
                    FileType('application/pdf'),
                    Disposition('attachment')
                )
                message.attachment = attached_file
            else:
                print(f"  [ERROR] Resume file not found: {resume_path}")
                return False

            print(f"  [3/4] Sending via SendGrid API...")
            response = self.client.send(message)

            print(f"  [4/4] Checking response...")
            if response.status_code in [200, 201, 202]:
                print(f"[SUCCESS] Email sent to {recipient_email}")
                print(f"  Status: {response.status_code}")
                return True
            else:
                print(f"[FAILED] Unexpected status code: {response.status_code}")
                return False

        except Exception as e:
            print(f"[FAILED] Error sending to {recipient_email}")
            print(f"  Error: {type(e).__name__}: {str(e)}")
            return False

    def send_bulk_emails(self, hr_emails: List[str], resume_path: str,
                        delay_seconds: int = 5):
        """
        Send emails to multiple HR contacts

        Args:
            hr_emails: List of HR email addresses
            resume_path: Path to your resume file
            delay_seconds: Delay between emails
        """
        successful = 0
        failed = 0

        print(f"\nStarting to send {len(hr_emails)} emails via SendGrid...")
        print("=" * 60)

        for i, email in enumerate(hr_emails, 1):
            print(f"\n[{i}/{len(hr_emails)}] Sending to: {email}")

            if self.send_email(email, resume_path):
                successful += 1
            else:
                failed += 1

            if i < len(hr_emails):
                print(f"Waiting {delay_seconds} seconds...")
                time.sleep(delay_seconds)

        print("\n" + "=" * 60)
        print(f"\nSummary:")
        print(f"[SUCCESS] Successfully sent: {successful}")
        print(f"[FAILED] Failed: {failed}")
        print(f"Total: {len(hr_emails)}")


def check_sendgrid_setup():
    """Check if SendGrid is properly set up"""
    if not SENDGRID_AVAILABLE:
        print("\n[ERROR] SendGrid package not installed!")
        print("\nTo install SendGrid:")
        print("  pip install sendgrid")
        print("\nOr if using Python 3:")
        print("  pip3 install sendgrid")
        return False
    return True


def main():
    """Main function"""
    print("=" * 70)
    print(" SendGrid Email Sender (Works on Corporate Networks!)")
    print("=" * 70)

    if not check_sendgrid_setup():
        return

    print("\nThis script uses SendGrid API instead of SMTP.")
    print("It works on corporate networks because it uses HTTPS (port 443).")
    print("\nSetup required:")
    print("  1. Sign up at https://sendgrid.com (free: 100 emails/day)")
    print("  2. Verify your sender email")
    print("  3. Create an API key")
    print("  4. Add SENDGRID_API_KEY to config.py")

    try:
        import config

        if not hasattr(config, 'SENDGRID_API_KEY'):
            print("\n[ERROR] SENDGRID_API_KEY not found in config.py")
            print("Add this line to config.py:")
            print('  SENDGRID_API_KEY = "your_api_key_here"')
            return

        if config.SENDGRID_API_KEY == "your_api_key_here":
            print("\n[ERROR] Please update SENDGRID_API_KEY in config.py")
            return

        emailer = JobApplicationEmailerSendGrid(
            sendgrid_api_key=config.SENDGRID_API_KEY,
            sender_email=config.YOUR_EMAIL,
            sender_name=config.YOUR_NAME
        )

        emailer.send_bulk_emails(
            hr_emails=config.HR_EMAIL_LIST,
            resume_path=config.RESUME_PATH,
            delay_seconds=config.DELAY_BETWEEN_EMAILS
        )

        print("\n[OK] Process completed!")

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")


if __name__ == "__main__":
    main()
