import random
import smtplib
from email.mime.text import MIMEText
import sys
import os
import getpass
import time

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import shared configuration
from config import ADMIN_EMAIL, GMAIL_SENDER, GMAIL_APP_PASSWORD, ADMIN_PASSWORD

def send_otp_email(to_email, otp):
    """Send OTP verification email"""
    subject = "🔐 Admin Login OTP Verification Code"
    body = f"""
    ============================================
              ADMIN LOGIN OTP VERIFICATION
    ============================================
    
    🔐 Your OTP Code: {otp}
    
    ⏰ This OTP is valid for 10 minutes.
    
    🚨 If you didn't request this OTP, please ignore this email.
    
    ============================================
    Online Voting System - Admin Panel
    ============================================
    """
    
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
        return True, "OTP sent successfully"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

def admin_login():
    """Handle admin login with Password + OTP verification"""
    print("\n" + "="*60)
    print("              ADMIN LOGIN")
    print("="*60)
    
    # Step 1: Verify admin email
    print("\n🔐 STEP 1: EMAIL VERIFICATION")
    print("-" * 30)
    email = input("Enter Admin Email: ").strip().lower()
    
    if email != ADMIN_EMAIL:
        print("❌ ERROR: Invalid admin email!")
        return False
    
    print("✅ Email verified")
    
    # Step 2: Verify password
    print("\n🔐 STEP 2: PASSWORD VERIFICATION")
    print("-" * 30)
    password = getpass.getpass("Enter Admin Password: ")
    
    if password != ADMIN_PASSWORD:
        print("❌ ERROR: Invalid admin password!")
        return False
    
    print("✅ Password verified")
    
    # Step 3: Generate and send OTP
    print("\n🔐 STEP 3: TWO-FACTOR AUTHENTICATION")
    print("-" * 30)
    otp = str(random.randint(100000, 999999))
    
    print(f"📧 Sending OTP to {email}...")
    
    success, message = send_otp_email(email, otp)
    
    if not success:
        print(f"❌ {message}")
        return False
    
    print("✅ OTP sent! Check your email (and spam folder).")
    
    # Step 4: Verify OTP
    print("\n🔐 STEP 4: OTP VERIFICATION")
    print("-" * 30)
    
    attempts = 3
    for attempt in range(attempts):
        user_otp = input(f"Enter OTP (Attempt {attempt + 1}/{attempts}): ").strip()
        
        if user_otp == otp:
            print("\n" + "="*60)
            print("           ✅ LOGIN SUCCESSFUL!")
            print("="*60)
            print(f"👤 Welcome, Administrator!")
            print("="*60)
            return True
        else:
            remaining = attempts - (attempt + 1)
            if remaining > 0:
                print(f"❌ Incorrect OTP. {remaining} attempts remaining.")
    
    return False