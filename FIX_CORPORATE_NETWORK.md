# SOLUTION: Corporate Network Blocking SMTP

## Problem
Your UKG corporate network firewall is blocking SMTP connections. The connection is reset during TLS/SSL handshake.

Error: `[WinError 10054] An existing connection was forcibly closed by the remote host`

---

## Solution 1: Use Personal Network (Easiest - 1 minute)

### Steps:
1. **Disconnect from corporate WiFi/network**
2. **Connect to**:
   - Your home WiFi, OR
   - Personal mobile hotspot, OR
   - Any non-corporate network
3. **Run**: `python quick_test.py`
4. **If successful, run**: `python send_applications.py`

**Pros**: Works immediately, no code changes
**Cons**: Must be on personal network to send emails

---

## Solution 2: Use SendGrid API (Works on Corporate Network - 10 minutes setup)

SendGrid uses HTTPS (port 443) instead of SMTP, so corporate firewalls don't block it.

### Quick Setup:

#### 1. Install SendGrid
```bash
pip install sendgrid
```

#### 2. Sign Up (Free)
- Go to: https://sendgrid.com/pricing/
- Click "Start with Free" (100 emails/day)
- Create account

#### 3. Verify Your Email
- Settings > Sender Authentication
- Verify Single Sender
- Use: nishantg2798@gmail.com

#### 4. Create API Key
- Settings > API Keys
- Create API Key: "Job Application"
- **COPY THE KEY** (starts with `SG.`)

#### 5. Update config.py
Add this line:
```python
SENDGRID_API_KEY = "SG.paste_your_key_here"
```

#### 6. Test It
```bash
python test_sendgrid.py
```

#### 7. Send Applications
```bash
python send_applications_sendgrid.py
```

**Pros**: Works on corporate network, better deliverability, tracking available
**Cons**: 10 minute setup, 100 emails/day limit (plenty for job hunting)

---

## Comparison

| Feature | Personal Network | SendGrid API |
|---------|-----------------|--------------|
| **Setup Time** | 1 minute | 10 minutes |
| **Works on Corporate Network** | ❌ No | ✅ Yes |
| **Daily Limit** | ~500 emails | 100 emails |
| **Cost** | Free | Free |
| **Deliverability** | Good | Excellent |
| **Tracking** | No | Yes |

---

## Recommendation

**For quick testing**: Use Solution 1 (personal network)
**For regular use**: Use Solution 2 (SendGrid) - works anywhere

---

## Files Reference

### Original SMTP Method (blocked on corporate network):
- [quick_test.py](quick_test.py) - Test SMTP email
- [send_applications.py](send_applications.py) - Send via SMTP

### SendGrid Method (works on corporate network):
- [test_sendgrid.py](test_sendgrid.py) - Test SendGrid email
- [send_applications_sendgrid.py](send_applications_sendgrid.py) - Send via SendGrid
- [SENDGRID_SETUP.md](SENDGRID_SETUP.md) - Detailed setup guide

---

## Need Help?

**SMTP Issues**: See [troubleshoot_network.py](troubleshoot_network.py)
**SendGrid Setup**: See [SENDGRID_SETUP.md](SENDGRID_SETUP.md)
**General Help**: See [README.md](README.md)
