"""
Network troubleshooting script to diagnose SMTP connection issues
"""
import socket
import ssl

def test_smtp_connection(server, port):
    """Test if we can connect to SMTP server"""
    print(f"\nTesting connection to {server}:{port}...")
    try:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        # Try to connect
        result = sock.connect_ex((server, port))

        if result == 0:
            print(f"[SUCCESS] Connected to {server}:{port}")
            sock.close()
            return True
        else:
            print(f"[FAILED] Cannot connect to {server}:{port}")
            print(f"  Error code: {result}")
            sock.close()
            return False
    except Exception as e:
        print(f"[FAILED] Connection failed: {str(e)}")
        return False

def test_ssl_smtp_connection(server, port):
    """Test SSL/TLS SMTP connection"""
    print(f"\nTesting SSL/TLS connection to {server}:{port}...")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((server, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=server):
                print(f"[SUCCESS] SSL/TLS connection successful to {server}:{port}")
                return True
    except Exception as e:
        print(f"[FAILED] SSL/TLS connection failed: {str(e)}")
        return False

def main():
    print("=" * 70)
    print(" SMTP Network Connectivity Diagnostic Tool")
    print("=" * 70)

    print("\nThis tool will test connectivity to various SMTP servers and ports.")
    print("This helps identify if your network is blocking email connections.\n")

    # Test Gmail SMTP servers
    print("\n" + "=" * 70)
    print("Testing Gmail SMTP Servers")
    print("=" * 70)

    gmail_servers = [
        ("smtp.gmail.com", 587, "TLS (recommended)"),
        ("smtp.gmail.com", 465, "SSL"),
        ("smtp.gmail.com", 25, "Standard (often blocked)"),
    ]

    gmail_works = False
    for server, port, description in gmail_servers:
        print(f"\n{description}:")
        if test_smtp_connection(server, port):
            gmail_works = True
            if port == 465:
                test_ssl_smtp_connection(server, port)

    # Test alternative SMTP servers
    print("\n" + "=" * 70)
    print("Testing Alternative SMTP Servers")
    print("=" * 70)

    alternative_servers = [
        ("smtp.office365.com", 587, "Outlook/Office365"),
        ("smtp.mail.yahoo.com", 587, "Yahoo"),
    ]

    for server, port, description in alternative_servers:
        print(f"\n{description}:")
        test_smtp_connection(server, port)

    # Test general internet connectivity
    print("\n" + "=" * 70)
    print("Testing General Internet Connectivity")
    print("=" * 70)

    print("\nHTTP/HTTPS (port 80/443):")
    test_smtp_connection("www.google.com", 80)
    test_smtp_connection("www.google.com", 443)

    # Summary and recommendations
    print("\n" + "=" * 70)
    print("Summary & Recommendations")
    print("=" * 70)

    if not gmail_works:
        print("\nWARNING:  ISSUE DETECTED: Cannot connect to Gmail SMTP servers")
        print("\nPossible causes:")
        print("  1. Corporate firewall blocking SMTP ports")
        print("  2. Antivirus/security software blocking connections")
        print("  3. VPN interfering with connections")
        print("  4. ISP blocking SMTP ports")

        print("\nSOLUTIONS: Solutions to try:")
        print("\n  Option 1: Use Personal Network")
        print("  - Disconnect from corporate network")
        print("  - Use personal WiFi or mobile hotspot")
        print("  - Run the script again")

        print("\n  Option 2: Contact IT Department")
        print("  - Ask if SMTP ports (587, 465) are blocked")
        print("  - Request whitelist for smtp.gmail.com")

        print("\n  Option 3: Use Alternative Email Service")
        print("  - Try Outlook/Office365 if you have access")
        print("  - Use SendGrid, Mailgun (free tier available)")

        print("\n  Option 4: Use Personal Device")
        print("  - Run this script from personal laptop/computer")
        print("  - Not connected to corporate network")

        print("\n  Option 5: Use Email Service APIs")
        print("  - Gmail API (requires OAuth2 setup)")
        print("  - SendGrid API (easier, free tier)")
        print("  - I can help you set this up!")
    else:
        print("\n[OK] SMTP connectivity looks good!")
        print("The connection issue might be temporary or related to authentication.")
        print("Make sure your App Password is correct in config.py")

if __name__ == "__main__":
    main()
