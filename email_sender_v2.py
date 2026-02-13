import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from typing import List
import time
import socket

class JobApplicationEmailer:
    def __init__(self, sender_email: str, sender_password: str, sender_name: str, sender_phone: str = "", sender_linkedin: str = "", sender_website: str = ""):
        """
        Initialize the email sender

        Args:
            sender_email: Your email address
            sender_password: Your email password or app-specific password
            sender_name: Your full name
            sender_phone: Your phone number (optional)
            sender_linkedin: Your LinkedIn profile URL (optional)
            sender_website: Your portfolio/website URL (optional)
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name
        self.sender_phone = sender_phone
        self.sender_linkedin = sender_linkedin
        self.sender_website = sender_website

    def create_email_body(self, hr_name: str = "Hiring Manager") -> str:
        """
        Create the email body content

        Args:
            hr_name: Name of the HR person (if known)

        Returns:
            Email body as string
        """
        # Build contact information section
        contact_info = f"{self.sender_email}"
        if self.sender_phone:
            contact_info += f"\nPhone: {self.sender_phone}"
        if self.sender_linkedin:
            contact_info += f"\nLinkedIn: {self.sender_linkedin}"
        if self.sender_website:
            contact_info += f"\nPortfolio: {self.sender_website}"
        
        email_body = f"""Dear {hr_name},

I hope this email finds you well.

I am writing to express my strong interest in DevOps SRE Engineer opportunities within your organization. With 4+ years of proven track record in cloud infrastructure, automation, and CI/CD pipelines, I am confident that my skills align well with your team's needs.

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
{contact_info}"""

        return email_body

    def send_email(self,
                   recipient_email: str,
                   resume_path: str,
                   hr_name: str = "Hiring Manager",
                   smtp_server: str = "smtp.gmail.com",
                   smtp_port: int = 587,
                   timeout: int = 60) -> bool:
        """
        Send email to a single recipient with improved timeout handling

        Args:
            recipient_email: HR email address
            resume_path: Path to your resume file
            hr_name: Name of the HR person
            smtp_server: SMTP server address
            smtp_port: SMTP port number
            timeout: Connection timeout in seconds

        Returns:
            True if successful, False otherwise
        """
        # Set default socket timeout
        socket.setdefaulttimeout(timeout)

        try:
            print(f"  [1/5] Creating email message...")
            # Create message
            message = MIMEMultipart()
            message['From'] = f"{self.sender_name} <{self.sender_email}>"
            message['To'] = recipient_email
            message['Subject'] = f"Application for DevOps Engineer Position - {self.sender_name}"

            # Add body
            body = self.create_email_body(hr_name)
            message.attach(MIMEText(body, 'plain'))

            print(f"  [2/5] Attaching resume...")
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
                print(f"  [ERROR] Resume file not found at {resume_path}")
                return False

            print(f"  [3/5] Connecting to {smtp_server}:{smtp_port}...")
            # Connect to server with increased timeout
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=timeout)
            server.set_debuglevel(0)  # Set to 1 for debug output

            print(f"  [4/5] Starting TLS encryption...")
            server.starttls()

            print(f"  [5/5] Logging in and sending...")
            server.login(self.sender_email, self.sender_password)
            server.send_message(message)
            server.quit()

            print(f"[SUCCESS] Email sent to {recipient_email}")
            return True

        except smtplib.SMTPAuthenticationError as e:
            print(f"[FAILED] Authentication error for {recipient_email}")
            print(f"  Error: {str(e)}")
            print(f"  Check your App Password in config.py")
            return False

        except smtplib.SMTPException as e:
            print(f"[FAILED] SMTP error for {recipient_email}: {str(e)}")
            return False

        except socket.timeout:
            print(f"[FAILED] Connection timeout for {recipient_email}")
            print(f"  The server took too long to respond (>{timeout}s)")
            print(f"  Try again or increase timeout value")
            return False

        except socket.error as e:
            print(f"[FAILED] Socket error for {recipient_email}: {str(e)}")
            return False

        except Exception as e:
            print(f"[FAILED] Unexpected error for {recipient_email}")
            print(f"  Error type: {type(e).__name__}")
            print(f"  Error: {str(e)}")
            return False

        finally:
            # Reset socket timeout
            socket.setdefaulttimeout(None)

    def send_bulk_emails(self,
                        hr_emails: List[str],
                        resume_path: str,
                        delay_seconds: int = 5,
                        smtp_server: str = "smtp.gmail.com",
                        smtp_port: int = 587,
                        timeout: int = 60):
        """
        Send emails to multiple HR contacts

        Args:
            hr_emails: List of HR email addresses
            resume_path: Path to your resume file
            delay_seconds: Delay between emails to avoid spam detection
            smtp_server: SMTP server address
            smtp_port: SMTP port number
            timeout: Connection timeout in seconds
        """
        successful = 0
        failed = 0

        print(f"\nStarting to send {len(hr_emails)} emails...")
        print("=" * 60)

        for i, email in enumerate(hr_emails, 1):
            print(f"\n[{i}/{len(hr_emails)}] Sending to: {email}")

            if self.send_email(
                email,
                resume_path,
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                timeout=timeout
            ):
                successful += 1
            else:
                failed += 1

            # Add delay between emails (except for the last one)
            if i < len(hr_emails):
                print(f"Waiting {delay_seconds} seconds before next email...")
                time.sleep(delay_seconds)

        print("\n" + "=" * 60)
        print(f"\nSummary:")
        print(f"[SUCCESS] Successfully sent: {successful}")
        print(f"[FAILED] Failed: {failed}")
        print(f"Total: {len(hr_emails)}")


def main():
    """
    Main function to run the email sender
    """
    print("=" * 60)
    print("DevOps Engineer Job Application Email Sender v2")
    print("=" * 60)

    # Configuration - UPDATE THESE VALUES
    YOUR_NAME = "Your Full Name"
    YOUR_EMAIL = "your.email@gmail.com"
    YOUR_PASSWORD = "your_app_password"
    RESUME_PATH = r"c:\path\to\your\resume.pdf"

    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    hr_email_list = [
        "hr1@company1.com",
        # Add more email addresses here
    ]

    # Validate configuration
    if YOUR_EMAIL == "your.email@gmail.com" or YOUR_PASSWORD == "your_app_password":
        print("\n[ERROR] Please update your email credentials in the script!")
        print("Update YOUR_EMAIL and YOUR_PASSWORD variables in the main() function")
        return

    if not os.path.exists(RESUME_PATH):
        print(f"\n[ERROR] Resume file not found at: {RESUME_PATH}")
        print("Please update the RESUME_PATH variable with the correct path to your resume")
        return

    if not hr_email_list or hr_email_list[0] == "hr1@company1.com":
        print("\n[WARNING] Please update the hr_email_list with actual HR email addresses")
        response = input("Do you want to continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            return

    # Create emailer instance
    emailer = JobApplicationEmailer(YOUR_EMAIL, YOUR_PASSWORD, YOUR_NAME)

    # Send emails with 60 second timeout
    emailer.send_bulk_emails(
        hr_emails=hr_email_list,
        resume_path=RESUME_PATH,
        delay_seconds=5,
        smtp_server=SMTP_SERVER,
        smtp_port=SMTP_PORT,
        timeout=60
    )


if __name__ == "__main__":
    main()
