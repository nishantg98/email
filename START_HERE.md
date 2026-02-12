# 🚀 DevOps Job Application Email Sender - START HERE

## 📦 What You Got

I've created a complete email automation system for your DevOps Engineer job applications:

### Files Created:

1. **[email_sender.py](email_sender.py)** - Main email sending engine
2. **[config.py](config.py)** - Your configuration file (⚠️ UPDATE THIS!)
3. **[send_applications.py](send_applications.py)** - Run this to send emails
4. **[test_email.py](test_email.py)** - Test script to verify setup
5. **[README.md](README.md)** - Detailed documentation
6. **[SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)** - Step-by-step setup guide
7. **[.gitignore](.gitignore)** - Protects sensitive files

---

## ⚡ Quick Start (3 Steps)

### Step 1: Create Gmail App Password

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Create **App Password** for Mail
4. Copy the 16-character password

### Step 2: Complete config.py

You've already started! Now add:

```python
YOUR_PASSWORD = "xxxx xxxx xxxx xxxx"  # ← Paste App Password here
RESUME_PATH = r"c:\path\to\your\resume.pdf"  # ← Add your resume path
HR_EMAIL_LIST = [  # ← Add actual HR emails
    "hr@company1.com",
    "recruiter@company2.com",
]
```

### Step 3: Test & Send

```bash
# Test first (sends to yourself)
python test_email.py

# If test works, send to all HRs
python send_applications.py
```

---

## 📧 What Email Will Look Like

**Subject:** Application for DevOps Engineer Position - Nishant Gupta

**Body:**
```
Dear Hiring Manager,

I hope this email finds you well.

I am writing to express my strong interest in DevOps Engineer
opportunities within your organization...

Key Highlights:
• Cloud platforms (AWS, Azure, GCP)
• Containerization (Docker, Kubernetes)
• CI/CD tools (Jenkins, GitLab CI, GitHub Actions)
• Infrastructure as Code (Terraform, Ansible)
• Monitoring (Prometheus, Grafana, ELK Stack)
• Scripting (Python, Bash, PowerShell)

[Resume attached as PDF]

Thank you for considering my application.

Best regards,
Nishant Gupta
nishantg2798@gmail.com
+91-8510094400
```

---

## ⚠️ What You MUST Do Before Running

- [ ] Create Gmail App Password (NOT your regular password!)
- [ ] Update `YOUR_PASSWORD` in config.py
- [ ] Update `RESUME_PATH` with path to your resume PDF
- [ ] Update `HR_EMAIL_LIST` with actual HR emails
- [ ] Run `python test_email.py` to test
- [ ] Only then run `python send_applications.py`

---

## 🎯 Your Current Progress

✅ YOUR_NAME = "Nishant Gupta"
✅ YOUR_EMAIL = "nishantg2798@gmail.com"
✅ YOUR_PHONE = "+91-8510094400"
❌ YOUR_PASSWORD = Need App Password
❌ RESUME_PATH = Need to set this
❌ HR_EMAIL_LIST = Need to add HR emails

---

## 📚 Need Help?

- **Full documentation**: See [README.md](README.md)
- **Setup checklist**: See [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- **Having issues?**: Check the Troubleshooting section in README.md

---

## 🔒 Security Reminder

- **NEVER** use your regular Gmail password → Use App Password only
- **NEVER** commit config.py to GitHub (it contains your password)
- Keep your resume and credentials secure

---

## 💡 Pro Tips

1. **Test first**: Always run `test_email.py` before sending to HRs
2. **Start small**: Begin with 5-10 HRs, not 50+
3. **Timing matters**: Send Tuesday-Thursday, 9 AM - 4 PM for best response
4. **Personalize**: If you know HR's name, update the code
5. **Track responses**: Keep a spreadsheet of who you contacted

---

## 🎬 Next Steps

1. Create App Password → Update config.py
2. Add your resume path → Update config.py
3. Add HR emails → Update config.py
4. Test: `python test_email.py`
5. Send: `python send_applications.py`

---

## ✨ Good Luck with Your Job Search! 🚀

You're all set to send professional DevOps Engineer applications at scale.
Focus on quality companies where you'd actually want to work!

**Questions?** Check the README.md for detailed answers.
