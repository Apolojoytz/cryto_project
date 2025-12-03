import json
import os
import random
import getpass
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
from config import DB_FILE, GMAIL_SENDER, GMAIL_APP_PASSWORD, get_blockchain, save_json

def load_json(path):
    """Helper function to load JSON data"""
    if not os.path.exists(path):
        return {}
    if os.path.getsize(path) == 0:
        return {}
    try:
        return json.load(open(path, "r"))
    except:
        return {}

def send_otp_email(to_email, otp):
    """Send OTP verification email"""
    subject = "Your OTP Verification Code"
    body = f"Your OTP Code is: {otp}\n\nThis code will expire in 10 minutes."
    
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
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def register():
    """Handle new user registration with blockchain"""
    print("\n" + "="*40)
    print("REGISTRATION")
    print("="*40)
    
    db = load_json(DB_FILE)
    blockchain = get_blockchain()

    gmail = input("Enter Gmail: ").strip().lower()
    
    if gmail in db:
        print("❌ This Gmail is already registered.")
        return None

    username = input("Username: ").strip()
    
    # Check if username already exists
    for email, data in db.items():
        if data["username"].lower() == username.lower():
            print("❌ Username already taken. Please choose another.")
            return None

    password = getpass.getpass("Password: ")
    
    if len(password) < 6:
        print("❌ Password must be at least 6 characters long.")
        return None
    
    confirm = getpass.getpass("Confirm Password: ")

    if password != confirm:
        print("❌ Passwords do not match!")
        return None

    # Generate and send OTP
    otp = str(random.randint(100000, 999999))
    print("\n⏳ Sending OTP to your email (check SPAM folder)...")

    if not send_otp_email(gmail, otp):
        print("❌ Failed to send OTP. Registration cancelled.")
        return None

    # Verify OTP
    print("\n" + "-"*40)
    user_otp = input("Enter the 6-digit OTP sent to your email: ").strip()

    if user_otp != otp:
        print("❌ Incorrect OTP! Registration failed.")
        return None

    # Save user data to regular database
    db[gmail] = {
        "username": username,
        "password": password,
        "verified": True,
        "voting_verified": False,
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": f"USER_{random.randint(10000, 99999)}"
    }

    save_json(DB_FILE, db)
    
    # Record registration on blockchain
    registration_data = {
        "email": gmail,
        "username": username,
        "user_id": db[gmail]["user_id"],
        "action": "user_registration",
        "timestamp": datetime.now().isoformat()
    }
    
    blockchain.add_transaction("registration", registration_data)
    
    print("\n✅ Registration successful!")
    print("   📗 Transaction recorded on blockchain")
    print("   👤 You can now login.")
    return gmail