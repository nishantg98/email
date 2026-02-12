# SendGrid Setup Guide - Bypass Corporate Firewall

## Why SendGrid?
Your corporate network (UKG) is blocking SMTP ports. SendGrid uses HTTPS (port 443) instead, which corporate firewalls allow.

## Setup Steps (5 minutes)

### Step 1: Sign Up for SendGrid
1. Go to https://sendgrid.com/pricing/
2. Click "Start with Free" (100 emails/day forever free)
3. Create account with your email

### Step 2: Verify Your Email
1. After signup, go to Settings > Sender Authentication
2. Click "Verify a Single Sender"
3. Fill in your details:
   - From Name: Nishant Gupta
   - From Email: nishantg2798@gmail.com
   - Reply To: nishantg2798@gmail.com
4. Check your email and click verification link

### Step 3: Create API Key
1. Go to Settings > API Keys
2. Click "Create API Key"
3. Name it: "Job Application Sender"
4. Choose "Full Access" (or just "Mail Send" permission)
5. Click "Create & View"
6. **COPY THE API KEY** (you can only see it once!)
   - It looks like: `SG.xxxxxxxxxxxxxxxxxxxxx`

### Step 4: Install SendGrid Package
Open Command Prompt and run:
```bash
pip install sendgrid
```

### Step 5: Update config.py
Add this line to your [config.py](config.py):
```python
# SendGrid Configuration (for corporate networks)
SENDGRID_API_KEY = "SG.paste_your_api_key_here"
```

### Step 6: Test It
```bash
python test_sendgrid.py
```

If successful, emails will be sent via HTTPS (bypasses corporate firewall)!

## Free Tier Limits
- 100 emails per day
- Forever free
- Perfect for job applications

## Benefits Over SMTP
- ✅ Works on corporate networks
- ✅ Better deliverability (less likely to go to spam)
- ✅ Email tracking available
- ✅ No firewall issues
- ✅ Faster sending

## Need Help?
If you see errors:
1. Make sure API key is copied correctly
2. Make sure sender email is verified
3. Check you installed sendgrid: `pip list | findstr sendgrid`
