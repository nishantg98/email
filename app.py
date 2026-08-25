"""
Email Sender Web Application
A beautiful web interface to send job application emails
"""
from flask import Flask, render_template, request, jsonify
from email_sender_v2 import JobApplicationEmailer, extract_name_from_email
import config
import os
import re
import tempfile
import time
import csv
from datetime import datetime

app = Flask(__name__)

SENT_LOG_PATH = os.path.join(os.path.dirname(__file__), 'sent_applications.csv')
SENT_LOG_FIELDS = ['timestamp', 'email', 'hr_name', 'company', 'success', 'message']


def _log_sent_email(email, success, message, hr_name='', company=''):
    """Append a record of every send attempt to a local CSV file for later review."""
    file_exists = os.path.exists(SENT_LOG_PATH)
    with open(SENT_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=SENT_LOG_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'timestamp': datetime.now().isoformat(timespec='seconds'),
            'email': email,
            'hr_name': hr_name,
            'company': company,
            'success': success,
            'message': message,
        })


def get_default_cover_letter():
    """Generate the default cover letter text from the emailer"""
    emailer = JobApplicationEmailer(
        sender_email=config.YOUR_EMAIL,
        sender_password=config.YOUR_PASSWORD,
        sender_name=config.YOUR_NAME,
        sender_phone=config.YOUR_PHONE,
        sender_linkedin=config.YOUR_LINKEDIN,
        sender_website=config.YOUR_WEBSITE
    )
    return emailer.create_email_body("Hiring Manager")


@app.route('/')
def index():
    """Serve the main page"""
    default_cover_letter = get_default_cover_letter()
    return render_template(
        'index.html',
        sender_name=config.YOUR_NAME,
        sender_email=config.YOUR_EMAIL,
        default_cover_letter=default_cover_letter
    )


EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
MAX_BULK_RECIPIENTS = 25


def _resolve_resume_path(uploaded_resume):
    """Save an uploaded resume to a temp file, or fall back to the configured default.
    Returns (resume_path, temp_resume_path_or_None)."""
    if uploaded_resume and uploaded_resume.filename:
        ext = os.path.splitext(uploaded_resume.filename)[1]
        temp_fd, temp_resume_path = tempfile.mkstemp(suffix=ext)
        os.close(temp_fd)
        uploaded_resume.save(temp_resume_path)
        return temp_resume_path, temp_resume_path
    return config.RESUME_PATH, None


def _greeting_name(hr_name, company, recipient_email):
    """Priority: explicit HR name > name guessed from the recipient's email > company > generic fallback."""
    if hr_name:
        return hr_name
    guessed = extract_name_from_email(recipient_email)
    if guessed:
        return guessed
    if company:
        return f"the {company} team"
    return "Hiring Manager"


def _build_emailer(custom_cover_letter):
    emailer = JobApplicationEmailer(
        sender_email=config.YOUR_EMAIL,
        sender_password=config.YOUR_PASSWORD,
        sender_name=config.YOUR_NAME,
        sender_phone=config.YOUR_PHONE,
        sender_linkedin=config.YOUR_LINKEDIN,
        sender_website=config.YOUR_WEBSITE
    )
    if custom_cover_letter:
        emailer.create_email_body = lambda hr_name="Hiring Manager", jd_text="", company="": custom_cover_letter
    return emailer


@app.route('/send', methods=['POST'])
def send_email():
    """Handle email sending with optional resume upload and custom cover letter"""
    recipient_email = request.form.get('email', '').strip()
    custom_cover_letter = request.form.get('cover_letter', '').strip()
    hr_name = request.form.get('hr_name', '').strip()
    company = request.form.get('company', '').strip()
    jd_text = request.form.get('jd_text', '').strip()
    uploaded_resume = request.files.get('resume')

    # Validate email
    if not recipient_email:
        return jsonify({'success': False, 'message': 'Please enter an email address.'}), 400

    if not re.match(EMAIL_REGEX, recipient_email):
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400

    resume_path, temp_resume_path = _resolve_resume_path(uploaded_resume)

    if not os.path.exists(resume_path):
        return jsonify({'success': False, 'message': 'Resume file not found. Please upload one or check config.py.'}), 500

    emailer = _build_emailer(custom_cover_letter)

    greeting_name = _greeting_name(hr_name, company, recipient_email)

    try:
        result = emailer.send_email(
            recipient_email=recipient_email,
            resume_path=resume_path,
            hr_name=greeting_name,
            jd_text=jd_text,
            company=company,
            smtp_server=config.SMTP_SERVER,
            smtp_port=config.SMTP_PORT,
            timeout=60
        )
    finally:
        if temp_resume_path and os.path.exists(temp_resume_path):
            os.remove(temp_resume_path)

    _log_sent_email(recipient_email, result.success, result.message, hr_name, company)

    if result.success:
        return jsonify({'success': True, 'message': result.message})
    return jsonify({'success': False, 'message': result.message}), 500


@app.route('/send-bulk', methods=['POST'])
def send_bulk():
    """Send the same application to a list of recipients, one at a time."""
    raw_emails = request.form.get('emails', '')
    custom_cover_letter = request.form.get('cover_letter', '').strip()
    hr_name = request.form.get('hr_name', '').strip()
    company = request.form.get('company', '').strip()
    jd_text = request.form.get('jd_text', '').strip()
    uploaded_resume = request.files.get('resume')

    # Split on commas/newlines, dedupe, validate
    candidates = [e.strip() for e in re.split(r'[,\n]', raw_emails) if e.strip()]
    seen = set()
    recipients = []
    invalid = []
    for email in candidates:
        if email in seen:
            continue
        seen.add(email)
        if re.match(EMAIL_REGEX, email):
            recipients.append(email)
        else:
            invalid.append(email)

    if not recipients:
        return jsonify({'success': False, 'message': 'No valid email addresses were provided.'}), 400

    if len(recipients) > MAX_BULK_RECIPIENTS:
        return jsonify({
            'success': False,
            'message': f'Too many recipients ({len(recipients)}). Limit is {MAX_BULK_RECIPIENTS} per batch to avoid request timeouts.'
        }), 400

    resume_path, temp_resume_path = _resolve_resume_path(uploaded_resume)

    if not os.path.exists(resume_path):
        return jsonify({'success': False, 'message': 'Resume file not found. Please upload one or check config.py.'}), 500

    emailer = _build_emailer(custom_cover_letter)

    results = []
    try:
        for i, recipient_email in enumerate(recipients):
            greeting_name = _greeting_name(hr_name, company, recipient_email)
            result = emailer.send_email(
                recipient_email=recipient_email,
                resume_path=resume_path,
                hr_name=greeting_name,
                jd_text=jd_text,
                company=company,
                smtp_server=config.SMTP_SERVER,
                smtp_port=config.SMTP_PORT,
                timeout=60
            )
            results.append({'email': recipient_email, 'success': result.success, 'message': result.message})
            _log_sent_email(recipient_email, result.success, result.message, hr_name, company)
            if i < len(recipients) - 1:
                time.sleep(config.DELAY_BETWEEN_EMAILS)
    finally:
        if temp_resume_path and os.path.exists(temp_resume_path):
            os.remove(temp_resume_path)

    for email in invalid:
        results.append({'email': email, 'success': False, 'message': 'Invalid email address, skipped.'})
        _log_sent_email(email, False, 'Invalid email address, skipped.', hr_name, company)

    sent = sum(1 for r in results if r['success'])
    return jsonify({
        'success': sent > 0,
        'message': f'Sent {sent}/{len(recipients)} emails successfully.',
        'results': results
    })


if __name__ == '__main__':
    import socket
    import sys

    # Windows consoles often default to cp1252, which can't encode the emoji
    # below and crashes the print before the server even starts.
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    # Get local IP for network access
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()

    print("\n" + "=" * 60)
    print("  📧 Email Sender Web Application")
    print("=" * 60)
    print(f"  Sender: {config.YOUR_NAME} <{config.YOUR_EMAIL}>")
    print(f"  Resume: {config.RESUME_PATH}")
    print(f"\n  Local:   http://localhost:5000")
    print(f"  Network: http://{local_ip}:5000")
    print("=" * 60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
