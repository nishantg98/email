"""
Send job applications using SendGrid API (works on corporate networks)
This version bypasses SMTP firewall issues by using HTTPS
"""
from email_sender_sendgrid import JobApplicationEmailerSendGrid, check_sendgrid_setup
import config
import os

def main():
    print("=" * 70)
    print(" DevOps Job Application Sender (SendGrid)")
    print("=" * 70)

    # Check SendGrid is installed
    if not check_sendgrid_setup():
        print("\nInstall SendGrid first:")
        print("  pip install sendgrid")
        print("\nSee SENDGRID_SETUP.md for complete setup instructions.")
        return

    # Validate configuration
    errors = []

    if not hasattr(config, 'SENDGRID_API_KEY'):
        errors.append("- Add SENDGRID_API_KEY to config.py")

    if hasattr(config, 'SENDGRID_API_KEY') and (
        config.SENDGRID_API_KEY == "your_api_key_here" or
        not config.SENDGRID_API_KEY.startswith("SG.")
    ):
        errors.append("- Update SENDGRID_API_KEY with your actual API key")

    if config.YOUR_EMAIL == "your.email@gmail.com":
        errors.append("- Update YOUR_EMAIL in config.py")

    if not os.path.exists(config.RESUME_PATH):
        errors.append(f"- Resume file not found: {config.RESUME_PATH}")

    if not config.HR_EMAIL_LIST or config.HR_EMAIL_LIST[0] == "hr@company1.com":
        errors.append("- Update HR_EMAIL_LIST with actual HR emails")

    if errors:
        print("\n[ERROR] Configuration issues found:\n")
        for error in errors:
            print(error)
        print("\nFix these in config.py, then run again.")
        print("See SENDGRID_SETUP.md for SendGrid setup help.")
        return

    # Display configuration summary
    print(f"\nConfiguration:")
    print(f"  Sender: {config.YOUR_NAME} <{config.YOUR_EMAIL}>")
    print(f"  Resume: {config.RESUME_PATH}")
    print(f"  Method: SendGrid API (HTTPS - bypasses firewall)")
    print(f"  Recipients: {len(config.HR_EMAIL_LIST)}")
    print(f"\nRecipients:")
    for i, email in enumerate(config.HR_EMAIL_LIST, 1):
        print(f"  {i}. {email}")

    # Confirm
    print("\n" + "=" * 70)
    print("Ready to send job applications via SendGrid!")
    print("This works on corporate networks (uses HTTPS, not SMTP).")
    print("=" * 70)

    # Note: In non-interactive mode, auto-proceed
    # For interactive, uncomment the lines below:
    # response = input("\nProceed? (yes/no): ")
    # if response.lower() not in ['yes', 'y']:
    #     print("Cancelled.")
    #     return

    # Create emailer and send
    try:
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
        print("\nNote: SendGrid free tier = 100 emails/day")

    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
        print("\nCheck SENDGRID_SETUP.md for troubleshooting.")

if __name__ == "__main__":
    main()
