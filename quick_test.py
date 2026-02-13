"""
Quick non-interactive test - sends to the first email in HR_EMAIL_LIST
"""
from email_sender_v2 import JobApplicationEmailer
import config
import os

def main():
    print("=" * 70)
    print(" Quick Email Test (Non-Interactive)")
    print("=" * 70)

    # Validate basic configuration
    if config.YOUR_EMAIL == "your.email@gmail.com":
        print("\n[ERROR] Please update YOUR_EMAIL in config.py first!")
        return

    if config.YOUR_PASSWORD == "xxxx xxxx xxxx xxxx":
        print("\n[ERROR] Please update YOUR_PASSWORD in config.py first!")
        return

    if not os.path.exists(config.RESUME_PATH):
        print(f"\n[ERROR] Resume file not found: {config.RESUME_PATH}")
        return

    if not config.HR_EMAIL_LIST:
        print("\n[ERROR] HR_EMAIL_LIST is empty in config.py")
        return

    test_email = config.HR_EMAIL_LIST[0]

    print(f"\nConfiguration:")
    print(f"  From: {config.YOUR_NAME} <{config.YOUR_EMAIL}>")
    print(f"  To: {test_email}")
    print(f"  Resume: {os.path.basename(config.RESUME_PATH)}")
    print(f"  SMTP: {config.SMTP_SERVER}:{config.SMTP_PORT}")
    print(f"  Timeout: 60 seconds")

    # Create emailer
    emailer = JobApplicationEmailer(
        sender_email=config.YOUR_EMAIL,
        sender_password=config.YOUR_PASSWORD,
        sender_name=config.YOUR_NAME,
        sender_phone=config.YOUR_PHONE,
        sender_linkedin=config.YOUR_LINKEDIN,
        sender_website=config.YOUR_WEBSITE
    )

    # Send test email
    print("\nStarting test email send...")
    print("=" * 70)

    success = emailer.send_email(
        recipient_email=test_email,
        resume_path=config.RESUME_PATH,
        hr_name="Test Recipient",
        smtp_server=config.SMTP_SERVER,
        smtp_port=config.SMTP_PORT,
        timeout=60
    )

    print("=" * 70)

    if success:
        print("\n[SUCCESS] Test email sent successfully!")
        print(f"Check your inbox at {test_email}")
        print("\nVerify:")
        print("  1. Email received in inbox (check spam folder too)")
        print("  2. Resume attachment is present and opens correctly")
        print("  3. Email content looks professional")
        print("\nIf everything looks good, you can now run send_applications.py")
    else:
        print("\n[FAILED] Test email failed!")
        print("Check the error messages above for details.")

if __name__ == "__main__":
    main()
