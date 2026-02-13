# 📋 Quick Setup Checklist

Follow these steps to get your job application email sender up and running!

## ✅ Step-by-Step Setup

### 1. ☑️ Create Gmail App Password

- [ ] Go to [Google Account Security](https://myaccount.google.com/security)
- [ ] Enable **2-Step Verification** (if not already enabled)
- [ ] Create **App Password** for Mail
- [ ] Copy the 16-character password (format: xxxx xxxx xxxx xxxx)

### 2. ☑️ Prepare Your Resume

- [ ] Save your resume as a PDF file
- [ ] Note the full file path (e.g., `c:\Users\nishant.gupta\Documents\Resume.pdf`)
- [ ] Make sure the resume is up-to-date and professional

### 3. ☑️ Update config.py

Open `config.py` and update:

- [ ] `YOUR_NAME` = "Your Full Name"
- [ ] `YOUR_EMAIL` = "your.email@gmail.com"
- [ ] `YOUR_PASSWORD` = "xxxx xxxx xxxx xxxx" (App Password from Step 1)
- [ ] `RESUME_PATH` = r"c:\full\path\to\your\resume.pdf"
- [ ] `HR_EMAIL_LIST` = Add actual HR email addresses

Example:
```python
YOUR_NAME = "Nishant Gupta"
YOUR_EMAIL = "nishxxx@gmail.com"
YOUR_PASSWORD = "abcd efgh ijkl mnop"
RESUME_PATH = r"c:\Users\nishant.gupta\Documents\Nishant_Gupta_Resume.pdf"
HR_EMAIL_LIST = [
    "hr@teccompany.com",
    "recruiter@startup.io",
    "jobs@corporation.com",
]
```

### 4. ☑️ Customize Email Template (Optional)

If you want to personalize the email:

- [ ] Open `email_sender.py`
- [ ] Find the `create_email_body()` function
- [ ] Modify the email text to match your experience
- [ ] Add your phone number, LinkedIn, GitHub, etc.

### 5. ☑️ Test Your Setup

Before sending to real HR contacts:

- [ ] Run test: `python test_email.py`
- [ ] Check your inbox for the test email
- [ ] Verify resume attachment opens correctly
- [ ] Check email formatting looks professional

### 6. ☑️ Prepare HR Email List

Collect HR email addresses:

- [ ] Search company careers pages
- [ ] Check LinkedIn for HR contacts
- [ ] Look for recruiter emails in job postings
- [ ] Verify email addresses are correct
- [ ] Add them to `HR_EMAIL_LIST` in `config.py`

### 7. ☑️ Send Your Applications!

- [ ] Double-check all configuration in `config.py`
- [ ] Run: `python send_applications.py`
- [ ] Review the list of recipients shown
- [ ] Type 'yes' to confirm and send
- [ ] Monitor the progress

---

## 🚨 Common Issues

### Issue: "Authentication failed"
**Solution:**
- You must use App Password, NOT your regular Gmail password
- Make sure 2-Step Verification is enabled
- Re-generate App Password if needed

### Issue: "Resume file not found"
**Solution:**
- Use full absolute path: `r"c:\Users\...\resume.pdf"`
- Use the `r` prefix for raw strings (handles backslashes)
- Verify file exists at that location

### Issue: Emails going to spam
**Solution:**
- Use the delay setting (5-10 seconds between emails)
- Don't send too many at once (start with 5-10)
- Make sure your email account is established (not brand new)

---

## 📝 Quick Reference Commands

### Test email setup:
```bash
python test_email.py
```

### Send applications:
```bash
python send_applications.py
```

### Check Python version:
```bash
python --version
```

---

## 🎯 Pro Tips

1. **Start Small**: Test with 2-3 emails first before sending to many
2. **Best Timing**: Send emails Tuesday-Thursday, 9 AM - 4 PM
3. **Personalize**: If you know the HR person's name, update it in the code
4. **Follow Up**: Keep track of who you've emailed for follow-ups
5. **Track Results**: Create a spreadsheet to track responses

---

## ✨ You're Ready!

Once all checkboxes above are complete, you're ready to send professional job applications at scale. Good luck with your DevOps Engineer job search! 🚀

**Remember:** Quality over quantity. Personalized applications to relevant positions work better than mass emailing.
