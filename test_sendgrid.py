"""
Quick test for SendGrid email sending
"""
import os

try:
    from email_sender_sendgrid import JobApplicationEmailerSendGrid, SENDGRID_AVAILABLE
except ImportError:
    SENDGRID_AVAILABLE = False

import config

def main():
    print("=" * 70)
    print(" SendGrid Quick Test")
    print("=" * 70)

    # Check if SendGrid is installed
    if not SENDGRID_AVAILABLE:
        print("\n[ERROR] SendGrid not installed!")
        print("\nInstall it with:")
        print("  pip install sendgrid")
        print("\nThen run this test again.")
        return

    # Check config
    if not hasattr(config, 'SENDGRID_API_KEY'):
        print("\n[ERROR] SENDGRID_API_KEY not found in config.py")
        print("\nAdd this to config.py:")
        print('  SENDGRID_API_KEY = "SG.your_api_key_here"')
        print("\nSee SENDGRID_SETUP.md for detailed instructions.")
        return

    if config.SENDGRID_API_KEY == "your_api_key_here" or not config.SENDGRID_API_KEY.startswith("SG."):
        print("\n[ERROR] Invalid SENDGRID_API_KEY in config.py")
        print("\nYour API key should:")
        print("  - Start with 'SG.'")
        print("  - Be about 69 characters long")
        print("\nSee SENDGRID_SETUP.md for setup instructions.")
        return

    if not config.HR_EMAIL_LIST:
        print("\n[ERROR] HR_EMAIL_LIST is empty in config.py")
        return

    if not os.path.exists(config.RESUME_PATH):
        print(f"\n[ERROR] Resume not found: {config.RESUME_PATH}")
        return

    # All checks passed
    test_email = config.HR_EMAIL_LIST[0]

    print(f"\nConfiguration:")
    print(f"  From: {config.YOUR_NAME} <{config.YOUR_EMAIL}>")
    print(f"  To: {test_email}")
    print(f"  Resume: {os.path.basename(config.RESUME_PATH)}")
    print(f"  Method: SendGrid API (HTTPS)")

    print("\n" + "=" * 70)
    print("Sending test email via SendGrid...")
    print("=" * 70)

    # Create emailer and send
    try:
        emailer = JobApplicationEmailerSendGrid(
            sendgrid_api_key=config.SENDGRID_API_KEY,
            sender_email=config.YOUR_EMAIL,
            sender_name=config.YOUR_NAME
        )

        success = emailer.send_email(
            recipient_email=test_email,
            resume_path=config.RESUME_PATH,
            hr_name="Test Recipient"
        )

        print("=" * 70)

        if success:
            print("\n[SUCCESS] Test email sent via SendGrid!")
            print(f"\nCheck your inbox at {test_email}")
            print("\nVerify:")
            print("  1. Email received (check spam folder too)")
            print("  2. Resume attachment present")
            print("  3. Email looks professional")
            print("\nIf all good, update send_applications.py to use SendGrid!")
        else:
            print("\n[FAILED] Test failed. Check errors above.")

    except Exception as e:
        print("=" * 70)
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
        print("\nCommon issues:")
        print("  1. API key incorrect - check it starts with 'SG.'")
        print("  2. Sender email not verified in SendGrid")
        print("  3. SendGrid account suspended")
        print("\nSee SENDGRID_SETUP.md for help.")

if __name__ == "__main__":
    main()
