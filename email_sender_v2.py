import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dataclasses import dataclass
import os
import re
from typing import List
import time
import socket

# Generic mailbox names that aren't a person's name, even though they sit
# before the @ (e.g. hr@company.com, careers@company.com)
_GENERIC_MAILBOX_NAMES = {
    "hr", "info", "careers", "career", "jobs", "job", "recruiting",
    "recruitment", "recruiter", "talent", "admin", "contact", "support",
    "noreply", "no-reply", "team", "hello", "apply", "applications",
    "resumes", "cv",
}


def extract_name_from_email(email: str) -> str:
    """Best-effort guess at a person's first name from an email's local part,
    e.g. "nishant.gupta@ukg.com" -> "Nishant". Returns "" for generic mailbox
    addresses (hr@, careers@, ...) where no real name can be inferred."""
    local_part = email.split('@', 1)[0]
    tokens = [t for t in re.split(r'[._\-+\d]+', local_part) if t]

    if not tokens:
        return ""

    candidate = tokens[0].lower()
    if candidate in _GENERIC_MAILBOX_NAMES or len(candidate) < 2:
        return ""

    return candidate.capitalize()

# PythonAnywhere sandboxes have no outbound IPv6 route, but smtp.gmail.com
# publishes AAAA records too. Forcing IPv4-only resolution avoids
# intermittent "[Errno 101] Network is unreachable" when DNS returns an
# IPv6 address for the SMTP host.
_original_getaddrinfo = socket.getaddrinfo


def _ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    return _original_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)


socket.getaddrinfo = _ipv4_only_getaddrinfo


@dataclass
class SendResult:
    """Outcome of a single send attempt. Truthy/falsy on `success` so
    existing `if emailer.send_email(...)` call sites keep working."""
    success: bool
    message: str = ""
    attempts: int = 1

    def __bool__(self):
        return self.success


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

    # (bullet text, short label for the highlight sentence, keywords to match in a JD)
    SKILL_CATEGORIES = [
        ("Expertise in cloud platforms (AWS, Azure, GCP)",
         "cloud infrastructure (AWS/Azure/GCP)",
         ["aws", "amazon web services", "azure", "gcp", "google cloud", "cloud platform", "cloud infrastructure"]),
        ("Proficient in containerization technologies (Docker, Kubernetes)",
         "containerization (Docker/Kubernetes)",
         ["docker", "kubernetes", "k8s", "container"]),
        ("Strong experience with CI/CD tools (Jenkins, GitLab CI, GitHub Actions)",
         "CI/CD pipelines",
         ["ci/cd", "continuous integration", "continuous deployment", "continuous delivery",
          "jenkins", "gitlab ci", "github actions", "circleci", "travis"]),
        ("Infrastructure as Code (Terraform, Ansible, CloudFormation)",
         "Infrastructure as Code",
         ["terraform", "ansible", "cloudformation", "infrastructure as code", "iac", "pulumi"]),
        ("Monitoring and logging solutions (Prometheus, Grafana, ELK Stack)",
         "monitoring and observability",
         ["prometheus", "grafana", "elk", "elasticsearch", "logging", "monitoring", "observability",
          "datadog", "splunk", "new relic"]),
        ("Scripting languages (Python, Bash, PowerShell)",
         "scripting and automation",
         ["python", "bash", "powershell", "shell scripting", "scripting"]),
        ("Version control systems (Git, GitHub, GitLab)",
         "version control",
         ["git", "github", "gitlab", "bitbucket", "version control"]),
    ]

    def _tailor_to_jd(self, jd_text: str):
        """Reorder skill bullets to surface JD-matched ones first, and build a
        one-line callout. Pure keyword matching — no AI, no invented content."""
        jd_lower = jd_text.lower()
        matched, unmatched, matched_labels = [], [], []

        for bullet, label, keywords in self.SKILL_CATEGORIES:
            if any(keyword in jd_lower for keyword in keywords):
                matched.append(bullet)
                matched_labels.append(label)
            else:
                unmatched.append(bullet)

        bullets = matched + unmatched

        highlight_sentence = ""
        if matched_labels:
            shown = matched_labels[:3]
            if len(shown) == 1:
                joined = shown[0]
            elif len(shown) == 2:
                joined = f"{shown[0]} and {shown[1]}"
            else:
                joined = f"{', '.join(shown[:-1])}, and {shown[-1]}"
            highlight_sentence = f"\n\nYour job description calls out {joined}, which are core parts of my day-to-day DevOps work."

        return bullets, highlight_sentence

    def create_email_body(self, hr_name: str = "Hiring Manager", jd_text: str = "", company: str = "") -> str:
        """
        Create the email body content

        Args:
            hr_name: Name of the HR person (if known)
            jd_text: Optional job description text used to reorder skill bullets
                     and add a one-line callout for matched keywords
            company: Optional company name, used in place of "your organization"

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

        if jd_text.strip():
            bullets, highlight_sentence = self._tailor_to_jd(jd_text)
        else:
            bullets = [b for b, _, _ in self.SKILL_CATEGORIES]
            highlight_sentence = ""

        bullet_block = "\n".join(f"• {b}" for b in bullets)
        org_name = company.strip() or "your organization"

        email_body = f"""Dear {hr_name},

I hope this email finds you well.

I am writing to express my strong interest in DevOps SRE Engineer opportunities within {org_name}. With 4+ years of proven track record in cloud infrastructure, automation, and CI/CD pipelines, I am confident that my skills align well with your team's needs.{highlight_sentence}

Key Highlights of My Profile:
{bullet_block}

These are my current details:
• Total Experience: 4.6 years
• Rel Experience: 4.6 years
• Current CTC: 14.7 lpa
• Expected CTC: 20 to 22lpa (negotiable)
• Notice Period:  30 days (negotiable)
• Current Location: Delhi NCR
• Open to Relocate: Yes

I have attached my resume for your review, which provides detailed information about my professional experience, technical skills, and accomplishments.

I would welcome the opportunity to discuss how my background and skills can contribute to your team's success. I am available for an interview at your convenience and can be reached at {self.sender_email}.

Thank you for considering my application. I look forward to the possibility of working with {org_name}.

Best regards,
{self.sender_name}
{contact_info}"""

        return email_body

    def send_email(self,
                   recipient_email: str,
                   resume_path: str,
                   hr_name: str = "Hiring Manager",
                   jd_text: str = "",
                   company: str = "",
                   smtp_server: str = "smtp.gmail.com",
                   smtp_port: int = 587,
                   timeout: int = 60,
                   max_retries: int = 3,
                   retry_delay: int = 5) -> SendResult:
        """
        Send email to a single recipient using Gmail SMTP

        Args:
            recipient_email: HR email address
            resume_path: Path to your resume file
            hr_name: Name of the HR person
            jd_text: Optional job description text to tailor the cover letter bullets
            company: Optional company name, used in place of "your organization"
            smtp_server: SMTP server address
            smtp_port: SMTP port number
            timeout: Connection timeout in seconds
            max_retries: Number of attempts for transient network/connection errors
            retry_delay: Seconds to wait between retries

        Returns:
            SendResult with a success flag, a human-readable reason, and the attempt count
        """
        print(f"  [1/5] Creating email message...")
        # Create message
        message = MIMEMultipart()
        message['From'] = f"{self.sender_name} <{self.sender_email}>"
        message['To'] = recipient_email
        message['Subject'] = f"Application for DevOps Engineer Position - {self.sender_name}"

        # Add body
        body = self.create_email_body(hr_name, jd_text, company)
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
            return SendResult(False, f"Resume file not found: {resume_path}")

        for attempt in range(1, max_retries + 1):
            try:
                print(f"  [3/5] Connecting to {smtp_server}:{smtp_port}... (attempt {attempt}/{max_retries})")
                server = smtplib.SMTP(smtp_server, smtp_port, timeout=timeout)
                server.set_debuglevel(0)

                print(f"  [4/5] Starting TLS encryption...")
                server.starttls()

                print(f"  [5/5] Logging in and sending...")
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                server.quit()

                print(f"[SUCCESS] Email sent to {recipient_email}")
                suffix = f" (succeeded on attempt {attempt}/{max_retries})" if attempt > 1 else ""
                return SendResult(True, f"Email sent successfully{suffix}.", attempt)

            except smtplib.SMTPAuthenticationError as e:
                # Bad credentials won't fix themselves on retry
                print(f"[FAILED] Authentication error for {recipient_email}")
                print(f"  Error: {str(e)}")
                print(f"  Check your App Password in config.py")
                return SendResult(False, "Gmail rejected the sender login — check the App Password in config.py.", attempt)

            except smtplib.SMTPRecipientsRefused as e:
                print(f"[FAILED] Recipient refused for {recipient_email}: {str(e)}")
                return SendResult(False, "The recipient address was rejected by the mail server.", attempt)

            except (socket.timeout, socket.error, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError) as e:
                # Transient connection issues (e.g. brief network unreachability) are worth retrying
                print(f"[RETRY] Connection issue for {recipient_email} on attempt {attempt}/{max_retries}: {str(e)}")
                if attempt == max_retries:
                    print(f"[FAILED] Giving up on {recipient_email} after {max_retries} attempts")
                    return SendResult(False, f"Connection issue after {max_retries} attempts: {str(e)}", attempt)
                time.sleep(retry_delay)

            except smtplib.SMTPException as e:
                print(f"[FAILED] SMTP error for {recipient_email}: {str(e)}")
                return SendResult(False, f"SMTP error: {str(e)}", attempt)

            except Exception as e:
                print(f"[FAILED] Unexpected error for {recipient_email}")
                print(f"  Error type: {type(e).__name__}")
                print(f"  Error: {str(e)}")
                return SendResult(False, f"Unexpected error: {str(e)}", attempt)

        return SendResult(False, "Failed to send after retries.", max_retries)

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
