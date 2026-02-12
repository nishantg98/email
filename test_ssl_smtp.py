"""
Test different SMTP connection methods to find what works
"""
from email_sender_v2 import JobApplicationEmailer
import config
import os
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_smtp_method_1():
    """Test standard SMTP with STARTTLS (port 587)"""
    print("\n" + "=" * 70)
    print("Method 1: SMTP + STARTTLS (port 587)")
    print("=" * 70)

    try:
        socket.setdefaulttimeout(60)
        print("  [1/4] Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=60)

        print("  [2/4] Starting TLS...")
        server.starttls()

        print("  [3/4] Logging in...")
        server.login(config.YOUR_EMAIL, config.YOUR_PASSWORD)

        print("  [4/4] Creating test message...")
        msg = MIMEMultipart()
        msg['From'] = config.YOUR_EMAIL
        msg['To'] = config.HR_EMAIL_LIST[0]
        msg['Subject'] = "Test Email - Method 1"
        msg.attach(MIMEText("This is a test email using SMTP + STARTTLS", 'plain'))

        server.send_message(msg)
        server.quit()

        print("[SUCCESS] Method 1 worked!")
        return True

    except Exception as e:
        print(f"[FAILED] Method 1 failed: {type(e).__name__}: {str(e)}")
        return False
    finally:
        socket.setdefaulttimeout(None)

def test_smtp_method_2():
    """Test SMTP_SSL (port 465)"""
    print("\n" + "=" * 70)
    print("Method 2: SMTP_SSL (port 465)")
    print("=" * 70)

    try:
        socket.setdefaulttimeout(60)
        print("  [1/3] Connecting to smtp.gmail.com:465 with SSL...")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=60)

        print("  [2/3] Logging in...")
        server.login(config.YOUR_EMAIL, config.YOUR_PASSWORD)

        print("  [3/3] Creating test message...")
        msg = MIMEMultipart()
        msg['From'] = config.YOUR_EMAIL
        msg['To'] = config.HR_EMAIL_LIST[0]
        msg['Subject'] = "Test Email - Method 2"
        msg.attach(MIMEText("This is a test email using SMTP_SSL", 'plain'))

        server.send_message(msg)
        server.quit()

        print("[SUCCESS] Method 2 worked!")
        return True

    except Exception as e:
        print(f"[FAILED] Method 2 failed: {type(e).__name__}: {str(e)}")
        return False
    finally:
        socket.setdefaulttimeout(None)

def test_smtp_method_3():
    """Test SMTP with STARTTLS and custom SSL context (port 587)"""
    print("\n" + "=" * 70)
    print("Method 3: SMTP + STARTTLS with custom SSL context (port 587)")
    print("=" * 70)

    try:
        import ssl
        socket.setdefaulttimeout(60)

        print("  [1/4] Creating SSL context...")
        context = ssl.create_default_context()

        print("  [2/4] Connecting to smtp.gmail.com:587...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=60)

        print("  [3/4] Starting TLS with custom context...")
        server.starttls(context=context)

        print("  [4/4] Logging in...")
        server.login(config.YOUR_EMAIL, config.YOUR_PASSWORD)

        print("  [5/5] Creating test message...")
        msg = MIMEMultipart()
        msg['From'] = config.YOUR_EMAIL
        msg['To'] = config.HR_EMAIL_LIST[0]
        msg['Subject'] = "Test Email - Method 3"
        msg.attach(MIMEText("This is a test email using custom SSL context", 'plain'))

        server.send_message(msg)
        server.quit()

        print("[SUCCESS] Method 3 worked!")
        return True

    except Exception as e:
        print(f"[FAILED] Method 3 failed: {type(e).__name__}: {str(e)}")
        return False
    finally:
        socket.setdefaulttimeout(None)

def main():
    print("=" * 70)
    print(" SMTP Connection Method Tester")
    print("=" * 70)

    if not config.HR_EMAIL_LIST:
        print("\n[ERROR] HR_EMAIL_LIST is empty in config.py")
        return

    if config.YOUR_PASSWORD == "xxxx xxxx xxxx xxxx":
        print("\n[ERROR] Please update YOUR_PASSWORD in config.py")
        return

    print(f"\nTesting SMTP connections...")
    print(f"From: {config.YOUR_EMAIL}")
    print(f"To: {config.HR_EMAIL_LIST[0]}")
    print(f"\nWill try 3 different methods...\n")

    results = []

    # Test Method 1
    results.append(("Method 1 (SMTP + STARTTLS, port 587)", test_smtp_method_1()))

    # Test Method 2
    results.append(("Method 2 (SMTP_SSL, port 465)", test_smtp_method_2()))

    # Test Method 3
    results.append(("Method 3 (SMTP + custom SSL, port 587)", test_smtp_method_3()))

    # Summary
    print("\n" + "=" * 70)
    print(" Summary")
    print("=" * 70)

    working_methods = []
    for method, success in results:
        status = "[SUCCESS]" if success else "[FAILED]"
        print(f"{status} {method}")
        if success:
            working_methods.append(method)

    if working_methods:
        print(f"\n[OK] {len(working_methods)} method(s) worked!")
        print("\nRecommendation:")
        if "Method 2" in working_methods[0]:
            print("  Update config.py to use:")
            print("  SMTP_SERVER = 'smtp.gmail.com'")
            print("  SMTP_PORT = 465")
            print("\n  This uses SMTP_SSL (more reliable on your network)")
        else:
            print("  Your current configuration (port 587) should work")
        print("\nCheck your email inbox for test messages!")
    else:
        print("\n[ERROR] None of the methods worked!")
        print("\nPossible solutions:")
        print("  1. Check your App Password is correct")
        print("  2. Try from a different network (not corporate)")
        print("  3. Check if antivirus is blocking Python")
        print("  4. Temporarily disable VPN if running")

if __name__ == "__main__":
    main()
