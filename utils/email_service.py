# voting_system/utils/email_service.py
from email.mime.text import MIMEText
import smtplib
from config import GMAIL_SENDER, GMAIL_APP_PASSWORD

def send_otp_email(to_email, otp, purpose="verification"):
    """Send OTP verification email"""
    if purpose == "login":
        subject = "Login OTP Code - Voting System"
        body = f"""Your Login OTP Code is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Voting System Team"""
    elif purpose == "registration":
        subject = "Registration OTP Code - Voting System"
        body = f"""Your Registration OTP Code is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Voting System Team"""
    elif purpose == "admin_login":
        subject = "Admin Login OTP Code - Voting System"
        body = f"""Your Admin Login OTP Code is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please contact system administrator.

Best regards,
Voting System Team"""
    else:
        subject = "OTP Verification Code - Voting System"
        body = f"""Your OTP Code is: {otp}

This code will expire in 10 minutes.

Best regards,
Voting System Team"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_SENDER
    msg["To"] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_SENDER, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_SENDER, to_email, msg.as_string())
        server.quit()
        print(f"📧 OTP sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False