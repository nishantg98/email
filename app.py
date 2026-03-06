"""
Email Sender Web Application
A beautiful web interface to send job application emails
"""
from flask import Flask, render_template, request, jsonify
from email_sender_v2 import JobApplicationEmailer
import config
import os
import re
import tempfile

app = Flask(__name__)


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


@app.route('/send', methods=['POST'])
def send_email():
    """Handle email sending with optional resume upload and custom cover letter"""
    recipient_email = request.form.get('email', '').strip()
    custom_cover_letter = request.form.get('cover_letter', '').strip()
    uploaded_resume = request.files.get('resume')

    # Validate email
    if not recipient_email:
        return jsonify({'success': False, 'message': 'Please enter an email address.'}), 400

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, recipient_email):
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400

    # Determine which resume to use
    resume_path = config.RESUME_PATH
    temp_resume_path = None

    if uploaded_resume and uploaded_resume.filename:
        # Save uploaded resume to a temp file
        ext = os.path.splitext(uploaded_resume.filename)[1]
        temp_fd, temp_resume_path = tempfile.mkstemp(suffix=ext)
        os.close(temp_fd)
        uploaded_resume.save(temp_resume_path)
        resume_path = temp_resume_path

    # Check resume exists
    if not os.path.exists(resume_path):
        return jsonify({'success': False, 'message': 'Resume file not found. Please upload one or check config.py.'}), 500

    # Create emailer
    emailer = JobApplicationEmailer(
        sender_email=config.YOUR_EMAIL,
        sender_password=config.YOUR_PASSWORD,
        sender_name=config.YOUR_NAME,
        sender_phone=config.YOUR_PHONE,
        sender_linkedin=config.YOUR_LINKEDIN,
        sender_website=config.YOUR_WEBSITE
    )

    # If custom cover letter provided, override the email body method
    if custom_cover_letter:
        original_create_body = emailer.create_email_body
        emailer.create_email_body = lambda hr_name="Hiring Manager": custom_cover_letter

    try:
        success = emailer.send_email(
            recipient_email=recipient_email,
            resume_path=resume_path,
            smtp_server=config.SMTP_SERVER,
            smtp_port=config.SMTP_PORT,
            timeout=60,
            sendgrid_api_key=config.SENDGRID_API_KEY,
            email_service=config.EMAIL_SERVICE
        )
    finally:
        # Clean up temp file
        if temp_resume_path and os.path.exists(temp_resume_path):
            os.remove(temp_resume_path)

    if success:
        return jsonify({
            'success': True,
            'message': f'Application sent successfully to {recipient_email}!'
        })
    else:
        return jsonify({
            'success': False,
            'message': f'Failed to send email to {recipient_email}. Check server logs for details.'
        }), 500


if __name__ == '__main__':
    import socket
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
