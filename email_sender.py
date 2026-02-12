import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import List
import time

class JobApplicationEmailer:
    def __init__(self, sender_email: str, sender_password: str, sender_name: str):
        """
        Initialize the email sender

        Args:
            sender_email: Your email address
            sender_password: Your email password or app-specific password
            sender_name: Your full name
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name

    def create_email_body(self, hr_name: str = "Hiring Manager") -> str:
        """
        Create the email body content

        Args:
            hr_name: Name of the HR person (if known)

        Returns:
            Email body as string
        """
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

    def send_email(self,
                   recipient_email: str,
                   resume_path: str,
                   hr_name: str = "Hiring Manager",
                   smtp_server: str = "smtp.gmail.com",
                   smtp_port: int = 587) -> bool:
        """
        Send email to a single recipient

        Args:
            recipient_email: HR email address
            resume_path: Path to your resume file
            hr_name: Name of the HR person
            smtp_server: SMTP server address
            smtp_port: SMTP port number

        Returns:
            True if successful, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = f"{self.sender_name} <{self.sender_email}>"
            message['To'] = recipient_email
            message['Subject'] = f"Application for DevOps Engineer Position - {self.sender_name}"

            # Add body
            body = self.create_email_body(hr_name)
            message.attach(MIMEText(body, 'plain'))

            # Attach resume
            if os.path.exists(resume_path):
                with open(resume_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())

                encoders.encode_base64(part)
                filename = os.path.basename(resume_path)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}'
                )
                message.attach(part)
            else:
                print(f"Warning: Resume file not found at {resume_path}")
                return False

            # Connect to server and send
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            print(f"✓ Email sent successfully to {recipient_email}")
            return True

        except Exception as e:
            print(f"✗ Failed to send email to {recipient_email}: {str(e)}")
            return False

    def send_bulk_emails(self,
                        hr_emails: List[str],
                        resume_path: str,
                        delay_seconds: int = 5,
                        smtp_server: str = "smtp.gmail.com",
                        smtp_port: int = 587):
        """
        Send emails to multiple HR contacts

        Args:
            hr_emails: List of HR email addresses
            resume_path: Path to your resume file
            delay_seconds: Delay between emails to avoid spam detection
            smtp_server: SMTP server address
            smtp_port: SMTP port number
        """
        successful = 0
        failed = 0

        print(f"\nStarting to send {len(hr_emails)} emails...")
        print("=" * 60)

        for i, email in enumerate(hr_emails, 1):
            print(f"\n[{i}/{len(hr_emails)}] Sending to: {email}")

            if self.send_email(email, resume_path, smtp_server=smtp_server, smtp_port=smtp_port):
                successful += 1
            else:
                failed += 1

            # Add delay between emails (except for the last one)
            if i < len(hr_emails):
                print(f"Waiting {delay_seconds} seconds before next email...")
                time.sleep(delay_seconds)

        print("\n" + "=" * 60)
        print(f"\nSummary:")
        print(f"✓ Successfully sent: {successful}")
        print(f"✗ Failed: {failed}")
        print(f"Total: {len(hr_emails)}")


def main():
    """
    Main function to run the email sender
    """
    print("=" * 60)
    print("DevOps Engineer Job Application Email Sender")
    print("=" * 60)

    # Configuration - UPDATE THESE VALUES
    YOUR_NAME = "Your Full Name"  # Update with your name
    YOUR_EMAIL = "your.email@gmail.com"  # Update with your email
    YOUR_PASSWORD = "your_app_password"  # Update with your app-specific password
    RESUME_PATH = r"c:\path\to\your\resume.pdf"  # Update with your resume path

    # SMTP Configuration (for Gmail)
    # For other email providers, update these:
    # Outlook: smtp.office365.com, port 587
    # Yahoo: smtp.mail.yahoo.com, port 587
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    # List of HR email addresses
    hr_email_list = [
        "hr1@company1.com",
        "hr2@company2.com",
        "recruiter@company3.com",
        # Add more email addresses here
    ]

    # Validate configuration
    if YOUR_EMAIL == "your.email@gmail.com" or YOUR_PASSWORD == "your_app_password":
        print("\n⚠ ERROR: Please update your email credentials in the script!")
        print("Update YOUR_EMAIL and YOUR_PASSWORD variables in the main() function")
        return

    if not os.path.exists(RESUME_PATH):
        print(f"\n⚠ ERROR: Resume file not found at: {RESUME_PATH}")
        print("Please update the RESUME_PATH variable with the correct path to your resume")
        return

    if not hr_email_list or hr_email_list[0] == "hr1@company1.com":
        print("\n⚠ WARNING: Please update the hr_email_list with actual HR email addresses")
        response = input("Do you want to continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            return

    # Create emailer instance
    emailer = JobApplicationEmailer(YOUR_EMAIL, YOUR_PASSWORD, YOUR_NAME)

    # Send emails
    emailer.send_bulk_emails(
        hr_emails=hr_email_list,
        resume_path=RESUME_PATH,
        delay_seconds=5,  # Wait 5 seconds between emails
        smtp_server=SMTP_SERVER,
        smtp_port=SMTP_PORT
    )


if __name__ == "__main__":
    main()
