"""
Test script to send a single email to yourself to verify everything works
Uses improved version with better timeout and error handling
"""
from email_sender_v2 import JobApplicationEmailer
import config
import os

def main():
    print("=" * 70)
    print(" Test Email Sender - Send to Yourself First!")
    print("=" * 70)

    # Validate basic configuration
    if config.YOUR_EMAIL == "your.email@gmail.com":
        print("\n⚠️  Please update YOUR_EMAIL in config.py first!")
        return

    if config.YOUR_PASSWORD == "xxxx xxxx xxxx xxxx":
        print("\n⚠️  Please update YOUR_PASSWORD in config.py first!")
        return

    if not os.path.exists(config.RESUME_PATH):
        print(f"\n⚠️  Resume file not found: {config.RESUME_PATH}")
        return

    test_email = input(f"\nEnter your email to send a test (or press Enter to use {config.YOUR_EMAIL}): ").strip()
    if not test_email:
        test_email = config.YOUR_EMAIL

    print(f"\nSending test email to: {test_email}")
    print(f"From: {config.YOUR_NAME} <{config.YOUR_EMAIL}>")
    print(f"Resume: {os.path.basename(config.RESUME_PATH)}")
    print(f"SMTP: {config.SMTP_SERVER}:{config.SMTP_PORT}")

    response = input("\nProceed with test? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Test cancelled.")
        return

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
    print("\nSending test email with 60 second timeout...")
    success = emailer.send_email(
        recipient_email=test_email,
        resume_path=config.RESUME_PATH,
        hr_name="Test Recipient",
        smtp_server=config.SMTP_SERVER,
        smtp_port=config.SMTP_PORT,
        timeout=60
    )

    if success:
        print("\n✅ Test email sent successfully!")
        print(f"Check your inbox at {test_email}")
        print("\nVerify:")
        print("  1. Email received in inbox (or spam folder)")
        print("  2. Resume attachment is present and opens correctly")
        print("  3. Email content looks professional")
        print("\nIf everything looks good, you can now run send_applications.py")
    else:
        print("\n❌ Test email failed!")
        print("Check the error message above and verify your configuration in config.py")

if __name__ == "__main__":
    main()
