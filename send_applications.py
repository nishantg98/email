"""
Simple script to send job application emails using configuration from config.py
Uses improved version with better timeout and error handling
"""
from email_sender_v2 import JobApplicationEmailer
import config
import os

def main():
    print("=" * 70)
    print(" DevOps Engineer Job Application Email Sender")
    print("=" * 70)

    # Validate configuration
    errors = []

    if config.YOUR_EMAIL == "your.email@gmail.com":
        errors.append("- Update YOUR_EMAIL in config.py")

    if config.YOUR_PASSWORD == "xxxx xxxx xxxx xxxx":
        errors.append("- Update YOUR_PASSWORD in config.py with your app password")

    if not os.path.exists(config.RESUME_PATH):
        errors.append(f"- Resume file not found: {config.RESUME_PATH}")

    if not config.HR_EMAIL_LIST or config.HR_EMAIL_LIST[0] == "hr@company1.com":
        errors.append("- Update HR_EMAIL_LIST in config.py with actual HR emails")

    if errors:
        print("\n⚠️  Configuration Errors Found:\n")
        for error in errors:
            print(error)
        print("\nPlease fix these errors in config.py and try again.")
        return

    # Display configuration summary
    print(f"\nConfiguration:")
    print(f"  Sender: {config.YOUR_NAME} <{config.YOUR_EMAIL}>")
    print(f"  Resume: {config.RESUME_PATH}")
    print(f"  SMTP Server: {config.SMTP_SERVER}:{config.SMTP_PORT}")
    print(f"  Number of recipients: {len(config.HR_EMAIL_LIST)}")
    print(f"\nRecipients:")
    for i, email in enumerate(config.HR_EMAIL_LIST, 1):
        print(f"  {i}. {email}")

    # Confirm before sending
    print("\n" + "=" * 70)
    response = input("\nDo you want to send emails to all recipients? (yes/no): ")

    if response.lower() not in ['yes', 'y']:
        print("Operation cancelled.")
        return

    # Create emailer and send
    emailer = JobApplicationEmailer(
        sender_email=config.YOUR_EMAIL,
        sender_password=config.YOUR_PASSWORD,
        sender_name=config.YOUR_NAME,
        sender_phone=config.YOUR_PHONE,
        sender_linkedin=config.YOUR_LINKEDIN,
        sender_website=config.YOUR_WEBSITE
    )

    emailer.send_bulk_emails(
        hr_emails=config.HR_EMAIL_LIST,
        resume_path=config.RESUME_PATH,
        delay_seconds=config.DELAY_BETWEEN_EMAILS,
        smtp_server=config.SMTP_SERVER,
        smtp_port=config.SMTP_PORT,
        timeout=60
    )

    print("\n✅ Process completed!")

if __name__ == "__main__":
    main()
