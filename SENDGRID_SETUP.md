# 🚀 SendGrid Setup for Render Deployment

## Why SendGrid?

**SendGrid solves the Gmail SMTP blocking issue on Render** and other cloud platforms:

✅ Works reliably on Render, Heroku, AWS, and all cloud platforms  
✅ Free tier: 100 emails/day  
✅ Professional email service  
✅ No connection timeouts  
✅ Better deliverability  

## Step 1: Create SendGrid Account

1. **Go to [SendGrid](https://sendgrid.com/)**
2. **Click "Sign Up"**
3. **Create a free account** (no credit card required)
4. **Verify your email address**

## Step 2: Create SendGrid API Key

1. **After sign up, go to Dashboard**
2. **Left sidebar → Settings → API Keys**
3. **Click "Create API Key"**
4. **Name it**: `email-sender` (or any name)
5. **Permissions**: Select "Full Access" (or at minimum "Mail Send")
6. **Click "Create & View"**
7. **Copy the API Key** (starts with `SG.`)
   - ⚠️ **SAVE THIS IMMEDIATELY** - You can only see it once!

## Step 3: Configure Sender Email (if needed)

1. **If using a custom domain email**:
   - Go to **Settings → Sender Authentication**
   - Verify your domain/email address
   - Follow their instructions

2. **If using free tier**: You can use any email, but replies won't reach you unless you properly authenticate.

## Step 4: Update .env (Local Testing)

Update your `.env` file:
```
SENDGRID_API_KEY=SG.your_actual_api_key_here
EMAIL_SERVICE=sendgrid
YOUR_PASSWORD=
```

## Step 5: Deploy to Render

1. **Go to Render Dashboard → Your Web Service**
2. **Go to Environment tab**
3. **Add these variables**:
   ```
   SENDGRID_API_KEY = SG.your_actual_api_key_here
   EMAIL_SERVICE = sendgrid
   ```
4. **Save and redeploy**

## Testing

### Local Testing
```bash
# With .env configured, test locally:
python -c "from email_sender_v2 import JobApplicationEmailer; print('SendGrid ready!')"
```

### Test via Web App
1. **Go to your Render app URL**
2. **Enter your test email**
3. **Upload resume (or use default)**
4. **Send email**
5. **Check your inbox**

## Troubleshooting

### "sendgrid API error"
- Copy your API key exactly (including `SG.` prefix)
- No extra spaces
- Make sure variable name is exactly `SENDGRID_API_KEY`

### "Email not received"
- Check spam folder
- Verify sender email in SendGrid dashboard
- Try with a different recipient email first

### "Module 'sendgrid' not found"
- Make sure `requirements.txt` has `sendgrid==6.11.0`
- Redeploy on Render

## FAQ

**Q: Can I use both Gmail and SendGrid?**  
A: Yes! The app auto-switches based on which API key is configured.

**Q: Is SendGrid free?**  
A: Yes, free tier: 100 emails/day, forever free.

**Q: What if I exceed 100 emails/day?**  
A: You'd need to upgrade to a paid plan, but that's unlikely for job applications.

**Q: Can I use my own domain email?**  
A: Yes, verify it in SendGrid dashboard (Settings → Sender Authentication).

**Q: Is SendGrid secure?**  
A: Yes, industry standard email service used by major companies.

---

## Quick Copy-Paste Checklist

- [ ] SendGrid account created
- [ ] API Key generated and saved
- [ ] API Key added to `.env` (local testing)
- [ ] API Key added to Render environment variables
- [ ] `EMAIL_SERVICE=sendgrid` set in Render
- [ ] App redeployed on Render
- [ ] Test email sent successfully

---

**Once SendGrid is set up, your Render app will send emails reliably! 🎉**
